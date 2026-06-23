# CyberAlchemy v2 Definition Drift Audit

Status: active
Owner: definitions-governance
Last updated: 2026-06-22

## Audit Scope

This first audit covered the starter artifacts created for CyberAlchemy v2:

- [../../README.md](../../README.md)
- [../../SOURCE-MAP.md](../../SOURCE-MAP.md)
- [../README.md](../README.md)
- [../boundaries.md](../boundaries.md)
- [../promotion-policy.md](../promotion-policy.md)
- [../constitutions/STABLE-REPOSITORY-CONSTITUTION.md](../constitutions/STABLE-REPOSITORY-CONSTITUTION.md)
- [../../disciplines/DISCIPLINES.md](../../disciplines/DISCIPLINES.md)
- [../../disciplines/cards/stable-repository-stewardship.md](../../disciplines/cards/stable-repository-stewardship.md)
- [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md)
- [DEFINITIONS-INDEX.md](DEFINITIONS-INDEX.md)
- [../../CRAFT.md](../../CRAFT.md)
- [../../.craft/ledger.yml](../../.craft/ledger.yml)
- [../../ontology/README.md](../../ontology/README.md)
- [../../development/research/2026-06-21-ontology-package-consolidation-model/findings.md](../../development/research/2026-06-21-ontology-package-consolidation-model/findings.md)

## Findings

| Finding | Status | Remediation |
| --- | --- | --- |
| Starter artifacts use `stable repository`, `source-ledgered amalgamation`, `authority layer`, `source spine`, `promotion gate`, and `stable repository stewardship` consistently with [DEFINITIONS.md](DEFINITIONS.md). | pass | None. |
| Existing upstream CyberAlchemy terms are referenced but not yet promoted into this project definition source. | flag | Later audit should review `AgenticSystem`, `ContextSolution`, and `TranslationResidue`; `OperationalOntology` is already demoted into D19/D23 language. |
| Arcanum-wide `contract` and `schema` semantics are not redefined locally. | pass | Continue linking to Arcanum definitions when needed. |
| Authority imports were missing from the first project skeleton. | fixed | Added `CAV2-D7`, `CAV2-D8`, and import manifests under [../imports/](../imports/README.md). |
| Canonical local definitions lacked explicit domain-context voices under the current definitions-governance contract. | fixed | Added domain-context voice sections for `CAV2-D1` through `CAV2-D8`. |
| Top-anchor tower terms were candidate-only in the Craft and tower surfaces. | fixed | Promoted `CAV2-D9` through `CAV2-D15` in [DEFINITIONS.md](DEFINITIONS.md) and synced [DEFINITIONS-INDEX.md](DEFINITIONS-INDEX.md). |
| [DEFINITION-TOWERS.md](DEFINITION-TOWERS.md) now references the promoted Q1 anchors rather than treating them as candidate-only. | pass | Continue using the tower map for clustering remaining imports. |
| Non-orthogonal dependencies were implicit in source material under orthogonality, typed edges, provenance, and coupling language. | fixed | Promoted `CAV2-D16` typed coupling invariant and synced [DEFINITIONS-INDEX.md](DEFINITIONS-INDEX.md). |
| Reflection tower appeared across Craft, framework-unification, and DomainSpec evidence as both structure and method, with risk of conflating it with ontology or capability towers. | fixed | Promoted `CAV2-D17` reflection tower method with an explicit residue-escalation boundary and synced [DEFINITIONS-INDEX.md](DEFINITIONS-INDEX.md). |
| Direct formalization evidence in `domainspec-formalization` and `domainspec-lean-formalization` sharpens `CAV2-D17` beyond the earlier Craft-only wording. | fixed | Updated [DEFINITIONS.md](DEFINITIONS.md) with the `Carrier(mu_n)` promotion hook and omega/fixed-point caution; synced [source-clusters/primordial.md](source-clusters/primordial.md). |
| Residue had multiple source meanings across DomainSpec formalization, Lean residue files, Craft, and reflection-tower material. | fixed | Promoted `CAV2-D18` as the local umbrella primitive while preserving subtype boundaries for `ResidueObject`, `ResidueStructure`, `ResidueCat`, `Carrier(mu_n)`, and imported `TranslationResidue`. |
| Entropy evidence appeared across Lean residue objects, finite Boltzmann FF-residue bridges, entropy profiles, retrieval-entropy classification evidence, and thermodynamics research notes, creating risk that bare entropy would be promoted as an overloaded primitive. | fixed | Promoted `CAV2-D27` residue entropy as a primitive observable under typed residue, and added constitution rule `CAV2-C12` requiring entropy-register and residue-source declarations before entropy claims can govern authority. |
| The TO-VLAD AX-ONT review showed that Shannon-style label independence and Lean Hilbert/projector orthogonality are different objects, while preserving a useful edge-layer tripwire. | fixed | Clarified `CAV2-D22` as classification/admission discipline, promoted `CAV2-D28` value-cycle edge guard, and added constitution rule `CAV2-C13` for value-constraining cyclic edge proposals. |
| Ontology was overloaded across inventory, ontology-vault, CyberAlchemy operational ontology, branch-aware business/system/bridge maps, framework-unification ontology-view, and Ontologize branch language. | fixed | Promoted `CAV2-D19` as the local governed meaning layer while demoting `Operational Ontology` to source-local shorthand for an operation-facing D19 projection governed by D23 lifecycle axes. |
| Craft method was defined operationally in Arcanum Craft and supported by `CRAFT-FORMAL-FOUNDATIONS.md`, but CyberAlchemy v2 only had a Craft execution surface definition. | fixed | Promoted `CAV2-D20` Craft method while keeping `CAV2-D12` as the surface and preserving the formal-foundations honesty boundary. |
| Four-facet action obligations were first framed too narrowly as promotion-readiness, while the operator intent was a basic CyberAlchemy action primitive. | fixed | Promoted `CAV2-D21` four-facet action method and preserved the correction that each governed action must bind, create, or residue classification/taxonomy, schema, human-continuation view, and machine-checkable view. |
| The imported house_project vault surfaced reusable value concepts, but they were still only Inventory read models and source-local vocabulary. | fixed | Promoted `CAV2-D22` through `CAV2-D26` for orthogonal classification, authority lifecycle axis, provenance-first navigation, schema amendment witness, and append-only event ledger; preserved source-local vocabulary in [source-clusters/house-project-vault.md](source-clusters/house-project-vault.md). |
| Ledger is emerging as a cross-method primitive candidate, but overlaps `authority import`, `Craft execution surface`, ontology, and signal ledgers. | flag | Added [reviews/ledger-primitive-review.md](reviews/ledger-primitive-review.md); `CAV2-D30` resolves the recursivity-name blocker, but canonical ledger promotion remains deferred until relation inheritance and local Craft ledger conformance are resolved. |
| Schema and relationship invariant evidence is spread across Arcanum definitions, DomainSpec edge catalogs, framework-unification invariants, and formalization sources. | flag | Added [../../../.arcanum/inventory/queries/2026-06-21-schema-relationship-invariants/search-sequence.md](../../../.arcanum/inventory/queries/2026-06-21-schema-relationship-invariants/search-sequence.md); keep `schema` as Arcanum authority and route `relationship invariant` through inventory evidence before promotion. |
| Repository objective was implicit in narrative discussion: CyberAlchemy v2 should become the downloadable CyberAlchemy base, while `ontology/` fixes authority shape as a candidate/projection package. | fixed | Updated [DEFINITIONS.md](DEFINITIONS.md) for `CAV2-D1`, `CAV2-D9`, and `CAV2-D19`; synced [DEFINITIONS-INDEX.md](DEFINITIONS-INDEX.md), [../../README.md](../../README.md), and [../../ontology/README.md](../../ontology/README.md). |
| Operational Ontology's relation to `CAV2-D19`, `CAV2-D22`, and `CAV2-D23` was unresolved after the authority lifecycle review. Identity collapse into D23 failed, but the term still lacked a D22-tested unique distinction. | fixed | Accepted the demotion decision: `Operational Ontology` is not a primitive, peer ontology branch, standalone subtype, separate candidate term, or D23 alias. Normalize it into D19 typed ontology obligations plus D23 lifecycle-axis obligations; name any remaining agent-operation obligation directly. |
| Broad orthogonality was ambiguous across primordial axis independence, D22 orthogonal classification, D16 non-orthogonal coupling, D23 lifecycle axis separation, and Lean/Hilbert projector orthogonality. | fixed | Promoted `CAV2-D29` axis orthogonality invariant as the broad governance invariant. `CAV2-D22` remains the classification specialization; Hilbert/projector orthogonality remains excluded from CAV2 authority unless separately typed. |
| `Recursivity` was witnessed but too vague to promote as an unbounded label. It overlapped ordinary recursion, generic self-hosting, `CAV2-D17` reflection tower method, and `CAV2-D20` Craft method. | fixed | Promoted `CAV2-D30` bounded recursive self-application. `recursivity` is now only an alias for the bounded meaning with artifact, altitude, owner, gate, residue/state, recomposition, and stopping conditions. |
| `Primitive type`, generic `method`, and `definition` were T-1 candidate terms but still lived as queue language rather than canonical CyberAlchemy v2 semantics. | fixed | Promoted `CAV2-D31` primitive type, `CAV2-D32` method, and `CAV2-D33` definition. The promotion keeps local CAV2 primitive roles separate from programming types, DomainSpec meta-types, Arcanum schema/contract terms, concrete methods, and non-authority glossary or inventory records. |
| `Authority`, `provenance`, `traceability`, `gate`, `claim <= proof`, and `intent` were still T-1 queue terms even though they govern how CyberAlchemy v2 makes work count, carries receipts, navigates links, moves through checkpoints, bounds claims, and preserves work purpose. | fixed | Promoted `CAV2-D34` authority, `CAV2-D35` provenance, `CAV2-D36` traceability, `CAV2-D37` gate, `CAV2-D38` claim <= proof, and `CAV2-D39` intent. `artifact` remains the only explicit T-1 review candidate. |
| Challenge/contradiction handling existed as House-vault challenge response, `contradicts`, `validates`, confidence axes, and v2 promotion residue, but the v2 node shape had no single field for how a node may be contested. | fixed | Promoted `CAV2-D40` challenge contract and added `challenge_contract` to the candidate ontology node/package shape while preserving `veracidade` and `convicção` as the existing confidence axes rather than adding a third confidence dimension. |

## Undefined Critical Terms

| Term | Source pressure | Route |
| --- | --- | --- |
| Agentic System | Prior CyberAlchemy definition material. | definitions-governance after project shape review. |
| Context Solution | Prior CyberAlchemy retrieval concept. | definitions-governance after storage route is selected. |
| Translation Residue | CyberAlchemy and framework-unification material. | definitions-governance plus residuality-spec review; classify as subtype, alias, or separate term relative to `CAV2-D18`. |
| Ledger | Craft recursive ledger, authority import ledgers, framework-unification signal ledgers, and v2 tower execution material. | Defer promotion; `CAV2-D30` resolves the recursivity-name blocker, but ledger still requires inheritance-relation and local Craft ledger conformance review. |
| Relationship Invariant | DomainSpec typed relationship system, `CAV2-D16`, framework-unification graph invariants, and sigma-valid edge formalization. | Use the inventory [schema/relationship search sequence](../../../.arcanum/inventory/queries/2026-06-21-schema-relationship-invariants/search-sequence.md); classify as subtype of `CAV2-D16`, alias, or separate primitive after evidence-cards exist. |

## Imported Definition Candidate Count

| Ledger | Candidates | Auxiliary sources | Status |
| --- | --- | --- | --- |
| [../imports/definitions/MANIFEST.md](../imports/definitions/MANIFEST.md) | 149 | 28 | candidate import only |

## Open Questions

### OQ-1. Should prior CyberAlchemy glossary terms be imported or referenced?

Context: the import ledger now stages the broad corpus. Recommendation: classify
and deduplicate the imported terms before promoting any large batch into this
canonical file. The Q1 top-anchor terms are already promoted. Status: OPEN.
