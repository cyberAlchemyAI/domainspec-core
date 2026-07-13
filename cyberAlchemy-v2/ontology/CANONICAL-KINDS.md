# Canonical Kinds

Status: candidate
Owner: CyberAlchemy v2 ontology route (term authority: definitions-governance)
Governed term: [canonical artifact — CAV2-D51](../authority/definitions/DEFINITIONS.md#cav2-d51-canonical-artifact)
Durability axis: [CAV2-D52](../authority/definitions/DEFINITIONS.md#cav2-d52-artifact-durability)

## Purpose

Canonical kinds are the **fine artifact-types** the project recognizes: the
specific typed things a governed process produces (a discovery, a research, a
ledger, a spec). An artifact instantiating one of these is a `CAV2-D51` **canonical
artifact** — typed and process-born, and *decoupled from authority*. An artifact
whose kind is not enumerated here is **non-canonical**: free working material.

This is a **Tier-1** enumeration. It is *finer than* and *rolls up into* the
coarse **Tier-2** [AUTHORITY-MODEL Authority Kinds](../authority/AUTHORITY-MODEL.md#authority-kinds)
(`CAV2-D49`): several canonical kinds (discovery, research, ledger, session) share
one `authority_kind` (`Evidence`). Membership here does **not** grant authority —
authority is earned per `CAV2-D48`, and only kinds whose `authority_kind` is an
authority-bearing kind can earn it at all.

## Kind Contract

| Field | Meaning |
| --- | --- |
| `canonical_kind` | The specific canonical-kind (local identifier). |
| `process` | The governed process whose output is this kind. |
| `authority_kind` | The Tier-2 authority-kind it rolls up to (`CAV2-D49`); typed coupling `CAV2-D16`. |
| `durability` | `CAV2-D52` default: `ephemeral` or `perennial` (overridable per instance with an owner note). |
| `contradictions` | Derived from durability: `tolerated` (ephemeral) or `resolve-required` (perennial). |
| `authority_reachable` | Whether an instance can *ever* become authority (true only if `authority_kind` is authority-bearing). |

## Enumeration (seed — candidate)

This seed carries only the kinds named or clearly implied in the 2026-07-07 design
session. **It is not closed yet**: adding a canonical-kind is owner-gated (route:
ontology route to propose, definitions-governance/decision-gate if it changes term
semantics or the coarse enumeration). Durability defaults marked `(review)` are
candidate assignments awaiting owner ratification.

| Canonical kind | Process | Authority kind (`CAV2-D49`) | Durability | Contradictions | Authority-reachable |
| --- | --- | --- | --- | --- | --- |
| discovery | scope/discovery run | Evidence | ephemeral | tolerated | no |
| research | research dispatch / research-tower | Evidence | ephemeral | tolerated | no |
| session | session record (`sessions/`) | Evidence | ephemeral | tolerated | no |
| ledger | append-only ledger (`CAV2-D26`) | Evidence | perennial | resolve-required (live); temporal supersession allowed | no |
| axiom | axiom authoring | unresolved — OQ-2 *(provisionally governs as `Definition`; term = [`CAV2-D53`](../authority/definitions/DEFINITIONS.md#cav2-d53-axiom), whose boundary holds axiom ≠ definition)* | perennial | resolve-required | deferred (OQ-2) |
| definition | definitions-governance | Definition | perennial | resolve-required | yes |
| constitution | constitution-governance | Constitution | perennial | resolve-required | yes |
| decision | decision-gate | Decision | perennial | resolve-required | yes |
| spec | spec owner + decision-gate | Spec | perennial | resolve-required | yes |
| **discipline** | discipline-governance | Discipline | perennial | resolve-required | yes |
| **runtime contract** | task-session after owner gates | Runtime contract | perennial | resolve-required | yes |
| **projection** | ontology route + source owner | Projection | ephemeral (regenerable) | tolerated | no *(inferred — OQ-5)* |
| **residue** | *no producer of its own — emitted by other kinds (OQ-6)* | Residue | ephemeral | tolerated | no *(inferred — OQ-5)* |
| **premise** | definitions-governance | unresolved — OQ-4 *(a bet is not evidence; term = [`CAV2-D55`](../authority/definitions/DEFINITIONS.md#cav2-d55-premise))* | perennial | resolve-required | deferred (OQ-4) |
| **invariant** | definitions-governance | unresolved — OQ-2 *(same fork as `axiom`; term = [`CAV2-D54`](../authority/definitions/DEFINITIONS.md#cav2-d54-invariant))* | perennial | resolve-required | deferred (OQ-2) |
| **review** | review dispatch (`domainspec-subagents-strategy` → `review`) | Evidence | ephemeral | tolerated | no |
| **handoff** | `invoke handoff` | Evidence | ephemeral | tolerated | no |
| **implementation-plan** | `invoke plan` | unresolved *(prescribes execution; not Spec, not Decision — OQ-8)* | ephemeral | tolerated | deferred (OQ-8) |
| **audit** | audit run | Evidence | ephemeral | tolerated | no |
| **conceptual** | *no single producer — context authored in-place (OQ-8)* | Evidence | perennial | resolve-required | no |
| **backlog** | backlog maintenance | Evidence | perennial | tolerated *(a list of open items is not a contradiction)* | no |
| **readme** | *no single producer — authored beside what it describes (OQ-8)* | Projection | ephemeral (regenerable) | tolerated | no |

Rows in **bold** are added 2026-07-09 and are `candidate`. The first four close a
real hole: `Discipline`, `Runtime contract`, `Projection`, and `Residue` are
enumerated `CAV2-D49` authority kinds that **no canonical kind rolled up to**, so
nothing in the repository could be one of them.

**`canonical_kind` is the one label; `node_type` is its old name.** Ratified
[2026-07-13](../authority/decisions/2026-07-13-canonical-kind-one-label.md). An artifact
carries **one** type, not a schema-type plus a role-label. A session record's
`canonical_kind` is `session` — not the role it played; a session that did audit work is
a `session`, and what it *did* is expressed as **edges leaving it**.

An earlier version of this file claimed the opposite — that a canonical kind names a
schema and `node_type` names an orthogonal role. That claim was written by an agent on
2026-07-09 without an owner gate, and the decision above **overturns it**.

**The corpus does not conform to this enumeration, and is not required to.** No file
carries a `canonical_kind:` field; all 37 session records still declare a role-value
(`discovery` ×17, `conceptual` ×8, `audit` ×7, `constitution` ×3, `test`, `implementation-plan`).
The decision is **forward-looking and migrates nothing**. Do not read this table as a
description of the repository.

## Rules

1. **Rollup is a typed coupling** (`CAV2-D16`): every canonical-kind names exactly one
   authority-kind. Changing a rollup is an authority-model change, not an ontology
   edit.
2. **Durability is orthogonal** to the `authority_kind` (`CAV2-D29`) and to maturity
   (`CAV2-D23`): canonical-kinds under the same `authority_kind` may differ in durability
   (discovery vs ledger are both `Evidence`).
3. **Canonical =/= authority.** A row here makes an instance *canonical*, never
   *authoritative*. `authority_reachable = no` means instances of that kind are
   terminal evidence/records; they never earn authority (consistent with
   `CAV2-D48`'s boundary: evidence, ledger events, sessions are inputs/terminal).
   Even for an authority-*reachable* kind, an instance is authoritative only at
   `authority_state: promoted` (`CAV2-D51` / `CAV2-D48`) — `candidate` is
   proposed-not-yet-accepted and `demoted` is withdrawn/superseded. A candidate
   `definition` is still a definition, just not yet authority.
4. **Ledger contradiction.** A ledger is perennial but append-only: a later event
   overriding an earlier one is *temporal supersession*, not a live contradiction
   (`CAV2-D52`). Only a simultaneously-held `P and not-P` is a defect.
5. **Extension is owner-gated.** Adding a canonical-kind follows the same default-deny
   posture as `CAV2-D49`: until a kind is enumerated with a process, `authority_kind`,
   and durability, an artifact of that kind is non-canonical.

## Edges

Status: **candidate — and in unresolved collision with a consolidated catalog. Do not
build on this section until that is settled.**

> ⚠️ **This section forks an existing owner.**
> [`implementation/domainspec/vault/ontology-conventions.md`](../../implementation/domainspec/vault/ontology-conventions.md)
> (`node_type: constitution`, `status: consolidated`, **v2.3.0**) already owns a 22-edge
> catalog with typed endpoints, inverses, and a deprecation table. A 2026-07-09 review
> ([findings.md](../authority/definitions/reviews/2026-07-09-post-correction-audit/findings.md))
> established that the section below:
> - **revives six edges that catalog explicitly deprecated** — `contextualizes` (→`cites`),
>   `depends-on` (→`derives-from`), `questions` (→`opens-question`), `updates` (→"use
>   `version:` frontmatter"), `exemplifies` (deferred), `resolves` (→`closes-question`) —
>   and promotes `updates` to a succession *morphism*;
> - **omits `creates`/`created-by`** (session → any, *"A produced B as output"*), which is
>   the producer edge the spine has been trying to invent as `process_origin`;
> - **mis-cites `consumed-by`**: the catalog owns it as a *session* provenance edge that
>   explicitly carries **no** lineage; this section files it under *grounding*, sourced
>   from a definition card. Same name, opposite category.
>
> The claim below that these verbs are *"already in use, not invented here"* is therefore
> **false as written** — several are in use only as tombstones. This section must
> supersede, import, or scope itself out of that catalog. It may not silently fork it.
> **Open. Route: decision-gate.**

The kinds above are the **types** of the repository's document schema. Edges are the
declared relations between typed documents. A schema is types + edges + hom-sets; the
hom-sets are **not settled** — see the next section.

Edges split into four classes, and the class determines what an edge *is*, not merely
how it reads:

| Class | Edges | Status in the schema |
| --- | --- | --- |
| **grounding** | `derives-from`, `implements`, `validates`, `depends-on`, `rollup`, `consumed-by` | **morphisms** (proposed). Directed and typed. **The type graph MAY cycle** — a discovery may derive from a research *or vice versa* (owner, 2026-07-13). Acyclicity is an **instance** constraint (no document derives from itself), never a type-level one. |
| **succession** | `supersedes`, `updates`, `deprecates` | **morphisms** (proposed). Endomorphisms (`T -> T`, same kind both ends) — note a `T -> T` arrow **is** a type-level self-loop, which is admissible; the strict order holds over **instances**. |
| **conflict** | `contradicts`, `alternative-to` | **not morphisms** — symmetric, so they induce cycles and make hom-sets infinite. Annotations on a pair. |
| **navigational** | `questions`, `refines`, `exemplifies`, `contextualizes`, `flags` | **not morphisms** (candidate) — carry no authority; annotations. |

Only the first two classes belong in the category. A symmetric edge admitted as a
morphism makes `Hom(A,B)` infinite (`A contradicts B contradicts A ...` is an endless
family of distinct paths), which is why `contradicts` is a **defect marker to
eliminate**, never a relation to compose.

Provenance for these verbs — they are already in use, not invented here:

- `rollup` is the `Authority kind` column above: `canonical_kind -> authority_kind`, a
  `CAV2-D16` typed coupling.
- `consumed-by` is the `### Primary Consumers` list carried by every definition card.
- `validates` and `questions` appear verbatim in the `## Contradictions` section of
  session records (e.g. `2026-07-08-1520`: *"validates …/constitution-invariant-axiom-role-review.md"*,
  *"questions …/attacks.md"*).
- `flags` is what `DEFINITION-DRIFT-AUDIT.md` does to a definition.
- `supersedes` / `deprecates` is the `CAV2-D48` demotion path (`demoted` ≈ withdrawn
  or superseded).

## Hom-Sets

Status: **OPEN — under design.** Nothing below is authority.

A hom-set `Hom(A,B)` is every path from `A` to `B`, modulo declared path equations. It
is *not* a list of permitted pairs, and the difference matters: once edges exist,
composition exists whether or not it was intended. If `spec --implements--> constitution`
and `constitution --derives-from--> axiom`, then a morphism `spec -> axiom` exists.
The only choice is whether it equals a named edge or is a distinct path.

Two constraints govern edges, and they are **not the same mechanism**:

1. **Endpoint typing — type-level, belongs in the schema.** For each grounding edge,
   the admissible `(source kind, target kind)` pairs. This deletes arrows: e.g.
   `readme --implements--> axiom` should not exist. Precedent for the machine form is
   [`projects/domainspec-v2/definitions/relationships/relationships.yml`](../../projects/domainspec-v2/definitions/relationships/relationships.yml),
   whose 31 signatures carry `source_type`, `target_type`, and
   `violation_class: unconstructible-edge`.

2. **Standing monotonicity — instance-level, NOT a hom-set.** For every grounding
   edge, the target's `authority_state` must not be lower than the source's: a
   `promoted` constitution may **cite** a `candidate` session as context but may not
   *derive its authority* from it. This cannot be expressed by deleting arrows,
   because `authority_state` varies per document, not per kind. It is a constraint on
   the filled graph, checked over instances.

Conflating (1) and (2) is the same error that malformed the `Process` column above —
a per-instance fact crammed into a per-type table.

Undecided, and blocking a machine-readable edge table:

- Which classes are morphisms (proposal: grounding + succession only).
- Whether the category is **free** (every path distinct) or carries **path equations**
  (proposal: declare exactly one — `derives-from` is transitive — so that "what does
  this ultimately rest on?" is a single query).
- The endpoint table itself, per grounding edge.

## Open Questions

### OQ-1. Is the canonical-kind enumeration closed (default-deny), like Tier-2?

Context: `CAV2-D49` makes the Tier-2 authority-kind set closed. Whether Tier-1
should also be closed-with-default-deny, or stay open-and-additive, is unresolved.
Recommendation: keep it **candidate/open** during design, decide closure before
standalone extraction. Status: OPEN.

### OQ-2. Does `axiom` roll up to `Definition`, or become its own coarse kind?

Context: mirrors [AUTHORITY-MODEL OQ-2](../authority/AUTHORITY-MODEL.md#oq-2-should-invariant-and-axiom-become-first-class-authority-kinds).
As of 2026-07-08 `axiom` is canonically defined ([`CAV2-D53`](../authority/definitions/DEFINITIONS.md#cav2-d53-axiom))
with an explicit boundary that an axiom is **not** a definition. Its `authority_kind`
is therefore marked **`unresolved`** rather than `Definition` — the one row that does
not yet name exactly one authority-kind (a `CAV2-D16` open coupling, not a hidden
assumption), pending the OQ-2 decision-gate call. If OQ-2 promotes `invariant`/`axiom`
to first-class authority kinds, set the rollup accordingly. Status: OPEN (tracked
upstream).

### OQ-3. Per-instance durability override — recorded where?

Context: durability defaults live per kind; an instance may override with an owner
note. The carrier for that override (frontmatter field, ledger entry, Craft state)
is not yet decided. Status: OPEN.

### OQ-4. What authority-kind does `premise` roll up to?

Context: `CAV2-D55` holds a premise is a bet (`veracidade` low, `convicção` high),
adopted to proceed and *not* established true. It is therefore not `Evidence` — evidence
reports, a premise wagers — and not `Definition`. It provisionally grounds invariants and
rules, which is authority-shaped behaviour without authority-bearing standing. Related to
`PR-OQ-3` on the `CAV2-D55` card (may a premise ground an invariant or constitution rule?).
Marked `unresolved` rather than guessed. Route: decision-gate. Status: OPEN.

### OQ-5. Are `projection` and `residue` authority-reachable?

Context: both rows are marked `no` by **inference** from the `CAV2-D49` "must not collapse
into" column — `Projection` must not collapse into a promotion decision, `Residue` must not
collapse into a defect by default. Neither is stated. The inference is recorded so it is
visible as an inference and not read as a ratified value. Route: owner ratification.
Status: OPEN.

### OQ-6. `residue` has no producing process.

Context: every other kind names a producer. Residue is not authored — it is what a
`CAV2-D18` operation *leaves behind*, emitted by whatever process failed to carry it. That
makes `residue` the one kind whose origin is a by-product rather than an output, which is
independent evidence that "produced by a declared process" was never the right membership
test for canonicity. If a kind can be canonical with no producer at all, the producer
column is a property of kinds, not a condition of the type. Related to `CA-OQ-1` /
`CA-OQ-2` on `CAV2-D51`. Status: OPEN.

### OQ-7. `session` — one label or two? SETTLED BY DECISION (not by this file).

**This question was previously marked RESOLVED/CLOSED by the same agent that wrote it,
within one session, with no owner gate, on the reasoning that `canonical_kind` (schema)
and `node_type` (role) are orthogonal. That reasoning was false and the self-closure was
improper.** Both are struck.

The owner settled it on 2026-07-13
([decision](../authority/decisions/2026-07-13-canonical-kind-one-label.md)): **one label**,
named `canonical_kind`. A session record's `canonical_kind` is `session`; what the session
*did* becomes edges, not a second type label. `is_session` is therefore redundant as a type
axis.

Note the source of the original objection — that a session's role varies, so `session`
should not be a type — is `implementation/domainspec/vault/ontology-conventions.md`, a
**consolidated** constitution. This file never cited it. The decision supersedes it as to
the label's name and cardinality only; that catalog's **edges** remain authoritative.
Status: CLOSED by owner decision.
