# Spec card — pipeline.seats.scribe (Round 2: §7.5 draft composition — SectionDraft schema + composer)

**STATUS:** PRE-STAGED 2026-04-21 at Scribe R1 SELF-LOCK (lock_history row 120). R2 UNBLOCKED — §7.5 draft-output shapes compose over R1 types + the already-LOCKED §7.6-§7.9 primitives. Still zero-LLM, zero-network, zero-subprocess; the LLM call lands at R3 `seat.py`.

**Framework:** per `pipeline/templates/component_analysis_template.md` (Five Laws, Four Rules, failure-mode taxonomy, standard interface pattern — not restated).

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_07_scribe.md` **v1.1.1 LOCKED 2026-04-21** — principal source:
  - **§7.5** `SectionDraft`, `ClaimEvidence`, `EligibleActivityMatch`, `SectionLimit`, `ScopeCheckComment`, `AdminRiskFlag` (draft-output shapes + section-ordering invariant + per-section output contract)
  - **§7.10** `CompressedSectionDraft` wrapper (over-limit protocol; shape-level pin at R2, operator-ranking loop at R3)
  - **§7.2 Law 2** `eligible_activity_map` exhaustiveness invariant (R2 shape; R3 Logician POST-gate `F-SCRIBE-INELIGIBLE-ACTIVITY`)
  - **§7.2 Law 1** `claim_evidence_map` shape (R2 shape; R3 Logician POST-gate `F-SCRIBE-UNSOURCED-CLAIM`)
  - **§7.11** `AdminRiskFlag` in-shape surface (R2 shape only; admin-risk register query lands at R3)
- `pipeline/blueprint/v0.1/section_00_5_section_07_scribe_amendment.md` **§0.5 v7 LOCKED 2026-04-21** — R2 lands against rows:
  - `scribe.section_draft.v1` [NEEDED from §0.5 v7 — confirm row number at card-open]
  - `scribe.claim_evidence.v1`, `scribe.eligible_activity_match.v1`, `scribe.section_limit.v1`, `scribe.scope_check_comment.v1`, `scribe.admin_risk_flag.v1`, `scribe.compressed_section_draft.v1`
- `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 LOCKED — §4.2.1 PRE/POST-gate slot table carries the F-SCRIBE-* codes R2 shapes will feed at R3 wiring.

**Blueprint hash-at-card** (pre-fill at Round-open; recompute via `hashlib.sha3_512(path.read_bytes()).hexdigest()[:16]`):
- `section_07_scribe.md` v1.1.1 → currently pinned in `pipeline/seats/scribe/__init__.py` at `85b244a26888b52e` (verify at card-open; zero drift expected)
- `section_00_5_section_07_scribe_amendment.md` §0.5 v7 → currently pinned at `b99312d9a3ba3527` (verify at card-open)
- `section_04_logician.md` v2.1 → currently pinned at `e0507e6daaa18676` (verify at card-open)

**Spec-card version:** v1
**Round:** §7 Scribe Round 2 — draft composition (§7.5 SectionDraft + supporting draft-output shapes + composer wiring)
**Depends on:**
- R1 LOCKED row 120 — `pipeline.seats.scribe.types` + `pipeline.seats.scribe.kgie` (types + KGIE predicate)
- §7.6/§7.7/§7.8/§7.9 primitives — **already on disk and LOCKED per R1 `BLUEPRINT_DEPS.sections_implemented`** (`smart.py`, `overlooked_expenses.py`, `dialect.py`, `program_templates.py`; see OQ-1 for scope reconciliation with dispatch prompt)
- §6 Operating Envelope LOCK — **SATISFIED** 2026-04-21 v1-r1 (§7.15 interlock for Scribe R3; R2 code does not reach §6 surfaces)

**Canonical home:** `pipeline/seats/scribe/` (R1 path). New modules only; R1/R2-primitives files untouched.

---

## 1. Purpose

Ship the §7.5 draft-output shape layer + the deterministic composer that wires R1 types + R2 primitives (SMART / overlooked / dialect / program-template) into a single `SectionDraft`. R2 is the last pure-deterministic layer before R3's LLM-facing `seat.py` subprocess entry — after R2, Editor R1 and Judge R1 can typecheck and consume `SectionDraft` without waiting for the Anthropic provider call.

**R2 scope (shapes + composer, no LLM):**

1. `pipeline/seats/scribe/draft.py` — `SectionDraft` + `ClaimEvidence` + `EligibleActivityMatch` + `SectionLimit` + `ScopeCheckComment` + `AdminRiskFlag` dataclasses (§7.5 + §7.11 shape surface). Shape-level invariants via `__post_init__` (frozen kw_only slots; tuple-ization; tz-aware datetime; non-empty text fields where §7.5 pins them).
2. `pipeline/seats/scribe/over_limit.py` — `CompressedSectionDraft` wrapper (§7.10 shape) + `compute_word_char_counts(text) -> tuple[int, int]` helper. No operator-ranking loop at R2; the wrapper carries `source_uncut_draft_sha3_512` + `compression_rationale` as shape-level pins.
3. `pipeline/seats/scribe/composer.py` — pure-deterministic assembly function `compose_section_draft(...)` that takes R1 `RfaExtractedRecord` + R1 `KgiePreflightResult` (PASS precondition) + drafter-provided `body_text` + evidence map + eligible-activity map + already-computed R2 primitives (SMART list per section 5, `OverlookedExpensesWalk` for section 7, `DIALECT_VOCABULARY`-derived dialect, `ProgramTemplate` for program-code override) and returns a frozen `SectionDraft`. Pure: no LLM, no Vault, no logician.

**R2 does NOT ship:**
- Phase 2 drafting loop (LLM-dispatched; R3).
- `seat.py` stdin/stdout envelope (R3 per §5 v6 `invoke_seat` contract).
- Admin-risk register query / register read (§7.11 runtime read via Vault `admin-risk-register-query` skill; R3).
- Runtime PRE/POST-gate wiring (F-SCRIBE-UNSOURCED-CLAIM, F-SCRIBE-INELIGIBLE-ACTIVITY, F-SCRIBE-EVALUATION-CRITERION-MISSING, F-SCRIBE-SECTION-OVER-LIMIT-UNFLAGGED, F-SCRIBE-ADMIN-RISK-*, F-SCRIBE-DIALECT-DRIFT, F-SCRIBE-DIALECT-INDUCED-IDENTITY, F-SCRIBE-PARAPHRASED-NUMERIC, F-SCRIBE-TEMPLATE-DRIFT — all at R3 via `pipeline.logician`).
- Conversation-log USER_DATA anchor resolver (§7.4a — R3 under §6 persistence contract).
- Cross-family telemetry emission / SFR output (§D.3 / A3 — R3).

R2 ships the SHAPE + the composer wiring; R3 Logician turns the shape evidence into failure codes.

## 2. Module layout

```
pipeline/seats/scribe/
├── __init__.py                  # R1+R2-primitives already landed; R2-composition EXTENDS __all__ + BLUEPRINT_DEPS
├── types.py                     # R1 LOCKED (row 120)
├── kgie.py                      # R1 LOCKED (row 120)
├── smart.py                     # R2-primitive (already on disk per __init__.py sections_implemented)
├── overlooked_expenses.py       # R2-primitive (already on disk)
├── dialect.py                   # R2-primitive (already on disk)
├── program_templates.py         # R2-primitive (already on disk)
├── draft.py                     # R2-composition NEW — §7.5 SectionDraft + 5 support shapes
├── over_limit.py                # R2-composition NEW — §7.10 CompressedSectionDraft + word/char helper
└── composer.py                  # R2-composition NEW — pure compose_section_draft(...) wiring function
```

Corpus fixtures extend R1 layout at `tests/corpus/scribe/v1/`:
```
tests/corpus/scribe/v1/
├── pass/
│   ├── vapg_happy_path/       (R1 — KGIE fixture)
│   ├── vapg_section_5_smart/  (R2 NEW — full §7.5 section 5 SectionDraft with 8 SMART objectives)
│   ├── reap_happy_path/       (R1)
│   └── scbgp_budget_walk/     (R2 NEW — §7.5 section 7 Budget + §7.7 walk with needed_count=0)
└── fail/
    ├── missing_geography/                 (R1 — KGIE)
    ├── identity_claim_no_source/          (R1)
    ├── experience_critical_gap/           (R1)
    ├── ineligible_activity_unmapped/      (R2 NEW — eligible_activity_map exhaustiveness gap)
    └── over_limit_unflagged/              (R2 NEW — over-limit body_text with over_limit_flag=False)
```

## 3. Public API additions (R2-composition)

Draft-output shapes per §7.5 (frozen, kw_only, slots=True — A-13 memory-layout discipline):

```python
# pipeline/seats/scribe/draft.py

@dataclass(frozen=True, kw_only=True, slots=True)
class SectionLimit:
    """§7.5 per-section RFA limit. limit_kind pinned closed-set."""
    limit_kind: Literal["words", "characters", "pages"]
    limit_value: int   # must be > 0 — __post_init__ enforces

@dataclass(frozen=True, kw_only=True, slots=True)
class ClaimEvidence:
    """§7.2 Law 1 — every factual claim maps to RFA / PROJECT_CONTEXT / USER_DATA.
    evidence_kind closed-set; evidence_ref non-empty.
    """
    claim_text: str
    evidence_kind: Literal["RFA", "PROJECT_CONTEXT", "USER_DATA"]
    evidence_ref: str

@dataclass(frozen=True, kw_only=True, slots=True)
class EligibleActivityMatch:
    """§7.2 Law 2 — every activity phrase in body_text maps to an
    RfaExtractedRecord.eligible_project_activities entry (or None with
    match_kind == 'scope_check_needed').
    """
    activity_phrase: str
    matched_rfa_activity: str | None
    match_kind: Literal["exact", "paraphrase", "scope_check_needed"]

@dataclass(frozen=True, kw_only=True, slots=True)
class ScopeCheckComment:
    """§7.5 [SCOPE-CHECK] flag — proposed activity that could be boundary drift."""
    activity_phrase: str
    reason: str

@dataclass(frozen=True, kw_only=True, slots=True)
class AdminRiskFlag:
    """§7.11 in-shape surface. severity closed-set per §7.11.
    operator_approved False by default; R3 sets True on explicit approval.
    proposed_substitution None when the admin-risk register offers no
    canonical substitution.
    """
    flagged_term: str
    severity: Literal["low", "medium", "high"]
    proposed_substitution: str | None
    operator_approved: bool

@dataclass(frozen=True, kw_only=True, slots=True)
class SectionDraft:
    """§7.5 per-section output contract. Consumed by Editor (§8) and Judge (§9).

    Invariants enforced at __post_init__:
    - section_name non-empty.
    - section_order >= 1.
    - body_text non-empty string.
    - word_count == caller-supplied OR recomputed via compute_word_char_counts
      (caller must pass consistent values; see §7 decision 7 in prior shapers card).
    - rfa_section_limit: if present, word_count/character_count/page-estimate
      must be <= limit_value UNLESS over_limit_flag is True.
    - draft_dialect in {conservative, centrist, progressive, soul_fire}.
    - drafted_at_utc tz-aware.
    - Tuple fields: claim_evidence_map / eligible_activity_map /
      admin_risk_flags / scope_check_comments all coerced to tuple.
    """
    section_name: str
    section_order: int
    body_text: str
    word_count: int
    character_count: int
    rfa_section_limit: SectionLimit | None
    over_limit_flag: bool
    claim_evidence_map: tuple[ClaimEvidence, ...]
    eligible_activity_map: tuple[EligibleActivityMatch, ...]
    admin_risk_flags: tuple[AdminRiskFlag, ...]
    scope_check_comments: tuple[ScopeCheckComment, ...]
    draft_dialect: Literal["conservative", "centrist", "progressive", "soul_fire"]
    drafted_at_utc: datetime
```

§7.10 wrapper + helper:

```python
# pipeline/seats/scribe/over_limit.py

@dataclass(frozen=True, kw_only=True, slots=True)
class CompressedSectionDraft:
    """§7.10 — wraps an uncut SectionDraft with a compressed version.
    source_uncut_draft_sha3_512: 128-hex SHA-3-512 of the uncut body_text
    (canonical UTF-8 NFC bytes).
    compression_rationale: tuple of operator-supplied rank decisions.
    """
    uncut: SectionDraft
    compressed: SectionDraft
    source_uncut_draft_sha3_512: str         # 128-hex; __post_init__ validates
    compression_rationale: tuple[str, ...]

def compute_word_char_counts(text: str) -> tuple[int, int]:
    """Whitespace-split word count + UTF-8 char count. Caller convenience;
    SectionDraft does NOT recompute at __post_init__ (caller-responsibility
    pattern from prior shapers spec-card decision 7). Tests pin both paths.
    """
```

Composer (pure-deterministic wiring; no LLM, no I/O):

```python
# pipeline/seats/scribe/composer.py

_ComposerClock = ClockFn   # alias re-export from kgie

def compose_section_draft(
    *,
    rfa: RfaExtractedRecord,
    kgie_result: KgiePreflightResult,     # status=="pass" precondition
    section_name: str,
    section_order: int,
    body_text: str,
    claim_evidence_map: tuple[ClaimEvidence, ...],
    eligible_activity_map: tuple[EligibleActivityMatch, ...],
    draft_dialect: Dialect,
    rfa_section_limit: SectionLimit | None = None,
    admin_risk_flags: tuple[AdminRiskFlag, ...] = (),
    scope_check_comments: tuple[ScopeCheckComment, ...] = (),
    program_template: ProgramTemplate | None = None,
    clock: _ComposerClock = _default_utc_now,
) -> SectionDraft:
    """Assemble a SectionDraft. Raises ValueError on KGIE precondition
    violation (status != 'pass'). Does NOT fire failure codes — that is R3
    Logician wiring. Raises shape-level errors only.

    Over-limit detection: if rfa_section_limit is present AND
    word_count > limit (or character_count > limit, by kind), sets
    over_limit_flag=True; caller chooses whether to pair with
    CompressedSectionDraft.
    """
```

All three modules import from stdlib + `pipeline.seats.scribe.{types, kgie, smart, overlooked_expenses, dialect, program_templates}` only. No `pipeline.logician` / `pipeline.vault` / `pipeline.providers` / `pipeline.loop` imports — R2-composition preserves R1 import discipline (per `pipeline/seats/scribe/__init__.py` docstring paragraph on import discipline).

## 4. Design decisions

1. **SectionDraft is the contract Editor R1 + Judge R1 consume.** R2-composition ships the type; Editor/Judge R1 typecheck and round-trip through it without waiting for R3's LLM path. This is the load-bearing §7.12 handoff-contract shape.
2. **`over_limit_flag` is on `SectionDraft` (not inferred at `__post_init__`).** §7.5 + §7.10 pin the uncut draft is emitted WITH the flag; the caller (composer at R2, LLM drafter at R3) sets it. `__post_init__` validates consistency (limit present AND counts exceed → flag MUST be True; counts within limit → flag MAY be False; no limit → flag MAY be False). Permits the §7.10 operator-ranking loop at R3 without a shape churn.
3. **`CompressedSectionDraft` carries both uncut + compressed at R2.** §7.10 shape-level pin. Operator-ranking loop + compression heuristic lands at R3 (LLM-assisted compression). R2 ships the wrapper so downstream Editor/Judge can typecheck against it.
4. **`claim_evidence_map` + `eligible_activity_map` are tuples, not dicts.** Exhaustiveness checks at R3 POST-gate require ordered iteration; `Mapping` would obscure duplicate-phrase cases. `tuple[ClaimEvidence, ...]` preserves drafter ordering and allows duplicates (a single phrase may trace to multiple evidence entries).
5. **`AdminRiskFlag.operator_approved` defaults to False; no silent True at R2.** §7.2 Law 4 invariant — never silently rewrite. R3 sets True only after operator approval surface fires and operator explicitly approves.
6. **`compose_section_draft` is pure.** No `pipeline.vault` read (admin-risk register is a §7.11 runtime read at R3), no `pipeline.logician` (POST-gate codes at R3), no LLM. R2's composer is the deterministic skeleton an R3 LLM drafter will populate `body_text` into.
7. **KGIE PASS precondition at composer entry.** §7.4 pins "Scribe refuses to draft if KGIE fails." R2's composer enforces at the type-boundary: `ValueError` on `kgie_result.status != "pass"`. R3 will translate this into `F-SCRIBE-KGIE-FAIL` at PRE-gate; R2 raises to keep the shape contract honest when called outside the Logician-gated path (tests, composition primitives).
8. **`SectionDraft.drafted_at_utc` uses injected clock (E-017).** 12th firing of the injected-callable pattern. Tests pin determinism; production default is `datetime.now(tz=timezone.utc)`.
9. **V1 inline-literal rebind-resistance on every closed-set.** `_DIALECT_VALID`, `_EVIDENCE_KIND_VALID`, `_LIMIT_KIND_VALID`, `_SEVERITY_VALID`, `_MATCH_KIND_VALID` — all module-top `Final[frozenset[str]]` matching R1 precedent (`_KGIE_STATUS_VALID`, `_KEYWORD_AFFIRMATION_VALID`). Rebind attempts OUT-OF-MODEL per CPython semantics; tests pin the discipline.
10. **BLUEPRINT_DEPS extension** (per §4.6):
    ```python
    BLUEPRINT_DEPS["section_07_scribe.md"]["sections_implemented"] += [
        "§7.5 SectionDraft + ClaimEvidence + EligibleActivityMatch + SectionLimit + ScopeCheckComment",
        "§7.10 CompressedSectionDraft wrapper (shape-level; R3 wires operator-ranking loop)",
        "§7.11 AdminRiskFlag shape (R3 wires admin-risk register read)",
    ]
    BLUEPRINT_DEPS["section_00_5_section_07_scribe_amendment.md"]["sections_implemented"] += [
        # [NEEDED from §0.5 v7 — confirm row numbers at card-open]
        "§A rows <N1-Nk> (section_draft + claim_evidence + eligible_activity_match + ...)",
    ]
    ```

## 5. Invariant checklist (per-dataclass `__post_init__`)

- `SectionLimit`: `limit_kind ∈ _LIMIT_KIND_VALID`; `limit_value > 0`.
- `ClaimEvidence`: `claim_text.strip()` non-empty; `evidence_kind ∈ _EVIDENCE_KIND_VALID`; `evidence_ref.strip()` non-empty.
- `EligibleActivityMatch`: `activity_phrase.strip()` non-empty; `match_kind ∈ _MATCH_KIND_VALID`; if `match_kind in {"exact","paraphrase"}` then `matched_rfa_activity` non-None AND non-empty; if `match_kind == "scope_check_needed"` then `matched_rfa_activity is None`.
- `ScopeCheckComment`: both fields non-empty.
- `AdminRiskFlag`: `flagged_term.strip()` non-empty; `severity ∈ _SEVERITY_VALID`; `operator_approved` is bool.
- `SectionDraft`: `section_name.strip()` non-empty; `section_order >= 1`; `body_text` non-empty; `word_count >= 0`; `character_count >= 0`; `draft_dialect ∈ _DIALECT_VALID`; `drafted_at_utc.tzinfo is not None`; tuple fields coerced via `tuple(...)`; over-limit consistency per decision 2.
- `CompressedSectionDraft`: `len(source_uncut_draft_sha3_512) == 128` AND lowercase hex; `uncut.section_name == compressed.section_name`; `uncut.section_order == compressed.section_order`; `compressed.over_limit_flag is False`; `len(compression_rationale) >= 1`.

## 6. Discipline requirements

Per `pipeline/templates/component_analysis_template.md` (not restated) + the R1-established patterns:

- **V1 inline-literal rebind-resistance** — every closed-set enumeration as module-top `Final[frozenset[str]]`; no `Literal[...]` runtime inspection. Matches R1 `_KGIE_STATUS_VALID` precedent.
- **E-017 provider-seam pattern** — `composer.py` carries a `_ComposerClock = ClockFn` alias re-export; no `datetime.utcnow()` anywhere. 12th consecutive firing.
- **E-023 residual handling** — composer does NOT silently drop evidence-map entries with unknown `evidence_kind`; construction raises; R3 translates to `F-SCRIBE-UNSOURCED-CLAIM` at POST-gate.
- **Threat-model docstring** — `draft.py` module-docstring enumerates the three Law-enforcement sites the shape feeds (Law 1 claim_evidence, Law 2 eligible_activity, Law 4 admin_risk_flags + draft_dialect, Law 5 dialect-identity proxy via §7.8 primitive). Pin where R3 wires each code.
- **E-024 test-count multiplier** — R2-composition test surface targets 30+ tests per module with E-024 ~1.5-2× multiplier on adversarial (E-023 residual handling + Protocol seam coverage). Target ~150 tests total for three modules.
- **E-026 module-lineage discipline** — `composer.py` imports `ClockFn` via `from pipeline.seats.scribe.kgie import ClockFn`, never re-declares; single-source-of-truth pattern for Protocol seams.
- **E-027 payload-size pre-check** — at committee dispatch (if escalated), per-module split recommended to keep qwen3-32b under 80k prompt tokens. R2-composition is 3 small modules; per-module dispatch conserves format compliance.
- **E-028 transport-retry discipline** — not code-surface at R2, but spec card flags that if committee fires, single 60s-backoff retry on transport errors per L-005 §8; non-transport errors escalate immediately.
- **Fail-closed on KGIE violation** — composer raises ValueError on `kgie_result.status != "pass"`. R3 translates; R2 keeps the shape contract honest.

## 7. Testing budget (target: ~150 tests; coverage ≥ 95%)

**`test_draft.py` (~40 tests):**
- Every dataclass constructible with full field set (6 × happy + 6 × frozen-invariant).
- `SectionDraft.__post_init__` over-limit consistency: (a) limit present, counts exceed, flag True → valid; (b) limit present, counts exceed, flag False → raises; (c) limit present, counts within, flag True → allowed; (d) no limit, any flag value → allowed.
- `ClaimEvidence` evidence_kind closed-set enforcement (3 valid + 3 invalid-literal-string rejections).
- `EligibleActivityMatch` match_kind + matched_rfa_activity consistency (4 valid + 3 invalid combinations).
- Tuple coercion: pass `list` → stored as `tuple`; pass `None` → raises at shape level.
- `__all__` surface matches exactly; no leakage.

**`test_over_limit.py` (~25 tests):**
- `CompressedSectionDraft` constructs with paired uncut + compressed.
- `source_uncut_draft_sha3_512` 128-hex validation (length 127/129, non-hex rejection).
- `compressed.over_limit_flag is False` invariant (raises if True).
- `compute_word_char_counts`: empty string, whitespace-only, multi-line, Unicode NFC, UTF-8 multi-byte.
- Idempotence: counts over same input twice → equal.

**`test_composer.py` (~45 tests):**
- Happy-path compose from R1 fixtures (VAPG + REAP + SCBGP + SARE) — produces valid `SectionDraft` per program.
- KGIE status='fail' → raises ValueError at composer entry.
- KGIE status='needs_operator_input' → raises ValueError at composer entry.
- Missing `rfa_section_limit` + long body_text → over_limit_flag=False (no limit to breach).
- Present `rfa_section_limit.limit_kind='words'`, word_count exceeds → over_limit_flag=True.
- Present `rfa_section_limit.limit_kind='characters'`, char_count exceeds → over_limit_flag=True.
- Clock injection determinism: fixed clock → identical `drafted_at_utc` across calls.
- Admin-risk flags + scope-check comments pass-through (composer does not mutate).
- `program_template` passed: `program_template.dialect_default` matches `draft_dialect` (warn-level pin at R2; R3 enforces).
- `eligible_activity_map` with mixed match_kind entries composes cleanly.
- `claim_evidence_map` with duplicate activity_phrase entries preserved (drafter authored duplicates on purpose).

**Adversarial (~20 tests, E-024 multiplier):**
- `object.__setattr__` on frozen `SectionDraft` field raises (OUT-OF-MODEL documentation).
- Round-trip through `dataclasses.asdict` + reconstruction preserves invariants.
- Malformed `draft_dialect` string ("PROGRESSIVE" uppercase, "soul-fire" with hyphen) rejected at shape level.
- `drafted_at_utc` naive datetime rejected.
- `SectionDraft` with 1000-entry `claim_evidence_map` constructs under 100ms (performance floor, not a tight bench).
- Hypothesis property: `compose_section_draft` idempotent under fixed clock across 1000 random input permutations.
- Hypothesis property: every `SectionDraft` with `over_limit_flag=True` AND `rfa_section_limit is not None` has counts exceeding limit.

**Corpus-driven (~15 tests):**
- `tests/corpus/scribe/v1/pass/vapg_section_5_smart/` — 8-objective section 5 SectionDraft with full claim_evidence_map; composer test asserts round-trip.
- `tests/corpus/scribe/v1/pass/scbgp_budget_walk/` — section 7 Budget + `OverlookedExpensesWalk(needed_count=0)`; asserts composer composes cleanly.
- `tests/corpus/scribe/v1/fail/ineligible_activity_unmapped/` — body_text with 3 activity phrases; eligible_activity_map only maps 2; test asserts R3's future POST-gate would fire (R2 records the shape, does NOT fire).
- `tests/corpus/scribe/v1/fail/over_limit_unflagged/` — composer produces SectionDraft with over_limit_flag=False while body exceeds limit; test asserts `__post_init__` raises.

## 8. Verification

- **Full suite green** — current baseline 5206 pass post-R1 LOCK (row 120); R2-composition expected delta +130-170 tests → target ≥5336.
- **AST-lint R1-R7 clean** on `pipeline/seats/` tree (lint_tree(Path('pipeline/seats'), DEFAULT_RULES) → 0 violations).
- **BLUEPRINT_DEPS pin verified** — R2 extends `pipeline/seats/scribe/__init__.py::BLUEPRINT_DEPS` with §7.5 / §7.10 / §7.11 rows; L-015 regression test `tests/vault/test_blueprint_deps_citations.py` scope-expansion to `pipeline/seats/` (if not landed at R1, queue as pre-LOCK task).
- **Coverage ≥ 95%** on `pipeline/seats/scribe/{draft,over_limit,composer}.py` (R1 achieved 100%; hold the bar).
- **Import-discipline verified** — no imports of `pipeline.logician` / `pipeline.vault` / `pipeline.providers` / `pipeline.loop` in R2-composition files.

## 9. Done definition

- Three new modules ship at `pipeline/seats/scribe/{draft,over_limit,composer}.py`.
- `pipeline/seats/scribe/__init__.py` re-exports new public symbols; `__all__` extended; `BLUEPRINT_DEPS` updated with §7.5 / §7.10 / §7.11 citations.
- R1 modules (`types.py`, `kgie.py`) and R2-primitive modules (`smart.py`, `overlooked_expenses.py`, `dialect.py`, `program_templates.py`) untouched — regression guard.
- Tests landed; coverage met; AST-lint clean; full suite delta positive.
- LOCK row appended to `pipeline/engineering/lock_history.v1.jsonl` with reviewer tokens (self-LOCK → 0), test count, sections_implemented list, self-audit narrative.
- Memory entry authored at `~/.claude/projects/-Users-goldenquill-Downloads-GoldenQuill/memory/project_impl_section_07_scribe_round_2_locked.md`.
- MEMORY.md top entry prepended.
- Session metrics entry appended per `pipeline/metrics/SESSION_METRICS_SPEC.md`.
- Self-LOCK eligible per R1 precedent (pure Python, shape + one pure composer; no LLM, no network, no subprocess). Escalate to committee only if any §5 invariant (decisions 1-10) is authored differently than the blueprint pins.

## 10. Unblocks

- **Editor R1** — consumes `SectionDraft` schema (§7.12 handoff contract). Editor's clarity review + goal/output/outcome/objective sorting reads `SectionDraft.body_text` + `SectionDraft.claim_evidence_map` + `SectionDraft.eligible_activity_map` + `SectionDraft.admin_risk_flags`. Without R2 SectionDraft shape, Editor R1 cannot typecheck its input.
- **Judge R1** — consumes finalized `SectionDraft` + `claim_evidence_map` (§7.12 + architecture §D.4). Judge scores against funder rubric; rubric-rows map to `SectionDraft.body_text` spans + `evaluation_criteria` traces. Without R2 SectionDraft shape, Judge R1 cannot typecheck its input.
- **Scribe R3** — consumes R2 composer as the deterministic skeleton the LLM drafter populates. R3 adds: Anthropic provider call, admin-risk register read via Vault query skill, PRE/POST-gate wiring through pipeline.logician, Vault draft-manifest write, SFR emission, subprocess entry.

## 11. Committee composition (if escalated)

Scribe production binding = Anthropic per `router.yaml` row 31; code-reviewer committee rows 71-87 are codex / qwen3-32b / llama-3.3-70b / gpt-oss-120b / kimi-k2 — none Anthropic. Cross-family clean (A3).

**Self-LOCK recommendation** per R1 precedent (row 120 self-LOCK, zero committee dispatch). R2-composition is:
- Pure-Python shape + one pure composer function.
- No I/O, no LLM, no subprocess, no network.
- No new closed-set enumerations beyond what §7.5 + §7.10 + §7.11 pin verbatim.
- Composes over already-LOCKED R1 + R2-primitive surfaces.

Committee credits conserved for R3 (first LLM-facing round; Anthropic provider call + subprocess-envelope + cross-family telemetry = material composition risk).

Escalate only if:
- Any shape field is authored differently than §7.5 pins (e.g., dict instead of tuple, `Mapping` instead of frozen tuple).
- Composer introduces a subjective decision not in §7.5 (e.g., auto-computing word_count at `__post_init__` rather than caller-supplied).
- Over-limit detection logic requires a subjective choice between `word_count` and `character_count` when both present (§7.10 pin is explicit on this; verify at card-open).

## 12. Open questions for operator

- **OQ-1 — Scope reconciliation with dispatch prompt.** Dispatch prompt framed R2 as "§7.6 SMART + §7.7 overlooked-expenses + §7.8 dialect + §7.9 program-template," but `pipeline/seats/scribe/__init__.py` already re-exports `smart.py`, `overlooked_expenses.py`, `dialect.py`, `program_templates.py` and `BLUEPRINT_DEPS.sections_implemented` lists §7.6/§7.7/§7.8/§7.9 as LOCKED. Three plausible readings: (a) R1 LOCK (row 120) silently absorbed §7.6-§7.9 into R1 and the dispatch prompt's R2 scope is now stale — this R2 should be §7.5 draft-composition; (b) R2-primitive modules are on disk but NOT yet in lock_history — a separate LOCK row is needed for them before this R2-composition round proceeds; (c) the prior spec cards (`section_07_scribe_round_2_drafting_primitives.md` and `section_07_scribe_round_2_shapers.md`) were BOTH superseded by a silent merge. **Recommendation:** (a) — this spec card proceeds as §7.5 draft-composition, which is what Editor R1 + Judge R1 actually need to consume (Editor/Judge both need `SectionDraft`, not the R2-primitives). Operator confirms: treat §7.6-§7.9 primitives as landed; this R2 = draft composition; append a row 120.b to `lock_history.v1.jsonl` covering §7.6-§7.9 primitives if the silent-merge reading (c) holds.
- **OQ-2 — SectionDraft.word_count source of truth.** §7.5 pins both `word_count: int` and `character_count: int` as caller-supplied. Prior shapers spec card decision 7 pinned caller-responsibility. Confirm R2 keeps caller-supplied (operator-friendly for ad-hoc composition; R3 LLM drafter passes both). **Recommendation:** caller-supplied, with `compute_word_char_counts` in `over_limit.py` as convenience helper; `__post_init__` does NOT recompute (would be O(n) over body_text on every draft construction).
- **OQ-3 — `over_limit_flag` over-character vs over-words disambiguation.** §7.10 describes word/char/page limits but does not pin whether `over_limit_flag=True` requires BOTH counts to exceed (when limit_kind permits either) or EITHER count. **Recommendation:** `limit_kind` is singular (one of {words, characters, pages}); composer checks only the kind the RFA pins. If RFA has two separate limits (rare), this is a v0.2 shape extension — out of scope here.
- **OQ-4 — §0.5 v7 row numbers for R2-composition primitives.** R2 lands six new dataclasses (`SectionDraft`, `ClaimEvidence`, `EligibleActivityMatch`, `SectionLimit`, `ScopeCheckComment`, `AdminRiskFlag`) + `CompressedSectionDraft`. `pipeline/seats/scribe/__init__.py::BLUEPRINT_DEPS["section_00_5_section_07_scribe_amendment.md"]["sections_implemented"]` currently lists rows 118-124 + 132-135 + 154. R2-composition needs new rows (proposed: 125-131 for the new shapes, one row per). **Recommendation:** operator confirms row-append is in scope for R2 LOCK OR that `[NEEDED from §0.5 v7 — confirm row numbers at card-open]` resolves to an existing row range already reserved in the amendment.
- **OQ-5 — AdminRiskFlag at R2 without admin-risk register.** `AdminRiskFlag` shape ships at R2 but the admin-risk register query is R3 (Vault `admin-risk-register-query` skill). Dev-mode test fixtures for R2 hand-populate `AdminRiskFlag` entries. **Recommendation:** proceed; R2 ships the SHAPE Editor/Judge consume; R3 wires the register read. R2 test fixtures carry representative `AdminRiskFlag` entries drawn from the 18-entry v0.1 register per `project_openclaw_state.md` memory, without reading the register file (pure fixtures).

## 13. Non-goals at R2-composition

- No LLM call — zero across R2.
- No admin-risk register read — R3 via Vault query skill.
- No claim-evidence grep POST-gate — R3 via Logician.
- No eligible-activity exhaustiveness POST-gate — R3 via Logician (R2 ships the shape that POST-gate walks).
- No over-limit operator-ranking loop — R3 (R2 ships `CompressedSectionDraft` shape only).
- No conversation-log USER_DATA anchor resolution — R3 under §6.
- No SFR emission — R3.
- No subprocess entry — R3.
- No seat-runner invocation wiring — R3.

## 14. Changelog

- **v1 PRE-STAGED 2026-04-21** — authored at Scribe R1 SELF-LOCK closeout (lock_history row 120). R2-composition scoped as §7.5 draft-output shape layer + composer wiring, treating §7.6-§7.9 primitives as already-LOCKED per R1 `BLUEPRINT_DEPS.sections_implemented` (see OQ-1 for scope reconciliation). Unblocks Editor R1 + Judge R1 consumption of `SectionDraft`.

## 15. Artifacts (placeholders for LOCK)

- **lock_history row** — row 121 (next after row 120 R1). JSONL entry at `pipeline/engineering/lock_history.v1.jsonl`. Template: `{"row": 121, "module": "pipeline.seats.scribe (Round 2: draft composition)", "blueprint_section": "section_07_scribe.md", "blueprint_version": "v1.1.1", "blueprint_hash_at_lock_prefix_section_07": "<recompute>", "lock_timestamp_utc": "<ISO8601>", "lock_class": "code", "round_name": "§7 Scribe Round 2 — draft composition (§7.5 + §7.10 + §7.11 shape surface + composer)", "lock_mode": "SELF-LOCKED (first-cycle, zero committee dispatch)", "modules_landed": [{"path": "pipeline/seats/scribe/draft.py", "lines": <N>, "sha3_512_prefix16": "<hash>"}, {"path": "pipeline/seats/scribe/over_limit.py", ...}, {"path": "pipeline/seats/scribe/composer.py", ...}], "tests_landed": [...], "fixtures_landed": [...], "coverage_pct_module": <N>, "tests_added": <N>, "full_suite_tests_green": <N>, "ast_lint_violations": 0, "sections_implemented": ["§7.5 SectionDraft + ClaimEvidence + EligibleActivityMatch + SectionLimit + ScopeCheckComment + AdminRiskFlag", "§7.10 CompressedSectionDraft shape", "§7.11 AdminRiskFlag shape"], "sections_deferred_to_r3": ["§7.1 seat.py subprocess entry", "Anthropic provider call", "§7.11 admin-risk register read", "Logician PRE/POST-gate wiring", "§6 conversation-log USER_DATA resolution", "SFR emission"], "unblocks": ["Editor R1 (SectionDraft schema)", "Judge R1 (SectionDraft + claim_evidence_map)"]}`.
- **Memory recap** — `~/.claude/projects/-Users-goldenquill-Downloads-GoldenQuill/memory/project_impl_section_07_scribe_round_2_locked.md`. Fact / Why / How / Artifacts / Unblocks structure per precedent.
- **MEMORY.md prepend** — top entry: "Scribe R2 (draft composition) LOCKED — §7.5 SectionDraft shipped. Editor R1 + Judge R1 unblocked. Row 121."
- **Session metrics** — entry appended to `pipeline/metrics/session_log.jsonl` per `pipeline/metrics/SESSION_METRICS_SPEC.md`.

*End spec card — PRE-STAGED to dispatch at Code-session open. No §6 / Thesis gate; R1 LOCKED (row 120); §7.6-§7.9 primitives landed.*
