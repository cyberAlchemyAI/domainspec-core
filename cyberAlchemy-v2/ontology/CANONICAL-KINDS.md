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
