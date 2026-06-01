# CANONICAL_NAMING_AND_ORTHOGONALITY_AUDIT

**Phase 2 of the Tilth Card System Deep Research run, 2026-05-17.**

| Field | Value |
|---|---|
| Filed | 2026-05-17 |
| Workspace | `/Users/goldenquill/Downloads/GoldenQuill/` |
| Scope | Canonical naming consistency + CIC/CLC orthogonality enforcement layers + the operator's v2.1 Law-5 reconciliation patch as an orthogonality-adjacent discipline. |
| Phase boundary | Continues directly from Phase 1 (`CARD_LIFECYCLE_AND_LOADER_GOVERNANCE_AUDIT.md`); feeds Phase 3 (`INITIAL_CTO_HANDOFF_BLOCKERS.md`) and Phase 8.1-5 (`FILE_BY_FILE_PATCH_QUEUE_PRE_V0_2.md`). |
| Authority | Same source set as Phase 1; additionally `pipeline/blueprint/v0.1/section_18_v1_2_amendment.md`, the dialect_routing_table on-disk state in all 6 CIC cards, the `funder_political_axis` grep tally, and the operator's v2.1 reconciliation patch as folded into the corrective. |
| Non-negotiable folded in from operator corrective | `common_funders_observed` is operator-confirmed engagement only (Law 5). Subagent-populated funders go under `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation`. This audit treats that as the schema-of-record Law-5 discipline and reports on its current enforcement posture. |

---

## §0. Findings summary (by severity)

| ID | Severity | One-liner | Surface | Detail § |
|---|---|---|---|---|
| L2-F0 | **P0** | §18 v1.2 amendment is LOCKED (frontmatter line 5: `LOCKED 2026-05-16T14:00:00Z`) but the CIC schema file on disk **still carries the retired four-axis political enum**. The amendment claims to have replaced `funder_political_axis` → `clc` + `dialect` + `register_description` + `example_program`. The schema has not been updated. 31 instances of `funder_political_axis` across 6 CIC cards + the CIC schema file remain. | amendment-vs-schema drift | §3.1 |
| L2-F1 | **P0** | None of the three multi-track CLC cards (CLC-05 market_access, CLC-06 credit_underwriting, CLC-07 sponsorship_corporate) actually carry a top-level `track_a:` / `track_b:` block on disk. The §18.6 v2 dual-track amendment is LOCKED + claims a post-restructure SHA3-512 hash per card per the master prompt §2.5/§2.6/§2.7, but the on-disk cards are still single-track shape. Grep for `^track_a:` / `^track_b:` in `pipeline/cards/CLC/`: zero matches. | amendment-vs-card drift | §3.2 |
| L2-F2 | **P1** | The CIC README at `pipeline/cards/README.md:9-11` defines BOTH layers as `**Cards**` — same word for visual + runtime. Per architecture v7.0.11 §1.1 (line 51-53) the canonical distinction is "Cards" (visual) vs "cards" (runtime, lowercase), but the README mojibake renders both `**Cards**` in bold without distinguishing them. A reader following the README cannot tell visual from runtime references. | README naming collision | §4.1 |
| L2-F3 | **P1** | Customer Identity Cards (canonical) vs Customer Information Cards (legacy/working-name) — the operator's working artifact and the master prompt §0 line 4 use both. The OD-C value-position regex (per §4 v2.x.7) catches `[Cc]ustomer [Ii]dentity` but NOT `[Cc]ustomer [Ii]nformation`. A regression test for the legacy phrase landing in a card body would not fire. | regex coverage gap | §4.2 |
| L2-F4 | **P1** | The OD-C value-position regex itself is documented in the §4 v2.x.7 amendment as live in the gate body, but the gate body on disk raises `NotImplementedError` (cross-ref L1-F3 Phase 1). The orthogonality enforcement on `TILTH-CIC-\d{2}` / `TILTH-CLC-\d{2}` / `[Cc]apital [Ll]ogic` / `[Cc]ustomer [Ii]dentity` value-position literals is **not active at runtime today.** Only the loader-time field-name scan is live. | enforcement gap | §5.4 |
| L2-F5 | **P1** | The operator's v2.1 Law-5 reconciliation (operator-confirmed engagement only on `common_funders_observed`; subagent-populated candidates routed under `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation`) is **applied uniformly across the 6 CIC cards** (good) but is **NOT applied across the 8 CLC cards**. CLC cards either have populated top-level `common_funders_observed` lists or omit the field entirely; the Law-5 split is CIC-only. Schema does not enforce the discipline on either axis. | Law-5 enforcement asymmetry | §6 |
| L2-F6 | **P2** | The CIC + CLC schemas both declare `additionalProperties: true` at root (`card_cic.schema.json:594`, `card_clc.schema.json:415`). Combined with the `not.anyOf` forbidden-field-name block, the schemas catch the named forbidden fields but accept any other unknown top-level field. A typo-renamed forbidden field (e.g., `eligible_clc_subsett` — extra 't') would pass. This is a defense-in-depth weakness the FORBIDDEN_FIELD_REGISTRY can't close on its own. | schema laxity | §5.2 |
| L2-F7 | **P2** | Six CIC cards still carry 31 `funder_political_axis` occurrences (5 in cooperative/arts_culture/public_agency/educator/ecosystem_intermediary, 4 in food_systems, 2 in the CIC schema). Per FI-9 REVISED in the §18 v1.2 amendment (lines 209): the rewrite is **content-judgment-driven; NO political-axis-to-CLC table** (operator pushback: "any heuristic mapping re-encodes the retired axis"). Burden estimate from the amendment: 3-5 hours per card × 6 cards = 18-30 hours operator review at cards-ceremony. This work is pending. | operator backlog | §3.1 |
| L2-F8 | **P2** | The `f_cic_clc_coupling_violation.py` gate (the v7.0.8 progenitor) is LIVE with four detection layers, but uses different conventions than `f_cards_coupling_violation_extension.py` (the v7.0.11 successor) — the former returns `CouplingFinding` dataclasses with `subcode` like `F-CIC-CLC-COUPLING-VIOLATION.layer1_lexical`; the latter is meant to return `GateOutcome` with `sub-tag` like `.value_literal_clc_slug`. Two parallel coupling-gate vocabularies. CTO clarity benefit if they converge. | gate vocabulary fork | §5.3 |
| L2-F9 | **P2** | The schemas' `coverage_axis` enum (`["Production", "Learning", "Public Sector", "Culture", "Member Ownership", "Intermediary Infrastructure"]`, CIC schema `card_cic.schema.json:60-66` + `models.py:47-54`) reads like one-to-one CIC → coverage_axis. If that's the intent, it should be a derived field, not stored. If it's many-to-one, the docs should clarify. | minor naming clarity | §4.3 |

---

## §1. Scope, sources, methodology

This audit reads naming + orthogonality discipline across the same surfaces as Phase 1, plus:

- All 6 CIC cards' `dialect_routing_table:` blocks (where `funder_political_axis` lives).
- All 6 CIC cards' `common_funders_observed:` top-level block and `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` nested block (to confirm the operator's v2.1 Law-5 split status).
- All 8 CLC cards' `common_funders_observed:` block (or absence thereof).
- The §18 v1.2 amendment's claimed schema delta (`section_18_v1_2_amendment.md:56-140`).
- The §4 v2.x.7 amendment's claimed value-position regex spec (`section_04_v2_x_7_card_coupling_value_position_amendment.md:108-120`).
- The `f_cic_clc_coupling_violation.py` v7.0.8 gate body (LIVE).
- The `f_cards_coupling_violation_extension.py` v7.0.11 gate body (STUB).

Out of scope: dialect substance, register substance, admin-risk register consolidation (Phase 7 surface), per-card research currency (Phases 4-CIC + 4-CLC).

---

## §2. Canonical naming — what's the agreed vocabulary?

Architecture v7.0.11 §1.1 line 51-53:

> A **Card** is a signed, versioned, machine-readable knowledge artifact ... One card per Card. Cards live under `pipeline/cards/` on disk per §18 directory layout.
>
> A **Card** is the human-readable visual asset; a **Card** is the machine-readable runtime artifact. The naming distinction is load-bearing: any code path, prompt, or seat instruction that says "load the Card" is structurally wrong — it must say "load the Card."

This text is itself broken in the canonical bytes — the visual/runtime distinction collapses because both surfaces are written identically as "Card" / "Cards" without a typographic disambiguator. The README at `pipeline/cards/README.md:9-11` carries the same collision:

```
**Cards** = visual / conceptual layer (human-readable; PNGs at `assets/cards/customer_identification/` + `assets/cards/capital_logic/`).
**Cards** = runtime layer (machine-readable; this directory).
```

Identical bold-`**Cards**` text for both. Reading order is the only disambiguator. The naming-discipline claim ("load-bearing") cannot be honored when the rendered text doesn't distinguish.

The **other** canonical axis pair — Customer Identity Cards (CIC, canonical) vs Customer Information Cards (legacy / working-name) — is documented at `pipeline/cards/README.md:7`:

> **Customer Identity Cards** is the canonical repo term; **Customer Information Cards** is legacy / working-language only.

And the master prompt at `docs/cic_clc_unified_master_prompt_2026-05-17.md:14` (§1):

> The operator's working artifact uses "Customer Information Cards" as a working name. The canonical repo terminology — used everywhere in the codebase, schemas, gates, and blueprint — is **Customer Identity Cards (CIC)** and **Capital Logic Cards (CLC)**.

The two-name posture is settled in prose. The enforcement posture is partial (§4.2 below).

---

## §3. Amendment-vs-on-disk drift

### §3.1 §18 v1.2 — the dialect_routing_table re-keying (L2-F0, L2-F7)

The §18 v1.2 amendment frontmatter (line 5):

> amendment_status: LOCKED 2026-05-16T14:00:00Z. L-005 strict two-cycle Thesis CLOSED ...

The amendment's §1.4 (lines 65-140) gives the explicit schema delta — drop `funder_political_axis`; add `clc` + `dialect` + `register_description` + `example_program` (the FI-6 Cycle 1 fold-in at line 208 renamed `register` → `register_description`); preserve `dialect`; require `[clc, dialect, register_description]`; ban `funder_political_axis` via `additionalProperties: false` (FI-5 Cycle 1 fold-in at line 207 removed the `not: required[funder_political_axis]` clause as ineffective).

The amendment's `companion_code_landed_at_LOCK` (lines 16-23) explicitly enumerates the schema patch and the six CIC card patches.

**On-disk reality.** The CIC schema at `pipeline/cards/_schema/card_cic.schema.json:208-274`:

```json
"dialect_routing_table": {
  "type": "array",
  "description": "Funder-political-axis to Scribe-dialect mapping. ...",
  "items": {
    "type": "object",
    "required": [
      "funder_political_axis",
      "dialect"
    ],
    "properties": {
      "funder_political_axis": {
        "type": "string",
        "enum": [
          "conservative",
          "centrist",
          "progressive",
          "soul_fire"
        ]
      },
      "dialect": { "type": "string" },
      "example_funder": { "type": "string" }
    },
    "additionalProperties": true,
    ...
  }
}
```

The schema is still v1.1 shape: `required: [funder_political_axis, dialect]`, with the four-axis enum present and `clc` / `register_description` / `example_program` absent. The required-vs-v1.2 delta is byte-for-byte the "Before" block in `section_18_v1_2_amendment.md:67-88`, NOT the "After" block at lines 90-140.

The six CIC cards still carry `funder_political_axis: "<axis_value>"` rows in their `dialect_routing_table:` blocks. Per the grep tally (`Grep` `funder_political_axis` in `pipeline/cards`):

| File | Occurrence count |
|---|---|
| `CIC/food_systems.yaml` | 4 |
| `CIC/educator.yaml` | 5 |
| `CIC/public_agency.yaml` | 5 |
| `CIC/arts_culture.yaml` | 5 |
| `CIC/cooperative.yaml` | 5 |
| `CIC/ecosystem_intermediary.yaml` | 5 |
| `_schema/card_cic.schema.json` | 2 |
| **Total** | **31** |

Sample evidence from `pipeline/cards/CIC/food_systems.yaml:326-338`:

```yaml
dialect_routing_table:
  - funder_political_axis: "conservative"
    dialect: "scribe.formal_commercial"
    example_funder: "USDA Rural Development ..."
  - funder_political_axis: "centrist"
    dialect: "scribe.technical_precise"
    ...
  - funder_political_axis: "progressive"
    ...
  - funder_political_axis: "soul_fire"
    ...
```

**Diagnosis.** The §18 v1.2 amendment's own frontmatter (line 5, last sentence) explains: *"Cards + admin_risk_register re-sign + Wave 2 LOCK deferred to separate ceremony per operator-confirmed Option B split (22-36 hour pre-ceremony operator work required first)."* The deferral is intentional — the LOCK was on the amendment text + the architecture/v1.2/§4 v2.x apolitical_dialect/§0.5 v28 compound, but the actual schema delta + 6-card patches were deferred to a separate "cards-ceremony" that has not yet fired.

Per FI-9 REVISED (line 209): *"Operator reads each existing routing row's dialect content + example_funder text + decides which CLC slug captures the funder cluster THIS row served. No reference to the old `funder_political_axis` value should appear in the new row. Burden estimate: 3-5 hours per card × 6 cards = 18-30 hours operator review at cards-ceremony."*

**This is the largest deferred backlog item from the §18 v1.2 ceremony.** Until the cards-ceremony fires, the repo is in a half-LOCKed state: the amendment-of-record says one thing, the schema + 6 cards say another. The downstream consequence: any seat that reads `dialect_routing_table` (Scribe in particular) is keying on the retired political axis. The `funder_political_axis` enum is currently the binding runtime routing primitive even though the amendment says it should not be.

**Recommended remediation** (full ceremony shape in Phase 8.1-5):

1. Operator dispatches the cards-ceremony to do the per-row content-judgment re-keying (the 18-30 hour work).
2. Patch `pipeline/cards/_schema/card_cic.schema.json` with the "After" block from `section_18_v1_2_amendment.md:90-140`.
3. Patch all 6 CIC cards' `dialect_routing_table:` blocks.
4. Re-sign 6 CIC cards (supersession-re-sign per OD-C/OD-E precedent).
5. Update `pipeline/seats/scribe/dialect.py` + `pipeline/engineering/agents/references/dialect_codebook.yaml` (cited at `section_18_v1_2_amendment.md:59`) — these read from the old axis and need re-wiring.

### §3.2 §18.6 v2 — the dual-track restructure (L2-F1)

The master prompt §2.5 line 244 claims:

> Card file: `pipeline/cards/CLC/market_access.yaml` (Wave 2 LOCKED 2026-05-16 row 258; superseded post-OD-E restructure at row 276, 2026-05-17T16:00:00Z; post-restructure SHA3-512 = `4eb75e9296cffdf658f313614e6cd7730acafc1f471b69c59b48304506f2ec23cf8455a28cbe6c49583ca292f2983bfc10bf4b9ac2d11b12c3078022428be55e`).

And §2.5 line 245:

> §18.6 v2 LOCKED row 274: top-level `track_a` (sbir_phase_ii) + `track_b` (sbir_phase_iii). Shared root metadata stays at root.

Similarly for CLC-06 credit_underwriting (master prompt §2.6 line 277-278: post-restructure SHA3-512 `bc050602…fca6ce9`) and CLC-07 sponsorship_corporate (§2.7 line 306: `58b61e03…dbe79e3b`).

**On-disk reality.** Grep `^track_a:|^track_b:` in `pipeline/cards/CLC/`: **zero matches.** Grep `^_partition_provenance:` (the master prompt mentions `_partition_provenance.domain_clarification` on credit_underwriting): zero matches.

Spot-check `pipeline/cards/CLC/credit_underwriting.yaml:41-52`:

```yaml
schema_version: "1.0-clc"
card_axis: "CLC"
card_id: "TILTH-CLC-06"
slug: "credit_underwriting"
display_name: "Credit & Underwriting"
funding_mechanism_summary: "Loans, guarantees, and credit-readiness funding ..."
tilth_clc_id: "TILTH-CLC-06"

# ---------------------------------------------------------------------------
# UNDERWRITING CRITERIA — what reviewers evaluate (per §18.10 starter content)
# ---------------------------------------------------------------------------
underwriting_criteria:
  - criterion: "repayment_capacity"
    ...
```

This is the single-track shape from §18 v1, not the §18.6 v2 dual-track shape that the master prompt claims is on disk.

**Diagnosis.** Same pattern as L2-F0. The §18.6 v2 amendment LOCKed on paper but the companion card-restructure ceremony either did not fire or was rolled back. The CLC schema at `pipeline/cards/_schema/card_clc.schema.json` was not read end-to-end for this audit but the snippet I read (lines 230-372 lifecycle block + lines 380 _research_metadata block) does not show top-level `track_a` / `track_b` / `$defs.track_container` / a `oneOf` branch — the schema is also still single-track shape.

**Recommended remediation:** in the cards-ceremony that lands §18 v1.2, also land §18.6 v2: patch the CLC schema, patch the 3 multi-track CLCs (CLC-05, CLC-06, CLC-07), re-sign each. CLC-06 Track B stays minimal-stub per the operator's L-024 directive (master prompt §6 lines 422-430).

### §3.3 §4 v2.x.7 — the value-position regex (cross-ref L1-F3)

Already documented in Phase 1 §6.3 (L1-F3). Summary for completeness: the §4 v2.x.7 amendment claims the predicate body was graduated to LIVE with field-name + value-position + matrix-structural scanners. The on-disk gate body is the pre-graduation stub. The compensating control — `loader.py`'s `enforce_no_forbidden_coupling` — covers only the field-name layer.

**Three amendments, three drifts.** §18 v1.2, §18.6 v2, and §4 v2.x.7 all carry `LOCKED` frontmatter but their on-disk companion code/schema/cards are in pre-LOCK state. Pattern suggests a workflow gap: amendments are being LOCKed before the companion-code ceremony fires.

---

## §4. README + display-name discipline

### §4.1 The Cards/Cards naming collision (L2-F2)

`pipeline/cards/README.md:9-11`:

```
**Cards** = visual / conceptual layer (human-readable; PNGs at `assets/cards/customer_identification/` + `assets/cards/capital_logic/`).
**Cards** = runtime layer (machine-readable; this directory).
```

Both layers rendered as `**Cards**`. The README's own intent (per the prose at architecture v7.0.11 §1.1) is to use `Card` (capitalized) for visual and `card` (lowercase) for runtime, but the README rendering doesn't preserve that. Two fix options:

1. **Edit the README** to use distinguishable typography: e.g., `**Cards** (visual layer, capital C)` vs `**cards** (runtime layer, lowercase c)`. Minor cosmetic edit; documentation-only.
2. **Adopt a new disambiguating term** for one of the layers. Common pattern: keep "Card" for the conceptual artifact, and use "card cartridge" or "card YAML" or "runtime card" for the machine-readable artifact. Heavier doctrinal change.

Architecture v7.0.11 §1.1 also has the same collision, so the fix should propagate to the architecture amendment text. Document-only edit at the architecture layer; no LOCK ceremony required (the amendment doesn't change behavior or signatures).

### §4.2 Customer Identity vs Customer Information (L2-F3)

Per `pipeline/cards/README.md:7` and master prompt §1: "Customer Identity Cards" is canonical; "Customer Information Cards" is legacy.

The §4 v2.x.7 value-position regex set (per amendment lines 108-120, which the gate body should but does NOT enforce — see L1-F3) covers:

```python
_VALUE_POSITION_PATTERNS = (
    ("value_literal_cic_slug", re.compile(r"TILTH-CIC-\d{2}")),
    ("value_literal_clc_slug", re.compile(r"TILTH-CLC-\d{2}")),
    ("value_literal_capital_logic_phrase", re.compile(r"[Cc]apital [Ll]ogic")),
    ("value_literal_customer_identity_phrase", re.compile(r"[Cc]ustomer [Ii]dentity")),
)
```

The pattern `[Cc]ustomer [Ii]dentity` catches the canonical phrase but NOT the legacy phrase `[Cc]ustomer [Ii]nformation`. A researcher (or a Cycle-1 fold-in author) who slips back into "Customer Information Cards" in a card body would NOT be caught by the value-position scan even when it's wired up.

This is symmetric with the canonical name — the regex protects against drift toward the canonical name only when the canonical name is the *forbidden* surface. Since the canonical name itself is forbidden in value positions (exempt-paths aside), the regex is correct for the canonical form. The legacy form is not currently in any card body (no grep hits for "Customer Information" in `pipeline/cards/`) so the gap is theoretical rather than active. Adding a `[Cc]ustomer [Ii]nformation` pattern is cheap defense-in-depth.

Recommend: when the §4 v2.x.7 gate body graduates (see L1-F3 patch), include `[Cc]ustomer [Ii]nformation` in the pattern set under sub-tag `.value_literal_customer_information_legacy_phrase`. Tag it as a legacy-phrase defense rather than a coupling-discipline defense.

### §4.3 coverage_axis enum laxity (L2-F9)

`card_cic.schema.json:57-67` declares `coverage_axis` with enum `["Production", "Learning", "Public Sector", "Culture", "Member Ownership", "Intermediary Infrastructure"]`. `models.py:47-54` mirrors this in `COVERAGE_AXES`. The README and the architecture amendment never explicitly name the six entries.

Looking at the 6 CIC cards' `coverage_axis:` values (spot-check via `food_systems.yaml:36 coverage_axis: "Production"`):

- food_systems → Production
- educator → Learning (probable)
- public_agency → Public Sector (probable)
- arts_culture → Culture (probable)
- cooperative → Member Ownership (probable)
- ecosystem_intermediary → Intermediary Infrastructure (probable)

It's 1:1. Six CICs, six coverage_axis values. Why is this a stored enum and not a derived field? If the operator ever introduces a 7th CIC, they'd have to update both the slug enum AND the coverage_axis enum. The slug already implies the coverage_axis.

Recommendation: either (a) make `coverage_axis` derived (drop from schema; loader infers from slug; saves a possible source of drift), or (b) explicitly document that it's a 1:1 lookup for human readability and accept the redundancy. Either way, document. This is a P2 minor; not blocking.

---

## §5. CIC/CLC orthogonality enforcement layers

The architecture's orthogonality discipline (per v7.0.11 §6.1 + v7.0.8 + §4 v2.x.7) is meant to prevent CIC bodies from encoding CLC preferences and vice versa. There are **five distinct enforcement layers** at varying maturity.

### §5.1 Layer 1 — Schema-level top-level forbidden-field block

`pipeline/cards/_schema/card_cic.schema.json:555-593` declares a top-level `not.anyOf` that forbids the 7 CIC-side coupling field names:

```json
"not": {
  "anyOf": [
    { "required": ["common_clc_patterns_observed"] },
    { "required": ["eligible_clc_subset"] },
    { "required": ["clc_allowlist"] },
    { "required": ["clc_denylist"] },
    { "required": ["preferred_clcs"] },
    { "required": ["clc_win_rate"] },
    { "required": ["clc_ranking_preferences"] }
  ]
}
```

Symmetric in `card_clc.schema.json:381-413` for the 6 CLC-side forbidden fields.

**Status: LIVE.** Any tool that runs JSON-schema validation against a card YAML (e.g., a `jsonschema` CLI invocation, a `pydantic` model construction, a downstream KFR signature flow that re-validates) catches the named forbidden top-level fields.

The 6+7 = 13 forbidden field names are also enumerated at `f_cards_coupling_violation_extension.py:32-53` as `_FORBIDDEN_FIELD_REGISTRY_RAW`, wrapped in `MappingProxyType` for immutability (line 53). The two sources are consistent — same 13 names.

### §5.2 Layer 2 — Schema-level nested-item forbidden-field block (L2-F6)

The CIC schema additionally embeds the `not.anyOf` block inside three nested item-array properties:

- `provenance_requirements.additionalProperties.not.anyOf` — `card_cic.schema.json:133-171`
- `dialect_routing_table.items.not.anyOf` — `card_cic.schema.json:235-273` (defense-in-depth even though item.required structure already constrains shape)
- `common_funders_observed.items.not.anyOf` — `card_cic.schema.json:339-377`

Symmetric in CLC schema for the 6 CLC-side names:

- `common_funders_observed.items.not.anyOf` — `card_clc.schema.json:140-173`
- `provenance_requirements.additionalProperties.not.anyOf` — `card_clc.schema.json:194-227`

This is the §18 v1.1 RT-02 fold-in (Cycle 2 defense-in-depth — per the master prompt §0 line 9 + §18 v1.1 amendment's `_research_metadata` references in the cards themselves). The intent: a creative renamer can't smuggle a forbidden field into a deeply nested item.

**Status: LIVE for the three specifically-blocked items.** Other items/objects in the schema are not covered — e.g., a forbidden field name nested inside `evidence_signals[*]` or `kfr_fact_classes[*]` is NOT blocked at the schema level. Layer 3 (loader recursive scan) covers those.

**Schema laxity at root.** Both schemas declare `additionalProperties: true` at root (`card_cic.schema.json:594`, `card_clc.schema.json:415`). The `not.anyOf` catches the specific 13 forbidden names but doesn't catch *renamed* coupling fields. A field named `eligible_clc_subsett` (typo) passes the schema. A field named `clc_eligibility_subset` (re-ordered) passes. Only Layer 3 (loader recursive scan) sees that, and only if the name is in FORBIDDEN_FIELD_REGISTRY.

This is a known limitation; the architecture trusts contributor discipline + the F-CIC-CLC-COUPLING-VIOLATION layer-2 Pydantic-AST scan + the eventual §4 v2.x.7 value-position regex. Document the trust boundary explicitly.

### §5.3 Layer 3 — Loader recursive field-name scan (LIVE)

`pipeline/cards/loader.py:309-344` (`enforce_no_forbidden_coupling` + `_find_forbidden_keys`) walks the entire parsed YAML tree, checks every dict key (including nested keys) against `FORBIDDEN_FIELD_REGISTRY[axis]`, and raises `CardCouplingError` with the dotted-path of the violating key on hit. Per the implementation at line 322:

```python
forbidden = FORBIDDEN_FIELD_REGISTRY[declared_axis]
found = tuple(_find_forbidden_keys(card_body, forbidden=forbidden))
if found:
    raise CardCouplingError(
        f"F-CARDS-COUPLING-VIOLATION-EXTENSION: {card_path} contains forbidden "
        f"{declared_axis} coupling keys {found!r}. CICs may recommend compatible CLCs "
        "only at orchestration time, never by embedding CLC pattern logic in card files."
    )
```

**Status: LIVE.** This is the actual runtime enforcement, even though the named gate module's `evaluate()` raises `NotImplementedError`.

This is a notable ownership-clarity issue. The named gate `F-CARDS-COUPLING-VIOLATION-EXTENSION` doesn't enforce its own gate ID — the loader does, by raising a `CardCouplingError` with the gate ID in the string. If a test or audit tool decides to mock the gate module to verify a specific behavior, it would not actually be testing the live enforcement path.

### §5.4 Layer 4 — F-CARDS-COUPLING-VIOLATION-EXTENSION value-position scan (STUB) (L2-F4)

The §4 v2.x.7 amendment specifies (lines 108-120) four regex patterns plus a path-level allowlist (lines 116-119, 160-171). The amendment claims the body graduated. On disk it's `NotImplementedError`. Per L1-F3.

**Net coverage today.** Coupling-language drift via value-position literals is unprotected by any runtime gate. The only mitigating control is the §4 v2.x.7 backfill-scan script that the amendment describes — but that script is not in `pipeline/scripts/` on disk either. The amendment cross-references it at `outputs/od_c_backfill_scan.py:238`, suggesting it lives in the Cowork workspace outputs/ directory (not committed to the repo).

### §5.5 Layer 5 — F-CIC-CLC-COUPLING-VIOLATION (v7.0.8 four-layer scan, LIVE) (L2-F8)

`pipeline/logician/gates/f_cic_clc_coupling_violation.py:1-328` is the v7.0.8 progenitor. Four detection layers:

| Layer | Mechanism | Surface |
|---|---|---|
| 1 | Lexical regex on field names | `LAYER_1_FIELD_REGEX = re.compile(r"^(primary\|preferred\|allowed\|activated\|enabled\|valid)_(capital_logic\|clc)(...)?$", re.IGNORECASE)` (`f_cic_clc_coupling_violation.py:68-72`) |
| 2 | Pydantic AST inspection | Catches `Mapping[CIC, Collection[CLC]]` shapes regardless of name (`_layer_2_pydantic` at line 201) |
| 3 | Value-set subset check | Catches creative-renamed value lists where a CIC key holds a CLC value-list or vice versa (`_layer_3_value_set` at line 234) |
| 4 | Knowledge-pack manifest schema | Forbids any KnowledgePackManifest field annotation containing `CapitalLogicCard` (line 278) |

**Status: LIVE** for all four layers, per the module's well-formed `run()` function at lines 306-327. The function takes four injected source callables (file-globbing / YAML-parsing / Pydantic-AST-walking happen outside the gate) and aggregates `CouplingFinding` records.

**Vocabulary fork (L2-F8).** The v7.0.8 gate uses `CouplingFinding.subcode` like `F-CIC-CLC-COUPLING-VIOLATION.layer1_lexical`. The §4 v2.x.7 amendment for the v7.0.11 successor uses `GateOutcome.violations` like `forbidden_field_name:CIC:clc_allowlist (sub-tag .forbidden_field_name_for_axis)`. The two vocabularies will eventually have to converge or be documented as deliberate parallel surfaces. The v7.0.11 successor extends the v7.0.8 progenitor in spirit but doesn't re-export or wrap its outcomes.

**Coverage relationship:**

- v7.0.8 F-CIC-CLC-COUPLING-VIOLATION scans the entire repo (knowledge packs, pipeline code, vault, orgs) for cross-axis coupling at startup. Card files would be scanned too if the four injected sources walk them.
- v7.0.11 F-CARDS-COUPLING-VIOLATION-EXTENSION targets specifically the card files at loader time + at build-time AST-lint.

They are complementary, not duplicate. Documenting the overlap explicitly would help a CTO understand the layered defense.

---

## §6. The operator's v2.1 Law-5 reconciliation — `common_funders_observed` discipline (L2-F5)

### §6.1 What the corrective said (verbatim)

From the operator's corrective in this run:

> 6. **Non-negotiable folded in from operator's v2.1 reconciliation patch:**
>    - `common_funders_observed` is **operator-confirmed engagement only** (Law 5 discipline). Subagent-populated funders based on sector knowledge belong in `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation`, NOT in the live observational block. If any of your audit findings touch this field, enforce this distinction in your patch-plan recommendations.

This is a direct application of Law 5 ("Applicant Brings the Substance"; `SOUL.md:38`) to the card schema: subagent imagination about which funders this CIC works with does not count as observed engagement. Only operator-confirmed engagement counts.

### §6.2 What the schema says

The CIC schema (`card_cic.schema.json:297-378`) declares `common_funders_observed:` with `description: "Observational-only funder roster. NOT a CIC × CLC binding."` Each item requires `funder_name` + `funder_type`, optionally carries `typical_award_range` / `frequency_observed` / `note`, and is blocked from carrying the 7 forbidden CIC-coupling field names via the nested `not.anyOf`.

**The schema does NOT distinguish operator-confirmed engagement from subagent-populated speculation.** The description ("Observational-only funder roster") is true but does not capture Law 5's binding distinction. A subagent who populates this list with "USDA VAPG (frequency_observed: FREQUENT)" because USDA VAPG is sector-canonical, but Tilth has never actually engaged USDA VAPG, would PASS the schema but VIOLATE Law 5.

Symmetric on the CLC side (`card_clc.schema.json:98-174`), same description language.

### §6.3 What the cards say — the Phase E Option 2 cleanup pattern

The 6 CIC cards all carry the same structural pattern (sample from `pipeline/cards/CIC/food_systems.yaml`):

| Block | Lines | Content |
|---|---|---|
| Top-level `common_funders_observed:` | 626-631 | **Empty list** with a comment block explaining the relocation: *"2026-05-16. Prior content moved to `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` below; operator graduates candidate entries to this live list as actual engagement confirms."* |
| Nested `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation:` | 798-808+ | List of funder candidates with sector-derived metadata, marked as pending operator engagement confirmation. |

Confirmed pattern is uniform across all 6 CIC cards by grep:

| CIC card | Empty top-level `common_funders_observed:` line | `_research_metadata.draft_funder_candidates_*:` line |
|---|---|---|
| food_systems.yaml | 626 | 808 |
| cooperative.yaml | 893 | 1059 |
| educator.yaml | 1011 | 1197 |
| ecosystem_intermediary.yaml | 1056 | 1273 |
| arts_culture.yaml | 1024 | 1235 |
| public_agency.yaml | 992 | 1188 |

**All 6 CIC cards apply the operator's v2.1 Law-5 split correctly.** The on-disk state matches the operator's intent.

### §6.4 The CLC side is not aligned

Grep for `^common_funders_observed:|draft_funder_candidates_pending_operator_engagement_confirmation` across `pipeline/cards/CLC/`: **zero matches.** None of the 8 CLC cards have an empty top-level `common_funders_observed:` block with a Phase E Option 2 comment. None of them have the `_research_metadata.draft_funder_candidates_*:` nested block.

Three possibilities:

1. CLC cards omit `common_funders_observed:` entirely (the field is optional per the schema; not in `required` at line 7-23 of the CLC schema). If so, no Law-5 violation exists today — there's just nothing to confirm.
2. CLC cards have populated top-level `common_funders_observed:` lists with subagent-speculative funder entries (the very Law-5 violation the operator's v2.1 patch addresses).
3. CLC cards have populated top-level lists with operator-engagement-confirmed funders only (Law-5 compliant; no draft block needed).

This audit hit the grep wall and didn't read each CLC card's full body. **Phase 4-CLC (the per-CLC card researcher dispatch) must surface this.** For now: flag as P1.

### §6.5 Schema-level enforcement

The schema does not enforce the operator-confirmed-vs-subagent-speculative distinction. Patch options:

- **Patch A (minimal):** add a `description` clause to the schema's `common_funders_observed:` block stating: *"Operator-confirmed engagement only (Law 5). Subagent-populated candidates pending engagement confirmation route to `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation`."* Documentation-only.
- **Patch B (additive):** add an optional `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation:` array schema sibling, with the same item-shape as `common_funders_observed:`. This makes the draft block schema-known and lintable.
- **Patch C (binding):** add a logician gate `F-CARDS-FUNDERS-OBSERVED-LAW-5-UNCONFIRMED` that fires when `common_funders_observed:` is non-empty AND the card lacks an operator engagement attestation (a new lifecycle-adjacent field, e.g., `_research_metadata.operator_engagement_attested_at`). Heavyweight but matches Law 5's "fail closed" doctrine.

Recommend Patch B for v0.2 (schema knows about both blocks; loader doesn't need new logic; aligns with the existing CIC card pattern). Patch C is a v1.x candidate after the v0.2 loader graduation.

---

## §7. Forward-pointers

This audit feeds:

- **Phase 3 (INITIAL_CTO_HANDOFF_BLOCKERS.md):** L2-F0 (P0), L2-F1 (P0), L2-F4 (P1), L2-F5 (P1).
- **Phase 8.1-5 (FILE_BY_FILE_PATCH_QUEUE_PRE_V0_2.md):** the cards-ceremony to land §18 v1.2 + §18.6 v2; the README typography fix; the schema description addition for Law-5 discipline; the gate-body graduation patches.
- **Phase 4-CLC (deferred to a separate dispatch):** must audit each CLC card's `common_funders_observed:` state to determine whether the Law-5 split needs to apply.

---

## §8. Files cited

| File | Lines referenced | Purpose |
|---|---|---|
| `pipeline/cards/_schema/card_cic.schema.json` | 24-67, 208-274, 297-378, 555-595 | CIC schema (forbidden-field blocks, dialect_routing_table, common_funders_observed) |
| `pipeline/cards/_schema/card_clc.schema.json` | 7-23, 98-174, 194-227, 381-415 | CLC schema (forbidden-field blocks, common_funders_observed) |
| `pipeline/cards/loader.py` | 309-344, 331-344 (`_find_forbidden_keys`) | Live coupling enforcement |
| `pipeline/cards/models.py` | 27-54, 47-54 (`COVERAGE_AXES`) | Schema mirror |
| `pipeline/cards/README.md` | 7, 9-11 | Naming discipline documentation |
| `pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md` | 51-53 (§1.1) | Canonical naming intent |
| `pipeline/blueprint/v0.1/section_18_v1_2_amendment.md` | 1-220 (full) | LOCKED-but-not-applied amendment |
| `pipeline/blueprint/v0.1/section_04_v2_x_7_card_coupling_value_position_amendment.md` | 38-47, 108-120, 160-171 | Value-position regex spec |
| `pipeline/logician/gates/f_cards_coupling_violation_extension.py` | 32-53 (FORBIDDEN_FIELD_REGISTRY), 63-82 (stub body) | Card-coupling gate (stub) |
| `pipeline/logician/gates/f_cic_clc_coupling_violation.py` | 1-328 (full) | v7.0.8 progenitor (LIVE) |
| `pipeline/cards/CIC/food_systems.yaml` | 28 (stale header), 36 (coverage_axis), 326-345 (dialect_routing_table), 626-631 (empty common_funders_observed), 808 (draft funder candidates) | CIC sample |
| `pipeline/cards/CIC/cooperative.yaml` | 45 (stale header), 893-901, 1059 | CIC sample |
| `pipeline/cards/CIC/educator.yaml` | 1011, 1197 | CIC sample |
| `pipeline/cards/CIC/arts_culture.yaml` | 1024, 1235 | CIC sample |
| `pipeline/cards/CIC/public_agency.yaml` | 36 (stale header), 992, 1188 | CIC sample |
| `pipeline/cards/CIC/ecosystem_intermediary.yaml` | 113 (stale header), 1056, 1273 | CIC sample |
| `pipeline/cards/CLC/credit_underwriting.yaml` | 1-52 (top-of-file; no track_a/track_b) | CLC single-track shape confirmation |
| `SOUL.md` | 38 (Law 5 text) | Law 5 binding statement |
| `docs/cic_clc_unified_master_prompt_2026-05-17.md` | §1 line 14 (vocabulary anchoring), §2.5/§2.6/§2.7 (multi-track CLC restructure claims), §3 (regex framing), §4 (dual-track shape), §6 (CLC-06 Track B carve-out) | Master prompt naming + orthogonality claims |

---

*End of Phase 2 deliverable.*
