# Instantiation — Expense claims — framework 0.1

## Viability
- [x] Criteria A1–A5 assertable; invariants: A2, A4, A5 deterministic on every case.
- [x] Canonical form: structured fields in the expense system.
- [x] Corpus: approver mailbox reachable by Distiller identity under thread-membership rule; HR flags as boolean only.
- [x] Risk assessment done; ceiling L1 signed by FinOps-Lead and Internal Control; legal categorisation answered 2026-10-16.
- [x] Process Owner FinOps-Lead; monthly review, first 2026-11-20.

## Minimum viable instance
- [x] Definition v1; service plan v1.
- [x] Permission matrix: payment only under SA-1 or per-case approval; rejection notice only on approval.
- [x] Human roles bound; ladders; approvers briefed on automation bias.
- [x] Budgets; telemetry verified 2026-10-17.
- [x] Ledger; baseline: 1,300 claims/month, 2 approvers × ~60 % of their time, median 4.2 working days end-to-end, 3.1 % claims corrected after payment.
- [x] Signal channels open; incident register.
- [x] Information map with retention; disclosure line configured.
- [x] Ruling cadence booked.
- [x] Decision classes on R1–R6; H1–H5; SA-1 signed with validity.

## Substrate contract
- [x] R1–R19 demonstrated 2026-10-17; R7 present (tenant classifier).

## People and legal
- [x] Works council informed 2026-10-14; per-person override visibility limited to Internal Control.
- [x] DPIA completed 2026-10-16 (employee data; HR flag as boolean).
- [ ] FRIA — not applicable (Legal).
- [x] Disclosure configured on rejection notices.

## First supervised run
- [x] 40 claims run 2026-10-20 with every gate human; ledger read with FinOps-Lead; Q-H5 threshold set to 0.70 (from 0.60) after 11 false routes.

## Handover
- [x] Process map current. Builder ledger: 2 corrections (standing-approval validity asked after thresholds, should be together; H-rule list needed a "sensitivity" example) — filed.

**Declared ready by:** Builder 2026-10-20  **Countersigned:** FinOps-Lead 2026-10-20
