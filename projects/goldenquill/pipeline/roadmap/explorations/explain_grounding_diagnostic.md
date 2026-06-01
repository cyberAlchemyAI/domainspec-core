# Design Note — Explain-Grounding Dev Diagnostic

**Status:** EXPLORATION (not committed)
**Stage:** v0.2 dev tooling
**Created:** 2026-05-06
**Origin:** SSI Booster reference review — inspired by `--dot-report` per-sentence groundedness gradient

---

## Problem

When a Scribe draft goes sideways — Judge scores it low, or the operator spots a claim that feels ungrounded — there's no easy way to see *which specific sentences* lack evidence backing. The operator or dev has to manually cross-reference the draft against PROJECT_CONTEXT and RFA to find the weak spots.

The Logician gates are binary (PASS/FAIL) and deterministic — they catch structural violations but don't provide a per-sentence evidence heat map. That's by design: Logician is a gate, not a diagnostic.

## Proposed Design

### What it is

A **dev-only diagnostic command** that prints a per-sentence evidence breakdown for a Scribe draft. Not a gate. Not a runtime filter. A debugging affordance.

```bash
tilth scribe --explain-grounding --draft pipeline/drafts/vapg_fy26_v3.md
```

### What it is NOT

- **Not a Logician gate.** Logician is deterministic Python + Cedar. This diagnostic uses BM25-style retrieval, which is statistical. Mixing statistical scoring into Logician's gate battery would violate the determinism contract.
- **Not a runtime filter.** This never blocks promotion. It's a read-only diagnostic.
- **Not a Judge replacement.** Judge scores against the funder's rubric. This scores against the evidence corpus. Different axes.

### Output format

Per-sentence breakdown showing evidence retrieval scores:

```
SENTENCE 1: "MycoSymbiotics Cooperative has operated a 2-acre mushroom 
             production facility since 2023."
  EVIDENCE:  PROJECT_CONTEXT.md §production_history (BM25: 0.91)
  GROUNDING: STRONG

SENTENCE 2: "The cooperative's training program has graduated over 200 
             participants."  
  EVIDENCE:  PROJECT_CONTEXT.md §workforce_metrics (BM25: 0.34)
  GROUNDING: WEAK — closest match: "training program enrolled 45 
             participants in 2025"
  FLAG:      Number mismatch (200 vs 45). Possible Law 5 violation.

SENTENCE 3: "Urban agriculture contributes $1.2B annually to the 
             Philadelphia economy."
  EVIDENCE:  No match in PROJECT_CONTEXT or RFA
  GROUNDING: UNGROUNDED — external claim, not sourced
```

### Architecture

1. **Sentence segmentation:** split draft into sentences (spaCy or simple regex — this is dev tooling, not production NLP).
2. **Evidence corpus:** PROJECT_CONTEXT.md + RFA text + any supplemental docs listed in PROJECT_CONTEXT's `supporting_documents` field.
3. **Retrieval:** BM25 (rank_bm25 or similar) against the evidence corpus. Each sentence is a query; top-k evidence passages returned with scores.
4. **Thresholds:** `STRONG` >= 0.7, `WEAK` 0.3-0.7, `UNGROUNDED` < 0.3. Thresholds are tunable via CLI flags.
5. **Number mismatch detection:** simple regex extraction of numbers from sentence and matched evidence; flag if sentence number > evidence number by >2x.

### Uses existing primitives

Scout already has BM25-style evidence retrieval for VERIFY-stage source checking. This diagnostic reuses those primitives against a different corpus (PROJECT_CONTEXT instead of web sources).

### Drop point

- `scripts/explain_grounding.py` — standalone script, or
- `--explain-grounding` flag on the seat CLI (if seat CLI exists at v0.2)

Either way, it's in `scripts/` or behind a `--` flag. Not in the pipeline's hot path.

### Dev workflow

1. Scribe produces draft v3.
2. Judge scores it 72/100 — below threshold.
3. Dev runs `tilth scribe --explain-grounding --draft drafts/vapg_fy26_v3.md`.
4. Output shows sentences 14, 22, and 31 are UNGROUNDED.
5. Dev inspects those sentences, identifies that Scribe hallucinated a partnership and inflated a metric.
6. Operator corrects PROJECT_CONTEXT or instructs Scribe to revise.

### Dependencies

- `rank_bm25` or equivalent (pure Python, no external service)
- spaCy sentence segmentation (already a dep for the NER gate)
- PROJECT_CONTEXT parser (existing)
- RFA text loader (existing)

## Open questions

1. **Output format — terminal vs file?** Terminal-printed for quick checks, or write to `pipeline/diagnostics/<draft>_grounding.md` for review?
2. **Integration with Editor?** Editor R2 (clarity pass) could consume the grounding report as input — but that couples a dev diagnostic to a production seat. Probably keep them separate.
3. **Corpus expansion?** Should the evidence corpus include prior successful grant drafts (with operator permission), or strictly PROJECT_CONTEXT + RFA?

## Non-goals

- Not a replacement for Judge rubric scoring.
- Not a production gate (violates Logician determinism).
- Not an auto-fix tool — it diagnoses, operator decides.
