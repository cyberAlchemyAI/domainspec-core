---
tags: [inventory, cyberalchemy-v2, scientific-authority-lifecycle, knowledge-promotion, operational-evidence, pattern-authority, ontology-lifecycle, relation-provenance, promotion-guardrail]
node_type: synthesis
is_session: false
layer: architecture
nature: reference
status: candidate
created: 2026-06-23
sources: [cyberAlchemy-v2/authority/definitions/DEFINITIONS.md, cyberAlchemy-v2/development/research/2026-06-23-governed-artifact-primitive-formalization/findings.md, projects/ontologize/DAG-AND-METRICS.md, cyberAlchemy-v2/ontology/README.md, cyberAlchemy-v2/ontology/BRANCH-AS-VIEW.md, cyberAlchemy-v2/ontology/PACKAGE-MODEL.md, .arcanum/inventory/entries/evidence-sets/2026-06-23-governed-artifact-primitive-formalization-sets.md]
---

# Scientific Authority Lifecycle Synthesis

This is a candidate Inventory synthesis, not a canonical definition. It records
the reusable thesis:

> CyberAlchemy promotes knowledge by running the scientific method over
> operational evidence, then routing surviving candidates through ontology
> views, inventory evidence, owner decisions, and authority governance until
> some candidates become reusable patterns, invariants, or constitutions.

## Candidate Name

**Canonical-track term (reconciled per review CR-2, 2026-06-23):
`authority promotion lifecycle`** (= candidate `CAV2-CAND-LIFECYCLE-001`). The
names below are **aliases** of that one term, not separate terms:

- `scientific authority lifecycle` — this synthesis's lookup / framing name (the scientific-method reading).
- `pattern authority lifecycle` — narrower, architecture-facing; **alias only** (adjacent to `CAV2-D43 pattern promotion lifecycle`, so never canonical).

## Boundary

Scope (per review CR-6): only the **promotion segment**
(`PromotionCandidate -> ArchitecturePatternAuthority`) is the binding-rule scope;
the upstream evidence / event / metric portion is descriptive input, not
authority-bearing. The binding rule itself is the closed kind-enumeration
(`CAV2-CAND-LIFECYCLE-002`), not "everything."

This synthesis does not promote a new primitive. It composes existing sources:

- `CAV2-D41` authority model says evidence, ontology, research, generated
  projections, implementation success, and repetition must not silently become
  authority.
- `CAV2-D43` pattern promotion lifecycle says operational/code/spec hypotheses
  can become pattern authority only after evidence, generalization,
  cross-context exercise, challenge, and owner promotion.
- Ontologize's DAG supplies the operational evidence chain.
- The governed-artifact research blocks the shortcut from artifact/view/tree to
  primitive authority.

## Provenance Spine

| Provenance | Source refs | Role in the synthesis |
| --- | --- | --- |
| Authority model | `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md:2604-2630`, `:2650-2664` | Gives the non-collapse law and owner-routed authority movement. |
| Governed artifact tree | `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md:2683-2701`, `:2715-2747` | Allows load-bearing trees as inspectable governance interfaces, not primitive authority. |
| Pattern promotion lifecycle | `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md:2766-2802`, `:2806-2829` | Defines the route from operational/code/spec hypothesis to pattern authority and possible invariant/constitution pressure. |
| View-bearing concept | `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md:2848-2872`, `:2888-2900` | Names when a concept deserves its own governed view without letting the view decide authority. |
| Operational DAG | `projects/ontologize/DAG-AND-METRICS.md:20-23`, `:43-48`, `:154-167`, `:228-251` | Supplies the evidence-production loop: event, metric, candidate, owner decision, projection, feedback. |
| Ontology boundary | `cyberAlchemy-v2/ontology/README.md:12-31`, `cyberAlchemy-v2/ontology/PACKAGE-MODEL.md:50-82` | Ontology models, relates, projects, and stages; owner routes decide. |
| Branch/view boundary | `cyberAlchemy-v2/ontology/BRANCH-AS-VIEW.md:8-24`, `:36-47` | Branch views ask better questions but cannot answer authority questions without owner gates. |
| Governed-artifact no-primitive review | `cyberAlchemy-v2/development/research/2026-06-23-governed-artifact-primitive-formalization/findings.md:12-21`, `:45-61`, `:113-124` | Blocks primitive inflation and preserves candidate-only handoffs. |
| Inventory read-model boundary | `.arcanum/inventory/entries/evidence-sets/2026-06-23-governed-artifact-primitive-formalization-sets.md:17-19`, `:31-55` | Keeps this synthesis searchable while non-authoritative. |

## Relation Map

```text
OperationalEvidence
  derives_from -> OutcomeEvent
  observed_by -> MetricObservation
  may_signal -> PromotionCandidate

PromotionCandidate
  traced_to -> InventoryEvidenceSet
  viewed_by -> OntologyView
  blocked_by -> ChallengeContract | Contradiction | OwnerGate
  decided_by -> OwnerDecision

OwnerDecision
  may_promote_to -> KnowledgeProjection
  may_reject_to -> Residue
  may_retire_to -> History
  may_contradict_to -> ResidueWithPath

KnowledgeProjection
  feeds -> OntologyCards | RoutingRules | AgentGates | ClassificationRegisters
  may_generalize_to -> PatternCandidate

PatternCandidate
  must_be_exercised_in -> SecondContext
  must_survive -> ChallengeReview
  may_promote_to -> ArchitecturePatternAuthority

ArchitecturePatternAuthority
  may_create_pressure_for -> Invariant | Constitution | Discipline | Validator
```

## Relation Semantics

| Relation | Meaning | Guardrail |
| --- | --- | --- |
| `derives_from` | A claim or candidate cites operational/source evidence. | Source refs required; no source means reject or mark low confidence. |
| `observed_by` | A source-backed event feeds a metric observation. | Metric must declare denominator and evidence refs. |
| `may_signal` | A metric or event can raise a candidate. | Signal does not promote. |
| `traced_to` | Candidate links to inventory EvidenceCards/EvidenceSets. | Inventory is read model only. |
| `viewed_by` | Candidate is placed in ontology/view surface. | View is not authority. |
| `blocked_by` | Challenge, contradiction, gate, or unresolved residue prevents movement. | Open contradiction blocks promotion. |
| `decided_by` | Owner route makes explicit approve/reject/retire/contradict decision. | Authority movement needs owner decision. |
| `may_promote_to` | Owner-approved candidate can become projection, pattern authority, invariant, or constitution pressure. | Claim strength cannot exceed evidence set. |
| `feeds` | Promoted knowledge changes future routing/scoring/gates. | Feedback must remain traceable to the approved projection. |
| `may_generalize_to` | Repeated successful local evidence may become a generalized pattern candidate. | Cross-context exercise is required before authority. |

## Scientific Method Reading

| Scientific method role | CyberAlchemy role |
| --- | --- |
| Hypothesis | code/spec/workflow/design claim |
| Experiment | domain execution or operational run |
| Observation | OutcomeEvent, MetricObservation, trace, residue |
| Falsification | contradiction path, challenge contract, negative control |
| Replication | second context / cross-context exercise |
| Theory | promoted architecture pattern authority |
| Law-like pressure | invariant, constitution, discipline, or validator after owner review |

## Downstream Use

Use this synthesis when a future task asks how CyberAlchemy connects:

- operations and knowledge governance;
- Ontologize DAG and authority movement;
- inventory evidence and ontology views;
- pattern candidates and architecture pattern authority;
- owner decisions and invariant/constitution pressure.

Do not use it as a canonical definition. If this becomes load-bearing, route the
term `scientific authority lifecycle` or `pattern authority lifecycle` through
definitions-governance and constitution-governance.

## Open Residue

- No schema for `scientific authority lifecycle` exists.
- No validator checks `pattern_candidate -> architecture_pattern_authority`.
- Saturn and DomainSpec bridge claims remain outside this EvidenceSet unless a
  later review adds source-backed cards for those systems.
- The base term `artifact` remains a definitions-governance review candidate.
