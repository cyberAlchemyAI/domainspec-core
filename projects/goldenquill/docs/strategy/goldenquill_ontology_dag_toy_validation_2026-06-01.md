---
title: GoldenQuill Ontology DAG Toy Validation Handoff
date: 2026-06-01
status: validation-design-not-run
source_research: docs/strategy/goldenquill_ontology_dag_grant_research_findings_2026-06-01.md
---

# GoldenQuill Ontology DAG Toy Validation Handoff

## Purpose

Define the first safe validation target for a GoldenQuill grant-writing DAG.

This is a validation design, not a completed validator run. The research found
adjacent gates and fixtures, but no first-class `grant_dag` validator exists
yet.

## Toy Fixture Shape

Use synthetic, non-client data.

Minimum nodes:

| Node | Branch | Purpose |
| --- | --- | --- |
| `applicant_archetype` | operational | Synthetic applicant context, explicitly non-client. |
| `funder` | meaning | Real or curated funder identity with source provenance. |
| `program` | meaning | Program/rule object with eligibility constraints. |
| `eligibility_gate` | system | Deterministic pass/fail rule. |
| `evidence_source` | bridge | Source/provenance record. |
| `research_partner` | operational | Partner/capacity requirement. |
| `funder_fit_hypothesis` | bridge | Candidate hypothesis that must cite its substrate. |
| `grant_outcome_event` | operational | Source-backed submission, review, award, decline, reporting, or closeout event. |
| `application_lifecycle_state` | operational | Deepest verified grant stage reached. |
| `grant_kpi_observation` | bridge | Metric observation with numerator, denominator, and denominator definition. |

Minimum edges:

- `program constrained_by eligibility_gate`
- `funder_fit_hypothesis evidenced_by evidence_source`
- `funder_fit_hypothesis constrained_by program`
- `applicant_archetype tested_by eligibility_gate`
- `research_partner evidenced_by evidence_source`
- `funder_fit_hypothesis blocked_by_gate eligibility_gate` for negative cases
- `application_lifecycle_state advanced_to_stage grant_outcome_event`
- `grant_kpi_observation measured_by grant_outcome_event`
- `grant_outcome_event outcome_recorded_by evidence_source`

## Positive Case

A SARE-like research program passes when:

- applicant archetype is a producer or producer-led applicant,
- researcher/extension/NGO partner exists,
- outreach/dissemination evidence exists,
- funder/program identity has source provenance,
- every graph edge is acyclic and resolved,
- no per-org source is read.
- one source-backed outcome event is present;
- one KPI observation has an explicit denominator definition.

## Negative Cases

Each case should fail closed:

| Case | Expected result |
| --- | --- |
| Missing producer | Eligibility fail; no Scribe path. |
| Missing researcher/extension/NGO partner | Eligibility or evidence gap fail. |
| Fabricated funder/source | Fabrication fail. |
| Unknown namespace | Namespace fail. |
| Cross-org source | Org isolation fail. |
| Cycle in DAG | Graph structure fail. |
| Individual/for-profit attempted against non-org-forbidden program | Eligibility fail. |
| Edge target missing | Graph resolution fail. |
| Node lacks authority class | Authority classification fail. |
| Win-rate KPI missing denominator definition | Metric safety fail. |
| Rejection learning promoted without source-backed feedback | Promotion guardrail fail. |
| Stage-depth score treated as a win | Stage/outcome separation fail. |
| Org-scoped feedback generalized without redaction | Org-scope fail. |

## Validator Requirements

The first validator should check:

1. all node ids are unique;
2. all edge endpoints exist;
3. graph is acyclic;
4. every node has branch, authority class, org scope, and source/provenance;
5. every edge has a typed relation from the allowed set;
6. no edge uses vague `supports`;
7. `MemoryEvidencePacket` references are valid when used;
8. workspace-scoped evidence does not smuggle per-org source paths;
9. per-org evidence is rejected unless the fixture explicitly declares one org;
10. fabricated funder/program/source identifiers fail;
11. hard eligibility failures stop traversal to draft/Scribe nodes;
12. card-derived nodes are marked as working YAML, signed contract, or candidate
    source explicitly;
13. `research_evidence` and `research_and_evidence` aliases cannot silently
    unify without a mapping.
14. `GrantOutcomeEvent` requires a source reference;
15. `ApplicationLifecycleState` points to the event that justifies the stage;
16. `GrantKpiObservation` carries numerator, denominator, and denominator
    definition;
17. a won, lost, or pending grant can create a learning candidate, but not a
    promoted lesson;
18. post-award reporting evidence is distinct from award evidence.

## Suggested File Scope

```text
projects/goldenquill/pipeline/grant_dag/
  __init__.py
  models.py
  validate.py

projects/goldenquill/tests/grant_dag/
  test_grant_dag_validator.py
  fixtures/
    valid_sare_like_research_graph.json
    invalid_missing_producer.json
    invalid_missing_research_partner.json
    invalid_fabricated_funder.json
    invalid_unknown_namespace.json
    invalid_cross_org_source.json
    invalid_cycle.json
    invalid_for_profit_forbidden_program.json
    invalid_missing_authority_class.json
    invalid_vague_supports_edge.json
    invalid_card_alias_drift.json
    invalid_kpi_missing_denominator.json
    invalid_rejection_promoted_without_feedback.json
    invalid_stage_depth_treated_as_win.json
    invalid_org_feedback_generalized_without_redaction.json
```

## Suggested Validation Commands

From `projects/goldenquill`:

```bash
.venv/bin/python3 -m pytest tests/grant_dag/test_grant_dag_validator.py -v
.venv/bin/python3 -m pytest tests/cli/test_tilth_memory_query.py -v
.venv/bin/python3 -m pytest tests/memory/ -v
.venv/bin/python3 -m pytest tests/logician/gates/test_f_vector_ns_mismatch.py -v
```

If the existing venv is unavailable, follow
`projects/goldenquill/docs/GETTING_STARTED.md` rather than using system
`python3 -m pytest` as the production validation surface.

## Promotion Boundary

Passing this toy validator should mean only:

- the grant DAG contract is structurally coherent,
- demo/non-org fixtures satisfy the minimal graph rules,
- negative cases fail closed.

It should not mean:

- Ontology Vault schema is canonical in GoldenQuill,
- cards or FID records are updated,
- org-vault memory can be read or written,
- Reflection Packet is active,
- proposal prose can be reused as evidence,
- card runtime graphing is active,
- retrieved card working YAML has signed-bundle authority.
- win/loss KPI observations are promotion authority.
- post-award reporting success proves all proposal claims true.

## Next Task Session

Recommended SWU:

```text
Implement GrantDagNode/GrantDagEdge models and the first acyclicity,
endpoint-resolution, authority-class, org-scope, MemoryEvidencePacket-reference,
card-authority, alias-drift, no-vague-supports, lifecycle-outcome, and KPI
denominator validator tests using only synthetic/demo fixtures.
```

Done criteria:

- validator passes one positive fixture;
- validator fails the listed negative fixtures;
- no production memory/card/org files are read or written;
- test output is deterministic.
- one positive fixture includes an outcome event and KPI observation.
