# Decision Gate — Whisper Lifecycle Acceptance

## Blocked work

`SWU-WEG-001` cannot modify public Whisper until the W0 entry gate has a Spellcraft acceptance receipt. Dispatch validation already passes; the missing decision is whether to route the approved Invoke design to Spellcraft now.

## Decision question

How should the Whisper editorial-gate handoff proceed?

### Option 1 — Accept and route to Spellcraft design (recommended)

- Benefit: Spellcraft reviews the revision boundary, phase contract, public/private split, and selected SWU, then returns the required owner receipt.
- Cost/risk: one lifecycle review step before fixtures; Spellcraft may flag a design correction.
- Reversibility: high. This authorizes proposal/design review, not Whisper implementation or promotion.
- Downstream impact: if the owner receipt passes, Task Session can rebuild context and execute SWU-WEG-001.
- Exact route: `spellcraft:design:proposal-only` for the Whisper editorial-gate hardening handoff.

### Option 2 — Return the package for design revision

- Benefit: permits another Invoke/author review before lifecycle acceptance.
- Cost/risk: delays executable evidence and requires the user to name what should change.
- Reversibility: high.
- Downstream impact: SWU-WEG-001 stays blocked; the work pack must be refreshed after revision.

### Option 3 — Defer or stop

- Benefit: no further mutation or lifecycle work.
- Cost/risk: Whisper retains the identified false-positive editorial-readiness gap.
- Reversibility: work can resume later from this evidence.
- Downstream impact: Task Session remains blocked.

### Explain / more context

Non-committal. Expands why Spellcraft acceptance is distinct from Task Session authorization and then presents the same options again.

## Current result

- Result: `PASS`
- Selected option: Option 1 — accept and route to `spellcraft:design:proposal-only`
- Rationale: obtains the exact lifecycle-owner receipt required by W0 without authorizing Whisper implementation or transport promotion.
- Decision source: user reply `1`
- Remaining blockers: 0 for the Spellcraft owner hop
- Mutation after gate: none
- Recorded: 2026-07-22
