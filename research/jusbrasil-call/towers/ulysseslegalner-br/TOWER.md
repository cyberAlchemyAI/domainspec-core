# TOWER.md — Manifest & Integrity

**Tower:** ulysseslegalner-br
**Paper lane:** jusbrasil-call
**Status:** BUILT (standard depth). Landing page + README accessible; full PDF body NOT fetched (open-residue for fine-grained schema enumeration).

## File manifest

| File | Role |
|---|---|
| `README.md` | Entry point, reading order, source discipline |
| `TOWER.md` | This manifest + integrity rules |
| `L0-corpus.md` | Source record, section map, date checked, accessibility |
| `claim-ledger.md` | Every claim + source-kind label |
| `glossary.md` | Term list (NER, entity types, CRF, BiLSTM, BERTimbau, normalization) |
| `definitions.md` | Governed definitions for load-bearing terms |
| `distill.md` | One-sentence model, compositional spine, borrow/analogy/block |
| `bridge-decisions.md` | Paper -> Jusbrasil pipeline bridge statuses |
| `LEARNING-PACK.md` | Synthesis: claims, operator model, takeaways, 5 things, cutoff |
| `open-residue.md` | Unverified items / fabrication guard |

## Integrity rules

1. **Separation of voice.** Paper claims (primary), lineage (related), and Arcanum readings are visually and lexically separated in every file.
2. **No invented numbers.** Every numeric claim traces to L0-corpus source IDs S1/S2/S3. Numbers not present in an accessible source are open-residue.
3. **LOCAL-ONLY.** Nothing here is promoted into the `arcanum` submodule. This tower lives under `research/jusbrasil-call/towers/`.
4. **Date stamp.** All fetched-source claims carry the check date 2026-06-10.
5. **Open-residue is honest cutoff.** If the PDF body is later fetched, residue items migrate to claim-ledger with primary-source labels.

## Source IDs (see L0-corpus.md)

- **S1** — ACL Anthology landing page (abstract, BibTeX, metadata).
- **S2** — GitHub README, `ulysses-camara/ulysses-ner-br` (predecessor UlyssesNER-Br resources).
- **S3** — Web search corroboration (LeNER-Br, UlyssesNER-Br, CDJUR-BR lineage).
