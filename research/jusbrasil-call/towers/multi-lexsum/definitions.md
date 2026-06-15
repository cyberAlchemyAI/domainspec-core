# definitions.md — Governed canonical definitions

Date checked: **2026-06-10**. These are the *governed* wordings for this tower; downstream
files should not redefine these terms. Source-kind in brackets.

## D1 — Multi-LexSum (the dataset) [S]
A benchmark of **9,280 expert-authored summaries** of U.S. **civil rights lawsuits**, drawn
from the Civil Rights Litigation Clearinghouse, where each case's long multi-document file is
summarized at **three fixed granularities** (tiny / short / long).

## D2 — Granularity tier [S-site]
A target output specification fixing approximate length and abstraction. Canonical set:
- **tiny** = one sentence, ~25 words
- **short** = one paragraph, ~130 words
- **long** = multiple paragraphs, ~650 words

(Abstract phrasing: from one-sentence "extreme" summaries to multi-paragraph narrations of
over five hundred words. [S])

## D3 — Multi-document case file (the input) [S/S-site]
The set of legal documents for a single lawsuit — dockets, complaints, motions, opinions,
settlements — **often exceeding two hundred pages per case**, treated as one input to be
summarized.

## D4 — Expert reference summary [S/S-site]
A gold summary written by trained lawyers/law students under explicit guidelines with expert
review, used as the evaluation reference. Distinguished from crowdsourced or model-generated
text.

## D5 — Controllable-granularity summarization (Arcanum reading) [A]
The capability of producing, from one fixed input, summaries at *operator-selected* length
tiers. Multi-LexSum operationalizes this with three discrete tiers; Jus IA's main-theses
feature is the same shape at the "tiny/short" end over a corpus of decisions.

## Governance note
D1–D4 are source-grounded; D5 is explicitly an Arcanum reading and must keep its **[A]** label
when reused. No definition here asserts an ungrounded number (case counts, baselines, splits
are in `open-residue.md`).
