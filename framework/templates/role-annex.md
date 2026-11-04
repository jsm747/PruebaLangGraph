# Role annex — template

**Filled by:** Architect / Builder, one per LLM role active in the instance. **Read by:** that role at session start, together with its generic mandate. **Lifecycle:** versioned with the instance; a change revisits tools, budget and actor guard together.

---

# <Role> — annex for <instance>

## 1. Mandate (instance additions)
<What this role does *here* that the generic mandate does not say: the deliverables it touches, the domain, the people it serves.>
**Never does, here:** <additions to the generic list>

## 2. Positional rules
<The rules this role must follow every time, as they will appear in the header of what it produces. Short, imperative, numbered.>
1. <…>
2. <…>

## 3. Reads / materializes
**Reads:** <data classes, by name from the information map>
**Materializes:** <facts, from the protocol, that only this role writes>

## 4. Tools
<Allowlist. Nothing else.>

## 5. Trigger and actor guard
**Runs on:** <event / state>  **May be triggered by:** <roles / identities>  **Concurrency:** <one per item | one per series | …>

## 6. Budget and model tier
**Session caps:** turns <n> · tokens <n> · wall time <n>
**Model tier:** <tier>  **Fallback:** <tier>  **Override:** Platform Operator

## 7. Reading discipline
<What it reads first, then, and never; the reading budget.>

## 8. Failure mode
<fail-open | fail-closed>, because <human present? external effect downstream?>. **Caps:** <rounds / retries>. **Convergence rule:** <applies | n/a>. **Breaker:** after <n> → <to whom>.

## 9. Session output rule
Every hand-off is published as: <fact / comment / record>. Nothing stays in the session.

## 10. Value measurement
**Ledger class:** productive | sensor | null | redundant | reverted
**Series:** <the metric that shows whether this role earns its cost>

## 11. Rationale
<One line per non-obvious rule above: the problem it prevents.>
