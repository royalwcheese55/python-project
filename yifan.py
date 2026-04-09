from collections import defaultdict
from datetime import datetime, timedelta
import json

def callAI(text):
    try:
        # simulate AI call; real one would be a REST API
        return json.loads(text) if isinstance(text, str) and text.startswith("{") else {
            "intent": "LOW", "nextAction": "NONE", "confidence": 0.0
        }
    except:
        return {"intent": "LOW", "nextAction": "NONE", "confidence": 0.0}

def process_events(events):
    valid, rejected, dedup_map = [], [], defaultdict(list)
    deduped = set()
    enriched_events = []
    actions = []

    for e in events:
        if not all(k in e for k in ("eventId", "leadId", "eventType", "ts")):
            rejected.append({"eventId": e.get("eventId", "UNKNOWN"), "reason": "missing required field"})
            continue
        valid.append(e)

    # Deduplication
    valid.sort(key=lambda x: x["ts"])
    for e in valid:
        key = (e["leadId"], e["eventType"])
        ts = datetime.fromisoformat(e["ts"])
        dedup_map[key].append((ts, e))

    unique_events = []
    for key, events in dedup_map.items():
        window = []
        for ts, e in events:
            if not window:
                window = [(ts, e)]
            else:
                last_ts = window[-1][0]
                if (ts - last_ts).total_seconds() <= 600:
                    deduped.add(e["eventId"])
                else:
                    window.append((ts, e))
        unique_events.extend([e for _, e in window])

    # Enrichment
    for e in unique_events:
        if "text" in e and e["text"]:
            enrichment = callAI(e["text"])
        else:
            enrichment = {"intent": "LOW", "nextAction": "NONE", "confidence": 0.0}
        e["enrichment"] = enrichment

        # Decide action
        if e["eventType"] == "form_submit" and "utmCampaign" in e and "webinar" in e["utmCampaign"].lower():
            actions.append({
                "leadId": e["leadId"],
                "actionType": "ADD_TO_AUDIENCE:webinar_leads",
                "reason": "form_submit + webinar"
            })
        elif (enrichment.get("intent") == "HIGH" and enrichment.get("nextAction") == "DEMO" and enrichment.get("confidence", 0) >= 0.7):
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
    summary = {
        "rejected": len(rejected),
        "deduped": len(deduped),
        "actionsByType": defaultdict(int)
    }
    for a in actions:
        summary["actionsByType"][a["actionType"]] += 1

    return {
        "actions": actions,
        "summary": summary,
        "rejected": rejected
    }

events = [
    {"eventId": "e0", "leadId": "L0", "eventType": "form_submit"},

    {"eventId": "e1", "leadId": "L1", "eventType": "form_submit",
     "ts": "2024-01-01T10:00:00", "utmCampaign": "Spring_Webinar", "text": "signed up"},

    {"eventId": "e2", "leadId": "L1", "eventType": "form_submit",
     "ts": "2024-01-01T10:05:00", "utmCampaign": "Spring_Webinar", "text": "follow up"},

    {"eventId": "e3", "leadId": "L2", "eventType": "message",
     "ts": "2024-01-01T11:00:00", "text": '{"intent":"HIGH","nextAction":"DEMO","confidence":0.9}'},

    {"eventId": "e4", "leadId": "L3", "eventType": "message",
     "ts": "2024-01-01T12:00:00", "text": "hello"},
]

result = process_events(events)

print("\n- ACTIONS -")
print(json.dumps(result["actions"], indent=2))

print("\n- REJECTED -")
print(json.dumps(result["rejected"], indent=2))

print("\n- SUMMARY -")
print(json.dumps(result["summary"], indent=2, default=dict))

