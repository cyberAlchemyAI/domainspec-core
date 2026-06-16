---
node_type: discovery
status: exploratory
governance_status: project-local-overlay
topic: Hellbender client research - engineer-view
last_updated: 2026-06-15
created_by: codex
---

# Engineer-view - Hellbender client research

This is the mechanics and verdict view for the Hellbender account research. It owns the decision
inventory for every stance named in [system-view.md](system-view.md), uses terms from
[ontology-view.md](ontology-view.md), and translates the research into implementation-ready offering
work.

## Objective

The central value thesis is that a narrow physical AI lifecycle intelligence pilot can convert one
Hellbender lifecycle metric into governed, boundary-aware reusable learning. This view records which
parts of that thesis are decided, open, or critical, with each row tied to local authority.

## What this view owns

1. The decision inventory for every named stance.
2. The draft contracts needed to turn the account research into an offering package.
3. The mechanics for moving from public-source research to discovery call to pilot design.
4. The blocker open questions that must be resolved before external collateral or pilot execution.

## 1. Decision inventory

Status legend: **RESOLVED** means decided and enforced by an existing local artifact or validated
dispatch; **OPEN** means named but not client-validated; **CRITICAL** means open and blocking the
core thesis until resolved.

| # | Decision / stance | Verdict | Status | Authority |
| --- | --- | --- | --- | --- |
| D1 | Offer status - back-ref `system-view#stance:offer-status` | Treat the Hellbender package as internal candidate account research only; client-facing collateral requires a later owner-reviewed route. | **RESOLVED** | [README.md](README.md) status; [SUMMARY.md](SUMMARY.md) status; `hellbender-research.dispatch.json` validated `pass`. |
| D2 | First wedge - back-ref `system-view#stance:first-wedge` | Candidate first wedge is EOL QA/calibration to field performance to sustaining engineering, but the actual wedge remains discovery-call dependent. | **OPEN** | [SUMMARY.md](SUMMARY.md) first-offer section; [sessions/hellbender-research-receipts.md](sessions/hellbender-research-receipts.md) parent synthesis. |
| D3 | Proof metric - back-ref `system-view#stance:proof-metric` | Start offering work around one defensible priority metric, not a broad dashboard, but the exact metric is not selected. | **OPEN** | [PUBLIC-OFFERING.md](../../PUBLIC-OFFERING.md) pilot shape; [SUMMARY.md](SUMMARY.md) proof metrics. |
| D4 | Boundary first - back-ref `system-view#stance:boundary-first` | Any pilot must start metadata-first and fail closed on data/IP/security scope; raw images, model data, design files, or regulated data are blocked until a boundary register exists. | **CRITICAL** | [RESEARCH-STRATEGY.md](RESEARCH-STRATEGY.md) hard stops; [SUMMARY.md](SUMMARY.md) risks and guardrails. |
| D5 | Delivery lane - back-ref `system-view#stance:delivery-lane` | Default offering assumption is Hybrid delivery: Hellbender tools keep operational data and BI surfaces while CyberAlchemy/Ontologize handles governance receipts and promotion logic; assessment may override. | **OPEN** | [DELIVERY-LANES.md](../../DELIVERY-LANES.md) selection rule; [SUMMARY.md](SUMMARY.md) delivery-lane guardrail. |
| D6 | Owner reuse - back-ref `system-view#stance:owner-reuse` | Reusable lessons require owner-reviewed promotion; no automatic cross-product or cross-client reuse. Client owner and reuse rights are still unknown. | **CRITICAL** | [PUBLIC-OFFERING.md](../../PUBLIC-OFFERING.md) promotion graph and pilot proof; [SUMMARY.md](SUMMARY.md) discovery questions. |
| D7 | Offering package scope | Next work should be an invoke design/plan bundle for one-page offer, discovery script, questionnaire, metadata request, boundary template, acceptance criteria, and risk appendix. | **OPEN** | [SUMMARY.md](SUMMARY.md) offering work to start next; [RESEARCH-STRATEGY.md](RESEARCH-STRATEGY.md) next route. |

The OPEN / CRITICAL rows are the ones a stakeholder must weigh before treating this as a real offer.
D4 and D6 gate the value thesis: without a safe data boundary and owner decision path, the pilot is
not trustworthy.

## 2. Schemas and contracts

These are draft contracts for the next offering package. They are not canonical schemas yet.

### 2.1 Pilot offer contract

Source: [SUMMARY.md](SUMMARY.md), [RESEARCH-STRATEGY.md](RESEARCH-STRATEGY.md).

Minimum fields:

- `offer_name`: working title, currently Physical AI Lifecycle Intelligence Pilot.
- `account_scope`: one product line, production loop, or CVaaS deployment.
- `proof_metric`: one priority metric tied to a source event boundary.
- `evidence_chain`: source event, denominator, evidence references, confidence, interpretation limits.
- `boundary_register`: data classes, approved uses, restricted uses, owner.
- `promotion_graph`: event, evidence, candidate lesson, owner decision, projection or residue.
- `acceptance_criteria`: what proves the pilot worked.

Realizes D2, D3, D4, D6, and D7.

### 2.2 Metric proof contract

Source: [PUBLIC-OFFERING.md](../../PUBLIC-OFFERING.md), [SUMMARY.md](SUMMARY.md).

Minimum fields:

- `metric_name`
- `run_boundary`
- `source_systems`
- `denominator`
- `included_events`
- `excluded_events`
- `evidence_refs`
- `confidence`
- `interpretation_limits`
- `decision_improved`

Realizes D3.

### 2.3 Data boundary register contract

Source: [SUMMARY.md](SUMMARY.md), [sessions/hellbender-research-receipts.md](sessions/hellbender-research-receipts.md).

Minimum fields:

- `data_class`
- `owner`
- `examples`
- `allowed_use`
- `blocked_use`
- `storage_boundary`
- `reuse_boundary`
- `review_required`
- `fail_closed_default`

Realizes D4.

### 2.4 Promotion decision contract

Source: [PUBLIC-OFFERING.md](../../PUBLIC-OFFERING.md), [SUMMARY.md](SUMMARY.md).

Minimum fields:

- `source_event`
- `evidence`
- `candidate_lesson`
- `owner`
- `decision`
- `allowed_reuse_scope`
- `private_residue`
- `contradiction_path`
- `retire_condition`

Realizes D6.

### 2.5 Delivery lane contract

Source: [DELIVERY-LANES.md](../../DELIVERY-LANES.md), [SUMMARY.md](SUMMARY.md).

Minimum fields:

- `lane`: Lane A, Lane B, or Hybrid.
- `client_data_location`
- `dashboard_surface`
- `governance_surface`
- `promotion_layer`
- `adoption_constraints`
- `assessment_override_reason`

Realizes D5.

## 3. Runtime mechanics

1. **Source capture.** The account starts from public Hellbender sources, Ontologize source docs, and
   the four read-only fanout lanes. This realizes D1 by keeping the work internal and candidate-only.
2. **View triad.** `system-view.md` carries account shape, `ontology-view.md` carries typed nodes and
   edges, and this file carries verdicts and contracts. This realizes D1 and prevents duplicated
   decisions.
3. **Discovery call gate.** Before an offering package can be shared, the account owner must validate
   sponsor, lifecycle stage, proof metric, source event boundary, data class, and owner-decision path.
   This is where D2-D6 move from internal candidate posture toward client-validated posture.
4. **Invoke offering route.** The next executable route should produce one-page offer, call script,
   assessment questionnaire, sample metadata request, boundary-register template, acceptance criteria,
   and risk appendix. This realizes D7.
5. **Pilot execution gate.** Pilot execution remains blocked until D4 and D6 are satisfied: safe data
   boundary and owner-reviewed reuse path.

## 4. Named stances - verdicts

- **offer-status (D1)** - RESOLVED: internal candidate research only; later owner review controls
  any client-facing collateral.
- **first-wedge (D2)** - OPEN: EOL QA/calibration to field performance is the current candidate, but
  the client has not confirmed the painful lifecycle slice.
- **proof-metric (D3)** - OPEN: one defensible metric is the shape, but the metric and source system
  are unknown.
- **boundary-first (D4)** - CRITICAL: the pilot is not safe without data class, security review path,
  and fail-closed handling.
- **delivery-lane (D5)** - OPEN: Hybrid is the candidate default, but assessment facts may choose
  Lane A or Lane B.
- **owner-reuse (D6)** - CRITICAL: the learning-loop claim fails without a named owner and reuse
  boundary.
- **offering package scope (D7)** - OPEN: the package contents are named, but not yet authored.

## Open questions

- **OQ-1** - Which Hellbender sponsor owns the first lifecycle metric? Recommendation: resolve in a
  discovery call before drafting external collateral. Owner: account owner.
- **OQ-2** - Which lifecycle slice is first: DFM/DVT, EOL QA/calibration, field support, CVaaS, or
  custom-to-platform transfer? Recommendation: test against urgency, source-system access, and
  decision impact. Owner: account owner plus client sponsor.
- **OQ-3 (BLOCKER)** - Which data classes are approved for a metadata-first sample? Recommendation:
  create a boundary register before requesting sample data. Owner: client security/data owner.
- **OQ-4 (BLOCKER)** - Who can approve reusable lessons, and what reuse scopes are allowed?
  Recommendation: name owner and allowed reuse scope before pilot acceptance. Owner: client sponsor.
- **OQ-5** - Should the first offering package use "Physical AI Lifecycle Intelligence Pilot" or the
  sales-forward subtitle? Recommendation: decide after sponsor persona is known. Owner: offering
  owner.

## Residue ledger

| # | Verdict / claim | Status | Surviving residue | Citation |
| --- | --- | --- | --- | --- |
| R1 | Internal candidate posture is enforced locally. | closed | No external collateral authored in this route. | [README.md](README.md), [SUMMARY.md](SUMMARY.md) |
| R2 | EOL QA/calibration is the candidate first wedge. | open | Client has not confirmed pain or source-system access. | [SUMMARY.md](SUMMARY.md), [sessions/hellbender-research-receipts.md](sessions/hellbender-research-receipts.md) |
| R3 | One proof metric is the right sale shape. | open | Exact metric, event boundary, denominator, and decision impact are unknown. | [PUBLIC-OFFERING.md](../../PUBLIC-OFFERING.md), [SUMMARY.md](SUMMARY.md) |
| R4 | Data boundary-first is critical. | open | Needs a data owner and allowed data classes. | [RESEARCH-STRATEGY.md](RESEARCH-STRATEGY.md) |
| R5 | Owner-reviewed promotion is critical. | open | Needs owner, reuse rights, and contradiction/retirement path. | [PUBLIC-OFFERING.md](../../PUBLIC-OFFERING.md), [SUMMARY.md](SUMMARY.md) |
| R6 | Hybrid delivery is the candidate default. | open | Assessment may override after data residency and adoption facts are known. | [DELIVERY-LANES.md](../../DELIVERY-LANES.md) |

## Cross-reference map

| This view row / section | Relationship | Owner | What is owned there |
| --- | --- | --- | --- |
| D1-D6 | answers | [system-view.md](system-view.md) | The shape and stakeholder stakes of the named stances. |
| Terms in contracts | defined-by | [ontology-view.md](ontology-view.md) | Typed node and edge meaning. |
| D3 metric contract | cites | [PUBLIC-OFFERING.md](../../PUBLIC-OFFERING.md) | General CyberAlchemy pilot pattern. |
| D5 delivery lane | cites | [DELIVERY-LANES.md](../../DELIVERY-LANES.md) | Lane selection rule. |
| D7 next route | derives-from | [SUMMARY.md](SUMMARY.md) and [RESEARCH-STRATEGY.md](RESEARCH-STRATEGY.md) | Offering package scope and next route. |

## Connections

| Document | Type | Description |
| --- | --- | --- |
| [SUMMARY.md](SUMMARY.md) | derives-from | Reconciled from the offering-start summary as source corpus. |
| [RESEARCH-STRATEGY.md](RESEARCH-STRATEGY.md) | derives-from | Uses hard stops and next route. |
| [sessions/hellbender-research-receipts.md](sessions/hellbender-research-receipts.md) | derives-from | Uses lane findings and risk synthesis. |
| [system-view.md](system-view.md) | refines | Refines system-view stances into decisions and mechanics. |
| [ontology-view.md](ontology-view.md) | cites | Uses typed terms from ontology-view. |
