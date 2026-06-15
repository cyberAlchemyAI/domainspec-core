# Glossary

Each entry: **source kind** · **local meaning** (as used in this paper/tower) ·
**operator reading** (Arcanum/Jusbrasil) · **misuse warning**.

---

### Hallucination (legal)
- **Source kind:** PRIMARY.
- **Local meaning:** A model response that is **incorrect OR misgrounded** — either it
  states something false, or it asserts that a (possibly real) source supports a claim
  the source does not actually support.
- **Operator reading:** The audit's *failure* label. For Jus IA, this is the metric an
  internal audit should report — and it must include misgrounding, not just fabrication.
- **Misuse warning:** Do NOT equate hallucination with "made up a fake case." Under this
  paper a confident, correct-sounding answer with a real-but-irrelevant citation is still
  a hallucination. Narrowing the definition makes any tool look "hallucination-free."

### Correctness
- **Source kind:** PRIMARY.
- **Local meaning:** Whether the response is **factually accurate and relevant** to the
  query. Values: correct / incorrect / refusal.
- **Operator reading:** Axis 1 of the Jus IA scoring rubric — "is the legal answer right?"
- **Misuse warning:** Correctness alone is insufficient. A correct answer can still be a
  hallucination if it is misgrounded. Never report "% correct" as "% non-hallucinated."

### Groundedness
- **Source kind:** PRIMARY.
- **Local meaning:** Whether the response's key factual propositions make **valid
  references to relevant legal documents** — i.e., the cited authority actually supports
  what is claimed. Values: grounded / misgrounded / ungrounded. Assessed **only for
  correct responses**.
- **Operator reading:** Axis 2 of the rubric — "do the citations actually hold up?" This
  is the axis RAG was supposed to fix and the one Jus IA must measure directly.
- **Misuse warning:** This is the paper's legal-domain sense ("grounded in governing
  caselaw"), distinct from generic CS "groundedness" (any source overlap). Don't conflate
  citation *existence* with citation *support*.

### Misgrounded citation
- **Source kind:** PRIMARY.
- **Local meaning:** The cited source is **real and valid**, the statement may even be
  **correct**, but the **source does not actually say what the model claims it says**.
- **Operator reading:** The single most dangerous and least visible failure for a legal
  RAG product — it survives "does the link resolve?" checks. The primary thing a Jus IA
  audit must hunt.
- **Misuse warning:** A green checkmark on "citation exists / link valid" does NOT mean
  grounded. Misgrounding is invisible to link-validation; it needs human/LLM verification
  that the source supports the proposition.

### Ungrounded response
- **Source kind:** PRIMARY.
- **Local meaning:** A correct response that **lacks valid supporting citation** (no
  source, or sources that don't connect). Counted under *incomplete*, not *accurate*.
- **Operator reading:** "Right answer, but you can't trust/audit how it got there."
- **Misuse warning:** Don't bucket ungrounded with accurate just because the answer was
  right; in legal practice an unverifiable right answer is not deliverable.

### RAG (Retrieval-Augmented Generation)
- **Source kind:** PRIMARY.
- **Local meaning:** Architecture that retrieves source documents and conditions
  generation on them, marketed by vendors as eliminating hallucination.
- **Operator reading:** Jus IA's own architecture. The paper's lesson: RAG moves the
  failure surface to **retrieval quality** and **citation faithfulness** — it does not
  remove it.
- **Misuse warning:** "We use RAG" is not a hallucination guarantee. The paper exists
  precisely to refute that marketing inference.

### Retrieval failure
- **Source kind:** PRIMARY.
- **Local meaning:** The retrieval stage returns **irrelevant or poor documents**, so the
  model has nothing good to ground in.
- **Operator reading:** One of two diagnosable failure stages; if Jus IA hallucinations
  trace here, fix the index/retriever, not the prompt.
- **Misuse warning:** Don't assume all hallucinations are generation-side. The paper
  shows retrieval failure can produce *correct-but-misgrounded* outputs.

### Generation failure
- **Source kind:** PRIMARY.
- **Local meaning:** Good documents were retrieved but the model **misreads** them
  (misstates holdings, swaps majority/dissent, mis-ranks precedent authority).
- **Operator reading:** Second failure stage; fix via grounding constraints, prompting,
  or model choice — not the retriever.
- **Misuse warning:** Don't fix the retriever when the bug is interpretation.

### Sycophancy / false-premise failure
- **Source kind:** PRIMARY / RELATED.
- **Local meaning:** When the user's query embeds a wrong legal premise, the tool tends to
  **support the premise** with plausible authority instead of correcting it.
- **Operator reading:** A targeted test category (22 queries). Jus IA should include
  adversarial false-premise prompts in its audit set.
- **Misuse warning:** Don't only test well-formed questions; real lawyers ask leading,
  premise-loaded ones.

### Preregistered evaluation
- **Source kind:** PRIMARY.
- **Local meaning:** The query set and scoring rubric were **fixed and published before**
  running the tools, preventing cherry-picking and post-hoc metric tuning.
- **Operator reading:** The credibility mechanism. An internal Jus IA audit gains
  defensibility by preregistering its query set + rubric before testing.
- **Misuse warning:** Running queries first and choosing favorable metrics afterward is
  the opposite of this — it produces marketing, not an audit.

### Accurate / Incomplete / Hallucinated (response labels)
- **Source kind:** PRIMARY.
- **Local meaning:** The three terminal scoring buckets — **accurate** = correct AND
  grounded; **incomplete** = refusal or correct-but-ungrounded/partial; **hallucinated**
  = incorrect OR misgrounded.
- **Operator reading:** The exact reporting schema to adopt for a Jus IA audit dashboard.
- **Misuse warning:** Incomplete is not "safe success." High incompleteness (e.g. Ask
  Practical Law's 62%) is reduced usefulness — track it as a cost, not a win.
