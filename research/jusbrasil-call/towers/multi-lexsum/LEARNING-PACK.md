# LEARNING-PACK.md — Multi-LexSum (the payload)

Paper: **Multi-LexSum** (Shen et al., NeurIPS 2022 D&B) · arXiv 2206.10883
Date checked: **2026-06-10** · Lane: multi-lexsum
Legend: **[S]** paper · **[S-site]** official site · **[A]** Arcanum reading · **[O]** ungrounded

---

## 1. Source-backed claims (the spine)

1. **9,280 expert-authored summaries** of U.S. civil rights lawsuits from the Civil Rights
   Litigation Clearinghouse. [S]
2. **Three granularity tiers per case** — tiny (~25 words, one sentence), short (~130 words,
   one paragraph), long (~650 words, multi-paragraph). [S-site] Abstract: one-sentence
   "extreme" summaries up to multi-paragraph narrations of 500+ words. [S]
3. **Multi-document, long input** — case files often **exceed 200 pages**, spanning dockets,
   complaints, motions, opinions, settlements. [S/S-site]
4. **Expert authoring + review** under guidelines (lawyers / law students), not crowdsourced. [S/S-site]
5. **SOTA summarization models perform poorly** — there is real headroom. [S]
   (Which models, and their ROUGE scores, are **[O]** — see cutoff.)
6. **Licensing:** dataset ODC-By; summaries/metadata **CC BY-NC**; source docs public domain;
   commercial use needs alternative licensing (info@clearinghouse.net). [S-site] / CC-BY-4.0 on landing. [S]

## 2. Operator model (how to think about it) [A]

> One very long multi-document input → **a length knob with three detents** → expert-quality
> summaries. Granularity is a *parameter of one pipeline*, not three separate tasks. The
> benchmark's value is the gap: experts can do tiered MDS; current models can't.

Four orthogonal axes to reason with: **input** (long, multi-doc) · **output** (3 tiers) ·
**label** (expert) · **eval** (large headroom). See `distill.md`.

## 3. Main-theses ("principais teses") takeaways [A]

- **Adopt the tiered output spec.** A one-sentence tese ≈ tiny tier; a tese-with-reasoning ≈
  short tier. Anchor lengths against 25/130 words to start.
- **Frame it as multi-document fusion**, then add a **clustering stage** Multi-LexSum doesn't
  need: group *decisions* by legal question/thesis before summarizing. Input set = a theme
  cluster, not one lawsuit.
- **Output is plural.** Main-theses are N recurring statements per cluster — don't force the
  one-summary-per-input shape.
- **Use the methodology, not the texts.** The gold summaries are NC-licensed; build your own
  PT-language expert-reference set and re-baseline metrics locally.

## 4. Five things for the call

1. **Closest public analog exists.** Multi-LexSum = tiered (1-sentence → multi-paragraph)
   summarization over 200+ page multi-doc legal files — the same shape as main-theses. [S]
2. **Granularity is a knob, proven by experts.** Three fixed tiers from one input; that design
   directly maps to controllable tese length. [S-site]
3. **The task is genuinely hard.** SOTA summarizers fail it — so a strong Jus-IA result is
   defensible, and naive baselines will underperform. [S]
4. **Licensing is a real gate.** Summaries are CC BY-NC; commercial reuse of the gold texts
   needs Clearinghouse alternative licensing. Borrow the method, not the data. [S-site]
5. **Numbers to verify before quoting in product specs:** case count, baseline models + ROUGE,
   train/dev/test splits, per-case doc counts are **not yet grounded** — see honest cutoff. [O]

## 5. Honest cutoff (do not exaggerate beyond this)

Grounded from arXiv landing + official site only. The **PDF body did not parse** this build,
so the following are NOT established here and must be fetched before use:
- Baseline **model names** and their **ROUGE / metric scores**. [O]
- **Number of cases** (9,280 is a *summary* count across 3 tiers, not a case count). [O]
- **Train/dev/test split** sizes. [O]
- **Per-case document counts**. [O]
- Verbatim section structure of the paper (section map in `L0-corpus.md` is inferred). [O]

Full open items: `open-residue.md`. Trust ledger: `claim-ledger.md`.
