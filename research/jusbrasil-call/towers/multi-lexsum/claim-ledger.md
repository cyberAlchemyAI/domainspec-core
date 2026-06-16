# claim-ledger.md — Claims with source-kind labels

Date checked: **2026-06-10**
Legend: **[S]** source (paper) · **[S-site]** official site · **[A]** Arcanum reading · **[O]** open/ungrounded

## Dataset size & scope

| # | Claim | Kind | Source |
|---|-------|------|--------|
| C1 | The dataset contains **9,280 expert-authored summaries**. | [S] | abstract |
| C2 | Summaries cover **civil rights lawsuits** sourced from the Civil Rights Litigation Clearinghouse (CRLC). | [S] | abstract |
| C3 | Summaries are authored by **lawyers and law students** who spend hours per case across multiple documents. | [S] | abstract |
| C4 | Authoring followed **carefully created guidelines** with additional **expert review** for QA. | [S-site] | site |
| C5 | Number of distinct **cases/lawsuits** covered. | [O] | not fetched (9,280 is a summary count, not necessarily case count) |

## Multi-granularity design

| # | Claim | Kind | Source |
|---|-------|------|--------|
| C6 | Three granularity tiers per case: **long, short, tiny**. | [S-site] | site |
| C7 | **Long** summary: multiple paragraphs, **~650 words**. | [S-site] | site |
| C8 | **Short** summary: single paragraph, **~130 words**. | [S-site] | site |
| C9 | **Tiny** summary: one sentence, **~25 words**. | [S-site] | site |
| C10 | Abstract framing: summaries range from one-sentence "extreme" summaries to multi-paragraph narrations of **over five hundred words**. | [S] | abstract |
| C11 | Each case has one summary at each level. | [S-site] | site (stated; cross-check vs C5 case count = [O]) |

## Multi-document / long-input setup

| # | Claim | Kind | Source |
|---|-------|------|--------|
| C12 | Source documents are long, **often exceeding two hundred pages per case**. | [S] | abstract |
| C13 | Multiple document **types**: dockets, complaints, motions, opinions, settlements. | [S-site] | site |
| C14 | Per-case document **count** (how many docs feed one summary). | [O] | not fetched |
| C15 | This is therefore a **multi-document, long-input** summarization task. | [S]/[A] | stated as multi-doc [S]; "long-input" emphasis is [A] reading |

## Baselines & findings

| # | Claim | Kind | Source |
|---|-------|------|--------|
| C16 | **State-of-the-art summarization models perform poorly** on this task. | [S] | abstract |
| C17 | Specific baseline **model names** (e.g., BART/PRIMERA/Longformer/Pegasus). | [O] | PDF not parsed |
| C18 | **ROUGE / metric scores** per model and per granularity. | [O] | PDF not parsed |
| C19 | **Train/dev/test split** sizes. | [O] | PDF not parsed |

## Access & license

| # | Claim | Kind | Source |
|---|-------|------|--------|
| C20 | Paper/landing license: **Creative Commons Attribution 4.0**. | [S] | arXiv landing |
| C21 | Dataset license (site): **Open Data Commons Attribution (ODC-By)**. | [S-site] | site |
| C22 | Summaries/metadata: **CC BY-NC**; source documents: **public domain**. | [S-site] | site |
| C23 | **Commercial use** requires contacting info@clearinghouse.net for alternative licensing. | [S-site] | site |

> Note for Jus IA (C22/C23): the summary text is **non-commercial (NC)**. Commercial reuse of
> the gold summaries needs the alternative-licensing path. This is a real constraint. [A]
