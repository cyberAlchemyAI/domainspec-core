# glossary.md — Key Terms

Plain-language entries. Governed/precise versions live in `definitions.md`.

- **LegalPT** — The Portuguese **legal** pretraining corpus introduced by the
  paper. Aggregates 6 legal sources (court rulings, parliament, accounts-court
  decisions, legal MC4) into ~125 GiB / 22.5B tokens. [PRIMARY]

- **CrawlPT** — The **general** Portuguese web corpus assembled as the non-legal
  half of the pretraining mix (brWaC + CC100-PT + OSCAR-PT), ~163 GiB / 29.2B
  tokens. The "general" in the legal+general recipe. [PRIMARY]

- **PortuLex** — The 4-task **legal benchmark** introduced to evaluate Portuguese
  legal models: LeNER-Br, UlyssesNER-Br, FGV-STF (all NER), and RRI
  (classification). Reported as average macro-F1. [PRIMARY]

- **MinHash / LSH deduplication** — A near-duplicate detection technique. MinHash
  produces a small fingerprint (here: 256-value signature over 5-grams) that
  estimates **Jaccard similarity** between documents; **LSH** buckets similar
  fingerprints so you avoid all-pairs comparison. Docs with Jaccard > 0.7 are
  collapsed as duplicates. Decisive here because legal text is heavily
  boilerplate-duplicated. [PRIMARY]

- **Jaccard similarity** — Overlap measure = |A∩B| / |A∪B| over the two docs'
  n-gram sets. Threshold of 0.7 = "70%+ shared n-grams ⇒ duplicate." [PRIMARY]

- **RoBERTa pretraining** — Encoder-only transformer trained with **masked
  language modeling (MLM)** only (no next-sentence prediction), large batches,
  dynamic masking. Here: RoBERTa-base, from scratch, 62.5k steps, batch 2048,
  15% masking. Produces contextual embeddings, not a generator. [PRIMARY]

- **Domain mix (legal + general)** — The pretraining recipe combining
  domain (LegalPT) and general (CrawlPT) data. The paper's finding: the **mix
  beats legal-only** for legal downstream tasks. [CORROBORATED]

- **Boilerplate duplication (ementas/citations)** — Brazilian judicial documents
  repeat large templated blocks (headnotes/*ementas*, citation strings,
  standardized decision language) across millions of documents; naive corpora
  over-represent these, which dedup removes. [READING / CORROBORATED motivation]

- **Encoder / foundation layer** — (Jusbrasil framing) the layer that turns legal
  text into embeddings/representations feeding retrieval and classification —
  where this paper's model sits. [READING]
