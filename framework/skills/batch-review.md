# Skill — batch review (Process Reviewer)

## When
At the batch rule (n audits or n days, whichever first) or a P0 audit alone.

## Order
1. **Previous rulings first.** What was approved and is in flight; what was closed and must not be re-proposed; which falsifiable criteria expire in this batch and with what result.
2. **Read the batch** of audits in one context; list recurrences across audits: the same observation, the same series moving the same way, the same human reason.
3. **Dedupe by axis.** One proposal per axis; a new finding on an axis with an approved proposal in flight is merged into it, not opened.
4. **Write proposals**, bounded per batch, each with: axis (local / framework) · shape (project / process / both) · evidence (the audits and the series) · what it moves, (a) or (b), and why (c) does not worsen · the series that will show it · the falsifiable criterion and its date. No series, no proposal.
5. **Trainable skills.** For each learning section it may edit: announce the intended diff on the audit, apply it with a dated marker inside the section only, verify after that nothing outside the section changed; schedule the revert check for the window.
6. **Publish** the batch result on every audit of the batch (including "no proposals"), so no audit is left silently unconsumed.

## Rules
- Patterns seen once are noted, not proposed; seen in two or more audits, proposed.
- A cost finding without its quality pair from the same period is not a proposal.
- Framework-axis proposals are forwarded, never executed here.
- A dead session leaves a "no result" on each audit — the orchestrator writes it if the Reviewer could not.
