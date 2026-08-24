# Shared Context

## Exact anchors

- Define: `../../../define/DEFINE.md`
- Design: `../../../design/ARCHITECTURE.md`
- Design selection: `../../../design/DESIGN-SELECTION-RESULT.json`
- Research verdict: `../../../../../findings.md`
- Frozen fixture: `../../../../../research.md` lines 270-490
- Craft authority: `arcanum/arcana/craft/SKILL.md`
- Craft schema stack: `arcanum/arcana/craft/templates/ledger.schema.yml`

## Shared invariants

- canonical YAML remains exact and authoritative;
- no package install/build/addon load before provenance pass;
- no query before fresh YAML and complete generation verification;
- no active pointer, database-to-YAML path, receipt key family, or in-place
  recovery;
- every control uses explicit isolated paths;
- every failure emits zero rows and preserves a stable code;
- passing local evidence never implies promotion/publication/deployment.

Task Session must rehash live anchors and build a fresh task-local context pack.
This planning context is navigation, not runtime admission evidence.
