# DomainSpec Lean Formalization Relation Ledger

Date: 2026-06-01
Dispatch: `domainspec-lean-formalization-research-20260601`

## Relation Principle

Relations are graded. A path citation can establish a documented relation, but it does not automatically promote that relation into a theorem, ontology edge, product dependency, or canonical ownership rule.

Use these labels:

- `formal`: relation is represented in Lean theorem/proof structure or typed framework source.
- `documented`: relation is stated in repository prose or audit material.
- `operational`: relation appears as a workflow, architecture, governance, or implementation alignment.
- `analogy`: relation helps explain but is not formal equivalence.
- `candidate`: relation is plausible but needs owner review or deeper evidence.
- `demoted`: relation wording exists but should not be used literally.

## Core Self-Relation

`domainspec-lean-formalization` relates to itself as an atlas, not a single theorem file.

Evidence:

- `domainspec-lean-formalization/CLAUDE.md:1-6` calls the repo an atlas of residue, with Lean formalization, research bridges, conjectures, and audits.
- `domainspec-lean-formalization/README.md:19-31` frames the DomainSpec Theorem and defines the informal "fractal" vocabulary as fully-faithfulness on specified adjunction slots.
- `domainspec-lean-formalization/LEAN-ARCHITECTURE.md:23-33` says the repository is part demonstration, part counterexample hunt, and part Mathlib PR pipeline.
- `domainspec-lean-formalization/README.md:114-128` lays out the materialized reflection-tower organization: Lean source, `files/new`, internal tools, docs, research, `research-gpt`, bridges, and physics.

Relation label: `documented` plus `formal` where individual Lean files prove local claims.

Synthesis: the repository is best read as a theorem-research atlas for typed residue accounting in translations.

## Relation To DomainSpec Implementation

Evidence:

- `implementation/domainspec/DRIFT-CONVERGENCE.md:3-15` places drift/convergence at the implementation level while keeping research-level normative semantics in `research/projects/domainspec`.
- `implementation/domainspec/DRIFT-CONVERGENCE.md:18-41` defines drift and convergence operationally.
- `implementation/domainspec/DRIFT-CONVERGENCE.md:61-90` maps build-time and runtime fidelity.
- `implementation/domainspec/DRIFT-CONVERGENCE.md:150-166` summarizes control docs and the implementation-level one-sentence thesis.

Relation label: `operational`.

Reading: `implementation/domainspec` is the implementation/runtime register for related fidelity and drift concerns. It is not the Lean proof authority, but it is a natural downstream surface for applying the residue vocabulary to systems.

Boundary: do not import Lean theorem status into implementation claims without a bridge artifact. Do not mutate implementation docs from this research route.

## Relation To DomainSpec Research Project

Evidence:

- `research/projects/domainspec/README.md:1-17` describes the DomainSpec evidence program.
- `research/projects/domainspec/README.md:18-33` gives a status snapshot and weighted completeness.
- `research/projects/domainspec/README.md:61-69` lists missing experiments.
- `research/projects/domainspec/README.md:71-83` summarizes claim coverage.
- `research/projects/domainspec/definitions/DEFINITIONS.md:1-14` marks canonical definitions authority.
- `research/projects/domainspec/definitions/DEFINITIONS.md:28-50` and `research/projects/domainspec/definitions/DEFINITIONS.md:54-80` define contribution-level and meta-type-system terms.

Relation label: `documented` and `operational`.

Reading: the research project is the empirical and definitional evidence register for DomainSpec. The Lean formalization is a mathematical/proof register. They should cross-reference, but neither should silently overwrite the other's authority.

Boundary: canonical definitions belong to the definitions governance surface, not to this one-off research brief.

## Relation To CyberAlchemy

Evidence:

- `cyberAlchemy/README.md:11-18` says CyberAlchemy gathers product, method, and agentic-system knowledge around preserving alignment between intent, execution, and evidence.
- `cyberAlchemy/README.md:32-50` centers intent, execution, evidence, name drift, route correction, provenance, and knowledge improvement.
- `cyberAlchemy/README.md:80-110` lists stack concepts including structured intent, Arcanum, Inventory, Ontology, knowledge governance, bridge/residue, memory, context builder, execution, observability, and reflection.
- `cyberAlchemy/agentic-system-architecture.md:12-19` says the design intent is to reduce residue between schema layer and data/evidence layer.
- `cyberAlchemy/agentic-system-architecture.md:23-31` names symmetry pursuit, residue reduction, candidate-before-canon, evidence/commitment split, local-first operation, and bounded action.

Relation label: `operational` plus `analogy`.

Reading: CyberAlchemy is the agentic/operational register of the same family of concerns: translation, drift, residue, evidence, and promotion. The relation is useful and documented, but it is not a formal theorem-level equivalence.

Boundary: use "operational register" or "compatible presentation"; avoid "same object" unless a formal equivalence is supplied.

## Relation To Arcanum

Evidence:

- `domainspec-lean-formalization/docs/reflection-tower-arcanum-isomorphism.md:15-28` proposes a relation among Arcanum anchors, the reflection tower, and the C7 knowledge taxonomy.
- `domainspec-lean-formalization/docs/reflection-tower-arcanum-isomorphism.md:36-44` gives a side-by-side table.
- `domainspec-lean-formalization/docs/reflection-tower-arcanum-isomorphism.md:48-66` maps the Arcanum 13-step loop, with 7 clean, 5 partial, and 1 no-counterpart step.
- `domainspec-lean-formalization/docs/reflection-tower-arcanum-isomorphism.md:70-86` records what each instance lacks.
- `domainspec-lean-formalization/docs/reflection-tower-arcanum-isomorphism.md:102-113` lists judgment calls and open questions.

Relation label: `documented`, `operational`, and `analogy`; "isomorphism" wording is `demoted`.

Reading: Arcanum is the capability-lifecycle and governed-execution register. It can use the reflection-tower/residue vocabulary as a design lens, but the current evidence supports partial alignment rather than formal identity.

Boundary: DomainSpec remains semantic governance and traceability substrate; Arcanum remains lifecycle authority for sigils, spells, invoke, spellcraft, and task-session.

## Relation To The Mathematical Spine And CyberAlchemy Bridge

Evidence:

- `domainspec-lean-formalization/docs/spine-cyberalchemy-relation.md:14-23` says the mathematical spine and CyberAlchemy are the same framework in formal/mathematical and operational/agentic registers.
- `domainspec-lean-formalization/docs/spine-cyberalchemy-relation.md:27-37` provides the correspondence table.
- `domainspec-lean-formalization/docs/spine-cyberalchemy-relation.md:39-50` lists what each side has and lacks.
- `domainspec-lean-formalization/docs/spine-cyberalchemy-relation.md:52-62` interprets the relation for readers and users.

Relation label: `documented` and `analogy`; literal sameness is `demoted`.

Reading: this bridge is valuable as a translation artifact. It should stay in "same pattern/register" language unless proof obligations are introduced.

## Relation To Project Snapshots

Evidence currently in scope:

- The strategy targeted other repositories and projects inside the root, but the delegated relation lane timed out.
- Local memory and path inspection indicate project snapshots exist under the root, but this execution did not complete a path-cited deep map of every project.

Relation label: `candidate`.

Reading: project snapshots such as product or applied-domain folders are likely downstream examples or testing surfaces for DomainSpec/Arcanum methods, but this route should not promote them as authoritative relations.

Next action: run a dedicated relation-map pass over root project directories with the same claim discipline and produce a graph with owner, evidence, dependency type, and promotion risk.

## Relation Verdict

The strongest root-internal relation map is:

1. `domainspec-lean-formalization`: mathematical/proof and research-atlas register.
2. `research/projects/domainspec`: empirical evidence and canonical definition register.
3. `implementation/domainspec`: implementation/runtime fidelity register.
4. `cyberAlchemy`: operational/agentic knowledge-system register.
5. `arcanum`: lifecycle/orchestration/governed execution register.
6. Project snapshots and sibling roots: candidate downstream or adjacent examples requiring a separate relation pass.

The safe language is "register", "bridge", "translation", "candidate alignment", and "documented analogy". The unsafe language is "same object", "formal isomorphism", or "theorem-level equivalence" unless a formal artifact supplies it.
