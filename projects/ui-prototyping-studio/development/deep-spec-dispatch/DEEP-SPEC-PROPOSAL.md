---
id: ui-prototyping-studio-deep-spec-proposal
feature: ui-prototyping-studio
title: "Deep Spec Proposal (s9): ergonomics-first deepened spec resolving the eight shallow areas, folding s5 stressors as invariants"
summary: >
  PROPOSAL ONLY — does not mutate the canonical SPEC. Folds s4 (deep design), s5 (residuality stressors),
  s6 (UX evidence/validator layers), s7 (Playwright plan), and s8 (naive-user cold-start) into one deepened
  spec expressed in domainspec UI types with field-level detail. Resolves all eight shallow areas; for each,
  cites the driving evidence and states the ergonomics rationale (lead-when / load / friction). Adopts s5's
  eight invalidations as new invariants so the spec is survivable, not just happy-path correct. First principle,
  non-negotiable: ergonomics — agentic tools that improve human work and form symbiotic human-agent relations;
  governance is a feature, not friction.
status: proposal
node_type: design
dispatch_id: ui-prototyping-studio-deep-spec-001
step_id: s9-synthesis
lane: synthesis
owners:
  - web-core
reads:
  - handle.synthesis        # SYNTHESIZED-DEEP-DESIGN.md (s4)
  - handle.residuality      # RESIDUALITY-STRESSORS.md (s5)
  - handle.ux-evidence      # UX-EVIDENCE-REPORT.md (s6)
  - handle.playwright-plan  # PLAYWRIGHT-TEST-PLAN.md (s7)
  - handle.naive-user       # COLD-START-USABILITY-FINDINGS.md (s8)
updatedAt: 2026-06-15
---

# DEEP-SPEC-PROPOSAL.md

> **This is a PROPOSAL.** It does not claim to mutate the canonical SPEC. It is the input a `decision-gate` / spec-owner would adjudicate before promotion. Where s5 invalidated an s4 acceptance claim, the resolution is written as a *new invariant* and flagged as proposed-not-calibrated.

**First principle (non-negotiable):** ergonomics. Every resolution below carries `lead-when` (who leads, who may act, what the human sees before durability), `load` (recognition vs recall, comparison breadth, decision count), and `friction` (the manual step removed). **Governance is a feature, not friction.**

**Why status is FLAG, not pass.** s4 converged on a strong spine and resolved the eight shallow areas, but s5 proved that three trust-bearing assumptions are unguarded (determinism across versions, disposal atomicity/single-writer, an unfatigued human reading before disposing) and three durable stores are unbounded, and s8 proved the *current build* fails a cold-start naive user on jargon, missing preview, and a misleading core label. A spec is not one-shot-buildable until those are written down. This proposal writes them down.

---

## Section 0 — Evidence-to-resolution crosswalk

Each shallow area is resolved using a named slice of evidence. This is the audit trail the first principle demands: no resolution is asserted on novelty.

| Shallow area | Primary driver | Corroborated / pressured by | Resolution kind |
|---|---|---|---|
| Fitness scoring model | s4 D-S0/Q1 (named-signal Pareto, no composite) | s8 (a single score would invite "the system said B is best") | DECIDE |
| Exploit conformance metric | s4 D1/Q2 (signed field-delta) | s5 E1 (token drift -> pending not green); s6 cog.3/FX-SF-05 (false-trust chip) | DECIDE + new invariant |
| Identity/DNA rejection lifecycle | s4 D3/Q3 (durable, reversible) | s5 T7/X3 (over-constrained genome); s8 Task 3 (panel not findable) | DECIDE + new invariant |
| Component registry model | s4 Q4 (typed edge) — entity is residue | s5 A6 (whose taste); s8 dom.3/FX-SF-08 (recognition) | PARTIAL DECIDE + RESIDUE |
| Accessibility interaction detail | s4 Q9; s6 a11y.1..6; s7 Part D | s6 gaps: no apply modal, no aria-describedby; s8 (keyboard parity) | DECIDE (hard-gate deterministic parts) |
| Error/recovery flows | s4 D5/Q5 (4 named states) | s5 A7/T2,T3 (sustained outage, malformed); s6 FX-KG-02/FX-KB-08 | DECIDE + 3 new states |
| Cognitive-load handling | s4 D2/Q6 (champion+challengers) | s5 S1/S2 (distrust, fatigue); s8 (paralysis is the lesser problem; *orientation* is the real one) | DECIDE + new invariant |
| Human-vs-agent lead | s4 D-S0/Q0 (3-tier matrix) | s5 X1 (structural enforcement); s8 (every disabled control needs a reason) | DECIDE + new invariant |

---

## Section 1 — Resolved shallow areas (domainspec UI types, field-level)

Ordering follows leverage: the lead boundary first (it parents the rest), then the areas s8 ranked most broken.

### 1.1 Human-vs-agent lead boundary (Q0) — the parent resolution

**Decision:** a typed three-tier `lead-when` matrix over all 13 operations, enforced **structurally** (s5 X1/Inv-6), with **every disabled control carrying a typed reason** (s8 cross-cutting gap #2).

**Field-level type expression.**
- New value object `LeadTier` enum: `reversible | durable | rule-change`.
- Every Operation carries a `leadTier: LeadTier` annotation (not a runtime field — a contract property verified by test).
- New value object `GateReason { gateState: GateState; reasonCode: string; reasonText: string; releasePath: ReleaseAffordance | null }`. **Every `GateState=blocked|pending` on a tier-2/3 control MUST resolve a `GateReason` with non-null `reasonText`** (s8: only the Annotation panel told the user *why*; all others just greyed out).
- New value object `ReleaseAffordance { kind: "unlock" | "prerequisite" | "documented-exception"; targetOperation: string }` (s5 Inv-7 / X2: no state from which the human cannot reach an unblocking action).

| Tier | Operations | Agent may act alone | Human sees before durability |
|---|---|---|---|
| `reversible` | InitializeSession, SubmitPrompt, GenerateVariants, SynthesizeMutationBatch(->draft), RecordFitnessSignal(governance/test/risk), proposedChampionLabel nomination, conformance-delta compute, proposal-tuning | **Yes** | n/a (no durable effect) |
| `durable` | SelectOrCommitBaseline, ConfirmUIDecisionEvidence, ApproveMutationBatch, ApplyApprovedBatch, ExportDesignHandoff | **No** | proposal + evidence + GateReason if blocked |
| `rule-change` | EvaluateProofGate, PromoteEvolutionRule | **No** (DEFERRED in MVP, D-009) | ProofObligation + RulePromotionRequest |

**New invariant (Inv-6, from s5 X1):** tier-2/3 operations are NOT agent-callable; `prompt` and `CommentEvent.note` text are **data, never governance instruction**. Verified by a prompt-injection corpus test (s7 Part C), not assumed.

- **Evidence:** s4 D-S0 (matrix); s5 X1 (structural enforcement is the survival property), Inv-7 (reachable exit); s8 (disabled-without-reason is the #2 cross-cutting failure).
- **lead-when:** human attention spent only at tiers 2/3; tier 1 is where the agent earns its keep. **load:** policing two named checkpoints, not a continuous audit. **friction:** trust becomes structural — the human lets the agent run free where mistakes are cheap because nothing durable happens without their `BatchApproval`.

### 1.2 Identity/DNA rejection lifecycle (Q3)

**Decision:** rejection is durable, reversible negative evidence typed as a relation; the genome's negative-constraint set is **bounded by a feasibility check** (s5 T7/X3).

**Field-level type expression.**
- `UIDecisionRecord { decisionId; type: UIDecisionType; relation: UIIdentityRelationType; targetIdentityRef: TypedReference; fitnessSignalRef: TypedReference; durable: boolean; operatorRef: string; createdAt: string }`. A reject is `type=reject`, `relation in {replaced-by, removed, reshaped, merged-into, split-from}`, `durable=true` only after `ConfirmUIDecisionEvidence`.
- `PrototypeGenome.negativeConstraints: NegativeConstraint[]` where `NegativeConstraint { identityRef: TypedReference; relation: UIIdentityRelationType; reversible: true; sourceDecisionId: string }`.
- **New invariant (Inv-3-adjacent / Deg-3, from s5 T7/X3):** when accumulated `negativeConstraints` make `GenerateVariants` infeasible, the agent STOPs and emits a new session state `GenerationInfeasible`, surfacing the conflicting (reversible) constraints — **never silently relaxes a remembered no**. New observability signal `negative_constraint_count`.
- `FitnessSignal(source=human, preference=-1, dimension=<element/DNA field>)` records the selection pressure.

- **Evidence:** s4 D3/D-S3 (durable != irreversible); s5 T7 (over-constraint), X3 (poisoning is recoverable because D-S3 + one-action reset to neutral); s8 Task 3 (the panel must actually be *confirmable* — see 1.3).
- **lead-when:** human disposes every rejection (tier-2); agent honors, never re-proposes a `removed` identity. **load:** decreasing over a session (system gets quieter as taste accrues) until/unless infeasible, when it speaks up. **friction:** a no is remembered in the token contract, never re-fought — but never at the cost of silent capability loss.

### 1.3 Identity Evidence as a confirmable, previewable surface (Q3/Q4 + s8 Critical #1)

**Decision (driven hardest by s8):** the Identity Evidence surface MUST render a **live preview** of the chosen variant's artifact and carry an explicit `ConfirmUIDecisionEvidence` action with a confirmed-state indicator. s8 ranked this the single Critical failure: a named, required step the user literally cannot perform because there is no findable, confirmable content and nothing to *see*.

**Field-level type expression.**
- `UIElementInstance { instanceId; identityRef: TypedReference; variantLabel: VariantLabel; signature: UIVisualSignature; previewRef: TypedReference; confirmed: boolean }`. **`previewRef` is new and load-bearing**: it resolves to a renderable artifact (the variant HTML), not an opaque string. s8: "all are represented as text references, never something the user can see."
- `UIVisualSignature` = the 24 controlled-vocab fields; each field is either a confirmed enum/token or a `TypedReference`-pending (the s1 ROSI underfill: Motion/Interaction/State/Feedback/Numeric per R-7).
- `ConfirmUIDecisionEvidence` flips `UIElementInstance.confirmed=true` and is the ONLY path to durability (RULE: generated identity/DNA suggestions become durable only after human confirm).
- **New invariant (Inv from s6 cog.3 / FX-SF-05, D-S2):** a `UIVisualSignature` field whose `TypedReference` is unresolved MUST NOT render a confident "held" chip — it renders `pending`. False trust is the worst ergonomic outcome.

- **Evidence:** s8 Critical #1 (impossible task — no preview, no confirm, jargon name); s4 D-XC/R-4 (shape vs meaning); s6 FX-SF-05 (false-trust chip soft_flag).
- **lead-when:** agent proposes the signature (tier-1); human confirms meaning (tier-2). **load:** recognition (eyeball a preview + plain "Is this the right look?") over recall (decode a reference string). **friction:** turns an impossible task into a one-glance confirm.

### 1.4 Exploit-mode conformance metric (Q2)

**Decision:** conformance = signed field-delta over two `UIVisualSignature`s, each delta a governance `FitnessSignal`, with confidence honesty (D-S2) and constrain-lock blocking; **a `TypedReference` that no longer resolves forces `pending`, never a stale green** (s5 E1).

**Field-level type expression.**
- `DiffSummary` (extended from the implemented `{added, changed, removed}` counts): `{ counts: {added, changed, removed}; fieldDeltas: FieldDelta[] }` where `FieldDelta { dimension; fromValue; toValue; preference: -1|0|1; confidence: 0..1; gateState: GateState; reason: GateReason | null }`. **s8 Medium #7 fix:** the bare `2/1/0` triple is kept for density but MUST carry labels ("2 added, 1 changed, 0 removed") and the human-readable `fieldDeltas` are the primary surface.
- `FitnessVector.confidence` = 1.0 **only** when both ends resolve to a confirmed enum/token; `<1.0` or `pending` otherwise (D-S2 honesty floor).
- A delta on a `constrain`-locked field sets `gateState=blocked` on the candidate's *selectability* with a non-null `GateReason.reasonText` and a `releasePath` (unlock-from-here, s5 Inv-7/X2).
- Locked fields fold into `PrototypeGenome.positiveConstraints`.

- **Evidence:** s4 D1/D-S2; s5 E1 (token-set change must turn the chip pending, not green; fixture: remove a token -> assert pending); s6 a11y.5/FX-SF-01 (reason must be associated); s8 Task 2 (confirmation hidden in a status string — it must be a visible badge/diff).
- **lead-when:** agent computes the delta (tier-1, judgment-free); human disposes the lock/accept per field (tier-2). **load:** 72 cells -> 2-5 changed, labeled fields. **friction:** on-brand-ness is recognizable; the diff format is stable across cycles.

### 1.5 Fitness scoring model (Q1)

**Decision:** named-signal Pareto; **no composite score, ever.**

**Field-level type expression.**
- `FitnessSignal { signalId; source: FitnessSignalSource; vector: FitnessVector; subjectRef: TypedReference; createdBy: string; createdAt: string }`.
- `FitnessVector { preference: -1|0|1; severity: "block"|"high"|"medium"|"low"|"info"; confidence: 0..1; dimension: string }`.
- For `source=human`: human owns `preference` and `severity` (this is how the human "owns the weights" without touching a weight vector). For `source in {governance,test,risk}`: agent derives deterministically.
- Selection is `SelectOrCommitBaseline` (tier-2). Candidates compared on the *set* of human-locked dimensions; a dominated candidate is surfaced as such; **no scalar score is ever computed or shown.**

- **Evidence:** s4 Q1/O-004; s8 (a single number would read as "the system said B is best" — automation bias the naive user cannot challenge).
- **lead-when:** human owns weights (by locking dimensions), agent owns measurement. **load:** reads facts, not arithmetic. **friction:** named evidence invites informed disposal ("B drifted on two unlocked fields, zero axe blockers — ratify?").

### 1.6 Cognitive-load / paralysis handling (Q6) + orientation (s8 root cause)

**Decision:** champion + challengers with the two D-S1 guardrails (override symmetry + worst-dimension disclosure), PLUS a typed **workflow-step model** because s8 proved the real cognitive failure is *orientation*, not choosing-among-three.

**Field-level type expression.**
- `proposedChampionLabel` — non-durable read-model field (not a `BaselineRevisionAnchor`, not a `UIDecisionRecord` until the human acts). References the nominated variant, the deterministic basis (fewest blocking `FitnessSignal`s), and a rationale that MUST include the champion's *worst* dimension. Vanishes on override.
- **New value object `WorkflowStep { ordinal: number; operation: string; state: "locked"|"available"|"done"; unlockReason: GateReason | null }`** — a read-model projection over the implemented 10-state machine that exposes the *hidden linear pipeline* (Session -> Prompt -> Generate -> Choose -> Confirm -> Annotate -> Synthesize -> Approve -> Apply -> History -> Handoff). s8 cross-cutting #1: "the workflow is a hidden linear pipeline, but the UI presents seven coequal panels with no numbering." This is the highest-leverage ergonomic addition in the whole proposal.
- **New invariant (D-S1):** override MUST cost exactly what ratify costs; a one-sided rationale (no worst-dimension) is rejected. Verified by s6 FX-SF-04 (override-asymmetry soft_flag).
- Graceful degradation: at `variantCount=1` no champion; on a tie, co-challengers with no nominated champion.

- **Evidence:** s4 D2/D-S1; s6 cog.1/FX-FP-01 (grouped expert density is NOT a defect — must not gate); s8 Tasks 1,2,5 (every stall was "what do I do next?" signaled only by greyed buttons).
- **lead-when:** agent nominates + assembles rationale + projects the step model (tier-1); human ratifies-or-overrides (tier-2). **load:** drops from "rank 3 from scratch" to "ratify or veto one pre-surfaced candidate"; and from "guess the order" to "follow the lit next step." **friction:** kills both paralysis and disorientation without manufacturing rubber-stamping.

### 1.7 Error / recovery flows (Q5) — foundation-first, extended for sustained failure

**Decision:** the four s4 additive failure states PLUS three from s5's degradation-mode attractor (A7). All recoverable, none auto-applies or auto-discards, all preserve the append-only `CommentEvent` stream and draft `MutationBatch`.

**Field-level type expression — `StudioSessionState` 10 -> 17 states** (additive on the implemented enum):

| New state | Trigger | Preserved | Safe-retry basis | Recovery (tier-2) | Evidence |
|---|---|---|---|---|---|
| `GenerationFailed` | GenerateVariants transient fail | prompt, prior baseline | D-002 determinism | retry / discard | s4 D5 |
| `SynthesisTimedOut` | SynthesizeMutationBatch timeout | comment stream, draft | comments are durable source | retry / discard draft | s4 D5 |
| `SourceStale` | ApplyApprovedBatch precheck vs `BaselineRevisionAnchor` | draft, comments | re-anchor recomputes | re-anchor+retry / discard | s4 D5 |
| `ApplyConflicted` | ApplyApprovedBatch deterministic re-diff conflict | batch, comments | deterministic re-diff | resolve / re-approve / discard | s4 D5 |
| `DeterminismDrift` | provenance fingerprint mismatch on retry | all prior work | n/a — output offered as *fresh*, never a retry | treat as new generation | s5 A1/T1 (Inv-1) |
| `StudioReadOnly` | sustained backend outage | all prior work readable/exportable | n/a — generation stopped honestly, retry rate-limited | wait / export | s5 A7/T2 |
| `GenerationDegraded` | shape-failing output (raw px slips through) | named failing fields | never selectable, never folds into genome | discard / re-generate | s5 A7/T3 + D-XC |

- **New invariant (Inv-1, from s5 A1):** `PrototypeGenome` and `BaselineRevisionAnchor` carry `BaselineProvenance.provenanceFingerprint = {modelId, tokenSetVersion, libLockfileHash}`. No output is presented as a "safe retry" unless the fingerprint matches. This is the single highest-leverage hardening — it sits under every "safe to retry" and "same genome -> same output" claim.
- **New invariant (s5 S4):** "discard" under any failure state is *soft* (recoverable for the session) because the `CommentEvent` stream is append-only; only `ApplyApprovedBatch`/`SelectOrCommitBaseline` are irreversible.
- `GateState=blocked` carries the `GateReason`; `aria-live="polite"` announces each transition once.

- **Evidence:** s4 D5 (ranked #1 in necessity by both lanes); s5 A1/A7 (determinism unguarded, no read-only mode); s6 FX-KG-02/FX-KB-08 (work-loss must fire as a hard gate); s8 (no visual confirmation a change landed — the failure surface must be legible).
- **lead-when:** agent detects + reports honestly (tier-1); human disposes recovery (tier-2). **load:** removes anxiety + recall under failure — named state + one-line reason + single safe action. **friction:** "safe to retry" becomes a type-backed claim (Inv-1 fingerprint), not an assumption.

### 1.8 Concurrency & disposal atomicity (Q5-adjacent, from s5 A4) — new spec material

**Decision (entirely from s5; s4 was silent):** a tier-2 disposal is atomic and anchor-checked.

**Field-level type expression.**
- **New invariant (Inv-4):** no tier-2 operation reports complete until its `UIDecisionRecord`/`BatchApproval` is durably written; on write failure it returns to a re-tryable pending state with intent preserved — **never a false success**.
- **New invariant (Inv-5):** durable disposals are serialized and anchor-checked against the `BaselineRevisionAnchor` they were made against; a disposal against a stale anchor raises `SourceStale` *before* commit, never last-write-wins.
- New observability: `disposal_write_failure`, `concurrent_anchor_conflict`.

- **Evidence:** s5 A4/T4,T6 (risks the exact lost/phantom human disposal the whole design exists to prevent).
- **lead-when:** human disposes; the system guarantees the disposal is real or visibly pending. **load:** zero added in the happy path; removes the worst silent-failure class. **friction:** the human can trust that "approved" means "durably approved."

### 1.9 Accessibility interaction detail (Q9)

**Decision:** hard-gate the deterministic parts; governance is keyboard-first; close the two s6 implementation gaps.

**Field-level type expression / surface contract.**
- Tab order across the 7 panels = reading order (s6 a11y.2 / FX-KB-03).
- **New (closes s6 gap):** `ApplyApprovedBatch` opens a `role=dialog`/`aria-modal` with focus trap + return-focus (s6 a11y.4 / FX-KG-04 — currently UNBUILDABLE against impl; this is the acceptance target).
- **New (closes s6 gap):** every disabled governance button's `GateReason.reasonText` is `aria-describedby`-associated (s6 a11y.5 / FX-SF-01).
- `aria-live="polite"` on `SessionStateIndicator` announces each `StudioSessionState` transition once.
- All gates (`SelectOrCommitBaseline`, `ApproveMutationBatch`, `ApplyApprovedBatch`) fully keyboard-operable; target size >= WCAG 2.2 SC 2.5.8 24x24 on touch (s6 layout.2 / FX-KG-06), with product-context exception for low-risk secondary controls (FX-FP-02).

- **Evidence:** s4 Q9; s6 a11y.1..6 + the two named gaps; s7 Part D.
- **lead-when:** the human operates every gate by keyboard alone (governance must be universal). **load:** announce-once prevents auditory spam. **friction:** governance is not a mouse-only privilege.

### 1.10 Component registry model (Q4) — partial decision + owned residue

**Decision (partial):** the typed version edge lands now; the persistence/indexing entity remains residue (R-1, owner s9/future).

**Field-level type expression.**
- `UIElementIdentity { identityId; conceptName: string }` = stable concept node.
- `UIElementInstance` (see 1.3) = versioned realization; version edge typed by `UIIdentityRelationType`.
- `TypedReference` indexes instance -> identity.
- **New invariant (s6 dom.3 / FX-SF-08):** the agent MUST reuse known `UIElementIdentity.conceptName` across cycles so the human recognizes components (recognition-over-recall); rendering the same identity under a new name each cycle is a soft_flag.
- **New (s5 A6/Inv-8):** session-scoped signals carry `operatorRef` + timestamp; D4-prop visibility copy names *whose* choice ("A chose Density=comfortable 3x on 2026-06-15. Keep / reset?").

- **Evidence:** s4 Q4 (typed edge free from D3; entity is residue); s5 A6 (whose taste); s8 (recognition).
- **Residue:** the storage/match/index entity across `BaselineGenealogyFamily` lineages (R-1).

---

## Section 2 — New / changed domainspec UI types (consolidated field-level)

### 2.1 Changed enums (additive)
- `StudioSessionState`: 10 -> 17 (adds the 4 s4 D5 states + `DeterminismDrift`, `StudioReadOnly`, `GenerationDegraded`; plus `GenerationInfeasible` from 1.2 = 18 if counted — proposal flags the exact count as a decision-gate item). No other enum changes value set (deliberate: deepening needs almost no new vocabulary).

### 2.2 New value objects
- `LeadTier (reversible|durable|rule-change)`; `GateReason {gateState, reasonCode, reasonText, releasePath}`; `ReleaseAffordance {kind, targetOperation}`; `WorkflowStep {ordinal, operation, state, unlockReason}`; `FieldDelta {dimension, fromValue, toValue, preference, confidence, gateState, reason}`; `NegativeConstraint {identityRef, relation, reversible, sourceDecisionId}`.

### 2.3 Extended value objects
- `BaselineProvenance` += `provenanceFingerprint {modelId, tokenSetVersion, libLockfileHash}` (Inv-1). Currently `{mode, label}` in code — additive.
- `DiffSummary` += `fieldDeltas: FieldDelta[]` and labeled counts (currently bare `{added,changed,removed}`).
- `FitnessVector` fully specified (preference/severity/confidence/dimension) with the D-S2 confidence floor.
- `PrototypeGenome` += `positiveConstraints` + `negativeConstraints` + feasibility check.
- `UIElementInstance` += `previewRef` (load-bearing for s8).
- `UIDecisionRecord`, `FitnessSignal` += `operatorRef` (Inv-8).

### 2.4 New non-durable read-model fields
- `proposedChampionLabel` (D2); `WorkflowStep[]` projection (s8 orientation).

### 2.5 Proof schema (specify, do not build) — D-009 deferral
- `ProofObligation {obligationId, claim/dimension, status: ProofStatus, evidenceRef: TypedReference, bindsTo: RulePromotionRequest}` — shape-only (D-XC).
- `RulePromotionRequest {proposedRuleChange, motivatingEvidence: FitnessSignal[], boundObligations: ProofObligation[], status: RulePromotionStatus}` — always `deferred` in MVP.
- **New invariant (s5 O2/Inv-3):** a `RulePromotionRequest=deferred` has provably ZERO runtime effect (a 100-deferred session behaves identically to a 0-deferred session).

---

## Section 3 — Proposed invariants from s5 (the eight that move status off pass)

| Inv | Statement | Driver | Verification target |
|---|---|---|---|
| Inv-1 | provenance fingerprint gates "safe retry"; mismatch -> `DeterminismDrift` | A1/T1 | s7 fixture: pin genome, change modelId, assert refusal |
| Inv-2 | `CommentEvent` retention never truncated; only presentation paginates | A3/T5 | large-set fixture: fold correct, no drop |
| Inv-3 | deferred `RulePromotionRequest` has zero runtime effect | A3/O2 | 100-vs-0 equivalence test |
| Inv-4 | no tier-2 op reports complete until durably written | A4/T4 | inject write failure -> no false success |
| Inv-5 | durable disposals serialized + anchor-checked; `SourceStale` before commit | A4/T6 | two-tab test -> re-anchor not overwrite |
| Inv-6 | tier-2/3 ops not agent-callable; prompt/note text is data | A5/X1 | injection corpus -> zero gate effect |
| Inv-7 | no blocked state without a reachable accountable exit | A5/X2/S3 | universal-lock test -> unblock path reachable |
| Inv-8 | session-scoped signals carry operator + timestamp provenance | A6/O1 | handoff test -> attribution from artifacts alone |

All eight are **proposed, not yet calibrated** against the s6 fixture corpus — that calibration is Layer-specific work in the implementation plan.

---

## Section 4 — Residue carried (owned, not hidden)

R-1 registry entity (s9); R-2 full conflict algebra (s9); R-3 rule-track learning DEFERRED behind D-009; R-4 semantic enum/token meaning stays human (never automated); R-5 the entire ergonomics floor is unproven (s8 + s6/s7); R-7 ROSI token underfill (s1->s9). Open questions OQ-1 (trust meter), OQ-2 (seen-diff proxy), OQ-3 (operator-handoff carry/reset/prompt), OQ-4 (import-integrity scope) routed per s5 Section 5.

**One sentence for the spec owner:** Promote the spine and the eight shallow resolutions; treat the eight s5 invariants and the s8-driven preview + workflow-step + disabled-reason additions as the load-bearing deltas; keep the rule-track deferred and the ergonomics floor explicitly unproven until s8 re-tests it.