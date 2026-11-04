# Rubric — viability of a deliverable

Used in step 1 of the Builder script and by the Critic. A deliverable is controllable when both tests pass.

## Test A — assertable criteria
A statement is **assertable** when, given the delivered result, two people who have never spoken would answer true or false the same way.

| Statement | Assertable? | Why |
|---|---|---|
| "The model's balance sheet balances in every year" | yes | computed |
| "Every assumption in the register cites a source" | yes | checked field by field |
| "The letter cites the policy clause the decision rests on" | yes | literal search |
| "The plan covers all departments listed in the brief" | yes | list against list |
| "The analysis is thorough" | no | opinion |
| "The customer will be satisfied" | no | future, not in the result |
| "The report is well written" | no, unless reduced to checks (length, structure, required sections) | |

**Minimum:** at least three assertable statements per deliverable, covering its purpose, or an L0 entry with the questions L1 must answer.

## Test B — comparable form
| Form | Comparable? | Canonical representation |
|---|---|---|
| spreadsheet, list, record set | yes | cell / field diff |
| text document | yes | extracted text, line diff, or platform compare |
| slide deck with text | yes, weakly | extracted text per slide; images uncompared |
| image, drawing, whiteboard photo | no | agree a text or structured companion, or the deliverable stays with people |
| message to be sent | yes | text |
| decision in another system | yes | the record's fields |

## Test C — at least one executable invariant
Something that can be run against the result: a calculation, a count, a presence check, a consistency check between two artefacts. If none exists at entry, the plan names the milestone by which one will.

## Verdict
- A, B and C pass → go.
- A passes, B fails for some deliverables → go for the others; the failing ones stay with people.
- A fails but the owner can state L1 questions → go at L0.
- A fails and no L1 questions → no-go, written as such.
