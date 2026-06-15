---
module: keystone-lift
task: TASK-TPL-PORT
docType: work-pack-task
updatedAt: 2026-06-14
---

# TASK-TPL-PORT — Sanitize + place the DomainSpec SPEC+aspect templates in invoke

Layer: L0 · Wave: W0 · Complexity: medium · Gate: ready

## Objective
Bring the DomainSpec SPEC + aspect-doc templates into invoke's template directory as a new `domainspec-spec/` family, sanitized for public use — **without** yet making them the default (cutover is TASK-INVOKE-CUTOVER).

## Dependencies
None (W0 entry). Source: `implementation/domainspec/templates/{SPEC,operations,queries,interfaces,states,events,mappings,STORIES,domain,rules}.md`.

## Implementation Detail Spec
- **Inputs:** DS template files (SPEC.md + aspect docs).
- **Outputs:** `arcanum/spells/invoke/templates/domainspec-spec/` containing the sanitized templates + a short `README.md` describing the family.
- **Ordered rules:**
  1. Copy SPEC.md + each aspect doc into `domainspec-spec/`.
  2. Sanitize: remove DS-private paths, `ZefraHub`, Portuguese terms (`veracidade`/`convicção`), hardcoded DS registry/CI references; keep generic governance thresholds + Concept Registry structure.
  3. Re-point any internal links to arcanum-relative paths.
  4. Keep the Concept Registry table (it's the sync-registry interface for M2).
  5. Do not alter invoke's `define` baseline yet.
- **Edge cases:** a template references a DS-only artifact (e.g. governance-baseline) → drop that row/section or genericize; record in audit.
- **Validation:** templates render; `grep -iE 'ZefraHub|veracidade|convic|/home/.*domainspec'` over `domainspec-spec/` → 0; link-checker green.

## Smallest Working Units
- **SWU-KSL-003** — copy + sanitize + place templates (write scope: `arcanum/spells/invoke/templates/domainspec-spec/`). Owner: subagent. Verify: grep clean + render.

## Handoff Note
Work in arcanum only. Do not touch `module-formulae/` (removed later). Return SWU result shape.
