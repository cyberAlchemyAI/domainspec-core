---
id: refine-review-ui-ux-interaction-skill
project: ui-prototyping-studio
title: "Refine-Review (s3) — Ergonomics-Critic Interrogation of the Define + Flow X-Ray"
status: review
node_type: refine-review
run_id: 20260616-ui-ux-interaction-skill
dispatch_id: refine-ups-ui-ux-skill-20260616
step_id: s3-review
capability_ref: interrogation
mode: refine-review
pattern: validation
lens: ergonomics-critic
role_id: ergonomics-critic
consumes_frame: frame.evidence-baseline
consumes_handle: handle.define
emits_decision: decision.define-ready
updatedAt: 2026-06-16
---

# Refine-Review (s3) — Ergonomics-Critic Interrogation of the Define + Flow X-Ray

> **What this stage does.** It attacks the s2 define + x-ray (`stages/02-define-and-flow-xray.md`)
> through the ergonomics-critic lens — *independent of the designer* (dispatch subagent_strategy:
> "the ergonomics critique must be independent of the designer to be honest"). It tests four things:
> (1) is **who-leads-when** right at every step — is the agent ever given an unaccountable durable
> action, or is the human burdened where the agent should lead; (2) is the annotation flow genuinely
> **low-friction** against the cold-start findings, not just asserted; (3) are the **criteria** (the
> rubric the tournament inherits) the right ones; (4) **what is missing** — error/empty states, how
> the human SEES the diff, keyboard/AT parity coverage, decision-paralysis on 1–3 variants.
> It does **not** redesign (s5/s6) or prove ergonomics (s8). It emits `decision.define-ready` with a
> pass/flag/block verdict and concrete, owner-routed fixes.
>
> **Receipts consumed.** `frame.evidence-baseline` (s1), `handle.define` (D1–D5, s2). The critique
> cites `[xray §N]` for the define artifact and `[s1 §N]` for the context pack.

---

## 0. Verdict (up front)

**FLAG — define is structurally sound and proceed-able, but six concrete gaps must be carried as
named obligations into s5/s6 before the design can be called ergonomically honest.** None rise to
*block*: the who-leads-when spine is correct (no agent durable action survives scrutiny — §1), and
the gates-only-on-durable rule holds. But the x-ray (a) under-specifies the degraded paths the
cold-start user is *most* likely to hit, (b) leaves "how the human sees the diff" — the strongest
disposal-side ergonomic — undefined, (c) carries a keyboard-parity inconsistency between §3.2 and
§5.3, and (d) ships a rubric whose build-cost axis can quietly trade away the very root-causes this
run exists to close. The six FLAGs and one near-block are below; each is routed to an owning stage.

| # | Finding | Severity | Owner |
|---|---|---|---|
| F1 | Agent-triggered synthesize (step 6) can freeze the human's annotation set without the human leading the "I'm done annotating" moment | **FLAG (who-leads-when)** | s6 design |
| F2 | No error / empty / degenerate states anywhere in the 12-step map; the `discard` path is absent entirely | **FLAG (missing — highest cold-start exposure)** | s2 amend → s5/s6 |
| F3 | "How the human SEES the diff" (steps 9–10) is undefined — visual vs textual diff is left open, and a textual diff re-introduces cold-start root-cause #7 | **FLAG (missing — load-bearing ergonomic)** | s6 design (ODQ-4) |
| F4 | Keyboard-parity (`a11y.3`) is tagged on steps 4–5 only in §3.2, but §5.3 requires it on *every* gate (7, 9, 12) — the map under-states a hard-gate obligation | **FLAG (a11y coverage)** | s2 amend (cheap) |
| F5 | Single-variant / decision-paralysis on 1–3 variants is unhandled; step 4 assumes a multi-way choice and inherits cold-start #2 ("no select control for single-variant") | **FLAG (cognitive load / empty state)** | s5/s6 |
| F6 | The tournament rubric (§5.2) weights build-cost (C5) flat against the ergonomic axes, letting the cheapest surface win by trading away C3/C4 — the exact root-causes the run exists to close | **FLAG (criteria)** | s5 tournament |
| N1 | The two-gate accept-diff (steps 9–10) is unbuilt **and** the SKILL teaches only single-gate `batch apply` (§5.4) — the *canonical loop the run blesses* and the *loop the toy-game can actually walk* diverge | **near-BLOCK (must be reconciled before s8)** | s9 plan + s8 scope |

---

## 1. Who-leads-when — is the agent ever given an unaccountable durable action?

**Tested:** I walked all 12 steps [xray §3.2] and tried to find any place the agent (a) owns a
durable/irreversible state transition, (b) can actuate a gate, or (c) can change head/store/clock.

**The spine holds.** The agent's authority is confined to steps 2 (generate+register), 6 (trigger
only), 8 (propose candidate) [xray §3.3]. All three are `reversible`. Gates 4/7/9/10/12 are
human-disposed and refused server-side for a non-human actor (INV-3/4, AC-L0-6/10). Core — not the
agent — computes synthesis (6), stages (9), records (11). **There is no unaccountable durable agent
action.** This is the strongest part of the define and it should be preserved verbatim.

**But one who-leads-when seam is wrong — F1.** Step 6 says synthesize is "Claude Code *or* human;
core computes … either may trigger" [xray §3.2 row 6]. The computation being deterministic protects
*intent fidelity* — the agent cannot reinterpret the notes. It does **not** protect *timing*. If the
agent may trigger synthesize, the agent decides **when the human's annotation set is frozen into a
batch**. A cold-start human mid-annotation (still adding the 3rd of 4 notes) whose agent helpfully
runs `synthesize` has had the "I am done annotating" decision taken from them. That is a durable-ish
boundary (the batch is what the human then approves at gate 7) being led by the agent.

- *Who-leads-when:* the **human** must lead the "annotation set is complete" moment; the agent may
  *offer* ("want me to turn these 4 notes into a draft change?") but not *initiate* the freeze.
- *Cognitive load:* agent-initiated synthesize forces the human to notice a state change they didn't
  ask for (the opposite of recognition-over-recall — it's surprise).
- *Fix (route s6):* make synthesize **human-initiated by default**; if the SKILL.md permits the agent
  to run it, require the narration "I'll only synthesize when you say you're done annotating" and a
  re-open path (annotations remain append-only and a re-synthesize supersedes — already reversible per
  [xray §3.2 row 5], so the fix is cheap). The define should state this explicitly rather than leave
  "either may trigger" flat.

**Secondary (accept, not block):** step 8 (agent proposes candidate) has no human-visible artifact
between 8 and the diff at 9. That is *correct* — the human shouldn't review a pre-diff candidate; the
diff at 9–10 is the review surface. Engine-purity (value-in/value-out) plus deterministic admit means
the agent cannot smuggle a divergent candidate past core. No finding; noted so s6 doesn't "helpfully"
add a redundant pre-diff gate (which would be friction on a reversible step — clause 4).

---

## 2. Is the agent burdened-onto-human anywhere (the inverse failure)?

**Tested:** the inverse of F1 — is the human made to do work the agent should lead?

- **Step 1 (prompt)** — human-only is correct; intent capture is irreducibly human. No finding.
- **Step 5 (annotate)** — human authors, agent never annotates. Correct: the agent annotating "for"
  the human would be exactly the unaccountable durable action clause 1 forbids [xray §4.3]. No finding.
- **Step 3 (review)** — human leads, but the x-ray asserts "recognition + comparison" without saying
  what the *agent* does to lower that load. The agent could narrate ("variant 2 differs from 1 only in
  button placement") to convert raw comparison into guided recognition. The define assigns the agent a
  narration duty at gates [xray §4.4] but **not** at the review step. This is a *missed* agent-leads
  opportunity, not a burden-misplacement — routed into F5's cognitive-load fix.

**Net:** the human is not over-burdened on the durable gates (those are correctly theirs). The only
human-side load gap is *unguided comparison* at step 3, folded into F5.

---

## 3. Is the annotation flow genuinely low-friction — or asserted?

This is the heart of the run (the annotation decision, [s1 §2]). The cold-start findings [s1 §4] name
the friction the new flow must *beat*, with the explicit caveat that they were measured against the
**old React workbench**, not the CLI/overlay — only the *vocabulary and conceptual* friction transfers.

**What the x-ray gets right.** Step 5 correctly replaces recall (type a selector) with recognition
(point at the component) and captures `data-od-id` [xray §3.2 row 5]. That is a real friction
reduction *in kind* and it directly attacks root-cause #4-jargon. The keyboard constraint is named.

**Where the friction claim is over-stated — and must be re-scoped, not deleted.** Several rows state
friction reduction as accomplished fact while the accomplishment is *conditional on unbuilt surface
behavior*:

- Step 2: "removes the hidden prerequisite chain (root-cause #5) **IF the surface shows progress**."
- Step 6: "removes the disconnected Mutation-panel ritual (#3) **IF surfaced near the note**."
- Step 3: "**the single biggest cold-start win**."
- Step 5: "removes typed-selector jargon (root-cause #4)."

The "IF" clauses are doing heavy lifting: the friction is **closeable by the surface**, not **closed
by the define**. Per charter clause 5 [s1 §0] and the x-ray's own stance ("asserts no ergonomic gain"
[xray §2]), these should read as *targets* ("addresses root-cause #N") not *outcomes* ("removes"). The
distinction matters because the toy-game (s8) is the cheapest *falsification* [s1 §6 ODQ-7], and if the
define already records the win as done, s8 has nothing to falsify.

- *Fix (cheap, route s2 amend or carry as s3 ruling):* downgrade every "removes / closes / win" verb
  in §3.2 to "is the affordance that *targets* root-cause #N; gain is `human_study` residue until s8."
  This is consistent with §2's carried gap and just makes §3.2 match it.

**Caveat-transfer is unexamined — sub-finding.** The cold-start findings are against a 7-panel React
workbench. Surfaces B (TUI) and C (local web page) inherit a *different* friction profile than the
overlay (A): e.g. root-cause #4 ("no live preview") is *structurally unclosable* in a pure TUI (B)
[xray §5.1 B cost/risk] — the x-ray says this, but the friction table is applied uniformly across all
three contenders. The define should state that **the cold-start root-cause closure is surface-specific
and is itself a tournament input** (it already is — C3 — but §3.2 reads as if the closure is settled).
Folded into F6.

---

## 4. Missing — the degraded paths (F2, the largest gap)

The 12-step map is a **happy path**. Every step assumes success. The cold-start user — the exact
reader this run serves — spends *most* of their friction budget in the degraded states, and the
original findings are dominated by them (disabled-without-reason #2, no-visible-confirmation #3,
opaque-output #6). The x-ray has **no step, invariant, or ergonomics rationale for any of:**

1. **Generation fails / returns zero variants** (step 2). What does the human see? The cold-start
   finding #5 is precisely "hidden prerequisite chain signaled only by disabled buttons." A failed
   generate with no plain-language reason re-creates root-cause #2 at the very first agent action.
2. **`data-od-id` absent → selector fallback flagged non-durable** (step 5). [s1 §2] says the overlay
   "falls back to the CSS selector and flags the target as non-durable." This is a *partial-success*
   state with real ergonomic stakes (the human's note may break on regenerate) and it appears nowhere
   in the map.
3. **`discard` — the entire reject branch is missing.** [s1 §1.2] and [s1 §7] name `accept`/`discard`
   as the two-gate apply outcomes. The map has step 10 = accept only. **What happens when the human
   sees the diff and rejects it?** Where do the annotations go — preserved, re-openable, lost? A
   disposal gate with only the "yes" path is not a gate; it's a confirmation. This is a who-leads-when
   *and* a missing-state defect: the human's "no" is the most important accountability signal and it
   has no home in the define.
4. **Empty / single-variant** (steps 3–4) — see F5.
5. **Batch apply conflict / nothing-to-apply** (step 9) — if synthesize produced an empty or
   conflicting batch, the map has no degraded branch.

- *Severity:* FLAG, but it is the finding with the **highest cold-start exposure** — the naive user
  meets these states first and they are where the old workbench failed hardest.
- *Fix (route s2 amend for the map skeleton; s5/s6 for the surface treatment):* add a **degraded-state
  column or companion table** to §3.2 naming, per step, the failure/empty/partial state, who leads the
  recovery, and the plain-language reason the human must see (`a11y.5` disabled-reason contract). At
  minimum the **discard branch must become a named step (10b)** with its own who-leads-when and an
  explicit ruling on annotation fate. Until discard exists in the define, the loop is not closed.

---

## 5. How the human SEES the diff (F3 — the strongest disposal ergonomic, left open)

Steps 9–10 are the irreversible boundary — the place [s1 §5] calls "registered, not rubber-stamped"
(`human.2`). The x-ray tags them `cog.5 screenshot_review` (salience) and `a11y.4` (focus-trap), but
**never says what the diff IS to the human's eye.** Two very different renderings both satisfy "honest
diff":

- a **visual** before/after of the rendered component (closes cold-start root-cause #4 "no live
  preview of the applied change" — the whole reason the overlay exists), versus
- a **textual** `OdDiffFragment` / `DiffSummaryHonest` count (`diff=2/1/0`) — which is *precisely*
  cold-start root-cause #7 ("unlabeled `diff=2/1/0`, no plain summary") re-introduced at the most
  consequential gate.

A focus-trapped, keyboard-operable, salient dialog that shows an unreadable textual diff passes every
tagged ux-evidence check and still fails the human. The define classifies the diff's *container*
(`a11y.4`, `cog.5`) but not its *content legibility*. This is the single highest-leverage ergonomic in
the loop and it is undefined.

- *Fix (route s6 / ODQ-4):* the define should add a fixed obligation to §5.3 — **the accept-diff must
  render the change visually (rendered before/after of the affected `data-od-id` region) with a
  plain-language summary, not a count** — and classify it (`screenshot_review` for salience +
  `human_study` for "did the human actually understand what they accepted," the `human.2` residue).
  ODQ-4 already owns "how is the diff rendered"; this finding *raises its priority from open-question to
  a winner-obligation* and ties it to root-cause #7, which the current §5.3 does not.

---

## 6. Keyboard / accessibility coverage (F4)

`a11y.3` (governance gates fully keyboard-operable, **hard_gate/block**, [s1 §5]) is a *block-class*
constraint on **every** tier-2 disposal. §5.3 states this correctly: "every gate disposal must be
keyboard-operable … step 4/5/7/9/10." But the **map (§3.2) tags `a11y.3` only on steps 4 and 5.**
Steps 7 (approve), 9 (apply), 12 (handoff) carry `flow.2` / `cog.5` / `human_study` in their
ux-evidence column with **no keyboard tag**, and step 12 (terminal handoff disposal) is not in §5.3's
list at all.

This is an internal inconsistency, not a design error — but it under-states a block-class obligation
on three of five gates, and a reader of §3.2 alone (the map is the artifact s5 consumes most) would
miss it.

- *Fix (cheap, route s2 amend):* add `a11y.3 hard_gate` to the ux-evidence cell of steps 7, 9, 12, and
  add step 12 to the §5.3 list. Also state the **focus-order / announcement** expectation once
  (`a11y.5` disabled-reason must be `aria-describedby`-associated, not just present in DOM — the s1
  finding flags exactly this gap). Accessibility here is not a per-surface nicety; it is the
  block-class floor every contender must clear, and the map should show it on every gate.

---

## 7. Decision-paralysis and the degenerate variant count (F5)

Charter clause 2 bounds comparison breadth to ≤3 [s1 §0] and the x-ray honors the upper bound
[xray §3.2 row 3]. But the **lower** bound is unhandled:

- **1 variant:** cold-start finding #2 is explicit — "**no select control for single-variant**." Step
  4 ("select baseline — human picks the option to iterate on") *assumes a choice among multiple*. When
  the agent returns one variant, "pick the option" is a non-action with a confusing gate. The define
  needs a ruling: does a single variant auto-baseline (with narration), or is the human still made to
  "select" one of one (the old workbench's exact failure)?
- **3 variants:** the load is asserted as "recognition + comparison breadth," but **nothing in the map
  lowers the comparison load** — three rendered variants with no agent guidance is recall-heavy
  ("which differed how?"). Per §2 above, the agent's narration duty [xray §4.4] stops at gates and
  doesn't cover the *compare* step.

- *Fix (route s5/s6):* (a) define the single-variant path (recommend: auto-select with a one-line
  narration "only one option was generated; it's selected — annotate it or ask for more"); (b) extend
  the agent narration duty to **step 3**: the agent states *what differs between variants* so the human
  recognizes rather than recalls. Both are who-leads-when refinements (agent leads the *framing* of the
  choice; human leads the *choice*), and both reduce decision-paralysis directly.

---

## 8. Are the criteria the right ones? (F6 — the rubric the tournament inherits)

The 5-axis rubric §5.2 (C1 who-leads-when clarity, C2 cognitive load, C3 friction reduction, C4
annotation fidelity, C5 build cost) is the convergence_criteria the dispatch hands the tournament. Two
problems:

**(a) Build-cost is not an ergonomic axis and must not trade against the others.** C5 is a *project
constraint*, not a measure of human work. Scored flat alongside C1–C4 in a pareto, a cheap surface
(B/TUI) can dominate by winning C5 and C1 while **losing C3 (friction) and C4 (annotation fidelity) —
the two axes that encode the run's entire reason to exist** (close root-cause #4, give click-on-
component annotation, [s1 §2]). The first principle is ergonomics [s1 §0]; build cost is a tie-break /
feasibility filter, not a co-equal vote. As written, the rubric permits an ergonomically-worse-but-
cheaper winner and calls it pareto-optimal.

- *Fix (route s5):* re-class C5 as a **gating constraint / tie-break**, not a scored axis — or state a
  **lexicographic order** (C3+C4 are the run's defining objectives; a surface that fails to close
  root-cause #4 cannot win regardless of C5). The §5.3 "fixed obligations any winner must satisfy" is
  the right mechanism; **move the cold-start root-cause-#4 closure and click-on-component annotation
  into §5.3 as obligations**, leaving C5 as a tie-break among surfaces that already clear them.

**(b) Two axes are missing from the rubric.** The findings above expose two dimensions the rubric does
not score, yet they are where the cold-start user actually fails:

- **Degraded-state legibility / recoverability** (F2) — how well each surface handles fail/empty/
  discard. A surface can ace the happy path and collapse on the first error.
- **Diff legibility** (F3) — does the surface render the change *visually* (C-style web / overlay) or
  only textually (B/TUI)? This is decisive for the irreversible gate and is currently invisible to the
  rubric.

- *Fix (route s5):* add **C6 degraded-state legibility** and fold **diff legibility into C3 or as C7**,
  each with a tie-break source (cold-start #2/#3/#7; `human.2`).

**What the rubric gets right:** C1 (who-leads-when clarity) is the correct primary axis and maps to
`human.1`; C4 (annotation fidelity) correctly preserves the recorded annotation decision. Keep both.

---

## 9. The two-gate / single-gate divergence (N1 — the near-block)

This is the load-bearing residue the define handed me [xray §7] and it is the one finding close to
*block*. The define resolves ODQ-6 with the two-layer scoping rule §5.4: the **SKILL teaches only the
runnable X2 subset** (single-gate `batch apply`, no `accept`/`discard`), while the **canonical loop
§3.2 keeps the two-gate accept-diff (steps 9–10)** as the target, flagged DRIFT and pushed to the s9
plan as a build dependency. Each half is internally defensible. **Together they create a contradiction
the run cannot defer past s8:**

- The **canonical who-leads-when map** (the primary deliverable, what s5/s6 design against) blesses a
  **two-gate** flow with a saw-the-diff accept (step 10) — the strongest disposal ergonomic.
- The **runnable** flow (what the SKILL teaches, what a real session executes, what the toy-game s8
  must walk) collapses 9+10 into a **single-gate `batch apply`** with **no saw-the-diff step at all**.

So: **which flow is `define-ready`?** If the run blesses the two-gate target, then s8's dual
walkthrough **cannot actually be run** on the runnable CLI — the most consequential gate (accept-diff,
the `human.2` "registered not rubber-stamped" probe) does not exist to walk. The toy-game would either
walk a flow that isn't built or simulate one that the SKILL forbids the agent to invoke. Either way the
gate g5 evidence (named friction on a *real* session) is compromised at the exact step that matters
most.

- *Severity:* near-BLOCK. Not a block today because the define **does** name it (it is honest about the
  DRIFT). It becomes a block if it reaches s8 unreconciled.
- *Fix (route s9 plan **and** s8 scope — must be settled before s8):* the run must make an explicit
  ruling, recorded now as an s3 obligation:
  1. **either** scope s8's walkthrough to the **runnable single-gate** flow and explicitly mark the
     saw-the-diff accept as *walked-in-simulation-only, evidence = design-intent not session-fact*
     (honest, cheap, but the strongest ergonomic stays unfalsified — acceptable only if §9 plan
     commits to building the two-gate apply as the first post-run SWU);
  2. **or** make the two-gate apply a **precondition** the s9 plan must satisfy before s8 can claim
     real evidence (more expensive, but the only way the `human.2` probe is honest).
  The define should not be allowed to carry both the two-gate canonical map and the single-gate SKILL
  forward without naming which one s8 will actually test. **This is the one item I require resolved
  before `decision.define-ready` flips to a clean pass.**

---

## 10. What the define got right (preserve — do not let s5/s6 erode these)

So the downstream stages do not "fix" things that are correct:

- **The gates-only-on-durable rule** [xray §3.3] — 5 gates, all clause-4-justified, zero gates on
  reversible drafts. This is the cleanest part of the design. Any s5/s6 surface that adds a gate on a
  reversible step (e.g. a "confirm annotation" gate, a pre-diff candidate gate) **re-introduces
  friction and violates clause 4** — reject it.
- **Engine purity / value-in-value-out at step 8** — the agent cannot touch store/clock/append. Keep.
- **Two artifacts, separate readers** [xray §1.3] — correct partition; do not merge the SKILL and the
  surface into one document.
- **No ergonomic gain asserted** [xray §2] — clause 5 honored at the framing layer (the §3.2 verb
  over-statement in F3 is the only slip, and it's cheap to fix).
- **The narration duty as the agent-side jargon fix** [xray §4.4] — correct division of labor with the
  surface; F5 only *extends* it to the compare step.

---

## 11. Decision — `decision.define-ready`

**FLAG — proceed to s4/s5 with six carried obligations; one (N1) must be resolved before s8.**

The define is a genuinely good x-ray: the who-leads-when spine is correct and the gates are honestly
justified. It is not *block*-grade because nothing in it is wrong-and-dangerous; the agent is never
given an unaccountable durable action (the one timing seam, F1, is a refinement not a breach). It is
*flag*-grade because it is a happy-path map that under-specifies exactly the degraded states, the diff
legibility, and the rubric-weighting where the cold-start user actually fails — and because it carries
forward a two-gate/single-gate contradiction that will compromise s8 if left unreconciled.

**Carried obligations (each routed):**

| Obl | Becomes | Owner | Gate tie |
|---|---|---|---|
| F1 | Synthesize is human-initiated by default; agent may offer, not freeze | s6 design | g4 |
| F2 | Add degraded-state column to §3.2; **discard becomes named step 10b** with annotation-fate ruling | s2 amend → s5/s6 | g4 |
| F3 | Accept-diff must render the change **visually + plain summary**, not a count; add to §5.3 obligations | s6 design (ODQ-4) | g4 |
| F4 | Tag `a11y.3` on gates 7/9/12; add 12 to §5.3; require `aria-describedby` disabled-reason | s2 amend | (a11y.3 block-class) |
| F5 | Define single-variant path; extend agent narration to the compare step (3) | s5/s6 | g4 |
| F6 | Re-class C5 build-cost as tie-break; move root-cause-#4 + click-annotation into §5.3 obligations; add C6 degraded-state + diff-legibility axis | s5 tournament | g3 |
| **N1** | **Ruling on which flow (single- vs two-gate) s8 actually walks; record before s8** | **s9 plan + s8 scope** | **g5** |

**ODQ status after this review:** ODQ-6 stays resolved (§5.4) **but is reopened in scope** by N1 — the
resolution is correct for the *SKILL target* and incomplete for the *toy-game target*. ODQ-2/3/4 gain
priority (F3 raises ODQ-4 from open-question to winner-obligation; F2 sharpens ODQ-2). ODQ-7 (minimum
claim) is *strengthened* by F3's verb-downgrade ruling: the run may claim "the design *targets* these
root-causes"; it may not claim closure until s8.

---

## 12. Stop condition + receipts

- **Define attacked through the ergonomics-critic lens** (who-leads-when §1–2, friction §3, missing
  §4–7, criteria §8, the carried residue §9). **Met.**
- **Independent of the designer** — this is the s3 critic role, not the s5/s6 author. **Honored.**
- **Pass/flag/block + concrete, owner-routed fixes** (§0 table, §11 table). **Met.**
- **g4-ergonomics-rationale:** the critique itself states who-leads-when / cognitive-load / friction
  for every finding (F1, F5 explicitly; F3/F6 via the rubric). **Discharged as a review.**
- **g6-owner-boundary:** this stage emits a *review decision* only; no SKILL install, no SPEC mutation,
  no redesign — fixes are *routed* to owning stages, not authored here. **Honored.**

**Frame handoff:** consumed `frame.evidence-baseline` + `handle.define`; emits `decision.define-ready =
FLAG` with the §11 obligation table. **Residue carried to s4/s5:** N1 must be ruled on before s8 or g5
evidence is compromised; the §3.2 friction verbs should be downgraded from "removes" to "targets" so s8
has something to falsify (ODQ-7).
