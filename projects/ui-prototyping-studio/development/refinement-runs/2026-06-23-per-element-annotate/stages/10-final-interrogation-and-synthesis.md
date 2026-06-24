# Stage 10 — Final Interrogation and Synthesis

- Capability: `interrogation` (refine-final) + Refine synthesis
- Status: **flag** (MVP plan ready; honest-diff truth + untagged-apply are named deferrals; one open operator scope decision)

## Owner-boundary check (g06)

- Refine produced: seed, dispatch (validated **pass**), research decision, stage receipts, repaired plan, this synthesis. ✓
- Refine did **not** promote any sigil/spell/inventory/ontology artifact, and did **not** execute studio code. ✓
- Task Session / Sigil Development appear only as **next routes**, not loop stages. ✓

## What the loop established (high-confidence, code-verified)

1. The studio **already has** the skeleton (click→postMessage annotate, `odId`-nullable comments, `/comment` persist, `listPendingComments` drain, two-gate apply, in-page accept/discard/revert). The ask is an **evolution**, not a rebuild.
2. The honest diff's blind spot is **real and specific**: `diffByOdId` **excludes `<style>` nodes** and the `null` bucket is **structural-only** — so theme/token edits are diff-invisible. The fence *rejects* them at apply, so they can't silently ship, but the surface must stop implying "0 changes."
3. Per-element **capture** of untagged elements is cheap and safe (data model already supports it); per-element **apply** of untagged elements is **expensive** (stable-identity vs `GAP-V3-NODE-IDENTITY-008` + the M1 fence) and is correctly deferred.

## Residue carried out of the run (unresolved by design)

- **R-A — Honest-diff truth (S4) is the real engineering and is deferred.** The MVP delivers the *UX* loop (S1–S3) before the *diff-honesty* fix (S4). Until S4b, theme edits remain unsupported-and-disclosed. This is an honest, named gap — but it means "the per-element loop is done" is only true for **tagged/structural** edits at MVP.
- **R-B — Scope-coarsening vs ergonomics (stable disagreement).** Governance wants pointed-at≠applied-to fully recorded (RP-3); ergonomics wants frictionless capture. RP-3 reconciles them with disclosure, but the *experience* of "your comment will apply to the parent instead" is still a friction the operator should validate with real use.

## Open operator decision (g05)

The five forks were resolved as **recommendations** (DD-F1…F5, repaired). One scope choice is genuinely the operator's:

> **Does the MVP stop at S1–S3 (the Figma-feel capture/preview/expand loop, shippable in ~one file each), or must S4 (honest-diff truth for theme/unattributed edits) be in the first cut?**

This changes cost materially (S1–S3 are single-file/dep-free; S4 touches the diff domain + tests).

## Recommended next routes (after operator picks scope)

- `task-session` — build S1 (then S2, S3) as bounded tasks; each is single-file, dep-free, test-green.
- `task-session` (separate) — S4 honest-diff lane, gated by the pre-registered toy-game (recolor `--green` → visible CSS-lane row).
- *optional* `experiment` — run the toy-game as a falsification probe before committing S4's design.
- *optional* `bounded-research` — stable in-DOM element addressing (for the deferred untagged-apply).
