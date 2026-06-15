# Governed Definitions — Load-Bearing Concepts

These are the 3–5 concepts the whole paper turns on. Each keeps **formal meaning +
intuition + anti-misuse** together so downstream use cannot drift. All PRIMARY-sourced
from the paper unless noted.

---

## 1. Legal hallucination (the operational definition)

**Formal meaning.** A model response is a *hallucination* iff it is **incorrect OR
misgrounded**. Formally, hallucination = NOT(correct AND grounded). It is the union of
two independent failure axes (see §2 and §3), so a response counts as hallucinated if it
fails *either* axis — even a factually correct answer fails if its citations don't
support it.

**Intuition.** "Hallucination" is broader than "invented a fake case." It includes the
quiet failure where everything looks right — real citation, plausible legal statement —
but the source doesn't actually back the claim. The paper's whole point is that vendors
implicitly use the narrow definition ("no fake cases") to claim "hallucination-free,"
while the honest definition still catches them 17–33% of the time.

**Anti-misuse.** Never report a "non-hallucination rate" computed only from fabrication
checks or only from correctness. Both axes must be scored, and the metric is the union of
their failures. Shrinking the definition is exactly the marketing move the paper rebuts.

---

## 2. Correctness (axis 1)

**Formal meaning.** A property of a response: it is **correct** if it is both factually
accurate and relevant to the query; **incorrect** if it contains any inaccurate
information; **refusal** if the model declines to answer. Independent of where/whether the
answer is cited.

**Intuition.** "Is the legal answer actually right?" — judged against the law itself, not
against the cited document.

**Anti-misuse.** Correctness is necessary but not sufficient for a good answer. Do not
equate "% correct" with "% trustworthy"; a correct answer can still be misgrounded and is
then a hallucination (see §1). Refusals are their own category — do not score them as
incorrect.

---

## 3. Groundedness (axis 2)

**Formal meaning.** A property assessed **only on correct responses**: whether the key
factual propositions make **valid references to relevant legal documents** that actually
support them. Values: **grounded** (cited sources support the claim), **misgrounded**
(sources cited but they don't support the claim), **ungrounded** (no valid supporting
source). This is the legal-domain sense — "grounded in actual governing caselaw" —
explicitly distinguished from generic CS "groundedness."

**Intuition.** "Do the citations actually hold up if a lawyer checks them?" RAG was sold
as the fix for this axis; the paper shows it is exactly where the residual failures hide.

**Anti-misuse.** Do not conflate citation *existence* / link validity with groundedness.
A resolvable link to a real case is NOT groundedness; the source must *support the
specific proposition*. Groundedness is undefined for incorrect responses (you can't
ground a wrong claim) — assess it only after correctness passes.

---

## 4. Misgrounded citation (the diagnostic failure)

**Formal meaning.** A correct (or correct-sounding) proposition supported by a **citation
to a real, valid source that does not actually establish the proposition.** A specific
value of the groundedness axis, and (with "incorrect") one of the two triggers of the
hallucination label.

**Intuition.** The citation passes every cheap check — it exists, it resolves, it's a
real case — yet it's a bluff. This is the failure that survives automated link-validation
and most embarrasses a lawyer who relied on it without reading the source.

**Anti-misuse.** Treating "citation resolves" as proof of grounding is the core error
this concept guards against. Any audit that only checks citation existence will report
near-zero hallucination while misgrounding runs free.

---

## 5. Correctness × Groundedness framework (the composition)

**Formal meaning.** The two axes form a typology that collapses to three reportable
buckets: **accurate** = correct AND grounded; **incomplete** = refusal, or
correct-but-ungrounded/partial; **hallucinated** = incorrect OR misgrounded.
Groundedness is evaluated only within the "correct" branch.

**Intuition.** A decision tree: first ask "is it correct?" (correct / incorrect /
refusal). If correct, ask "is it grounded?" (grounded / misgrounded / ungrounded). The
buckets then fall out — and crucially the *correct-but-misgrounded* leaf lands in
"hallucinated," not "accurate."

**Anti-misuse.** Don't flatten the framework into one accuracy number. The whole
analytical value is the separation — it tells you *whether to fix the retriever
(groundedness/retrieval failure) or the generator (correctness/generation failure)*.
Reporting a single blended score throws that diagnostic signal away.

> **Portability note (OPERATOR-READING, not the authors' claim):** Definitions 1–5 are a
> *scoring rubric*, not a fact about US law. They transfer wholesale to any RAG legal-QA
> product, including Jus IA — see `distill.md` and `bridge-decisions.md`.
