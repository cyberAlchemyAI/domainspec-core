---
id: interaction-design-ui-ux-interaction-skill
project: ui-prototyping-studio
title: "Interaction Design (s6) — AGENT-AUTONOMY vs HUMAN-CONTROL resolved into the C surface"
status: design
node_type: design-artifact
run_id: 20260616-ui-ux-interaction-skill
dispatch_id: refine-ups-ui-ux-skill-20260616
step_id: s6-interaction-design
capability_ref: invoke
mode: design
pattern: dialectic
consumes_decision: decision.surface
consumes_handle: handle.define
emits_design: design.interaction
updatedAt: 2026-06-16
---

# Interaction Design (s6)

> **What this stage does.** It takes the s5 tournament winner — **C (minimal local web review page)
> as the build-now spine + a named deferred A-upgrade** — and resolves the **AGENT-AUTONOMY vs
> HUMAN-CONTROL** dialectic into a concrete interaction design: the surface, the overlay mechanics,
> the step-by-step human-agent loop with an ergonomics rationale per step, the accept-diff gate UX,
> the error/empty/decision-paralysis states, and the accessibility floor. It is the co-owner (with the
> skill-author) of the s6 dialectic; this artifact is the **interaction-designer** half. It does NOT
> re-run the tournament (s5 owns ODQ-1), does NOT author the SKILL.md (skill-author half, draft carried
> in the dispatch), and does NOT prove ergonomics (s8 toy-game owns ODQ-7).
>
> **Frame receipt.** Consumed `decision.surface` (s5: C-spine + deferred A) and `handle.define`
> (D1–D5: the two problems, the 12-step who-leads-when map §3.2, the SKILL required-contents §4, the
> surface rubric + fixed obligations §5.3, the two-layer scoping rule §5.4). Every code claim below was
> re-verified in this checkout against `backend/src/modules/ui-prototyping-studio/`, not taken from the
> briefs (verification ledger §0.1).

---

## 0. The dialectic, stated and resolved

**Thesis — AGENT-AUTONOMY.** Let Claude Code do the reversible, generative work fluidly: invent
variants, stamp ids, register, synthesize, propose the candidate mutation. Friction on these steps is
pure cost — they are undoable by simply not carrying them forward, so a gate there is friction, not
governance (charter clause 4).

**Antithesis — HUMAN-CONTROL.** The human disposes every **durable** change and **sees the diff**
before anything advances head. A change the human did not knowingly authorize is a governance failure
even if the agent was "right." The human's accountability is the product, not an obstacle to it.

**Synthesis (the resolution this whole design enacts).** *Autonomy is the default on the reversible
arc; control is absolute at the durable boundary; and the surface's entire job is to make the handoff
between the two legible at a glance.* The poles do not compete for the same step — the 12-step map
(D2 §3.2) already partitioned them: **6 reversible steps the agent may drive (1,2,3-render,5-capture,
6,8), 5 durable/irreversible gates the human alone disposes (4,7,9,10,12).** The design's load-bearing
move is not *choosing* a pole but *rendering the boundary*: at every moment the surface shows who leads
now, why the next gate is locked or open, and — at the one irreversible step — what exactly will change.
This is why C wins the dialectic and A does not: C keeps note + render + disposition **co-located in one
served page**, so the autonomy→control handoff never crosses a surface boundary (A risked splitting it
across browser + terminal, re-opening root-cause #3, s5 §3 tie-break reason 3).

### 0.1 Code re-verification ledger (this checkout)

| Claim the design rests on | Verified at | Result |
|---|---|---|
| `readHtml(ref)` exists; serves staged/committed HTML by content-addressed ref | `infrastructure/file-artifact-content-store.ts:50` | **TRUE** — only the route + page are new work. |
| No `text/html` route anywhere | `interface/http-routes.ts` (whole file: 14 JSON routes, no `reply.type("text/html")`/`sendFile`) | **TRUE** — C's only new server work is one GET. |
| Comment capture POST exists | `http-routes.ts:229` `POST …/sessions/:sessionId/comments` → `orchestration.captureCommentEvent` | **TRUE.** |
| INV-2 enforced server-side (annotation gated on baseline) | `application/capture-comment-event.ts:45` throws `BASELINE_GATE_UNSATISFIED` when `selectionGate !== "satisfied"` | **TRUE** — INV-2 is in the core, not the surface. |
| INV-3 auto-apply refusal is server-side | `application/apply-approved-batch.ts:33` throws `AUTO_APPLY_FORBIDDEN` when actor lowercases to `system:auto` | **TRUE but narrow** — keyed on a literal actor string (residue R3). |
| `odId` optional; `selector`+`elementLabel` REQUIRED | `http-routes.ts:680-695` `parseAnnotationTarget`: selector + elementLabel via `parseRequiredString`, odId nullable | **TRUE — and stricter than s5's phrasing.** The page MUST always emit selector + elementLabel even when odId is null (design constraint DC-1 below). |
| Two-gate apply unbuilt in routes/CLI | `apply-approved-batch.ts` is single-gate (stages + advances head in one call); `two-gate-apply.test.ts` is the only referencer of the two-gate module | **TRUE** — accept-diff (step 10) is a build dependency (N1 → s9). |

> **Correction folded forward to s9.** The s5 verdict said `CaptureCommentBody.target` is
> "optional/unknown-validated." The *body field* is typed `unknown`, but `parseAnnotationTarget`
> **hard-requires** a non-empty `selector` and `elementLabel`. The design is still contract-valid (it
> always synthesizes both), but the SKILL.md must not imply odId-only annotation works — see DC-1.

---

## 1. The chosen surface

**A minimal local web review page**, served by the existing Fastify app, opened by the human in a
browser tab. One page, one session, three regions, no SPA and no build step (vanilla HTML + a single
small inline script). It is *ephemeral and local-only*: bound to `127.0.0.1`, lifetime = the review
session, no remote exposure.

```
┌──────────────────────────────────────────────────────────────────────┐
│  UI Prototyping Studio · session <id> · prompt: "<the human's words>"  │  header: plain-language state
├───────────────────────────────┬──────────────────────────────────────┤
│  REGION 1 — Variants (≤3)      │  REGION 3 — Gate panel                │
│  ┌─────────┐ ┌─────────┐       │  Step 4  Choose the option to build → │  one disposal per durable
│  │ iframe  │ │ iframe  │  ...  │     on   [ Choose this one ]          │  gate, each with its
│  │ sandbox │ │ sandbox │       │  Step 7  Approve the change list      │  enabled/disabled REASON
│  └─────────┘ └─────────┘       │     locked — "choose an option first" │  rendered in words
│  click an element to comment   │  Step 9-10 Apply + see the diff       │  (a11y.5)
├───────────────────────────────┤     locked — "approve the list first" │
│  REGION 2 — Notes on this      │  Step 12 Export the handoff           │
│  option (this session's        │     locked — "land a change first"    │
│  comments, newest first)       │                                       │
└───────────────────────────────┴──────────────────────────────────────┘
```

- **Region 1 — variant renders.** Up to 3 variants, each in a `sandbox`ed `<iframe>` whose `src` is the
  new `GET …/render` route (§2). Side-by-side satisfies "see the thing" (root-cause #4) and bounds
  comparison breadth to ≤3 (charter clause 2).
- **Region 2 — notes on this option.** The session's captured comments, newest first, each as a plain
  sentence ("`<severity>`: `<note>` — on `<elementLabel>`"), linked back to the element. Co-locating
  the note with the render is the structural answer to root-cause #3 ("disconnected from the note").
- **Region 3 — gate panel.** The five durable/terminal gates (steps 4, 7, 9–10, 12) as native
  `<button>` controls, each rendered with **its enabled/disabled state AND the one-line reason** in
  words (a11y.5). This is where HUMAN-CONTROL lives, in the same page as the render — the dialectic
  resolution made visible.

**ux-evidence per surface claim.**

| Surface claim | Class | proxy_limit |
|---|---|---|
| Side-by-side ≤3 renders reduce the "can't see it" stall | `screenshot_review` (salience) + `human_study` (comprehension) | a screenshot shows the renders exist; it cannot show the human *understood the options* |
| Gate panel reasons reduce the "disabled without reason" stall | `soft_flag` (a11y.5: reason text present + `aria-describedby`-associated) | DOM presence ≠ the human read or believed the reason |
| Co-locating note + render reduces root-cause #3 | `human_study` | layout adjacency is checkable; "felt connected" is not |
| One page lowers who-leads-when ambiguity vs A's two channels | `not_automatable` (a design-shape claim) + `human_study` | we can verify one origin; we cannot verify the human inferred the boundary (Q0) |

---

## 2. Overlay mechanics (the build-now C path)

The "overlay" in C is **in-page, same-origin, on the served review page** — not injected into a foreign
browser (that is the deferred A-upgrade, §2.4). Mechanics, in build order:

### 2.1 Render HTML — the one new GET

Add a single read-only route to `http-routes.ts`:

```
GET /api/ui-prototyping-studio/sessions/:sessionId/variants/:label/render
  → orchestration reads the variant's htmlArtifactRef
  → contentStore.readHtml(ref)              // EXISTS, content-store.ts:50
  → reply.type("text/html").send(html)      // the ONLY new server behavior
```

- **Read scope only** (`assertReadScope`, mirroring the existing GET routes) — rendering is reversible,
  so it carries the read scope, never the write scope. AGENT-AUTONOMY: Claude Code may request renders
  freely; nothing durable happens.
- **`readHtml` returns `null`** for an unknown/missing ref → the route returns a small, honest
  placeholder document ("This variant has no rendered HTML yet"), never a 500 and never a blank iframe
  (empty-state E-EMPTY-2, §5).
- A second `GET …/render` variant serves the **served review page itself** (the static HTML + inline
  script). This is the page humans open. It needs no build step.

### 2.2 Click-to-annotate, capture the target

The served page's inline script attaches one delegated click handler inside each iframe-rendered
document (same-origin, so the parent page can reach into the iframe DOM — this is exactly why C is
same-origin and A is not):

1. On click of a rendered element, walk up to the nearest element carrying `data-od-id` (if any).
2. **Compose the `AnnotationTarget` the core REQUIRES** (DC-1, from `parseAnnotationTarget`):
   - `selector` — a stable CSS selector for the clicked element (REQUIRED, non-empty).
   - `elementLabel` — a human-readable label (REQUIRED, non-empty): the element's visible text
     trimmed, or its tag + role.
   - `odId` — the captured `data-od-id` **if present, else `null`** (the contract allows null).
3. Open the comment form: `{severity, intent, note}` as three plain controls, pre-anchored to the
   chosen element (highlight it so the human sees what they pointed at — recognition over recall).
4. **Honesty marker.** When `odId` is null, the form shows a quiet "this target may not survive a
   regenerate" note (the content-pack non-durable-fallback rule). The SKILL.md narration must not claim
   pixel/id fidelity the capture lacks (s5 constraint 4).

> **DC-1 (design constraint, load-bearing).** Because `selector` and `elementLabel` are
> server-REQUIRED, the page can NEVER POST an odId-only comment. Every capture path — mouse click,
> keyboard tab-to-element (§6), or the manual fallback — must yield both. This is stricter than the s5
> summary and is the single most important correctness fact handed to s9.

### 2.3 Ephemeral local server → POST → CaptureCommentEvent, gated by INV-2

- The page POSTs to the **existing** `POST …/sessions/:sessionId/comments` (http-routes.ts:229) with
  `x-scopes: domainspec.ui-prototyping.write` and the body `{revisionId, target, severity, intent,
  note, createdBy}`.
- **INV-2 is enforced in the core, not the page** (`capture-comment-event.ts:45`): if no baseline is
  selected, the POST is refused with `BASELINE_GATE_UNSATISFIED`. The page therefore renders the
  annotate affordance as **disabled-with-reason until step 4 fires** ("Pick an option to build before
  you can comment on it") — a client mirror of the server gate, never a client *replacement* for it.
  The server remains the authority; the disabled state is an ergonomic courtesy that avoids a failed
  round-trip (root-cause #2).
- The server is **ephemeral + local**: bound to loopback, no auth beyond the scope header, lifetime =
  the session. It is the same runnable Fastify bootstrap (`index.ts`), not a new process per s5.

**ux-evidence.**

| Overlay claim | Class | proxy_limit |
|---|---|---|
| Capturing on the rendered element removes typed-selector jargon (root-cause #4) | `human_study` | we can verify a target was captured; not that the human found it easier than typing |
| Client mirror of INV-2 (disabled-with-reason) avoids a failed POST | `soft_flag` (a11y.5 reason present) | the soft mirror can drift from the server gate — only the server gate is authoritative |
| The captured `CommentEvent` is contract-identical to `comment add` | `hard_gate` (shape: body validates against `parseAnnotationTarget`) | shape-only; says nothing about annotation *quality* |

### 2.4 The deferred A-upgrade hook (named, not built)

If `data-od-id` capture is later ruled mandatory (not preferred), swap the same-origin in-iframe pick
for an A-style `postMessage` element-pick into a fully isolated (cross-origin) iframe to restore A's
in-DOM fidelity. **This is the trigger that fires G-A11Y** (s5 §6): at that point the click-to-annotate
keyboard/AT pattern pass becomes a live, bounded dependency. Until then, C is keyboard-native (§6) and
G-A11Y stays unfired. Recorded so the trigger is not lost.

---

## 3. The full human-agent loop, step-by-step, with ergonomics rationale

The 12-step map (D2 §3.2) rendered into surface behavior. **[YOU]** = Claude Code (autonomy arc),
**[HUMAN GATE]** = human disposes (control boundary), **[CORE]** = deterministic core. Each step states
**who-leads-when / cognitive-load / friction** (g4) and carries a ux-evidence class.

| # | Step (surface behavior) | Lead | who-leads-when · cognitive load · friction | ux-evidence |
|---|---|---|---|---|
| 1 | **Prompt.** Human types the UI intent in plain words in the header. | HUMAN | Human leads (only from-scratch authoring step); load = expression not selection; friction = the Figma-like entry the cold-start user expects | `human_study` (intent capture) |
| 2 | **Generate + register.** Claude Code produces 1–3 variants, stamps `data-od-id`, calls `variants register`. The page shows a live "generating…" state then the renders appear. | YOU (reversible) | Agent leads — the agentic action; zero human load; friction = removes the hidden Start→Submit→Generate chain (root-cause #5) **only if the page shows progress** | `soft_flag` (variant count + id-stamp shape) |
| 3 | **Review.** Human sees the ≤3 renders side by side (Region 1). | HUMAN (reversible) | Human leads; load = recognition + bounded comparison (≤3); friction = closes "no live preview" (root-cause #4) — *expected* to be the largest cold-start win, pending the cold-start study (clause 5; F7) | `screenshot_review` + `human_study` |
| 4 | **Choose the option to build.** Human clicks "Choose this one" on a variant. → `baseline`. | **HUMAN GATE** (durable, INV-2) | Human disposes — first control boundary; load = one decision; friction = "Baseline" relabeled **"the option you chose"** (root-cause #3, the #2 Critical jargon trap) | `hard_gate` (keyboard-operable, a11y.3) |
| 5 | **Comment on a component.** Human clicks a rendered element; captures `{target, severity, intent, note}`; appears in Region 2. | HUMAN (reversible append) | Human authors — agent NEVER annotates; load = recognition (point) not recall (selector); friction = removes typed-selector jargon; **unlocked only post-baseline** (INV-2 mirror) | `hard_gate` for capture shape + `human_study` for the comprehension gain |
| 6 | **Synthesize.** Comments → a draft batch. Either actor may trigger; **core computes.** Page shows the draft batch as a plain change list. | YOU or HUMAN trigger; **CORE computes** (reversible) | Either may trigger but core leads the compute so the agent can never reinterpret intent; zero net new load; friction = removes the disconnected "Mutation panel" ritual **if surfaced near the notes** | `not_automatable` (deterministic; shape-checkable) |
| 7 | **Approve the change list.** Human approves the synthesized batch. | **HUMAN GATE** (durable, INV-3) | Human disposes; **scope is enforced server-side but identity is NOT — `approve` has zero actor-class check (`approve-mutation-batch.ts`), so the SKILL never-do spine is the SOLE control on agent self-disposal** (real identity gate routed to core, R-S7-1 / F1); load = one decision over a recognizable list; friction = justified only because it gates a durable action | `flow.2` `hard_gate` |
| 8 | **Propose candidate.** Within apply, Claude Code produces the candidate mutation (value-in/value-out). | YOU (reversible, staged) | Agent proposes; **forbidden the store/clock/append path** (engine purity); zero human load; friction = removes manual edit authoring | `not_automatable` (engine-purity shape) |
| 9 | **Apply (runnable: single-gate `batch apply` — stages AND advances head in one call).** Human triggers apply. *Target (unbuilt, N1):* core stages the candidate and renders the honest diff before head advances. | **HUMAN GATE** (durable) | Human triggers; **runnable today = single-gate (no saw-the-diff pause)**; load = one decision; *target* two-gate stage+diff is a build dependency (`two-gate-apply.ts` exists, not wired — F6) | `cog.5` `screenshot_review` (diff salience, target) |
| 10 | **Accept the diff (saw-the-diff) — TARGET gate, unbuilt.** Human accepts in a focus-trapped `<dialog>` after seeing the rendered diff; head advances by one revision. | **HUMAN GATE** (IRREVERSIBLE, target second gate) | Human disposes; *intended* as the saw-the-diff control (registered-not-rubber-stamped is a `human.2` hypothesis, **not asserted** — F7); load = one consequential decision; **needs `<dialog>` (a11y.4) + the two-gate build (F6)** | `a11y.4` `hard_gate` (BLOCKED on impl) + `human.2` `human_study` |
| 11 | **Record.** Core appends exactly one revision; the page's history shows timestamp + plain summary + link to the originating note. | CORE (irreversible record) | Core leads (deterministic bookkeeping); zero human load; friction = history shows sentences + timestamps + note link, not raw `diff=2/1/0` (root-cause #7) | `soft_flag` (one-revision shape) |
| 12 | **Export the handoff.** Human exports; the page shows a **visible, openable** deliverable, not opaque IDs. | **HUMAN GATE** (terminal) | Human disposes (leaves the system); load = one action; friction = a *visible* deliverable, not reference IDs (root-cause #6) | `human_study` (findable/usable?) |

**What the loop proves about the dialectic.** The autonomy arc (2, 5-capture, 6-trigger, 8) and the
control boundary (4, 7, 9, 10, 12) never share a step, and every control step sits in Region 3 of the
same page that hosts the render and the note. The handoff is always one page-glance, never a
channel-switch. That is the synthesis, operationalized.

---

## 4. How the human sees + accepts the diff (the accept-diff gate UX)

This is the irreversible boundary (step 10) — the place HUMAN-CONTROL is most absolute and the one gate
that **leans on an unbuilt dependency** (two-gate apply, N1).

### 4.1 The two-gate sequence on the page

1. **Apply (step 9, gate 1 of 2).** Human clicks "Apply" on the approved batch. The core stages the
   candidate (does NOT advance head) and returns the honest diff. The page renders the diff inline:
   the staged change list + (when available) a before/after render of the affected region.
2. **The accept `<dialog>` (step 10, gate 2 of 2).** The human clicks "Review and accept." A
   **focus-trapped `<dialog>`** opens (a11y.4) showing:
   - the honest diff (what exactly changes, in plain language: "2 changes will be applied: …");
   - two controls — **"Accept — apply this change for good"** and **"Cancel — keep editing"**;
   - the irreversibility stated in words ("This advances the design by one revision and cannot be
     undone except by a new change").
3. On **Accept**, the page POSTs the accept; the core advances head by exactly one revision (step 11);
   the dialog closes; the history region updates with a plain summary + note link.

### 4.2 Why a focus-trapped dialog (the a11y.4 + saw-the-diff rationale)

- **Saw-the-diff, not rubber-stamped.** The dialog forces the diff into the foreground before the only
  irreversible control is reachable — the human cannot accept *past* the diff. This is the `human.2`
  "registered, not rubber-stamped" ergonomic, made structural rather than asserted.
- **Focus trap = the keyboard floor for the highest-stakes gate.** Tab cycles within the dialog;
  `Esc` cancels; focus returns to the trigger on close (a11y.4). A non-modal accept would let a
  keyboard user advance head while focus is elsewhere — exactly the failure a11y.4 names.
- **One decision, maximum salience.** Modal salience is justified here and *only* here (cog.5): it is
  the one irreversible step. Putting every gate in a dialog would be friction; putting this one in a
  dialog is governance-as-a-feature (clause 4).

### 4.3 Build honesty (carried to s9)

The two-gate apply is **unbuilt** (`apply-approved-batch.ts` is single-gate; `two-gate-apply.ts` is
referenced only by its own test). So **steps 9–10 as designed are a build dependency (N1), not a
current capability.** The SKILL.md must reference the accept gate as a *target gate gated on the
two-gate build* (D3 §5.4), and the page ships the `<dialog>` shell against the target contract. Until
N1 lands, the runnable path is single-gate `batch apply` (which stages + advances in one call, with no
saw-the-diff pause) — the design names this gap rather than hiding it.

**ux-evidence.**

| Accept-gate claim | Class | proxy_limit |
|---|---|---|
| `<dialog>` is focus-trapped, Esc-cancellable, focus-restoring | `hard_gate` (a11y.4, WAI-ARIA APG dialog pattern) — promotable only after fixture calibration | passes the pattern; cannot prove the human *comprehended* the diff |
| The diff is foregrounded before the accept control is reachable | `hard_gate` (DOM order / focus order check) | order ≠ attention; "saw" in the WCAG sense, not the cognitive sense |
| Accept is "registered, not rubber-stamped" | `human_study` (`human.2`) | unprovable in this run — toy-game prepares timing/trace evidence only |
| Apply gate has higher salience than decorative regions | `cog.5` `screenshot_review` | salience ≠ noticed |

---

## 5. Error / empty / decision-paralysis states

Each state names the trigger (a real error code where the core enforces it), the surface behavior, and
the ergonomics rationale. Codes verified in §0.1.

### 5.1 Error states (server-authoritative; the page narrates, never overrides)

| State | Trigger (verified code) | Surface behavior | Rationale |
|---|---|---|---|
| **Annotate before baseline** | `BASELINE_GATE_UNSATISFIED` (`capture-comment-event.ts:45`) | Annotate affordance disabled-with-reason ("Pick an option to build first"); if the POST still races, show the same sentence, not the code | INV-2 mirror; turns a raw refusal into a plain next-step (root-cause #2) |
| **Agent tries to apply/accept** | `AUTO_APPLY_FORBIDDEN` (`apply-approved-batch.ts:33`) — fires **only** for the literal actor `system:auto` | Not a UI path — the gate buttons are human-only. **Caveat (F1): the core refuses ONLY the literal `system:auto` actor; Claude Code's actor (`STUDIO_ACTOR`) is NOT refused server-side. The SKILL never-do spine is the actual control** (real identity gate routed to core, R-S7-1). | INV-3 spine narrow-but-real; the refusal is honest about its narrowness, not overclaimed |
| **Apply before approve / stale approval** | `BATCH_APPROVAL_REQUIRED` / `APPROVAL_STALE` (errors.ts) | Apply button disabled-with-reason ("Approve the change list first" / "The list changed — re-approve") | gate-ordering legibility (root-cause #1) |
| **Variant has no HTML to render** | `readHtml` returns `null` (content-store.ts:51) | iframe shows an honest placeholder doc, never blank, never 500 | a blank iframe reads as "broken app"; the placeholder reads as "not generated yet" |
| **Auth/scope missing** | `UPS_AUTH_REQUIRED` / `UPS_AUTH_FORBIDDEN` (http-routes.ts:570-607) | Page-level banner: "This page needs read/write access to the studio session." | the scope header is plumbing; the human should see a sentence, not a 401 |
| **Session not found / expired** | `SESSION_NOT_FOUND` (404) | Full-page empty state: "This review session has ended. Ask Claude Code to start a new one." | the ephemeral server outlives nothing; the dead-tab case must be graceful |

### 5.2 Empty states

| Empty state | Surface behavior | Rationale |
|---|---|---|
| **E-EMPTY-1: no variants yet** | Region 1 shows a single calm line: "Ask Claude Code for a UI to get started" + echoes the prompt if one exists | the cold-start user lands here first; it must read as "ready," not "broken" (counters root-cause #5) |
| **E-EMPTY-2: variant ref missing** | per-iframe placeholder (§5.1) | isolates one missing render from the others |
| **E-EMPTY-3: no comments yet** | Region 2: "No notes yet — click any element above to comment" | teaches the annotate affordance by pointing at it (recognition) |
| **E-EMPTY-4: no revisions yet** | History: "No changes landed yet" | absence stated plainly, not an empty table of `diff=0` |

### 5.3 Decision-paralysis states (the cognitive-load failure mode)

The control boundary can stall a human who does not know *which* gate to dispose or *whether* they are
allowed to. The design treats paralysis as a first-class state, not an edge case.

| Paralysis trigger | Surface behavior | Rationale |
|---|---|---|
| **"What do I do next?"** | The gate panel always shows exactly one **next-step** control as primary (visually + `aria-current`); locked gates show their reason. There is always a single obvious next action. | answers root-cause #1 (no step ordering) without a wizard that removes agency |
| **"Am I allowed to do this, or is the agent?"** | Every gate control is labeled with its actor in words ("you choose," "you approve") and the SKILL.md narrates the boundary on request. The agent's reversible work is visibly *not* a gate. | the Q0 boundary (human.1) made legible — the dialectic's whole point |
| **"Too many variants / I can't choose"** | Comparison is bounded to ≤3 (clause 2); the page never shows a 4th. Choosing is one click, reversible until apply. | bounds the decision count; lowers the stakes of step 4 (it is durable but re-selectable pre-apply) |
| **"I'm afraid to accept (irreversible)"** | The accept dialog states reversibility-by-counter-action plainly ("undone only by a new change") so the human knows the cost precisely, not vaguely. | calibrated fear beats vague dread; control without paralysis |

**ux-evidence.**

| Error/empty/paralysis claim | Class | proxy_limit |
|---|---|---|
| Every disabled gate has an associated reason | `soft_flag` (a11y.5: `aria-describedby` present) | presence ≠ the human read it |
| Exactly one primary next-step is marked at all times | `hard_gate` (DOM: exactly one `aria-current` step control) | one-marked ≠ the human noticed it |
| No blank/500 iframe ever reaches the human | `hard_gate` (placeholder doc returned for null ref) | "not blank" ≠ "understood as not-yet-generated" |
| Paralysis is reduced | `human_study` | unprovable here; the toy-game is the falsification |

---

## 6. Accessibility notes (the L1 floor)

C is **keyboard-native by construction** — this is the structural reason it beat A on the fixed-gate
obligation (s5 §3 tie-break reason 2). The floor:

- **a11y.3 — every disposal keyboard-operable.** All five gates (4, 7, 9, 10, 12) are native
  `<button>`s in normal tab order, operable by Enter/Space, with `aria-disabled` + an associated reason
  when locked. No mouse-only disposal exists. **Hard gate / block** — promotable after fixture
  calibration (known-good passes, known-bad mouse-only fails, the dense-but-legitimate layout does not
  false-fire).
- **a11y.4 — focus-trapped accept.** The step-10 accept is a `<dialog>`: focus enters on open, traps
  within, `Esc` cancels, focus returns to the trigger on close (WAI-ARIA APG dialog pattern). **Hard
  gate / high, BLOCKED on impl** until the two-gate build (N1).
- **a11y.5 — disabled-reason associated.** Each disabled gate's reason is `aria-describedby`-linked to
  its control, so AT announces *why*, not just *disabled*. **Soft flag / medium** (the on-record
  finding is that the reason exists in DOM but is not yet associated — this design closes that gap).
- **Keyboard annotation path (the click-to-annotate floor).** Because click is mouse-shaped, the page
  provides a **keyboard-equivalent**: Tab moves through annotatable elements (those carrying
  `data-od-id`, plus a roving-tabindex fallback for elements without), Enter opens the comment form for
  the focused element. The same `AnnotationTarget` (selector + elementLabel + odId-or-null, DC-1) is
  composed from the focused element. The **`comment add` CLI remains the ultimate AT fallback** (the B
  salvage, s5 §7). This keeps C keyboard-native **without** firing G-A11Y — G-A11Y only arms if the
  deferred A-upgrade (cross-origin `postMessage` pick) is pulled, where keyboard parity stops being
  native.
- **Region semantics + landmarks.** Header, three regions, and the dialog use native landmarks/roles so
  AT users can navigate by region (variants / notes / gates). The history list is a real list with
  timestamps as readable text, not a `diff=2/1/0` string (root-cause #7).
- **iframe a11y caveat (residue R2).** Sandboxed iframes can complicate AT traversal across the
  parent↔iframe boundary. The keyboard annotation path must be validated to actually reach in-iframe
  elements; if same-origin traversal proves brittle for AT, the `comment add` fallback is the floor.
  Carried to s8/s9 as a calibration item, not asserted solved.

---

## 7. Constraints discharged / handed forward

| s5 constraint | Discharged how in this design |
|---|---|
| Build C this run (one GET + one static page) | §2.1 (render GET) + §1/§2.2 (vanilla page); no SPA, no build step |
| Keep gates IN the page (resolve ODQ-2) | §1 Region 3 + §3: all five gates co-located with render + note; no terminal-split |
| `a11y.4` accept via `<dialog>` on the two-gate build | §4: focus-trapped dialog, named as N1-gated |
| Annotation honesty (no asserted pixel-fidelity) | DC-1 + §2.2 odId-null marker; ux-evidence rows keep capture-quality `human_study` |
| Deferred A-upgrade hook re-arms G-A11Y | §2.4 + §6: named, unbuilt, trigger preserved |

### 7.1 Residue handed to s8 (toy-game) and s9 (plan)

- **R1 — every `human_study` row is unproven** (root-causes #3/#4, paralysis reduction, "registered not
  rubber-stamped"). The toy-game prepares evidence (timing/traces); it does not prove the gains
  (ODQ-7 unchanged). No ergonomic claim is asserted in this artifact (charter clause 5).
- **R2 — iframe↔parent AT traversal** for the keyboard annotation path is a calibration unknown (§6);
  `comment add` is the named floor if it proves brittle.
- **R3 — INV-3 refusal is keyed on the literal actor string `system:auto`** (`apply-approved-batch.ts:33`,
  case-insensitive). The refusal is real but narrow: a misconfigured/forged write-scope actor that is
  not literally `system:auto` is not blocked by this check. The *page* never offers the agent a
  disposal control (gates are human-only UI), so the surface does not widen the hole — but s9 should
  note whether the human-only gates need a stronger actor-class check than a string match. Flagged, not
  resolved here (out of this stage's scope — it is core enforcement, not interaction design).
- **N1 — two-gate apply (steps 9–10) is a build dependency** for the accept-diff UX (§4.3); the
  single-gate `batch apply` is the runnable interim with no saw-the-diff pause. Routed to s9.
- **DC-1 — selector + elementLabel are server-REQUIRED**; every capture path must emit both (§2.2).
  This corrects the s5 "odId optional/target unknown" phrasing and is the load-bearing correctness fact
  for s9.

---

## 8. Stop condition + handoff

- **Chosen surface named** (§1, = s5 winner C). **Met.**
- **Overlay mechanics specified** — render GET, in-page click-to-annotate, `data-od-id`/selector/label
  capture (DC-1), ephemeral local server, POST → CaptureCommentEvent, gated by INV-2 (§2). **Met.**
- **Full human-agent loop step-by-step with per-step ergonomics rationale** (§3, all 12 steps). **Met.**
- **Accept-diff gate UX** — two-gate sequence, focus-trapped `<dialog>`, saw-the-diff, build honesty
  (§4). **Met.**
- **Error / empty / decision-paralysis states** with verified codes (§5). **Met.**
- **Accessibility floor (L1)** — a11y.3/.4/.5 + keyboard annotation path + iframe caveat (§6). **Met.**
- **Every non-trivial UX claim classified** against the five ux-evidence classes with a `proxy_limit`;
  no ergonomic gain asserted (charter clause 5). **Met.**
- **ODQ-2 resolved** (gates in-page), **ODQ-3 resolved** (keyboard annotation path + `comment add`
  fallback, C-native), **ODQ-4 resolved** (accept-diff via `<dialog>`, target-scoped on N1), **ODQ-5
  partially** (surface owns the labels/relabels; SKILL.md owns narration — glossary owner still routed
  to the skill-author half). **G-A11Y re-checked: does not fire** (C keyboard-native; re-armed on the
  deferred A-upgrade).

**Emits:** `design.interaction = the C review-page interaction design — one same-origin page hosting
≤3 sandboxed renders + co-located notes + the five durable gates; in-page click-to-annotate composing
the server-required {selector, elementLabel, odId-or-null} target POSTed to the existing comments route
under INV-2; the two-gate apply + focus-trapped `<dialog>` accept named as build dependency N1; a
keyboard-native a11y floor that keeps G-A11Y unfired`. Carried residue R1–R3, N1, DC-1 to s8/s9.
