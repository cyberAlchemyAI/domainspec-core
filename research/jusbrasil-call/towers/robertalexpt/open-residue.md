# open-residue.md — What Remains Open

Date checked: 2026-06-10. Items NOT verified from a fetched source. **No numbers
were invented to fill these.** Each has a fetch path to close it.

| # | Open item | Why open | How to close |
|---|---|---|---|
| R1 | **% of corpus removed by dedup** / size-reduction ratio | Not stated in model card, repo, or dataset cards; PDF body not machine-readable in this env. | Extract from PDF Section 4 (Deduplication) — table of pre/post sizes. |
| R2 | **Dedup ablation delta** (score with vs without dedup) | Same as R1; the "decisive" claim is qualitative in fetched artifacts. | PDF results/ablation table. |
| R3 | **Exact legal:general token ratio** in the final pretraining mix | Mix finding is corroborated but ratio not in artifacts. | PDF Section 5 (Pretraining) / data-mix description. |
| R4 | **Per-task macro-F1 breakdown** (LeNER-Br, UlyssesNER-Br, FGV-STF, RRI) | Only the 85.41 average captured. | PDF results table / repo leaderboard detail. |
| R5 | **Verbatim abstract** | ACL landing omitted abstract; Linguamática mirror = redirect loop; ResearchGate = 403; PDF not text-extractable here. | Retry Linguamática (article/view/457) or extract PDF text with a working pdftotext. |
| R6 | **Verbatim section TOC** | Section map in L0 is reconstructed, not from PDF TOC. | Confirm against PDF headings. |
| R7 | **Full baseline table** (all compared models + scores) | Only the beaten subset captured (Albertina-xlarge, BERTimbau base/large, Legal-RoBERTa-PT-large). | PDF main results table. |
| R8 | **Embedding-initialization finding** | Search summary mentions it was studied; specifics not captured. | PDF Section 5. |

## Environment note

The ACL PDF was downloaded but not text-extractable in this environment
(`pdftoppm`/`pdftotext` unavailable; binary FlateDecode streams). Closing R1–R8
mainly requires a working PDF text extractor or accessible HTML mirror.

## Residue count: **8 open items.**
