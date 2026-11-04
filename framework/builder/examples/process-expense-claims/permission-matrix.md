# Permission matrix — Expense claims (abridged)

Data classes: normative (definition, policy, records) · deliverables (decision records, instructions) · operational records · raw corpus (approver mailbox threads with claimants; HR flags via system) · HR flags (restricted).
External effects: payroll instruction (payment); rejection notice to the employee.

| Role | Reads | Writes state | Writes knowledge | Triggers | External effects |
|---|---|---|---|---|---|
| Executor | case, definition, policy, rate table | proposal, scope | none | none | none |
| Mechanisms | case, receipts, HR flag (yes/no only) | checks, classifier facts, route, closure | none | next step | payroll instruction **only under SA-1 or a per-case approval**, traced |
| Reviewer | routed and sampled cases | review verdict | none | none | none |
| Auditor | all trace, telemetry, overrides | audit verdict, ledger | none | proposals to definition | none |
| Distiller | approver mailbox (member threads), override reasons | draft queue | drafts | none | none |
| Process Assistant | state in scope | signals on behalf | none | as the person may | rejection notice **on the approver's approval**, with disclosure line |
| Approver-A / B | packaged case | approval, override + reason | none | none | payment and rejection within scope |
| Process Owner | all | rulings | ratifies drafts | arm after ruling | per scope |
| Internal Control | audits, ledger, per-person overrides | signs ceiling and SA | none | none | none |
| Platform Operator | telemetry, config | budgets, tiers | none | pause / resume | none |

Rulings that loosen a default: none. HR flags are read by a mechanism as a boolean only; no role sees the flag's content.
