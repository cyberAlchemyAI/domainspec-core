---
title: GoldenQuill Canonical Promotion Record Refinement
date: 2026-06-03
status: refined-canonical-direction
target_owner: GoldenQuill strategy with Ontology Vault governance
source_artifacts:
  - docs/strategy/goldenquill_promotion_mechanism_research_2026-06-01.md
  - docs/strategy/goldenquill_promotion_mechanism_invoke_design_2026-06-01.md
  - docs/strategy/goldenquill_promotion_governance_architecture_design_2026-06-01.md
  - docs/strategy/goldenquill_ontology_dag_grant_research_synthesis_2026-06-01.md
  - docs/decisions/goldenquill-promotion-mechanism-open-gaps.md
  - arcanum/arcana/ontology-vault/development/schema-validation-plan/GOVERNED-CANDIDATE-BUNDLE.md
---

# GoldenQuill Canonical Promotion Record Refinement

## Refinement Verdict

GoldenQuill should treat this strategy surface as the canonical applied version
of the promotion-record solution.

The canonical split is:

```text
GoldenQuill grant-specific model
  -> PromotionCandidate
  -> OntologyVaultProjection
  -> PromotionRecord-compatible owner decision
  -> approved reuse, rejection, contradiction, retirement, or private residue
```

GoldenQuill owns the grant-domain runtime semantics: grant-run DAG nodes,
outcome events, KPI observations, redaction/generalization, and application
lifecycle state.

Ontology Vault owns the promotion-governance semantics: evidence sufficiency,
target owner routing, review gate, contradiction path, approved uses, and the
decision record that allows something to become reusable authority.

Other implementations should follow or adapt from this model by keeping their
local domain objects local, then projecting promotion decisions into the same
PromotionRecord-compatible governance boundary.

## Why This Can Be Canonical Here

This is not just a proposal anymore. The existing strategy set already resolves
the core ownership decisions:

- `PromotionCandidate` lives in GoldenQuill's local model.
- Ontology Vault is an explicit governance layer, not an afterthought.
- `proposed_allowed_uses` and `approved_allowed_uses` stay separate.
- KPIs can create candidates, but never promote directly.
- org-scoped feedback requires redaction/generalization before shared reuse.
- stage depth remains separate from outcome truth and validation truth.

Those decisions are strong enough to make GoldenQuill the canonical applied
reference for grant-writing promotion governance.

## Canonical Objects

### `MemoryEvidencePacketRef`

Source-bound evidence reference.

Required behavior:

- points to evidence, source, locator, authority class, org scope, retrieval
  surface, and freshness;
- never approves reuse;
- never mutates memory, cards, ontology, definitions, or org vault state.

### `PromotionCandidate`

GoldenQuill-local proposal object.

Required behavior:

- names the proposed claim, relation, lesson, card delta, org memory, definition,
  or gate rule;
- cites evidence packets, outcome events, and KPI observations;
- names target owner and target artifact;
- carries proposed allowed uses only;
- carries review gate, blockers, privacy scope, redaction status, and
  contradiction path;
- cannot be treated as approved reuse.

### `OntologyVaultProjection`

Compatibility layer from GoldenQuill local semantics to PromotionRecord
governance.

Required behavior:

- maps a candidate to `record_kind: promotion_record` semantics when the target
  is ontology or reusable governance;
- verifies evidence refs, target relation, review gate, contradiction path, and
  governance state;
- blocks mutation when governance evidence is incomplete;
- does not mutate the target artifact.

### `OwnerDecision`

The local approved/rejected/retired/contradicted decision record.

Required behavior:

- records the owner decision;
- records approved allowed uses;
- records conditions, source, date, and contradiction path;
- is appendable to an audit projection;
- hands accepted changes to the owning lifecycle route.

### `PromotionRecord`

The canonical governance decision shape.

Required behavior:

- one primary claim or relation;
- evidence pointers, not raw source dumps;
- target owner and target relation;
- review or validation gate;
- evidence confidence and commitment confidence preserved;
- contradiction path;
- rollback, retirement, or supersession path;
- no replacement of the owner artifact.

## What Other Implementations Must Preserve

Other implementations may rename local candidate objects, use different domain
events, or maintain different ledgers. They must preserve these invariants:

1. Evidence capture is not promotion.
2. Retrieval is not authority.
3. Review signal is not truth.
4. KPI or dashboard observation is not promotion authority.
5. Candidate use and approved use are separate.
6. Private or org-scoped evidence cannot become workspace-global without a gate.
7. Promotion requires an owner decision.
8. Promotion requires a contradiction path.
9. The audit ledger is a projection, not the canonical source of truth.
10. Owner artifacts mutate only through their owning lifecycle route.

## What We Need Next

### L0: Canonical Fixture Pack

Create fixture-only proof under:

```text
projects/goldenquill/pipeline/grant_dag/fixtures/
projects/goldenquill/tests/grant_dag/fixtures/
```

Required positive fixtures:

- source-backed outcome event;
- KPI with denominator definition;
- promotion candidate with proposed allowed uses;
- ontology-vault projection with PromotionRecord-compatible fields;
- redacted feedback candidate;
- owner decision with approved allowed uses.

Required negative fixtures:

- outcome event without source;
- KPI without denominator definition;
- stage-depth treated as award;
- candidate without contradiction path;
- candidate with approved uses before owner decision;
- workspace-global reuse from org-scoped feedback without redaction;
- governance projection missing evidence;
- promotion from KPI threshold alone.

### L1: Local Validator

Implement a deterministic validator that checks fixture shape and closes false
promotion paths.

Suggested package:

```text
projects/goldenquill/pipeline/grant_dag/
  models.py
  validate.py
  promotion/
  ontology_vault/
  metrics/
  privacy/
```

The validator should return named failures, not prose-only warnings.

### L2: Ontology Vault Compatibility

Add an adapter that proves GoldenQuill candidates can become
PromotionRecord-compatible records without making GoldenQuill itself the global
ontology authority.

This adapter should be the contract other implementations copy or adapt.

### L3: Owner Decision And Audit Projection

Add append-only audit projection after owner decision.

The ledger may answer:

- what was proposed;
- who decided;
- what was approved;
- what was rejected, contradicted, or retired;
- what owner route must perform any real mutation.

The ledger must not perform mutation.

## Canonical Boundary

Canonical now:

- GoldenQuill's applied promotion-governance split;
- local `PromotionCandidate` as proposal unit;
- `OntologyVaultProjection` as compatibility layer;
- PromotionRecord-compatible decision requirements;
- state separation across evidence, candidate, decision, outcome, KPI, and
  ledger.

Candidate until proven by L0/L1:

- exact Python module names;
- exact fixture file names;
- exact enum spelling for every grant stage and KPI;
- whether `OwnerDecision` is a standalone file, model, or projection;
- whether Ontology Vault later exposes a separate canonical PromotionRecord
  template.

Not allowed yet:

- production org-vault mutation;
- signed-card mutation;
- canonical ontology template mutation;
- automatic KPI-based promotion;
- dashboard-driven promotion;
- workspace-global reuse of private feedback without redaction and owner
  approval.

## Recommended Next Route

Run a bounded task session for L0:

```text
Create the GoldenQuill grant_dag canonical promotion fixture pack and validator
plan. Use synthetic/demo data only. Prove positive and negative cases for
PromotionCandidate, OntologyVaultProjection, OwnerDecision, GrantOutcomeEvent,
GrantKpiObservation, and privacy redaction. Do not mutate production memory,
cards, org vault, ontology, or dashboard code.
```

Done criteria:

- fixture list exists;
- each fixture names expected pass/fail result;
- validator rule IDs exist;
- no production state is read or written;
- GoldenQuill-to-PromotionRecord compatibility is explicit.
