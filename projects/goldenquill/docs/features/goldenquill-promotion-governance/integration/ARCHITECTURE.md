---
template_id: invoke.architecture
template_type: architecture
applies_to:
  - design
status: candidate
authority_level: invoke-local
observed_capability: invoke
invoke_mode: design
target_artifact: Victor ↔ Promotion-Governance Runtime Integration
target_owner: GoldenQuill grant-runtime + Ontology Vault governance (joint)
promotion_evidence: []
promotion_decision: pending
created_at: 2026-06-10
updated_at: 2026-06-10
---

# Architecture Plan: Victor ↔ Promotion-Governance Runtime Integration

> Authoring provenance: observed capability `invoke`, mode `design`. This
> artifact belongs to the GoldenQuill promotion-governance development cycle.
> It **promotes nothing**; L0 stays fixture-only and audit-only.

## Architecture Intent

Make Victor's **D7 learning loop** ("designed, not built — CRITICAL") buildable
by overlaying the promotion-governance event spine onto Victor's already-LOCKED
council, substrate, and ontology stores — without merging grant-runtime
authority with promotion-safety authority, and without auto-promoting any
shared knowledge.

## Source Contracts

| Contract ID | Source | Required | Notes |
| --- | --- | --- | --- |
| SC-001 | [integration/runtime-design.md](runtime-design.md) | yes | Resolved runtime design; topology + decisions |
| SC-002 | [integration/seam-map.md](seam-map.md) | yes | Four seams with both-side evidence |
| SC-003 | [integration/layering.md](layering.md) | yes | L0→L3 build path |
| SC-004 | [../architecture.md](../architecture.md) | yes | Promotion-governance L0 component contract |
| SC-005 | [../domain.md](../domain.md), [../events.md](../events.md), [../states.md](../states.md), [../mappings.md](../mappings.md) | yes | Entities, 13 events, state machines, OntologyVaultProjection |
| SC-006 | [victor/engineer-view.md](../../../../victor/engineer-view.md) | yes | LOCKED substrate (D2/ADR-001); D7 verdict; Five Laws |
| SC-007 | [ops/development/goldenquill-victor-promotion-integration.dispatch.json](../../../../../../ops/development/goldenquill-victor-promotion-integration.dispatch.json) | yes | Validated dispatch route + boundary evidence |

## View 1: Context View

- **GoldenQuill grant-runtime (Victor)** — owns the council cycle and the
  *event shape*. External actor that produces grant work.
- **Promotion-governance spine** — listens to grant work, records the
  execution DAG, computes KPIs, builds candidates. Owns no promotion.
- **Ontology Vault governance layer** — separate owner of *promotion safety*:
  target routing, evidence sufficiency, approved uses, non-promotion guards.
- **Operator** — the only source of `approved_allowed_uses` (Ed25519-signed).
- **Outcome sources** — portal/agency/email/report; required `source_ref`.

Ownership boundary (dispatch `b1-runtime-vs-governance`): GoldenQuill emits
typed events and candidates only; promotion safety stays with the Vault layer.

## View 2: High-Level Structure View

Three planes, one owner each (dispatch `state_namespace_boundary`):

1. **Council cycle (unchanged)** → thin AdapterProducer wrappers.
2. **Event/governance spine (new)**: journal → accept → project → KPI →
   candidate → vault projection → privacy → owner decision → reuse packet →
   hydrate.
3. **Storage**: per-org sovereign plane (Law-3), shared ontology plane
   (owner-gated), governance/audit plane (append-only, `mutation_allowed=false`
   in L0).

Observability (Logfire, `session_log.jsonl`) is a **separate plane**, never the
source of authority.

## View 3: Low-Level Components View

| # | Component | New? | Substrate | Layer |
| --- | --- | --- | --- | --- |
| C1 | AdapterProducer wrappers | thin | Pydantic | L1 |
| C2 | Event journal + idempotency index | **new** | JSONL→SQLite | L0/L1 |
| C3 | AcceptGrantWorkEvent + receipts | new | Pydantic+Logician | L0 |
| C4 | DAG + lifecycle/KPI projectors | new | Pydantic | L0/L1 |
| C5 | KPI engine (44 KPIs) | new | numpy/scipy | L1 |
| C6 | Analytics registry (L0 descriptive) | new | numpy/scipy | L1 |
| C7 | Promotion candidate builder | new | Pydantic | L1 |
| C8 | OntologyVaultProjection (audit-only) | new | Pydantic+Cedar | L0 |
| C9 | ScopeAndPrivacyGate | new | Cedar+Python | L1 |
| C10 | RecordOwnerDecision + Ed25519 | new | Python+Ed25519 | L1 |
| C11 | ApprovedReusePacket store + hydrator | new | Pydantic/YAML | L2 |
| C12 | Victor operator card-edit gate | new | Python+operator UX | L2 |
| C13 | F-PROMOTION-* failure codes | new | Logician | L1 |
| C14 | Per-CIC redaction rule tables | new | YAML (signed) | L2 |
| C15 | Improvement engine (per-org auto-refine; shared-card operator edit) | new | DSPy+GEPA / operator UX | L2.5 |
| C16 | Improvement verification (held-out eval, KPI-delta gate) | new | experiment-harness + numpy/scipy | L2.5 |

## View 4: Workflow Process View

Per-run flow (one grant cycle): council seats emit events → `AcceptGrantWorkEvent`
(idempotency: dup+same→no-op; dup+diff→fail-closed P0) → DAG + lifecycle/KPI
projection → on cycle close, KPI/outcome → `CreatePromotionCandidate` →
`ValidatePromotionGovernance` → `OntologyVaultProjection` (audit) →
`ScopeAndPrivacyGate` → `RecordOwnerDecision` (operator Ed25519) →
`PublishApprovedReusePacket` → `HydrateFutureGrantContext` into Scout/Scribe/
Judge/Logician.

Failure paths: missing `source_ref` → reject; blocked Logician gate → no
downstream node without reopen evidence; candidate carrying
`approved_allowed_uses` → block (`F-PROMOTION-NO-AUTO-APPROVE`).

## View 5: Decision Flow View

- **Apply route by scope:** `reuse_scope=single_org` → append to per-org
  KFR/Match-DB automatically (post-approval, no tier check);
  `reuse_scope=workspace_global` → Victor operator card-edit gate (manual).
- **Shared-card promotion** requires `consent_tier == composable_with_others`
  **and** owner decision **and** generalized redaction. Never automatic.
- **Privacy is two-layer:** Classification Register (routing) ⟂ RedactionStatus
  (reuse), joined by `ScopeAndPrivacyGate`.
- **Promotion ≠ improvement:** an approved packet is *applied* by C15 (per-org
  auto via DSPy+GEPA; shared-card operator edit) producing a *candidate* refined
  artifact, then **gated by C16** — re-run a diverse held-out grant set and
  compare the KPI delta to the optimization chain's expected delta. Improved →
  promote (per-org auto-apply; shared-card through the owner gate). Regressed →
  reject + residue. No promotion ever changes a live artifact unproven.

## View 6: Dependency Interface View

| Dependency | Direction | Contract | Boundary rule |
| --- | --- | --- | --- |
| Council seats | inbound | GrantWorkEventEnvelope | observation authority only; no DAG/promotion |
| Event journal | internal | EventProjectionReceipt | replayable, idempotent, append-only |
| Outcome sources | inbound | GrantOutcomeEvent | `source_ref` required |
| Ontology Vault layer | outbound | OntologyVaultProjection | audit-only; `mutation_allowed=false` in L0 |
| Future grant context | outbound | ApprovedReusePacket | only approved allowed uses hydrate |
| Logfire / session_log | observe | OTel spans / JSONL | observability only; not authority |

## Constraints

| Constraint | Source | Impact |
| --- | --- | --- |
| LOCKED substrate (Pydantic AI, Logfire, Cedar, Ollama/vLLM) | SC-006 D2/ADR-001 | only open vendoring = event-journal store + numpy/scipy |
| Frozen Golden Image, no marketplace/network | SC-006 | rules out embedded event-store vendors; favors JSONL/SQLite |
| Law-3 per-org isolation (F-MATCH-DB-CROSS-ORG) | SC-006 | per-org stores read-isolated; cross-org blocked |
| D5a: shared cards = guardposts, no metric hill-climb | SC-006 | shared-card promotion bounded; assert in PromotionAuthorityPolicy |
| L0 fixture-only, audit-only | SC-004 | no production memory or signed-card mutation in L0 |

## Dependency And Interface Rules

| Rule ID | Rule | Applies To | Enforcement |
| --- | --- | --- | --- |
| R-001 | Adapters cannot set `approved_allowed_uses` | C1, C7 | schema constraint + F-PROMOTION-NO-AUTO-APPROVE |
| R-002 | Authority only via AcceptGrantWorkEvent + projection | C2–C4 | idempotency index + projection receipt |
| R-003 | `approved_allowed_uses` exist only on OwnerDecision | C10 | ScopeAndPrivacyGate + Ed25519 validation |
| R-004 | Shared-card promotion needs composable_with_others + operator gate | C11, C12 | F-MATCH-DB-CONSENT-TIER-VIOLATION + card-edit gate |
| R-005 | OntologyVaultProjection mutates nothing in L0 | C8 | `mutation_allowed=false` |
| R-006 | Observability planes are not authority | Logfire, session_log | journal is sole replay source |
| R-007 | A refinement goes live only after a positive held-out KPI delta | C15, C16 | C16 verification gate; regression → reject + residue |

## Decision Log

| Decision ID | Decision | Options Considered | Reason |
| --- | --- | --- | --- |
| D-A | Event journal = JSONL (v0.1) → SQLite @50k/cycle → DuckDB @L2+ | JSONL, SQLite, DuckDB, embedded event-store | zero new deps, transparent replay, fixture-testable; offline constraint |
| D-B | Three distinct planes: Logfire / session_log / event journal | merge into Logfire; extend session_log; new journal | only journal is replayable+idempotent+source-backed |
| D-C | Victor owns stores; governance owns decision; hybrid apply | external canonical store; mutate-through; federated | Law-3 + offline; per-org auto, shared-card operator-gated |
| D-D | One jointly-owned PromotionGovernance vocabulary | Victor canonical; promo-gov canonical; dual | promo-gov enum richer; resolves OQ-4; adds Ed25519 + two-layer privacy |
| D-E | Freeze numpy+scipy for L0; defer heavy causal stack | full stack now; hand-code; numpy/scipy | footprint + scope; L0 needs only descriptive stats |
| D-F | Improvement application = both by target (per-org auto / shared-card operator), both C16-verified | auto-all; manual-all; both-by-target | closes D5/D7; respects D5a guardpost + per-org/shared split |

## Risks

| Risk ID | Risk | Mitigation | Owner |
| --- | --- | --- | --- |
| RK-001 | JSONL replay slow at scale | per-cycle segmentation; SQLite migration trigger | grant-runtime |
| RK-002 | Card-edit conflict / no rollback | versioning + operator gate before L2 | grant-runtime |
| RK-003 | OQ-4 enum divergence surfaces externally | LOCK vocabulary (D-D) before L1 candidate shape | joint vocabulary owner |
| RK-004 | Matrix coupling (OQ-9) re-enters via generalization | guard candidate generalization against CIC×CLC binding | governance |
| RK-005 | Per-CIC redaction rules unauthored | author at L2 before workspace reuse | governance |
| RK-006 | Held-out set too narrow → overfit one funder | diverse eval set; measure across CICs/CLCs (D5a) | grant-runtime + experiment-harness |

## Downstream Planning Notes

- Implementation-plan inputs: per-component task specs for C2/C3/C8 (L0), then
  C1/C4–C7/C9/C10/C13 (L1).
- Work-pack implications: L0 SWU = event-spine + projector + audit projection
  against the existing 35-case TEST-SPEC fixtures.
- Validation implications: every slice carries fixture evidence; promotion
  guardrail check (no `approved_allowed_uses` pre-decision) is a gate on each.

## Design Transport Notes

Carry this six-view architecture into `invoke plan` for the L0 work-pack, then
`task-session` for execution. The D-D vocabulary LOCK and C12 operator gate are
human gates and must not be auto-promoted.

## Gate Result

- Status: **pass**
- Reason: six views present; seven source contracts cited; dependency/interface
  rules and decision log populated; promotes nothing; L0 fixture-only preserved.
