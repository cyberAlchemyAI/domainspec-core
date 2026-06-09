# L0 — Corpus

Source evidence recovered from `projects/goldenquill` @ `codex/goldenquill-client-package`.
Read-only. Each item is a concrete, citable artifact.

## Ontology substrate

- `projects/goldenquill/CLAUDE.md` — CIC (6 Customer Identity Cards) × CLC (8 Capital Logic
  Cards) taxonomy; orthogonality rule; the five card primitives each card configures.
- `projects/goldenquill/assets/cards/customer_identification/`, `assets/cards/capital_logic/` — card assets.
- `projects/goldenquill/pipeline/cards/models.py` — frozen-dataclass card models, lifecycle, signature gate.
- `projects/goldenquill/pipeline/orchestrator/classification_review.py` — per-org signed classification register.
- Admin-Risk Register + Key Facts Register (referenced in CLAUDE.md / institutional_memory).

## Promotion record DAG

- `projects/goldenquill/pipeline/grant_dag/validate.py` — L0 validator, 11 deterministic rules.
- `projects/goldenquill/pipeline/grant_dag/fixtures/promotion_record_l0_fixture_pack.json` — synthetic fixtures (positive + negative).
- `projects/goldenquill/tests/grant_dag/` — L0 tests.
- `projects/goldenquill/docs/strategy/goldenquill_promotion_governance_architecture_design_2026-06-01.md` — execution DAG + ontology DAG, six design views.
- `projects/goldenquill/docs/strategy/goldenquill_promotion_mechanism_research_2026-06-01.md` — promotion unit, state model, owner matrix.
- `projects/goldenquill/docs/decisions/` — ADR-001, promotion mechanism interrogation, open gaps.
- Commit `2822e96` "Add GoldenQuill promotion record DAG"; predecessor `24d04ed` research.

## Business intelligence

- `projects/goldenquill/docs/client-packages/.../evidence_and_kpi_appendix.md` — KPI families with interpretation limits + source rules.
- `projects/goldenquill/pipeline/vault/sub_kinds/cycle_receipts.py` — CycleReceipt (actual vs counterfactual, span-traced).
- `projects/goldenquill/pipeline/orchestrator/seats/wpfa/` — dashboard + buyer-facing PDF emitter.
- `projects/goldenquill/pipeline/vault/sub_kinds/reflection_packets.py` — Reflection Packet (dormant v0.1 hook).

## Agent work

- `projects/goldenquill/CLAUDE.md` — the Council (six seats), Four Autonomy Rules, three routing postures, Five Operating Laws.
- `projects/goldenquill/skills/` — council-pipeline, logician, scout-discovery, judge-rubric, scribe-ghostwriter, editor, red-team, sentinel, etc.
- `projects/goldenquill/logician/logician.py`, `logician/board_health.py`, `logician/gates/workspace_isolation_gate.py` — deterministic policy/health/isolation gates.
- `projects/goldenquill/router.yaml` — seat→model bindings, cross-family rigor.

## Client packaging precedent

- `projects/goldenquill/docs/client-packages/goldenquill_promotion_governance_client_sendable_2026-06-01/` —
  README, MANIFEST, HTML overview, executive_brief, evidence_and_kpi_appendix, client_decisions. The
  closest existing precedent to a CyberAlchemy consulting deliverable.
