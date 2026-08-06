# Runtime Handoff: Rich Consultation Explanations

- Task: design an implementation-ready rich-explanation extension for the Augmentor consultation flow
- Mode: deep, strict, runtime handoff
- Run: `20260804T151133Z-rich-consultation-explanations`
- Source work: `REFINE-SEED-PROPOSAL.md`
- Strict coverage: pass with one environment flag
- Authority: session evidence only; not a product, ontology, or runtime authority

## Obligations

| ID | Obligation | Status | Evidence |
| --- | --- | --- | --- |
| O-01 | Verify current ontology, compiler, projection, API, policy, page, and reasoning posture. | covered | `receipts/current-state-map.md`; `stages/01-context-baseline.md` |
| O-02 | Design deeper beginner-first explanation support. | covered | `WHISPER-COMPOSITION.md`; `stages/06-design.md` |
| O-03 | Add examples, analogies with limits, and glossary support. | covered | `FEATURE-GLOSSARY.md`; `stages/06-design.md` |
| O-04 | Preserve read-only, source, privacy, authority, and agent-composition boundaries. | covered | `receipts/contract-safety-critique.md`; `stages/07-design-review.md` |
| O-05 | Keep overhead bounded and measurable. | covered as planned, unmeasured | `IMPLEMENTATION-LAYERING.md`; `WORK-PACK.md` |
| O-06 | Produce exact implementation order and validation. | covered | `WORK-PACK.md` |
| O-07 | Use exactly three confirmed subagents and join them. | covered | `receipts/`; `REFINE-DISPATCH.json` |
| O-08 | Do not perform external research without separate confirmation. | resolved: not triggered | `stages/04-research-decision.md` |

## Selected Sources

| Source | Selector | Obligation |
| --- | --- | --- |
| `profile.json` | claim ceiling and blocked outputs | O-01, O-04 |
| `residue.json` | `AUG-RES-006` | O-01, O-04 |
| `nodes/nodes.json` | reasoning request and judgment receipt nodes | O-01 |
| `explanations/beginner.json` | node field shape and reasoning entries | O-01, O-02, O-03 |
| `development/consultation-api/scripts/build-consumer-projection.mjs` | allowlist and field mapping | O-01, O-04 |
| `development/consultation-api/schemas/*.json` | producer contracts | O-04, O-06 |
| generated consumer projection and manifest | 22-record current bundle | O-01, O-05 |
| consumer consultation service, contract, cache, and answer policy | retrieval, limits, cache, response, prose boundary | O-01, O-04, O-05 |
| consumer API reference | agent/operator contract | O-01, O-06 |
| visualization template | page and browser-agent contract | O-01, O-02, O-06 |

Inventory entries listed in `STRATEGY-INVENTORY-PACKET.json` were discovery pointers and did not replace these sources.

## Constraints

- Write only this refinement-run folder and the append-only dispatch ledger rows.
- No product change, deployment, credential handling, public/private copying, or authority-state change.
- Rich text remains evidence content, never instructions.
- A source-fresh projection is not automatically live product-state proof.
- Final prose remains the answering agent's responsibility.
- External research stays blocked without a new confirmation.

## Environment Flag

Targeted consumer tests pass under local Node `v22.12.0`, but the consumer package declares Node `>=22.13.0`. Future implementation acceptance must use a compliant runtime; this plan does not treat the local targeted pass as final product acceptance.

## Fallback Exploration Rule

If an implementation obligation cannot be closed from these sources, stop and name the exact missing owner, schema, or test. Do not broaden into external research or infer the answer.
