# Lane Receipts — jusbrasil-legal-nlp-deep-research-20260610

Dispatch: `jusbrasil-legal-nlp-deep-research-20260610` · Step: `literature-fanout` · Join: parent_synthesis · 2026-06-10

Receipts below are verbatim subagent returns. Agent IDs: L1 `a46a890a21ab86e4a`, L2 `a3617b88b5d35502b`, L3 `ae830d416054a3a20`, L4 `a5f0004ac97e1d2fc`, L5 `a47ce08265f5d9f79`, L7 `acdd1c04e3f8b3939`.

---

## L1 — Portuguese & Legal-Domain Language Models

### Papers

1. **BERTimbau: Pretrained BERT Models for Brazilian Portuguese** — Souza et al., 2020, BRACIS (Springer LNCS). [BR-specific]
   DOI: [10.1007/978-3-030-61377-8_28](https://link.springer.com/chapter/10.1007/978-3-030-61377-8_28)
   The foundational PT-BR encoder, trained on BrWaC, that nearly every Brazilian legal NLP system (including most legal BERT derivatives below) builds on. Still the default backbone for classification/NER/retrieval components like those behind Jus IA's "principais teses" extraction and jurisprudence organization. Useful as the baseline reference point when discussing why domain adaptation on top of it pays off.

2. **Albertina PT-*: Advancing Neural Encoding of Portuguese** — Rodrigues et al., 2023. [General]
   arXiv: [2305.06721](https://arxiv.org/abs/2305.06721) (follow-up family paper: [arXiv:2403.01897](https://arxiv.org/abs/2403.01897), 2024)
   DeBERTa-based open encoders with separate PT-PT and PT-BR variants (100M–1.5B), explicitly addressing the European/Brazilian variant split. Relevant to Jusbrasil's embedding/reranking stack: a stronger encoder than BERTimbau for the same compute class, and the PT-BR/PT-PT contrast is a clean way to discuss register sensitivity in Portuguese legal text.

3. **Sabiá: Portuguese Large Language Models** — Pires et al., 2023, EPIA. [BR-specific]
   arXiv: [2304.07880](https://arxiv.org/abs/2304.07880)
   The canonical evidence that cheap continued pretraining on Portuguese (≤3% of original budget on GPT-J/LLaMA) yields large monolingual gains. This is the recipe Juru applies to law, and the core argument for whether Jusbrasil should continue-pretrain vs. prompt a frontier model for the Jus IA assistant. (Successor: [Sabiá-2, arXiv:2403.09887](https://arxiv.org/abs/2403.09887), with Brazilian exam evals incl. OAB.)

4. **RoBERTaLexPT: A Legal RoBERTa Model Pretrained with Deduplication for Portuguese** — Garcia et al., 2024, PROPOR. [BR-specific]
   ACL Anthology: [2024.propor-1.38](https://aclanthology.org/2024.propor-1.38/)
   Builds the LegalPT corpus and the PortuLex benchmark; shows that MinHash/LSH deduplication matters enormously because legal corpora are massively duplicated (boilerplate ementas, repeated citations) — directly the "millions of long, redundant judicial documents" problem. A legal+general pretraining mix beat larger generic models, which informs any Jus IA encoder used for similar-jurisprudence retrieval.

5. **LegalBert-pt: A Pretrained Language Model for the Brazilian Portuguese Legal Domain** — Silveira et al., 2023, BRACIS (Springer LNCS). [BR-specific]
   DOI: [10.1007/978-3-031-45392-2_18](https://link.springer.com/chapter/10.1007/978-3-031-45392-2_18)
   Compares from-scratch legal pretraining vs. continued pretraining from BERTimbau on a diverse Brazilian legal corpus; wins on legal NER and classification. Directly informs the extraction pipeline behind "principais teses" (identifying parties, dispositivos, thesis statements) and gives a concrete from-scratch-vs-adapt data point for the call.

6. **JurisBERT: A New Approach that Converts a Classification Corpus into an STS One** — Viegas et al., 2023, ICCSA (Springer LNCS). [BR-specific]
   DOI: [10.1007/978-3-031-36805-9_24](https://link.springer.com/chapter/10.1007/978-3-031-36805-9_24)
   Trains a legal BERT from scratch and converts a multi-level classification corpus of ~24k ementa pairs into graded STS data for fine-tuning legal similarity. This is the closest published analogue to Jus IA's "similar jurisprudence beyond keyword matching" feature — semantic similarity over acórdão summaries with a small, cheap model.

7. **Juru: Legal Brazilian Large Language Model from Reputable Sources** — Junior et al., 2024. [BR-specific]
   arXiv: [2403.18140](https://arxiv.org/abs/2403.18140)
   Continued pretraining of Mistral-7B on 1.9B curated tokens of Brazilian legal text (academic papers, federal regulations, rulings); improves legal benchmarks but documents catastrophic forgetting on general knowledge. The single most on-point paper for Jusbrasil: it quantifies the trade-off they face if they specialize an LLM for the Jus IA assistant, and its "reputable sources" curation stance speaks to hallucination mitigation.

8. **ptt5-v2: A Closer Look at Continued Pretraining of T5 Models for the Portuguese Language** — Piau et al., 2024, BRACIS. [General]
   arXiv: [2406.10806](https://arxiv.org/abs/2406.10806) (original PTT5: [arXiv:2008.09144](https://arxiv.org/abs/2008.09144))
   Systematic ablations of continued-pretraining knobs for Portuguese (quality filters, optimizer schedules, multi-epoch training) up to 3B params, with SOTA on assin2 RTE and TweetSentBR. Practical playbook for the seq2seq components plausible in Jus IA's smart summaries, and methodologically transferable to legal continued pretraining.

9. **Tucano: Advancing Neural Text Generation for Portuguese** — Corrêa et al., 2024. [General]
   arXiv: [2411.07854](https://arxiv.org/abs/2411.07854)
   Fully open PT pipeline: the GigaVerbo corpus (~200B dedup'd tokens), Portuguese-native tokenizer, open decoder models, plus a critical look at weaknesses of existing Portuguese benchmarks. Relevant to tokenizer fertility on Portuguese (and by extension legal) text and to evaluation pitfalls Jusbrasil will hit when benchmarking Jus IA against generic LLMs.

### Read-first picks

- **Juru (arXiv:2403.18140)** — the only paper that does exactly what Jusbrasil would consider (legal continued pretraining of an LLM on Brazilian sources) and honestly reports the forgetting cost.
- **RoBERTaLexPT (2024.propor-1.38)** — brings the corpus (LegalPT), the benchmark (PortuLex), and the deduplication lesson that maps one-to-one onto Jusbrasil's document-scale problem.

### Residue

- **Tokenizer-specific work for Portuguese *legal* text**: no dedicated paper found on legal-PT tokenizer fertility/vocabulary adaptation; Tucano and Sabiá touch tokenization only in passing. Worth asking Jusbrasil whether they measured token inflation of legalese (e.g., Latin expressions, citation strings) under Llama/GPT tokenizers.
- **Gervásio PT-* (decoder sibling of Albertina)**: exists, but arXiv ID not verified this session, so excluded rather than risk a wrong ID.
- **BERTimbau arXiv ID**: a search snippet attributed arXiv:1909.10649 to BERTimbau, but that ID is associated with Souza et al.'s BERT-CRF NER paper; cited the verified Springer DOI instead.
- **OCR-noise-robust pretraining for Portuguese legal documents**: queries returned nothing specific — likely lives in other lanes (document AI/OCR) or is unpublished industrial practice; good call question ("how do you handle OCR noise in pretraining/retrieval corpora?").
- **2025–2026 Brazilian legal LLMs**: no verified successor to Juru surfaced in these searches (Sabiá-3 is general-purpose, technical report only); ask Jusbrasil whether they continue-pretrain in-house or rely on RAG over frontier models — the literature gap after mid-2024 suggests the field moved to retrieval+frontier-LLM architectures.

---

## L2 — Legal Retrieval & RAG

### Papers

1. **SAILER: Structure-aware Pre-trained Language Model for Legal Case Retrieval** — Haitao Li et al., 2023, SIGIR 2023. [arXiv:2304.11370](https://arxiv.org/abs/2304.11370) — [General]
   Foundational dense-retrieval paper for case law: exploits the canonical structure of judgments (facts → reasoning → decision) in pre-training so the encoder learns which sections carry legal-relevance signal. Directly relevant to Jus IA's "similar jurisprudence" feature, since Brazilian acórdãos have an analogous structure (relatório / voto / dispositivo / ementa) that a structure-aware encoder could exploit. Also a partial answer to the long-document challenge — it compresses key sections rather than truncating naively.

2. **LeCaRDv2: A Large-Scale Chinese Legal Case Retrieval Dataset** — Haitao Li et al., 2023, SIGIR 2024. [arXiv:2310.17609](https://arxiv.org/abs/2310.17609) — [General]
   The reference benchmark design for similar-case retrieval: 800 queries / 55k candidates from 4.3M criminal cases, with relevance decomposed into characterization, penalty, and procedure dimensions. The main transferable lesson for Jus IA is its multi-dimensional definition of "legal relevance" and its two-level candidate pooling — both are templates for how Jusbrasil could build internal eval sets for "similar jurisprudence" over tribunal-heterogeneous corpora.

3. **CaseGNN: Graph Neural Networks for Legal Case Retrieval with Text-Attributed Graphs** — Yanran Tang et al., 2023, ECIR 2024. [arXiv:2312.11229](https://arxiv.org/abs/2312.11229) — [General]
   Represents each case as a text-attributed graph and retrieves with GNN encoders plus contrastive learning, beating dense baselines on COLIEE 2022/2023 case-retrieval tracks. This is the citation-/structure-graph line of work that goes "beyond keyword matching" — the exact framing Jusbrasil uses for similar jurisprudence — and sidesteps the encoder length limit because node attributes are sentence-level (relevant to millions of long documents). Follow-ups by the same group (CaseLink [arXiv:2403.17780](https://arxiv.org/abs/2403.17780), CaseGNN++ [arXiv:2405.11791](https://arxiv.org/abs/2405.11791)) extend this to inductive precedent-graph learning.

4. **CLERC: A Dataset for Legal Case Retrieval and Retrieval-Augmented Analysis Generation** — Abe Bohan Hou et al., 2024, NAACL 2025. [arXiv:2406.17186](https://arxiv.org/abs/2406.17186) — [General]
   Builds retrieval + RAG tasks from 1.84M US federal cases / 20.7M citations: find the precedents a passage should cite, then generate the analysis grounded in them. Key sobering numbers for the research-assistant feature: zero-shot IR reaches only ~48% recall@1000 and GPT-4o hallucinates most while scoring best on ROUGE — i.e., surface fluency and groundedness diverge. The citation-to-query construction method is replicable on Jusbrasil's own citation graph.

5. **Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools** — Varun Magesh et al., 2024, Journal of Empirical Legal Studies 2025. [arXiv:2405.20362](https://arxiv.org/abs/2405.20362), DOI: [10.1111/jels.12413](https://onlinelibrary.wiley.com/doi/full/10.1111/jels.12413) — [General]
   Stanford audit of commercial legal RAG products (Lexis+ AI, Westlaw AI): even the best tool hallucinated ~17% of the time, and a large share of hallucinations traced back to retrieval failures, not generation. Provides a hallucination typology and preregistered eval methodology that Jus IA's research assistant should be benchmarked against — the most directly relevant paper to Jusbrasil's stated hallucination-risk challenge.

6. **Towards Reliable Retrieval in RAG Systems for Large Legal Datasets** — Markus Reuter et al., 2025. [arXiv:2510.06999](https://arxiv.org/abs/2510.06999) — [General]
   Identifies "Document-Level Retrieval Mismatch" — chunks retrieved from the wrong source document — as a dominant failure mode in large legal RAG, and proposes Summary-Augmented Chunking (prepending synthetic document summaries to chunks) as a cheap fix. Highly practical for Jus IA's research assistant and smart summaries over millions of long judgments, where chunking destroys document identity (which tribunal, which instance, which outcome).

7. **JurisTCU: A Brazilian Portuguese Information Retrieval Dataset with Query Relevance Judgments** — Leandro Carísio Fernandes et al., 2025. [arXiv:2503.08379](https://arxiv.org/abs/2503.08379) — [BR-specific]
   16k TCU jurisprudence documents + 150 queries with graded relevance judgments — one of the first Brazilian Portuguese legal IR datasets with proper qrels. Reports ~70% gains of embedding-based semantic search over lexical baselines on keyword-style queries, giving an empirical anchor for the dense-vs-BM25 question in the Brazilian legal register. Useful off-the-shelf eval for Jus IA's retrieval stack before building proprietary judgments.

8. **Juru: Legal Brazilian Large Language Model from Reputable Sources** — Roseval Malaquias Junior et al., 2024. [arXiv:2403.18140](https://arxiv.org/abs/2403.18140) — [BR-specific]
   Domain-pretrains Sabiá-2 on 1.9B tokens of reputable Brazilian legal sources and evaluates on Brazilian legal exams (OAB etc.): legal performance improves with little data, but general-domain ability degrades. Informs the build-vs-buy question for the model behind the research assistant, and its curation of "reputable" Brazilian legal text speaks to the OCR-noise and register challenges.

9. **JUÁ — A Benchmark for Information Retrieval in Brazilian Legal Text Collections** — Jayr Pereira et al., 2026. [arXiv:2604.06098](https://arxiv.org/abs/2604.06098) — [BR-specific]
   The first unified public benchmark for Brazilian legal IR (April 2026), spanning jurisprudence, legislative/regulatory, and question-driven search regimes, with shared protocols, leaderboard, and baselines including BM25, dense retrievers, and a domain-adapted Qwen embedding model; it builds on JurisTCU, Ulysses-RFCorpus, and BR-TaxQA-R. Its central finding — retrieval performance varies sharply across legal collection types — is precisely Jusbrasil's tribunal-heterogeneity problem, making this the natural shared yardstick for "similar jurisprudence."

### Read-first picks

- **Magesh et al. (arXiv:2405.20362)** — the empirical ceiling and failure taxonomy for exactly the product category Jus IA is in; arrive at the call knowing the 17%-hallucination result and that retrieval failures cause much of it.
- **JUÁ (arXiv:2604.06098)** — the freshest BR-specific artifact; asking whether Jusbrasil evaluates on or contributes to JUÁ is an immediate, concrete talking point.

### Residue

- **LegalSearchLM: Rethinking Legal Case Retrieval as Legal Elements Generation** ([arXiv:2505.23832](https://arxiv.org/abs/2505.23832)) — ID verified via arXiv link in search results, but first author/venue not confirmed in time; promising generative-retrieval angle for similar-case matching if the parent wants a 10th entry.
- **CaseLink / CaseGNN++** (IDs above, same group as CaseGNN) — verified but folded into entry 3 rather than given separate slots.
- No arXiv-verifiable COLIEE 2024/2025 overview paper surfaced (COLIEE summaries are usually in JURISIN/ICAIL proceedings, not arXiv); CaseGNN entry carries the COLIEE benchmark context instead.
- Did not find a public STF/STJ similar-jurisprudence dataset with qrels (RulingBR is summarization-oriented); JurisTCU + JUÁ are the closest substitutes.
- Questions worth asking Jusbrasil on the call: (1) How is "similar jurisprudence" relevance defined and annotated — does it decompose relevance like LeCaRDv2 (facts vs. thesis vs. outcome)? (2) Do they measure document-level retrieval mismatch (Reuter et al.) in their RAG pipeline? (3) Are they evaluating on JUÁ/JurisTCU or only on internal sets, and would they publish a benchmark from their corpus? (4) How do they exploit their own citation graph — anything like CaseGNN/CLERC-style citation-derived training data?

---

## L3 — Legal Summarization & Thesis Extraction

### Papers

1. **A Comprehensive Survey on Legal Summarization: Challenges and Future Directions** — Akter et al., 2025, arXiv. [General]
   [arXiv:2501.17830](https://arxiv.org/abs/2501.17830). Systematic review of 120+ transformer-era papers covering extractive/abstractive methods, datasets, and evaluation in legal summarization, with explicit treatment of informativeness vs. faithfulness. The single best map of the field for "smart summaries" — useful for benchmarking Jus IA's approach against the state of the art and for vocabulary alignment before the call.

2. **How Ready are Pre-trained Abstractive Models and LLMs for Legal Case Judgement Summarization?** — Deroy et al., 2023, LegalAIIA workshop. [General]
   [arXiv:2306.01248](https://arxiv.org/abs/2306.01248). Evaluates domain-specific abstractive models and general LLMs on court judgments and finds competitive ROUGE but frequent hallucinated/inconsistent content, recommending human-in-the-loop checking. Directly informs Jus IA's stated hallucination risk in "smart summaries" and argues for inconsistency audits beyond n-gram metrics.

3. **PublicHearingBR: A Brazilian Portuguese Dataset of Public Hearing Transcripts for Summarization of Long Documents** — Fernandes et al., 2024, arXiv. [BR-specific]
   [arXiv:2410.07495](https://arxiv.org/abs/2410.07495). Brazilian Portuguese long-document summarization corpus (legislative hearing transcripts paired with structured summaries) plus annotated Portuguese NLI data and a discussion of hallucination-aware evaluation of LLM summaries. Rare PT-BR resource hitting three Jus IA pain points at once: long documents, Portuguese legal/institutional register, and faithfulness evaluation — also adjacent to the audio-transcription-to-summary pipeline.

4. **Improving abstractive summarization of legal rulings through textual entailment** — Feijó & Moreira, 2023, Artificial Intelligence and Law. [BR-specific]
   [DOI: 10.1007/s10506-021-09305-4](https://link.springer.com/article/10.1007/s10506-021-09305-4). Generates "ementa"-style summaries of Brazilian Supreme Court rulings (RulingBR data) and uses textual entailment to score/select candidate summaries, reducing unfaithful output. The closest published analogue to Jus IA's "smart summaries" for acórdãos: same language, same document genre (ementa as gold summary), and an entailment-based faithfulness filter worth probing on the call.

5. **Multi-LexSum: Real-World Summaries of Civil Rights Lawsuits at Multiple Granularities** — Shen et al., 2022, NeurIPS Datasets & Benchmarks. [General]
   [arXiv:2206.10883](https://arxiv.org/abs/2206.10883). 9,280 expert-authored summaries over multi-document case files (often 200+ pages) at three granularities, from one-sentence to multi-paragraph. The reference benchmark for multi-document case-cluster summarization — the core technical shape of "main theses," which must compress many decisions into recurring short statements at controlled granularity.

6. **LegalSeg: Unlocking the Structure of Indian Legal Judgments Through Rhetorical Role Classification** — Nigam et al., 2025, arXiv. [General]
   [arXiv:2502.05836](https://arxiv.org/abs/2502.05836). Largest rhetorical-role dataset to date (7,000+ judgments, 1.4M sentences, 7 roles) with head-to-head evaluation of hierarchical BiLSTM-CRF, transformer, GNN, and role-aware architectures. Rhetorical segmentation (facts / arguments / ratio / ruling) is the standard pre-processing step that makes both "smart summaries" and thesis extraction tractable on very long judgments.

7. **Semantic Segmentation of Legal Documents via Rhetorical Roles** — Kalamkar et al., 2022, NLLP workshop @ EMNLP. [General] *(foundational)*
   [arXiv:2112.01836](https://arxiv.org/abs/2112.01836). Introduces the widely reused 13-role rhetorical scheme (facts, issue, precedent, ratio, ruling, etc.) and baseline segmenters. Foundational for holding/ratio decidendi localization: the "ratio" role is essentially the raw material from which "main theses" are distilled.

8. **Towards Argument-Aware Abstractive Summarization of Long Legal Opinions with Summary Reranking** — Elaraby, Zhong & Litman, 2023, Findings of ACL. [General]
   [arXiv:2306.00672](https://arxiv.org/abs/2306.00672). Uses argument-role structure to generate multiple candidate summaries of long legal opinions, then reranks by coverage of the document's argument structure. A concrete recipe for making long-judgment summaries argument-complete — relevant to keeping the winning thesis and its grounds in a "smart summary" rather than just outcome boilerplate.

9. **When Does Pretraining Help? Assessing Self-Supervised Learning for Law and the CaseHOLD Dataset** — Zheng et al., 2021, ICAIL. [General] *(foundational)*
   [arXiv:2104.08671](https://arxiv.org/abs/2104.08671). Introduces CaseHOLD (53k+ questions on identifying the correct holding of a cited case) and shows domain pretraining pays off precisely on legally hard tasks like holding identification. The canonical formulation of holding extraction as an NLP task — the per-case building block underneath "main theses" — and an argument for legal-domain pretraining in PT-BR.

10. **Large Legal Fictions: Profiling Legal Hallucinations in Large Language Models** — Dahl et al., 2024, Journal of Legal Analysis. [General]
    [arXiv:2401.01301](https://arxiv.org/abs/2401.01301). Large-scale empirical profiling of LLM hallucination rates on legal queries, including closed-domain settings such as summarizing judicial opinions. Gives Jusbrasil-relevant base rates and a taxonomy for the hallucination risk they flag across both the research assistant and summarization features.

### Read-first picks

- **Feijó & Moreira (DOI 10.1007/s10506-021-09305-4)** — the only paper that is literally Jus IA's task: ementa generation for Brazilian rulings with an entailment-based faithfulness mechanism.
- **Multi-LexSum (arXiv:2206.10883)** — the benchmark whose multi-document, multi-granularity setup most closely matches "main theses" extraction over case clusters.

### Residue

- **RulingBR original dataset paper** (de Vargas Feijó & Moreira, PROPOR 2018, ~10.6k STF decisions with ementa as gold summary): confirmed to exist via secondary sources but no standalone arXiv ID or DOI verified — cite via the 2023 AI & Law paper (#4) which uses it.
- Found **no published work specifically on Brazilian "temas repetitivos"/tese jurídica extraction** (STJ repetitive-theme statements as supervision for thesis extraction) — a real gap and a strong call question: does Jusbrasil train "principais teses" against STJ/STF tema-repetitivo statements as silver labels?
- No PT-BR rhetorical-role-labeled judgment corpus surfaced (LegalSeg-style resources are Indian/English); worth asking whether Jusbrasil segments acórdãos (relatório/voto/dispositivo) with rules or learned models.
- Queries for "long-document transformer + Portuguese legal summarization" returned retrieval datasets instead (JurisTCU [arXiv:2503.08379](https://arxiv.org/abs/2503.08379), JUÁ) — relevant to the similar-jurisprudence lane, not L3; flagged for the synthesizer to avoid a coverage gap.
- Open question for the call: how is faithfulness of ementa-style summaries evaluated at scale — entailment/NLI (as in #3, #4), citation grounding, or human review sampling?

---

## L4 — Legal NER, Extraction & Document Structure

### Papers

1. **LeNER-Br: A Dataset for Named Entity Recognition in Brazilian Legal Text** — Luz de Araujo et al., 2018, PROPOR (Springer LNCS). DOI: [10.1007/978-3-319-99722-3_32](https://doi.org/10.1007/978-3-319-99722-3_32) · [project page](https://teodecampos.github.io/LeNER-Br/) — [BR-specific]
   The foundational Brazilian legal NER dataset: court documents annotated for PERSON/LOCATION/TIME/ORG plus legal-specific LEGISLATION and JURISPRUDENCE tags, with LSTM-CRF baselines (F1 ~97% legislation, ~89% legal cases). The de facto benchmark any Jus IA entity-extraction stage will be compared against; its tag set (law vs. case citations as first-class entities) maps directly onto citation linking in a legal research product.

2. **UlyssesLegalNER-Br: from Legislative to Legal, a comprehensive corpus of Brazilian legal documents for NER** — Albuquerque et al., 2026, PROPOR 2026. [ACL Anthology: 2026.propor-1.33](https://aclanthology.org/2026.propor-1.33/) — [BR-specific]
   The most current successor to LeNER-Br/UlyssesNER-Br: 560 public documents spanning bills, case law, and statutes, 9 categories / 23 fine-grained entity types, with CRF, BiLSTM, and BERTimbau baselines (best micro-F1 96.18). Directly informs the NER/entity-normalization stage with a modern, fine-grained Brazilian schema covering both legislative and judicial registers. Companion resources at [github.com/ulysses-camara/ulysses-ner-br](https://github.com/ulysses-camara/ulysses-ner-br).

3. **VICTOR: a Dataset for Brazilian Legal Documents Classification** — Luz de Araujo et al., 2020, LREC. [ACL Anthology: 2020.lrec-1.181](https://aclanthology.org/2020.lrec-1.181/) — [BR-specific]
   The STF (Supreme Court) corpus: ~692k documents / 4.6M pages from 45k appeals, labeled for document-type classification and multilabel theme assignment. The canonical resource for the "split an OCR'd case bundle into its constituent piece types" stage — the precondition for any downstream summarization or extraction over PJe-style filings. Its scale and noise profile mirror Jusbrasil's production data better than any clean academic corpus.

4. **Sequence-aware Multimodal Page Classification of Brazilian Legal Documents** — Luz de Araujo et al., 2022, IJDAR. [arXiv:2207.00748](https://arxiv.org/abs/2207.00748) — [BR-specific]
   Follow-on to VICTOR: 6,510 lawsuits / 339k pages, fusing ResNet image features with CNN-over-OCR text features, plus biLSTM-CRF over the page sequence, with learned embeddings for missing modalities. The closest published blueprint to a document segmentation/zoning stage for scanned Brazilian court bundles — multimodal + sequence modeling beats text-only or vision-only when pages arrive in case order. Strong talking point on handling OCR-noisy PJe PDFs.

5. **Sequence-to-Sequence Models for Extracting Information from Registration and Legal Documents** — Pires et al., 2022 (NeuralMind), DAS/ICDAR workshop. [arXiv:2201.05658](https://arxiv.org/abs/2201.05658) — [BR-specific]
   Generative (seq2seq) extraction from Brazilian registration and legal documents that emits structured output directly, replacing token-classification + post-processing rules, and includes an output-to-source alignment method for auditability. An early template for the now-dominant "LLM emits JSON, then ground spans for citation" pattern — the auditability trick is directly relevant to a lawyer-facing product that must show provenance.

6. **verBERT: Automating Brazilian Case Law Document Multi-label Categorization Using BERT** — Serras & Finger, 2022. [arXiv:2203.06224](https://arxiv.org/abs/2203.06224) — [BR-specific]
   Uses the Kollemata corpus (~24k Brazilian property-law jurisprudence documents) to fine-tune multi-class/multi-label BERT models, +30 F1 points over statistical baselines. Informs the jurisprudence-organization stage (Jus IA's thematic clustering of case law) and is the citable entry point to the Kollemata resource.

7. **LayoutLM: Pre-training of Text and Layout for Document Image Understanding** — Xu et al., 2020, KDD. [arXiv:1912.13318](https://arxiv.org/abs/1912.13318) — [General]
   The foundational layout-aware pretraining paper: joint modeling of token text and 2D position over scanned documents, root of the LayoutLMv2/v3 family widely applied to government and legal forms. Grounds the discussion of whether Jusbrasil should run layout-aware encoders on PJe scans (headers, stamps, signature blocks, tables) instead of treating OCR output as flat text.

8. **LegalSeg: Unlocking the Structure of Indian Legal Judgments Through Rhetorical Role Classification** — Nigam et al., 2025. [arXiv:2502.05836](https://arxiv.org/abs/2502.05836) — [General]
   Largest rhetorical-role-labeled judgment corpus (Indian courts, 7k+ documents), benchmarking hierarchical encoders, GNNs, and LLMs for sentence-level segmentation into Facts/Arguments/Reasoning/Ruling etc. Rhetorical zoning is the structural prerequisite for faithful long-document summarization; the method transfers to acórdãos/sentenças. Pair with [arXiv:2302.06448](https://arxiv.org/abs/2302.06448) (joint span segmentation + role labeling) for the modeling-choice angle.

9. **OCR Error Post-Correction with LLMs in Historical Documents: No Free Lunches** — Kanerva et al., 2025, RESOURCEFUL. [arXiv:2502.01205](https://arxiv.org/abs/2502.01205) — [General]
   Systematic study of open-weight LLMs for OCR post-correction: clear CER reductions in English but failure to reach practical utility in Finnish (lower-resource morphology — a cautionary analogue for Portuguese legal register). Informs the OCR post-correction stage decision: clean text before NER/extraction, or train extractors to be noise-robust. See also [arXiv:2504.00414](https://arxiv.org/abs/2504.00414) (multimodal LLMs doing OCR + correction + NER end-to-end).

10. **CitaLaw: Enhancing LLM with Citations in Legal Domain** — Zhang et al., 2024. [arXiv:2412.14556](https://arxiv.org/abs/2412.14556) — [General]
    Benchmark for citation-grounded legal LLM answering: legal questions paired with a statute/precedent reference corpus and a syllogism-inspired metric checking that cited law actually supports the generated answer. Informs the citation extraction/normalization and answer-grounding stage of Jus IA — hallucinated citations are the top product risk for a lawyer-facing assistant.

### Read-first picks

- **#2 UlyssesLegalNER-Br (2026)** — the current state of the art and schema for Brazilian legal NER; one paper that summarizes the whole LeNER-Br lineage with quotable BERTimbau baselines.
- **#4 Sequence-aware multimodal page classification (2022)** — the single closest match to Jusbrasil's stated pain (OCR-noisy, scanned, multi-document case bundles) and a concrete architecture to react to.

### Residue

- **LGPD Benchmark (pseudonymization eval for PT-BR legal text)** — found only on ResearchGate, no verifiable arXiv/DOI; likely STIL/BRACIS 2025. Worth locating before citing.
- **LegNER (PMC12631292)** — exists on PubMed Central but language/jurisdiction not confirmed as Portuguese; left out rather than mis-tag.
- No dedicated arXiv paper on **Brazilian legal citation normalization** — the practical standard is the LexML URN scheme (lexml.gov.br), infrastructure rather than a paper. Ask Jusbrasil: do they normalize citations to LexML URNs, and how do they resolve OCR-corrupted citation strings?
- No published work applying **LayoutLM-family models to Brazilian tribunals** specifically — the VICTOR multimodal line (#4) is the nearest. Call question: did Jusbrasil try layout-aware encoders on PJe scans, or OCR-text-only plus noise-robust fine-tuning?
- RulingBR exists but no stable arXiv/DOI verified this session; it is summarization-lane material.
- Open question for the call: how do they handle **LGPD-mandated anonymization at scale** (segredo de justiça cases) — NER-based redaction recall targets, and whether pseudonymization survives OCR noise.

---

## L5 — Evaluation, Benchmarks & Hallucination

### Papers

1. **Large Legal Fictions: Profiling Legal Hallucinations in Large Language Models** — Dahl et al. (Dahl, Magesh, Suzgun, Ho), 2024, *Journal of Legal Analysis* — [arXiv:2401.01301](https://arxiv.org/abs/2401.01301) — [General]
   Stanford RegLab study showing hallucination rates of 58–88% on verifiable questions about US federal case law, with a reusable typology of legal hallucinations (existence, holding, citation, etc.) and evidence that models fail to push back on false legal premises in user questions. Directly frames Jus IA's core product risk; the contra-factual probing methodology is replicable on Brazilian tribunal data.

2. **Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools** — Magesh et al., 2024, *Journal of Empirical Legal Studies* 2025 — [arXiv:2405.20362](https://arxiv.org/abs/2405.20362) — [General]
   First empirical audit of commercial RAG-based legal research products (Lexis+ AI, Westlaw AI-AR): 17–33% hallucination rates despite retrieval grounding, with a preregistered query set and a typology distinguishing groundedness from correctness. The closest published analogue to evaluating Jus IA itself; "misgrounded" citations (real case, wrong proposition) are the hardest failure mode to catch. A template for an internal Jusbrasil audit protocol.

3. **LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models** — Guha et al., 2023, NeurIPS 2023 Datasets & Benchmarks — [arXiv:2308.11462](https://arxiv.org/abs/2308.11462) — [General]
   162 expert-crafted tasks across six types of legal reasoning, built with practicing lawyers. The de facto standard for legal-reasoning evaluation and the methodological reference for building a Brazilian-law equivalent; rule-recall tasks are the family most predictive of hallucinated legal claims.

4. **LawBench: Benchmarking Legal Knowledge of Large Language Models** — Fei et al., 2023 — [arXiv:2309.16289](https://arxiv.org/abs/2309.16289) — [General]
   20 tasks over a civil-law (Chinese) system organized by cognitive level: memorization, understanding, application; evaluated on 51 LLMs. More relevant to Brazil than US-centric benchmarks because it structures evaluation for a codified civil-law jurisdiction (statute recall vs. application), mapping better to Brazilian códigos and súmulas than common-law issue-spotting.

5. **CLERC: A Dataset for Legal Case Retrieval and Retrieval-Augmented Analysis Generation** — Hou et al., 2024, NAACL 2025 — [arXiv:2406.17186](https://arxiv.org/abs/2406.17186) — [General]
   Large-scale benchmark (1.84M cases, 20.7M citations) for citation retrieval and retrieval-grounded analysis generation; GPT-4o scores highest on ROUGE while hallucinating the most. Demonstrates that surface-quality metrics anti-correlate with citation faithfulness — Jusbrasil needs citation-level factuality metrics, not fluency metrics.

6. **A Reasoning-Focused Legal Retrieval Benchmark** — Zheng et al., 2025, ACM CS&Law 2025 ([DOI 10.1145/3709025.3712219](https://dl.acm.org/doi/10.1145/3709025.3712219)) — [arXiv:2505.03970](https://arxiv.org/abs/2505.03970) — [General]
   Introduces Bar Exam QA and Housing Statute QA, retrieval benchmarks where the relevant passage requires legal reasoning to identify, not just lexical match — current retrievers degrade sharply there. Hallucination upstream-causes often live in retrieval; this gives a way to measure retrieval quality on reasoning-heavy legal queries.

7. **Automatic Legal Writing Evaluation of LLMs (oab-bench)** — Pires et al. (Pires, Malaquias Junior, Nogueira), 2025 — [arXiv:2504.21202](https://arxiv.org/abs/2504.21202) — [BR-specific]
   Builds oab-bench from the Brazilian Bar Exam (OAB) second phase: 105 essay/procedural-document questions across seven areas of law, graded by an LLM judge against official OAB correction criteria, with validation that judge scores correlate strongly with human examiner grades. A ready-made Brazilian legal evaluation set plus evidence on when LLM-as-judge is reliable for Portuguese legal text.

8. **Juru: Legal Brazilian Large Language Model from Reputable Sources** — Malaquias Junior et al., 2024 — [arXiv:2403.18140](https://arxiv.org/abs/2403.18140) — [BR-specific]
   Domain-specializes Mistral-7B on 1.9B tokens of curated Brazilian legal sources; evaluates on OAB 2023 and ENADE, finding legal gains but degradation on general knowledge. The main published precedent for Brazilian legal-domain LLM evaluation, and a caution: domain specialization shifts, rather than removes, the reliability problem.

9. **BLUEX: A Benchmark based on Brazilian Leading Universities Entrance eXams** — Almeida et al., 2023, BRACIS 2023 — [arXiv:2307.05410](https://arxiv.org/abs/2307.05410) — [BR-specific]
   Portuguese-language benchmark from UNICAMP/USP entrance exams (1,260 questions, 2018–2024) with contamination-aware recent-exam splits. Useful for the general-capability and Portuguese-fluency axis of a Jus IA eval matrix; its contamination-control design matters because OAB questions are widely scraped into training data.

10. **Know Your Limits: A Survey of Abstention in Large Language Models** — Wen et al., 2024, TACL 2025 ([DOI 10.1162/tacl_a_00754](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00754/131566)) — [arXiv:2407.18418](https://arxiv.org/abs/2407.18418) — [General]
    Survey organizing abstention ("I don't know" / refusal under uncertainty) across query, model, and human-values perspectives, covering calibration-based methods and abstention evaluation. For a high-stakes product serving lawyers, the right behavior when retrieval is thin is abstention, not generation — the entry point for designing Jus IA's refuse/hedge policy.

### Read-first picks

- **Magesh et al. (arXiv:2405.20362)** — the single most product-relevant paper: audits exactly Jus IA's category, quantifies residual hallucination, supplies a reusable audit typology.
- **Pires et al., oab-bench (arXiv:2504.21202)** — the strongest BR-specific asset: a Brazilian legal benchmark plus validated LLM-as-judge methodology adoptable nearly off the shelf.

### Residue

- **COLIEE**: no single canonical arXiv paper; annual summaries live in Springer *Review of Socionetwork Strategies* / JURISIN proceedings. Cite via competition site if needed; its entailment tasks are the classic format for citation-claim verification.
- **"LegalBench-BR"** surfaced only as a ResearchGate entry without verifiable arXiv/DOI — excluded. **"Rabula"** (CEUR-WS Vol-4089) not verified to a stable identifier; both worth a follow-up check.
- No dedicated, verified paper on *citation-faithfulness verification for Brazilian jurisprudence* (STJ/STF súmula-level grounding) — apparent literature gap.
- **Call questions:** Do they run a Magesh-style preregistered hallucination audit on Jus IA, and what is their measured misgrounded-citation rate? Do they distinguish retrieval failure from generation failure in error attribution? What is the abstention policy when retrieval confidence is low? Have they checked OAB-question contamination in base models?

---

## L7 — Next-Product Opportunities

### Clusters and papers

#### 1. Judicial outcome prediction / case duration & settlement estimation
**Candidate product:** A "Probabilidade de Êxito" widget inside Jus IA that, given a case profile (court, class, subject, parties' briefs), returns calibrated win-probability and expected time-to-disposition bands, trained on Brazilian appellate corpora.

1. **Predicting Brazilian Court Decisions** — Lage-Freitas et al., 2022, PeerJ Computer Science — [arXiv:1905.10348](https://arxiv.org/abs/1905.10348) / [DOI 10.7717/peerj-cs.904](https://peerj.com/articles/cs-904.pdf) — [BR-specific]
   Predicts outcomes (favorable/unfavorable/partial) of Tribunal de Justiça de Alagoas appeals with ~80% F1 from decision text. Proof that outcome prediction works on ordinary Brazilian state-court data — exactly the corpus class Jusbrasil indexes at national scale; the label taxonomy (including "partially favorable") maps directly onto a product-grade prediction API.

2. **Using deep learning to predict outcomes of legal appeals better than human experts: A study with data from Brazilian federal courts** — de Menezes-Neto et al., 2022, PLOS ONE — [DOI 10.1371/journal.pone.0272287](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0272287) — [BR-specific]
   ULMFiT/BERT/BigBird trained on 612,961 Juizados Especiais Federais appeals (TRF5), beating human-expert predictions ~3x. The strongest published evidence that Brazilian outcome prediction exceeds practitioner intuition at volume — a citable anchor for an "appeal or settle?" recommendation feature.

3. **Rethinking Legal Judgement Prediction in a Realistic Scenario in the Era of Large Language Models** — Nigam et al., 2024, NLLP Workshop @ EMNLP 2024 — [arXiv:2410.10542](https://arxiv.org/abs/2410.10542) — [General]
   Evaluates LJP using only information available *at filing time* (not the leaked final-decision text most benchmarks use). Cautionary methodology paper: any Jusbrasil prediction product must be evaluated this way or it will overpromise.

4. **Investigation of lawsuit process duration using machine learning and process mining** — Verçosa et al., 2024, Discover Analytics — [DOI 10.1007/s44257-024-00015-0](https://link.springer.com/article/10.1007/s44257-024-00015-0) — [BR-specific]
   Combines process-mining clustering of procedural movement logs with regression on 60k+ Brazilian labor-court cases to predict total duration. The movimentações-based feature engineering matches Jusbrasil's processo-tracking data exactly — directly reusable for a case-duration estimator.

#### 2. Petition and legal-document drafting assistance
**Candidate product:** A petição-inicial/contestação drafting copilot that fills firm-approved templates section-by-section via multi-agent retrieval over the client's facts plus Jusbrasil's jurisprudence index, with citation verification before insertion.

5. **LLM Based Multi-Agent Generation of Semi-structured Documents from Semantic Templates in the Public Administration Domain** — Musumeci et al., 2024 (AI4PA / HCII 2024) — [arXiv:2402.14871](https://arxiv.org/abs/2402.14871) — [General]
   Multi-agent pipeline decomposes a semantic template, retrieves per-section content, and generates iteratively to curb hallucination in bureaucratic documents. The template+LLM hybrid is the right architecture for Brazilian petitions, which are heavily structured (qualificação, fatos, direito, pedidos).

6. **Juru: Legal Brazilian Large Language Model from Reputable Sources** — Malaquias Junior et al., 2024 — [arXiv:2403.18140](https://arxiv.org/abs/2403.18140) — [BR-specific]
   Continued pretraining of Mistral-7B on 1.9B tokens of reputable Brazilian legal text improves legal-benchmark performance cheaply (at some general-knowledge cost). Evidence that a small domain-specialized PT-BR legal model is feasible — relevant to fine-tune-vs-frontier-API for drafting.

#### 3. Contract review and clause risk analysis
**Candidate product:** A contract-review module ("Jus IA Contratos") that flags risky clauses (multa, rescisão, foro, não-concorrência) against LGPD/CDC/Civil Code norms, with side-by-side market-standard clause suggestions.

7. **CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review** — Hendrycks et al., 2021, NeurIPS 2021 Datasets & Benchmarks — [arXiv:2103.06268](https://arxiv.org/abs/2103.06268) — [General]
   510 contracts, 13k expert annotations across 41 clause categories lawyers check in review. The canonical task definition; a Portuguese-language CUAD analogue built from Brazilian contracts would be both a product moat and a publishable asset.

8. **ContractEval: Benchmarking LLMs for Clause-Level Legal Risk Identification in Commercial Contracts** — Liu et al., 2025, NLLP Workshop @ EMNLP 2025 — [arXiv:2508.03080](https://arxiv.org/abs/2508.03080) / [ACL Anthology 2025.nllp-1.19](https://aclanthology.org/2025.nllp-1.19/) — [General]
   Benchmarks 19 LLMs on CUAD clause-risk identification; most perform at "junior legal assistant" level, open-source models need fine-tuning, and reasoning mode can hurt correctness. Useful for model-selection and expectation-setting on a contract product.

#### 4. Agentic legal workflows
**Candidate product:** A "Jus IA Agente" that executes multi-step jobs — monitor a process, pull movimentações via DataJud API, retrieve precedents, draft the responsive filing, and assemble a partner-review packet — with intermediate-step auditing.

9. **LegalAgentBench: Evaluating LLM Agents in Legal Domain** — Li et al., 2024, ACL 2025 — [arXiv:2412.17259](https://arxiv.org/abs/2412.17259) — [General]
   300 annotated multi-step legal tasks over 17 corpora with 37 external-knowledge tools, scoring agents on intermediate "process rate," not just final answers. The closest existing blueprint for evaluating a tool-using legal agent over Jusbrasil's own retrieval/process APIs; process-rate is how you make agent quality auditable for OAB-conscious customers.

#### 5. Multimodal: hearings, audio, ASR for PT-BR legal speech
**Candidate product:** Extend the existing meeting-transcription feature into a hearing/deposition product: diarized transcription of audiências (routinely recorded on video per CNJ digital-justice norms), witness-by-witness summaries, and contradiction flags against the case file.

10. **CORAA: a large corpus of spontaneous and prepared speech manually validated for speech recognition in Brazilian Portuguese** — Candido Junior et al., 2021 (journal version: Language Resources and Evaluation, 2022) — [arXiv:2110.15731](https://arxiv.org/abs/2110.15731) / [DOI 10.1007/s10579-022-09621-4](https://link.springer.com/article/10.1007/s10579-022-09621-4) — [BR-specific]
    290+ hours of validated PT-BR speech, heavy on spontaneous/accented speech, with Wav2Vec 2.0 baselines (WER 24% spontaneous). Spontaneous-speech WER is the binding constraint for courtroom audio; CORAA is the fine-tuning/eval substrate for a legal-domain PT-BR ASR layer on top of Whisper-class models.

#### 6. Litigation analytics at scale
**Candidate product:** A "Jurimetria" analytics suite — judge/court/vara-level grant rates, duration distributions, and opposing-counsel track records — built by joining Jusbrasil's full-text archive with CNJ DataJud's standardized national metadata.

11. **National Brazilian judicial database (DataJud): transparency and better administration of justice** — Rocha et al., 2023, ICEGOV 2023 — [DOI 10.1145/3614321.3614381](https://dl.acm.org/doi/10.1145/3614321.3614381) — [BR-specific]
    Describes how all Brazilian courts mandatorily feed standardized XML case data into DataJud since 2020, the CNJ governance around it, and its use for judicial indicators. The authoritative description of the open-data substrate any litigation-analytics product would join against — worth citing when discussing data rights and coverage.

12. **Document classification using a Bi-LSTM to unclog Brazil's supreme court** — Braz et al., 2018, NeurIPS 2018 ML4D Workshop (Project VICTOR, UnB/STF) — [arXiv:1811.11569](https://arxiv.org/abs/1811.11569) — [BR-specific]
    The STF's VICTOR project: neural classification of supreme-court case documents (tema de repercussão geral routing) at scale. Brazilian courts themselves run ML triage pipelines — a private-sector analytics product can position as the lawyer-side mirror of what tribunals already do internally.

### Read-first picks
- **de Menezes-Neto et al. 2022 (PLOS ONE)** — the single best evidence that outcome prediction on Brazilian court data beats human experts at 600k-case scale; sets the ceiling and credibility story for the most differentiated next product.
- **LegalAgentBench (arXiv:2412.17259)** — if the call turns to "what's after chat," this defines how to build and *measure* a tool-using legal agent.

### Residue
- **Failed/weak queries:** No arXiv-indexed paper found specifically on *settlement-value* (valor de acordo/indenização) prediction for Brazil; no paper on *deposition/hearing summarization* as an NLP task for PT-BR — the cluster-5 product rests on CORAA + general meeting-summarization literature.
- **Unverified candidates excluded:** "Transforming Justice: The Rise of AI in Brazilian Courts" (DGO 2025) — no clean DOI confirmed; "MASLegalBench" (arXiv 2509.24922) and "LLM Agents in Law" survey (arXiv 2601.06216) surfaced but not individually verified.
- **Questions worth asking Jusbrasil:** (1) Do they already join full-text archives with DataJud metadata, and what are the licensing limits on commercializing DataJud-derived judge analytics given CNJ Resolution 331 and LGPD? (2) For outcome prediction, would they ship calibrated probabilities given OAB advertising/ethics constraints? (3) Is hearing audio/video accessible at scale, or only to case parties? (4) Build-vs-buy on a PT-BR legal LLM: does Juru-style continued pretraining beat frontier-API prompting on their internal evals?
