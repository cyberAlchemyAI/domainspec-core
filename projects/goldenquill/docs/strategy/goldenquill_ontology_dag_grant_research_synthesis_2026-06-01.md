---
title: GoldenQuill Ontology DAG Grant Research Synthesis
date: 2026-06-01
status: synthesized
findings: docs/strategy/goldenquill_ontology_dag_grant_research_findings_2026-06-01.md
dispatch: docs/strategy/goldenquill_ontology_dag_grant_research_strategy_2026-06-01.dispatch.json
---

# GoldenQuill Ontology DAG Grant Research Synthesis

## Core Finding

GoldenQuill should not copy the Paradigma research-DAG idea as "everything is a
graph" in the abstract. It should adapt it into a grant-specific
claim/evidence/review/decision graph with authority attached to every node and
edge.

The useful move is:

```text
proposal as document
  -> proposal run as execution DAG
  -> grant knowledge as ontology DAG
  -> reusable learning only through owner-approved promotion
```

GoldenQuill already has most of the raw material: Scout discovery and
verification, Scribe claim/source discipline, Judge scoring and responsiveness
maps, Logician gates, memory/vault query helpers, signed cards, FID/PRP
boundaries, demo fixtures, and substrate evidence contracts. What is missing is
the graph contract that prevents those pieces from collapsing into an
undifferentiated "memory" or "draft context."

Late GQ1 memory/vault research sharpened this: `MemoryEvidencePacket` already
exists as a narrower schema, card content already contains rich ontology
material, and card graphing is explicitly named in the loader contract but not
live. So the first implementation should extend and validate existing concepts,
not invent a parallel architecture.

## Recommended Architecture

Use two linked DAGs.

### 1. Execution DAG

This is the runtime/process graph. It answers: what happened in this grant run,
in what order, and what gate allowed or blocked the next step?

Minimum nodes:

- `run_context`
- `project_context_reference`
- `rfa_reference`
- `scout_discovery_record`
- `scout_verification_record`
- `operator_review_decision`
- `rfa_dissection`
- `kgie_preflight`
- `scribe_section_draft`
- `editor_suggestion_report`
- `judge_score_report`
- `responsiveness_map`
- `red_team_review` (conditional)
- `logician_gate_result`
- `operator_signoff`
- `delivery_envelope`

Minimum edges:

- `precedes`
- `consumes`
- `emits`
- `blocked_by_gate`
- `revised_by`
- `approved_by`
- `delivered_as`

### 2. Ontology DAG

This is the meaning/evidence/authority graph. It answers: what claim was made,
what evidence supports or contradicts it, what review tested it, where it was
used, and whether it may be reused.

Use Ontology Vault's candidate branch split:

| Branch | Function |
| --- | --- |
| `meaning` | Funder/applicant/grant semantics: RFA requirements, funder priorities, rubric criteria, applicant facts, budget claims, compliance obligations. |
| `system` | Tilth machinery: Scout outputs, Scribe sections, Editor suggestions, Judge scores, Logician gates, FID records, Cards, PRPs. |
| `operational` | One bounded grant context: org, grant id, RFA, draft version, run id, posture, deadline. |
| `bridge` | Alignment evidence: traceability, realization, validation, constraint, contradiction, drift. |

Minimum node families:

- `authority_surface`
- `opportunity`
- `rfa_requirement`
- `funder_priority`
- `rubric_criterion`
- `applicant_fact`
- `budget_assumption`
- `compliance_rule`
- `evidence_item`
- `proposal_claim`
- `objection`
- `replication_check`
- `score_observation`
- `gate_result`
- `decision`
- `reuse_candidate`
- `card_concept`
- `review_signal`
- `learning_signal`
- `grant_outcome_event`
- `application_lifecycle_state`
- `grant_kpi_observation`

Typed edge families:

- `evidenced_by`
- `contradicted_by`
- `constrained_by`
- `tested_by`
- `scored_by`
- `realized_by`
- `traced_to`
- `consumed_by`
- `blocked_by_gate`
- `approved_by`
- `promoted_by`
- `retired_by`
- `drifts_from`
- `requires_evidence`
- `classified_by_card`
- `forbidden_for_use`
- `advanced_to_stage`
- `measured_by`
- `outcome_recorded_by`

Avoid the machine edge `supports` unless a profile later defines it. It is too
vague for grant authority.

## How This Adapts The Paradigma Reference

The Paradigma reference treats research as a DAG of questions, claims,
experiments, replications, objections, and extensions rather than as a static
paper. For grant writing, the analogous unit is not "the proposal." It is a
traceable graph of funder-fit claims, source evidence, compliance checks,
reviewer objections, draft surfaces, rubric scores, and reuse decisions.

Translation:

| Research DAG primitive | Grant-writing primitive |
| --- | --- |
| Hypothesis | Funder-fit hypothesis, eligibility claim, budget assumption, reviewer-risk claim. |
| Experiment | Draft section, evidence search, rubric scoring pass, compliance check, outreach test. |
| Replication | Second source, second seat, cross-family review, prior-award precedent, repeated scoring pass. |
| Objection | Red Team/Judge challenge, admin-risk warning, missing evidence, rule conflict. |
| Extension | Proposal variant, adjacent opportunity, reusable evidence packet, next funder strategy. |
| Consensus | Signed/operator-approved state after evidence and gate checks, not model agreement. |

This gives GoldenQuill a stronger grant-writing loop:

1. Scout emits candidate opportunity and verification records.
2. Scribe drafts only from source-authorized context.
3. Editor and Judge create review/test nodes, not truth nodes.
4. Logician creates gate nodes that can block graph traversal.
5. Operator decisions create approval/retirement/promotion nodes.
6. Reflection Packet proposes future deltas but does not silently mutate memory.

## Invoke Refresh: Real-World Evidence And KPI Nodes

The grant DAG should track real-world evidence after submission. A proposal that
is declined after agency review is more informative than one that was never
submitted, and a won grant with post-award reporting problems should not be
treated as unqualified proof of proposal quality.

Add three DAG node families:

| Node | Branch | Purpose |
| --- | --- | --- |
| `grant_outcome_event` | operational | Source-backed event such as submitted, portal validated, agency retrieved, under review, awarded, declined, report accepted, or closed out. |
| `application_lifecycle_state` | operational | Projection of the deepest verified stage reached by an application. |
| `grant_kpi_observation` | bridge | Metric read model with denominator semantics and interpretation limits. |

Add these edges:

| Edge | Meaning |
| --- | --- |
| `advanced_to_stage` | outcome event moves an application to a verified lifecycle stage |
| `outcome_recorded_by` | outcome or lifecycle state is backed by a notification, portal export, agency notice, or report |
| `measured_by` | a set of events contributes to a KPI observation |
| `learned_from` | a rejection, win, or feedback event creates a learning candidate |
| `generalized_by` | an org-scoped lesson is redacted or abstracted into workspace-safe learning |

GoldenQuill should enforce this validation rule: do not collapse application
stage, final outcome, and validation state.

- application stage is the point the application reached;
- final outcome is the award, decline, withdrawal, report acceptance, closeout,
  or other source-backed event;
- verification is whether the claim, compliance fact, KPI denominator, or
  feedback interpretation was checked.

This prevents a dashboard metric from becoming promotion authority.

## Authority Model

Every graph node should carry:

```json
{
  "node_id": "stable-id",
  "node_family": "proposal_claim",
  "branch": "meaning | system | operational | bridge",
  "source_path": "path/to/source",
  "locator": "line, key, row, hash, or section",
  "authority_class": "canonical_source | signed_contract | runtime_index | derived_summary | proposal_only | generated_state",
  "org_scope": "workspace_global | single_org | no_org_loaded | cross_org_forbidden",
  "allowed_uses": ["orient", "cite", "draft_support", "decision_input", "promotion_candidate"],
  "verification_state": "unverified | source_resolved | gate_passed | reviewed | contradicted | retired",
  "promotion_owner": "operator | logician | card_ceremony | lessons_memory | org_vault | decision_gate | none"
}
```

Every graph edge should carry:

```json
{
  "edge_id": "stable-id",
  "relation": "evidenced_by",
  "from": "node-id",
  "to": "node-id",
  "evidence_path": "path/to/evidence",
  "bridge_outcome": "aligned | partial | drift | insufficient | contradicted | not_applicable | unknown",
  "created_by": "seat-or-validator",
  "validation_state": "candidate | checked | failed | waived",
  "residue": []
}
```

This merges GoldenQuill's proposed `MemoryEvidencePacket` with Ontology Vault's
branch-aware authority model and GoldenQuill's rule not to collapse application
stage, final outcome, and validation state.

Important repair: the existing `MemoryEvidencePacket` schema currently lacks
`allowed_uses` and `promotion_owner`. The grant DAG can either extend that
schema or define a separate edge payload that references it. The safer first
task is to keep `MemoryEvidencePacket` as an evidence reference and define
grant-DAG edges separately.

## First Implementation Unit

Implement a toy validator before any production graph.

Candidate path:

```text
projects/goldenquill/pipeline/grant_dag/
projects/goldenquill/tests/grant_dag/
```

First objects:

- `GrantDagNode`
- `GrantDagEdge`
- `GrantDagFixture`
- `validate_acyclic`
- `validate_resolved_edges`
- `validate_authority_class`
- `validate_org_scope`
- `validate_no_fabricated_funder`
- `validate_required_positive_case`

First fixture:

- one synthetic applicant archetype,
- one SARE-like research program,
- one producer requirement,
- one researcher/extension/NGO partner requirement,
- one outreach requirement,
- one evidence source,
- one proposed funder-fit hypothesis.

First negative fixtures:

- missing producer,
- missing researcher,
- fabricated funder/source,
- unknown namespace,
- cross-org source,
- cycle,
- individual/for-profit against a non-org-forbidden program.

## Validation Sources To Reuse

- Demo fixtures:
  `projects/goldenquill/tests/demo/demo_rfa/`,
  `projects/goldenquill/tests/demo/demo_project_context/`,
  and `projects/goldenquill/apps/tilth_demo_v0/fixtures/orgs.json`.
- Memory mesh artifacts:
  `docs/strategy/development/memory-knowledge-mesh-plan/schema/memory_evidence_packet.schema.json`
  and
  `docs/strategy/development/memory-knowledge-mesh-plan/WORK-PACK.md`.
- Card surfaces:
  `pipeline/cards/models.py`,
  `pipeline/cards/CLC/research_evidence.yaml`,
  `pipeline/cards/loader.py`,
  and `pipeline/cards/validators.py`.
- Existing tests:
  `projects/goldenquill/tests/demo/test_demo_driver.py`,
  `projects/goldenquill/tests/cli/test_tilth_memory_query.py`,
  `projects/goldenquill/tests/memory/`,
  and vector namespace gate tests.
- Existing gate concepts:
  `F-SCOUT-HYPOTHESIS-FABRICATED`,
  `F-SCOUT-HYPOTHESIS-CROSS-APPLICANT-LEAK`,
  `F-VECTOR-NS-MISMATCH`,
  RFA traceability,
  org isolation,
  KGIE,
  boundary drift.

## What Not To Do Yet

- Do not promote Ontology Vault's candidate schema into GoldenQuill production.
- Do not write to cards, lessons, org vault, Inventory, or canonical ontology.
- Do not use live org context for the toy validation.
- Do not let `supports` become a generic edge type.
- Do not treat Judge score, Scribe prose, or model agreement as truth.
- Do not merge workspace-wide funder intelligence and per-org match/KFR facts.
- Do not rely on card runtime graphing as live; loader step 6 is named but still
  beyond v0.1.
- Do not assume card retrieval proves signed-bundle authority; retrieval may
  return working YAML.
- Do not ignore `research_evidence` vs `research_and_evidence` naming drift.

## Decision Points

1. Use `meaning` as the candidate branch label, with `business/domain/intent` as
   local aliases. This aligns with the newer Ontology Vault candidate without
   globally promoting it.
2. Keep execution DAG and ontology DAG separate but linked. A single graph would
   blur run order with claim authority.
3. Treat "verified" as compound, not scalar. A reusable grant claim should
   require source evidence, authority class, allowed use, and relevant gate or
   review state.
4. Start with JSON fixtures and a deterministic validator. Defer database or UI
   work until the graph contract survives toy cases.
5. Treat card content as `authority_surface` or `card_concept` candidates with
   explicit authority class, not as automatically promoted ontology truth.

## Next Route

Recommended: `task-session` for a small implementation of the toy validator and
fixtures, with `ontology-vault` review after the validator passes.

Fallback: if implementation should wait, run `feature-glossary` over the node and
edge vocabulary first so the contract becomes easier to review.

Pre-task cleanup candidate: update or wrap `MemoryEvidencePacket` so the DAG can
carry `allowed_uses` and `promotion_owner` without overloading retrieval
provenance.
