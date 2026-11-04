# Expense claims — definition v1

**Owner:** Finance Operations Lead (FinOps-Lead)  **Risk & Control:** Internal Control  **Autonomy ceiling:** L1 (signed 2026-10-18)  **Framework version:** 0.1

## Purpose and boundaries
Decide whether an employee's expense claim is reimbursed, in full or in part, under the expense policy v7, and produce the reimbursement instruction or the explanation of a rejection. Never changes the policy; never contacts the merchant; never decides on claims of Finance staff themselves (segregation).

## Case types
| Type | Entry source | Data fields | Deliverable per step | Canonical representation |
|---|---|---|---|---|
| travel | expense system | claimant id, cost centre, dates, lines (category, amount, currency, receipt ref), trip ref | reimbursement decision record | structured fields |
| non-travel | expense system | claimant id, cost centre, lines, purpose text | same | structured fields |

## State machine of a case
As in the template: received → armed → checked → routed → (review | waiting:human:approver) → closed; exception.

## Rules of decision
| Id | Rule | Decision class | Derivable inputs | Deliverable |
|---|---|---|---|---|
| R1 | A line with a valid receipt, within the category limit of policy v7 §3, within 60 days of the expense date, is reimbursable in full. | favourable · reversible (payroll correction) · no third party | policy §3 limits table; line fields | reimbursement line |
| R2 | A line without a receipt above 25 EUR is not reimbursable. | adverse · reversible · no third party | policy §4.1 | rejection line with explanation |
| R3 | A line above the category limit is reimbursed up to the limit; the excess is rejected. | partly adverse · reversible | policy §3 | split line |
| R4 | A claim older than 60 days is rejected in full. | adverse · reversible | policy §2.2 | rejection |
| R5 | Alcohol lines are reimbursable only within a client-entertainment claim with named attendees. | adverse if rejected · reversible | policy §3.6 | line decision |
| R6 | Currency conversion uses the system rate of the expense date. | favourable · reversible | system rate table | amount |

## Mandatory-human rules (step 0)
| Id | Condition | Route | Reason |
|---|---|---|---|
| H1 | claim total > 2,000 EUR | human | threshold of standing approval |
| H2 | any rejection line (R2, R3 excess, R4, R5) | human | adverse decisions are never automatic at ceiling L1 |
| H3 | claimant is in group `finance-ops` | human (second approver) | segregation |
| H4 | claimant flagged `leave-of-absence` or `grievance-open` in HR | human | sensitivity |
| H5 | purpose text mentions a customer name or a gift | human | compliance |

## Assertable criteria
- A1. Every reimbursed line has a receipt reference that resolves in the expense system.
- A2. Every line amount ≤ category limit, or the line is split per R3.
- A3. Every rejection line cites the rule id and the policy clause.
- A4. The sum of reimbursed lines equals the reimbursement instruction amount.
- A5. No line older than 60 days is reimbursed.

## Exceptions policy
A line whose category is not in policy §3, a receipt the system cannot resolve, or a claim in a currency without a system rate is an exception: to the approver, counted, and reported to the process loop.

## Changes in flight
Open claims finish under v1. A policy change marked immediate pauses and re-runs open claims.

## Explanation artefact (rejections)
Fields: lines rejected, rule id, policy clause text, amount, how to resubmit (receipt, correction), who decided (role), contact for queries.
