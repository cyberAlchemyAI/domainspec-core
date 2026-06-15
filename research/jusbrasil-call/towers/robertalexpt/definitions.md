# definitions.md — Governed Definitions

Governed = precise, source-anchored definitions of the **load-bearing** concepts.
Each definition states its scope and its source-kind. These are the terms whose
exact meaning the rest of the tower depends on.

---

## D1. LegalPT (corpus)

**Definition.** The Portuguese-language **legal** pretraining corpus introduced by
Garcia et al. (2024), formed by aggregating six legal sources and deduplicating
them. Measured at **125.1 GiB / ~22.5B tokens** (raw aggregate).
**Constituents.** MultiLegalPile-PT, Ulysses-Tesemõ, ParlamentoPT, Iudicium
Textum (STF), Acórdãos TCU, DataSTF (STJ).
**Scope.** Refers to the aggregate corpus; the deduplicated artifact is
`LegalPT_dedup`. **Source-kind:** [PRIMARY] (dataset card + repo).

## D2. CrawlPT (corpus)

**Definition.** The **general-domain** Portuguese web corpus assembled as the
non-legal half of the pretraining data: brWaC + CC100-PT + OSCAR-2301-PT,
**163.2 GiB / ~29.2B tokens**, with a deduplicated artifact `CrawlPT_dedup`.
**Role.** Supplies the "general" in the legal+general pretraining mix.
**Source-kind:** [PRIMARY] (repo).

## D3. PortuLex (benchmark)

**Definition.** A **four-task legal evaluation benchmark** for Portuguese,
introduced alongside the model, reported as **average macro-F1** across:
LeNER-Br (NER), UlyssesNER-Br (NER), FGV-STF (NER), RRI (classification).
**Use.** The yardstick on which RoBERTaLexPT scores 85.41.
**Source-kind:** [PRIMARY] (repo + model card).

## D4. MinHash + LSH deduplication (method)

**Definition.** A near-duplicate removal pipeline that (a) represents each
document by a MinHash **signature of size 256** over its **5-grams**, (b) uses
**LSH** to bucket candidate near-duplicates efficiently, and (c) **collapses any
document pair whose estimated Jaccard similarity exceeds 0.7** into one.
**Implementation.** `text-dedup` library.
**Why load-bearing.** It is the paper's decisive intervention: legal corpora are
boilerplate-heavy, so dedup changes what the model actually learns from.
**Source-kind:** [PRIMARY] for parameters; magnitude of effect is [OPEN] (see B4).

## D5. Legal+general pretraining mix (recipe / finding)

**Definition.** Pretraining a single encoder on **both** the legal corpus
(LegalPT) and the general corpus (CrawlPT), rather than legal-only.
**Governed finding.** For legal downstream tasks, the **mixed** pretraining
yields a more effective model than legal-only, and the resulting base-size model
**outperforms larger generic models**.
**Caveat.** The exact legal:general token ratio in the final training set is
**[OPEN]** (not in fetched artifacts). Do not cite a ratio.
**Source-kind:** [CORROBORATED] for the finding; ratio [OPEN].

## D6. RoBERTaLexPT-base (the model)

**Definition.** A **RoBERTa-base** encoder, MLM-pretrained **from scratch** on
the deduplicated LegalPT+CrawlPT mix (62.5k steps, batch 2048, LR 4e-4, seq 512,
15% masking, AdamW), released under **CC BY 4.0**.
**Headline result.** 85.41 average macro-F1 on PortuLex, beating larger generic
and prior legal Portuguese models.
**Source-kind:** [PRIMARY] (model card).
