---
tags: [inventory, dispatch-spec, ontology-vault, lint, cartography, promotion-guardrail]
node_type: lint-report
is_session: false
layer: architecture
nature: validation
status: pass
created: 2026-06-18
dispatch_id: 2026-06-18-dispersed-knowledge-cartography
dispatch_type: research
working_folder: .arcanum/inventory/queries/2026-06-18-dispersed-knowledge-cartography/
sources: [.arcanum/inventory/queries/2026-06-18-dispersed-knowledge-cartography/DISPATCH.json, .arcanum/inventory/schema.md, .arcanum/inventory/tags.md]
---

# Lint Report - Dispersed Knowledge Cartography

## Checks

| Check | Result | Evidence |
| --- | --- | --- |
| Dispatch JSON parses | pass | `node -e JSON.parse(...)` |
| Dispatch Spec validation | pass | `python3 .agents/skills/dispatch-spec/scripts/validate-dispatch.py ... --json` returned `validation: pass`, no blocks, no flags. |
| Source immutability | pass | Route writes only under `.arcanum/inventory/` and `.arcanum/ontology-vault/`. |
| Promotion guardrail | pass | Route carries promotion split gates and ontology candidate status. |
| Frontmatter profile | pass | Schema documents YAML frontmatter profile. |
| Cartographer receipts | pass | Four read-only cartographers joined and closed; receipts filed in `cartographer-receipts.md`. |
| Evidence cards | pass | Candidate cards filed in `entries/evidence-cards/2026-06-18-dispersed-knowledge-cards.md`. |
| EvidenceSets | pass | Candidate sets filed in `entries/evidence-sets/2026-06-18-dispersed-knowledge-sets.md`. |
| Boundary skeptic | flag | Skeptic returned `block`; repairs filed in `boundary-skeptic-review.md` and residual status is `flag`. |
| Dispatch ledger close row | pass | Close row appended with `exit_reason: resolved` and `agents_spawned.total: 7`. |

## Current Gaps

- Evidence-cards and EvidenceSets are candidate read models, not promoted
  authority.
- Ontology map is still candidate-level; owner promotion is required before use
  as architecture authority.
- The v2 repository tree is a structure hypothesis, not an accepted design.

## Validation Result

pass
