# Why — what each principle prevents

For the reader who asks "why is this rule here?". One line per principle: the problem it prevents, stated as a problem. No cases, no history. The second table lists the failure classes a workflow engine must demonstrably handle (acceptance suite for requirement R3).

## Principles and the problems they prevent

| Principle | Without it |
|---|---|
| Closed contract | The executing agent fills gaps with plausible choices; each one is a decision nobody took, discovered at review or audit, and the item runs again |
| Materialized state | State is inferred from prose; prose gets sanitized, truncated or paraphrased; two components disagree about where an item is and the chain stalls or double-runs |
| One owner per fact; no self-certification | The executor declares its own work verified or ready; the gate accepts it; the first defect that passes is attributed to the gate, not to the declaration |
| Turn | An item sits with nobody responsible for it, and nothing detects it because nothing is "failing" |
| Deterministic signatures act immediately | A missing mechanical step is detected only after an age threshold; when the environment is slow, the threshold misfires and the wrong item is relaunched |
| Liveness caps are not cost controls | A cap lowered to save money lets a stall last a night; the money saved is smaller than the work lost |
| Session output is ephemeral | A decision or a hand-off that lived only in a session is gone when the session ends; the next actor starts blind |
| Mandate, tools, budget and actor guard change together | A role is told to do something it cannot do; it fails at the last step and the failure looks like a design question |
| Rules go where they are followed | A rule stated as a final step is skipped under pressure; the same rule in the header of the artefact's template is followed |
| Citations exist or they are not citations | A paraphrase presented as a quote becomes the source for the next contract; the drift compounds across items until a person notices the product is wrong |
| Categorize by nature | A deterministic guard written as guidance is a guard that is sometimes applied |
| Memory is not a mechanism | A duty that depends on remembering is forgotten whenever the session that remembered is not the one that acts |
| Three tiers of verification | Everything is judged by an LLM: cost grows with volume, and a judge that explains nothing mechanically is hard to calibrate |
| Make the deliverable diffable | Review becomes an opinion about a whole document; scope cannot be reconciled; nothing can be rolled back precisely |
| Fail-closed with a convergence rule | A control with no convergence rule loops; a control with no breaker loops forever |
| Humans as turns with ladders | A waiting person looks like a stall or is never reminded; a decision nobody can take blocks a series instead of one item |
| False escalations and rubber stamps measured | Autonomy stays below what people would accept, or oversight becomes a formality nobody notices |
| Standing approvals | Every automatic closure with effect either violates the human-gate rule or requires a person on every case |
| Mandatory-human rules before any score | A classifier lowers the route of a case that policy says a person must see |
| Random sampling alongside risk-directed | The system audits only what it chose to look at; the classifier grades itself |
| Overrides with a reason | The main learning signal of a process is a decision without an explanation |
| Content is data, never instruction | A sentence inside a mail or a document steers an agent that had no reason to obey it |
| Distiller as the only reader of raw corpus | Personal data spreads to every role; nothing has an owner or a promotion rule |
| Drafts before current | A misread transcript becomes a recorded decision |
| One writer per layer | One session's error reaches every instance; a template is patched by whoever noticed something |
| Proposal queue separate from work | Improvements execute because an agent proposed them, or never execute because nobody saw them |
| Ruling, not deferral | A queue of "later" grows until it is ignored |
| Objective function with quality as a constraint | Cost falls and nobody sees that the gates stopped catching defects |
| Instrument calibration | A score or a size that nobody checks against outcomes starts deciding on its own |
| Budgets in four levels | One session, one item or one month spends what the whole instance was meant to |
| Ledger and baseline from day one | Improvement cannot be shown; the loop has nothing to read |
| Map updated in the same change | The system drifts from its description; the next person designs against a map that is wrong |

## Failure classes a workflow engine must demonstrably handle (R3)

| Class | What the engine must show |
|---|---|
| Lost event | A state change whose event is not delivered is still acted upon (reconciliation from state, not only from events) |
| Duplicate trigger | Two triggers for the same step run once |
| Dead holder of a lock | A lock whose holder died is released without the holder |
| Double arm | Two attempts to start the same item or series result in one run |
| Orphaned flag | A state set by a step that then died is cleared or acted upon by a third party |
| Zombie turn | A turn held by an actor that is not running is detected without an age threshold where a mechanical trace is missing |
| Ghost run | A run that exists but never started is distinguished from a slow one by its structure, not its age |
| Lost amendment | A signal sent during a turn is delivered at the turn's close, never dropped, never applied mid-turn |
| Pause with in-flight work | New arms stop; in-flight work finishes; resume restarts in order |
| Priority change in flight | An item moved ahead enters at the next boundary without running in parallel |
| Queue exit without pop | Every path that frees a series also advances the queue |
| Timeout of a human turn | Escalation up the ladder with the packaged decision; top of ladder stops the item, not the series |
| Engine outage | An independent monitor detects it and can revive or flag it |
| Budget exhaustion | New arms stop in the exhausted scope; in-flight work finishes; the fact is visible |
| Actor without permission | A write by an identity without the role is refused and logged, including by agents on human-gate facts |
