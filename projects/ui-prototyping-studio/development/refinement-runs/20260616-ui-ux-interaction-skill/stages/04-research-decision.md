---
id: research-decision-ui-ux-interaction-skill
project: ui-prototyping-studio
title: "Research Decision (s4) — No-Research (Local-First); One Named Gap Held for a Bounded Pass"
status: decision
node_type: research-decision
run_id: 20260616-ui-ux-interaction-skill
dispatch_id: refine-ups-ui-ux-skill-20260616
step_id: s4-research
capability_ref: refine
mode: research-if-gap-appears
pattern: decision
consumes_decision: decision.define-ready
consumes_frame: frame.evidence-baseline
emits_decision: decision.research
updatedAt: 2026-06-16
---

# Research Decision (s4)

> **What this stage does.** It reads the s2 define + s3 ergonomics-critic review and decides whether the
> design needs **one bounded external pass** (e.g. prior art on agentic-tool interaction patterns,
> click-to-annotate overlays, in-context review UX) before s5/s6, or whether the run is **local-first**
> and proceeds on existing evidence. It does **not** run research now. It emits `decision.research`.

---

## 0. Decision (up front)

**NO-RESEARCH — proceed local-first to s5/s6.** Every one of the seven s3 obligations (F1–F6 + N1) is
resolvable from evidence the run **already holds on-record**; none turns on an open empirical question
about how the *outside world* builds these surfaces. The first principle (ergonomics) is unproven, but
the run already names the **cheapest local falsification** for it — the s8 toy-game (ODQ-7) — not an
external study. External prior art would not change any routed obligation and would dilute the
local-first charter.

One **named gap** (G-A11Y) is worth a *bounded* pass and is recorded below so a later stage can pull the
trigger if it actually blocks — but it does **not** fire now, and s5/s6 are not gated on it.

---

## 1. Why local-first is sufficient for the six FLAGs

Each s3 FLAG is a *use-the-evidence-you-have* fix, not an *acquire-new-knowledge* fix:

| Obl | What it needs | Where the answer already lives | External pass needed? |
|---|---|---|---|
| F1 (synthesize timing / who-leads-when) | A who-leads-when ruling | charter clause 1 + the §3.2 reversibility model (annotations are append-only/re-openable) | No — design ruling |
| F2 (degraded / discard states) | The failure/empty/discard branches | s1 §1.2 / §2 / §7 already name `accept`/`discard` + the selector fallback + disabled-reason contract | No — author the branch from on-record states |
| F3 (diff legibility, visual vs textual) | Render obligation on the accept-diff | cold-start root-cause #4 (no live preview) + #7 (unlabeled `diff=2/1/0`) already fix the target | No — local ux-evidence already names the failure mode |
| F4 (`a11y.3` on all gates; `aria-describedby`) | Coverage + association rule | `a11y.3`/`a11y.5` on-record findings (s1 §5); WCAG association is a settled standard, not novel | No — apply the standard already cited |
| F5 (single-variant / compare-load) | Lower-bound ruling + agent narration extension | cold-start #2 ("no select control for single-variant") + the narration duty (xray §4.4) | No — design ruling on a named cold-start state |
| F6 (rubric: C5 build-cost trade; missing axes) | Re-class C5, add C6/diff-legibility | derives entirely from the run's own first principle + the cold-start table | No — rubric edit |

**Read across the column:** the run's evidence base — the cold-start friction table, the five ux-evidence
classes with on-record findings, the SPEC interaction model, the charter clauses, and the built-vs-spec
DRIFT — is *already* the right corpus for all six. The standards-grade items (keyboard parity,
focus-trap, `aria-describedby`) are **resolved fact** (WCAG), not prior art to be discovered. Bringing in
external UX prior art here would (a) not move any obligation and (b) violate the local-first default for
no gain.

## 2. Why N1 is a design ruling, not a research question

N1 (two-gate canonical map vs single-gate runnable SKILL/§5.4 divergence) is the only near-block. It is a
**scoping/sequencing ruling** the run must make about *its own* artifacts — which flow s8 walks, and
whether the two-gate apply becomes an s9-plan precondition. The two options s3 already wrote (§9) are both
internal. **No external evidence can tell the run which of its own targets to test first.** N1 is routed
to s9 plan + s8 scope, unchanged; research does not touch it.

## 3. The one named gap held for a bounded pass (does NOT fire now)

**G-A11Y — keyboard/AT parity pattern for a click-to-annotate overlay (ODQ-3, surface A).** *If* the s5
tournament selects surface **A** (the mouse-shaped browser overlay), the **mechanism** by which a
pointer-first click-to-annotate affordance is given a genuine keyboard/AT-equivalent path
(roving-tabindex element list, command-palette element picker, etc.) is a place where external prior art
(established overlay/annotation a11y patterns) would be *genuinely useful and not already on-record*.

- **Why it is a real gap, not a fix-from-evidence:** F4 settles *that* parity is owed and *that*
  `aria-describedby` is required (settled standards). It does **not** settle the *interaction pattern*
  for keyboard-equivalent element selection over a rendered DOM — that is design prior art the run does
  not currently hold.
- **Why it does NOT fire now:** it is **conditional on s5 choosing A** (B and C are keyboard-native and
  moot it), and even under A it is a *bounded design-pattern lookup*, not a blocker for s5/s6 to begin.
  Firing it now would research a branch the tournament may discard.
- **Trigger to pull (bounded, ≤1 pass):** s5 selects surface A (or an A-leaning synthesis) **and** s6
  cannot discharge ODQ-3 from local convention. Owner: whoever runs s6 design; scope: one pass on
  click-to-annotate / overlay keyboard-AT patterns, time-boxed, findings folded into the §5.3 `a11y.3`
  obligation. **Requires explicit confirmation per the local-first default — not auto-run.**

## 4. Confirmation state

- Bounded research selected by user: **no**
- Gap-triggered research confirmed: **no** (G-A11Y is held, not fired)
- External sources used this stage: **none**
- Default posture: **local-first** (charter); external pass runs only on explicit confirmation when a held
  gap's trigger is met.

## 5. Dependency + handoff

- **Consumed:** `decision.define-ready = FLAG` (s3), `frame.evidence-baseline` (s1).
- **Previous stage status:** `flag` — does not change this decision; a FLAG with locally-resolvable
  obligations is precisely the local-first case.
- **Emits:** `decision.research = NO-RESEARCH (local-first)` with one held, unfired gap **G-A11Y**
  (conditional on s5 selecting surface A; bounded; requires confirmation to run).
- **Residue carried to s5/s6:** if s5 picks surface A, re-check the G-A11Y trigger at s6 before
  discharging ODQ-3.

**Status:** `pass` (decision rendered; no research executed).
