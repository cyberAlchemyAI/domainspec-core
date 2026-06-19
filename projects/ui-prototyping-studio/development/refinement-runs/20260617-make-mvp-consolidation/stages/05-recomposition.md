---
id: recomposition-make-mvp
run_id: 20260617-make-mvp-consolidation
step_id: s5-s8 (memory + distill + recompose + repair, consolidated)
capability_ref: distill (inline)
updatedAt: 2026-06-17
---

# Recomposition — every accumulated thread → one MVP sequence

## §1 Memory: what's already true (don't rebuild)
- **Built + verified:** mutation core L0–L2; `variants register` (real HTML + `OD_ID_MISSING`); two-gate
  `apply`/`accept`/`discard` + honest od-id diff (live-run proven: candidate "Start free" applied, head rev-0001);
  operating SKILL installed; behavior harness; `openPaths` path-print.
- **Shipped public:** curated studio + open-design refs (MIT + Apache-2.0, licenses included) on arcanum.
- **Decided:** F2 = honest interim (DEC-025); SKILL installed (DEC-026); publish curated (DEC-027).

## §2 The make-it obligations → coverage map (recomposition_proof)
| Obligation (what "make it" means) | Covered by | Status |
|---|---|---|
| The loop runs clean (no erroring documented steps) | **G1** (baseline-commit idempotent) + **G2** (handoff-export standalone) | build-needed |
| I can SEE the variants live in VSCode | **P1** (`studio preview <sid>` served page → Simple Browser) | build-needed |
| I can SEE the change before accepting | **P2** (rendered before/after diff at the gate) | build-needed |
| I can DESIGN UI with it | P1+P2 + open-design refs (published) + SKILL (installed) | enabled by P1/P2 |
| The public deliverable is honest | **DOC** (refresh README/TEST-PROTOCOL: add `preview`, drop the G1/G2-erroring steps; republish) | build-needed |
| Account­ability (agent can't self-dispose) | F2 token | **deferred** (interim accepted, DEC-025) |

**No orphan obligation; no duplicate SWU.** G1/G2 retire the two live-run errors; P1/P2 are the D2/Surface-C
surface; DOC closes the public-honesty loop the publish opened.

## §3 Distill: the single coherent unit
The MVP unit = **"design a real UI through the studio and see it live in VSCode, with no documented step
erroring."** Everything outside that is deferred (P3 annotate, F2 token, OD-id granularity, e2e/M3/SWU-Z).
Rejected alternative units: "ship the full visual+annotate+identity surface" (too big — that's beyond MVP);
"docs-only" (doesn't deliver the see-it goal).

## §4 Route decision (the one ambiguity)
**gaps-then-preview-then-doc** (recorded in dispatch.route_menu): the loop must be clean before a human
runs it (G1/G2), the visual surface is the headline (P1/P2), docs/republish last (DOC) — after the
commands they document exist and work. Rejected: preview-first (ships a clean-looking surface over an
erroring loop), doc-first (documents commands that still error).

## §5 Residue ledger (carried, explicitly deferred — not orphaned)
- **F2 token** (GAP-CORE-IDENTITY-010) — interim accepted; fast-follow when autonomy/injection surface grows.
- **P3 click-to-annotate** — the full visual-ergonomics surface; not needed to *see* the product.
- **OD-id granularity** (GAP-017) — coarse gate MVP; per-component later.
- **Public spec dangling DEC-refs** — sub-item of DOC (neutralize identifiers in the published SPEC/ARCH).
- **e2e Playwright, M3 recorder atomicity, full SWU-Z** — not on the make-MVP path.
