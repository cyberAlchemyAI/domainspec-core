---
module: body-war-suggested-track-ontology-domainspec-integration
version: current
status: pass
updatedAt: 2026-07-27
docType: distill-validation
runId: distill-bwoi-20260727T172835Z
parentRunId: invoke-bwoi-20260727T172835Z
---

# Distill Validation

## Intent and Budget

- Intent: validate the executable size and recomposition of the drafted
  ontology, DomainSpec, and integration Plan.
- Target context: one existing Body War rule, CT-2.
- Output: medium-complexity split work-pack.
- Optimization goal: independently reviewable tests with one exact integration
  seam.
- Mode: Validate.
- Budget: one Balancer-led pass plus one reconciliation pass.

No subagent dispatch was run. The route had no approved delegation document,
and the serial three-unit boundary was already explicit, so Proposer and
Balancer roles were simulated locally with the same trace fields.

## Role Conversation

| Role | Claim or objection | Category | Reconciliation |
| --- | --- | --- | --- |
| Proposer | Three SWUs match the three requested test verdicts; VERIFY remains closure-only. | proposed unit map | accepted |
| Balancer | W1 follows W0 and may accidentally imply ontology is an input to DomainSpec. | hidden dependency | revised: W1 has an ordering gate but explicitly no semantic/data dependency |
| Balancer | The ontology SWU bundles schema, entries, and two polarities. | atomicity | retained: none has an independent semantic verdict; together they own one admission decision |
| Balancer | The DomainSpec SWU bundles compile and backend comparison. | meaning loss on split | retained: compile-only is structural evidence; CT-2 behavior requires source-derived expectation versus observation |
| Balancer | The integration SWU bundles multiple checks. | task-shaped risk | retained: checks are internal cases of one fail-closed bridge admission; only one integration receipt is accepted |
| Balancer | Candidate ontology might be mistaken for authority. | claim inflation | resolved: candidate-only experimental profile, promoted-required negative control, authority_effect none |
| Balancer | Financial Settlement-specific tooling may be copied. | implementation gap | resolved: generic APIs are exact source anchors; copying the business runner is forbidden |
| Balancer | First unit could still affect upstream ontology. | scope safety | resolved: write scope is only the Body War proof package; CyberAlchemy ontology is forbidden |

## Smallest Coherent Unit

SWU-BWOI-001 is the smallest reversible trust-building unit. It answers one
question—whether CT-2 meaning is coherent in a local ontology fixture—and can
pass or fail without app runtime, DomainSpec compilation, bridge code, or
promotion mutation.

## Recomposition Proof

```text
SWU-BWOI-001 -> ontology receipt
SWU-BWOI-002 -> DomainSpec receipt
both receipts + bridge -> SWU-BWOI-003 integration receipt
all receipts -> TASK-BWOI-VERIFY reproducibility audit
```

There is no hidden glue: every cross-unit dependency is an exact receipt or
bridge handle with a digest.

## Technique Trace

| Technique | Activation | Result |
| --- | --- | --- |
| abstraction-level guard | tests risk mixing meaning, logic and release | kept all units at experimental verification level |
| recomposition proof | three independent tests must form one answer | pass; receipt graph is explicit |
| evolution profile | formal lane may later require promoted ontology | sidecar profile boundary preserved |
| frame-expiry note | profile, ontology lifecycle or app rule may change | exact invalidation triggers recorded below |
| navigable result | Task Session needs one entry point | selected SWU-BWOI-001 and linked task/W0 |
| boundary-object check | bridge crosses ontology and DomainSpec | bridge contains IDs/digests only, no executable logic |
| concept-vs-knowledge status | ontology entries are candidate | candidate state remains visible and non-promoting |
| premortem | integration could pass decoratively | stale-digest and insufficient-state negatives are mandatory |

Skipped:

- tournament: no competing architecture remains;
- requisite-variety expansion: only one rule and one adapter are in scope;
- deep recursive rounds: another split would separate artifacts from their
  only meaningful verdict.

## Hidden Gap Review

- GAP-BWOI-001 is implementation-relevant but not an acceptance blocker because
  the generic compiler, projection, decoder, case, evaluator and proof modules
  exist. Execution must block if they cannot support a consumer-local runner.
- GAP-BWOI-002 is deliberately a negative formal-lane witness.
- GAP-BWOI-003 is avoided by the selected Rule/Operation/Event graph.

## Premortem

Most likely false success: integration reports pass while the ontology binding
is decorative. Guardrail: mutate one bound digest and increase the required
ontology state; both must reject before backend execution.

## Frame Expiry

Rerun Define/Design/Plan if any of these changes:

- CT-2 or its stronger-claim guardrails;
- DomainSpec node-logic schema or development profile digest;
- ontology lifecycle state ordering;
- Body War repository creation result;
- the decision that `body.logic` is the sole executable rule source.

## Verdict

- Smallest coherent unit: pass
- SWU atomicity: pass; task-shaped count 0
- First-unit narrowness: pass
- Recomposition: pass
- Acceptance-critical gaps: none
- Navigation: pass
- Verdict: pass
- Next route: Task Session to SWU-BWOI-001

