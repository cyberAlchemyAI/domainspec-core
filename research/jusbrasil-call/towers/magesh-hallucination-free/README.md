# Research Tower — Magesh et al., "Hallucination-Free?" (2024/2025)

**Lane:** `magesh-hallucination-free`
**Paper:** Magesh, Surani, Dahl, Suzgun, Manning, Ho — *Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools* (arXiv 2405.20362; J. Empirical Legal Studies, 2025).
**Date built:** 2026-06-10
**Promotion boundary:** LOCAL-ONLY. Nothing here is written into the `arcanum` submodule.

## What this tower is

A local, source-backed learning tower for ONE paper. It lets a reader understand
and decompose the paper — and apply it to **Jusbrasil's Jus IA research-assistant
feature** — without reading the paper cover to cover. The substantive content lives
in the files below; this README is the map.

The paper is the closest published audit of *exactly* Jus IA's product category:
RAG-based legal research assistants that vendors market as hallucination-resistant.

## How to use this to accelerate reading

1. Read `LEARNING-PACK.md` first — it is the 10-minute accelerator (claims, operator
   model, borrow/block calls, the 5 things to remember for the Jusbrasil call, and an
   honest cutoff of what could NOT be verified without the full PDF).
2. If you need the source spine, read `L0-corpus.md` (citation + section map) then
   `claim-ledger.md` (every claim tagged by source kind).
3. For precise meanings, use `glossary.md` (terms) and `definitions.md` (the 3–5
   load-bearing concepts with formal meaning + intuition + anti-misuse).
4. For "what do we actually do with this at Jusbrasil," read `distill.md` then
   `bridge-decisions.md` (explicit borrow/block/analogy statuses).
5. `open-residue.md` lists what still needs the full PDF and the follow-ups.

## File index

| File | Purpose |
|------|---------|
| `README.md` | This map. |
| `TOWER.md` | Level overview (L0 → claims → distill → learning pack) and reading order. |
| `L0-corpus.md` | Source record: citation, link, date checked, source boundary, section map. |
| `claim-ledger.md` | Claims tagged primary-source / related-source / local-inference / analogy / operator-reading / open-residue. |
| `glossary.md` | Key terms; each with source kind, local meaning, operator reading, misuse warning. |
| `definitions.md` | Governed definitions for load-bearing concepts (taxonomy, groundedness, correctness, misgrounded citation). |
| `distill.md` | One-sentence model, compositional spine, borrow / analogy-only / block. |
| `bridge-decisions.md` | Explicit statuses for applying findings to Jusbrasil. |
| `LEARNING-PACK.md` | The accelerator + honest cutoff. |
| `open-residue.md` | Unresolved questions, what needs the full PDF, follow-ups. |

## Source-kind discipline

Every claim is labelled. **primary-source** = stated in the paper / its official
summaries. **operator-reading** / **local-inference** = our Arcanum/Jusbrasil
interpretation, not the authors'. We never invent numbers; figures not seen in fetched
material are marked **open-residue**.
