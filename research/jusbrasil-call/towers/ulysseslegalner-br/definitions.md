# Definitions (Governed)

Canonical definitions for load-bearing terms in this tower. Each carries a source label. Drift check: if a future PDF fetch contradicts a definition, update here first and propagate to glossary + claim-ledger.

## D1 — UlyssesLegalNER-Br (the artifact) [PRIMARY, S1]

A comprehensive corpus of **560 public Brazilian legal documents** annotated for NER across **bills, case laws, and laws**, organized in **9 categories and 23 fine-grained types**, expanding the legislative-only UlyssesNER-Br to the full legal domain and contributing the first NER corpus built exclusively on Brazilian laws. Released with CRF/BiLSTM/BERTimbau baselines.

## D2 — "From Legislative to Legal" (the framing) [PRIMARY, S1 + READING]

Source fact: the corpus extends coverage from the *legislative* domain (bills) to the broader *legal* domain (adding case law and statutes). **Reading:** this completes a document-type triad — bills (proposed law), case law (jurisprudence), statutes (enacted law) — which mirrors the three ingestion streams a legal platform like Jusbrasil must NER-tag.

## D3 — Micro F1 (headline metric) [governed]

Instance-weighted harmonic mean of precision and recall over all entity spans. The paper's top result is **micro F1 96.18%** (BERTimbau, unified corpus) [C9]. Macro/per-label breakdown beyond "6 categories / 7 types > 95%, lowest 71–82%" is open-residue (O2).

## D4 — Baseline triad: CRF / BiLSTM / BERTimbau [PRIMARY, S1]

Three architectures of increasing modeling power evaluated as baselines:
- **CRF** — feature-based structured prediction (non-neural).
- **BiLSTM** — recurrent neural sequence encoder.
- **BERTimbau** — Brazilian-Portuguese transformer encoder; the strongest.
Establishes "a strong baseline for Brazilian legal NER" [C9]. Hyperparameters and exact configs are open-residue.

## D5 — Hybrid annotation approach [PRIMARY label, detail open]

Stated annotation method [C5]. Precise definition (manual + automatic pre-annotation, adjudication, inter-annotator agreement) is **open-residue (O4)** — do not assert specifics.

## D6 — Entity normalization (downstream, NOT in paper) [READING]

The step that maps NER output (mention span + type) to a canonical entity identifier. This paper produces the *recognition* layer; normalization, citation linking, and jurisprudence organization are **downstream consumers**, not contributions of UlyssesLegalNER-Br. Kept distinct to avoid over-claiming the paper's scope.
