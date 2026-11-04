# Skill — authoring records, contracts and plans (Architect, Builder, Critic)

How normative artefacts are written so that an Executor can act on them and a Critic can pass them.

## Identifiers and quotation
- Every sentence others may rely on carries an identifier (D1, A1, R3, Inv.2). A sentence without an identifier is not citable.
- A quotation reproduces the source literally and names the identifier. A paraphrase is written as a paraphrase, never inside quotation marks.
- Numbers, thresholds, names and dates are written exactly. "About", "roughly", "to be confirmed" do not appear in a closed contract.

## Decisions
- Each decision is one of: **closed** (the text decides it) · **derivable** (the text points to the record and clause from which an Executor derives it by quotation) · **free** (the text says the Executor may choose, and within what bounds).
- A decision that is none of the three is a defect of the author, not flexibility.
- Rules that bound behaviour are typed **O** (must), **P** (may, with the bounds stated) or **F** (must not); a step of a procedure is operational and says so. An untyped rule is a defect.

## Criteria and invariants
- Acceptance criteria are assertable (rubric `builder/rubrics/viability.md`): true or false against the result.
- Invariants are executable; each carries its pre-execution result; each cites the clause it protects (`Inv.2 ⇐ D3`). An invariant that predicts the opposite of its clause is a defect.
- Quantitative clauses carry an executable assertion (input → expected output); they are never left to reading.

## Existing state
- Any claim that something already exists, is computed, is covered or is in place carries a verified anchor (`state: <claim> ⇐ <where>`), verified in session.
- Without an anchor it is written as `UNKNOWN: <claim> — Executor verifies; if false, escalate with the finding`.

## Scope and partition
- One item is one proposal. Split by default when: two areas of responsibility · more than about five criteria · an open design decision · an enumerable definition of done.
- The scope declaration structure (sections or fields with identifiers) is part of the contract so reconciliation is mechanical.
- Every item has its link to the next, or the end marker; every external effect names its gate.

## Plans
- Milestones have dates; those with external commitment are marked and name to whom.
- Gates are bound to people, with availability checked for the window.
- Later items may be sketches (purpose and dependencies); the plan says so and no sketch is armed.

## Before publishing
A mechanical pass, not a reading: every identifier unique · every quotation found literally · every decision classified · every criterion assertable · every invariant with pre-result and clause · every existing-state claim anchored or UNKNOWN · every external effect gated · every item linked or ended.
