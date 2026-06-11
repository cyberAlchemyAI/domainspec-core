# Victor ↔ Promotion-Governance — Implementation Layering

- Status: draft (non-executed plan)
- Updated: 2026-06-10
- Dispatch: `gq-victor-promotion-integration-2026-06-10` (step `s5-layering`)
- Input: [runtime-design.md](runtime-design.md)

Layers run from a minimum working unit (fixture-only proof) to the governed
promotion loop. Each layer names its value, its cost boundary, and the
recomposition proof that it still fits the whole.

---

## L0 — Event-spine + projection proof (fixture-only)

- **Value:** prove the seam shape is real before any production wiring.
- **Build:** event envelope schema (C3), JSONL journal + idempotency index
  (C2, fixture form), DAG projector (C4), `OntologyVaultProjection` audit-only
  (C8), positive/negative fixtures, deterministic validator.
- **Boundary:** no UI, no real importer, no memory writes, no signed-card
  mutation, `mutation_allowed=false`. Matches [SPEC.md](../SPEC.md) §596–621
  and the existing [TEST-SPEC.md](../TEST-SPEC.md) T1–T35.
- **Recomposition proof:** the 35-case fixture corpus replays to a stable DAG +
  KPI read model with idempotent re-acceptance.
- **Cost:** low — pure Python + Pydantic, no new vendors.

## L1 — Live capture on one org, read-only governance

- **Value:** real council cycles emit real events; KPIs + candidates compute;
  governance validates but **promotes nothing**.
- **Build:** AdapterProducer wrappers (C1), `RecordOutcomeEvent` +
  `outcome_source` adapters, KPI engine (C5, `numpy`/`scipy`), L0 analytics
  registry (C6), candidate builder (C7), `ScopeAndPrivacyGate` (C9),
  `F-PROMOTION-*` codes (C13). Vocabulary reconciliation (D-D) landed.
- **Boundary:** SQLite migration only if >50k events/cycle; per-org
  `mutation_allowed` may flip true; shared-card mutation still blocked.
- **Recomposition proof:** a full MycoSymbiotics cycle produces a candidate
  that stops cleanly at `decision_pending` with evidence + contradiction path.
- **Cost:** medium — freezes `numpy`/`scipy` into the Golden Image.

## L2 — Owner-gated reuse (the closed D7 loop)

- **Value:** Victor's D7 learning loop runs end-to-end with governance.
- **Build:** `RecordOwnerDecision` + Ed25519 validation (C10),
  ApprovedReusePacket store + future-context hydrator (C11), per-CIC redaction
  tables (C14), Victor operator card-edit gate (C12).
- **Boundary:** per-org hydration auto-applies; shared-card promotion requires
  `composable_with_others` + operator card-edit review; D5a "guardpost level,
  no metric" asserted in `PromotionAuthorityPolicy`.
- **Recomposition proof:** an approved per-org packet hydrates the next Scout/
  Scribe run; a shared-card packet is held at the operator gate, never auto.
- **Cost:** medium-high — operator UX + signing chain + rollback design.

## L2.5 — Improvement loop (promotion → *proven* better)

- **Value:** close the gap between an approved lesson and a measurably better
  artifact. This is what makes the system *self-improve* rather than merely
  *remember*. Closes Victor D5 (calibration) and completes D7.
- **Build:** improvement engine (C15) — per-org auto-refine via **DSPy+GEPA**,
  shared-card refinement via operator edit; improvement verification (C16) —
  re-run a diverse held-out grant set, compute the KPI delta against the
  optimization chain's expected delta.
- **Boundary:** a refinement goes live only on a positive held-out delta
  (R-007); regression → reject + residue. Shared cards lift to the **guardpost
  level** (D5a), never overfit one funder. DSPy+GEPA stays offline / library-dev
  only, per locked substrate.
- **Recomposition proof:** a Rubric Coverage Lift chain produces a refined
  `food_systems` card whose held-out `rubric_coverage` beats baseline; a
  refinement that doesn't beat baseline never ships.
- **Cost:** high — eval-set curation, DSPy+GEPA pipelines, calibration search.

## L3 — Scale + advanced analytics (v0.2 horizon)

- **Value:** multi-org fleet (Stage 2 "Twelve Tilths"), richer learning.
- **Build:** DuckDB journal if warranted; L1–L4 analytics methods with bias
  gates; Reflection Packet producer flip; card-edit versioning/rollback.
- **Boundary:** Law-3 multi-tenant proven before any cross-org opt-in; heavy
  stats stack (`scikit-learn`/`statsmodels`/causal) vendored only here.
- **Recomposition proof:** twelve isolated orgs share zero per-org state; only
  `composable_with_others` insights ever reach shared cards.
- **Cost:** high — new vendors, multi-tenant hardening.

---

## Critical path

L0 (fixture proof) → **D-D vocabulary reconciliation** (blocks L1 candidate
shape) → L1 (live read-only) → **D-C per-org mutation flip** → L2 (owner-gated
reuse) → **L2.5 improvement loop** (the actual self-improvement: apply +
verify). The two hardest gates are human, not technical: shared-card promotion
review (C12) and the joint PromotionGovernance vocabulary LOCK (D-D). The
hardest *technical* gate is C16 — proving a refinement actually helped before
it ships.
