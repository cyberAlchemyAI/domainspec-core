---
id: plan-m2-wire-two-gate
run_id: 20260617-m2-wire-two-gate
step_id: s9-plan
capability_ref: invoke (plan)
status: proposal
complexity: medium
updatedAt: 2026-06-17
---

# Plan — build M2-wire (live two-gate apply)

Non-executed. One SWU **MW1** (3 sub-slices). Deps exist (two-gate engine, M0b port, M0c, M0a fields,
MR1 real HTML). No F2 dependency. **Chain dep: MW1's live path requires MR1-registered variants.**

## SWU — MW1: live two-gate apply `[algorithmic]`

### MW1-a — staged-candidate persistence (Tournament A)
- **Write scope:** `application/ports.ts` (+`infrastructure/file-studio-session-store.ts`).
- **Add:** `saveStagedCandidate(sessionId, {stagedRef, candidateHtmlHash, batchId})`,
  `getStagedCandidate(sessionId)`, `clearStagedCandidate(sessionId)` — a per-session record under a
  separate store key (StudioSession entity untouched).
- **Verify:** save/get/clear round-trip unit test.

### MW1-b — use-cases (the two gates)
- **Write scope:** `application/apply-and-stage.ts` (new), `application/accept-staged-revision.ts` (new),
  `application/discard-staged-revision.ts` (new), `application/studio-orchestration-module.ts` (wire,
  inject the ArtifactContentPort already plumbed in MR1).
- **applyAndStage({sessionId, batchId, candidateHtml, requestedBy}):** guard (baseline gate, batch
  approved, not stale, actor != system:auto); resolve `currentHtml` (head revision committed ref via
  readHtml, else baseline variant ref); `scopeOdIds = batch.tasks[].odId` (non-null); call
  `validateAndStage`; on REJECT throw/return REJECT (no write, stay MutationApproved); on NOT_REJECT
  `saveStagedCandidate` + set state `RevisionApplied` (head NOT advanced); compute + return
  `DiffSummaryHonest` (od-id fragment diff via admission/canonicalize). **Edge:** no scope od-ids → REJECT;
  unresolvable currentHtml (stub variants) → clear error (chain dep on MR1).
- **acceptStagedRevision({sessionId, candidateHtmlHash, requestedBy}):** get staged; `acceptStaged`
  (commit; CANDIDATE_HASH_MISMATCH / NO_STAGED_CANDIDATE fail-closed); append
  `RevisionManifestEntry{candidateHtmlHash, diffSummaryHonest, htmlArtifactRef=committedRef}`; head++;
  state `RevisionRecorded`; `clearStagedCandidate`. Exactly-one-revision invariant (mirror legacy apply).
- **discardStagedRevision({sessionId}):** `discardStaged`; `clearStagedCandidate`; state `MutationApproved`.
- **Verify:** the §4 toy-game as unit/slice tests (ADMIT/REJECT/ACCEPT/MISMATCH/DISCARD + idempotency).

### MW1-c — CLI verbs
- **Write scope:** `cli/studio.ts`.
- `studio apply <sid> <bid> --candidate-from <file>` → applyAndStage (reads full mutated HTML).
- `studio accept <sid>` → acceptStagedRevision (reads staged candidateHtmlHash).
- `studio discard <sid>` → discardStagedRevision.
- Keep `batch apply` (single-gate) as **legacy/deprecated** (the SKILL can stop teaching it).
- **Verify:** e2e — register (MR1) → baseline → approve → apply --candidate-from (in-scope) → accept →
  RevisionRecorded with honest diff; out-of-scope candidate → REJECT; accept wrong hash → mismatch.

## Implementation-layering
- **L0** MW1-a persistence — promotion: round-trip test.
- **L1** MW1-b use-cases + honest diff — promotion: the 5 toy-game fixtures + idempotency.
- **L2** MW1-c CLI + e2e — promotion: the end-to-end two-gate run green.

## Validation strategy
unit (persistence, use-cases) → slice (toy-game fixtures) → e2e (full two-gate loop over MR1-registered
variants) → the §4 fixtures as regression guards.

## Follow-ons (post-MW1)
- Update the live SKILL: `accept`/`discard` now EXIST; `apply` is two-gate (remove the "do not exist yet"
  + single-gate caveat). [SKILL refresh]
- Update the harness: an `accept`/`discard`/`apply --candidate-from` aware transcript scenario.
- `preview --annotate` (SWU-P) so the human SEES the honest diff in a surface (still separate).

## Residue / gaps
- Chain dep MR1 → MW1 (live path needs real registered HTML).
- `currentHtml` for a multi-revision chain = the head revision's committed ref; ensure each accepted
  revision stores its `htmlArtifactRef` (committed ref) so the next apply resolves it.

## Next route
`task-session` to build MW1 (a → b → c). No F2 dependency.
