---
module: keystone-lift
task: TASK-PROSE-RECOMPOSE
docType: work-pack-task
updatedAt: 2026-06-14
---

# TASK-PROSE-RECOMPOSE — Recompose TAXONOMY/RELATIONSHIPS prose as the example layer

Layer: L2 · Wave: W2 · Complexity: low · Gate: ready-after S-001

## Objective
Make the lifted `TAXONOMY.md`/`RELATIONSHIPS.md` prose the human-facing **example/explanatory layer** that points at the canonical DS-D1/DS-D2 IDs (decision C1) — not a second source of truth.

## Dependencies
S-001 (canonical IDs exist in arcanum).

## Implementation Detail Spec
- **Inputs:** lifted prose TAXONOMY.md/RELATIONSHIPS.md (in arcanum); canonical DS-D1/D2 entries.
- **Outputs:** edited arcanum prose files with every concept/edge linking to its canonical ID.
- **Ordered rules:**
  1. For each type/edge in the prose, add a link to the canonical `DEFINITIONS.md#DS-D*` anchor.
  2. Strip any normative-sounding language that competes with the canonical entry; keep examples, intuition, templates.
  3. Sanitize residual DS-private strings.
- **Validation:** link-checker resolves every ID anchor; no duplicated normative statements (review).

## Smallest Working Units
- **SWU-KSL-007** — rewrite prose as example layer with ID links (write scope: `arcanum/definitions/{TAXONOMY,RELATIONSHIPS}.md`). Owner: subagent. Verify: link-checker.

## Handoff Note
Arcanum-only edit; runs alongside TASK-DEFS-REF-PRIVATE in W2.
