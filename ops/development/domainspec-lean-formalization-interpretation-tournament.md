# DomainSpec Lean Formalization Interpretation Tournament

Date: 2026-06-01
Dispatch: `domainspec-lean-formalization-research-20260601`

## Purpose

This artifact runs the dialectic requested by the strategy: competing readings are tested against the evidence, then demoted or selected.

## Candidate A: Pure Theorem Repository

Claim: `domainspec-lean-formalization` is mainly a Lean theorem repository.

Evidence for:

- It contains a large Lean corpus and root default targets: `lean-formalization/files/lakefile.toml:1`.
- It has central theorem and counterexample files such as `DomainSpec.lean`, `Bicyclic.lean`, `M2Counter.lean`, `M6Counter.lean`, `ReflectionTower.lean`, and `SecondLawDiscrete.lean`.
- `LEAN-ARCHITECTURE.md:209-222` lists load-bearing types and direct consumers.

Evidence against:

- `CLAUDE.md:1-6` describes an atlas with Lean formalization, research bridges, conjectures, and audits.
- `README.md:114-128` includes docs, research, `research-gpt`, bridges, physics, and internal tools as part of the shape.
- The corpus has active `sorry`s in some areas and stale front-door proof-status claims.

Verdict: useful but too narrow.

## Candidate B: Pure Research Notebook

Claim: it is mainly a prose/math research notebook with Lean as support.

Evidence for:

- `research/README.md:12-15` and `research/README.md:31-35` define the two-layer by three-axis research spine.
- `docs/paper.md:15-25` and `docs/paper-companion.md:27-36` define publication surfaces.
- `BACKLOG.md:151-185` and `BACKLOG.md:309-343` identify open formal targets.

Evidence against:

- Core negative and positive claims are in Lean source, not only prose: `Bicyclic.lean:51`, `M2Counter.lean:51`, `M6Counter.lean:145`, `BridgeAdjunction.lean:21`.
- The repo has Mathlib PR staging and build architecture, not just notes: `LEAN-TYPES.md:66-100`, `lean-formalization/files/new/README.md:10`.

Verdict: useful but also too narrow.

## Candidate C: Mathlib PR Staging Repository

Claim: it is mainly a pipeline for extracting Mathlib-ready files.

Evidence for:

- `LEAN-TYPES.md:66-100` organizes PR waves.
- `lean-formalization/files/new/README.md:10` frames `files/new` as Mathlib-shaped staging.
- `lean-formalization/files/new/CommuteExpSmul_PR.md:8` shows PR handoff material.

Evidence against:

- The root project is much broader than `files/new`.
- `files/new` contains declared analytic work with active `sorry`s, so "PR-ready" cannot describe the whole subtree.
- The research spine, bridges, and theorem counterexamples are not reducible to Mathlib extraction.

Verdict: a real subsystem, not the main identity.

## Candidate D: Operational Bridge To Arcanum/CyberAlchemy

Claim: it is mainly an operational bridge into Arcanum and CyberAlchemy.

Evidence for:

- `docs/spine-cyberalchemy-relation.md:14-23` bridges the mathematical spine and CyberAlchemy.
- `docs/reflection-tower-arcanum-isomorphism.md:15-28` maps Arcanum, reflection tower, and C7.
- `cyberAlchemy/agentic-system-architecture.md:12-19` uses residue between schema and data/evidence layers as design intent.

Evidence against:

- The bridge docs qualify their own strength: `docs/spine-cyberalchemy-relation.md:39-50`, `docs/reflection-tower-arcanum-isomorphism.md:102-113`.
- The repository's primary proof/research identity is not operational execution.
- "Same object" and "isomorphism" language should be demoted unless formal equivalence is supplied.

Verdict: important relation surface, not the controlling identity.

## Candidate E: Theorem-Research Atlas For Typed Residue

Claim: it is a theorem-research atlas for typed residue accounting in translations.

Evidence for:

- `CLAUDE.md:1-6` calls it an atlas of residue.
- `README.md:19-31` frames the DomainSpec Theorem as information preservation in compilation and translation, with "fractal" as fully-faithfulness on adjunction slots.
- `LEAN-ARCHITECTURE.md:23-33` says the project is part demonstration, part counterexample hunt, and part Mathlib PR pipeline.
- `research/README.md:12-15` and `research/README.md:31-35` state the two-layer by three-axis residue thesis.
- `docs/domainspec-two-layer-framework.md:54-65` says residue is not metaphor but a typed two-object/two-layer issue.
- `docs/domainspec-two-layer-framework.md:158-167` records the central status: M6 strong and M2 unrestricted refuted; restricted variants open.
- `research-gpt/TOWER.md:41-50` turns unresolved gaps into named, typed, actionable residue.

Evidence against:

- Front-door status claims are stale and require mechanical refresh.
- Some bridge language is stronger than current evidence.
- Build validation could not be completed in this route.

Verdict: winner.

## Winning Reading

`domainspec-lean-formalization` is best understood as a theorem-research atlas for typed residue accounting in translations.

It combines:

- Lean proofs and counterexamples.
- Category-theoretic methods around functors, Kan extensions, adjunctions, fully-faithful thresholds, units, counits, and finite witnesses.
- A two-layer by three-axis research program.
- A bridge discipline for physics, operational systems, Arcanum, and CyberAlchemy.
- A Mathlib staging subsystem.
- A residue-governance practice where unresolved gaps are named, typed, and either proved, refuted, demoted, or promoted.

## Dialectic Results

What should become the headline:

- "typed residue accounting in translations"
- "schema fidelity does not automatically imply instance fidelity"
- "counterexamples are constructive map-makers"
- "bridge claims are valuable but must remain scoped"

What should be demoted:

- "all Lean is sorry-free"
- "the Mathlib staging tree is all PR-ready"
- "Tier-1 closes the full physical theorem"
- "Arcanum/CyberAlchemy are literally the same object as the formal spine"
- "Noether/Lawvere language is theorem-level in the current formalization"

What should drive the next research pass:

- Current-truth refresh of counts, sorry status, build status, PR status, and root docs.
- Build-environment repair and a dependency-cone proof-status audit.
- Publication-spine decision between `paper.md`, older paper drafts, and the horizontal companion.
- Dedicated cross-repository relation map with owner and authority boundaries.
- Formal target selection among M2/M6', Delta-parametric tower, residue composition, and system-of-towers.
