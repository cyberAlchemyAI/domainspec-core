# Corpus: Vault Integration Review

Dispatch: `2026-06-18-cyberalchemy-vault-integration-review`
Status: review corpus, not canonical vault mutation

## Executive Reading

This review is about authority surfaces, not immediate schema installation.
DomainSpec already owns a governed vault grammar: node frontmatter, lifecycle
status, confidence semantics, edge catalogs, session provenance, and schema
amendment routes. CyberAlchemy contributes a rich method ontology for thinking,
review, promotion, witness records, and reflective operation, but those concepts
do not become DomainSpec vault fields by naming similarity alone.

The safe integration posture is to treat CyberAlchemy as method-local evidence
and review profile until DomainSpec admits specific schema, edge, node, and
authority changes through its existing governance path.

## Corpus Map

| Area | Source Surface | Integration Reading |
| --- | --- | --- |
| Vault human grammar | `implementation/domainspec/vault/ontology-conventions.md` | The vault already defines the required frontmatter shape: `node_type`, `layer`, `nature`, and `status`. CyberAlchemy should map into this grammar first. |
| Executable frontmatter | `implementation/domainspec/internal_tools/vault_common/frontmatter.py` | The executable owner is narrower than the conceptual ambition: 16 node types, 6 statuses, and a constrained edge-field set. New CyberAlchemy values require schema change, not prose-only adoption. |
| Status and confidence | `implementation/domainspec/vault/ontology-conventions.md` | Vault status, veracidade, conviccao, and applicability are governed axes. CyberAlchemy labels should remain method-local unless explicitly projected into these axes. |
| Sessions and provenance | Vault session/navigation surfaces | Sessions, telemetry, reflections, synthesis notes, and subagent outputs can seed candidates, but they do not become canonical authority without an owner promotion route. |
| Schema evolution | Vault schema-amendment discipline | New node types, statuses, edge fields, or control values need migration, validator updates, and owner acceptance. |
| Edge catalog split | `ontology-conventions.md`; `frontmatter.py` | The conceptual edge catalog and runtime field catalog are not identical. The 21/22 edge count split and `retrofits` inverse exception must be reconciled before method-specific edges are introduced. |
| Enforcement gap | `vault/discovery/documents-metadata-enforcement/documents-metadata-enforcement.md` | The vault has documented enforcement gaps: no linter, CI, pre-commit, or build-time validation for several metadata rules. Integration must not assume these checks already exist. |
| CyberAlchemy thick entries | `cyberAlchemy/agentic-system-ontology-entry-model.md` | Useful as a rich entry model and adapter seed, but not currently a DomainSpec vault schema. |
| Thinking-method ontology | `cyberAlchemy/research/2026-06-18-thinking-method-ontology/findings.md` | The prior run is a research finding and witness matrix direction, not a canonical DomainSpec mutation. |
| Promotion records | Arcanum ontology-vault and CyberAlchemy lifecycle materials | PromotionRecord-like records are useful as review/evidence companions, but cannot be treated as DomainSpec `node_type`, `status`, or frontmatter values until admitted. |
| Branch/evidence records | `projects/ontologize/development/view-triad-method/BRANCH-MATERIALIZATION.md` | B3/B4 records are run evidence and bridge ledger material, not DomainSpec vault node types. |
| Observed invocation | `arcanum/spells/observed-invocation-loop/README.md` | OIL result/evidence can inform provenance and review packets, not standalone vault authority. |
| Retrieval and session futures | Vault retrieval/session design surfaces | Retrieval and close-session surfaces are important, but should be treated as proposed or exploratory where not backed by current validators. |

## Integration Reading

- Target the current vault axes first: `node_type`, `layer`, `nature`, `status`,
  veracidade, conviccao, applicability, edge fields, and session provenance.
- Represent CyberAlchemy states as method-local fields such as `method_status`
  or `witness_status` before considering projection into vault-governed
  lifecycle status.
- Keep PromotionRecord, B3/B4, and OIL-style evidence as companion records or
  review records until a DomainSpec owner admits them through schema amendment.
- Block method-specific edges until the edge catalog is reconciled across
  human conventions, executable frontmatter, inverse rules, and validation.
- Use the current `layer` field for implementation alignment. Treat proposed
  axes such as `scope`, `domain`, `schema`, and `instance` as migration pressure,
  not current contract.
- Cap sessions, telemetry, synthesis, reflections, and subagent outputs at
  candidate/review authority unless promoted through the owner route.
- Require a validation path before any integration is described as enforceable:
  frontmatter checks, edge-name checks, graph checks, and cross-system fixtures.

## Corpus Boundary

This corpus extracts ontology-relevant material for review. It does not change
the DomainSpec vault, promote CyberAlchemy concepts into canonical schema, or
assert that proposed Arcanum ontology-vault records are already active in this
private vault.
