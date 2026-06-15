# LEARNING-PACK.md — RoBERTaLexPT

Deliverable for the Jusbrasil ("Jus IA") call. Source-backed claims, an operator
model, dedup takeaways, 5 things to say, and an honest cutoff.
Date checked: **2026-06-10**. Labels: [PRIMARY] / [CORROBORATED] / [READING] / [OPEN].

---

## 1. Source-backed claims (the spine, with numbers)

- **What it is.** RoBERTaLexPT-base: a Portuguese **legal** RoBERTa-base encoder,
  MLM-pretrained **from scratch** on a deduplicated legal+general corpus mix,
  released under CC BY 4.0. [PRIMARY]
- **Corpora.** LegalPT (legal) = **125.1 GiB / 22.5B tokens** from 6 sources;
  CrawlPT (general web) = **163.2 GiB / 29.2B tokens** from brWaC + CC100-PT +
  OSCAR-PT. [PRIMARY]
- **Dedup.** MinHash + LSH, **5-grams, signature 256, Jaccard > 0.7**, via
  `text-dedup`. Motivated by heavy boilerplate duplication in legal text. [PRIMARY/CORROBORATED]
- **Benchmark.** PortuLex = 4 legal tasks (LeNER-Br, UlyssesNER-Br, FGV-STF NER;
  RRI classification). [PRIMARY]
- **Result.** **85.41 average macro-F1**, beating Albertina-PT-BR-xlarge (85.08),
  BERTimbau-large (84.60), Legal-RoBERTa-PT-large (84.02), BERTimbau-base
  (83.78). A **base-size** model beats **larger** models. [PRIMARY]
- **Key finding.** Pretraining on **legal + general** data beats **legal-only**
  for legal tasks. [CORROBORATED]

## 2. Operator model (how to think about it)

Think of it as a **two-knob recipe** for a domain encoder:
- **Knob 1 — corpus hygiene (dedup).** Legal corpora are dominated by repeated
  boilerplate; without dedup the model wastes capacity memorizing templates.
  MinHash/LSH collapses near-duplicates so the model learns signal, not echoes.
- **Knob 2 — domain mix.** Legal-only narrows the model; adding general web text
  keeps language breadth while the legal data sharpens domain terms. The mix wins.

The punchline: **turning these two knobs lets a small (base) model beat big
generic models on legal tasks.** Data beats size, in this regime.

## 3. Dedup takeaways (the Jusbrasil-relevant core) — [READING over PRIMARY method]

- Dedup is presented as **decisive**, not cosmetic — it is the paper's headline
  intervention against redundancy.
- The exact params are reusable as a default: **5-grams, 256-sig, Jaccard 0.7.**
- This maps directly onto Jusbrasil's **"millions of redundant judicial
  documents"**: repeated *ementas*, citation strings, and templated decisions are
  exactly the boilerplate MinHash/LSH targets.
- Implication for the **encoder/foundation layer**: dedup the corpus first, then
  pretrain/represent — cleaner embeddings for **similar-jurisprudence retrieval**
  and classification. (Retrieval itself is a [READING]; paper evaluates NER/clf.)

## 4. Five things to bring to the call

1. **"Data hygiene beats model size here."** A deduplicated legal+general
   base-size RoBERTa (85.41 macro-F1) beat larger generic models — relevant when
   weighing GPU spend vs corpus curation for Jus IA. [PRIMARY]
2. **A ready dedup recipe for our redundancy problem.** MinHash/LSH, 5-grams,
   sig 256, Jaccard 0.7 — directly applicable to repeated ementas/citations. [PRIMARY]
3. **Open, CC-BY artifacts to bootstrap with.** Model, LegalPT/CrawlPT (+dedup),
   and the PortuLex benchmark are all public — usable as a starting encoder and
   an eval harness rather than building from zero. [PRIMARY]
4. **The mix question is settled for legal tasks.** Legal+general > legal-only —
   shapes our pretraining/continued-pretraining recipe. (Exact ratio is open.) [CORROBORATED/OPEN]
5. **Scope honestly.** This is a Brazilian/PT **legal NER + classification**
   encoder at base scale — strong evidence for representation quality, not a
   generative model and not a measured retrieval system. Don't oversell. [READING]

## 5. Honest cutoff (what this pack does NOT establish)

- **Magnitude of dedup's effect** — how much was removed / the size-reduction
  ratio and the ablation delta from dedup — **[OPEN]**: not in the artifacts we
  fetched; the PDF body wasn't machine-readable here. See `open-residue.md`.
- **Exact legal:general token ratio** in the final training mix — **[OPEN]**.
- **Per-task F1 breakdown** (vs the 85.41 average) — **[OPEN]**.
- **Verbatim abstract** — not captured (mirrors blocked/redirected) — **[OPEN]**.
- **Retrieval performance** — the paper does not evaluate retrieval; the
  "similar-jurisprudence retrieval" framing is our reading, not a measured claim.
- All Jusbrasil mappings here are **[READING]**, kept separate from source claims
  per `bridge-decisions.md`.

Sources (checked 2026-06-10): ACL Anthology landing/PDF
(aclanthology.org/2024.propor-1.38), HuggingFace model + dataset cards
(eduagarcia/*), GitHub eduagarcia/roberta-legal-portuguese.
