# Invoke Refresh Report: Arcanum Add-on SWU Re-entry Repair

## Identity

- Evidence date: `2026-07-30`
- Activation source: `direct-user`
- Mutation mode: `apply-approved`
- Mutation mode source: `default-direct-user`
- Target owner: `resonantos-planning-owner`
- Target worktree:
  `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha-arcanum-addon-plan`
- Branch: `docs/arcanum-addon-invoke-plan`
- Source commit and `origin/dev`:
  `80dcd79677ad73b21dbaded12e0e9cd47aace82b`

## Result

- Phase status: `pass`
- Phase basis: exact refresh applied and validated; zero refresh-authoring
  blockers
- Handoff: ready for fresh independent exact-byte revalidation
- Work-pack gate: remains `block`
- Selected SWU: remains `none`
- Runtime/product/browser implementation: not started

## Source Signal

The confirmed repair revalidation admitted corpus
`5b5e79f5632b2e29e7a20e7ac4d9e92addef6f707e9525c71e7266c24349e4b0`
and returned one surviving MAJOR finding: `g-swu-reentry` was prose-only and no
executable SWU step consumed a fresh selection input.

## Applied Scope

Ten unique Plan targets were material-validated and byte-verified:

1. `plan/DISPATCH.json`
2. `plan/WORK-PACK.md`
3. `plan/EXECUTION-PACK.md`
4. `plan/work-pack/shared/CLOSEOUT-SYNC.md`
5. `plan/DISPATCH-TECHNIQUE-TRACE.md`
6. `plan/DISTILL-VALIDATION.md`
7. `plan/PLAN-RESULT.json`
8. `plan/PLAN-TRANSPORT.md`
9. `plan/work-pack/shared/SWU-SELECTION-RECEIPT.schema.json`
10. `plan/work-pack/shared/validate-swu-selection-reentry.mjs`

The final route has exactly 25 machine-bound SWU admissions. Joins, readiness,
and `s14-boot-post-refresh` have no independent selection input. Every terminal
SWU receipt must echo its selection ID and selection-receipt digest.

The runtime validator checks literal path/content identity, current dispatch,
Plan, work-pack, source, dependencies, and predecessor closeout; it atomically
claims one selection before starts. Replays and mismatches block with task
start, owner attempt, and mutation counters all zero.

## Material Evidence

- Primary package:
  `arcanum-addon-invoke-reentry-repair-20260730-v1`
- Primary digest:
  `820288a121d9fc9b57a2718d108b36d392ce277a09c004d6d2ae0da5e36384ab`
- Bounded path/content hardening package:
  `arcanum-addon-selection-path-repair-20260730-v2`
- Hardening digest:
  `cc281225d5f9733d591f87360b4e6e3e3ab64c278247133a7efb48b1ea6183b5`
- Both material receipts: `pass`
- Both mutation handoffs: `ready`
- Both applies: byte-verified

## Validation

- Dispatch Spec: pass
- Static selection validator: 25 exact admissions; 25 unique selection inputs;
  zero internal-node selections
- Validator self-test: mismatch, drift, expiry, predecessor closeout,
  manual/verification SWUs, internal BOOT postcondition, and replay covered
- Live validator test: exact selection accepted once; atomic replay rejected;
  path/content mismatch rejected
- Prior repair invariants: 25 exact producers, complete wave joins, typed
  lifecycle bindings, `selectedSWU: none`
- Planning JSON: all parsed
- Changed Markdown local targets: 6/6 pass
- Staged whitespace: pass
- `npm run docs:check`: pass
- `npm run test:docs`: 224/224 pass
- Target state: `HEAD == origin/dev ==
  80dcd79677ad73b21dbaded12e0e9cd47aace82b`; only the pre-existing untracked
  `development/` package remains

## Current Corpus

- File count: `77`
- Aggregate SHA-256:
  `5fad9693428f841a10cec7d2ee0c5e599826ea204a75ac57177fe70f55f466a0`
- Aggregate algorithm: sorted absolute-path `sha256sum` stream across
  `define/`, `design/`, and `plan/`, then SHA-256 of that stream

## Remaining Gates

- Audit: `B-DESIGN-001` remains open until fresh independent exact-byte
  revalidation passes over the 77-file corpus above.
- Target lifecycle: `B-GOV-001`, `B-BOOT-001`, `B-OWNER-001`,
  `B-ADAPTER-001`, and `B-RETENTION-001` remain independent.
- Browser: not eligible before implementation plus deterministic/security
  closure.

## Next Route

Run the prepared two-lane exact-byte revalidation. If it passes,
`B-DESIGN-001` can close; Task Session must then resolve governance and
Bootstrap compatibility before selecting the first implementation SWU.
