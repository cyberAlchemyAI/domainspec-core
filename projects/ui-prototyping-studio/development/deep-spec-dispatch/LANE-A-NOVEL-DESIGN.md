# LANE-A-NOVEL-DESIGN.md — Novel & Better Directions (Antithesis)

Full artifact written to: projects/ui-prototyping-studio/development/deep-spec-dispatch/LANE-A-NOVEL-DESIGN.md

Five directions, each expressed entirely in domainspec UI types, each carrying: idea, types changed/added, shallow areas resolved (by Q-id), resonant-token philosophy leveraged, who-leads-when, cognitive load, friction reduction, implementation cost, Pareto rank.

## Direction 1 — Conformance Delta as the primary review surface
Review the field-level diff between a candidate's UIVisualSignature and the committed baseline's, not 24 enums. Each delta is a FitnessSignal(source=governance, dimension=<DNA field>, confidence=1.0, preference -1|0|1); reuses DiffSummary; locks/accepts via UIDecisionRecord(constrain/change/preserve). Resolves Q2 (exploit conformance metric) directly, plus Q1/Q6. Leverages "token layer is the contract, no raw values" — exact enum diffs only because raw px/color are forbidden; neutralizes ROSI's no-alias problem by diffing the domainspec Tier-2 role layer. Agent computes delta, human locks fields. Load collapses 72 cells to 2-5 changed fields. Cost low-to-medium (Style Dictionary pure transform). **Pareto #1 — dominant.**

## Direction 2 — Champion + challengers framing
Agent nominates one proposed champion with evidence-linked rationale (FitnessSignals from axe + D1 deltas), human ratifies or overrides — never auto-select (D-005 preserved). proposedChampionLabel is a non-durable read-model field, not a BaselineRevisionAnchor. Resolves Q6 (paralysis) directly, sharpens Q0 (agent may have an opinion, not an action), keeps Q1 faithful to "fitness is evidence not ranking." Anti-automation-bias guardrail: rationale always names what champion is worse at. Cost medium. **Pareto #2.**

## Direction 3 — Rejection as durable negative evidence
UIDecisionType=reject persists as durable UIDecisionRecord, typed by UIIdentityRelationType (replaced-by/removed/reshaped), folded into PrototypeGenome as negative constraint, never re-surfaced. Resolves Q3 fully, partially Q4 (replaced-by = registry successor edge). Load decreases over time — system gets quieter as taste is learned. Cost medium. **Pareto #3 — compounding gain.**

## Direction 4 — Preference-learning loop, proof-walled
Overrides/rejections (FitnessSignal source=human) deterministically tune the next nomination and generation defaults — reversible proposal-tuning is ungated; rule-change requires RulePromotionRequest + ProofObligation + EvaluateProofGate=pass (stays deferred per D-009/EC5). Resolves Q7 (autonomy envelope = reversible agent may / irreversible human+proof disposes), operationalizes Q1, forces Q8 proof schema. Learned preferences auditable because expressed in controlled vocab. Cost med-high, risk high (touches D-009). **Pareto #4 — near frontier, sequence last.**

## Direction 5 — Failure & recovery as first-class states
Closes the grep-verified "no failure states" gap. Adds named states (GenerationFailed, SynthesisTimedOut, SourceStale, ApplyConflicted) to the existing state sets; reuses GateState=blocked with reasons; annotations never lost (append-only CommentEvent); staleness detected against existing BaselineRevisionAnchor. Resolves Q5 fully, synergistic with Q9 (aria-live announce once) and Q0 (lead-when under failure). Determinism makes "safe to retry" a true type-backed claim. Cost low-to-medium (mostly specification). **Pareto #5 in novelty, #1 in necessity — precondition for trusting D2/D4.**

## Cross-cutting
Lift "no raw values" into a named ProofObligation checked by EvaluateProofGate (shape only, not meaning — enum/token binding stays human-confirmed per W3C-DTCG caveat). It makes D1 diffs honest, D2 rationales reproducible, D4 preferences auditable.

## Ranked Recommendation
1. D5 (failure/recovery) — foundation first. 2. D1 (conformance delta) — highest gain/cost, produces the signal substrate. 3. D2 (champion framing) — kills paralysis, articulates Q0. 4. D3 (durable rejection) — closes Q3, compounds. 5. D4 (preference learning) — bounded reversible half only in MVP, rule-promotion specified but deferred behind proof.

Thesis for s3: *Make the human review the change not the genome; let the agent have an accountable opinion but never an unaccountable action; remember every yes and no in the token contract; never lose the human's work — then let the agent start to learn.*