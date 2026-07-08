---
tags: [ontologize, ontology-building, subagent-dispatch, prior-art-research, node-schema, anti-bias]
node_type: discovery
is_session: true
layer: architecture, ontology
nature: explanatory, technical
status: active
created: 2026-07-08
timestamp: 2026-07-08T13:21:12-03:00
expires: 2026-09-06
conversation_id: 2026-07-08-enterprise-ontology-research
decisions_made: true
contradictions_found: false
specs_updated: [projects/ontologize/research/2026-07-07-enterprise-ontology-building/research.md, projects/ontologize/research/2026-07-07-enterprise-ontology-building/findings.md, telemetry/agents/subagents-dispatch.yaml]
promoted_candidates: []
expected_importance: 5
importance_rationale: "Produced a cited, adversarially-tested verdict on which parts of the ontologize design are genuinely novel vs standard prior art, but yielded no vault-node contradiction, no code change, and no canonical mechanism — context for a citations/positioning decision the user explicitly deferred."
---

# How ontologies are built inside companies — a prior-art dispatch, and where ontologize actually stands

## Summary

The session opened as grounded Q&A: the user drilled into three pieces of the ontologize vocabulary — the node schema (`ontology-node.schema.json`), "system ontology" in its two senses, and the four-branch B1/B2/B3/B4 model — which I explained from source rather than reproducing jargon. The user then asked to design, then run, a research fan-out on "how ontologies are built inside companies," wanting per-agent angles, a synthesizer, reviewers, and a final evaluator. I proposed an 8-agent sheet via the dispatch router (4 pairwise-tensioned explorers → synthesizer ◀zig-zag▶ 2 skeptics → auditor) and, on the user's confirmation, ran it end-to-end through the full machinery. The check-tension gate REJECTED the first sheet (two explorer pairs cited the skeptics-only "attack" axis), and passed after I relabeled onto in-group axes and re-ran with two fresh independent agents. The dispatch (`2026-07-07-enterprise-ontology-building`) was registered, the four explorers retrieved and read real external sources, the synthesizer reconciled them onto the five commitments, two skeptics attacked from independent axes, the synthesizer revised once, and the auditor ACCEPTED. The load-bearing finding: most of the ontologize design (typed nodes, edge governance, promotion governance) is standard prior art re-typed — BFO/OWL2/SHACL/schema.org/DAMA own it — and only the divergence-preserving (anti-functorial) bridge edge is distinctive-and-owned, justified by the cross-repo `M6Counter.lean` no-go. The anti-bias design paid off concretely: the precedent skeptic grep'd the repos and demoted two of the synthesizer's "discoveries" to self-citation of owned, schema-enforced architecture, and showed CQL's constraint-preservation does not transfer to a drift-preserving bridge. Deliverables `research.md` + `findings.md` were written to the research folder and the ledger was closed cleanly (exit_reason `resolved`, two appends). In the closing discussion I gave a deflating but honest read on practicality: the bridge is a real drift-discipline (~70% already in the schema) whose value is defensive, but it is inert without real runtime evidence feeding `OutcomeEvent`/`MetricObservation`. The user decided NOT to add prior-art citations now, and elected to close.

## Open questions

- Does real runtime evidence actually flow into `OutcomeEvent` (B2) and `MetricObservation` (B3), or is the anti-functorial bridge comparing intent against an empty side? The whole practical value of the one distinctive commitment hangs on this, and it is currently unknown.

## Next steps

- Inspect the ontologize implementation to determine what actually produces `OutcomeEvent`/`MetricObservation` instances — establishing whether the bridge has real operands before any further bridge work or cadence/threshold tuning.

## Recommendation

- The keystone is the **runtime-operand check** (Next step 1). The dispatch established that the bridge edge is the single distinctive-and-owned asset, but `findings.md` also concluded it is worthless without real B2/B3 telemetry to compare — so verifying the observed side is fed is the cheapest move that decides whether any of the "distinctiveness" is real in practice. This is a hunch on priority, licensed by the findings' explicit "comparison operator with nothing to compare" conclusion, not a validated fact. It should precede both the deferred citations work and the cadence/threshold residue.

## Files touched

- projects/ontologize/research/2026-07-07-enterprise-ontology-building/research.md
- projects/ontologize/research/2026-07-07-enterprise-ontology-building/findings.md
- telemetry/agents/subagents-dispatch.yaml
