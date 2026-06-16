# LEARNING-PACK.md — Juru, Read for the Jusbrasil Call

**Lane:** `juru-legal-llm` · **Paper:** arXiv 2403.18140 (2024) · **Date checked:** 2026-06-10
**Frame:** foundation-model layer / build-vs-buy.

---

## 1. What the paper actually did (source-backed)

- Took **Mistral-7B** and **continued pretraining** it on **1.9B unique tokens** of reputable
  Brazilian legal text. [primary-source: abstract]
- Corpus = academic legal papers (~1.805B tokens) + LexML federal statutes (~60.4M) + STF
  Supreme Court decisions (~133.3M; 32,535 docs). ~90% is academic by volume.
  [primary-source: HTML body]
- Trained ~4 epochs, ~7.96B tokens processed, ~3.35×10²⁰ FLOPs. [primary-source: HTML body]
- Evaluated **few-shot** on legal exams (OAB-2023/2024, ENAM-2024) and general-knowledge suites
  (Brazilian exams in PT; MMLU in EN). [primary-source: abstract + HTML]

## 2. The result, in one line (source-backed)

> Legal benchmarks went **up** (mean 44.5% -> 49.2%, ~+4.7 pts) and general knowledge went
> **down** in both Portuguese (~50.5 -> 48.1) and English (~61.6 -> 58.0) — measured
> **catastrophic forgetting**. [primary-source: abstract = direction; HTML tables = the
> numbers, mean-level high confidence, per-benchmark decimals lower confidence]

## 3. Operator model (how to think about it)

**Specialization is redistribution, not addition.** Continued pretraining is a *weight-mutating*
operation: it moves model capacity toward the domain and away from everything else. A
continue-pretrained legal base is a **narrow-band amplifier** — louder in law, quieter in
general. That is the whole build-vs-buy story in one image.

## 4. Build-vs-buy takeaways for the foundation-model layer

1. **CPT works — and it is feasible at modest scale.** ~1.9B reputable tokens on a 7B base
   produced real legal gains. The in-house lane is technically viable. [borrow-carefully]
2. **CPT is not free.** You are *choosing to forget* general ability. For a single base model
   serving mixed traffic, that is a real product risk. [BD1/BD7]
3. **Reputable curation transfers; Juru's exact mix may not.** Jusbrasil owns superior legal
   corpora, but Juru's ~90%-academic blend is provenance-good, not query-representative. Re-weight
   toward real Jus IA traffic before assuming transfer. [BD2]
4. **Benchmark gain ≠ product readiness.** OAB/ENAM accuracy is a proxy; citation correctness,
   hallucination, and drafting quality are unmeasured here. [BD5 / block]
5. **Default lean for mixed traffic: RAG over a frontier model and/or a router**, reserving CPT
   for law-pure, cost/latency/data-sovereignty-bound workloads. Juru proves CPT is *possible*,
   not that it is the *default*. [BD7 / operator-reading]

## 5. Five things to say on the call

1. "Juru is the keystone Brazilian legal-LLM paper — continue-pretrain Mistral-7B on ~1.9B
   reputable legal tokens, with measured OAB/ENAM gains."
2. "But it documents **catastrophic forgetting** — general knowledge drops ~2–4 points in both
   PT and EN. Specialization is a choice to forget."
3. "So the foundation-model decision isn't 'is a legal model good?' — it's 'can we afford a base
   model that's worse at everything non-legal?'"
4. "For Jus IA's mixed traffic, that argues for **RAG-over-frontier or a router**, not one
   specialized base — unless a workload is law-pure and cost/sovereignty-bound."
5. "Juru's value to us is as **evidence the in-house CPT lane is feasible**, plus a corpus-quality
   playbook (academic + LexML + STF) — not as a recipe to copy verbatim."

## 6. Honest cutoff

- Numbers are from the arXiv **abstract** (verbatim, high confidence) and **HTML body**
  (WebFetch-summarized). The **direction** of every result (legal up, general down) is robust and
  cross-checked across two fetches. **Per-benchmark decimal scores are lower confidence** — the
  PDF could not be rendered locally (no pdftoppm), so tables were not read pixel-for-pixel.
- Not captured: few-shot **k**, full per-sub-exam scores, `roseval/Juru-7B` license terms, and
  whether any **forgetting mitigation** (replay/data-mixing) was attempted. See `open-residue.md`.
- All Jusbrasil readings in this pack are labeled `operator-reading`/`analogy` and are kept
  separate from the paper's own `primary-source` claims in `claim-ledger.md`.
- Promotion is **LOCAL-ONLY**; the `arcanum` submodule was not touched.
