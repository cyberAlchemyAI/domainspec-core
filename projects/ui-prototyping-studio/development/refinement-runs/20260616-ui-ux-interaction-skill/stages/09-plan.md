---
id: invoke-plan-ui-ux-interaction-skill
project: ui-prototyping-studio
title: "Invoke Plan (s9) — Non-executed build plan: SKILL.md + studio preview --annotate + accept-diff + L1 a11y floor"
status: plan
node_type: build-plan
run_id: 20260616-ui-ux-interaction-skill
dispatch_id: refine-ups-ui-ux-skill-20260616
step_id: s9-invoke-plan
capability_ref: invoke
mode: plan
pattern: layered-mwu-to-hardening
consumes_design: design.interaction
consumes_walkthrough: walkthrough.toy-game
consumes_handle: handle.define
emits_plan: plan.build
executed: false
updatedAt: 2026-06-16
---

# Invoke Plan (s9)

> **What this stage does.** It turns the s6 interaction design and the s8 dual-walkthrough repairs into a
> **NON-EXECUTED, layered build plan** for four deliverables: (a) installing the operating **SKILL.md**,
> (b) building **`studio preview --annotate`** (ephemeral local server + the injected click-to-annotate
> overlay + POST→CaptureCommentEvent), (c) the **accept-diff review surface** (two-gate saw-the-diff), and
> (d) the **L1 accessibility floor** on the surface. It layers each from a **minimum working unit (MWU)**
> to **progressive hardening** (value/cost boundaries per `implementation-layering`), maps every layer to
> the **project shape** (backend CLI verb + a served asset over the existing Fastify app), and names
> **verification** for every layer (a manual walkthrough + one Playwright check). It writes **no code**,
> runs **nothing**, and **marks proposals** explicitly.
>
> **Frame receipt.** Consumed `design.interaction` (s6: the C review-page design, DC-1, N1, R1–R3),
> `walkthrough.toy-game` (s8: D-REP-1…7, S-REP-1…8, A1–A6, F-COLD-1…8, F-CRIT-1 driving-side confirmation),
> and `handle.define` (the 12-step who-leads-when map, the SKILL required-contents §4, the two-layer
> scoping rule §5.4). Every code fact below was **re-verified in this checkout** (ledger §0.1); the plan
> does not inherit code claims from prose.

---

## 0. Plan posture, scope, and what "non-executed" means here

- **Non-executed.** This artifact is a build plan. It defines layers, owners, files-to-touch, acceptance
  checks, and verification. It does **not** edit `backend/`, does not run `studio`, does not start a
  server, and does not author the final SKILL.md prose (that is the skill-author half's deliverable; this
  plan specifies its *required contents, layering, and install steps*).
- **Everything new is a PROPOSAL.** Each layer is tagged **[PROPOSAL]**. Items that already exist and run
  in this checkout are tagged **[EXISTS]** so the plan never claims to "build" what is already built.
- **The project shape every layer maps to.** Two surfaces only: (1) **backend CLI verb(s)** in the
  `studio` CLI that route to the existing orchestration module, and (2) **a served asset** — HTML +
  inline script + the new `GET …/render` route — over the **existing** Fastify app (`index.ts`), bound to
  loopback. No SPA, no build step, no second process (s5/s6 constraint).
- **MWU→hardening layering rule.** Each deliverable is split at value/cost boundaries: **L0 = the smallest
  end-to-end slice that delivers the headline user value once** (the MWU), then **L1, L2, …** each adding
  one band of hardening (honesty, a11y, the two-gate engine, calibration) only when the prior layer's
  value is realized and verified. A later layer never blocks an earlier layer's value.

### 0.1 Code re-verification ledger (this checkout — re-run for s9, not inherited)

| Fact the plan rests on | Verified at | Result |
|---|---|---|
| `readHtml(ref): string \| null` exists | `infrastructure/file-artifact-content-store.ts:50` | **TRUE** — render route is a thin read, not new engine work |
| No `text/html`/`sendFile`/`reply.type` anywhere in routes | `interface/http-routes.ts` (0 matches) | **TRUE** — the render GET is genuinely new server behavior |
| Comment capture POST exists | `interface/http-routes.ts:230` `POST …/sessions/:sessionId/comments` | **TRUE** — `preview --annotate` POSTs to an existing route |
| INV-2 enforced in core | `application/capture-comment-event.ts:45` throws `BASELINE_GATE_UNSATISFIED` when `selectionGate !== "satisfied"` | **TRUE** — gate is server-authoritative |
| INV-3 refusal is a narrow literal-string check | `application/apply-approved-batch.ts:33` refuses only when actor lowercases to `system:auto` | **TRUE & NARROW** (residue R3 / R-S7-1) |
| Apply route **defaults actor to `"web-ui"`** | `interface/http-routes.ts:341` `parseActor(request.body.applyRequestedBy, "web-ui")` (same default at 7 other write routes) | **TRUE** — the core cannot tell agent from human; SKILL is the only self-disposal guard (F-CRIT-1) |
| Two-gate engine **already exists as pure functions** but is **unwired** | `application/two-gate-apply.ts`: `validateAndStage(...)` → `StagedRevision{stagedRef, candidateHtmlHash}` → `acceptStaged(stagedRef, acceptedHash, …)`; **only referencer is its own `two-gate-apply.test.ts`** | **TRUE — sharpens N1.** The accept-diff engine is built and tested; N1 is **wiring** (route + CLI + page), not authoring the engine. |
| Single-gate `apply-approved-batch.ts` stages **and** advances head in one call | `application/apply-approved-batch.ts` | **TRUE** — the runnable interim with no saw-the-diff pause |

> **N1 re-scoped (load-bearing correction for the plan).** s6/s8 treated the two-gate saw-the-diff apply
> as "unbuilt." Re-verified: the **pure engine is built and unit-tested** (`two-gate-apply.ts`:
> `validateAndStage` → `acceptStaged`, idempotency-at-verdict by accepted-hash match). What is missing is
> the **wiring**: no route exposes stage/accept, no CLI verb calls them, no page renders the staged diff.
> This makes the accept-diff deliverable **cheaper and lower-risk than s8 implied** — it is integration,
> not engine design. Captured as **N1' (wiring, not authoring)**.

---

## 1. Dependency graph across the four deliverables

```
                ┌────────────────────────────────────────────────────┐
                │  PRE: render GET route (one read-only GET)  [PROPOSAL]│  ← C's only new server work
                └───────────────┬───────────────────────────┬─────────┘
                                │                           │
            (b) preview --annotate (MWU)            (d) L1 a11y floor
            ephemeral server + overlay + POST        rides ON the served page
                                │                           │
                ┌───────────────┴──────────┐                │
                │                          │                │
        (a) SKILL.md install        (c) accept-diff surface  │
        teaches the runnable        wires two-gate engine ───┘ (a11y.4 dialog lives here)
        subset + STOP discipline    (route+CLI+page) = N1'
```

- The **render GET** is the shared prerequisite for (b), (c), and (d) — nothing the human *sees* works
  without it. It is the single cheapest, highest-leverage first build.
- **(a) SKILL.md** can be installed in parallel with (b) at the **honest-interim** level (teach only the
  runnable single-gate path), then upgraded when (c) lands.
- **(c) accept-diff** depends on the render GET (to show the staged diff) and unblocks the SKILL's
  saw-the-diff narration (S-REP-4).
- **(d) a11y floor** rides on the served page from (b); its highest gate (a11y.4 focus-trapped dialog)
  is *part of* (c)'s accept surface.

---

## 2. PRE — the shared render route (the one new GET) [PROPOSAL]

The cheapest prerequisite; every visible deliverable depends on it. Built as a single layer.

| Field | Value |
|---|---|
| **Project surface** | served asset — one new read-only route on the existing Fastify app |
| **File to touch** | `interface/http-routes.ts` (add route); reuse `infrastructure/file-artifact-content-store.ts:50` `readHtml` **[EXISTS]** |
| **Route** | `GET /api/ui-prototyping-studio/sessions/:sessionId/variants/:label/render` → `readHtml(ref)` → `reply.type("text/html").send(html)` (the only `text/html` reply in the module) |
| **Scope** | `assertReadScope` (mirror the existing GET routes) — rendering is reversible, read scope only |
| **Null-ref behavior** | `readHtml` returns `null` → return the honest placeholder document ("This variant has no rendered HTML yet"), **never a 500, never a blank iframe** (E-EMPTY-2) |
| **Second render target** | `GET …/render` (no `:label`) serves the **review page itself** (static HTML + inline script). No build step. |

- **MWU (L0):** the variant-render GET returns staged HTML for a known ref; iframe shows it.
- **Hardening (L1):** null-ref placeholder + the page-serving render target + read-scope assertion.
- **Acceptance:** a known variant ref renders as HTML in an iframe; an unknown ref renders the placeholder
  doc, not a 500.

**Verification.**
- *Manual:* open the served page, confirm a generated variant appears in its iframe; hit an unknown
  `:label` and confirm the placeholder doc (not a blank/500).
- *Playwright:* `GET …/variants/:knownLabel/render` returns `200` + `content-type: text/html`; an
  unknown label returns `200` + the placeholder marker string (assert on a stable text node), never `5xx`.

**ux-evidence.** `hard_gate` (route returns text/html for a valid ref; placeholder doc for null) ·
proxy_limit: "not blank/500" ≠ "the human read it as not-yet-generated" (that residual is `human_study`).

---

## 3. Deliverable (b) — `studio preview --annotate`: ephemeral server + overlay + POST→CaptureCommentEvent

The headline cold-start value: **see the renders, click an element, leave a note.** Note the SKILL keep-
list forbids the *agent* from "standing up its own server" — `preview` is a **human-facing CLI verb** that
opens the existing Fastify app's review page on loopback (s8 A2 resolution); it is not the agent spinning
up a rogue process.

### 3.0 Layer map (MWU → hardening)

| Layer | What it adds | Value/cost boundary | Tag |
|---|---|---|---|
| **b-L0 (MWU)** | `studio preview --annotate --session <id>` boots the **existing** Fastify app on `127.0.0.1` (reusing `index.ts` bootstrap **[EXISTS]**), prints the review-page URL, and the page shows ≤3 variant iframes via the render GET. Click an in-iframe element → compose `{selector, elementLabel, odId-or-null}` (DC-1) → open the 3-control comment form → POST to `…/comments` **[EXISTS route]** → note appears in Region 2. INV-2 enforced **by the core** (b-L0 does not mirror it yet). | Delivers preview + click-annotate end-to-end once. | [PROPOSAL] |
| **b-L1** | **INV-2 client mirror**: annotate affordance disabled-with-reason until baseline is chosen ("Pick an option to build before you can comment on it") — avoids a failed round-trip (root-cause #2). Server stays authoritative. | One band: turn a server refusal into a pre-emptive disabled-with-reason. | [PROPOSAL] |
| **b-L2** | **Honesty markers (DC-1 + S-REP-4 + D-REP-4):** odId-null marker re-worded out of jargon ("this note is pinned to where you clicked; if the card is regenerated it may move"); plain-language helper text on `severity`/`intent` (F-COLD-5). | One band: comprehension repairs the surface leaks. | [PROPOSAL] |
| **b-L3** | **Seam + progress repairs (D-REP-1, D-REP-2):** persistent "Claude is driving this session in your chat/terminal" seam line (F-COLD-1); a "generating…" state with a bounded "taking longer than expected / generation failed — ask Claude to retry" branch (F-COLD-2 / M1). | One band: close the agent↔surface seam and the generation gap. | [PROPOSAL] |
| **b-L4** | **Loopback hard-binding as a SKILL+server rule (S-REP-8 / M4):** bind strictly to `127.0.0.1`; never expose beyond loopback — given F-CRIT-1 this is the de-facto network security boundary for the durable gates. | One band: the network backstop for the SKILL-only self-disposal guard. | [PROPOSAL] |

### 3.1 Project-surface mapping

- **CLI verb [PROPOSAL]:** `studio preview --annotate --session <id>` — a new verb wrapping the existing
  Fastify bootstrap and printing the URL. (Resolves s8 A2: the sanctioned "here is your review page"
  handoff. The agent does NOT run `preview` to self-serve gates — it tells the human the URL.)
- **Served asset [PROPOSAL]:** the review page (static HTML + one inline `<script>`) served by the render
  GT (§2). The script: render iframes, delegated in-iframe click handler, target composition (DC-1),
  comment form, POST to `…/comments` **[EXISTS]**, Region 2 note list.
- **Reused [EXISTS]:** Fastify bootstrap (`index.ts`), comments POST route (`http-routes.ts:230`),
  `captureCommentEvent` (`capture-comment-event.ts`), INV-2 gate, `readHtml`.

### 3.2 DC-1 constraint, restated as a build gate

Every capture path — **mouse click, keyboard pick (§5), and the `comment add` AT fallback** — MUST emit a
non-empty `selector` AND a non-empty `elementLabel`; `odId` is captured if present else `null`. The page
can **never** POST an odId-only comment (verified: `parseAnnotationTarget` hard-requires both via
`parseRequiredString`). This is an acceptance gate on every layer that captures.

### 3.3 Verification

- *Manual walkthrough (the s8 sample session "prototype an onboarding card"):* run `preview --annotate`;
  confirm three iframes render; click the card's button; confirm highlight + 3-control form + odId-null
  honesty marker (re-worded); submit; confirm the note appears co-located in Region 2; confirm the
  annotate affordance was disabled-with-reason before a baseline was chosen.
- *Playwright check:* with a chosen baseline, click an in-iframe annotatable element → assert a POST to
  `…/comments` fires with a body whose `target` carries **non-empty `selector` AND `elementLabel`**
  (DC-1); without a baseline, assert the affordance is `aria-disabled` with an associated reason and **no
  POST fires**.

**ux-evidence.** capture shape = `hard_gate` (body validates against `parseAnnotationTarget`) · INV-2
mirror = `soft_flag` (reason present + associated; can drift from the server gate — only the server is
authoritative) · "click beats typing a selector" = `human_study` (proxy_limit: a captured target ≠ the
human found it easier).

---

## 4. Deliverable (c) — the accept-diff review surface (two-gate saw-the-diff) = N1'

**Re-scoped to WIRING, not engine authoring** (ledger §0.1): `validateAndStage` → `acceptStaged` already
exist and are unit-tested. This deliverable exposes them as a route + CLI verb + page so the human can
**see the staged diff, then accept the exact staged hash** before head advances. Until c-L0 lands, the
runnable path is single-gate `batch apply` (stages + advances in one call) and the surface/SKILL must say
so honestly (D-REP-6 / S-REP-4).

### 4.0 Layer map (MWU → hardening)

| Layer | What it adds | Value/cost boundary | Tag |
|---|---|---|---|
| **c-L-HONEST (interim, ships FIRST, before any wiring)** | **D-REP-6:** until the two-gate is wired, the runnable single-gate control is labeled honestly — **"Apply this change — it will be applied in one step"**, NOT "Apply + see the diff." The s6 §3 step-9/10 cells mirror the single-gate reality. No broken promise on the surface. | Zero new engine; removes the F-COLD-7 broken promise immediately. | [PROPOSAL] |
| **c-L0 (MWU)** | Wire **gate-1**: a route + `studio apply --stage` CLI verb calling `validateAndStage` **[EXISTS]** → returns `{stagedRef, candidateHtmlHash}` **without advancing head**. Page renders the staged diff inline (the change list + before/after of the affected region via the render GET). | First delivery of "see the diff before it lands." | [PROPOSAL] |
| **c-L1** | Wire **gate-2**: the **accept** — a focus-trapped `<dialog>` (a11y.4) showing the honest diff + two controls ("Accept — apply this change for good" / "Cancel — keep editing") + the irreversibility stated in words; on Accept, POST the **accepted hash** → `acceptStaged(stagedRef, acceptedHash, …)` **[EXISTS]** advances head by exactly one revision (idempotency-at-verdict: a hash mismatch is rejected). | Completes saw-the-diff; the irreversible gate is reachable only past the diff. | [PROPOSAL] |
| **c-L2** | **History + handoff repairs (D-REP-7):** post-accept, history shows plain summary + timestamp + note link **[design EXISTS]**; pin the handoff to a **visible, openable** deliverable (a link that opens the rendered result), never a bare reference ID (F-COLD-8). | One band: the exit reads as a deliverable, not an ID. | [PROPOSAL] |
| **c-L3 (PROPOSAL, core-hardening — flagged, see §7)** | **R-S7-1 / R3:** widen the self-disposal guard from the literal `system:auto` string match to an **actor-class check** at the durable routes (stage/accept/approve/baseline), so the core — not only the SKILL — can refuse agent self-disposal. | Highest band: turns the SKILL-only guard into a core guard. | [PROPOSAL — out of this surface's scope; routed to core owners] |

### 4.1 Project-surface mapping

- **Routes [PROPOSAL]:** `POST …/apply/stage` → `validateAndStage`; `POST …/apply/accept` → `acceptStaged`
  (accepted-hash in body). Both reuse the **existing pure engine**.
- **CLI verbs [PROPOSAL]:** `studio apply --stage --session <id>` (gate 1) and `studio apply --accept
  --staged-ref <ref> --hash <hash>` (gate 2). Both are **human-only** in the SKILL never-do spine.
- **Served asset [PROPOSAL]:** the inline diff render (gate 1) and the focus-trapped `<dialog>` (gate 2).
- **Reused [EXISTS]:** `two-gate-apply.ts` (`validateAndStage`, `acceptStaged`), the render GET (§2) for
  before/after, the revision-record path.

### 4.2 Build honesty (carried from s6 §4.3 / s8 D-REP-6 / S-REP-4)

**c-L-HONEST ships before c-L0.** No control may be labeled "Apply + see the diff" and no SKILL narration
may promise a diff-pause until c-L1 is verified. This is **Blocking-for-honesty**: the label/narration must
match the runnable path at all times.

### 4.3 Verification

- *Manual walkthrough:* (interim) confirm the single-gate control reads "applied in one step" and lands
  the change with no diff-pause claim; (post-c-L1) click "Apply this change" → staged diff renders inline
  → "Review and accept" opens the `<dialog>` → read the diff → Accept → head advances by exactly one
  revision and the dialog closes; Cancel keeps editing with no head change.
- *Playwright check:* assert that on gate-1 the route returns a `stagedRef` + hash and **head did not
  advance** (revision manifest length unchanged); on gate-2 accept with the matching hash, head advances
  by **exactly one**; an accept with a **mismatched hash is rejected** (idempotency-at-verdict). For the
  interim, assert **no control bears the string "see the diff"** until two-gate is wired.

**ux-evidence.** stage-without-advance + accept-by-hash = `hard_gate` (deterministic, engine already
tested) · diff foregrounded before the accept control is reachable = `hard_gate` (DOM/focus order) ·
"registered, not rubber-stamped" = `human_study` (`human.2`, unprovable here) · diff salience = `cog.5`
`screenshot_review` (proxy_limit: salience ≠ comprehended).

---

## 5. Deliverable (d) — the L1 accessibility floor on the surface

Rides on the served page (b) and the accept dialog (c). C is keyboard-native by construction (s5 tie-break
reason 2); this floor makes that concrete and **keeps G-A11Y unfired** (G-A11Y only arms if the deferred
cross-origin A-upgrade is pulled — §2.4 of s6).

### 5.0 Layer map (MWU → hardening)

| Layer | What it adds | Value/cost boundary | Tag |
|---|---|---|---|
| **d-L0 (MWU = the guaranteed AT floor)** | **`comment add` as the explicit L1 AT fallback (S-REP-6):** `studio comment add --selector … --elementLabel … --severity … --intent … --note …` emits the **identical** CommentEvent (DC-1). This is the floor that holds even if iframe keyboard traversal proves brittle (R2). | The annotate path that works for AT **today**, no harness needed. | [PROPOSAL — CLI verb may already exist; verify, do not re-author] |
| **d-L1** | **a11y.3 — every disposal keyboard-operable:** all five gates (4, 7, 9, 10, 12) are native `<button>`s in tab order, Enter/Space operable, `aria-disabled` + associated reason when locked. No mouse-only disposal. | The control boundary is keyboard-reachable. | [PROPOSAL] |
| **d-L2** | **a11y.5 — disabled-reason associated:** each locked gate's reason is `aria-describedby`-linked so AT announces *why*, not just *disabled* (closes the on-record gap). Plus **exactly one** primary next-step marked `aria-current` at all times (D-REP-5 / paralysis state), and that marker maps to a **runnable** action (resolves F-COLD-6: surface the synthesize/draft control). | AT hears the reason and the single next step. | [PROPOSAL] |
| **a11y.4** | **Focus-trapped accept dialog** — built **inside c-L1** (§4): focus enters on open, traps within, `Esc` cancels, focus returns to trigger on close (WAI-ARIA APG dialog pattern). | The keyboard floor for the one irreversible gate. | [PROPOSAL — co-owned with (c)] |
| **d-L3 (calibration, PROPOSAL — UNBUILT harness)** | **R-S7-2 / R2:** the keyboard-annotation-over-iframe AT-reachability harness. Tab must reach an in-iframe annotatable element across the sandboxed boundary and Enter must open the form composing DC-1. Until this harness passes, the in-page keyboard pick stays **Tier-B/provisional** and `comment add` (d-L0) is the floor. | Promotes the keyboard pick from provisional to a hard gate — only after a deterministic harness exists. | [PROPOSAL — harness is unbuilt; claim stays unproven until it passes] |

### 5.1 Verification

- *Manual walkthrough:* tab through Region 3 — every gate reachable and operable by Enter/Space; locked
  gates announce their reason (with a screen reader if available); confirm exactly one primary next-step;
  run `studio comment add …` and confirm the identical CommentEvent lands in Region 2.
- *Playwright check (a11y assertions, deterministic subset):* assert (i) every gate `<button>` is in tab
  order and operable by keyboard; (ii) each locked gate has an `aria-describedby` resolving to a non-empty
  reason node; (iii) **exactly one** element carries `aria-current` and it maps to an enabled, runnable
  control; (iv) the accept `<dialog>` traps focus (Tab cycles within; focus returns to trigger on close;
  `Esc` cancels). **The iframe-traversal harness (d-L3) is named but NOT run here — it is the unbuilt
  dependency the keyboard-native claim rests on (R-S7-2); until it passes, `comment add` is the asserted
  floor and the keyboard-pick claim is marked unproven.**

**ux-evidence.** a11y.3/a11y.4 = `hard_gate` (deterministic, **promotable only after fixture calibration:**
known-good passes, known-bad mouse-only / non-trapping fails, dense-but-legitimate layout does not
false-fire) · a11y.5 + single-`aria-current` = `soft_flag`/`hard_gate` (DOM presence is checkable; that the
human/AT *read* it is `human_study`) · iframe traversal = `hard_gate` **once the harness exists, UNBUILT
now** (proxy_limit: reachability ≠ an AT user found it easy).

---

## 6. Deliverable (a) — installing the operating SKILL.md

The SKILL is **the binding control on agent self-disposal** — the core defaults the apply actor to
`"web-ui"` and refuses only the literal `system:auto`, so it cannot tell agent from human (F-CRIT-1, ledger
§0.1). The install plan specifies the SKILL's required contents, its layering, and the install steps; it
does **not** author the final prose (skill-author half).

### 6.0 Layer map (MWU → hardening)

| Layer | What it adds | Value/cost boundary | Tag |
|---|---|---|---|
| **a-L0 (MWU = honest-interim SKILL)** | Teach **only the runnable X2 subset** (§5.4): `variants register`, `synthesize`, `batch approve`, `batch apply` (single-gate, narrated honestly), `comment add`, `baseline select\|commit`, `handoff export`. **Never-do spine** (`baseline select\|commit`, `batch approve`, `batch apply`/`apply`/`accept` are human-only) with the **F-CRIT-1 wording carried into the narration** (S-REP-1): "the system would NOT stop me — it cannot tell me from you — my discipline is the control." | A correct, honest operating contract that ships with single-gate truth. | [PROPOSAL] |
| **a-L1** | **Seam + author-to-disk repairs (S-REP-7):** specify where Claude writes HTML before `variants register --from <dir>` (A1) and the sanctioned "here is your review page" URL narration without standing up its own server (A2). | Removes the two undefined agent seams. | [PROPOSAL] |
| **a-L2** | **Stranding + refusal scripts (S-REP-2, S-REP-3):** scripted **refusal-with-recommendation** for "you choose/approve/apply for me" (A3); require Claude to **proactively offer** to synthesize once notes exist (A4 → resolves the agent side of F-COLD-6). | The human is never stranded at a gate or a missing list. | [PROPOSAL] |
| **a-L3** | **Ownership + AT + network rules (S-REP-5, S-REP-6, S-REP-8):** resolve `handoff export` ownership in the never-do spine (A6); teach `comment add` as the explicit L1 AT fallback (DC-1) and frame the in-page keyboard pick as Tier-B until d-L3 passes; carry M4 loopback-only as a SKILL rule. | Closes the remaining SKILL ambiguities. | [PROPOSAL] |
| **a-L4 (upgrade, gated on c-L1)** | **Saw-the-diff narration (S-REP-4):** once the two-gate accept-diff is wired (c-L1), upgrade the apply narration from "applied in one step" to the two-gate saw-the-diff flow. **Until then, never describe the unbuilt accept as current.** | The honest narration upgrade, gated on the build. | [PROPOSAL — gated on c-L1] |

### 6.1 Install steps (non-executed — specified, not run)

1. Place `SKILL.md` at the studio skill package path (skill-author authors the prose against a-L0…a-L4).
2. Validate the **taught command set ⊆ runnable X2 subset** (A5 shape check) — no taught verb may be
   unbuilt; `accept`/two-gate stays named-as-build-dependent until c-L1.
3. Validate the **never-do spine** lists every human-only durable verb (`baseline select|commit`, `batch
   approve`, `batch apply`/`apply`/`accept`, and the resolved `handoff export` decision).
4. Confirm the F-CRIT-1 wording appears in the do/never-do narration, not only the description (S-REP-1).

### 6.2 Verification

- *Manual walkthrough (s8 agent voice):* drive "prototype an onboarding card" per the installed SKILL;
  confirm Claude leads only the reversible arc, STOPs at all five durable gates, narrates each STOP with
  the F-CRIT-1 wording, proactively offers synthesize, and hands the review-page URL.
- *Playwright/CLI check:* a shape assertion that **every command the SKILL teaches resolves to a built CLI
  verb** (taught ⊆ runnable, A5), and that no taught control bears the saw-the-diff promise while c-L1 is
  unwired (A5/S-REP-4 honesty gate).

**ux-evidence.** taught ⊆ runnable = `hard_gate` (shape-checkable against the CLI) · F-CRIT-1 is the sole
control = `not_automatable` + `soft_flag` (the SKILL *stating* it ≠ the agent obeying it — obedience is R1,
carried to runtime) · refusal/offer scripts = `human_study` (presence checkable; acceptance unprovable
here).

---

## 7. Proposals marked, residue, and what this plan does NOT do

### 7.1 Proposals (every new build, marked)

| ID | Proposal | Deliverable | Layer | Severity / gating |
|---|---|---|---|---|
| P-PRE | The one new read-only render GET | shared | §2 | prerequisite for all visible value |
| P-b0…b4 | `preview --annotate` MWU + INV-2 mirror + honesty + seam/progress + loopback-bind | (b) | §3.0 | b-L0 = MWU; b-L4 = network backstop |
| P-cH | Honest single-gate label/narration (ships first) | (c) | §4.0 | **Blocking-for-honesty** (D-REP-6/S-REP-4) |
| P-c0/c1 | Wire `validateAndStage` (stage) + `acceptStaged` (accept dialog) = **N1'** | (c) | §4.0 | wiring of an EXISTS engine — lower risk than s8 implied |
| P-c2 | Visible/openable handoff + plain history | (c) | §4.0 | Medium (F-COLD-8) |
| P-c3 | **Core actor-class self-disposal guard** | (c)/core | §4.0 | **PROPOSAL — out of surface scope; routed to core owners (R-S7-1/R3)** |
| P-d0…d3 | `comment add` AT floor + a11y.3/.5 + (a11y.4 in c) + iframe harness | (d) | §5.0 | d-L0 = floor; d-L3 = unbuilt calibration |
| P-a0…a4 | SKILL install: honest-interim → seams → scripts → ownership/AT/net → saw-the-diff upgrade | (a) | §6.0 | a-L0 = MWU; a-L4 gated on c-L1 |

### 7.2 Residue carried (not resolved by this plan)

- **R1 — every `human_study` row remains unproven.** The plan names manual + Playwright verification that
  proves *shape/behavior*; it does NOT prove ergonomic gain. Only a real cold-start study settles the
  human_study claims (charter clause 5). **No ergonomic gain is asserted here.**
- **R-S7-1 / R3 — the core self-disposal guard is a narrow literal-string match** (`system:auto`) and the
  apply actor defaults to `"web-ui"`. The SKILL (a-L0) is the binding control; P-c3 proposes the core fix
  but it is **out of this interaction surface's scope** and routed to core owners. **Flagged, not closed.**
- **R-S7-2 / R2 — the keyboard-annotation-over-iframe harness (d-L3) is UNBUILT.** Until it passes the
  keyboard pick is Tier-B and `comment add` (d-L0) is the asserted AT floor. **The keyboard-native claim
  stays unproven.**
- **DC-1** is an acceptance gate on every capture path (mouse / keyboard / `comment add`): non-empty
  `selector` + non-empty `elementLabel` + odId-or-null. Verified server-required; carried as a hard check.
- **G-A11Y stays unfired** — it arms only if the deferred cross-origin A-upgrade (s6 §2.4) is pulled.

### 7.3 What this plan explicitly does NOT do

- Does not author the final SKILL.md prose (skill-author half) — it specifies required contents + layering.
- Does not write, run, or test any backend code; does not start a server; does not run `studio`.
- Does not re-run the tournament (s5) or re-author the design (s6).
- Does not resolve the core actor-class guard (P-c3) — flagged and routed, not decided.

---

## 8. Stop condition + handoff

- **(a) SKILL.md install plan** — required contents, layering a-L0…a-L4, install steps, verification (§6).
  **Met.**
- **(b) `studio preview --annotate`** — ephemeral loopback server (reusing `index.ts`) + injected
  click-to-annotate overlay (DC-1) + POST→`CaptureCommentEvent` (existing route, INV-2 in core), layered
  b-L0…b-L4 with verification (§3). **Met.**
- **(c) accept-diff review surface** — re-scoped to **N1' wiring** of the EXISTS two-gate engine
  (`validateAndStage`→`acceptStaged`) + focus-trapped `<dialog>`, with the honest single-gate interim
  shipping first, layered c-L-HONEST…c-L3 with verification (§4). **Met.**
- **(d) L1 a11y floor** — `comment add` AT floor (d-L0) + a11y.3/.4/.5 + the unbuilt iframe-traversal
  harness named, layered d-L0…d-L3 with verification, G-A11Y kept unfired (§5). **Met.**
- **MWU→hardening layering** at value/cost boundaries for every deliverable (§3.0/§4.0/§5.0/§6.0). **Met.**
- **Project mapping** — backend CLI verb(s) + a served asset over the existing Fastify app, with
  EXISTS-vs-PROPOSAL marked per layer. **Met.**
- **Verification named per layer** — a manual walkthrough + a Playwright check for each deliverable (§2.x,
  §3.3, §4.3, §5.1, §6.2). **Met.**
- **Proposals marked** (§7.1); residue R1/R-S7-1/R-S7-2/DC-1 carried (§7.2); non-executed (§0, §7.3).
  **Met.**

**Emits:** `plan.build = a NON-EXECUTED, MWU→hardening layered build plan for the four deliverables — the
shared render GET (prerequisite); (b) preview --annotate (b-L0…b-L4); (c) the accept-diff surface re-scoped
to N1' wiring of the already-built two-gate engine with an honest single-gate interim shipping first
(c-L-HONEST…c-L3); (d) the L1 a11y floor with comment add as the AT floor and the iframe-traversal harness
named-but-unbuilt (d-L0…d-L3); (a) the SKILL.md install plan (a-L0…a-L4) with F-CRIT-1 as the binding
self-disposal control. Every layer maps to a backend CLI verb and/or a served asset over the existing
Fastify app, marks EXISTS vs PROPOSAL, and names a manual walkthrough + a Playwright check. Residue
R1/R-S7-1/R-S7-2/DC-1 carried; G-A11Y unfired; P-c3 (core actor-class guard) flagged and routed to core
owners; no ergonomic gain asserted.`
