---
id: arcanum-framework-source-map
kind: page
type: source
title: Arcanum framework source map
updated: 2026-08-06
status: verified
confidence: high
tags:
  - inventory
  - arcanum
  - arcanum-runtime
  - public-private-boundary
  - claim-le-proof
sources:
  - arcanum/framework/README.md
  - arcanum/framework/ANTI-PATTERNS.md
  - arcanum/framework/ARTIFACT-AUTHORING-MEMORY.md
  - arcanum/framework/ARTIFACT-CONSTITUTION.md
  - arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md
  - arcanum/framework/CYBERALCHEMY-METHOD.md
  - arcanum/framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md
  - arcanum/framework/EXPERIMENT-HARNESS-STANDARD.md
  - arcanum/framework/GITIGNORE-CONSTITUTION.md
  - arcanum/framework/MARKDOWN-LINKING-CONSTITUTION.md
  - arcanum/framework/QUALITY-BAR.md
  - arcanum/framework/RECEIPT-ID-LEGEND-CONSTITUTION.md
  - arcanum/framework/SCHEMA-CONSTITUTION.md
  - arcanum/framework/SIGIL-DEVELOPMENT-WORKFLOW.md
  - arcanum/framework/VALIDATION-EXPERIMENT-PROTOCOL.md
  - arcanum/framework/observability/ARCHITECTURE-OVERVIEW.md
  - arcanum/framework/observability/HOOK-OPERATIONS-LEDGER.md
  - arcanum/framework/observability/OBSERVED-RUNS.md
  - arcanum/framework/observability/README.md
  - arcanum/framework/observability/REPOSITORY-PACKAGE.md
  - arcanum/framework/observability/SIGIL-OBSERVABILITY-HOOK.md
  - arcanum/framework/runtime/README.md
  - arcanum/framework/runtime/adapters/codex-exec.md
  - arcanum/framework/runtime/adapters/local-skill.md
selectors:
  - '#framework-documents'
  - '#local-runtime'
  - '#registry-boundary'
evidence_card_ids: []
evidence_set_ids: []
residue:
  - development-packets-not-current-framework-authority
  - scripts-and-templates-require-their-own-behavior-validation
  - source-file-statuses-vary-and-are-not-promoted-by-inventory
---

# Arcanum framework source map

This entry is a non-authoritative Inventory map of `arcanum/framework`. The framework defines how Arcanum capabilities are authored, validated, composed, observed, and maintained. It is distinct from the registry, which lists reusable sigils and spells, and from the consuming repository's `.arcanum/` runtime data.

## Observed source cohorts

The 2026-08-06 ingest observed 88 files:

| Cohort | Files | Inventory treatment |
| --- | ---: | --- |
| Primary framework, observability, and runtime documents | 24 | Read and indexed as the semantic source cohort. |
| Templates | 9 | Discoverable support assets; not treated as execution evidence. |
| Observability scripts | 17 | Implementation surfaces; not treated as validated behavior by this ingest. |
| Development, fixture, and refinement-run material | 38 | Candidate or historical evidence; excluded from current framework authority. |

The sorted primary path-set digest was `e8fc57ba451f371b7a4f605818f6e8a78594f1ac5b82381edfd4beecedb113f6`. Across all 88 tracked files, the path-list digest was `08b0f7818e335388edc7e71a82e89da4ee98e476ca41e9015e1267ba99571636`, the Git-index source-set digest was `9a35ede29eff32dab0266b8cdeff2cb4cf5afd591f0155055a45ca12cf401d1c`, and the observed working-tree path-plus-content digest was `7f580d3be143ab41f898fbdf2995cc920c0f3f69f880747b2385434352cbd87b`. These digests identify the ingest snapshot; they do not prove runtime behavior, publication, or currentness after that snapshot.

## Boundary

The source remains owned by public Arcanum. This parent Inventory is a private repository-local lookup projection. It may summarize and point to framework sources, but it cannot redefine them, promote candidate constitutions, validate scripts by inspection, or turn development evidence into canonical rules.
