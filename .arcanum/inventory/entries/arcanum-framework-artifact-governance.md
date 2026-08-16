---
id: arcanum-framework-artifact-governance
kind: page
type: dependency-rule
title: Arcanum framework artifact governance
updated: 2026-08-06
status: verified
confidence: high
tags:
  - inventory
  - arcanum
  - artifact-governance
  - schema
  - promotion-guardrail
  - public-private-boundary
sources:
  - arcanum/framework/ARTIFACT-AUTHORING-MEMORY.md
  - arcanum/framework/ARTIFACT-CONSTITUTION.md
  - arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md
  - arcanum/framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md
  - arcanum/framework/GITIGNORE-CONSTITUTION.md
  - arcanum/framework/MARKDOWN-LINKING-CONSTITUTION.md
  - arcanum/framework/RECEIPT-ID-LEGEND-CONSTITUTION.md
  - arcanum/framework/SCHEMA-CONSTITUTION.md
selectors:
  - '#classes'
  - '#promotion-boundary-rules'
  - '#core-metadata'
  - '#recommended-edge-vocabulary'
  - '#process'
evidence_card_ids: []
evidence_set_ids: []
residue:
  - artifact-metadata-constitution-remains-candidate
  - gitignore-constitution-remains-candidate-and-review-only
  - receipt-id-cross-file-resolution-remains-incomplete
  - markdown-edge-vocabulary-adapter-remains-candidate
---

# Arcanum framework artifact governance

Arcanum separates source artifacts, deliberately promoted durable evidence, reproducible generated artifacts, and machine-local runtime state. Source is versioned by default; generated outputs are ignored unless explicitly promoted; local runtime state must not become versioned source or durable evidence.

Development evidence can change canonical source only through a promotion patch that names the target owner, selected durable claim, omitted material, validation surface, approval state, and required lookup synchronization. Passing validation is evidence for owner review, not authority by itself.

## Composed rules

- Canonical new machine-readable schemas use `.schema.yml`; existing non-YAML formats require scoped migration rather than silent replacement.
- Governed Markdown should resolve links, cite summarized sources, expose relationship direction, and mark non-authority projections.
- Artifact metadata proposes intent-driven constitution and validation selection, but its parser and adapter promotion gates remain open.
- Ignore rules should narrowly cover generated, local, cache, and secret material without hiding canonical source; that constitution remains candidate and review-only.
- Human-facing receipts gloss tracked IDs inline; cross-file definition resolution and bulk enforcement are not yet fully deterministic.

## Claim ceiling

The source documents have mixed lifecycle statuses. This entry preserves those statuses and dependencies; it does not flatten candidate rules into canonical ones or authorize a source mutation.
