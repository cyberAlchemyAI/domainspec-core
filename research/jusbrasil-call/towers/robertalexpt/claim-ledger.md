# claim-ledger.md — Captured Claims

Date checked: 2026-06-10. Each claim carries a **source-kind** label:

- **[PRIMARY]** — stated by the paper or authors' released artifacts (model card,
  repo, dataset cards). Verbatim quotes are ≤125 chars and attributed.
- **[CORROBORATED]** — appears consistently across ≥2 author artifacts/search summaries.
- **[READING]** — our (Arcanum) interpretation or Jusbrasil mapping. NOT a source claim.
- **[OPEN]** — not yet verified from a source; tracked in `open-residue.md`.

---

## A. Corpora

| # | Claim | Source-kind | Source |
|---|---|---|---|
| A1 | LegalPT aggregates **6 Portuguese legal corpora** into **125.1 GiB / 22.5B tokens**. | [PRIMARY] | repo + model card |
| A2 | LegalPT subcorpora: MultiLegalPile (PT) ~92 GiB / 13.76B words; Ulysses-Tesemõ ~26 GiB / 2.2M docs; ParlamentoPT 2.6M docs; Iudicium Textum ~1 GiB (STF rulings 2010–2018); Acórdãos TCU 600k docs (1992–2019); DataSTF 700k decisions / 5 GiB. | [PRIMARY] | LegalPT dataset card |
| A3 | CrawlPT = general PT web corpus, **163.2 GiB / 29.2B tokens**, from 3 sources: brWaC (16.3 GiB / 2.7B), CC100-PT (49.1 GiB / 8.4B), OSCAR-2301-PT (97.8 GiB / 18.1B). | [PRIMARY] | repo |
| A4 | Deduplicated versions released: LegalPT_dedup, CrawlPT_dedup. | [PRIMARY] | model card |

## B. Deduplication method (decisive)

| # | Claim | Source-kind | Source |
|---|---|---|---|
| B1 | Dedup via **MinHash + Locality Sensitive Hashing (LSH)**, using **5-grams**, **signature size 256**, treating two docs as identical if **Jaccard similarity > 0.7**. | [PRIMARY] | repo / model card (verbatim threshold) |
| B2 | Implementation used the **`text-dedup`** library. | [PRIMARY] | model card |
| B3 | Brazilian/Portuguese legal corpora are heavily duplicated (repeated ementas, citations, templated decisions), motivating dedup. | [CORROBORATED] | search summary + abstract paraphrase |
| B4 | Exact % of documents removed / size-reduction ratio by dedup. | [OPEN] | not in fetched artifacts — needs PDF |

## C. Model + pretraining

| # | Claim | Source-kind | Source |
|---|---|---|---|
| C1 | RoBERTaLexPT-base is a **RoBERTa-base architecture MLM, pretrained from scratch** on LegalPT + CrawlPT. | [PRIMARY] | model card |
| C2 | Hyperparameters: **62,500 steps, batch 2048, LR 4e-4, max seq len 512, 15% masking, AdamW** w/ linear warmup+decay. | [PRIMARY] | model card |
| C3 | Paper studies impact of **hyperparameters and embedding initialization**. | [CORROBORATED] | search summary |

## D. PortuLex benchmark

| # | Claim | Source-kind | Source |
|---|---|---|---|
| D1 | PortuLex = aggregated **4-task legal benchmark** for Portuguese. | [PRIMARY] | repo + model card |
| D2 | Tasks/datasets: **LeNER-Br** (NER), **UlyssesNER-Br** (NER), **FGV-STF** (NER), **RRI / RRIP** (classification). | [PRIMARY] | repo |
| D3 | Split sizes: RRI 8.26k/1.05k/1.47k; LeNER-Br 7.83k/1.18k/1.39k; UlyssesNER-Br 3.28k/489/524; FGV-STF 415/60/119 (train/dev/test). | [PRIMARY] | repo |

## E. Results + key findings

| # | Claim | Source-kind | Source |
|---|---|---|---|
| E1 | RoBERTaLexPT-base scores **85.41 average macro-F1** on PortuLex. | [PRIMARY] | model card + repo |
| E2 | It **beats larger generic models** (e.g., Albertina-PT-BR-xlarge 85.08) and **legal models** (Legal-RoBERTa-PT-large 84.02). | [PRIMARY] | model card + repo |
| E3 | It beats BERTimbau-base (83.78) and BERTimbau-large (84.60). | [PRIMARY] | model card |
| E4 | **Pretraining on legal + general data > legal-only** for legal tasks (the mix wins). | [CORROBORATED] | search summary + abstract paraphrase |
| E5 | Dedup is **decisive** for the quality gain (a central thesis). | [CORROBORATED] / [READING-amplified] | search summary; magnitude unquantified (see B4) |

## F. Artifacts / licensing

| # | Claim | Source-kind | Source |
|---|---|---|---|
| F1 | Model + datasets released openly under **CC BY 4.0**. | [PRIMARY] | model card |
| F2 | All artifacts hosted on HuggingFace under `eduagarcia/*`; code at GitHub `eduagarcia/roberta-legal-portuguese`. | [PRIMARY] | model card + repo |

---

### Numbers explicitly NOT invented

Any figure absent above (e.g., dedup removal %, per-task F1 breakdown, exact
legal:general token ratio in the final mix) is **[OPEN]** and logged in
`open-residue.md`. No placeholder numbers were fabricated.
