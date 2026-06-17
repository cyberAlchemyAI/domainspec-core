---
id: toy-game-walkthrough-ui-ux-interaction-skill
project: ui-prototyping-studio
title: "Toy-Game Walkthrough (s8) — Dual Walkthrough of the C surface + SKILL on one sample session"
status: walkthrough
node_type: toy-game-walkthrough
run_id: 20260616-ui-ux-interaction-skill
dispatch_id: refine-ups-ui-ux-skill-20260616
step_id: s8-toy-game-walkthrough
capability_ref: task-session
mode: dual-walkthrough
pattern: cold-start + agent-trace
consumes_design: design.interaction
consumes_review: review.design
consumes_handle: handle.define
emits_walkthrough: walkthrough.toy-game
sample_session: "prototype an onboarding card"
updatedAt: 2026-06-16
---

# Toy-Game Walkthrough (s8)

> **What this stage does.** It runs the s6 interaction design + the SKILL (the X2-scoped operating
> contract from s2 §4, corrected by s7 F-CRIT-1) through ONE sample session — **"prototype an onboarding
> card"** — twice, in two independent voices:
> **(1)** a **cold-start naive user** who has never seen the tool, knows only the task goal and what the
> rendered surface shows them, and who receives **no internal rationale** (no charter, no s2 x-ray, no
> who-leads-when map, no SKILL prose); and
> **(2)** a **Claude Code session** driving the `studio` CLI per the SKILL, narrating each command, every
> STOP-and-hand-to-human boundary, and every place the SKILL is ambiguous.
>
> It interprets the friction each voice hits, classifies each finding against the five ux-evidence classes
> ([s1 §5]), and names the required repairs to **the design** and **the SKILL**. It is the cheapest
> falsification of the ergonomics first principle (ODQ-7) — it **prepares evidence, it does not prove
> gains** (charter clause 5; R1 unchanged). It does NOT re-run the tournament, re-author the design or
> SKILL, or build anything.
>
> **Frame receipt.** Consumed `design.interaction` (s6: the C review-page design), `review.design` (s7:
> FLAG + F-CRIT-1 blocking + F1/F2/F3 + M1–M4), and `handle.define` (s2: the 12-step x-ray §3.2, the SKILL
> required-contents §4, the two-layer scoping rule §5.4, the cold-start table §4). Every code/command fact
> the walkthroughs lean on is the s6 §0.1-verified set; this stage adds no new code claims.
>
> **Walkthrough method (so the friction is honest, not narrated-into-existence).** The naive user sees
> ONLY: the task goal in their own head ("make an onboarding card"), and the literally-rendered surface
> (region text, button labels, enabled/disabled state, reason strings). They do not see step numbers,
> "[HUMAN GATE]" tags, the dialectic, or any class label — those are author scaffolding, stripped before
> they look. The Claude Code voice sees ONLY: the SKILL it is bound by, the CLI help/output, and the
> human's typed requests. Neither voice is allowed to "know" the other's reasoning. Confirmation that the
> naive user got no internal rationale is recorded explicitly in §3.0.

---

## 0. Setup — the one sample session, and what each voice is handed

**Sample task (fixed for both voices):** *"Prototype an onboarding card"* — a small UI card shown to a
new user on first login (title, one line of body copy, a primary button). The human wants to: see some
options, pick one, leave a note or two about what to change, get the change made, and walk away with
something they can hand off.

**The surface under test (s6 C):** one same-origin local web review page served by the existing Fastify
app on `127.0.0.1`, three regions — Region 1 (≤3 sandboxed-iframe variant renders), Region 2 (co-located
notes, newest first), Region 3 (the five durable gates as native buttons, each with an enabled/disabled
reason in words). The human opens it in a browser tab.

**The SKILL under test (s2 §4 + s7-corrected):** the X2-scoped Claude-Code operating contract. Posture:
*Claude Code proposes; the human disposes at every durable gate.* It teaches only the **runnable X2
subset** — `variants register`, `synthesize`, `batch approve`, `batch apply`, `comment add`, `baseline
select|commit`, `handoff export` (§5.4) — and names `preview --annotate`, `apply`/`accept` two-gate as
build-dependent. Its never-do spine forbids Claude Code from running `baseline select|commit`, `batch
approve`, `batch apply`/`apply`/`accept`. **Per F-CRIT-1 the SKILL is the binding control on
self-disposal — the core does not distinguish the agent from the human by identity.**

**Drift carried into the walkthrough (so it is realistic, not idealized).** The s6 design's saw-the-diff
two-gate accept (steps 9–10, the `<dialog>`) is **unbuilt (N1)**; the runnable path is single-gate `batch
apply`, which stages AND advances head in one call with **no diff-pause**. The C render route (one GET) is
also **new work** the design specs but the current checkout has not built. The walkthrough runs against
**what exists today** and marks every place the design's intended affordance is not yet there as a
DRIFT-driven friction — that is the point of a toy-game.

---

## 1. WALKTHROUGH ONE — the cold-start naive user (surface only, zero rationale)

> **Persona.** A product designer. Comfortable with Figma and v0. Has never seen this tool. Was told "open
> the link Claude gave you and make the onboarding card you wanted." Sees only the rendered page. Has no
> idea what "baseline," "synthesize," "batch," or "revision head" mean and has read nothing about the
> tool's governance model. **Every reaction below is what the SURFACE caused, with no internal rationale
> available to rescue them.**

### 1.1 Lands on the page (before Claude Code has generated anything)

What they see: a header — `UI Prototyping Studio · session 7f3a · prompt: "prototype an onboarding card"`
— and Region 1 showing the empty state **E-EMPTY-1**: *"Ask Claude Code for a UI to get started."*

- **Reaction (calm, not stuck).** "OK, it knows what I asked for — my prompt is right there in the
  header. It's telling me to ask Claude. Fine." The echoed prompt is the single most reassuring thing on
  the page — it reads as *ready*, not *broken*. **This works.** (counters root-cause #5)
- **Small confusion.** "Ask Claude Code *how*? In this page, or back in my terminal/chat?" The page tells
  them WHAT to do but not WHERE. There is no input box on the page for the prompt (Step 1 in the design is
  "human types in the header," but the surface as drawn shows the prompt as already-captured header text,
  not an editable field). **The naive user does not know the channel.** → **F-COLD-1.**

### 1.2 The variants appear (Region 1, three iframes)

Claude Code generates three onboarding-card variants; the page swaps to three side-by-side renders.

- **Reaction (the big win).** "Oh — there they are. I can actually *see* three cards. This is the v0
  thing I expected." Seeing the rendered options side-by-side is exactly the cold-start payoff the design
  promised (root-cause #4 closed). **This is the strongest moment in the whole session.**
- **Friction — "what just happened / can I trust these?"** There was a gap between "Ask Claude Code" and
  "three cards appeared." If Claude took 8 seconds, did the page show anything? The design says a
  "generating…" state (Step 2) "if the page shows progress" — but the design **never specifies the
  in-between or the never-returns case** (s7 M1). The naive user who saw a blank-ish pause for 10s starts
  to wonder if it hung. → **F-COLD-2** (the generation-progress/timeout gap, surfacing on the naive side).

### 1.3 Wants to comment on a card — but can't yet

They like card #2 but want the button to say "Get started," not "Continue." They click the button in
card #2 to leave a note.

- **What happens:** nothing — or a disabled affordance with a reason: *"Pick an option to build before
  you can comment on it."* (the INV-2 client mirror, §2.3 / §5.1).
- **Reaction (confused, then redirected).** "Wait, I can't comment until I 'pick an option to build'?
  But I'm just trying to leave a note on the one I like. Why is picking and commenting two different
  things?" The reason string IS present (a11y.5 win — far better than a silent dead click), and it does
  point at the next step. But the *concept* — that you must commit to one option before annotating it —
  is **not something the naive user expected**, and the reason string explains the mechanic without
  explaining the *why*. They comply, but grudgingly. → **F-COLD-3.**
- **Confirmation of "no rationale":** the surface gives them the reason ("pick first") but **not the
  rationale** (that annotation is gated on a baseline so the change-set is anchored to a chosen option,
  INV-2). That rationale lives in the SKILL/charter, which the naive user never sees. The reason string is
  the *only* bridge — and it bridges the mechanic, not the meaning.

### 1.4 The gate panel — "Choose this one" (the relabel win, and a residual trap)

They look right (Region 3). The first gate reads **"Choose the option to build → [ Choose this one ]"**.

- **Reaction (the #2-Critical jargon trap, defused).** "Choose this one — that's clear. I click it under
  card #2." The s6 relabel of "Baseline" → "the option you chose / Choose this one" **lands**. The naive
  user never sees the word "baseline" and never has to guess what it controls. This is the design directly
  defeating cold-start finding #2 (Critical). **This works.**
- **Residual trap.** After clicking, the variant they DIDN'T choose are still on screen. Are they gone?
  Can they switch? The design says the choice is "re-selectable pre-apply" (§5.3), but the **surface does
  not say so** — there is no "you can change this" affordance or text. A Figma-trained user fears they've
  locked themselves in. → **F-COLD-4** (reversibility of step 4 is true in the model but invisible on the
  surface).

### 1.5 Now commenting works (the central friction win)

Comment is now unlocked. They click the button element in card #2; it highlights; a small form opens with
three controls — severity, intent, note.

- **Reaction (recognition over recall — the win).** "I clicked the actual button and it highlighted —
  yes, *that's* the thing I mean. I type 'change label to Get started.'" Pointing at the rendered element
  instead of typing a selector is the friction win the design built C for (root-cause #4). **This works.**
- **Friction — "severity? intent?"** The form asks for **severity** and **intent** as required-looking
  controls. The naive user wanted to leave a note, not triage a bug. "What severity is 'I'd prefer
  different button text'? Is 'intent' the same as my note?" These are **internal taxonomy words**
  (CommentEvent fields) leaking to the surface. The note field they understand; severity + intent read as
  jargon with no on-screen glossary. → **F-COLD-5** (the CommentEvent field vocabulary is unexplained;
  cold-start root-cause #8 / #3, jargon, resurfacing inside the comment form).
- **Quiet honesty marker.** Because this button may not have a `data-od-id`, the form shows *"this target
  may not survive a regenerate."* The naive user reads this as faint alarm: "survive a what?" The honesty
  is correct (DC-1, no false fidelity claim) but the **wording is itself jargon** ("regenerate"). →
  folds into **F-COLD-5**.

### 1.6 The note appears co-located (Region 2 win)

Their note shows up immediately below the renders as a plain sentence ("change label to Get started — on
the primary button").

- **Reaction (the co-location win).** "Good, my note is right under the card, I can see what I said about
  what." Co-locating note + render (root-cause #3) **works** — they never lose the thread between the
  thing and the comment about it.

### 1.7 Getting the change made — the multi-gate wall

They've left two notes. They want the card *changed*. Region 3 now shows, top to bottom:
`Approve the change list` (locked — "synthesize your notes first" or similar), `Apply + see the diff`
(locked — "approve the list first"), `Export the handoff` (locked — "land a change first").

- **Reaction (decision-paralysis, the first-class state — partially handled).** "There are three more
  buttons and they're all greyed out with reasons. Which do I press? It says 'approve the change list' —
  what list? I haven't made a list. Where's the 'synthesize' thing the first reason mentioned?" The
  gate-ordering reasons ARE present (a11y.5 / paralysis design §5.3) and the design says exactly one
  primary next-step is marked with `aria-current`. **If that single-primary marker renders, the naive
  user is rescued** ("oh, THIS one is the lit-up next step"). **But** the synthesize step (Step 6) is
  "either actor may trigger" and is a **draft-compute, not a gate** — so it may not appear as a button in
  Region 3 at all, leaving the naive user reading "approve the change list" with **no visible control that
  produces the list.** → **F-COLD-6** (the synthesize/draft step is who-leads-ambiguous on the surface:
  the human is told to approve a list they have no on-screen way to create; they must go back to Claude).
- **Confirmation of "no rationale":** the naive user has NO way to know that synthesize is deterministic,
  core-computed, and triggerable by either actor. That is SKILL/x-ray knowledge. The surface shows a
  locked "approve" with a reason that names a step they can't perform. They are stuck **between** the
  agent's arc and their own.

### 1.8 Approve → Apply → the diff that isn't paused (the DRIFT bite)

Suppose Claude synthesizes; the "Approve the change list" button lights up; they read a plain change list
("1 change: button label 'Continue' → 'Get started'") and click **Approve**. Then **Apply** lights up.

- **Reaction (approve works).** "I can read what's about to change — one change, button text. I approve.
  That's reasonable." Recognizable change list, one decision (the design's §4 intent). **This works as
  far as it's built.**
- **Friction — the saw-the-diff promise is not kept (N1 DRIFT).** The design's centerpiece is step 10:
  click "Apply," see the staged diff in a focus-trapped dialog, THEN accept-for-good. **But the built
  path is single-gate `batch apply` — it stages and advances head in ONE call, no pause, no dialog.** So
  the naive user clicks "Apply + see the diff" and… the change is just *done*. They never saw a diff
  before it landed. The button label **promised a diff they never got.** → **F-COLD-7** (the single most
  consequential surface-vs-build gap on the naive side: the irreversible step happens without the
  saw-the-diff moment the label advertises).

### 1.9 History + handoff (the exit)

History (Region 11 behavior) shows: *"Changed button label to 'Get started' — just now"* with a link
back to their note. The "Export the handoff" gate unlocks.

- **Reaction (history win).** "It shows what changed in words, with a time, linked to my note. Good." The
  plain-summary + timestamp + note-link history (root-cause #7) **works**.
- **Reaction (handoff — partial win).** They click "Export the handoff." The design promises a *visible,
  openable* deliverable (root-cause #6). **If** the export surfaces an openable artifact (a link to the
  rendered HTML), this works. **If** it surfaces a reference ID or a bundle path with no open-link, the
  naive user is back to cold-start #6 ("no visible deliverable"). The design intends the former; the
  surface drawing doesn't pin it. → **F-COLD-8** (handoff visibility depends on an unspecified detail).

### 1.10 Cold-start scorecard (what the surface earned vs. cost)

| Moment | Outcome | Cold-start root-cause |
|---|---|---|
| Empty state echoes the prompt | **Win** — reads as ready | #5 (step-order) |
| Three renders side-by-side | **Win** — the biggest payoff | #4 (no preview) |
| "Choose this one" relabel | **Win** — defuses the #2 Critical "Baseline" trap | #2 jargon |
| Click-element-to-comment | **Win** — recognition over recall | #4 (annotation jargon) |
| Note co-located under render | **Win** | #3 (disconnected note) |
| Plain-language history | **Win** | #7 (raw diff/IDs) |
| Channel ambiguity ("ask Claude *where*?") | **Friction F-COLD-1** | new (surface↔agent seam) |
| Generation progress/timeout gap | **Friction F-COLD-2** | #5 re-formed |
| "Pick before you comment" surprise | **Friction F-COLD-3** | INV-2 mechanic unexplained |
| Step-4 reversibility invisible | **Friction F-COLD-4** | new |
| severity/intent/"regenerate" jargon in the form | **Friction F-COLD-5** | #8/#3 jargon |
| "Approve a list I can't create" (synthesize gap) | **Friction F-COLD-6** | #1 step-order / who-leads |
| "Apply" lands the change with no diff (N1 DRIFT) | **Friction F-COLD-7** | the saw-the-diff promise broken |
| Handoff visibility unpinned | **Friction F-COLD-8** | #6 |
| **Identity-evidence task** | **NOT ENCOUNTERED** — out of scope (L4, `BLK-IDENTITY-TYPES-002`); the naive user never needed it for "an onboarding card," confirming F3's deferral is defensible for this task | #1 (deferred, not dropped) |

**Net.** The surface delivers its headline wins (preview, click-annotate, relabel, co-location, plain
history). The friction is concentrated at **the seams the surface alone can't close**: the agent↔surface
channel (F-COLD-1/6), the un-built saw-the-diff (F-COLD-7), and residual taxonomy jargon the SKILL's
narration was supposed to translate but the *surface* leaks anyway (F-COLD-5).

---

## 2. WALKTHROUGH TWO — the Claude Code session driving the CLI per the SKILL

> **Voice.** Claude Code, bound by the X2-scoped SKILL. It narrates each command it issues, each point
> where it must STOP and hand to the human, and each ambiguity it hits in the SKILL. It sees only the
> SKILL, the CLI, and the human's requests. The human's typed request that opens the session:
> *"prototype an onboarding card."*

### 2.1 Reversible arc — Claude Code leads (Steps 1–2, 6, 8)

**Human:** "prototype an onboarding card."

**Claude Code (narrating, per the §4.4 narration duty):** "I'll make a few onboarding-card options for
you to look at. I'll generate them, then you'll pick one and tell me what to change — I won't decide any
of that for you."

1. **Generate (Step 2, reversible, agent-led).** Claude generates 1–3 onboarding-card HTML variants and
   stamps `data-od-id` on annotatable elements (§4.2). Bound to ≤3 (clause 2).
   - **SKILL-ambiguity A1 — generation has no home command.** §5.4 says the runnable subset is
     `variants register --from <dir>`; both `variants generate` and `variants register` route to the
     **deterministic stub** `generateVariants` ([s1 §1.2 / E3]). So Claude's *own* HTML is supplied via
     `variants register --from <dir>` — but the SKILL does not say **where Claude writes the HTML** before
     registering (a temp dir? whose?), nor how the `--fake` stub interacts when Claude wants real HTML.
     The SKILL teaches the registration *verb* but not the **author-to-disk step before it.** → **A1.**

   ```
   studio variants register --from /tmp/ups-7f3a/variants  --session 7f3a
   ```

2. **Render (Step 3 support).** For the human to *see* the cards, the design adds one new GET render route
   (§2.1). **DRIFT/ambiguity:** that route is **unbuilt** in this checkout, and the SKILL (X2-scoped) does
   **not** teach a render command at all — rendering is the *surface's* job, not a CLI verb.
   - **SKILL-ambiguity A2 — how does Claude open/show the page?** The SKILL forbids "stand up your own
     server" (s7 §6 keep-list) and teaches no `preview`. So Claude's correct move is: tell the human the
     review page URL the *existing* Fastify app serves. But the SKILL does not give Claude the **URL
     shape** or a sanctioned "here is your review page" narration. Claude must improvise the handoff to the
     browser. → **A2** (the agent→browser handoff is undefined in the SKILL).

**Claude narrates:** "Three options are ready. Open the review page in your browser to see them, pick the
one you want, and click any element to leave a note." — **STOP #1: hand to human for Steps 3–5 (review,
choose, annotate).** Claude does not and cannot choose. ✓ (boundary honored)

### 2.2 STOP #1 — the durable boundary at "choose the option" (Step 4)

The human reviews and decides which card to build on. **Claude must STOP here.**

- **Per the never-do spine (§4.3):** `baseline select|commit` is human-only. Claude does **not** run it.
- **F-CRIT-1 surfaces in the agent voice.** Claude *holds the write scope* (it needed it for `variants
  register`). If Claude ran `studio baseline select --variant 2 --session 7f3a`, the **core would accept
  it** — `baseline select` has the same write scope and no human-vs-agent identity check. **Nothing in the
  core stops Claude from self-selecting the baseline.** The *only* control is the SKILL's never-do line.
  - **SKILL must say this honestly (F-CRIT-1).** The corrected SKILL states: "I will never run `baseline
    select`. This is not because the system would stop me — it would not; it cannot tell me from you — but
    because choosing the option to build is *your* decision, and my discipline is the thing that keeps it
    yours." The walkthrough confirms the corrected wording is **load-bearing**: if the SKILL said "refused
    server-side" (the old, false claim), Claude would be resting its refusal on a backstop that does not
    exist. → **repairs S-REP-1** (carry the F-CRIT-1 wording into the do/never-do narration, not just the
    description).

- **SKILL-ambiguity A3 — when the human asks Claude to "just pick one for me."** A real human WILL say
  "they all look fine, you choose." The refusal-narration duty (§4.5) says Claude must *explain the
  boundary, not silently fail*. But the SKILL (visible draft) gives **no scripted refusal for the
  most-likely human ask** ("you pick"). Claude must compose: "I can tell you which I'd lean toward and
  why, but the actual 'choose this one' is yours to click — it's the first point where the work becomes
  *your* committed choice." The SKILL should **supply this refusal-with-recommendation pattern**, because
  the naive user's F-COLD-6 ("which do I press?") is exactly the moment they'll punt to Claude. → **A3 /
  S-REP-2.**

### 2.3 Reversible again — synthesize (Step 6), then STOP for approve (Step 7)

After the human selects a baseline and leaves notes, the human (or Claude) triggers synthesis.

3. **Synthesize (Step 6, reversible, core-computes).**
   ```
   studio synthesize --session 7f3a
   ```
   - Claude may *trigger* this; the **core computes** the batch (§4.2). Claude must not pre-compute or
     substitute the batch. ✓
   - **SKILL-ambiguity A4 — who triggers synthesize, and does the human know it exists?** The x-ray says
     "either actor may trigger." On the surface, the naive user hit F-COLD-6 precisely because **no
     surface control creates the list.** If the SKILL leaves synthesize as "either may trigger," the
     common path is the human, stuck, asking Claude "make the list." The SKILL should make Claude
     **proactively offer** to synthesize after notes exist ("Want me to turn your notes into a draft
     change list you can approve?") so the human is never stranded. → **A4 / S-REP-3** (resolves the agent
     side of F-COLD-6).

4. **STOP #2 — approve (Step 7).** `batch approve` is human-only (§4.3).
   - **F-CRIT-1 again:** `approve-mutation-batch.ts` has **zero actor-class check** — it accepts any
     non-empty `approvedBy`. Claude running `studio batch approve --approvedBy claude-code` would
     **succeed**. The SKILL's never-do line is, again, the **sole** control. Confirmed against the
     corrected wording. ✓ (Claude does not run it.)
   - **Claude narrates:** "I've drafted one change. Approving it is your call — open the page and click
     'Approve the change list,' or tell me you've approved and I'll continue." — hand to human.

### 2.4 The apply boundary — the N1 DRIFT bites the agent too (Steps 8–10)

5. **Propose candidate (Step 8, reversible, staged).** *Within* apply, Claude produces the candidate
   mutation as value-in/value-out, never touching the store/clock/append path (engine purity, §4.2). ✓
6. **STOP #3 — apply/accept (Steps 9–10).** `batch apply` / `apply` / `accept` are human-only (§4.3).
   - **SKILL-ambiguity A5 — the SKILL teaches `batch apply`, which is the single-gate path that BOTH
     stages AND advances head.** The two-layer scoping rule (§5.4) says teach only the runnable X2 subset
     (which includes `batch apply`) and name `accept`/two-gate as build-dependent. So the SKILL's honest
     position is: "the saw-the-diff accept is not built; today applying is one step that lands the change."
     **But this means the SKILL must NOT promise the human a diff-pause that the runnable command does not
     give** — exactly the surface's F-COLD-7. If the SKILL narrates "apply, then you'll review the diff
     before it's final," it lies about the built path. → **A5 / S-REP-4** (the SKILL's apply-narration must
     match the single-gate reality until N1 lands, and say plainly "this applies the change in one step"
     OR route to N1 as a named gap — it cannot describe the unbuilt two-gate accept as current).
   - **F-CRIT-1, sharpest here:** the route **defaults the apply actor to `"web-ui"`** and refuses only
     the literal `"system:auto"`. Claude running `studio batch apply` (or POSTing with any actor ≠
     `system:auto`) would **succeed and advance head.** This is the most dangerous self-disposal and the
     core does not stop it. The SKILL's never-do line is the only guard. Confirmed. ✓ (Claude does not run
     it; it hands to the human.)

### 2.5 Record + handoff (Steps 11–12)

7. **Record (Step 11, core).** After the human applies, the core appends exactly one revision. Claude does
   not touch this. ✓
8. **STOP #4 — handoff export (Step 12).** `handoff export` is the terminal human gate.
   - **SKILL-ambiguity A6 — is export human-only or agent-runnable?** §4.3's never-do spine lists
     `baseline`, `approve`, `apply`, `accept` — it does **not** explicitly list `handoff export`, yet the
     x-ray §3.2 step 12 tags it **[HUMAN GATE] (terminal)**. So the SKILL is **silent/ambiguous on
     whether Claude may run `handoff export`** on the human's behalf. The design treats it as a human
     disposal ("Human disposes (leaves the system)"). The SKILL must **resolve** this: either export is
     human-only (add it to the never-do spine) or it is an agent-runnable convenience after the human's
     accept (then say so). → **A6 / S-REP-5.**

### 2.6 Claude Code command + STOP trace (the whole session)

| Order | Claude action | Command (X2-runnable) | Boundary |
|---|---|---|---|
| 1 | Author + register variants | `variants register --from <dir>` | reversible — agent leads (A1: author-to-disk step undefined) |
| 2 | Point human to the review page | *(no CLI verb; A2 undefined handoff)* | reversible — agent leads |
| — | **STOP #1** | — | **hand to human: review + choose + annotate (Steps 3–5)** |
| 3 | Trigger synthesis | `synthesize` | reversible, core-computes (A4: should proactively offer) |
| — | **STOP #2** | — | **hand to human: `batch approve` (Step 7) — core would NOT stop Claude (F-CRIT-1)** |
| 4 | Propose candidate | *(within apply; value-in/value-out)* | reversible, staged (engine purity) |
| — | **STOP #3** | — | **hand to human: `batch apply` (Steps 9–10) — core defaults actor to web-ui; SKILL is the only guard (F-CRIT-1)** |
| 5 | (core records) | *(none — core-owned)* | irreversible record |
| — | **STOP #4** | — | **hand to human: `handoff export` (Step 12) — A6: SKILL ambiguous on who may run it** |

**What the agent voice proves about the dialectic.** Claude leads exactly the reversible arc (register,
trigger-synthesize, propose-candidate) and STOPS at all five durable gates. The partition holds in
behavior. **But every STOP is held by the SKILL's discipline alone** — at each one, the core would have
let Claude through (F-CRIT-1). The toy-game confirms s7's central finding from the *driving* side: the
SKILL is not merely a usability layer, it is **the security boundary** for self-disposal (with loopback-
only as the network backstop, M4).

---

## 3. Friction findings (with ux-evidence classes)

### 3.0 Confirmation — the naive user received no internal rationale

**Confirmed.** In Walkthrough One the naive user was handed ONLY the task goal and the literally-rendered
surface (region text, button labels, enabled/disabled state, reason strings, empty-state copy, the honesty
marker). They were given **none** of: the charter clauses, the s2 x-ray / who-leads-when map, the
reversible/durable partition, the SKILL prose, the dialectic, the invariant codes, or any ux-evidence
class label. Every place they understood *what to do* came from an on-surface reason string or label
(e.g. "pick an option to build first," "Choose this one"); every place they failed to understand *why*
(F-COLD-3 "why pick before comment," F-COLD-6 "approve a list I can't create," F-COLD-7 "apply with no
diff") is precisely a place where the **rationale lives off-surface** (in the SKILL/charter/x-ray) and the
surface alone did not carry it. This is the intended test condition and it held.

### 3.1 Surface (design) friction — with ux-evidence classes

| ID | Friction | Where (voice) | ux-evidence class | proxy_limit |
|---|---|---|---|---|
| **F-COLD-1** | Page says "ask Claude Code" but not *where* (no on-page channel/seam) | naive 1.1 | `human_study` | we can verify the seam text is absent; not that the human stalled — they may know the chat is elsewhere |
| **F-COLD-2** | Generation progress/timeout unspecified; pause reads as hung (s7 M1) | naive 1.2 | `screenshot_review` (a progress state is present-or-absent) + `human_study` (did it read as broken?) | a screenshot shows a spinner exists; not that the wait felt safe |
| **F-COLD-3** | "Pick before you can comment" (INV-2 mirror) surprises; reason explains mechanic not meaning | naive 1.3 | `soft_flag` (a11y.5: reason string present + associated) + `human_study` (comprehension) | reason presence ≠ the human accepted the constraint |
| **F-COLD-4** | Step-4 choice is re-selectable pre-apply (model) but surface shows no "you can change this" | naive 1.4 | `human_study` | layout/text checkable; "felt locked in" is not |
| **F-COLD-5** | `severity` / `intent` / "regenerate" CommentEvent jargon leaks into the form, no on-surface glossary | naive 1.5 | `human_study` (comprehension) + `soft_flag` (presence of helper text, if added) | we can check helper text exists; not that the words became clear |
| **F-COLD-6** | Human told to "approve the change list" with no surface control to *create* the list (synthesize is a non-gate draft step) | naive 1.7 / agent 2.3 | `hard_gate` (DOM: is there exactly one primary next-step `aria-current`, and does it map to a runnable action?) + `human_study` | DOM can prove a primary marker exists; not that it pointed at a doable action |
| **F-COLD-7** | "Apply + see the diff" lands the change with NO diff-pause (N1 single-gate DRIFT); label promises an unbuilt affordance | naive 1.8 / agent 2.4 | `screenshot_review` (is a diff dialog shown before head advances?) + `hard_gate` (focus-trap, once N1 built) | until N1, this is a **known broken promise**, not a calibratable gate |
| **F-COLD-8** | Handoff deliverable visibility (openable artifact vs. reference ID) unpinned | naive 1.9 | `human_study` | "openable" is checkable once specified; "findable/usable" is not |

### 3.2 SKILL ambiguities — with ux-evidence classes

| ID | SKILL ambiguity | Where (agent voice) | ux-evidence class | proxy_limit |
|---|---|---|---|---|
| **A1** | Generation has no author-to-disk home; SKILL teaches the `register` verb but not where Claude writes HTML first (and the stub/real-HTML interaction) | 2.1 | `not_automatable` (a contract-gap, shape-checkable: does the SKILL name the source-dir step?) | presence of the instruction ≠ the agent produced correct HTML |
| **A2** | Agent→browser handoff undefined: no sanctioned "here is your review page" URL/narration; SKILL forbids standing up a server | 2.1 | `not_automatable` + `human_study` | we can check the SKILL names the handoff; not that the human found the page |
| **A3** | No scripted refusal-with-recommendation for the likely "you pick one for me" ask (refusal-narration §4.5 underspecified for Step 4) | 2.2 | `human_study` | a script can be present; whether the human accepted the refusal is unprovable here |
| **A4** | Synthesize "either may trigger" leaves the human stranded (F-COLD-6 root); SKILL doesn't require Claude to proactively offer to build the list | 2.3 | `not_automatable` (does the SKILL mandate the offer?) + `human_study` | mandate present ≠ stranding removed |
| **A5** | SKILL teaches single-gate `batch apply` (stages+advances) but must not narrate the unbuilt two-gate saw-the-diff accept as current | 2.4 | `hard_gate` (does the SKILL's taught command set ⊆ runnable X2? — shape-checkable against the CLI) | command-set ⊆ runnable is checkable; honest *narration* of it is `human_study` |
| **A6** | SKILL ambiguous whether Claude may run `handoff export` (not in the never-do spine, but x-ray tags it a human gate) | 2.5 | `not_automatable` (resolve to a single owner) | resolved ownership is checkable; correct human expectation is not |
| **F-CRIT-1 (driving-side confirmation)** | At every STOP the core would let Claude through; the SKILL never-do line is the SOLE control on self-disposal | 2.2 / 2.3 / 2.4 | `not_automatable` (the gap is real and code-verified) + `soft_flag` (the SKILL *states* it is the sole control) | the SKILL stating it ≠ the agent obeying it — obedience is the unprovable residue R1 carried to runtime |

### 3.3 What the toy-game does NOT prove (charter clause 5 / R1)

This walkthrough **prepares** falsification evidence; it does not prove ergonomic gain. Every `human_study`
row above is the kind of claim only a real cold-start study could settle. The wins recorded in §1.10 are
**plausible and well-targeted**, not measured. The single thing the toy-game *does* establish with
confidence is **negative**: the saw-the-diff promise (F-COLD-7) is broken on the built path, and the
self-disposal guard (F-CRIT-1) is behavioral-only — both are code-grounded, not study-dependent.

### 3.4 R-S7-2 — the keyboard-annotation-over-iframe calibration (prioritized per s7)

s7 routed R-S7-2 to this stage: *prioritize calibrating keyboard-annotation-over-iframe AT-reachability —
the entire keyboard-native claim rests on it.* The toy-game's finding: **this walkthrough cannot calibrate
it** — it is a screen-reader-on-real-iframes test, not a narrative dual-walkthrough, and neither voice here
is an AT user. What the walkthrough CAN say is the **falsification setup**: a Playwright + AT harness must
verify that **Tab reaches an in-iframe annotatable element of the rendered onboarding card across the
sandboxed boundary, and Enter opens the comment form composing selector + elementLabel + odId-or-null
(DC-1)**. Until that harness passes:

- the keyboard annotation path stays **Tier-B / provisional** (s7 F1), and
- **`comment add` is the guaranteed L1 AT floor** (the B-salvage): an AT user prototyping the onboarding
  card who cannot reach the in-iframe button by keyboard must be able to run
  `studio comment add --selector ... --elementLabel ... --severity ... --intent ... --note ...` and get
  the identical CommentEvent. This is the explicit fallback the SKILL must teach. → **S-REP-6.**

ux-evidence: `hard_gate` (the harness pass/fail is deterministic, once built) — **currently UNBUILT, so
the claim is unproven**, exactly per F1/R2. proxy_limit: a harness pass proves *reachability*, not that an
AT user found annotating the card *easy*.

---

## 4. Required repairs (to the design + the SKILL)

### 4.1 Repairs to the DESIGN (interaction surface)

| ID | Repair | Closes | Severity |
|---|---|---|---|
| **D-REP-1** | Add an on-surface **agent-seam affordance**: the page must state *where* "ask Claude Code" happens (e.g. a persistent "Claude is driving this session in your chat/terminal" line, or an in-page prompt field if Step 1 is page-authored). Resolve whether Step 1's prompt is page-editable or pre-captured. | F-COLD-1 | High |
| **D-REP-2** | Specify the **generation progress + timeout/failure** state in §5 (M1): a visible "generating…" with a bounded "this is taking longer than expected / generation failed — ask Claude to retry" branch. | F-COLD-2 | High (re-forms #5) |
| **D-REP-3** | Make **step-4 reversibility visible**: after "Choose this one," show "you can switch options until you apply a change." | F-COLD-4 | Medium |
| **D-REP-4** | Add **plain-language helper text** to the comment form's `severity` and `intent` controls and **re-word the odId-null honesty marker** out of jargon ("this note is pinned to where you clicked; if the card is regenerated it may move"). Surface owns the labels (ODQ-5 surface half). | F-COLD-5 | High (#8/#3) |
| **D-REP-5** | Surface the **synthesize/draft step as a visible control** near the notes (or auto-run it on first note) so the human is never told to "approve a list" with no way to make one; ensure the single-primary `aria-current` next-step always maps to a runnable action. | F-COLD-6 | High |
| **D-REP-6** | **Do not label a control "Apply + see the diff" until N1 is built.** Until the two-gate saw-the-diff exists, the runnable single-gate must be labeled honestly ("Apply this change — it will be applied in one step") and the design's §3 step-9/10 cells must mirror §4.3's single-gate reality (s7 M2). | F-COLD-7 | **Blocking-for-honesty** (the label promises an unbuilt affordance) |
| **D-REP-7** | **Pin the handoff to a visible, openable deliverable** (a link that opens the rendered result), never a bare reference ID (root-cause #6). | F-COLD-8 | Medium |

### 4.2 Repairs to the SKILL

| ID | Repair | Closes | Severity |
|---|---|---|---|
| **S-REP-1** | Carry the **F-CRIT-1 corrected wording into the do/never-do narration**, not just the description: each STOP states "the system would NOT stop me — it cannot tell me from you — my discipline is the control." The never-do spine is the binding control, stated as such. | F-CRIT-1 (driving-side) | **Blocking** (already gated by s7) |
| **S-REP-2** | Add a **scripted refusal-with-recommendation** for the "you choose for me" ask at Step 4 (and the analogous "you approve/apply for me"): recommend + explain the boundary + return the click to the human (discharges §4.5 for the most likely ask). | A3 / F-COLD-6 | High |
| **S-REP-3** | Require Claude to **proactively offer to synthesize** once notes exist ("want me to turn your notes into a draft change list?"), so the human is never stranded between the agent arc and the approve gate. | A4 / F-COLD-6 | High |
| **S-REP-4** | Make the **apply-narration match the single-gate built reality**: state plainly that applying lands the change in one step today, and name the saw-the-diff two-gate accept as a **build-dependent (N1)** gap — never describe the unbuilt accept as current (two-layer scoping §5.4 applied to narration). | A5 / F-COLD-7 | **Blocking-for-honesty** |
| **S-REP-5** | **Resolve `handoff export` ownership** in the never-do spine: either add it as human-only, or sanction it as an agent-runnable convenience *after* the human's accept — and narrate accordingly. | A6 | Medium |
| **S-REP-6** | Teach **`comment add` as the explicit L1 AT fallback** for annotation (selector + elementLabel + odId-or-null per DC-1), and frame the in-page keyboard pick as Tier-B until the R-S7-2 harness passes. | R-S7-2 / F1 | High |
| **S-REP-7** | Specify the **author-to-disk + register seam (A1)** and the **agent→browser review-page handoff (A2)**: where Claude writes HTML before `variants register --from <dir>`, and the sanctioned "here is your review page" narration with the served URL (without standing up its own server). | A1 / A2 | High |
| **S-REP-8** | Carry **M4 as a SKILL-level rule**: never expose the review server beyond loopback — given F-CRIT-1, loopback-only is the de-facto network security boundary for the durable gates. | M4 / F-CRIT-1 | High |

### 4.3 Repairs already owned upstream (confirmed, not re-opened)

- **F2** (a11y hard_gate "pending calibration" qualifier) and **F3** (cold-start #1 identity-evidence
  explicit deferral) are s6/s7 author edits, not toy-game findings; the walkthrough **confirms** F3's
  deferral is defensible for this task (§1.10: the naive user never needed identity-evidence to build an
  onboarding card).
- **R-S7-1** (core human-vs-agent identity signal) is s9 core hardening; the toy-game **confirms its
  urgency from the driving side** (every STOP is SKILL-only).

---

## 5. Stop condition + handoff

- **Dual walkthrough on one sample session ("prototype an onboarding card")** — both voices, surface-only
  naive + SKILL-driven Claude Code (§1, §2). **Met.**
- **Naive user: where they get stuck / confused / what affordance is missing** — F-COLD-1…8 with the
  scorecard (§1). **Met.**
- **Claude Code: each command, each STOP-and-hand-to-human, each SKILL ambiguity** — the command+STOP
  trace (§2.6) + A1–A6 (§2). **Met.**
- **Friction interpreted; required repairs to design + SKILL named** — §3 (with ux-evidence classes +
  proxy_limit per finding) + §4 (D-REP-1…7, S-REP-1…8). **Met.**
- **Confirmed the naive user received no internal rationale** — §3.0, explicit. **Met.**
- **R-S7-2 keyboard-annotation-over-iframe prioritized** — §3.4: set up as the deterministic harness the
  whole keyboard-native claim depends on; `comment add` named as the L1 AT floor until it passes. **Met
  (setup, not calibrated — the harness is UNBUILT, per F1/R2).**
- **No ergonomic gain asserted** (charter clause 5 / R1) — §3.3. **Met.**

**Carried forward to s9 (plan).**

- **N1 (two-gate saw-the-diff apply)** is now confirmed from BOTH voices as the highest-impact build gap
  (F-COLD-7 / A5 / D-REP-6 / S-REP-4) — the surface label and the SKILL narration both currently promise
  an affordance the runnable single-gate `batch apply` does not deliver. **Honest interim:** label + narrate
  single-gate truthfully until N1 lands.
- **R-S7-1 (core identity signal)** urgency **confirmed from the driving side**: every one of Claude's four
  STOPs is held by SKILL discipline alone; the core would accept agent self-disposal at all of them.
- **DC-1** holds across all three capture paths exercised here (click, the keyboard Tier-B path, and the
  `comment add` AT floor) — each must emit selector + elementLabel + odId-or-null.
- **New surface repairs D-REP-1…7** and **SKILL repairs S-REP-1…8** routed to s9's non-executed build
  plan and the SKILL-author full draft.

**Emits:** `walkthrough.toy-game = dual walkthrough of "prototype an onboarding card" — cold-start naive
user (8 surface frictions F-COLD-1…8, 6 wins) + Claude-Code SKILL-driving trace (4 STOPs, 6 SKILL
ambiguities A1–A6, F-CRIT-1 confirmed from the driving side); every finding ux-evidence-classified with a
proxy_limit; 7 design repairs + 8 SKILL repairs named; naive user confirmed to have received no internal
rationale; no ergonomic gain asserted (R1).` Carried N1, R-S7-1, DC-1, D-REP-1…7, S-REP-1…8 to s9.
