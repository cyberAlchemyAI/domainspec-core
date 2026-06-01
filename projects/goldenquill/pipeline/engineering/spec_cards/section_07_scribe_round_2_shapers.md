# Spec card — pipeline.seats.scribe (Round 2: SMART + overlooked-expenses + dialect + program-template shapers)

**STATUS:** PRE-STAGED 2026-04-21 at Scribe R1 SELF-LOCK. R2 is UNBLOCKED — depends on R1 `types.py` + stdlib only. Still zero-LLM, zero-network, zero-subprocess — R2 is the **second deterministic-shaper layer** before R3's LLM-facing seat.py entry.

**Framework:** per `pipeline/templates/component_analysis_template.md` (Five Laws, Four Rules, failure-mode taxonomy — not restated).

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_07_scribe.md` **v1.1.1 LOCKED 2026-04-21** — principal source. R2 implements:
  - §7.5 `SectionDraft`, `ClaimEvidence`, `EligibleActivityMatch`, `SectionLimit`, `ScopeCheckComment` (draft-output shapes + section-ordering invariant)
  - §7.6 `SmartObjective` + numeric-verbatim invariant (pure Python; numeric tokenizer + unit-normalizer + byte-identity predicate — no LLM)
  - §7.7 `OverlookedExpensesWalk` + `OverlookedExpenseEntry` + checklist definition + "cannot finalize if needed_count > 0" invariant
  - §7.8 dialect code-switch **scaffold** — four dialect vocabulary tables (conservative / centrist / progressive / soul_fire) as frozen tuples + dialect-keyed identity-proxy closed set table (§7.2 Law 5 input) + register-mix detector. NO prompt compilation (R3), NO LLM call (R3).
  - §7.9 `ProgramTemplate` loader — reads `skills/scribe-ghostwriter/templates/<program>.md`, captures `template_content_sha3_512` at load time, exposes `verify_template_hash(program_code, pinned_sha) -> bool` for R3's `F-SCRIBE-TEMPLATE-DRIFT` PRE-gate.
- `pipeline/blueprint/v0.1/section_00_5_section_07_scribe_amendment.md` **§0.5 v7 LOCKED 2026-04-21** — R2 lands against rows covering `scribe.section_draft.v1`, `scribe.smart_objective.v1`, `scribe.overlooked_expenses_walk.v1`, `scribe.program_template.v1`, `scribe.dialect_identity_proxy_table.v1`, plus failure codes `F-SCRIBE-PARAPHRASED-NUMERIC`, `F-SCRIBE-SMART-INVENTED-METRIC`, `F-SCRIBE-DIALECT-DRIFT`, `F-SCRIBE-DIALECT-INDUCED-IDENTITY`, `F-SCRIBE-INELIGIBLE-ACTIVITY`, `F-SCRIBE-TEMPLATE-DRIFT`. R2 exports the string constants; PRE/POST-gate wiring lands at R3.
- `pipeline/seats/scribe/__init__.py` — R1 public surface. R2 EXPANDS `__all__` and appends new blueprint anchors to `BLUEPRINT_DEPS`.

**Blueprint hash-at-card:** §7 v1.1.1 `85b244a26888b52e`, §0.5 v7 `b99312d9a3ba3527`. Recompute at R2 LOCK; no drift expected (both sealed 2026-04-21 and no amendments scheduled).

**Spec-card version:** v1 (pre-staged at R1 SELF-LOCK)
**Round:** §7 Scribe Round 2 — deterministic shapers
**Depends on:** R1 `pipeline.seats.scribe.types` + `pipeline.seats.scribe.kgie` (already LOCKED). No §2 Vault / §4 Logician / router.yaml imports. Stdlib only + `pathlib` + `hashlib.sha3_512` + `decimal.Decimal` + optionally `re` for the numeric tokenizer.

## Summary

Ship four deterministic shaper modules + their test suites, each layered over R1 types:

1. **`smart.py`** — `SmartObjective` dataclass + `validate_smart_objective()` predicate + `numeric_verbatim_check()` — enforces §7.6 numeric-verbatim invariant at shape-layer time. Called by R3's POST-gate runner for `F-SCRIBE-PARAPHRASED-NUMERIC` + `F-SCRIBE-SMART-INVENTED-METRIC`.

2. **`overlooked_expenses.py`** — checklist definition (11 items per §7.7 blueprint), `OverlookedExpensesWalk` shape, `walk_checklist()` builder + `needed_count` consistency invariant at `__post_init__`. Non-bypassable for section 7 finalize per §7.7.

3. **`dialect.py`** — four frozen vocabulary tables + identity-proxy closed set + `detect_dialect_drift()` predicate (scans a draft body for out-of-register vocabulary tokens relative to the pinned `draft_dialect`). Register-mix = F-SCRIBE-DIALECT-DRIFT; identity-proxy without KGIE affirmation = F-SCRIBE-DIALECT-INDUCED-IDENTITY.

4. **`templates.py`** — `ProgramTemplate` dataclass + `load_program_template(program_code, templates_root)` reader + `verify_template_hash(template, pinned_sha)` predicate. Hash-pinning per §7.9 template-integrity invariant. Loader is stdlib-only (`pathlib.Path.read_bytes()` + `hashlib.sha3_512`); does NOT yet go through Vault (R3 promotes to Vault `template-query` primitive).

Plus the draft-output shape layer (consumed by R3):

5. **`draft.py`** — `SectionDraft`, `ClaimEvidence`, `EligibleActivityMatch`, `SectionLimit`, `ScopeCheckComment` dataclasses. Pure types; no behavior. Split from `smart.py` / `overlooked_expenses.py` because R3 seat.py composes all three.

## Scope boundary (R1 vs R2 vs R3)

**R1 (LOCKED):** types foundation (RFA record + KGIE shapes + USER_DATA anchor) + KGIE preflight predicate.

**R2 (this card):** draft-output shapes (`SectionDraft` + evidence map + eligible-activity map + scope-check-comment), SMART + overlooked + dialect + templates — all pure Python, all deterministic, all still zero-LLM.

**R3 (future):** `seat.py` stdin/stdout envelope, Anthropic `pipeline.providers.anthropic` provider call, admin-risk register integration (§7.11), PRE/POST gate wiring through `pipeline.logician`, Vault `template-query` migration for §7.9.

R2 is the last round before LLM integration. Keeping R2 deterministic ensures the Logician gate contracts are testable without an Anthropic API key in the test environment.

## Public API additions (R2)

```python
# pipeline/seats/scribe/draft.py

@dataclass(frozen=True, kw_only=True, slots=True)
class SectionLimit:
    limit_kind: Literal["words", "characters", "pages"]
    limit_value: int

@dataclass(frozen=True, kw_only=True, slots=True)
class ClaimEvidence:
    claim_text: str
    evidence_kind: Literal["RFA", "PROJECT_CONTEXT", "USER_DATA"]
    evidence_ref: str

@dataclass(frozen=True, kw_only=True, slots=True)
class EligibleActivityMatch:
    activity_phrase: str
    matched_rfa_activity: Optional[str]
    match_kind: Literal["exact", "paraphrase", "scope_check_needed"]

@dataclass(frozen=True, kw_only=True, slots=True)
class ScopeCheckComment:
    activity_phrase: str
    reason: str

@dataclass(frozen=True, kw_only=True, slots=True)
class AdminRiskFlag:
    flagged_term: str
    severity: Literal["low", "medium", "high"]
    proposed_substitution: Optional[str]
    operator_approved: bool

@dataclass(frozen=True, kw_only=True, slots=True)
class SectionDraft:
    section_name: str
    section_order: int
    body_text: str
    word_count: int
    character_count: int
    rfa_section_limit: Optional[SectionLimit]
    claim_evidence_map: tuple[ClaimEvidence, ...]
    eligible_activity_map: tuple[EligibleActivityMatch, ...]
    admin_risk_flags: tuple[AdminRiskFlag, ...]
    scope_check_comments: tuple[ScopeCheckComment, ...]
    draft_dialect: Literal["conservative", "centrist", "progressive", "soul_fire"]
    drafted_at_utc: datetime
```

```python
# pipeline/seats/scribe/smart.py

@dataclass(frozen=True, kw_only=True, slots=True)
class SmartObjective:
    objective_text: str
    outcome_text: str
    measurement_text: str
    timeline_text: str
    achievability_evidence: str
    relevance_pointer: tuple[str, ...]

def validate_smart_objective(obj: SmartObjective) -> tuple[str, ...]:
    """Return tuple of SMART-dimension failure reasons (empty == valid).
    S: objective_text must contain a verb + object pattern.
    M: outcome_text must contain a numeric token OR percentage.
    A: achievability_evidence must be non-empty.
    R: relevance_pointer must be non-empty.
    T: timeline_text must match a duration pattern (N {days|weeks|months|years} or ISO-8601).
    """

def numeric_verbatim_check(
    *,
    draft_text: str,
    claim_evidence_map: tuple[ClaimEvidence, ...],
    source_texts: Mapping[str, str],   # evidence_ref → source body (caller-loaded)
) -> tuple[ParaphraseViolation, ...]:
    """Walk every numeric token in draft_text; resolve against claim_evidence_map
    entries; fail on byte-mismatch after unit-normalization. Returns violations
    for R3's POST-gate to translate into F-SCRIBE-PARAPHRASED-NUMERIC.
    Unit-normalization: 1 year <=> 12 months; 1 ft <=> 12 in; $1,000 <=> $1000.
    Qualitative paraphrase NOT in scope (§7.6 v0.2 roadmap).
    """

F_SCRIBE_PARAPHRASED_NUMERIC: Final[str] = "F-SCRIBE-PARAPHRASED-NUMERIC"
F_SCRIBE_SMART_INVENTED_METRIC: Final[str] = "F-SCRIBE-SMART-INVENTED-METRIC"
```

```python
# pipeline/seats/scribe/overlooked_expenses.py

OVERLOOKED_EXPENSES_CHECKLIST: Final[tuple[str, ...]] = (
    "In-kind space and utilities",
    "Volunteer / board labor (match value)",
    "Printing, postage, branding, translation",
    "Audit and grant-reporting costs",
    "Compliance (FDA, GAP, organic certification, FSMA)",
    "Travel / mileage for outreach",
    "Evaluation / data collection tools",
    "Insurance and legal fees",
    "Packaging, storage, freight",
    "Training and professional development",
    "Indirect costs (if allowed by RFA)",
)

@dataclass(frozen=True, kw_only=True, slots=True)
class OverlookedExpenseEntry:
    item: str
    status: Literal["included", "n_a", "needed"]
    rationale: str

@dataclass(frozen=True, kw_only=True, slots=True)
class OverlookedExpensesWalk:
    walk_at_utc: datetime
    entries: tuple[OverlookedExpenseEntry, ...]
    needed_count: int    # __post_init__ asserts == sum(1 for e in entries if e.status == "needed")
    rfa_indirect_costs_allowed: Optional[bool]

def walk_checklist(
    *,
    operator_entries: Mapping[str, tuple[Literal["included", "n_a", "needed"], str]],
    rfa_indirect_costs_allowed: Optional[bool],
    clock: ClockFn,
) -> OverlookedExpensesWalk: ...
# Every item in OVERLOOKED_EXPENSES_CHECKLIST must have a matching operator_entries key;
# missing keys raise ValueError (exhaustiveness invariant).
```

```python
# pipeline/seats/scribe/dialect.py

Dialect = Literal["conservative", "centrist", "progressive", "soul_fire"]

DIALECT_VOCABULARY: Final[Mapping[Dialect, frozenset[str]]] = MappingProxyType({
    "conservative": frozenset({
        "production efficiency", "economic impact", "market competitiveness",
        "return on investment", "food security",
    }),
    "centrist": frozenset({
        "balanced growth", "community resilience", "evidence-based",
        "public-private partnership",
    }),
    "progressive": frozenset({
        "equity", "food sovereignty", "environmental justice",
        "climate resilience", "community self-determination",
    }),
    "soul_fire": frozenset({
        "land rematriation", "ancestral knowledge", "healing justice",
        "community power", "liberation",
    }),
})

# §7.2 Law 5 POST-gate feed: identity-proxy phrases keyed by dialect.
# Closed-set per v0.1 (v0.2 adds semantic-embedding supplement).
DIALECT_IDENTITY_PROXY_TABLE: Final[Mapping[Dialect, frozenset[str]]] = MappingProxyType({
    "soul_fire": frozenset({
        "my grandmother taught me", "my elders showed us",
        "our ancestral land", "indigenous knowledge keepers",
    }),
    # conservative / centrist / progressive start empty at v0.1; operator-curated growth
    "conservative": frozenset(),
    "centrist": frozenset(),
    "progressive": frozenset(),
})

def detect_dialect_drift(
    *,
    body_text: str,
    draft_dialect: Dialect,
) -> tuple[DialectDriftHit, ...]: ...
# Scans body_text for vocabulary tokens from OTHER dialects; returns hits for
# F-SCRIBE-DIALECT-DRIFT translation at R3 POST-gate.

def detect_identity_proxy_leaks(
    *,
    body_text: str,
    draft_dialect: Dialect,
    affirmed_identity_claims: tuple[IdentityClaim, ...],
) -> tuple[IdentityProxyLeak, ...]: ...
# Scans body_text for DIALECT_IDENTITY_PROXY_TABLE[draft_dialect] hits;
# rejects any hit without matching entry in affirmed_identity_claims.
# Feeds F-SCRIBE-DIALECT-INDUCED-IDENTITY at R3 POST-gate.

F_SCRIBE_DIALECT_DRIFT: Final[str] = "F-SCRIBE-DIALECT-DRIFT"
F_SCRIBE_DIALECT_INDUCED_IDENTITY: Final[str] = "F-SCRIBE-DIALECT-INDUCED-IDENTITY"
```

```python
# pipeline/seats/scribe/templates.py

@dataclass(frozen=True, kw_only=True, slots=True)
class ProgramTemplate:
    program_code: str
    template_path: str                                   # relative to templates_root
    section_overrides: Mapping[str, SectionSpec]
    required_content_cues: tuple[str, ...]
    dialect_default: Dialect
    template_content_sha3_512: str                       # full 128-hex
    template_at_utc: datetime

def load_program_template(
    *,
    program_code: str,
    templates_root: pathlib.Path,
    clock: ClockFn,
) -> ProgramTemplate: ...
# Reads <templates_root>/<program_code>.md via pathlib; computes sha3_512;
# does NOT yet parse section_overrides (v0.2 front-matter YAML parser);
# at R2 the operator hand-writes a companion .deps.json sidecar that declares
# section_overrides + required_content_cues + dialect_default. R3 migrates to
# Vault template-query primitive.

def verify_template_hash(
    *,
    template: ProgramTemplate,
    templates_root: pathlib.Path,
) -> bool: ...
# Re-reads file, recomputes hash, compares to pinned. Feeds F-SCRIBE-TEMPLATE-DRIFT
# PRE-gate at R3.

F_SCRIBE_TEMPLATE_DRIFT: Final[str] = "F-SCRIBE-TEMPLATE-DRIFT"
F_SCRIBE_INELIGIBLE_ACTIVITY: Final[str] = "F-SCRIBE-INELIGIBLE-ACTIVITY"
```

## §7 v1.1.1 compliance decisions (confirm at ORIENT)

1. **Unit-normalization table scope (§7.6).** R2 ships a LOCKED unit-normalization table: `1 year ↔ 12 months`, `1 ft ↔ 12 in`, `1 km ↔ 1000 m`, `$1,000 ↔ $1000` (comma removal), `1 acre ↔ 43560 sq ft`. Inline-literal in `smart.py`; rebind-resistant. Additions require R2 amendment.

2. **Qualitative-paraphrase v0.2 roadmap explicit.** `numeric_verbatim_check` is numeric-only. Qualitative paraphrase ("nearly half a decade" for "3 years" where the token is numeric) IS in scope (the "3" is the numeric token; "nearly half a decade" has no numeric token and fails the verbatim check). But "significant growth" → "substantial growth" (no numerics either side) is v0.2. Documented in module docstring.

3. **Dialect token detection strategy.** R2 uses simple case-insensitive substring matching with word-boundary anchors. Stop-word / polysemy ambiguity (e.g., "equity" appearing in a conservative finance draft meaning "shareholder equity") is a known false-positive source. Mitigation: dialect-drift detection is **advisory** (emits hits for R3's Logician POST-gate, which gates on threshold count + dialect-family distance). Single cross-dialect token does NOT hard-block; R3 POST-gate aggregates.

4. **Identity-proxy table v0.1 coverage.** Per §7.2 Law 5 POST-gate closed-set — R2 ships 4 soul_fire entries + empty sets for others. Operator curates via `pipeline/seats/scribe/dialect_identity_proxy_table.v1.json` sidecar (R2 loads from JSON at module-import time; falls back to inline `DIALECT_IDENTITY_PROXY_TABLE` if sidecar missing). v0.2 roadmap: ≥100 phrases across all four dialects + semantic-embedding supplement.

5. **Template format at v0.1.** `skills/scribe-ghostwriter/templates/<program>.md` plus `<program>.deps.json` sidecar carrying `section_overrides` + `required_content_cues` + `dialect_default`. R2 does NOT parse Markdown front-matter; sidecar is stdlib-JSON. v0.2 roadmap: YAML front-matter + single-file template.

6. **Template-root location at v0.1.** `skills/scribe-ghostwriter/templates/` per §7.9. R3 Vault migration relocates to `vault_shared/scribe_templates/`. R2 ships with the skills-root default + caller override `templates_root: pathlib.Path` so tests inject `tmp_path`.

7. **SectionDraft word/char counts caller-provided.** Per R1 decision 6; R2 ships a helper `count_words_and_chars(text: str) -> tuple[int, int]` in `draft.py` for caller convenience but does NOT reimpose computation at `__post_init__`. Tests pin both paths (caller-supplied, helper-supplied).

8. **Frozen mapping discipline** from R1 extends: every `Mapping` field copied into `MappingProxyType(dict(...))` at construction. `DIALECT_VOCABULARY` / `DIALECT_IDENTITY_PROXY_TABLE` / `section_overrides` all covered.

## Test plan (target coverage ≥95%; AST-lint R1-R7 clean; full-suite delta: +200 tests estimated)

**Happy paths** (~50 tests across 5 files):
- `test_draft.py` — SectionDraft constructs with 13-section full draft + claim_evidence_map + eligible_activity_map; word/char helper; every dataclass frozen + slots + kw_only.
- `test_smart.py` — SmartObjective validation pass/fail per S/M/A/R/T dimension; numeric_verbatim_check on a 500-word draft with 12 numeric tokens all matching; unit-normalization table coverage (5 pairs).
- `test_overlooked_expenses.py` — walk_checklist builds all 11 entries; needed_count consistency invariant; exhaustiveness raises on missing key.
- `test_dialect.py` — detect_dialect_drift on conservative body with 3 progressive tokens → 3 hits; detect_identity_proxy_leaks on soul_fire body with "ancestral land" claim AND no matching KGIE affirmation → 1 leak.
- `test_templates.py` — load_program_template on VAPG / REAP / SCBGP fixtures; verify_template_hash round-trip; mismatch on mutated fixture.

**Adversarial** (~100 tests × E-024 2× = ~200 effective):
- SMART: numeric tokens with locale variants (`$1,000` vs `$1.000` EU); `pathological paraphrase "5K" for "5000"` (claim-side accepts both via normalization); missing achievability_evidence; empty relevance_pointer.
- Overlooked: `needed_count` mismatch raises; mutation via `.entries = ...` raises FrozenInstanceError.
- Dialect: cross-dialect stop-word false-positives documented ("equity" in conservative — single hit, below POST-gate threshold); case-insensitive matching; Unicode-normalized matching.
- Templates: symlinked templates_root refused; hash-mismatch returns False not raises; empty template file accepted (hash computed on zero bytes).

**Property tests** (via hypothesis, ~25 tests):
- `numeric_verbatim_check` idempotence on fixed inputs.
- `walk_checklist.needed_count == sum(...)` holds for all generated entry permutations.
- `detect_dialect_drift` monotonicity: adding tokens cannot reduce hit count.
- `verify_template_hash` is pure (repeated calls with same inputs = same output).

**Corpus fixtures** (extend R1 `tests/corpus/scribe/v1/`):
- Add `drafts/vapg_section_5_smart/` — SMART-structured §7.5 section 5 draft with 8 objectives, each with full claim_evidence_map.
- Add `drafts/reap_numeric_paraphrase/` — pathological draft where "nearly 1000 kWh" cites source saying "800 kWh"; test pins F-SCRIBE-PARAPHRASED-NUMERIC detection.
- Add `templates/vapg.md` + `vapg.deps.json` + `reap.md` + `reap.deps.json` — minimal viable fixtures.

## Done definition

- [ ] 5 production modules ship: `draft.py` + `smart.py` + `overlooked_expenses.py` + `dialect.py` + `templates.py`.
- [ ] `__init__.py` `__all__` expanded with ~30 new public names.
- [ ] `BLUEPRINT_DEPS` extended with new §7 section citations (§7.5-§7.9) + new failure-code constants.
- [ ] 100% module coverage; full suite target +200 tests → ≥5406 baseline.
- [ ] AST-lint R1-R7 clean on `pipeline/seats/scribe/`.
- [ ] R1 modules untouched (regression guard: R2 is additive only).
- [ ] No imports of `pipeline.vault` / `pipeline.logician` / `pipeline.providers` / `pipeline.loop` — R2 stays stdlib + intra-module.
- [ ] `lock_history.v1.jsonl` R2 self-LOCK entry.
- [ ] MEMORY.md index + R2 round-recap memory file.
- [ ] Pre-stage R3 spec card — last round before LLM integration.

## Lines-of-code target (E-024 2× multiplier)

| File | Target | Target ±25% | Comment |
|------|--------|-------------|---------|
| `pipeline/seats/scribe/draft.py` | 200 | 150–250 | 5 dataclasses + 1 helper + `AdminRiskFlag` wrapper. |
| `pipeline/seats/scribe/smart.py` | 280 | 210–350 | SmartObjective + validate + numeric_verbatim_check + unit-normalization table. |
| `pipeline/seats/scribe/overlooked_expenses.py` | 180 | 135–225 | 11-item checklist + walker + exhaustiveness check. |
| `pipeline/seats/scribe/dialect.py` | 260 | 195–325 | 4 vocabulary tables + identity-proxy table + drift + leak detectors. |
| `pipeline/seats/scribe/templates.py` | 220 | 165–275 | loader + hash-verify + sidecar JSON parser. |
| `tests/seats/scribe/test_draft.py` | 350 | 260–440 | ~12 happy tests. |
| `tests/seats/scribe/test_smart.py` | 500 | 375–625 | ~15 happy + ~10 adv × 2×. |
| `tests/seats/scribe/test_overlooked_expenses.py` | 300 | 225–375 | ~12 tests. |
| `tests/seats/scribe/test_dialect.py` | 450 | 335–565 | ~15 happy + ~10 adv × 2×. |
| `tests/seats/scribe/test_templates.py` | 350 | 260–440 | ~10 happy + ~8 adv × 2×. |
| `tests/seats/scribe/test_adv_shapers.py` | 600 | 450–750 | Cross-module adversarial + hypothesis property tests. |

## Self-LOCK eligibility

**Eligible if single-cycle pass.** R2 is still pure-Python deterministic — unit-normalization tables + substring detection + JSON-sidecar loader + stdlib sha3_512. No LLM, no network, no subprocess. Follows R1 precedent (SELF-LOCKED without committee); committee credits conserved for R3 (Anthropic provider + subprocess envelope = material composition risk).

## R3+ preview

**R3** — `seat.py` stdin/stdout envelope (per §5 v6 `invoke_seat` contract), Anthropic `pipeline.providers.anthropic.complete()` call, admin-risk register integration (§7.11 query + flag generator), PRE/POST gate wiring through `pipeline.logician` (22 F-SCRIBE-* codes per §7.13), Vault `template-query` migration for §7.9, conversation-log append via §4.10 kind-class `conversation_log` dispatcher. Cross-family committee review recommended — first LLM-facing round of Scribe-as-pipeline-code.

## Open questions (resolve at ORIENT)

1. **Dialect-drift false-positive threshold.** R2 ships hits; R3 POST-gate aggregates. Propose threshold: ≥3 cross-dialect tokens in a single section → F-SCRIBE-DIALECT-DRIFT (default), operator-tunable at `scribe.dialect_drift_threshold` config row (v0.1 add to §0.5 v7 amendment? or defer to R3 spec-card?). Recommend: defer — R2 ships detection; R3 owns the threshold config row.

2. **Template sidecar parser robustness.** R2 uses `json.load()` for `.deps.json`. Malformed JSON → raise; what about missing `section_overrides` key? Propose: fail-closed — missing keys raise `ValueError`, operator must author complete sidecar. Mitigation: R2 ships 3 reference sidecars (VAPG / REAP / SCBGP) as copyable fixtures.

3. **Unit-normalization table v0.1 coverage.** 5 pairs cover the grant-writing hot path. Additions (kg/lb, °F/°C, gallons/liters) are v0.1.x iterations. Propose: ship R2 with the 5-pair LOCKED table; add a `pipeline.seats.scribe.smart.EXTENSIONS_V0_2_ROADMAP` comment block flagging known-omitted pairs.

4. **Numeric-verbatim byte-identity scope.** After unit normalization, do we require byte-identity on the numeric token itself, or allow trailing-zero variation (`1000` vs `1,000` vs `1000.00`)? Propose: normalize to stripped-comma integer string for integers; `Decimal`-canonical for fractions. Document the canonicalization in module docstring. Tests pin 6 canonical-form fixtures.
