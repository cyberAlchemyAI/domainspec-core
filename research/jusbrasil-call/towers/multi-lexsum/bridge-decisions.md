# bridge-decisions.md — Adopt / adapt / reject for Jus IA

Date checked: **2026-06-10**
Statuses: **ADOPT** (use as-is) · **ADAPT** (use with translation) · **REJECT** (do not carry) ·
**DEFER** (needs ungrounded fact before deciding)

| # | Decision area | Status | Rationale | Depends on |
|---|---------------|--------|-----------|------------|
| B1 | Explicit length-anchored granularity tiers for main-theses (tiny/short/long) | **ADOPT** | Core, proven design; 25/130/650 are calibration anchors. [S-site] | — |
| B2 | Expert-guideline authoring + review as gold-label process | **ADOPT** | Validated path for professional summaries. [S/S-site] | — |
| B3 | Multi-document fusion framing (fuse + dedupe across many sources) | **ADOPT** | Matches main-theses' many-decisions input. [S] | — |
| B4 | Input grouping = single lawsuit's file | **ADAPT** | Jus IA groups by thesis/legal-question cluster across decisions; add a clustering stage. [A] | — |
| B5 | "One summary per input" output shape | **ADAPT** | Main-theses are plural recurring statements; allow N theses per cluster. [A] | — |
| B6 | Reuse the gold summary *texts* in a commercial product | **REJECT** | Summaries are CC BY-NC; source docs public-domain. Use methodology, not texts. [S-site] | — |
| B7 | Trust SOTA-summarizer "poor performance" as transferable | **ADAPT** | Direction (long-MDS is hard) holds; magnitude is English-domain-specific. Re-baseline on PT data. [S] | C17/C18 |
| B8 | Pick baseline architectures by copying Multi-LexSum's exact baselines | **DEFER** | Model names not yet fetched from PDF. | open-residue R1 |
| B9 | Size Jus IA eval splits using Multi-LexSum's splits as reference | **DEFER** | Split sizes not fetched. | open-residue R3 |
| B10 | Treat 9,280 as a case count | **REJECT** | 9,280 is a *summary* count (3 tiers); case count is ungrounded. [S] | open-residue R2 |

## Net read [A]
Strong **ADOPT** on the design ideas (tiers, expert loop, MDS framing). **ADAPT** for the
many-decisions clustering and plural-output shape. **REJECT** copying texts (NC license) and
the assumption that one input = one summary. **DEFER** anything needing baseline/split numbers
until the PDF body is parsed.
