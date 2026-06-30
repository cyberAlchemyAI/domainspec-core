---
run_id: 20260629T0700Z-inventory-js-updater
target: a deterministic simple inventory updater (JavaScript) for .arcanum/inventory/
preset: compact
research_mode: no-research
owner: refine
---

# Refine Seed — deterministic inventory updater (JS)

## Target
A small, dependency-free Node.js tool that **deterministically** appends one inventory record
(entry / evidence-card-bundle / evidence-set-bundle) to `.arcanum/inventory/index.json`, updating
**all** index maps consistently, so the LLM never hand-edits the machine index again.

## Source context (Context Builder baseline)
- The schema: `.arcanum/inventory/index.json` — top keys `{schema_version, inventory_root, generated_at,
  human_index, entries[], indexes{by_id,by_type,by_tag,by_source,by_status,by_evidence_card,by_evidence_set},
  projections, validation}`; `by_id` value = path **string**; the machine-index contract in the inventory SKILL.
- The motivating drift (this session's residue): index.json was hand-edited via ad-hoc Python ~6× this session;
  a **`by_evidence_set` keying inconsistency** was introduced (new entry keyed by set-id; existing 13 keyed by
  bundle-entry-id). A deterministic updater removes both the drift and the inconsistency.
- `tags.md` = the controlled tag vocabulary (for validation); `index.md` = the human catalog (row per entry).

## Write scope (the design fork — resolved in Design)
Recommended **(b)**: own `index.json` (core) **+** append the matching `index.md` table row. Leave `log.md`
prose to the human (judgment text, not mechanical). Smallest viable owner of the mechanical surface.

## Done criteria
A non-executed **build plan + design** with: the determinism contract, the input record contract, the
index-map update rules (one normalized `by_evidence_set` convention), the `index.md` row sync, the validation
checks, and a **falsification test** (byte-identical + idempotent). NOT the built code (that is task-session).

## Validation surface
The toy_game test: same record applied to a fixture index.json → byte-identical output; applied twice → no-op
(idempotent); a known record → expected map deltas.

## Preset / research
`compact` (the user asked for "simple"); `no-research` (schema is local + owned).
