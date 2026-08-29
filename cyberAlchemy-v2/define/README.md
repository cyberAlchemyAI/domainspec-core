# CyberAlchemy v2 Define

Status: private candidate package. No authority effect.

In plain terms: this is a private proposal under review. These files grant no
permission to change, publish, execute, or deploy anything.

## Start with a real problem

A team wants to add refunds to an online shop. Before it starts, the team notices
that the word “customer” is unclear. It could mean the buyer, the account owner,
or the person who received the product.

The same problem can appear after work has started. A developer, designer, or
reviewer may discover that two parts of the project use “customer” differently.

Define handles this problem. It helps people and tools identify and clarify the
important terms, where they apply, who owns them, where current information came
from, and what is still unanswered. This can happen before work starts or while
it continues.

Example only: this refund scenario does not define “customer” or authorize
implementation.

## What Define records

Define keeps these concrete items together:

| Item | What it means |
| --- | --- |
| Goal | The specific result wanted, including its limits. |
| Intent | The original reason for the goal. |
| Context | Where the work applies: for example, one product, feature, domain, user group, or time period. |
| Concept | An important term or idea that the work depends on. |
| Source | The exact document, record, or system where information came from. |
| Evidence | Information used to support a statement or decision. |
| Owner | The person or role allowed to decide one exact matter. |
| Open question | Something important that is still unknown, unclear, or disputed. |

For every required concept, Define records one handling choice. The package calls
this choice a **disposition**:

- reuse: an existing owned definition fits this context;
- specialize: an existing definition fits after its context is narrowed;
- propose: a new candidate definition is needed; or
- open: the answer is not ready and the question remains visible.

## What Define produces

Define produces a checked bundle containing the goal, intent, context, concepts,
sources, evidence, owners, dispositions, and open questions. This bundle is
called a **Definition Pack**.

The named person, team, or tool that uses the pack is its **consumer**. The
consumer decides whether the pack is useful input for one stated use. The pack
does not choose the consumer's product, design, or technical solution.

## When Define is used

Define is not only an upfront stage.

- Before work starts, it can expose unclear concepts and missing context.
- While work continues, it can answer new questions or record them as open.
- After evidence or context changes, it can refresh an existing Definition Pack.

Define is also not mandatory before every design or implementation task. Use it
when unclear or unstable concepts would cause guessing, rework, or an ownership
conflict.

## Read the documents

1. [docs/DEFINE.md](docs/DEFINE.md) — the capability, its inputs, work, result,
   boundaries, and owners.
2. [docs/LIFECYCLE.md](docs/LIFECYCLE.md) — the states of the Define package and
   one Define session.
3. [docs/AUTHORITY.md](docs/AUTHORITY.md) — who may decide what and when a
   separate decision is required.
4. [docs/DEFINITION-PACK.md](docs/DEFINITION-PACK.md) — the output fields and
   checks.
5. [docs/INTERACTION.md](docs/INTERACTION.md) — how one saved session appears in
   the CLI and chat.

[documents.json](documents.json) records each document's ID, owner, intended
type, expected lifetime, authority state, required headings, and current blocker.

## Ontology packages

Define now separates product meaning, proposed runtime structure, and their
alignment:

- [business-ontology/](business-ontology/) owns the private
  `business-domain` ontology: 8 product-meaning nodes and 7 business
  relations;
- [system-ontology/](system-ontology/) owns the private `system-runtime`
  ontology: 36 DomainSpec-typed nodes and 72 source-owned relations; and
- this parent package owns only the `business-system-bridge`: one bridge node,
  eight cross-package relations, and explicit evidence gaps.

Each child has its own profile, sources, schema bindings, validator, and
append-only receipt history. The parent excludes child material bytes from its
own digest while validating each declared child identity, current receipt, and
cross-package endpoint.

## Document status

These files are intended to be long-lived and kept up to date. CyberAlchemy calls
that **perennial**.

They are still **canonical-document candidates**. They are not admitted canonical
artifacts and they grant no decision rights.

Candidate does not mean unsupported. It means the material has not crossed the
separate owner-controlled promotion step.

CAV2-D51 says a canonical artifact must have:

1. a recognized artifact type; and
2. an owner-approved process that produced it.

The current type table does not approve a creation process for this exact Define
document set. Putting files in this folder cannot approve them.

## Evidence already used

This package is built from prior CyberAlchemy, Arcanum, and DomainSpec work. It
is not a definition written without evidence.

The current package records 22 exact sources. They include:

- 10 active CAV2 definitions for ontology, method, definition, authority,
  claim-to-proof limits, intent, promotion, canonical artifacts, durability,
  and schema;
- the CAV2 product thesis, product ontology, authority model, source rules, and
  package model;
- the existing Arcanum Define contract, overview, stage catalog, and Invoke
  ontology; and
- the DomainSpec v2 Define CLI experiment, including its profile, nodes, and
  relations.

The package validator checks that those exact sources and selected text
locations still exist and that their recorded bytes have not changed.
Historical PASS receipts remain immutable history; they do not cover the
refactored bridge bytes or clear current source drift.

Together, this evidence supports the need for Define, its concepts, its method,
its authority limits, its output structure, and its relationship to existing
mechanics. It does not yet establish measured outcomes from people using the
finished CyberAlchemy Define product.

## Source order

If two files disagree, use this order and record the disagreement:

1. cyberAlchemy-v2/authority/definitions/DEFINITIONS.md owns formally accepted
   CyberAlchemy v2 terms.
2. [definitions.json](definitions.json) holds the three Define definition
   candidates. It does not allocate canonical CAV2-D* IDs.
3. [business-ontology/](business-ontology/) owns product meaning,
   [system-ontology/](system-ontology/) owns the proposed runtime, and
   [profile.json](profile.json), [nodes.json](nodes.json),
   [relations.json](relations.json), [views.json](views.json), and
   [migration/invoke.json](migration/invoke.json) hold their bridge and package
   lifecycle model.
4. The files under docs/ explain that model for people.
5. This README introduces and links the package.

A human-readable document cannot silently change a machine record. A changed
definition, relationship, owner, status, or permission limit must also change
the machine-readable source that owns it.

## Product and migration boundary

CyberAlchemy v2 owns this proposal for what Define should do and why.

Arcanum Invoke provides implemented mechanics and public evidence that may be
reused. The DomainSpec v2 experiment provides a candidate CLI and system model.
Neither source owns CyberAlchemy's product meaning.

[migration/invoke.json](migration/invoke.json) records a possible future change:
CyberAlchemy v2 may become the main home for Define while Invoke is kept as an
adapter or retired. This package does not change, deprecate, or remove any public
Arcanum file.

## Validate

From the repository root:

    python3 cyberAlchemy-v2/define/scripts/validate.py

The validator checks the parent file boundary, child identities and current
receipts, document headings, exact source versions, definition links,
cross-package relationships, open-gap references, permission limits, and
historical parent receipt integrity.

## Claim ceiling

A PASS would say the parent bridge and both declared children are internally
coherent and still match their recorded sources. The current parent result is
BLOCK because five pre-existing exact source bindings have drifted. Child PASS
or FLAG results do not clear that blocker. No result here makes the documents
canonical, promotes a definition, proves the interactive runtime, removes
Invoke, publishes, releases, deploys, or establishes measured product outcomes.
