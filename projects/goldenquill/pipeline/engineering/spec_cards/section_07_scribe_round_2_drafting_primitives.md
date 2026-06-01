# Spec card — §7 Scribe Round 2 — drafting primitives

**Parent spec:** `pipeline/engineering/spec_cards/section_7_council_seats_pipeline_modules.md`

**Prior round:** Scribe R1 SELF-LOCKED 2026-04-21 — see
`pipeline/engineering/spec_cards/section_07_scribe_round_1_types_and_kgie.md`.

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_07_scribe.md` v1.1.1 LOCKED 2026-04-21
  — §7.6, §7.7, §7.8, §7.9, §7.2 (Law 5 dialect-identity table).
- `pipeline/blueprint/v0.1/section_00_5_section_07_scribe_amendment.md`
  §0.5 v7 LOCKED 2026-04-21 — rows 120 (smart_objective), 121
  (overlooked_expenses_walk), 122 (program_template), 123
  (dialect_register), 124 (dialect_identity_proxy_table).

## 1. Purpose

Ship the deterministic drafting-primitive modules that R3 (Anthropic Scribe
seat runner) will compose to build section drafts. R2 is PURE DATA + PURE
PREDICATES — zero LLM calls, zero network, zero subprocess. Same
pure-deterministic discipline as R1.

**R2 does NOT ship:**
- Phase 2 drafting loop (LLM-dispatched; R3).
- `SectionDraft` / `EligibleActivityMatch` / `ClaimEvidenceEntry` shapes
  (those are authored in R3 alongside the drafting loop that produces them;
  §7.5 pins them).
- Conversation-log persistence / USER_DATA anchor resolver (§7.4a — R3
  after §6 v1-r1 INTERLOCK surfaces land).
- AdminRiskFlag / admin-risk register integration (§7.11, §7.16 — R3).
- Runtime POST-gate wiring (F-SCRIBE-SMART-INVENTED-METRIC,
  F-SCRIBE-OVERLOOKED-EXPENSE-UNRESOLVED, F-SCRIBE-DIALECT-DRIFT,
  F-SCRIBE-DIALECT-INDUCED-IDENTITY, F-SCRIBE-TEMPLATE-DRIFT — all at R3
  through pipeline.logician PRE/POST dispatch).

R2 lands the SHAPES + PURE HELPERS those future POST-gates will query.

## 2. Module layout

```
pipeline/seats/scribe/
├── __init__.py                 # R1 landed; R2 extends __all__ + BLUEPRINT_DEPS
├── types.py                    # R1 landed
├── kgie.py                     # R1 landed
├── smart.py                    # R2 — SmartObjective + validator
├── overlooked_expenses.py      # R2 — walk primitive + checklist
├── dialect.py                  # R2 — dialect enum + vocab table + drift checker
└── program_templates.py        # R2 — template shape + known-program registry
```

No sub-packages. Each module is single-purpose. Coverage target ≥ 95% per
module (R1 landed 100%).

## 3. Public API

### 3.1 `smart.py`

```python
@dataclass(frozen=True, kw_only=True, slots=True)
class SmartObjective:
    objective_text: str
    outcome_text: str
    measurement_text: str
    timeline_text: str
    achievability_evidence: str      # pointer to PROJECT_CONTEXT field
    relevance_pointer: tuple[str, ...]  # evaluation_criteria names

# Construction-time invariants (non-empty strings for the 5 SMART text
# fields; relevance_pointer may be empty tuple when the drafter has not yet
# assigned a criterion — R3 POST-gate F-SCRIBE-EVALUATION-CRITERION-MISSING
# catches the full-draft exhaustiveness violation).

def validate_smart_objective(obj: SmartObjective) -> tuple[str, ...]:
    """Return tuple of violation codes (empty tuple = valid)."""

def extract_numeric_tokens(text: str) -> tuple[str, ...]:
    """§7.6 numeric-verbatim helper — extract every numeric token
    (integer / decimal / percent / money) in canonical form."""

def check_numeric_verbatim(
    claim_text: str,
    evidence_text: str,
) -> tuple[str, ...]:
    """§7.6 pin — returns tuple of numeric tokens from claim that do NOT
    appear byte-identical in evidence. Empty tuple = verbatim-clean."""
```

### 3.2 `overlooked_expenses.py`

```python
ExpenseStatus = Literal["included", "n_a", "needed"]

DEFAULT_CHECKLIST: Final[tuple[str, ...]] = (
    "In-kind space and utilities",
    "Volunteer / board labor (match value)",
    "Printing, postage, branding, translation",
    "Audit and grant-reporting costs",
    "Compliance (FDA, GAP, organic, FSMA)",
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
    status: ExpenseStatus
    rationale: str   # non-empty when status ∈ {"included", "n_a"}; may be
                     # empty when "needed" (operator will supply later)

@dataclass(frozen=True, kw_only=True, slots=True)
class OverlookedExpensesWalk:
    walk_at_utc: datetime
    entries: tuple[OverlookedExpenseEntry, ...]
    needed_count: int  # MUST == count(status == "needed") — invariant
    rfa_indirect_costs_allowed: bool | None

def build_walk(
    entries: tuple[OverlookedExpenseEntry, ...],
    *,
    rfa_indirect_costs_allowed: bool | None,
    clock: ClockFn = _default_utc_now,
) -> OverlookedExpensesWalk

def is_finalizable(walk: OverlookedExpensesWalk) -> bool:
    """§7.7 pin — True iff walk.needed_count == 0."""
```

### 3.3 `dialect.py`

```python
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

# §7.2 Law 5 dialect-identity-proxy table — closed-set per §0.5 v7
# row 124 (`scribe.dialect_identity_proxy_table.v1`). Dialect-keyed
# phrases that if emitted require a matching KgiePreflightResult
# identity_claim. Example: "my grandmother taught me" in soul_fire implies
# ancestral-knowledge identity claim — missing identity_claim → FAIL.
DIALECT_IDENTITY_PROXY_TABLE: Final[Mapping[Dialect, Mapping[str, str]]] = ...

def detect_dialect_drift(
    text: str,
    declared_dialect: Dialect,
) -> tuple[str, ...]:
    """§7.8 pin — returns phrases from OTHER dialects present in text.
    Non-empty tuple → F-SCRIBE-DIALECT-DRIFT at POST-gate."""

def detect_dialect_induced_identity(
    text: str,
    declared_dialect: Dialect,
    identity_claims: tuple[IdentityClaim, ...],
) -> tuple[str, ...]:
    """§7.2 Law 5 enforcement — returns dialect-identity-proxy phrases
    in text that have no matching identity_claim. R3 POST-gate
    F-SCRIBE-DIALECT-INDUCED-IDENTITY reads this."""
```

### 3.4 `program_templates.py`

```python
@dataclass(frozen=True, kw_only=True, slots=True)
class ProgramTemplate:
    program_code: str
    section_overrides: Mapping[str, SectionSpec]   # frozen at construction
    required_content_cues: tuple[str, ...]
    dialect_default: Dialect
    template_content_sha3_512: str  # full 128-hex (not prefix)
    template_at_utc: datetime

# Eight known programs from §7.9. Operator-extensible by adding a new entry.
KNOWN_PROGRAMS: Final[Mapping[str, Mapping[str, object]]] = MappingProxyType({
    "VAPG":   {...},
    "REAP":   {...},
    "SCBGP":  {...},
    "SARE":   {...},
    "SBIR":   {...},
    "AFRI":   {...},
    "2501":   {...},
    "UAIP":   {...},
})

def build_known_template(
    program_code: str,
    *,
    clock: ClockFn = _default_utc_now,
) -> ProgramTemplate

def compute_template_sha3_512(content_bytes: bytes) -> str
```

All predicates pure-deterministic. No I/O at R2 — `build_known_template`
synthesizes a template from the `KNOWN_PROGRAMS` constant; the Phase 0 file
load + SHA-pin lands at R3 when `pipeline.vault` + filesystem seams are
available.

## 4. Design decisions

### 4.1 Closed-set vocabulary (§7.8)

Each dialect's vocabulary is a frozenset inlined at module top. V1
rebind-resistance (matches R1 `_KGIE_STATUS_VALID`). Matching is
case-insensitive substring on the lowercased draft text. Multi-word phrases
preserved verbatim.

### 4.2 DIALECT_IDENTITY_PROXY_TABLE shape (§0.5 v7 row 124)

Mapping[Dialect, Mapping[phrase → identity_claim_label]]. A match means:
"if phrase present AND declared_dialect == key, expect
identity_claims to contain a claim whose text contains the implied label".
Examples in soul_fire: `"my grandmother taught me" → "ancestral-knowledge"`,
`"elder wisdom" → "ancestral-knowledge"`. R3 POST-gate enforces.

### 4.3 Numeric-verbatim helper

`extract_numeric_tokens(text)` returns canonical-form tokens: integer
(`"12"`), decimal (`"12.5"`), money (`"$1,200"` normalized to `"1200"`),
percent (`"75%"` normalized to `"75"`). Byte-identity check runs over the
normalized tokens. Paraphrase detection (`"nearly half a decade"` for 3
years) is NOT in R2 — that's the full semantic-match v0.2 roadmap per
§7.6.

### 4.4 OverlookedExpensesWalk.needed_count invariant

`__post_init__` MUST verify `needed_count == count(e for e in entries if
e.status == "needed")`. Drift raises `ValueError`. Callers build via
`build_walk` helper which computes `needed_count` correctly; passing a
hand-constructed `OverlookedExpensesWalk` with wrong count is a programmer
error caught at construction.

### 4.5 ProgramTemplate registry shape

`KNOWN_PROGRAMS` is the closed-set of eight v0.1 programs. Adding a new
program at v0.2 = one-row append; no core refactor per §7.9 extensibility.
`build_known_template(code)` raises `KeyError` with a clear message for
unknown codes — R3 will translate this into PRE-gate
`F-SCRIBE-TEMPLATE-UNKNOWN`.

### 4.6 Import discipline

R2 adds NO new cross-package imports. Still stdlib + intra-module
(`pipeline.seats.scribe.types`, `pipeline.seats.scribe.kgie` for `ClockFn`).
`pipeline.logician` / `pipeline.vault` imports land at R3, NOT R2. The
parent spec card's "R2 unblocks the door to logician/vault" statement was
about namespace authorization — R2 proves the import-discipline R1
established holds across all drafting-primitive modules.

## 5. Invariant checklist (per module)

- `@dataclass(frozen=True, kw_only=True, slots=True)` on every dataclass.
- `Mapping` fields frozen via `MappingProxyType` in `__post_init__`.
- Closed-set enumerations inlined as module-top frozensets with `Final`.
- Tz-aware datetime enforced in `__post_init__` for any datetime field.
- Every public function pure — no I/O, no globals mutation.
- `clock: ClockFn = _default_utc_now` on every public function that
  constructs a record with a datetime field.
- AST-lint R1-R7 clean.

## 6. Test surface (target ~150 tests)

**`test_smart.py` (~35 tests):**
- Shape: construction happy-path, empty-field rejection, tuple-field
  freeze.
- `validate_smart_objective` happy + each of the 5 SMART dimensions failing.
- `extract_numeric_tokens` on integer / decimal / money / percent / mixed
  / no-numerics / adjacent-punctuation.
- `check_numeric_verbatim` happy + paraphrase detection (claim="3 years",
  evidence="3 years" → clean; claim="nearly half a decade", evidence="3
  years" → flagged because "3" doesn't appear in claim-extracted tokens;
  ...).

**`test_overlooked_expenses.py` (~30 tests):**
- `OverlookedExpenseEntry` happy + status closed-set + rationale invariant.
- `OverlookedExpensesWalk` `__post_init__` needed_count = true count
  invariant.
- `build_walk` correctness on mixed/all-included/all-needed inputs.
- `is_finalizable` happy + needed>0 fails.
- Clock injection determinism.
- `DEFAULT_CHECKLIST` has 11 entries.

**`test_dialect.py` (~35 tests):**
- `DIALECT_VOCABULARY` keys closed-set + frozen.
- `DIALECT_IDENTITY_PROXY_TABLE` keys closed-set + frozen + every
  soul_fire/progressive phrase maps to a non-empty identity label.
- `detect_dialect_drift` happy / drift from each other dialect /
  case-insensitive.
- `detect_dialect_induced_identity` happy / phrase-without-claim flagged
  / phrase-with-matching-claim clean / empty-text clean.

**`test_program_templates.py` (~30 tests):**
- `KNOWN_PROGRAMS` contains all 8 v0.1 programs.
- `build_known_template` happy per program.
- `build_known_template("UNKNOWN")` raises `KeyError`.
- `compute_template_sha3_512` deterministic + 128-char output.
- `ProgramTemplate` construction invariants.
- `section_overrides` frozen mapping.
- `required_content_cues` non-empty tuples.

**Property / adversarial (~25 tests):**
- `detect_dialect_drift` over 20 seeded random-phrase draws asserts drift
  detection symmetry.
- `extract_numeric_tokens` over random digit-strings asserts round-trip.
- `build_walk` over random status-distributions asserts needed_count =
  walk.needed_count.
- Malformed inputs (None, wrong types) never raise uncaught
  `TypeError`/`AttributeError` — raise `TypeError` with clear messages
  where appropriate.

**Corpus-driven (~5 tests):**
- Extend `tests/corpus/scribe/v1/` with a SMART-happy, SMART-missing-
  measurement, dialect-drift-conservative-progressive, and
  program-template-VAPG fixture. Corpus loader test asserts fixtures route
  to expected helper-function outcomes.

## 7. Done definition

- Modules exist at `pipeline/seats/scribe/{smart,overlooked_expenses,
  dialect,program_templates}.py`.
- `pipeline/seats/scribe/__init__.py` re-exports all new public symbols;
  `__all__` extended; `BLUEPRINT_DEPS` updated with new `sections_implemented`
  entries.
- Every new dataclass has 100% branch coverage on `__post_init__`.
- Coverage ≥ 95% on `pipeline/seats/scribe/` module tree at R2.
- Full suite green (current baseline 5206 pass post-R1 LOCK; R2 expected
  delta ≈ +140-180 tests).
- AST-lint R1-R7 clean on `pipeline/seats/` tree.
- LOCK row appended to `pipeline/engineering/lock_history.v1.jsonl`.
- Memory entry authored at
  `~/.claude/projects/-Users-goldenquill-Downloads-GoldenQuill/memory/`
  with Fact / Why / How / Artifacts / Unblocks structure.
- MEMORY.md top entry updated.
- Session metrics entry appended.

## 8. Committee composition

**Self-LOCK eligible per §5 R1-foundations precedent** — R2 is pure-data
primitives over already-LOCKED R1 types. No new seats, no subprocess, no
LLM. The §5 Round 3–12 cadence of single-cycle self-LOCKs applies: pure
Python + pure pytest + AST-lint is author-self-audit-sufficient.

Escalate to committee only if:
- Any new dataclass shape is added that is NOT in the §7 blueprint verbatim.
- Any helper function takes a Vault or Logician surface.
- Numeric-verbatim normalization introduces a subjective canonicalization
  decision not in §7.6.

## 9. Failure modes deferred to R3

- `F-SCRIBE-SMART-INVENTED-METRIC` — needs session manifest +
  PROJECT_CONTEXT read.
- `F-SCRIBE-OVERLOOKED-EXPENSE-UNRESOLVED` — runtime POST-gate wiring.
- `F-SCRIBE-DIALECT-DRIFT` / `F-SCRIBE-DIALECT-INDUCED-IDENTITY` — POST-gate
  dispatch reads R2 helper functions but is wired at R3.
- `F-SCRIBE-TEMPLATE-DRIFT` / `F-SCRIBE-TEMPLATE-UNKNOWN` — Phase 0
  template read via Vault + re-read at Phase 2.
- `F-SCRIBE-PARAPHRASED-NUMERIC` — POST-gate dispatch reads R2
  `check_numeric_verbatim`.

R2 helpers are the *evidence-producers*; R3 Logician wiring turns the
evidence into failure codes.

## 10. Changelog

- **2026-04-21:** initial authoring; spec card pre-staged from R1 LOCK
  closeout.
