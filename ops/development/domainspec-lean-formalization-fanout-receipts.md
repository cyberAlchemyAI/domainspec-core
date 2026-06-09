# DomainSpec Lean Formalization Fan-Out Receipts

Date: 2026-06-01
Dispatch: `domainspec-lean-formalization-research-20260601`
Target: `domainspec-lean-formalization`
Mode: read-only research execution

## Route

The approved dispatch was executed as a fan-out plus parent synthesis. The route used four delegated lanes and one parent synthesis lane:

- Lean corpus cartographer: completed.
- Research spine reader: completed.
- Bridge and relation mapper: closed after timeout; parent synthesis used local relation evidence already collected.
- Skeptical math auditor: completed.
- Operational synthesis editor: completed by parent lane.

No theorem/proof source was intentionally edited. A Lake build attempt changed `domainspec-lean-formalization/lean-formalization/files/lean-toolchain` during toolchain setup; that file was restored to the original `leanprover/lean4:v4.30.0-rc2`, and the subrepo diff for that path was empty afterward.

## Lane 1: Lean Corpus Cartographer

Status: completed
Agent: `019e82fb-a2fe-7f41-8650-49d806238b82`

Main findings:

- The project vocabulary uses "fractal" as an informal name for fully-faithfulness on specified adjunction slots, not as a new mathematical object: `domainspec-lean-formalization/README.md:29`, `domainspec-lean-formalization/lean-formalization/NAMING.md:14`.
- The corpus has three overlapping maps: root Lean development, `lean-formalization/files/new/` Mathlib staging, and prose/research folders.
- Front-door counts drift. `README.md:45` says 122 root files plus 29 `files/new` files; `README.md:96` says 23 PR-ready files; local count found 144 top-level root Lean files and 29 top-level `files/new/*.lean`.
- Counterexamples are load-bearing: `Bicyclic.lean:51`, `M6Counter.lean:145`, and `M2Counter.lean:51` support the idea that the repository discovers structure by failed preservation, not only by positive theorem accumulation.
- Tier-1 thermodynamics is finite/discrete/costed in its landed surface, not a full continuous physical theorem: `Tier1PrizeStatement.lean:36`, `Tier1PrizeStatement.lean:305`.
- `files/new/` is a separate Lake project, but default target status, declared library status, and PR-ready status are not the same category: `lean-formalization/files/new/lakefile.toml:1`, `lean-formalization/files/new/lakefile.toml:84`.

Parent use:

- Used to split "proof source", "build target", "sorry-free", and "PR-ready" into separate ledgers.
- Used to demote whole-repo sorry-free and PR-ready claims into scoped claims pending mechanical refresh.

## Lane 2: Research Spine Reader

Status: completed
Agent: `019e82fc-4d4a-7d60-b902-443572721bdd`

Main findings:

- The core thesis is a two-layer by three-axis residue program: translations have source/target layers, and failures split into vertical, horizontal, and diagonal axes: `research/README.md:12-15`, `research/README.md:31-35`.
- The central vertical result is that schema discipline does not force instance fidelity. M6 strong and M2 unrestricted are refuted; M2-restricted, M6', and M6-restricted remain open: `docs/domainspec-two-layer-framework.md:158-167`.
- The current publication surface is the two-layer residue paper in functorial data migration, with horizontal-axis material reserved for a companion paper: `docs/paper.md:15-25`, `docs/paper-companion.md:27-36`.
- `research-gpt` treats unresolved gaps as named residue and closes them through proof, paper, negative result, or promotion: `research-gpt/README.md:21-31`, `research-gpt/TOWER.md:41-50`.
- Noether and Lawvere language is deliberately demoted unless formal ingredients exist: `BACKLOG.md:81-99`, `docs/paper.md:295-326`, `docs/paper-companion.md:51-53`.
- Thermodynamics is bounded to finite/discrete supplied-chain results; continuous/RG/Landauer/Clausius claims remain open: `THERMODYNAMICS.md:46-70`, `THERMODYNAMICS.md:136-153`.

Parent use:

- Used to state the research direction as "typed residue accounting in translations" rather than broad metaphysics.
- Used to name the open formal frontier: M2-restricted, M6', M6-restricted, `(Delta, X)` Lan-unit faithfulness, Delta-parametric towers, system-of-towers, rung-2/rung-3 geometry, and residue compositionality.

## Lane 3: Bridge And Relation Mapper

Status: closed after timeout
Agent: `019e82fc-4ed0-7bd0-adb4-0ee3ddbfaa88`

Parent fallback evidence:

- `docs/spine-cyberalchemy-relation.md:14-23` frames the spine and CyberAlchemy as the same framework in formal/mathematical and operational/agentic registers.
- `docs/spine-cyberalchemy-relation.md:39-50` says each register lacks what the other provides, so the relation is productive but incomplete.
- `docs/reflection-tower-arcanum-isomorphism.md:15-28` proposes a three-register relation among Arcanum, reflection tower, and knowledge-taxonomy C7.
- `docs/reflection-tower-arcanum-isomorphism.md:102-113` explicitly flags judgment calls and open questions, so "isomorphism" language must be demoted unless formal equivalence is supplied.
- `cyberAlchemy/README.md:11-18` and `cyberAlchemy/README.md:80-110` present CyberAlchemy as the operational knowledge-system register.
- `cyberAlchemy/agentic-system-architecture.md:12-19` directly names residue between schema and data/evidence layers as design intent.
- `implementation/domainspec/DRIFT-CONVERGENCE.md:3-15` connects implementation drift/convergence to the broader DomainSpec program while keeping research-level normative semantics elsewhere.
- `research/projects/domainspec/README.md:1-17` and `research/projects/domainspec/definitions/DEFINITIONS.md:1-14` hold the empirical/normative evidence program and canonical definitions for DomainSpec.

Parent use:

- Used to build the relation ledger as a graded graph: formal source, research spine, implementation/evidence substrate, operational Arcanum/CyberAlchemy register, and downstream project examples.
- Because the delegated lane timed out, sibling-repository relations outside the root were not promoted beyond candidate status.

## Lane 4: Skeptical Math Auditor

Status: completed
Agent: `019e82fc-5196-79d2-bff2-e045c7d26b79`

Main findings:

- `CLAUDE.md:28` gives the audit rule: claim must be a subset of Lean proof or cited theorem. Several docs follow it locally, but root-level claims can outrun current source.
- `research/README.md:73` claims zero Lean sorry; this must be demoted. A strict read-only text scan found active `sorry` lines in 8 files.
- `README.md:96` says the Mathlib-PR-ready tree has 23 files and all are sorry-free; this must be demoted because declared analytic libraries under `files/new` contain active `sorry`s.
- `LEAN-ARCHITECTURE.md:305` correctly qualifies Tier-1 as typed finite witnesses/contracts, not a continuous physical prize closure.
- `docs/reflection-tower-arcanum-isomorphism.md:13` uses "same object" and "isomorphism" language, but `docs/reflection-tower-arcanum-isomorphism.md:105` flags the wording as too strong.
- Literature audits support "adjacent, not preempting" only as local audit verdicts, not as proof of absolute novelty: `SMITHE-2024-AUDIT.md:112`, `VLACHOPULOS-2026-AUDIT.md:104`.

Parent use:

- Used to produce the claim-discipline ledger.
- Used to separate theorem, documented audit, conjecture, analogy, refuted claim, and unsupported/overstated claim.

## Parent Synthesis Lane

Status: completed

The parent lane read the router/guardrails, front-door files, research spine, architecture/taxonomy docs, two-layer framework, paper status, backlog, thermodynamics notes, relation documents, and DomainSpec/CyberAlchemy/Arcanum relation surfaces.

The parent lane also ran local checks:

- Top-level root Lean file count: 144.
- Top-level `files/new/*.lean` count: 29.
- Strict active-sorry text scan: 30 active `sorry` lines in 8 files.
- Lake build attempts did not complete due toolchain/Mathlib fetch/ref-lock issues, not due a proof failure.

## Receipt Verdict

The strategy executed successfully enough to produce the requested research understanding and ledgers. The only partial lane was the relation mapper, which timed out; its scope was covered by parent local evidence for root-internal relations, but sibling-repository relation claims should be treated as a next pass rather than a closed result.
