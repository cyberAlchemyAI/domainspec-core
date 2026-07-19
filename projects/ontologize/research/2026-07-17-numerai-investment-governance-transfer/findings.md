## Goal

Determine which Numerai mechanisms can strengthen Investiment Strategy validation and Ontologize evidence governance, which require adaptation, and which must be rejected—without authorizing implementation, staking, or live-capital exposure.

## TL;DR

Numerai is useful implementation precedent, not a missing product layer. Its strongest portable evidence is config-driven evaluation, machine-readable result artifacts, time-respecting validation, and explicit separation of performance, contribution, exposure, and delayed outcomes; its exact metrics, constants, data, runtime, and economics do not transfer. Investiment Strategy remains the proposed or specified calculation surface, while Ontologize may record and govern evidence but may not calculate financial scores, select models, trade, or make monetary stake a proxy for truth. No local runtime was proven. [Agent 1](./research.md#agent-1--official-numerai-example-scripts-code-archaeology) [Agent 2](./research.md#agent-2--official-numerai-scoring-and-staking-mechanism-analysis) [Agent 3](./research.md#agent-3--local-ownership-gap-and-authority-boundary-audit)

## Context

The question crossed executable Numerai examples, official scoring/staking semantics, and two local authority surfaces. Static inspection found concrete precedent but no clean-environment execution; official documentation bounded what the metrics and staking can prove; the local audit then exposed collisions with specified-but-unbuilt validation and Ontologize's unproved runtime lineage. A single-source reading would therefore confuse precedent, ownership, and proof. [Agent 1](./research.md#agent-1--official-numerai-example-scripts-code-archaeology) [Agent 2](./research.md#agent-2--official-numerai-scoring-and-staking-mechanism-analysis) [Agent 3](./research.md#agent-3--local-ownership-gap-and-authority-boundary-audit)

## Synthesis

Agent 1 establishes the implementation surface: versioned dataset materialization and ID/time alignment, config-driven era-aware evaluation, OOF/result artifacts, and results JSON. It also exposes portability limits: Numerai-specific data/schema coupling, inconsistent embargo defaults, no dependency lock, an unreliable tutorial drawdown cell, and no local cost or execution model. These are precedents and cautions, not runtime proof. [Agent 1](./research.md#agent-1--official-numerai-example-scripts-code-archaeology) [frozen example-scripts tree](https://github.com/numerai/example-scripts/tree/2447005b3f2af1fd45b883f2e63d1ebb80f75981/numerai)

Agent 2 supplies the semantic boundary. CORR measures target alignment, MMC residual contribution relative to a changing Meta Model, and FNC linear feature dependence; none establishes realized return, causality, robustness, or general truth. Staking signals willingness to accept tournament-defined loss and affects ensemble weight, but even Numerai distinguishes trust from correctness. [Agent 2](./research.md#agent-2--official-numerai-scoring-and-staking-mechanism-analysis) [CORR](https://docs.numer.ai/numerai-tournament/scoring/correlation-corr) [MMC](https://docs.numer.ai/numerai-tournament/scoring/meta-model-contribution-mmc) [FNC](https://docs.numer.ai/numerai-tournament/scoring/feature-neutral-correlation) [staking](https://docs.numer.ai/numerai-tournament/staking)

Agent 3 supplies ownership reality. Pearson/Spearman, purged walk-forward validation, anti-overfit controls, regimes, baselines, and ablation are specified but unbuilt; the work pack reports all implementation and verification tasks not started. Feature exposure, neutralization, aggregate-residual contribution, ensembles, and deployment remain genuinely absent or have only proposed destinations. Ontologize's evidence contracts are designed but runtime-unproved, and its entrypoint lineage is internally inconsistent. [Agent 3](./research.md#agent-3--local-ownership-gap-and-authority-boundary-audit) [L0 method](/home/vrondelli/projects/investiment-strategy/docs/features/quant-delay-validation-mvp/l0-method-design.md:61) [work pack](/home/vrondelli/projects/investiment-strategy/docs/features/quant-delay-validation-mvp/WORK-PACK.md:32) [Ontologize method](/home/vrondelli/projects/domainspec-core/projects/ontologize/OPTIMIZATION-CHAIN-METHOD.md:127)

## Verdict matrix

`KILL` is used only for a failed/nonexistent witness or a definitional collapse. A PASS witness means testable now, not novel or implemented.

| candidate | owner (precedent) | witnessed? (non-vacuity) | sound? (definitional) | verdict |
|---|---|---|---|---|
| Versioned dataset materialization + ID/time alignment | Investiment Strategy proposed destination; precedent-clean Numerai implementation pattern | **PASS:** freeze/rerun one manifest; inject duplicate, missing ID, and coverage gap | **KEEP as a distinct implementation pattern; existing local concept ownership was not established** | Adapt as proposed implementation precedent; owner acceptance required [A1][A3] |
| Config-driven execution + results JSON | OOS validation specified-unbuilt; Numerai precedent-clean for execution/results form | **PASS:** one frozen lane/config, derived purge, fold-indexed OOS rows, reproducible result | **SPLIT** from prediction artifacts and local infrastructure | Adapt the implementation form, not Numerai semantics [A1][A3] |
| Hashes, environment capture, formal result schema | Proposed local obligations; no ownership proved | **PASS only as additions to the reproducibility witness** | Sound as proposals, not Numerai precedent | Owner decision required [A1][A3] |
| Evidence-linked `N3 MetricObservation` | Ontologize designed, runtime-unproved; build-from-owned | **PASS:** validate one non-authoritative record pointing to immutable calculation evidence | **COLLAPSE** into existing generic observation | **KILL as new transfer**; exercise owned design [A3] |
| Absolute performance + ablation lift | Investiment Strategy specified-unbuilt; build-from-owned | **HOLD:** identical folds, baseline vs baseline-plus-delay, paired OOS delta | **COLLAPSE** into existing taxonomy; never call it MMC | **KILL as transfer**; build locally [A2][A3] |
| Linear factor-exposure measurement | Genuinely absent; Investiment Strategy only a proposed destination; FNC precedent-clean | **HOLD:** predeclare factor, point-in-time columns, method/version, threshold | **KEEP**, separate from intervention | Adapted diagnostic candidate [A2][A3] |
| Prediction-neutralization intervention | Genuinely absent; destination unaccepted | **HOLD:** exposure witness plus before/after after-cost OOS and signal-loss bound | **KEEP**, separate from measurement; do not call it FNC | Defer [A1][A2][A3] |
| Aggregate-baseline residual contribution | Genuinely absent/deferred; no accepted owner | **HOLD:** implemented aggregate baseline and orthogonalized OOS comparison | **KEEP only if distinct from ablation**; do not call it MMC | Defer [A2][A3] |
| Delayed paper-validation automation | Proposed destination; ownership/runtime unproved | **HOLD:** frozen model, cadence, realization horizon, costs, rule, independent periods; zero capital | **COLLAPSE as Numerai transfer** into local paper-validation intent | **KILL as new transfer**; automation remains proposed [A2][A3] |
| Auxiliary-target prediction ensemble | Genuinely absent; no owner | **KILL:** no independently validated local targets/models | **KEEP** as a distinct deferred experiment | Defer until leakage-safe component artifacts and leave-one-out ablation [A1][A3] |
| Prediction-model runtime contract | Genuinely absent; no runtime/deployment authority | **KILL:** serialization alone cannot prove safe deployment | **KEEP** as distinct, deferred contract | Reject under current authority [A1][A3] |
| Exact CORR/MMC/FNC names/forms and Numerai constants | Numerai-only or overlapping local questions | **KILL:** no decision-changing local witness; `4/8/13/16/200` are unjustified | **COLLAPSE/REJECT** proprietary or renamed forms | Reject [A1][A2][A3] |
| Tournament API/Compute/obfuscated data | Numerai-only | **KILL:** compatibility would not prove local validity | Sound only inside tournament boundary | Reject; no dataset reuse [A1][A2] |
| Staking/token/stake-weighted authority/live capital | Numerai-only; boundary-incompatible | **KILL:** financial loss tolerance cannot evidence truth | Category-boundary failure | Reject [A2][A3] |
| “Numerai validates Ontologize” | No owner or precedent | **KILL:** no causal/comparative bridge | Category error | Reject [A2][A3] |

Evidence for the code candidates comes from Agent 1; metric/economic proof limits from Agent 2; and local statuses/authority from Agent 3. [Agent 1](./research.md#agent-1--official-numerai-example-scripts-code-archaeology) [Agent 2](./research.md#agent-2--official-numerai-scoring-and-staking-mechanism-analysis) [Agent 3](./research.md#agent-3--local-ownership-gap-and-authority-boundary-audit)

[A1]: ./research.md#agent-1--official-numerai-example-scripts-code-archaeology
[A2]: ./research.md#agent-2--official-numerai-scoring-and-staking-mechanism-analysis
[A3]: ./research.md#agent-3--local-ownership-gap-and-authority-boundary-audit

## Typed negative bank

- **Duplicate-import** — dataset/run concepts, generic metric observation, absolute/ablation evidence, and paper-validation intent cannot be claimed as Numerai-derived novelty.
- **Premature-witness** — an auxiliary-target ensemble without independently validated components manufactures apparent diversification.
- **Authority-absent runtime** — cloudpickle success is serialization evidence, not a trusted deployment contract.
- **Definition/coupling failure** — exact CORR/MMC/FNC names obscure locally meaningful targets, baselines, exposures, and transforms.
- **Ungrounded constant** — tournament values and recent-era windows have no valid local witness.
- **Proof-boundary violation** — tournament platform/data compatibility cannot establish local investment validity.
- **Stake-is-not-proof** — loss-bearing, token economics, and ensemble weight cannot establish truth or governance quality.
- **Proof-scope category error** — Numerai cannot validate Ontologize; Ontologize can only preserve and govern resulting evidence.

These negatives are grounded respectively in the implementation mismatches, official proof limits, and local authority audit. [Agent 1](./research.md#agent-1--official-numerai-example-scripts-code-archaeology) [Agent 2](./research.md#agent-2--official-numerai-scoring-and-staking-mechanism-analysis) [Agent 3](./research.md#agent-3--local-ownership-gap-and-authority-boundary-audit)

## Authority and authorization boundary

Investiment Strategy owns financial calculation only where its contracts say so; several destinations above remain merely proposed. Ontologize may store evidence references, denominator semantics, bounded claims, contradiction paths, and owner decisions, but it does not calculate financial metrics, select models, construct portfolios, place trades, or bind truth to monetary stake. Its `veracidade` and commitment topology must remain independent. This dispatch promotes none of the reviewer-suggested type names, proves no runtime, authorizes no file implementation beyond this findings artifact, and recommends no NMR, token, broker, or live-capital action. [Agent 3](./research.md#agent-3--local-ownership-gap-and-authority-boundary-audit) [Ontologize metrics](/home/vrondelli/projects/domainspec-core/projects/ontologize/DAG-AND-METRICS.md:53)

## Connections

| Document | Type | Description |
|---|---|---|
| `./research.md` | `derives-from` | Verbatim explorer evidence synthesized by this findings artifact. |

## Dispatch closeout

- **Exit reason:** `resolved` — final approver Brandenburg accepted the revised findings after one bounded auditor→writer feedback revision.
- **Agents spawned:** `{"total":9,"tree":{"explorer":3,"synthesizer":1,"skeptic":3,"writer":1,"auditor":1,"helpers":0},"loops_used":1}`.
- **Reviewer exchange:** the synthesizer/reviewer zig-zag used its two reviewer turns; the second turn left exact factual corrections that were frozen into the writer brief and accepted by the final auditor.
- **Init gate:** the two independent check-tension agents reached double PASS after the explorer anti-bias axis was rewritten as an explicit specialization of the global theme. Gate infrastructure is not counted in `agents_spawned`.

## Open Questions

- **OQ-1** — What local decision-time unit, horizon, embargo derivation, availability contract, and point-in-time alignment policy should govern the first reproducibility witness? Recommendation: decide these prospectively before adapting any Numerai execution pattern. Owner: Investiment Strategy owner.
- **OQ-2** — Should linear factor-exposure measurement enter a post-L0 validation lane? Recommendation: name one exposure hypothesis and decision threshold first; otherwise decline the candidate. Owner: Investiment Strategy owner.
- **OQ-3** — Who, if anyone, owns the metrics/result JSON artifact, environment capture, and future model-runtime contract? Recommendation: treat a formal schema as a separate proposed obligation, keep these proposals separate, and do not infer ownership from Numerai precedent. Owner: Investiment Strategy owner; human assignment unresolved.
- **OQ-4** — Can Ontologize validate a non-authoritative `N3 MetricObservation` against immutable external calculation evidence without schema expansion? Recommendation: test the existing schema before proposing a new definition-version entity. Owner: Ontologize owner; human assignment unresolved.
- **OQ-5** — Is delayed paper-validation automation in scope, and what cadence, costs, promotion rule, and independent-period minimum apply? Recommendation: resolve scope before building automation; preserve the zero-capital boundary. Owner: Investiment Strategy owner; human assignment unresolved.
- **OQ-6** — Which Ontologize entrypoint reflects the actual runtime state? Recommendation: resolve the `README.md`/`NEXT.md` lineage conflict in a separate governed task; do not silently repair it here. Owner: Ontologize owner; human assignment unresolved.
