---
docType: handoff
updatedAt: 2026-06-14
source: domainspec→arcanum open-core session
---

# Next Steps — DomainSpec → Arcanum

## Where we are (shipped + verified, public)
- **Keystone live in arcanum:** canonical DS-D1/D2 definitions, TAXONOMY/RELATIONSHIPS example layer, DomainSpec spec template family (define/design/plan stages), invoke `define` cut over.
- **M2 capability sigils (all 6):** definitions-governance registry-aggregation (C1), code-tag-audit (C2, **toolchain runs green**), test-derivation (C3, **L0 engine deterministic + round-trip PASS**), observability-derivation (C4), sync-user-stories (C5), audit-alignment (C6).
- **Private side intact:** moat cluster (CyberAlchemy/DS-F-series) + ambiguous D4/D5/D6 stay in domainspec; every public diff passed a moat-leak audit.

## Prioritized next routes

### P1 — Make the 6 M2 sigils promotion-ready (highest value, low risk)
The new sigils are `status: draft`. Each needs validation examples + a worked run against a real DomainSpec spec before draft→active.
- Route: `sigil-development` (observe/validate) per sigil → promote.
- Owner: sigil lifecycle. Runtime available for the code-bearing ones (C2, C3).

### P2 — Expand the test-derivation engine (C3 next layers)
L0 (state-transition) is proven. Add invalid-transition cardinality, presence/range/count-cap rules, richer TEST-SPEC + runnable scaffolds — keeping determinism + round-trip oracle.
- Route: `invoke plan M2-C3-impl-L1` → `sigil-development` → `task-session`. Verifiable via `tsx`.

### P3 — M3 harvest (the deferred high-value improvements)
From the capability-delta harvest, not yet built:
- ⭐ **interrogation modes** (populate the empty mode contract from DS interview-kits)
- ⭐ **dispatch-spec anti-bias** pairwise-tension check
- workflow-reflect TH1–TH8 thresholds, context-builder scoring, orchestrate planner-gate, implementation-layering drift-audit
- free-standing new sigils: **ontology-view** (unconstructible forbidden edges), **brownfield-translation**, **delegation-adapter**
- Route: `decision-gate` to pick the M3 set → per-capability `invoke plan` → build.

### P4 — Cleanup (separate, non-blocking)
- Physical `module-formulae/` deletion — gated on fixing the **pre-existing** example-runner breakage (6 missing `.codex/commands/invoke-example-*.md` in the parent). Decide: fix the codex example-runner files, or retire the example-runner.
- Full prose de-dup is done; no residual wedge duplication.

## Recommended immediate move
**P1** — promote the M2 sigils (validate + worked examples). It hardens what we just built into usable, governed capabilities before widening scope. Then P2 (engine expansion) since its runtime is proven.
