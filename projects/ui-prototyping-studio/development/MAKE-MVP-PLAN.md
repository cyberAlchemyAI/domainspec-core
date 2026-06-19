---
id: make-mvp-plan
project: ui-prototyping-studio
title: "MAKE-MVP Plan — design UI in the studio and see it live in VSCode (one converged sequence)"
status: proposal
node_type: implementation-plan
invoke_mode: plan
complexity: medium
source: refinement-runs/20260617-make-mvp-consolidation (consolidates PLAN-STUDIO-PREVIEW + PLAN-D1-D2-D3 + cycle-close-research)
updatedAt: 2026-06-17
---

# MAKE-MVP Plan — the one sequence to a usable studio

**Done = "I can design a real UI through the studio and SEE it live in VSCode, and every documented step
works."** This consolidates every remaining thread into one ordered build. Each SWU is a `task-session`.

## The sequence (ordered; route: gaps → preview → doc)

| # | SWU | Why (the obligation it closes) | Write scope | Acceptance / verify |
|---|-----|-------------------------------|-------------|---------------------|
| 1 | **G1** baseline-commit idempotent | loop runs clean (live-run error #1) | `application/select-or-commit-baseline.ts` + test | `baseline select B` then `baseline commit` succeeds (no `BASELINE_SELECTION_REQUIRED`); suite green |
| 2 | **G2** handoff-export standalone | loop runs clean (live-run error #2) | `application/export-design-handoff.ts` + test | `handoff export` returns a bundle with only the lean docs (optional refs + `missingRefs` note); the accepted-red slice test flips/rescopes |
| 3 | **P1** `studio preview <sid>` | **SEE variants in VSCode** (the ask) | `interface/preview-routes.ts` + `cli/studio.ts` `preview` + static `preview/` page | ephemeral fastify route serves a no-build page; each variant's committed HTML renders in a sandboxed iframe + plain state; opens in VSCode "Simple Browser"; `curl …/variant/B` returns HTML; loopback-only |
| 4 | **P2** rendered before/after diff at the gate | **SEE the change** (irreducible render) | preview page + diff route | a staged candidate shows baseline-vs-candidate side-by-side + honest od-id fragments; human sees it before `accept` |
| 5 | **DOC** refresh + republish public docs | honest public deliverable | `README.md`, `TEST-PROTOCOL.md` (+ neutralize dangling DEC-refs in published SPEC/ARCH) → arcanum | docs add `studio preview`, drop the now-fixed erroring steps; republish to arcanum (submodule-first, bump gitlink) |

## Definition of done (MVP)
A human (you) can: have Claude Code author real variant HTML **grounded in the published open-design refs**
→ `variants register` → `studio preview <sid>` → **see the variants in VSCode** → `comment add` → Claude
proposes a mutation → **see the before/after diff (P2)** → `accept` → a recorded revision. No documented
step errors. That is "UI designed with it," visible in your editor.

## Implementation-layering
- **L0** G1+G2 — clean loop (promotion = both fixes' tests + README steps no longer error).
- **L1** P1 — see variants in VSCode (promotion = served page renders in Simple Browser).
- **L2** P2 — see the change (promotion = staged before/after + honest diff visible).
- **L3** DOC — honest public surface (promotion = republished docs match the working CLI).

## Validation strategy (per slice)
G1/G2 → unit tests + the documented steps stop erroring. P1 → route test (`curl` returns variant HTML) +
manual VSCode Simple Browser render. P2 → staged-session shows before/after + diff. DOC → the published
quickstart runs clean from a fresh checkout. Backend suite (42/42) stays green throughout.

## Deferred (explicitly, not orphaned)
F2 identity-gate token (interim accepted, DEC-025) · P3 click-to-annotate · OD-id per-component granularity
(GAP-017) · e2e Playwright · M3 recorder atomicity · full SWU-Z workspace.

## Recomposition proof
Every make-it obligation maps to exactly one SWU (G1/G2 = clean loop, P1 = see variants, P2 = see change,
DOC = honest public); no obligation orphaned; deferrals named. See
`refinement-runs/20260617-make-mvp-consolidation/stages/05-recomposition.md`.

## Next route
`task-session`: **G1 → G2 → P1 → P2 → DOC**. Fastest "I can see it in VSCode": G1 → G2 → P1.
