# Review cadence — template

**Filled by:** Builder with the Process Owner. **Read by:** Process Owner, Process Reviewer, Architect, Process Assistant (for reminders). **Lifecycle:** the dates are commitments; a missed review is an incident of the instance.

---

# Periodic review of <instance>

**Cadence:** <every n weeks | after n audits, whichever first>  **Next:** <date>  **Chair:** Process Owner  **Prepares:** Architect  **Attends:** <Risk & Control, Platform Operator as needed>

## Agenda (always in this order)
1. State of the previous queue: what was executed, which falsifiable criteria expired and with what result.
2. Instruments: calibration of classifier, sizing, risk scores; by group.
3. Human series: overrides and reasons, false escalations, rubber stamps, SLA compliance.
4. Economics: (a), (b), (c) against the baseline and the previous period.
5. New proposals, one by one; every one gets a ruling.
6. Framework candidates (axis *framework*): forwarded to the framework queue.
7. Incidents of the period.
8. Next review date confirmed.

## Ruling (one per proposal, written on the proposal)
```
Ruling — <date> — <outcome>
Outcome: approved (position <n>) | merged into <id> | local | owner-action | closed
Scope: what is in, what is out
Moves: (a) | (b) — without worsening (c); series that will show it at the next review
Falsifiable criterion: <what must be true by <date>>
```
No "deferred": a proposal is executed or closed.

## After the review
Approved items run in order without further approval; the queue stops by itself where nothing is ruled.
