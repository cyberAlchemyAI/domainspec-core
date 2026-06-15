# definitions.md — Governed Definitions

**Date checked:** 2026-06-10
Governed definitions for the load-bearing concepts. Each pins the term precisely enough that
claims and bridge decisions cannot drift on it.

## D1. Continued pretraining (CPT)

> The continuation of the self-supervised (next-token) pretraining objective on a new,
> domain-specific corpus, starting from the weights of an already-pretrained base model,
> with the goal of shifting the model's distribution toward the target domain.

- **In Juru:** Mistral-7B + 1.9B unique legal tokens, ~4 epochs, ~7.96B tokens processed.
- **Boundary:** NOT supervised fine-tuning (no task labels), NOT RAG (no retrieval at
  inference), NOT instruction tuning. It changes the *weights*, permanently.
- **Why it is load-bearing:** the entire build-vs-buy comparison hinges on CPT being a
  weight-mutating, capability-redistributing operation — which is exactly why it forgets.

## D2. Catastrophic forgetting

> A measurable decline in a model's previously-held capabilities caused by training on new
> data, where the new objective overwrites representations the old capability relied on.

- **In Juru:** general-knowledge means drop in both PT (~−2.4 pts) and EN (~−3.6 pts) after
  legal CPT, while legal mean rises (~+4.7 pts).
- **Boundary:** it is a property of *weight updates*, not of the data being "bad." Even
  reputable in-domain data causes it. It is the structural cost of specialization.
- **Governed reading:** "specialization is redistribution, not pure addition." Capacity moves
  toward the domain and away from the rest.

## D3. Domain adaptation

> Any method that increases a model's performance on a target domain. CPT is one
> implementation; retrieval augmentation, fine-tuning, and prompting are alternatives that
> trade off cost, recency, and forgetting differently.

- **Boundary:** "domain adaptation" is the *goal*; CPT, RAG, SFT are *mechanisms*. Conflating
  them is the classic build-vs-buy error.

## D4. Reputable-source curation

> A corpus-construction policy that admits only authoritative, provenance-clear documents —
> here: Brazilian academic legal papers, official statutes (LexML), and apex-court (STF)
> decisions — in service of the "high-quality data beats more data" hypothesis.

- **In Juru:** ~90% academic papers by token volume; statute and case law are the minority.
- **Boundary:** "reputable" describes *provenance and authority*, not *task coverage*. A
  reputable corpus can still be unrepresentative of downstream query distribution.

## D5. OAB / legal exam benchmark

> An evaluation suite built from Brazilian legal qualifying/judiciary exams — the OAB (Bar
> Association) exam and ENAM (national judiciary exam) — used as a proxy for legal reasoning
> and knowledge capability.

- **In Juru:** OAB-2023, OAB-2024, ENAM-2024; this is where Juru's gains are demonstrated.
- **Boundary:** exam accuracy is a proxy, not a measure of production legal-task quality
  (drafting, citation accuracy, hallucination rate). Promotion to Jusbrasil claims must respect
  this gap.
