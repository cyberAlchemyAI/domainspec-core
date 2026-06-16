# Distill

## One-sentence model

UlyssesLegalNER-Br extends Brazilian legal NER from the legislative domain to the full legal domain by releasing a 560-document corpus over bills + case law + statutes with a 9-category / 23-type schema and CRF/BiLSTM/BERTimbau baselines, where BERTimbau hits 96.18% micro F1 on the unified corpus. [C1–C9]

## Compositional spine

```
PROBLEM:   Brazilian legal NER is data-starved; prior corpora cover only sub-domains.
              | LeNER-Br -> case law focus (2018)        [R3]
              | UlyssesNER-Br -> legislative bills (2022) [R1, C3]
              | (gap) -> no corpus exclusively on statutes/laws
   v
CONTRIBUTION: A unified corpus spanning the triad.
              | bills + case laws + laws = 560 docs       [C1, C4]
              | first NER corpus exclusively on Brazilian laws [C2]
              | 9 categories / 23 fine-grained types       [C6]
              | hybrid annotation                          [C5]
   v
METHOD:    Evaluate baselines across the corpus.
              | CRF (feature-based)                        [C7]
              | BiLSTM (recurrent)                         [C7]
              | BERTimbau (PT-BR transformer)              [C7]
              | measure: predictive perf + compute cost + per-label [C8]
   v
RESULT:    Strong, reusable baseline.
              | best micro F1 96.18% (BERTimbau, unified)  [C9]
              | 6 cat / 7 types > 95%; floor 71-82%        [C10]
```

## Borrow / Analogy / Block (for the Jusbrasil pipeline)

- **BORROW.** The **document-type triad** (bills / case law / statutes) and the **9-cat/23-type fine-grained schema** as a reference annotation target for a Brazilian-legal ingestion NER layer. BERTimbau-as-baseline is directly reusable. [C6, C7]

- **ANALOGY.** "Unified corpus beats per-domain" -> Jusbrasil should consider a **single cross-document-type NER model** rather than siloed models per source. The 71–82% floor is the analog of *hard normalization classes* — the entity types where downstream linking will need extra rules/disambiguation. [A1, READING]

- **BLOCK (do not over-borrow).** The paper stops at **recognition**. It does NOT deliver entity **normalization**, citation linking, or jurisprudence organization — those are Jusbrasil-side and out of scope here. The specific 23 type names, per-label scores, splits, and license are **open-residue**; do not design against assumed schema names until the PDF is read (O1–O8).
