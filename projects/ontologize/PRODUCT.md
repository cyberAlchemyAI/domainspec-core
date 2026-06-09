# CyberAlchemy — First Product (Candidate)

> **Status: candidate offer.** Synthesized from the GoldenQuill client-package research. Nothing
> here is built or sold yet. Every capability claim is tagged **[proven]** (demonstrated in
> GoldenQuill, with a source path in [L0-corpus.md](levels/L0-corpus.md)) or **[hypothesis]**
> (carries a validation step). No pricing, contracts, or named clients are committed.

## The offer (one sentence)

**CyberAlchemy installs an ontology + DAG layer over a company's existing data and agents, turning
scattered runs and dashboards into a governed learning loop with auditable business intelligence.**

## Who it's for

Companies that (a) serve multiple customer segments through multiple value mechanisms, (b) already
have dashboards/metrics they don't fully trust, and (c) are starting to run AI agents but lack
governance. Primary buyer: an ops/data or AI lead with an executive sponsor.

## The problem we name

Most companies produce work and dashboards but don't _learn_ from outcomes systematically:

- Metrics collapse — a single number (win rate, conversion, NPS) can fail in two independent ways one
  number cannot see: **concept erasure** (the schema drops a dimension — lifecycle depth, realization
  gap, evidence quality) and **number hallucination** (the value is distorted — wrong denominator,
  invented rows), and nobody can trace where it came from. **[proven]** GoldenQuill showed flat win-rate
  hides four dimensions. **[hypothesis]** the two-axis framing is an interpretive grounding (see
  DAG-AND-METRICS §5), not a mathematical proof.
- Knowledge is ungoverned — lessons live in staff memory and stale docs; private signal leaks into
  shared "truth," or useful learning never gets reused safely. **[proven]** the promotion DAG exists
  precisely to stop "turning a draft or dashboard number into reusable authority too early."
- Agents are ungoverned — LLM agents run without deterministic guardrails, self-validation, or
  routing rules, so output can't be trusted in a real workflow. **[proven]** the Council + Logician.

## The method — four installed layers

1. **Ontology** — map the company's two orthogonal axes (subject/segment × value-mechanism) as cards
   that configure search vocabulary, evidence schema, language register, and reporting rhythm; match
   them at runtime, never hardcoded. **[proven]** CIC × CLC + the coupling-violation guard.
2. **Data governance register** — install a signed field→authority-class register that gates where
   data may travel (cloud vs local, internal vs shareable), fail-closed. **[proven]** classification
   register + routing postures.
3. **Promotion DAG (governed learning loop)** — wire operational runs into events → evidence →
   candidate → review gates → owner decision → promoted/retired, enforced by deterministic rules
   (source-truth, contradiction path, privacy redaction, metric≠authority). **[proven]** the 11-rule
   L0 validator + state model.
4. **Evidence-linked BI + governed agents** — rebuild KPIs so each traces to its evidence chain
   (anti-collapse, anti-drift), carries an explicit `veracidade` grade + `evidence_refs` (so BI is
   _graded_, not just traceable), and emit counterfactual receipts; route the agent workforce by ontology
   and govern it with deterministic gates + per-agent self-validation. **[proven]** KPI families +
   CycleReceipt + Council/Logician/cross-family rigor. **[hypothesis]** the per-node veracidade grade is
   an adaptation, validated in the pilot.

## What proves it works

GoldenQuill is the **reference implementation**: in the grant-intelligence vertical, ontology
(cards/registers) + DAG (promotion graph) measurably restructured BI (evidence-linked KPI families,
auditable receipts) and agent work (a routed, self-validating, deterministically-gated council). The
product generalizes that single-vertical proof. **[proven for grants / hypothesis for other verticals]** —
the cross-vertical claim is what a first pilot must validate.

## Engagement shape (candidate)

1. **Assessment** — map the two ontology axes; inventory data sources and existing agents; score
   agent maturity against the Four Autonomy Rules.
2. **Design** — propose ontology cards, classification register, promotion DAG, and KPI taxonomy;
   surface the owner decisions (who approves reuse, what stays private, review cadence).
3. **Pilot** — install one thin slice (one segment × one mechanism, one learning loop) and prove
   evidence-linked metrics on the client's real data.
4. **Handoff** — deliver the layered client package + a current→target transition plan; train owners
   on the governance gates.

## Deliverable

A layered, client-sendable package — overview, executive brief, reference appendix (KPI/ontology
taxonomy), and an open-decisions sheet that becomes the implementation spec. **[proven]** template
lifted from the GoldenQuill client package.

## Honesty / guardrails

- The cross-vertical generalization is a **hypothesis** until a non-grant pilot proves it.
- GoldenQuill gaps we inherit and must address (or list as backlog): meta-metrics on whether the
  governance layer itself works (the per-node `veracidade` field opens one — *what fraction of promoted
  KnowledgeProjections were `veracidade: high` at decision time?*); buyer-readiness scaffolding;
  consequence/cost statements per decision; an explicit current→target transition plan; failure modes
  in buyer language.
- The anti-collapse "concept erasure vs number hallucination" framing is borrowed as an interpretive
  principle from the DomainSpec two-layer framework; the underlying Lean result is about data migration
  and is silent on metrics — we do not claim a proof that KPIs cannot collapse.
- No pricing, contract terms, or named client engagements are authorized in this artifact.

## Why "CyberAlchemy"

The transmutation framing fits the method: ontology + DAG turn the base material a company already
has (raw runs, noisy dashboards, ungoverned agents) into something trustworthy and reusable
(governed knowledge and auditable intelligence). The name is a positioning candidate, not a
committed brand.
