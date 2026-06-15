---
id: ui-prototyping-studio-residuality-stressors
feature: ui-prototyping-studio
title: "Residuality Stress Analysis (s5): invalidations, residues, and attractors over the synthesized deep design"
summary: >
  Audit-mode residuality pass over SYNTHESIZED-DEEP-DESIGN.md (s4). Generates stressors across technical,
  social, environmental, organizational, and adversarial/misuse dimensions; for each significant stressor
  decides the desired residue (survive / degrade / stop) and converts it into concrete spec implications
  (invariant, degradation behavior, fallback, user communication, observability signal, verification idea).
  Clusters stressors into seven ATTRACTORS (vulnerability clusters) with spec implications. The s4 design is
  strong on the happy-path-to-failure transition for four named technical faults, but its survival posture
  is thin or absent for: trust-erosion under repeated agent error, determinism drift across model/token/lib
  versions, the unbounded-growth of durable negative evidence, multi-session / concurrency contention, the
  adversarial use of governance gates themselves, and operator/organizational continuity. Status FLAG: the
  spine survives, but eight stressors invalidate at least one s4 acceptance claim and require new invariants
  before one-shot implementation.
status: draft
node_type: residuality
dispatch_id: ui-prototyping-studio-deep-spec-001
step_id: s5-residuality
lane: audit
owners:
  - web-core
reads:
  - frame.evidence-baseline        # CONTEXT-PACK.md (s0)
  - handle.synthesis               # SYNTHESIZED-DEEP-DESIGN.md (s4)
updatedAt: 2026-06-15
---

# RESIDUALITY-STRESSORS.md — Residuality Stress Analysis (s5)

**Dispatch:** `ui-prototyping-studio-deep-spec-001` · **Step:** `s5-residuality` (audit mode) · **Consumes:** `handle.synthesis` (s4 deep design), `frame.evidence-baseline` (CONTEXT-PACK s0). · **Produces:** this file.

**Scope of this pass.** I stress the *deepened* design, not the spine in the abstract. The s4 design already owns a residue ledger (R-1..R-7) covering *unspecified work*. This pass covers a different axis: **stressor survival** — what happens to behavior, data, and the human-agent relation when the world pushes on the design. Where s4's residue ledger already names something, I cite it and do not double-count; where a stressor invalidates an s4 *claim* (e.g., "safe to retry", "the system gets quieter", "override costs exactly what ratify costs"), I flag the invalidation and assign a residue or a named open question.

**Normal intent (the thing that must mostly survive).** Accountable UI exploration: the agent has an *accountable opinion* and never an *unaccountable action*; the human reviews the *change* not the genome; every yes and no is remembered in the token contract; the human's work is never lost; the learning wall stands at session-scope.

**First-principle lens carried through.** Every residue below is judged against ergonomics: a stressor "survives" only if the human's *control and trust* survive it, not merely if the process does not crash. A degradation that quietly converts "human disposes" into "human rubber-stamps" is a **first-principle failure even if no exception is thrown.** This is the residuality-specific reading of the governance-is-a-feature clause.

---

## Section 0 — Method and how this differs from s4's residue ledger

| Axis | s4 Section 4 (residue ledger) | This pass (s5 residuality) |
|------|-------------------------------|----------------------------|
| Question asked | What work is unspecified / deferred? | What happens under stress, and what must remain? |
| Unit | RESIDUE / DEFER item | Stressor → desired residue → spec implication |
| Failure it guards | Hidden scope, silent over-claiming | Silent capability loss, trust erosion, determinism drift, lock-in, gate abuse |
| Output | Owned residue + un-defer gate | Invariant / degradation / fallback / comms / observability / verification + attractor |

**Stressor severity scale** (reusing the validator severity vocabulary from CONTEXT-PACK §3): `block | high | medium | low | info`.

**Desired-residue verbs.** `SURVIVE` (must remain fully correct), `DEGRADE` (may reduce capability in a bounded, communicated way), `STOP` (may cease, but safely and visibly). A residue is incomplete unless it says which.

I do **not** claim this stressor map is exhaustive. Unknown-stress areas are marked `UNKNOWN-STRESS` and converted to open questions rather than false coverage.

---

## Section 1 — Stressor catalogue (by dimension)

Each stressor carries: ID, dimension, severity, the s4 claim it pressures, the desired residue (verb + content), and the attractor it clusters into (Section 2). "INVALIDATES" means it breaks a stated s4 acceptance criterion or claim; "GAP" means s4 is silent; "PARTIAL" means s4 covers part of it.

### 1.1 Technical stressors

| ID | Stressor | Sev | s4 claim pressured | Status | Desired residue |
|----|----------|-----|--------------------|--------|-----------------|
| **T1** | **Non-determinism drift.** The LLM/codegen backend, the resonant-os token set, or shadcn/Radix/Tailwind versions change between two runs of the "same" genome. D-002's "same genome → same output" is the load-bearing basis for *every* "safe to retry" claim (D5) and for the deterministic champion nomination (D-S1). | block | D-002 determinism; D5 "safe to retry"; D-S1 "same candidates + same signals → same champion"; Q10 "same comments → same tasks" | **INVALIDATES** | **SURVIVE**: retry must never *silently* produce a different design. If the backend/token/lib fingerprint differs from the one a draft was generated under, the system must DEGRADE: surface a `DeterminismDrift` condition, do **not** present the new output as a safe retry. The genome must record a **provenance fingerprint** (model id, token-set version, lib lockfile hash) so equality is checkable, not assumed. |
| **T2** | **Generation/synthesis backend hard-down or quota-exhausted** (not just slow). D5 covers `GenerationFailed`/`SynthesisTimedOut` as *transient retryable*, but not a sustained outage where retry is futile. | high | D5 recovery contract (retry/discard) | **PARTIAL** | **DEGRADE to read-only**: prior baseline, comments, drafts, revision history remain fully readable and exportable; new generation STOPs with an honest "backend unavailable, your work is safe and exportable" state. Retry must be rate-aware (no retry-storm against a downed backend). |
| **T3** | **Partial / truncated generation** — backend returns malformed or incomplete HTML/DNA (a `UIVisualSignature` with raw px slips through, or a variant with no resolvable identity). The shape-only `ProofObligation` (D-XC) is the only structural guard. | high | D-XC shape gate; "no raw values" invariant | **PARTIAL** | **SURVIVE (data integrity)**: a candidate that fails the shape gate must never become selectable and never fold into `PrototypeGenome`. DEGRADE: it is shown as `GenerationDegraded` with the failing fields named, not silently dropped (silent drop hides that the agent produced garbage). |
| **T4** | **Durable-store write failure during a tier-2 disposal** — the human clicks approve/commit/confirm and the persistence write fails after the UI optimistically advanced. Risks the worst outcome: human *believes* they disposed, but no `UIDecisionRecord`/`BatchApproval` persisted. | block | Tier-2 "human disposes"; "never lose the human's work"; append-only `CommentEvent` | **GAP** | **SURVIVE (the human's intent)**: a disposal is not "done" in the UI until durably written; on write failure the action returns to a re-tryable pending state with the human's intent preserved, never a false success. No tier-2 action may be reported complete on an unconfirmed write. |
| **T5** | **Append-only comment stream grows unbounded** within a long session; synthesis fold (Q10) is O(N) over comments each cycle and the dedup/conflict pass degrades. | medium | Q10 deterministic fold; "approve fast but not blind" | **GAP** | **DEGRADE gracefully**: fold remains *correct* but may surface a "large annotation set" soft signal; never silently truncate comments (truncation = lost human work). Bound is on *presentation* (paginate the `DiffSummary`), not on *retention*. |
| **T6** | **Two cycles / two tabs mutate the same baseline concurrently** (the human opens the studio twice, or an autonomous tier-1 tuning runs while the human edits). `SourceStale`/`ApplyConflicted` cover apply-time staleness, but not concurrent durable disposals racing. | high | D5 `SourceStale`/`ApplyConflicted` (apply-time only); tier-2 disposal atomicity | **PARTIAL** | **SURVIVE (no lost disposal)**: durable disposals serialize against the `BaselineRevisionAnchor` they were made against; a second disposal on a now-advanced anchor surfaces `SourceStale` *before* commit, not after silent overwrite. Last-write-wins on durable governance is a first-principle failure. |
| **T7** | **`PrototypeGenome` negative-constraint set grows monotonically** across a long session (every `reject` adds a negative constraint `GenerateVariants` must honor). Eventually the constraint set over-constrains generation: the agent can produce nothing that satisfies all accumulated nos. | medium | D3 "a no is remembered, never re-fought"; D-S3 reversibility | **GAP** | **DEGRADE visibly**: when the negative-constraint set makes generation infeasible, the agent must STOP and *report the conflict* ("3 of your prior rejections together leave no valid variant — relax which?"), exposing the offending constraints for the human to reverse (D-S3 makes them reversible). Never silently ignore a remembered no to make room (that re-fights the no invisibly). |

### 1.2 Social / user stressors

| ID | Stressor | Sev | s4 claim pressured | Status | Desired residue |
|----|----------|-----|--------------------|--------|-----------------|
| **S1** | **Trust erosion under repeated agent error.** The agent nominates a champion (D2) or computes a conformance delta (D1) and is *wrong* (worst-dimension disclosure is technically honest but the pick is bad) several times. The human stops reading rationales and starts blind-overriding or blind-ratifying. This is automation bias's mirror: *automation distrust*. | high | D-S1 "kills decision-paralysis without manufacturing automation bias"; the whole "accountable opinion" value | **GAP** | **SURVIVE (informed disposal)**: the design must make agent fallibility *legible and recoverable*, not just disclosed once. Residue: an observable signal of nomination accuracy over a session (how often the human overrode), surfaced so the human can *calibrate trust* rather than swing to a blind extreme. **Open question OQ-1**: is there a session-level "agent has been overridden N/M times" trust meter, and does showing it help or harm? (L6 human-study residue.) |
| **S2** | **Rubber-stamping via fatigue, not via cost asymmetry.** D-S1 ensures override *costs* the same as ratify, but says nothing about *attention*. A tired human ratifies a batch of drafts without reading. The gate is satisfied; accountability is hollow. | high | D-004 "recognition over authoring"; governance-is-a-feature; tier-2 "what the human sees before durability" | **GAP** | **DEGRADE → friction-on-demand**: for *irreversible* tier-2 actions (`ApplyApprovedBatch`, `SelectOrCommitBaseline`) the design may require the human to have *seen* the `DiffSummary` (e.g., the apply button is `GateState=blocked` with reason "review the diff first" until the diff panel was opened/scrolled). This is the one place added friction is pro-ergonomic (it protects the irreversible). Reversible tier-1/draft actions stay frictionless. **Open question OQ-2**: what is the minimal "you have actually seen this" proxy that is not theater? |
| **S3** | **The human disagrees with a *shape* gate.** D-XC's `ProofObligation` hard-blocks raw px/color. A power user legitimately needs a one-off raw value the controlled vocab cannot express. The hard gate becomes a wall the human cannot get past — governance as friction, the exact anti-pattern the charter forbids. | medium | D-XC shape-only hard gate; charter clause 4 ("gates only on irreversible/durable; never friction on reversible") | **INVALIDATES** | **DEGRADE with an accountable escape**: the shape gate is correct as a default, but a hard gate on a *reversible draft* violates the charter. Residue: shape violations should `GateState=blocked` *selectability/apply* (durable) but allow the human to **explicitly accept a documented exception** (`UIDecisionType=constrain` with an exception note), converting a wall into an accountable override. Never a silent bypass; never an un-overridable wall on a draft. |
| **S4** | **Operator error on a destructive recovery action.** Under a D5 failure state, the recovery options include "discard draft". A stressed human discards comments/draft they meant to keep. | medium | D5 "never lose the human's work" | **PARTIAL** | **DEGRADE → recoverable discard**: "discard" under any failure state must be *soft* (recoverable for the session) since the underlying `CommentEvent` stream is append-only anyway. The destructive boundary is only `ApplyApprovedBatch`/`SelectOrCommitBaseline`. Communicate: "discarded draft can be re-synthesized from your comments" (true because comments are the durable source). |

### 1.3 Environmental stressors

| ID | Stressor | Sev | s4 claim pressured | Status | Desired residue |
|----|----------|-----|--------------------|--------|-----------------|
| **E1** | **Token-set / design-system upstream change** (resonant-os-design-tokens evolves; an enum value is renamed or removed). Already half-named in R-7 (ROSI underfill) but R-7 is about *incompleteness*, not *change after binding*. A committed baseline references a `TypedReference` that no longer resolves. | high | D-S2 confidence honesty; D1 conformance delta; "constraints resumable across cycles" | **PARTIAL (R-7 adjacent)** | **SURVIVE (no false green)**: a `TypedReference` that no longer resolves must force `confidence<1.0`/`pending` (D-S2 already forbids false 1.0) and surface the broken binding, never render a stale value as "held". DEGRADE: conformance on the affected field becomes `pending`, not `held`, until re-bound. Verification: a fixture where a token is removed must turn the chip pending, not green. |
| **E2** | **W3C-DTCG semantic drift.** R-4 already keeps *meaning* human-confirmed, but environmental drift can change which token group a name *implies* over time, silently shifting what a previously-confirmed enum means. | low | D-XC / R-4 "shape not meaning"; ConfirmUIDecisionEvidence durability | **PARTIAL (R-4 covers it)** | **SURVIVE**: a human-confirmed `UIDecisionRecord` is durable evidence of *the human's* meaning at confirm-time; environmental re-interpretation must not silently re-confirm. Covered by R-4; flagged here so s5 does not double-own. No new residue. |
| **E3** | **Regulatory / a11y standard change** (axe ruleset updates; WCAG target-size threshold changes). Q9 hard-gates against today's axe. | low | Q9 L1 hard_gate | **GAP (low)** | **DEGRADE**: an axe ruleset bump may newly-fail a previously-passing baseline; this must surface as a *new* `FitnessSignal(source=risk)`, not retroactively invalidate committed history. Communicate as "new standard flags this existing baseline", not silent failure. |

### 1.4 Organizational stressors

| ID | Stressor | Sev | s4 claim pressured | Status | Desired residue |
|----|----------|-----|--------------------|--------|-----------------|
| **O1** | **Session handoff between humans.** Designer A builds taste into a session (rejections, locks, tuned defaults D4-prop); Designer B resumes. B inherits A's accumulated `FitnessSignal(source=human)` and negative constraints without knowing *why*. The "agent meets the human where they already are" (D4-prop) now means the agent meets *the wrong human*. | high | D4-prop "visible + reversible in one action"; recognition-over-recall | **GAP** | **SURVIVE (provenance) + DEGRADE (inheritance)**: accumulated session signals must carry *whose* taste they encode and be visible/reversible by the new operator. D4-prop already requires "agent now defaults to X because you chose it 3×" — extend to "*A* chose it 3×". Open question OQ-3: on operator change, does session-scoped tuning carry, reset, or prompt? (Interacts with D-S4 session-scope wall — see attractor A6.) |
| **O2** | **Deferred rule-track never un-defers** (D-009 / R-3). Organizationally, "specified not built" can become "permanently shelved"; accumulated `RulePromotionRequest=deferred` records pile up as dead evidence nobody acts on. | low | D4-rule / R-3 "principled middle"; D-S4 wall | **PARTIAL (R-3 owns build)** | **DEGRADE (no harm from non-promotion)**: the deferred state must remain *inert and harmless* indefinitely — deferred requests must never accumulate into pressure or implicit behavior change. Invariant: a `RulePromotionRequest=deferred` has **zero runtime effect** on generation. Verification: a session with 100 deferred requests behaves identically to one with zero. |
| **O3** | **Loss of the human operator mid-cycle** (organizational continuity: the only person who understands a session leaves). Append-only history + revision manifest exist, but is the session *self-explaining* to a successor? | medium | Handoff Summary panel; `ExportDesignHandoff`; revision manifest | **PARTIAL** | **SURVIVE (auditability)**: the revision manifest + comment stream + decision records must reconstruct *what was decided and why* without the original operator. `ExportDesignHandoff` is the residue carrier. Verification: a fresh reviewer can replay the session's decisions from artifacts alone (this is also the s8 naive-user lane's adjacent test). |

### 1.5 Adversarial / misuse stressors

| ID | Stressor | Sev | s4 claim pressured | Status | Desired residue |
|----|----------|-----|--------------------|--------|-----------------|
| **X1** | **Prompt-injection via the brief or comments.** The human's prompt or a `CommentEvent.note` contains text that attempts to steer the agent to bypass a gate ("ignore the baseline lock", "auto-approve this batch"). | high | D-005 auto-apply forbidden; tier boundary; D-XC | **GAP** | **SURVIVE (gate integrity is structural, not promptable)**: the tier-2/tier-3 gates are enforced by *type and operation contract*, not by agent compliance — no prompt content can cause the agent to perform a `SelectOrCommitBaseline`/`ApplyApprovedBatch`/`PromoteEvolutionRule` because those are not agent-callable in tiers 2/3 by construction. This must be an **invariant verified by test**, not an assumed property. Comment/prompt text is *data*, never *instruction* to the governance layer. |
| **X2** | **Gate-as-griefing / denial via constrain-lock.** A user (or a malformed import) `constrain`-locks every DNA field, making `GateState=blocked` on every candidate's selectability — the studio becomes unusable, governance turned into a self-inflicted DoS. | medium | D1 constrain-lock blocking; charter "governance not friction" | **GAP** | **DEGRADE → always an exit**: when all candidates are blocked by locks, the human must always be able to *see the blocking locks and release them* (the disabled-reason contract already surfaces *why*; extend to *unlock from here*). Invariant: there is no state from which the human cannot reach an unblocking action. |
| **X3** | **Poisoning the genome via crafted rejections.** Accumulated negative evidence (D3) and tuned defaults (D4-prop) deterministically shape future generation. A malicious or careless sequence of rejects can steer the agent into a corner (overlaps T7 but adversarially intended). | low | D3 genome fold; D4-prop tuning | **PARTIAL (T7 + D-S3)** | **DEGRADE (reversible by design)**: because D-S3 makes every reject reversible and D4-prop reversible in one action, poisoning is *recoverable*, not permanent — the wall (D-S4) prevents it from ever becoming a *rule*. Residue is the same as T7 (infeasibility reporting); the adversarial framing adds: tuning/genome state must be *resettable to neutral* in one action. |
| **X4** | **Fabricated provenance / replay confusion.** An exported handoff or revision manifest is edited outside the system and re-imported, or a `BaselineRevisionAnchor` is forged to make a stale candidate look current. | low | `ExportDesignHandoff`; `BaselineRevisionAnchor` staleness oracle (T6/Q5) | **GAP (low)** | **SURVIVE (integrity check)**: re-imported/anchored artifacts must be validated against the durable store; an anchor that does not match a real revision is rejected, not trusted. Out-of-band edits are out of MVP scope but flagged so the staleness oracle is not assumed tamper-proof. **Open question OQ-4**: is import-integrity in MVP scope or deferred? |

---

## Section 2 — Attractors (vulnerability clusters)

Stressors are not anecdotes; they cluster around a small number of vulnerability centers. Each attractor names the cluster, the stressors that fall into it, the single underlying weakness, and the spec implication that addresses the *cluster*, not the instances.

### A1 — The Determinism Assumption (the load-bearing crack)
**Stressors:** T1, T2 (partial), E1, X4. **Underlying weakness:** Every trust-bearing claim in s4 — "safe to retry" (D5), "same candidates → same champion" (D-S1), "same comments → same tasks" (Q10), "constraints resumable" (D1) — rests on D-002 determinism, but determinism is *asserted, never fingerprinted*. The moment the model, token set, or lib versions move, the assumption silently breaks and every dependent claim becomes a quiet lie. **This is the highest-leverage attractor: it sits under more s4 claims than any other.**
**Spec implication:** introduce a **provenance fingerprint** on `PrototypeGenome` / `BaselineRevisionAnchor` (model id + token-set version + lockfile hash). "Safe to retry" becomes a *checkable* claim (fingerprint match), not an assumed one. Determinism mismatch is a first-class condition (`DeterminismDrift`), not an invisible divergence.

### A2 — Trust Calibration (the human-side mirror of determinism)
**Stressors:** S1, S2. **Underlying weakness:** s4 hardens against *automation bias* (D-S1 worst-dimension disclosure, override symmetry) but is silent on the two opposite failures: *automation distrust* (blind override after the agent is wrong) and *fatigue rubber-stamping* (attention, not cost, collapses). Both hollow out "accountable disposal" while every gate still reports satisfied. **The gate can be structurally perfect and ergonomically empty.**
**Spec implication:** make agent fallibility and human attention *observable*. A session-level override/accuracy signal (calibrates trust); a "seen the diff" proxy as the only sanctioned friction on irreversible tier-2 actions. Both carry L6 human-study residue — flagged, not asserted.

### A3 — Unbounded Durable State (the accumulation attractor)
**Stressors:** T5, T7, O2, X3. **Underlying weakness:** Three append-only / monotonic stores grow without a specified bound or feasibility check: the comment stream (T5), the genome's negative-constraint set (T7/X3), and the deferred `RulePromotionRequest` pile (O2). "Remember every no" (D3) and "specified not built" (D-009) are correct *until accumulation makes generation infeasible or makes deferred state non-inert*.
**Spec implication:** every monotonic store needs a specified behavior at scale: comments paginate but never truncate; the negative-constraint set must detect and *report* infeasibility (exposing reversible constraints) rather than silently dropping a remembered no; deferred rule requests must be provably zero-effect at runtime (verified by a 100-deferred-vs-0 equivalence test).

### A4 — Concurrency & Disposal Atomicity (the race attractor)
**Stressors:** T4, T6. **Underlying weakness:** s4's failure model is *sequential and apply-time* (`SourceStale`/`ApplyConflicted` fire at apply). It has no model for (a) a durable write failing mid-disposal, or (b) two durable disposals racing on the same baseline. Both can produce the worst outcome the whole design exists to prevent: a *lost or phantom human disposal*.
**Spec implication:** a tier-2 disposal is atomic and anchor-checked — not "done" until durably written, and serialized against the `BaselineRevisionAnchor` it was made against. `SourceStale` must fire *before* a durable overwrite, not only at apply. No last-write-wins on governance.

### A5 — Governance Surface as Attack/Failure Vector (the gate-abuse attractor)
**Stressors:** X1, X2, S3. **Underlying weakness:** s4 treats the gates as the *solution*; this attractor treats them as a *surface*. Gates can be (a) bypassed via prompt-injection if enforcement is agent-compliance rather than type-structural (X1), (b) weaponized into a self-DoS via universal constrain-locks (X2), or (c) turned into an un-overridable wall on a reversible draft (S3) — the precise charter anti-pattern. **A gate that cannot be escaped accountably, or that can be bypassed by data, is not governance.**
**Spec implication:** gate enforcement is *structural* (tiers 2/3 operations are not agent-callable — prompt/comment text is data, never instruction — verified by test); every blocked state has a reachable accountable exit (unlock-from-here, documented-exception override on drafts); the shape gate blocks *durable* selectability but never walls a reversible draft.

### A6 — Identity & Taste Provenance (the "whose taste is this" attractor)
**Stressors:** O1, O3, E1/E2 (binding provenance). **Underlying weakness:** Accumulated session state (rejections, locks, tuned defaults) and token bindings encode *a specific human's taste at a specific time*, but s4 stores them as anonymous session facts. On operator handoff or token drift, the agent confidently applies the wrong person's / wrong era's preferences — recognition-over-recall inverts into recognize-someone-else's-choices. This is the social/organizational shadow of the D-S4 session-scope wall: the wall says taste is session-scoped, but does not say *whose* session.
**Spec implication:** session-scoped signals carry operator + timestamp provenance and are visible/reversible by a successor; on operator change, session tuning carries-with-attribution or prompts (OQ-3); `ExportDesignHandoff` must make a session self-explaining without its author.

### A7 — Sustained Unavailability vs Transient Failure (the degradation-mode attractor)
**Stressors:** T2, T3, E3. **Underlying weakness:** D5's four failure states model *transient, retryable* faults and assume retry/discard resolves them. They have no *degraded read-only mode* for sustained backend loss, no *quarantine* for malformed-but-not-crashed output, and no model for *standards moving under committed history*. The design fails open to "retry" even when retry is futile or harmful.
**Spec implication:** a `StudioReadOnly` degradation (prior work fully readable/exportable, generation stopped honestly) for sustained outage; a `GenerationDegraded` quarantine for shape-failing output (named, never silently dropped, never selectable); new risk signals (not retroactive invalidation) when standards move.

---

## Section 3 — Spec implications (residue → concrete spec material)

Per the quality bar, every residue becomes at least one concrete, *observable* spec implication. Grouped by attractor. "Inv" = invariant, "Deg" = degradation behavior, "Fb" = fallback, "Comms" = user communication, "Obs" = observability signal, "Ver" = verification idea.

### From A1 — Determinism
- **Inv-1:** `PrototypeGenome` and `BaselineRevisionAnchor` carry a `provenanceFingerprint = {modelId, tokenSetVersion, libLockfileHash}`. No output is presented as a "safe retry" of a prior genome unless the fingerprint matches. *(Touches: `PrototypeGenome`, `BaselineRevisionAnchor`, `BaselineProvenance`.)*
- **Deg-1:** fingerprint mismatch → new state `DeterminismDrift` (additive on `StudioSessionState`); the new output is offered as a *fresh* generation, never as a retry of the old.
- **Comms-1:** "The generation backend/tokens changed since this draft; re-running may differ. Treat as new, not retry."
- **Obs-1:** signal `determinism_drift_detected{from_fingerprint, to_fingerprint}`.
- **Ver-1:** fixture — pin a genome, change the model id, assert the system refuses the "safe retry" label and emits `DeterminismDrift`.

### From A2 — Trust calibration
- **Obs-2:** per-session `nomination_override_rate = overrides / nominations` and `apply_without_diff_open_count` (the rubber-stamp proxy).
- **Deg-2:** for `ApplyApprovedBatch` and `SelectOrCommitBaseline` only, `GateState=blocked` with reason "review the diff first" until the `DiffSummary` was opened. (The single sanctioned friction — protects the irreversible; reversible drafts untouched.)
- **Comms-2:** optional trust meter "you overrode the agent's pick N of M times this session" (gated behind OQ-1; do not ship unvalidated).
- **Ver-2:** L4 soft_flag proxy (diff-opened-before-apply) is Playwright-observable; the trust-meter's *effect* is L6 human-study residue → s8.

### From A3 — Unbounded durable state
- **Inv-2:** `CommentEvent` retention is never truncated; only presentation paginates.
- **Inv-3:** a `RulePromotionRequest=deferred` has provably zero runtime effect on generation.
- **Deg-3:** when accumulated negative constraints make `GenerateVariants` infeasible, the agent STOPs and emits `GenerationInfeasible` listing the conflicting (reversible) constraints; never silently relaxes a remembered no.
- **Comms-3:** "Your rejections of X, Y, Z together leave no valid variant — relax which?"
- **Obs-3:** `negative_constraint_count`, `comment_stream_size`, `deferred_request_count`.
- **Ver-3:** equivalence test — a session with 100 deferred `RulePromotionRequest`s generates identically to a session with 0 (proves inertness). Infeasibility test — N mutually exclusive rejects produce `GenerationInfeasible`, not a silently constraint-violating variant.

### From A4 — Concurrency & disposal atomicity
- **Inv-4:** no tier-2 operation reports complete until its `UIDecisionRecord` / `BatchApproval` is durably written; on write failure it returns to a re-tryable pending state with intent preserved.
- **Inv-5:** durable disposals are serialized and anchor-checked; a disposal against a stale `BaselineRevisionAnchor` raises `SourceStale` *before* commit, never overwrites silently.
- **Deg-4:** concurrent second session/tab → the later durable disposal is rejected with a re-anchor prompt (reuses D5 `SourceStale` recovery).
- **Obs-4:** `disposal_write_failure`, `concurrent_anchor_conflict`.
- **Ver-4:** inject a write failure on approve → assert no false-success and intent preserved. Two-tab test → assert the second commit re-anchors rather than overwrites.

### From A5 — Governance surface
- **Inv-6:** tier-2/tier-3 operations (`SelectOrCommitBaseline`, `ApplyApprovedBatch`, `PromoteEvolutionRule`, `Approve…`) are **not agent-callable**; prompt and `CommentEvent.note` text are data, never governance instructions. (Structural restatement of D-005/D-S0 as an adversarial invariant.)
- **Inv-7:** there is no UI state from which the human cannot reach an unblocking action; every `GateState=blocked` surfaces both the reason *and* the path to release.
- **Deg-5:** shape-gate (D-XC) violation blocks *durable selectability/apply* but, on a reversible draft, allows an explicit `UIDecisionType=constrain` documented-exception override (accountable, never silent).
- **Comms-4:** disabled-reason already mandated by D-005; extend copy to include "release this lock" / "accept as documented exception".
- **Obs-5:** `gate_bypass_attempt_in_text` (matched injection patterns), `all_candidates_blocked_state_entered`.
- **Ver-5:** prompt-injection corpus test — comment/prompt text attempting "auto-approve"/"ignore lock" must have zero effect on gate state (the operations simply cannot be invoked by the agent). Universal-lock test — assert an unblock path remains reachable.

### From A6 — Identity & taste provenance
- **Inv-8:** every session-scoped `FitnessSignal(source=human)`, lock, and tuned default carries `operatorRef` + timestamp; D4-prop's visibility copy includes *whose* choice it reflects.
- **Deg-6:** on operator change, session tuning either carries-with-attribution or prompts to reset (OQ-3 decides which); never silently applies absent operator's taste as current.
- **Comms-5:** "Agent defaults to Density=comfortable because **A** chose it 3× on 2026-06-15. Keep / reset?"
- **Obs-6:** `session_operator_changed`, `inherited_signal_count`.
- **Ver-6:** handoff test — a successor reviewer can replay all decisions and see attribution from artifacts alone (overlaps s8/O3).

### From A7 — Degradation modes
- **Deg-7:** sustained backend loss → `StudioReadOnly` (read/export all prior work; generation stopped honestly; retry rate-limited).
- **Deg-8:** shape-failing generation → `GenerationDegraded` quarantine: named failing fields, never selectable, never folded into genome, never silently dropped.
- **Deg-9:** axe/standard bump → new `FitnessSignal(source=risk)` on existing baselines, not retroactive invalidation of committed history.
- **Comms-6:** "Backend unavailable — your work is safe and exportable." / "This baseline now flags a new accessibility rule."
- **Obs-7:** `backend_unavailable_duration`, `generation_quarantined_count`, `standard_bump_new_flags`.
- **Ver-7:** kill the backend → assert read-only, exportable, no retry-storm. Feed malformed DNA → assert quarantine, not selectability.

---

## Section 4 — Stressor → residue traceability matrix

Every significant stressor maps to a residue (with verb) or a named open question. No stressor is left as an anecdote.

| Stressor | Verb | Residue / spec implication | Open question | Attractor |
|----------|------|----------------------------|---------------|-----------|
| T1 determinism drift | SURVIVE | Inv-1, Deg-1, Ver-1 (provenance fingerprint) | — | A1 |
| T2 backend hard-down | DEGRADE | Deg-7 (read-only), Obs-7 | — | A7 |
| T3 malformed generation | SURVIVE/DEGRADE | Deg-8 (quarantine), Ver-7 | — | A7 |
| T4 disposal write failure | SURVIVE | Inv-4, Ver-4 | — | A4 |
| T5 unbounded comments | DEGRADE | Inv-2, Deg (paginate) | — | A3 |
| T6 concurrent disposals | SURVIVE | Inv-5, Deg-4, Ver-4 | — | A4 |
| T7 over-constrained genome | DEGRADE | Inv-3-adjacent, Deg-3, Ver-3 | — | A3 |
| S1 trust erosion | SURVIVE | Obs-2, Comms-2 | **OQ-1** (trust meter help/harm?) | A2 |
| S2 fatigue rubber-stamp | DEGRADE | Deg-2 (seen-diff proxy) | **OQ-2** (minimal non-theater proxy?) | A2 |
| S3 shape-gate disagreement | DEGRADE | Deg-5 (documented exception) | — | A5 |
| S4 destructive recovery error | DEGRADE | Deg (soft discard, re-synth from comments) | — | A7/A3 |
| E1 token-set change | SURVIVE | Inv-1-adjacent, D-S2 pending; ties R-7 | — | A1/A6 |
| E2 DTCG semantic drift | SURVIVE | covered by R-4 (no new residue) | — | A6 |
| E3 standard bump | DEGRADE | Deg-9 (new risk signal) | — | A7 |
| O1 operator handoff | SURVIVE/DEGRADE | Inv-8, Deg-6, Comms-5 | **OQ-3** (carry/reset/prompt on operator change?) | A6 |
| O2 dead deferred pile | DEGRADE | Inv-3, Ver-3 (zero-effect) | — | A3 |
| O3 operator loss | SURVIVE | Ver-6 (self-explaining handoff) | — | A6 |
| X1 prompt injection | SURVIVE | Inv-6, Ver-5 (structural enforcement) | — | A5 |
| X2 gate-as-DoS | DEGRADE | Inv-7, Ver-5 (reachable exit) | — | A5 |
| X3 genome poisoning | DEGRADE | Deg-3 + one-action reset (D-S3) | — | A3/A5 |
| X4 forged provenance | SURVIVE | Ver (anchor integrity check) | **OQ-4** (import-integrity in MVP?) | A1/A5 |

---

## Section 5 — Open questions (named, owned, not silently absorbed)

| ID | Question | Why it cannot be decided here | Suggested owner / route |
|----|----------|-------------------------------|-------------------------|
| **OQ-1** | Does a session-level "agent overridden N/M times" trust meter *help* calibrate trust or *harm* by inducing distrust/over-trust? | L6 human-study claim; no user data exists (CONTEXT-PACK evidence-floor clause). | s8 naive-user lane / `decision-gate` if it blocks build. |
| **OQ-2** | What is the minimal "the human actually saw the diff" proxy for irreversible applies that is not accountability theater? | Ergonomic + L4/L6; the proxy must be observable yet not friction. | s6/s7 validator (L4 proxy) + s8 (L6). |
| **OQ-3** | On operator handoff, does session-scoped tuning carry-with-attribution, reset, or prompt? | Interacts with D-S4 session-scope wall and the first-principle (whose taste); a real product/UX decision. | `decision-gate` → s9. |
| **OQ-4** | Is artifact import-integrity (re-imported handoff / forged anchor) in MVP scope or deferred? | Adversarial scope decision; X4 is low-severity but the staleness oracle is assumed tamper-proof without it. | s9 scope decision. |

---

## Section 6 — Net position handed forward

**Spine survives.** No stressor invalidates D-001..D-009 or the four convergence refinements (D-S1..D-S4). The "accountable opinion, never unaccountable action" core holds — in fact several stressors (X1, X3) are *survivable precisely because* of the spine (structural gates, reversible nos, the session-scope wall).

**Eight invalidations / gaps require new spec material before one-shot implementation** (this is why status is FLAG, not pass):
1. **Determinism is asserted, not fingerprinted (A1/T1)** — undercuts every "safe to retry" claim. Highest leverage. Needs Inv-1.
2. **No degraded read-only mode for sustained outage (A7/T2)** — D5 fails open to futile retry.
3. **Disposal atomicity & concurrency are unmodeled (A4/T4,T6)** — risks the exact lost/phantom disposal the design exists to prevent.
4. **Trust calibration is one-directional (A2/S1,S2)** — hardened against bias, blind to distrust and fatigue.
5. **Monotonic stores have no scale behavior (A3/T5,T7,O2)** — "remember every no" can make generation infeasible; deferred pile must be provably inert.
6. **Gate enforcement must be structural, not compliance (A5/X1)** — must be an invariant verified by test, not an assumed property.
7. **Shape gate can wall a reversible draft (A5/S3)** — a charter anti-pattern; needs the documented-exception escape.
8. **Session state has no operator provenance (A6/O1,O3)** — recognition-over-recall inverts on handoff.

**Four open questions** (OQ-1..OQ-4) are named with owners; none are silently absorbed.

**One sentence for s6/s7/s9:** The synthesized design is correct on the happy-path-to-named-failure transition, but its trust- and survival-claims rest on three unguarded assumptions — that generation is deterministic across versions, that disposals are atomic and single-writer, and that an unfatigued human reads before disposing — and on three unbounded stores; fingerprint the determinism, atomicize the disposal, make attention and provenance observable, and bound the stores, and the design survives stress without ever converting "human disposes" into "human rubber-stamps."