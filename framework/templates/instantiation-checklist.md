# Instantiation checklist — template

**Filled by:** Builder, as assertions it checks before declaring the instance ready; countersigned by the Process Owner. **Read by:** Process Owner, Platform Operator, Framework review. **Lifecycle:** one per instance; re-run after any framework version change.

---

# Instantiation of <instance> — framework version <x.y>

## Viability (go / no-go)
- [ ] Checked against enterprise policy v<n>: no conflict; prohibitions that apply listed.
- [ ] Assertable criteria and at least one executable invariant per deliverable, or discovery items that will produce them (projects: read for the entry level L0–L4).
- [ ] Every deliverable has a canonical diffable representation.
- [ ] Raw corpus reachable by a Distiller identity under the classification rules, or the owner accepts an instance without distillation.
- [ ] Process: risk assessment done; autonomy ceiling signed by owner and Risk & Control; legal categorisation questions answered.
- [ ] A Process Owner with authority to rule, and a ruling cadence they will keep.

## Profile (I.18)
- [ ] Pilot (end <date>; scope <volume, users>; ceiling L0; no standing approvals; deferred items <list>; Risk & Control engaged by <date>) — signed by the Portfolio Owner — or production.

## Path
- [ ] Path decided and the deciding condition written: project · simple process · complex process (defined by project <id>).

## Minimum viable instance
- [ ] Spec with criteria and invariants; plan (project) or service plan (process).
- [ ] Permission matrix with external-effects column; every effect has a gate.
- [ ] Human roles bound: holders, deputies, superiors, SLAs, competence; ladders defined.
- [ ] Budgets at four levels; session telemetry verified on a test session.
- [ ] Ledger schema deployed; baseline recorded.
- [ ] Signal channels open: proposal queue, audit panel, decision digest, corrections ledger, draft queue, incident register.
- [ ] Information map with classification and retention floors.
- [ ] Ruling cadence booked with a date.
- [ ] Process: decision classes on every rule; mandatory-human rules; standing approvals signed with validity.

## Substrate contract (demonstrated by the Platform Operator)
- [ ] R1–R19 each demonstrated per its acceptance test; R7 present or degradation accepted and budget recomputed.

## People and legal
- [ ] Workers and their representatives informed before use at the workplace.
- [ ] Data-protection impact assessment done where applicable.
- [ ] Fundamental-rights impact assessment done where applicable.
- [ ] Disclosure wording configured for agent-generated external effects.
- [ ] Override attribution governance decided before the ledger records persons.

## First supervised run
- [ ] One item or a small batch of cases run with every gate human; ledger read with the owner; thresholds set from what was seen.

## Handover
- [ ] Registry entry complete; agents registered; first review date set; status set to active after the first run.
- [ ] Process map current. Builder ledger closed; framework proposals filed.

**Declared ready by:** Builder <date>  **Countersigned:** Process Owner <date>
