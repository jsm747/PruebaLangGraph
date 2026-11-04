# Budget — template

**Filled by:** Builder with the Platform Operator and the Process Owner. **Read by:** Budget Controller (enforcement), Auditor (attribution). **Lifecycle:** reviewed at every periodic review; lesson-bearing floors apply upwards. *Draft area of the framework: expect to rewrite with experience.*

---

# Budget of <instance>

## Levels
| Level | Bound | On exhaustion | Notified |
|---|---|---|---|
| Session — <role> | turns <n> · tokens <n> · time <n> | session ends, cause materialized | — |
| Item / case | <currency> | item paused and escalated | Process Owner |
| Chain / process version | <currency> | no new arms in chain | Process Owner |
| Period (<month>) | <currency> | no new arms in instance | Platform Operator, Process Owner |

## Model tiers
| Role | Tier | Fallback | Effort (if applicable) |
|---|---|---|---|
| Architect / Builder | strong | | |
| Critic | strong | | |
| Reviewer | strong | | |
| Resolver | strong | | |
| Auditor | strong | | |
| Process Reviewer | strong | | |
| Executor | cheapest that passes the gates | | |
| Researcher / Pre-reviewer | cheap | | |
| Distiller | <by corpus volume> | | |
| Process Assistant | cheap | | |
| Typed Classifier | <model / service> | LLM judge (degraded) | |

## Cost routing
deterministic → typed classifier → cheap LLM → strong LLM. Escalation criteria: <failure | risk band | contested finding>.

## Floors that apply upwards
| Parameter | Floor | Reason (problem it prevents) |
|---|---|---|

## Separation
Liveness caps (retries, relaunches, rounds) are in the protocol and role annexes, owned by <role>; they are not changed from here.
