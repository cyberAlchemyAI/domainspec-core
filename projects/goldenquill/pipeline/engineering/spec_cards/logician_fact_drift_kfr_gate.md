# Spec card — pipeline.logician.fact_drift_gate (Key Facts Register)

**Blueprint anchor:** `pipeline/blueprint/v0.1/section_04_logician.md` — Logician POST-gate battery; Law 5 (Applicant Brings Substance) quantitative-claim sibling to F-LOGICIAN-FABRICATED-ORG.
**Spec-card version:** v1
**Round:** post-v0.1 (v0.2 roadmap, **high priority** — quantitative substance is foundational)
**Priority:** v0.2 high
**Origin:** Exploration `pipeline/roadmap/explorations/key_facts_register_design.md` (2026-05-06) — operator-approved design intent. This card converts that exploration to spec by resolving the five open design questions.

---

## Purpose

Deterministic Logician POST-gate that catches numeric drift and fabricated quantitative claims in Scribe drafts. Complements the existing Law 5 verbatim-substring gate (which catches fabricated string credentials) and F-LOGICIAN-FABRICATED-ORG (which catches fabricated organisations) by targeting a third specific failure mode: **numeric values in the draft that don't trace to an operator-validated entry in the Key Facts Register (KFR)**.

**Doctrine** (from exploration): bad numbers in a grant are not a quality problem — they are an audit-finding, clawback, "you lied to a federal agency" problem. Worst-case cost is orders of magnitude higher than narrative drift. Every quantitative claim Scribe makes must trace to a validated, confirmed, time-bounded entry in a structured register. No exceptions.

**Example catch:** Scribe drafts "FIT Farms LLC enrolled 247 students in 2025-26" but the KFR entry `enrollment_2025_2026` has `value: 231` (perhaps an older draft used `247` and the new fact is `231`, or perhaps Scribe hallucinated `247`). Gate fires `F-LOGICIAN-FACT-DRIFT` with both values shown and DENIES promotion.

---

## Open-question resolutions (from exploration § "Open questions")

| Q | Exploration proposal | **Spec resolution** |
|---|---|---|
| 1. Format | YAML | **YAML.** Operator-readable, machine-parseable, diff-friendly, version-controllable. Schema validation via JSON Schema applied at load. |
| 2. Tolerance | 0% default with operator-overridable | **0% default + per-fact `display_tolerance_pct` field**. Default exact-match; operator opts into rounding tolerance per fact (e.g., "approximately 250" with KFR `value: 247` requires `display_tolerance_pct: 5`). |
| 3. Per-grant subset | Whole KFR vs RFA-derived subset | **Whole KFR at v0.2.** Subset derivation deferred to v0.3 if context budget proves an issue. Reasonable cap: 200 facts/org for v0.2 (~40KB YAML — fits comfortably in any LLM context window). |
| 4. Cross-org benchmarks | Per-org dup vs separate register | **Same KFR; dedup acceptable.** Cross-org benchmarks are rare and dedup cost is low. Separate `pipeline/benchmarks_register.yaml` is a v0.3+ option if dedup becomes painful. |
| 5. Refresh cadence | Per-fact expiry vs annual review event | **Per-fact expiry only.** No org-level annual review event. Operator handles cadence at the SP0 stop point per grant; per-fact expiry surfaces stale entries automatically when a grant flow asks for them. |

---

## Architecture

### Drop point

Logician POST-gate, fires after Scribe output, alongside the existing F-POST-10/11 + F-LOGICIAN-FABRICATED-ORG gates. Sequenced after fabricated-ORG gate (orgs first, then numbers). Wired into `pipeline/logician/post_gate.py` `run_post_gate_skeleton` via the same kwargs pattern used for fabricated-org.

### Pipeline

1. **Load.** Read `orgs/<org>/key_facts_register.yaml`. Validate schema. Empty/missing register → FAIL with reason `kfr_missing` (the operator must explicitly seed an empty `[]` to declare "no quantitative claims expected" — not a default behavior).
2. **Extract.** Parse Scribe draft for numeric claims. Each claim = (number, unit-or-context-token, surrounding-subject-tokens, sentence-context). Use deterministic regex + spaCy POS tagging to identify claim shape; details below.
3. **Match.** For each extracted claim:
   - a. Filter KFR facts by temporal validity (current `as_of` is non-expired and the grant's funding-cycle window includes the fact's `period`).
   - b. Match by `who` token-overlap + `what` token-overlap (Jaccard ratio ≥ 0.70 default).
   - c. If no match: FAIL with reason `kfr_no_match` and the unmatched claim's text.
4. **Verify.** For matched (claim, fact) pairs:
   - a. Compute `delta_pct = abs(claim_value - fact_value) / fact_value * 100`.
   - b. Effective threshold = `fact.display_tolerance_pct or 0`.
   - c. If `delta_pct > effective_threshold`: FAIL with reason `kfr_value_drift`, both values shown.
5. **Verdict.** Zero failures → PASS with per-claim trace. Any failure → FAIL with full findings list.

### Properties

- **Deterministic:** YAML load is deterministic; numeric extraction via regex + spaCy POS (deterministic given seeded model); set-membership + Jaccard + arithmetic are all deterministic. Zero LLM tokens.
- **Fail-closed:** unmatched claim or value drift → FAIL. Operator override via M13 bypass (audited).
- **Explicit operator surface:** failures surface the unmatched claim text + nearest KFR fact (if any) so the operator decides: update KFR, edit draft, or M13 bypass.

---

## Failure codes

| Code | Trigger | Severity | Reason tag |
|---|---|---|---|
| `F-LOGICIAN-FACT-DRIFT` | Any numeric claim in Scribe draft fails KFR match or value tolerance | HIGH | `kfr_no_match`, `kfr_value_drift`, `kfr_temporal_invalid`, `kfr_missing` |

---

## Public API

```python
# pipeline.logician.gates.f_logician_fact_drift

def check_fact_drift(
    *,
    draft_text: str,
    kfr_path: pathlib.Path,
    grant_funding_period: tuple[date, date],  # (start, end) — used for temporal validity
    nlp: Any = None,                          # spaCy injection seam
) -> FactDriftGateResult: ...

def load_kfr(path: pathlib.Path) -> KeyFactsRegister: ...

def extract_numeric_claims(text: str, *, nlp: Any = None) -> tuple[NumericClaim, ...]: ...
```

---

## Data structures

```python
@dataclass(frozen=True, kw_only=True)
class TemporalWindow:
    period: str            # human label, e.g. "2025-2026 academic year"
    as_of: date
    expiry: date | None    # None for non-expiring facts (e.g., credentials)


@dataclass(frozen=True, kw_only=True)
class ValidationBlock:
    confirmed_by: str
    confirmed_at: date
    source_doc: str        # path
    source_doc_hash: str | None  # sha256: when populated


@dataclass(frozen=True, kw_only=True)
class KfrFact:
    id: str
    who: str
    what: str
    when: TemporalWindow
    where: str
    why: str
    how: str
    value: Decimal | str   # Decimal for numeric facts; str for credential lists / similar
    unit: str
    projection_or_actual: Literal["projection", "actual"]
    validation: ValidationBlock
    confidence: Literal["HIGH", "MEDIUM", "LOW"]
    display_tolerance_pct: float = 0.0  # 0 = exact match required
    notes: str = ""


@dataclass(frozen=True, kw_only=True)
class NumericClaim:
    number: Decimal
    unit_token: str         # e.g. "students", "USD", "%"
    subject_tokens: tuple[str, ...]  # nominal subjects of the claim
    sentence: str           # full sentence containing the number


@dataclass(frozen=True, kw_only=True)
class FactDriftFinding:
    claim: NumericClaim
    nearest_kfr_fact: KfrFact | None
    reason_tag: Literal["kfr_no_match", "kfr_value_drift", "kfr_temporal_invalid"]
    delta_pct: float | None  # None when no nearest fact


@dataclass(frozen=True, kw_only=True)
class FactDriftGateResult:
    verdict: Literal["PASS", "FAIL"]
    failure_code: str | None
    findings: tuple[FactDriftFinding, ...]
    claim_count_extracted: int
    claim_count_drifted: int
```

---

## Dependencies

- `pyyaml>=6.0` — already in pyproject.toml. KFR YAML load.
- `spacy>=3.7` — already added for F-LOGICIAN-FABRICATED-ORG. Reuses `en_core_web_sm` for POS tagging in numeric-claim extraction.
- `python-decimal` — stdlib. Exact-arithmetic on `value` fields.
- (No new substrate deps. Builds on existing locked-substrate.)

---

## Test surface

### Failure-code tests

- Draft with one numeric claim that matches a KFR fact within tolerance → PASS.
- Draft with claim matching no KFR fact → `F-LOGICIAN-FACT-DRIFT` / `kfr_no_match`.
- Draft with claim matching a KFR fact but value differs > tolerance → `F-LOGICIAN-FACT-DRIFT` / `kfr_value_drift`.
- Draft with claim matching a KFR fact whose `as_of` is past `expiry` → `kfr_temporal_invalid`.
- Missing KFR file → `F-LOGICIAN-FACT-DRIFT` / `kfr_missing`.
- Empty draft → PASS (vacuously true).
- Draft with no numeric claims → PASS.
- Multiple drifts → all reported.

### Edge cases

- "approximately 250" with KFR `value: 247` and `display_tolerance_pct: 5` → PASS.
- Same number "247" matching two KFR facts (same value, different `who`) → match by closest `who`.
- Number in compound unit ("$4.2M operating budget") → unit-token extraction + Decimal parse.
- Year references ("FY 2026") not classified as numeric claims (denylist + grant-domain regex).

### Integration tests

- Wire into `run_post_gate_skeleton` via new `kfr_path` + `grant_funding_period` kwargs (same backward-compat pattern as fabricated-org).
- Combined run: F-POST-10 + F-LOGICIAN-FABRICATED-ORG + F-LOGICIAN-FACT-DRIFT all surface in `failure_codes` when all three fire.

---

## Interaction with existing gates

| Gate | Scope | Relation |
|---|---|---|
| Law 5 verbatim-substring | Fabricated *string* credentials | **Sibling.** This gate covers numeric claims; Law 5 covers string claims. Both POST-gate, both fail-closed. |
| F-LOGICIAN-FABRICATED-ORG | Fabricated *organisations* | **Sibling.** Law 5 trio: orgs + strings + numbers. |
| KGIE preflight | Required-section affirmation tri-state | **Upstream prerequisite.** SP0 KFR review happens before KGIE; KGIE asks "did the operator confirm KFR is fresh + complete for this grant"; this gate enforces that during drafting. |
| Sector knowledge packs | Per-sector terminology | **Adjacent.** Sector packs supply qualitative vocabulary; KFR supplies quantitative substance. |
| Narrative spine (`F-LOGICIAN-SPINE-DRIFT`) | Per-grant strategic framings | **Adjacent.** Spine holds *strategic framings*; KFR holds *quantitative substance*. Spine's `cross_section_anchors.budget_justification_must_cite` references framing IDs; KFR provides the numbers those framings rest on. |

---

## Stop-point integration (from exploration)

This gate is enforced at POST-gate runtime, but its **inputs are operator-curated at SP0**:

- **SP0 — KFR Freshness Review.** Before KGIE preflight. Operator reviews fact list, expiries, RFA-derived gaps. Refreshes any expired facts. Confirms register is ready for this grant.
- **Output artifact:** `orgs/<org>/grants/<grant_id>/sp0_kfr_review.yaml`.
- **What this gate does at runtime:** enforces that Scribe's draft does not numeric-drift from the operator-confirmed KFR.

---

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Numeric-claim extraction misses a number (e.g., "two hundred" written out) | Acceptable for v0.2 — operator can write in numerals. v0.3 may add number-word-to-numeral conversion if field experience shows the gap. |
| Numeric-claim extraction over-extracts (flags non-claim numbers like page counts) | Use POS-tag context (must be modifying a noun phrase) to filter. Findings are operator-visible, not silent — false positives surface as M13 review items. |
| KFR temporal-validity edge case: grant cycle straddles two fact periods | Match against the fact whose `period` overlap with the grant cycle is largest. Tie → flag for operator review. |
| Decimal precision drift on currency claims ("$4.2M" vs `4_287_000`) | Operator declares the canonical-form unit in `unit` field; extractor normalises ($M → integer USD). |
| KFR YAML schema evolves | Schema-version field on the register file; loader validates against current; older versions migration-pathed not load-failed. |

---

## Implementation sequencing

1. **Round v0.2.A** — KFR loader + schema validation + dataclasses. (~200 LOC + 200 LOC tests.)
2. **Round v0.2.B** — Numeric-claim extractor + matcher + tolerance evaluation. (~250 LOC + 250 LOC tests.)
3. **Round v0.2.C** — `check_fact_drift` entry point + `run_post_gate_skeleton` wiring + integration tests. (~150 LOC + 200 LOC tests.)
4. **Round v0.2.D** — SP0 stop-point artifact format + operator-facing display tooling. Separate concern from the gate; queue separately.

Total gate scope: ~600 LOC production + ~650 LOC tests = ~1250 LOC across 3 rounds. Comparable to F-LOGICIAN-FABRICATED-ORG.
