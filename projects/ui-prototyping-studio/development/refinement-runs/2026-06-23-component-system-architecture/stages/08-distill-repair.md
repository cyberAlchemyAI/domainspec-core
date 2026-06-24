# Stage 08 — Distill Repair

- Capability: `distill` · Mode: `validate` (repair) · Status: **pass**

## Repairs

- **RP-1 (closes DR1) — repo-scoped index.** `UIIdentityIndex` aggregates over **all session event logs in the repo**, keyed by `UIElementIdentity`, so cross-session recognition and `BaselineGenealogyFamily` lineages resolve. Still derived/regenerable, still not canonical — scope is repo, not session.
- **RP-2 (closes DR2) — anti-canonical guard.** The cache file is stamped `derived; regenerable; do not edit`, ships with a `rebuild` path, and any drift is resolved by trusting the events. The index is never a write target.
- **RP-3 (closes DR3) — provenance note even un-vendored.** The resonant namespace→enum mapping records source repo + commit + retrieval date in the DNA-fill note (mirrors `VENDORED-LICENSES.md`), so the `external_context` boundary (A3) is auditable without vendoring.

## Validated architecture (post-repair)

`UIIdentityIndex` = repo-scoped, derived, regenerable read-model over the append-only event logs → owned 24-enum canonical DNA (resonant names fill R-7 dims, external_context, attributed) → `DiffSummary` conformance → components page as a projection. Phase-1 `data-od-id` matching ships; DNA-similarity + vendoring deferred.

## repair-frame → s09
