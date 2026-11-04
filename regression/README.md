`draft — owner: Framework Architect, Juan (jsm747)` · regression bank (I.16.5), readiness phase 8

# Regression bank

- `bank-v1.json` — golden cases: 12 router cases from the expense-claims example (III.3), 12 deterministic-check cases (R5, R11, R12), 8 role cases (Critic, Reviewer, Executor) from the two worked examples.
- `run.py` — runs every executable case; exits red if any case gives a result other than expected. Workflow `regression` runs it on every pull request.
- Role cases are `pending-runner` until the role workflows exist (phase 9); they are then executed against the role's live session and the expected fact.
- Rule: a change that breaks an old case does not ship. New cases come from every audited instance (platform guide §5).
