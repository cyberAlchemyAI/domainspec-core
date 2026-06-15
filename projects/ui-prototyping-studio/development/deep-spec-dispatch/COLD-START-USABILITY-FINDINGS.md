# COLD-START-USABILITY-FINDINGS.md

> **Confirmation:** I received **no internal rationale, documentation, design decisions, or onboarding** for this tool. Everything below is my reaction as a first-time "naive user" who only sees the screen. I grounded my reactions in the actual on-screen labels and copy that a fresh user would literally read, but I was given zero explanation of *why* anything works the way it does. Where I say "what I imagine is there," that is a guess, not knowledge.

---

## Orientation (before I even start a task)

I land in **"UI Prototyping Studio"** and see seven labeled areas: Session Controls, Variant Canvas, Identity Evidence Panel, Annotation Panel, Mutation Approval Panel, Revision Timeline, Handoff Summary.

My honest first thought: *"This looks like a developer's internal tool, not a design tool."* I expected something like Figma or v0 ("type an idea, see pretty mockups"). Instead almost every panel shows machine-y status strings like `sessionId=pending`, `selectionGate=...`, `applyGate=pending`, `baseline=pending`, `revisionHead=pending`. I don't know what a "gate" is, what a "baseline" is, or what a "revision head" is. None of these words are defined anywhere I can see. There is no "Start here" / "Step 1" / wizard / tutorial. I have to *guess* the order of operations.

The biggest cold-start problem: **the workflow is a hidden linear pipeline, but the UI presents seven coequal panels with no numbering, no arrows, and no "do this next" cue.** I only discover the required order by clicking things and watching buttons stay greyed out.

---

## Task 1 — Generate some UI options for an idea I have

**What I did:** Went to **Session Controls**. Saw a "Prompt" textarea: *"Describe the UI concept to prototype."* Good — that matches my mental model. I typed my idea and looked for a big "Generate" button. I see two buttons: **Submit Prompt** and **Generate Variants**. Both are **greyed out**.

**Where I got stuck:** I couldn't generate anything. The buttons were disabled and the UI gave me no reason why. Eventually I noticed a separate **"Start Session"** button above and a tiny line reading `sessionId=pending`. I *guessed* I had to click "Start Session" first. After clicking it, "Submit Prompt" and "Generate Variants" lit up.

**Word/affordance that confused me:**
- **"Start Session"** — I don't know what a "session" is or why I need one before describing my idea. As a user I just want to type an idea and get options.
- **"Submit Prompt" vs "Generate Variants"** — *two* buttons. Do I click both? In what order? Does "Submit Prompt" already generate the options, or do I then *also* click "Generate Variants"? Nothing tells me. (I eventually assumed: Submit, then Generate.)
- **"Variant count: 1 / 2 / 3"** — the word "variant" instead of "option" or "design." I worked it out, but "options" is the word in my head.

**Expected vs. (imagined) reality:** I expected one obvious "Generate options" button that just works after I type. Reality: a 3-step hidden sequence (Start Session → Submit Prompt → Generate Variants) where the prerequisites are only signaled by buttons being disabled and a cryptic `sessionId=pending` string.

**Inferred MISSING affordance:** The disabled buttons need an inline reason ("Start a session first"), OR "Start Session" should happen automatically when I type my first prompt. The two-button submit/generate split needs to be either merged or visibly numbered (Step 1 / Step 2). A one-line "How this works" intro would erase most of this friction.

---

## Task 2 — Choose one option to move forward with

**What I did:** After variants appeared in **Variant Canvas**, each card showed "Variant A/B/C", a `status=...` line, some rationale/tradeoff/risk text, an `artifact=...` reference, and a `components=...` list. I looked for "Choose this one" / "Select" / a checkmark / clicking the card itself.

**Where I got stuck:** I tried **clicking the variant card** to select it — nothing happened. Then I found a button **"Select Baseline A"** (and B/C). I hesitated: I want to *pick an option*, but the button says *"Select Baseline."* I don't know if "baseline" means "the one I chose" or some technical reference snapshot. I clicked it on faith. Then I noticed `selectionGate=` changed — but I had to hunt for that confirmation; the card's own appearance barely changed (just an `is-baseline` style I might not even notice).

**Another trap:** If I'd only generated **1** variant, there is **no Select button at all** (it only renders when count > 1). A single-variant user would be completely stuck on "how do I choose this one," because the only confirmation is a buried note: `Single-variant branch committed baseline: ...`. I would never connect "I picked it" to that sentence.

**Word/affordance that confused me:**
- **"Baseline"** — to me this means "the original/control to compare against," which is almost the *opposite* of "the option I'm moving forward with." This is the single most misleading word in the whole tool.
- The card itself isn't clickable, which violates my instinct.

**Expected vs. (imagined) reality:** I expected to click the card or a clear "Choose this option" button and get an obvious "Selected ✓" state on the card. Reality: a "Select Baseline X" button, confirmation hidden in a `selectionGate=` status string, and no select control at all for single-variant runs.

**Inferred MISSING affordance:** Make the whole card selectable; rename "Select Baseline" to "Choose this option" (or at least "Use this design"); show an unmistakable "Selected" badge **on the card**; and always provide a select/confirm control even when there's only one variant.

---

## Task 3 — Confirm the "identity / visual evidence" the tool asks about

**What I did:** This is the task I was *most* lost on. The orientation listed an **"Identity Evidence Panel."** I went looking for it. **I could not find a panel by that name with any actual content.** What I *can* find scattered around are: `baseline=...` badges, an `artifact=...` reference on each variant card, and a `components=...` line. Nothing on screen ever literally says "Identity Evidence" or "confirm the visual evidence," and nothing ever *asks* me to confirm anything.

**Where I got stuck:** Completely. There is no visible prompt like *"Is this the right look? Confirm."* No image/preview I can eyeball. No "Confirm" button tied to anything called identity or evidence. I'm left guessing that maybe selecting the baseline in Task 2 *was* the "confirmation," or that the `artifact=...` string is the "visual evidence" I'm supposed to verify — but I can't open or view that artifact, so I can't actually confirm it.

**Word/affordance that confused me:**
- **"Identity Evidence"** — I have no idea what this means in a UI tool. Brand identity? My login identity? Visual fingerprint? The phrase reads like internal jargon.
- **"artifact="** followed by a reference string — I assume this is the actual generated UI, but it's shown as text I can't preview, so it's evidence I can't inspect.

**Expected vs. (imagined) reality:** I expected a panel that shows me the actual rendered look (a thumbnail/preview) and a plain "Yes, this is what I meant — Confirm" button. Reality: there's a named area in the orientation that doesn't correspond to any labeled, content-bearing, confirmable panel I can locate; the closest things are unclickable text references.

**Inferred MISSING affordance:** A real, clearly-titled panel that (a) **renders a preview** of the chosen variant's artifact, (b) explains in plain words what "identity/visual evidence" means, and (c) has an explicit **"Confirm"** action with a confirmed-state indicator. Right now the task is essentially impossible to complete with confidence.

---

## Task 4 — Leave a note on one specific button I want changed

**What I did:** Found the **Annotation Panel** (good — "annotation" roughly = "note"). But the whole panel was **greyed out / disabled**, with the message: *"Annotation gate locked: select baseline first."*

**Where I got stuck (twice):**
1. First, the gate-locked state. At least this one *tells* me what to do ("select baseline first") — the only good prerequisite message in the app. But it uses "baseline" again (see Task 2 confusion), so I had to recall that "select baseline" = "choose my option."
2. Once unlocked, I wanted to leave a note on *one specific button*. The form asks for: **Target selector**, **Element label**, **OD ID (optional)**, **Severity**, **Intent**, **Note**. As a naive user I expected to *click the button in the preview and type a comment.* Instead I'm asked to fill in a **"Target selector"** — I don't know what a CSS selector is, and I have no preview to click anyway. "Element label" I can fuzzily guess ("the Save button"). **"Intent"** vs **"Note"** — what's the difference? Both feel like "what I want." **"Severity: blocker/high/medium/low"** feels like a bug tracker, not "I'd like this button to be blue."

**Word/affordance that confused me:**
- **"Target selector"** — pure developer jargon; a non-technical user cannot fill this in.
- **"OD ID"** — completely opaque. No expansion, no tooltip. I have no idea what OD means.
- **"Intent" vs "Note"** — redundant-seeming; unclear which holds my actual request.
- **"Severity"** — makes my cosmetic note feel like filing a defect.

**Expected vs. (imagined) reality:** I expected: hover/click the actual button in a live preview → a comment bubble → type "make this blue" → done. Reality: a manual form requiring a selector string and several jargon fields, with no on-canvas pointing at the element.

**Inferred MISSING affordance:** **Click-to-annotate directly on the preview** (which auto-fills target/selector). Plain-language fields ("Which element?", "What should change?"), tooltips for "Intent" and "OD ID," and making developer-only fields optional/auto-derived. Severity should be optional or hidden behind "advanced."

---

## Task 5 — Get that change actually applied

**What I did:** Left my note, then expected the change to just... happen, or a "Apply my note" button near the note. Instead applying lives in a *separate* **Mutation Approval Panel** with three buttons: **Synthesize Draft**, **Approve Draft**, **Apply Approved Batch**, plus `draftStatus=none` and `applyGate=pending`.

**Where I got stuck:** This is a **three-step ritual across a different panel** with no connection drawn back to my note. "Approve Draft" and "Apply Approved Batch" start disabled. I had to guess the order: Synthesize → Approve → Apply. Even the panel's own subtitle ("Synthesize deterministic draft tasks, approve manually, then apply") is the only hint, and it's full of jargon.

**Word/affordance that confused me:**
- **"Mutation"** — alarming word; sounds like genetics or something destructive, not "apply my edit."
- **"Synthesize Draft"** — I don't know what gets synthesized or why I, the user, must trigger it. I expected the tool to just turn my note into a change.
- **"Batch" / "Approved Batch"** — I left *one* note about *one* button; "batch" makes me think I'm missing a bigger queue.
- **"applyGate=pending / satisfied"** — I have no idea what makes the gate "satisfied," so I'm clicking buttons hoping to flip it.

**Expected vs. (imagined) reality:** I expected an "Apply this change" button right where I left the note, and to see the button visibly change in a preview afterward. Reality: a separate 3-stage Synthesize→Approve→Apply pipeline with gate strings, and (because there's no preview) **no visual confirmation that my button actually changed** — only a `draftStatus`/`applyGate` text flip.

**Inferred MISSING affordance:** Either auto-link my note to a one-click "Apply" flow, or strongly label the 3 steps as a numbered sequence with explanations. Critically: **show me the before/after of the actual button** so I can confirm the change landed. Replace "Mutation" with "Change" and "Synthesize Draft" with "Prepare change."

---

## Task 6 — Find the history of what changed

**What I did:** Went to **Revision Timeline** ("Append-only revision evidence for each successful apply"). This was relatively findable — "timeline" + "history" align.

**Where I got stuck:** The entries are unreadable to me. Each row shows: `revision=... parent=...`, `batch=... tasks=N`, and `diff=2/1/0`. I wanted plain history: *"Changed the Save button color — 2 min ago."* Instead I get IDs and a `diff=added/changed/removed` triple I have to *decode* (I'm guessing 2 added / 1 changed / 0 removed, but the labels aren't shown). There's no human-readable description of *what* changed, *when* (no timestamp), or *who*. I also can't tell which row corresponds to *my* note from Task 4.

**Word/affordance that confused me:**
- **"Revision" / "revision head" / "parent revision"** — version-control vocabulary I don't carry as a casual user.
- **`diff=2/1/0`** — unlabeled numbers; I can only guess their meaning.
- No timestamps, no plain-English summary, no link back to the originating note.

**Expected vs. (imagined) reality:** I expected a readable changelog ("You changed X at 3:42 PM"). Reality: an append-only list of revision IDs, parent IDs, batch IDs, and a cryptic diff ratio.

**Inferred MISSING affordance:** Human-readable history rows with **timestamps**, a **plain summary of each change**, labeled diff counts ("2 added, 1 changed, 0 removed"), and a link from each revision back to the note/comment that caused it.

---

## Task 7 — Hand the result off to my dev team

**What I did:** Found **Handoff Summary Panel** ("Export and inspect handoff references for downstream UI/test implementation"). Two buttons: **Export Handoff** and **Refresh Bundle**. Status reads `handoff=pending`.

**Where I got stuck:** I clicked **Export Handoff** and... I don't know what happened. There's no "Downloaded to..." message, no link, no file, no "copy to clipboard," no "share with team." Afterward I see a list of reference strings: `stories=...`, `requirements=...`, `acceptance=...`, `uiSpec=...`, `testSpec=...`. These look like internal IDs, not something I can actually *hand* to a person. And **what is "Refresh Bundle"?** When do I need it vs. Export? The status `handoff=refresh-required` hints they interact, but I don't understand the dependency.

**Word/affordance that confused me:**
- **"Handoff bundle" / "Export Handoff"** — "export" implies a file or link, but I get on-screen reference strings instead.
- **"Refresh Bundle" vs "Export Handoff"** — two buttons, unclear which to press, and `handoff=refresh-required` makes me feel I did it wrong.
- **`uiSpec=`, `testSpec=`, `stories=`, `acceptance=`** — reference IDs with no obvious way to actually send/share them.

**Expected vs. (imagined) reality:** I expected a "Share / Export" that produces a real link, file, or "copied to clipboard" I can paste to my dev team. Reality: button clicks with no visible output channel, and a list of opaque reference strings.

**Inferred MISSING affordance:** A concrete, visible delivery: a download, a shareable link, or a "Copy handoff link" with a success toast. Clarify Export vs. Refresh (or merge them), and label what "refresh-required" means and how to satisfy it.

---

## Friction ranked by severity

| Rank | Task | Friction | Severity | Why this severity |
|---|---|---|---|---|
| 1 | 3 | **"Identity Evidence Panel" has no findable, confirmable content; no preview to inspect.** Task is effectively impossible to complete with confidence. | **Critical** | A named, required step the user literally cannot perform. |
| 2 | 2 | **"Baseline" is misleading** (reads as "control/original," means "the option I chose"); card not clickable; no select control at all for single-variant. | **Critical** | Core "choose an option" action is mislabeled and partly absent. |
| 3 | 5 | **Applying a change is a hidden 3-step "Synthesize→Approve→Apply" ritual** in a separate "Mutation" panel, disconnected from the note, with no visual proof the change landed. | **High** | Main "make my edit happen" goal; alarming jargon + no confirmation. |
| 4 | 4 | **Annotation form demands "Target selector" / "OD ID"** (dev jargon) with no click-to-annotate on a preview; "Intent" vs "Note" ambiguous. | **High** | Blocks non-technical users from leaving a basic note. |
| 5 | 1 | **Hidden prerequisite chain** (Start Session → Submit Prompt → Generate Variants) signaled only by disabled buttons + `sessionId=pending`. | **High** | First action; disabled buttons give no reason, so users stall immediately. |
| 6 | 7 | **"Export Handoff" produces no visible deliverable**; Export vs. Refresh unclear; output is opaque reference IDs. | **Medium** | Last step; user can't tell if/what they shared. |
| 7 | 6 | **Revision history is IDs + unlabeled `diff=2/1/0`**, no timestamps, no plain summary, no link to originating note. | **Medium** | Findable but unreadable; informational rather than blocking. |
| 8 | All | **Pervasive machine-status strings** (`gate=pending`, `=committed`, `revisionHead=pending`) used as primary UI signals; no glossary, no onboarding, no step numbering. | **High (cross-cutting)** | Underlies most of the above; the whole flow reads as an internal tool. |

---

## Cross-cutting cold-start gaps (the root causes)

1. **No onboarding / no step ordering.** Seven coequal panels, but the real workflow is a strict pipeline (Session → Variants → Choose → Annotate → Apply → History → Handoff). Numbering, arrows, or a "Next step" highlight would fix most stalls.
2. **Disabled state without reason.** Most blocking buttons just grey out. Only the Annotation panel says *why* ("select baseline first"). Every disabled control needs that one-line reason.
3. **Internal jargon as user-facing labels.** "Baseline," "Mutation," "Synthesize," "Gate," "Revision head," "OD ID," "Target selector," "Identity Evidence," "Handoff bundle." None are explained on screen.
4. **No live preview anywhere.** Variants, the selected design, the annotated button, the applied change, the handoff output — all are represented as *text references*, never something the user can *see*. This single missing affordance (a rendered preview/canvas) is what makes Tasks 2–7 feel hollow.
5. **Status shown as raw key=value strings** instead of human sentences/badges, so confirmations are easy to miss (e.g., selection success is buried in `selectionGate=`).
