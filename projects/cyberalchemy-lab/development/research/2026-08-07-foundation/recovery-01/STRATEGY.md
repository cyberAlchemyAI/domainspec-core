# CyberAlchemy Lab Foundation Recovery Strategy

This is a confirmation-ready continuation proposal, not a registered dispatch
or execution authorization.

## Why a new dispatch is required

Run `run-001` is terminally blocked at `g-evidence-closure`. The host rejected
`spawn-0007`, the run-evidence validator confirms that its receipt is absent,
and Orchestrate forbids retrying a failed action implicitly. The existing
dispatch has therefore been closed with `exit_reason: error`.

## Minimal continuation

The continuation reuses immutable run-001 evidence and contains only three
sequential roles:

1. definition skeptic: complete the missing non-collapse review;
2. writer: create `findings.md` only after the review passes;
3. auditor: audit those findings, with one bounded writer-revision loop.

It does not rerun explorers or synthesis, retry the failed action, implement a
fixture or workbench surface, promote ontology meaning, ingest repository
research, publish, deploy, release, or perform Git work.

## Gates

- Exact candidate sheet must pass the live schema/readiness validator.
- Two independent tension verdicts must pass on the same sheet digest.
- New direct human confirmation is required before registration or spawning.
- Definition-review failure blocks the writer.
- Findings-audit failure blocks parent approval.
- Parent remains final approver.
