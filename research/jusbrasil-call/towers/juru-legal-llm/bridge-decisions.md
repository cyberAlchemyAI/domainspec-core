# bridge-decisions.md — Carry-to-Jusbrasil Verdicts

**Date checked:** 2026-06-10
**Frame:** foundation-model layer / build-vs-buy (continue-pretrain in-house vs RAG over a frontier model).
**Verdict vocab:** borrow-carefully | analogy-only | block | promotion-candidate | future-work
**Promotion scope:** LOCAL-ONLY. The `arcanum` submodule is never touched.

## BD1 — The legal-up / general-down trade-off

- **Verdict:** borrow-carefully + promotion-candidate (local).
- **Why:** Juru is direct, recent, Brazilian-legal evidence that CPT yields real legal gains
  (~+4.7 pts) at a measurable general-knowledge cost (~2–4 pts). This is the keystone fact for
  the layer decision.
- **Carry condition:** always quote it as a *trade-off*, never as "specialized = better."
- **Promotion target:** Jusbrasil foundation-model decision memo (local research lane only).

## BD2 — Reputable-source curation as the quality lever

- **Verdict:** borrow-carefully.
- **Why:** Curating from academic + LexML statute + STF case law is a transferable corpus
  policy and matches Jusbrasil's authority advantage (it owns/curates large legal corpora).
- **Caveat:** Juru's corpus is ~90% academic papers — provenance-reputable but not necessarily
  representative of Jus IA query distribution. Re-weight toward query-relevant text before
  assuming transfer.

## BD3 — "Narrow-band amplifier" mental model

- **Verdict:** analogy-only.
- **Why:** A clean way to communicate the build-vs-buy tension to stakeholders; it is a frame,
  not a paper claim. Do not attach Juru's numbers to the analogy as if measured.

## BD4 — The ~1.9B-token / 4-epoch / Mistral-7B recipe

- **Verdict:** analogy-only (not a transferable spec).
- **Why:** Specific to Juru's setup. Base model, token budget, and epoch count would all need
  re-tuning for any Jusbrasil build. Treat as existence proof of feasibility at modest scale,
  not as a recipe to copy.

## BD5 — Exam accuracy as the success metric

- **Verdict:** block (for production decisions).
- **Why:** OAB/ENAM accuracy is a proxy. Production legal quality (citation correctness,
  hallucination, drafting) is not measured here. Do not let the call equate benchmark gain with
  product readiness.

## BD6 — Forgetting mitigation (replay / rehearsal / mixing general data)

- **Verdict:** future-work.
- **Why:** The paper documents forgetting but (per fetched content) does not report a mitigation
  that recovers general ability. Whether replay/data-mixing or a router solves it for Jus IA is
  an open engineering question worth its own spike. See open-residue.

## BD7 — Build-vs-buy default for Jus IA mixed traffic

- **Verdict:** operator-reading -> promotion-candidate (local decision memo).
- **Why:** Given measured forgetting, a single specialized base is risky for mixed traffic.
  Default lean: **RAG over a frontier model and/or a router**, reserving CPT for law-pure,
  cost/latency/data-sovereignty-constrained workloads. Juru is the evidence that the CPT lane is
  feasible — not that it is the right default.
