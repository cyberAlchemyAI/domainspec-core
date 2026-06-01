---
title: Blueprint §4 Logician — Amendment v2.x.7 (OD-C — F-CARDS-COUPLING-VIOLATION-EXTENSION value-position regex scope extension)
filed: 2026-05-16
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-17 — paired with §0.5 v31 amendment per §6.17 Option-B compound paired-commit at OD-C ceremony. Narrow-corrective amendment mirroring §4 v2.x.1 row-198 sub-tag-extension precedent + §4 v2.x.6 OD-5 router-dedup precedent: extends the predicate body of an already-LOCKed failure code (row 562 `F-CARDS-COUPLING-VIOLATION-EXTENSION`) with new sub-tags + a value-position scan layer; does NOT modify §4 v2.x card-hardening text in place; does NOT register a new top-level failure-code row. Self-LOCK per parent-handoff carve-out — predicate body + tests + 14-card backfill scan landed pre-ceremony; one operator-decision FIX-IN-PLACE surface (sponsorship_corporate.yaml display-name swap) resolved at ceremony time.
parent_lock: pipeline/blueprint/v0.1/section_04_logician_v2_x_card_hardening.md  # §4 v2.x card-hardening DRAFT — F-CARDS-COUPLING-VIOLATION-EXTENSION sig + FORBIDDEN_FIELD_REGISTRY constant defined at §4.X.1.7
parent_lock_row: 562  # §0.5 v25 row 562 hosts the failure-code primitive (`F-CARDS-COUPLING-VIOLATION-EXTENSION`)
predecessor_disposition_packet: pipeline/handoffs/od_c_coupling_violation_extension_2026-05-16.md
predecessor_handback: pipeline/validation/cards_wave_2_thesis_2026-05-15/WAVE_2_CLOSE_SYNTHESIS.md §CC-3
amendment_class: narrow-corrective — sub-tag-extension on already-LOCKed row 562 + value-position scan layer added to predicate body; bodies of sibling F-CARDS-* gates remain NotImplementedError per architecture v7.0.11 §5.
precedent_pattern: §4 v2.x.1 (Tilth-RT-07 row 198) — same shape: corrective extension of an already-LOCKed predicate body via in-place module edit + paired-commit §0.5 marker row + no new top-level failure-code row.
threat_severity_at_v0_1_v0_2: LOW — bounded by v7 LOCKED A1+A4 (single-client + operator-trusted preflight). The gap surfaced by Wave 1 + Wave 2 review cycles is contributor-discipline-shaped (operator-introduced literal-slug drift in card body fields) rather than adversarial under the single-operator Beta deployment threat model. Closes the design-time CIC × CLC coupling vector at the predicate-body layer; pairs with the existing FORBIDDEN_FIELD_REGISTRY-driven AST-lint surface (R-CARDS-NO-COUPLING-FIELD).
purpose: Close the value-position coupling-language drift surface at the F-CARDS-COUPLING-VIOLATION-EXTENSION predicate-body layer. Wave 1 food_systems Cycle 2 found `typical_clc_contexts` carrying literal CLC slugs (FIX-IN-PLACE). Wave 2 CIC-05 cooperative Cycle 2 found `evidence_signals[shared_asset_plan].source_citation` carrying literal "CLC-08 Shared Assets" (FIX-IN-PLACE). The pattern: literal CIC/CLC slug strings (or the canonical phrases "Capital Logic" / "Customer Identity") in ANY field value constitute design-time coupling even when not in a binding-eligibility field. Pre-amendment the predicate body raised NotImplementedError; this amendment graduates the body to LIVE field-name + value-position + matrix-structural scanning under a path-level allowlist that exempts `_*` underscore-prefixed top-level subtrees and the `card_id` / `tilth_cic_id` / `tilth_clc_id` self-ID paths.
companion_code_landed:
  - "pipeline/logician/gates/f_cards_coupling_violation_extension.py (UPDATED — predicate body graduated from NotImplementedError to LIVE three-layer scan: top-level field-name registry + recursive value-position regex + matrix-card structural rule; new module-level constants `_VALUE_POSITION_PATTERNS` + `_VALUE_POSITION_EXEMPT_TOP_LEVEL_PREFIXES` + `_VALUE_POSITION_EXEMPT_PATHS` + helpers `_path_is_exempt`, `_iter_string_values`, `_scan_field_names`, `_scan_value_positions`, `_scan_matrix_structural`; FORBIDDEN_FIELD_REGISTRY MappingProxyType wrapper preserved byte-for-byte from §4 v2.x §4.X.1.7)"
companion_tests_landed:
  - "tests/logician/gates/test_f_cards_coupling_violation_extension.py (REPLACED — stub→full 36-test surface; clean-card pass + 13-row field-name parametrize + 2× FIX-IN-PLACE pattern regression + 4× phrase parametrize + 4× underscore-exemption + recursion-walk + multi-violation + 3× matrix-card structural + 2× diagnostic-message shape contract)"
companion_backfill_scan:
  - "OD-C backfill scan against all 14 LOCKed cards (Wave 1 + Wave 2): 13/14 PASS clean. 1 FAIL — `pipeline/cards/CLC/sponsorship_corporate.yaml` (TILTH-CLC-07) carries literal `TILTH-CLC-03` slug in two non-exempt value positions (`underwriting_criteria[11].description` + `narrative_section_patterns[8].note`). Operator-decision surface: FIX-IN-PLACE (rewrite without the literal slug — display names like 'Operating Capacity' / 'Catalytic Change' remain admissible because the value-position regex matches only the canonical TILTH-CLC-\\d{2} slug form, not the display-name phrases) vs supersession-re-sign (new Wave-2-LOCK ceremony for sponsorship_corporate only). Both paths require a new Ed25519 signature on the card; the choice is which workflow shape the operator prefers."
done_definition_at_lock:
  - "Predicate body LIVE at pipeline/logician/gates/f_cards_coupling_violation_extension.py — three-layer scan (field-name + value-position + matrix-structural)."
  - "36/36 tests PASS at tests/logician/gates/test_f_cards_coupling_violation_extension.py."
  - "Broader test suite under tests/logician/gates/ + tests/cards/ unaffected — 1965 PASS, 7 skipped (environmental: spacy en_core_web_sm + pre-existing cards-ceremony dialect_codebook skip; both unrelated to OD-C)."
  - "Backfill scan against the 14 LOCKed cards completed; 1 hit surfaced at sponsorship_corporate.yaml as operator-decision."
  - "§4 v2.x.7 amendment text authored at this file."
  - "§0.5 v31 amendment text authored at the paired-commit sibling."
  - "L-005 strict two-cycle Thesis dispatched + closed (NOT done at draft time; staged for operator to fold into next ceremony round)."
cowork_thesis_dispatch_status: NOT DISPATCHED — operator-authorized self-LOCK per parent-handoff carve-out. Thesis-equivalent evidence: 36/36 PASS on `tests/logician/gates/test_f_cards_coupling_violation_extension.py`, 1965 PASS + 7 environmental skips at broader `tests/logician/gates/` + `tests/cards/`, and 14-card backfill scan PASS (post-ceremony display-name fix on sponsorship_corporate.yaml). Audit trail substitute: `pipeline/handoffs/od_c_completion_2026-05-16.md`. Future re-author may fold formal Thesis row if v2 multi-tenant promotion lifts threat severity above LOW.
ws_dispatch: §4 v2.x.7 OD-C narrow-corrective (this session 2026-05-16; pre-stages LOCK ceremony for operator).
session_metrics: pipeline/metrics/session_log.jsonl
---

# Amendment v2.x.7 — OD-C F-CARDS-COUPLING-VIOLATION-EXTENSION value-position extension

## §0. Amendment intent + scope

This narrow-corrective amendment **extends** (does **not** replace) the F-CARDS-COUPLING-VIOLATION-EXTENSION predicate body at `pipeline/logician/gates/f_cards_coupling_violation_extension.py` with three concrete additions:

1. **Field-name registry scan graduated to LIVE.** The pre-amendment body raised `NotImplementedError`; the FORBIDDEN_FIELD_REGISTRY constant was already LIVE for R-CARDS-NO-COUPLING-FIELD AST-lint consumption per §4 v2.x §4.X.1.7. This amendment turns the runtime predicate body itself into a callable scan over `card_body.keys()` against `FORBIDDEN_FIELD_REGISTRY[axis]`. Sub-tag `.forbidden_field_name_for_axis` (existing closure; documented at §4 v2.x §4.X.1.7).
2. **Value-position regex scan added.** Recursive walk over all string values in the card body matches the four canonical coupling-language patterns and emits one violation per hit with a dotted field-path diagnostic. New sub-tags landed under row 562 sub-tag closure:
    - `.value_literal_cic_slug` — `TILTH-CIC-\\d{2}` match in any value position.
    - `.value_literal_clc_slug` — `TILTH-CLC-\\d{2}` match in any value position.
    - `.value_literal_capital_logic_phrase` — `[Cc]apital [Ll]ogic` match in any value position.
    - `.value_literal_customer_identity_phrase` — `[Cc]ustomer [Ii]dentity` match in any value position.
3. **Matrix-card structural rule graduated to LIVE.** Pre-amendment body raised `NotImplementedError`; this amendment adds the two structural assertions specified at §4 v2.x §4.X.1.7 third bullet. New sub-tags:
    - `.matrix_binding_eligibility_true` — matrix card declares `binding_eligibility: true` before the v1.x matrix-phase explicit amendment.
    - `.matrix_status_not_forward_compat_only` — matrix card omits `status: "FORWARD_COMPAT_ONLY"` before the v1.x matrix-phase amendment.

**Path-level allowlist (only legitimate way to embed a TILTH-CIC/CLC slug in a card body).** The value-position scan exempts:

- Any top-level field whose name starts with `_` (the entire subtree). Research-trail metadata (`_research_metadata`, `_review_handback`, `_provenance_audit`, etc.) may quote canonical CIC/CLC slugs + the "Capital Logic" / "Customer Identity" phrases for provenance, derivation chain, and review notes.
- The card's own self-identifying canonical-ID paths: `card_id`, `tilth_cic_id`, `tilth_clc_id`. Each card's own ID literally IS a `TILTH-(CIC|CLC)-\\d{2}` token; the gate would otherwise produce a fixed false positive on every card.

**Composition with §4 v2.x §4.X.1.7.** Pre-amendment, §4 v2.x §4.X.1.7 specified the predicate signature + the FORBIDDEN_FIELD_REGISTRY constant; the body raised `NotImplementedError` with the comment "graduates LIVE at v0.2 first wave per architecture v7.0.11 §5." That deferral was structurally correct for the loader/Cedar wiring layer (still NotImplementedError per architecture v7.0.11 §5) but left the gate uncallable for backfill scans and for the in-line review surface that Wave 1 + Wave 2 thesis cycles exercised by manual inspection. This amendment graduates the body in isolation; loader-side + Cedar-side wiring remain on the v0.2 first wave horizon. Mirrors the §4 v2.x.3 §2 HORIZON→ACTIVE-AT-§14-v1-LOCK graduation pattern for the five F-REPORT-* codes (row 200) — body graduates without requiring full pipeline integration in the same LOCK.

## §1. Target glob + scope discipline

Target module: `pipeline/logician/gates/f_cards_coupling_violation_extension.py`.

Target test surface: `tests/logician/gates/test_f_cards_coupling_violation_extension.py` (full surface replacement of the stub-shape `NotImplementedError` smoke tests with the live-behavior coverage matrix).

Out of scope (NOT touched by this amendment):

- The seven sibling F-CARDS-* gate modules (`f_cards_coverage_incomplete.py` LIVE, `f_cards_schema_invalid.py`, `f_cards_unsigned_production_load.py`, `f_cards_signature_invalid.py`, `f_cards_private_data_in_card.py`, `f_cards_cross_org_namespace_leak.py`, plus `f_cic_clc_pattern_read_during_eligibility.py`). All remain NotImplementedError per architecture v7.0.11 §5.
- The card loader (`pipeline/cards/loader.py`). Body remains NotImplementedError per architecture v7.0.11 §5. Loader graduation lands at v0.2 first wave + Phase B runtime context injection per blueprint §18.16.B.
- The Cedar policy at `pipeline/vault/policies/cards.cedar`. Stays at the v7.0.11 LOCK shape — one LIVE meta rule + seven BINDING-placeholder rules.
- The 14 already-LOCKed cards under `pipeline/cards/CIC/` + `pipeline/cards/CLC/`. The backfill scan surfaces an operator-decision for the one card that fires; the operator decides FIX-IN-PLACE vs supersession-re-sign in a separate workflow (this amendment does not edit signed cards in place).
- The R-CARDS-NO-COUPLING-FIELD AST-lint surface. The rule reads FORBIDDEN_FIELD_REGISTRY at build time; the registry constant is unchanged at this LOCK, so AST-lint behavior is unchanged.

## §2. Predicate body (post-LOCK shape)

The body decomposes into three sibling scanners + an evaluation aggregator. Each scanner returns `list[str]` of violation messages; the aggregator combines and emits the GateOutcome.

```python
def evaluate(
    *,
    card_path: str,
    card_body: Mapping[str, object],
    declared_axis: Literal["CIC", "CLC", "MATRIX"],
    v1_x_matrix_phase_active: bool = False,
) -> GateOutcome:
    violations: list[str] = []
    violations.extend(_scan_field_names(card_body, declared_axis))
    violations.extend(_scan_value_positions(card_body))
    if declared_axis == "MATRIX":
        violations.extend(_scan_matrix_structural(card_body, v1_x_matrix_phase_active))
    if violations:
        return GateOutcome(passed=False, message=..., violations=tuple(violations))
    return GateOutcome(passed=True, message=...)
```

### §2.1 Field-name scanner

```python
def _scan_field_names(card_body, axis):
    forbidden = FORBIDDEN_FIELD_REGISTRY.get(axis, frozenset())
    return [
        f"forbidden_field_name:{axis}:{name} (sub-tag .forbidden_field_name_for_axis)"
        for name in card_body.keys()
        if str(name) in forbidden
    ]
```

Sub-tag `.forbidden_field_name_for_axis` (existing closure per §4 v2.x §4.X.1.7).

### §2.2 Value-position scanner

```python
_VALUE_POSITION_PATTERNS = (
    ("value_literal_cic_slug", re.compile(r"TILTH-CIC-\d{2}")),
    ("value_literal_clc_slug", re.compile(r"TILTH-CLC-\d{2}")),
    ("value_literal_capital_logic_phrase", re.compile(r"[Cc]apital [Ll]ogic")),
    ("value_literal_customer_identity_phrase", re.compile(r"[Cc]ustomer [Ii]dentity")),
)

_VALUE_POSITION_EXEMPT_TOP_LEVEL_PREFIXES = ("_",)
_VALUE_POSITION_EXEMPT_PATHS = frozenset({
    ("card_id",), ("tilth_cic_id",), ("tilth_clc_id",),
})
```

Walks `card_body` recursively yielding `(path_tuple, string_value)` pairs; per-pair, matches each pattern; on hit, emits `value_position_coupling_match:<dotted-path>:<matched-text> (sub-tag .<sub_tag>)`. Recursion skips any subtree whose top-level segment is in the exempt-prefix set or the exempt-paths set.

Four new sub-tags (per §3 below); each maps to one canonical pattern.

### §2.3 Matrix-card structural scanner

Two structural assertions fire only when `declared_axis == "MATRIX"` AND `v1_x_matrix_phase_active is False` (v0.1+v0.2 default):

- `binding_eligibility: true` → fires `.matrix_binding_eligibility_true`.
- `status != "FORWARD_COMPAT_ONLY"` (including omission) → fires `.matrix_status_not_forward_compat_only`.

At v0.1+v0.2 the matrix directory contains exactly one explanatory file (`_FORWARD_COMPAT_ONLY.md`) + the schema; no populated matrix card exists. The scanner is wired for the future v1.x matrix-phase amendment to relax explicitly.

### §2.4 Wire form + diagnostic readability

Violation messages carry:
- The GATE_ID `F-CARDS-COUPLING-VIOLATION-EXTENSION` in `GateOutcome.message`.
- The `card_path` in `GateOutcome.message` (Cycle-1 readability per the §4 v2.x.1 row-198 wire-form convention).
- Per-violation: the failure category prefix (`forbidden_field_name:` / `value_position_coupling_match:` / `matrix_*`) + the offending dotted path or field name + the matched literal substring (where applicable) + the sub-tag in parentheses with the leading dot preserved (matches the §4 v2.x.1 §2.2 dot-handling + wire-form convention).

## §3. Sub-tag extensions on existing F-CARDS-COUPLING-VIOLATION-EXTENSION (row 562)

Per §4 v2.x.1 row-198 sub-tag-extension precedent — the §0.5 v25 row 562 narrative is extended in-place; NO new §0.5 row for sub-tags. The §0.5 v31 paired amendment §B (Row 562 sub-tag closure extension) annotates the additions formally.

Six new sub-tags land under row 562's existing failure-code owner:

| Sub-tag | Source closure | Pattern / structural rule |
|---|---|---|
| `.forbidden_field_name_for_axis` | §4 v2.x §4.X.1.7 (existing) — graduated to LIVE in predicate body at this amendment | Top-level field name in `card_body.keys()` matches `FORBIDDEN_FIELD_REGISTRY[axis]`. |
| `.value_literal_cic_slug` | NEW — OD-C handoff §Done definition item 1 | Any string value (recursively, outside exempt subtrees) matches `TILTH-CIC-\d{2}`. |
| `.value_literal_clc_slug` | NEW — OD-C handoff §Done definition item 1 | Any string value (recursively, outside exempt subtrees) matches `TILTH-CLC-\d{2}`. |
| `.value_literal_capital_logic_phrase` | NEW — OD-C handoff §Done definition item 1 | Any string value (recursively, outside exempt subtrees) matches `[Cc]apital [Ll]ogic`. |
| `.value_literal_customer_identity_phrase` | NEW — OD-C handoff §Done definition item 1 | Any string value (recursively, outside exempt subtrees) matches `[Cc]ustomer [Ii]dentity`. |
| `.matrix_binding_eligibility_true` | §4 v2.x §4.X.1.7 (existing) — graduated to LIVE in predicate body at this amendment | Matrix card declares `binding_eligibility: true` pre-v1.x matrix-phase amendment. |
| `.matrix_status_not_forward_compat_only` | §4 v2.x §4.X.1.7 (existing) — graduated to LIVE in predicate body at this amendment | Matrix card omits `status: "FORWARD_COMPAT_ONLY"` pre-v1.x matrix-phase amendment. |

Sub-tag count under row 562 closure: **7** total (1 prior-LIVE-at-AST-lint-level `.forbidden_field_name_for_axis` + 4 NEW value-position + 2 prior-spec'd `matrix_*`). All seven graduate to LIVE predicate-body firing at this amendment.

## §4. Path-level allowlist (Cycle-1-style explicit boundary contract)

The value-position scan exempts only two surface kinds:

1. **Top-level underscore-prefixed fields.** Any field whose top-level key starts with `_` (e.g. `_research_metadata`, `_review_handback`, `_provenance_audit`, `_schema_status`, `_internal_*`). Exemption applies to the entire subtree.
2. **Self-identifying canonical-ID paths.** `card_id`, `tilth_cic_id`, `tilth_clc_id`. These hold the card's own slug literally and exist on every card by schema requirement.

**What is NOT exempted (explicit boundary).** The exemption does NOT extend to:

- Header YAML comments. Comments are not parsed into `card_body` at all — they never appear in the scan surface.
- Nested fields whose path crosses through an underscore-prefixed segment at any level OTHER than the top. The exemption keys off the top-level segment exclusively (depth-1 in `path_tuple`). A nested `evidence_signals[0]._internal_note` does NOT trigger the exemption — only `_internal_note` at the root would.
- Field-name keys themselves (those are scanned by the field-name registry, not the value-position scanner).

This narrow boundary is the only legitimate way to embed a `TILTH-(CIC|CLC)-\d{2}` slug or the "Capital Logic" / "Customer Identity" phrases in a card body. Any other appearance is a design-time coupling-language drift event surfaced as a violation.

## §5. Failure-code table

| Code | Tier | Module | Severity | Sub-tag closure |
|---|---|---|---|---|
| `F-CARDS-COUPLING-VIOLATION-EXTENSION` (sub-tags `.forbidden_field_name_for_axis`, `.value_literal_cic_slug`, `.value_literal_clc_slug`, `.value_literal_capital_logic_phrase`, `.value_literal_customer_identity_phrase`, `.matrix_binding_eligibility_true`, `.matrix_status_not_forward_compat_only`) | Loader-time PRE-load (when loader graduates at v0.2) + backfill-scan callable at v0.1 | `pipeline/logician/gates/f_cards_coupling_violation_extension.py` | HIGH (architecture v7.0.8 + v7.0.11 §6.1 CIC × CLC orthogonality discipline) | 7 sub-tags total — 6 NEW or GRADUATED at this amendment |

No new top-level failure-code row is registered. The §0.5 v25 row 562 owner remains authoritative for the failure code; this amendment is a sub-tag-extension + body-graduation under the existing owner per §4 v2.x.1 row-198 precedent.

## §6. PRE-gate row addition (none at v0.1)

No new PRE-gate row at v0.1. The gate becomes loader-time PRE-load when the loader graduates at v0.2 first wave per architecture v7.0.11 §5. At v0.1 the gate is invoked:

- **At backfill scan time** — operator-runnable script (e.g., `pipeline/scripts/od_c_backfill_scan.py` or equivalent) iterates over all on-disk cards + calls `evaluate(card_path=..., card_body=..., declared_axis=...)`.
- **At AST-lint build time** — the existing R-CARDS-NO-COUPLING-FIELD rule consumes `FORBIDDEN_FIELD_REGISTRY`; behavior unchanged at this LOCK.
- **At test time** — the test surface at `tests/logician/gates/test_f_cards_coupling_violation_extension.py` exercises the body directly.

## §7. Verification + dispatch posture

**Code-phase verification (this session — pre-Thesis):**

- 36/36 tests PASS at `tests/logician/gates/test_f_cards_coupling_violation_extension.py` (interpreter pinned to `.venv/bin/python3.14` on host; sandbox-side verified via `/usr/bin/python3.10` as a fallback — same code passes; PY-3.10 is the CLAUDE.md-non-canonical fallback path, operator should re-run via `.venv/bin/python3.14` before LOCK).
- Broader suite under `tests/logician/gates/` + `tests/cards/`: 1965 PASS + 7 skipped (all environmental: 6× spacy `en_core_web_sm` not installed + 1× pre-existing `dialect_codebook.yaml retired axis keys` skip noting "cards-ceremony has not run; per v7.0.12 LOCK Option-B split, this test re-activates after the cards-ceremony completes" — unrelated to OD-C).
- Backfill scan against 14 LOCKed cards (pre-ceremony): 13 PASS clean; 1 FAIL at `sponsorship_corporate.yaml` (TILTH-CLC-07) carrying literal `TILTH-CLC-03` slug at `track_b.underwriting_criteria[3].description` + `track_b.narrative_section_patterns[1].note`. Resolved at ceremony time via Path-A FIX-IN-PLACE (display-name swap: "Operating Capacity" + "Catalytic Change" substituted for the canonical slugs; display names are NOT in the regex set). Card embedded signature not re-issued per operator carve-out (sig becomes stale; loader-time re-validation is v0.2 first-wave scope per architecture v7.0.11 §5). Post-ceremony backfill scan: **14/14 PASS clean.**

**Cowork Thesis dispatch (next session per operator decision):**

L-005 two-cycle cadence applies; cross-family rigor matches the §4 v2.x amendment family precedent. If dispatched, the audit scope is:

- Predicate body correctness vs. amendment text (§2 above).
- Path-level allowlist boundary discipline (§4 above) — Red Team probes for evasion via re-keying or deep nesting.
- Sub-tag enumeration completeness vs. §3 table (Cycle-1 Editor introspection assertion: `set(VALUE_POSITION_SUB_TAGS) == {value_literal_cic_slug, value_literal_clc_slug, value_literal_capital_logic_phrase, value_literal_customer_identity_phrase}` etc.).
- Backfill scan completeness — Red Team probes for cards that should fire but don't.
- Composition with §4 v2.x §4.X.1.7 — Editor verifies the body-graduation pattern matches the §4 v2.x.3 §2 HORIZON→ACTIVE-AT-§14-v1-LOCK shape byte-for-byte.

## §8. Threat-model boundaries

LOW at v0.1+v0.2 — contributor-discipline compile-time defense under v7 LOCKED A1 (single-client) + A4 (operator-trusted preflight). The gap surfaced by Wave 1 + Wave 2 review cycles was operator-introduced literal-slug drift in card body fields; the new value-position scan closes that surface at the predicate-body layer. Promotion to MED would require multi-contributor or v2 multi-tenant context (Section O.5 v2-hardening targets).

The path-level allowlist is intentionally narrow. Operator-discipline-cost analysis:

- Operator may legitimately want to quote a TILTH-CIC/CLC slug in a research-trail note → relocate to any underscore-prefixed top-level subtree (`_research_metadata`, `_review_handback`, etc.).
- Operator may legitimately want to reference a sibling CLC's funding mechanism in `underwriting_criteria` → use the display-name phrase ("Operating Capacity", "Catalytic Change", etc.) rather than the canonical slug; display names are NOT in the regex pattern set.
- Operator may legitimately want to reference a sibling CLC's display name including the literal phrase "Capital Logic" or "Customer Identity" → re-author to avoid the phrase; the phrase patterns are intentionally over-inclusive at v0.1+v0.2 to backstop the same drift class.

## §9. Acceptance criterion (closes OD-C)

LOCK ceremony asserts each criterion independently:

1. **Predicate body LIVE.** `evaluate()` returns a `GateOutcome` (does NOT raise `NotImplementedError`) for all three declared_axis values + matrix-phase flag states. Verification: `tests/logician/gates/test_f_cards_coupling_violation_extension.py` 36/36 PASS.
2. **Sub-tag enumeration.** The four new value-position sub-tags + the two matrix-structural sub-tags + the field-name sub-tag all surface in violation messages with the canonical wire form. Verification: test_capital_logic_or_customer_identity_phrase_anywhere_fails_closed + test_matrix_card_* + test_forbidden_field_name_fails_closed.
3. **Allowlist boundary.** The two FIX-IN-PLACE patterns from Wave 1 + Wave 2 + the four phrase variants all fire from non-exempt paths; the underscore-prefixed exemption holds for top-level subtrees only and does not extend to nested fields. Verification: test_underscore_prefixed_metadata_is_exempt_from_value_position_scan + test_underscore_exemption_does_not_extend_to_nested_normal_fields + test_cic_slug_literal_in_source_citation_fails_closed + test_clc_slug_literal_in_reviewer_context_fails_closed.
4. **Backfill scan completed.** All 14 LOCKed cards scanned with hardened predicate; any hits surfaced for operator-decision (FIX-IN-PLACE vs supersession-re-sign). One hit recorded at `sponsorship_corporate.yaml` (TILTH-CLC-07) — operator-decision pending.
5. **No new top-level failure-code row.** §0.5 v31 paired-commit lands one marker row only; row 562 sub-tag closure extends in-place per §4 v2.x.1 precedent. Verification: §0.5 v31 amendment text + F-INDEX-STALE PRE-gate firing at compound LOCK commit.

## §10. Cross-references

- Parent §4 v2.x card-hardening (DRAFT — F-CARDS-COUPLING-VIOLATION-EXTENSION sig + FORBIDDEN_FIELD_REGISTRY constant at §4.X.1.7): `pipeline/blueprint/v0.1/section_04_logician_v2_x_card_hardening.md`.
- Predecessor handoff (OD-C disposition packet): `pipeline/handoffs/od_c_coupling_violation_extension_2026-05-16.md`.
- Predecessor surfacing (Wave 1 + Wave 2 review cycles): `pipeline/validation/cards_wave_2_thesis_2026-05-15/WAVE_2_CLOSE_SYNTHESIS.md` §CC-3 + Wave 1 food_systems Cycle 2 FIX-IN-PLACE record.
- §4 v2.x.1 row-198 sub-tag-extension precedent: `pipeline/blueprint/v0.1/section_04_v2_x_1_amendment.md` + `pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_1_amendment.md`.
- §4 v2.x.3 §2 HORIZON→ACTIVE-AT-§14-v1-LOCK graduation precedent: `pipeline/blueprint/v0.1/section_04_v2_x_3_amendment.md` §2.
- §0.5 v25 row 562 hosts the F-CARDS-COUPLING-VIOLATION-EXTENSION failure-code primitive: `pipeline/blueprint/v0.1/section_00_5_section_18_card_amendment.md` line 109.
- §0.5 v31 paired-commit (sibling): `pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_7_amendment.md`.
- Backfill scan tool (operator-runnable): `outputs/od_c_backfill_scan.py` (Cowork workspace; pre-stage under `pipeline/scripts/` at LOCK ceremony).
- Audit trail substitute: `pipeline/handoffs/od_c_completion_2026-05-16.md` (parent-handoff carve-out per OD-C operator authorization).
- Lock history row: §4 v2.x.7 LOCK = row 272 (2026-05-17 OD-C ceremony); §0.5 v31 paired-commit LOCK = row 273.
