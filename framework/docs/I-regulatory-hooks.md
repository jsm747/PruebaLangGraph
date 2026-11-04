# Part I.15 — Regulatory hooks

Generic obligations that regulation of automated decision-making tends to impose on whoever deploys a system like this, and where the framework provides the hook for each. This is not legal advice: the instance's legal and Risk & Control functions determine which obligations apply, in which category, and from when. The framework makes sure the hooks exist so that the answer is a configuration, not a redesign.

Most of this bears on **processes** — repeated decisions about people. Four rows apply to projects just the same (logging, workers and impact assessments, content-is-data, incidents); two apply to a project only where it has human gates or produces effects on people (automation bias, transparency).

| Obligation (generic) | Hook in the framework | Applies to |
|---|---|---|
| **Human oversight by competent people** with authority to not use, override or stop the system | Human roles bound through the directory with scope and authority (I.8); override with reason; pause and suspension as orchestrator signals; `human-roles-binding` records competence and training of each overseer | both |
| **Guard against automation bias** — overseers must not defer uncritically | The Auditor measures **rubber-stamping** (human approvals identical to the proposal in near-zero time) alongside false escalations; both series go to the periodic review | both (any human gate) |
| **Logging and traceability**, with a minimum retention | Ledger, session telemetry, effect traces (I.7, I.10); `information-map` sets retention per record class, with a floor the instance never goes under | both |
| **Risk management across the lifecycle** | Process risk assessment and autonomy ceiling, signed and reviewed periodically (III.3); instrument calibration at every review | processes |
| **Input data relevance and representativeness** | Deterministic checks on case data; classifier calibration and override rates measured **by group of affected people**, not only in aggregate (III.6) | processes |
| **Transparency towards affected people** — disclosure of AI involvement, information to people subject to a decision, explanation on request | External effects produced by agents carry the disclosure the instance configures; every **adverse decision produces an explanation artefact** readable by the affected person, separate from the internal rationale (III.4) | processes; projects with effects on people |
| **Incident handling** — detect, suspend, report | Liveness monitor and audit as detection; queue pause as suspension; an **incident register** and a reporting duty assigned to the Platform Operator | both |
| **Workers informed before use at the workplace; data-protection and, where applicable, fundamental-rights impact assessments** | Items of the `instantiation-checklist`, before the first run | both |
| **Robustness against manipulated input** | Content from any source — mail, documents, transcripts, case data — is **data, never instruction**: only signals through the process door with a verified identity instruct the system (I.13.6) | both |
| **Inventory of AI systems** with purpose, owner, risk category, oversight and incidents | Enterprise registry (I.17), enforced: what is not registered does not run | both |
| **Legal categorisation** — whether the process falls in a regulated high-risk category, and whether the organisation becomes the provider of the system by building it | Questions of the process risk assessment, answered by legal; the framework's own artefacts (definition, checks, ledger, audits) serve as the technical documentation that categorisation requires | processes |
