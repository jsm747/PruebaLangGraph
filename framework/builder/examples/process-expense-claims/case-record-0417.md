# Case 0417 — travel

**Definition version:** v1  **Received:** 2026-10-20 09:14  **Source:** expense system  **Classification:** employee personal data

## Data
claimant E-2231 (cost centre 410) · trip T-88 (10-13 to 10-15) · lines: L1 hotel 2 nights 310.00 EUR receipt RC-5510 · L2 dinner 48.50 EUR receipt RC-5511 · L3 taxi 23.00 EUR no receipt · L4 wine with client 36.00 EUR receipt RC-5512, attendees: 2 named

## Step 0 — mandatory-human rules
H1 no (417.50) · H2 **yes** — L4 under R5 would be reimbursable (attendees named), but L3 is no-receipt under 25 EUR (R2 threshold not reached → reimbursable) — no rejection line → H2 no · H3 no · H4 no · H5 **yes** — purpose text names a client (L4)

## Proposal (Executor)
R1 → L1 310.00, L2 48.50 reimbursed · R2 → L3 23.00 reimbursed (≤ 25 EUR without receipt) · R5 → L4 36.00 reimbursed (client entertainment, 2 attendees named) · R6 n/a (EUR). Total 417.50. Derived from: §3 limits ("hotel ≤ 180/night"), §4.1 ("receipts required above 25 EUR"), §3.6 ("client entertainment with named attendees").
Scope declared: lines L1–L4, instruction amount.

## Checks and classifier
`checks:green` (receipts resolve; limits; 60-day; sum) · risk 0.22 · A1 0.98 · A2 0.99 · A3 n/a · A4 1.00 · A5 0.99

## Route
**human** — because H5 (client named in purpose text), although band would be auto.

## Human turn
Assigned: Approver-A · Due: 2026-10-21 09:14 · Action: **approve** 2026-10-20 15:02 · Reason: — (approval as proposed; time to decide 3 min 40 s — not a rubber stamp by the instance's 60 s rule)

## Closure
Decision: reimburse 417.50 EUR · Approval cited: per-case fact by Approver-A · Effect: payroll instruction P-20261020-0417 · Explanation artefact: none (no rejection) · Closed 2026-10-20 15:03

## Audit
stratum: — (not sampled; H5 cases are all reviewed at the monthly audit for the H5 rule's precision)
