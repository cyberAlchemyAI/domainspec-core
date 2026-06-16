---
id: refine-result-mutation-execution-mechanics
project: ui-prototyping-studio
title: "Refine RESULT — Mutation Execution Mechanics"
status: proposal
node_type: refine-result
run_id: 20260615-mutation-execution-mechanics
updatedAt: 2026-06-15
---

# Refine RESULT — Mutation Execution Mechanics

**Chosen model:** Approach C — agentic-propose behind the `studio` CLI seam, deterministic-validate in the pure core: generation is left non-deterministic and expressive in the one impure lane (Claude Code), and determinism is recovered at the *admission* boundary inside the pure core, so a revision becomes head only after a pure clock-free validator suite admits it and a human accepts the exact staged candidate they previewed.
**Status:** flag · **Guardrail:** PROPOSAL — no SPEC/operations/architecture mutation without operator approval.

## Decisions
- Chosen model: Approach C (agentic-propose behind the studio CLI seam, deterministic-validate in the pure core); A and B recorded as Pareto-frontier residue, reachable as config (C-2 to A, C-1 to B), not redesign.
- Determinism lives at the ADMISSION boundary in the pure validator/recorder lane (D3), never in the producer or persist-step alone; enforced by purity obligations (D3a), one shared canonicalizer across the seam (D3b), and replay-by-verdict not replay-by-production (D3c).
- Schema: GAP-1 (odId + MutationChangeType union on MutationTask, D4 checksum re-baseline), DiffSummaryHonest + per-od-id OdDiffFragment with buildDiffSummary deleted (D5), GAP-2 (htmlArtifactRef + candidateHtmlHash + ExecutionProvenance on RevisionManifestEntry, F9/D6).
- Validator set V1-V9b adopted with required/soft criticality, fixed deterministic run order, composite fail-closed admission rule (D14); two A-mechanics imported (V9b + same-od-id conflict).
- Apply state machine: two gates (approve-intent + accept-diff) via the activated dormant RevisionApplied preview state (D7/D8); fail-closed reject + bounded retry (D9/D10); produce-then-persist whole-batch all-or-nothing (D11/D12); hash-bound idempotency-at-verdict so seen==recorded (D13); value-in/value-out engine contract (D15).
- Toy game falsified two load-bearing C claims on a one-card prototype: V3 scope fence was odIndex-blind to un-anchored markup (TG-1, repaired to whole-tree diff) and acceptanceText is never machine-checked (TG-2, priced in budget); plus TG-3 V2 false-rejects idiomatic CSS sizing (deferred to spike R2-a/R2-b).
- Plan is 7 layers MWU->hardening with the three BLOCK-LOCAL fixes (A1 artifact port, B1 whole-tree V3, C1 RevisionApplied lifecycle) in the early layers; every contract change tagged [PROPOSAL]; nothing executed.

## Residue / open
- RESIDUE-B (the C-1 spike) is the single gating action between 'C designed' and 'C trusted': must build/stress-test the whole-tree od-id-attributed V3 fence, decide V2 R2-a vs R2-b, and commit+report calibration constants S/B/k/c on real comment workloads. Owner: bounded local spike; GAP-R1 external pass is the named fallback if it stalls.
- TG-2/s7-B2 intent-fidelity gap accepted as a ceiling, not closed: admit != acceptanceText satisfied; quantitative criteria like '44x44px' are judged only by the human eye at the accept-diff gate, never by the pure lane (no geometry/CSS-layout check). Priced in the determinism budget.
- RESIDUE-A recorder atomicity/compensation: upgrade VARIANT_GENERATION_COUNT_MISMATCH from detect-only to compensating rollback; requires a removeRevision port that does not exist today. Owner: recorder lane (Layer 3).
- RESIDUE-C shared canonicalizer (Dom/odIndex/canonicalizerVersion) must be one module used on both sides of the seam; dominant source of accidental non-determinism. Owner: Layer 0.
- RESIDUE-G governance IDs (INV-3/4/5/6/8, DEC-* ids, OQ-2) are grep-negative; the design honors an INFERRED INV->G mapping. Must land citable artifacts or restate in citable G-codes. Owner: Layer 6.
- RESIDUE-D selector-only degrade fidelity when odId is null (V2/V3/V4 and OdDiffFragment degrade to selector matching) — lower DC4 posture, surfaced in provenance.
- Deferred options dormant with triggers: O1 repair path (revisit if retry-churn telemetry shows a dominant mechanically-fixable failure class), O2 A-fallback (enumerable workload), O3 B-fallback (V3 cannot be made deterministic).

## Recommended next routes
- RESIDUE-B C-1 spike (gating): run a bounded local design spike to build and stress-test the whole-tree od-id-attributed V3 fence (R1), decide V2 R2-a vs R2-b (TG-3), and commit+report S/B/k/c calibration on real comment workloads. This is the next action before any implementation; if it stalls, confirm GAP-R1 (deterministic validation of LLM-generated artifacts) as a separate bounded external research pass.
- task-session: execute Layer 0 (substrate) as the first bounded implementation task — schema migrations (GAP-1/GAP-2/DiffSummaryHonest/ExecutionProvenance), the artifact content port (readHtml/stageHtml/commitHtml/discardStagedHtml, closing A1), and the shared canonicalizer (RESIDUE-C). Closes the unbuildable-substrate finding and unblocks everything downstream.
- task-session: Layer 1 (MWU) — the pure deterministic validator suite + composite verdict + whole-tree V3 fence, with the toy-game falsifiers (TG-1/Case 2-B, Case 2-A, Case 1-A, TG-2/Case 1.3) landed as passing regression fixtures.
- decision-gate (or domainspec-decision-gate): resolve the 10 [PROPOSAL] gate items before canonical mutation — especially the RevisionApplied state semantics (persistence/single-flight/expiry), the V8 claim downgrade + capability-denial guard (A2), the ProposeInput canonical-serialization/promptHash contract (F1), and the D4 checksum re-baseline migration.
- domainspec-spec-feature / discovery promotion: land RESIDUE-G — promote the inferred INV->G governance mapping into citable INV-3/4/5/6/8 + DEC-* + OQ-2 artifacts, or restate the design in the G-codes (G1-G9) it can actually cite.

---

## RESULT — Mutation Execution Mechanics (refined synthesis)

**Refine target:** `mutation-execution-mechanics` · **Project:** `ui-prototyping-studio`
**Run:** `20260615T205403Z` · **Overall verdict:** FLAG (conditional pass — design is sound and coherent, but plannable only after three BLOCK-LOCAL fixes land and one spike resolves). **Nothing was executed.**

This is the refined synthesis of the s1–s9 chain, not a route proposal. It states the chosen execution model, where determinism lives, the schema changes, the validator set, and the apply state machine; then it is candid about what was *decided* versus *deferred*, including the two load-bearing claims the toy game falsified.

---

### 1. The chosen execution model (one sentence, then the lanes)

Let generation be non-deterministic and expressive **behind the CLI seam**, and **recover determinism at the ADMISSION boundary inside the pure core.** Four lanes, the seam between lane 2 and lanes 3–4 being the load-bearing boundary:

| Lane | Owner | Purity | Responsibility |
| --- | --- | --- | --- |
| 1. Synthesis | core | pure | comments → `MutationBatch` (checksummed) — unchanged |
| 2. Proposer (engine) | Claude Code | **impure (LLM)** | `propose(currentHtml, tasks, context) → candidateHtml + provenance`, behind the `studio` CLI seam |
| 3. Validator suite | core | **pure, clock-free** | `validate(...) → AdmissionVerdict` (V1–V9b) |
| 4. Recorder | core | pure-effectful | admit ⇒ persist HTML + append exactly-one revision + advance; reject ⇒ persist nothing |

Selected over A (deterministic typed-patch transformer) and B (full agentic regeneration). The s5 tournament found **no strict Pareto dominance** — all three are on the frontier — so C was selected on the equal-weight total (C 22.0 > B 19.5 > A 17.5) **plus** its structural resolution of the auditability-vs-expressiveness tension, with explicit demotion rules: **C-1** (validator unbuildable ⇒ flip to B) and **C-2** (workload enumerable ⇒ A). Both fallbacks are reachable as *configuration of the same machine*, not redesign.

### 2. Where determinism lives (the spine)

Determinism is **relocated, not abandoned** — it lives in the validator/recorder lane in the pure core, never in the producer and never in the persist step alone (D3). Three sub-commitments make it enforceable: D3a purity obligations (no `Date.now`/`Math.random`/fs/network in any validator; structural validators run over a canonical parse, not raw bytes); D3b **one shared canonicalizer used on both sides of the seam** (the dominant source of accidental non-determinism); D3c determinism is **at admission, not at production** — the *decision to admit* is replayable (V8), the *proposal* is not. This is the honest content of "auditability 4 not 5" and is priced as the determinism budget, not papered over.

### 3. Schema changes (all in `domain/models.ts`)

- **GAP-1:** add `odId: string | null` and replace `changeType: string` with the `MutationChangeType = "add"|"remove"|"change"` union on `MutationTask`. D4: `synthesize` copies `comment.target.odId` into the task; the batch `sha256` now incorporates `odId` — a one-time chain re-baseline requiring a checksum version stamp so old batches don't read as tampered.
- **Honest diff:** `buildDiffSummary(batch)` (which tallied `changeType` substrings *before any HTML exists*) is **deleted**. New `DiffSummaryHonest` with per-od-id `OdDiffFragment` units; counts are **derived** from `odIndex` set-diff, never from `changeType` (D5).
- **GAP-2:** add `htmlArtifactRef`, `candidateHtmlHash`, and `provenance: ExecutionProvenance` to `RevisionManifestEntry`. `ExecutionProvenance` (F9) carries the non-replayable proposer record (model, `promptHash`, input/output hashes) and the replayable validator verdicts (`verdictHash`, per-validator results) — turning replay-by-verdict and replay-by-record from claims into checkable records.

### 4. The validator set (admission contract)

Nine + one validators, fixed deterministic run order (V6 → V1 → V2/V4 → V3 → V7 → V9 → V9b → V5(soft) → V8), so the *first* failure code is itself reproducible. **Composite rule (D14):** all required pass ⇒ admit; any required fails ⇒ reject (fail-closed). V1 target-exists, V2 target-changed, **V3 no-out-of-scope-change (the crux)**, V4 od-id-preserved, V5 acceptance-proxy (**soft/pivotal**), V6 well-formed, V7 delta-injection escaping, V8 idempotency self-check, V9 diff-bounded, V9b ops-reconcile (optional, skipped if no ops). Two A-mechanics imported at low cost: V9b and the same-od-id static conflict check.

### 5. The apply state machine

Two gates, activating the dormant `RevisionApplied` state as the preview gate:

`MutationApproved` → **[propose]** (impure) → **[validate]** (pure; required-fail ⇒ REJECT, no write, stay `MutationApproved`) → **`RevisionApplied`** (candidate staged at a temp ref, NOT head; honest diff computed and shown — the real saw-the-diff moment) → human **accept-diff** (second gate) → **[record]** (atomic, all-or-nothing) → `RevisionRecorded`.

Decided here: D7/D8 two gates (approve-intent + accept-diff); D9 fail-closed reject; D10 bounded `maxProposeAttempts` retry; D11 produce-then-persist single commit point; D12 whole-batch all-or-nothing (no partial apply); D13 **idempotency-at-verdict** — the human accepts a specific `candidateHtmlHash` and record commits *exactly* that hash, so seen == recorded; D15 frozen `ProposeInput` envelope in / `ProposeOutput` candidate out, the engine forbidden the store/clock/append path.

### 6. What was DECIDED vs DEFERRED (be candid)

**Decided (resolved now):** the four lanes and the CLI seam (D1–D2); determinism-at-admission (D3a–c); the full schema delta (GAP-1, GAP-2, `DiffSummaryHonest`, `ExecutionProvenance`); the validator set and composite rule (V1–V9b, D14); the two-gate machine and its decisions (D7–D15); the engine value-in/value-out contract; B/A reachable as config (O2/O3).

**Falsified and repaired (the honest core of this run):** the s8 toy game ran the model on a one-card prototype and **falsified two load-bearing claims of C** on minimal input:
- **TG-1 / s7-B1 (BLOCK):** V3's scope fence as originally written computed `ChangedSet` from `odIndex` only, so it was **blind to all un-anchored markup** (`<style>`, `<head>`, `<h2>`, layout containers — most of a prototype). An adversarial proposer's `<style>`/`<h2>` edits were *admitted and hidden from the diff*. C's auditability/odid advantage over B was a fiction against a non-cooperative proposer. **Repaired:** V3 change-detection rewritten to a **whole-tree canonical diff with od-id attribution** — any change not dominated by a `TaskScope` od-id is rejected. odIndex is the attribution/display key, not the detection domain.
- **TG-2 / s7-B2 (FLAG):** the `acceptanceText` is **never machine-checked** — a `33px` button and a `48px` button yield the *identical ADMIT verdict* against `"button >= 44x44px"`. Admit means "anchored, in-scope, well-formed, safe, bounded change occurred," NOT "acceptance met." Acceptance is judged only by the human eye at the diff gate. **Repaired:** priced explicitly in the §8 determinism budget as the intent-fidelity ceiling.
- **TG-3 (new, BLOCK-adjacent):** the same `odIndex`-only assumption **false-rejects the idiomatic CSS way** of satisfying a sizing task (edit a `.cta` rule in `<style>` → button subtree byte-identical → V2 reports "unchanged"). The model was simultaneously too loose (admits adversarial un-anchored change) and too strict (rejects legitimate un-anchored change). **Deferred to the spike:** R2-a (declare style allowance + attribute) vs R2-b (resolved-style hash in the cascade).

**Deferred (named, with owner/trigger):** O1 repair path (dormant — protects G7 lane separation); the C-1/C-2 levers wired as config; calibration constants `S`/`B`/`k`/`c` (B3/TG-4 — *fail-closed at an unknown threshold is not auditable*); R2 V2-vs-CSS decision; RESIDUE-G (land citable `INV-3/4/5/6/8`/`DEC-*`/`OQ-2` artifacts — the design currently honors an *inferred* INV→G mapping). No external research was run (s4: no-research-now); GAP-R1 (deterministic validation of LLM artifacts) is the named bounded fallback if the spike stalls.

### 7. The single unbuildable assumption the design rested on

s7-A1 (BLOCK-LOCAL): the entire design reads/writes HTML through a **port that does not exist**. `StudioSessionStorePort` has zero HTML read/write methods; `htmlArtifactRef` is a dangling path string never written and never read. The plan closes this in Layer 0 by adding `readHtml/stageHtml/commitHtml/discardStagedHtml` (and `removeRevision` in Layer 3, since atomic compensation is not even *expressible* against the current port). Until this lands, lanes 3/4 have no input and the recorder has nothing to commit.

### 8. The plan shape (s9, non-executed)

Seven layers (L0–L6), MWU → hardening, mapped to the real `domain/application/infrastructure/interface` layout, every contract change tagged `[PROPOSAL]`:
- **L0** substrate: schema + artifact content port + shared canonicalizer (closes A1) — *unblocks everything*.
- **L1 (MWU)** pure validator suite + composite verdict + whole-tree V3 fence (closes B1/TG-1); toy-game falsifiers become passing regression fixtures.
- **L2** two-gate state machine + `RevisionApplied` lifecycle (closes C1) + accept-time staleness re-check (C3).
- **L3** recorder atomicity: all-or-nothing commit + compensating rollback + `removeRevision` (C2/RESIDUE-A).
- **L4 (spike-gated)** calibrate `S`/`B`/`k`/`c`; decide R2 (V2 CSS); wire C-1/C-2 levers.
- **L5** `studio apply` CLI + Claude Code proposer adapter; toy-game-style e2e with a *scripted* proposer (no live LLM in CI).
- **L6** governance closeout (RESIDUE-G citable artifacts) + D4 checksum migration.

L0–L3 are buildable *before* the spike; L4 numbers and V2 semantics are spike-gated. **RESIDUE-B (the C-1 spike) is the single boundary between "C designed" and "C trusted."**

### 9. Residue carried (owner named)

RESIDUE-A recorder compensation (L3); RESIDUE-B the C-1 spike (whole-tree V3 + R2 decision + calibration); RESIDUE-C shared canonicalizer (L0); RESIDUE-D selector-only degrade fidelity; RESIDUE-G citable governance IDs (L6). Deferred options O1/O2/O3 remain dormant with named triggers.

---

**Stage artifacts (all absolute):**
`/home/vrondelli/projects/domainspec-core/implementation/domainspec/docs/features/ui-prototyping-studio/development/refinement-runs/20260615T205403Z-mutation-execution-mechanics/stages/{01-context-pack,02-define,03-refine-review,04-research-decision,05-approach-comparison,06-design,06-validator-model,07-design-review,08-toy-game,09-plan}.md`