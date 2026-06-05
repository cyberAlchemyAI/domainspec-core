# DomainSpec Lean Formalization Research Brief

Date: 2026-06-01
Dispatch: `domainspec-lean-formalization-research-20260601`
Status: executed, with one relation lane closed after timeout and covered by parent fallback evidence

## Executive Answer

`domainspec-lean-formalization` is a theorem-research atlas for typed residue accounting in translations.

Its central concern is not "fractal" as a new object. The repository uses "fractal" as informal project vocabulary for fully-faithfulness on specified adjunction slots: `README.md:29`, `lean-formalization/NAMING.md:14`. The stronger mathematical story is that translation systems have multiple layers of fidelity, and preserving schema-level structure does not automatically preserve instance-level information.

The cleanest bounded thesis is:

> DomainSpec Lean formalization studies where structure survives translation, where it leaks, and how those leaks can be typed, proved, refuted, named, and reused as research residue.

## What It Is About

The repository is about information preservation across compilation, translation, and migration-like processes.

Evidence:

- `CLAUDE.md:1-6` calls it an atlas of residue with Lean formalization, research bridges, conjectures, and audits.
- `README.md:19-31` frames the DomainSpec Theorem as a formal framework for information preservation in compilation and translation.
- `docs/domainspec-two-layer-framework.md:54-65` says residue is not metaphor: it is a two-layer distinction between categorical objects/types.
- `research/README.md:12-15` and `research/README.md:31-35` define the two-layer by three-axis residue program.

The basic research object is not one theorem, one proof file, or one product architecture. It is a disciplined corpus that asks:

1. Which translation properties preserve source structure?
2. Which properties fail to preserve target/instance information?
3. Which failures are generic, compositional, or axis-specific?
4. Which analogies to physics, operational systems, and reflective workflows are formally supported, and which are only explanatory?

## Methods

### 1. Categorical Formalization

The Lean corpus uses category theory, functors, adjunctions, Kan extensions, fully-faithful thresholds, units, counits, finite witnesses, and related Mathlib machinery.

Evidence:

- `LEAN-ARCHITECTURE.md:23-33` describes the repository as demonstration, counterexample hunt, and Mathlib PR pipeline.
- `LEAN-ARCHITECTURE.md:91-108` lays out five acts: foundations, infrastructure, bridges, witnesses/counterexamples, and capstone.
- `lean-formalization/files/new/LanAdjunctionFullyFaithful.lean:54` and related files stage categorical infrastructure.

### 2. Counterexample Discipline

Counterexamples are load-bearing results. They show exactly where attractive preservation claims fail.

Evidence:

- `lean-formalization/Bicyclic.lean:51` closes a faithful-but-leaky Lan-unit counterexample.
- `lean-formalization/M6Counter.lean:145` refutes strong M6.
- `lean-formalization/M2Counter.lean:51` refutes unrestricted M2.
- `docs/domainspec-two-layer-framework.md:158-167` summarizes M6 strong and M2 unrestricted refutations while leaving restricted variants open.

Interpretation: failures are not just obstacles. They are how the repo discovers typed residue.

### 3. Two-Layer By Three-Axis Research Frame

The research spine splits residue into:

- Vertical: schema/type versus instance/data.
- Horizontal: time/spec/system evolution.
- Diagonal: promotion/reflection/fixed-point-like persistence.

Evidence:

- `research/README.md:31-35` names the axes.
- `research/README.md:41-47` distinguishes proved product gadgets from still-conjectural native DomainSpec-system independence.
- `BACKLOG.md:81-99` demotes finite Lawvere fixed-point language and recasts diagonal as persistence.

### 4. Bridge Discipline

The repository maps to thermodynamics, physics, Arcanum, CyberAlchemy, and operational governance, but it uses a claim discipline: bridge claims must stay bounded.

Evidence:

- `THERMODYNAMICS.md:46-70` bounds the current theorem spine to finite/discrete/uniform-prior supplied-chain material.
- `THERMODYNAMICS.md:136-153` keeps beta-not-zero Gibbs, continuous time/RG, Landauer/Clausius, and strong asymptotic second-law claims open.
- `docs/paper.md:295-308` treats Noether language as a scope warning rather than a theorem.
- `docs/spine-cyberalchemy-relation.md:39-50` records what the mathematical and operational registers each lack.

### 5. Gap Promotion And Reflection

`research-gpt` and the tower materials make gaps first-class. A gap should become named, typed, blocked, and actionable, or else stay atmosphere.

Evidence:

- `research-gpt/README.md:21-31` describes observing `/research`, capturing residue, and promoting gaps into closure obligations.
- `research-gpt/TOWER.md:41-50` says named residue must be typed, blocked, and actionable.

### 6. Mathlib PR Staging

`files/new` is a real extraction/staging subsystem, but it should not be conflated with the whole repository.

Evidence:

- `LEAN-TYPES.md:66-100` organizes PR waves.
- `lean-formalization/files/new/README.md:10` frames Mathlib-style staging.
- `lean-formalization/files/new/CommuteExpSmul_PR.md:8` shows PR handoff material.

Current caution: `files/new` contains declared analytic libraries with active `sorry`s, and docs disagree about counts and readiness.

## Research Direction

The strongest current research direction is narrow and publishable:

- Lead with two-layer residue in functorial data migration.
- Keep horizontal-axis material in a companion.
- Use counterexamples to show that schema preservation and instance preservation are irreducible.
- Keep broader physics/Noether/Lawvere/Arcanum/CyberAlchemy language as scoped bridge material.

Evidence:

- `docs/paper.md:1-8` marks `paper.md` as current.
- `docs/paper.md:15-25` chooses the two-layer residue title and reserves horizontal-axis material for a companion.
- `docs/paper.md:30-33` still contains horizontal abstract language, which should be cleaned up or explained.
- `docs/paper.md:320-326` says M6 strong fails and the two budgets do not collapse.

Main formal frontier:

- M2-restricted.
- M6'.
- M6-restricted.
- Joint `(Delta, X)` characterization of Lan-unit faithfulness.
- Delta-parametric tower.
- System-of-towers.
- Rung-2/rung-3 geometry once enough higher-category infrastructure exists.
- Residue compositionality.

Evidence:

- `docs/domainspec-two-layer-framework.md:158-167`
- `BACKLOG.md:151-185`
- `BACKLOG.md:309-343`

## Main Insights

### Insight 1: There Are Two Budgets

Schema fidelity and instance fidelity are different budgets. One can be preserved while the other leaks.

This is the core DomainSpec Lean insight surfaced by the M2/M6 refutations and the two-layer framework.

### Insight 2: Residue Is Typed

Residue is not vague leftover information. It is classified by layer, axis, bridge status, and proof status.

### Insight 3: Counterexamples Are Productive

The corpus treats counterexamples as map-making. They identify boundaries where theorems should weaken, split, or become new conjectures.

### Insight 4: Bridges Need Status Labels

Physics, Noether, Lawvere, Arcanum, and CyberAlchemy language helps explain the program, but those bridges must be labeled as theorem, documented research, conjecture, analogy, or candidate relation.

### Insight 5: The Repo Is Self-Reflective But Not Self-Justifying

The reflection-tower and research-gpt surfaces make unresolved residue visible. That does not make every attractive self-relation true; it creates a governance route for deciding what can be promoted.

## Relations Inside The Root

### `research/projects/domainspec`

Role: empirical evidence and canonical definition register.

Evidence: `research/projects/domainspec/README.md:1-17`, `research/projects/domainspec/definitions/DEFINITIONS.md:1-14`.

Relation: complements the Lean theorem register. It owns empirical/normative DomainSpec definitions more directly than the Lean atlas.

### `implementation/domainspec`

Role: implementation/runtime fidelity register.

Evidence: `implementation/domainspec/DRIFT-CONVERGENCE.md:3-15`, `implementation/domainspec/DRIFT-CONVERGENCE.md:61-90`.

Relation: operationalizes related drift/convergence concerns. It should not inherit theorem status without an explicit bridge.

### `cyberAlchemy`

Role: operational/agentic knowledge-system register.

Evidence: `cyberAlchemy/README.md:11-18`, `cyberAlchemy/README.md:80-110`, `cyberAlchemy/agentic-system-architecture.md:12-19`.

Relation: aligns with residue reduction between intent, execution, and evidence. Treat as compatible operational presentation, not formal equivalence.

### `arcanum`

Role: lifecycle/orchestration/governed execution register.

Evidence: `docs/reflection-tower-arcanum-isomorphism.md:15-28`, `docs/reflection-tower-arcanum-isomorphism.md:48-66`, `docs/reflection-tower-arcanum-isomorphism.md:102-113`.

Relation: partial alignment with the reflection-tower pattern. The safe wording is "register", "bridge", or "presentation"; avoid literal "isomorphism".

### Downstream Project Snapshots And Sibling Repositories

Role: candidate downstream examples or adjacent applications.

Status: not closed by this execution. The delegated relation lane timed out, so this remains a next-route target.

## What To Demote Immediately

- Whole-repo "zero sorry" claims.
- Whole-tree "Mathlib PR-ready" claims.
- Count claims that disagree across `README`, `LEAN-ARCHITECTURE`, `LEAN-TYPES`, and local filesystem reality.
- Full continuous physical thermodynamics closure.
- Literal Arcanum/CyberAlchemy/spine isomorphism.
- Absolute novelty claims beyond dated literature-audit scope.

## Recommended Next Routes

1. Current-truth refresh.
   Update or regenerate count, build, sorry, axiom, default target, and PR-readiness status across `README`, `LEAN-ARCHITECTURE`, `LEAN-TYPES`, `LEAN-TAXONOMY`, and `files/new/README.md`.

2. Build environment repair.
   Fix Lake/Mathlib fetch/ref-lock issues, then run focused builds plus dependency-cone sorry and axiom audits.

3. Publication spine decision.
   Decide whether `paper.md` is the sole current spine, how `paper-v2`/`paper-v3` are treated, and how horizontal-axis companion material is separated.

4. Cross-repository relation map.
   Run a dedicated path-cited pass over root projects and sibling repos with labels for formal, documented, operational, analogy, candidate, and demoted relations.

5. Formal target selection.
   Choose one next theorem/research frontier: M2/M6' restricted claims, Delta-parametric tower, residue compositionality, or system-of-towers.

## Bottom Line

The repo is strongest when read as a disciplined theorem-research atlas: Lean proves and refutes local preservation claims; prose names the broader residue program; bridges translate the idea into operational and physical registers; governance artifacts prevent attractive analogies from being promoted too early.
