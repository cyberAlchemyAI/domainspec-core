# Stage 5 — Distill (x-ray of the concrete unit)

**Verdict: pass.** Research decision: **no-research** (local + master branch).

Distilled the coherent unit from GoldenQuill source (read via git on `master`):

- **5 node types** from `grant_dag/validate.py`: `GrantOutcomeEvent`, `application_lifecycle_state`,
  `GrantKpiObservation`, `PromotionCandidate`, `OntologyVaultProjection`, `OwnerDecision` — [SB, verbatim].
- **11 rules** (GQ-PR-L0-001…011) — [SB, verbatim from RULES dict + validation bodies].
- **Edge set** (`precedes`, `consumes`, `emits`, `blocked_by_gate`, `revised_by`, `approved_by`;
  ontology relations `promotes_to`/`supersedes`/`retires`/`constrains`/`validates`) — [SB].
- **Two-DAG split** (execution vs ontology, audit-immutable) — [SB].
- **KPI families** (6) — [SB, KPI appendix].

Generalization decision (x-ray): map each to a vertical-agnostic node/edge/event/metric, with cap
factory + logistics instantiations. Rejected alternative: invent a fresh model (ignores proven work).

Residue carried: cap-factory run boundary; exact event catalog; per-vertical proof metric; reflection cadence.

Output unit → [DAG-AND-METRICS.md](../../../../DAG-AND-METRICS.md).
