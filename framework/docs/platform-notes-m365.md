# Platform notes — Microsoft 365 (non-normative)

Pointers for the platform team on where the framework's requirements may already be met by the Microsoft stack. These are notes, not requirements: verify each against your tenant and the current product before relying on it. The substrate contract (I.10) remains the test.

| Requirement | Candidate implementation | What to check |
|---|---|---|
| R3 orchestrator; `process-definition` | A durable workflow engine running the process definition expressed in **BPMN**, with agentic steps modelled as ad-hoc subprocesses (the agent chooses among modelled tasks; the engine executes them). Power Automate / Logic Apps, Microsoft Agent Framework workflows (checkpointing, human approval with pause/resume), or a BPMN engine (Camunda, UiPath Maestro) | Exactly-once steps, lock release by a third party, signals without races, state visible on the item |
| R8 telemetry | OpenTelemetry GenAI traces from Agent Framework / Foundry; cost derived from tokens | Tokens per call, agent and tool spans, outcome per session — for Copilot Studio agents specifically |
| R10 identity, registry | **Entra Agent ID** for agent identities; **Agent 365** registry (owner, lifecycle, ownerless agents flagged) | Per-session short-lived identity; whether a lapsed review can block an agent (Agent 365 triggers reviews by risk, not by expiry — the framework's enforcement in I.17.2 is stricter and may need a policy or a gateway) |
| R13 corpus isolation and classification | Purview sensitivity labels and DLP on mailboxes, transcripts and libraries | That only the Distiller identity reads raw sources |
| R15 approvals | Approvals in Power Automate / Teams with identity | That agents cannot invoke them on their own behalf |
| R16, I.16 security | Defender for build-time and run-time agent risks; independent heartbeat outside the orchestrator's tenant resources | Independence of the liveness path |
| Interoperability | A2A and MCP support in Copilot Studio and Agent Framework | Authentication of agent-to-agent calls; MCP gateway as audit point |
