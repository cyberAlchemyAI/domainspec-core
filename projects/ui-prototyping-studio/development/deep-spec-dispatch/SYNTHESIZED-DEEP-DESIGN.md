---
id: ui-prototyping-studio-synthesized-deep-design
feature: ui-prototyping-studio
title: "Synthesized Deep Design (s4): one deepened, ergonomics-first design resolving the Lane A / Lane B dialectic"
summary: >
  The load-bearing synthesis of the deep-spec dispatch. Resolves every contested point between Lane A
  (challenger / antithesis) and Lane B (defender / thesis) into exactly one of: a DECISION with an
  ergonomics-first rationale, a logged RESIDUE with an owner, or an explicitly DEFERRED option. The
  entire synthesized design is expressed in domainspec UI types (entities, value objects, enums,
  states, operations). First principle, non-negotiable: ergonomics — agentic tools that improve human
  work and form symbiotic human-agent relations; governance is a feature, not friction. Every kept or
  changed decision states who leads when (human vs agent), the cognitive load it imposes, and how it
  reduces friction. The spine (D-001..D-009) is held; the eight shallow areas are deepened to one-shot
  implementation readiness; residue is owned, not hidden.
status: draft
node_type: design
dispatch_id: ui-prototyping-studio-deep-spec-001
step_id: s4-synthesis
lane: synthesis
stance: synthesis
owners:
  - web-core
reads:
  - frame.evidence-baseline   # CONTEXT-PACK.md (s0)
  - handle.antithesis         # LANE-A-NOVEL-DESIGN.md (s2)
  - handle.thesis             # LANE-B-DEFENSE.md (s3)
updatedAt: 2026-06-15
---

# SYNTHESIZED-DEEP-DESIGN.md — Deep Design (s4 Synthesis)

**Dispatch:** `ui-prototyping-studio-deep-spec-001` · **Step:** `s4-synthesis` · **Owns:** this file (load-bearing) · **Consumes:** `handle.antithesis` (Lane A), `handle.thesis` (Lane B), `frame.evidence-baseline` (CONTEXT-PACK).

**First principle (non-negotiable):** ergonomics — agentic tools that improve human work and form synergetic, symbiotic human-agent relations. **Governance is a feature, not friction.** Every kept/changed decision below carries `lead-when` (who leads, who may act, what the human sees before durability), `load` (recognition vs recall, comparison breadth, decision count), and `friction` (the manual step removed).

## How the dialectic resolved (orientation for downstream)

The zig-zag converged before it reached me. The challenger (Lane A) attacked the *shallow areas* without attacking the *spine*, and the defender (Lane B) confirmed the spine survives every push and absorbed four of the five novel directions outright. Synthesis is therefore not a compromise between two opposed designs; it is the **deepening of one design** along the axis both lanes already agreed on:

> Make the human review the **change**, not the genome; let the agent have an **accountable opinion** but never an **unaccountable action**; remember every **yes and every no** in the token contract; **never lose the human's work**; and draw the learning wall at **session-scope** so the agent may get better at proposing without ever, quietly, changing itself.

The only genuine residual tensions were the four refinements Lane B added to Lane A's directions (override symmetry, confidence honesty, durable-not-irreversible rejection, session-scope wall). I adopt all four — each tightens a direction *toward* the first principle rather than away from it — and they appear as DECISIONS D-S1..D-S4 below.

---

## Section 1 — Resolved decisions table

Every contested or pressured point is resolved to exactly one verdict. `Verdict ∈ {DECIDE, RESIDUE, DEFER}`. Each DECIDE carries an ergonomics-first rationale (the *why* is human work, not novelty) and the domainspec UI types it touches. RESIDUE rows carry an owner; DEFER rows carry the gate behind which the option waits.

| # | Contested point (origin) | Verdict | Ergonomics-first rationale (lead-when / load / friction) | DomainSpec UI types touched |
|---|--------------------------|---------|----------------------------------------------------------|-----------------------------|
| **D-S0** | Q0 — where is the human-leads-vs-agent-proposes boundary, per operation? (CONTEXT-PACK meta-question; both lanes) | **DECIDE** | The boundary becomes a **typed three-tier lead-when matrix** over all 13 operations (Section 2.8). Human attention is spent only at tier-2 (durable) and tier-3 (rule-change) checkpoints; tier-1 (reversible) is where the agent earns its keep. Load: the human polices two named gates, not a continuous background audit. Friction: converts "is everything OK to ship?" into a bounded, recognizable, disabled-reason-carrying decision. **This is the typed form of the governance-is-a-feature clause and the parent of every other row.** | `UIDecisionType`, `GateState`, `BatchApproval`, all 13 Operations |
| **D-S1** | Direction 2 override symmetry — is override "one click away" (A) or "exactly as cheap as ratify, with disclosed weakness" (B)? | **DECIDE** (adopt B's hardening) | Override MUST cost exactly what ratify costs, and the nomination MUST disclose the champion's worst dimension. Lead-when: agent nominates (tier-1), human ratifies-or-overrides (tier-2) in one action either way. Load: 1 decision (recognition), comparison breadth ≤2 pairwise. Friction: kills decision-paralysis (Q6) without manufacturing automation bias. If override were costlier than ratify, the design would silently convert "human disposes" into "human rubber-stamps" — a first-principle violation. **Acceptance criterion, not a nicety.** | `proposedChampionLabel` (read-model field), `FitnessSignal`, `UIDecisionRecord(select)`, `SelectOrCommitBaseline`, `VariantCount` |
| **D-S2** | Direction 1 confidence honesty — is `confidence=1.0` valid for every exact enum diff (A) or only when both ends resolve to a confirmed enum/token (B)? | **DECIDE** (adopt B's honesty floor) | A delta `FitnessSignal` carries `confidence=1.0` ONLY when both signatures resolve to a confirmed enum/token; where a field is `TypedReference`-pending (the s1 ROSI underfill: Motion / Interaction / State / Feedback / Numeric) it MUST carry `confidence<1.0` or be `pending`. Lead-when: agent computes the delta (tier-1); honesty of the chip is structural, not discretionary. Load: a green "held" chip on an *unresolved* field is the worst possible outcome — false trust — so it is forbidden by type. Friction: the human trusts the conformance surface precisely because it never overclaims. | `FitnessVector(confidence)`, `UIVisualSignature`, `TypedReference`, `FitnessSignal(source=governance)` |
| **D-S3** | Direction 3 reversibility — is a human rejection durable (A's emphasis) or durable-AND-irreversible (the latent risk)? | **DECIDE** (adopt B's durable ≠ irreversible) | A `UIDecisionType=reject` is **durable** (persists as negative evidence, never silently re-surfaced) but **reversible by the human** via a later `UIDecisionRecord(change|select)`. Lead-when: human disposes the reject (tier-2) and human disposes any recovery (tier-2); the agent honors but never invents either. Load: decreasing over a session (system gets quieter as taste accrues). Friction: prevents "the system got quieter" from degrading into silent capability loss / lock-in. Only `ApplyApprovedBatch` and `SelectOrCommitBaseline` are the truly irreversible boundaries. | `UIDecisionRecord(reject/change/select)`, `UIIdentityRelationType`, `PrototypeGenome`, `FitnessSignal(source=human, preference=-1)` |
| **D-S4** | Direction 4 wall location — "reversible vs irreversible" (A) or "session-scope as the operational test" (B)? | **DECIDE** (adopt B's session-scope test) + **DEFER rule-track** | The wall predicate is a single checkable test: *does this change survive a fresh session with no accumulated signals?* If yes → it is a **rule** (irreversible across sessions) → gated by `RulePromotionRequest` + `ProofObligation` + `EvaluateProofGate=pass` + human `PromoteEvolutionRule`. If no → it is a **proposal default** (session-scoped, reversible) → ungated. Lead-when: agent may tune reversible proposals (tier-1); human disposes durable (tier-2); human + `ProofStatus=pass` jointly dispose rule changes (tier-3). The rule-track is **DEFERRED in MVP behind D-009** (every `RulePromotionRequest` resolves `deferred`); the proposal-track is built. Load/friction: fewer re-corrections per cycle without the agent ever rewriting itself behind the human's back. | `RulePromotionRequest`, `ProofObligation`, `ProofStatus`, `EvaluateProofGate`, `PromoteEvolutionRule`, `RulePromotionStatus`, `FitnessSignal(source=human)` |
| **D1** | Direction 1 — conformance delta as the primary exploit-mode review surface (A proposed; B absorbed fully) | **DECIDE** | Exploit-mode conformance = signed field-delta over two `UIVisualSignature`s, each delta a `FitnessSignal(source=governance)`; a delta on a `constrain`-locked field sets `GateState=blocked` on that candidate's selectability *with the reason surfaced*. Lead-when: agent computes the delta (judgment-free, tier-1); human locks/accepts per field (tier-2). Load: collapses 3×24=72 cells to 2-5 changed fields (recognition over recall). Friction: makes on-brand-ness recognizable and constraints resumable across cycles. | `DiffSummary`, `UIVisualSignature`, `FitnessSignal(source=governance)`, `UIDecisionType(constrain/change/preserve)`, `GateState(blocked)`, `PrototypeGenome` |
| **D2** | Direction 2 — champion + challengers framing (A proposed; B absorbed with two guardrails) | **DECIDE** (with D-S1 guardrails) | Agent nominates one `proposedChampionLabel` (non-durable read-model field) with evidence-linked rationale; human ratifies or overrides; **never auto-select** (D-005 held). Degrades gracefully: at `variantCount=1` no champion; on a tie, co-challengers with *no* nominated champion (an arbitrary tiebreak is an unaccountable opinion). Lead-when / load / friction per D-S1. | `proposedChampionLabel`, `FitnessSignal`, `SelectOrCommitBaseline`, `UIDecisionRecord(select)`, `VariantCount` |
| **D3** | Direction 3 — rejection as durable negative evidence (A proposed; B absorbed) | **DECIDE** (with D-S3 reversibility) | `UIDecisionType=reject` is a durable, reversible relation typed by `UIIdentityRelationType` (`replaced-by`/`removed`/`reshaped`/`merged-into`/`split-from`); folded into `PrototypeGenome` as a negative constraint `GenerateVariants` must honor. Lead-when: human disposes; agent honors. Load: low per occurrence, decreasing over session. Friction: a no is remembered, never re-fought. | `UIDecisionRecord(reject)`, `UIIdentityRelationType`, `PrototypeGenome`, `FitnessSignal(source=human)` |
| **D4-prop** | Direction 4 reversible half — proposal-tuning from accumulated human signals | **DECIDE** (ungated, session-scoped) | Accumulated `FitnessSignal(source=human)` deterministically tunes the next nomination (D2) and generation defaults, session-scoped. Must be **visible** ("agent now defaults to `Density=comfortable` because you chose it 3×") and **reversible in one action**. Lead-when: agent tunes reversible proposals (tier-1); human disposes every durable boundary unchanged. Load: fewer re-corrections. Friction: the agent meets the human where they already are. A gate here would be friction on a reversible draft (governance-is-a-feature clause's own test). | `FitnessSignal(source=human)`, `PrototypeGenome`, `proposedChampionLabel`, `GenerationMode` |
| **D4-rule** | Direction 4 irreversible half — generation-rule promotion | **DEFER** (behind D-009 / `EvaluateProofGate`) | Specified, not built. Every `RulePromotionRequest` resolves `RulePromotionStatus=deferred` in MVP. Un-defers only with a passing `ProofObligation` and a human `PromoteEvolutionRule`. Lead-when: human + proof jointly dispose (tier-3). Rationale: the wall is the precondition that makes future autonomy a *human decision* rather than a *system fait accompli*. | `RulePromotionRequest`, `ProofObligation`, `EvaluateProofGate`, `PromoteEvolutionRule`, `RulePromotionStatus` |
| **D5** | Direction 5 — failure & recovery as first-class states (both lanes; ranked #1 in necessity) | **DECIDE** (foundation-first) | Additive named states (`GenerationFailed`, `SynthesisTimedOut`, `SourceStale`, `ApplyConflicted`) on `StudioSessionState`/`EvolutionCycleState`; `GateState=blocked` carries the reason; append-only `CommentEvent` and draft `MutationBatch` are never lost; no path auto-applies or auto-discards. Lead-when: agent detects + reports honestly (tier-1); human disposes recovery (tier-2). Load: removes anxiety + recall under failure (named state + one-line reason + single safe action). Friction: "safe to retry" is a type-backed claim because of D-002 determinism. | `StudioSessionState`(+4), `EvolutionCycleState`(+4), `GateState(blocked)`, `MutationBatchStatus`, `BaselineRevisionAnchor`, `CommentEvent` |
| **D-XC** | Cross-cutting — "no raw values" as a named `ProofObligation` checked by `EvaluateProofGate` (A proposed; B absorbed shape-only) | **DECIDE** (shape-only) + **RESIDUE** (semantic confirm stays human) | The obligation checks **shape** (every `UIVisualSignature` field resolves to a controlled-vocab enum or a `TypedReference` into the token namespace; zero raw px/color) — deterministic, a legitimate hard gate. It MUST NEVER check **meaning** (which enum is "correct"), which stays human-confirmed via `ConfirmUIDecisionEvidence` (W3C-DTCG caveat: token group names are not semantically load-bearing). Lead-when: agent/gate proves shape (tier-1/gate); human disposes meaning (tier-2). Friction: makes D1 diffs honest, D2 rationales reproducible, D4 preferences auditable. | `ProofObligation`, `EvaluateProofGate`, `ProofStatus`, `UIVisualSignature`, `TypedReference`, `ConfirmUIDecisionEvidence` |
| **D-001..D-003, D-006..D-008** | Spine assumptions the challenger relied on | **DECIDE — HELD** | The challenger validated the spine by building on it five times. D-002 (HTML-first) is the substrate of A's own "safe to retry" and "reproducible nomination" claims; D-003 (canonical comments) makes synthesis replayable; D-006 (`variantCount` 1..3) reframed as an *ergonomic ceiling the agent may underfill*, not a fixed default; D-008 (`FitnessSignal` is evidence, not ranking) is the spine every direction routes through. | `GenerationMode`, `VariantCount`, `CommentEvent`, `DiffSummary`, `FitnessSignal`, `FitnessVector` |
| **D-004 / D-005 / D-009** | Manual governance + draft-first + proof-gated self-improvement | **DECIDE — HELD, hardened** | D-004: agent drafts (`MutationBatchStatus=draft`), human confirms (`approved`) — recognition over authoring. D-005: gate placed ONLY on irreversible steps (`SelectOrCommitBaseline`, `ApplyApprovedBatch`); reversible ops explicitly agent-may-act so the gate never creeps onto drafts. D-009: the wall that makes D4 buildable. The gates are not the price of the good ideas; they are the precondition for them. | `MutationBatchStatus`, `BatchApproval`, `GateState`, all gated Operations |
| **Q1 / O-004** | Fitness scoring model — qualitative vs weighted vector vs Pareto | **DECIDE** | **No composite score, ever.** Fitness is a set of named, human-readable `FitnessSignal`s; selection is a human act the agent may justify but never perform. Pareto over a small human-locked set of named dimensions (D1+D2). Lead-when: human owns the weights (by locking dimensions); agent owns the measurement. Load: the human reads facts, not arithmetic. Friction: a single number invites automation bias; named evidence invites informed disposal. | `FitnessSignal`, `FitnessVector(preference/severity/confidence/dimension)`, `FitnessSignalSource`, `UIDecisionType(constrain)` |
| **Q4** | Component registry data model & versioning | **RESIDUE** (owner s4→s9) + partial DECIDE | Partial decision landed: `UIElementIdentity` = stable concept node; `UIElementInstance` = versioned realization; the version edge typed by `UIIdentityRelationType` (`replaced-by` successor, `reshaped` same-concept evolution, `same-concept` reuse); `TypedReference` indexes instances→identities. This gives matching + versioning *for free* from D3. The **persistence/indexing entity itself remains residue.** Ergonomic anchor: the agent must reuse known `UIElementIdentity` nodes so the human recognizes components (recognition-over-recall). | `UIElementIdentity`, `UIElementInstance`, `UIIdentityRelationType`, `TypedReference` |
| **Q8** | Proof storage schema | **DECIDE — specify, do not build** | `ProofObligation` and `RulePromotionRequest` schemas specified (Section 2 / 3) so D-009's deferral is a *specified decision with a schema*, not an open hole. Gating predicate = the session-scope test (D-S4). In MVP every `RulePromotionRequest` resolves `deferred`. | `ProofObligation`, `ProofStatus`, `RulePromotionRequest`, `RulePromotionStatus`, `TypedReference` |
| **Q9** | Accessibility interaction detail | **DECIDE** (hard-gate deterministic parts) | Tab order across 7 panels = reading order; focus trap + return-focus on the `ApplyApprovedBatch` approval modal; `aria-live="polite"` announces session/failure state once. Governance gates fully keyboard-operable — governance must not be a mouse-only privilege. Maps to L1 hard_gate + manual (s7 Playwright + axe). | `SessionStateIndicator` (read-model), `GateState`, `StudioSessionState` |
| **Q10** | Synthesis determinism `CommentEvent → MutationTask` | **DECIDE** (contract) + **RESIDUE** (full conflict algebra) | Pure, ordered, deterministic fold: sort by `CommentSeverity` (blocker→high→medium→low) then stable `AnnotationTarget` order; dedup on identical `(target, intent)`; conflicting tasks on one target surface as a single `MutationTask` with both intents noted, never silently dropped. Predictability is the load-reducer (approve fast but not blind). **Full conflict algebra remains residue (owner s4→s9).** | `CommentEvent`, `MutationTask`, `MutationBatch`, `DiffSummary`, `CommentSeverity`, `AnnotationTarget` |
| **L4/L6 ergonomics floor** | Are any ergonomic gains proven? | **RESIDUE — explicit** | **No ergonomic gain in this document is asserted as proven.** Every claim is L4 soft_flag / screenshot_review or L6 human-study residue. The s8 naive-user lane is the live test of Q0, Q3, Q6. | (validator classification, §3 of CONTEXT-PACK) |

---

## Section 2 — Deepened design per shallow area

Each subsection is expressed in §2 vocabulary and carries lead-when / load / friction. Ordered by the CONTEXT-PACK leverage ranking, with Q0 first because every other answer inherits its posture.

### 2.1 Fitness scoring model (Q1 / O-004)

**Decision: named-signal Pareto; no composite score, ever.**

- **Type expression.** Fitness is never a number. It is a set of `FitnessSignal` entities, each carrying a `FitnessVector(preference ∈ {-1,0,1}, severity, confidence ∈ 0..1, dimension)` and a `FitnessSignalSource ∈ {human, test, risk, telemetry, governance}`.
  - `source=human` signals: the human owns `preference` and `severity` (this is how the human "owns the weights" without ever touching a weight vector).
  - `source ∈ {governance, test, risk}` signals: deterministic, agent-supplied (e.g., a conformance delta is `source=governance`; an axe blocker is `source=risk`).
- **Selection.** Selection is `SelectOrCommitBaseline`, a tier-2 human act. The agent may *justify* it (D2 nomination) but may never *perform* it.
- **Pareto, not weighted.** Candidates are compared on the *set* of named dimensions the human has locked (`UIDecisionType=constrain`); a candidate dominated on every locked dimension is surfaced as such, but no scalar score is ever computed or shown.
- **Lead-when:** human owns weights (by locking dimensions), agent owns measurement. **Load:** the human reads facts, not arithmetic; comparison breadth bounded to locked dimensions. **Friction:** a single composite number invites "the system said B is best" automation bias; named evidence invites "B drifted on two unlocked fields and has zero axe blockers — ratify?".

### 2.2 Exploit-mode conformance metric (Q2 / D1)

**Decision: signed field-delta over `UIVisualSignature`, each delta a governance `FitnessSignal`, with confidence honesty (D-S2) and constrain-lock blocking.**

- **Type expression.** Conformance = a `DiffSummary` over two `UIVisualSignature`s (committed `BaselineRevisionAnchor` vs candidate). Each of the up-to-24 field deltas becomes a `FitnessSignal(source=governance, dimension=<DNA field>, preference ∈ {-1,0,1})`.
- **Confidence honesty (D-S2).** `confidence=1.0` only when *both* ends resolve to a confirmed enum/token. For `TypedReference`-pending fields (Motion / Interaction / State / Feedback / Numeric per the s1 ROSI underfill) the signal carries `confidence<1.0` or `pending`. A green "held" chip on an unresolved field is forbidden — false trust is the worst ergonomic outcome.
- **Constrain-lock enforcement.** A delta on a `constrain`-locked field sets `GateState=blocked` on that candidate's *selectability*, with the disabled-reason surfaced (reusing D-005's disabled-reason contract). The human is never silently prevented from selecting — they see *why*.
- **Genome fold.** Locked fields fold into `PrototypeGenome` as constraints on the next `GenerateVariants` (constraints resumable across cycles).
- **Lead-when:** agent computes the delta (tier-1, judgment-free) and *proposes* which deltas look intentional; human disposes the lock/accept per field via `ConfirmUIDecisionEvidence` (tier-2). **Load:** 72 cells → 2-5 changed fields. **Friction:** on-brand-ness becomes recognizable; the human reads the same diff format every cycle.

### 2.3 Identity / DNA rejection lifecycle (Q3 / D3)

**Decision: durable, reversible negative evidence typed as a relation.**

- **Type expression.** A rejection is `UIDecisionRecord(UIDecisionType=reject)`, durable only via `ConfirmUIDecisionEvidence`. The *why* is typed by `UIIdentityRelationType` — a rejection is a relation, not a void: `replaced-by` (a successor identity supersedes it), `removed` (the identity should not recur), `reshaped` (same concept, different realization), `merged-into` / `split-from`. A `FitnessSignal(source=human, preference=-1, dimension=<element/DNA field>)` records the selection pressure.
- **Genome fold.** The rejected suggestion folds into `PrototypeGenome` as a negative constraint: `GenerateVariants` must not regenerate a `removed` identity and must respect a `replaced-by` mapping.
- **Durable ≠ irreversible (D-S3).** A `removed` identity the human later wants back is recoverable via a new `UIDecisionRecord(change | select)`. The negative constraint is durable, not irreversible; only `ApplyApprovedBatch` and `SelectOrCommitBaseline` are irreversible.
- **Lead-when:** human disposes every rejection (tier-2); agent *honors* it (reads negative evidence, does not re-propose). **Load:** very low per occurrence, decreasing over a session (the system gets quieter as taste accumulates — the opposite of decision fatigue). **Friction:** a no is remembered in the token contract, never re-fought every generation.

### 2.4 Component registry model (Q4)

**Decision (R-1 closed 2026-06-24, A1 / `DEC`-goal-loop).** The registry entity is now specified — see [`UIIdentityIndex-DESIGN.md`](../component-registry-spec/UIIdentityIndex-DESIGN.md). The typed identity/instance/edge vocabulary below lands as before; the previously-residual persistence/index entity is closed as **`UIIdentityIndex`**: a **repo-scoped, derived, regenerable read-model** over the append-only event log (no new durable entity name), keyed by `UIElementIdentity` via `TypedReference`, aggregating across session logs so cross-session recognition and `BaselineGenealogyFamily` lineages resolve. Matching is two-phase: `data-od-id` equality (exact, ships first) → `DiffSummary` DNA-similarity *proposes* an edge → human confirms. The components page is a read-model projection of the index.

- **What lands now (decision).**
  - `UIElementIdentity` = the stable concept node ("primary button", "filter chip").
  - `UIElementInstance` = a versioned realization of an identity within a `PrototypeVariant`.
  - The version edge between successive instances is typed by `UIIdentityRelationType`: `replaced-by` (D3 successor), `reshaped` (same-concept evolution), `same-concept` (reuse), `new` (first appearance), `split-from` / `merged-into` (structural change).
  - `TypedReference` indexes `UIElementInstance` → `UIElementIdentity`.
  - This inherits matching + versioning semantics *for free* from D3's relation vocabulary.
- **Persistence / indexing entity (specified — R-1 closed).** `UIIdentityIndex` is a derived projection over the append-only event log, **repo-scoped** and **regenerable** (a rebuildable cache, stamped *do not edit*; the event log stays the single source of truth). It stores/queries identities across sessions and `BaselineGenealogyFamily` lineages without introducing a second canonical store or a new entity name (A1-invariant). Full field shape in [`UIIdentityIndex-DESIGN.md` §2](../component-registry-spec/UIIdentityIndex-DESIGN.md). Implementation (`models.ts` types + the projection) remains a gated build node (A2), not a design hole.
- **Ergonomic anchor:** the agent must *reuse* known `UIElementIdentity` nodes so the human *recognizes* components rather than re-learning novel ones each run — recognition-over-recall as the registry's design goal, not just an implementation detail.

### 2.5 Accessibility interaction detail (Q9)

**Decision: hard-gate the deterministic parts; governance is keyboard-first.**

- **Type/surface expression.** Across the 7 workbench panels (Session Controls · Variant Canvas · Identity Evidence · Annotation · Mutation Approval · Revision Timeline · Handoff Summary) plus `SessionStateIndicator`:
  - Tab order follows reading order across panels.
  - Focus trap + return-focus on the `ApplyApprovedBatch` approval modal (the irreversible gate).
  - `aria-live="polite"` on `SessionStateIndicator` announces each `StudioSessionState` transition — including the D5 failure states — *once*, not spammed.
  - All gates (`SelectOrCommitBaseline`, `ApproveMutationBatch`, `ApplyApprovedBatch`) are fully keyboard-operable.
- **Validator class:** L1 hard_gate + manual; deterministic → s7 Playwright + axe.
- **Lead-when:** the human operates every gate by keyboard alone (tier-2 governance must be universal). **Load:** announce-once prevents auditory spam. **Friction:** governance is not a mouse-only privilege — keyboard users dispose durable actions exactly as mouse users do.

### 2.6 Error / recovery flows (Q5 / D5) — foundation-first

**Decision: four additive failure states, each with a preserved / safe-retry / recovery contract.**

Additive on `StudioSessionState` (10→14) and the mutation/apply portion of `EvolutionCycleState` (12→16); no new entity. `GateState=blocked` carries the reason; `aria-live="polite"` announces once (Q9); recovery is keyboard-first. **No path auto-applies or auto-discards annotations.**

| Failure class | New state | Preserved | Safe-retry basis | Recovery (human disposes, tier-2) |
|---------------|-----------|-----------|------------------|-----------------------------------|
| Generation failure | `GenerationFailed` | prompt, prior baseline | D-002 determinism: same genome → same output | retry / discard |
| Synthesis timeout | `SynthesisTimedOut` | append-only `CommentEvent` stream, draft `MutationBatch` | comments are the durable source; synthesis is replayable | retry synthesis / discard draft |
| Stale revision on apply | `SourceStale` (detected vs `BaselineRevisionAnchor`) | draft `MutationBatch`, comments | re-anchor recomputes against current baseline | re-anchor and retry / discard |
| Batch-apply conflict | `ApplyConflicted` (`MutationBatch` returns to a recoverable `MutationBatchStatus`) | the batch, comments | deterministic re-diff | resolve / re-approve / discard |

- **Lead-when:** agent detects and reports honestly — what failed, what is preserved, what is safe to retry (tier-1); human disposes recovery (tier-2). Failure never auto-resolves into a durable change. **Load:** removes the worst load — anxiety + recall under failure; a named state + one-line reason + single safe action beats a cryptic error and "did I lose my comments?". **Friction:** "safe to retry" is a *type-backed* claim (D-002 determinism guarantees retry never silently produces a different design). This is the trust substrate D2 and D4 stand on — it is ranked #1 in necessity by both lanes.

### 2.7 Cognitive-load / decision-paralysis handling (Q6 / D2)

**Decision: champion + challengers with the two D-S1 guardrails; D-006 as an ergonomic ceiling.**

- **Type expression.** `proposedChampionLabel` is a *non-durable read-model field* (mirroring how identity/DNA suggestions are non-durable until confirmed) — explicitly **not** a `BaselineRevisionAnchor`, which exists only after a human `SelectOrCommitBaseline`. The rationale is one or more `FitnessSignal`s (`source ∈ {governance, risk, test}`, explicit `dimension`). Ratify = `SelectOrCommitBaseline` unchanged; override = the same op with a different label, recorded as `UIDecisionRecord(UIDecisionType=select)` whose rationale captures the disagreement.
- **Guardrail 1 (D-S1, deterministic + worst-dimension disclosure).** The nomination is "fewest blocking `FitnessSignal`s", computed deterministically (same candidates + same signals → same champion). The rationale renderer MUST name the champion's *worst* dimension. A one-sided rationale is an automation-bias generator and is rejected.
- **Guardrail 2 (graceful degradation).** At `variantCount=1` there is no champion to nominate. On a tie on blocking signals, the system presents co-challengers with *no* nominated champion ("no clear champion; here is why each leads") rather than breaking the tie arbitrarily — an arbitrary tiebreak is an unaccountable opinion.
- **D-006 reframed (ergonomic ceiling).** `default=3` is a *ceiling the agent may underfill*: in exploit mode under heavy constraints the agent may propose 2 (champion + 1 challenger) if a third adds no decision-relevant variance; the human can still request 3. Bounded breadth without manufacturing slot-filling variants.
- **Lead-when:** agent nominates + assembles rationale (tier-1); human ratifies-or-overrides (tier-2). **Override must cost exactly what ratify costs** (D-S1). **Load:** drops from "rank 3 from scratch" (open-ended, recall-heavy, paralysis-prone) to "ratify or veto one pre-surfaced candidate" (recognition + 1 decision); comparison breadth ≤2 pairwise. **Friction:** kills paralysis without manufacturing rubber-stamping.
- **Evidence:** L4 soft_flag (the proxy: comparison breadth ≤2, decision count = 1) + L6 human-study residue (s8 naive-user lane is the live test).

### 2.8 Human-vs-agent lead boundary (Q0 / Q7) — the parent decision

**Decision: a typed three-tier lead-when matrix over all 13 operations.** This is the canonical answer to Q0, the typed form of the governance-is-a-feature clause, and the operational definition of the Q7 autonomy envelope ("supervised autonomy" = agent free in tier 1, human disposes in tier 2, human + proof in tier 3).

| Tier | Operations | Who leads | Agent may act alone? | What the human sees before durability |
|------|-----------|-----------|----------------------|---------------------------------------|
| **1 — Reversible (agent-may-act)** | `InitializeSession`, `SubmitPrompt`, `GenerateVariants`, `SynthesizeMutationBatch` (→draft), `RecordFitnessSignal` (governance/test/risk sources), nomination of `proposedChampionLabel`, conformance-delta computation, proposal-tuning (D4-prop) | Agent | **Yes** — reversible, no durable effect | N/A (no durable change) |
| **2 — Durable (human-disposes)** | `SelectOrCommitBaseline`, `ConfirmUIDecisionEvidence` (select/reject/preserve/change/constrain), `ApproveMutationBatch`, `ApplyApprovedBatch`, `ExportDesignHandoff` | Human | **No** | the proposal + its evidence + the disabled-reason if `GateState=blocked` |
| **3 — Rule-change (human + proof dispose)** | `EvaluateProofGate`, `PromoteEvolutionRule` | Human + `ProofStatus=pass` | **No** (DEFERRED in MVP, D-009) | the `ProofObligation` record + `RulePromotionRequest` |

- **Q7 envelope (O-003).** The autonomy envelope *is* this matrix's three tiers. Reversible autonomy: yes. Irreversible autonomy: no. Rule-change: proof-gated and deferred. The session-scope test (D-S4) is what assigns a borderline behavior to tier 1 vs tier 3: a tuning that survives a fresh, signal-less session is a rule (tier 3); one that does not is a proposal default (tier 1).
- **Lead-when:** the human's attention is spent only at tiers 2 and 3 — bounded, recognizable, named. Tier 1 is where the agent earns its keep. **Load:** the human polices two named checkpoints, not a continuous audit. **Friction:** trust becomes *structural* — the human can let the agent run free where mistakes are cheap because nothing durable happens without their `BatchApproval`. The gate is what makes delegation psychologically affordable.

### 2.9 Synthesis determinism (Q10) and proof schema (Q8) — supporting deepenings

- **Q10 fold (decision + residue).** `CommentEvent → MutationTask` is a pure, ordered, deterministic function: sort comments by `CommentSeverity` (blocker→high→medium→low) then by stable `AnnotationTarget` order; dedup on identical `(target, intent)`; conflicting tasks on the same target surface as a single `MutationTask` with both intents noted, never silently dropped; the result is a `MutationBatch(draft)` the human reviews as a `DiffSummary`. Same comments → same ordered tasks (predictability lets the human approve fast but not blind, D-004). **Full conflict algebra remains s4→s9 residue.**
- **Q8 proof schema (decision: specify, do not build).** A `ProofObligation` records: `obligationId`; the `dimension`/claim it asserts (e.g., "no raw values in `UIVisualSignature`"); a `ProofStatus(pending|pass|flag|block)`; an evidence reference (`TypedReference` to the deterministic check output); and the `RulePromotionRequest` it binds to. A `RulePromotionRequest` records: the proposed rule change; the accumulated `FitnessSignal(source=human)` evidence motivating it; the bound `ProofObligation`(s); and a `RulePromotionStatus(deferred|rejected|promoted)`. The session-scope test (D-S4) is the gating predicate. In MVP every `RulePromotionRequest` resolves `deferred` — D-009's deferral becomes a specified decision with a schema, not an open hole.

---

## Section 3 — New / changed domainspec UI types (field-level detail)

No new *entity* names are introduced beyond the §2 vocabulary; the deepening is achieved by (a) additive enum states, (b) field-level specification of existing value objects, and (c) one explicitly non-durable read-model field. This is deliberate: staying inside the vocabulary keeps the design auditable and keeps "agent proposes, human disposes" encoded in the existing type rules.

### 3.1 Changed enums (additive states)

**`StudioSessionState`** — 10 → 14 states. Add the four D5 failure states as recoverable branches off the happy path:
- `GenerationFailed` — reached from the `GenerateVariants` step; preserves prompt + prior baseline; transitions to retry (back to `PromptCaptured`/`VariantsReady`) or discard.
- `SynthesisTimedOut` — reached from `SynthesizeMutationBatch`; preserves the append-only `CommentEvent` stream + draft `MutationBatch`; transitions to retry-synthesis or discard-draft.
- `SourceStale` — reached on `ApplyApprovedBatch` precheck when the candidate's `BaselineRevisionAnchor` no longer matches the current baseline; preserves draft + comments; transitions to re-anchor-and-retry or discard.
- `ApplyConflicted` — reached on `ApplyApprovedBatch` when the deterministic re-diff conflicts; returns the `MutationBatch` to a recoverable `MutationBatchStatus`; transitions to resolve / re-approve / discard.

**`EvolutionCycleState`** — 12 → 16 states. The same four failure states added on the mutation/apply portion of the cycle machine (generation, synthesis, apply-staleness, apply-conflict), mirroring the session machine so lineage stays consistent.

**No change** to: `CommentSeverity`, `MutationBatchStatus`, `BaselineMode`, `GateState`, `FitnessSignalSource`, `UIDecisionType`, `UIIdentityRelationType`, `ProofStatus`, `RulePromotionStatus`, the 24 Visual DNA enums. Each is *used* as deepened below but its value set is unchanged — a deliberate constraint that proves the deepening needs no new vocabulary.

### 3.2 Field-level specification of value objects

**`FitnessVector`** (used by `FitnessSignal`). Fields, now fully specified:
- `preference ∈ {-1, 0, 1}` — for `source=human` the human assigns it; for `source ∈ {governance,test,risk}` the agent derives it deterministically.
- `severity` — ranked (block/high/medium/low/info per the validator severity scale); human-assigned for `source=human`.
- `confidence ∈ 0..1` — **D-S2 honesty rule:** `=1.0` only when both ends of a comparison resolve to a confirmed enum/token; `<1.0` or `pending` when a `TypedReference` is unresolved.
- `dimension` — the named DNA field or element identity the signal speaks to (this is what makes fitness Pareto-comparable without a composite score, Q1).

**`DiffSummary`** (the conformance artifact, Q2/D1). Specified as: an ordered list of per-field deltas over two `UIVisualSignature`s, each delta = `{dimension, fromValue, toValue, preference, confidence}`, each surfaced as a `FitnessSignal(source=governance)`. A delta on a `constrain`-locked dimension additionally carries a `GateState=blocked` flag with a surfaced reason.

**`PrototypeGenome`**. Now carries two constraint sets folded from `UIDecisionRecord`s: **positive constraints** (`constrain`-locked fields that the next `GenerateVariants` must hold) and **negative constraints** (`reject`-typed identities/fields that `GenerateVariants` must not regenerate, honoring any `replaced-by` mapping). This is where D3 (durable nos) and D1 (locked fields) physically influence generation.

**`ProofObligation`** (Q8). Fields: `obligationId`; `claim`/`dimension` (the assertion, e.g., "no raw values"); `ProofStatus(pending|pass|flag|block)`; `evidenceRef: TypedReference` (to the deterministic check output); `bindsTo: RulePromotionRequest`. Shape-only (D-XC): it checks structure, never meaning.

**`RulePromotionRequest`** (Q8). Fields: `proposedRuleChange`; `motivatingEvidence: FitnessSignal(source=human)[]`; `boundObligations: ProofObligation[]`; `RulePromotionStatus(deferred|rejected|promoted)`. In MVP `status` is always `deferred`.

### 3.3 One new non-durable read-model field

**`proposedChampionLabel`** (D2/Q6). A *non-durable read-model* field on the variant-comparison surface — explicitly **not** persisted, **not** a `BaselineRevisionAnchor`, **not** a `UIDecisionRecord` until the human acts. It references: the nominated `PrototypeVariant`; the deterministic nomination basis (fewest blocking `FitnessSignal`s); and a rationale that MUST include the champion's worst dimension. It vanishes if the human overrides — the durable fact is the human's `SelectOrCommitBaseline` → `UIDecisionRecord(select)`, never the agent's nomination. This is the type-level guarantee that the agent has an opinion but never an action.

### 3.4 Unchanged but newly load-bearing

`BaselineRevisionAnchor` is now the staleness oracle for `SourceStale` (Q5). `CommentEvent` (append-only, D-003) is the never-lost durable source under every failure state. `BatchApproval` is the tier-2 disposal token referenced by the lead-when matrix. `TypedReference` is the index for the registry edge (Q4) and the proof evidence pointer (Q8). None changed shape; all gained a specified role.

---

## Section 4 — Residue ledger

Every item below is owned, not hidden. RESIDUE = unspecified work passed forward; DEFER = an option intentionally walled behind a gate.

| ID | Type | Item | Owner | Gate / un-defer condition | Why it is residue, not a decision |
|----|------|------|-------|---------------------------|-----------------------------------|
| R-1 | ~~RESIDUE~~ **CLOSED** (2026-06-24, A1) | Component-registry **persistence/indexing entity** (Q4) — specified as **`UIIdentityIndex`**, a repo-scoped derived read-model over the append-only event log (see §2.4 + `UIIdentityIndex-DESIGN.md`). | s4 → **A2 build** | Design closed; A2 = implement `models.ts` types + the projection (gated on L4). | Was residue because neither lane specified the entity; now specified inside the existing vocabulary (no new entity name), so the design hole is closed. Implementation, not specification, is what remains. |
| R-2 | RESIDUE | **Full conflict algebra** for `CommentEvent → MutationTask` (Q10). The deterministic fold (sort/dedup/co-locate) is decided; the complete algebra for multi-intent conflicts on one target beyond "note both" is not. | **s4 → s9** | s9 plan, or implementation spec. | The contract is enough for predictable approval; the full algebra is an implementation-depth concern, not a one-shot blocker. |
| R-3 | DEFER | **Rule-track preference learning** (D4-rule / Q7 / O-003). Generation-rule promotion. | human + `ProofStatus=pass` | `EvaluateProofGate=pass` + human `PromoteEvolutionRule`; un-defers per D-009/EC5. In MVP every `RulePromotionRequest` = `deferred`. | D-009 deferral is the only wall between "agent got better at proposing" and "agent changed itself." Specified-not-built is the principled middle. |
| R-4 | RESIDUE | **Semantic correctness of enum/token binding** (D-XC). The proof gate checks shape (no raw values); which enum is *meaningfully* correct stays human-confirmed. | **human** (per `ConfirmUIDecisionEvidence`) | Never automated — W3C-DTCG caveat (token group names not semantically load-bearing). | Conflating shape and meaning would let the gate make a judgment that belongs to the human — a governance regression dressed as automation. |
| R-5 | RESIDUE | **The entire ergonomics floor.** No ergonomic gain in this document is asserted as proven. | **s8** (naive-user lane), s6/s7 (validator) | L4 soft_flag / screenshot_review (s6/s7); L6 human-study (s8). | The first principle is the *design goal*; the *evidence* for it is the live test. s8 is where a fresh user stalls on Q0/Q3/Q6. Calling any gain "proven" here would violate the evidence-floor clause. |
| R-6 | RESIDUE | **Open decisions outside this dispatch's scope.** O-001 (brief normalization), O-002 (live-data mode), O-005 (which rule types may be promoted). | s9 / future route | Out of the deep-spec convergence set (Q1-Q5 are the required resolutions). | These are on record in `DECISIONS.md §Open` but were not the leverage targets; carried forward so nothing is silently dropped. O-005 in particular is the natural companion to R-3 when D-009 un-defers. |
| R-7 | RESIDUE (approach decided, 2026-06-24) | **`TypedReference`-pending DNA fields** (s1 ROSI underfill: Motion / Interaction / State / Feedback / Numeric). These drive D-S2's `confidence<1.0` rule but their token-namespace mapping is incomplete. | s1 → A2/A3 | Token mapping completion. **Decided approach (A1):** fill from resonant token **namespace-names as enum members** (`MOTION_EMPHASIZED`, `NUMERIC_STEP_3`) — never literal values (holds the no-raw-values rule), `external_context`/no-promotion, no vendoring. Provenance recorded. | The honesty rule (D-S2) makes the underfill *safe* (no false 1.0); the fill approach is now decided, the per-dimension enum members remain to be authored (A3). |

---

## Net position handed forward (to s5 residuality, s6/s7 validator, s8 naive-user, s9 proposal)

- **Spine held:** D-001..D-009 survive intact; the challenger validated them by building on them five times. Manual governance (D-005), draft-first (D-004), and proof-gating (D-009) are hardened, not loosened.
- **Decided:** the lead-when matrix (D-S0/Q0), conformance delta (D1/Q2), champion framing (D2/Q6), durable-reversible rejection (D3/Q3), named-signal Pareto fitness (Q1/O-004), reversible proposal-tuning (D4-prop), failure/recovery states (D5/Q5), shape-only proof obligation (D-XC), a11y interaction detail (Q9), the deterministic synthesis fold (Q10), and the four convergence refinements (D-S1 override symmetry, D-S2 confidence honesty, D-S3 durable≠irreversible, D-S4 session-scope wall).
- **Deferred:** rule-track learning (R-3), specified-not-built behind D-009.
- **Residue, owned:** registry entity (R-1, s9), full conflict algebra (R-2, s9), semantic binding stays human (R-4), the ergonomics floor is unproven (R-5, s8), out-of-scope opens (R-6), and the ROSI token underfill (R-7, s1→s9).

**One sentence for s9:** Build the agent that has an accountable opinion and never an unaccountable action — review the change not the genome, remember every yes and no in the token contract, never lose the human's work, and let it get better at *proposing* while the wall that stops it from changing *itself* stays standing at session-scope.