---
id: ui-prototyping-studio-deep-spec-context-pack
feature: ui-prototyping-studio
title: "Deep-Spec Context Pack (s0 evidence baseline + ergonomics charter)"
summary: Compact, task-ready evidence baseline for deepening the UI Prototyping Studio spec to one-shot implementation readiness. Folds current design + decisions, the domainspec UI type vocabulary, the ux-evidence-validator model, and the ergonomics-first charter, then states the highest-leverage shallow areas as crisp questions.
status: draft
node_type: context
dispatch_id: ui-prototyping-studio-deep-spec-001
step_id: s0-frame
owners:
  - web-core
updatedAt: 2026-06-15
---

# CONTEXT-PACK.md — UI Prototyping Studio Deep-Spec (s0)

**Dispatch:** `ui-prototyping-studio-deep-spec-001` · **Step:** `s0-frame` · **Owner capability:** `context-builder`
**Output frame:** `frame.evidence-baseline` (consumed by s1 research, s2 challenger, s3 defender)
**Goal of the route:** take the spec from *architecture-strong / evidence-sparse* to **one-shot implementation readiness**, with **human–agent ergonomics as the first principle.**

This pack is the shared evidence floor every downstream lane reads. It does not decide anything; it fixes the vocabulary, the current design, the validator basis, the charter, and the questions the deep-spec must answer. All citations are to repo paths under `projects/ui-prototyping-studio/` unless noted.

---

## 0. First Principle (non-negotiable charter) — Ergonomics

Design agentic tools that **improve human work** and form **synergetic, symbiotic human–agent relations.** This is the lens every kept or changed decision in this dispatch must pass through.

**Charter clauses (binding on s2–s9):**

1. **Lead-when clause.** Every kept/changed decision MUST state *who leads when* — human or agent — at each decision point. Default posture: **agent proposes, human disposes** at every durable boundary (baseline, identity/DNA, apply, promotion).
2. **Cognitive-load clause.** Every kept/changed decision MUST state *what cognitive load it imposes* on the human (recognition vs recall, comparison breadth, memory burden, decision count per cycle) and how the design keeps that load bounded.
3. **Friction-reduction clause.** Every kept/changed decision MUST state *how it reduces friction* — what manual conversational step it removes, what it makes recognizable instead of remembered, what it makes resumable instead of repeated.
4. **Governance-is-a-feature clause.** Manual gates (baseline selection, explicit apply, proof gate) are **ergonomic features, not friction.** They exist so the human stays accountable and in control without having to police the agent. A gate is justified only if it protects a durable/irreversible action; gates on reversible drafts are friction and must be challenged.
5. **Evidence-floor clause.** No ergonomic claim is asserted; each is classified against the ux-evidence-validator model (§3) and is either Playwright-observable or named as human-study residue.

**Operator sentence (from dispatch intent):** "Explore max depth so we can implement this in depth; this is a test of our one-shot design and planning ability."

---

## 1. Current Studio Design + Load-Bearing Decisions

Source: `DECISIONS.md`, `DISCOVERY.md` §6, `UI-SPEC.md`, `states.md`, `EVOLUTION-ARCHITECTURE.md`.

### 1.1 Product in one line
Accountable UI exploration: generate 1–3 bounded variants → intentionally select/commit a baseline → review identity/DNA evidence → annotate with canonical comments → synthesize deterministic mutation tasks (draft) → require explicit human approval → apply → append append-only revision manifest → hand off to downstream domainspec delivery. Modeled internally as an **Evolution Engine** (population / fitness / selection / mutation / lineage) with a future proof gate.

### 1.2 Spec flow (canonical)
`prompt → variants → baseline + identity/DNA → comments → mutations → revisions → handoff`

### 1.3 Surfaces (from `UI-SPEC.md` workbench layout)
Single route `/ui-prototyping-studio`, `StudioWorkbenchLayout`. Panels:
Session Controls · Variant Canvas · Identity Evidence Panel · Annotation Panel · Mutation Approval Panel · Revision Timeline · Handoff Summary (+ `SessionStateIndicator`).

### 1.4 Load-bearing decisions (locked; defended by Lane B, challenged by Lane A)

| ID | Locked decision | Who-leads-when (current) | Friction posture |
| -- | --------------- | ------------------------ | ---------------- |
| D-001 | `shadcn/ui` + Radix + Tailwind for **studio surfaces only**. | Agent generates against primitives; human unaffected elsewhere. | Bounded adoption; contains migration risk. |
| D-002 | **HTML-first** MVP; React islands deferred. | Agent emits deterministic HTML; human reads auditable diffs. | Keeps generation/diff deterministic. |
| D-003 | Canonical comment schema `{target, severity, intent, note}`; severity `blocker/high/medium/low`. | Human authors comments; agent consumes one contract. | Stable schema → deterministic synthesis + replay. |
| D-004 | Auto-task generation is **draft-only until human confirm**. | Agent drafts; human confirms before any apply. | Keeps automation; preserves accountability gate. |
| D-005 | **Manual governance:** baseline-selection gate (`variantCount>1`) + explicit apply approval; **auto-apply forbidden.** | Human leads both gates; agent blocked from self-apply. | Protects deterministic, irreversible decision points. |
| D-006 | `variantCount` ∈ `1..3`, default `3`; `1` = committed baseline. Resets to `3` per session unless overridden. | Human chooses breadth; agent generates exactly that count. | Bounded exploration; deterministic single-path fallback. |
| D-007 | Newspaper integration is **adapter-only**, no runtime dep. | N/A (architecture). | Reuse contract shape without coupling. |
| D-008 | Model iteration as **Evolution Engine** (population/fitness/selection/mutation/lineage/environment). | N/A (model). | Makes the evolutionary engine explicit + traceable. |
| D-009 | Self-improvement / generation-rule promotion **proof-gated and deferred** in MVP. | Agent may request; human + proof gate dispose. | Prevents the system rewriting its own rules without evidence. |

**Open decisions already on record** (`DECISIONS.md` §Open): O-001 brief-normalization mandatory?, O-002 live-data mode?, **O-003 multi-cycle autonomy beyond manual gates?**, **O-004 fitness scoring model (qualitative | weighted vector | Pareto)?**, O-005 which rule types may be promoted?

### 1.5 State model (current — note the gaps)
- `StudioSessionState` (`states.md`): `SessionInitialized → PromptCaptured → VariantsReady → BaselineReady → (IdentityEvidenceConfirmed | CommentsCaptured) → MutationDrafted → MutationApproved → RevisionApplied → RevisionRecorded → {ContinueIteration ↻ | SessionCompleted}`.
- `EvolutionCycleState` (`states.md`): genome/population → selection → identity/DNA → mutation proposed/approved/applied → lineage recorded → {continue | handoff ready}; proof side is parallel (`EvaluateProofGate → ProofEvaluated`).
- **Confirmed gap (grep verified):** there are **no failure / stale / timeout / conflict states** in either machine. Every transition assumes the happy path. This is load-bearing evidence for shallow area Q5.

---

## 2. DomainSpec UI Type Vocabulary (use exact types; do NOT invent UI terms)

The synthesized design (s4) and proposal (s9) MUST be expressed entirely in these types. Source: dispatch intent + `domain.md` + `states.md` + `EVOLUTION-ARCHITECTURE.md`.

**Entities:** `StudioSession`, `PrototypeVariant`, `CommentEvent`, `MutationBatch`, `RevisionManifestEntry`, `EvolutionCycle`, `BaselineGenealogyFamily`, `FitnessSignal`, `UIElementIdentity`, `UIElementInstance`, `UIDecisionRecord`, `RulePromotionRequest`.

**Value objects:** `VariantCount(1..3, default 3)`, `GenerationMode(explore|exploit)`, `TypedReference`, `BaselineRevisionAnchor`, `AnnotationTarget(selector | elementLabel | odId)`, `UIVisualSignature` (24 controlled visual-DNA fields), `MutationTask`, `BatchApproval`, `BaselineProvenance`, `DiffSummary`, `PrototypeGenome`, `FitnessVector(preference -1|0|1 / severity / confidence 0..1 / dimension)`, `ProofObligation`, `IntegrationReadiness`.

**Enums:** `CommentSeverity(blocker|high|medium|low)`, `MutationBatchStatus(draft|approved|applied|rejected)`, `BaselineMode(selected|committed)`, `GateState(pending|satisfied|blocked)`, `FitnessSignalSource(human|test|risk|telemetry|governance)`, `UIDecisionType(select|reject|preserve|change|constrain|approve)`, `UIIdentityRelationType(same-concept|reshaped|split-from|merged-into|replaced-by|removed|new)`, `ProofStatus(pending|pass|flag|block)`, `RulePromotionStatus(deferred|rejected|promoted)`, plus **24 Visual DNA enums** (ColorRole, SurfaceTone, ContrastIntent, AccentUsage, VisualShape, CornerProfile, BorderTreatment, Elevation, AspectPattern, TypeRole, TypeWeight, TypeScale, TextTransform, NumericStyle, LayoutRole, Density, Alignment, SpacingPattern, CompositionPattern, InteractionPattern, StateModel, FeedbackStyle, MotionIntent, ElementCategory, ElementRole, Hierarchy).

**States:** `StudioSessionState` (10 states), `EvolutionCycleState` (12 states).

**Operations:** `InitializeSession`, `SubmitPrompt`, `GenerateVariants`, `SelectOrCommitBaseline`, `ConfirmUIDecisionEvidence`, `CaptureCommentEvent`, `SynthesizeMutationBatch`, `ApproveMutationBatch`, `ApplyApprovedBatch`, `RecordFitnessSignal`, `EvaluateProofGate`, `PromoteEvolutionRule`, `ExportDesignHandoff`.

**Two type rules (hard):**
- Visual DNA uses **controlled vocab + token refs**, NOT raw color/px.
- Generated identity/DNA suggestions become **durable only after a human `ConfirmUIDecisionEvidence`** (`UIDecisionType` ∈ select/reject/preserve/change/constrain/approve). This is the single most ergonomically load-bearing rule: it is where "agent proposes, human disposes" is encoded in the type system.

---

## 3. UX-Evidence-Validator Model (basis for all UX work)

Source: prompt + `arcanum/arcana/ux-evidence-validator/SKILL.md`. This is how every ergonomic claim in s5–s9 gets classified. Hard gates are **only** for deterministic or standards-backed failures.

**Six validator layers:**
- **L0 Smoke** — load/assets/console/network → *hard gate* (after calibration).
- **L1 Accessibility** — axe, ARIA snapshot, role/name/state, keyboard, forms → *hard gate + manual*.
- **L2 Layout Integrity** — overflow/clip/overlap/target-size/responsive → *hard gate*.
- **L3 Interaction Flow** — user-facing locators, task completion, visible state change → *hard gate*.
- **L4 Cognitive / Attention** — density, memory burden, salience, hierarchy → *soft flag / screenshot review*.
- **L5 Domain Practice** — design-system rule packs → *soft flag*.
- **L6 Human Evidence** — workload, comprehension, trust, real task success → *human-study residue*.

**Claim classes:** `hard_gate | soft_flag | screenshot_review | human_study | not_automatable`.
**Severity:** `block | high | medium | low | info`.
**Rule:** cognitive claims (L4/L6) need a conservative UI **proxy + fixture**; always name **what Playwright observed vs what it cannot prove** (`proxy_limit`).

**Mapping to the studio (pre-classified anchors for s6/s7):**
- D-005 apply gate disabled-reason, baseline-required errors → **L3 hard_gate** (visible state change, deterministic).
- `SessionStateIndicator` `aria-live="polite"`, focus order, focus trap on approval modal → **L1 hard_gate + manual**.
- 3-variant side-by-side comparison cognitive load → **L4 soft_flag / screenshot_review**, with an L6 human-study residue (no real-user data exists).
- "Does the human trust the agent's draft enough to approve fast but not blindly?" → **L6 human_study** (not automatable).

---

## 4. Shallow Areas the Deep-Spec MUST Resolve (highest-leverage, phrased as questions)

Each is grounded in `DISCOVERY.md`/`DECISIONS.md` open items, the dispatch rationale, or direct artifact inspection. Each carries an ergonomics lens (lead-when / load / friction) and a type anchor. Ordered by leverage.

**Q0 (meta, dominates) — Where is the human-leads-vs-agent-proposes boundary drawn, per decision point, and what is its cognitive load?** Boundary is implied by D-004/D-005 but never specified as a per-operation contract; state it for each of the 13 operations. Type anchor: `UIDecisionType`, `GateState`, `BatchApproval`. No user-validated UX evidence exists (L6 residue).

**Q1 — What fitness scoring model governs selection pressure (O-004)?** Qualitative-only vs weighted `FitnessVector` vs Pareto. Does scoring help or overload the human? Type anchor: `FitnessSignal`, `FitnessVector`, `FitnessSignalSource`.

**Q2 — How does Exploit mode measure conformance of candidates to the committed baseline/DNA?** `UI-SPEC.md` says Exploit "shows conformance" but no metric over the 24 `UIVisualSignature` fields is defined. Type anchor: `UIVisualSignature`, `BaselineGenealogyFamily`, `UIDecisionType=constrain`.

**Q3 — What is the identity/DNA suggestion REJECTION lifecycle?** `UIDecisionType` has `reject` but the rejected-suggestion lifecycle (persist as negative evidence? re-surface? feed genome?) is unspecified; rejecting must be one cheap action. Type anchor: `UIDecisionRecord`, `UIIdentityRelationType`, `PrototypeGenome`.

**Q4 — What is the component-registry data model and versioning story?** Registry named in `DISCOVERY.md` §6.2 / D-001 but absent from `domain.md` types. Type anchor: `UIElementIdentity`, `UIElementInstance`, `TypedReference`.

**Q5 — What are the error/recovery flows?** Verified gap: state machines have no failure states. Cover generation failure, synthesis timeout, stale-revision on apply, batch-apply conflict; never silently lose annotations. Type anchor: new states, `GateState=blocked`, `MutationBatchStatus`.

**Q6 — What is the cognitive load of 3-variant review, and how is decision-paralysis prevented?** Default `variantCount=3` side-by-side never validated as ergonomic. What L4 proxy bounds comparison load; what affordance (default focus / diff-against-baseline / recommended pick) prevents paralysis? Type anchor: `VariantCount`, `PrototypeVariant`, `BaselineProvenance`. L4 soft_flag + L6 residue; s8 naive-user targets this.

**Q7 — Should multi-cycle autonomy be permitted beyond manual gates, and under what envelope (O-003)?** Manual-only vs supervised vs bounded autonomous batches; reduce toil on reversible drafts, keep human-disposes on durable actions. Type anchor: `GateState`, `EvolutionCycle`, `BatchApproval`, `FitnessSignalSource=governance`.

**Q8 — What is the proof storage schema for the deferred proof gate (D-009)?** `ProofObligation`/`ProofStatus` exist as types with no persistence/lineage; bind to `RulePromotionRequest`. Type anchor: `ProofObligation`, `ProofStatus`, `RulePromotionRequest`, `RulePromotionStatus`.

**Q9 — What accessibility INTERACTION detail does the workbench guarantee?** `UI-SPEC.md` lists ARIA requirements but no interaction timing: tab order across 7 panels, focus trap + return focus on approval modal, `aria-live` timing for `SessionStateIndicator`. L1 hard_gate + manual; deterministic → s7 Playwright + axe.

**Q10 — What is the synthesis determinism + traceability contract from `CommentEvent` to `MutationTask`?** D-003/D-004 promise deterministic draft synthesis but the mapping (N mixed-severity comments → ordered tasks, dedup, conflict) is unspecified. Type anchor: `CommentEvent → MutationTask`, `MutationBatch`, `DiffSummary`.

---

## 5. Downstream Hand-Off Notes (how lanes should use this pack)

- **s1 research:** all web/GitHub sources are `external_context`; map resonant-os-design-tokens onto the 24 `UIVisualSignature` enums (consumers Q2/Q4). No promotion to canonical memory (gate g1).
- **s2 challenger (Lane A):** ≥2 novel directions in §2 types; cite s1 evidence or log residue; rank by ergonomics-gain vs cost. Targets Q1, Q2, Q6.
- **s3 defender (Lane B):** restate D-001..D-009 with §0 charter clauses; absorb-vs-reject per Lane A direction; defend manual governance via governance-is-a-feature. Targets Q0, Q5, Q7.
- **s4 synthesis:** each contested point → decision | residue | deferred; result entirely in §2 types; ergonomics-first rationale (lead-when + load + friction) per kept/changed decision.
- **s5 residuality:** stress resolved areas, especially Q5 (no failure states) and Q7 (autonomy envelope).
- **s6/s7 ux-evidence + Playwright:** classify every claim against §3; Q9/Q10/D-005-gates are hard-gate candidates; Q6 is L4/L6.
- **s8 naive-user (context-isolated):** ONLY task goals + rendered surface (gate g6, boundary b-naive-isolation). Live test of Q0, Q3, Q6.
- **s9 proposal + plan:** resolve Q1–Q5 explicitly; carry the rest as named residue with owners. Outputs are proposals only (gates g7/g8).

---

## 6. Evidence Index (citations)

| Claim | Source |
| ----- | ------ |
| Locked decisions D-001..D-009 + open O-001..O-005 | `DECISIONS.md` |
| MVP product shape, variant gate, modules, build-vs-buy, web landscape | `DISCOVERY.md` §4, §6, §10 |
| Workbench layout, panels, routes, forms, error codes, a11y reqs | `UI-SPEC.md` |
| State machines + invariants; no failure states (grep verified) | `states.md` |
| Evolution Engine model, fitness signal as evidence not ranking, O-004 open | `EVOLUTION-ARCHITECTURE.md` |
| Dispatch route, lanes, gates, subagent roles, ergonomics-first intent | `development/deep-spec-dispatch/DEEP-SPEC-DISPATCH.json`, `README.md` |
| Six validator layers, claim classes, proxy_limit rule | prompt + `arcanum/arcana/ux-evidence-validator/SKILL.md` |
| UI type vocabulary | dispatch intent + `domain.md` (confirmed in `states.md`, `EVOLUTION-ARCHITECTURE.md`) |
