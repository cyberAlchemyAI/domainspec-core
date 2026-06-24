---
tags: [definitions-governance, schema, ontology, cyberalchemy-v2, subagents-review, morphisms]
node_type: discovery
is_session: true
layer: ontology, architecture
nature: reference, procedural
status: active
created: 2026-06-22
timestamp: 2026-06-22T19:45:00-03:00
expires: 2026-08-21
conversation_id: 2026-06-22-cav2-definitions-schema-governance
decisions_made: true
contradictions_found: false
specs_updated: [cyberAlchemy-v2/authority/definitions/DEFINITIONS.md, cyberAlchemy-v2/authority/definitions/DEFINITIONS-INDEX.md, cyberAlchemy-v2/authority/definitions/DEFINITION-DRIFT-AUDIT.md, cyberAlchemy-v2/authority/definitions/DEFINITION-SCHEMAS.md, arcanum/arcana/definitions-governance/SKILL.md]
promoted_candidates: [CAV2-D34 constitution, CAV2-D35 discipline, CAV2-D36 decision, CAV2-D37 spec]
expected_importance: 7
importance_rationale: "Promoted four artifact-kind definitions, established schema tracking, hardened the definitions-governance sigil, and ran a verified review that steered the schema decision toward reuse/MINIMAL rather than a new abstraction."
---

# CAV2 Definitions Governance — Artifact Kinds, Schema Tracking, and the Schema-Depth Review

## Summary

Ran definitions-governance on `cyberAlchemy-v2`: promoted four authority-object meta-types (D34 constitution, D35 discipline, D36 decision, D37 spec) and established schema tracking (a colocated `### Schema` section on D23 + a new `DEFINITION-SCHEMAS.md` registry), and hardened the public definitions-governance sigil (v0.1.0→0.2.0) with a generic schema-tracking step. A 13-agent `review` dispatch (tension-gated; attackers → synthesizer → 3 verifier layers) then **overturned** the proposal to define `schema` = objects+morphisms+laws at "Fuller" depth: objects+morphisms are already owned (D16/D19/DS-D8), the laws are a real but consumer-less surplus, so the verdict is MINIMAL depth with the registry **drain rule** as the real leverage. Closed by assessing ZefraHub's `ontology-conventions.md` as the proven model to adopt for CAV2's document corpus.

## Next Steps

- Apply in-lane fixes to `DEFINITION-SCHEMAS.md` (drain rule: per-row owner + per-pass resolve-or-reaffirm; resolve OQ-1) and reconcile D23's 6-vs-7 field cardinality + de-duplicate `L(a)`.
- Decision-gate: adopt ZefraHub edge model (objects+typed-morphisms+directionality, **no laws**) for CAV2 docs via `VAULT-CONCEPT-ADOPTION-CONSTITUTION` — only if the edges-table + CI consumer gets built.
- Do NOT mint a generic/Fuller `schema`; if pursued, only a narrow Arcanum-subtyped handle (cite parent; reference D16/D19/DS-D8) gated on a filed D25 witness.
- Submodule discipline: commit+push `arcanum` (sigil edit) before bumping the parent gitlink; regenerate installed sigil copies via `arcanum-bootstrap`.
- Backfill the ~15 queued schema-bearing definitions listed in `DEFINITION-SCHEMAS.md`.

## Open Questions

- Will CAV2 build/wire an edge-type consumer (validator/edges-table)? Without it, all typed-edge/Fuller work stays inert — see review `findings.md` flip condition.
- Is `schema` worth defining locally at all, or stay referenced-to-Arcanum? → definitions-governance.
- Reconcile ZefraHub's 14-edge catalog as concrete instances of D16/D19/DS-D8, or keep separate? → decision-gate.

## Files touched

- cyberAlchemy-v2/authority/definitions/DEFINITIONS.md
- cyberAlchemy-v2/authority/definitions/DEFINITIONS-INDEX.md
- cyberAlchemy-v2/authority/definitions/DEFINITION-DRIFT-AUDIT.md
- cyberAlchemy-v2/authority/definitions/DEFINITION-SCHEMAS.md
- arcanum/arcana/definitions-governance/SKILL.md
- cyberAlchemy-v2/development/reviews/2026-06-22-schema-objects-morphisms-laws-review/findings.md
- cyberAlchemy-v2/development/reviews/2026-06-22-schema-objects-morphisms-laws-review/RETURNS.md
- telemetry/agents/subagents-dispatch.yaml
