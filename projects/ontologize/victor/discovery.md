---
node_type: handoff
status: exploratory
topic: ontologize — what "ontology" means here, built bottom-up (session handoff for Victor)
last_updated: 2026-06-10
created_by: session-handoff (invoke handoff)
pattern_reference: ../../goldenquill/victor/discovery.md
---

# Handoff — "What is an ontology?" in ontologize, from one node up to the whole model

> Orientation document for Victor. Plain language, concrete first, then the abstraction.
> Every claim points to the file it came from. Everything authored this session is a
> **candidate** — nothing is promoted to canonical Arcanum or CyberAlchemy vocabulary, and the
> GoldenQuill project stays read-only source. Candidate/unproven items are marked ⚠️.
>
> Patterned on [`goldenquill/victor/discovery.md`](../../goldenquill/victor/discovery.md) (same
> concrete→abstract walk, same "cite the file" discipline). Where that doc explains a *product*,
> this one explains a *definition and a schema* — what the word "ontology" was made to mean here,
> and the machine shape of one node.

## Objective

Let Victor reason about the work done this session: we took the project's scattered vocabulary
(six node types, four branches, an edge catalog) and produced (a) a **candidate canonical
definition of "ontology"** and (b) a **proposed node schema** that a machine can check. This doc
walks from the most concrete thing — a single node on disk — up to the abstract claim about what
an ontology *is*.

---

## 0. What changed this session (the concrete artifacts)

Six files, all under [`projects/ontologize/`](../), all candidate:

| File | What it is |
|---|---|
| [`definitions/DEFINITIONS.md`](../definitions/DEFINITIONS.md) | The new canonical definitions: **DEF-ONT-001 "Ontology"** + node, branch, edge. |
| [`definitions/DEFINITIONS-INDEX.md`](../definitions/DEFINITIONS-INDEX.md) | Lookup table + N1–N6 quick reference. |
| [`definitions/DEFINITION-DRIFT-AUDIT.md`](../definitions/DEFINITION-DRIFT-AUDIT.md) | Reconciles the new definitions against the existing glossary/branches/DAG docs. |
| [`schemas/ontology-node.schema.json`](../schemas/ontology-node.schema.json) | The machine shape of one ontology node (JSON Schema). |
| [`examples/ontology-node.logistics-on-time-delivery.json`](../examples/ontology-node.logistics-on-time-delivery.json) | A real node that validates against the schema. |
| [`ontology-definition-and-node-schema.dispatch.json`](../ontology-definition-and-node-schema.dispatch.json) | The governed route that produced all of the above (passes the validator). |

---

## 1. Start concrete: one node

Here is a single ontology node, exactly as it sits on disk
([examples/ontology-node.logistics-on-time-delivery.json](../examples/ontology-node.logistics-on-time-delivery.json)):

```json
{
  "node_id": "node.mo.on-time-delivery-lane-ab",
  "node_type": "MetricObservation",
  "branch": "B3-run-context",
  "label": "On-time delivery, lane A to B",
  "run_context_ref": "node.ls.shipment-2026-q2",
  "veracidade": "high",
  "evidence_refs": ["tms-event:delivered#2026-04..06", "tms-event:delivery_exception#2026-04..06"],
  "denominator": {
    "numerator": "shipments delivered on or before promised date",
    "denominator": "shipments delivered (not booked) in the period",
    "period": "2026-Q2"
  },
  "interpretation_limits": ["Divides by delivered, not booked: does not count cancellations."],
  "edges": [
    { "edge_type": "observed_by", "target_node_id": "node.ls.shipment-2026-q2", "category": "structural" },
    { "edge_type": "drifts_from", "target_node_id": "node.kp.lane-ab-sla-rule", "category": "structural" }
  ]
}
```

Read it left to right and you have the whole idea in miniature:

- **It is one typed assertion.** `node_type: MetricObservation` — it is a *measurement*, not an
  event, not a rule, not a decision. There are exactly six types (next section).
- **It knows which branch of reality it lives in.** `branch: B3-run-context` — it is a per-run
  number, scoped to a specific run (`run_context_ref`), not a timeless fact.
- **It carries its own honesty.** `veracidade: high` says "this is tested against reality," and
  because it claims `high` it is *forced* to list `evidence_refs` — you cannot claim "proven"
  without receipts. The `denominator` block stops the classic lie ("on-time ÷ *delivered*, not ÷
  *booked*").
- **Its relationships are typed, not freeform.** Each edge has an `edge_type` from a fixed
  catalog. `drifts_from` here points at a promoted rule — it says "actual behavior is diverging
  from what we intended," which is the raw signal the whole improvement loop runs on.

That single node is the atom. The rest of this doc is just "what are the legal atoms, how do they
connect, and what do you get when you have a whole graph of them?"

---

## 2. The six legal node types (the concrete vocabulary)

Every node is exactly one of these. Adapted from GoldenQuill's `validate.py` (5 types) plus one
([DAG-AND-METRICS.md §2](../DAG-AND-METRICS.md), [DEF-ONT-002](../definitions/DEFINITIONS.md#def-ont-002--ontology-node--candidate-canonical)):

| #  | Type                  | Branch        | In one line                                        | Carries evidence? |
|----|-----------------------|---------------|----------------------------------------------------|-------------------|
| N1 | **OutcomeEvent**      | B2 system     | a real-world event that happened (must cite a source) | no — its honesty is the mandatory `source` |
| N2 | **LifecycleState**    | B3 run-context| how far a run got (stage ≠ outcome)                | no |
| N3 | **MetricObservation** | B3 run-context| a number with an honest denominator (our example)  | **yes** |
| N4 | **PromotionCandidate**| B4 bridge     | a proposed lesson, not yet trusted                 | **yes** |
| N5 | **OwnerDecision**     | B4 bridge     | a human approve / reject / retire / contradict     | no — the decision *is* the commitment |
| N6 | **KnowledgeProjection**| B1 meaning   | a lesson that got promoted into the store          | **yes** |

The three "evidence-bearing" types (N3/N4/N6) carry `veracidade` (high/medium/low) + `evidence_refs`.
⚠️ The "primary branch" column is a **new mapping introduced this session** — it's consistent with
the existing branch↔DAG mapping but wasn't previously stated 1:1 (see Open Question A).

---

## 3. The schema is the gates, written down

[schemas/ontology-node.schema.json](../schemas/ontology-node.schema.json) is "what a node must look
like" made machine-checkable. The interesting part isn't the field list — it's that the schema
encodes the project's *honesty rules* as conditional requirements, so a malformed node fails
validation instead of slipping through prose review:

- `OutcomeEvent` ⇒ must carry `source` (no event without provenance).
- `MetricObservation` ⇒ must carry a `denominator` block.
- `PromotionCandidate` ⇒ must carry a `contradiction_path` (how it could be proven wrong).
- `KnowledgeProjection` ⇒ must be `record_kind: promotion_record` with non-empty evidence.
- **Any** node claiming `veracidade: high` ⇒ must list `evidence_refs`.

The example node in §1 validates against this schema as-is (verified this session). So "an honest
node" is now a thing a script can confirm, not a thing a reviewer has to vouch for.

---

## 4. Now the abstraction: what *is* an ontology, then?

Here is the jump from concrete to abstract. One node is one assertion. A glossary would stop at
"an ontology is an explicit model of a company's concepts." The canonical definition we wrote
([DEF-ONT-001](../definitions/DEFINITIONS.md#def-ont-001--ontology--candidate-canonical)) is
deliberately **stronger**. It says a body of knowledge is an ontology *in this project's sense*
only when **all five** of these hold:

1. **Branched, not flat** — knowledge is split into B1 meaning / B2 system / B3 run-context /
   B4 bridge, so *what we intend* (B1) stays separate from *what actually happened* (B2/B3) and
   the gap between them (drift) is visible instead of smoothed away.
2. **Typed nodes** — every assertion is one of N1–N6 (§2). The type set is the vocabulary.
3. **Edge-governed** — every relationship obeys the edge catalog (a typed contract: which
   source-type may point at which target-type, cardinality, inverse, acyclicity).
4. **Two orthogonal DAGs** — an immutable execution record (what happened, in order) kept apart
   from the ontology graph (what it means / what becomes reusable); the second references the
   first but never rewrites it.
5. **Promotion-governed** — knowledge earns reuse authority only through
   evidence → candidate → owner decision → projection, with `veracidade` + `evidence_refs` on
   every evidence-bearing node. Nothing auto-promotes.

The slogan: a company "has an ontology" here when its knowledge is **branched, typed,
edge-governed, evidence-graded, and promotion-gated** — not merely catalogued. The single node in
§1 is one drop of that; the definition is the shape of the whole reservoir.

**Why bother making it stronger than the glossary?** Because the weak version ("an explicit model
of concepts") is satisfied by any tidy spreadsheet, and a spreadsheet can't tell intended from
actual, can't say how confident it is, and can't stop a bad lesson from being trusted. The five
commitments are exactly the properties that let the system *improve safely over time* — which is
the product's actual selling point.

---

## 5. How this was produced (the governance layer)

The whole thing ran as a governed dispatch route
([ontology-definition-and-node-schema.dispatch.json](../ontology-definition-and-node-schema.dispatch.json),
validated `pass`): gather existing definitions + node types → author the canonical definitions
under `definitions-governance` → propose the node schema → validate. The point of routing it
this way (rather than just writing files) is provenance: every gate is named, the "no promotion to
canonical without owner review" guardrail is explicit, and GoldenQuill stays read-only. If you want
to see *why* a given choice was made, the dispatch is the audit trail.

---

## 6. Open questions (for Victor)

Each is one question, one current stance.

1. **Is the node-type → branch mapping real, or did we invent it?** ⚠️ DEF-ONT-002 assigns each
   of N1–N6 a single "primary branch." That 1:1 wasn't previously stated — the prior docs map
   *branches → DAGs*, not *node-types → branches*. *Stance:* keep it candidate; confirm against
   the engine spec in assessment. (Drift finding D5.) The schema currently **hard-pins** each
   type's branch — that may be too strong before owner review; easy to relax to "expected branch."
2. **Are all five commitments really necessary?** ⚠️ The definition claims a model is an ontology
   only if *all five* hold. The contradiction path: if a client gets durable BI value with only
   some (say typed + evidence-graded but un-branched), the "all five" claim is falsified and the
   definition should weaken to a *graded* one (a thing is an ontology *to the degree* it satisfies
   the five). *Stance:* test in the pilot.
3. **Which way does the canonical definition point — inward (governance) or outward (sales)?** The
   glossary's "Ontology [generic]" is the elevator pitch; DEF-ONT-001 is the contract. *Stance:*
   keep both, with the generic one back-referencing the canonical one. Decide if the five
   commitments are also the *client-facing* promise or just the internal build standard.
4. **Two load-bearing terms are still undefined as canon** — `record_kind` and
   `proposed/approved_allowed_uses` gate the promotion flow but live only inline in DAG-AND-METRICS.
   *Stance:* promote to DEF entries if they recur in client artifacts.

---

## Connections

- This session's artifacts: [definitions/](../definitions/), [schemas/ontology-node.schema.json](../schemas/ontology-node.schema.json),
  [the dispatch](../ontology-definition-and-node-schema.dispatch.json).
- Upstream design this builds on: [DAG-AND-METRICS.md](../DAG-AND-METRICS.md) (nodes/edges/gates),
  [ONTOLOGY-BRANCHES.md](../ONTOLOGY-BRANCHES.md) (the four branches),
  [PRODUCT.md](../PRODUCT.md) (the consulting offer this serves).
- Pattern source for this doc: [goldenquill/victor/discovery.md](../../goldenquill/victor/discovery.md).
