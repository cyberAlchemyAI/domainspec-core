# Pattern Extraction Receipts — ontologize fanout

- Dispatch: `ontologize-research-20260608`
- Step: `extract-ontology-dag-patterns` (pattern: fanout, parallel, join: parent_synthesis)
- Source under read: `projects/goldenquill` @ branch `codex/goldenquill-client-package`
- Authorization: operator approved ("run it"), 2026-06-08
- Boundary: GoldenQuill read-only; no GoldenQuill writes made.

Each finding is tagged **[SB]** source-backed (path), **[RP]** reusable-pattern, or **[H]** hypothesis.

---

## Lane 1 — ontology-pattern-reader

**Structures found (all [SB]):**

- **CIC — Customer Identity Cards** (6 applicant-world archetypes). Each card configures
  five operational primitives: Search Vocabulary, Evidence Schema, Language Register,
  Reporting Rhythm, Capital Logic Activation. `projects/goldenquill/CLAUDE.md`, `assets/cards/customer_identification/`, `pipeline/cards/models.py`.
- **CLC — Capital Logic Cards** (8 funder-side mechanism archetypes). Each carries
  underwriting criteria, evidence weights, reviewer profile, red flags, compliance obligations.
  `assets/cards/capital_logic/`, `pipeline/cards/models.py`.
- **Card models** — Pydantic frozen dataclasses with lifecycle state (draft → review_passed →
  signed → deprecated), research metadata, Ed25519 signature, `runtime_loadable` gate.
- **Classification register** — per-org, operator-signed YAML mapping each field to an authority
  class (public / shareable / confidential / operator_flagged). `pipeline/orchestrator/classification_review.py`.
- **Admin-Risk Register** — flagged-term register with severity tiers + per-CLC dialect mapping.
- **Key Facts Register (KFR)** — applicant facts with verbatim-quote provenance + per-field class.

**Mechanics ([SB]):** CIC × CLC are **orthogonal** — no design-time coupling; matching is
opportunity-driven at runtime. `F-CIC-CLC-COUPLING-VIOLATION` fail-closes any baked binding.
Cards are immutable at runtime (frozen + signed); closed-set enums fail-closed on invalid.

**What generalizes ([RP]):** CIC → _customer/segment ontology_; CLC → _revenue/funding-mechanism
ontology_; classification register → _data-governance register_; admin-risk register → _compliance
& market-dialect register_; KFR → _customer/project fact register_; the orthogonality rule →
_don't hardcode segment×mechanism bindings; match at runtime_.

**Residue:** card runtime concept-graphing is named but dormant (`NotImplementedError` at v0.1);
sector enum vs CIC reconciliation open; Memory Evidence Packet schema unsettled.

---

## Lane 2 — dag-promotion-reader

**DAG structure (all [SB], `pipeline/grant_dag/validate.py`, `fixtures/promotion_record_l0_fixture_pack.json`, `docs/strategy/goldenquill_promotion_governance_architecture_design_2026-06-01.md`):**
Two linked graphs.

- **Execution DAG** — what happened, in order: run_context → scout_discovery → scout_verification
  → operator_review → rfa_dissection → kgie_preflight → scribe_draft → editor → judge → red_team
  → logician_gate → operator_signoff → delivery_envelope. Edges: `precedes`, `consumes`, `emits`,
  `blocked_by_gate`, `revised_by`, `approved_by`, `delivered_as`.
- **Ontology DAG** — meaning/authority: grant_outcome_event → application_lifecycle_state →
  grant_kpi_observation → **promotion_candidate** → **owner_decision** → ontology_vault_projection.

**Promotion state machine ([SB]):** captured → candidate → reviewed → decision_pending →
{promoted | rejected | retired | contradicted}. Reuse permitted only within the target's rules
after an owner_decision.

**Deterministic gates — L0 validator enforces 11 rules ([SB]):**

- GQ-PR-L0-001 evidence requires source (type+locator+captured_at)
- GQ-PR-L0-002 KPI requires denominator definition
- GQ-PR-L0-003 application stage ≠ outcome truth
- GQ-PR-L0-004 candidate requires a contradiction path
- GQ-PR-L0-005 no `approved_allowed_uses` without an `owner_decision_ref`
- GQ-PR-L0-006 org-scoped feedback → workspace reuse requires redaction/generalization
- GQ-PR-L0-007 projection requires non-empty evidence_refs
- GQ-PR-L0-008 KPIs cannot trigger promotion directly
- GQ-PR-L0-009 projection record_kind must be `promotion_record`
- GQ-PR-L0-010 approved decision requires approved_allowed_uses + valid decision_source
- GQ-PR-L0-011 candidate requires non-empty proposed_allowed_uses

**What generalizes ([RP]):** generic chain `events/runs → evidence → candidate insight →
governed review (privacy + contradiction + semantics gates) → promoted/retired knowledge`.
Eight reusable primitives: source-truth discipline; evidence≠candidate≠promotion; metric≠authority
(anti-Goodhart); privacy-safe generalization boundary; mandatory contradiction path; stage≠outcome≠
validation; two-stage allowed-uses (propose vs approve); governance layer orthogonal to execution
(audit integrity).

**Residue:** L0 is synthetic-fixtures-only; owner-decision persistence TBD; PromotionRecord home
(sibling vs projection of Ontology Vault) unresolved; KPI denominator authority TBD.

---

## Lane 3 — bi-value-reader

**BI artifacts ([SB]):**

- **Evidence & KPI appendix** — 6–7 KPI families (Lifecycle Depth, Outcome Evidence, Quality &
  Review Movement, Strategy Fit, Effort & ROI, Capacity & Relationship), each metric carrying
  interpretation limits + source-validation rules. `docs/client-packages/.../evidence_and_kpi_appendix.md`.
- **CycleReceipt** — actual vs counterfactual dollars + watt-hours; every claim traces to a Logfire
  span_id + Coefficient Registry version. `pipeline/vault/sub_kinds/cycle_receipts.py`.
- **WPFA dashboard + buyer-facing PDF emitter** — per-org/per-quarter rollups; every dollar links to
  coefficient + cycle_id + trace. `pipeline/orchestrator/seats/wpfa/`.
- **Reflection Packet** — pattern observations (frequency/severity), proposed lessons gated by
  frequency≥2 OR severity=HIGH, span provenance. `pipeline/vault/sub_kinds/reflection_packets.py`.

**Structure → insight ([SB]/[RP]):** the ontology + DAG prevent _metric collapse_. A flat
dashboard win-rate hides lifecycle depth, realization gap, evidence class, and promotion owner.
Embedding each KPI in the source-backed chain + authority model + governance gate makes metrics
auditable ("here is the trace_id", not "the model's best guess") and prevents private signal from
leaking into shared learning.

**What generalizes ([RP]):** (1) traceable, evidence-linked metrics that cannot silently drift;
(2) a governed observe→propose→approve learning loop; (3) private↔reusable signal separation via
classification; (4) a signed decision-accountability ledger. Plus a reusable "you paid X vs
counterfactual Y = delta, with proof" receipt pattern.

**Residue:** Reflection Packet producer dormant until v0.2; coefficient registry external; on-hardware
energy measurement v1.x.

---

## Lane 4 — agent-work-reader

**Structures ([SB]):**

- **The Council** — six seats: Scout, Scribe, Editor, Judge, Red Team, **Logician** (deterministic
  Python + Cedar, zero-token, fail-closed, cannot be overridden). `CLAUDE.md`, `skills/`, `logician/`.
- **Four Autonomy Rules** — Save State Always; **Test Your Own Work (Rule 2 — the "magic step")**;
  Be Explicit (typed handoffs: input path, output path, scope, done-definition); Clean Output.
- **Classification-driven routing** — three postures (Frontier-Eligible / Split-Context Hybrid /
  Local-Only) decide cloud vs local per call, gated by the signed classification register.
- **Cross-family rigor** — Judge ≠ Scribe model family; Red Team ≠ either. Structural independence.
- **Board Health detector** — classifies degraded seat output and runs a remedy ladder. `logician/board_health.py`.
- **Org-isolation gate** — path-level fail-closed confinement to the active org's vault. `logician/gates/workspace_isolation_gate.py`.

**How ontology+DAG drive agents ([SB]/[RP]):** CIC/CLC cards + classification register decide
_routing_ (which seat, cloud vs local); the promotion DAG + Logician gates make output _trustworthy_;
Rule 2 self-validation makes silent partial output impossible.

**What generalizes ([RP]):** ontology-driven agent routing + deterministic governance gates (not
LLMs) + per-seat self-validation + structural isolation — portable to any company's agent workforce
(sales, compliance, risk worked as concrete examples).

**Residue:** Report track / Data Collector / Report Generator are v0.2; multi-tenant hardening v2.

---

## Lane 5 — client-packaging-reader

**Package anatomy ([SB], `docs/client-packages/goldenquill_promotion_governance_client_sendable_2026-06-01/`):**
six interdependent artifacts — README (cover + reading order), MANIFEST (inventory),
HTML overview (visual entry point), executive_brief (≈400-word positioning + benefits),
evidence_and_kpi_appendix (taxonomy / reference), client_decisions (open governance questions
that become the spec). Separates _value framing_ from _implementation requirements_ from _reference_.

**Framing moves ([SB]/[RP]):** (1) "learning loop, not document production"; (2) source-backed
evidence discipline as rigor ("award notification ≠ post-award performance"); (3) privacy-aware
reuse; (4) owner-approved (not algorithmic) promotion; (5) meaningful KPIs beyond win rate;
(6) traceable authority chain as an audit feature. Shows architecture/KPIs/evidence; hides code,
model names, infra.

**What generalizes ([RP]):** a reusable client-deliverable template —
`README + MANIFEST + HTML overview + executive_brief + reference_appendix + client_decisions` —
plus a 5-beat value-prop script (name status-quo pain → reframe as learning/governance layer →
separate authority from observation → provide a taxonomy → close with governance decisions).

**Residue / gaps ([H]):** no meta-metrics on whether governance itself works; no buyer-readiness
scaffolding; client decisions lack consequence/cost statements; no current→target transition plan;
failure modes not in buyer language. These are direct backlog items for a CyberAlchemy offer.
