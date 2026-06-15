# DomainSpec → Arcanum Wedge/Moat Seam Decisions

Date: 2026-06-12
Status: accepted
Decision source: `decision-gate` over the four seams escalated by dispatch `domainspec-into-arcanum-research-20260610`; user selected all four recommended options

## Scope

Resolves the four blocker-level seams that the integration research
([implementation/domainspec/development/arcanum-integration/research/domainspec-integration/README.md](../../implementation/domainspec/development/arcanum-integration/research/domainspec-integration/README.md))
could **not** auto-resolve and escalated to `decision-gate` (the `decision.wedge-vs-moat-split` output of step `s04`).

The bulk split was already resolved by rule: **free wedge → public `arcanum`; paid moat + runtime → private `implementation/domainspec`**, grounded in `implementation/domainspec/development/COMMERCIALIZATION-SYNTHESIS.md` (v0.2.0). These four seams decide what concretely crosses the public/private boundary, which is irreversible once published.

This record authorizes the **cut lines only**. Actual lifting remains gated behind `g03` (human approval per artifact), `g05` (moat protection), and submodule-first discipline. **No content has been moved.**

## Decisions

### D1 — Craft seam: **Schema only**

Publish the Craft ledger **schema** — the type/lane system and blocker-refinement discipline data model — to public arcanum. Keep **private**: role-delegation, scoring, generated index, hosted reflection, and **metering**.

- **Rationale:** §2 marks the ledger schema as the free wedge; §3 marks automation/metering as the paid meter ("bill on governed-run throughput"). The cut runs at the schema/automation seam.
- **Source:** README gray-zone 1; COMMERCIALIZATION §2/§3, R2.
- **Caveat:** Every monetizable Craft surface is currently **unbuilt** (R-CRAFT-1), so this is a design-time seam, not a code split yet. Hold the line when the automation is built.
- **Rejected:** "Schema + reference automation" (leaks the meter's shape); "Defer all Craft" (withholds a confirmed wedge).

### D2 — Spec→test seam: **Method + templates only**

Publish the spec→test **derivation method and templates** to public arcanum. Keep **private**: the LLM-driven engine and the Lean formal lever.

- **Rationale:** The derivation method is wedge; the engine re-anchors as the governance-data asset / Lean lever and is moat-adjacent.
- **Source:** README gray-zone 2; residue R1.
- **Caveat (R1):** v1 spec→test is **LLM-driven, not a deterministic compiler**, so the paid line re-anchors on the governance-data asset or the Lean lever — this is what keeps the engine private rather than the method.
- **Rejected:** "Method + deterministic reference engine" (more engine surface goes public); "Defer" (stalls the most demo-able wedge).

### D3 — Lean concepts: **Generic concepts only, plain-language**

Lift only attestation-**decoupled** engineering concepts, restated in plain language with the category-theory machinery dropped: typed residue, two-residue independence, declared-scope stopping (C7), regimes-of-residue typology, reflection-tower ↔ Arcanum mapping, subset rule (claim ≤ proof). Keep **private**: all formal-proof/attestation mechanism and the FF-threshold formalism insofar as it underpins the paid proof claim.

- **Rationale:** Lean is "the formal-proof half" of the paid attestation moat (§3/§9); lifting the attestation machinery would erode the moat (the `g05` block). The generic concepts reinforce the *free* legibility story (R-IB-1), not the paid proof engine.
- **Source:** README Part B; COMMERCIALIZATION §3/§9.
- **Discipline on any crossing concept:** plain-language restatement only; do **not** lift refuted `NOVEL-MAPPINGS.md` claims as settled; assign new IDs to avoid the `schema` term-collision with arcanum's existing `DEFINITIONS.md` (and the Lean/Spivak `schema` usage).
- **Rejected:** "Keep all Lean private" (forfeits free legibility reinforcement); "Broader lift incl. FF-threshold" (high moat-erosion risk).

### D4 — Host skill trees: **Regenerate via `arcanum-bootstrap`**

Treat the five host skill trees (`.claude` / `.agents` / `.codex` / `.github` / `copilot`) as **generated host installs** and regenerate them from `arcanum-bootstrap` rather than hand-migrating.

- **Rationale:** They are generated host installs, not authored source; regeneration avoids drift between hosts and committing authored-looking content that should be generated.
- **Source:** README gray-zone 4.
- **Blocking precondition (residue item 2):** verify `arcanum-bootstrap` / `copilot/install.sh` generator wiring **before** moving — generated-vs-authored ambiguity is the biggest coupling risk. Regeneration is the chosen *method*; the wiring check is a prerequisite to executing it.
- **Rejected:** "Hand-migrate" (risks authored/generated drift); "Defer until wiring verified" (subsumed — wiring verification is now a precondition of D4, not an alternative).

## Consequences / Next actions (each still gated by `g03` + `g05`)

1. **Lift the unambiguous wedge first** — taxonomy/relationships (`DS-D1`/`DS-D2` as canonical arcanum definition, prose `TAXONOMY.md` recomposed as the explanatory layer) + generic intent-tool sigils — with the R-IB-1 "relocate, don't reduce" framing baked in.
2. **Apply the four seams above** when lifting Craft (D1), spec→test (D2), and Lean concepts (D3).
3. **Verify generator wiring** (D4 precondition), then regenerate host trees.
4. **Quarantine the moat** — CyberAlchemy engine, Craft automation/metering, enforcement runtime, attestation product, Golden Quill/Tilth, the Lean formal-proof half, and the governance-attenuation definitions cluster (`DS-C3`/`DS-D9`/`DS-COR-1`, `DS-F1`/`DS-F5`/`DS-F6`, `DS-M13`) stay private.

## Carry-forward constraints

- **R-IB-1 (mandatory):** never market the wedge as "reduces human review" — it **relocates** review upstream and makes it cheaper, unskippable, legible.
- **R-IB-2:** the human owns the spec/intent ground truth; gates **add** friction at intent-critical points.
- **R-IB-3 / R-RT-2:** no public claim that these tools cut escaped intent bugs (no measurement yet); do not overclaim the SOC 2 / ITGC / SOX forcing function as statutory.

## Remaining blockers

None at the seam level — all four escalated blockers are resolved. Execution-time gates (`g03` per-artifact human approval, `g05` moat protection, submodule-first commit discipline) remain in force for the actual lift.

## Deferred / open (not blockers for the cut lines)

- The `arcana/` / `spells/` **sigil parity diff** is still open (Part C covered definitions only — those showed zero overlap, a clean first lift).
- Pick **one** public canonical home for the taxonomy so the lift does not create a third source of truth (DS already has two: `TAXONOMY.md` and the normative `DEFINITIONS.md`).
