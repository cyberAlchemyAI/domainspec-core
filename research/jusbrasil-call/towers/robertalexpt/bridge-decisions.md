# bridge-decisions.md — Source vs Reading Boundary

Records where we drew the line between a **source claim** and an **Arcanum
reading**, and the status of each bridge. Keeps the tower honest.

| ID | Bridge (from → to) | Decision | Status |
|---|---|---|---|
| BR1 | Paper's "high duplication in legal corpora" → "dedup is decisive for Jusbrasil's millions of redundant judicial documents" | Treat magnitude/decisiveness as paper's thesis ([CORROBORATED]); the Jusbrasil applicability is a [READING]. | OPEN-MAGNITUDE (B4 unquantified) |
| BR2 | PortuLex 85.41 macro-F1 → "good enough for production legal retrieval/classification" | Keep 85.41 as [PRIMARY] benchmark result only; production-readiness is NOT claimed by the source. | BLOCKED (do not promote to production claim) |
| BR3 | "legal+general mix > legal-only" → "use mix recipe for Jus IA encoder" | Finding is [CORROBORATED]; the recipe recommendation is a [READING]. Token ratio is [OPEN]. | ACCEPTED (reading, ratio caveated) |
| BR4 | RoBERTa encoder embeddings → "similar-jurisprudence retrieval" | Encoder produces embeddings ([PRIMARY] by architecture); retrieval use-case is a [READING] — paper evaluates NER/classification, not retrieval. | ACCEPTED-AS-READING |
| BR5 | Released CC-BY artifacts → "reusable off-the-shelf for Jusbrasil" | Licensing + availability are [PRIMARY]. Direct reuse is a [READING] pending fit/eval. | ACCEPTED (reading) |
| BR6 | Reconstructed section map → "paper structure" | Section map is reconstructed from artifacts, not verbatim TOC. | PROVISIONAL (verify vs PDF) |

## Promotion policy

LOCAL-ONLY. Nothing in this tower is promoted into the `arcanum` submodule or any
shared store. All bridges above are local readings unless explicitly relabeled
[PRIMARY] with a fetched source.
