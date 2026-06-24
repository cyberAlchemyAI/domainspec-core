# CyberAlchemy v2 Stable Repository Constitution

Status: candidate
Owner: constitution-governance
Authority level: project-local constitution
Selectors: `cyberAlchemy-v2/**`

## Scope

This constitution governs the structure and authority behavior of CyberAlchemy
v2 while it is staged inside `domainspec-core` and while it prepares for a
future standalone repository.

## Rules

### CAV2-C1. Source-Ledgered Consolidation

Validation mode: hybrid

Every durable synthesis must cite source paths or label claims as synthesis,
inference, or open question. Consolidation must preserve source role and
authority posture.

Examples:

- [../../SOURCE-MAP.md](../../SOURCE-MAP.md) lists cohorts, roles, and posture.
- A research finding cites upstream paths before proposing a v2 rule.

Non-examples:

- Copying a private source into v2 and treating the copy as canonical.
- Saying "the repo proves" without naming which source or evidence set.

### CAV2-C2. Authority Layer Separation

Validation mode: review

Definitions, constitutions, disciplines, decisions, specs, implementation,
inventory, ontology, observability, and ops must remain separate authority
layers.

Examples:

- Definitions live in [../definitions/DEFINITIONS.md](../definitions/DEFINITIONS.md).
- Constitution rules live in this file.

Non-examples:

- Letting an ontology candidate redefine a project term.
- Letting observability signals become design authority without review.

### CAV2-C3. Research Before Specification

Validation mode: review

Research may propose, compare, and synthesize. Specs and implementation must
wait for a promotion gate.

Examples:

- A research tower proposes a runtime contract and routes it to specs.
- A validation report supports but does not replace a promotion decision.

Non-examples:

- Moving a research hypothesis directly into implementation.

### CAV2-C4. Inventory And Ontology Non-Promotion

Validation mode: review

Inventory and ontology may reduce search and create candidate read models. They
cannot promote definitions, constitutions, glossaries, sigils, spells, runtime
contracts, or public claims by themselves.

Examples:

- Inventory cards feed a context pack for owner review.
- Ontology branch maps create promotion requests.

Non-examples:

- Treating `.arcanum/ontology-vault` as a final architecture decision.

### CAV2-C5. Public/Private Boundary

Validation mode: hybrid

Public derivatives must be scrubbed for private parent paths, private
implementation details, validation submodule specifics, sessions, telemetry,
and owner-only residue.

Examples:

- A public method page cites public Arcanum and rewritten, reviewed patterns.

Non-examples:

- Publishing private DomainSpec evidence as if it were public framework proof.

### CAV2-C6. Generated Projection Traceability

Validation mode: review

Generated skill, command, runtime, or host projections must trace to canonical
source before they influence contracts or capability definitions.

Examples:

- A `.agents/skills/` package cites its canonical `arcanum/arcana/**/SKILL.md`.

Non-examples:

- Editing generated projections as if they were canonical source.

### CAV2-C7. Navigable Work Surface

Validation mode: review

Each durable area must expose entrypoints, status, owner, role, source links,
and next route.

Examples:

- Area `README.md` files name the folder role and what does not belong there.

Non-examples:

- Dropping useful material into a folder without a local entrypoint.

### CAV2-C8. Open Questions As Residue

Validation mode: review

Informational artifacts should preserve unresolved questions in an `Open
Questions` section or link to the artifact that owns the unresolved questions.

Examples:

- A source map records whether visible `inventory/` and `ontology/` remain open.

Non-examples:

- Hiding unresolved public/private or promotion choices in confident prose.

### CAV2-C9. Validation Before Implementation

Validation mode: hybrid

Implementation work waits for a task-session, execution pack, or equivalent
approved route naming scope, evidence, validation, and rollback boundary.

Examples:

- A spec routes to a bounded task-session before code is written.

Non-examples:

- Starting runtime code from a research-only hypothesis.

### CAV2-C10. Standalone Extraction Gate

Validation mode: review

CyberAlchemy v2 may become a standalone repository only after authority model,
source spine, public/private boundary, validation surface, and extraction plan
pass owner review.

Examples:

- A decision record approves extraction and names what remains private.

Non-examples:

- Running `git init` inside the project as a substitute for a promotion decision.

### CAV2-C11. Import Before Promotion

Validation mode: hybrid

Scattered definitions, glossaries, constitutions, axioms, quality rules, and
anti-patterns must be staged in authority import ledgers before their contents
are promoted into CyberAlchemy v2 canonical definitions, constitutions, specs,
or implementation.

Examples:

- A glossary source is captured in
  [../imports/definitions/MANIFEST.md](../imports/definitions/MANIFEST.md)
  before its terms are promoted.
- A private DomainSpec constitution is captured in
  [../imports/constitutions/MANIFEST.md](../imports/constitutions/MANIFEST.md)
  before any public-safe derivative rule is drafted.
- The imported house_project vault stays under
  [../imports/house_project/](../imports/house_project/) while reusable value
  concepts are re-authored through
  [VAULT-CONCEPT-ADOPTION-CONSTITUTION.md](VAULT-CONCEPT-ADOPTION-CONSTITUTION.md).

Non-examples:

- Adding a term to the canonical definition file because it appeared in one
  source glossary.
- Copying a private constitution rule into CyberAlchemy v2 without source
  posture and boundary review.

### CAV2-C12. Entropy Register Declaration

Validation mode: hybrid

Any durable CyberAlchemy v2 artifact that uses entropy, entropic language,
entropy profiles, free energy, KL divergence, Gibbs/Boltzmann entropy,
retrieval entropy, or a similar quantitative information-loss claim to support
authority, ontology, routing, validation, or implementation must declare its
entropy register and typed residue source.

At minimum, the artifact must name:

- the entropy register or mathematical reading,
- the source operation or transformation,
- the typed residue being measured,
- the measure or observable used,
- the scope boundary such as finite, weighted, retrieval, probabilistic, or
  categorical,
- the claim status: theorem, conjecture, analogy, review evidence, or open
  question,
- the intended authority effect or non-governing residue treatment.

Examples:

- A definition citing finite Boltzmann entropy states that it is using
  `log |fiber|` as the finite microcanonical readout of `Residue_FF(Macro)`.
- An ontology review using retrieval entropy states that the entropy value is
  evidence for classification uniqueness, not proof that a node type is
  canonical.
- A research artifact discussing Gibbs entropy marks the claim as a weighted
  bridge or open research route unless a promoted weighted proof exists.

Non-examples:

- Saying "entropy increased" without naming which residue and which register
  were measured.
- Treating retrieval entropy, Boltzmann entropy, Gibbs entropy, and KL
  divergence as interchangeable because they all use entropy language.
- Letting a speculative entropy analogy promote a definition, constitution,
  ontology node, or implementation task without a promotion gate.

### CAV2-C13. Value-Cycle Edge Guard

Validation mode: hybrid

Any CyberAlchemy v2 relation, edge type, ontology movement, schema link, or
authority transition that can constrain a value, label, authority state, schema
field, or validation outcome must be acyclic unless schema governance records a
contextuality-obstruction review and an explicit exception.

Before a value-constraining cyclic edge can influence authority, ontology,
validation, or implementation, the review must name:

- the edge endpoints and direction or symmetry,
- the constrained value, label, state, field, or validation outcome,
- why a cycle is required,
- the satisfiability or obstruction risk,
- the validator, fixture, formal witness, or review witness,
- the owner route and typed residue if enforcement is incomplete.

Examples:

- `derives-from`-like authority or value constraints remain acyclic.
- `contextualizes`-like cyclic relations remain value-free unless separately
  reviewed.
- A future negotiated relation that both forces a label and cycles is blocked
  until the obstruction review exists.

Non-examples:

- Adding a cyclic relation and relying on prose to say it will not affect
  values.
- Treating a candidate ontology movement edge as safe because it is useful for
  navigation.
- Using a contextuality analogy as authority without naming the edge semantics
  that make the analogy live.

### CAV2-C14. Governed Artifact Tree Interface

Validation mode: hybrid

Any load-bearing artifact tree, architecture view, pattern library, ontology
view, validation tree, or view-bearing concept must expose a governance
interface before it can promote knowledge, constrain future work, or become a
reusable authority surface.

At minimum, the interface must name:

- owner route,
- canonical source or source boundary,
- view roles,
- evidence inputs,
- promotion path,
- validation surface,
- challenge contract,
- drift route,
- allowed uses and blocked uses.

A tree may organize search, inspection, reuse, and candidate promotion
preparation. It may not become authority by having a folder, branch view,
inventory row, concept card, architecture package, or projection. Authority
requires the relevant owner route and promotion gate.

Examples:

- An architecture-pattern-inventory package records concept cards, relationship
  cards, dependency rules, testing alignment, and observability alignment, then
  routes pattern candidates to the CyberAlchemy authority model before they
  constrain future work.
- A UX lesson can be stored as a pattern-shaped card while remaining local
  evidence until a second context, challenge review, and owner promotion exist.
- An ontology branch view declares allowed readings and forbidden authority
  moves before downstream agents use it as context.

Non-examples:

- Treating an architecture pattern card as an invariant because it appears in a
  pattern library.
- Treating a folder tree as canonical because it is well organized.
- Letting successful code reuse become architecture authority without evidence,
  challenge, and owner promotion.
- Creating a view for every new term without distinct evidence, lifecycle,
  owner route, and reuse surface.

### CAV2-C15. Interface Evidence Boundary

Validation mode: hybrid

Any UX/UI lesson, interface pattern, validator claim, screenshot review, studio
mutation intent, frontend validation report, or interface-governance artifact
must declare its evidence class before it can constrain downstream work,
promotion, validation, or implementation.

The evidence class must be one of:

- hard gate,
- soft flag,
- screenshot review,
- human study,
- not automatable.

Hard gates may govern only deterministic or standards-backed browser evidence
after fixture calibration. Cognitive, perception, trust, comprehension,
delight, market-practice, or subjective experience claims must remain soft
flags, screenshot review, human-study prompts, or residue unless a later owner
route records the calibrated evidence that makes a narrower claim admissible.

Examples:

- An unnamed critical button can be a hard gate when the role/name/state failure
  is directly observed and calibrated.
- A dense expert dashboard can receive a soft flag for decision density without
  blocking release until false-positive fixtures justify the threshold.
- A screenshot can route a salience concern to review, but it cannot prove where
  a user looked.
- A `ux-pattern` from one session stays seed evidence and cannot become a hard
  validator rule until cross-session evidence and owner promotion exist.

Non-examples:

- Publishing a single UX score as if it summarized accessibility, usability,
  delight, and market fit.
- Treating a passing Playwright run as proof of subjective product quality.
- Promoting an anecdotal UX lesson into a hard gate.
- Blocking a specialized expert interface with a generic density heuristic
  before false-positive calibration.

## Validation Adapters

| Rule | Adapter |
| --- | --- |
| CAV2-C1 | Markdown link check plus source-map review. |
| CAV2-C2 | Constitution-governance review. |
| CAV2-C3 | Promotion-policy review before spec or implementation mutation. |
| CAV2-C4 | Ontology-vault and inventory owner review. |
| CAV2-C5 | Public/private boundary scrub. |
| CAV2-C6 | Canonical-source trace review. |
| CAV2-C7 | Area README and navigation review. |
| CAV2-C8 | Open Questions section review. |
| CAV2-C9 | Task-session or execution-pack review. |
| CAV2-C10 | Decision-gate. |
| CAV2-C11 | Import manifest check plus owning governance route. |
| CAV2-C12 | Entropy-register keyword scan plus definitions-governance review. |
| CAV2-C13 | Edge proposal review plus schema amendment witness; future edge validator. |
| CAV2-C14 | Governed artifact tree interface checklist plus owner-route review; future architecture package validator. |
| CAV2-C15 | Interface evidence class checklist plus ux-evidence-validator review; future fixture-calibrated Playwright validator. |

## Promotion Boundary

This constitution is project-local. Promote it beyond CyberAlchemy v2 only after
evidence shows it works across at least one additional repository or public
Arcanum route.

## Split Triggers

Split this constitution if public/private policy, generated projection policy,
or implementation validation becomes large enough to require its own validator
or owner.

## Open Questions

### OQ-1. Which rules can become deterministic first?

Context: most rules are currently review or hybrid. Recommendation: start with
Markdown link checks and source-map field checks before writing broader
validators. Status: OPEN.
