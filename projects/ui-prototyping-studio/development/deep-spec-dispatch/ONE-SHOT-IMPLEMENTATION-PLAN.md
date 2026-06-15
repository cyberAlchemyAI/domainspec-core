---
id: ui-prototyping-studio-one-shot-implementation-plan
feature: ui-prototyping-studio
title: "One-Shot Implementation Plan (s9): layered minimum-working-unit -> progressive hardening, Playwright-gated"
summary: >
  PROPOSAL ONLY. A layered, traceable plan to implement the deepened spec in one shot. Layers run from a
  minimum working unit (the already-built happy-path spine, L0) through six progressive-hardening layers.
  Each layer states scope, the domainspec UI types touched, the Playwright/fixture scenarios that gate it
  (grounded in the real e2e mock-api and the s6 fixture corpus + s7 plan), and the residual risks it carries.
  First principle: ergonomics — every layer states who leads when, the cognitive load, and the friction removed.
  Status FLAG: genuinely buildable, but Layers 5-6 carry the unproven ergonomics floor and the eight s5
  invariants are proposed-not-calibrated.
status: proposal
node_type: plan
dispatch_id: ui-prototyping-studio-deep-spec-001
step_id: s9-synthesis
lane: synthesis
owners:
  - web-core
reads:
  - handle.deep-spec-proposal
  - handle.residuality      # s5
  - handle.ux-evidence      # s6
  - handle.playwright-plan  # s7
  - handle.naive-user       # s8
updatedAt: 2026-06-15
---

# ONE-SHOT-IMPLEMENTATION-PLAN.md

> **PROPOSAL.** Grounded in the actual implementation: `backend/.../domain/models.ts` (10-state machine, gate fields), `apps/web/src/hooks/useUiPrototypingStudio.ts` (the wired spine), `apps/web/e2e/.../mock-api.ts` (the only backend the suite sees, with canonical error codes), and `StudioWorkbenchLayout.tsx` (panel/tab order). The plan is buildable because L0 already exists; every later layer is an additive, independently-gated increment.

**Layer-boundary heuristic:** a new layer begins where the *value* delivered changes kind (proof-of-flow -> survival -> trust -> ergonomic legibility) or where the *cost* of getting it wrong changes (reversible -> durable -> irreversible). **First principle on every layer:** lead-when / load / friction.

---

## Layer map (at a glance)

| L | Name | Value kind | Gate sev floor | s5 invariants closed | s8 friction addressed |
|---|---|---|---|---|---|
| L0 | Minimum working unit: happy-path spine | proof-of-flow | smoke + flow (block) | — (baseline) | — |
| L1 | Governance integrity (structural gates) | trust-is-real | flow + injection (block) | Inv-6 | — |
| L2 | Accessibility + disabled-reason | universal access | a11y (block/high) | Inv-7 (exit) | #2 (disabled w/o reason) |
| L3 | Error/recovery + determinism fingerprint | survival | flow.3 (high) | Inv-1, Inv-2 | (failure legibility) |
| L4 | Conformance + identity preview + confirm | informed disposal | soft_flag (no gate) | — | #1, #2 (preview/confirm) |
| L5 | Concurrency, atomicity, bounded stores | no lost disposal | flow (block) | Inv-3,4,5,8 | — |
| L6 | Ergonomic legibility (workflow steps, plain copy) | the first principle | soft_flag + L6 study | — | #1,3,5 + Tasks 1-7 copy |

**Why this order is one-shot-safe:** each layer's gate suite is a strict superset of the prior layer's; nothing in a later layer can regress an earlier gate without the suite going red. L0 is the integration backbone; L1-L3 are the survival/trust floor (must hold before any ergonomic polish is meaningful); L4-L6 are where the first principle is delivered and where the residual risk concentrates.

---

## L0 — Minimum working unit: the happy-path spine

**Scope.** Already implemented and wired: InitializeSession -> SubmitPrompt -> GenerateVariants -> SelectOrCommitBaseline -> CaptureCommentEvent -> SynthesizeMutationBatch -> ApproveMutationBatch -> ApplyApprovedBatch -> RevisionManifestEntry -> ExportDesignHandoff. Seven panels mount; the 10-state machine advances; gates are `selectionGate`/`applyGate`.

**DomainSpec UI types touched.** `StudioSession`, `PrototypeVariant`, `CommentEvent`, `MutationBatch`, `RevisionManifestEntry`, `HandoffBundle`, `GateState`, `BaselineProvenance` (current `{mode,label}`), the 10-state `StudioSessionState`.

**Playwright scenarios that gate this layer (from s7 Part B + s6 FX-KG-01):**
- `FX-KG-01` full compliant studio: all 7 panels mount, every control has accessible name+role, happy-path cycle completes via `getByRole`. Calibrates smoke.1, flow.1/2, dom.1. **Expected ALL PASS.**
- s7 Part B workflow spine: init -> ... -> handoff using the real `mock-api.ts` state transitions (variantCount=3 selected branch AND variantCount=1 committed branch — the mock special-cases count=1 to auto-commit baseline + `rev-0000`).
- `FX-KB-01` broken asset -> smoke.1/2 FIRE.

**lead-when / load / friction.** lead: agent runs all tier-1 reversible steps; human disposes the tier-2 baseline/approve/apply. load: high today (this is exactly what s8 flagged). friction: none removed yet — L0 only proves the flow exists.

**Residual risk carried.** Everything s8 ranked Critical/High is still present (no preview, misleading "baseline", hidden pipeline). L0 is correct-but-unergonomic by design; the first principle is delivered in L6.

---

## L1 — Governance integrity (gates are structural, not promptable)

**Scope.** Make tier-2/3 enforcement structural (Inv-6): tier-2/3 operations are not agent-callable; `prompt`/`note` text is data. Confirm `AUTO_APPLY_FORBIDDEN` and apply-requires-approval at the network layer, not just the UI.

**Types touched.** `LeadTier` annotation on all 13 operations; `BatchApproval`; `GateState`; `MutationBatchStatus`.

**Playwright gates (s7 Part C + s6):**
- `FX-KB-07` gate bypass: Apply enabled before approval (`applyEnabled` true with `draftStatus!=approved`) -> flow.2 FIRE (block).
- s7 Part C direct-network probe: POST apply with `applyRequestedBy=system:auto` -> mock returns `AUTO_APPLY_FORBIDDEN` (409); assert UI never reaches applied.
- **Injection corpus (Inv-6 / s5 Ver-5):** comment/prompt text containing "auto-approve"/"ignore lock" -> zero gate effect (the ops simply are not agent-callable).
- s7 lead-when-matrix smoke test: each tier-1 op callable by agent path; each tier-2 op requires the human affordance.

**lead-when / load / friction.** lead: human disposes durable; agent structurally cannot. load: zero added. friction: trust becomes structural — the human can let tier-1 run free.

**Residual risk.** Inv-6 is *proposed*; the injection corpus is a new fixture not yet authored. X4 (forged provenance/import-integrity, OQ-4) is out of MVP scope — flagged.

---

## L2 — Accessibility + disabled-reason (governance is universal)

**Scope.** Tab order = reading order; `ApplyApprovedBatch` modal with focus trap + return-focus (closes s6 a11y.4 gap, currently UNBUILDABLE); `aria-describedby` on every disabled gate (closes s6 a11y.5 gap); `aria-live=polite` announce-once; 24x24 target size on irreversible governance controls with product-context exception. **Every disabled control resolves a `GateReason.reasonText`** (s8 #2).

**Types touched.** `GateReason`, `ReleaseAffordance`, `GateState`, `SessionStateIndicator` (read-model).

**Playwright gates (s7 Part D + s6):**
- `FX-KG-04` compliant apply dialog (role=dialog/aria-modal, Tab cycles within, Escape closes, focus returns) -> a11y.4 PASS. **This fixture is the acceptance target for the gap.**
- `FX-KB-04` untrapped modal -> a11y.4 FIRE (high).
- `FX-KB-02` unnamed icon-only Apply -> a11y.1 FIRE (block) + axe button-name.
- `FX-KB-03` tab scramble -> a11y.2 FIRE (high).
- `FX-KG-05` gate with associated reason -> a11y.5 PASS; `FX-SF-01` unassociated reason -> a11y.5 soft_flag.
- `FX-KG-06` >=24x24 PASS; `FX-KB-06` 18x18 apply -> layout.2 FIRE (medium); `FX-FP-02` compact secondary toolbar -> layout.2 does NOT fire on low-risk controls.
- Inv-7 reachable-exit: `FX` universal-lock -> assert an unblock path is reachable from every blocked state.

**lead-when / load / friction.** lead: human operates every gate by keyboard alone. load: announce-once. friction: governance is not mouse-only; disabled controls stop being dead ends.

**Residual risk.** axe dependency must be added (s7 residue). Inv-7 reachable-exit fixture is new.

---

## L3 — Error/recovery + determinism fingerprint (survival floor)

**Scope.** Add the failure states to `StudioSessionState`: the 4 s4 D5 states + `DeterminismDrift`, `StudioReadOnly`, `GenerationDegraded`. Each preserves prompt/comments/draft, carries a `GateReason`, offers exactly one safe recovery, never auto-applies/auto-discards. Add `BaselineProvenance.provenanceFingerprint` (Inv-1). "Discard" is soft (re-synth from comments).

**Types touched.** `StudioSessionState` (+7), `BaselineProvenance` (+fingerprint), `GateReason`, `MutationBatchStatus`, `BaselineRevisionAnchor`, `CommentEvent` (append-only retention, Inv-2).

**Playwright gates (s7 Part E + s6 FX-KG-02 + s5 Ver):**
- `FX-KG-02` compliant failure/recovery: each D5 state shows prompt+comments+draft preserved, blocked reason text, exactly one safe control, no auto-apply/auto-discard -> flow.3 PASS. (Requires new D5 mock states — s7 gap-detector residue.)
- `FX-KB-08` work loss: a path that silently drops comment stream/draft -> flow.3 FIRE (high).
- Inv-1 fixture (s5 Ver-1): pin a genome, change `modelId` -> assert system refuses the "safe retry" label and emits `DeterminismDrift`.
- s5 Ver-7: kill the backend -> assert `StudioReadOnly`, exportable, no retry-storm. Feed malformed DNA -> assert `GenerationDegraded` quarantine, not selectability.
- Inv-2: large comment set -> fold correct, no truncation, presentation paginates.

**lead-when / load / friction.** lead: agent detects + reports honestly; human disposes recovery. load: removes anxiety + recall under failure. friction: "safe to retry" is type-backed (fingerprint).

**Residual risk.** The 7 new states need mock-api support that does not exist yet (s7 names this as a gap-detector residue). `SynthesisTimedOut`/`SourceStale`/`ApplyConflicted` re-diff conflict algebra is partial (R-2).

---

## L4 — Conformance delta + identity preview + confirm (informed disposal)

**Scope.** Build the Identity Evidence surface s8 ranked Critical: render a live `previewRef` of the chosen variant, plain-language "Is this the right look?", explicit `ConfirmUIDecisionEvidence` with a confirmed-state indicator. Build the conformance `DiffSummary.fieldDeltas` with D-S2 confidence honesty (pending, not false-green) and constrain-lock blocking. Label the diff counts.

**Types touched.** `UIElementIdentity`, `UIElementInstance` (+previewRef, +confirmed), `UIVisualSignature` (24 fields + TypedReference-pending), `DiffSummary` (+fieldDeltas, labeled counts), `FieldDelta`, `FitnessSignal(source=governance)`, `FitnessVector(confidence)`, `UIDecisionType(constrain/preserve/change)`, `PrototypeGenome.positiveConstraints`, `ConfirmUIDecisionEvidence`.

**Playwright gates (s6 soft_flags + new):**
- `FX-SF-05` false-trust chip: a TypedReference-pending field shown with a confident green "held" chip -> cog.3 soft_flag (D-S2 honesty). MUST flag.
- `FX-SF-08` renamed components: same `UIElementIdentity` under a new name each cycle -> dom.3 soft_flag (recognition).
- s5 E1 fixture: remove a token -> assert the chip turns `pending`, not green.
- New scenario: select baseline -> Identity Evidence renders a preview, Confirm flips `confirmed=true` and shows the badge (closes s8 Critical #1). This is a presence/behavior test, NOT a hard gate (the ergonomic *gain* is L6/s8).
- `FX-FP-01` legitimate dense expert studio: cog.1 density proxy stays SILENT (the conformance surface must not be punished for showing many fields).

**lead-when / load / friction.** lead: agent proposes signature + deltas; human confirms meaning + locks fields. load: recognition (preview + 2-5 labeled deltas) over recall (decode references). friction: turns an impossible task into a one-glance confirm.

**Residual risk.** R-4: semantic correctness of enum/token meaning stays human (never automated). R-7: ROSI token underfill means some fields are legitimately `pending` (the honesty rule makes this safe, not absent). The conformance surface is net-new and the largest build chunk in L4.

---

## L5 — Concurrency, atomicity, bounded stores (no lost disposal)

**Scope.** Inv-4 (no tier-2 op complete until durably written; write-failure -> re-tryable pending with intent preserved). Inv-5 (durable disposals serialized + anchor-checked; `SourceStale` before commit, not after). Inv-3 (deferred `RulePromotionRequest` zero runtime effect; negative-constraint feasibility check -> `GenerationInfeasible`). Inv-8 (operator provenance on every session-scoped signal).

**Types touched.** `UIDecisionRecord` (+operatorRef), `BatchApproval`, `BaselineRevisionAnchor`, `PrototypeGenome.negativeConstraints` (+feasibility), `RulePromotionRequest`/`ProofObligation` (specified, deferred), `FitnessSignal` (+operatorRef).

**Playwright gates (s5 Ver + s7 Part C):**
- s5 Ver-4: inject a write failure on approve -> assert no false-success, intent preserved (block). Two-tab test -> second commit re-anchors, never overwrites (block).
- s5 Ver-3: 100 deferred `RulePromotionRequest`s generate identically to 0 (equivalence). N mutually-exclusive rejects -> `GenerationInfeasible`, not a silently constraint-violating variant.
- s5 Ver-6: handoff test -> successor reviewer replays all decisions with attribution from artifacts alone.

**lead-when / load / friction.** lead: human disposes; system guarantees real-or-visibly-pending. load: zero in happy path. friction: "approved" reliably means "durably approved"; "a no" never silently over-constrains.

**Residual risk.** Concurrency requires backend serialization the current file-store may not provide — flagged as a backend-side build item. OQ-3 (operator handoff carry/reset/prompt) is unresolved -> Inv-8 ships attribution but the carry/reset policy is decision-gated. R-1 registry entity still unspecified.

---

## L6 — Ergonomic legibility (the first principle, load-bearing)

**Scope (driven entirely by s8).** The `WorkflowStep[]` projection (numbered/lit next step over the hidden pipeline — s8 cross-cutting #1). Plain-language copy replacing jargon: "baseline" -> "chosen design"/"use this design" (s8 Critical #2), "Mutation"/"Synthesize" -> "Change"/"Prepare change" (s8 High #3), human-readable revision history with timestamps + labeled diffs + link back to originating comment (s8 #6/#7), a concrete handoff deliverable (download/copy-link + success toast, s8 #6). Champion+challengers nomination with override symmetry (D-S1). Make the variant card itself selectable (s8 Task 2). Click-to-annotate on the preview (s8 Task 4) — auto-fills target/selector so non-technical users are not asked for a CSS selector.

**Types touched.** `WorkflowStep` (read-model), `proposedChampionLabel` (read-model), `AnnotationTarget` (auto-derived from preview click), `HandoffBundle` (delivery affordance), `DiffSummary` (human-readable rows), `RevisionManifestEntry` (timestamp + comment backlink surfacing).

**Playwright gates (s6 L4 soft_flags + s8 L6 study):**
- `FX-SF-04` override asymmetry: override behind an extra confirm while ratify is one click -> cog.2 soft_flag (D-S1). MUST flag.
- `FX-SF-03` ungrouped density vs `FX-FP-01` grouped expert: cog.1 flags ungrouping, NOT total count.
- `FX-SF-06` hidden prior selection -> cog.4 soft_flag (working memory).
- `FX-SR-01`/`FX-SR-02` screenshot-review: apply less salient than promo; indistinct failure badge (reviewer prompt, never a gate).
- s7 Part F cognitive proxies as L4 soft_flags only.
- **L6 human-study (s8):** a fresh naive user completes Tasks 1-7 without stalling on orientation/jargon/preview. THIS IS NOT AUTOMATED — supporting traces/screenshots from `FX-KG-01` are handed to the s8 naive-user study. OQ-1 (trust meter) and OQ-2 (seen-diff proxy) are gated behind this study; do not ship the trust meter unvalidated.

**lead-when / load / friction.** lead: agent projects steps + nominates champion (tier-1); human ratifies (tier-2). load: drops from "guess the order + decode jargon" to "follow the lit step in plain words." friction: removes the entire cold-start wall s8 documented.

**Residual risk (the largest in the whole plan).** R-5: **no ergonomic gain here is proven.** Every L6 claim is L4 proxy or L6 human-study residue. The s8 cold-start findings are the evidence that the *current* build fails the first principle; L6 is the proposed fix but its success is unproven until s8 re-tests. OQ-1/OQ-2 unresolved. Deg-2 (the only sanctioned friction: "review the diff first" before irreversible apply) interacts with OQ-2 and must not become accountability theater.

---

## Cross-layer coverage matrix (traceability)

| Evidence item | Layer | Gating fixture/scenario |
|---|---|---|
| s4 spine D-001..D-009 | L0/L1 | FX-KG-01, s7 Part B/C |
| s5 Inv-1 determinism | L3 | Ver-1, DeterminismDrift fixture |
| s5 Inv-2 bounded comments | L3 | large-set fold test |
| s5 Inv-3 deferred inert + infeasibility | L5 | Ver-3 (100-vs-0), GenerationInfeasible |
| s5 Inv-4/5 atomicity+concurrency | L5 | Ver-4 (write-fail, two-tab) |
| s5 Inv-6 structural gates | L1 | injection corpus, FX-KB-07 |
| s5 Inv-7 reachable exit | L2 | universal-lock test |
| s5 Inv-8 operator provenance | L5 | Ver-6 handoff replay |
| s5 A7 read-only/quarantine | L3 | Ver-7 |
| s6 a11y.1..6 | L2 | FX-KG-04/05/06, FX-KB-02/03/04 |
| s6 layout target-size + FP | L2 | FX-KG-06, FX-KB-06, FX-FP-02 |
| s6 cog.* soft_flags | L4/L6 | FX-SF-03..06, FX-FP-01 |
| s8 Critical #1 preview/confirm | L4 | identity-preview behavior test |
| s8 Critical #2 baseline label | L6 | plain-copy + selectable-card |
| s8 #1 orientation | L6 | WorkflowStep projection |
| s8 #3 apply ritual | L6 | plain-copy + before/after surfacing |
| s8 #4 annotation jargon | L6 | click-to-annotate |
| s8 #6/#7 handoff/history | L6 | deliverable + readable rows |

---

## Buildability statement

This is genuinely one-shot-buildable because: (1) L0 already exists and passes its real e2e harness; (2) every later layer is purely additive against the existing `StudioSessionState` enum, `GateState`, and HTTP contract — no rewrite of the spine; (3) each layer's gate suite is a strict superset, so regressions are caught immediately; (4) every new type is field-specified in the deep-spec proposal; (5) the fixtures already exist as a designed corpus (s6) and a structured plan (s7). The honest caveats: the 7 new failure states and the conformance/identity-preview surface require **new mock-api support that does not exist yet** (s7's named gap), the eight s5 invariants are **proposed-not-calibrated**, and the entire first-principle payoff in L6 is **unproven until the s8 naive-user study re-runs**. Build L0-L3 to make the tool survive; build L4-L6 to make it deserve the human's trust.