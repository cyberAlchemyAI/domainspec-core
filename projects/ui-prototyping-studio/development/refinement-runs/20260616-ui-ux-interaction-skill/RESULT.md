---
id: result-ui-ux-interaction-skill
project: ui-prototyping-studio
title: "RESULT (s10) — Final Synthesis: the ui-prototyping-studio interaction surface + operating SKILL"
status: flag
node_type: refinement-result
run_id: 20260616-ui-ux-interaction-skill
dispatch_id: refine-ups-ui-ux-skill-20260616
step_id: s10-interrogation-synthesis
capability_ref: refine
consumes: [decision.surface, design.interaction, review.design, walkthrough.toy-game, plan.build, skill.draft]
emits: result.refinement
updatedAt: 2026-06-16
---

# RESULT — ui-prototyping-studio interaction surface + operating SKILL

This run answered two coupled questions for the ui-prototyping-studio: **what review surface should a cold-start human use to dispose of agent-generated UI variants**, and **what operating SKILL binds Claude Code as the propose-only engine behind it**. The answer is decided and code-grounded for the surface and the loop; it ships **one BLOCKING correction** (a false authority claim in the SKILL) plus three required fixes, and it carries an **unproven ergonomics floor** as honest residue. Overall status: **FLAG** — sound and buildable, not clean-pass.

## 1. The chosen interaction surface (one sentence)

**Build surface C: one same-origin local web review page** — the existing Fastify app gains exactly one new read-only `text/html` render route, and serves a static, no-build page with three regions (≤3 sandboxed-iframe variant renders side-by-side, co-located notes, and a five-gate disposition panel that renders session state as sentences with each gate's enabled/disabled reason in words), with in-page click-to-annotate composing and POSTing the existing `CommentEvent` contract; surface A's in-DOM `data-od-id` capture is preserved as a **named deferred upgrade**, and surface B (terminal/TUI) is **eliminated**.

## 2. Key decisions

### 2.1 Surface (ODQ-1, owned by s5) — DECIDED
- **C selected via Pareto + first-principle tie-break.** B is *dominated* by C on the two axes that ARE the cold-start problem — C3 friction (B cannot render HTML; it offloads preview to a browser tab) and C4 annotation (B picks an id by recall-from-a-list, not by pointing) — and B's only edge (C5 build cost) is marginal because C5 is already cheap. A and C are *both* Pareto-non-dominated on the raw vectors; the tie broke to C because (i) the two axes A wins (C3, C4) are the two the run can most afford to defer, while the two C wins (C1 who-leads-when, C5 build cost) are the two it cannot; (ii) A fails the fixed obligation `a11y.3` (keyboard-operable disposal) *as designed* while C gets it free from native HTML; (iii) A re-opens root-cause #3 (note disconnected from disposition) unless it also hosts the gates.
- **The disputed build-cost claim was verified against runnable code, not the advocate briefs.** C's most expensive component — the ephemeral server + JSON API + content store — **already exists and runs**; C's only new server work is one GET that calls the existing `readHtml(ref)` (`file-artifact-content-store.ts:50`). There is no `text/html` route today (14 JSON routes only). A, by contrast, is unbuilt from zero (no `preview` command exists in `studio.ts`).
- **The recorded decision `DEC-INPROTO-ANNOTATION-013` (which presumed A) was sequenced, not overturned:** it fixes the annotation *intent/contract* (capture a stable target by pointing), which C satisfies via the identical `CommentEvent`; it did not fix build *sequencing*. A's in-DOM capture is folded forward as a costed deferred hook.

### 2.2 Who-leads-when boundaries — DECIDED (the design spine)
The AGENT-AUTONOMY vs HUMAN-CONTROL dialectic resolves to: *autonomy is the default on the reversible arc; control is absolute at the durable boundary; the surface's whole job is to render that handoff legibly.* The 12-step loop partitions cleanly and never puts a gate on a reversible step:
- **6 reversible steps Claude Code may drive:** generate (2), render, capture-compose (5), synthesize (6), propose-mutation (8), plus the stamping/registration arc (1, 3).
- **5 durable/irreversible gates the human alone disposes:** choose baseline (4), approve batch (7), apply (9), accept-diff (10), handoff export (12).
- Claude Code is bound as **propose-only**: it generates → stamps `data-od-id` → registers variants → synthesizes → proposes a mutation (value-in/value-out; core validates and stages), and **NEVER** approves, applies, or accepts.

### 2.3 Overlay / capture mechanics — DECIDED
- One new same-origin `GET …/variants/:label/render` reads staged/committed HTML via `readHtml` into a sandboxed iframe; null-ref returns an honest placeholder document, never a blank iframe or 500.
- In-page, same-origin click-to-annotate composes the capture target and POSTs to the **existing** comments route. Gated server-side by INV-2 (`capture-comment-event.ts:45` throws `BASELINE_GATE_UNSATISFIED` until a baseline is chosen).
- **DC-1 (load-bearing contract constraint):** every capture path — mouse click, keyboard pick, and the `comment add` fallback — MUST emit non-empty `selector` AND non-empty `elementLabel`; `odId` is captured if present else null. Re-verified: `parseAnnotationTarget` (`http-routes.ts:680-695`) hard-requires both via `parseRequiredString`. The page can **never** POST an `odId`-only comment. (This corrects s5's looser "odId may be null / target optional" phrasing.)

### 2.4 The accept-diff UX — DECIDED, with a build-honesty rule
- Accept is a **two-gate, saw-the-diff** sequence: gate-1 stages the candidate and renders the diff inline *without advancing head*; gate-2 is a **focus-trapped `<dialog>` (a11y.4)** showing the honest diff plus "Accept — apply for good" / "Cancel — keep editing", with irreversibility stated in words; Accept POSTs the accepted hash and advances head by exactly one revision (idempotency-at-verdict: a hash mismatch is rejected).
- **The two-gate engine already exists and is unit-tested** (`two-gate-apply.ts`: `validateAndStage` → `acceptStaged`; referenced only by its own test). This is a key sharpening from s9: the accept-diff deliverable is **wiring** (route + CLI + page), *not* engine authoring — lower-risk than s8 implied.
- **Build-honesty rule (blocking-for-honesty):** until the two-gate is wired, the runnable path is single-gate `batch apply` (stages and advances in one call). No control may be labeled "Apply + see the diff" and no SKILL narration may promise a diff-pause until the wiring is verified.

### 2.5 The operating SKILL — DRAFTED, with one blocking correction owed
The SKILL binds Claude Code as the propose-only generation/mutation engine: frontmatter, when-to-use, the loop discipline (generate → stamp → register → synthesize → NEVER dispose), an allowed-vs-forbidden command table grounded in the *runnable* `studio.ts` surface, the propose-a-mutation contract, and the who-leads-when boundary. It honors the two-layer scoping rule (teach only runnable X2 verbs; name target gates as build dependencies) and asserts no ergonomic claims (charter clause 5).

## 3. Residue and open questions (decided-vs-deferred, candidly)

### 3.1 BLOCKING — must be fixed before build (s7 F-CRIT-1)
- **The SKILL's "refused server-side" authority claim is FALSE and must be rewritten.** Code verification shows the durable gates do **not** distinguish Claude Code from the human: the **approve** gate has *zero* actor-class check (`approve-mutation-batch.ts` accepts any non-empty `approvedBy`), and the **apply** gate refuses only the literal lowercased string `system:auto` (`apply-approved-batch.ts:33`) while the route defaults the actor to `"web-ui"` and reads it from the request body. Both share one write scope with the agent's own reversible calls. **The SKILL's own never-do discipline is therefore the SOLE control on self-disposal — the "refused server-side" backstop it cites does not exist.** The boundary is designed correctly but justified falsely in the one place the SKILL claims its authority. Fix: state honestly that scope is enforced, identity is not, and the SKILL is the binding control; route the real human-vs-agent identity gate to core owners.

### 3.2 Required fixes (s7 F1–F3, non-blocking but gating a clean pass)
- **F1 — a11y floor is two-tiered, not one.** Gate-disposal keyboard-operability + `<dialog>` focus-trap + disabled-reason association are solid/standards-backed. The keyboard **annotation** path over the sandboxed-iframe boundary is *novel and unvalidated*; `comment add` is the guaranteed AT floor until an iframe-traversal harness proves it. Do not claim it as a settled native win.
- **F2 — two a11y `hard_gate` cells need the "(pending calibration)" qualifier** the design already uses in prose (s1 rule 4: no hard gate promotes without fixture calibration); reword the contract gate to test `parseAnnotationTarget` directly per DC-1.
- **F3 — cold-start coverage claim is overstated.** Six of seven in-scope root-causes are well-addressed, but the **top-ranked Critical finding (#1 identity evidence)** is silently dropped. It is legitimately out of scope (`BLK-IDENTITY-TYPES-002`, L4), but the design must *say so*; correct "every root-cause" to "every in-scope root-cause" and name the glossary owner (ODQ-5).

### 3.3 The unproven ergonomics floor (ODQ-7, R1) — DEFERRED, by charter
- **No ergonomic gain is asserted anywhere in this run** (charter clause 5). Every cognitive/friction claim (C2, C3, "felt connected", "registered not rubber-stamped", paralysis-reduction) is held as `human_study` with a proxy_limit. The s8 dual walkthrough *prepares* falsification evidence; it does **not** prove the surface is easier. The naive-user voice confirmed it received no internal rationale, but that the surface *reduces* cold-start friction remains unproven until a real cold-start study runs. **This is the run's single largest open epistemic gap and it is deliberately not closed here.**

### 3.4 Carried residue
- **R-S7-1 / R3 (→ core owners):** durable gates need a real human-vs-agent identity signal; today scope + a `system:auto` string match is the only server check. Flagged and routed, not decided (P-c3 in the plan).
- **R-S7-2 / R2 (→ calibration):** the keyboard-annotation-over-iframe AT-reachability harness is UNBUILT; the keyboard-native claim rests on it.
- **R-S7-3 (→ SKILL author):** the SKILL draft handed to s7 review was truncated — the never-do spine, refusal narration, two-layer scoping rule, and DC-1 propagation were UNREVIEWED and must be checked at full draft.
- **G-A11Y stays UNFIRED** — it arms only if the deferred cross-origin A-upgrade (in-DOM `data-od-id` capture) is pulled.
- **M1–M4 (recommended, non-gating):** generation-timeout state; mirror single-gate honesty into the step-9/10 table cells; teach the *code* gate label (`BASELINE_GATE_UNSATISFIED`, not the spec's `ANNOTATION_GATE_LOCKED`); state loopback-only as a security boundary and forbid exposure.

## 4. Decided vs deferred — at a glance

| Item | Status |
|---|---|
| Surface = C (local web page); B eliminated; A deferred | **DECIDED** (code-verified) |
| Who-leads-when 12-step partition (6 reversible / 5 durable) | **DECIDED** |
| Overlay mechanics (one render GET + same-origin click-to-annotate + DC-1) | **DECIDED** (code-verified) |
| Accept-diff = two-gate saw-the-diff; engine EXISTS, needs wiring | **DECIDED** (re-scoped to wiring) |
| SKILL propose-only contract + command table | **DRAFTED** — blocked on F-CRIT-1 rewrite |
| "Refused server-side" authority claim | **FALSE — must be corrected before build** |
| a11y annotation path keyboard/AT equivalence | **DEFERRED** (Tier-B; `comment add` is the floor) |
| Core human-vs-agent identity gate | **DEFERRED** (routed to core owners) |
| Ergonomic gain (ODQ-7) | **DEFERRED** (unproven by charter; the floor is open) |
| Cold-start root-cause #1 (identity evidence) | **OUT OF SCOPE** (L4) — must be stated explicitly |

## 5. Recommended next routes

1. **domainspec-subagents-strategy REVIEW (the operator's requested next step).** Route the SKILL draft + this design through a `dispatch_type: review` red-team before building. The blocking F-CRIT-1 correction (the "refused server-side" overclaim) is exactly a review-shaped target: the SKILL's load-bearing authority claim is false, and a review dispatch is the right surface to verify the rewrite makes the SKILL honestly the sole control and that the never-do spine (truncated/unreviewed in s7) holds end-to-end. This precedes build.
2. **task-session to build (after review passes).** Execute the s9 non-executed plan as bounded task-sessions in dependency order: (PRE) the shared render GET; (b) `preview --annotate` MWU; (a) the honest-interim SKILL install; (c) wire the existing two-gate engine for accept-diff, shipping the honest single-gate label first; (d) the L1 a11y floor with `comment add` as the AT floor. Each layer maps to a backend CLI verb and/or a served asset over the existing Fastify app, is tagged EXISTS-vs-PROPOSAL, and carries a manual walkthrough + a Playwright check.
3. **Route R-S7-1 / P-c3 to core owners** as a separate decision: a real human-vs-agent identity signal at the durable routes, so the core — not only the SKILL — can refuse agent self-disposal.
4. **(Deferred, do not block build)** a real cold-start ergonomics study to settle the `human_study` claims (ODQ-7 / R1), and the iframe-traversal a11y harness (R-S7-2) to promote the keyboard annotation path from provisional.

## 6. Stop condition

Chosen surface stated in one sentence (§1). Key decisions named with who-leads-when boundaries, overlay mechanics, and accept-diff UX (§2). Residue and open questions named, including the BLOCKING SKILL correction and the unproven ergonomics floor (§3). Decided-vs-deferred made explicit (§4). Next routes recommended, with domainspec-subagents-strategy REVIEW as the operator's requested next step ahead of task-session build (§5). **Status: FLAG** — a sound, code-grounded, honestly-classified outcome that ships one blocking correction and three required fixes before it is built.