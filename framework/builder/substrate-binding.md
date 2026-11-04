# Substrate binding of the Builder

Filled by the Platform Operator before the first Builder session. **If this file is empty, the Builder stops at load and says so.**

| What the Builder needs | Binding (platform specifics) |
|---|---|
| Identity it runs under | |
| Where instance files are written (library / repository / workspace) and how versioning works there | |
| How a decision record is created and how append-only is enforced | |
| How a template becomes an instance artefact (copy, render, form) | |
| How a role annex is loaded by the role at session start | |
| How the protocol's states, facts and signals map to fields, lists, flows, events | |
| How the directory is queried for roles, deputies, superiors, availability | |
| Where the ledger and telemetry land, and how a test session proves they do | |
| How a budget level is enforced and how exhaustion pauses arms | |
| Which messaging channels the Process Assistant may use | |
| Which classifier service is available (R7) or that none is | |
| How an external effect is executed and traced, and how the approval primitive is invoked | |
| Framework version tag in use | |

The substrate contract (`docs/I-substrate-contract.md`) says what each line must guarantee; the instantiation checklist asks the operator to demonstrate it.
