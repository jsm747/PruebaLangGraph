# Work item — template (project)

**Filled by:** Architect (contract); Critic approves; Executor fills the scope declaration and the delivery report. **Read by:** Executor, Researcher, Pre-reviewer, Reviewer, Integrator, Auditor. **Lifecycle:** one proposal per item; reopened on partial delivery within caps.

---

# <#id> — <title>

**Chain position:** <n of N>  **Depends on:** <ids>  **Next:** <id> | END (arms the Auditor)  **Milestone:** <m>
**Level:** L1 | L2 | L3  **Discovery item?** yes (deliverable = contracts of <ids>) | no
**External effect:** none | <kind, gate>

## Purpose
<One paragraph.>

## Contract
### Acceptance criteria (assertable)
- A1. <…>
- A2. <…>

### Invariants (executable)
| Id | Check | Pre-execution result |
|---|---|---|

### Anchors to existing material
<Semantic anchors — names, identifiers, record ids — never locations that move. UNKNOWN where not verified, with the escalation.>

### Decisions
| Decision | Status (closed · derivable from <record/clause> · free) |
|---|---|

### Deliverable
<What, in which canonical representation, where.>

### Scope declaration structure
<The sections / fields the Executor must declare touched, with identifiers.>

## Critique
`critique:lgtm` by Critic on <date> | findings: <…>

## Execution (filled by the Executor)
**Scope declared:** <identifiers touched>
**Polarity:** complete | partial — remaining scope: <verifiable list>
**Decisions derived:** <quote and source for each>
**Blocked on:** <the question, if any>

## Verification
`delta:computed` · `scope:match|mismatch` · `checks:green|red` · classifier facts · `review:pass|findings`

## Closure
`integrated` on <date> by Integrator · reopened (partial <n> of cap) · escalated
