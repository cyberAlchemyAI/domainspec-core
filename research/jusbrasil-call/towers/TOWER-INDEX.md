# Paper Towers — Index & Closeout Ledger

Built 2026-06-10 for the Jusbrasil call. Eight research towers, one per read-first paper from [../READING-LIST.md](../READING-LIST.md), each with a validated `read-decompose.dispatch.json` route. Purpose: decompose each paper into a source-backed learning path so the reader can absorb the core without reading cover to cover.

Promotion boundary: **local-only**. These are research artifacts; nothing here promotes into Inventory, Ontology, glossary, sigils, or spells, and nothing was written into the public `arcanum` submodule.

## How to use a tower

Each `towers/<slug>/` directory has the same spine. Fastest path:
1. **LEARNING-PACK.md** — the accelerator: source-backed claims, operator model, borrow/block, "5 things for the call", honest cutoff.
2. **distill.md** — one-sentence model + what to borrow / analogy-only / block.
3. **claim-ledger.md** — when you need to know *what is actually proven* vs inferred (source-kind labels).
4. **open-residue.md** — what still needs the full PDF before you cite it externally.

`read-decompose.dispatch.json` is the validated route (recover-source → claim-ledger → governed-definitions → distill → learning-pack → handoff) if you want to re-run or extend the decomposition.

## The eight towers

| # | Tower (slug) | Paper | Jus IA mapping | Dispatch |
|---|---|---|---|---|
| 1 | [magesh-hallucination-free](magesh-hallucination-free/LEARNING-PACK.md) | Hallucination-Free? (arXiv:2405.20362) | Research-assistant reliability / internal audit | [route](magesh-hallucination-free/read-decompose.dispatch.json) |
| 2 | [juru-legal-llm](juru-legal-llm/LEARNING-PACK.md) | Juru (arXiv:2403.18140) | Foundation model / build-vs-buy | [route](juru-legal-llm/read-decompose.dispatch.json) |
| 3 | [robertalexpt](robertalexpt/LEARNING-PACK.md) | RoBERTaLexPT (PROPOR 2024) | Encoder + corpus dedup | [route](robertalexpt/read-decompose.dispatch.json) |
| 4 | [jua-benchmark](jua-benchmark/LEARNING-PACK.md) | JUÁ (arXiv:2604.06098) | Similar-jurisprudence retrieval eval | [route](jua-benchmark/read-decompose.dispatch.json) |
| 5 | [feijo-moreira-entailment-summ](feijo-moreira-entailment-summ/LEARNING-PACK.md) | Feijó & Moreira (AI&Law 2023) | Smart summaries + faithfulness | [route](feijo-moreira-entailment-summ/read-decompose.dispatch.json) |
| 6 | [multi-lexsum](multi-lexsum/LEARNING-PACK.md) | Multi-LexSum (NeurIPS 2022) | Principais teses / multi-doc summ | [route](multi-lexsum/read-decompose.dispatch.json) |
| 7 | [ulysseslegalner-br](ulysseslegalner-br/LEARNING-PACK.md) | UlyssesLegalNER-Br (PROPOR 2026) | NER ingestion pipeline | [route](ulysseslegalner-br/read-decompose.dispatch.json) |
| 8 | [menezes-neto-outcome-prediction](menezes-neto-outcome-prediction/LEARNING-PACK.md) | de Menezes-Neto et al. (PLOS ONE 2022) | Next product: outcome prediction | [route](menezes-neto-outcome-prediction/read-decompose.dispatch.json) |

## Subagent closeout ledger

One builder agent per tower. All eight reached a terminal integration state; no lane is hidden or unreviewed.

| Lane | Agent ID | Source grounding | Integration decision | Status | Open residue |
|---|---|---|---|---|---|
| magesh-hallucination-free | a2ead818e80dc9656 | arXiv abstract + HTML v1; PDF garbled, JELS paywalled | integrated | closed | 12 |
| juru-legal-llm | aac3d8f9041ea22ce | arXiv abstract + HTML body (2 fetches); PDF not rendered | integrated | closed | 7 |
| robertalexpt | a269e4d638e69bef9 | ACL landing + HF model/dataset cards + GitHub; PDF not extractable | integrated | closed | 8 |
| jua-benchmark | a2abeb81025c865aa | arXiv abs + HTML v2; PDF via summarizer (decimals = transcription risk) | integrated | closed | 12 |
| feijo-moreira-entailment-summ | a2de599bc6ec484d8 | Abstract + metadata via dblp/S2; Springer paywalled; UFRGS thesis not extractable | integrated | closed | 10 |
| multi-lexsum | a560a5f8a4f117689 | arXiv landing + official site; PDF body binary; S2 404 | integrated | closed | 8 |
| ulysseslegalner-br | a77f0eb74ddc61b74 | ACL landing + BibTeX + GitHub README; PDF body not ingested | integrated | closed | 10 |
| menezes-neto-outcome-prediction | a6bdbad74559a55b4 | PLOS ONE open access, full article read (real numbers) | integrated | closed | 8 |

**Total open residue: 75 items**, all named in the per-tower `open-residue.md` files.

## Cross-tower residue pattern (honest cutoff)

The dominant residue theme is **PDF body inaccessibility in this environment** (no working PDF text extractor; several venues paywalled). Consequence:

- **Fully ground-truthed numbers:** only tower #8 (PLOS ONE, open access) — its headline figures (MCC 0.3688 vs human 0.1253; 765,602 cases) are read directly from the article.
- **Abstract/landing-grounded, decimals need PDF check before external citation:** towers #1–#7. Qualitative models and method spines are call-ready; specific table decimals (exact ROUGE, per-task F1, leaderboard NDCG) carry transcription risk and are fenced in residue.
- **Recommended next step before quoting any number on the call:** run the `recover-source` → `claim-ledger` steps of each dispatch once a PDF extractor is available, or open the flagged best-source link in each `open-residue.md`.

## Reproduce

The eight dispatches were generated and validated by [gen-dispatches.py](../gen-dispatches.py) against `arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py` (all 8 `VALIDATION=pass`).
