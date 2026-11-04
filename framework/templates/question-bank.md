# Question bank — template (process)

**Filled by:** Architect from the definition's assertable criteria and compliance clauses; thresholds tuned at the periodic review. **Read by:** Typed Classifier (execution), Auditor (calibration). **Lifecycle:** versioned with the definition; a new question is a definition change.

---

# Questions of <process> v<n>

## Risk score
**Definition:** <what the score expresses; the state passed to the classifier; scale>  **Bands:** low < <x> ≤ medium < <y> ≤ high

## Assertions
| Id | Criterion / clause | Question type (boolean · choice · score) | State given to the classifier | Threshold for a fact | Grey band | Fact written | On fail | On grey |
|---|---|---|---|---|---|---|---|---|

## Calibration (Auditor, per period)
| Id | Stated probability band | Observed rate | n | By group | Drift |
|---|---|---|---|---|---|

## Rules
- Quantitative clauses are executed by a deterministic check, never asked here.
- A question whose calibration drifts beyond <threshold> is suspended: its cases go to review until re-tuned.
- Proposed questions from override reasons enter as drafts; the definition change makes them current.
