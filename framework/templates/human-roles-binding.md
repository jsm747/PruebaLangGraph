# Human roles binding — template

**Filled by:** Builder with the Process Owner; identities resolved by the Platform Operator against the corporate directory. **Read by:** the orchestrator (assignment, SLAs, ladders), the Process Assistant. **Lifecycle:** reviewed at every periodic review; availability checked by the Critic against planned gates.

---

# Human roles of <instance>

| Role | Scope | Holder (directory id) | Deputy | Superior | SLA for a turn | Reminder before | Competence / training required | Last trained |
|---|---|---|---|---|---|---|---|---|
| Process Owner | whole instance | | | | | | | |
| Gatekeeper | <kind of effect, threshold> | | | | | | | |
| Gatekeeper | <…> | | | | | | | |
| Domain expert | <topic> | | | | | | | |
| Risk & Control | risk assessment, standing approvals | | | | | | | |
| Platform Operator | substrate | | | | | | | |

## Escalation ladders
<One per role: holder → deputy → superior → … → final breaker (stops the item, not the series).>

## Standing approvals (processes)
| Approval | Signed by | Scope | Thresholds | Valid from | Valid until | Cited by |
|---|---|---|---|---|---|---|

## Rules
- A gate is bound to a person, not to a mailbox.
- Availability in the window of a planned gate is a Critic check.
- Overseers hold the competence listed; the instance records training.
- Attribution of overrides per person is governed by: <the governance decision taken before the ledger was switched on>.
