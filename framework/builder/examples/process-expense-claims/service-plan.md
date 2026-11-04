# Expense claims — service plan v1

## Risk assessment and autonomy ceiling
| Dimension | Assessment | Note |
|---|---|---|
| regulatory exposure | low | internal reimbursement; tax rules applied by payroll |
| financial impact | medium | above 2,000 EUR not recoverable in practice |
| reversibility | low (reversible) | payroll correction next cycle |
| personal data | medium | employee data; HR flags |
| who bears an error | the organisation; the employee on a wrong rejection | |
| reputation | internal | |
| legal categorisation | not a regulated high-risk category (Legal, 2026-10-16); deployer | |
**Ceiling:** L1  **Signed:** FinOps-Lead 2026-10-18 · Internal Control 2026-10-18  **Review:** 2027-01-15

## Volumes and SLAs
| Case type | Expected volume / month | SLA end-to-end | SLA per human turn |
|---|---|---|---|
| travel | 900 | 3 working days | 1 working day |
| non-travel | 400 | 3 working days | 1 working day |

## Routing bands
| Band | Risk score | Assertions | Amount | Route |
|---|---|---|---|---|
| auto | < 0.30 | all ≥ 0.95 | ≤ 2,000 EUR, no rejection line | close under standing approval SA-1 |
| review | 0.30–0.60, or any assertion in 0.80–0.95 | | | LLM Reviewer, then auto if pass |
| human | > 0.60 · H1–H5 · any assertion < 0.80 · abstention · exception | | | approver |

## Standing approvals
| Id | Decision class covered | Threshold | Signed by | Scope | Valid from | Valid until |
|---|---|---|---|---|---|---|
| SA-1 | favourable, reversible, full reimbursement under R1/R6 | ≤ 2,000 EUR per claim | Approver-A (FinOps-Lead) | all cost centres | 2026-10-18 | 2027-04-18 |

## Sampling
| Stratum | Rate | Purpose |
|---|---|---|
| random, by route and type | 5 % of auto; 10 % of review | calibration |
| risk-directed (closed cases) | 3 % | borderline scores, unusual merchant patterns, repeated near-threshold claims |
| all exceptions and overrides | 100 % | learning |

## Budget per period
Session caps per budget template; case cap 1.20 EUR; month cap 1,800 EUR agent spend.

## Audit cadence
Monthly; report to FinOps-Lead and Internal Control.
