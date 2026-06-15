# TOWER.md — Tower Map

Lane: `robertalexpt`. Paper: RoBERTaLexPT (PROPOR 2024).

## Floors (files) and what each holds

| Floor | File | Holds | Source-kind |
|---|---|---|---|
| L0 | `L0-corpus.md` | Source record (URLs, IDs, artifacts) + section map | Provenance |
| Claims | `claim-ledger.md` | Every captured claim with a source-kind label | Mixed (labeled) |
| Terms | `glossary.md` | Plain-language glossary of key terms | Reading |
| Defs | `definitions.md` | Governed definitions for load-bearing concepts | Source-anchored |
| Distill | `distill.md` | One-sentence model + compositional spine + borrow/analogy/block | Reading |
| Bridge | `bridge-decisions.md` | Source-claim vs Arcanum-reading statuses | Governance |
| Pack | `LEARNING-PACK.md` | The deliverable: claims, operator model, takeaways, 5-for-call, cutoff | Mixed (labeled) |
| Residue | `open-residue.md` | What was not fetched / open questions | Governance |

## Spine (how the paper composes)

```
Problem: Brazilian legal corpora are massively boilerplate-duplicated
   (repeated ementas, citations, templated decisions).
        |
        v
Contribution 1: LegalPT corpus  (aggregate 6 legal sources -> 125.1 GiB / 22.5B tokens)
Contribution 2: CrawlPT corpus  (general web PT -> 163.2 GiB / 29.2B tokens)
        |
        v
Method: MinHash + LSH deduplication (5-grams, 256 sig, Jaccard > 0.7)
        |
        v
Pretrain RoBERTa-base from scratch on LegalPT + CrawlPT (legal + general mix)
        |
        v
Contribution 3: PortuLex benchmark (4 legal tasks: LeNER-Br, UlyssesNER-Br, FGV-STF, RRI)
        |
        v
Result: RoBERTaLexPT-base = 85.41 avg macro-F1, beats larger generic + legal baselines.
Finding: legal + general mix > legal-only; dedup is decisive.
```

## Jusbrasil mapping (Arcanum reading)

Encoder/foundation layer for Jus IA: corpus dedup → embeddings for
similar-jurisprudence retrieval; legal+general mix as the pretraining recipe;
direct answer to the "millions of redundant judicial documents" challenge.
Mapping detail lives in `LEARNING-PACK.md` and is labeled as a reading, not a
source claim.
