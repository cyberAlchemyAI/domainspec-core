# Glossary

Plain-language term list for this tower. Definitions governed in `definitions.md`; here they are quick-reference.

- **NER (Named Entity Recognition).** Subtask of NLP that locates and classifies spans of text into predefined entity classes (e.g., person, organization, law reference). The core task of this paper. [from S1 abstract]

- **Entity category.** Coarse-grained class in the schema. UlyssesLegalNER-Br defines **9 categories**. [C6]

- **Entity (fine-grained) type.** Finer subdivision under categories. UlyssesLegalNER-Br defines **23 fine-grained types**. Specific names are open-residue (O1). [C6]

- **Corpus.** An annotated collection of documents used to train/evaluate NER. Here: 560 public Brazilian legal documents — bills, case laws, laws. [C1, C4]

- **Hybrid annotation approach.** Labeling method combining more than one technique (e.g., manual + rule/automatic). Named in abstract; exact composition is open-residue (O4). [C5]

- **Unified corpus.** The combined evaluation setting where BERTimbau reached 96.18% micro F1. Exact merge semantics open-residue (O5). [C9]

- **Micro F1.** F1 aggregated over all entity instances (each instance weighted equally), as opposed to macro F1 (each class weighted equally). The paper's headline metric is **micro F1 96.18%**. [C9]

- **CRF (Conditional Random Field).** Classic structured-prediction sequence model; predicts label sequences using hand-crafted features + transition scores. A non-neural NER baseline. [C7]

- **BiLSTM (Bidirectional Long Short-Term Memory).** Recurrent neural network reading a sequence both forward and backward; common pre-transformer NER backbone, often paired with a CRF decoding layer. [C7]

- **BERTimbau.** A BERT language model pre-trained on Brazilian Portuguese (by NeuralMind). Transformer encoder fine-tuned for NER; the **top performer** here. [C7, C9]

- **Entity normalization (a.k.a. entity linking / canonicalization).** Mapping a recognized entity mention to a canonical identifier (e.g., a specific law, court, or party record). NOT a task of this paper (NER stops at span+type) but the **downstream step** in the Jusbrasil ingestion pipeline that consumes NER output. [READING; Jusbrasil context]

- **LeNER-Br.** PROPOR 2018 dataset — first Brazilian legal NER corpus (case-law focused). Lineage ancestor. [R3]

- **UlyssesNER-Br.** Predecessor legislative-domain corpus (bills/consultations/comments) that this paper expands. [C3, R1]

- **CDJUR-BR.** Parallel fine-grained Brazilian legal NER golden collection (arXiv 2305.18315) — adjacent SOTA context. [R4]
