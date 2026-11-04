# Item checks — template (project)

**Filled by:** Architect per deliverable type; Platform Operator wires the deterministic checks. **Read by:** Deterministic Checks, Typed Classifier, Reviewer, Auditor. **Lifecycle:** versioned with the spec; a new deliverable type adds a block.

---

# Checks for deliverable type <type> in <project>

## Canonical representation
<How the deliverable is converted for comparison; what the delta looks like.>

## Deterministic checks
| Id | Check | Tool / rule | On red |
|---|---|---|---|
| C1 | required fields present | | back to Executor |
| C2 | format valid | | back to Executor |
| C3 | calculations reproduce | | back to Executor |
| C4 | consistency with <source> | | back to Executor |
| C5 | citations exist literally | Citation Verifier | back to Executor |
| C6 | scope declared = scope changed | reconciliation | `scope:mismatch` → Executor |

## Classifier questions (one per assertable criterion)
| Id | Question (boolean / choice / score) | Threshold | Grey band | On fail | On grey |
|---|---|---|---|---|---|
| Q-A1 | | | | Reviewer | Reviewer |

## What is left for the Reviewer
<The criteria that neither a check nor a question can settle; the Reviewer judges only these, plus findings on anything red above.>

## Invariant execution (Auditor)
<How each invariant of the spec is run against the final state, and where the output is pasted.>
