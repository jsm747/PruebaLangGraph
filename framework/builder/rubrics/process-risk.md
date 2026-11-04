# Rubric — process risk and autonomy ceiling

Used in step 1 of the Builder script for processes; written into the `service-plan`; signed by the Process Owner and the Risk & Control function; reviewed at each periodic review.

## Dimensions
Answer each with the level and one line of reason.

| Dimension | Low | Medium | High |
|---|---|---|---|
| Regulatory exposure | no regulated decision | regulated process, non-adverse decisions | decisions about people in a regulated category |
| Financial impact of a wrong decision | below the per-case threshold, recoverable | above threshold, recoverable | above threshold, not recoverable |
| Reversibility | reversible within the process | reversible with cost | irreversible (sent, paid, published, notified) |
| Personal data | none or minimal | personal data of members | sensitive data, or data of third parties / customers |
| Who bears an error | the team | the organisation | a customer or a third party |
| Reputation | none | internal | external |

## Legal categorisation (handed to legal, with a date)
- Does the process fall in a regulated high-risk category for automated decisions about people?
- Does building the system make the organisation its provider rather than its deployer?
- Which transparency, explanation and record-keeping duties apply, from when?

## Ceiling
| Ceiling | When |
|---|---|
| **L0** — no automatic closure | any dimension High, or the legal answers pending |
| **L1** — automatic closure only for favourable, reversible decisions below threshold | some Medium, none High, legal answered |
| **L2** — full routing | all Low or Medium with a signed justification |

The ceiling is a floor for human involvement, never a target: a process may run below its ceiling for as long as the owner wants.
