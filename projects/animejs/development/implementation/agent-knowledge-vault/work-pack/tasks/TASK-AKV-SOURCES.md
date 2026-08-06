# TASK-AKV-SOURCES — Official source manifests

## Objective

Materialize comprehensive, digest-bound source inventories without mirroring
documentation prose or treating source presence as executed behavior.

## SWU-AKV-NV-004 — official documentation manifest

- Primary behavior: capture one structured row for every canonical official documentation route.
- Inputs: `https://animejs.com/documentation/` and `article#docs-info` pages.
- Algorithm: discover internal documentation links; canonicalize trailing slashes; fetch each route; extract title, H1, heading selectors, headings, family/topic kind, parameter/return/example/version-note dispositions, related route IDs, HTTP status, and raw digest; sort by canonical path; never store body prose.
- Write scope: `schemas/documentation-topic.schema.json`, `scripts/ingest-documentation.mjs`, `sources/documentation.jsonl`, `sources/documentation-manifest.json`.
- Edge cases: redirects, duplicate paths, missing article, route drift, partial fetch, unexpected content type, mutable snapshot drift.
- Done: all discovered routes have unique rows and zero failed fetches; the exact 418-row serialization reproduces semantic digest `681f004e04a91ab1a3462e882edff24d09454297f34a41863e81df06e20066fb` and raw page-set digest `63125e931350f5dbf8552a289ac80d687bb1867e7c94c1e2d6e33904f16befcd`. Those formerly returned-not-written identities are now materialized and validated; the approximate candidate serialization is superseded.
- Validation: `node projects/animejs/ontology/agent-knowledge-vault/scripts/ingest-documentation.mjs --check`.
- Split analysis: discovery and row extraction must close as one manifest transaction; pinned repository evidence is an independent context in 005.
- Execution owner: local fallback; network limited to the official Anime.js domain.

## SWU-AKV-NV-005 — pinned repository manifest

- Primary behavior: materialize the immutable v4.5.0 source/type/test/example inventory at commit `2c9cf8ea00329f6768c7d7902252ed977d75ce42`.
- Algorithm: read the immutable recursive Git tree; keep README, package metadata, source, declarations, tests, and examples; classify rows without inferring execution; sort by path; bind every row to the commit and blob identity.
- Write scope: `schemas/source-artifact.schema.json`, `scripts/ingest-repository.mjs`, `sources/repository.jsonl`, `sources/repository-manifest.json`.
- Edge cases: truncated tree, changed tag target, missing expected roots, duplicate paths, unsupported blobs, unmatched family ownership.
- Done: 348 unique pinned rows reproduce exact manifest digest `f4026dec178de523262aca34dcddc5e419681b3494f37f496d9da8553d3ebcc0`, counts 70/70/125/81/2, and the tree is not truncated. That formerly returned-not-written identity is now materialized and validated; the approximate candidate serialization is superseded.
- Validation: `node projects/animejs/ontology/agent-knowledge-vault/scripts/ingest-repository.mjs --check`.
- Split analysis: the immutable repository transaction is independent from the live documentation snapshot and must retain its own digest.
- Execution owner: local fallback; network limited to GitHub API/raw endpoints for the pinned commit.
