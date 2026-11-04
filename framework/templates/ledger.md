# Ledger — template (schema)

**Filled by:** mechanisms (telemetry, facts) and the Auditor (sizing, classifications, periodic figures). **Read by:** Auditor, Process Owner, Process Reviewer, Framework review. **Lifecycle:** append-only; closed per period; retention per the information map.

---

# Ledger of <instance>

## Baseline (before the instance ran)
| Measure | Value | Source | Date |
|---|---|---|---|
| cost per item / case (human process) | | | |
| elapsed time per item / case | | | |
| quality (defects, rework, complaints) | | | |
| human decisions per item / case | | | |

## Sessions (one row per agent session, from telemetry)
`session_id · actor (role) · item/case · model · tokens_in · tokens_out · cost · turns · wall_time · outcome (success | budget | error | dead) · ledger_class (productive | sensor | null | redundant | reverted)`

## Items / cases
`id · shape · size_pre · size_post (Auditor) · proposals · review_rounds · route (process) · checks_red · classifier_facts · human_turns · escalations · false_escalations · rubber_stamps · overrides (with role, reason) · cost_total · elapsed · outcome`

## Human turns
`turn_id · role · person (or role only, per governance) · item/case · assigned_at · due_at · acted_at · action (approve | override | escalate | timeout) · reason`

## Instruments
`instrument (classifier question | sizing | risk score) · period · stated_probability_band · observed_rate · n · by_group`

## Period summary (Auditor)
| Measure | Value |
|---|---|
| (a) human intervention per delivered point, by human role | |
| (b) delivered points per unit of cost | |
| (c) leak · rework | |
| override rate · reasons distribution | |
| false escalations · rubber stamps | |
| SLA compliance by role | |
| calibration drift, by question and by group | |
| cost per route / per role | |
| L1-vs-L4 realisation gap (projects) | |
