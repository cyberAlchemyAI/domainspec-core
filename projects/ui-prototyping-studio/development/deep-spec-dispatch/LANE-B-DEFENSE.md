---
id: ui-prototyping-studio-lane-b-defense
feature: ui-prototyping-studio
title: "Lane B (Thesis): Defense & Deepening of the Current Design (D-001..D-009)"
summary: Ergonomics-first defense of the load-bearing decisions the challenger pressured, an ABSORB / PARTIALLY-ABSORB / REJECT verdict per Lane A direction expressed entirely in domainspec UI types, and a concrete deepening of the shallow areas (fitness, exploit conformance, rejection lifecycle, cognitive load, lead-when boundary, failure/recovery, proof schema, registry). Every kept or changed decision states who leads when, the cognitive load it imposes, and how it reduces friction. Governance is defended as a feature, not as friction. Confirms s3's central agreement with the challenger: the human reviews the change, not the genome; the agent may have an accountable opinion but never an unaccountable action.
status: draft
node_type: design
dispatch_id: ui-prototyping-studio-deep-spec-001
step_id: s3-lane-b-defender
lane: B
stance: thesis
owners:
  - web-core
updatedAt: 2026-06-15
---

# LANE-B-DEFENSE.md — Defense & Deepening (Thesis)

**Dispatch:** `ui-prototyping-studio-deep-spec-001` · **Step:** `s3-lane-b-defender` · **Owns:** this file · **Handle:** consumes `handle.antithesis`
**Reads:** `frame.evidence-baseline` (CONTEXT-PACK.md), LANE-A-NOVEL-DESIGN.md (challenger), s1 research cards.
**First principle (non-negotiable):** ergonomics — agentic tools that improve human work and form symbiotic human–agent relations. **Governance is a feature, not friction.**

## How to read this document

This is the *thesis* lane in the zig-zag. The challenger did something rare and useful: it attacked the shallow areas without attacking the spine. Almost every direction it offered is an *amplification* of two commitments the current design already holds — "`FitnessSignal` is evidence, not ranking" (D-008) and "agent proposes, human disposes via `ConfirmUIDecisionEvidence`" (D-005). My job is therefore **not** to repel the challenger. It is to (1) confirm that the spine survives every push, (2) absorb the directions that deepen the design without weakening governance, (3) reject or wall the parts that would quietly relocate accountability from the human to the agent, and (4) deepen the genuinely shallow areas so s4 inherits decisions, not hand-waves.

Radical-candid opening admission: the current design *is* shallow exactly where the challenger says it is. Pretending otherwise would be the opposite of defending it. The strongest defense of a governance-first design is to show that governance is what makes the challenger's best ideas *safe to build* — Direction 4 (preference learning) is only trustworthy because D-005/D-009 exist to wall it. That is the thesis: **the gates are not the price of the good ideas; they are the precondition for them.**

Each verdict carries the same fixed contract the challenger used, so s4 can compose the two lanes mechanically:
- **Verdict** — ABSORB / PARTIALLY ABSORB / REJECT.
- **Reasoning** — principled, type-anchored.
- **Lead-when** — who leads, who may act, what the human sees before a durable change.
- **Cognitive load** — recognition vs recall, comparison breadth, decision count.
- **Friction reduction / cost** — what manual step it removes; what it would cost to keep governance intact.

---

## Part I — Defense of the pressured decisions

The challenger pressured (directly or by implication) D-004, D-005, D-008, and D-009, and leaned on D-002/D-003/D-006 as load-bearing assumptions. I defend each on **ergonomics** grounds, not on tradition.

### D-005 — Manual governance (baseline gate + explicit apply; auto-apply forbidden). **HELD, hardened.**

This is the decision the whole challenger document orbits, and it survives intact — the challenger itself preserves it ("never auto-select," D2; "human + proof dispose," D4). So the defense is not against the challenger; it is the articulation of *why* the challenger was right to keep it.

- **Who leads when.** Human leads (disposes) at exactly two durable/irreversible boundaries: `SelectOrCommitBaseline` and `ApplyApprovedBatch`. The agent leads everything *reversible* up to those lines: generation, delta computation, draft synthesis, nomination. The gate is placed *only* on the irreversible step — which satisfies the governance-is-a-feature clause's own test ("a gate is justified only if it protects a durable/irreversible action").
- **Cognitive load.** A gate *reduces* load: it converts an open-ended "is everything OK to ship?" worry into a single bounded, recognizable decision with a visible disabled-reason (`GateState=blocked` carries the reason). The human does not have to *police* the agent continuously; they police it at two named checkpoints. That is the symbiosis — the agent runs free where mistakes are cheap, the human is sovereign where mistakes are expensive.
- **Friction reduction.** Without the gate, the human must run a continuous background audit of an autonomous agent (maximal cognitive load, maximal distrust). With the gate, trust is *structural*: the human can let the agent work because they know nothing durable can happen without their `BatchApproval`. **The gate is what makes delegation psychologically affordable.**
- **Deepening (closing Q0 at this boundary).** I make D-005 a *typed per-operation contract*, not a prose promise. See Part III, "Lead-when matrix." Auto-apply remains forbidden; the new precision is that *reversible* operations are explicitly marked agent-may-act so the gate does not accidentally creep onto drafts (which would turn governance into friction — the failure mode the clause warns against).

### D-004 — Auto-task generation is draft-only until human confirm. **HELD.**

- **Who leads when.** Agent leads synthesis (`SynthesizeMutationBatch` → `MutationBatchStatus=draft`); human leads confirmation (`ApproveMutationBatch` → `approved`). The agent never crosses `draft → applied` alone.
- **Cognitive load.** Draft-first is *recognition over authoring*: the human reviews a proposed batch (recognition) instead of writing mutation tasks from comments (recall + authoring). The challenger's Direction 2 ("ratify, don't rank") is the same ergonomic move applied to baseline selection — which is itself evidence that draft-first is the right pattern, and an argument to extend it (I absorb that below).
- **Friction reduction.** Removes the manual "translate my comments into tasks" step while keeping the accountability checkpoint. The challenger's Q10 residue (synthesis determinism) is the legitimate deepening target — I deepen it in Part III so the draft the human approves is *predictable* (same comments → same tasks), which is what makes fast-but-not-blind approval possible.

### D-008 — Model iteration as an Evolution Engine; `FitnessSignal` is evidence, not ranking. **HELD; this is the spine the challenger builds on.**

- **Defense.** Every challenger direction routes its new information through `FitnessSignal` (governance deltas in D1, nomination rationale in D2, durable nos in D3, learning substrate in D4). That is only possible *because* fitness was already modeled as typed evidence rather than a black-box score. The challenger validated D-008 by using it five times.
- **Ergonomics of "evidence not ranking."** A ranking hides its reasons and invites automation bias ("the system said B is best"). Evidence exposes its reasons and invites *informed* disposal ("B drifted on two unlocked fields and has zero axe blockers — ratify?"). Evidence-not-ranking is therefore an *anti-automation-bias* design choice, which is an ergonomics choice. The human stays the author of meaning; the agent supplies inspectable facts.
- **Where it was shallow (O-004).** "Fitness is evidence" did not answer "*how* does evidence inform selection?" The challenger's D1 + D2 answer it well, and I absorb that answer in Part III as the resolution of O-004: **no composite score, ever; fitness is a set of named, human-readable signals; selection is a human act the agent may justify but never perform.**

### D-009 — Self-improvement / rule promotion is proof-gated and deferred. **HELD; this is the wall that makes D4 buildable.**

- **Defense.** The challenger's boldest direction (D4, preference learning) explicitly stays on the reversible side of D-009 and only *specifies* the proof wall for later. That is precisely the contract D-009 exists to enforce. D-009 is not a "no"; it is a "not without proof and a human" — which is the only way an agent that modifies its own generation rules can ever be trustworthy.
- **Ergonomics.** Proof-gating is the ultimate governance-is-a-feature case: it is what lets a human *eventually choose* to delegate rule changes, with evidence, instead of waking up to a system that silently rewrote itself. The gate is the feature that makes future autonomy a *human decision* rather than a *system fait accompli*.
- **Where it was shallow (Q8).** D-009 named `ProofObligation`/`ProofStatus`/`RulePromotionRequest` but gave them no schema. I deepen the schema in Part III so the proposal-track/rule-track wall the challenger leans on is type-backed, not aspirational.

### D-002 / D-003 / D-006 — load-bearing assumptions the challenger relied on. **HELD.**

- **D-002 (HTML-first).** The challenger's "safe to retry" claim (D5) and "reproducible nomination" claim (D2) both depend on *deterministic* output. HTML-first + Style-Dictionary-pure-transform is what makes determinism real. Defended as the substrate of the challenger's own trust claims. Ergonomics: deterministic diffs are *recognizable* (the human reads the same diff format every time) and auditable.
- **D-003 (canonical comment schema).** The challenger's D5 relies on the comment stream being *append-only and never lost*. D-003's stable `{target, severity, intent, note}` contract is what makes comments durable and synthesis replayable. Held; deepened only by Q10 (the comment→task function).
- **D-006 (`variantCount` 1..3, default 3).** The challenger's D2 reframes *how* 3 variants are reviewed (champion + challengers) without changing *that* there are up to 3. I hold D-006 and absorb D2's reframing as the answer to Q6 — keeping breadth bounded while killing paralysis. One sharpening: I treat `variantCount=3` not as a fixed default but as an ergonomic *ceiling*; see Part II, Direction 2.

---

## Part II — Verdict per challenger direction

### Direction 1 — Conformance Delta as the primary review surface. **VERDICT: ABSORB (fully).**

This is the strongest direction in the challenger document and it strengthens governance rather than eroding it. It makes the human's review *cheaper and more accurate* without moving any decision from human to agent. Absorb as the resolution of Q2, and as the partial resolution of O-004 (Q1) and Q6.

- **How it lands in types.** A `DiffSummary` over two `UIVisualSignature`s is the conformance artifact (semantic extension of an existing VO — acceptable, no new entity). Each field-delta is a `FitnessSignal(source=governance, dimension=<DNA field>, preference ∈ {-1,0,1}, confidence=1.0)`. Accepting a deliberate drift is `UIDecisionRecord(UIDecisionType=change)`; locking is `constrain`; holding is `preserve`. Locked fields fold into `PrototypeGenome` as constraints on the next `GenerateVariants`. All existing types.
- **Lead-when.** Agent leads the (deterministic, judgment-free) delta computation and *proposes* which deltas look intentional. Human leads (disposes) the lock/accept per field via `ConfirmUIDecisionEvidence`. The agent may pre-select "lock all fields that were `constrain` last cycle" but cannot make a drift durable. This is a clean expression of D-005's posture at the field level.
- **Cognitive load.** Collapses `3 × 24 = 72` cells to "how many fields drifted, on which locked ones" (typically 2–5). Recognition over recall.
- **Defender-added guardrail (deepening, not objection).** Two ergonomic refinements so the delta surface does not itself become a trust trap:
  1. **Confidence must stay honest.** `confidence=1.0` is only legitimate where both signatures resolve to a *confirmed* enum/token. Where a field is `TypedReference`-pending (the s1 ROSI underfill: Motion/Interaction/State/Feedback/Numeric), the delta `FitnessSignal` must carry `confidence < 1.0` or be marked `pending`, never a fabricated 1.0. A green "held" chip on an *unresolved* field would be a false-trust signal — the worst ergonomic outcome. This keeps D1 honest under the s1 residue the challenger itself flagged.
  2. **A violation on a `constrain`-locked field is `GateState=blocked` on that candidate's selectability, with the reason surfaced** (reusing D-005's disabled-reason contract). The human is never silently prevented from selecting; they see *why*.
- **Verdict rationale.** Pure governance gain: it makes on-brand-ness recognizable, makes constraints resumable across cycles, and produces the `FitnessSignal(source=governance)` substrate D2/D4 consume — all without weakening a single gate. **Absorb as the centerpiece of the deepened exploit-mode design.**

### Direction 2 — Champion + challengers framing. **VERDICT: ABSORB (with two hard guardrails).**

Absorb, because it is the cleanest possible articulation of D-005's "agent may have an opinion, never an action," and it directly kills the documented paralysis risk (Q6). It deepens, rather than threatens, manual governance: the nomination is a *proposal carrying its reasons*, and `SelectOrCommitBaseline` stays a human act.

- **How it lands in types.** `proposedChampionLabel` is a *non-durable read-model field* (mirroring how identity/DNA suggestions are non-durable until confirmed) — explicitly **not** a `BaselineRevisionAnchor`, which only exists after a human `SelectOrCommitBaseline`. The rationale is one or more `FitnessSignal`s (`source ∈ {governance, risk, test}`, explicit `dimension`). Ratify = `SelectOrCommitBaseline` unchanged; override = same op with a different label, recorded as `UIDecisionRecord(UIDecisionType=select)` whose rationale captures the disagreement.
- **Lead-when.** Agent leads nomination + rationale assembly. Human leads (disposes) ratify-or-override. Critically: **override must be exactly as cheap as ratify** — one action, no extra confirmation, no "are you sure you want to disagree with the recommendation?" friction. If override is more expensive than ratify, the design has manufactured automation bias.
- **Cognitive load.** Drops from "rank 3 from scratch" (open-ended, recall-heavy, paralysis-prone) to "ratify or veto one pre-surfaced candidate" (recognition + one decision).
- **Defender-added guardrails (the two reasons this is ABSORB-with-conditions, not unconditional ABSORB).**
  1. **The nomination must be deterministic and must name what the champion is *worse* at.** The challenger already proposed this; I make it a *hard requirement*, not a nicety. A nomination is "fewest blocking `FitnessSignal`s," computed deterministically (same candidates + same signals → same champion). The rationale renderer MUST include at least the champion's worst dimension. A one-sided rationale is an automation-bias generator and is rejected.
  2. **The champion frame must degrade gracefully to the symmetric frame.** When `variantCount=1` (committed baseline, D-006) there is no champion to nominate; when two candidates tie on blocking signals, the system must present them as co-challengers with *no* nominated champion rather than breaking the tie arbitrarily — an arbitrary tiebreak is an unaccountable opinion. Ties surface as "no clear champion; here is why each leads," which is *more* honest, not less helpful.
- **Sharpening D-006 (ergonomic ceiling, not fixed default).** Because the champion frame makes 3-way review cheap, the paralysis argument for *reducing* the default disappears — so I hold `default=3` but reframe it as a *ceiling the agent may underfill*: in exploit mode with heavy constraints, the agent may legitimately propose 2 (champion + 1 challenger) if a third adds no decision-relevant variance. The human can still request 3. This keeps breadth bounded *and* avoids manufacturing variants that exist only to fill a slot.
- **Verdict rationale.** It is the operational answer to Q0 at the most consequential decision point, and it preserves D-005 by construction. **Absorb, conditioned on the two guardrails — without them it risks converting "human disposes" into "human rubber-stamps," which would violate the first principle.**

### Direction 3 — Rejection as durable negative evidence. **VERDICT: ABSORB (fully).**

Absorb without reservation. This is the highest-integrity direction: it makes a *human's no* as durable and load-bearing as a human's yes, which is the symmetric completion of D-005's accountability model. It resolves Q3 entirely and gives Q4 a free versioning edge.

- **How it lands in types.** `UIDecisionRecord(UIDecisionType=reject)` is the durable rejection fact (durable only via `ConfirmUIDecisionEvidence`). The *why* is typed with the existing `UIIdentityRelationType` (`replaced-by` / `removed` / `reshaped` / `merged-into` / `split-from`) — a rejection is a *relation*, not a void. The rejected suggestion folds into `PrototypeGenome` as a negative constraint; `GenerateVariants` must not regenerate a `removed` identity and must respect a `replaced-by` mapping. A `FitnessSignal(source=human, preference=-1, dimension=<element/DNA field>)` records the selection pressure.
- **Lead-when.** Human leads (disposes) every rejection. Agent leads *honoring* it — it must read negative evidence from the genome and not re-propose. The agent is *constrained by* the human's prior nos; this is the inverse-direction proof that the agent serves the human's accumulated judgment.
- **Cognitive load.** Very low per occurrence and **decreasing over a session** — the system gets quieter as taste accumulates. This is the opposite of decision fatigue and a genuine symbiosis property.
- **Defender-added guardrail (one).** A no must be **reversible by the human**, not permanent by accident. A `removed` identity the human later wants back must be recoverable via a new `UIDecisionRecord` (`UIDecisionType=change` or `select`) — the negative constraint is durable, not irreversible. Otherwise "the system gets quieter" silently becomes "the system forgot a capability and the human can't get it back," which is lock-in masquerading as learning. Durable ≠ irreversible; only `ApplyApprovedBatch` and `SelectOrCommitBaseline` are the irreversible boundaries.
- **Verdict rationale.** It completes the accountability ledger (every yes *and* every no is a typed fact), it compounds in the human's favor over time, and it costs no governance. **Absorb.**

### Direction 4 — Preference-learning loop, proof-walled. **VERDICT: PARTIALLY ABSORB (reversible half only; rule-track REJECTED-for-MVP behind D-009, specified-not-built).**

This is the direction the charter told Lane B to stress hardest (Q7), and it is where defense earns its keep. The split the challenger drew is correct *in principle* but its safety lives entirely in how rigorously the wall is typed. I absorb the reversible half and *reject building* the rule half in MVP — not because the idea is wrong, but because D-009's deferral is the only thing standing between "the agent got better at proposing" and "the agent changed itself." I keep the wall standing and specify it precisely (Q8) so a future route can un-defer it *with evidence*.

- **ABSORB — proposal-tuning (reversible).** Accumulated `FitnessSignal(source=human)` deterministically tunes the *next champion nomination* (D2) and the *generation defaults*. No model training, no weights — deterministic preference accumulation over the controlled vocabulary. This is ungated because it only affects reversible drafts, and per the governance-is-a-feature clause, a gate on a reversible draft is *friction*. The human still disposes every durable action downstream. Lead-when: agent improves reversible proposals; human disposes every durable boundary, unchanged.
- **REJECT-for-MVP / DEFER-behind-proof — rule-tuning (irreversible).** Changing a generation *rule* requires `RulePromotionRequest` + `ProofObligation` + `EvaluateProofGate → ProofStatus=pass` + human `RulePromotionStatus=promoted`. This stays `deferred` in MVP per D-009/EC5. I reject *building* it now and absorb only the obligation to *specify its schema* (Part III, Q8).
- **Defender-added guardrails — the three that make the wall load-bearing (this is the core of the defense).**
  1. **The wall is typed, not prosaic. The single test:** *does this change survive a fresh session with no accumulated signals?* If yes, it is a rule (irreversible across sessions) and is gated. If no, it is a proposal default (reversible, session-scoped) and is ungated. Session-scope is the wall. A "learned default" that silently persists across sessions and reshapes generation *is* a rule and must not sneak through the ungated door. **This is the load-bearing refinement the challenger left implicit; I make it the type test.**
  2. **Learned defaults must be visible and reversible in one action.** A "learned defaults" summary surface ("agent now defaults to `Density=comfortable` because you chose it 3×") with one-action reversal. Learning that cannot be seen or undone is indistinguishable from the agent changing its own rules — i.e., it has crossed the D-009 wall through the back door. Visibility + reversibility is what keeps it on the reversible side *by construction*.
  3. **Automation-bias floor.** Direction 2's "name what the champion is worse at" rule applies to learned nominations too — a nomination tuned by learned preference must *still* disclose its weak dimension. Otherwise learning quietly converts informed ratification into reflexive rubber-stamping, defeating the first principle.
- **Lead-when (typed, not prosaic).** Reversible → agent may act; durable/irreversible → human disposes; **rule-change → human + `ProofStatus=pass` jointly dispose.** This three-tier lead boundary is itself a deepening of Q0/Q7.
- **Verdict rationale.** The reversible half is a real, compounding ergonomic gain (fewer re-corrections per cycle) and stays inside existing gates. The rule half is exactly what D-009 was written to defer. **Partial absorb is the principled verdict: take the gain that is safe, wall the gain that is not, and specify the wall so deferral is a decision, not a dodge.**

### Direction 5 — Failure & recovery as first-class states. **VERDICT: ABSORB (fully) — and re-rank as #1 in necessity, agreeing with the challenger.**

Absorb without reservation. The challenger and defender fully agree: this is the least novel and most load-bearing direction, and it is the *precondition* for trusting D2 and D4. The deepest ergonomic harm is not a bad variant; it is losing the human's annotations or leaving them unsure whether retry is safe. A governance-first design that loses the human's work under failure is governance theater.

- **How it lands in types.** Additive named states on `StudioSessionState` and `EvolutionCycleState` (the vocabulary enumerates them as "10 states" / "12 states" — additive, no new entity): `GenerationFailed`, `SynthesisTimedOut`, `SourceStale`, `ApplyConflicted`. `GateState=blocked` carries the *reason* (generalizing the existing "approve/apply buttons expose disabled reasons" contract to every gate). A stale or conflicted apply returns the `MutationBatch` to a recoverable `MutationBatchStatus` rather than destroying it; `CommentEvent`s (append-only, D-003) are never lost. Staleness is detected against `BaselineRevisionAnchor` (which exists precisely for this) → `SourceStale` with a "re-anchor and retry" path.
- **Lead-when.** Agent leads detection and honest reporting (what failed, what is preserved, what is safe to retry). Human leads (disposes) recovery: retry / re-anchor / discard. **No failure path may auto-apply or auto-discard the human's annotations** — failure never auto-resolves into a durable change. This is D-005's posture under stress, and it is where governance proves it is a feature.
- **Cognitive load.** Designed to *remove* the worst load: anxiety + recall under failure. A named state + one-line reason + single safe action beats a cryptic error and an uncertain "did I lose my comments?".
- **Defender-added deepening (closing Q5 fully and tying to Q9).** Each failure state must specify: (a) what is *preserved* (the append-only `CommentEvent` stream, the draft `MutationBatch`); (b) what is *safe to retry* — true *because* of D-002 determinism (same genome → same output, so retry never silently produces a different design); (c) the `aria-live="polite"` announce-once contract on `SessionStateIndicator` (Q9) so failure is announced, not spammed; (d) keyboard-first recovery so governance-under-failure is not mouse-only. See Part III for the per-class table.
- **Verdict rationale.** It costs almost no new machinery (mostly specification) and it is the trust substrate every other direction stands on. **Absorb; treat as foundation-first in sequencing, exactly as the challenger ranked it.**

### Cross-cutting — "no raw values" as a named `ProofObligation`. **VERDICT: ABSORB (shape-only), with the W3C-DTCG caveat enforced.**

Absorb. Lifting "every `UIVisualSignature` field resolves to a controlled-vocab enum or a `TypedReference` into the token namespace; zero raw px/color" into a named `ProofObligation` checked by `EvaluateProofGate` gives the existing hard type rule a `ProofStatus` and a home in the Q8 schema. It is what makes D1 diffs honest, D2 rationales reproducible, and D4 preferences auditable.

- **Defender-enforced caveat (the reason it is shape-only).** Per W3C-DTCG, token group names are not semantically load-bearing. So this `ProofObligation` checks *shape* (no raw values) — which is deterministic and a legitimate hard gate — and **must never** check *meaning* (which enum is "correct"), which stays human-confirmed via `ConfirmUIDecisionEvidence`. Conflating the two would let the proof gate quietly make a *judgment* (semantic correctness) that belongs to the human — a governance regression dressed as automation. Shape is provable; meaning is disposed. **This boundary is itself a defense of D-005's posture inside the proof system.**

---

## Part III — Deepening the shallow areas (consistent with the current architecture)

These are the concrete deepenings s4 should inherit. Each is expressed in §2 types and carries lead-when / load / friction.

### Q0 — Lead-when matrix (the per-operation contract that was only implied).

The single most load-bearing deepening: turn D-004/D-005's implied posture into a typed per-operation contract over the 13 operations. Three tiers:

| Tier | Operations | Who leads | Agent may act alone? | What the human sees before durability |
| ---- | ---------- | --------- | -------------------- | ------------------------------------- |
| **Reversible (agent-may-act)** | `InitializeSession`, `SubmitPrompt`, `GenerateVariants`, `SynthesizeMutationBatch` (→draft), `RecordFitnessSignal` (governance/test/risk sources), nomination of `proposedChampionLabel`, conformance-delta computation | Agent | **Yes** — reversible, no durable effect | N/A (no durable change) |
| **Durable (human-disposes)** | `SelectOrCommitBaseline`, `ConfirmUIDecisionEvidence` (select/reject/preserve/change/constrain), `ApproveMutationBatch`, `ApplyApprovedBatch`, `ExportDesignHandoff` | Human | **No** | The proposal + its evidence + the disabled-reason if `GateState=blocked` |
| **Rule-change (human + proof dispose)** | `EvaluateProofGate`, `PromoteEvolutionRule` | Human + `ProofStatus=pass` | **No** (deferred in MVP, D-009) | The `ProofObligation` record + `RulePromotionRequest` |

Ergonomics: the human's attention is spent only at tier 2 and tier 3 — bounded, recognizable, named. Tier 1 is where the agent earns its keep. **This matrix is the canonical answer to Q0 and the typed form of the governance-is-a-feature clause.**

### Q1 / O-004 — Fitness scoring model. **Decision: no composite score; named-signal Pareto.**

Resolve O-004 against the qualitative/weighted/Pareto trichotomy: **reject the weighted composite vector outright** (it produces a single number the human distrusts and that invites automation bias — an ergonomic failure), and adopt **Pareto over a small, human-locked set of named dimensions** (the D1 + D2 model). Fitness is never shown as a score; it is shown as a set of `FitnessSignal`s, each with `source`, `dimension`, `preference ∈ {-1,0,1}`, `confidence`. The human assigns/owns `preference` and `severity` for `source=human` signals; the agent supplies deterministic `source ∈ {governance,test,risk}` signals. Selection is a human act (`SelectOrCommitBaseline`) the agent may *justify* (D2 nomination) but never *perform*. Lead-when: human owns the weights (by being the one who locks dimensions); agent owns the measurement. Load: the human reads facts, not arithmetic.

### Q2 — Exploit-mode conformance. **Decision: D1 signed field-delta over `UIVisualSignature`.** (Fully specified in Part II / Direction 1.) Conformance = count + direction of `UIVisualSignature` field deltas vs the committed baseline, each a `FitnessSignal(source=governance, confidence=1.0 only when both ends resolve to confirmed enums)`; a delta on a `constrain`-locked field is `GateState=blocked` with a surfaced reason.

### Q3 — Identity/DNA rejection lifecycle. **Decision: D3 durable negative evidence, typed by `UIIdentityRelationType`, reversible by the human.** (Fully specified in Part II / Direction 3.)

### Q4 — Component registry data model/versioning. **PARTIAL — residue with a starting edge, owner s4/s9.**

Candidly: neither lane fully specifies the registry entity. The honest defender position is to *not* over-claim. What I can land in types now: `UIElementIdentity` is the stable concept node; `UIElementInstance` is a versioned realization; the version edge between successive instances is typed by `UIIdentityRelationType` (`replaced-by` for D3 successors, `reshaped` for same-concept evolution, `same-concept` for re-use). `TypedReference` indexes instances back to identities. This gives the registry *matching and versioning semantics for free* from D3, but the persistence/indexing entity itself remains residue. **Ergonomic anchor for s4:** the agent must *reuse* known `UIElementIdentity` nodes so the human *recognizes* components rather than re-learning novel ones each run — recognition-over-recall as the registry's design goal, not just an implementation detail.

### Q5 — Error/recovery flows. **Decision: D5 named states, per-class contract.**

| Failure class | New state | Preserved | Safe-retry basis | Recovery (human disposes) |
| ------------- | --------- | --------- | ---------------- | ------------------------- |
| Generation failure | `GenerationFailed` | prompt, prior baseline | D-002 determinism: same genome → same output | retry / discard |
| Synthesis timeout | `SynthesisTimedOut` | append-only `CommentEvent` stream, draft `MutationBatch` | comments are the durable source; synthesis is replayable | retry synthesis / discard draft |
| Stale revision on apply | `SourceStale` (detected vs `BaselineRevisionAnchor`) | draft `MutationBatch`, comments | re-anchor recomputes against current baseline | re-anchor and retry / discard |
| Batch-apply conflict | `ApplyConflicted` (`MutationBatch` returns to recoverable status) | the batch, comments | deterministic re-diff | resolve / re-approve / discard |

All four: `GateState=blocked` carries the reason; `aria-live="polite"` announces the state once (Q9); recovery is keyboard-first. No path auto-applies or auto-discards annotations.

### Q6 — Cognitive load / paralysis. **Decision: D2 champion + challengers with the two guardrails; D-006 as ergonomic ceiling.** (Specified in Part II / Direction 2.) The L4 proxy for s6/s7: comparison breadth = "challengers vs champion" (≤2 pairwise), decision count = 1 (ratify/override). L6 human-study residue remains — the s8 naive-user lane is the live test.

### Q7 — Multi-cycle autonomy envelope (O-003). **Decision: three-tier envelope from the Q0 matrix; reversible autonomy yes, irreversible no, rule-change proof-gated.** (Specified in Part II / Direction 4.) The envelope is exactly the Q0 matrix's three tiers; "supervised autonomy" = agent free in tier 1, human-disposes in tier 2, human+proof in tier 3.

### Q8 — Proof storage schema (deepening D-009 so the D4 wall is type-backed). **Decision: specify, do not build.**

A `ProofObligation` records: `obligationId`; the `dimension`/claim it asserts (e.g., "no raw values in `UIVisualSignature`"); the `ProofStatus(pending|pass|flag|block)`; the evidence reference (`TypedReference` to the deterministic check output); and the `RulePromotionRequest` it binds to. A `RulePromotionRequest` records: the proposed rule change; the accumulated `FitnessSignal(source=human)` evidence motivating it; the bound `ProofObligation`(s); and the `RulePromotionStatus(deferred|rejected|promoted)`. **The session-scope test (Part II/D4 guardrail 1) is the gating predicate:** a tuning that survives a fresh, signal-less session is a rule → it *requires* a `RulePromotionRequest` + passing `ProofObligation`; a tuning that does not is a proposal default → ungated. In MVP every `RulePromotionRequest` resolves `deferred`. This makes D-009's deferral a *specified decision with a schema*, not an open hole — which is the difference between "deferred" and "unaddressed."

### Q9 — Accessibility interaction detail. **Decision: hard-gate the deterministic parts, per Q5/D5.** Tab order across the 7 panels follows reading order; focus trap + return-focus on the approval modal (the `ApplyApprovedBatch` gate); `aria-live="polite"` announces session/failure state once. These are L1 hard_gate + manual (s7 Playwright + axe). Ergonomics: the governance gates (baseline, apply) must be fully keyboard-operable — governance must not be a mouse-only privilege, or it stops being a universal feature.

### Q10 — Synthesis determinism (`CommentEvent → MutationTask`). **Decision: specify the deterministic fold; owner s4 for full function, defender lands the contract.** The mapping must be a *pure, ordered, deterministic* function: comments sort by `CommentSeverity` (blocker → high → medium → low) then by stable `AnnotationTarget` order; same comments → same ordered `MutationTask`s; dedup on identical `(target, intent)`; conflicting tasks on the same target surface as a single task with both intents noted, never silently dropped. This is what lets the human approve a draft *fast but not blind* (D-004) — predictability is the load-reducer. Full conflict algebra remains s4 residue.

---

## Part IV — Where the defender and challenger disagree (for s4)

Honest accounting of the *only* real tensions, so s4 does not have to re-derive them:

1. **Direction 4's wall location.** Challenger draws the proposal/rule wall at "reversible vs irreversible." Defender sharpens it to **session-scope as the operational test** (survives a signal-less session = rule = gated). s4 should adopt the session-scope test; it is the same wall, made checkable.
2. **Direction 2's override symmetry.** Challenger says override is "one click away." Defender hardens this to **override must cost exactly what ratify costs** and the nomination **must disclose the champion's weak dimension** — both as *hard requirements*, because without them D2 silently converts "human disposes" into "human rubber-stamps." s4 should treat these as acceptance criteria, not nice-to-haves.
3. **Direction 1's confidence honesty.** Challenger sets `confidence=1.0` for exact enum diffs. Defender requires **`confidence<1.0` or `pending` wherever a field is `TypedReference`-unresolved** (the s1 ROSI underfill), so a "held" chip is never a false-trust signal. s4 should fold this into the conformance spec.
4. **Direction 3 reversibility.** Challenger emphasizes durability. Defender adds **durable ≠ irreversible** — a human-rejected identity must be human-recoverable, or "the system gets quieter" becomes silent capability loss. s4 should make recovery a first-class path.

None of these are rejections of the spine; all four *tighten* the challenger's directions toward the first principle. The lanes converge.

---

## Part V — Net position handed to s4

- **Spine held:** D-002, D-003, D-005, D-006, D-008, D-009 all survive intact; D-001/D-007 untouched (architecture). The challenger validated the spine by building on it five times.
- **Absorbed:** Directions 1, 2 (with 2 guardrails), 3, 5, and the cross-cutting `ProofObligation` (shape-only). These resolve Q1(partial), Q2, Q3, Q5, Q6, Q9 and anchor Q0/Q7.
- **Partially absorbed:** Direction 4 — reversible proposal-tuning **in**, rule-tuning **walled and specified-not-built** behind D-009 with the session-scope test.
- **Deepened shallow areas:** Q0 (lead-when matrix), Q1/O-004 (named-signal Pareto, no composite score), Q2, Q3, Q5, Q7, Q8 (proof schema), Q9, Q10 (deterministic fold).
- **Residue passed forward (owned, not hidden):** Q4 registry entity (s4/s9), Q10 full conflict algebra (s4), Q8 proof schema is *specified* but un-built (intentional, D-009), and the entire ergonomics floor remains **L4 soft_flag / L6 human-study residue** — *no ergonomic gain in this document is asserted as proven; s8 is the live test.*

**Thesis confirmed and tightened:** *Make the human review the change, not the genome; let the agent have an accountable opinion but never an unaccountable action; remember every yes and every no in the token contract; never lose the human's work — and draw the learning wall at session-scope so the agent may get better at proposing without ever, quietly, changing itself.* Governance is the feature that makes all of this safe to build.
