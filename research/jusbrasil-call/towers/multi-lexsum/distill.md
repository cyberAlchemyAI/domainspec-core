# distill.md — Smallest coherent model + compositional spine

Date checked: **2026-06-10**

## One-sentence model [A, grounded on S]
> Multi-LexSum proves that **the same long multi-document input can be summarized at several
> fixed granularities by experts**, and that off-the-shelf SOTA summarizers fail at it —
> making it a controllable-granularity, long-input MDS benchmark. [S for facts; framing A]

## Compositional spine

The dataset decomposes into four orthogonal axes. Hold one fixed, vary the rest:

```
INPUT axis        : multi-document, very long (>200 pp)        [S]
OUTPUT axis       : 3 fixed granularity tiers (25 / 130 / 650 words) [S-site]
LABEL axis        : expert-authored + reviewed references      [S/S-site]
EVAL axis         : SOTA models perform poorly (gap = headroom)[S]
```

The product insight is the **OUTPUT axis is a knob**: one pipeline, multiple selectable
output sizes from the same evidence. Granularity is a *parameter*, not a separate task.

## Borrow / Analogy / Block for Jus IA main-theses

### BORROW (take directly) [A]
- **Tiered output spec.** Adopt explicit, length-anchored tiers (a one-sentence tese; a short
  paragraph; an optional long synthesis). Multi-LexSum's 25/130/650 are concrete starting
  anchors to calibrate against.
- **Expert-guideline authoring + review loop** as the gold-label process. Theses are
  professional artifacts; crowdsourcing them degrades quality. This dataset validates the
  expert-reference path.
- **Multi-document fusion as the core task.** Main-theses inherently fuse *many* decisions —
  the MDS framing (fuse + dedupe across docs) is the right mental model, not single-doc
  summarization.

### ANALOGY (maps with translation) [A]
- Multi-LexSum: many docs of **one case** → tiered summaries of that case.
  Jus IA main-theses: many **decisions** → recurring short **theses** across them.
  The "input set" is a *theme/legal-question cluster*, not a single lawsuit. The grouping step
  (cluster decisions by thesis) is an extra stage Multi-LexSum doesn't have to do.
- The "tiny" tier ≈ a single tese statement; "short" tier ≈ a tese with its supporting
  reasoning sketch.

### BLOCK (do NOT copy) [A]
- **License shape.** Multi-LexSum summaries are **CC BY-NC** (non-commercial); source docs are
  US public domain. Jus IA cannot lift the gold summaries into a commercial product without the
  alternative-licensing path (info@clearinghouse.net). Use the *methodology*, not the texts.
- **Domain transfer of metrics.** ROUGE on English civil-rights summaries does not validate
  Portuguese-language thesis extraction. Re-baseline on Jus IA's own data. (Their exact ROUGE
  numbers are also ungrounded here — see `open-residue.md`.)
- **Assuming one canonical summary.** Main-theses are plural/recurring statements, not a single
  narration per input; do not force the single-summary-per-case shape onto thesis extraction.

## Recompose check
Borrowed tiers + expert loop + MDS framing, with the clustering stage added and licensing
re-derived, reconstitute a Jus-IA-appropriate main-theses pipeline from the Multi-LexSum core.
