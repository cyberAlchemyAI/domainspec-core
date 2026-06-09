# CyberAlchemy — Executive Brief

> **Candidate offer. Not a contract or priced engagement.** Every capability claim is tagged
> `[proven]` (demonstrated in the GoldenQuill reference build) or `[hypothesis]` (carries a validation
> step). Cross-vertical generalization is a hypothesis. No pricing, no named-client commitments. A
> claim-tag audit is at the end of this document.

## Executive summary

Most companies produce dashboards but do not *learn* from outcomes systematically. Numbers are trusted
or distrusted on instinct; lessons live in staff memory; agents run without guardrails. CyberAlchemy
installs an ontology + DAG layer that does two things at once: it makes your **business intelligence
auditable today**, and it wires a **governed learning loop** that keeps that BI trustworthy and
improving as you run.

We lead with BI because it is the fastest measurable value on data you already have. The governance
layers underneath are what make the BI defensible over time — and they are the durable differentiator.

## Layer 1 (lead) — Evidence-linked, graded business intelligence **[BI first]**

Each key metric is rebuilt as an **evidence-linked observation** that reports a *pair, not a number*:

- its **denominator / dimension definition** — what it covers and divides by (guards against quietly
  dropping a dimension), and
- its **source-event chain + interpretation limit** — where the value came from and what it does not
  count (guards against a distorted value).

Each observation also carries a **`veracidade` (veracity) grade** (high / medium / low) and
**`evidence_refs`** (the locators that justify the grade). A metric cannot be graded `high` with an empty evidence list —
"proven" always comes with receipts.

- **[proven]** evidence-linked KPI families, explicit denominators, and counterfactual receipts were
  built in GoldenQuill (KPI family appendix + `CycleReceipt`).
- **[hypothesis]** the per-node `veracidade` + `evidence_refs` grade is an adaptation; validated in the
  pilot by checking that the chosen proof metric grades `high` with reproducible receipts.

**Anti-collapse, stated honestly.** A number can fail two independent ways — *concept erasure* (its
schema drops a dimension) and *number hallucination* (its value is distorted at populate-time). These
are two separate audits. This pairing is an **interpretive principle** we use because it names a real,
separable pair of failure modes our gates already enforce (denominator semantics vs source-truth). It
is **[hypothesis / interpretive]** — borrowed from the DomainSpec two-layer framework; the underlying
Lean result is about data migration and is *silent on metrics*. **We do not claim a proof that your
KPIs cannot collapse.**

## Layer 2 — Ontology cards (what makes the BI trustworthy: shared meaning)

Two orthogonal axes — *subject/segment* × *value-mechanism* — modeled as cards that configure search
vocabulary, evidence schema, language register, and reporting rhythm. Cards are **matched at runtime,
never hardcoded**; coupling between the axes is forbidden (a guard blocks baked bindings).

- **[proven]** the customer-identity × capital-logic card model and the coupling-violation guard exist
  in the reference build.
- **[hypothesis]** your specific axes (see your vertical instantiation) are candidates to confirm in
  assessment.

## Layer 3 — Classification register (what makes the BI trustworthy: data boundaries)

A signed `field → authority class` register gates where each field may travel — local vs cloud,
private vs shareable — **fail-closed** (unknown class defaults to restricted). No agent runs on your
data before this register is signed.

- **[proven]** the classification register + routing postures exist in the reference build.
- **[hypothesis]** in pilot-1 the register runs **advisory with a manual operator hash**; cryptographic
  signing is added when agent volume justifies it (see `gaps/transition-plan.md`).

## Layer 4 — Promotion DAG + governed agents (what makes the BI trustworthy: the learning loop)

Your runs flow through a governed chain. Nothing auto-promotes:

```text
run  ->  source-backed event  ->  measured metric / learning signal
     ->  reviewable candidate lesson (states how it could be wrong)
     ->  privacy + governance review  ->  owner decision
     ->  promoted reuse | rejected | retired | contradicted | private residue
```

Eleven deterministic gates enforce this: no event without a source; stage depth is never an outcome; a
metric may not self-promote; every candidate states its contradiction path; scoped feedback is redacted
before shared reuse; reuse needs an explicit owner decision; a promotion carries non-empty evidence.

- **[proven]** the 11-rule deterministic validator + the promotion state machine + the
  contradiction-path rule exist in the reference build.
- **[proven]** agents are routed by ontology, gated deterministically, and self-validate
  (cross-family review; reviewer ≠ author).
- **[hypothesis]** in pilot-1 the **owner decision stays human** and the autonomous "promotion scorer"
  runs as a **manual periodic review** — the self-maintaining pipeline is the post-pilot target, not the
  pilot deliverable. **We do not sell autonomous scoring.**

## How it is installed (delivery lane)

The four layers install either on your existing tools (**Lane A**), on the Arcanum governance substrate
(**Lane B**), or — the usual answer — a **Hybrid**: operational data + BI on your tools, the governed
promotion core on Arcanum. The lane is chosen during assessment from observable facts (data residency,
scale, agent maturity, dashboard demand). **[proven]** Lane A maps to existing-tool tables/sheets;
**[hypothesis]** Lane B's five bridges are real build items scoped before being promised.

## Generalization claim — stated as a hypothesis

GoldenQuill is the reference implementation in a single vertical (grant intelligence). The claim that
this pattern generalizes to *your* vertical is **[hypothesis]**, which is exactly what the parallel
pilots (cap factory + logistics) are designed to test — independently, then compared.

---

## Claim-tag audit (G-honesty)

Every capability statement in this brief is tagged. Counts below are **substantive bolded claims** in
this document's body (excluding the banner's definition line and this audit table's own references).

| Tag | Count (substantive claims, this file) | Notes |
| --- | --- | --- |
| `[proven]` | 6 | Each cites the GoldenQuill reference build as basis. |
| `[hypothesis]` | 6 | Each names a validation step (pilot / assessment). |
| `[hypothesis / interpretive]` | 1 | The anti-collapse framing — explicitly *not* a proof. |
| untagged capability claims | 0 | None permitted; G-honesty blocks on untagged claims. |

> The counts above are the substantive in-body claims of *this file*. A raw `grep` of `[proven]` /
> `[hypothesis]` will return more occurrences, because it also catches the banner's definition line and
> this audit table's own tag references — subtract those to reproduce the counts. The honesty gate
> requires that no capability claim ships without one of these two tags (`/ interpretive` is a
> qualifier on `[hypothesis]`, not a third class), and that the anti-collapse principle is never
> presented as a proof.
