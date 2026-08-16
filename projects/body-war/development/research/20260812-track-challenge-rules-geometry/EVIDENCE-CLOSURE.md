# Exact-Binding Evidence Closure

## Verdict

`ready` for an honestly labelled **decision-ready research candidate**.

This verdict is not readiness for rule adoption, deterministic simulation,
pilot execution, Volta do Taquaral geometry acceptance, reward settlement, or
prize-bearing launch. Those edges remain blocked or deferred below.

## Bound Artifact Set

| Artifact | SHA-256 | Role |
|---|---|---|
| `receipts/explorer-competition.json` | `a51146eddcf2f9ac42c155fe99af6f724c3f88e7c1761bb601bcb04de6f4eb71` | competition evidence return |
| `receipts/explorer-geometry.json` | `66d389fee6f5cb854066edb21df1f4097218f15811a158e646aa9cc5c024f665` | geometry evidence return |
| `receipts/explorer-economy-risk.json` | `215ec24cace525ac0de89542061a3dffe5845ee11d96ed5f10455008a256ba60` | economy and risk evidence return |
| `receipts/synthesis.json` | `06d55c5315074fc142dd5116d01129707ed1e648e50b157fd4d8d023bd367b79` | initial synthesis |
| `receipts/synthesis-revised.json` | `f7e2c340c37583badfcde48fdafd489d2c275defed9e7d1d115c5b54d0418ffa` | one-loop revised synthesis |
| `receipts/reviewer-precedent.json` | `b56acbbefc7929798297d1c213609fce5e72114e7287119c2f43ebc1a05806c6` | precedent gate |
| `receipts/reviewer-nonvacuity.json` | `a495c80b0fd50be2e69bcdb968f7212fea5540ceb952b700f2dd25b4f3b64b03` | non-vacuity gate |
| `receipts/reviewer-definition.json` | `163a4b4b1945fcd27ff9846b489f03e79e61f4d07d0746c647ac5da5fc4f87f4` | definition gate |
| `receipts/confrontation-precedent.md` | `72d9e2cb40732187f7f77141996448545ad14aa2caf175a60e103eec97766eb3` | Robot-Talks precedent verdict |
| `receipts/confrontation-nonvacuity.md` | `8deb52ed83115d71d71f4f637e97bc16bce2e1f83d103f6c469ad1b36e416b3b` | Robot-Talks non-vacuity verdict |
| `receipts/confrontation-definition.md` | `c017adf2f77c07bb3d2a4dd294b4921fd4371d7eb0345736fee6f3771023abc7` | Robot-Talks definition verdict |

All 14 exact JSON-pointer references declared by the revised synthesis were
resolved to present, non-null values. This binds what the explorer and reviewer
receipts report. It does not upgrade a mutable external URL into an immutable
source snapshot or convert an agent observation into parent-reverified fact.

## Closure Matrix

| ID | Load-bearing proposition or fixture | Exact binding | Evidence scope and proof status | Closure |
|---|---|---|---|---|
| `EC-COMP-01` | external challenge and exercise-gamification sources provide bounded rationale for cadence, competition, verification, and durability concerns | `receipts/explorer-competition.json#/external_source_table` plus receipt digest above | explorer-reported current platform and peer-reviewed sources; not Body War authority; external sources not independently reopened by parent | `bound` as rationale only |
| `EC-COMP-02` | open standings, frozen division standings, and personal breakthrough are three candidate comparison views; all-time record is a separate record domain | `receipts/synthesis-revised.json#/rule_derivation/10`, `#/compact_glossary/open_standing`, `#/compact_glossary/all_time_record` | informed design hypothesis, not precedent-backed or adopted | `bound` as candidate; adoption `deferred` |
| `EC-COMP-03` | Speed and fixed-duration Distance are separate candidate modes; Speed uses wall-clock elapsed time | `receipts/synthesis-revised.json#/rule_derivation/1`, `#/rule_derivation/7`, `#/compact_glossary/mode` | wall-clock rule has bounded support; Distance duration and boundary function remain unset | `bound` candidate plus parameter `deferred` |
| `EC-COMP-04` | result comparisons require one explicit versioned competition domain and precision policy | `receipts/synthesis-revised.json#/compact_glossary/competition_key`, `#/comparison_invariants` | candidate semantics; exact policy versions and thresholds absent | `bound` candidate plus execution `deferred` |
| `EC-COMP-05` | whether one result projects into open, division, and breakthrough views or each view is a separate competition identity | `receipts/confrontation-definition.md#key-findings`, item 5 | unresolved semantic/product choice exposed by the confrontation | `deferred` to product owner |
| `EC-GEO-01` | TrackGeometry Contract v0 field/lifecycle shape is a candidate specification structure | `receipts/explorer-geometry.json#/track_geometry_contract_v0`; `receipts/synthesis-revised.json#/geometry_boundary` | RFC 7946 supports representation only; gates, corridor, lifecycle, matching, canonicalization, and validator are Body War-designed hypotheses | `bound` as candidate; exact schema/validator `deferred` |
| `EC-GEO-02` | synthetic valid, partial, reverse, shortcut, version-change, replay, vehicle, jump, and drift cases are required test ideas | `receipts/explorer-geometry.json#/deterministic_synthetic_fixtures`; `#/adversarial_examples` | deterministic fixture descriptions, not executed validator results | `bound` as fixture requirements; execution `deferred` |
| `EC-GEO-03` | exact Volta do Taquaral centerline, gates, direction, corridor, length, license, calibration, bytes, digest, and acceptance | `receipts/explorer-geometry.json#/verdict`; `#/missing_exact_evidence`; `receipts/synthesis-revised.json#/deferred_parameters_and_artifacts/0` | no exact course artifact exists in the evidence set | `deferred`; named-course execution blocked |
| `EC-GEO-04` | municipal data is a preferred or corroborating route, not the sole admissible authority; qualified organizer survey may become operational authority after exact acceptance | `receipts/reviewer-precedent.json#/findings/2`; `receipts/synthesis-revised.json#/geometry_boundary/authority_routes` | candidate authority routing, not geometry acceptance | `bound` routing; acquisition `deferred` |
| `EC-ECO-01` | participant-paid attempts or participant-derived value feeding a rolling prize pool | `receipts/explorer-economy-risk.json#/model_comparison/0`; `#/official_sources/0`; `#/official_sources/1` | explorer-reported Brazilian statutory risk analysis; not legal advice or final classification | `killed` for pilot candidate; specialist classification still `deferred` |
| `EC-ECO-02` | earned-only non-purchasable credits plus committed sponsor-funded fixed vouchers in separate ledgers | `receipts/explorer-economy-risk.json#/model_comparison/2`; `receipts/synthesis-revised.json#/rule_derivation/18` | lowest-risk compared informed hypothesis, not safe harbor | `bound` candidate; adoption and launch `deferred` |
| `EC-ECO-03` | only committed and fulfillment-backed unused sponsor inventory may roll; participant-derived value never rolls | `receipts/synthesis-revised.json#/rule_derivation/19`; `#/state_machines/reward_fulfillment/invariants` | candidate invariant; inventory units, caps, expiry, fulfiller, tax, and failure policy absent | `bound` candidate plus settlement `deferred` |
| `EC-STATE-01` | result finality and reward fulfillment are distinct candidate state machines | `receipts/synthesis-revised.json#/state_machines` | semantic topology only; exact guards, actors, intervals, reason codes, and fraud adjudication absent | `bound` candidate plus operation `deferred` |
| `EC-RISK-01` | privacy, safety, overexertion, minors, supplement-claim, fraud-review, appeal, and disclosure constraints | `receipts/explorer-economy-risk.json#/mandatory_terms_and_disclosures`; `#/adversarial_controls`; `receipts/explorer-geometry.json#/track_geometry_contract_v0/privacy_and_safety` | bounded risk inputs; no legal, medical, sponsor, or operational approval | `bound` as constraints; policies and specialists `deferred` |
| `EC-OWNER-01` | alignment with current Body War owner files and ontology delta map | explorer limitations in `receipts/explorer-competition.json#/limitations/0` and `receipts/explorer-economy-risk.json#/source_boundary/limitation` | action inputs did not cause the competition/economy explorers to inspect direct owner files; Inventory remains discovery-only | `deferred`; writer must not claim completed owner alignment |
| `EC-SIM-01` | division fairness, attempt limits, recovery, ties, settlement, cross-version rejection, and sponsor failure are deterministically simulated | `receipts/reviewer-nonvacuity.json#/review/minimum_closure_tests`; `receipts/synthesis-revised.json#/required_revalidation` | tests are required but not executed in this research dispatch | `deferred`; pilot execution blocked |
| `EC-SOURCE-01` | external-source freshness and immutable content binding | explorer URL/selector tables plus local receipt digests | the local report bytes are immutable here; external pages were not snapshotted or independently refreshed by the parent | `deferred` for launch/legal/geometry authority claims |

No matrix row remains `unresolved`: every row is explicitly `bound`,
`deferred`, or `killed`. Deferred rows are not permission to omit them or
describe them as closed.

## Repair Routing And Loop State

- Precedent, non-vacuity, and definition reviewers returned material repairs.
- The single confirmed synthesizer-reviewer zig-zag was exercised once and is
  exhausted.
- The revised synthesis received three independent
  `READY_FOR_EVIDENCE_CLOSURE` confrontation verdicts.
- No explorer feedback was consumed because missing exact Taquaral source bytes
  cannot be acquired inside this run without owner authorization, municipal or
  organizer evidence, consented calibration, and later exact-byte acceptance.
- Writer revision capacity remains available only for citation placement,
  verdict structure, or wording where supporting evidence already exists.

## Writer Contract

The writer may create `findings.md` only and must:

1. title and describe it as a decision-ready **research candidate**;
2. say “three comparison views plus a separate all-time record domain,” not
   an unexplained four-ladder model;
3. call `rule_derivation` rows candidate propositions according to their
   classification, never adopted rules;
4. preserve the ladder-projection-versus-separate-key choice as deferred;
5. distinguish the originating agents’ read-only returns from parent-owned
   persistence;
6. cite explorer receipts and their exact selectors for every load-bearing
   external claim, with their stated proof status;
7. carry every deferred, killed, blocked, and not-independently-refreshed row;
8. include a verdict matrix and never call the result executable, test-ready,
   pilot-ready, legally cleared, source-backed Taquaral geometry, implemented,
   released, deployed, or production-ready.
