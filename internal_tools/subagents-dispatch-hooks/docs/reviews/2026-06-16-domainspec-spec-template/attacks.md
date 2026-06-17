---
tags: [review, findings, specs, domainspec, subagents-dispatch]
node_type: review
is_session: false
layer: architecture
nature: evidence
status: draft
version: 0.1.0
last_updated: 2026-06-16
dispatch_id: 2026-06-16-domainspec-spec-template-review
---

# Attacks — DomainSpec Spec Template Family Review

Target: `arcanum/spells/invoke/templates/domainspec-spec/` (SPEC.md, operations.md, queries.md, interfaces.md, states.md, events.md, mappings.md, architecture-bundle.md, README.md).
Three attackers ran in parallel, then confronted each other (robot-talks). This file records INITIAL returns and the collapse log. The verifier pass has not yet run.

## Collected attacker returns (INITIAL)

### A1 — fidelity / governance
- **A1-1 MAJOR** — registry `Type` column shows `Enum / Type` (SPEC.md L53), not a canonical single DS-D1 token; registry is sync source of truth.
- **A1-2 MINOR** — no comment ties the `Type` column to the DS-D1 meta-type set.
- **A1-3 MAJOR** — architecture-bundle.md L34/L47 promise DS-D8 edge signatures, but the SPEC Feature Concept Graph carries no endpoint meta-types, so the signature is uncheckable from the spec.
- **A1-4 MAJOR** — line-count governance thresholds (SPEC.md L23-25) leave the band `(200,300]` uncovered.
- **A1-5 MINOR** — a band-2 SPEC still shows the band-1 inline `### {Capability Name} (inline variant)` subsection.
- **A1-6 MINOR** — ">15 rows" (L25) names no addressable table.
- **A1-7 MAJOR** — README↔SPEC aspect-doc file drift; `domain.md` is the linchpin.
- **A1-8 MAJOR** — registry can type `Saga`/`Workflow`/`Policy` with no `workflows.md` shipped.
- **A1-9 MINOR** — UI meta-types are valid but no UI aspect doc exists.

### A2 — ownership / reference-integrity
- **F1 MINOR** — Aspect Docs table links architecture/glossary/domain/workflows.md, none of which ship; governed by SPEC.md L82 "Link only to aspect files that exist... Delete unused lines" → intentional.
- **F2 MAJOR** — Domain Concepts + Concept Registry hard-link `domain.md` with NO delete-unused instruction; README omits domain; operations.md L8 / queries.md also route Entity to domain.md.
- **F3 MAJOR** — README lists 6 aspect docs, SPEC table claims 10, disk has 6.
- **F4 MINOR** — Feature Concept Graph endpoints Rule/Event never appear in the sample registry.
- **F5 MINOR** — anchor-slug inconsistent: SPEC bare `#{anchor}` vs aspect docs `#{name-lowercase}`.

### A3 — operability / abuse-gaming
- **F1 CRITICAL** — registry IDs link `domain.md` which has no template; README sells the registry as a consumer surface (spec→test / registry sync); Entity is un-fillable end-to-end.
- **F2 MAJOR** — architecture/glossary/workflows orphans.
- **F3 MAJOR** — anchor convention unspecified, 3 lowercasing variants, non-deterministic ID→anchor.
- **F4 MAJOR** — no "registry ID ⇔ non-empty aspect section" gate; registry can be hollow.
- **F5 MINOR** — unfilled `{tokens}` / empty single-row tables pass as complete; no "zero residual `{`" check.
- **F6 MINOR** — governance split keyed on line/row count is gameable by under-documenting.

## Robot-talks collapse log (P14 collapse-detection record)

Verified on disk during confrontation: SPEC.md L82 delete-unused comment sits ONLY under Aspect Docs; Domain Concepts L48 = "for quick human understanding"; Concept Registry L57 = "Source of truth for registry sync. Keep compact" — mandatory, with no delete-unused cover.

- **A1-9 ABANDONED** — optional-aspect scope (UI doc absence) is by-design; not a defect.
- **A1-5 DEMOTED** — folded into M5 as an instance of the same line-count governance gap (A1-4), not a standalone finding.
- **A1-7 SPLIT** — Aspect-Docs-table portion DEMOTED to MINOR (conceded to A2-F1); `domain.md`-on-the-registry-path portion RAISED to CRITICAL and merged into C1.
- **A1-8 UPHELD MAJOR**, rescoped to Saga/Workflow/Policy only → M4.
- **A2-F2 RAISED to CRITICAL** — Entity has no aspect home, is multiply fanned-in (Domain Concepts, Concept Registry, operations.md L8, queries.md), and the registry comment makes its target mandatory not optional → merged into C1.
- **A2-F4 ABANDONED standalone → MERGED** with A1-3 and A3-F4 into one "registry is not a closed/validated surface" MAJOR → M1.
- **A2-F5 conceded DUPLICATE of A3-F3**; severity raised MINOR→MAJOR → M6.
- **A2-F1 UPHELD MINOR**, kept distinct from C1 (the delete-unused comment reaches the table but not the registry) → m1.
- **A2-F3 UPHELD MAJOR**, overlaps A1-7a → MERGED into one aspect-doc-set-disagreement MAJOR → M3.
- **A3-F1 UPHELD CRITICAL** → C1.
- **A3-F2 SPLIT** — table-links portion DEMOTED to MINOR (A2-F1 correct) → m1; workflows.md-as-registry-target portion folds into C1/M4.
- **A3-F3 ABANDONED standalone → duplicate of A2-F5** → M6.
- **A3-F4 UPHELD MAJOR**, reinforced by A1-8 → M1.
- **A1-1 / A1-3 / A1-4 UPHELD MAJOR** → M2 / M1 / M5. **A1-6 UPHELD MINOR** → m3. **A3-F5 UPHELD MINOR** → m4. **A3-F6 UPHELD MINOR** → m5. **A1-2 UPHELD MINOR** → m2.

### Deduped ledger after collapse
- CRITICAL: **C1** domain.md orphan on the mandatory registry consumer path (A1-7b = A2-F2 = A3-F1).
- MAJOR: **M1** registry not a closed/validated surface (A2-F4 + A1-3 + A3-F4); **M2** `Enum / Type` non-canonical DS-D1 (A1-1); **M3** aspect-doc set three-way disagreement README6 / SPEC10 / disk6 (A1-7a + A2-F3); **M4** registry types Saga/Workflow/Policy with no workflows.md (A1-8); **M5** governance line-count gap `(200,300]` (A1-4); **M6** anchor-slug convention underspecified (A2-F5 + A3-F3).
- MINOR: **m1** Aspect Docs table links to non-shipping files, delete-unused-governed (A2-F1 / A3-F2); **m2** no comment tying `Type` column to DS-D1 set (A1-2); **m3** ">15 rows" names no addressable table (A1-6); **m4** hollow `{tokens}` / empty rows pass as complete (A3-F5); **m5** line/row-count split gameable (A3-F6).

## Verifier returns

Zig-zag (synthesizer ⇄ verifiers, loop_cap 2). V1 raised objections on loop 1; the synthesizer
adopted the verifiers' verdicts wholesale (demote/drop), so a re-check would raise no new
objection — the exchange terminates. See `findings.md` "Verification reconciliation" for the table.

### V1 — deductive against DomainSpec governing law
Refuted the **severities**, not the facts. Core argument: the target is a fill-the-placeholder
**authoring template** — SPEC.md L82 (`Link only to aspect files that exist… Delete unused lines`)
and README (`Authoring a spec in this format`) make every unfilled link dangling-by-design, DS-D8
enforcement lives downstream (architecture-bundle/plan), and partial aspect coverage is the
explicit contract. Verdicts: **C1 DROP** (over-stated), **M1 DROP** (DS-D8 is downstream),
**M2 DROP** (`Enum / Type` is TAXONOMY's shipped label for DS-D1 `Enum`), **M4 DROP** (partial
coverage by design), **M5 DROP** (bands are guidance, not a partition), **M3 DEMOTE→MINOR**
(Aspect Docs table is a by-design menu), **M6 DEMOTE→MINOR** (no slug law); m1–m5 survive as nits.

### V2 — empirical against the literal files
CONFIRMED every cited fact on disk. Directory has 10 files; `domain.md`, `workflows.md`,
`architecture.md`, `glossary.md` are **absent**. SPEC L53 = `Enum / Type` (literal); Concept
Registry comment at L57; `domain.md#{anchor}` at L52-53 (Domain Concepts) and L61 (Registry);
`Delete unused lines` at L82 under Aspect Docs only; `[Workflows](workflows.md)` at L93; bands at
L23-25 leave `(200,300]` literally uncovered; README L7 lists 6 aspect docs and **omits** domain.
Line-numbers in the draft verified accurate. One framing correction: README does not list `domain`.

### Strategist reconciliation (claim ≤ proof)
V2 confirms the facts; V1 is right that the draft category-errored an author-time template — but
V1 **overshoots on C1**: the delete-unused license demonstrably does **not** reach the Concept
Registry / Domain Concepts sections (V2-confirmed), and README omits `domain.md`, so the primary
`Entity` meta-type is routed to a file the family neither ships nor lists. That survives as a
real **MAJOR** (recoverable by the author, not system-breaking). All other findings demote to
MINOR or drop. Net verified: **1 MAJOR (C1) + 11 MINOR.**
