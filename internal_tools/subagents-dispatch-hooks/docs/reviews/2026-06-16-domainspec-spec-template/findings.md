---
tags: [review, findings, specs, domainspec, subagents-dispatch]
node_type: review
is_session: false
layer: architecture
nature: evidence
status: verified
version: 0.2.0
last_updated: 2026-06-16
dispatch_id: 2026-06-16-domainspec-spec-template-review
---

# Findings — DomainSpec Spec Template Family Review (verified)

Target: `arcanum/spells/invoke/templates/domainspec-spec/`. Deliverable: verified change
requests. Severity: **CRITICAL** (breaks the system / corrupts the registry / contradicts
DomainSpec law) · **MAJOR** (functional gap / doc-vs-doc drift / load-bearing omission) ·
**MINOR** (wording / stale pointer). Every surviving finding quotes the template and cites its
attacker return (claim ≤ proof). Raw returns + robot-talks collapse log: `attacks.md`.

## Verification reconciliation (the load-bearing step)

The draft carried 1 CRITICAL + 6 MAJOR. Two verifiers refuted it on independent corpora:

- **V2 (empirical-vs-files)** — CONFIRMED every cited fact literally: `domain.md`,
  `workflows.md`, `architecture.md`, `glossary.md` are all absent on disk; SPEC L53 reads
  `Enum / Type`; the line-count bands are literally `<120 / 120-200 / >300`, leaving
  `(200,300]` uncovered; README L7 lists 6 aspect docs and omits `domain`.
- **V1 (deductive-vs-law)** — refuted the **severities**, not the facts: the target is a
  *fill-the-placeholder authoring template* (SPEC L82 `Link only to aspect files that exist…
  Delete unused lines`; README `Authoring a spec in this format`), so every unfilled link is
  "dangling by design," DS-D8 enforcement legitimately lives **downstream**
  (architecture-bundle/plan), and partial aspect coverage is the template's explicit contract.
  Holding it to a shipped/validated-artifact standard is the draft's category error.

**Reconciled outcome (claim ≤ proof):**

| draft | verified | why |
|-------|----------|-----|
| C1 CRITICAL | **C1 MAJOR** | Real and **not** covered by V1's author-time defense: unlike the Aspect Docs *menu*, the Concept Registry (L57 "Source of truth for registry sync") and Domain Concepts (L48) sections carry **no** delete-unused license, and README omits `domain.md` entirely — so the primary `Entity` meta-type is routed to a file the family neither ships nor lists. But an author can recover by creating it → MAJOR, not a system-breaker. |
| M1 MAJOR | **DROPPED → m6 (MINOR, optional)** | V1: no law obliges the define-stage SPEC graph to be DS-D8-checkable; architecture-bundle.md/plan enforce it downstream. Only an optional "DS-D8 is enforced downstream" pointer remains. |
| M2 MAJOR | **MINOR** | V1: `Enum / Type` is TAXONOMY's shipped human label for the DS-D1 token `Enum`; at most a label-vs-sync-token nit. |
| M3 MAJOR | **MINOR** | V1: the 10-row Aspect Docs table is a by-design superset menu (delete-unused), not a claim of 10 docs. Residue (README omits domain) rolls into C1. |
| M4 MAJOR | **MINOR** | V1: partial aspect coverage is the template's explicit contract; `workflows.md` sits under the delete-unused menu (weaker than the domain.md case). |
| M5 MAJOR | **MINOR** | V1 reads the bands as guidance, not a partition; V2 confirms `(200,300]` is literally unaddressed — a clarification nit. |
| M6 MAJOR | **MINOR** | V1: no law mandates a canonical anchor slug; underspecification, not a violation. |
| m1–m5 | **MINOR (survive)** | Below the law-violation bar by construction; none refuted. |

Net verified severity: **1 MAJOR + 11 MINOR.** The adversarial pass prevented an
over-claimed CRITICAL and five MAJORs from shipping — the review's claim ≤ proof working.

## SPEC.md

| # | evidence (quoted, line-confirmed by V2) | severity | proposed fix |
|---|------------------------------------------|----------|--------------|
| **C1** | Concept Registry L61 `\| [{ConceptName}](domain.md#{anchor}) \| {feature}.{ConceptName} \| Entity \|` + Domain Concepts L52-53 `domain.md#{anchor}`; registry comment L57 `Source of truth for registry sync. Keep compact`; the delete-unused license (L82) sits under Aspect Docs ONLY; `domain.md` absent on disk; README L7 omits `domain`. (A1-7b = A2-F2 = A3-F1; V2 CONFIRMED, V1 author-time defense does not reach the registry) | **MAJOR** | Ship a `domain.md` template and list it in README, OR repoint the Entity/Enum Registry+Domain-Concepts rows to an existing aspect doc. Reconcile so the primary meta-type has a real, acknowledged home. |
| m1 | Aspect Docs table L86-93 links `architecture.md`/`glossary.md`/`workflows.md`/`domain.md`, none shipped — governed by L82 `Delete unused lines` (author-time). | MINOR | Add a note that these are not shipped in the family. |
| m2 | Registry comment L57 governs shape but never says `Type ∈ DS-D1 meta-types`. | MINOR | Add `Type ∈ DS-D1 meta-types (DEFINITIONS.md#ds-d1)`. |
| m3 | README(6) / SPEC Aspect Docs table(10) / disk(6) differ (menu vs core). | MINOR | Mark the table as a prune-menu; align README + core set. |
| m4 | SPEC L53 `Enum / Type` is a label, not a single sync token. | MINOR | Note label-vs-token, or alias-map for registry sync. |
| m5 | Governance bands L23-25 (`<120 / 120-200 / >300`) leave `(200,300]` unaddressed. | MINOR | Clarify the bands are non-exhaustive guidance, or use `>200`. |
| m6 | SPEC `#{anchor}` (L41,L52) vs operations.md `#entityname` (L8) — no canonical slug rule; and the SPEC Feature Concept Graph (L73 `From\|Edge\|To`) carries no endpoint meta-types, so the DS-D8 signature architecture-bundle.md L34/L47 requires is enforced only downstream. | MINOR | Publish one anchor-slug rule; optionally note DS-D8 is enforced downstream. |
| m7 | `> 15 rows` (L25) names no addressable table; capability extraction keys on authored line/row count (gameable by under-documenting). | MINOR | Name the counted table; tie extraction to registry concept count. |
| m8 | Every table ships a blank data row + `{tokens}`; no `zero residual {…}` completion gate. | MINOR | State a completion gate (no residual `{…}`, no empty data rows). |

**Verdict: FIX** (1 surviving MAJOR — C1).

## README.md

| # | evidence | severity | proposed fix |
|---|----------|----------|--------------|
| C1 (contrib) | L7 lists 6 aspect docs, omits `domain` — the omission that hides C1 at the index level. | (rolls up to C1) | Resolved by C1's fix (list `domain.md` or the author-created set). |

**Verdict: FIX** (participates in C1).

## operations.md · queries.md

Route `Entity` references to `domain.md` (operations.md L8, queries.md L31) — fan-in sites of
C1; no independent finding. **Verdict: KEEP** (resolved by C1's fix).

## interfaces.md · states.md · events.md · mappings.md · architecture-bundle.md · execution-pack.md

V1+A3 confirmed these give real, test-derivable structure and correctly defer to DEFINITIONS.md;
architecture-bundle.md is the correct downstream home of the DS-D8 enforcement (m6). They carry
only the cross-cutting anchor-slug nit (m6). **Verdict: KEEP.**

## Change requests (verified, severity-ordered)

1. **C1 (MAJOR)** — Give the `Entity`/`Enum` meta-type a real, acknowledged home: ship a
   `domain.md` template and list it in README, or repoint the Concept Registry + Domain
   Concepts rows to an existing aspect doc. (The one finding the author-time defense does not
   cover.)
2. **m1 (MINOR)** — Note that `architecture.md`/`glossary.md`/`workflows.md`/`domain.md` are not shipped.
3. **m2 (MINOR)** — Add a `Type ∈ DS-D1 meta-types` comment to the Concept Registry.
4. **m3 (MINOR)** — Mark the Aspect Docs table as a prune-menu; align README + the core set.
5. **m4 (MINOR)** — Resolve `Enum / Type` label vs registry-sync token (note or alias-map).
6. **m5 (MINOR)** — Clarify the line-count bands are non-exhaustive guidance (or use `>200`).
7. **m6 (MINOR)** — Publish one canonical anchor-slug rule; optionally note DS-D8 is enforced downstream.
8. **m7 (MINOR)** — Name the table the `>15 rows` rule counts; tie extraction to registry concept count.
9. **m8 (MINOR)** — Add a `zero residual {…} tokens / no empty data rows` completion gate.
