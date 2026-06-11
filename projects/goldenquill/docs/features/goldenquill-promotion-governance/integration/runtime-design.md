# Victor ↔ Promotion-Governance — Runtime Integration Design

- Status: draft (refined design; non-executed)
- Updated: 2026-06-10
- Dispatch: `gq-victor-promotion-integration-2026-06-10` (step `s4-runtime-design`)
- Inputs: [seam-map.md](seam-map.md), four resolved decisions (§Decisions)
- Authority boundary: GoldenQuill grant runtime owns *event shape*; the
  Ontology Vault governance layer owns *promotion safety*. This document
  designs the seam and **promotes nothing**.

> Scope note: L0 stays fixture-only and audit-only, matching
> [SPEC.md](../SPEC.md) §596–621. Everything marked **L1+** is design, not a
> commitment to build.

---

## 1. Runtime topology

```
            VICTOR COUNCIL CYCLE (one grant run)                  PROMOTION-GOVERNANCE SPINE
  ┌─────────────────────────────────────────────┐
  │ Scout → operator review → Scribe → Editor →  │   emit typed     ┌──────────────────────────┐
  │ Judge → Red Team → Logician → Uploader       │ ───────────────▶ │ AcceptGrantWorkEvent      │
  └─────────────────────────────────────────────┘   GrantWorkEvent  │  (validate · idempotency) │
        │ spans                  │ outcomes (portal/agency/email)    └────────────┬─────────────┘
        ▼                        ▼                                                ▼
  ┌───────────┐          ┌───────────────┐                          ┌──────────────────────────┐
  │  Logfire  │          │ outcome_source│ ───────────────────────▶ │  EVENT JOURNAL (new)      │
  │ (observ.) │          │   adapters    │                          │  append-only · replayable │
  └───────────┘          └───────────────┘                          └────────────┬─────────────┘
   (NOT authority)                                                                ▼
                                                          ┌─────────────────────────────────────┐
                                                          │ ProjectEventToDag  ProjectToLifecycle │
                                                          │   ↓ GrantRunNode/Edge   ↓ KPI obs.    │
                                                          │ ComputeKpiObservation → analytics     │
                                                          │   ↓ CreatePromotionCandidate          │
                                                          │ ValidatePromotionGovernance           │
                                                          │   ↓ OntologyVaultProjection (audit)   │
                                                          │ RedactionGeneralizationGate (privacy) │
                                                          │   ↓ ScopeAndPrivacyGate               │
                                                          │ RecordOwnerDecision (operator Ed25519)│
                                                          │   ↓ PublishApprovedReusePacket        │
                                                          └────────────────┬────────────────────┘
                                                                           ▼
                              HydrateFutureGrantContext ──▶ Scout · Scribe · Judge · Logician · Funding Goal
```

The council cycle is **unchanged**; the spine is a **listener + governance
overlay**. Seats keep producing their existing artifacts; thin adapter wrappers
turn those artifacts into typed events.

---

## 2. How events are emitted and listened

### 2.1 Emit (council → journal)

- Each seat call is wrapped by an **AdapterProducer** (one per
  `AdapterProducerKind`). The wrapper builds a `GrantWorkEventEnvelope`
  (`event_id`, `event_kind`, `producer_kind`, `run_id`, `org_scope`,
  `source_ref`, `occurred_at`, `captured_at`, `idempotency_key`,
  `interpretation_limits`, `gate_refs`) and hands it to `AcceptGrantWorkEvent`.
- **Adapters have observation authority only.** They cannot set
  `approved_allowed_uses`, write the DAG, or promote ([architecture.md] external
  dependencies table). Boundary `b1-runtime-vs-governance`.
- Outcome facts (`submitted`, `portal_validated`, `awarded`, `declined`,
  `closed_out`, …) come from `outcome_source` adapters and **require a
  `source_ref`** — no source, no event (SPEC acceptance criterion).

### 2.2 Accept + project (the only authority path)

`AcceptGrantWorkEvent` is the single ingress. It enforces idempotency:

- same `idempotency_key` + same content hash → no-op, receipt
  `skipped_reason = idempotent_replay`;
- same key + different hash → fail closed, receipt
  `blocked_reason = duplicate_conflict`, P0 metric.

Accepted events fan out to `ProjectEventToDag` (nodes/edges) and
`ProjectEventToLifecycleAndKpi` (lifecycle state + KPI). Every projection emits
an `EventProjectionReceipt` (`created_refs`, `updated_refs`, `skipped_reason`,
`blocked_reason`, `validation_state`) — the replay/audit record.

### 2.3 Listen (who consumes what)

| Producer | Event | Listeners |
|---|---|---|
| `AcceptGrantWorkEvent` | `GrantWorkEventAccepted` / `…Rejected` | DAG + lifecycle/KPI projectors / adapter owner |
| `ProjectEventToDag` | `DagProjectionUpdated` | DAG validator, audit |
| `RecordOutcomeEvent` | `GrantOutcomeEventRecorded` | lifecycle + KPI projectors, candidate generator |
| `ComputeKpiObservation` | `KpiObservationComputed` | dashboard, candidate generator, validator |
| `CreatePromotionCandidate` | `PromotionCandidateCreated` | governance validator, vault projection |
| `RecordOwnerDecision` | `OwnerDecisionRecorded` | runtime planning, vault handoff, audit |
| `PublishApprovedReusePacket` | `ApprovedReusePacketPublished` | future-context hydrator, memory query, audit |
| `HydrateFutureGrantContext` | `FutureGrantContextHydrated` | Scout, Scribe, Judge, Logician, Funding Goal |

### 2.4 Observability is a separate plane

Logfire spans and `session_log.jsonl` are **never** the source of authority.
`CycleReceipt` (`wpfa_cycle_accountant`) and `Reflection Packet` (v0.2,
`reflection_packet`) *read* Logfire span trees and *emit* typed events into the
journal — they are adapters, not the journal. Trace events for this dispatch
are grouped under `dispatch_id` (see the dispatch artifact `observability`).

---

## 3. How ontology is stored

Three storage planes, each with one owner (boundary
`state_namespace_boundary`):

1. **Per-org sovereign plane** — `orgs/<slug>/vault/…` (KFR, classification,
   match_database). Law-3 read-isolated (`F-MATCH-DB-CROSS-ORG`). Append-only.
   Hydration targets here apply **automatically** after owner approval.
2. **Shared ontology plane** — `pipeline/cards/CIC|CLC/*`,
   `admin_risk_register.yaml`. Owner-decision-gated; refined to "guardpost
   level" only (D5a — no metric hill-climb). Promotion here is **never
   automatic**: it requires `consent_tier == composable_with_others` plus a
   Victor operator card-edit review.
3. **Governance/audit plane** — the event journal + `OntologyVaultProjection`
   (audit-only, `mutation_allowed=false` in L0) +
   `vault_shared/promotion_governance/approved_reuse_packets/`. Append-only,
   replayable; mutates nothing canonical.

```
ApprovedReusePacket
  ├─ reuse_scope = single_org      ──▶ append to orgs/<slug>/vault/{kfr,match_db}      (auto, no tier check)
  └─ reuse_scope = workspace_global ─▶ Victor operator card-edit gate ─▶ pipeline/cards (manual review)
```

`approved_allowed_uses` exist **only** on an `OwnerDecision` (boundary
`b2-owner-decision-approval`); candidates and KPI thresholds never self-promote.

---

## 4. How each part of a run integrates

| Run phase (Victor) | Emits | Projects to | Governance touch |
|---|---|---|---|
| Discovery / verify | scout records | DAG `scout_*` nodes; lifecycle `eligible_match` | — |
| Operator go/no-go | `operator_review_decision` | DAG edge `approved_by` | — |
| Draft → edit → score → red-team | seat reports | DAG draft/score/review nodes | Logician gate edges `blocked_by_gate` |
| Logician gates | gate results | DAG `logician_gate_result` | fail-closed; no downstream without reopen |
| Deliver / submit | `delivery_envelope` | lifecycle `application_submitted` | `operator_signoff` required |
| Outcome (portal/agency) | `outcome_source` events | lifecycle → `awarded`/`declined`/… | source_ref required |
| Cycle close | `CycleReceipt`, (v0.2) `Reflection Packet` | KPI observations (47 KPIs) | feeds candidate generator |
| Learning | KPI + outcome | `PromotionCandidate` → vault projection | privacy + owner decision → reuse packet |

This is Victor's **D7 loop, fully wired**: outcome → KPI/Insight → candidate →
ScopeAndPrivacyGate → owner decision → approved reuse → future context.

---

## 5. Components to design / build

| # | Component | New? | Substrate | First layer |
|---|---|---|---|---|
| C1 | AdapterProducer wrappers (one per seat + outcome sources) | new thin | Pydantic | L1 |
| C2 | Event journal store + idempotency index | **new** | JSONL (→SQLite) | L0 fixture, L1 real |
| C3 | `AcceptGrantWorkEvent` + projection receipts | new | Pydantic + Logician | L0 |
| C4 | DAG + lifecycle/KPI projectors | new | Pydantic | L0/L1 |
| C5 | KPI engine (47 KPIs, denominator-safe) | new | numpy/scipy | L1 |
| C6 | Analytics method registry (L0 descriptive only) | new | numpy/scipy | L1 |
| C7 | Promotion candidate builder | new | Pydantic | L1 |
| C8 | `OntologyVaultProjection` (audit-only) | new | Pydantic + Cedar | L0 |
| C9 | `ScopeAndPrivacyGate` (consent-tier ∧ redaction) | new | Cedar + Python | L1 |
| C10 | `RecordOwnerDecision` + Ed25519 validation | new | Python + Ed25519 | L1 |
| C11 | ApprovedReusePacket store + future-context hydrator | new | Pydantic/YAML | L2 |
| C12 | Victor operator card-edit gate (shared-card apply) | new | Python + operator UX | L2 |
| C13 | `F-PROMOTION-*` failure-code family | new | Logician | L1 |
| C14 | Per-CIC redaction/generalization rule tables | new | YAML (signed) | L2 |
| C15 | Improvement engine (per-org auto-refine; shared-card operator edit) | **new** | DSPy+GEPA / operator UX | L2.5 |
| C16 | Improvement verification (held-out eval, KPI-delta gate) | **new** | experiment-harness + numpy/scipy | L2.5 |

Reused as-is from the LOCKED substrate: Pydantic AI, Logfire, Cedar/Logician,
weasyprint, Ed25519 signing chain, **DSPy+GEPA** (offline refinement).

---

## 5b. The improvement loop — promotion → *proven* better

`HydrateFutureGrantContext` only makes an approved lesson **available**.
Promotion is not improvement. Closing Victor's D7 (and answering D5,
calibration) requires a second loop that **applies** the lesson to an artifact
and **proves** it helped before it goes live.

```
ApprovedReusePacket
   ├─ per-org target  ──▶ C15 DSPy+GEPA auto-refine ──┐
   └─ shared-card target ─▶ C15 operator card-edit ───┤
                                                       ▼
                              C16 Improvement verification
                       (re-run held-out grant set · compute KPI delta
                        vs optimization-chain expected delta)
                                   │
              improved ───────────┤────────── not improved / regressed
                 ▼                                      ▼
        promote refined artifact              reject + residue ledger
        (per-org: auto-apply;                 (no silent live change)
         shared-card: through owner gate)
```

- **What is optimized:** per-org KFR/context (auto) and shared CIC/CLC card
  content — `search_vocabulary`, `evidence_signals`, `dialect_routing` — plus
  seat calibration params (D5).
- **The target is a named optimization chain** ([optimization-chains.md](../optimization-chains.md)):
  e.g. *Rubric Coverage Lift* expects `rubric_coverage` ↑. C16 measures the
  actual delta against that expectation.
- **The proof is a held-out re-run**, not the grant that produced the lesson —
  a *diverse* set, so a shared card is lifted to the **guardpost level**
  (D5a) rather than overfit to one funder's metric.
- **Two gates now exist:** (1) *lesson approved for reuse* (OwnerDecision,
  already designed) and (2) *refinement proven to improve* (C16). A change that
  passes (1) but fails (2) is rejected and logged — never assumed.

---

## 6. Decisions (resolved blockers — `s3` gate `g1`)

### D-A — Event-journal vendor → **JSONL for v0.1**
Append-only `orgs/<slug>/vault/event_journal/<cycle_id>.jsonl` + in-memory
idempotency index (`idempotency_key → {offset, content_hash}`). Zero new deps
(Golden Image already ships Python + Pydantic), transparent replay, fully
fixture-testable. **Migrate to SQLite** (`INSERT OR IGNORE` = native
idempotency) at ~50k events/cycle; **DuckDB** only if analytics reach L2+.
Rejected: Logfire-as-journal (no replay/idempotency), `session_log.jsonl`
extension (wrong schema/granularity), embedded event store (violates
no-marketplace).

### D-B — Journal vs Logfire boundary → **three distinct planes**
Logfire = observability (not authority); `session_log.jsonl` = agent CI
metrics (unrelated); event journal = the sole replayable authority store.
`CycleReceipt` / `Reflection Packet` are adapters that emit events, not the
journal itself.

### D-C — Ontology storage location → **Victor owns stores, governance owns the decision (hybrid apply)**
Production knowledge stays in Victor's files; `ApprovedReusePacket` lands in
`vault_shared/promotion_governance/approved_reuse_packets/`. Per-org targets
auto-apply (append-only); shared-card targets pass a Victor operator card-edit
gate. `mutation_allowed=false` in L0; flips true **per-org only** in L1.

### D-D — Vocabulary owner → **one jointly-owned PromotionGovernance vocabulary**
Adopt promotion-governance's 4-value `OwnerDecision` enum
(approved/rejected/retired/contradicted). Separate `consent_tier` (applicant
**input**, 3 tiers) from `OrgScope` (system-**derived**, 4 values) with an
explicit map. Upgrade `decision_source: SourceRef` to accept Ed25519. Two-layer
privacy: Classification Register (routing) ⟂ RedactionStatus (reuse), joined by
`ScopeAndPrivacyGate`. Add `F-PROMOTION-*` codes. Victor's engineer-view D7
verdict stays CRITICAL/unbuilt and now **points to this spec as its
implementation vehicle**.

Analytics-library sub-decision: freeze `numpy` + `scipy` for L0; defer the
heavy causal/regression stack to v0.2.

### D-F — Improvement application → **both, by target** (closes D5/D7)
Promotion only delivers a lesson; this decision is how the lesson becomes a
*measurably better* artifact. Per-org context refines **automatically** via
DSPy+GEPA (locked substrate: "offline Card refinement, Library development
only") — cheap, low blast radius. Shared CIC/CLC cards refine by **operator
edit** — one card affects every same-CIC org, so a human stays in the loop.
**Both** must pass C16 held-out verification (KPI delta vs the optimization
chain's expected delta) before going live; a refinement that regresses is
rejected and logged as residue. Rejected alternatives: auto-refine shared cards
(overfit + cross-org risk, violates D5a guardpost rule); manual-only per-org
(wastes the locked DSPy+GEPA engine).

---

## 7. Residue ledger (carried to plan)

1. Event-count canonicalization (13 vs "12"); Logician blocked-gate →
   `GrantWorkEventRejected`? ; CycleReceipt `trace_id` existence check.
2. Card-edit versioning / rollback; mutation ordering when two packets touch
   one card field; new-Insight consent-tier default.
3. JSONL replay performance at scale; per-CIC redaction rule authoring;
   analytics-method implementations not vendored.
4. OQ-4 enum unification; D5a "no metric hill-climb" assertion in
   `PromotionAuthorityPolicy`; OQ-9 matrix coupling must not re-enter via
   candidate generalization.
5. Held-out evaluation set composition for C16 (diverse enough to lift the
   guardpost, not one funder); calibration-param search space for D5; what
   counts as a passing KPI delta per optimization chain.

Owner for items 1–3: GoldenQuill grant-runtime. Owner for item 4: joint
PromotionGovernance vocabulary owner. Owner for item 5: GoldenQuill
grant-runtime + experiment-harness. None may promote until resolved.
