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
