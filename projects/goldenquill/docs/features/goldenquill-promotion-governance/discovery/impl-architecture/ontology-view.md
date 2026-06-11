---
view: ontology (entities, enums, state machines, invariants — owns the types)
audience: the team
status: draft — spec-derived 2026-06-10
source: _derivation-substrate.md (read-only derivation from goldenquill-promotion-governance spec)
---

# Ontology-view — goldenquill-promotion-governance (current implementation architecture)

> This is the **ontology-view** — the typed layer beneath the three sibling views. It owns
> the formal model: every entity and value object, every closed set (enum), the five state
> machines, and the load-bearing data-integrity invariants. It decides **what the types are**;
> it decides no verdicts and tells no story.
>
> **What this view owns:** the entity & value-object catalog, the analytics-fact catalog, the
> enum/closed-set inventory, the five state machines (states + governing invariants), the
> relation/edge model, the invariant set, and the honest count-mismatch residue.
>
> **What this view points across for:** the plain-language story → [discovery.md](discovery.md);
> the build-status / decision verdicts (designed-not-built, D7 CRITICAL) → [engineer-view.md](engineer-view.md);
> the stakeholder-altitude shape + the full cross-reference map → [system-view.md](system-view.md).
>
> Every load-bearing claim cites a spec selector (`file:line` or `file SECTION`). Where the spec
> defers, is silent, or contradicts itself, this view marks it **[RESIDUE]** and does **not**
> reconcile it — reconciliation is not authored here.

---

## Cross-reference map

This view names a stance and points to the owner; it never restates a verdict or a story.

| This view's construct | Points to (owner) | What is owned there |
|---|---|---|
| The plain-language "what is this loop" story | [discovery.md](discovery.md) | Orientation narrative + open business questions |
| Build status of every component / entity (designed vs built) | [engineer-view.md](engineer-view.md) | The D7 "designed, not built — CRITICAL" verdict; C1–C16 build status; L0/L1/L2 layering |
| Stakeholder-altitude shape + cross-cutting reference map | [system-view.md](system-view.md) | The topology at altitude; how the planes/components compose |
| `approved_allowed_uses` = sole authority of OwnerDecision | this view §4 + [engineer-view.md](engineer-view.md) | Type fact owned here; promotion-lane verdict owned there |
| The "47 vs 44" KPI / "13 vs 12" event count mismatches | this view §6 (RESIDUE) | Flagged here as unreconciled; **no owner has reconciled them** (GrantRunNodeKind 15-vs-~14 was resolved to 16) |

---

## 1. Entity & value-object catalog

The core domain types (domain.md). Each carries its one-line purpose and its load-bearing
field/invariant. The promotion-governance discipline lives almost entirely in *which type may
carry `approved_allowed_uses`* — see §4.

### Core entities

| Entity | Purpose | Load-bearing field / invariant | Selector |
|---|---|---|---|
| **GrantWorkEvent** | The typed unit an adapter emits — what happened in grant work | Must be wrapped in a `GrantWorkEventEnvelope` before any projection | domain.md:13–30 |
| **GrantWorkEventEnvelope** *(VO)* | Wraps every adapter event before projection; carries source truth + replay semantics | `producer`, `org_scope`, `idempotency_key`, `interpretation_limits` all **Required**; `source_ref` required for source-backed facts; `gate_refs` required when gates acted | domain.md:242–260 |
| **AdapterProducer** | The bounded observer identity that emits an event | Observation-only; **cannot set `approved_allowed_uses`** (A-R6) | domain.md:32–46 |
| **EventProjectionReceipt** | Proof that one accepted event projected into a read model | `projection_kind ∈ {dag, lifecycle, kpi, candidate, owner_decision, approved_reuse, future_context}`; **every projection emits one** (A-R7) | domain.md:48–66 |
| **GrantRunNode** | A node in the grant-run DAG (what happened, in what order) | Typed by `GrantRunNodeKind`; must have a path from `run_context` (GRT-I2) | domain.md:68–86 |
| **GrantRunEdge** | A directed relation between run nodes (ordering / consumption / gating) | Typed by `GrantRunEdgeKind`; `blocked_by_gate` stops downstream traversal (GRT-I1) | domain.md:88–105 |
| **GrantOutcomeEvent** | A real-world grant result (submitted … awarded/declined/withdrawn/closed_out) | `source_ref` **REQUIRED** (ALS-I2) — outcomes are source-or-nothing | domain.md:107–130 |
| **GrantKpiObservation** | A computed KPI read model derived from outcome/lifecycle events | `source_events` **REQUIRED**; denominator-safe only | domain.md:132–151 |
| **PromotionCandidate** | The local grant-learning **proposal** object | Carries `proposed_allowed_uses` (Required); **MUST NOT** carry `approved_allowed_uses` (PCS-I1); `current_state`, `review_gate`, `contradiction_path`, `privacy_scope`, `redaction_status` all Required | domain.md:169–197 |
| **OwnerDecision** | The approved/rejected/retired/contradicted disposition of a candidate | `approved_allowed_uses` **conditional — required only for approved** (ODS-I1/I2); `decision_source` Required (ODS-I3); **"approved uses live here, not on raw evidence or candidates"** | domain.md:199–216 |
| **ApprovedReusePacket** | The bounded handoff carrying approved uses back into future grant work | `approved_allowed_uses` Required; `reuse_scope` Required; "future grant context may consume **only** approved allowed uses from a packet" | domain.md:218–238 |
| **MemoryEvidencePacketRef** *(VO)* | Reference to an existing evidence packet / source-backed equivalent | `authority_class` + `org_scope` Required; **"does not approve reuse"** | domain.md:262–277 |
| **SourceRef** *(VO)* | A stable, locatable source pointer | `source_type ∈ {document, url, portal_export, email_archive, agency_notice, report, operator_upload, fixture}`; `captured_utc` Required (integration upgrades to accept Ed25519) | domain.md:279–287 |
| **StageProfile** *(VO)* | A named override of the global lifecycle stage baseline | `override_reason` Required when overriding baseline (ALS-I3) | domain.md:289–296 |

### Analytics facts (analytics-methods.md / optimization-chains.md)

Evidence-only types. None may carry `approved_allowed_uses` (analytics no-approved-uses; A-R3).

| Fact | Purpose | Load-bearing field / invariant | Selector |
|---|---|---|---|
| **GrantActionFact** | One observed grant action, normalized for association analysis | The leaf the analytics pipeline projects from | analytics-methods.md:51–81 |
| **GrantLifecycleTransitionFact** | A normalized lifecycle stage transition | Pairs with the lifecycle state machine | analytics-methods.md:83–100 |
| **GrantOutcomeFact** | A normalized outcome for outcome-response analysis | Source-backed | analytics-methods.md:102–135 |
| **GrantCostFact** | A normalized cost/resource-use record | Cost denominator for cost KPIs | analytics-methods.md:137–158 |
| **KpiResponseWindow** | The time window joining an action to its KPI response | **Pending outcomes must be `censored`, not counted as losses** | analytics-methods.md:160–191 |
| **StatisticalMethodSpec** | The registry policy gating which method may make which claim | Bias / sample / temporal-leakage checks **fail closed** | analytics-methods.md:195–214 |
| **ActionKpiAssociation** | A measured association between an action and a KPI response | Evidence only; **cannot promote** (W-I2); cannot carry approved uses | analytics-methods.md:253–283 |
| **BIInsightCandidate** | A packaged business-intelligence insight profile | Cannot exceed its method's claim label | analytics-methods.md:500–523 |
| **OptimizationChainDefinition** | A named BI optimization built from associations | Packages evidence; **cannot approve reuse or exceed method claim label** (OCR-005/OCR-007) | optimization-chains.md:69–90 |
| **OptimizationChainExpression** | The 7 rendering forms of a chain | `{plain_language, operator, executive, contract, causal_careful, dashboard_label, ontology}` | optimization-chains.md:92–105 |

---

## 2. Enums / closed sets

Counts as derived from domain.md (analytics enums from analytics-methods.md). The
governance-critical sets are expanded; the rest are listed with their value counts.

### Governance-critical sets (expanded)

| Enum | Count | Values | Selector |
|---|---|---|---|
| **PromotionCandidateStateValue** | 8 | `captured`, `candidate`, `validated`, `decision_pending`, `approved`, `rejected`, `retired`, `contradicted` | domain.md:451–462 |
| **OwnerDecisionStateValue** | 4 | `approved`, `rejected`, `retired`, `contradicted` | domain.md:464–471 |
| **ApprovedReusePacketStateValue** | 3 | `active`, `retired`, `contradicted` | domain.md:473–479 |
| **AllowedUse** | 9 | `orient`, `draft_support`, `decision_input`, `dashboard`, `learning_candidate`, `workspace_reuse`, `org_private_reuse`, `citation_candidate`, `do_not_use` | domain.md:481–493 |
| **OrgScope** | 4 | `workspace_global`, `single_org`, `no_org_loaded`, `cross_org_forbidden` | domain.md:506–513 |
| **ValidationState** | 5 | `candidate`, `checked`, `failed`, `waived`, `contradicted` | domain.md:515–523 |
| **RedactionStatus** | 5 | `not_required`, `required`, `redacted`, `generalized`, `blocked` | domain.md:525–533 |

`generalized` (RedactionStatus) and `workspace_reuse` (AllowedUse) are the two values the
privacy gate keys on: workspace-safe reuse requires `redaction_status == generalized` **and**
owner approval (PCS-I3).

### Remaining closed sets (by count)

| Enum | Count | Selector / note |
|---|---|---|
| GrantWorkEventKind | 9 | domain.md:301–313 |
| AdapterProducerKind | 9 | domain.md:315–327 |
| GrantRunNodeKind | 16 | domain.md:329–348 (SPEC.md:102–119 "minimum execution nodes" also lists 16) |
| GrantRunEdgeKind | 7 | domain.md:350–360 |
| GrantOutcomeEventKind | 11 | domain.md:362–376 |
| ApplicationStage | 19 | domain.md:378–400 |
| GrantKpiKind | 44 | domain.md:402–449 — **[RESIDUE: component-inventory prose says "47 KPIs"; 3-entry gap]** (see §6) |
| AuthorityClass | 6 | domain.md:495–504 |
| PromotionCandidateKind | 6 | domain.md:535–544 |
| StatisticalMethodFamily | 11 | analytics-methods.md |
| AnalyticsMaturityLevel | 5 (L0–L4) | analytics-methods.md |
| AnalyticsClaimLabel | 6 (incl. terminal `blocked_or_residue`) | analytics-methods.md |

---

## 3. The five state machines

Each machine is the set of legal transitions of one lane in the promotion sequence. States +
the governing invariants below; full transition tables at the cited selectors.

### 3.1 GrantRunTraversalState — states.md:11–40

`[*] → not_started → active → {blocked ↔ active} → delivered → outcome_tracking → [*]`

| ID | Invariant | Formal | Selector |
|---|---|---|---|
| GRT-I1 | No downstream draft/delivery after a blocked gate without reopen evidence | `blocked_by_gate -> no downstream delivery_envelope until reopen` | states.md:38 |
| GRT-I2 | Every non-initial node has a path from `run_context` | `node != run_context -> path(run_context, node)` | states.md:39 |
| GRT-I3 | Every delivery requires `operator_signoff` | `delivery_envelope -> exists operator_signoff approved_by edge` | states.md:40 |

### 3.2 ApplicationLifecycleState — states.md:42–101

19 stages: `prospect → eligible_match → … → {awarded | declined | withdrawn | closed_out}`
(branching at `under_review`/`review_feedback_received`; `withdrawn` is reachable from
`application_submitted`).

| ID | Invariant | Formal | Selector |
|---|---|---|---|
| ALS-I1 | Application stage is not final-outcome truth | `stage_depth != final_outcome` | states.md:98 |
| ALS-I2 | Final outcome requires a source-backed event | `stage in {awarded,declined,withdrawn,closed_out} -> source_ref != null` | states.md:99 |
| ALS-I3 | Global baseline overridden only by a named profile with source | `profile_override -> stage_profile != global and source_ref != null` | states.md:100 |

### 3.3 PromotionCandidateState — states.md:102–141

`captured → candidate → {validated | rejected}; validated → decision_pending;
decision_pending → {approved | rejected | retired | contradicted}; approved → {retired | contradicted}`

| ID | Invariant | Formal | Selector |
|---|---|---|---|
| PCS-I1 | Candidates cannot contain approved allowed uses | `candidate.approved_allowed_uses == null` | states.md:139 |
| PCS-I2 | Approved state requires an owner decision | `state == approved -> owner_decision_ref != null` | states.md:140 |
| PCS-I3 | Workspace-safe reuse requires generalized redaction + owner approval | `workspace_reuse -> redaction_status == generalized and owner_decision.approved` | states.md:141 |

### 3.4 OwnerDecisionState — states.md:143–176

`[*] → pending → {approved | rejected | retired | contradicted}; approved → {retired | contradicted}`

| ID | Invariant | Formal | Selector |
|---|---|---|---|
| ODS-I1 | Approved decisions require non-empty approved allowed uses | `decision == approved -> len(approved_allowed_uses) > 0` | states.md:174 |
| ODS-I2 | Non-approved decisions must not grant approved uses | `decision != approved -> len(approved_allowed_uses) == 0` | states.md:175 |
| ODS-I3 | Every decision has decision-source evidence | `decision_source != null` | states.md:176 |

### 3.5 ApprovedReusePacketState — states.md:178–203

`[*] → active → {retired | contradicted}`

| ID | Invariant | Formal | Selector |
|---|---|---|---|
| ARP-I1 | Active packets require approved allowed uses | `packet.status == active -> len(packet.approved_allowed_uses) > 0` | states.md:201 |
| ARP-I2 | Retired/contradicted packets cannot hydrate future context | `packet.status in {retired,contradicted} -> no HydrateFutureGrantContext` | states.md:202 |
| ARP-I3 | Hydration use ⊆ approved allowed uses | `requested_use in packet.approved_allowed_uses` | states.md:203 |

> The optimization-chain `status` (`candidate / validated / approved / rejected / retired /
> residue`) is a **flat field, not a transition machine** in the spec — it is not the sixth
> state machine. (substrate §3)

---

## 4. Relation / edge model and the data-integrity invariant set

### The promotion sequence (relation backbone)

The entity types compose one directed sequence; the read-model edges are the `GrantRunEdgeKind`
set, the governance edges are the projection receipts plus the `*_ref` fields on the promotion
lane:

```
GrantWorkEvent → [Envelope] → EventProjectionReceipt
  → { GrantRunNode/Edge,  GrantOutcomeEvent → ApplicationLifecycleState,  GrantKpiObservation }
  → { GrantActionFact … KpiResponseWindow → ActionKpiAssociation → BIInsightCandidate / OptimizationChain }
  → PromotionCandidate  (proposed_allowed_uses)
  → [OntologyVaultProjection · RedactionGeneralizationGate]
  → OwnerDecision  (approved_allowed_uses — first appearance)
  → ApprovedReusePacket
  → HydrateFutureGrantContext  (requested_use ⊆ approved_allowed_uses)
```

`GrantRunEdgeKind` (the only first-class edge type set): `precedes`, `consumes`, `emits`,
`blocked_by_gate`, `revised_by`, `approved_by`, `delivered_as` (domain.md:350–360). The
candidate→decision→packet links are reference fields (`owner_decision_ref`, `decision_id`,
`candidate_id`), not run-DAG edges.

### Data-integrity invariant set

| ID | Invariant | Selector |
|---|---|---|
| **PCS-I1** | `candidate.approved_allowed_uses == null` — candidates carry only proposed uses | states.md:139; domain.md:196–197 |
| **PCS-I2** | `state == approved -> owner_decision_ref != null` | states.md:140 |
| **ODS-I1** | `decision == approved -> len(approved_allowed_uses) > 0` | states.md:174 |
| **ODS-I2** | `decision != approved -> len(approved_allowed_uses) == 0` | states.md:175 |
| **A-R3** | No approved uses exist anywhere before an OwnerDecision | substrate §2/§4 (architecture.md A-R3) |
| **A-R6** | Adapters cannot set approved uses (observation-only) | substrate §2/§4; domain.md:32–46 |
| **A-R7** | Every projection emits an `EventProjectionReceipt` | substrate §2; domain.md:48–66 |
| **analytics no-approved-uses** | Analytics facts / associations / chains cannot carry approved uses | substrate §2; OCR-005/OCR-007 |

**The single load-bearing rule these compose:** `approved_allowed_uses` is **set in exactly one
place — OwnerDecision** (domain.md:216, "approved uses live here, not on raw evidence or
candidates"; SPEC.md:89). Adapters (A-R6), the journal (SPEC.md:200), KPIs/outcomes/associations/
chains (W-I2, analytics no-approved-uses), and candidates (PCS-I1) are all structurally
forbidden from it. The promotion-lane verdict that depends on this fact is owned by
[engineer-view.md](engineer-view.md) — not authored here.

---

## 5. Pointers (not authored here)

- **Build status** of every entity/component (everything is **designed, not built — D7 CRITICAL**;
  L0 is fixture-only and audit-only, `mutation_allowed=false`) → [engineer-view.md](engineer-view.md).
- **Plain-language story** of the loop → [discovery.md](discovery.md).
- **Topology / planes / stakeholder shape** and the broader cross-reference map →
  [system-view.md](system-view.md).

---

## 6. RESIDUE — unreconciled spec count mismatches (honest, not reconciled here)

These are real disagreements between the enum tables (domain.md) and prose elsewhere in the
spec. **This view does not pick a winner** — reconciliation is not authored at this altitude.

| # | Mismatch | Counted side | Prose side | Status |
|---|---|---|---|---|
| RES-1 | **GrantKpiKind: 47 vs 44** | `GrantKpiKind` enum has **44** entries (`stage_depth` … `grant_retention_rate`, domain.md:402–449; verified by direct count 2026-06-10) | Component inventory C5 / KPI-engine prose says **"47 KPIs"** (runtime-design / ARCHITECTURE C5) | **open / unreconciled** — 3-entry gap; an earlier "49" figure was a miscount, now corrected |
| RES-2 | **GrantWorkEvent count: 13 vs 12** | events.md has 13 event sections | runtime-design §7 / OPEN-QUESTIONS-LEDGER list it as open residue; "12" source unidentified | **open / unreconciled** — note: `GrantWorkEventKind` *enum* itself has **9** values (domain.md:301–313); the 13-vs-12 residue is at the event-catalog (events.md) level, canonical count unresolved in spec |
| RES-3 | ~~GrantRunNodeKind: 15 vs ~14~~ **RESOLVED — not residue** | `GrantRunNodeKind` enum has **16** entries (domain.md:329–348) | SPEC.md:102–119 independently lists the same **16**; the earlier "15"/"~14" were miscounts | **resolved** — counts agree at 16 |

Additional caveat carried from the substrate: TEST-SPEC.md (T1–T35), glossary.md, and
OPEN-QUESTIONS-LEDGER.md are referenced load-bearingly but sit **outside this view's verified
read set**; **B-001** flags TEST-SPEC T1–T35 stability as unconfirmed (substrate §5). The
analytics enum counts (StatisticalMethodFamily 11, AnalyticsClaimLabel 6) are carried from the
substrate, not re-verified line-by-line here.
