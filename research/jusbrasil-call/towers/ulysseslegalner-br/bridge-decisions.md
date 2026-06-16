# Bridge Decisions — Paper -> Jusbrasil Ingestion Pipeline

Maps UlyssesLegalNER-Br concepts to the Jusbrasil ("Jus IA") **ingestion pipeline (NER / entity normalization)** that feeds citation linking, jurisprudence organization, and extraction. Each bridge carries a **status**: BRIDGED (source-grounded mapping), TENTATIVE (reading, needs PDF/data), or BLOCKED (cannot bridge without open-residue).

| # | Paper concept | Jusbrasil pipeline target | Status | Basis |
|---|---|---|---|---|
| B1 | Document-type coverage: bills + case law + statutes [C1] | The three ingestion streams Jusbrasil tags (proposed law, jurisprudence, enacted law) | **BRIDGED** | C1 + Jusbrasil context |
| B2 | "First NER corpus exclusively on Brazilian laws" [C2] | Statute-ingestion stream — the historically weakest-covered stream | **BRIDGED** | C2, A2 |
| B3 | 9-category / 23-type schema [C6] | Reference target schema for ingestion NER labels | **TENTATIVE** | C6; type NAMES are open-residue (O1) — cannot align to Jusbrasil's 23 types until enumerated |
| B4 | BERTimbau baseline, 96.18% micro F1 [C7, C9] | Encoder choice + accuracy bar for the NER model serving ingestion | **BRIDGED** | C7, C9 |
| B5 | "Unified corpus" best result [C9] | Single cross-document-type NER model vs. per-source silos | **TENTATIVE** | A1; "unified" semantics open-residue (O5) |
| B6 | 71–82% low-F1 floor [C10] | Hard entity types -> where entity **normalization** rules / disambiguation must concentrate | **TENTATIVE** | A1; which types is open-residue (O2) |
| B7 | Entity normalization / citation linking / jurisprudence org | Downstream of NER | **BLOCKED (by scope)** | Paper is recognition-only (D6); not a paper contribution — bridge is to Jusbrasil's own layer, not to this paper |
| B8 | Corpus reuse for fine-tuning Jusbrasil models | Training data acquisition | **BLOCKED (by access)** | License + download URL open-residue (O7) — cannot confirm reusability terms |
| B9 | Lineage LeNER-Br + UlyssesNER-Br + CDJUR-BR [R3, R4] | Candidate auxiliary training corpora for the same pipeline | **TENTATIVE** | R3, R4; related-source, schema-compatibility unverified |

## Decision summary

- **Safe to act on now:** B1, B2, B4 (document triad, statute gap filled, BERTimbau bar).
- **Needs PDF/data before acting:** B3, B5, B6, B9 (schema alignment, unified semantics, hard-type targeting, aux corpora).
- **Out of scope / blocked:** B7 (normalization is Jusbrasil's own layer), B8 (license unknown).
