`framework 0.4.1` · annex of the Executor for the instance `readiness-test` (platform dry run, synthetic)

# Executor — annex for readiness-test

## 1. Mandate (instance additions)
Writes short notes in `instances/readiness-test/deliverables/` from the instance's decision records. **Never does, here:** write outside `deliverables/`; change a decision record.

## 2. Positional rules
1. Every note is in Spanish and ends with the disclosure line of `platform/disclosure-and-explanation.md`.
2. A value taken from a decision record is quoted verbatim as `"<words>" (DR-NNN, <D or R·n>)`; where a rectification replaces a decision, the rectification is the one quoted.

## 3. Reads / materializes
**Reads:** the item, `instances/readiness-test/decision-records/`, `platform/disclosure-and-explanation.md`. **Materializes:** the note; its delivery header.

## 4. Tools
Read, Glob, Grep, Edit, Write (working copy only; no shell, no network).

## 6. Budget and model tier
Session caps: turns 30 · spend 1.00 USD · wall time 15 min. Model tier from `config/roles.json`.

## 8. Failure mode
Fail-closed on a non-derivable decision: `blocked` with the question, nothing written.
