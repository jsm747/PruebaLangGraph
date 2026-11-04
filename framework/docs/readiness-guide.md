# Getting the platform ready with the Readiness Agent — a guide

You are preparing the platform on which agent projects and processes will run, and **you own the final design**. The framework, its checklist and its documents are a starting point: keep, change or drop whatever you decide. The **Readiness Agent** works for you: it drafts, maps requirements to your stack, writes tests, records what they show and keeps track of open topics. When you depart from a recommendation, it tells you once what that recommendation was meant to prevent and what else in the framework depends on it, records your choice, and carries on with your version. It reads the whole framework so that it can do this.

## What you get

A platform designed by you, with what it has shown in tests clearly separated from what it has not; the documents you decided you need; a regression bank; a dry run with a real task; and an adaptation register that records where you chose differently from the framework and why.

## What it is not

- It does not configure your platform. Your engineers do; the agent tells them what has to be true and how to prove it.
- It does not run anything in production or with real personal data. Tests run on synthetic data in a test environment, under your identity.
- It does not decide for you, insist, or re-open what you have decided. It does not ask for signatures for your design choices.
- It does not report as working what it has not seen working: a test counts by its output.
- It does not replace the Risk & Control function, legal or data protection. It prepares drafts and questions for them.

## Before you start — have these ready

- **Names**: Platform Operator lead, Framework Architect lead, Framework Owner (someone who will not implement framework changes), Portfolio Owner, and contacts in Risk & Control, legal, data protection and security.
- **Your stack**: which products you intend to use for the orchestrator, agent runtime, identities, storage, approvals, monitoring — even if undecided.
- **A test environment** where your engineers can run the agent's tests with synthetic data.
- **What already exists**: AI or data policies, retention rules, incident procedures, existing approval flows.
- **A decision on the profile**: pilot first, or straight to production.

## The phases

| Phase | What the agent asks or does | What you decide or do | What it produces |
|---|---|---|---|
| **0 · Profile** | Pilot or production? For a pilot: end date, scope, which (P) items you defer, when Risk & Control joins | The profile; the Portfolio Owner signs a pilot | Profile section of the checklist |
| **1 · People** | Who holds each role; is the Framework Owner independent of implementation; who owns each hand-off between teams | Confirm names | Section A, as a draft for confirmation; gaps flagged |
| **2 · Stack map** | For each of the 21 requirements, which product will provide it — or "gap" | The intended stack | A map that becomes the first column of the substrate binding |
| **3 · Measure first** | Writes the tests for telemetry (R8) and budgets (R17); drafts the price table and budget defaults | Your engineers run the tests; you approve the drafts | Evidence rows R8, R17 |
| **4 · Engine and people** | Writes the failure-class tests for the orchestrator (R3) and the escalation tests for people (R19) | Engineers run them; HR / directory owner confirms the directory | Evidence rows R3, R19 |
| **5 · The rest** | Tests for the remaining requirements you keep; for any you drop or change, one line on what it was meant to prevent | Run tests; keep, change or drop | Demonstration log; adaptation register |
| **6 · Documents** | Drafts each of the 18 documents and asks its owner the questions to complete it | Each owner corrects and approves theirs | Approved documents |
| **7 · Binding** | Fills the substrate binding and the operations skill from phases 2–5 | Platform Operator approves | The two files the Builder and every agent read |
| **8 · Regression bank** | Builds golden cases from the worked examples, with the facts each role must produce | Framework Architect approves | Bank v1 |
| **9 · Dry run** | Helps choose a friendly owner and a small real task; observes the Builder's session and the first supervised run | You run it | Dry-run evidence; first Builder corrections |
| **10 · Go-live** | Assembles what was shown, what was not, and the adaptations | Your go-live decision | Platform ready — pilot or production |

The agent works one topic at a time and closes each only when its owner closes it.

## How evidence works

The agent separates **shown** from **not yet shown**: a requirement is shown when a test's output says so. "We configured it" is recorded as not yet shown — not as a failure. What you accept as not yet shown is your call; the record just makes it visible.

## Pilot or production

The framework suggests what a pilot can defer — rows marked **(P)**: the classifier, tamper-evident audit, independent monitoring, part of the orchestrator tests, the four budget levels, an approved enterprise policy, the Risk & Control signature — and recommends never deferring telemetry, the registry, the ability to pause, the logs, or any legal obligation. You decide. Every instance on a pilot platform runs with agents only preparing and people deciding. The agent keeps the list of what was deferred.

## A taste of the work

> **Readiness Agent:** The framework asks that an agent cannot write an approval. Which product will hold approvals?
> **Platform Operator:** Approvals in Teams through a flow. And agents run under one service account — we're not changing that for now.
> **Readiness Agent:** Understood. One line for the record: per-agent identity is there so you can tell which agent did what, and so one agent's permissions can't be used by another. I've written it in the adaptation register as your decision. The test I'll write is: the flow refuses an approval from the service account, with the attempt logged. Can your engineer run it in the test tenant?
> **Platform Operator:** Yes.

Notice: the agent said once what the recommendation was for, recorded the choice, and adapted the test to your design. It will not raise it again.

## While the agent is new

The Readiness Agent starts in pilot itself: the Platform Operator reviews every draft and every test before it is used, and checks each log row against its evidence. Your corrections are recorded and improve the agent for the next platform.

## After sign-off

The agent steps back. It returns when the platform changes substantially or a framework release touches the substrate contract — to re-run only the rows affected. From here the Builder takes over, one project or process at a time.

## Frequently asked

**Can we skip a requirement?** Yes. You own the design. The agent tells you once what it was meant to prevent and records your decision in the adaptation register.

**Our product does it "automatically". Do we still need a test?** Yes. The test is what proves it in your configuration.

**Who writes the enterprise policy?** The Risk & Control function with the Portfolio Owner. The agent drafts questions and a first version for them to rewrite.

**What if a test fails?** It is recorded as not yet shown. You fix and re-run, accept it as it is, or change the requirement — your call.
