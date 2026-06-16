# Research Tower — UlyssesLegalNER-Br

**Lane:** `jusbrasil-call / towers / ulysseslegalner-br`
**Paper:** Albuquerque et al. (2026), "UlyssesLegalNER-Br: from Legislative to Legal, a comprehensive corpus of Brazilian legal documents for Named Entity Recognition", PROPOR 2026.
**Built:** 2026-06-10
**Depth:** standard

## What this tower is

A local, source-backed learning tower for ONE paper. It lets a reader understand and decompose the paper — corpus, schema, baselines, results — without reading it cover to cover, and maps it to the Jusbrasil ("Jus IA") ingestion pipeline (NER / entity normalization) that feeds citation linking, jurisprudence organization, and extraction.

## How to read it (suggested order)

1. **`LEARNING-PACK.md`** — start here. Source-backed claims, operator model, NER-pipeline takeaways, 5 things for the call, honest cutoff.
2. **`distill.md`** — one-sentence model + compositional spine.
3. **`L0-corpus.md`** — the source record (what was fetched, when, accessibility).
4. **`claim-ledger.md`** — every claim with a source-kind label (primary / related / open-residue).
5. **`glossary.md`** + **`definitions.md`** — terms.
6. **`bridge-decisions.md`** — how paper concepts bridge to the Jusbrasil pipeline.
7. **`open-residue.md`** — what is NOT verified and needs the PDF or further fetch.
8. **`TOWER.md`** — manifest + integrity rules.

## Source-claim discipline

- **Primary-source** = stated on the ACL Anthology landing page (abstract/BibTeX) or the GitHub README, captured verbatim where load-bearing.
- **Related-source** = LeNER-Br / UlyssesNER-Br lineage and external SOTA context.
- **Arcanum reading** = our interpretation/mapping; always labeled as a reading, never as a paper claim.
- **Open-residue** = not verified from an accessible source (e.g., the full PDF body); marked, never fabricated.

No invented numbers. LOCAL-ONLY promotion — the arcanum submodule is never touched.
