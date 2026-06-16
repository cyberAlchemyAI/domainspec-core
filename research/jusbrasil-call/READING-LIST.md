# Jusbrasil Call-Prep Reading List — Legal NLP for Jus IA

Dispatch: `jusbrasil-legal-nlp-deep-research-20260610` · Synthesized 2026-06-10 from 6 research-lane receipts ([lane-receipts.md](lane-receipts.md)). All entries carry lane-verified arXiv IDs, DOIs, or ACL Anthology links; unverifiable candidates were demoted to the residue ledger.

## Read-first shortlist (limited prep time — read these 8)

1. **Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools** — Magesh et al. 2024 — [arXiv:2405.20362](https://arxiv.org/abs/2405.20362)
   Audits exactly Jus IA's product category (RAG legal research assistants): 17–33% residual hallucination, much of it caused by retrieval failures, plus the "misgrounded citation" failure mode. Know the 17% number cold before the call.
2. **Juru: Legal Brazilian Large Language Model from Reputable Sources** — Malaquias Junior et al. 2024 — [arXiv:2403.18140](https://arxiv.org/abs/2403.18140)
   The one paper that does what Jusbrasil would consider in-house: continued pretraining on curated Brazilian legal text, with the catastrophic-forgetting cost honestly measured. Cited by four of six lanes — the keystone BR paper.
3. **RoBERTaLexPT** — Garcia et al. 2024, PROPOR — [ACL: 2024.propor-1.38](https://aclanthology.org/2024.propor-1.38/)
   LegalPT corpus + PortuLex benchmark; shows deduplication is decisive because Brazilian legal corpora are massively boilerplate-duplicated — a direct hit on the "millions of redundant documents" challenge.
4. **JUÁ: A Benchmark for IR in Brazilian Legal Text Collections** — Pereira et al. 2026 — [arXiv:2604.06098](https://arxiv.org/abs/2604.06098)
   The freshest BR artifact: unified Brazilian legal IR benchmark whose core finding — retrieval quality varies sharply across legal collection types — is precisely the tribunal-heterogeneity problem. Asking "do you evaluate on JUÁ?" is an instant credibility move.
5. **Improving abstractive summarization of legal rulings through textual entailment** — Feijó & Moreira 2023, AI & Law — [DOI 10.1007/s10506-021-09305-4](https://link.springer.com/article/10.1007/s10506-021-09305-4)
   Literally Jus IA's "smart summaries" task: ementa generation for Brazilian rulings with an entailment-based faithfulness filter.
6. **Multi-LexSum** — Shen et al. 2022, NeurIPS D&B — [arXiv:2206.10883](https://arxiv.org/abs/2206.10883)
   Multi-document, multi-granularity case-cluster summarization — the closest benchmark shape to "principais teses" extraction.
7. **UlyssesLegalNER-Br** — Albuquerque et al. 2026, PROPOR — [ACL: 2026.propor-1.33](https://aclanthology.org/2026.propor-1.33/)
   Current state of the art and schema for Brazilian legal NER; one paper covering the whole LeNER-Br lineage with quotable baselines.
8. **Using deep learning to predict outcomes of legal appeals better than human experts (Brazilian federal courts)** — de Menezes-Neto et al. 2022, PLOS ONE — [DOI 10.1371/journal.pone.0272287](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0272287)
   612k Brazilian appeals; models beat human experts ~3x. The credibility anchor if the conversation turns to next products.

## Their "unique NLP challenges" — what the literature says they probably mean

| Stated/likely challenge | Evidence-backed framing | Key papers |
|---|---|---|
| Brazilian Portuguese legal register | PT-BR vs PT-PT variant split; legalese token inflation; domain adaptation beats generic models | Albertina ([2305.06721](https://arxiv.org/abs/2305.06721)), Sabiá ([2304.07880](https://arxiv.org/abs/2304.07880)), LegalBert-pt, Juru |
| Millions of long, redundant judgments | Dedup is decisive (boilerplate ementas); structure-aware encoding beats truncation | RoBERTaLexPT, SAILER ([2304.11370](https://arxiv.org/abs/2304.11370)), LegalSeg ([2502.05836](https://arxiv.org/abs/2502.05836)) |
| Tribunal heterogeneity | Retrieval quality varies sharply by collection type; needs per-regime evaluation | JUÁ, JurisTCU ([2503.08379](https://arxiv.org/abs/2503.08379)), LeCaRDv2 ([2310.17609](https://arxiv.org/abs/2310.17609)) |
| OCR-noisy scanned filings (PJe) | Multimodal page-sequence models beat text-only; LLM OCR post-correction has no free lunch in lower-resource languages | VICTOR multimodal ([2207.00748](https://arxiv.org/abs/2207.00748)), Kanerva ([2502.01205](https://arxiv.org/abs/2502.01205)), LayoutLM ([1912.13318](https://arxiv.org/abs/1912.13318)) |
| Hallucination risk for lawyers | RAG reduces but does not eliminate; fluency metrics anti-correlate with citation faithfulness; abstention is the missing behavior | Magesh, Dahl ([2401.01301](https://arxiv.org/abs/2401.01301)), CLERC ([2406.17186](https://arxiv.org/abs/2406.17186)), Abstention survey ([2407.18418](https://arxiv.org/abs/2407.18418)) |

## By Jus IA product feature

### Research assistant (legal Q&A with citations)
- Magesh et al. ([2405.20362](https://arxiv.org/abs/2405.20362)) — audit template and failure taxonomy for the product category.
- Dahl et al., *Large Legal Fictions* ([2401.01301](https://arxiv.org/abs/2401.01301)) — hallucination base rates and typology; contra-factual premise probing.
- Reuter et al. ([2510.06999](https://arxiv.org/abs/2510.06999)) — document-level retrieval mismatch + summary-augmented chunking, a cheap practical fix.
- CitaLaw ([2412.14556](https://arxiv.org/abs/2412.14556)) — syllogism-style check that a cited source actually supports the answer.
- Zheng et al., reasoning-focused retrieval ([2505.03970](https://arxiv.org/abs/2505.03970)) — retrievers degrade on reasoning-heavy queries.
- Abstention survey ([2407.18418](https://arxiv.org/abs/2407.18418)) — designing the refuse/hedge policy.

### Similar jurisprudence
- SAILER ([2304.11370](https://arxiv.org/abs/2304.11370)) — structure-aware case encoders (maps to relatório/voto/dispositivo/ementa).
- CaseGNN ([2312.11229](https://arxiv.org/abs/2312.11229)) + CaseLink ([2403.17780](https://arxiv.org/abs/2403.17780)) — precedent/citation-graph retrieval "beyond keyword matching."
- JurisBERT (DOI [10.1007/978-3-031-36805-9_24](https://link.springer.com/chapter/10.1007/978-3-031-36805-9_24)) — ementa-pair STS, the closest BR analogue to the feature.
- LeCaRDv2 ([2310.17609](https://arxiv.org/abs/2310.17609)) — multi-dimensional legal-relevance definition for building internal eval sets.
- JUÁ ([2604.06098](https://arxiv.org/abs/2604.06098)) + JurisTCU ([2503.08379](https://arxiv.org/abs/2503.08379)) — the BR benchmarks to evaluate against.
- CLERC ([2406.17186](https://arxiv.org/abs/2406.17186)) — citation-to-query training data construction from their own citation graph.

### Smart summaries & main theses
- Feijó & Moreira (DOI [10.1007/s10506-021-09305-4](https://link.springer.com/article/10.1007/s10506-021-09305-4)) — ementa generation with entailment-based faithfulness.
- Multi-LexSum ([2206.10883](https://arxiv.org/abs/2206.10883)) — multi-document, multi-granularity case-cluster summaries.
- CaseHOLD ([2104.08671](https://arxiv.org/abs/2104.08671)) — holding identification, the per-case building block of "teses."
- Rhetorical roles: Kalamkar ([2112.01836](https://arxiv.org/abs/2112.01836)), LegalSeg ([2502.05836](https://arxiv.org/abs/2502.05836)) — segmentation that makes long judgments tractable.
- Argument-aware summarization + reranking ([2306.00672](https://arxiv.org/abs/2306.00672)); LLM-readiness caution ([2306.01248](https://arxiv.org/abs/2306.01248)); field survey ([2501.17830](https://arxiv.org/abs/2501.17830)).
- PublicHearingBR ([2410.07495](https://arxiv.org/abs/2410.07495)) — PT-BR long-document summarization + NLI faithfulness; also adjacent to audio transcription.

### Foundation-model layer (build vs. buy)
- Juru ([2403.18140](https://arxiv.org/abs/2403.18140)); Sabiá ([2304.07880](https://arxiv.org/abs/2304.07880)) / Sabiá-2 ([2403.09887](https://arxiv.org/abs/2403.09887)); RoBERTaLexPT (ACL 2024.propor-1.38); LegalBert-pt (DOI [10.1007/978-3-031-45392-2_18](https://link.springer.com/chapter/10.1007/978-3-031-45392-2_18)); BERTimbau (DOI [10.1007/978-3-030-61377-8_28](https://link.springer.com/chapter/10.1007/978-3-030-61377-8_28)); Albertina ([2305.06721](https://arxiv.org/abs/2305.06721)); ptt5-v2 ([2406.10806](https://arxiv.org/abs/2406.10806)); Tucano ([2411.07854](https://arxiv.org/abs/2411.07854)).
- Narrative: cheap continued pretraining works (Sabiá → Juru), but costs general ability; post-2024 the field shifted toward RAG over frontier models — a good question to put to them.

### Ingestion pipeline (NER, structure, OCR)
- LeNER-Br (DOI [10.1007/978-3-319-99722-3_32](https://doi.org/10.1007/978-3-319-99722-3_32)) → UlyssesLegalNER-Br (ACL 2026.propor-1.33) — the BR legal NER lineage.
- VICTOR (ACL [2020.lrec-1.181](https://aclanthology.org/2020.lrec-1.181/)) + multimodal page classification ([2207.00748](https://arxiv.org/abs/2207.00748)) — STF-scale bundle splitting under OCR noise.
- Seq2seq extraction with source alignment ([2201.05658](https://arxiv.org/abs/2201.05658)) — provenance-preserving structured extraction.
- verBERT/Kollemata ([2203.06224](https://arxiv.org/abs/2203.06224)) — jurisprudence categorization.
- LayoutLM ([1912.13318](https://arxiv.org/abs/1912.13318)); OCR post-correction caution ([2502.01205](https://arxiv.org/abs/2502.01205), see also [2504.00414](https://arxiv.org/abs/2504.00414)).

### Evaluation stack
- BR-specific: oab-bench ([2504.21202](https://arxiv.org/abs/2504.21202)) — validated LLM-as-judge on OAB essays; BLUEX ([2307.05410](https://arxiv.org/abs/2307.05410)) — contamination-aware PT capability axis.
- General: LegalBench ([2308.11462](https://arxiv.org/abs/2308.11462)); LawBench ([2309.16289](https://arxiv.org/abs/2309.16289)) — the civil-law-jurisdiction benchmark design, structurally closer to Brazil than US benchmarks.

## Next-product opportunities (L7 lane)

1. **Outcome & duration prediction ("Probabilidade de Êxito")** — Lage-Freitas ([1905.10348](https://arxiv.org/abs/1905.10348)), de Menezes-Neto (PLOS ONE, 612k appeals, beats experts), Verçosa duration/process-mining (DOI [10.1007/s44257-024-00015-0](https://link.springer.com/article/10.1007/s44257-024-00015-0)); methodology caution: filing-time-only evaluation ([2410.10542](https://arxiv.org/abs/2410.10542)).
2. **Petition drafting copilot** — template+multi-agent generation ([2402.14871](https://arxiv.org/abs/2402.14871)) + Juru for the model question.
3. **Contract review ("Jus IA Contratos")** — CUAD ([2103.06268](https://arxiv.org/abs/2103.06268)); ContractEval ([2508.03080](https://arxiv.org/abs/2508.03080)) — a PT-BR CUAD analogue would be both moat and publishable asset.
4. **Agentic legal workflows** — LegalAgentBench ([2412.17259](https://arxiv.org/abs/2412.17259)) — "process rate" makes agent quality auditable.
5. **Hearing/audio products** — CORAA ASR corpus ([2110.15731](https://arxiv.org/abs/2110.15731)) — spontaneous-speech WER is the binding constraint; extends their existing transcription feature.
6. **Jurimetria analytics** — DataJud (DOI [10.1145/3614321.3614381](https://dl.acm.org/doi/10.1145/3614321.3614381)) + STF's own VICTOR project ([1811.11569](https://arxiv.org/abs/1811.11569)) — position as the lawyer-side mirror of court-internal ML.

## Questions to ask on the call (evidence-motivated)

1. How is "similar jurisprudence" relevance defined and annotated — decomposed (facts vs. thesis vs. outcome) like LeCaRDv2, or single-label? Do they evaluate on JUÁ/JurisTCU or only internal sets?
2. Do they run a Magesh-style preregistered hallucination audit, and what is the measured misgrounded-citation rate? Is error attribution split between retrieval and generation (CLERC framing)?
3. What is the abstention policy when retrieval confidence is low — and is abstention itself evaluated?
4. Are "principais teses" trained against STJ/STF temas-repetitivos statements as silver labels? (No published work does this — possible joint-publication gap.)
5. Do they segment acórdãos (relatório/voto/dispositivo) with rules or learned models? Any PT-BR rhetorical-role corpus internally?
6. OCR pipeline: layout-aware encoders on PJe scans, or OCR-text-only with noise-robust fine-tuning? How do OCR-corrupted citation strings get normalized (LexML URNs?)?
7. Build vs. buy: did Juru-style continued pretraining beat frontier-API prompting on their internal evals? Did they measure legalese token inflation under frontier tokenizers?
8. LGPD: anonymization recall targets for segredo-de-justiça content, and DataJud licensing limits for judge-level analytics (CNJ Resolution 331)?

## Residue ledger (gaps & unverified — do not cite without checking)

- No published work on **tese jurídica extraction supervised by temas repetitivos** — literature gap, possible collaboration angle.
- No PT-BR **rhetorical-role-labeled judgment corpus**; no **legal-PT tokenizer fertility** study; no **Brazilian citation-faithfulness** (súmula-level grounding) paper; no **settlement-value prediction** or **PT-BR deposition summarization** papers found.
- Unverified candidates excluded from the list: Gervásio PT-* (decoder sibling of Albertina), RulingBR standalone dataset paper, "LegalBench-BR" (ResearchGate only), "Rabula" (CEUR-WS Vol-4089), LGPD pseudonymization benchmark (ResearchGate only), "MASLegalBench" (arXiv 2509.24922, unverified), "LLM Agents in Law" survey (arXiv 2601.06216, unverified), LegalSearchLM ([2505.23832](https://arxiv.org/abs/2505.23832), ID verified but authorship unconfirmed), COLIEE annual overview papers (not on arXiv).
- All relevance notes are research-lane claims pending operator review before the call (per dispatch promotion guardrails).
