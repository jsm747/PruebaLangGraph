# Enterprise policy — template

**Filled by:** the Risk & Control function with the Portfolio Owner; amended only by them, with a dated record. **Read by:** Builder (viability and every step), Critic (every contract and definition), Architect, Reviewer, Auditor. **Lifecycle:** versioned; every instance records the policy version it was checked against; a new version triggers a check of every active instance at the next portfolio review.

---

# Enterprise policy v<n> — <organisation>

Every rule has an identifier and a type: **O** obligation (must) · **P** permission (may, within bounds) · **F** prohibition (must not). Instances may add stricter rules; they may never loosen these.

## Intent
<What the organisation uses agents for, and what it will not use them for. Two or three sentences.>

## Prohibitions (F)
| Id | Rule | Applies to |
|---|---|---|
| F1 | No agent decides, without a person, on <employment / credit / health / … the organisation's list> | all instances |
| F2 | No agent communicates externally without the disclosure line | all |
| F3 | No personal data of class <x> leaves <region / system> | all |

## Obligations (O)
| Id | Rule | Applies to |
|---|---|---|
| O1 | Every instance is in the registry with an owner and a review date | all |
| O2 | Every adverse decision about a person carries an explanation artefact | processes |
| O3 | Logs retained at least <n> months | all |

## Permissions (P)
| Id | Rule (with bounds) | Applies to |
|---|---|---|
| P1 | Automatic closure of favourable, reversible decisions below <amount> under a standing approval | processes, ceiling ≥ L1 |
| P2 | Agent spend up to <amount> per instance per month without portfolio approval | all |

## Accountability
<Who answers for what at enterprise level: Portfolio Owner, Risk & Control, Platform Operator; escalation path above a Process Owner.>

## Amendment record
| Version | Date | Change | Approved by |
|---|---|---|---|
