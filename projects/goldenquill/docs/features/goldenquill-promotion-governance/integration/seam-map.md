# Victor ↔ Promotion-Governance — Seam Map

- Status: draft
- Updated: 2026-06-10
- Dispatch: `gq-victor-promotion-integration-2026-06-10`
- Evidence step: `s2-seam-xray` (4 read-only seam agents, join=parent_synthesis)

## The one-line finding

`projects/goldenquill/victor/` and
`docs/features/goldenquill-promotion-governance/` are **two halves of one
system**. Victor's engineer-view names **D7, the learning loop, as
"designed, not built — CRITICAL."** The promotion-governance feature is the
**L0 buildout spec for exactly that loop**: typed event journal → execution
DAG → KPI observations → promotion candidates → Ontology Vault governance →
owner decision → approved reuse packet → future grant context.

"Integrate" therefore means: **wire the promotion-governance event/DAG/
governance machinery onto Victor's already-locked council, substrate, and
ontology storage**, and close the four seams below.

Sources: [victor/engineer-view.md](../../../../victor/engineer-view.md) §5 (D7 verdict);
[architecture.md](../architecture.md) View 2; [SPEC.md](../SPEC.md) §39–51.

---

## Seam 1 — Event emit / listen

**Map: council seat → AdapterProducer → GrantRunNode.** Each Victor council
seat becomes an `AdapterProducerKind: seat` that emits a typed
`GrantWorkEvent`, projected to one of the ~14 mandatory `GrantRunNode` kinds:

| Victor seat (engineer-view §3) | AdapterProducerKind | GrantRunNode kind |
|---|---|---|
| Scout DISCOVER / VERIFY | `seat` (+ `portal` source) | `scout_discovery_record`, `scout_verification_record` |
| operator go/no-go | `operator_upload` | `operator_review_decision` |
| Scribe | `seat` | `scribe_section_draft` |
| Editor | `seat` | `editor_suggestion_report` |
| Judge | `seat` | `judge_score_report` |
| Red Team | `seat` | `red_team_review` |
| Logician (deterministic) | `seat` | `logician_gate_result` |
| Uploader | `uploader` | `delivery_envelope` |
| WPFA CycleReceipt | `wpfa_cycle_accountant` | `cycle_receipt_recorded` (operational) |
| Reflection Packet (v0.2) | `reflection_packet` | `reflection_packet_recorded` |
| portal/agency/email outcomes | `outcome_source` | `GrantOutcomeEventRecorded` |

**Three observability layers are distinct and must not be merged:**

1. **Logfire traces** (LOCKED substrate) — real-time spans; observability,
   **not** authority. Cannot be replayed; no idempotency.
2. **`pipeline/metrics/session_log.jsonl`** — per-agent CI/process metrics;
   unrelated to grant-work authority.
3. **Event journal** (new) — the only replayable, idempotent, source-backed
   authority store. `CycleReceipt` and `Reflection Packet` are **adapters**
   that read Logfire spans and emit typed events into this journal; they do
   not create DAG authority until accepted + projected.

The 13 domain events in [events.md](../events.md) wire emitters →
`AcceptGrantWorkEvent` → `ProjectEventToDag` / `…ToLifecycleAndKpi` →
`CreatePromotionCandidate` → `ValidatePromotionGovernance` → privacy gate →
`RecordOwnerDecision` → `PublishApprovedReusePacket` → `HydrateFutureGrantContext`
(consumers: Scout, Scribe, Judge, Logician, Funding Goal, memory query).

**Open decision (resolved in runtime-design §D-A/D-B):** the event journal is
a *new* durable store, not Logfire and not `session_log.jsonl`.

**Residue:** event-count (13 vs "12") needs canonical enumeration; Logician
blocked-gate → does it also emit `GrantWorkEventRejected`?; CycleReceipt
`trace_id` existence validation (anti-phantom-cost).

---

## Seam 2 — Ontology storage

**Victor owns production knowledge stores; promotion-governance owns the
decision.** No store is duplicated.

| Store | Owner / isolation | Role in the loop |
|---|---|---|
| `pipeline/cards/CIC/*`, `pipeline/cards/CLC/*` | shared, owner-gated | shared-card promotion **target**; refined to "guardpost level" only (D5a) |
| `orgs/<slug>/match_database/register.yaml` | per-org, Law-3 (F-MATCH-DB-CROSS-ORG) | outcome source + consent-tier transitions |
| `orgs/<slug>/vault/key_facts_register/` | per-org, Law-3 | per-org hydration target (append-only) |
| `orgs/<slug>/vault/classification/register.yaml` | per-org, Ed25519-signed | drives privacy gate + routing |
| `pipeline/institutional_memory/admin_risk_register.yaml` | shared | policy primitive |
| **ApprovedReusePacket** (new) | promotion-governance | decision artifact → hydrates future context |

The `OntologyVaultProjection` is **audit-only, `mutation_allowed = false` in
L0** ([mappings.md](../mappings.md) §OntologyVaultProjection). The
promotion split is enforced by storage boundary:

- **Per-org target** (KFR / Match-DB): append-only, auto-applies after owner
  approval, no cross-org tier check. Offline-friendly.
- **Shared-card target** (CIC/CLC): requires `source_consent_tier ==
  composable_with_others` **and** a Victor operator card-edit review. Never
  automatic.

**Open decision (resolved in runtime-design §D-C):** ApprovedReusePacket lands
at `vault_shared/promotion_governance/approved_reuse_packets/<packet_id>.yaml`;
hybrid apply model (per-org auto, shared-card operator-gated).

**Residue:** no version/rollback for in-place card edits; mutation ordering
when two packets touch one card field; consent-tier default for a new Insight.

---

## Seam 3 — Vendor / substrate

Victor's substrate is **LOCKED** (engineer-view D2 / ADR-001): Pydantic AI,
Logfire, Ollama/vLLM, DSPy+GEPA, Python+Cedar, weasyprint — on a 128 GB
offline appliance with a frozen Golden Image (no marketplace/network fetch).
Promotion-governance is implementation-agnostic, so **almost every component
maps onto the locked stack**:

| Component | Locked-substrate answer |
|---|---|
| event_spine, execution, metrics, promotion, reuse | Pydantic (frozen models) |
| ontology_vault, privacy, validate | Cedar + deterministic Python (Logician); fail-closed |
| observability | Logfire ("OTel-style", per observability.md) |
| analytics_methods (L0) | `numpy` + `scipy.stats` |

**Two genuinely open vendor decisions:**

1. **Event-journal durable store** — no locked answer. Options: JSONL (zero
   deps, transparent replay), SQLite (ACID + `INSERT OR IGNORE` idempotency),
   DuckDB (columnar, good for L2+ analytics), embedded event store (rejected:
   violates no-marketplace). **Recommended: JSONL for v0.1**, SQLite migration
   at ~50k events/cycle, DuckDB if analytics mature to L2+.
2. **Analytics libraries** — freeze `numpy` + `scipy` for L0 methods
   (descriptive cohort, funnel, sequence, anomaly). **Defer** `scikit-learn`,
   `statsmodels`, `pymc`, `causalml` (100 MB+) to v0.2 L1–L4.

**Residue:** JSONL replay performance at scale; per-CIC redaction rule tables
not yet authored; analytics-method implementations not vendored.

---

## Seam 4 — Governance vocabulary / authority

Both specs prevent auto-promotion through an operator gate, but use different
words. Victor reifies a single typed **Promotion gate** (decision +
`operator_signature: ed25519` + `consent_tier_check`); promotion-governance
splits it into three operations (`ValidatePromotionGovernance` →
`RedactionGeneralizationGate` → `RecordOwnerDecision`).

Term reconciliation (canonical = promotion-governance's richer model):

| Victor | promotion-governance | Verdict |
|---|---|---|
| `confirmed_fit` | `approved` | align |
| `rejected` | `rejected` | align |
| `declined_cycle` | `retired` | partial (promo-gov broader) |
| `pending` | `decision_pending` (candidate state) | partial (different layer) |
| Scout `ACCEPT/REJECT/HOLD` | — (pre-promotion in promo-gov) | **OQ-4 open** |
| `consent_tier` (3, applicant **input**) | `OrgScope` (4, system **derived**) | orthogonal — keep both, map |
| Classification Register (routing) | RedactionStatus (reuse) | orthogonal — two-layer privacy |
| `operator_signature: ed25519` | `decision_source: SourceRef` (generic) | upgrade SourceRef to accept Ed25519 |

**Open decision (resolved in runtime-design §D-D):** create one unified,
jointly-owned **PromotionGovernance** vocabulary that adopts the 4-value
`OwnerDecision` enum, separates consent-tier (input) from OrgScope (derived),
adds Ed25519 validation to `RecordOwnerDecision`, defines the two-layer
privacy model, reifies a single `ScopeAndPrivacyGate`, and adds an
`F-PROMOTION-*` failure-code family.

**Residue:** OQ-4 enum unification; shared-card "no metric hill-climb"
constraint (D5a) must be asserted in `PromotionAuthorityPolicy`; OQ-9 matrix
coupling must not re-enter via candidate generalization.

**OQ-4 candidate resolution (PROPOSED — shape under review 2026-06-10; see
`integration/OPEN-QUESTIONS-LEDGER.md`):** do NOT unify into one enum. The three
vocabularies are three decision surfaces at three layers — `PursuitDecision`
(Scout `accept/reject/hold`, pre-promotion), `MatchFitVerdict` (Match-DB
`confirmed_fit/rejected/declined_cycle/pending`, evidence), `OwnerDecision`
(`approved/rejected/retired/contradicted`, the sole promotion vocabulary). Under
this resolution the `confirmed_fit→approved` and `declined_cycle→retired` rows
above are cross-layer category errors slated for deletion, and `OwnerDecision`
becomes the single enforcement point that may set `approved_allowed_uses`. Rows
left intact pending operator confirmation of three-surfaces vs single-enum.
