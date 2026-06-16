# Design Review (Adversarial): Mutation Execution Mechanics — VERDICT: FLAG

Artifact: /home/vrondelli/projects/domainspec-core/implementation/domainspec/docs/features/ui-prototyping-studio/development/refinement-runs/20260615T205403Z-mutation-execution-mechanics/stages/07-design-review.md

## A. Determinism preserved where claimed?
- **A1 [BLOCK-LOCAL]** The design reads `currentHtml` and stages/commits `candidateHtml`, but `StudioSessionStorePort` (ports.ts) has ZERO HTML read/write methods. `htmlArtifactRef` (models.ts:136, generate-variants.ts:56) is a synthetic path string nothing ever writes bytes to or reads. The "4th write" the design counts does not exist as a write surface. Engine input cannot be populated; recorder has nothing to commit.
- **A2 [FLAG]** V8 double-run verdict-hash equality catches FLAPPING nondeterminism, not LATENT (same `Date.now()` ms twice, seeded RNG). It cannot establish the replay-by-verdict purity INV-6 leans on. Restate as flap-detection + capability-denial (throwing frozen clock/RNG).
- **A3 [NOTE]** D4 odId-into-checksum re-baseline is correctly disclosed; add a migration/version stamp (invalidates existing stored checksums).

## B. Can validators be fooled?
- **B1 [BLOCK-LOCAL]** V3's `ChangedSet` = symmetric set-diff of `odIndex` (od-id-bearing nodes ONLY). Every change to un-anchored markup (wrappers, siblings, `<style>`, inline `style=`, skeleton, meta) is invisible to V3 and admitted. The scope fence has a hole the width of the un-anchored DOM — most of a prototype. Falsifies C's odid/auditability scores against the non-cooperative proposer the design defines. Fix: whole-tree canonical diff, attribute each change to nearest owning od-id, reject undominated change.
- **B2 [FLAG]** V2+V5 prove "anchor touched + structurally plausible," not "intent realized" or "only the right thing changed." Combined with B1, validators pass while the real (wrong) change hides in un-anchored markup. Add this intent-fidelity gap to the §8 budget (currently prices only proposal non-determinism).
- **B3 [FLAG]** V9's `B(taskCount)`, `k`, `c`, and V3's `S` define fence strength but have no proposed defaults/calibration. Fail-closed at an unknown threshold is not auditable.

## C. Apply state machine complete?
- **C1 [BLOCK-LOCAL]** New `RevisionApplied` staged-candidate wait-state is under-specified: persistence? single-flight per head? expiry/abandon transition? stale-stage rejection? A crash/walk-away leaves an undefined state; the failure model only covers proposer fail at propose time.
- **C2 [FLAG]** D11 "all-or-nothing" relies on compensation that is deferred as RESIDUE-A; today the post-check (apply-approved-batch.ts:144-155) detects-and-throws, does NOT roll back, and the design adds a 4th write in front. Port has `appendRevision` but no `removeRevision` — compensation is not even expressible. Pull into this plan; name rollback order.
- **C3 [FLAG / INV-4]** D13 hash-bound accept closes seen≠recorded (good) but does not re-check `BATCH_STALE_FOR_HEAD` at the new accept-diff gate; the two-gate window reopens staleness.
- **C4 [NOTE]** Two-gate split via dormant `RevisionApplied` (verified present/unused, models.ts:18) correctly fixes the approve-then-generate sequencing problem.

## D. DiffSummary genuinely honest?
- **D1 [FLAG]** Deleting count-tally `buildDiffSummary` (verified dishonest, apply-approved-batch.ts:165-187) is real progress, but fragments/counts derive from `odIndex` (same root as B1), so the human "saw the diff" of anchored elements while un-anchored changes are invisible — a subtler dishonesty. Fix couples to B1: reject (whole-tree V3) or surface an "unattributed change" bucket.
- **D2 [NOTE]** candidateHtmlHash binding + GAP-2 replay-by-record sound; RESIDUE-D degrade honestly flagged.

## E. Honors INV-3/4/5/6/8?
Design admits (lines 438-440) the INV-numeric→meaning mapping is INFERRED from G-codes; define stage uses G1-G9, never INV-*. INV-3(G2) PASS; INV-4(G4) FLAG (C3); INV-5(G5) FLAG (C2, no removeRevision); INV-6(G6) FLAG (A1/A2); INV-8(G7) PASS w/ B2 budget caveat; saw-the-diff FLAG (C1/D1). Fix: cite real INV artifacts (RESIDUE-G) or restate in citable G-codes — honoring a guessed mapping is not honoring the invariant.

## F. Engine contract precise enough?
- **F1 [FLAG]** `promptHash` claims to hash the whole `ProposeInput`, but `componentLibrary?: unknown` + free-text + unpinned JSON canonical form means the hash is non-recomputable by an auditor. Pin canonical serialization; type `componentLibrary`.
- **F2 [NOTE]** Value-in/value-out, engine forbidden store/clock/append, advisory self-preview recomputed authoritatively — sound and testable.

## Required before plan
BLOCK-LOCAL: (1) add artifact content port (readHtml/stageHtml/commitHtml) — also unblocks C2; (2) V3 whole-tree change-detection; (3) specify RevisionApplied lifecycle.
FLAG-decide: A2, C2 (pull RESIDUE-A in + removeRevision port), C3, D1+B2 budget, F1, E/RESIDUE-G.
Buildable after fixes 1-3. The RESIDUE-B spike must now also exercise B1's whole-tree scope diff, not just V3/V5 tightness.