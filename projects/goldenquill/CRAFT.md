# CRAFT — GoldenQuill promotion-governance

> Human-readable **view** of `.craft/ledger.yml`. The ledger is the source of truth; do not edit state here. Generated 2026-06-10.

## Contexts

### CTX-GQ-PROMO-GOV (root) — GoldenQuill promotion-governance readiness · stage: validate · gate: **flag**
An event-sourced governance spine where **owner decision alone** converts a learning candidate into approved, scope-bounded reusable knowledge. Designed-not-built; L0 fixture-only/audit-only.
- **Next move:** Resolve OQ-4 decision shape (three surfaces vs single enum) — top P0 (DEC-OQ4).

### CTX-GQ-IMPL-ARCH — Implementation-architecture discovery (victor pattern) · stage: validate · gate: **pass**
Derived the implementation architecture + model READ-ONLY from spec, rendered four victor-pattern views, drift-checked every claim to a spec selector.
- **Next move:** Recomposed into root; optional — link the pack from the feature SPEC.md.

### CTX-GQ-ARCH-DESIGN — Whole-system architecture design (integration + promotion governance) · stage: validate · gate: **flag**
Consolidated baseline + Part II design proposals (D1–D4) for the open decisions; rendered two team-shareable PDFs.
- **Next move:** Take D1–D4 to the team alongside the open-questions PDF; close DEC-OQ4 first.

## Blockers (raw blockers cannot be resolved directly)
| ID | Lane | Status | Closure condition |
|----|------|--------|-------------------|
| BLK-OQ4-VOCAB | governance | active (refined) | Operator confirms three-surface vs single enum; promotion vocabulary LOCKED before L1 |
| BLK-B001-TESTSPEC | validator | active (raw) | TEST-SPEC T1–T35 confirmed stable before TASK-FIX |
| BLK-D5A-THRESHOLD | governance | active (raw) | Machine-checkable "general guardpost" threshold + "no metric hill-climb" in PromotionAuthorityPolicy |
| BLK-OQ13-EDGES | governance | active (raw) | GQ-AMD-001/002 filed; edge-amendments discovery authored for vault graduation |

## Enablers
- **ENA-DISPATCH-ROUTE** — validated, reusable dispatch route (validate-dispatch.py = pass).
- **ENA-IMPL-PACK** — four-view victor-pattern explanation pack, drift-checked.

## Open / blocking decisions
- **DEC-OQ4** *(active, blocking)* — three decision surfaces (PursuitDecision / MatchFitVerdict / OwnerDecision) vs single unified enum. Operator: "let me think." Blocks L1 candidate shape.

## Open architecture proposals (non-blocking — for team decision)
- **DEC-D2-FLIP** — operator-signed per-org Ed25519 flip of `mutation_allowed`, journaled.
- **DEC-D3-SHARED-GATE** — structural "general" rule (no metric hill-climb) + operator card-edit review; links BLK-D5A-THRESHOLD.
- **DEC-D4-VERIFY** — diverse held-out set (≥2 CIC/CLC); reject on negative delta or guardrail significance.

## Closed decisions
- **DEC-PACK-LOCATION** — pack lands under `docs/.../discovery/impl-architecture/`.
- **DEC-USE-CRAFT** — record this work in a goldenquill-scoped Craft ledger.

## Gaps
| ID | Severity | Owner | Summary |
|----|----------|-------|---------|
| GAP-DESIGNED-NOT-BUILT | block | grant-runtime | Learning loop designed, not built (human edits cards by hand) |
| GAP-PROMO-ENFORCE | block | grant-runtime | No centralized promotion-authority enforcement test |
| GAP-L0L1-FLIP | flag | governance | No gate for flipping per-org `mutation_allowed` at L0→L1 |
| GAP-REDACTION-TABLES | flag | governance | Per-CIC redaction rule tables (C14) unauthored |
| GAP-KPI-COUNT | flag | grant-runtime | Prose "47 KPIs" vs enum 44 (verified) — 3-entry gap |
| GAP-EVENT-COUNT | flag | grant-runtime | Event count "13 vs 12" unresolved |

## Candidate definitions (local — not canonical)
- **promotion authority** — OwnerDecision is the only setter of `approved_allowed_uses` (SPEC.md:89; domain.md:216).
- **L0 fixture-only / audit-only** — only C2/C3/C8; `mutation_allowed=false`; no org-vault/card/dashboard write (mappings.md:114; SPEC.md:596-630).

## Recomposition
- **CTX-GQ-IMPL-ARCH → root: pass.** Architecture derived + explained in four views; drift-checked and count-corrected (KPI 44, node-kinds 16, D-E reworded). Residue: KPI 47-vs-44, event 13-vs-12, OQ-4 LOCK pending. Next parent move: resolve DEC-OQ4.

## Artifacts
- `.craft/ledger.yml` (source of truth) · `CRAFT.md` (this view)
- `docs/features/goldenquill-promotion-governance/integration/OPEN-QUESTIONS-LEDGER.md`
- `docs/features/goldenquill-promotion-governance/integration/whole-system-architecture-design.md`
- `docs/features/goldenquill-promotion-governance/discovery/impl-architecture/` (README + 4 views + substrate + drift-check)
- **Team PDFs:** `docs/features/goldenquill-promotion-governance/team-review/open-questions-and-blockers.pdf` · `…/whole-system-architecture-design.pdf`
- Tooling: `.craft/artifacts/render_pdf.py` (Markdown→PDF) · `[repo-root] ops/development/goldenquill-impl-architecture-discovery.dispatch.json`
