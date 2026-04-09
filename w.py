



from datetime import datetime
from collections import defaultdict


DEDUP_WIN_SEC = 600


DEFAULT_AI = {"intent": "LOW", "nextAction": "NONE", "confidence": 0.0}




def parse_ts(ts):
   if isinstance(ts, datetime):
       return ts
   return datetime.fromisoformat(ts.replace("Z", "+00:00"))




def safe_ai(call_ai, text):
   try:
       out = call_ai(text)
       if (
           isinstance(out, dict)
           and out.get("intent") in {"LOW", "MEDIUM", "HIGH"}
           and out.get("nextAction") in {"EMAIL", "CALL", "DEMO", "NONE"}
           and 0 <= float(out.get("confidence", -1)) <= 1
       ):
           return out
   except Exception:
       pass
   return DEFAULT_AI.copy()




def process_events(events, call_ai=lambda _: DEFAULT_AI):
   rejected = []
   valid = []


   # 1. validation
   for e in events:
       try:
           for k in ("eventId", "leadId", "eventType", "ts"):
               if k not in e:
                   raise ValueError("missing field")
           e["ts"] = parse_ts(e["ts"])
           valid.append(e)
       except Exception:
           rejected.append({"eventId": e.get("eventId"), "reason": "invalid event"})


   # 2. dedup (keep earliest)
   valid.sort(key=lambda x: x["ts"])
   last_seen = {}
   deduped = set()
   unique = []


   for e in valid:
       key = (e["leadId"], e["eventType"])
       if key in last_seen and (e["ts"] - last_seen[key]).seconds <= DEDUP_WIN_SEC:
           deduped.add(e["eventId"])
           continue
       last_seen[key] = e["ts"]
       unique.append(e)


   # 3. actions
   actions = []
   for e in unique:
       ai = safe_ai(call_ai, e.get("text", "")) if e.get("text") else DEFAULT_AI


       utm = (e.get("utmCampaign") or "").lower()


       if e["eventType"] == "form_submit" and "webinar" in utm:
           action = "ADD_TO_AUDIENCE:webinar_leads"
       elif ai["intent"] == "HIGH" and ai["nextAction"] == "DEMO" and ai["confidence"] >= 0.7:
           action = "CREATE_TICKET:sales_demo"
       else:
           action = "NO_ACTION"


       actions.append({"leadId": e["leadId"], "actionType": action})


   # 4. summary
   counts = defaultdict(int)
   for a in actions:
       counts[a["actionType"]] += 1


   return {
       "actions": actions,
       "summary": {
           "processed": len(actions),
           "rejected": len(rejected),
           "deduped": len(deduped),
           "actionsByType": dict(counts),
       },
       "rejected": rejected,
   }


def run_case(title, events, call_ai=None):
       print("\n" + "=" * 80)
       print(title)


       out = process_events(events, call_ai=call_ai or (lambda _: DEFAULT_AI))


       for a in out["actions"]:
           print(a)
       print(out["summary"])


       if out["rejected"]:
           print("rejected:", out["rejected"])


if __name__ == "__main__":
  
   run_case(
       "Case 1: webinar + dedup (expect: 2 actions, deduped=1, webinar audience x2)",
       [
           {"eventId": "e1", "leadId": "L1", "eventType": "form_submit", "ts": "2026-02-04T10:00:00", "utmCampaign": "webinar"},
           {"eventId": "e2", "leadId": "L1", "eventType": "form_submit", "ts": "2026-02-04T10:05:00", "utmCampaign": "webinar"},  # deduped
           {"eventId": "e3", "leadId": "L1", "eventType": "form_submit", "ts": "2026-02-04T10:11:00", "utmCampaign": "webinar"},
       ],
   )


   run_case(
       "Case 2: same lead, different eventType (expect: 2 actions, deduped=0)",
       [
           {"eventId": "e4", "leadId": "L1", "eventType": "click", "ts": "2026-02-04T10:00:00"},
           {"eventId": "e5", "leadId": "L1", "eventType": "view", "ts": "2026-02-04T10:05:00"},
       ],
   )


   run_case(
       "Case 3: rejected events (missing fields + invalid ts) (expect: rejected=2, processed=0)",
       [
           {"eventId": "bad1"},  # missing required fields
           {"eventId": "bad2", "leadId": "L1", "eventType": "x", "ts": "not-a-time"},  # invalid ts
       ],
   )


   def hi_demo_ai(_):
       return {"intent": "HIGH", "nextAction": "DEMO", "confidence": 0.9}


   run_case(
       "Case 4: AI high-intent demo (expect: CREATE_TICKET:sales_demo)",
       [
           {"eventId": "e6", "leadId": "L2", "eventType": "x", "ts": "2026-02-04T10:00:00", "text": "please schedule demo"},
       ],
       call_ai=hi_demo_ai,
   )


   run_case(
       "Case 5: webinar overrides AI (expect: ADD_TO_AUDIENCE:webinar_leads)",
       [
           {
               "eventId": "e7",
               "leadId": "L3",
               "eventType": "form_submit",
               "ts": "2026-02-04T10:00:00",
               "utmCampaign": "Big_Webinar_2026",
               "text": "demo please",
           }
       ],
       call_ai=hi_demo_ai,
   )


   def bad_ai(_):
       return {"intent": "???", "nextAction": "DEMO", "confidence": 2.0}


   run_case(
       "Case 6: malformed AI output -> fallback (expect: NO_ACTION)",
       [
           {"eventId": "e8", "leadId": "L4", "eventType": "x", "ts": "2026-02-04T10:00:00", "text": "something"},
       ],
       call_ai=bad_ai,
   )


   run_case(
       "Case 7: mixed leads (expect: webinar add for L1, NO_ACTION for L2 unless AI triggers)",
       [
           {"eventId": "e9", "leadId": "L1", "eventType": "form_submit", "ts": "2026-02-04T09:00:00", "utmCampaign": "webinar"},
           {"eventId": "e10", "leadId": "L2", "eventType": "x", "ts": "2026-02-04T09:01:00"},
           {"eventId": "e11", "leadId": "L3", "eventType": "x", "ts": "2026-02-04T09:02:00", "text": "need demo"},
       ],
       call_ai=hi_demo_ai,
   )





