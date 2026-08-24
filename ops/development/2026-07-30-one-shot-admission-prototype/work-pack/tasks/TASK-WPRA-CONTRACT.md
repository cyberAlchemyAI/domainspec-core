# TASK-WPRA-CONTRACT

## SWU-OAP-001 — Freeze additive public contracts

- Primary behavior: express a versioned objective-execution projection and
  audit v2 input/output without breaking v1.
- Dependencies: none.
- Source anchors: `work-pack/shared/context.md`; accepted manifest in research.
- Write scope:
  - `arcanum/spells/work-pack-readiness-audit/README.md`
  - `arcanum/spells/work-pack-readiness-audit/schemas/objective-execution-manifest.schema.json`
  - `arcanum/spells/work-pack-readiness-audit/schemas/audit-config-v2.schema.json`
  - `arcanum/spells/work-pack-readiness-audit/schemas/audit-report-v2.schema.json`
- Algorithm:
  1. Define project-neutral owner/binding records and exact digest refs.
  2. Keep status families independent.
  3. Encode epoch approval, risk, budget, frontier, semantic digest, and
     authority-none projection.
  4. Preserve v1 files unchanged.
- Failure modes: collapsed readiness, optional owner refs, generated authority,
  private literals, implicit compensation.
- Done criteria: every schema parses; examples satisfy schemas; README ownership
  is explicit.
- Validation: JSON parse and schema meta-validation.
- Execution owner: local fallback under candidate fast lane.
