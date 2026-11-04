# Protocol — template

**Filled by:** Architect at instantiation; Platform Operator for substrate mappings. **Read by:** every role; the orchestrator configuration is derived from it. **Lifecycle:** append-only: a marker or state is never renamed, only added or retired with a date.

---

# Protocol of <instance>

## States of an item / case
| State | Meaning | Written by | Turn belongs to | Leaves when |
|---|---|---|---|---|
| `armed` | ready for execution | Integrator / Process Owner | Executor | proposal exists |
| `proposed` | a proposal with structured scope exists | Executor | mechanisms | checks run |
| `checked` | deterministic checks and classifier materialized | mechanisms | Reviewer / routing | verdict or route |
| `findings` | Reviewer returned findings | Reviewer | Executor | new proposal |
| `approved` | human approval fact written | Gatekeeper | Integrator | integration |
| `integrated` | proposal is current | Integrator | — | — |
| `blocked` | non-derivable decision pending | Executor | Resolver (project) / human (process) | decision or escalation |
| `waiting:human:<role>` | a person must act | orchestrator | the assignee | fact written or SLA escalation |
| `paused` | queue or scope paused | Budget Controller / Process Owner | — | resume signal |
| <add per instance> | | | | |

## Facts (materialized state)
| Fact | Sole writer | Consumed by | Invalidated by |
|---|---|---|---|
| `delta:computed` | Deterministic Checks | Reviewer, Auditor | new proposal |
| `scope:match` / `scope:mismatch` | Deterministic Checks | routing | new proposal |
| `checks:green` / `checks:red` | Deterministic Checks | gate | new proposal |
| `classifier:<question>` | Typed Classifier | routing, Auditor | new proposal |
| `review:pass` / `review:findings` | Reviewer | gate | new proposal |
| `approval:<scope>` | human with that scope | Integrator, effect executor | — (traced) |
| `critique:lgtm` / `critique:findings` | Critic | arm gate | contract change |
| `audit:verdict` | Auditor | Process Owner, Process Reviewer | — |
| `budget:exhausted:<level>` | Budget Controller | orchestrator | reset / raise |
| <add per instance> | | | |

## Signals (through the process door, with the person's identity)
| Signal | Who may send | Effect | Acknowledged by |
|---|---|---|---|
| `approve` | role with scope | writes `approval:<scope>` | Integrator |
| `amend` | any member on their items | delivered at close of current turn; blocks integration until acknowledged | Executor / Architect |
| `pause` / `resume` | Process Owner, Platform Operator | stops new arms in scope | orchestrator |
| `escalate` | any member | moves the turn up the ladder | Process Assistant |
| `reprioritise` | Process Owner | reorders the queue | orchestrator |

## Interoperability
States map to the A2A task lifecycle where an instance exposes or consumes agents across systems: `armed`/`proposed`/`checked` → *working* · `waiting:human:*` and `blocked` → *input-required* · `integrated` → *completed* · viability no-go → *rejected* · pause → *canceled* where applicable. Tools are reached through MCP behind a gateway that is the audit chokepoint.

## Substrate mapping
<For each state, fact and signal: the field, list column, flow or event that implements it. Filled by the Platform Operator.>
