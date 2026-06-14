# BUILD-SPEC — Capital Logic Library

- Node: `capital-logic-library` (Craft ID `CTX-CLL-ROOT`)
- Workstream: D — Capital Logic Content (`docs/golden-quill-task-role-breakdown-handoff.md` rows 62–65)
- Status: **planning / spec only** — no executable code, no runtime stages, no `orgs/` reads
- Source of truth for canonical CIC/CLC architecture: project `CLAUDE.md` (Eight Capital Logic Cards · Six Customer Identity Categories · CIC×CLC orthogonality · `F-CIC-CLC-COUPLING-VIOLATION`). **This spec consumes that architecture; it does not mutate it.**
- Refine inputs: `RESEARCH-RESULT.md`, `.craft/ledger.yml`, `REFINE-DISPATCH.json` (run `2026-06-12-craft-pipeline-hydration`)

This file is the implementation-ready BUILD-SPEC for the two REFINE-SOLVABLE gaps that can be authored now. It carries Define → Design → Plan + acceptance criteria + first steps for each, an operator-input callout for the two gaps that require Josh, and the guardrails that bind every section.

---

## 0. Scope contract (read first)

**In scope to author now (Vlad-buildable schema/structure):**
1. `GAP-CLL-RULE-PACKS` — rule-pack schema + ownership/maintenance shape.
2. Card schema + governance structure (handoff row 62) — card schema + section-level defaults + testability rules.

**Out of scope (operator/external; listed as callout, NOT fabricated here):**
- `GAP-CLL-DOMAIN-EXPERTS` (block) — contracting four paid segment experts. Founder onboarding action.
- `GAP-CLL-LAUNCH-CARDS` (flag) — authoring/validating five launch cards + per-card status. Founder + domain-expert content.

**Rule content vs. schema.** Everywhere below, the **schema/structure is Vlad-authorable now**; the **content that fills it** (rule bodies, card text, segment source lists, per-card status) is operator/external and is explicitly fenced off. Authoring the schema does not author the content.

---

## GUARDRAILS (bind every section — non-negotiable)

- **G1 — No CIC→CLC coupling, anywhere.** No schema field, default, enum, validation rule, example, or rule pack may bind a Customer Identity Category to a subset of Capital Logic Cards, or vice versa. CIC and CLC are orthogonal axes; any (CIC × CLC) pair is reachable. Matching is **opportunity-driven at runtime**, never archetype-driven at design time. Any schema construct that could express "this CIC only uses these CLCs" is a category error and MUST fail closed under `F-CIC-CLC-COUPLING-VIOLATION` (architecture v7.0.8). This includes the legacy "Primary Capital Logic Activations" footer band — schemas authored here MUST NOT reintroduce it as a binding; if surfaced at all it is relabeled "Common patterns observed historically — not a constraint."
- **G2 — Law 3 (Org Isolation).** This node never reads, writes, or references anything under `orgs/`. Rule packs and cards are funder-side / archetype-side public artifacts. No client PROJECT_CONTEXT data enters a card or a rule pack.
- **G3 — Closed CLC set.** All capital-logic references resolve to the canonical eight CLCs in `TILTH-CLC-00`. No ninth card, no aliases promoted to first-class cards.
- **G4 — Planning/spec only.** This BUILD-SPEC produces schema definitions, governance shapes, acceptance criteria, and first-step direction. It does not write executable modules, does not run Refine runtime stages, and does not promote inventory/ontology/sigil/spell artifacts. Promotion-governance state (`[repo-root] .craft/ledger.yml`) is owner-boundary protected.
- **G5 — Law 1 / Law 5 alignment for rule content.** Rule-pack content (when later authored by operator) traces to a funder's actual RFA/program page (Law 1, source of truth). Schema MUST carry a mandatory provenance field so no rule can exist without a citable source. Cards shape existing substance; they never fabricate (Law 5).
- **G6 — Sector enum is not the archetype layer.** The internal six-sector enum (workforce / education / regen_ag / urban_ag / land_community / eco_art) is a separate, still-open taxonomy. Card/rule-pack schema MUST NOT silently rename or remap it; it may reference it only as an optional internal tag pending operator decision.

---

## 1. GAP-CLL-RULE-PACKS — rule-pack schema + ownership/maintenance shape

Owner: Vlad (schema) + Josh (content + maintenance-ownership decision). Severity: flag. Treatment: plan.

### 1.1 Define

A **rule pack** is a versioned, funder-scoped set of **codified hard requirements** for a recurring funder/program — the deterministic, non-negotiable constraints an application must satisfy (eligibility gates, format constraints, deadline structure, required attachments, page/word limits, match/cost-share requirements). Rule packs are **funder-side** artifacts that feed Logician-style deterministic checks; they are not draft content and not scoring rubrics.

- **What it is NOT:** not a rubric (that is Judge's domain), not a CLC card, not a CIC card, not draft prose, not client data.
- **Relationship to CLC:** a rule pack belongs to a *funder/program*. The CLC that an opportunity activates is determined at runtime by Scout/Logician (opportunity-driven). A rule pack MAY record which CLC(s) a given program historically expressed **only as observed, non-binding metadata** — it MUST NOT constrain which CIC may apply (G1).
- **ONGOING marker:** rule packs decay (funders change RFAs annually). The schema must carry the metadata that makes a maintenance cadence enforceable; the cadence decision itself is operator-owned (see callout).

### 1.2 Design — rule-pack schema (authorable now)

Proposed schema, one file per funder-program, stored under a library path **outside `orgs/`** (e.g. `pipeline/capital_logic/rule_packs/<funder_slug>/<program_slug>.yaml`). Fields:

| Field | Type | Req | Notes |
| --- | --- | --- | --- |
| `rule_pack_id` | str (slug) | yes | `<funder_slug>__<program_slug>__<fy>` |
| `funder_name` | str | yes | Display name |
| `program_name` | str | yes | Display name |
| `fiscal_year` / `cycle` | str | yes | The cycle this pack codifies; packs are per-cycle (decay unit) |
| `schema_version` | str (semver) | yes | Of the rule-pack schema itself |
| `source_provenance` | object | yes | **G5** — `{source_type: rfa\|program_page, url_or_handle, retrieved_date, quote_or_section}`. No rule without a citable source. |
| `requirements[]` | list[Requirement] | yes | The codified hard requirements (below) |
| `observed_clc_tags[]` | list[enum(CLC-8)] | no | **Non-binding** observed CLC(s); G1/G3. Label: "observed, not a constraint." MUST NOT reference any CIC. |
| `maintenance` | object | yes | `{review_cadence, last_reviewed, next_review_due, maintainer_role, status: current\|stale\|retired}` — see 1.3 |
| `status` | enum | yes | `draft \| active \| stale \| retired` |
| `signoff` | object | no | Operator attestation handle (reserved; aligns with future Ed25519 register discipline) |

**Requirement** sub-schema (the testable unit):

| Field | Type | Req | Notes |
| --- | --- | --- | --- |
| `req_id` | str | yes | Stable within pack |
| `kind` | enum | yes | `eligibility \| format \| deadline \| attachment \| limit \| match_cost_share \| registration \| other` |
| `statement` | str | yes | Human-readable hard requirement |
| `check_shape` | enum | yes | `boolean \| numeric_bound \| date \| set_membership \| presence` — the deterministic check class (so Logician can later realize it) |
| `params` | object | cond | Bound values for the check (e.g. `{max_pages: 15}`, `{deadline: 2026-09-01}`) |
| `severity` | enum | yes | `hard_fail \| warn` — hard requirements default `hard_fail` |
| `evidence_ref` | str | yes | Pointer into `source_provenance` quote/section (G5) |
| `clc_binding` | — | **FORBIDDEN** | **No field may bind a requirement to a CIC or constrain CIC eligibility (G1). Linter rejects any such field.** |

### 1.3 Design — ownership + maintenance shape (the ONGOING answer)

- **Maintainer role:** "Capital Logic Library maintainer." Today resolves to Founder (editorial) + Backend Engineer (schema/tooling) — Josh + Vlad. The schema records `maintainer_role` symbolically so the resolution can change without schema edits (mirrors the After-Acceleration "expert bench expansion" horizon, handoff row 93).
- **Cadence primitive:** every pack carries `review_cadence` + `next_review_due`. A pack whose `next_review_due` is past flips `status: stale` (deterministic, computable). A pack for a retired program flips `status: retired`.
- **Decay enforcement:** staleness is computed, not asserted — this is the lever that makes the ONGOING marker auditable. (Cadence *value* and *who owns recurring review* is the operator decision below; the *mechanism* is authored here.)
- **Promotion boundary (G4):** rule packs are library content, not promotion-governance state. They link to, never mutate, the root ledger.

### 1.4 Acceptance criteria

- [ ] Schema defines rule-pack + Requirement structures with all `yes`-required fields and closed-set enums above.
- [ ] Schema carries mandatory `source_provenance` on the pack and `evidence_ref` on every requirement (G5).
- [ ] Schema has **no** field — and the linter actively rejects any field — that binds a requirement/pack to a CIC or constrains CIC eligibility from a CLC (G1; fail-closed under `F-CIC-CLC-COUPLING-VIOLATION`).
- [ ] `observed_clc_tags` is optional, draws only from the canonical eight (G3), is labeled non-binding, and never references a CIC.
- [ ] `maintenance` block supports deterministic `stale` computation from `next_review_due`.
- [ ] One worked **schema example** (synthetic funder, NOT a real client, NOT fabricated rule content presented as authoritative) validates against the schema and demonstrates a `hard_fail` requirement with provenance.
- [ ] Storage path is outside `orgs/` (G2).
- [ ] A schema-conformance check exists (testability rule) that fails closed on: missing provenance, CIC-coupling field present, unknown CLC tag, missing `next_review_due`.

### 1.5 First steps

1. Author the rule-pack + Requirement schema (YAML/JSON-Schema or Pydantic model spec) at the library path; no executable wiring yet — schema definition + docstring only.
2. Write the conformance/testability rules (acceptance-criteria checklist as assertions) including the explicit anti-coupling assertion.
3. Produce one synthetic worked example to prove the schema round-trips.
4. Hand the maintenance-cadence-value + recurring-owner question to Josh (callout below); schema is complete without the answer because cadence is data, not structure.

---

## 2. Card schema + governance structure (handoff row 62)

Owner: Josh (governance/editorial) + Vlad (schema/testability). Effort: BUILD. No filed gap — this is a build task; schema authorable now, card *content* is GAP-CLL-LAUNCH-CARDS (operator).

### 2.1 Define

A **card** is the canonical machine-readable + governed representation of a CLC or CIC. Per `CLAUDE.md`:
- **CLC cards (8):** funder-side — *why/how funding flows* (underwriting logic, example sources).
- **CIC cards (6):** applicant-side — *what world the applicant operates in*. Each CIC configures five operational primitives: Search Vocabulary · Evidence Schema · Language Register · Reporting Rhythm · Capital Logic Activation; and carries a four-quadrant profile (Operating Reality · Tilth Configuration · Evidence Signals · Funding/Reporting Rhythm).

This task authors the **schema + section-level defaults + testability rules** that downstream Tilth components read. It does not author card text (that is the launch-cards operator gap). The PNG card assets at `assets/cards/` are the visual layer; this schema is the structured layer they must reconcile to.

### 2.2 Design — card schema (authorable now)

Two card families share a common envelope and diverge in body. Stored outside `orgs/` (e.g. `pipeline/capital_logic/cards/clc/<slug>.yaml`, `.../cards/cic/<slug>.yaml`).

**Common envelope:**

| Field | Type | Req | Notes |
| --- | --- | --- | --- |
| `card_id` | str (slug) | yes | e.g. `clc-public-purpose-works`, `cic-food-systems` |
| `card_family` | enum | yes | `clc \| cic` |
| `canonical_ref` | str | yes | Drawing ID — `TILTH-CLC-00` (CLC) or `TILTH-CIC-0N` / `TILTH-CIC-REVIEW-01` (CIC) |
| `display_name` | str | yes | From canonical naming in `CLAUDE.md` |
| `schema_version` | str (semver) | yes | Of the card schema |
| `status` | enum | yes | `draft \| in_authoring \| validated_v1 \| superseded` (drives per-card status capture, §3 callout) |
| `governance` | object | yes | See 2.3 |
| `asset_ref` | str | no | Path to PNG visual-layer counterpart under `assets/cards/` |

**CLC body** (the eight; closed set per G3):

| Field | Type | Req | Notes |
| --- | --- | --- | --- |
| `funding_logic` | str | yes | Why/how funding flows (underwriting logic) |
| `example_sources[]` | list[str] | yes | Illustrative funder/program classes (e.g. USDA RD, EPA) — examples, not bindings |
| `cic_binding` | — | **FORBIDDEN** | **No CLC card may enumerate which CICs it serves (G1).** |

**CIC body** (the six; closed set):

| Field | Type | Req | Notes |
| --- | --- | --- | --- |
| `coverage_axis` | str | yes | e.g. Production / Learning / Public Sector / Culture / Member Ownership / Intermediary Infrastructure |
| `includes[]` | list[str] | yes | Sub-world enumeration (the "Includes" band) |
| `operational_primitives` | object | yes | Five keys: `search_vocabulary`, `evidence_schema`, `language_register`, `reporting_rhythm`, `capital_logic_activation` — each a configuration block. **`capital_logic_activation` configures HOW the CIC processes whatever CLC an opportunity activates at runtime; it MUST NOT enumerate a CLC subset (G1).** |
| `four_quadrant_profile` | object | yes | `operating_reality`, `tilth_configuration`, `evidence_signals`, `funding_reporting_rhythm` |
| `primary_capital_logic_activations` | — | **FORBIDDEN as a binding** | The legacy footer band. If present at all, MUST be relabeled "Common patterns observed historically — not a constraint" and MUST NOT gate eligibility (G1). Default: omit. |

**Section-level defaults:** the schema carries archetype-level defaults per CIC for each operational primitive (e.g. default Language Register, default Reporting Rhythm) — these are the **Card-level archetype defaults** that the classification three-layer default chain (Card → operator override → per-grant SP0) reads. Defaults are configuration, never eligibility constraints across the CIC/CLC axes.

### 2.3 Design — governance structure

- **`governance` block per card:** `{owner_role, last_validated, validation_status, expert_reviewed: bool, expert_segment, version, change_log_ref}`.
- **Authority:** CLC/CIC *canonical naming and the orthogonality rule* live in `CLAUDE.md` and are owner-boundary protected (G4). This schema is the structured realization; it must conform to canon and cannot redefine it. Any schema change that touches canonical naming or the closed sets escalates to the operator, not authored here.
- **Validation lineage:** `expert_reviewed` + `expert_segment` connect to GAP-CLL-DOMAIN-EXPERTS — a card cannot reach `validated_v1` without recorded expert review for its segment (except Farmer, already v1). This makes the domain-expert block (§3) a structural gate, not just a note.
- **Visual/structured reconciliation:** schema is the source of truth for machine reads; PNG `asset_ref` is the human visual layer. Where the PNG shows a "Primary Capital Logic Activations" binding, the schema MUST NOT mirror it as a constraint (G1) — reconciliation is relabel-or-remove at regeneration.

### 2.4 Testability rules

- A card validates only if `card_family`/`canonical_ref` match a member of the correct closed set (8 CLC / 6 CIC).
- **Anti-coupling assertion (the load-bearing test):** no CLC card carries a CIC enumeration; no CIC card's `capital_logic_activation` enumerates a CLC subset as a constraint; no `primary_capital_logic_activations` binding is present. Violation → fail closed (`F-CIC-CLC-COUPLING-VIOLATION`).
- CIC card must define all five operational primitives and all four quadrant keys.
- `status` transition to `validated_v1` requires `governance.expert_reviewed == true` for the card's segment (Farmer exempt — already v1).
- No card references `orgs/` paths or client data (G2).

### 2.5 Acceptance criteria

- [ ] Common envelope + CLC body + CIC body schemas authored, with closed-set enforcement on both families (G3).
- [ ] Five operational primitives + four-quadrant profile modeled as required structure on CIC cards.
- [ ] Card-level archetype defaults modeled as the first layer of the classification three-layer default chain.
- [ ] Governance block present per card with validation lineage and expert-review gate.
- [ ] Anti-coupling tests authored and demonstrably fail-closed on a coupling-bearing fixture (G1).
- [ ] One CLC and one CIC **synthetic schema fixture** validate (structure only — not real card text, no fabricated authoritative content).
- [ ] Schema documents the PNG-reconciliation rule (relabel/remove the legacy footer band).
- [ ] Storage outside `orgs/` (G2).

### 2.6 First steps

1. Author the common envelope + the two body schemas (Pydantic model spec / JSON-Schema), closed-set enums sourced from `CLAUDE.md` canonical naming.
2. Author the governance block + status state machine (incl. the expert-review gate for `validated_v1`).
3. Author the testability suite, leading with the anti-coupling assertion and a coupling-bearing negative fixture.
4. Produce one synthetic CLC and one synthetic CIC fixture (structure-only) that validate.
5. Surface card *content* authoring + per-card status to Josh (callout §3) — schema ships without it.

---

## 3. OPERATOR-INPUT REQUIRED (callout — NOT fabricated)

> These gaps cannot be closed by Vlad or by research. They require Josh. Listed, not invented.

- **GAP-CLL-DOMAIN-EXPERTS [owner: Josh — BLOCK].** Four segment experts (Educator / Public Agency / Arts & Culture / Cooperative) need scoped **paid structured input + field correction** on their cards. Onboard form: contract, paid structured input (handoff rows 63 + 113). This is a **founder contracting/onboarding action**, not a research lookup and not authorable here. It structurally gates each non-Farmer card's path to `validated_v1` (§2.3). Recurring per After-Acceleration "expert bench expansion" (handoff row 93).
- **GAP-CLL-LAUNCH-CARDS [owner: Josh — FLAG].** Author + validate five launch cards (Farmer at v1; four in authoring) and **capture per-card current authoring/validation status** — content the handoff asserts only in aggregate. Founder + domain-expert content. The card schema (§2) provides the `status` field and governance block to *hold* this status once Josh captures it; the capture itself is Josh's.

**Also operator-owned (decisions, not blockers):**
- **Rule-pack maintenance cadence + recurring owner** (the ONGOING value behind §1.3): what `review_cadence` to set and who owns keeping recurring-funder packs current. Schema is complete without it (cadence is data); the decision is Josh + Vlad.
- **Deferred external-research classes (gate rg03, await Josh's approve/defer):** (1) segment source-universe lists, (2) recurring-funder rule references for rule-pack *content*, (3) expert-engagement scope norms. All bounded to public funder/program text; none read `orgs/` (G2). None are executed here.
- **Sector-enum reconciliation (G6):** whether the six-sector enum retires/persists/remaps under the archetype layer is an open operator decision; schema only optionally tags it.

---

## 4. Per-gap verdict lines

- `GAP-CLL-RULE-PACKS` — **REFINE-SOLVABLE (authored): Define→Design→Plan + acceptance criteria + first steps complete (§1).** Schema + ownership/maintenance shape authored; anti-coupling enforced (G1); rule *content* + cadence value fenced to operator.
- Card schema + governance (handoff row 62) — **REFINE-SOLVABLE (authored): Define→Design→Plan + acceptance criteria + first steps complete (§2).** Schema + section-level defaults + testability rules authored; anti-coupling enforced (G1); card *content* + per-card status fenced to operator.
- `GAP-CLL-DOMAIN-EXPERTS` — **OPERATOR-INPUT (block): not authored; founder contracting action (§3).**
- `GAP-CLL-LAUNCH-CARDS` — **OPERATOR-INPUT (flag): not authored; founder + domain-expert content; schema holds the status field (§3).**

---

## 5. Guardrail compliance attestation

- G1 (no CIC→CLC coupling): enforced as forbidden fields + load-bearing fail-closed tests in §1.2, §2.2, §2.4 (`F-CIC-CLC-COUPLING-VIOLATION`).
- G2 (Law 3): all storage paths outside `orgs/`; no client data in any card or pack.
- G3 (closed CLC set / 6 CIC): closed-set enforcement on both card families and on `observed_clc_tags`.
- G4 (planning/spec only): schema definitions + governance shapes only; no executable wiring, no Refine runtime execution, no promotion-governance mutation.
- G5 (Law 1/5 provenance): mandatory `source_provenance` / `evidence_ref`; no fabricated content.
- G6 (sector enum untouched): optional tag only; no silent rename/remap.
