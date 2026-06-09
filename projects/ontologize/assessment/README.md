# Assessment Instrument — CyberAlchemy ontology+DAG engagement

> **Status: candidate.** This is a blank, repeatable intake instrument synthesized from the
> ontologize design. Nothing here commits pricing, contracts, or named clients. "cap factory" and
> "logistics company" appear only as **pilot references**. Every method assertion is tagged **[SB]**
> source-backed (with a path) or **[H]** hypothesis. Sources are read-only. — *candidate-only.*

The assessment is the **L0 / Slice S1** intake step ([PLAN.md](../PLAN.md) IDS-1, [WORK-PACK.md](../WORK-PACK.md)
T1). It is filled **once per vertical** and produces the four inputs the rest of the engagement needs:
an `ontology-map`, a `data-inventory`, an `agent-inventory`, and a `maturity-score`. It is
**repeatable** and **vertical-agnostic** — the same instrument fills for cap factory (continuous
production) and logistics (discrete shipments) without structural change. [SB IDS-1 outputs;
[PLAN.md](../PLAN.md):24]

## Files

| File | Role |
| --- | --- |
| [`assessment-template.md`](assessment-template.md) | The blank fillable instrument. Sections A–E + sign-off. This is the artifact a consultant fills with a client. |
| [`maturity-rubric.md`](maturity-rubric.md) | The Four-Autonomy 0–3 scoring rubric with level descriptors per rule. Section D of the template references it. |
| [`worked-example.md`](worked-example.md) | A fully-filled **hypothetical** (clearly labeled illustrative, fabricated). Shows a peer what a complete fill looks like, end to end. |

## How to use (the repeatable procedure)

Fill the template top-to-bottom; the section order **is** the IDS-1 rule order [SB [PLAN.md](../PLAN.md):26-31]:

1. **Section A — Ontology mapping.** Elicit who/what the client serves (subject/segment axis), then how
   value flows (value-mechanism axis), as cards. Run the **orthogonality check** (A.4) before moving on.
2. **Section B — Data inventory.** Sources, systems, event types, residency, scale.
3. **Section C — Agent inventory.** Existing agents, what they do, governance state.
4. **Section D — Four-Autonomy maturity.** Score each of the four rules 0–3 against
   [`maturity-rubric.md`](maturity-rubric.md).
5. **Section E — Lane-selection inputs.** Capture the five observable facts T2b needs.
6. **Sign-off.** Client confirms the map + inventories reflect reality (S1 validation gate).

Per [IDS-1](../PLAN.md) edge cases [SB]: a continuous-production client with **no discrete run** flags
the run-boundary decision in A.3 (do not force one); a client with **no agents** scores
maturity = 0 and the agent layer is greenfield (Section C still gets filled with "none / greenfield").

## IDS-1 output → template section coverage

| IDS-1 required output [SB [PLAN.md](../PLAN.md):24-31] | Where in the instrument |
| --- | --- |
| `ontology-map` = {subject_axis: [cards], mechanism_axis: [cards], match_rule: runtime} | Section A (A.1 subject cards, A.2 mechanism cards, A.4 orthogonality + runtime match rule) |
| card primitives per axis card | A.1/A.2 card fields (search vocabulary, evidence schema, language register, reporting rhythm) + Section A.3 run-context block |
| `data-inventory` (sources, owner, sensitivity) | Section B |
| `agent-inventory` (existing agents) | Section C |
| `maturity-score` (each Four-Autonomy rule 0–3) | Section D + [`maturity-rubric.md`](maturity-rubric.md) |
| orthogonality assertion (reject baked subject→mechanism binding) | Section A.4 (coupling-violation guard) |
| run-boundary decision for continuous-production edge case | Section A.3 (run-context) |
| lane-selection inputs (T2b) | Section E |

## Branch alignment (reconciled naming)

The instrument mirrors the [ONTOLOGY-BRANCHES.md](../ONTOLOGY-BRANCHES.md) structure and uses the names
recommended by [RECONCILIATION.md](../RECONCILIATION.md):

- The subject × mechanism cards populate **B1 — business** (canonical name; "meaning / domain / intent"
  are aliases) [SB [RECONCILIATION.md](../RECONCILIATION.md) §1 decision]. The instrument uses
  **"business"** as the primary axis-grouping name.
- The data inventory (Section B) identifies **B2 — system** sources.
- The run-context block (Section A.3) defines **B3 — run-context** — the run boundary that defines
  metric denominators. Named **run-context** (not "operational ontology") to avoid colliding with the
  arcanum/cyberAlchemy "Operational Ontology = agent-operation knowledge" [SB
  [RECONCILIATION.md](../RECONCILIATION.md) §1 B3 decision].
- The assessment **seeds B4 — bridge** by recording observed drift candidates, but the instrument does
  not promote them (promotion is the pilot's job, T3/T5).

**Existing `cyberAlchemy/ontology/entries` are NOT pulled in.** Per [RECONCILIATION.md](../RECONCILIATION.md)
§2, the single existing entry and the digests are Arcanum/agentic-system meta-governance with no
manufacturing or logistics overlap; the assessment populates **fresh** per-vertical B1/B2/B3 entries.
[SB [RECONCILIATION.md](../RECONCILIATION.md) §2 decision]

## Source of the Four Autonomy Rules

The maturity rubric scores against the **canonical** Four Autonomy Rules: Save State Always · Test Your
Own Work · Be Explicit · Clean Output — defined verbatim in `projects/goldenquill/SOUL.md:40-50` (named
canonical there and by `projects/goldenquill/AGENTS.md:16`), and recorded as source-backed in
[DEFINITIONS.md](../DEFINITIONS.md):56. [SB]

## Guardrails honored

- Candidate-only; no pricing/contracts/named-client commitments/canonical promotion.
- No fabricated client data — the template is blank with field prompts; the worked example is labeled
  illustrative and fabricated.
- Method claims tagged [SB]/[H].
