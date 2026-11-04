# Working with the Builder — a guide for the person who owns the work

You have a piece of work and you want AI agents to take part of it off people's hands. The **Builder** is the agent that sets this up **with you**. It does not do the work; it builds the system that will — and, depending on the work, it takes one of three paths (below). This guide tells you what to expect, what to bring, and what you will have at the end.

## What you get

At the end of the sessions you have a **running instance**: a set of agents with clear jobs, the rules they follow, the checks that catch their mistakes, the points where a person decides, a budget, and a record of everything they do. Not a report about how it could work — the thing itself, ready for a first supervised run.

## What it is not

- It is not a chatbot that does your task while you watch.
- It will not invent your rules. If something is undecided, it asks you, or writes it down as open.
- It will not agree to automate something that cannot be checked. Saying "this is not ready to automate" is a valid and useful outcome.

## Three paths

| Your work | What the Builder does | Who carries on |
|---|---|---|
| **A project** — it ends (a launch, a redesign, a business case) | Sets the project up: its stage (idea, valued, planned…), rules, plan, people, budget | The **architect** agent runs the project with you |
| **A simple process** — it repeats, and you can say now how each case is decided | Defines the process with you in the sessions and runs the first cases with people approving everything | The process runs; you review it periodically |
| **A complex process** — it repeats, but the rules need analysis, several teams or approvers are involved, several systems are touched, the risk is high, or you want a lot of autonomy | Sets up a **project whose result is the process**. The architect runs that project: analyses cases, writes the rules, builds the checks, tests them. When the project closes, the process is born and goes through its first supervised run | First the architect (the project), then the process itself |

The Builder decides the path with you in step 2 and writes down why.

**While the Builder is new**, a member of the framework team sits in on your sessions and checks the result before handover; your project or process starts as a pilot. That is how the Builder learns; it is not a judgement on your work.

## Before you start — bring these

- **Two or three real examples** of the work: a past project's outputs, or a handful of recent cases (a typical one and a difficult one).
- **What "correct" means to you**, as concretely as you can: "the numbers balance", "every rejection cites the policy clause", "the plan covers every department in the brief".
- **Who is involved**: who approves what, who stands in when they are away, who is above them.
- **Where things live**: the folders, mailboxes, meetings and systems the work depends on.
- **Rough numbers**: how long the work takes today, how much it costs, how often it goes wrong.
- **Your calendar**: you will be asked to commit to a regular review, with a date.
- **Your risk contact** — the Risk & Control function, whichever team your organisation designates for it —, and anything that already governs this work: policies, regulatory constraints, a data-protection assessment if one exists. For a process that decides about people, legal will be asked a few questions; bring them in early.

You can stop at any point; nothing is lost — every decision is written down as it is made.

## The sessions, step by step

The Builder works **one topic at a time** and does not move on until you have closed it. It will push back if something does not hold together; that is its job.

| Step | What the Builder asks you | What you decide | What it writes |
|---|---|---|---|
| **0 · Your view** | "Tell me about this work as you would to a new colleague." | Nothing yet — it restates your view until you agree with it. | The work's entry in the company registry, marked *proposed* |
| **1 · Can it be checked? Is it allowed?** | Whether the company's AI policy allows it at all. For each thing the work produces: how would you know, without opinion, that it is right? In what form does it exist? Which sources does it need? Who rules on changes, and how often? For a process: the risk questions (see below) | **Go or no-go.** For a process, with Risk & Control, the maximum autonomy | The viability record; the policy rules that apply; for a process, the risk assessment |
| **2 · Which path?** | "Does this end, or does it repeat?" If it repeats: "Can you tell me now how each kind of case is decided?" — and whether several teams, approvers or systems are involved, or the risk is high | Project, simple process, or complex process (a project that will produce the process). For a project, the stage it starts at | The path and why; for a complex process, two registry entries — the project and the future process |
| **3 · The rules** | Purpose, what wins when good options conflict, what must never happen, what has already been decided, the checkable statements. For a simple process: how a typical and a difficult case are handled. For a complex process: what the defining project must find out and deliver | Every rule, in your words — or, for a complex process, the questions the project must answer | The spec or process definition; one record per decision you had already taken |
| **4 · The people and the controls** | Who approves what leaves the company or cannot be undone, and above what amount? Their deputy, their superior? Who is trained to oversee this? Which cases must always go to a person? Who must never approve their own work? | The approval points, who holds them, and the rules that always need a person | Who may do what; who is called, by when, and who comes next; the checks each output must pass |
| **5 · Money and time** | What does this cost and take today? What will you spend on agents per item and per month? | Budgets | Budget and the "before" picture to measure against |
| **6 · Information** | Where are the documents, who owns them, how long are they kept? What do people know that is not written down? | What agents may read | The information map; which mail and meetings the system may learn from |
| **7 · Generation** | — | — | All the instance's files, then a checklist run item by item; anything failing sends you back to the step that owns it |
| **8 · First run** | — | You read the results with the Builder | Project: the first item. Simple process: a small batch of cases with **every** approval done by a person; thresholds set from what you saw. Complex process: the first item of the defining project — the process gets its own first run when the project delivers it |
| **9 · Handover** | Confirm the review date | — | The registry entry completed and set to *active*; your corrections to the Builder sent to the people who improve it |

## Risk and controls

This is the part that decides whether the system can be trusted. The Builder will not let you skip it.

**Is it allowed?** Your organisation has an AI policy: things agents must never decide alone, things they must always do (log, disclose, explain), and what they may do within limits. The Builder checks your work against it first and tells you which rules apply. Some work cannot be automated at all; better to know in the first hour.

**How risky is it? (processes)** You and the Risk & Control function answer six questions — regulatory exposure, financial impact, whether decisions can be undone, personal data, who suffers an error, reputation — and legal answers whether the process falls in a regulated high-risk category. The result is a **ceiling** you both sign:

| Ceiling | Meaning |
|---|---|
| **L0** | Agents prepare everything; a person decides every case. Always the starting point while legal questions are open |
| **L1** | Agents may close favourable, reversible cases below a threshold you set; everything else goes to a person |
| **L2** | Full routing by risk, with sampling — only with a signed justification |

The ceiling is a maximum, not a target. It is reviewed at every periodic review.

**What always goes to a person**, whatever any score says: adverse or irreversible decisions (a rejection, a payment above the threshold, anything sent to a customer that cannot be recalled) and the cases on your "always a person" list. Automatic closures happen only under a **standing approval** you sign once, with a threshold and an expiry date.

**The controls you will have**, in plain words:
- Every output is checked mechanically first (fields, amounts, dates, citations), then by a classifier for the criteria you stated, and only what is left by a reviewing agent. Nothing counts until it passes.
- Before any work starts, a critic agent checks that the instructions are complete and do not break policy.
- A sample of what was closed automatically is audited every period — some at random, some chosen because they look unusual — so the system never only checks what it chose to look at.
- Everything is logged and kept for the period your organisation requires.

**Your duties as an overseer.** You will be briefed on what the system can and cannot do. When you override a proposal, you give a reason — that is how the system learns. Approving everything in seconds is measured too: it shows that oversight has become a formality, and it is raised at the review. Nobody approves their own work.

**People outside.** Anything an agent produces for a customer or an employee says that automated support was used. Every adverse decision comes with an explanation the person can read and contest. Staff and their representatives are informed before the system is used at work, and a data-protection assessment is done where needed — these are on the Builder's checklist, not optional extras.

**What agents can read.** Only the sources on the information map. Mail and meeting transcripts are read by one agent only, which writes drafts that a person confirms; nothing in an email or a document can instruct the system.

**When something goes wrong.** Containment is graded: a single session is frozen; or the work drops to "prepare only" (ceiling L0); or new work is paused; or, for a serious incident, the whole instance is quarantined. Each step is recorded with who lifted it. Incidents are registered, and reporting to providers or authorities is handled by the platform team as your legal function has set it up.

## A taste of a session

> **Builder:** For the expense claims: how would you know, without opinion, that a reimbursed claim was right?
> **Owner:** Well, the approver would agree with it.
> **Builder:** That is a judgement, not a check — two approvers could disagree. What would they look at?
> **Owner:** That there's a receipt, the amount is under the limit for the category, and it's not older than 60 days.
> **Builder:** Those three can be checked mechanically. I'll write them as criteria A1–A3. Is there anything an approver looks at that is *not* on that list?
> **Owner:** If a customer is named in the description, we always look — gifts are sensitive.
> **Builder:** Then that becomes a rule that always sends the claim to a person, whatever any score says. Closing this topic?
> **Owner:** Yes.

Notice what happened: a vague answer became checkable criteria, and a piece of judgement that cannot be checked became a rule that keeps a person in the loop.

## After the Builder leaves

- The agents run; you are called only where a decision is yours, with the decision prepared, a deadline, and a deputy behind you.
- A **process assistant** answers "where is this?" and lets you approve, amend or pause.
- An **architect** agent is your contact for anything about *what* is done and *why*.
- At each **review**, you see what the system proposes to improve and decide: approve, merge into another proposal, or close. Nothing is "deferred".
- If your review lapses or you leave, the system slows itself to "prepare only" until someone owns it again. It never keeps running unowned.

## Frequently asked

**What if I don't know an answer?** Say so. The Builder writes it as an open question with a name next to it, or as a first piece of work that will answer it.

**Can we start without all the rules?** Yes. A project can start at the idea or business-case stage and earn its rules as it goes. A process whose rules are not clear yet is a complex process: it starts as a project that works them out, and only then runs cases.

**My process is simple today but will grow.** Start it simple. When it needs another approver, another system or more autonomy, that change is made through a project, like any change to the process.

**Will it send anything outside the company on its own?** Only what a person with the authority has approved — per case, or once in advance for routine, favourable, reversible cases below a threshold you set and sign.

**Can we start with a pilot?** Yes. A pilot has an end date and a small scope, and in it the agents only prepare: a person decides every case and approves anything that leaves the company. Some controls can come later, and the Risk & Control function can join later, but measurement, the registry, the ability to pause and every legal obligation are there from day one. To move from pilot to production, everything that was deferred has to be closed.

**Who is responsible if an agent gets something wrong?** The owner of the instance answers for its outcomes; whoever approved a decision answers for that approval. The agents answer for nothing — which is why every decision, approval and override is recorded with who made it.

**Can the risk team stop it?** Yes. The Risk & Control function co-signs the ceiling and the standing approvals, and can lower the ceiling or pause the instance at any time; at the portfolio review, the governance function can degrade or retire it.

**What if the Builder gets something wrong?** Correct it. Every correction you make is recorded and goes to the people who improve the Builder, so the next person does not hit the same problem.
