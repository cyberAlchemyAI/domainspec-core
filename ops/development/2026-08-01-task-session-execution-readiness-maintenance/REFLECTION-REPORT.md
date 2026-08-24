# Task Session execution-readiness reflection

## Reflection context

- Target sigil: `task-session` 0.8.1.
- Trigger: manual maintainer correction after repeated repair/confirmation turns.
- Current package: `ops/development/2026-08-01-intent-route-arcanum-addon/`.
- Signals available: 136 Task Session rows before this observation; the repository reflection state records 31 related Task Session workflow gaps and two output-contract drift events.
- Inventory lookup: ready; selected evidence is recorded in `INVENTORY-LOOKUP-PACKET.json`.
- Mutation authority: none.

## Finding

Task Session is not the source of the readiness failure. It is the first stage
that correctly enforces a contract the producer already promised to satisfy.

The canonical Invoke Plan contract requires every mutation-capable SWU to bind
the terminal source receipt, exact closeout target inventory, baselines,
admitted deltas, owner validation, expected owner receipt, and deterministic
successor before handoff. The current package nevertheless reports Plan pass
while:

1. `SWU-IRO-001` permits only evidence-directory writes, but its Execution Pack
   says Invoke Refresh will update planning state without naming those planning
   targets or their baselines.
2. `CLOSEOUT-SYNC.md` lists delta classes but not the exact targets, baseline
   digests, owner command, receipt schema, or successor binding.
3. The task contract, Execution Pack, and Dispatch disagree on the terminal
   receipt fields. The Dispatch's generic `DECISION-RECEIPT.json` also omits
   Decision Gate's option-admissibility and durable-decision artifacts.
4. Dispatch Spec validated route shape, not Task Session execution readiness.
5. No Work Pack Readiness Audit v2 projection was generated for this package,
   even though that existing spell owns the producer-side dry-run boundary.

The perceived loop has a separate diagnostic cause: Task Session's policy
evaluator returns on the first failed closeout input and emits an empty
`diagnostics` array. Correct blockers therefore arrive serially instead of as
one owner-grouped repair set.

## Evidence threshold

The manual trigger is sufficient for reflection. The direction is also backed
by the prior closeout-sync signal and the Inventory entries on late producer
discovery and Work Pack Readiness Audit. Existing live fixture results show:

- Task Session: `25/25` governance, `11/11` nearest-resolution, and `23/23`
  mutation-admission cases pass.
- Work Pack Readiness Audit: `10/10` v1 and `3/3` v2 tests pass, including stable
  pre-route codes and deterministic projection.
- Sigil Maintenance Loop: six scenarios and four live regimes pass.

These results prove the reusable harnesses, not the current package's
readiness.

## Proposed iterations

### TS-DIAG-001 — aggregate stable Task Session diagnostics

- Owner: `task-session` through a later explicitly approved
  `sigil-development` run.
- Change: keep every current `BLOCK` rule, but evaluate all pre-write closeout
  inputs before returning. Populate the existing diagnostics surface with
  deterministic codes for every missing, stale, expanded, forbidden, or
  mismatched input, grouped as `producer_handoff`, `mutation_admission`,
  `closeout_sync`, and `authorization`. Each group names its repair owner.
- Prevention effect: one dry run returns the complete bounded repair set
  instead of revealing one predictable defect per re-entry.
- Compatibility: additive diagnostics only; verdicts, authority, mutation
  admission, owner boundaries, and closeout semantics do not change.
- Fixtures: incomplete-all returns the full ordered code set; stale baseline,
  glob-only output, undeclared producer artifact, and forbidden closeout target
  remain `BLOCK`; complete positive cases retain their current receipts.
- Priority: medium. This improves operator clarity but does not repair the
  producer false-positive.

### INVOKE-WPRA-001 — derive Plan handoff from readiness projection

- Owner: `invoke` through `spellcraft`, not this sigil-maintenance mutation.
- Change: before Plan may report `Task Session closeout sync: pass` or
  `pass-for-handoff`, generate and validate a Work Pack Readiness Audit v2
  configuration for the selected frontier. The status must be derived from the
  audit report, not authored as prose. A block produces an exact
  `invoke:refresh` signal pack.
- Prevention effect: the package is rejected at the producer boundary, before
  Task Session and before another confirmation request.
- Compatibility: Plan remains non-mutating; the readiness audit selects and
  executes nothing and grants no authority.
- Fixtures: use this intent-route package as the negative case; add one repaired
  positive case with exact receipt outputs, write algebra, closeout inventory,
  baselines, schemas, validation, and successor policy.
- Priority: high and primary.

### IRO-REFRESH-001 — repair this package once

- Owner: `invoke:refresh` after a separate approved package-repair scope.
- Change: reconcile the task, Execution Pack, and Dispatch terminal outputs;
  declare Decision Gate's complete producer artifacts; split execution outputs
  from Invoke-owned closeout targets; bind exact closeout targets, baselines,
  schemas, commands, delta classes, and successor rules; then run WPRA v2.
- Prevention effect: one bounded refresh replaces repeated Task Session repair
  attempts.
- Compatibility: changes planning/evidence only; it does not implement,
  publish, generate, install, or integrate the resolver.
- Priority: high after `INVOKE-WPRA-001` defines the producer rule, or as a
  one-off current-package repair using the existing WPRA v2 contract.

## Rejected changes

- Do not weaken missing-closeout or mutation-admission `BLOCK` verdicts.
- Do not treat Dispatch Spec pass as execution readiness.
- Do not infer exact files from `<run-id>/**`.
- Do not treat persistent evidence writes as standalone non-mutating work.
- Do not copy Decision Gate or Work Pack Readiness Audit logic into Task
  Session.
- Do not let Task Session edit Invoke-owned planning artifacts.
- Do not combine Task Session, Invoke, and Decision Gate changes into one
  canonical mutation.

## Maintenance-loop validation residue

The current Sigil Maintenance Loop harness returns `VALIDATION=pass` while its
four example outputs report `QUALITY_BAR_STATUS=not_checked` and zero quality
or anti-pattern criteria. This does not change the diagnosis above, but a
separate Spellcraft maintenance task should make reusable-behavior validation
fail or explicitly justify `not-applicable` when those criteria are empty.

## Decision

- Reflection decision: `targeted-update` for `TS-DIAG-001` only.
- Approved change scope: none.
- Canonical mutation: blocked pending explicit approval.
- Primary workflow repair: `INVOKE-WPRA-001` via Spellcraft.
- Current package repair: `IRO-REFRESH-001` via one bounded Invoke Refresh.

