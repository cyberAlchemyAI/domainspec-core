---
node_type: development-package
docType: glossary
module: architecture-pattern-enforcement
feature_code: APE
status: draft
updatedAt: 2026-07-12
---

# APE Glossary

Distilled definitions for the program's concepts. Candidate wording — the canonical homes are
`definitions/DEFINITIONS.md` (method terms) and `impl/spec/` (meta-types / edges); this glossary
routes to them, it does not replace them.

| Term | Meaning (candidate) | Canonical home / evidence |
| --- | --- | --- |
| **meta-type** | one of the current DomainSpec concept types — the node alphabet (Entity, Operation, Rule, …); 13 backend types are active and UI types remain separately staged | root DS-D1 definitions + `impl/spec/meta-types/` schemas |
| **edge / relationship verb** | a typed connection between two nodes (`enforces`, `produces`, `fetches`, …) — the edge alphabet | root DS-D8 authority in `definitions/relationships/relationships.yml`; R3A complete |
| **endpoint signature** | which node types a given edge may legally connect (from-type → to-type) | root DS-D8 authority; `validate-relationships.ts`; `validate-content.ts` |
| **uniformity** | the property that every instance of a meta-type has the same well-formed shape; checked as *schema conformance* | findings C-A; `validate-content.ts` |
| **composability** | the property that nodes connect only through legal edges with correct endpoint signatures | findings C-B; `validate-code-tags.ts` |
| **layering / adapter line** | the rule that decisions live in the domain, not adapters — inner layers never import outer | AXIOMS A2; DEPENDENCY-RULES.md; C6 |
| **concept card** | the human/agent-facing prose + code-example voice of one meta-type ("an Entity looks like …") | v1 `pattern-library/concepts/backend/*.md` |
| **relationship card** | the prose voice of one edge ("`enforces`: Rule→Operation, must pass before mutation") | v1 `ARCHITECTURE-PATTERN-LIBRARY.md` relationship cards |
| **content validator** | a tool that reads an aspect file / feature pack and checks each concept vs its criterion + each edge vs its signature | domainspec-v2-D10 (CANDIDATES.md #30) |
| **instance validator** | checks a machine-generated structured instance against its meta-type schema criterion | domainspec-v2-D12 (CANDIDATES.md #32) |
| **code tag** | an annotation (`domainspec.concept` / `domainspec.edges`) tying a line of code to a spec node/edge — the spec↔code thread | CODE-TAG-SCHEMA.md |
| **feature pack** | a real domain slice (SPEC + aspect docs + tagged code) — the *fuel* that makes validators non-vacuous | `impl/spec/features/financial-settlement/` is the first real witnessed pack; a second corpus remains open |
| **vacuous / witnessed** | *vacuous* = a validator that runs but has no real input to check; *witnessed* = has a runnable handle **and** real input | findings S2 (non-vacuity gate) |
| **pattern candidate** | an architecture mechanism that produces evidence but is not yet authority | cav2 CAV2-D43 pattern promotion lifecycle |
| **"has a tree ≠ has authority"** | the cav2 guardrail: a folder/card/passing-tool is evidence, never authorization | ARCHITECTURE-KNOWLEDGE-GOVERNANCE.md:26-33 |
| **promotion lifecycle** | candidate → exercised → evidence → owner promotion → binding (constitution/definition) | CAV2-D43; owner routing table |
| **substrate** | the project-independent set {meta-types, edge-law, validators, engine} a mint copies into a new repo | mint skill; SPEC.md APE.Substrate |
| **mint** | the act of standing up a new domain repo with the substrate baked in, so it authors its own governed spec | `mint` skill |
| **drift / convergence (C7)** | drift = spec↔code divergence measured over time; convergence = that drift trending down (never a single check) | DRIFT-CONVERGENCE.md; `compare-code-tag-drift.ts` |
| **R3 / R3A** | completed reformulation and root promotion of the relationship alphabet + endpoint signatures; no longer an edge-work blocker | root DS-D8 authority + R3A task-session receipt; dynamic code-tag consumption remains downstream work |
