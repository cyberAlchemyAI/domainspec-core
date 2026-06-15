# glossary.md — Core Terms (plain language)

- **Abstractive summarization** — Generating a summary by writing *new* sentences that capture the source's meaning (vs. *extractive*, which copies existing sentences). Typically done with an encoder–decoder neural model. Strength: human-like fluency. Risk: can introduce facts not in the source (hallucination).

- **Ementa** — In Brazilian legal practice, the official **headnote/summary** placed at the top of a court ruling: a condensed statement of the legal thesis and outcome. In RulingBR it is the **gold (ground-truth) summary** that models are trained to reproduce. Direct analogue of what Jus IA's smart summaries aim to produce.

- **Textual entailment / NLI (Natural Language Inference)** — The task of deciding whether a *hypothesis* is **entailed by** (logically supported by), **contradicts**, or is **neutral to** a *premise* (the source text). Here: treat the source ruling as premise and a candidate summary as hypothesis; high entailment ⇒ the summary is supported by the source ⇒ more faithful.

- **Faithfulness (vs. hallucination)** — A summary is **faithful** when every claim it makes is actually supported by the source. **Hallucination** is the failure mode where the summary asserts unsupported or wrong information. In legal use this is high-stakes: a wrong precedent summary can mislead an argument.

- **RulingBR** — A Portuguese-language legal summarization dataset (Feijó & Moreira, PROPOR 2018): ~10K Brazilian Supreme Court (STF) rulings, 2011–2018, each with `ementa` (gold summary), `relatório`, `voto`, `acórdão` plus metadata. The training/eval substrate for LegalSumm. Repo: github.com/diego-feijo/rulingbr.

- **LegalSumm** — The method in this paper: build multiple **views** over a long ruling, generate an independent candidate summary per view, then use an **entailment module** to score and **select** the most faithful candidate. Goal: reduce hallucination while improving ROUGE.

- **View** — A partial projection/segment of the (long) source ruling, created so the length-limited encoder can process it. Multiple views ⇒ multiple candidate summaries to choose among.

- **ROUGE** — Standard n-gram-overlap metric family (ROUGE-1/2/L) comparing a generated summary against the gold summary. Used here to report quality gains.
