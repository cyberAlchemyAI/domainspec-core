# glossary.md — Plain-language terms

Date checked: **2026-06-10**. For governed canonical wording see `definitions.md`.

- **Multi-document summarization (MDS):** Producing one summary from *several* source
  documents about the same thing (here: dockets, complaints, motions, opinions, settlements
  for one lawsuit), rather than from a single article. The model must fuse and deduplicate
  across documents. [S/A]

- **Granularity (of a summary):** The target length/abstraction level. Multi-LexSum defines
  three: **tiny** (~25 words, one sentence), **short** (~130 words, one paragraph), **long**
  (~650 words, multi-paragraph). Same input, three controlled output sizes. [S-site]

- **Expert reference summaries:** Gold summaries written by domain experts (lawyers, law
  students) under guidelines, with expert review — not crowdsourced. These are the references
  models are scored against. [S/S-site]

- **Long-document modeling:** Handling inputs far beyond standard transformer context limits
  (here, case files often >200 pages). Requires long-context architectures, chunking +
  hierarchical/iterative composition, or retrieval to fit the input. [S/A]

- **Extreme summarization:** Compressing a whole document set into a single sentence — the
  abstract's word for the tiny tier. [S]

- **CRLC (Civil Rights Litigation Clearinghouse):** The real-world source of cases and expert
  summaries; the dataset is a faithful extract of professional summarization labor. [S]

- **Compression ratio:** Source length ÷ summary length. Here it is extreme and *tunable* by
  granularity tier — a key property for a controllable feature. [A]

- **Main-theses / "principais teses" (Jus IA):** The product feature this tower bridges to —
  compressing many decisions into recurring short statements at controlled granularity. The
  analog of Multi-LexSum's tiny/short tiers over a multi-document input. [A]
