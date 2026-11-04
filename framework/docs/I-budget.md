# Part I.14 — Budget governance

> **Draft, to be developed with experience.** The reference implementation ran on a flat subscription and never governed spend; this part sets the structure (levels, separation from liveness caps, routing, attribution) but the policies — how levels are sized, how exhaustion is handled per role, how routing thresholds are set — have no operating evidence behind them yet. The first instances under pay-per-use are expected to rewrite it.

Agents consume paid capacity. Budgets are a layer of their own: deterministic, enforced by the orchestrator, owned by the Platform Operator, and separate from the caps that protect liveness.

## I.14.1 Four levels

| Level | Bounds | On exhaustion |
|---|---|---|
| **Session** | turns, tokens, wall time of one agent session | the session ends with the cause materialized; the item's turn passes to the role the failure mode names |
| **Item / case** | total spend on one item or case across all roles and rounds | the item is paused and escalated: it is too large or too contested for its contract |
| **Chain / process version** | total spend on one project chain, or on a process over a period | no new items are armed in that chain; in-flight sessions finish; the Process Owner is notified |
| **Period** | total spend of the instance per calendar period | no new arms in the instance; in-flight sessions finish; the Platform Operator is notified |

Exhaustion never kills an in-flight session (that loses work without saving money); it stops *new* arms in the exhausted scope.

## I.14.2 Separation from liveness caps

Retry, relaunch and round caps exist so that an unattended run cannot loop or stall indefinitely; they bound lost work. Budgets bound spend. They have different owners and are tuned separately; a budget problem is never solved by lowering a liveness cap, and a liveness problem never by raising a budget.

## I.14.3 Model tiers and cost routing

- Each role has a **model tier** as instance configuration, with a declared fallback on provider error and an operator override that needs no redeploy.
- Work is routed to the cheapest capable layer first: deterministic check → typed classifier → cheap LLM → strong LLM, escalating only on failure or by an explicit criterion (risk score, contested finding).
- Strong tiers by default for the roles that decide or judge (Architect, Critic, Reviewer, Resolver, Auditor); the cheapest that passes the gates for the Executor; cheap for subagents and the classifier.

## I.14.4 Attribution and the objective function

Every session's cost is attributed to its actor, item, chain and instance in the Auditor's ledger, in currency. This feeds the objective function used at every periodic review:

- **(a)** human intervention per delivered point, by human role;
- **(b)** delivered points per unit of cost;
- **(c)** gate quality — leak and rework — as a **constraint**.

Delivered points are the Auditor's sizing of each item or case (a common rubric, sized before and after delivery). A change is executed only if it moves (a) or (b) without worsening (c); a cost figure is never read without its quality pair from the same period.

## I.14.5 Defaults and clamps

Lesson-bearing defaults — a cap or threshold the framework raised because a lower value proved harmful — apply **upwards** in every instance, even where the instance pinned the old value; an instance that deliberately wants less declares it explicitly, and the framework release note names the instances affected.
