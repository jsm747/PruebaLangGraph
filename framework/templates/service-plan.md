# Service plan — template (process)

**Filled by:** Builder with the Process Owner, Risk & Control and the Gatekeepers who sign standing approvals. **Read by:** orchestrator (routing, SLAs, sampling), Budget Controller, Auditor, Process Assistant. **Lifecycle:** versioned with the definition; thresholds change only through a definition change.

---

# <Process> — service plan v<n>

## Risk assessment and autonomy ceiling
| Dimension | Assessment | Note |
|---|---|---|
| regulatory exposure | | |
| financial impact | | |
| reversibility of decisions | | |
| personal data | | |
| who bears an error | | |
| reputation | | |
| legal categorisation (high-risk category? provider or deployer?) | | answered by legal |
**Ceiling:** L0 | L1 | L2  **Signed:** owner <date> · Risk & Control <date>  **Review:** <date>

## Volumes and SLAs
| Case type | Expected volume / period | SLA end-to-end | SLA per human turn |
|---|---|---|---|

## Routing bands
| Band | Risk score | Assertions | Amount / impact | Route |
|---|---|---|---|---|
| auto | low | pass | below <threshold> | close under standing approval |
| review | medium or grey | | | LLM Reviewer |
| human | high · above threshold · exception · abstention · mandatory rule · adverse/irreversible class | | | Gatekeeper |

## Standing approvals
| Id | Decision class covered | Threshold | Signed by (role, person) | Scope | Valid from | Valid until |
|---|---|---|---|---|---|---|

## Sampling
| Stratum | Rate | Purpose |
|---|---|---|
| random, by route and type | <%> | calibrates classifier and Reviewer |
| risk-directed (closed cases) | <%> | coverage of borderline and high-impact |
| all exceptions and overrides | 100 % | learning |

## Budget per period
<Levels from the budget template, per case type if useful.>

## Audit cadence
<Every n days or n cases; who receives the report.>
