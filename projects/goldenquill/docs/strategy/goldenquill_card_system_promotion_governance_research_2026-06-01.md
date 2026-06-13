---
title: GoldenQuill Card System Lessons For Promotion Governance
date: 2026-06-01
status: research-synthesis
observed_capability: dispatch-spec
source_folder: ../card_system_deep_research_2026-05-17/
related_proposal: goldenquill_promotion_governance_proposal_2026-06-01.md
related_architecture: goldenquill_promotion_governance_architecture_design_2026-06-01.md
---

# GoldenQuill Card System Lessons For Promotion Governance

## Executive Summary

The May 17 card-system research is highly relevant to GoldenQuill promotion
governance. It is not only a historical audit of CIC/CLC cards; it is a concrete
case study in what goes wrong when a system has signed artifacts, governance
claims, runtime loaders, gates, amendments, and human approval ceremonies but
does not keep the authority boundary crisp.

The strongest lesson is:

> A claim that something is "locked," "signed," "loaded," "validated," or
> "approved" must name the exact layer where that authority exists.

Promotion governance needs the same discipline. A grant outcome, KPI, reviewer
comment, evidence packet, dashboard label, or candidate lesson can be useful
without being approved reusable knowledge. The card-system audit gives us a
vocabulary of failure modes and guardrails that should be folded into the
GoldenQuill promotion model.

## Source Set Reviewed

This synthesis reviewed:

- [CARD_LIFECYCLE_AND_LOADER_GOVERNANCE_AUDIT.md](../card_system_deep_research_2026-05-17/CARD_LIFECYCLE_AND_LOADER_GOVERNANCE_AUDIT.md)
- [CANONICAL_NAMING_AND_ORTHOGONALITY_AUDIT.md](../card_system_deep_research_2026-05-17/CANONICAL_NAMING_AND_ORTHOGONALITY_AUDIT.md)
- [INITIAL_CTO_HANDOFF_BLOCKERS.md](../card_system_deep_research_2026-05-17/INITIAL_CTO_HANDOFF_BLOCKERS.md)
- [FILE_BY_FILE_PATCH_QUEUE_PRE_V0_2.md](../card_system_deep_research_2026-05-17/FILE_BY_FILE_PATCH_QUEUE_PRE_V0_2.md)
- [PHASED_CARD_SYSTEM_RESEARCH_AUDIT.md](../card_system_deep_research_2026-05-17/PHASED_CARD_SYSTEM_RESEARCH_AUDIT.md)
- [goldenquill_promotion_governance_proposal_2026-06-01.md](goldenquill_promotion_governance_proposal_2026-06-01.md)
- [goldenquill_promotion_governance_architecture_design_2026-06-01.md](goldenquill_promotion_governance_architecture_design_2026-06-01.md)

## Dispatch Result

- Dispatch ID: `goldenquill-card-system-promotion-governance-research-20260601`
- Status: pass
- Mode: research
- Step count: 5
- Patterns: route, fanout, synthesis, validation, handoff
- Handoffs: card-system research -> authority-drift lanes -> promotion-governance mapping -> design backlog
- Subagent strategy: recommended, fanout lanes, requires user permission before runtime execution
- Observability: trace event names included in the dispatch JSON
- Promotion guardrail: pass; the route explicitly forbids treating card-system findings as promoted grant knowledge
- Next route: decision-gate or task-session after operator selects which lessons to adopt

The validated dispatch artifact is:
[goldenquill_card_system_promotion_governance_research_2026-06-01.dispatch.json](goldenquill_card_system_promotion_governance_research_2026-06-01.dispatch.json)

## What The Card-System Audit Teaches

### 1. Signed Or Locked Does Not Mean Fully Applied

The card-system audit repeatedly found documents marked `LOCKED` while the
companion schema, card, or gate body still reflected the pre-lock state.

Examples:

- §18 v1.2 claimed `funder_political_axis` was retired, but the CIC schema and
  six CIC cards still carried the old political-axis routing rows.
- §18.6 v2 claimed multi-track CLC cards existed, but the three target CLC cards
  were still single-track.
- §4 v2.x.7 claimed the value-position coupling gate was live, but the gate body
  still raised `NotImplementedError`.

Promotion-governance implication:

GoldenQuill must not collapse proposal approval, owner approval, source evidence,
metric observation, and reusable knowledge into one status. A grant lesson can
be:

- observed but not checked;
- checked but not generalized;
- generalized but not approved;
- approved for one client only;
- approved for workspace-safe reuse;
- contradicted or retired later.

The promotion model should avoid a single overloaded `approved` or `locked`
state.

### 2. State Machines Must Stay Separate

The card audit found drift between `draft_status`, `runtime_load_status`, and
the binding boolean `runtime_loadable`. The planning text treated one state as
if it answered all questions, while the runtime had a more precise split.

Promotion-governance implication:

GoldenQuill already identified five separate evidence states:

| Promotion State | Why It Must Stay Separate |
| --- | --- |
| application stage | Tells how far a grant moved; does not prove final result. |
| outcome event | Captures source-backed award, decline, withdrawal, feedback, report, or closeout. |
| validation state | Says whether an interpretation, denominator, claim, or feedback reading was checked. |
| graph authority | Says whether the run trace can explain the path and gate history. |
| source truth | Says what the external source actually proves. |

The card-system lesson strengthens this rule: do not let one visible status
stand in for all five.

### 3. Naming Drift Becomes Governance Drift

The card-system audit flagged naming collisions such as visual `Cards` versus
runtime `cards`, plus canonical `Customer Identity Cards` versus legacy
`Customer Information Cards`.

Promotion-governance implication:

GoldenQuill needs stable term separation for:

- evidence packet versus source truth;
- application stage versus final outcome;
- KPI observation versus authority;
- promotion candidate versus owner decision;
- proposed allowed uses versus approved allowed uses;
- org-scoped feedback versus workspace-safe learning.

If these terms drift, the system will eventually confuse "this was observed"
with "this is reusable."

### 4. Orthogonality Is A Promotion Safety Requirement

The card audit's CIC/CLC orthogonality findings are not just card-specific. They
show why concept families need coupling guards. CIC and CLC were supposed to be
separate axes, but field names, values, and gate vocabularies could blur them.

Promotion-governance implication:

Grant promotion needs its own orthogonality guards:

| Boundary | Drift To Prevent |
| --- | --- |
| grant outcome -> KPI | A final outcome being interpreted without denominator or context. |
| KPI -> candidate | A metric threshold becoming approved knowledge. |
| reviewer feedback -> reusable lesson | Private client feedback leaking into workspace-safe reuse. |
| evidence packet -> owner decision | A source reference being treated as approval. |
| candidate -> approved use | Proposed uses becoming final allowed uses before owner decision. |
| dashboard label -> source truth | A UI label being treated as evidence. |

The card system's coupling gates suggest GoldenQuill should have explicit
promotion-coupling checks, not just prose policy.

### 5. Human Confirmation Must Be Modeled, Not Implied

The card-system Law-5 discipline says `common_funders_observed` must contain
operator-confirmed engagement only. Subagent-populated candidates must go under
`_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation`.

Promotion-governance implication:

This maps almost perfectly to grant-learning promotion:

| Card-System Pattern | Promotion-Governance Equivalent |
| --- | --- |
| `common_funders_observed` | approved reusable knowledge or confirmed relationship signal |
| draft funder candidates | unapproved promotion candidates |
| operator engagement confirmation | owner decision |
| Law-5 split | proposed allowed uses versus approved allowed uses |
| `_research_metadata` pending block | private residue / candidate state |

GoldenQuill should preserve this separation: model-generated, subagent-generated,
or metric-generated learning belongs in candidate state until a human owner
decides.

### 6. Runtime Gates And Written Policy Can Diverge

The card audit found gates that existed as named modules but were stubs, while
some enforcement lived in the loader directly. This creates a clarity problem:
the named governance surface and the actual enforcement surface differ.

Promotion-governance implication:

For promotion governance, every claimed gate should identify whether it is:

- policy-only;
- manually reviewed;
- dashboard-observed;
- loader/enforcer-backed;
- validator-backed;
- production-enforced;
- blocked pending future work.

This prevents a client, operator, or engineer from reading a gate name and
assuming it already enforces behavior.

### 7. Patch Queues Are Governance Memory

The card-system patch queue is useful because it groups repairs into batches:
documentation-only, cards-ceremony, gate-body graduation, loader graduation, and
deferred cleanup.

Promotion-governance implication:

GoldenQuill should use similar promotion remediation buckets:

| Bucket | Promotion-Governance Use |
| --- | --- |
| documentation-only | Clarify vocabulary, client promises, and authority language. |
| evidence ceremony | Source-backed outcome import, feedback confirmation, owner signoff. |
| gate graduation | Turn policy guardrails into checks. |
| loader/import graduation | Allow real-world outcome feeds only when source and privacy rules are ready. |
| deferred cleanup | Normalize stale labels, old terms, and ambiguous states. |

The key is not the exact card ceremony model. The key is that repair work is
classified by authority impact.

## Direct Mapping To Promotion Governance

| Card-System Concept | Promotion-Governance Concept | Adopt? | Reason |
| --- | --- | --- | --- |
| Signed card | Owner-approved reusable lesson | Yes, conceptually | Both require source, lifecycle state, and authority boundary. |
| LOCKed amendment | Approved policy or design decision | Yes, with caution | Must distinguish text approval from companion artifact readiness. |
| Companion ceremony | Evidence or reuse approval ceremony | Yes | Prevents approved text from outrunning actual governed state. |
| `runtime_loadable` | `reuse_allowed` or approved-use eligibility | Yes, as a separate axis | Avoids conflating candidate state with active reuse. |
| `content_hash` / signature | Source integrity and decision receipt | Partial | Grant evidence needs source integrity, but not necessarily cryptographic signing in first pass. |
| F-CARDS gates | Promotion governance gates | Yes | Gate names should map to actual enforcement posture. |
| CIC/CLC orthogonality | Evidence/KPI/candidate/owner-decision orthogonality | Yes | Prevents authority drift. |
| Law-5 funder-confirmation split | Candidate versus approved learning split | Strong yes | This is the most directly reusable pattern. |
| Patch queue batches | Promotion remediation roadmap | Yes | Good way to manage gradual hardening. |
| Program Rule Pack routing | Grant compliance/rubric rule packs | Candidate | Useful if GoldenQuill later separates funder rules from grant-run outcomes. |

## New Research Questions To Explore

### RQ-1. What is the promotion equivalent of a signed card?

A signed card represents a knowledge artifact that passed lifecycle, review,
signature, and loadability expectations. The grant equivalent may be an owner
decision with approved allowed uses, source evidence, privacy treatment, and
contradiction path.

Research task: define the minimum fields for an approved reusable grant lesson.

### RQ-2. Should promotion governance have a companion-ceremony status?

The card-system audit shows `LOCKED` is too coarse when text is approved but
companion changes are pending.

Research task: decide whether promotion governance needs states such as:

```text
approved_text_pending_evidence
approved_evidence_pending_privacy
approved_privacy_pending_owner
approved_for_org_only
approved_for_workspace_reuse
```

### RQ-3. What are the promotion orthogonality gates?

The card system has coupling gates for CIC/CLC drift. Promotion governance needs
equivalent drift gates.

Research task: define gates such as:

- KPI cannot create approved reuse;
- source reference cannot create owner decision;
- org-scoped feedback cannot become workspace-safe;
- dashboard status cannot create final outcome;
- candidate cannot carry approved allowed uses;
- reviewer feedback cannot validate funding quality.

### RQ-4. What should be human-confirmed versus model-suggested?

Law-5 is the key precedent. Operator-confirmed engagement belongs in one field;
subagent-populated candidate funders belong elsewhere.

Research task: classify grant-learning fields into:

- model-suggested;
- source-backed;
- operator-confirmed;
- owner-approved;
- workspace-safe.

### RQ-5. How should historical card governance influence the grant DAG?

The promotion DAG currently tracks `precedes`, `consumes`, `emits`,
`blocked_by_gate`, `revised_by`, `approved_by`, and `delivered_as`.

Research task: decide whether the grant DAG also needs explicit edges for:

- `verified_by_source`;
- `candidate_generated_from`;
- `privacy_reviewed_by`;
- `owner_decided_by`;
- `contradicted_by`;
- `retired_by`.

These may remain promotion-layer edges instead of execution-run edges.

## Recommended Follow-Up Dispatch

Run a focused fanout across five lanes:

1. **Authority States Lane**
   Extract card lifecycle/signature/loadability states and propose promotion
   state axes.

2. **Orthogonality Lane**
   Map CIC/CLC coupling controls to grant evidence/KPI/candidate/decision
   coupling controls.

3. **Human Confirmation Lane**
   Use Law-5 as the model for source-backed versus human-confirmed grant
   learning.

4. **Ceremony And Drift Lane**
   Study `LOCKED`-but-not-applied drift and propose promotion companion-status
   labels.

5. **Rule-Pack Lane**
   Explore whether program rule packs should become a separate GoldenQuill
   layer for funder/compliance rules, distinct from outcome-learning promotion.

The dispatch JSON beside this file encodes that route.

## Immediate Design Recommendations

1. Add a promotion-authority state split modeled after the card-system lifecycle
   split: candidate, validated, privacy-reviewed, owner-approved, retired, and
   contradicted should remain separate from source-backed outcome status.
2. Add an explicit "companion readiness" concept for any promoted lesson whose
   approval depends on later evidence, redaction, or owner review.
3. Add a Law-5-style split for grant-learning provenance:
   model-suggested, source-backed, operator-confirmed, owner-approved.
4. Add promotion orthogonality gates to prevent evidence, metrics, feedback,
   candidates, and owner decisions from collapsing into one authority surface.
5. Treat card-system "signed card" as an analogy, not a direct implementation
   requirement. Grant lessons may not need cryptographic signing immediately,
   but they do need source, decision, and contradiction receipts.
6. Keep PRP-style compliance rules separate from grant outcome learning. Funder
   rules and grant-run results should meet at the responsiveness map and gates,
   not merge into one artifact.

## Open Gaps

| Gap | Why It Matters |
| --- | --- |
| Promotion approved-use lifecycle is not yet as detailed as card lifecycle. | Needed to prevent status overload. |
| There is no named promotion equivalent of `runtime_loadable`. | Needed to distinguish "approved exists" from "may be reused now." |
| Companion-readiness status is not yet modeled. | Needed to avoid card-style "locked but not applied" drift. |
| Promotion gates are mostly policy-level today. | Needed to make authority boundaries executable later. |
| PRP/compliance rule layer relationship is unresolved. | Needed to keep funder rules separate from outcome-learning memory. |

## Bottom Line

The card-system research should be treated as a warning and a pattern library.
It warns that authority language drifts unless every state says exactly what it
means. It also gives GoldenQuill a usable pattern:

```text
observed candidate
  -> source-backed record
  -> human-confirmed interpretation
  -> governance-reviewed lesson
  -> owner-approved allowed use
  -> active reuse with contradiction path
```

That is the same shape promotion governance needs.
