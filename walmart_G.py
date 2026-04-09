from collections import defaultdict
from datetime import datetime
import json

ALLOWED_INTENTS = {"LOW", "MEDIUM", "HIGH"}
ALLOWED_NEXT = {"EMAIL", "CALL", "DEMO", "NONE"}

DEFAULT_ENRICHMENT = {"intent": "LOW", "nextAction": "NONE", "confidence": 0.0}

def _parse_ts(ts: str):
    if not isinstance(ts, str):
        raise ValueError("ts must be a string")
    ts2 = ts.replace("Z", "+00:00")
    return datetime.fromisoformat(ts2)

def _validate_enrichment(obj):
    if not isinstance(obj, dict):
        return DEFAULT_ENRICHMENT

    intent = obj.get("intent")
    next_action = obj.get("nextAction")
    conf = obj.get("confidence")

    if intent not in ALLOWED_INTENTS:
        return DEFAULT_ENRICHMENT
    if next_action not in ALLOWED_NEXT:
        return DEFAULT_ENRICHMENT
    if not isinstance(conf, (int, float)) or conf < 0.0 or conf > 1.0:
        return DEFAULT_ENRICHMENT

    return {"intent": intent, "nextAction": next_action, "confidence": float(conf)}

def callAI(text):
    try:
        if isinstance(text, str) and text.strip().startswith("{"):
            return _validate_enrichment(json.loads(text))
        return DEFAULT_ENRICHMENT
    except Exception:
        return DEFAULT_ENRICHMENT

def process_events(events):
    valid, rejected = [], []
    dedup_map = defaultdict(list)
    deduped = set()
    actions = []

    for e in events:
        if not all(k in e for k in ("eventId", "leadId", "eventType", "ts")):
            rejected.append({"eventId": e.get("eventId", "UNKNOWN"), "reason": "missing required field"})
            continue
        try:
            _ = _parse_ts(e["ts"]) 
        except Exception:
            rejected.append({"eventId": e.get("eventId", "UNKNOWN"), "reason": "invalid ts"})
            continue
        valid.append(e)

    # 2) Deduplicate (keep earliest per 10-min window per (leadId,eventType))
    valid.sort(key=lambda x: x["ts"])
    for e in valid:
        key = (e["leadId"], e["eventType"])
        ts = _parse_ts(e["ts"])
        dedup_map[key].append((ts, e))

    unique_events = []
    for key, bucket in dedup_map.items():
        window = []
        for ts, e in bucket:
            if not window:
                window = [(ts, e)]
            else:
                last_kept_ts = window[-1][0]
                if (ts - last_kept_ts).total_seconds() <= 600:
                    deduped.add(e["eventId"])
                else:
                    window.append((ts, e))
        unique_events.extend([e for _, e in window])

    # Optional: keep global ordering
    unique_events.sort(key=lambda x: x["ts"])

    # 3) Enrich + 4) Decide action
    for e in unique_events:
        text = e.get("text")
        enrichment = callAI(text) if isinstance(text, str) and text.strip() else DEFAULT_ENRICHMENT
        e["enrichment"] = enrichment

        utm = e.get("utmCampaign") or ""
        utm = utm if isinstance(utm, str) else ""

        if e["eventType"] == "form_submit" and "webinar" in utm.lower():
            actions.append({
                "leadId": e["leadId"],
                "actionType": "ADD_TO_AUDIENCE:webinar_leads",
                "reason": "form_submit + webinar"
            })
        elif (enrichment["intent"] == "HIGH"
              and enrichment["nextAction"] == "DEMO"
              and enrichment["confidence"] >= 0.7):
            actions.append({
                "leadId": e["leadId"],
                "actionType": "CREATE_TICKET:sales_demo",
                "reason": "high intent demo"
            })
        else:
            actions.append({
                "leadId": e["leadId"],
                "actionType": "NO_ACTION",
                "reason": "no matching rule"
            })

    # Summary
    actions_by_type = defaultdict(int)
    for a in actions:
        actions_by_type[a["actionType"]] += 1

    summary = {
        "processed": len(unique_events),
        "rejected": len(rejected),
        "deduped": len(deduped),
        "actionsByType": dict(actions_by_type),
    }

    return {"actions": actions, "summary": summary, "rejected": rejected}

events = [
    {
        "eventId": "e1",
        "leadId": "L1",
        "eventType": "form_submit",
        "ts": "2024-01-01T10:00:00",
        "utmCampaign": "Spring_Webinar"
    },
    {
        "eventId": "e2",
        "leadId": "L2",
        "eventType": "message",
        "ts": "2024-01-01T11:00:00",
        "text": '{"intent":"HIGH","nextAction":"DEMO","confidence":0.9}'
    },
    {
        "eventId": "e3",
        "leadId": "L3",
        "eventType": "message",
        "ts": "2024-01-01T12:00:00",
        "text": "hello"
    }
]

result = process_events(events)

print("\n ACTIONS ")
print(json.dumps(result["actions"]))

print("\n SUMMARY ")
print(json.dumps(result["summary"]))

