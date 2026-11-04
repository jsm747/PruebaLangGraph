# Incident register — template

**Filled by:** Platform Operator (mechanics), Process Owner (process), anyone through the process door. **Read by:** periodic review, Framework review, Risk & Control. **Lifecycle:** append-only.

---

# Incidents of <instance>

| Id | Date | Detected by | Class | What happened | Effect on people / outside | Suspended? | Reported to | Root cause | Countermeasure | Closed |
|---|---|---|---|---|---|---|---|---|---|---|

## Classes
mechanics (stall, dead sessions, orchestrator outage) · wrong decision with effect · data (classification breach, personal data where it should not be) · instrument (calibration drift beyond threshold) · human gate (missed SLA at the top of a ladder, approval without authority) · security (manipulated input acted upon)

## Rules
- An incident with effect on people or outside the system suspends the affected scope (queue pause) until the Process Owner lifts it.
- Reporting duties beyond the instance (provider, authority) are the Platform Operator's, as the instance's legal function has configured.
- Every incident ends in a countermeasure recorded in the process map's failure classes, or in a framework proposal.
