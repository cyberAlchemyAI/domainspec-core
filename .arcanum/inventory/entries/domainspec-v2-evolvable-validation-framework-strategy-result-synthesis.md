---
id: domainspec-v2-evolvable-validation-framework-strategy-result-synthesis
kind: page
type: synthesis
title: DomainSpec v2 evolvable validation framework strategy result
updated: 2026-07-17
status: verified
confidence: high
tags:
  - inventory
  - strategy-result
  - dispatch
  - subagents
  - research
  - domainspec-v2
  - validation
  - formalization
  - graph
  - relationships
  - alloy
  - tla
  - claim-le-proof
  - non-authority
sources:
  - projects/domainspec-v2/research/evolvable-validation-framework/research.md
  - projects/domainspec-v2/research/evolvable-validation-framework/findings.md
  - telemetry/agents/subagents-dispatch.yaml
  - projects/domainspec-v2/impl/spec/minted-project/node.schema.json
  - projects/domainspec-v2/impl/tools/minted-project/compiler.ts
  - projects/domainspec-v2/definitions/meta-types/meta-types.yml
  - projects/domainspec-v2/definitions/minted-project/supported-profiles.yml
  - projects/domainspec-v2/definitions/relationships/relationships.yml
  - projects/domainspec-v2/development/meta-type-formalization/research/2026-07-02-formalism-and-primitives/findings.md
  - projects/domainspec-v2/research/alloy-tla-modeling/TOWER.md
selectors:
  - '#goal'
  - '#strict-authority-and-derivation-matrix'
  - '#obligation-routing-matrix'
  - '#verdict-matrix'
  - '#residue-and-next-gates'
evidence_card_ids: []
evidence_set_ids: []
residue:
  - no-end-to-end-TestCase-evaluator-typed-ReceiptEnvelope-witness
  - no-wired-cross-graph-FOL-Cedar-Datalog-evaluator
  - profile-admits-4-of-13-active-backend-kinds
  - current-30-vs-historical-29-relationship-read-model-drift
  - Saga-vs-Workflow-orchestrates-mismatch-remains-open
  - Alloy-TLA-models-and-extractor-contract-unvalidated
---

# DomainSpec v2 evolvable validation framework strategy result

The confirmed research dispatch `2026-07-17-domainspec-evolvable-validation-framework` closed with an auditor `ACCEPT`. The result is a candidate, non-authoritative layered framework: keep authored node/edge sources and registry/profile owners distinct; use schema/table-walk for node and edge shape; reserve FOL/Cedar/Datalog for cross-rule or cross-graph properties; reserve bounded Alloy for static graph counterexamples and TLA/TLC for temporal traces; preserve existing Lean ownership; and return typed, claim-limited receipts.

The repository already has a real structural substrate: an opaque minted-node envelope, profile/compiler admission hooks, typed relationship signatures, normalized graph and obligation IR, deterministic validators, generated test/residue surfaces, and digest-bound build receipts. The current profile is still experimental and admits four kinds while the registry lists thirteen active backend members. The historical twenty-nine-signature read model must not override the current thirty-signature relationship authority.

The dispatch used three explorers (Church structural kernel, Curry formal-query boundary, Gödel graph/relationship realization), a synthesis lane, three independent review gates (Tarski precedent, Popper non-vacuity, Quine definitional soundness), a writer, and Bourbaki auditor. Registration and close rows are recorded in `telemetry/agents/subagents-dispatch.yaml`; the dispatch ran one review loop and closed `resolved`.

## Accepted result

- Candidate framework objects are `KindDefinition` (an adapter descriptor separating registry/profile/formation references), `NodeSource`, `EdgeSource`, `Constraint`, `Obligation`, `TestCase`, and typed `ReceiptEnvelope` families.
- `NodeSource`, authored connections, registry/profile files, and relationship signatures remain canonical owners. Normalized graphs, generated tests/specs, receipts, and Inventory rows are derived/read-model evidence only.
- Structural obligations route to JSON Schema, `.schema.yml`, attribute-map, and deterministic table-walk validators. Cross-rule/cross-graph reachability, cycles, closure, and common-state relations are a separate Row-2 FOL/Cedar/Datalog candidate lane. SMT remains private and encoding-dependent; Alloy/TLA remain bounded promotion candidates; no universal solver or unbounded proof claim is allowed.
- A real relationship validator witness passes: `1 specs checked, edgesChecked=6, canonicalSignatures=30`. The key-and-door compiler witness is deterministic with four nodes, three edges, and seven provenance records. These prove the current structural path only.
- The hand-built `C2 -> C13 -> C4 -> C2` cycle is a design-target counterexample, not a shipped cross-graph evaluator result. A minimal end-to-end `TestCase -> evaluator -> typed ReceiptEnvelope` witness remains the next implementation gate.

## Owner and promotion boundary

Inventory is a verified read-model projection of the closed research result. It does not promote a DomainSpec kind, relationship, profile, compiler, formal evaluator, receipt, or release state. Any implementation of the next gates requires a separately authorized task/session and owner decision.
