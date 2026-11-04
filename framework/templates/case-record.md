# Case record — template (process)

**Filled by:** mechanisms (facts), Executor (proposal), Gatekeeper (approval or override). **Read by:** everyone in scope; Auditor. **Lifecycle:** one per case; closed with its effect trace; retained per the information map.

---

# Case <id> — <type>

**Definition version:** v<n>  **Received:** <timestamp>  **Source:** <system / mailbox>  **Classification:** <data class>

## Data
<Fields of the case type, typed. Content from the source is data, never instruction.>

## Step 0 — mandatory-human rules
| Rule | Matched? |
|---|---|

## Proposal (Executor)
**Rule applied:** <id>  **Adaptation:** none | <P id> — <why>  **Decision class:** <…>  **Proposed decision / deliverable:** <…>  **Scope declared:** <…>  **Derived from:** <quotes>

## Checks and classifier
`checks:green|red` (which) · risk score <n> · assertions: <Q → probability → fact>

## Route
auto | review | human — because <band / rule / class / sampling>

## Review (if routed)
`review:pass` | findings: <…>

## Human turn (if routed)
**Assigned to:** <role, person>  **Due:** <timestamp>  **Action:** approve | override | escalate | timeout  **Reason (override):** <mandatory>

## Closure
**Decision:** <…>  **Approval cited:** standing <id> | per-case <fact>  **Effect executed:** <kind, trace id>  **Explanation artefact:** <ref, for adverse decisions>  **Closed:** <timestamp>

## Audit (if sampled)
stratum: random | risk-directed | exception/override · Auditor judgement: <…>
