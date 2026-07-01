---
node_type: work-pack
is_session: false
status: candidate
boundary: INTERNAL — reformulate Batch-1 spec docs (v1→v2); v1 read-only; engine src/rules δ-algorithm never described
created: 2026-07-01
authored_by: invoke (mode: plan)
design: ./DESIGN.md
layering: ./implementation-layering.md
target_artifact: projects/domainspec-v2/impl/spec (+ authority/constitutions on R6b)
source_of_verdicts: ../../research/2026-06-29-v1-import-triage/findings.md
manifest: ../../IMPORT-MANIFEST.md
complexity: medium
---

# Reformulate Batch-1 Spec Docs — Work-Pack

Batch 1's engine fork is done and green; its **6 spec docs are `reformulation-pending`** (copied verbatim
to unblock the build). This work-pack re-authors them for v2's *govern + enforce Ontology A on evidence*
mandate, binds each to its ratified governance owner, and closes the **v1-freeze gate**
([IMPORT-MANIFEST.md](../../IMPORT-MANIFEST.md)). **v1 (`implementation/domainspec/`) is read-only** —
reformulate the v2 copies under `impl/spec/`. Validators are runnable post-G3, so acceptance is
machine-checkable, not just declared.

**Reformulation contract (every SWU):** (a) strip v1-specific content/paths; (b) re-anchor to
`impl/spec/`; (c) bind to the governance owner + matching constitution rule; (d) make the governance
method *runnable* where one exists; (e) preserve load-bearing terms with tracked definition IDs (C(meta-4));
(f) no v1 residue (grep clean); (g) **no moat leak** — never describe the engine `src/rules` δ-algorithm;
(h) **matches the target-result in [DESIGN.md](./DESIGN.md) §3** for this doc — the *semantic* gate, above
validator-green (validator green proves well-formed; §3 proves it says the right v2 thing).

**Pre-execution blockers (from [DESIGN.md](./DESIGN.md) §4 — resolve before the mapped SWU runs):**
D1 drift-surface reconciliation → **R5** · D2 UI scope (25 vs backend-14) → **R2** · D3 v1-only file
references → **R5/R6a** · D4 forbidden-edge law form → **R3**.

## SWU manifest
| SWU | Layer | Doc → governance | Depends | Acceptance (green) |
| --- | --- | --- | --- | --- |
| **R1** | L0 | `impl/spec/AXIOMS.md` → base + layering (A2) | — | `validate:docs` RC 0; A2 bound to C6; namespace note folded in; review-pass |
| **R2** | L1 | `impl/spec/TAXONOMY.md` → layering | R1 | `tags:test`/`validate-code-tags` recognizes all concept types; `engine:lint` CLEAN; no v1 residue |
| **R3** | L1 | `impl/spec/RELATIONSHIPS.md` → layering law (C6) + validation check (C11) | R2 | `validate:rels` PASS; edge-law = what C11 checks & C6 forbids; endpoints typed; **+ R3-P1/P2/P3 catalog-coverage additions (toy T2b)** |
| **R4** | L2 | `impl/spec/TEST-PIPELINE.md` → validation (C5, C10) | R2, R3 | Consistent w/ engine `derive`/`lint`; contract-only (no δ-algorithm); review-pass |
| **R5** | L2 | `impl/spec/DRIFT-CONVERGENCE.md` → drift (C7) | R2 | 5 surfaces + trend-not-signal + write-authority proviso; code-tag-drift bound; review-pass |
| **R6a** | L3 | `impl/spec/CONSTITUTION.md` (v1 C1–C11) → domain governance | R1–R5 | Each v1 C-rule crosswalked or explicitly dropped; validators stay green; **OQ-2 crosswalk closed** |
| **R6b** | L3 | credibility-constitution per-governance split | R6a | base + validation/layering/drift constitutions created; C6↔C11 binding preserved; `npm run validate`+`engine:test` green |
| **R7** | L2 | `impl/spec/DEFINITIONS.md` (**NET-NEW** — migration omitted it) → domain vocabulary | R2, R3 | DS-D1 meta-types + DS-D2 verbs defined w/ IDs (3-voice); concept-registry home; `validate:docs` clean |

Global regression gate for **every** SWU: `npm run validate` **and** `npm run engine:test` stay RC 0 after the edit.

---

## R1 — AXIOMS (L0)
- **Write scope:** `impl/spec/AXIOMS.md`.
- **Steps:** re-author each axiom v2-native; make A1 (semantic authority precedes implementation) and A2 (adapter line — no dependency crosses it) explicit; **bind A2 to layering C6** (forbidden edges unconstructible); fold in the namespace-disambiguation note (the 5-line clause-reference note currently dirty in v1 `AXIOMS.md`); repoint any `docs/` or v1 paths to `impl/spec/`.
- **Impl detail:** axioms are review-mode rules; the load-bearing terms are the axiom IDs (A1, A2…) other docs cite — each must resolve. No behavior.
- **Validation:** `npm run validate:docs` RC 0; grep for `implementation/domainspec`/`docs/features` → none; review-pass.
- **Verification:** links resolve; A2↔C6 cross-reference present.

## R2 — TAXONOMY (L1, layering)
- **Write scope:** `impl/spec/TAXONOMY.md`.
- **Steps:** re-author the concept-type table (the 25 Ontology-A concepts) + layer-membership + the layer-law statement; bind to **layering governance**; ensure the type set is exactly what `validate-code-tags` + the engine consume (G3 already points them at `impl/spec/TAXONOMY.md`).
- **Impl detail:** the concept-type list is load-bearing (the tag validator checks tag `concept.type ∈ TAXONOMY`); every type needs a tracked definition ID; layer-membership assigns each concept a layer (feeds C6/adapter-line). A layer *assignment* is not a dependency *verdict* (C6).
- **Validation:** `npm run tags:test` RC 0 (8/8) with the reformulated taxonomy; `npm run engine:lint` CLEAN; no v1 residue.
- **Verification:** flip one concept type in a fixture → tag validator flags it (discriminating).

## R3 — RELATIONSHIPS (L1, layering law + validation check)
- **Write scope:** `impl/spec/RELATIONSHIPS.md`.
- **Steps:** re-author the typed-edge vocabulary + endpoint signatures + forbidden-edge set (the **edge-law**); bind the LAW to layering (C6) and note the CHECK is validation (C11, `validate-relationships`); keep the C6↔C11 relationship explicit.
- **Catalog-coverage additions (from toy T2b — [../../research/spec-ontology-unification/toy/catalog.md](../../research/spec-ontology-unification/toy/catalog.md)):** the current 29 edges don't cover 2 real relations T1 found. Add **R3-P1** `Operation→Entity` read (or generalize `queries` to Behavioral→Entity), **R3-P2** `Operation→ValueObject` returns; decide **R3-P3** the Event payload+publisher composite (one node vs split). The canonical-edge count grows past 29 accordingly.
- **Edge-law admissibility (build-from-owned — CAV2-D22 orthogonal classification / D29 axis orthogonality / D16 typed coupling):** an edge type is admissible only if it composes into *different code*; else fold the distinction into the node type or a typed coupling flag. Rulings: **keep** `enforces`≠`applies` (guard vs select); **collapse** `enforces`/`enforces-cross` (same code + cross flag); **reject** `queries` for `Calc→Policy` (redundant); **widen** `applies : Policy→{Op,Calc}`. Governance orthogonality only (NOT Lean/Hilbert). See `DEC-DSV2-EDGE-ADMISSIBILITY`.
- **Impl detail:** each edge = (name, from-type, to-type, allowed?) over TAXONOMY concepts; forbidden edges must be expressed so C6 renders them unconstructible, not merely flagged; `validate-relationships` reads this file (G3 default → `impl/spec/RELATIONSHIPS.md`).
- **Validation:** `npm run validate:rels` PASS at the **new** canonicalEdges total (>29 after R3-P1/P2); flip one edge in the sample feature → RC non-zero (discriminating); the 2 T1-found relations (op-reads-Entity, op-returns-VO) now resolve to a typed edge.
- **Verification:** every declared edge has typed endpoints; forbidden set present.

## R4 — TEST-PIPELINE (L2, validation)
- **Write scope:** `impl/spec/TEST-PIPELINE.md`.
- **Steps:** re-author the derived-obligation rules the engine runs; bind to **validation governance** (C5 derivation-from-spec, C10 completeness); describe the derive→check→emit **contract** and the obligation classes — **NOT** the `src/rules` δ-algorithm (moat).
- **Impl detail:** state, per spec construct, which obligations are derived + expected-value source (the spec, per C5); align terminology with the engine CLI (`derive`/`lint`/`emit-tests`); the algorithm that produces obligations stays private.
- **Validation:** cross-check the documented obligation classes against `engine:test` (97/97) behavior; **no-moat-leak** grep (no rule internals); review-pass.
- **Verification:** a reviewer can predict `derive` output classes from the doc without seeing `src/rules`.

## R5 — DRIFT-CONVERGENCE (L2, drift)
- **Write scope:** `impl/spec/DRIFT-CONVERGENCE.md`.
- **Steps:** re-author the 5 drift surfaces (semantic / contract / runtime / governance / coordination) + convergence criteria; bind to **drift governance** (C7); state convergence = evidence-backed trend, never a single signal; state the **write-authority proviso** (no surface writes a node's promotion-status) and that **Saturn is the actuator, not the authority**.
- **Impl detail:** the code-tag-drift tooling (`compare-code-tag-drift.ts`) is a drift *method* — bind it; note the `Stream<CheckResult>` + guardedness engine impl is **separate residue** (R-trend-type), not delivered here.
- **Validation:** review-pass (surfaces + criteria present); code-tag-drift method reference resolves; write-authority proviso stated.
- **Verification:** the 5 surfaces are enumerated and each has a convergence criterion.

## R6a — CONSTITUTION crosswalk (L3, domain governance)
- **Write scope:** `impl/spec/CONSTITUTION.md`.
- **Steps:** crosswalk each v1 C1–C11 into a v2 domain-governance rule (or explicitly DROP with reason); bind each rule to its governance (validation/layering/drift) + AXIOMS; reconcile with the credibility constitution's rules (no double-ownership).
- **Impl detail:** this is **OQ-2**'s crosswalk half; keep domain-governance rules (impl/spec) distinct from credibility rules (authority/); every rule gets a validation-mode label.
- **Validation:** `constitution-governance validate`; `npm run validate` + `engine:test` stay green; every v1 C-rule accounted for (crosswalked or dropped).
- **Verification:** a v1→v2 rule crosswalk table exists; no orphaned v1 rule.

## R6b — Credibility-constitution split (L3)
- **Write scope:** `authority/constitutions/{domainspec-v2-CONSTITUTION.md (slim to base), validation-governance-CONSTITUTION.md, layering-governance-CONSTITUTION.md, drift-governance-CONSTITUTION.md}`.
- **Steps:** execute the split plan recorded in the credibility constitution — move C5/C9/C10/C11 → validation, C6 → layering, C7 → drift; keep base = C1–C4, C8, C(meta-1..4); preserve the **C6↔C11** cross-binding; set each new file's owner route + selectors; update the split-plan section to "executed".
- **Impl detail:** composition order (narrowest-first) must be documented in the base; no rule text changes beyond relocation + the crosswalk from R6a; do not over-fragment (per-governance, never per-rule).
- **Validation:** `constitution-governance validate`; the four files compose without conflict; validators still green.
- **Verification:** every rule lives in exactly one file; C6↔C11 reference resolves across files; OQ-2 marked closed.

## R7 — DEFINITIONS (net-new, L2)  ← added 2026-07-01 (refresh)
- **Write scope:** `impl/spec/DEFINITIONS.md` (new) + `impl/spec/DEFINITIONS-INDEX.md` (new).
- **Depends:** R2 (meta-types) + R3 (edge verbs). **Net-new** — no v1 source in the 6-doc Batch-1 set (the migration omitted it; v1 definitions lived under `research/projects/domainspec/definitions/`).
- **Steps:** aggregate the finalized 25 TAXONOMY meta-types as **DS-D1** definitions + the RELATIONSHIPS edge verbs as **DS-D2** definitions (+ the DS-D8 edge signature), each with a stable ID + 3 voices (formal / plain / domain-context); wire it as the `definitions-governance` M2-C1 concept-registry-aggregation home.
- **Impl detail:** DS-D* = the *domain* vocabulary; do NOT duplicate the *governance* vocabulary `DSV2-D*` (that's `authority/definitions/`, already stood up). Each entry is a **term**, not a rule (rules stay in CONSTITUTION — no `RULES.md`, per DSV2-D1/CAV2-D22 orthogonality).
- **Validation:** `npm run validate:docs` clean; every TAXONOMY type + RELATIONSHIPS verb resolves to a DS-D* entry; `definitions-governance` can aggregate a feature Concept Registry against it.
- **Verification:** reviewer confirms every meta-type/verb has a definition; index synced.

---

## Dispatch technique trace
`sequence` (L0→L3 dependency gates) · `owner_boundary_check` (each doc→its governance owner; moat untouched; v1 read-only) · `artifact_contract_bridge` (each doc must satisfy its governance validator) · `validation_loop` (per-SWU acceptance = validator RC 0 + review) · `concrete_path_evidence` (exact paths + validators per SWU) · `scu_swu_reduction` (7 SWUs, one coherent doc/step each) · `recomposition_proof` (→ freeze gate) · `residue_ledger` (below). **No full dispatch JSON** — single-owner sequence. **Fan-out option:** R1→R6 are per-doc independent enough to dispatch one subagent each via `domainspec-subagents-strategy` (respecting the dependency order); that is a **task-session execution-mode choice**, not required by the plan.

## Distill validation — flag
- **Smallest coherent units:** ✅ one doc/step per SWU (R6 pre-split into R6a crosswalk + R6b split so neither is oversized).
- **Recomposition proof:** ✅ 7 SWUs green ⇒ 6 REFORMULATE rows done ⇒ freeze gate opens.
- **Gaps named (repair path):** (1) **R-trend-type** — DRIFT documents the surface; the `Stream<CheckResult>`+guardedness engine impl is separate → owner: validation/drift engine lane. (2) **moat-contract-only** — R4 documents the derive contract, never the δ-algorithm → enforced by the no-moat-leak check.
- **Verdict:** flag (routable — both gaps carried in the residue ledger below).

## Residue
- R-trend-type: drift's engine realization (`Stream<CheckResult>` + guardedness) is not in this pack.
- Moat boundary: TEST-PIPELINE is contract-only; `src/rules` stays private.
- The `sample` feature fixture is a test surface; real feature packs are separate work (makes C10 non-vacuous).

## Freeze gate
When R1–R6b are green AND the build-proof stays green, `implementation/domainspec/` becomes a FROZEN
evidence source (`IMPORT-MANIFEST.md` Freeze gate). Until then v1 stays readable, not edited.

## Next route
`task-session` per SWU, **R1 first** (L0 foundation). Solo or fan-out is the task-session decision (both
supported — see dispatch trace). Batch 2's reformulation-pending items (validator retarget already done in
G3; waiver reset; code-tag→drift binding) are a **sibling** work-pack, not in this pack.
