---
id: design-review-ui-ux-interaction-skill
project: ui-prototyping-studio
title: "Design Review (s7) — Adversarial Interrogation of the s6 Interaction Design + the SKILL Draft"
status: review
node_type: design-review
run_id: 20260616-ui-ux-interaction-skill
dispatch_id: refine-ups-ui-ux-skill-20260616
step_id: s7-design-review
capability_ref: review
mode: red-team
pattern: interrogation
consumes_design: design.interaction
consumes_handle: handle.define
emits_review: review.design
updatedAt: 2026-06-16
---

# Design Review (s7) — Interrogation

> **What this stage does.** It attacks the s6 interaction design AND the SKILL draft along four
> adversarial lines the dispatch named: (1) are the **who-leads-when boundaries honored** — does the SKILL
> ever let Claude Code self-approve/self-apply? (2) is the overlay actually **low-friction + accessible**?
> (3) are **UX claims correctly classified** (hard_gate only for deterministic/standards-backed; cognitive
> claims as soft_flag/human_study)? (4) does the design **address the cold-start findings**? It renders a
> single verdict per line of attack and one overall verdict with required fixes. It does NOT re-run the
> tournament, re-author the design, or build anything.
>
> **Frame receipt.** Consumed `design.interaction` (s6), `handle.define` (D1–D5, s2), and the s1 evidence
> floor (cold-start §4, ux-evidence five classes §5, charter §0). Every code claim I dispute was
> re-verified in this checkout against `backend/src/modules/ui-prototyping-studio/`.

---

## 0. Verdict (up front)

**FLAG — proceed to s8/s9 only after one BLOCKING correction (F-CRIT-1) and three required fixes
(F1–F3) are folded into the design and the SKILL draft.**

The design is, overall, **strong and honest**: it honors the reversible/durable partition step-for-step,
it classifies its UX claims unusually carefully (cognitive claims are correctly held as `human_study`,
not asserted as gates), it addresses every cold-start root-cause with a named surface behavior, and it is
keyboard-native by construction. Three things keep it from a clean pass, one of them serious:

- **F-CRIT-1 (BLOCKING for the SKILL's central claim).** The design and the SKILL draft both assert that
  the durable gates are **"human-only and refused server-side"** (SKILL description verbatim; s6 §3 step 7,
  §5.1). **This is false for the HTTP surface the design builds on.** Verified in code: the **approve**
  gate has *no actor-class check whatsoever* (`approve-mutation-batch.ts` accepts any non-empty
  `approvedBy`), and the **apply** gate refuses only the literal lowercased string `"system:auto"`
  (`apply-approved-batch.ts:33`), while the route defaults the actor to `"web-ui"` and reads it from the
  *request body* (`http-routes.ts:308,341`). Both gates share one write scope (`assertWriteScope`) with
  the agent's own reversible calls. **The core cannot tell Claude Code from the human.** On this surface,
  "the human disposes" is enforced by the SKILL's behavioral discipline + a client-side disabled button —
  *not* by the core. The design's own residue R3 sees the apply hole but understates it (it does not note
  approve has zero check) and the SKILL/description state the stronger claim as fact. This must be
  corrected before the SKILL ships, because the SKILL's posture ("refused server-side") is its load-bearing
  authority claim and it is not true.

- **F1 (required).** The keyboard annotation path is asserted as the thing that "keeps G-A11Y unfired,"
  but it is itself an *unvalidated, novel* interaction pattern over a sandboxed-iframe boundary (the design
  admits this in R2). The a11y floor is therefore softer than the design's own confident framing.

- **F2 (required).** Two `hard_gate` classifications are mis-scoped or premature against the s1 rule
  "hard gates only for deterministic/standards-backed failures, and none promotes without fixture
  calibration."

- **F3 (required).** Cold-start root-cause **#1 (identity evidence)** — the *top-ranked Critical* finding —
  is silently dropped from scope without the design saying so, leaving a coverage gap the reader cannot see.

The SKILL draft handed to this stage is **truncated** (it ends mid-loop at step 3); §6 below reviews only
what is visible and flags the rest as unreviewed.

---

## 1. Line of attack #1 — who-leads-when: does the SKILL let Claude Code self-approve/self-apply?

This is the dispatch's primary question and the one that surfaces the BLOCKING finding.

### 1.1 What the design + SKILL claim

- SKILL description (verbatim): *"You NEVER self-approve, self-apply, or self-accept — those are
  human-only and **refused server-side**."*
- SKILL posture: *"Everything that records an intentional choice or advances the work is a human-only gate,
  **enforced in the core** — not in CLI flags. A CLI flag is input, not authority."*
- s6 §0 synthesis: *"control is absolute at the durable boundary."*
- s6 §3 step 7 (approve): *"**Claude Code refused server-side if it tries** (`AUTO_APPLY_FORBIDDEN`
  lineage / INV-3)."*
- s6 §5.1: *"if invoked via API by `system:auto`, the core refuses."*

### 1.2 What the code actually enforces (re-verified this checkout)

| Gate | Server-side actor enforcement | Verified at |
|---|---|---|
| **Approve** (step 7) | **NONE.** Requires only that `approvedBy` is a non-empty string and `approvedAt` parses. Any actor string — `"claude-code"`, `"system:auto"`, `"human"` — is accepted. | `approve-mutation-batch.ts:61-77` (only `APPROVAL_METADATA_REQUIRED` non-empty check); route `http-routes.ts:308` passes `request.body.approvedBy` straight through |
| **Apply** (step 9) | **NARROW.** Refuses *only* if `applyRequestedBy.toLowerCase() === "system:auto"`. The route **defaults the actor to `"web-ui"`** and reads it from the request body. | `apply-approved-batch.ts:32-41`; route `http-routes.ts:341` `parseActor(request.body.applyRequestedBy, "web-ui")` |
| **Both** | Gated by one shared `assertWriteScope(x-scopes)` — the **same** scope Claude Code uses for `variants register` / `synthesize`. No human-vs-agent identity distinction exists at the server. | `http-routes.ts:303,336` |

**Consequence.** On the C surface this design builds (the HTTP routes + the served page), an actor holding
the write scope — which Claude Code holds, because it needs it for steps 2/6/8 — can:

1. **Self-approve** with zero server resistance (just send any `approvedBy`).
2. **Self-apply** by sending any `applyRequestedBy` other than the literal `"system:auto"` (and `"web-ui"`,
   the route default, is exactly such a string).

The *only* things standing between Claude Code and a self-disposed durable gate are (a) the SKILL's
behavioral never-do list and (b) the client-side disabled button on the page. **Neither is "the core."**
The `AUTO_APPLY_FORBIDDEN` check is real but is a tripwire for one hard-coded string, not an
identity-class gate; it would catch a literally-mislabeled batch job, not a write-scoped agent.

### 1.3 Why this is BLOCKING, not merely a residue

The design *partially* sees this (R3) but draws the wrong conclusion: it says "the *page* never offers the
agent a disposal control … so the surface does not widen the hole." That is true for the **page**, but the
SKILL operates the **CLI/HTTP surface directly**, not the page — the page is for the human. The whole point
of the SKILL is to make Claude Code drive the same surface the human drives. So the question "does the
SKILL let Claude Code self-approve?" reduces to: *what actually stops a write-scoped agent from POSTing the
approve route?* The honest answer is **only the SKILL's own words** — and the SKILL currently justifies
those words by appealing to a server enforcement that does not exist for approve and is trivially evadable
for apply. A behavioral rule that cites a false backstop is weaker than one that is honest about being the
only line of defense.

This does not mean the design is wrong to forbid self-approval — it is exactly right to. It means the
**justification is mis-stated**, and a mis-stated justification in the *one place the SKILL claims its
authority* is a correctness defect, not a nuance.

### 1.4 What is genuinely honored (credit where due)

The *partition* is correct and consistently applied: the 12-step map never puts a gate on a reversible step
(verified against s2 §3.2 and the reversibility model), Claude Code's authority is correctly confined to
steps 2/6-trigger/8, and the page never renders a disposal control for the agent. The engine-purity
framing (step 8, value-in/value-out, never the store/clock/append path) is sound. The defect is *only* the
"refused server-side" overclaim — but it is load-bearing.

### 1.5 Required fix F-CRIT-1

1. **Correct the SKILL description and posture.** Replace *"refused server-side"* with an honest statement:
   the durable gates are **human-only by contract and by this SKILL's absolute discipline**; the core
   enforces *scope* and refuses a literal `system:auto` apply, but it does **not** distinguish the agent
   from the human by identity, so **the SKILL itself is the binding control** on self-disposal. This makes
   the never-do list the primary control it actually is, and stops the SKILL resting on a backstop that
   isn't there.
2. **Correct s6 §3 step 7, §5.1, and §0** to state that approve has *no* server actor check and apply's
   check is the narrow `system:auto` string match — i.e. the "control is absolute at the durable boundary"
   claim is true *only if the SKILL holds*, not because the core enforces it.
3. **Upgrade R3 → a routed s9 hardening item:** the durable gates need a real human-vs-agent identity
   signal (e.g. a distinct human-disposal scope or an actor-class the agent provably cannot assert) if
   server-side enforcement is to match the SKILL's claim. This is core work, correctly out of s6's
   *interaction-design* scope, but it must be named as the gap that makes the SKILL the sole control today.

**Verdict, line #1: FLAG → BLOCKING correction F-CRIT-1.** The boundary is *designed* correctly but
*justified* falsely; the SKILL is currently the only real control and must say so.

---

## 2. Line of attack #2 — is the overlay actually low-friction + accessible?

### 2.1 Low-friction: largely yes, with one honest soft spot

- **Strong.** Same-origin in-page annotation removes the typed-selector jargon (root-cause #4) at one
  gesture; co-locating note + render + gate in one page removes the channel-switch the tournament rejected A
  for; the disabled-with-reason mirror of INV-2 avoids a failed round-trip. These are real friction wins and
  are correctly classed `human_study` (the gain) + `soft_flag`/`hard_gate` (only the *shape*).
- **Soft spot (already flagged, under-weighted).** Step 2's friction win is conditioned "**only if the page
  shows progress**," and the "generating…" state is asserted but not specified (no failure/timeout branch
  for a generation that never returns). A cold-start user staring at a stuck "generating…" re-creates
  root-cause #5 (hidden prerequisite chain) in a new form. **Minor** — name a generation-timeout/failure
  state in §5 alongside the other error states.

### 2.2 Accessible: keyboard-native by construction — but the annotation path is the weak link

The gate panel a11y is genuinely strong: native `<button>`s, tab order, `aria-disabled` + associated
reason, `<dialog>` focus-trap for accept. These follow settled WAI-ARIA APG patterns and are correctly
the standards-backed part of the floor.

**The weak link is the keyboard annotation path (§6), and the design both names and under-weights it:**

- It is a **novel interaction pattern** ("Tab moves through annotatable elements … roving-tabindex
  fallback") over a **sandboxed-iframe boundary**, and the design admits (R2) that "iframe↔parent AT
  traversal … is a calibration unknown" and "if same-origin traversal proves brittle for AT, the
  `comment add` fallback is the floor."
- Yet §6 and §0/§8 simultaneously assert the path "keeps C keyboard-native **without** firing G-A11Y."
  **These two statements are in tension.** G-A11Y (s4 §3) is precisely "the *mechanism* by which a
  pointer-first click-to-annotate affordance is given a genuine keyboard/AT-equivalent path … is design
  prior art the run does not currently hold." The design is *building exactly that mechanism* (a
  roving-tabindex element walker over rendered DOM) — it has simply done so from local invention rather
  than from the prior-art pass G-A11Y would have authorized. Calling it "native, so G-A11Y stays unfired"
  conflates *"the gates are keyboard-operable from native HTML"* (true, free, standards-backed) with
  *"click-to-annotate has a validated keyboard equivalent"* (asserted, novel, unvalidated).

### 2.3 Required fix F1

State the a11y floor as **two tiers**, not one:

- **Tier-A (solid, standards-backed):** gate disposal keyboard-operability + `<dialog>` focus-trap +
  disabled-reason association. Hard-gate-eligible after fixture calibration. Keep as-is.
- **Tier-B (provisional, unvalidated):** the keyboard *annotation* path. Reclassify honestly: it is a
  designed-but-unproven pattern whose AT-reachability across the iframe boundary is **a live calibration
  dependency (R2), and `comment add` is the guaranteed AT floor until it is proven.** Either (a) accept
  that designing this pattern locally *is* the G-A11Y work and mark G-A11Y "discharged-by-local-design,
  pending calibration" rather than "unfired," **or** (b) defer the keyboard annotation path to
  `comment add` as the L1 AT floor and mark the in-page keyboard pick as a Tier-B enhancement. Do not claim
  it as a settled native win.

**Verdict, line #2: FLAG → F1.** Friction story is strong; gate-a11y is solid; the annotation-a11y claim
overshoots its own evidence and must be down-graded to provisional.

---

## 3. Line of attack #3 — are UX claims classified correctly?

This is where the design is **strongest**. The s1 rules are: (1) hard gates only for
deterministic/standards-backed failures; (2) cognitive/perception/market claims are never hard gates;
(3) every finding names a `proxy_limit`; (4) no hard gate promotes without fixture calibration; (5)
governance keyboard-first.

**Audit of every ux-evidence row in s6 (§1, §2.3, §3, §4, §5):**

- **Cognitive claims correctly held.** Every comprehension/"felt-connected"/"registered-not-rubber-stamped"/
  paralysis-reduction claim is `human_study` with an explicit `proxy_limit`. The decision-paralysis table
  treats paralysis as a first-class state and still refuses to assert it is reduced (`human_study`,
  "unprovable here"). This is exactly rule 1+2+3 honored. **Pass.**
- **`proxy_limit` discipline.** Every row carries one, including for the `hard_gate` rows ("shape-only;
  says nothing about annotation quality"). **Pass — rule 3 fully honored.**
- **Two rows are mis-scoped or premature (rule 1 / rule 4 violations):**

  | Row | Stated class | Problem | Fix |
  |---|---|---|---|
  | §3 step 4 / §6 a11y.3 — "Choose the option to build … `hard_gate` (keyboard-operable, a11y.3)" | `hard_gate` | The *keyboard-operability* of the button is standards-backed and hard-gate-eligible. But the row is attached to **step 4's disposal semantics**, and the design elsewhere admits a11y.3 is "promotable **after fixture calibration**." Listing it as a flat `hard_gate` in the loop table reads as already-promoted, violating rule 4. | Annotate every a11y `hard_gate` in §3/§6 as **`hard_gate` (pending calibration)** to match §6's own honesty and rule 4. The design says this in prose for a11y.3/.4 but the §3 table cells drop the qualifier. |
  | §2.3 — "The captured `CommentEvent` is contract-identical to `comment add` … `hard_gate` (shape: body validates against `parseAnnotationTarget`)" | `hard_gate` | This is a *contract-shape* check — correctly hard-gate-able. But "contract-identical to `comment add`" is asserted, not verified in s6; and the s6 §0.1 correction shows the contract is *stricter* than s5 thought (selector+elementLabel REQUIRED). The gate is fine; the **"identical" wording** risks a false pass if the page ever emits an odId-only body (which the core would reject). | Keep `hard_gate` but reword the claim to "validates against `parseAnnotationTarget` (selector+elementLabel required, odId nullable — DC-1)," so the gate tests the *real* contract, not an "identical-to-CLI" proxy. |

- **`not_automatable` and `screenshot_review` uses are correct** (engine-purity shape; diff/variant
  salience). **Pass.**

### 3.1 Required fix F2

Add the **"(pending calibration)"** qualifier to every a11y `hard_gate` cell in the §3 loop table and §6
(to match the design's own prose and s1 rule 4), and reword the §2.3 contract gate to test
`parseAnnotationTarget` directly per DC-1 rather than "identical to `comment add`."

**Verdict, line #3: PASS with F2.** Classification discipline is the design's best feature — cognitive
claims are never gated, every row has a proxy_limit. The only defects are two over-promoted hard-gate
labels, both fixable by adopting the design's *own* calibration caveat consistently.

---

## 4. Line of attack #4 — does it address the cold-start findings?

The cold-start table (s1 §4) has 8 ranked frictions and 5 root-causes. Coverage audit:

| Cold-start item (rank/severity) | Addressed in s6? | Where |
|---|---|---|
| #2 Choose option — "Baseline" jargon, not clickable (**Critical**) | **Yes** | §3 step 4 relabel "the option you chose"; clickable variant |
| #3 Apply change — hidden 3-step ritual, no visual proof landed (**High**) | **Yes** | §3 steps 6/9/11 co-located; §4 honest diff; §5 history with summary |
| #4 Annotate — selector/OD-ID jargon, no click-to-annotate (**High**) | **Yes** | §2.2 in-page click-to-annotate; the central win |
| #5 Generate — hidden prerequisite chain (**High**) | **Partial** | §3 step 2 "generating…" state — but no failure/timeout branch (§2.1 above) |
| #6 Handoff — no visible deliverable (**Medium**) | **Yes** | §3 step 12 "visible, openable deliverable" |
| #7 History — IDs + unlabeled diff, no timestamps (**Medium**) | **Yes** | §3 step 11; §5 E-EMPTY-4 |
| #8 Pervasive machine-status strings, no glossary (**High, cross-cutting**) | **Partial** | §1 header "plain-language state"; §5.3 paralysis; **but glossary owner left to SKILL (ODQ-5 only "partially")** |
| **#1 Identity evidence — no findable/confirmable content (TOP-RANKED Critical)** | **NO — silently dropped** | nowhere |

**The gap: root-cause #1 / friction rank #1 (Identity Evidence) is the highest-severity cold-start finding
and it appears nowhere in the s6 design.** This is *defensible* — s2 §1.1 explicitly scoped the atomic-
design/component-registry/identity-types work OUT (`BLK-IDENTITY-TYPES-002`, L4) — but s6 **never says so**.
A reader of s6 alone cannot tell whether identity-evidence was deliberately deferred or forgotten. The s6
coverage claims (§7, §8 "addresses every cold-start root-cause") are therefore **overstated**: the design
addresses every root-cause *except the top-ranked one*, which it drops without acknowledgement.

### 4.1 Required fix F3

Add an explicit **"cold-start out-of-scope"** note to s6 §7: friction #1 / root-cause "identity evidence"
is deferred with its s2 §1.1 deferral (L4, `BLK-IDENTITY-TYPES-002`), and correct §7/§8 to claim coverage
of *"every cold-start root-cause in scope"* — not "every root-cause." Also resolve the #8 glossary-owner
question (ODQ-5) rather than leaving it "partially" between surface and SKILL: name one owner.

**Verdict, line #4: FLAG → F3.** Six of seven in-scope root-causes are well-addressed; the top-ranked
Critical finding is correctly deferrable but is dropped without acknowledgement, making the coverage claim
false-positive.

---

## 5. Secondary findings (minor — fold opportunistically, not blocking)

- **M1 — Generation timeout/failure state missing** (§2.1): add to §5 error states.
- **M2 — N1 (two-gate apply) honesty is good but asymmetric.** §4.3 is admirably honest that steps 9–10
  are a build dependency, but §3's step-9/10 cells present the two-gate accept as the live design with only
  a "DRIFT" tag. A first-time reader of the loop table could mistake the saw-the-diff accept for a shippable
  capability. Mirror §4.3's "the runnable path is single-gate `batch apply` with no saw-the-diff pause"
  into the step-9/10 table cells.
- **M3 — INV-2 label drift** (already noted in s6 §0.1: spec says `ANNOTATION_GATE_LOCKED`, code throws
  `BASELINE_GATE_UNSATISFIED`). The design uses the code label correctly in §5.1; just ensure the SKILL
  narration teaches the *code* label's plain-language meaning, not the spec label that never fires.
- **M4 — The "ephemeral + local, bound to 127.0.0.1, no auth beyond the scope header" posture (§1, §2.3)
  is the *de facto* security model for the durable gates** given F-CRIT-1. If loopback-only is the real
  control preventing a remote actor from self-approving, that should be stated as a *security boundary*,
  not a casual deployment detail — and the SKILL/plan should forbid exposing the server beyond loopback.

---

## 6. The SKILL draft (Problem B) — reviewed as far as it is legible

**Scope limit (flagged):** the SKILL draft handed to this stage is **truncated** — it ends mid-sentence in
the loop table at step 3. I review only the frontmatter, the posture block, the "when to use," the loop
discipline preamble, and steps 1–3. **§4 (do-list), §4.3 (the never-do spine), §4.4 (narration duty), and
§4.5 (refusal narration) are NOT in the provided text and are therefore UNREVIEWED.** s9/the SKILL author
must not treat this stage as having validated the never-do list.

What is visible:

- **F-CRIT-1 hits the description and posture directly** (§1 above): *"refused server-side"* and *"enforced
  in the core — not in CLI flags"* are both in the visible text and both are the false-backstop claim. This
  is the priority fix.
- **Strong, keep:** "you propose, the human disposes at every durable gate"; "a CLI flag is input, not
  authority"; the explicit "do not use this skill to … stand up your own server, or make any change the
  core has not validated"; the graceful "if the human asks for a one-off raw HTML file … offer it plainly
  rather than forcing it through the gates." These are exactly the cooperative-engine framing s2 §4.1 asked
  for.
- **Gap to check when the full draft is available:** s2 §4.5 requires the SKILL to (a) *narrate refusals*
  ("explain the boundary, not silently fail") and (b) carry the **two-layer scoping rule (§5.4)** — teach
  only the runnable X2 subset, reference `accept`/`preview` as build-dependent. Neither is in the visible
  text. Confirm both are present before the SKILL is promoted; if absent, that is an additional required
  fix.
- **DC-1 must reach the SKILL:** the SKILL's generation discipline must state that every emitted annotation
  target carries selector + elementLabel (odId nullable), because the core *rejects* an odId-only body. The
  visible draft does not reach the do-list, so this is unverified — flag for the full review.

**Verdict, §6: cannot fully validate (truncated). The visible text carries F-CRIT-1. The never-do spine,
narration duty, scoping rule, and DC-1 propagation are UNREVIEWED and must be checked at full-draft.**

---

## 7. Verdict summary + required fixes

| Line of attack | Verdict | Finding |
|---|---|---|
| #1 who-leads-when / self-approve | **FLAG → BLOCKING** | **F-CRIT-1** — "refused server-side" is false; core does not distinguish agent from human at approve (no check) or apply (only literal `system:auto`); the SKILL is the *sole* control and must say so |
| #2 low-friction + accessible | **FLAG** | **F1** — keyboard *annotation* path is novel + iframe-AT-unvalidated; "keeps G-A11Y unfired" overshoots; down-grade to provisional, `comment add` as the AT floor |
| #3 UX claim classification | **PASS w/ fix** | **F2** — cognitive claims correctly held as human_study (best feature); two a11y hard_gate cells need the "(pending calibration)" qualifier the design already uses in prose; §2.3 gate should test `parseAnnotationTarget` per DC-1 |
| #4 cold-start coverage | **FLAG** | **F3** — top-ranked Critical (identity evidence, #1) dropped without acknowledgement; coverage claim overstated; name the glossary owner (ODQ-5) |
| §6 SKILL draft | **INCOMPLETE** | truncated; carries F-CRIT-1; never-do spine + narration + scoping + DC-1 UNREVIEWED |

### Required fixes (gating s8/s9)

1. **F-CRIT-1 (BLOCKING).** Rewrite the SKILL description/posture and s6 §0/§3-step7/§5.1 to stop claiming
   "refused server-side." State honestly: scope is enforced; identity is not; **the SKILL's never-do
   discipline is the binding control** on self-disposal; route the "real human-vs-agent gate" gap to s9 as
   core hardening (R3 upgraded).
2. **F1.** Re-tier the a11y floor: gate-disposal a11y = solid/standards-backed; keyboard-*annotation* path =
   provisional, iframe-AT-unvalidated (R2), `comment add` is the L1 AT floor; reconcile the "G-A11Y unfired"
   claim with the fact the design *is* building the G-A11Y mechanism.
3. **F2.** Add "(pending calibration)" to every a11y hard_gate cell; reword the §2.3 contract gate to test
   `parseAnnotationTarget` (DC-1) directly.
4. **F3.** Add the explicit cold-start-out-of-scope note for friction #1 (identity evidence, L4 deferral);
   correct the "every root-cause" coverage claim to "every in-scope root-cause"; assign the glossary owner.

### Recommended (non-gating)

M1 (generation-timeout state), M2 (mirror N1 single-gate honesty into the step-9/10 table cells), M3
(SKILL teaches the *code* gate label), M4 (state loopback-only as a security boundary, forbid exposure).

---

## 8. Residue handed forward

- **R-S7-1 → s9 (core hardening).** Durable gates need a real human-vs-agent identity signal; today scope +
  a `system:auto` string match is the only server check and the SKILL is the de-facto control. (Upgrades
  s6 R3.)
- **R-S7-2 → s8 (toy-game).** The keyboard-annotation-over-iframe AT-reachability is the calibration the
  toy-game should prioritize, since the whole "keyboard-native" claim rests on it (F1/R2).
- **R-S7-3 → SKILL author.** Full-draft review still owed: never-do spine, refusal narration, two-layer
  scoping rule, DC-1 propagation — none were legible in the truncated draft.
- **R-S7-4 → s6 author.** The "addresses every cold-start root-cause" claim must be narrowed to in-scope;
  identity-evidence (#1) deferral must be made explicit.

**Status:** `flag` — design is sound and honestly classified, but ships one BLOCKING correction (the
"refused server-side" overclaim that misstates the SKILL's own authority) plus three required fixes before
s8/s9. **Emits:** `review.design = FLAG with F-CRIT-1 (blocking) + F1/F2/F3 (required) + M1–M4
(recommended); SKILL never-do spine UNREVIEWED (truncated draft).**
