# Refine Result

- Status: **flag** (MVP plan ready; honest-diff truth + untagged-apply named-deferred; one open operator scope decision)
- Target: `projects/ui-prototyping-studio` — annotate/preview surface (per-element Figma-like loop)
- Run manifest: `RUN-MANIFEST.md`
- Evidence index: `evidence-index.json`
- Seed proposal: `REFINE-SEED-PROPOSAL.md`
- Dispatch route: `REFINE-DISPATCH.json`
- Dispatch validation: **pass** (`validate-dispatch.py` → `VALIDATION=pass`)
- Runtime handoff: `RUNTIME-HANDOFF.md`
- Research mode: `no-research` (local evidence decisive)
- Preset: `full`
- Loop count: canonical ten-stage loop

## Dispatch Evidence

- Dispatch ID: `2026-06-23-per-element-annotate`
- Technique overlays: `baseline_sequence`, `route_menu_for_ambiguity`, `dialectic_for_tension`, `xray_for_hidden_structure` — all expressed by steps/gates/receipts.
- Subagent strategy: `recommended` → **authorized**; 6 receipts across two dialectic fan-outs (s03, s07); anti-bias axis ergonomic-freedom ⟷ governed-integrity, grounded by cost.
- Gates: g01 dispatch-valid **pass**; g02 subagent-permission **granted**; g03 receipts **pass**; g04 research **n/a (no-research)**; g05 product-forks **open (1 operator scope decision)**; g06 owner-boundary **pass**; g07 completeness **pass**.

## Stage Evidence

- Context Builder evidence baseline: **pass** (`stages/01`)
- Invoke Define: **pass** (`stages/02`)
- Interrogation refine-review: **flag** (`stages/03` — dialectic, F5 block dissolved, stable residue R1–R3)
- Research decision: **pass** (`stages/04` — no-research)
- Distill: **pass** (`stages/05` — SCU = hover-prefill → click-capture → governed-apply)
- Invoke Redefine / Design: **pass** (`stages/06` — DD-F1…F5)
- Interrogation refine-design-review: **block→repair** (`stages/07` — DD-F5 premise code-disconfirmed; scope-coarsening found)
- Distill Repair: **pass** (`stages/08` — RP-1…RP-7 + toy-game gate)
- Invoke Plan: **pass** (`stages/09` — slices S1–S4)
- Final Interrogation and Synthesis: **flag** (`stages/10`)

## Final synthesis (the answer)

Your vision is an **evolution of plumbing that already exists**, not a rebuild. The studio already does click→annotate, nullable-`odId` comments, server persist, CLI drain (`listPendingComments`), the run-cycle, and two-gate apply. The refinement adds: **hover-prefill of real element properties**, **per-element capture on any element (with disclosure)**, **expand/collapse**, and — the hard part — **honest-diff truth for theme/unattributed edits**.

The loop's decisive finding (verified in code by three independent reviewers): the honest diff **excludes `<style>` and the `null` bucket is structural-only**, so theme-token edits (the `--green` case you hit live) are **diff-invisible**. The fence rejects them at apply, so nothing ships silently — but the surface must stop implying "0 changes." Making theme edits *visible and attributable* (a new CSS-diff lane, **S4**) is the real engineering and is correctly separated from the cheap UX slices.

**Recommended build order:** S1 per-element capture+disclosure → S2 hover-prefill (the Figma feel) → S3 expand/collapse — each ~one file, dep-free, test-green — then **S4** honest-diff truth, gated by the pre-registered toy-game (recolor `--green` must produce a visible CSS-lane row).

## Open decision for you (g05)

**MVP scope:** stop at **S1–S3** (ship the Figma-feel loop fast), or require **S4** (honest-diff truth) in the first cut? This materially changes cost — S1–S3 are single-file; S4 touches the diff domain + tests.

## Recommended Next Routes

- `task-session` — build S1→S2→S3 (bounded, single-file each).
- `task-session` — S4 honest-diff CSS-lane, gated by the toy-game.
- *optional* `experiment` — run the toy-game as a falsification probe before S4.
- *optional* `bounded-research` — stable in-DOM element addressing for the deferred untagged-**apply**.

## Blocked / open fields

- `g05-product-fork-decision`: MVP scope (S1–S3 vs +S4) — operator's call.
- Deferred (named): untagged-element apply (GAP-V3-NODE-IDENTITY-008 + M1 fence); descriptor/DNA extraction; routed full view; optimistic sync.
