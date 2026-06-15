# open-residue.md — Unverified / Open Items

**Date checked:** 2026-06-10
Items referenced or implied but NOT verifiable from fetched content. Nothing here was invented;
these are explicitly open. Resolve by reading the rendered PDF or the HF model card.

## R1. Few-shot configuration
- The exact number of shots (k) used in few-shot evaluation is not captured.
- The prompt format / answer-extraction protocol is not captured.

## R2. Full per-benchmark scores
- Only **mean** accuracies are captured with reasonable confidence (legal 44.5->49.2;
  PT 50.5->48.1; EN 61.6->58.0).
- Per-benchmark decimals (e.g. OAB-2023 48.3->54.5, OAB-2024 49.6->52.0, ENAM 31.2->36.8,
  MMLU-College 54.2->49.4, MMLU-HighSchool 64.8->61.6) are **low-med confidence** —
  WebFetch-summarized, not read from a rendered table. Treat as approximate until confirmed.
- The exact list and per-exam results of the 44 PT and 20 EN general sub-exams is not captured.

## R3. Forgetting mitigation
- Whether the authors attempted replay/rehearsal, general-data mixing, LoRA-style partial
  updates, or any technique to reduce catastrophic forgetting is NOT confirmed from fetched
  content. (Bridge BD6 flags this as future-work.)

## R4. Model artifact terms
- `roseval/Juru-7B` on Hugging Face is referenced but its **license**, gating, and exact
  availability were not verified.

## R5. Training detail gaps
- Learning rate schedule, context length, hardware, and wall-clock are not captured (only
  ~4 epochs / ~7.96B tokens / ~3.35×10²⁰ FLOPs at med confidence).

## R6. Corpus provenance precision
- "Reputable Brazilian legal sources" enumerated as academic papers + LexML + STF, but the
  exact journal/institution list, date range, and dedup methodology are not captured.

## R7. Comparison baselines
- Whether Juru was compared against any baseline other than vanilla Mistral-7B (e.g. other
  PT-BR or legal LLMs) is not confirmed.

---

**Open residue count: 7**

**How to close:** render the PDF (`arxiv.org/pdf/2403.18140`) page-by-page for Tables 5–7 and
the training section, and read the `roseval/Juru-7B` HF model card for R4.
