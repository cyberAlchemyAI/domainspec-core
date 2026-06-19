---
id: design-closed-loop
run_id: 20260617-closed-loop-select-autoupdate
step_id: s5-s8 (x-ray + tournament + dialectic + toy-game)
capability_ref: distill+invoke+interrogation (inline)
updatedAt: 2026-06-17
---

# Design — closed-loop select + auto-update

## §1 X-ray — where "automatic" actually happens

```
TODAY: the preview is a READ-ONLY viewer (sandboxed iframes). All input is the CLI. No path browser->studio.

TARGET (closed loop), three new segments:
  (a) SELECT  [browser] click a rendered component -> capture its data-od-id + {severity,intent,note}
                 -> POST to the studio (new write route) -> captureCommentEvent (INV-2 gated)
  (b) PICKUP  [agent] Claude Code learns a comment is pending (no batch yet)
                 -> synthesize -> propose candidate HTML (the generative act) -> applyAndStage (M1 validate + stage)
                 -> state RevisionApplied (head NOT advanced)
  (c) REFLECT [browser] preview auto-refreshes -> shows before/after + honest diff
  [human gate] human clicks Accept (or `studio accept`) -> head advances by one
```
**Finding:** only (a) and (b) are new. (c) is a refresh of the existing P1/P2 page. The human gate (accept)
is **unchanged** — "automatic" lives in (a)+(b), and stops at the staged diff.

## §2 Tournament — the agent-pickup mechanism (the crux of "automatically")

| Option | How | automation | governance-safety | build-cost | turn-based fit |
|--------|-----|-----------|-------------------|-----------|----------------|
| **A watch loop** | Claude Code runs `/loop`/poll: every N s, find pending comments -> synthesize+propose+stage | **high (feels automatic)** | OK *iff* loop only proposes+stages, never accepts | medium (loop wrapper + idempotent pickup) | fits (Claude Code HAS /loop + ScheduleWakeup) |
| **B next-turn drain** | selection records a comment; agent drains pending on its NEXT turn (any interaction) | medium (not instant) | **high** (human implicitly in-loop each turn) | **low** (no daemon; "on next turn, check pending") | fits exactly |
| C event bridge (SSE/file-watch launches an agent) | studio emits event -> external trigger invokes Claude Code | high | lower (more moving parts; external launcher) | **high** (new infra; fights turn-based) | poor |

**Pareto pick: A for the "automatic" experience (Claude Code `/loop` watch), B as the cheap honest fallback;
C rejected** (over-infra, fights the turn-based runtime). A is feasible *because* the runtime already has
`/loop`/`ScheduleWakeup` — the loop polls the studio, and the preview the human is watching auto-refreshes.
Recommend: **ship B first (trivial, honest), upgrade to A (the watch loop) for the hands-off feel.**

## §3 Dialectic — automation vs the never-do spine + F2

- **P-automation:** make it fully hands-off (select -> applied).
- **P-governance:** the human disposes durable changes; the agent must never accept (spine; F2: core can't tell agent from human).

**Resolution — the automation boundary is the two-gate seam.** The agent may auto-**propose + STAGE**
(reversible, scope-fenced, `RevisionApplied` not head); the human **ACCEPTS** (durable gate, unchanged).
So "automatically getting the changes and doing the update" = automatic **up to a staged preview the human
sees**; accept stays human. This is exactly what the two-gate design was for — gate 1 automatable, gate 2 human.

**Residue (load-bearing): this RE-RAISES F2.** A watch loop (A) materially increases agent autonomy — the
agent now acts on browser events without a per-action human invocation. So:
- the loop MUST run under a clearly-agent actor (`agent:*`);
- **accept must be human-only** — which is precisely the F2 token's job. F2 moves from "interim accepted"
  toward "needed **before** unsupervised auto-pickup ships." (Mechanism B keeps the human in-loop each turn,
  so it's safe under the F2 interim; mechanism A needs the F2 token first to be safe unsupervised.)

## §4 Sandbox vs interactivity (selection capture)

The preview iframes are `sandbox`-locked (no scripts) for safety — but click-capture needs a script.
**Resolution:** keep the raw `/raw/variant` route script-free (sandboxed). Add a separate **annotate-mode**
render `/annotate/variant/:label` that wraps the (trusted, registered) variant HTML with a *minimal trusted
click->postMessage handler* (the only script; `sandbox="allow-scripts"` for this wrapper only). The parent
page receives `postMessage(odId)` -> opens a tiny comment form -> POSTs to the studio. Raw preview stays
sandboxed; interactivity is opt-in and isolated to the trusted wrapper.

## §5 Toy-game (falsification before planning)

| Case | Steps | Expected |
|------|-------|----------|
| capture | click `cta.primary` in annotate mode -> POST | a CommentEvent with `odId=cta.primary` (selector+elementLabel non-empty, DC-1) recorded; INV-2 gated (rejected pre-baseline) |
| pickup | agent watch tick finds the pending comment | synthesize -> propose -> applyAndStage; state RevisionApplied; staged candidate exists |
| reflect | preview refresh | before/after + honest diff shown |
| **governance** | (no human accept yet) | **head UNCHANGED** until human `accept` — the loop never auto-accepts |
Falsifies "the loop closes" AND "auto stops at staging."

## §6 Feasibility verdict
**YES, possible.** Selection capture = a known pattern (trusted wrapper + postMessage + a write route).
Auto-pickup = Claude Code `/loop` watch (A) for the automatic feel, or next-turn drain (B) now. The
governance boundary (auto up to stage; human accepts) is preserved and is exactly the two-gate payoff.
The one real new risk: the watch loop's autonomy **promotes F2 from interim to a pre-req for unsupervised use**.
