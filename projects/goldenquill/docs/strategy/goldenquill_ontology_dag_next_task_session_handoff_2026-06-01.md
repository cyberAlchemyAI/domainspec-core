---
title: GoldenQuill Ontology DAG Next Task Session Handoff
date: 2026-06-01
status: ready-for-task-session
source_synthesis: docs/strategy/goldenquill_ontology_dag_grant_research_synthesis_2026-06-01.md
---

# GoldenQuill Ontology DAG Next Task Session Handoff

## Recommended Route

Use `task-session` for the first implementation layer:

```text
Create a non-production grant DAG validator with synthetic/demo fixtures.
```

## Objective

Implement the smallest useful validation that GoldenQuill can represent grant
knowledge as a typed DAG without authority leakage:

- typed nodes,
- typed edges,
- acyclicity,
- endpoint resolution,
- authority class required,
- org scope required,
- no vague `supports` edge,
- valid `MemoryEvidencePacket` reference when an evidence packet is used,
- explicit card authority when card content appears,
- alias drift detection for `research_evidence` vs `research_and_evidence`,
- no per-org evidence in a workspace/demo run,
- negative fixtures fail closed.

## In Scope

- `projects/goldenquill/pipeline/grant_dag/`
- `projects/goldenquill/tests/grant_dag/`
- JSON fixtures under `tests/grant_dag/fixtures/`
- Deterministic pytest validation.
- Read-only reference to
  `docs/strategy/development/memory-knowledge-mesh-plan/schema/memory_evidence_packet.schema.json`.

## Out Of Scope

- Ontology Vault canonical schema promotion.
- Cards, lessons, Inventory, org vault, Reflection Packet, or FID mutation.
- UI.
- Live funder API calls.
- Reading real org project contexts.
- Hooking the DAG into Scribe/Judge/Logician runtime.

## Suggested SWUs

| SWU | Goal | Verification |
| --- | --- | --- |
| GDAG-SWU-001 | Add `GrantDagNode`, `GrantDagEdge`, `GrantDag` models with enums. | Unit tests construct valid and invalid models. |
| GDAG-SWU-002 | Implement endpoint resolution and acyclicity checks. | Invalid missing-target and cycle fixtures fail. |
| GDAG-SWU-003 | Implement authority/org-scope checks. | Missing authority and cross-org fixtures fail. |
| GDAG-SWU-004 | Implement relation allowlist and ban vague `supports`. | Vague-edge fixture fails. |
| GDAG-SWU-005 | Implement optional MemoryEvidencePacket reference validation. | Invalid packet reference fixture fails. |
| GDAG-SWU-006 | Implement card-authority and alias-drift checks. | Working-YAML-as-signed and alias drift fixtures fail. |
| GDAG-SWU-007 | Add positive SARE-like synthetic fixture. | Positive fixture passes all validators. |

## Acceptance

```bash
cd /home/vrondelli/projects/domainspec-core/projects/goldenquill
.venv/bin/python3 -m pytest tests/grant_dag/test_grant_dag_validator.py -v
```

If `.venv` is not available, record the blocker before using an alternate
runner.

## Residue

- GQ1 subagent memory/vault receipt arrived after the first synthesis draft and
  was folded into the research package.
- Red Team should be conditional in the first DAG contract because runtime
  support exists but not every v0.1 path requires it.
- `meaning` should be candidate-only until Ontology Vault branch naming is
  promoted through its own governance.
- "Verified" remains compound and should not be a single enum value yet.
- `MemoryEvidencePacket` is narrower than the DAG needs; avoid overloading it
  with relation semantics until a schema decision is made.
