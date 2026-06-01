# Spec card — pipeline.seats.judge (Round 1: types + rubric loader + dimension-scorer primitive)

**STATUS:** PRE-STAGED 2026-04-21

**Parent spec:** `pipeline/engineering/spec_cards/section_7_council_seats_pipeline_modules.md` (Lane A step 5; OQ-1 resolution: Judge = **FULL PORT** per parent §5 + §7 handoff pre-dispatch decisions).

**Framework:** per `pipeline/templates/component_analysis_template.md` (Five Laws, Four Rules, failure-mode taxonomy, standard interface pattern — not restated).

---

## 1. Blueprint anchors

- **§9 Judge blueprint — NOT YET AUTHORED.** Per parent spec §5 "Judge (third; 3 sessions) — Judge R1 — §9 blueprint round", §9 is a future blueprint authoring round. Judge-code R1 here is scoped deliberately to surfaces that do NOT require §9 LOCK:
  - rubric JSON shape comes from `pipeline/rubrics/vapg_fy26.json` (real, LOCKed de-facto by operator extraction 2026-04-12)
  - `JudgeVerdict` subprocess-output contract comes from `default_judge_parse` in `pipeline/loop/seat_runner.py` (non-empty dict, §4.5 structural contract)
  - Law 5 / cross-family discipline comes from architecture `tilth_architecture_locked.md` v7 §D.4 + §F.1 (already LOCKED 2026-04-19)
  - 12-dimension 90+ rubric semantics come from `skills/judge-rubric/SKILL.md` + `pipeline/engineering/agents/judge_scoring_agent_v1.md` v2 (OpenClaw skill, port source per OQ-1)
- `pipeline/rubrics/vapg_fy26.json` — canonical first-run demo rubric. 100 pts, 7 scoring criteria (a/b/c/d/e/f/g), criteria a + f have subcriteria. Structure pinned at card-open; hash-pinned at LOCK.
- `pipeline/blueprint/v0.1/section_07_scribe.md` v1.1.1 LOCKED 2026-04-21 — §7.5 `SectionDraft` handoff contract (Judge consumes); §7.2 Law 5 numeric-verbatim + evidence-sourcing posture (Judge mirrors this posture on the scoring side).
- `pipeline/blueprint/v0.1/section_00_5_interface_index.md` v4/v5 LOCKED 2026-04-19 — `pipeline.contract.judge` row is currently a STUB pending §9 round; R1 does NOT claim it (R1 types are internal + consumed by future R3 subprocess entry).
- `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 LOCKED + v2.2 consolidated amendment — POST-gate slot for `F-JUDGE-EVIDENCE-NOT-IN-DRAFT` (Law 5 on Judge's evidence strings) must be appended at §4.2.1 before R3; R1 lands the failure-code constant but does NOT wire the gate.
- `pipeline/architecture/v0.1/tilth_architecture_locked.md` v7 §D.4 (Judge role, cross-family rigor), §E (cross-family guard), §F.1 (SFR format — Judge is NOT SFR-exempt; R3 ships SFR emission).
- `router.yaml` — `tilth.judge` primary = `google/gemini-2.5-pro`; escalation = `anthropic/claude-opus-4-6` + `openai/gpt-5.1` (Reasoner Review tier). Judge committee carve-out: reviewer family MUST NOT be Google. Reference only — never hardcode inside modules.

**Blueprint hash-at-card** (BLUEPRINT_DEPS, computed at Round-open):
- `pipeline/rubrics/vapg_fy26.json` — sha256 at card-open
- `pipeline/blueprint/v0.1/section_07_scribe.md` — sha256 at card-open
- `pipeline/architecture/v0.1/tilth_architecture_locked.md` — sha256 at card-open
- `skills/judge-rubric/SKILL.md` — sha256 at card-open (port-source attestation)
- `pipeline/engineering/agents/judge_scoring_agent_v1.md` — sha256 at card-open (port-source v2 attestation)

**Spec-card version:** v1 (full port per parent OQ-1 resolution; adapter pattern explicitly rejected for Judge).

**Round:** §9 Judge Round 1 — **types + rubric loader + dimension-scorer primitive** (mirrors Scribe R1 pure-deterministic scope; zero LLM orchestrator; dimension scorer wraps a single LLMCallFn seam for unit-testability).

**Canonical home:** `pipeline/seats/judge/` (NEW — parallel to `pipeline/seats/scribe/`; per parent spec §2 module layout).

---

## 2. Depends on

- **Scribe R2 LOCKED (soft).** Judge consumes `SectionDraft` at R2/R3 time. Scribe R2 does NOT yet author `SectionDraft` — per Scribe R2 spec card §1, `SectionDraft` lands at Scribe R3 alongside the Phase 2 drafting loop. Therefore Judge R1 cannot import a concrete `SectionDraft` from `pipeline.seats.scribe` at R1 time. R1 resolves this by declaring a **forward-Protocol** `SectionDraftLike` inside `pipeline/seats/judge/types.py` (E-017 pattern) that captures the fields Judge actually reads: `section_name: str`, `section_order: int`, `body_text: str`, `claim_evidence_map: tuple[ClaimEvidenceLike, ...]`. At Scribe R3 LOCK + Judge R2 open, the Protocol-to-concrete bind lands (E-026 `__module__` lineage test added at R2). Judge R1 tests inject fake SectionDrafts satisfying the Protocol.
- **Architecture v7 §D.4 + §F.1 LOCKED** ✅ (2026-04-19).
- **VAPG rubric extraction LOCKed de-facto** ✅ (`pipeline/rubrics/vapg_fy26.json` 2026-04-12).
- **Logician v2.2 waves 3+4 LOCKED** ✅ (2026-04-21) — R1 lands F-code constants; R3 wires the POST-gate through `gate_runner.py`.

**Not depended on:** §9 Judge blueprint LOCK (R1 scope deliberately avoids §9-owned schema decisions — JudgeVerdict full shape, cross-rubric dispatch, responsiveness-map are §9 / Judge R2/R3). Parent spec §5 places §9 blueprint round as a prereq for Judge R2, not Judge R1.

---

## 3. Proposed modules

```
pipeline/seats/judge/
├── __init__.py               # __all__ public surface + BLUEPRINT_DEPS
├── types.py                  # frozen kw_only dataclasses + Protocols
├── rubric_loader.py          # deterministic JSON rubric load + schema validation + hash-pin
├── dimension_scorer.py       # pure predicate wrapping E-017 LLMCallFn seam
└── BLUEPRINT_DEPS            # engineering process §4.6 hash pins (5 anchors per §1)
```

No sub-packages. Each module single-purpose. Coverage target ≥ 95% per module (Scribe R1 precedent: 100%).

---

## 4. Public API (Round 1)

```python
__all__ = (
    # Rubric shapes
    "Rubric",
    "RubricCriterion",
    "RubricSubCriterion",
    "RubricScorerRole",            # Literal["review_panel", "state_office", "administrator"]
    # Scoring shapes
    "CriterionScore",
    "JudgeInput",
    "JudgeOutput",
    # Forward-Protocol contracts (bind to Scribe R3 at Judge R2)
    "SectionDraftLike",
    "ClaimEvidenceLike",
    # Rubric primitives
    "load_rubric",                 # deterministic JSON load + schema + hash-pin
    "compute_rubric_sha256",       # canonical-bytes SHA-256 for traceability
    # Dimension primitive
    "score_dimension",             # pure predicate: (draft, criterion, llm_call) -> CriterionScore
    "LLMCallFn",                   # E-017 injected-callable Protocol
    # Failure-code constants (strings; R3 wires Logician gates)
    "F_JUDGE_RUBRIC_MALFORMED",    # "F-JUDGE-RUBRIC-MALFORMED"
    "F_JUDGE_CRITERION_MISSING",   # "F-JUDGE-CRITERION-MISSING"
    "F_JUDGE_SCORE_UNPARSEABLE",   # "F-JUDGE-SCORE-UNPARSEABLE"
    "F_JUDGE_EVIDENCE_NOT_IN_DRAFT",  # "F-JUDGE-EVIDENCE-NOT-IN-DRAFT" — Law 5 core
    "F_JUDGE_SCORE_OUT_OF_BOUND",  # "F-JUDGE-SCORE-OUT-OF-BOUND"
    "F_JUDGE_RUBRIC_HASH_DRIFT",   # "F-JUDGE-RUBRIC-HASH-DRIFT"
)
```

No `seat.py`, no subprocess entry, no provider routing, no Google binding, no cross-rubric dispatch, no SFR emission at R1 — all R2/R3.

---

## 5. Interface signatures

```python
# types.py
@dataclass(frozen=True, kw_only=True, slots=True)
class RubricSubCriterion:
    id: str                                    # e.g. "a.i"
    name: str                                  # "Technological feasibility"
    max_points: int                            # 10 for a.i
    must_address: tuple[str, ...]              # checklist from rubric JSON
    tiers: tuple[Mapping[str, Any], ...]       # frozen scoring-tier table

@dataclass(frozen=True, kw_only=True, slots=True)
class RubricCriterion:
    id: str                                    # "a", "b", ..., "g"
    name: str
    max_points: int                            # 30, 20, 20, 5, 5, 10, 10
    scorer: RubricScorerRole                   # closed-set
    subcriteria: tuple[RubricSubCriterion, ...]  # empty tuple when none
    must_address: tuple[str, ...]              # criterion-level checklist
    tiers: tuple[Mapping[str, Any], ...]       # empty when only subcriteria present

@dataclass(frozen=True, kw_only=True, slots=True)
class Rubric:
    program_code: str                          # "VAPG-FY26"
    funder: str                                # "USDA Rural Development"
    nofo_number: str                           # "RDBCP-VAPG-2026"
    max_score: int                             # 100
    min_score: int                             # 50
    criteria: tuple[RubricCriterion, ...]      # length >= 1
    rubric_sha256: str                         # 64-hex canonical-bytes hash
    loaded_at_utc: datetime                    # tz-aware

@dataclass(frozen=True, kw_only=True, slots=True)
class CriterionScore:
    criterion_id: str                          # e.g. "a.i" or "b"
    score: int                                 # 0..criterion.max_points
    evidence_quote: str                        # VERBATIM from SectionDraft.body_text (Law 5)
    confidence: float                          # 0.0..1.0
    rationale: str                             # short prose; not evidence — safe to paraphrase

@dataclass(frozen=True, kw_only=True, slots=True)
class JudgeInput:
    section_drafts: tuple[SectionDraftLike, ...]
    rubric: Rubric
    rfa_content_sha3_512: str                  # 128-hex — pins which RFA this scoring run is against

@dataclass(frozen=True, kw_only=True, slots=True)
class JudgeOutput:
    criterion_scores: tuple[CriterionScore, ...]
    total_score: int                           # sum of criterion scores
    max_total: int                             # sum of max_points across scored criteria
    rubric_sha256: str                         # REPEATED from Rubric for audit traceability
    rfa_content_sha3_512: str                  # REPEATED from JudgeInput
    scored_at_utc: datetime

# Forward-Protocols (bind to Scribe R3 at Judge R2)
class ClaimEvidenceLike(Protocol):
    claim_text: str
    evidence_text: str
    source_field: str

class SectionDraftLike(Protocol):
    section_name: str
    section_order: int
    body_text: str
    claim_evidence_map: tuple[ClaimEvidenceLike, ...]

# rubric_loader.py
def load_rubric(
    rubric_path: Path,
    *,
    clock: ClockFn = _default_utc_now,
) -> Rubric:
    """Read JSON at rubric_path, validate schema, compute rubric_sha256 over
    canonical-bytes payload, return frozen Rubric. Raises F_JUDGE_RUBRIC_MALFORMED
    [as residual ValueError at R1; R3 wires to Logician PRE-gate]."""

def compute_rubric_sha256(rubric_bytes: bytes) -> str:
    """Canonical-bytes SHA-256 (64 hex). Input is rubric JSON serialized via
    sort_keys=True + separators=(',',':'). Used at load time + on every
    JudgeOutput emission for traceability."""

# dimension_scorer.py
class LLMCallFn(Protocol):
    """E-017 injected-callable seam. Production binds router.yaml tilth.judge
    (Google Gemini 2.5 Pro). Tests inject a fake returning structured tuples.
    Contract: takes a compiled prompt (str) + max tokens (int), returns raw
    LLM text output (str). Parsing happens in score_dimension."""
    def __call__(self, *, prompt: str, max_tokens: int) -> str: ...

def score_dimension(
    section_drafts: tuple[SectionDraftLike, ...],
    criterion: RubricCriterion | RubricSubCriterion,
    *,
    llm_call: LLMCallFn,
    clock: ClockFn = _default_utc_now,
) -> CriterionScore:
    """Pure-over-injected-seam predicate. Builds scoring prompt from criterion
    + drafts + must_address checklist, invokes llm_call, parses response,
    returns CriterionScore. Does NOT verify evidence-in-draft at R1 (that's the
    POST-gate at R3 via F_JUDGE_EVIDENCE_NOT_IN_DRAFT); R1 only produces the
    candidate score+quote+rationale. Score out-of-bound raises ValueError
    [R3 wires to Logician POST-gate F_JUDGE_SCORE_OUT_OF_BOUND]."""
```

---

## 6. Rubric hash-pinning

Every `JudgeOutput` carries `rubric_sha256` (64-hex) = canonical-bytes SHA-256 of the Rubric JSON loaded. Traceability chain:

```
pipeline/rubrics/vapg_fy26.json  ──load_rubric──►  Rubric(rubric_sha256=X)
                                                          │
                                                          ├──► score_dimension ──► CriterionScore
                                                          │
                                                          └──► JudgeOutput(rubric_sha256=X)
```

At any downstream audit, the operator can re-run `compute_rubric_sha256` over the on-disk rubric JSON and compare against the JudgeOutput's pinned hash. Mismatch = `F-JUDGE-RUBRIC-HASH-DRIFT` (the rubric was modified between score time and audit time; the score is stale). This is a pure-deterministic primitive in R1; R3 wires the runtime drift check as a PRE-gate before Judge is invoked.

Canonicalization discipline: `json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")` — pinned as inline literal in `compute_rubric_sha256` (V1 rebind-resistance).

---

## 7. Design decisions

1. **Frozen kw_only slots=True on every dataclass** (Scribe R1 + R2 precedent; A-13 memory-layout discipline).
2. **`SectionDraftLike` / `ClaimEvidenceLike` as Protocols, not concrete imports.** Scribe R3 has not yet landed `SectionDraft`. E-017 injected-Protocol pattern (11th+ firing). At Judge R2 open, a `test_section_draft_like_is_sourced_from_scribe` using `__module__` lineage check (E-026) binds the Protocol to Scribe's concrete class.
3. **LLMCallFn as injected Protocol (E-017 12th+ firing).** `dimension_scorer.score_dimension` is pure-over-injected-seam. Production wiring at R3 binds to `pipeline.providers.google.complete()` (cross-family committee's architecture §E.2 contract). R1 tests inject fakes returning deterministic strings.
4. **Rubric subcriteria as flat tuple, not nested class hierarchy.** The VAPG JSON structure has two levels (criteria with optional subcriteria). R1 flattens to `RubricCriterion.subcriteria: tuple[RubricSubCriterion, ...]` (empty when none). Criteria b/c/d/e scored at criterion level; criteria a/f scored at subcriterion level; criterion g scored at criterion level with discretionary cap. This matches VAPG FY26 JSON exactly.
5. **Score is `int`, not `float`.** VAPG rubric tiers are integers or integer ranges. R1 pins `score: int`. Out-of-bound = `score < 0 OR score > max_points` → `ValueError` at `__post_init__` of `CriterionScore` (R3 converts to `F_JUDGE_SCORE_OUT_OF_BOUND` POST-gate).
6. **Evidence quote is VERBATIM from SectionDraft — but R1 does NOT enforce.** Evidence-in-draft verification is Logician POST-gate (`F_JUDGE_EVIDENCE_NOT_IN_DRAFT`) at R3. R1 emits the candidate quote; the gate checks at downstream gate-runner time. This split is deliberate: Judge LLM call produces the candidate; deterministic Logician verifies. Composability over coupling.
7. **No provider call at R1.** `dimension_scorer` invokes `llm_call` injected Protocol. R1 tests pass a fake that returns canned strings. R3 binds the real Google adapter.
8. **Rubric loader refuses malformed JSON with specific error codes.** `load_rubric` distinguishes: file missing (raise), JSON parse error (raise ValueError with `F_JUDGE_RUBRIC_MALFORMED`), schema mismatch (missing `meta` / `scoring_criteria` / criterion missing `id`/`max_points` — ValueError + `F_JUDGE_RUBRIC_MALFORMED`), criterion id duplication (ValueError), score-bound inversion (`min_score > max_score` — ValueError). R3 converts to PRE-gate codes.
9. **V1 inline-literals with rebind-resistance.** Module-top constants (`_RUBRIC_SCORER_ROLES = frozenset({"review_panel", "state_office", "administrator"})`, `_JSON_CANONICAL_SEPARATORS = (",", ":")`) are `Final`-typed frozensets/tuples; validators check against inline-literal RHS (pattern from Scribe R2 §4.1 + seat_runner `MINIMAL_ENV_ALLOWED_KEYS`).
10. **Threat-model docstring at module top.** Each of `rubric_loader.py`, `dimension_scorer.py`, `types.py` carries a top-of-module Threat-model docstring (E-023 pattern) enumerating: in-scope at R1 (shape validation, canonical-bytes hashing, pure predicate), out-of-scope-at-R1-deferred-to-R3 (evidence-in-draft verification, LLM provider binding, cross-family routing, rubric-library dispatch, SFR format emission, subprocess entry).

---

## 8. Discipline requirements

- **V1 inline-literals with rebind-resistance** — per §7 design decision 9.
- **E-017 LLMCallFn seam** — production binds Google Gemini 2.5 Pro; tests inject deterministic fakes. 12th+ formal firing of the injected-Protocol pattern; cite E-017 in `dimension_scorer.py` module docstring.
- **E-023 residuals (malformed-input contract docs)** — `test_adv_judge.py` enumerates what R1 deliberately does NOT catch (rubric hash drift in-flight, evidence-fabrication, cross-family collision, SFR malformation, subprocess-envelope drift) with explicit citation to the R3 gate that will catch each. 6th+ formal firing.
- **E-024 1.5× multiplier on test-count floor** — R1 ships Protocols (SectionDraftLike, ClaimEvidenceLike, LLMCallFn) + V1 rebind-resistance + E-023 Threat-model docs → all three triggers. Floor ≥ 40 tests; expect ~60 given multiplier. Adversarial count inflated further per §12 (evidence-fabrication attack surface).
- **E-026 `__module__` lineage discipline** — Judge R2 WILL import Scribe R3's `SectionDraft`; Judge R2 spec will ship `test_section_draft_like_source_is_pipeline_seats_scribe_types` using `__module__` lineage assertion (NOT `is` identity). R1 pre-documents this in `types.py` docstring + defers the concrete test to R2.
- **E-027 + E-028 discipline** — R1 carries no committee dispatch payload exposure to Qwen/Groq; self-LOCK eligible per Scribe R1 precedent. If committee dispatched for cross-check, carve `qwen3-32b` → `gpt-oss-120b` substitution pin pre-dispatch (parent spec §7 committee guidance).
- **Threat-model docstring** — per §7 decision 10.

---

## 9. Law 5 enforcement (HARD discipline, not advisory)

**Judge MUST NOT fabricate evidence.** Evidence in `CriterionScore.evidence_quote` MUST be a verbatim substring of at least one `SectionDraftLike.body_text` in `JudgeInput.section_drafts`. No paraphrase. No summary. No invented quote.

**Split enforcement across R1 / R3:**
- **R1 (candidate-producer):** `score_dimension` returns a `CriterionScore` whose `evidence_quote` MAY or MAY NOT appear in any SectionDraft. R1 does NOT enforce — enforcement is the POST-gate's job per the separation-of-concerns in §7 decision 6.
- **R3 (gate):** Logician POST-gate `F_JUDGE_EVIDENCE_NOT_IN_DRAFT` walks every CriterionScore and asserts `evidence_quote in body_text` for at least one SectionDraft; fail-closed on miss. R3 appends the POST-gate slot to §4.2.1 + wires through `gate_runner.py`.

**R1 ships the F-code constant + the Threat-model docstring** (`test_adv_judge_evidence_fabrication_is_r3_post_gate_scope.py` with 4+ adversarial stubs demonstrating the fabrication attack vectors R3 will catch: invented quote, paraphrased quote, quote-from-other-org's-draft, quote-from-RFA-not-draft).

**Why this matters at R1.** Evidence-fabrication is a real attack vector — not a hypothetical. LLMs confabulate quotes. Josh's prior grant experience + Claude's general LLM behavior both confirm this. Shipping the failure-code constant + the adversarial docstring at R1 means the Logician R3 wiring has a clear target; shipping without the constant means R3 has to re-author the code. The hard discipline is: **R1 emits the attack-surface documentation AND the failure-code constant even though the enforcement is R3.** This is the L-006 existence-before-LOCK pattern applied upstream.

---

## 10. Test surface (target 30+ tests + 12 adversarial; ~50 total given E-024 multiplier)

**Type-shape tests (~10):**
- Every frozen dataclass constructible with full documented field set.
- `__all__` export surface matches §4 exactly.
- `Rubric.__post_init__`: rubric_sha256 is 64-hex lowercase; criteria non-empty; min_score ≤ max_score; max_score ≥ sum of criterion max_points (sanity).
- `CriterionScore.__post_init__`: score ≥ 0; confidence ∈ [0.0, 1.0].
- `DateTimeWithTimezone`-equivalent tz-aware enforcement on `loaded_at_utc`, `scored_at_utc`.

**Rubric-loader tests (~12):**
- VAPG FY26 happy-path load (fixture: actual `pipeline/rubrics/vapg_fy26.json`).
- Criterion `a` flattens to 3 subcriteria (a.i, a.ii, a.iii); max_points=30; sum(subcriteria.max_points)=30.
- Criterion `f` flattens to 2 subcriteria (f.i, f.ii); max_points=10.
- Criteria b/c/d/e/g have empty subcriteria tuple + non-empty tiers.
- Hash reproducibility: load_rubric twice → identical rubric_sha256.
- Malformed JSON → ValueError with F_JUDGE_RUBRIC_MALFORMED tag.
- Missing `meta` / `scoring_criteria` / criterion id/max_points → ValueError.
- Duplicate criterion id → ValueError.
- min_score > max_score → ValueError.
- sum(criterion.max_points) != max_score → documented tolerance (VAPG actual: 30+20+20+5+5+10+10 = 100 ✓).
- Canonical-bytes: dict-order-independent hash (sort_keys=True verified).

**Dimension-scorer tests (~10):**
- Happy-path: fake LLM returns parseable `{"score": 8, "evidence_quote": "<verbatim from injected SectionDraft>", "confidence": 0.85, "rationale": "..."}`; CriterionScore constructed correctly.
- Criterion-level scoring (criterion b, no subcriteria): prompt includes must_address checklist + criterion.tiers.
- Subcriterion-level scoring (criterion a.i, max 10): bound check enforced.
- Score out-of-bound (LLM returns score=15 for max=10): raises ValueError tagged F_JUDGE_SCORE_OUT_OF_BOUND.
- Unparseable LLM output: raises ValueError tagged F_JUDGE_SCORE_UNPARSEABLE.
- Confidence out-of-bound (LLM returns 1.5): raises ValueError.
- Clock injection determinism (fixed clock → identical scored_at_utc across runs).
- LLMCallFn raises (timeout, network error): propagates (not swallowed).
- Empty section_drafts tuple: raises ValueError (can't score with no draft).
- Must_address checklist from criterion appears verbatim in compiled prompt (prompt-compilation correctness).

**Adversarial tests (~12; E-024 2× multiplier honored):**
- `test_adv_judge_evidence_quote_not_in_draft_is_r3_scope` — constructs CriterionScore with evidence_quote not in any SectionDraft.body_text; R1 does NOT reject (documents deferral).
- `test_adv_judge_paraphrased_evidence_is_r3_scope` — LLM returns paraphrased evidence; R1 accepts at R1 (flags in Threat-model doc).
- `test_adv_judge_cross_org_evidence_is_r3_scope` — evidence_quote appears in a DIFFERENT org's SectionDraft; R1 cannot detect (no Law 3 context at R1).
- `test_adv_judge_rubric_hash_drift_mid_flight_is_r3_scope` — rubric file modified between load and JudgeOutput emission; R1 records load-time hash; R3 drift-check is PRE-gate.
- `test_adv_judge_score_injection_from_llm_prompt` — LLM returns JSON with extra fields (e.g., "override_max": 999); R1 parser ignores non-spec fields (no field leakage).
- `test_adv_judge_rubric_json_with_bom` — UTF-8 BOM at start → rejected (canonical-bytes discipline).
- `test_adv_judge_rubric_with_uppercase_hex_hash_rejected` — any `rubric_sha256` with uppercase → rejected at `__post_init__`.
- `test_adv_judge_mutability_via_object_setattr` — `object.__setattr__` on frozen Rubric field raises.
- `test_adv_judge_llm_returns_fenced_json` — LLM wraps JSON in ```json fences; parser strips (Rule 4 Clean Output discipline; matches Scribe + Editor pattern).
- `test_adv_judge_rubric_missing_tiers_both_levels` — criterion with empty tiers AND empty subcriteria → ValueError (incoherent rubric).
- `test_adv_judge_negative_max_points` — RubricCriterion with max_points=-1 → ValueError.
- `test_adv_judge_llm_call_raises_runtime_error` — llm_call raises RuntimeError → score_dimension propagates, does not swallow.

**Property tests (~6 via hypothesis):**
- Rubric load + serialize + re-load → identical rubric_sha256 (canonical round-trip).
- Hash is 64-hex-lowercase across 1000 random rubric JSON permutations.
- `score_dimension` with fixed (draft, criterion, fake-llm, fixed clock) is deterministic across 1000 runs.
- CriterionScore `__post_init__` invariant enforcement over random (score, max_points) pairs.

**Fixture corpus (~3):**
- `tests/corpus/judge/v1/vapg_fy26_happy_path/` — real VAPG rubric JSON (symlink or copy of `pipeline/rubrics/vapg_fy26.json`).
- `tests/corpus/judge/v1/malformed/missing_meta.json` — meta key absent.
- `tests/corpus/judge/v1/malformed/duplicate_criterion_id.json` — two criteria with id "a".

Total floor: **30+** (prompt spec) → **~50 actual expected** after E-024 1.5× multiplier + adversarial-count-inflation for evidence-fabrication attack surface.

---

## 11. Done definition (R1)

- Module exists at `pipeline/seats/judge/` with `__init__.py`, `types.py`, `rubric_loader.py`, `dimension_scorer.py`, `BLUEPRINT_DEPS`.
- Public API surface exactly matches §4 above — `__all__` leakage = LOCK fail.
- Every §5 invariant enforced via `__post_init__`; Hypothesis fuzz pass on 1000 random cases.
- **Rubric round-trip passes end-to-end:** `load_rubric(vapg_fy26.json)` → `compute_rubric_sha256` → `score_dimension(fake_llm)` → `CriterionScore` with matching `rubric_sha256` propagated to candidate `JudgeOutput` (R1 test constructs JudgeOutput manually; R2/R3 does it via orchestrator).
- Evidence-not-in-draft adversarial stubs document R3 deferrals with cited POST-gate slot.
- Fixture corpus at `tests/corpus/judge/v1/` with ≥ 1 pass (VAPG) + ≥ 2 fail (malformed, duplicate-id).
- **Coverage ≥ 95%** on `pipeline/seats/judge/` module tree.
- **AST-lint R1-R7 clean.** Module imports stdlib + `pipeline.seats.judge.*` only at R1; no `pipeline.logician` / `pipeline.vault` / `pipeline.providers` imports until R3 wiring. R2 `loop-logician-ban` does not apply to `pipeline/seats/` per parent §8.
- **BLUEPRINT_DEPS sha-pinned** against the 5 anchors per §1; L-015 regression test extended.
- **Full suite green** (baseline post-Scribe-R2 LOCK; R1 expected delta ≈ +50-70 tests).
- **LOCK row** appended to `pipeline/engineering/lock_history.v1.jsonl` with reviewer tokens (if committee dispatched) OR self-LOCK attestation, test count, F-code coverage.
- **Self-LOCK eligible** per §5 R1-foundations precedent + Scribe R1 precedent (12+ consecutive §5 single-cycle self-LOCKs; Scribe R1 self-LOCK 2026-04-21). Judge R1 is pure-Python shapes + one JSON loader + one pure predicate over an injected seam — similar complexity envelope. Committee credits conserved for Judge R3 (subprocess entry + Google binding + SFR format + POST-gate wiring = materially higher composition risk).

---

## 12. Unblocks

- **Judge R2** — scoring orchestrator composing R1 primitives + rubric library dispatch (rubric-family routing: VAPG → REAP → SCBGP → SARE etc. via `pipeline/rubrics/<program>.json` glob). R2 consumes Scribe R3's concrete `SectionDraft` (E-026 Protocol→concrete bind). R2 adds cross-rubric scoring (funder rubric first, then internal 90+ bar, then delta synthesis).
- **Judge R3** — `seat.py` subprocess entry + `pipeline.providers.google.complete()` binding + Logician PRE/POST gate wiring (F_JUDGE_EVIDENCE_NOT_IN_DRAFT, F_JUDGE_CROSS_FAMILY_COLLISION, F_JUDGE_RUBRIC_HASH_DRIFT) + SFR format emission per architecture §F.1 + stdin/stdout envelope satisfying `default_judge_parse`. §9 blueprint LOCK is prerequisite for R3 (JudgeVerdict full schema + cross-family contract + rubric-library dispatch contract).
- **Whole-seat Judge LOCK** after R3 Thesis 5/5 PASS.

---

## 13. Operator open questions (OQ)

- **OQ-1 — Rubric coverage at v0.1.** R1 lands primitives general-enough to load any rubric matching the VAPG FY26 JSON shape, but the only fixture rubric is VAPG FY26. Does v0.1 ship with VAPG FY26 only, or multi-rubric from day one (REAP, SCBGP, SARE, SBIR, AFRI, 2501, UAIP to mirror Scribe R2's `KNOWN_PROGRAMS` registry)? **Recommendation: VAPG FY26 only at v0.1 launch** — dogfood-first discipline; Scribe R2 KNOWN_PROGRAMS has 8 program templates but Judge has only 1 extracted rubric today. Adding rubric JSONs for the other 7 is operator-extraction work (8-16 hours each per prior VAPG extraction effort) and is not on the critical path. R2 spec card can pre-stage the multi-rubric extraction queue; v0.1 ships with single rubric; v0.1.1 or v0.2 adds the remaining 7.
- **OQ-2 — `SectionDraftLike` Protocol fields.** R1 pins the fields Judge reads from SectionDraft. Does `claim_evidence_map` need to flow through to Judge at R1 / R2 / R3? Judge's Law 5 evidence-in-draft verification is over `body_text` (the actual words), not over `claim_evidence_map` (Scribe's own traceability map). Recommendation: Judge reads `body_text` + `claim_evidence_map` (for cross-check of Scribe's sources at Judge R3 when confidence is low). R1 Protocol includes both; R2/R3 decide whether Judge consumes claim_evidence_map into scoring or only into gate-verification.
- **OQ-3 — Committee dispatch at R1 or self-LOCK.** Scribe R1 self-LOCKed; precedent strong. Judge R1 is comparable complexity (types + one loader + one pure predicate). **Recommendation: self-LOCK at R1**; reserve committee dispatch for R3 (subprocess entry + Google binding). Operator override welcome.
- **OQ-4 — Rubric-hash drift detection scope at R3.** R1 records `rubric_sha256` at load time. R3 PRE-gate check should also re-hash at every Judge invocation to catch mid-run rubric modification. Does the scope of `F_JUDGE_RUBRIC_HASH_DRIFT` include only load-time-vs-output-time (mid-session) OR also across-session (rubric modified between yesterday's score and today's audit)? Recommendation: both — R3 PRE-gate rehashes on every Judge invocation; audit-time replay uses same `compute_rubric_sha256` against on-disk JSON and compares against JudgeOutput's pinned hash. R1 primitive supports both — no additional R1 scope needed.

---

## 14. Non-goals at R1

- No `seat.py` — no subprocess entry — R3.
- No Google provider binding — R3.
- No Logician PRE/POST-gate wiring — R3.
- No cross-family collision PRE-gate — R3.
- No SFR format emission — R3.
- No cross-rubric dispatch (funder-rubric-then-internal-bar) — R2.
- No rubric-library glob (`pipeline/rubrics/*.json`) — R2.
- No claim-evidence-map cross-check with Scribe — R2 / R3.
- No Judge-against-Editor feedback loop — out of v0.1 scope (Judge scores; Editor clarifies; revision loop §5 R5 handles).
- No §9 blueprint authoring — separate blueprint round; R1 deliberately avoids §9-owned schema decisions.
- No Reasoner Review escalation wiring — R3 + architecture §D.7 envelope.
- No responsiveness-map generation (RFA-numbered-questions → draft-section) — §9 blueprint + R2.

---

## 15. Failure modes (delta per template §3)

- **Aspiration-as-enforcement on evidence-fabrication (L-006):** R1 lands the `F_JUDGE_EVIDENCE_NOT_IN_DRAFT` constant without the enforcing gate. Dev-mode symptom: R1 tests pass (constant exists, quote field is populated). Prod-mode failure: LLM confabulates quotes, Judge ships JudgeOutput with fabricated evidence, operator trusts the score. **Mitigation:** Threat-model docstring at R1 explicitly names the R3 gate slot; adversarial tests at R1 DOCUMENT the attack vectors even though they don't enforce; Logician R3 wiring is a BLOCKING prerequisite for Judge R3 LOCK. This is documented in the Done definition as a LOCK-phase check item.
- **Rubric-hash-drift between extraction and scoring:** VAPG FY26 JSON was extracted 2026-04-12; operator may edit rubric mid-session (typo fix, tier clarification). R1's `rubric_sha256` at load pins the version; R3 PRE-gate rehashes on every invocation. Dev-mode: hash drift uncaught at R1. Prod-mode: stale score against superseded rubric. **Mitigation:** R1 primitive is correct; the gap is R3 wiring discipline — flagged in OQ-4.
- **Protocol-to-concrete drift at Scribe R3 → Judge R2 bind:** `SectionDraftLike` Protocol may not exactly match Scribe R3's `SectionDraft` shape if Scribe R3 adds fields Judge doesn't anticipate. **Mitigation:** Judge R2 opens only AFTER Scribe R3 LOCK; R2 first task is `test_section_draft_like_binds_to_scribe` using `__module__` lineage + structural-subtype check. E-026 discipline from 3rd+ firing.
- **LLM returns valid JSON with out-of-spec fields:** LLM might return `{"score": 8, "override_max_points": 100, ...}`. R1 parser ignores non-`__all__` fields (test_adv_judge_score_injection_from_llm_prompt). Extra fields are dropped, not elevated — no field-leakage attack surface.
- **Canonical-bytes encoding drift:** `json.dumps` differs by Python version or locale. **Mitigation:** inline-literal `separators=(",", ":")` + `sort_keys=True` + `ensure_ascii=False` + `.encode("utf-8")` pinned at module top with V1 discipline.

---

## 16. Hardenings (delta per template §4 checklist)

- [ ] Frozen, kw_only, slots=True on every dataclass.
- [ ] `__post_init__` invariant enforcement on every frozen dataclass (score bound, confidence bound, hash hex format, tz-aware datetimes).
- [ ] `__all__` in `__init__.py` is a tuple literal (V1 rebind-resistance).
- [ ] E-017 LLMCallFn seam pinned; production binding deferred to R3.
- [ ] E-023 Threat-model docstring at module top of each of types.py, rubric_loader.py, dimension_scorer.py.
- [ ] BLUEPRINT_DEPS hash-pinned against 5 anchors (§1); L-015 citation-check clean.
- [ ] Canonical-bytes discipline on rubric hashing (sort_keys=True, separators=(",",":")).
- [ ] Evidence-fabrication attack-surface adversarial tests enumerate the R3 POST-gate deferrals.
- [ ] F-code constants present + string values exactly match §4 (no trailing whitespace, no case drift).
- [ ] `DIM_SCORER.score_dimension` is pure-over-injected-seam (no file I/O, no globals mutation, no LLM provider import at R1).
- [ ] Coverage ≥ 95%; Hypothesis fuzz pass on 1000 cases.
- [ ] Cross-family carve-out for any R1 committee dispatch: if Judge R1 elevates to committee, `code_reviewer_N` substitution pins NO Google-family reviewer (Judge's production binding).

---

## 17. Artifacts placeholders

- `pipeline/seats/judge/__init__.py`
- `pipeline/seats/judge/types.py`
- `pipeline/seats/judge/rubric_loader.py`
- `pipeline/seats/judge/dimension_scorer.py`
- `pipeline/seats/judge/BLUEPRINT_DEPS`
- `tests/unit/seats/judge/test_types.py`
- `tests/unit/seats/judge/test_rubric_loader.py`
- `tests/unit/seats/judge/test_dimension_scorer.py`
- `tests/unit/seats/judge/test_adv_judge.py`
- `tests/unit/seats/judge/test_prop_judge.py`
- `tests/corpus/judge/v1/vapg_fy26_happy_path/` (fixture)
- `tests/corpus/judge/v1/malformed/missing_meta.json`
- `tests/corpus/judge/v1/malformed/duplicate_criterion_id.json`
- Self-LOCK memo: `pipeline/engineering/locks/judge_round_1_self_lock_<date>.md`
- Metrics entry: `pipeline/metrics/session_log.jsonl` (R1 close)

---

## 18. Changelog

- **v1 PRE-STAGED 2026-04-21.** Authored post-Scribe-R1 LOCK + post-§7 v1.1.1 LOCK; pre-staged against Scribe R2 LOCK (soft) and Scribe R3 LOCK (SectionDraft concrete bind for Judge R2/R3). §9 Judge blueprint round remains open — R1 deliberately scoped to surfaces that do NOT require §9 LOCK. Judge is FULL PORT per parent OQ-1 resolution; R1 ships types + primitives only (subprocess entry, Google binding, SFR format, and Logician gate wiring land at R3). Operator decision queue: OQ-1..OQ-4.

*End spec card — PRE-STAGED; awaits Scribe R2 LOCK + operator OQ resolution before Code-session open.*
