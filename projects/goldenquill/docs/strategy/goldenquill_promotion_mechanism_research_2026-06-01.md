---
title: GoldenQuill Promotion Mechanism Research
date: 2026-06-01
status: proposal-only
route: docs/strategy/goldenquill_promotion_mechanism_route_2026-06-01.dispatch.json
related:
  - docs/strategy/goldenquill_ontology_dag_grant_research_synthesis_2026-06-01.md
  - arcanum/arcana/ontology-vault/development/schema-validation-plan/GOVERNED-CANDIDATE-BUNDLE.md
---

# GoldenQuill Promotion Mechanism Research

## Research Question

How should GoldenQuill promote grant-writing knowledge from source evidence,
draft behavior, review signals, and run residue into reusable memory or ontology
without collapsing candidate evidence, review judgment, operational success, and
canonical authority?

## Core Finding

The promotion mechanism should be a governed bridge, not a memory write path.

Promotion should move a candidate through explicit gates:

```text
captured evidence
  -> candidate relation
  -> reviewed bridge validation
  -> owner decision
  -> promoted governed artifact or rejected/retired residue
```

The most important design rule is separation of states:

- evidence capture is not promotion;
- retrieval is not authority;
- review is not truth;
- draft use is not reuse permission;
- operator approval for one proposal is not global memory promotion;
- generated state is not canonical unless a promotion owner says so.

This mirrors the GoldenQuill evidence rule that application stage, final
outcome, and validation state must not collapse into one field.

## Existing Groundwork

### GoldenQuill MemoryEvidencePacket

`MemoryEvidencePacket` already exists as a narrow evidence reference schema:

- `packet_id`
- `created_utc`
- `source_path`
- `authority_class`
- `org_scope`
- `retrieval_surface`
- `freshness_signal`
- `mutation_permission`
- `downstream_consumer`

It does not currently carry `allowed_uses`, `promotion_owner`, review gate,
contradiction path, target artifact, or promotion outcome. That is good news:
the packet can remain an evidence reference rather than becoming the promotion
mechanism itself.

### Ontology Vault PromotionRecord Candidate

Ontology Vault already has a candidate `promotion_record` shape in the
branch-aware schema bundle. The validator requires a real PromotionRecord to:

- use `entry_type: PromotionRecord`;
- have at least one target relation;
- point to evidence;
- name a review or validation gate;
- carry a contradiction path.

It also enforces that promoted entries require:

- `governance.promotion_state: promoted`;
- no open `promotion_blockers`;
- reviewed evidence or a decision record.

This is the closest existing mechanism to the desired GoldenQuill promotion
path.

### Inventory Evidence Cards

Inventory evidence-cards already include `promotion_owner`, selector-level
source references, trace, residue, and downstream non-authority language.

Inventory is therefore a strong capture and lookup source, but it must remain a
non-authority handoff surface until Ontology Vault, Definitions Governance,
GoldenQuill card governance, org-vault governance, or another lifecycle owner
accepts the candidate.

### GoldenQuill DAG Research

The ontology-DAG research already concluded that GoldenQuill should use typed
edges such as:

- `evidenced_by`
- `contradicted_by`
- `tested_by`
- `scored_by`
- `approved_by`
- `promoted_by`
- `retired_by`
- `forbidden_for_use`

The promotion mechanism should reuse this graph vocabulary instead of creating a
separate prose-only approval note.

## Promotion Unit

The smallest coherent unit is a `PromotionCandidate`.

It should not be identical to an evidence packet. It should reference evidence
packets and graph edges.

Minimum fields:

```json
{
  "candidate_id": "pc-2026-06-01-example",
  "candidate_kind": "claim | relation | card_delta | lesson | ontology_entry | org_memory | definition | gate_rule",
  "source_packets": ["mep-2026-06-01-example"],
  "target_owner": "ontology_vault | inventory | definitions | card_ceremony | org_vault | lessons_memory | logician | operator",
  "target_artifact": "path or governed handle",
  "proposed_relation": "promotes_to | supersedes | retires | constrains | validates",
  "allowed_uses": ["orient", "draft_support", "decision_input"],
  "current_state": "captured | candidate | reviewed | decision_pending | promoted | rejected | retired | contradicted",
  "review_gate": "decision-gate | logician-gate | card-review | operator-approval | validation-fixture",
  "contradiction_path": "path or procedure for counterevidence",
  "promotion_blockers": [],
  "decision_record": null
}
```

## State Model

Promotion should use a finite state model:

| State | Meaning | May Be Reused? |
| --- | --- | --- |
| `captured` | Evidence exists with provenance. | No, except as source lookup. |
| `candidate` | A relation or learning is proposed. | Only as proposal-only context. |
| `reviewed` | A gate or reviewer checked the candidate. | Only within named allowed uses. |
| `decision_pending` | Owner decision is required. | No additional reuse. |
| `promoted` | Owner accepted into governed target. | Yes, within target rules. |
| `rejected` | Owner declined promotion. | No, preserve as residue. |
| `retired` | Previously useful item is superseded or stale. | No, except history/audit. |
| `contradicted` | Counterevidence defeats or blocks the candidate. | No, preserve contradiction path. |

## Owner Matrix

| Target | Promotion Owner | Candidate Input | Required Gate |
| --- | --- | --- | --- |
| ontology relation | Ontology Vault | `PromotionCandidate` + evidence packets + bridge validation | `PromotionRecord` review |
| evidence lookup card | Inventory | source refs + selector trace + residue | inventory lint/validate |
| canonical definition | Definitions Governance | term candidate + usage evidence | definition drift check |
| GoldenQuill card delta | Card ceremony or card governance owner | card concept + signed/working-YAML boundary | card validator or ceremony decision |
| org memory | org-vault owner/operator | single-org evidence only | org authorization and mutation gate |
| reusable lesson | lessons memory owner | run residue + reflection packet | lesson promotion review |
| Logician gate rule | Logician owner | repeated hard-fail pattern + fixtures | deterministic validator |

## Promotion Guards

1. Evidence input must never claim promoted ontology authority.
2. Inventory handoff must include non-authority language.
3. Working YAML retrieval must not imply signed-card authority.
4. Cross-org material cannot promote into workspace-global memory.
5. Proposal prose cannot promote a source fact.
6. Judge or Editor output can be review evidence, not truth by itself.
7. Promoted entries require no open blockers.
8. Every promotion requires a contradiction path.
9. Generated state must remain generated unless explicitly promoted.
10. Promotion cannot mutate canonical templates, cards, definitions, org memory,
    or ontology without the owning lifecycle route.

## Open Design Questions

1. Should `PromotionCandidate` live inside GoldenQuill, Ontology Vault, or as a
   bridge artifact between them?
2. Should GoldenQuill implement a local validator first, or pressure-test the
   Ontology Vault `PromotionRecord` candidate with GoldenQuill fixtures?
3. Is `allowed_uses` owned by the candidate, the target owner, or both?
4. Which owner decides promotion into reusable grant strategy: operator,
   Logician, lessons memory, or a future GoldenQuill learning council?
5. Should `MemoryEvidencePacket` remain read-only evidence, or gain optional
   `allowed_uses` only after a schema gate?

## Invoke Refresh: Real-World Outcome Evidence

Grant writing needs outcome evidence that is richer than `won` or `lost`.
GoldenQuill should track how far each grant traveled through the real-world
lifecycle and what was learned at each stage.

Source-backed lifecycle evidence should include:

- opportunity discovered;
- eligibility matched;
- go/no-go approved;
- LOI submitted;
- full application invited;
- application submitted;
- portal validated;
- agency retrieved;
- agency tracking assigned;
- under review;
- feedback received;
- award recommended;
- awarded;
- declined;
- withdrawn;
- post-award active;
- reporting current;
- closed out.

The Grants.gov lifecycle supports this split: pre-award, award, and post-award
are distinct phases, and Grants.gov status tracking ends before many agency
decision events. Therefore GoldenQuill should distinguish:

- `portal_status`: what the submission portal knows;
- `agency_status`: what the funder or agency later reports;
- `outcome_event`: the source-backed decision or post-award event;
- `learning_candidate`: what GoldenQuill thinks should be reused.

External KPI research also argues against measuring grant writing only by win
rate. GoldenQuill should track:

- count win rate: awards / final decisions;
- dollar win rate: awarded dollars / requested dollars;
- stage-depth score: deepest lifecycle stage reached;
- agency retrieval rate;
- review reached rate;
- feedback received rate;
- resubmission success rate;
- repeat-funder win rate;
- new-funder conversion rate;
- grant retention rate;
- amount awarded;
- amount requested;
- award realization ratio;
- cycle time from discovery to submission;
- cycle time from submission to decision;
- evidence gap resolution rate;
- reviewer objection resolution rate;
- compliance pass rate;
- relationship touchpoints;
- collaboration artifacts;
- reporting burden hours.

The grant evidence-state model keeps application stage, final outcome, and
validation state separate:

```text
application status != outcome truth
outcome notification != reusable lesson
review feedback != source truth
dashboard KPI != promotion authority
post-award report accepted != validation that the original proposal claims were true
```

So real-world outcome evidence can feed promotion, but cannot itself promote a
claim. A rejection can promote a lesson only after the rejection notice,
reviewer comments, proposal context, and owner decision are represented as
separate source-backed nodes.

## Research Verdict

Use the existing `MemoryEvidencePacket` as evidence input, adapt Ontology
Vault's `PromotionRecord` as the governing promotion decision shape, preserve
Inventory as non-authority capture, and design a GoldenQuill-specific
`PromotionCandidate` bridge with typed states, owner routing, allowed uses,
review gates, and contradiction paths.
