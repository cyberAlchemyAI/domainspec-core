# Bounded Invoke Context

## Intent

Define, design, and plan a trustworthy generic Inventory append runtime and a
faceted organization model for new Inventory entries.

The user approved Invoke authoring after accepting the research recommendation
to plan the non-atomic, fail-closed Candidate B boundary. This authoring
approval does not accept a runtime implementation or atomicity claim.

## Obligation Matrix

| ID | Obligation | Evidence | Resolution |
|---|---|---|---|
| O-01 | Make append outcomes attributable and reproducible. | `../2026-07-24-inventory-runtime-research/findings.md#recommended-minimal-runtime-candidate-b` | Candidate B receipt contract. |
| O-02 | Resolve installed helpers without upstream checkout or caller CWD. | research findings, runtime acceptance hold | Package-relative runtime manifest and unrelated-CWD fixture. |
| O-03 | Separate introduced warnings from inherited debt. | research findings, warning-delta section | Stable warning identities and set delta. |
| O-04 | Preserve non-authority and public/private boundaries. | Inventory skill authority rule; research findings | Generic public sources; consumer evidence stays private. |
| O-05 | Organize new entries without tag-derived directory explosion. | live `.arcanum/inventory/index.json`; 111 flat entry files observed on 2026-07-24 | Namespace-first physical path, logical concepts. |
| O-06 | Avoid disruptive legacy migration. | existing 213-entry live index and current append-only updater | Legacy paths remain valid; migration excluded. |
| O-07 | Preserve current canonical Inventory development ownership. | `arcanum/arcana/inventory/development/WORK-PACK.md` | Sigil Development integration gate before mutation. |
| O-08 | Produce executable medium-complexity SWUs. | Invoke Plan contract | Split work-pack, task specs, waves, receipts, closeout sync. |
| O-09 | Keep atomicity and currentness claims bounded. | research closeout and final audit | Non-atomic failure fields; currentness verifier excluded. |

Coverage: 9/9 obligations covered or explicitly deferred.

## Selected Sources

| Source | Selectors | Obligations |
|---|---|---|
| `ops/development/2026-07-24-inventory-runtime-research/findings.md` | answer; runtime acceptance hold; receipt schema; ownership; warning delta; non-atomic limits; validation gates | O-01, O-02, O-03, O-04, O-09 |
| `ops/development/2026-07-24-inventory-runtime-research/closeout.json` | parent approval; selected result; remaining decisions | O-01, O-09 |
| `arcanum/arcana/inventory/SKILL.md` | machine-index contract; authority rule; install/ingest/sync | O-04, O-05 |
| `arcanum/arcana/inventory/development/WORK-PACK.md` | control fields; selected `SWU-INT-001`; blockers | O-07 |
| `.arcanum/inventory/schema.md` | entry fields; machine index; update behavior | O-05, O-06 |
| `.arcanum/inventory/index.json` | live path/type/tag/status projections | O-05, O-06 |
| `.arcanum/inventory/tools/inventory-update.cjs` | canonicalization, ID no-op, sequential writes | O-01, O-03, O-06, O-09 |

## Excluded Context

- Archived whole-repository Inventory programs: not required for the bounded
  runtime and new-entry path policy.
- Ontology and Definitions authority: concepts here are retrieval facets only.
- BTE, financial settlement, and other consumer-specific content: useful
  examples but forbidden in a generic public Inventory runtime.
- Existing unrelated dirty Inventory projections: preserved as user state.

## Assumptions

- Distill budget defaults to Standard/Validate because the user did not select
  a different budget.
- Role simulation is used because governed subagent dispatch requires a
  separate confirmed strategy.
- Non-atomic apply is acceptable as an MVP planning boundary only when failure
  receipts expose partial mutation and no rollback or atomicity claim is made.

