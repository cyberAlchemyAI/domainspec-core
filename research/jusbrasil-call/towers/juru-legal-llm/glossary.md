# glossary.md — Quick Terms

**Date checked:** 2026-06-10
Quick, readable definitions. Governed/load-bearing versions live in `definitions.md`.

- **Continued pretraining (CPT).** Taking an already-pretrained base model (here Mistral-7B)
  and running more self-supervised next-token training on a new corpus (here Brazilian legal
  text) to bias it toward a domain. Not fine-tuning on labeled tasks — same objective as
  pretraining, new data.

- **Domain adaptation.** The general goal of making a model perform better in a target domain.
  Continued pretraining is one mechanism; RAG, fine-tuning, and prompt engineering are others.

- **Catastrophic forgetting.** When training on new data erodes capabilities the model had
  before. In Juru it shows up as measurable drops on general-knowledge benchmarks (PT and EN)
  after legal specialization — the price paid for the legal gain.

- **Reputable-source curation.** The data-quality strategy of building the corpus only from
  authoritative material — Brazilian academic legal papers, official statutes via LexML, and
  Supreme Federal Court decisions — rather than scraped web text. The "high-quality data" lever.

- **OAB benchmark.** Test sets derived from the Ordem dos Advogados do Brasil (Brazilian Bar
  Association) exam — the qualifying exam to practice law in Brazil. Used as a legal-capability
  benchmark (OAB-2023, OAB-2024 in this paper). ENAM is the analogous national judiciary exam.

- **Few-shot evaluation.** Measuring the model by giving it a handful of in-context examples
  before each test question, rather than fine-tuning it for the task.

- **MMLU.** Massive Multitask Language Understanding — a broad English knowledge benchmark
  (used here, college + high-school splits) to measure general (out-of-domain) ability.
