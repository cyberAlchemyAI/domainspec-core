# L0-corpus.md — Source Record + Section Map

Date checked: **2026-06-10**. All claims downstream trace to these sources.

## Primary source (the paper)

- **Title:** RoBERTaLexPT: A Legal RoBERTa Model Pretrained with Deduplication for Portuguese
- **Authors:** Eduardo Garcia, Nadia Silva, Felipe Siqueira, Juliana Gomes, Hidelberg O. Albuquerque, Ellen Souza, Eliomar Lima, André de Carvalho
- **Venue:** Proceedings of the 16th Intl. Conf. on Computational Processing of Portuguese (PROPOR 2024), Santiago de Compostela, Galicia/Spain. Pages 374–383. Publisher: ACL.
- **Landing (ACL Anthology):** https://aclanthology.org/2024.propor-1.38/  [checked 2026-06-10]
- **PDF:** https://aclanthology.org/2024.propor-1.38.pdf  [checked 2026-06-10; downloaded, not text-extractable in this environment — see open-residue]

## Authors' released artifacts (primary-adjacent: author-published)

- **Model card:** https://huggingface.co/eduagarcia/RoBERTaLexPT-base  [checked 2026-06-10]
- **Code/resources repo:** https://github.com/eduagarcia/roberta-legal-portuguese  [checked 2026-06-10]
- **LegalPT dataset:** https://huggingface.co/datasets/eduagarcia/LegalPT  [checked 2026-06-10]
- **LegalPT (deduplicated):** eduagarcia/LegalPT_dedup
- **CrawlPT dataset:** https://huggingface.co/datasets/eduagarcia/CrawlPT
- **CrawlPT (deduplicated):** eduagarcia/CrawlPT_dedup
- **PortuLex benchmark:** https://huggingface.co/datasets/eduagarcia/PortuLex_benchmark
- **Collection:** https://huggingface.co/collections/eduagarcia/roberta-legal-portuguese-65c3f7247d10ab35a75de3e9

## Secondary / mirror sources (corroboration only)

- Linguamática journal mirror: https://linguamatica.com/.../article/view/457  [redirect loop on 2026-06-10 — not fetched]
- ResearchGate mirror: publication/378909440  [HTTP 403 on 2026-06-10 — not fetched]

## Section map (reconstructed from artifacts + abstract summaries)

> NOTE: The full PDF body was not machine-readable in this environment. Section
> structure below is reconstructed from the model card, repo, and search
> summaries, not from a verbatim TOC. Treat as approximate until PDF verified.

1. **Introduction** — legal NLP for Portuguese; need for domain-adapted models.
2. **Related work** — prior Portuguese / legal PLMs (BERTimbau, Albertina, Legal-RoBERTa-PT).
3. **Corpora** — LegalPT (6 legal sources) + CrawlPT (3 general web sources).
4. **Deduplication** — MinHash + LSH; high duplication in legal corpora.
5. **Pretraining** — RoBERTa-base from scratch; hyperparameters; embedding init.
6. **PortuLex benchmark** — 4 legal tasks (LeNER-Br, UlyssesNER-Br, FGV-STF, RRI).
7. **Experiments / results** — macro-F1 vs baselines; legal+general vs legal-only.
8. **Conclusion** — dedup decisive; mix outperforms larger generic models.

## License

Model and artifacts: Creative Commons Attribution 4.0 International (CC BY 4.0). [model card, 2026-06-10]
