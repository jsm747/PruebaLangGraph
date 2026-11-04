# Registry entry — template

**Filled by:** Builder (proposed → instantiating → handover), then per-field writers (I.17.1). **Read by:** orchestrator (enforcement), liveness monitor, Process Owner, Portfolio Owner, Risk & Control, auditors. **Lifecycle:** one per instance from step 0 of the Builder session until retirement; never deleted.

---

# <instance id> — <name>

| Field | Value | Writer |
|---|---|---|
| Purpose | <one line> | Builder / Architect |
| Shape | project · entry L<n> · current L<n> — or process · ceiling L<n> | Builder / Architect / mechanisms |
| Status | proposed · instantiating · pilot · active · paused · contained · retired | per I.17.3 |
| Launch profile | pilot (end <date>; deferred items <list>; signed <who, date>) · production | Builder; Portfolio Owner |
| Owner | <directory id> | Builder; ruling |
| Sponsor | <directory id> | Builder |
| Risk & Control contact | <directory id> | Builder |
| Registered · launched | <date> · <date> | mechanisms |
| Last review · next review | <date> · <date> | mechanisms |
| Enterprise policy version | <n> checked on <date> | Builder; Critic on change |
| Framework version | built <x.y.z> · current <x.y.z> | Builder; Platform Operator |
| External effects | <kind → gate; standing approvals with expiry> | Builder / Architect |
| Data classes | <from information map> | Builder |
| Risk / legal | <risk assessment ref; categorisation; ceiling signed date> | Builder; Risk & Control |
| Budget | <period budget> · spend to date <n> | Builder; mechanisms |
| Indicators | (a) <n> · (b) <n> · (c) leak <n> rework <n> · vs baseline | mechanisms |
| Incidents | <open ids; containment step> | mechanisms |
| Path | project · simple process · complex process — defined-by <project id> | Builder |
| Dependencies | <instance ids, direction; defines / defined-by> | Builder / Architect |
| Viability outcome | go at <level/ceiling> · or no-go: <reason> | Builder |

## Agents of this instance
| Agent identity | Role | Model tier | Tools ref | Created | Last review |
|---|---|---|---|---|---|

## People in roles
<Reference to this instance's human-roles-binding; the registry derives the people inventory from it.>

## Change log
| Date | Field | From → to | By |
|---|---|---|---|
