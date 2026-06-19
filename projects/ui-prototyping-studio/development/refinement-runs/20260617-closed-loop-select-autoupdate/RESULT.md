---
id: result-closed-loop
project: ui-prototyping-studio
title: "RESULT — closed-loop select + auto-update (feasibility + design)"
status: pass
node_type: refinement-result
run_id: 20260617-closed-loop-select-autoupdate
dispatch_id: refine-ups-closed-loop-select-autoupdate-20260617
capability_ref: refine
updatedAt: 2026-06-17
---

# RESULT — is it possible? YES.

## Answer
**Yes — select-in-preview → Claude Code auto-picks-up → proposes → stages → (auto-)accepts → preview updates
is feasible.** Two new segments vs today: (a) selection capture (browser→studio write), (b) agent pickup.
Per the owner principle shift below, the control is **reversibility, not gating** — the agent may run the
full loop including accept; the one human checkpoint is the irreversible export edge.

## Decisions
1. **Agent-pickup mechanism:** **next-turn drain (B) now** (trivial) → **watch loop (A, Claude Code `/loop`)
   for the "automatic" feel**; event-bridge (C) rejected (over-infra, fights the turn-based runtime). A is
   feasible because the runtime already has `/loop`/`ScheduleWakeup`.
2. **Control model (owner, supersedes the original "accept is human-only"):** **reversibility, not gating.**
   We do NOT distinguish human from agent. The agent may auto-accept; safety = every action is undoable
   (`discard`/`revert`) + visible (preview). The one human checkpoint is **export/handoff** (irreversible).
3. **Selection capture w/o breaking sandbox:** keep `/raw/variant` fully sandboxed; add `/annotate/variant`
   = the trusted variant wrapped with ONLY a click→`postMessage` script; parent POSTs the comment.

## Load-bearing residue — RESOLVED by principle shift (2026-06-17, owner)
Original residue: a watch loop seemed to re-raise F2 (a human-vs-agent identity gate). **Owner decision:
control is REVERSIBILITY, not gating.**
- **F2 is DROPPED** — DEC-F2-INTERIM-025 superseded ("won't build the identity gate").
- New invariant: every in-studio action is undoable + visible. `discard` reverses staging (exists);
  **`revert` must reverse accept** (NEW — append an inverse revision at a prior `candidateHtmlHash`; the
  append-only log + content-addressed HTML already preserve every prior state by hash; head never rewinds).
- The agent may run the full loop incl. **auto-accept** — safe because reversible + shown in the preview.
- The single human checkpoint moves to the **irreversible export/handoff edge**. Became plan SWU **CL5**
  (revert + export-confirm), replacing the F2 token.
- Follow-up (flagged, not silently applied): the installed SKILL never-do line "agent must never accept"
  must be rewritten to the reversibility principle before publish.

## Toy-game (falsification, updated)
click→comment→agent-pickup→stage→(accept)→preview-shows; **and `studio revert` restores the pre-accept HTML
with the log showing both events.** The loop closes AND every step is walk-back-able.

## Plan
`PLAN-CLOSED-LOOP.md` — CL1 capture · CL2 next-turn drain · CL3 watch loop · CL4 auto-refresh · **CL5
reversibility guarantee (revert + export-confirm, replaces F2)**. Builds on the live preview + two-gate apply.

## Stage evidence
s1–s10 pass (design consolidated in stages/05-design.md; plan in PLAN-CLOSED-LOOP.md). Research: research-if-gap,
no external pass triggered (the patterns — /loop, postMessage, SSE — are known; this is an architecture decision).

## Recommended next routes
`task-session`: CL1 → CL2 → CL4 (closed loop, visible) → **CL5 (revert + export-confirm — the reversibility
guarantee)** → CL3 (unsupervised watch, safe once CL5 lands). The MAKE-MVP doc-refresh (DOC) still pending
your public-push go.
