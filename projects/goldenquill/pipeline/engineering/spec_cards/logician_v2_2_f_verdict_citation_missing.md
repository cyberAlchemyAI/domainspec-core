# Spec card — Logician gate F-VERDICT-CITATION-MISSING (§4 v2.2 amendment-policy enforcement)

**STATUS:** LOCKED

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_04_logician.md` v2.1 (current LOCK)
- TSIP v0.1 Judge-citation-validation derivative
- Consolidated backlog: `pipeline/engineering/spec_cards/logician_v2_2_gates.md` gate #3

**Spec-card version:** v1
**Round:** Logician v2.2 — Wave 1 (no external deps)
**Date:** 2026-04-20
**Failure-code prefix:** `F-AMDT-03`

---

## Gate name and failure code

- **Gate:** `F-VERDICT-CITATION-MISSING`
- **Failure code:** `F-AMDT-03`
- **Kind:** POST-gate on Judge verdict ingest

## Purpose

Each per-dimension scoring entry in a Judge verdict must cite evidence from the draft under review. Without this gate, Judge scores could float free of draft content — arbitrary scores with fabricated or absent citations would pass silently. This gate mechanically enforces that every scored dimension has a citation string that resolves against the actual draft text, making Judge verdicts auditable and grounded.

## Trigger condition

Fires as a POST-gate on Judge verdict ingest specifically (not Editor or Red Team — those seats do not produce per-dimension scored verdicts with evidence fields). Fires after F-VERDICT-BLOCKING-MISSING passes (verdict structure must be valid before citation content is checked).

## Input contract

```python
@runtime_checkable
class DraftReaderCallable(Protocol):
    def __call__(self, draft_path: str) -> str: ...
```

- `verdict_json: dict` — the Judge's parsed verdict containing per-dimension entries, each with an `evidence` field.
- `draft_path: str` — path to the draft under review (from verdict metadata or pipeline state).
- `draft_reader: DraftReaderCallable` — injected callable that returns the full text of the draft. No direct file I/O in gate code.

## Pass/fail criteria (deterministic — no LLM)

1. Read the draft text via `draft_reader(draft_path)`.
2. For each dimension entry in the verdict's `dimensions` list:
   a. Extract the `evidence` field value (string).
   b. If `evidence` is absent, empty, or not a string → FAIL.
   c. Tokenize `evidence` into whitespace-delimited tokens.
   d. For each token, check verbatim presence in the draft text (case-sensitive substring match per §4 v2.1 `source_tag_verify` pattern).
   e. If ANY token does not appear verbatim in the draft text → FAIL for that dimension.
3. **PASS:** all dimensions have resolving evidence strings.
4. **FAIL (`F-AMDT-03`):** any dimension has missing, empty, or non-resolving evidence. Failure detail lists which dimensions failed and which tokens did not resolve.
5. **FAIL (`F-AMDT-03`):** draft read failure (reader raises). Fail-closed.

## Failure behavior

- **DENY** the Judge verdict ingest. The verdict is NOT recorded.
- Emit structured failure record to `pipeline/metrics/session_log.jsonl` with `event: "F-AMDT-03"`, `gate: "F-VERDICT-CITATION-MISSING"`, `failed_dimensions: [...]`, per-dimension `missing_tokens: [...]`.
- Pipeline halts at Judge step. Judge must re-score with valid evidence citations from the actual draft.

## Implementation notes

- Pure Python, zero LLM tokens, fail-closed.
- Reuses §4 v2.1 `source_tag_verify` infrastructure for token resolution — same substring-match semantics.
- Injected `DraftReaderCallable` Protocol for draft access (E-017 pattern). No direct file I/O.
- Token splitting: `evidence.split()` (whitespace-delimited). Single-word evidence strings are valid if they resolve.
- Lives at `pipeline/logician/gates/f_verdict_citation_missing.py`.
- AST-lint R1–R5 clean at module load.
- Gate ordering: runs AFTER F-VERDICT-BLOCKING-MISSING on the same verdict. If blocking-field gate fails, citation gate does not fire.

## Test criteria

### Unit tests (≥30)
- Single dimension, evidence resolves → PASS.
- Multiple dimensions, all evidence resolves → PASS.
- Single dimension, evidence missing key → DENY.
- Single dimension, evidence empty string → DENY.
- Single dimension, evidence is integer → DENY.
- Single dimension, evidence token not in draft → DENY.
- Multiple dimensions, one fails → DENY (lists the failing dimension).
- Evidence with multiple tokens, all resolve → PASS.
- Evidence with multiple tokens, last token missing → DENY.
- Draft is empty string → all evidence fails → DENY.
- Parametrized: 1, 3, 7, 12 dimension counts with valid/invalid evidence.
- Case-sensitive match: "Budget" in evidence, "budget" in draft → DENY.
- Evidence token appears as substring of a word in draft → PASS (substring match).

### Adversarial tests (≥5)
- `test_adv_draft_reader_raises` → gate DENY (fail-closed), not crash.
- `test_adv_evidence_is_whitespace_only` → `evidence: "   "` → tokens list empty → DENY.
- `test_adv_evidence_matches_different_draft` → evidence resolves against a different draft's text but not the actual draft → DENY (gate reads the correct draft via `draft_path`).
- `test_adv_unicode_token_resolution` → evidence contains Unicode characters that appear in draft → PASS (substring match works on Unicode).
- `test_adv_dimensions_is_not_list` → verdict `dimensions` field is a dict or string → DENY with structural error.

## Dependencies

- §4 v2.1 `source_tag_verify` infrastructure (token resolution pattern — can be imported or reimplemented as the same algorithm is simple).
- §4 v2.1 gate infrastructure (verdict ingest hook point).
- F-VERDICT-BLOCKING-MISSING must fire first (gate ordering).
- No external file or state dependencies beyond the injected draft reader — Wave 1 gate.

## §0.5 paired-commit rows

| Row | Content |
|-----|---------|
| Code | `pipeline/logician/gates/f_verdict_citation_missing.py` |
| Tests | `tests/logician/gates/test_f_verdict_citation_missing.py` + `tests/logician/gates/test_adv_f_verdict_citation_missing.py` |
| Lock history | `pipeline/engineering/lock_history.v1.jsonl` row with `gate: "F-VERDICT-CITATION-MISSING"`, `failure_code: "F-AMDT-03"` |
| Blueprint amendment | §4 v2.2 blueprint delta row for F-AMDT-03 |
| Memory | MEMORY.md index entry |

---

*Spec card v1 — 2026-04-20 — per-gate card split from consolidated logician_v2_2_gates.md.*
