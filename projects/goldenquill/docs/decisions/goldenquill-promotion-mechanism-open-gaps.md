---
title: GoldenQuill Promotion Mechanism Open Gaps Decision Gate
date: 2026-06-01
status: pass
target_scope: goldenquill-promotion-mechanism
source_artifacts:
  - ../strategy/goldenquill_promotion_mechanism_research_2026-06-01.md
  - ../strategy/goldenquill_promotion_mechanism_invoke_design_2026-06-01.md
  - ../strategy/goldenquill_promotion_mechanism_refresh_report_2026-06-01.md
  - ../strategy/goldenquill_promotion_mechanism_refine_seed_2026-06-01.md
  - ../strategy/goldenquill_ontology_dag_grant_research_synthesis_2026-06-01.md
  - ../strategy/goldenquill_ontology_dag_toy_validation_2026-06-01.md
---

# GoldenQuill Promotion Mechanism Open Gaps Decision Gate

## Gate Result

Result: `PASS` for proceeding to a bounded design/implementation plan.

Reason: all blocker-level choices about artifact ownership, first
implementation home, metric authority, org-scoped learning, and stage-depth
scoring have been resolved by operator decision.

Safe next step: refresh the design artifacts from this decision record, then
run Refine or Task Session against the now-resolved route.

Unsafe next step: implement production schema, dashboard importers, ontology
template promotion, org-vault mutation, or KPI-based promotion.

## Blocker Decisions

### DG-001: Promotion Unit Home

Question: Where does `PromotionCandidate` live?

Options:

| Option | Benefit | Cost / Risk | Choose When | Downstream Impact |
| --- | --- | --- | --- | --- |
| GoldenQuill local model | Fastest path to toy validator and grant-specific semantics. | May drift from Ontology Vault `PromotionRecord`. | The first goal is validating grant outcomes and KPIs. | Implement under GoldenQuill `grant_dag` or development fixtures. |
| Ontology Vault companion schema | Strongest governance alignment. | Slower; requires Ontology Vault gate and companion-template decision. | The first goal is reusable Arcanum-wide promotion semantics. | Route to Ontology Vault decision-gate before GoldenQuill implementation. |
| Bridge artifact between both | Preserves separation; can reference `MemoryEvidencePacket` and later emit `PromotionRecord`. | More moving parts in the first slice. | The first goal is avoiding premature ownership. | Implement a candidate bridge and map to owner-specific records later. |

Selected option: GoldenQuill local model with Ontology Vault as an explicit
governance layer.

Rationale: GoldenQuill needs a local grant-specific model, but Ontology Vault
should be embedded as the promotion-governance layer so local grant semantics do
not drift into ungoverned memory authority.

Downstream impact: the next route should design a GoldenQuill-local
`PromotionCandidate` surface with an `ontology_vault` layer or adapter that maps
to PromotionRecord-compatible governance. GoldenQuill may own grant-specific
runtime shape, while Ontology Vault owns promotion semantics and authority
checks.

Status: resolved and revised by operator answer on 2026-06-01.

### DG-002: First Implementation Location

Question: Where should the first executable slice land?

Options:

| Option | Benefit | Cost / Risk | Choose When | Downstream Impact |
| --- | --- | --- | --- | --- |
| `projects/goldenquill/pipeline/grant_dag/` | Matches current toy validation handoff. | Creates new package surface. | Grant DAG validation is the immediate task. | Enables local pytest fixtures. |
| memory mesh development folder | Keeps promotion near `MemoryEvidencePacket`. | Risks making evidence packet look like promotion owner. | The first task is schema pressure, not runtime. | Good for docs/fixtures, weaker for runtime validators. |
| Ontology Vault fixtures | Tests `PromotionRecord` pressure directly. | Not GoldenQuill-runtime ready. | The main gap is schema compatibility. | Requires Ontology Vault lifecycle route. |

Selected option: GoldenQuill local implementation with an Ontology Vault layer.

Rationale: the first executable slice should live where GoldenQuill can test
grant lifecycle, KPI, and outcome semantics, but the package must make Ontology
Vault promotion governance a first-class layer rather than an external afterthought.

Likely path:

```text
projects/goldenquill/pipeline/grant_dag/
  ontology_vault/
  promotion/
  metrics/
```

Downstream impact: the first validator can run in GoldenQuill while enforcing
PromotionRecord-compatible constraints and non-promotion guardrails.

Status: resolved by operator answer on 2026-06-01.

### DG-003: `allowed_uses` Ownership

Question: Who owns `allowed_uses`: evidence packet, candidate, owner decision,
or all three?

Options:

| Option | Benefit | Cost / Risk | Choose When | Downstream Impact |
| --- | --- | --- | --- | --- |
| Evidence packet owns uses | Simple and early. | Overloads `MemoryEvidencePacket`; may confuse retrieval with authority. | Evidence source itself imposes usage constraints. | Requires schema gate before changing packet. |
| Candidate owns uses | Keeps proposed use separate from source capture. | Candidate can overclaim without owner decision. | Need proposal-stage controls. | Useful in toy validator. |
| Owner decision owns final uses | Safest authority model. | Requires two-stage allowed use: proposed vs approved. | Promotion safety matters more than brevity. | Recommended for production. |
| Split proposed/approved uses | Most precise. | More fields and validation. | Need clear lifecycle distinction. | Best long-term fit. |

Selected option: split proposed/approved uses.

Rationale: `PromotionCandidate` should express requested or proposed uses, while
the Ontology Vault governance layer or owner decision records approved uses.
This preserves the distinction between retrieval, candidate intent, and
authorized reuse.

Downstream impact: candidate schema should use `proposed_allowed_uses`; owner
decision or PromotionRecord-compatible output should use `approved_allowed_uses`.

Status: resolved by operator answer on 2026-06-01.

### DG-004: KPI Authority Boundary

Question: Which KPIs are dashboard-only, and which may create promotion
candidates?

Options:

| Option | Benefit | Cost / Risk | Choose When | Downstream Impact |
| --- | --- | --- | --- | --- |
| All KPIs dashboard-only | Safest. | Learning loop is weaker. | Early implementation or sensitive data. | KPIs cannot trigger promotion. |
| Selected KPIs create candidates | Balanced. | Requires denominator and interpretation checks. | Need outcome-driven learning. | Metrics can create candidate lessons, not promotions. |
| KPIs can promote after thresholds | Automatable. | High risk of false authority and Goodhart effects. | Only after mature validation and owner approval. | Not suitable now. |

Selected option: selected KPIs create candidates.

Rationale: KPI observations should support outcome-driven learning, but only as
candidate generators. They cannot promote directly and must pass denominator,
source, org-scope, and interpretation checks first.

Downstream impact: `GrantKpiObservation` can emit `PromotionCandidate` records
when validation passes; the Ontology Vault layer or owner decision still owns
promotion.

Status: resolved by operator answer on 2026-06-01.

### DG-005: Org-Scoped Feedback Generalization

Question: How can rejection/win feedback become reusable without leaking private
org or funder context?

Options:

| Option | Benefit | Cost / Risk | Choose When | Downstream Impact |
| --- | --- | --- | --- | --- |
| Always org-scoped | Safest. | Reduces reusable learning. | Early or client-sensitive phase. | Feedback cannot become workspace-global. |
| Redaction/generalization gate | Reusable but controlled. | Needs policy and fixtures. | Need cross-client learning safely. | Adds validator cases. |
| Operator manual promotion only | Human judgment. | Slower and less consistent. | Low volume or high sensitivity. | Requires decision records. |

Selected option: redaction/generalization gate.

Rationale: feedback should remain org-scoped by default, but GoldenQuill should
be able to create reusable learning after privacy-safe abstraction and owner
approval.

Downstream impact: validators need negative fixtures for workspace-global
feedback without redaction, and positive fixtures for redacted/generalized
learning candidates.

Status: resolved by operator answer on 2026-06-01.

### DG-006: Stage-Depth Scoring

Question: Should `stage_depth_score` be global or funder-family-specific?

Options:

| Option | Benefit | Cost / Risk | Choose When | Downstream Impact |
| --- | --- | --- | --- | --- |
| Global enum/score | Simple and comparable. | Federal-centric enum may misfit foundations and corporate grants. | First toy validator. | Easy positive/negative fixtures. |
| Funder-family-specific score | More accurate. | Harder to compare and validate. | After several funder families are modeled. | Needs family profiles. |
| Global stage plus local profile override | Balanced. | Slightly more schema. | Want generality without overfitting. | Recommended production direction. |

Selected option: global stage plus local profile override.

Rationale: use one baseline stage-depth model for toy validation and dashboard
comparability, while allowing funder-family profile overrides once foundation,
federal, corporate, or other grant-family evidence proves the baseline too
coarse.

Downstream impact: schema should include a global lifecycle enum plus optional
profile override metadata.

Status: resolved by operator answer on 2026-06-01.

## Deferrable Decisions

| Decision | Why Deferrable |
| --- | --- |
| Whether wins and rejections both create Reflection Packet candidates by default. | Can wait until Reflection Packet activation or learning-loop implementation. |
| Whether post-award performance influences future proposal strategy promotion. | Important, but not needed for first outcome-event validator. |
| Whether `GrantOutcomeEvent`, `ApplicationLifecycleState`, and `GrantKpiObservation` are first-class runtime objects or projections. | Refine can decide; toy validator can model them as JSON nodes first. |
| Whether GoldenQuill's stage/outcome/validation split becomes a formal validator rule. | It can start as a design invariant and become a validator after fixtures exist. |
| Whether all portal/agency statuses are tracked internally or imported only as evidence packets. | Toy fixtures can use source-backed imported events first. |

## Assumptions Safe For Refine

- `MemoryEvidencePacket` remains evidence input, not promotion authority.
- `PromotionCandidate` remains proposal-level until an owner decision.
- `PromotionRecord` or owner-specific decision record owns promotion.
- KPI observations are read models and cannot promote anything by themselves.
- Rejections, wins, and review feedback can create learning candidates, not
  promoted lessons.
- Toy validation uses synthetic/demo fixtures only.

## Remaining Blockers

None.

## Next Step

Proceed to refresh the promotion-mechanism design from these decisions, then
run the validated Refine strategy or a bounded Task Session for the first toy
validator.
