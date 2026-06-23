---
tags: [definitions-governance, definitions, schema, sigil, arcanum, authority]
node_type: conceptual
is_session: true
layer: ontology, authority
nature: procedural, reference
status: active
created: 2026-06-22
timestamp: 2026-06-22T18:30:00-03:00
expires: 2026-08-21
conversation_id: 2026-06-22-definitions-governance-cav2
decisions_made: true
contradictions_found: false
specs_updated: [cyberAlchemy-v2/authority/definitions/DEFINITIONS.md, cyberAlchemy-v2/authority/definitions/DEFINITIONS-INDEX.md, cyberAlchemy-v2/authority/definitions/DEFINITION-DRIFT-AUDIT.md, cyberAlchemy-v2/authority/definitions/DEFINITION-SCHEMAS.md, arcanum/arcana/definitions-governance/SKILL.md]
promoted_candidates: [CAV2-D34, CAV2-D35, CAV2-D36, CAV2-D37]
expected_importance: 7
importance_rationale: "Adds the authority-artifact meta-types, a reusable schema-tracking mechanism, and the route for defining framework vocabulary — all affecting future definition work."
---

# Definitions Governance on cyberAlchemy-v2: artifact meta-types, schema tracking, skill-definition route

## Summary

Ran definitions-governance over cyberAlchemy-v2. Promoted four authority-artifact definitions — CAV2-D34 constitution, D35 discipline, D36 decision, D37 spec — completing the D31–D33 meta-type ladder under a define-the-artifact-cite-the-route framing. Established schema tracking: an inline `### Schema` section on D23, a new DEFINITION-SCHEMAS.md registry (D23 tracked, ~15 queued), and a generic schema-tracking step hardened into the canonical sigil. Then dispatched three subagents and found that sigil/spell/capability are undefined even in Arcanum, concluding they should be defined in Arcanum (not CAV2), with CAV2 referencing.

## Next Steps

- Decide and author `DEF-ARC-SIGIL`/`SPELL`/`CAPABILITY` (+ `skill` projection note) in arcanum/definitions/DEFINITIONS.md via arcanum definitions-governance; then add CAV2 reference rows in DEFINITIONS-INDEX.md (touches public submodule — commit+push arcanum before bumping parent).
- Backfill the ~15 queued schema-bearing definitions in DEFINITION-SCHEMAS.md into colocated `### Schema` sections.
- Regenerate installed definitions-governance sigil copies (.claude/skills, .agents/skills, .arcanum/runtimes) via arcanum-bootstrap.
- Optionally add `concept.sigil`/`concept.capability` to ontology/NODE-MODEL.md and route term-ownership (authority/README.md OQ-1) to decision-gate.

## Open Questions

- Where do sigil/spell/capability get defined — Arcanum canonical vs CAV2-local vs hybrid? (authority/README.md OQ-1 → decision-gate)
- Is "skill" a distinct definition (runtime projection of a sigil) or only a note under sigil? (arcanum/README.md capability model)
- Is D27 residue entropy's equation a structural schema worth tracking? (DEFINITION-SCHEMAS.md backlog)

## Files touched

- cyberAlchemy-v2/authority/definitions/DEFINITIONS.md
- cyberAlchemy-v2/authority/definitions/DEFINITIONS-INDEX.md
- cyberAlchemy-v2/authority/definitions/DEFINITION-DRIFT-AUDIT.md
- cyberAlchemy-v2/authority/definitions/DEFINITION-SCHEMAS.md
- arcanum/arcana/definitions-governance/SKILL.md
- telemetry/agents/subagents-dispatch.yaml
