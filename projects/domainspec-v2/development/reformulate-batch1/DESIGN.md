---
node_type: design
is_session: false
status: candidate
created: 2026-07-01
authored_by: invoke (mode: design)
work_pack: ./WORK-PACK.md
layering: ./implementation-layering.md
target_artifact: projects/domainspec-v2/impl/spec (6 Batch-1 REFORMULATE docs)
before_state_read: impl/spec/{AXIOMS,CONSTITUTION,DRIFT-CONVERGENCE,TAXONOMY,RELATIONSHIPS,TEST-PIPELINE}.md (verbatim v1)
governance_model: authority/AUTHORITY-MODEL.md (validation / layering / drift + μF/νF chain)
---

# Reformulate Batch-1 Spec Docs — Design

The **what-it-becomes** upstream of [WORK-PACK.md](./WORK-PACK.md). The work-pack says *how to execute +
validate*; this says *what the reformulated docs must BE* — so acceptance is "matches the target-result
below", not just "validator green" (which only proves well-formedness).

## 0. The core shift (why this is reformulation, not a path fix)

The v1 docs are organized around a **signal-emission + observer + Saturn-L-system** governance model:
AXIOMS A3–A6 (computable governance, observer independence, shift-left, feedback budget) and CONSTITUTION
C3/C4/C8/C9/C10/C11 (signal schema, dual observer, deterministic detectors, telemetry bundles, pruning,
M-001..M-006). v2 re-organizes **the same underlying material** around the **three ratified governances**
(`validation` / `layering` / `drift`) + the credibility meta + the μF/νF chain, with the engine as the
validation *method* and its δ-rules private.

So each doc is **re-homed to a governance owner**, de-duplicated against the credibility constitution, and
boundary-corrected — not rewritten from scratch. Nothing invents new domain content; the reformulation
moves existing content under the correct owner and makes the governance method runnable.

## 1. Architecture — target spec surface + governance binding

**Re-homing map (the spine):**

| Doc | v1 frame | v2 owner | Becomes |
| --- | --- | --- | --- |
| `TAXONOMY.md` | 25 meta-concepts + layer appendix | **layering** | The concept-type set + **layer-membership** feeding the layer-law; the type set `validate-code-tags` checks |
| `RELATIONSHIPS.md` | 29 allowed typed edges + registry | **layering** (law) + **validation** (check via C11) | The **edge-law**: allowed edges *plus the forbidden set made unconstructible* + endpoint signatures |
| `AXIOMS.md` | A1–A6 (signal/observer epistemics) | base + **layering** (A2) | A1→validation(derivation), A2→layering(adapter line), A3→"methods must be runnable", A4/A5/A6→drift |
| `TEST-PIPELINE.md` | doc-section→test-type rules | **validation** | The deterministic **derivation contract** (spec→obligations); the engine realizes it — **contract only, δ-rules private** |
| `DRIFT-CONVERGENCE.md` | 5 surfaces + Saturn | **drift** | The 5 drift surfaces + convergence-as-trend (C7) + Saturn-as-actuator; reconciled with the AUTHORITY-MODEL surfaces |
| `CONSTITUTION.md` | C1–C11 signal/observer rules | distributed | Each v1 C-rule → validation/layering/drift **or DROP**; this is the OQ-2 crosswalk |

**Composition (target v2 validation surface):** AXIOMS (foundation) → TAXONOMY+RELATIONSHIPS (layering:
what exists + what may connect) → TEST-PIPELINE (validation: what obligations derive) + DRIFT (drift: how
divergence is observed over time) → CONSTITUTION (the rules, distributed to the 3 governances). The engine
consumes TAXONOMY/RELATIONSHIPS + the feature packs; the validators (`validate-code-tags`,
`validate-relationships`, engine `lint`) enforce the layering + validation surfaces at build time.

**v1→v2 shift per governance:**
- **Layering** absorbs TAXONOMY + RELATIONSHIPS + A2. New: the **forbidden-edge law** (v1 only enumerates
  allowed edges; C6 requires forbidden edges to be *unconstructible*).
- **Validation** absorbs TEST-PIPELINE + A1. Boundary: documents the derivation *contract*, never the
  `src/rules` δ-algorithm (moat). The LLM test-generator is DROPPED (manifest).
- **Drift** absorbs DRIFT-CONVERGENCE + A4/A5/A6. Saturn = actuator, not authority (already v1-aligned).

## 2. Definitions ledger (what we reformulate) → `definitions-governance`

Load-bearing term sets each doc owns, tagged by reformulation action:

| Term set | Home doc | Action | Note |
| --- | --- | --- | --- |
| 25 meta-concepts (14 backend + 11 UI) | TAXONOMY | **reused** (verify each has a tracked ID) | UI-11 scope is a decision (§4-D2) |
| 29 typed edges (15+8+6) | RELATIONSHIPS | **reused + extended** | add forbidden-edge law + endpoint types |
| layer set + layer-dependency rule | TAXONOMY appendix | **reframed** → the layer-law (C6) | promote appendix rule to normative |
| A1–A6 axioms | AXIOMS | **reframed** → governance-bound | re-map "Governs: C*" to v2 owners |
| 5 drift surfaces + convergence | DRIFT | **reframed + reconciled** | reconcile with AUTHORITY-MODEL 5 (§4-D1) |
| v1 C1–C11 governance rules | CONSTITUTION | **crosswalked / dropped** | signal/observer rules → drift or DROP |
| obligation classes (transition/rule/calc/…) | TEST-PIPELINE | **reused** (contract only) | names, not the δ-algorithm |

Every term that survives must resolve to a tracked definition ID (credibility C(meta-4)); terms first cited
without one become `candidate` definitions via `definitions-governance`.

## 3. Per-doc target-result (before → after + semantic acceptance)

**R1 · AXIOMS** — *before:* A1–A6 each "Governs: C{n} in CONSTITUTION" (v1 signal/observer rules).
*after:* each axiom re-maps its "Governs" to a v2 governance owner (A1→validation, A2→layering/C6,
A3→runnable-method principle, A4/A5/A6→drift); the namespace note is folded in. *Semantic acceptance:* no
axiom points at a dropped v1 rule; A2 explicitly names the adapter-line = layering C6.

**R2 · TAXONOMY** — *before:* 25 concepts + a "Functional Style" layer appendix (non-normative).
*after:* concept-type set bound to layering; the **Layer Dependency Rule** promoted from appendix to the
normative layer-law; each concept carries its layer. *Semantic acceptance:* every concept type is one
`validate-code-tags` accepts; layer assignment ≠ dependency verdict (C6 wording preserved).

**R3 · RELATIONSHIPS** — *before:* 29 **allowed** edges + registry format. *after:* the allowed set
**plus an explicit forbidden-edge law** (which endpoint pairs are unconstructible) + endpoint type
signatures, **plus the catalog-coverage additions the toy T2b proved are missing**
(`../../research/spec-ontology-unification/toy/catalog.md` §C/§D): **R3-P1** add an `Operation→Entity`
read edge (or generalize `queries` to Behavioral→Entity); **R3-P2** add an `Operation→ValueObject`
(returns) edge; **R3-P3** resolve the Event payload+publisher composite (keep one node, or split
Structural payload / Connective publisher). *Semantic acceptance:* `validate-relationships` PASS at the
**new** canonical-edge count (**>29** — R3-P1/P2 add edges); a forbidden edge in a fixture is rejected as
*unconstructible*, not merely flagged (C6); C11 named as the check side; the two T1-found relations
(op-reads-Entity, op-returns-VO) now have a typed edge.

**R3 edge-law admissibility (build-from-owned — CAV2-D22 / D29 / D16).** An edge type is admissible only
if it adds a distinction *not silently redundant* with an existing axis (**CAV2-D22 orthogonal
classification**); the concept-type / relation-kind / composition-shape / feature-boundary axes stay
independent unless an explicit typed coupling relates them (**CAV2-D29 axis orthogonality** →
**CAV2-D16 typed coupling**). Operational test: **an edge earns its own type iff it composes into
different code.** Rulings: (a) `enforces` vs `applies` — **keep** (guard-vs-select is different code);
(b) `enforces` vs `enforces-cross` — **collapse candidate** (same code; make cross-feature a typed flag,
D16); (c) `queries` for `Calculation→Policy` — **reject** (redundant with `applies`; D22/D29); (d)
`applies : Policy → {Operation, Calculation}` — **widen** (endpoint generalization, no new label). Scope:
governance/classification orthogonality only — **not** Lean/Hilbert projector orthogonality (excluded from
cav2 authority). Recorded: `DEC-DSV2-EDGE-ADMISSIBILITY` in the v2 Craft ledger.

**R4 · TEST-PIPELINE** — *before:* doc-section→test-type rules + a payment example + `@source` traceability.
*after:* the deterministic **derivation contract** (which obligation classes derive from which spec
constructs) bound to validation (C5 from-spec, C10 completeness). *Semantic acceptance:* a reader can
predict the engine's obligation **classes** from the doc **without** seeing `src/rules`; **no δ-algorithm
detail present** (moat); the DROPPED LLM generator is not referenced as live.

**R5 · DRIFT-CONVERGENCE** — *before:* 5 surfaces (build-time / runtime / governance / tuning / closure)
citing v1 files (OBSERVABILITY, GOVERNANCE-SIGNALS, TUNING-LOOP, ADLC-ALIGNMENT, SATURN-L-SYSTEM).
*after:* 5 surfaces **reconciled** with the AUTHORITY-MODEL's (semantic / contract / runtime / governance /
coordination), bound to drift (C7), convergence = evidence-backed trend, write-authority proviso stated,
Saturn = actuator. *Semantic acceptance:* the surface set matches the AUTHORITY-MODEL (or the mismatch is
explicitly resolved per §4-D1); every cited doc resolves in v2 or is marked Batch-3/dropped.

**R6a · CONSTITUTION** — *before:* C1–C11 (signal/observer/pruning rules) mapped A{n}→C{n}→L6 gate.
*after:* a **v1→v2 crosswalk table**: each v1 C-rule → a v2 governance rule (validation/layering/drift) or
**DROP** with reason (e.g. C3/C8 signal-schema, C9 telemetry, C11 M-metrics likely → drift or DROP; C1→
validation; C2/C7→layering). *Semantic acceptance:* every v1 rule accounted for; no rule silently lost; no
overlap with the credibility constitution's rules; OQ-2 crosswalk closed. *(R6b then executes the
credibility-constitution per-governance split.)*

**R7 · DEFINITIONS (net-new — the migration's omission).** *before:* v1 had **no**
`impl/spec/DEFINITIONS.md` — the domain vocabulary lived under `research/projects/domainspec/definitions/`,
and the 6-doc Batch-1 set copied none of it (a real gap: TAXONOMY/RELATIONSHIPS *use* meta-types + verbs
with no definitions home). *after:* a **new** `impl/spec/DEFINITIONS.md` aggregating **DS-D1 meta-types**
(the 25 TAXONOMY types, from R2) + **DS-D2 edge verbs** (the RELATIONSHIPS edges, from R3) into typed
definitions with stable IDs, and serving as the **concept-registry-aggregation** home
(`definitions-governance` M2-C1). *Semantic acceptance:* every meta-type/verb TAXONOMY/RELATIONSHIPS use
resolves to a `DS-D*` definition (3-voice: formal + plain + domain-context); the concept-registry
aggregation can read it. **Owner:** `definitions-governance` — distinct from the *governance*-vocabulary
`DSV2-D*` already stood up in `authority/definitions/DEFINITIONS.md`. **Depends:** R2 + R3.

## 4. Design decisions surfaced (NOT decided here)

- **D1 — Drift-surface reconciliation.** DRIFT-CONVERGENCE.md's 5 surfaces (build-time/runtime/governance/
  tuning/closure) ≠ AUTHORITY-MODEL's 5 (semantic/contract/runtime/governance/coordination). Which is
  canonical? *Recommend:* AUTHORITY-MODEL is canonical (it's the ratified model); map the doc's surfaces
  onto it. **Owner decision.**
- **D2 — UI scope.** Keep the full 25 meta-concepts (incl. UI-11) as the v2 governance surface now, or
  scope the initial reformulation to backend-14 and defer UI? *Recommend:* keep 25 (they're already there +
  validated), but only backend needs the engine derivation. **Owner decision.**
- **D3 — v1-only file references.** DRIFT/CONSTITUTION cite OBSERVABILITY.md, GOVERNANCE-SIGNALS.md,
  TUNING-LOOP.md, SATURN-L-SYSTEM.md, ADLC-ALIGNMENT.md — none imported to v2 yet (ADLC is Batch-3; others
  may be drop/stub). *Recommend:* repoint to Batch-3 targets or mark "planned", don't leave dangling links
  (C9 link integrity would block).
- **D4 — Forbidden-edge law form.** How to express "unconstructible" in a Markdown edge-law the validator
  can check (an explicit forbidden table vs. a typed endpoint-signature the validator derives closure from).
  *Recommend:* endpoint-signature typing + a small explicit forbidden set; let `validate-relationships`
  compute admissibility. **Owner/validation-governance decision.**

## 5. Design → plan handoff

Each work-pack SWU's acceptance gains a **"matches §3 target-result"** gate on top of its validator. The 4
decisions above (D1–D4) are **pre-execution blockers for their specific SWU** (D1→R5, D2→R2, D3→R5/R6a,
D4→R3) — resolve each before that SWU runs. Distill verdict for the design: **flag** (usable; D1–D4 named
with owners + recommendations).
