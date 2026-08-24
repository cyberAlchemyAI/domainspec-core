# TASK-AKV-GRAPH — Populated ontology and consultation views

## SWU-AKV-NV-006 — graph materialization

- Primary behavior: deterministically materialize typed nodes and stored relations from validated source manifests and closed contracts.
- Algorithm: create one DocumentationTopic and DocumentationObservation EvidenceRecord per documentation row; create pinned source EvidenceRecords and one exact VersionContext; create only defensible APISymbol/SourceFact nodes from pinned exports; add retained edges only when endpoint/evidence rules pass; preserve zero verified Lessons; canonicalize JSON and compute one graph digest.
- Write scope: `contracts/node-vocabulary.json`, `schemas/node.schema.json`, `nodes/nodes.json`, `relations/relations.json`, `scripts/build-graph.mjs`.
- Edge cases: unsupported family join, duplicate identity, missing source row, endpoint mismatch, cycles, stale context, inferred runtime behavior, unverified lesson.
- Done: every node validates, every edge resolves and is evidence-bound, complete source coverage is reported, and authority/release fields remain none/not-granted.
- Validation: `node projects/animejs/ontology/agent-knowledge-vault/scripts/build-graph.mjs --check`.
- Split analysis: graph identity and endpoint closure form one transaction; user-facing projections can be regenerated separately in 007.
- Execution owner: local fallback.

## SWU-AKV-NV-007 — consultation views

- Primary behavior: generate deterministic task-facing read models from one exact graph digest.
- Views: documentation coverage, API/source lookup, task recipes, work lessons, unresolved gaps, and stable search index.
- Write scope: `scripts/build-views.mjs`, `views/documentation-coverage.json`, `views/api.json`, `views/task-recipes.json`, `views/work-lessons.json`, `views/unresolved-gaps.json`, `indexes/search.json`.
- Done: every view binds graph digest and transform version; searches return source refs, conflicts, gaps, and abstention instead of inventing missing knowledge.
- Validation: `node projects/animejs/ontology/agent-knowledge-vault/scripts/build-views.mjs --check && node projects/animejs/ontology/agent-knowledge-vault/scripts/query.mjs coverage /documentation/animation/`.
- Split analysis: all views share one projection transform boundary and graph digest; graph construction itself remains independently accepted in 006.
- Execution owner: local fallback.
