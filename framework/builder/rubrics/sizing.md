# Rubric — sizing of items and cases

Used by the Auditor (pre and post delivery) and by the objective function (I.14.4). Sizes are points: S = 1, M = 2, L = 4, XL = 8. The pre size is given before reading the delivered result; the post size after. If the two agree more often than the threshold set at the periodic review, the pre size may not be independent and a Sizer role is considered.

| Size | Deliverable scope | Decisions | Sources touched | Verification |
|---|---|---|---|---|
| **S** | one section, field set or short message | none beyond derivable | one | checks only |
| **M** | one deliverable or one case step of a common type | one or two derivable, none free | two or three | checks + classifier |
| **L** | one deliverable with several parts, or a case of an uncommon type | several, some declared free | several, one unfamiliar | checks + classifier + review |
| **XL** | more than one deliverable, or a deliverable with an open design question | open design | many | review + human gate |

Rules:
- An XL item is a partition candidate (II.3); the Auditor notes it.
- Post size records what was delivered, not what was planned; the gap pre→post is a series.
- Cases of a process are sized per type once in the service plan and re-sized only at audit for exceptions.
