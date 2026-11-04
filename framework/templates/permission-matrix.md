# Permission matrix — template

**Filled by:** Builder with the Process Owner; enforced by the Platform Operator. **Read by:** everyone; the platform's access configuration is derived from it. **Lifecycle:** any loosening is a ruling, dated and scoped; tightening needs none.

---

# Permission matrix of <instance>

Data classes from the information map: <list them>. External effects: <list the kinds this instance can produce: send, publish, pay, notify, write to <system>>.

| Role | Reads (data classes) | Writes state (facts) | Writes knowledge (layer / state) | Triggers | External effects |
|---|---|---|---|---|---|
| Architect / Builder | | | instance layer | arm first item after owner's go | none |
| Executor | | proposal, scope declaration, blocked | none | none | none |
| Researcher / Pre-reviewer | | findings | none | none | none |
| Critic | | critique verdict | none | none | none |
| Reviewer | | review verdict | none | none | none |
| Resolver | | decisions, re-dimensioned items | none | re-arm | none |
| Auditor | | audit verdict, ledger | none | correctives | none |
| Process Reviewer | | proposals | learning sections only | none | none |
| Distiller | **raw corpus** (named sources) | draft queue | records and skills in draft | none | none |
| Process Assistant | state, ledger in the person's scope | signals on behalf of the person | none | as the person may | as the person may |
| Process Owner | | rulings, approvals | ratifies drafts → current | arm after ruling | <per scope> |
| Gatekeeper <scope> | packaged decision | approvals | none | none | <kind, scope, threshold> |
| Platform Operator | telemetry, configuration | budgets, tiers, allowlists | none | pause, resume | none |
| Framework Owner / Architect | framework queue | framework rulings | framework layer | none | none |
| Mechanisms | state, deliverables | their own facts | none | next item, relaunch | none |

## Rulings that loosen a default
| Date | Role | Column | From → to | Scope | Signed by | Expires |
|---|---|---|---|---|---|---|

## Invariants (never loosened)
- No agent writes an approval fact.
- No agent changes what supervises it (budgets, allowlists, state machine, checks).
- One writer per knowledge layer.
- The external-effects column is empty for every agent unless a ruling above says otherwise.
- Whoever requested or executed never approves their own work.
