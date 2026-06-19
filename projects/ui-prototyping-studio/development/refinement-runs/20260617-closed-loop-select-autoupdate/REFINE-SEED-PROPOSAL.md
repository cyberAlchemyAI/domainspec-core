---
id: refine-seed-closed-loop
project: ui-prototyping-studio
run_id: 20260617-closed-loop-select-autoupdate
node_type: refine-seed
status: seed
updatedAt: 2026-06-17
---
# Refine Seed — closed-loop select + auto-update
## Target
Select a component in the preview -> Claude Code AUTOMATICALLY picks up the selection -> proposes + STAGES
the update -> preview reflects it; human still ACCEPTS. Feasibility + design + plan.
## Source context (local)
- studio preview (P1/P2, live): read-only sandboxed iframes + before/after + honest diff.
- two-gate apply/accept (MW1): stage (RevisionApplied, reversible) then human accept (head++).
- SKILL never-do spine + authorship rule; DEC-F2-INTERIM-025 (no core identity gate yet).
- Claude Code runtime is TURN-BASED (has /loop + ScheduleWakeup), not a daemon.
## Outcome
Feasibility verdict + chosen pickup mechanism + governance-preserved automation boundary + build plan. Non-executed.
## Params
Preset standard; research-if-gap (local-first; patterns /loop, postMessage, SSE are known); subagents none (inline).
