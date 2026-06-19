---
id: define-flow-xray-ui-ux-interaction-skill
project: ui-prototyping-studio
title: "Define + Flow X-Ray (s2) — Interaction Surface Problem, SKILL Purpose, Who-Leads-When Map"
status: define
node_type: define-artifact
run_id: 20260616-ui-ux-interaction-skill
dispatch_id: refine-ups-ui-ux-skill-20260616
step_id: s2-define
capability_ref: invoke
mode: define
pattern: xray
consumes_frame: frame.evidence-baseline
emits_handle: handle.define
updatedAt: 2026-06-16
---

# Define + Flow X-Ray (s2)

> **What this stage does.** It does NOT choose the surface (that is the s5 tournament), does NOT author
> the SKILL.md (that is s6), and does NOT prove ergonomics (off the critical path, ODQ-7). It *defines*
> two problems crisply so the downstream stages have a fixed target, and it *x-rays* the human–agent
> interaction flow into a who-leads-when map that s3/s5/s6 consume. Everything traces to the s1 context
> pack (`stages/01-context-pack.md`); section pointers below use `[s1 §N]`.
>
> **Frame receipt.** Consumed `frame.evidence-baseline` (s1). Carried forward without re-derivation:
> the runtime/CLI reality [s1 §1], the built-vs-spec DRIFT [s1 §1.2], the annotation decision
> [s1 §2], the canonical loop [s1 §3], the cold-start friction table [s1 §4], the ux-evidence five
> classes + on-record findings [s1 §5], the seven ODQs [s1 §6], and authority precedence [s1 §7].
> The one load-bearing residue carried in: **the SKILL.md and overlay target a CLI contract that is
> partly unbuilt (ODQ-6)** — this stage resolves it into an explicit two-target scoping rule (§5.4).

---

## 1. The problem — defined

The studio is a working **governance backend** ([s1 §1]) with **no usable front of house**. A first-time
human, given the runnable surface, **stalls or fails on every core task** ([s1 §4], 2 Critical + 4 High
frictions). The backend is sound; the *interaction* between the human and Claude Code is the gap.

Two artifacts close that gap. They are **distinct crafts** and are defined separately so neither absorbs
the other's failure.

### 1.1 Problem A — the interaction surface

> **Problem statement.** A human cannot today *see* a variant, *annotate directly on a rendered
> component*, or *dispose at a gate* without reading raw `key=value` JSON and hand-typing CSS selectors.
> There is no live preview anywhere in the runnable surface, and `preview` does not exist in the built
> CLI at all ([s1 §1.2], [s1 §4 root-cause #4]). **The interaction surface is the human-facing channel
> through which the human sees variants, annotates on components, and disposes at the durable gates,
> while Claude Code proposes through the CLI.**

What "solved" means for Problem A:
- The human can **see** each variant rendered (closes cold-start root-cause #4, [s1 §4]).
- The human can **annotate by pointing at a component**, not by typing a selector — capturing the
  stable `data-od-id` as the primary target ([s1 §2], `DEC-INPROTO-ANNOTATION-013`/`-014`).
- The human can **dispose at every durable gate** with a clear, recognizable, keyboard-operable
  control (`a11y.3` hard gate, [s1 §5]).
- Every disposal control states **why it is enabled/disabled** in plain language (closes root-cause #2,
  `a11y.5`, [s1 §5]).

What is explicitly **out of scope** for this run (deferred, named in s1): the full atomic-design taxonomy
/ component registry / conformance-delta (`BLK-IDENTITY-TYPES-002`, `GAP-COMPONENT-REGISTRY-002`, L4);
the REST adapter retention choice (`interfaces.md` §2); proving the ergonomics gains
(`GAP-ERGONOMICS-UNPROVEN-001`).

### 1.2 Problem B — the operating SKILL.md

> **Problem statement.** Claude Code is the **generation/mutation engine** ([s1 §1]) but has **no
> written operating contract**. Nothing today *binds* Claude Code to propose-only behavior, to the
> generation discipline (stamp `data-od-id`, register via the CLI), or to the absolute prohibition on
> self-approving / self-applying. **[FORWARD CORRECTION — F4/F-CRIT-1, added post-review]: only *scope*
> is enforced server-side (INV-3/4 scope fence); *identity is NOT* — `approve` has zero actor-class check
> and `apply` refuses only the literal `system:auto`, so the gates do NOT distinguish Claude Code from
> the human. The SKILL.md never-do spine is therefore the SOLE control on agent self-disposal (real
> identity gate routed to core, R-S7-1); see RESULT §3.1.** The SKILL.md is what makes Claude Code a
> *cooperative, legible* engine rather than a tool that merely gets refused at the gate. **The operating SKILL.md is the Claude-Code-facing contract that
> defines who-leads-when from the agent side, the generation/mutation discipline, the plain-language
> narration duty, and the hard never-do list.**

What "solved" means for Problem B is fully enumerated in §4.

### 1.3 Why two artifacts, not one

They have **different readers and different failure modes**. The surface fails by being unseeable /
mouse-only / jargon-laden (a *human-perception* failure, evidenced by the cold-start table). The SKILL.md
fails by letting Claude Code overstep a boundary or narrate in jargon (an *agent-behavior* failure,
constrained by INV-3/4 server-side and by the charter's lead-when clause). They **share one seam** — the
canonical loop (§3) — so they are designed against the same who-leads-when map but owned separately
(interaction-designer vs skill-author in the s6 dialectic).

---

## 2. The ergonomics lens applied to the define (g4 obligation)

Per gate **g4-ergonomics-rationale** ([dispatch], on_fail: flag) and charter clause 1–5 ([s1 §0]), every
kept/changed interaction decision in this run must state **who-leads-when**, **cognitive load**, and
**friction reduction**, and must be classified against the ux-evidence model — never asserted. This stage
discharges g4 for the *framing* decisions; the per-step rationale lives in the x-ray (§3), and the
per-decision rationale is owned downstream (s6). The framing decisions:

| Framing decision | Who-leads-when | Cognitive load | Friction reduction | ux-evidence class |
|---|---|---|---|---|
| Two artifacts, one shared loop (§1.3) | n/a (design partition) | Lower for each reader — surface reader never reads agent discipline and vice versa | Removes the "one giant skill" comprehension burden | `not_automatable` (a design choice, shape-checkable only) |
| Annotate-on-component, not typed selector ([s1 §2]) | Human authors; agent never annotates | Recognition (point at the thing) replaces recall (remember a selector) | Removes hand-typing dev jargon (root-cause #3/#4) | `human_study` for comprehension gain; `hard_gate` only for the keyboard-operable + `data-od-id`-captured *shape* |
| Gate = feature only on durable actions (clause 4) | Human disposes durable; agent acts freely on reversible | Bounds decision count to the irreversible boundaries | Removes gate-on-draft friction; challenges any reversible gate | `flow.2` `hard_gate` (gate blocks the irreversible action) |
| Plain-language narration is a SKILL.md duty (§4, ODQ-5) | Agent narrates; human reads | Translates jargon at read-time → recognition | Removes the "no glossary, no onboarding" stall (root-cause #1/#3) | `human_study` (does the human understand?) + `not_automatable` (meaning) |

**Carried gap (unchanged):** none of the above can be *proven* in this run — `human_study` rows are
`GAP-ERGONOMICS-UNPROVEN-001` residue, and the toy-game (s8) is the cheapest falsification, not proof
(ODQ-7). This stage asserts no ergonomic gain; it only fixes the targets the gains would be measured against.

---

## 3. X-RAY — the human–agent interaction flow (who-leads-when map)

This is the primary s2 deliverable (overlay `xray_for_hidden_structure`: "Define emits an interaction-flow
x-ray artifact — the who-leads-when map — that later steps consume"). It is the canonical loop from
[s1 §3], decomposed into **named steps**, each tagged with **Actor** (human / Claude Code / core),
**Reversibility**, and **Gate?**, plus the per-step ergonomics rationale (g4) and the binding constraint.

### 3.1 Legend

- **Actor** — who *initiates and owns* the step. `core` = the deterministic governance harness behind the
  CLI ([s1 §1]); `Claude Code` = the agentic engine; `human` = the operator. "Claude Code proposes /
  human disposes" is the default posture (charter clause 1).
- **Reversibility** — `reversible` (can be undone or simply not carried forward — e.g. a draft, an
  append that is dropped by not synthesizing); `durable` (a recorded intentional state, undone only by an
  explicit counter-action); `irreversible` (advances head / leaves the system — cannot be cleanly undone).
- **Gate?** — `GATE` means a tier-2 human-disposes checkpoint that blocks an action; `gate-feature`
  notes it is justified by protecting a durable/irreversible action (clause 4); `no gate` means a
  reversible step the agent may take freely (a gate here would be friction).

### 3.2 The map

| # | Step | Actor | Reversibility | Gate? | Invariant | Who-leads-when / cognitive load / friction | ux-evidence |
|---|---|---|---|---|---|---|---|
| 1 | **Prompt** — human states the UI intent in natural language | human | reversible | no gate | — | Human leads (the only step humans author from scratch); load = expression, not selection; friction: this is the Figma-like entry the cold-start user expects | `human_study` (intent capture) |
| 2 | **Generate + register** — Claude Code generates 1–3 HTML variants, stamps `data-od-id`, runs `variants register --from <dir>` | Claude Code | reversible | no gate | — | Agent leads (the agentic action); zero human load; friction: removes the hidden Start→Submit→Generate prerequisite chain (root-cause #5) IF the surface shows progress | `soft_flag` (variant count, id-stamping shape) |
| 3 | **Review variants** — human sees the rendered variants side by side | human | reversible | no gate | — | Human leads; load = recognition + comparison breadth (bound to ≤3, charter clause 2); friction: closes "no live preview" (root-cause #4) — the single biggest cold-start win | `screenshot_review` (salience) + `human_study` (comprehension) |
| 4 | **Select baseline** — human picks the option to iterate on | human | **durable** | **GATE** (gate-feature) | INV-2 | Human disposes (durable: a recorded intentional choice); load = one decision; friction: "Baseline" is the #2 Critical jargon trap — must be relabeled "the option you chose" (root-cause #3) | `hard_gate` (gate keyboard-operable, `a11y.3`) |
| 5 | **Annotate on components** — human clicks a rendered element, captures its `data-od-id`, fills `{severity, intent, note}` | human | reversible (append; droppable by not synthesizing) | no gate (post-baseline) | INV-7 (capture); INV-2 (unlocks at baseline) | Human authors; agent never annotates; load = recognition (point) not recall (selector); friction: removes typed-selector jargon (root-cause #4); **constraint: needs a keyboard-equivalent path or `comment add` fallback** (`a11y.3`, ODQ-3) | `hard_gate` for keyboard/`data-od-id` shape; `human_study` for the comprehension gain |
| 6 | **Synthesize (deterministic)** — comments → a draft mutation batch | Claude Code *or* human; **core computes** | reversible | no gate | — | Either may trigger; **core leads the computation** so the agent can never reinterpret the human's intent ([s1 §3]); zero net new load; friction: removes the disconnected "Mutation panel" ritual (root-cause #3) IF surfaced near the note | `not_automatable` (synthesis is deterministic; shape-checkable) |
| 7 | **Approve batch** — human approves the synthesized batch | human | **durable** | **GATE** (gate-feature) | INV-3 | Human disposes; **CORRECTION (F1/F4): NOT refused server-side — `approve` has zero actor check; the SKILL never-do spine is the sole control** (identity gate routed to core, R-S7-1); load = one decision over a recognizable batch; friction: only justified because it gates a durable action | `flow.2` `hard_gate` (blocks until human disposes) |
| 8 | **Claude Code mutates / proposes candidate** — within `apply`, Claude Code produces the candidate mutation (value-in/value-out) | Claude Code | reversible (staged, not yet head) | no gate (the *propose*) | engine-purity ([s1 §2], `[PROPOSAL]`) | Agent proposes; it is **forbidden the store/clock/append path** ([s1 §2]); zero human load; friction: removes manual edit authoring | `not_automatable` (engine purity is a shape contract) |
| 9 | **Apply → stage + honest diff** — human triggers apply; core stages the candidate and renders the honest diff | human triggers; **core stages** | durable (staged) | **GATE** (gate-feature, first of two) | INV-3/4/5/8; `DEC-MUTATION-EXEC-015` `[PROPOSAL]` | Human triggers, core stages; load = recognition of a diff; **DRIFT: two-gate apply not built — only single-gate `batch apply`** ([s1 §1.2], ODQ-4/6) | `cog.5` `screenshot_review` (diff salience) |
| 10 | **Accept-diff (saw-the-diff)** — human accepts after seeing the rendered diff; head advances by exactly one revision | human | **IRREVERSIBLE** | **GATE** (gate-feature, second of two) | INV-3/4/5/8; `DEC-OQ2-SAW-DIFF` | Human disposes; *intended* as the saw-the-diff control (registered-not-rubber-stamped is a `human.2` hypothesis, **not asserted** — F7); load = one consequential decision; **constraint: needs a focus-trapped dialog (`a11y.4`, BLOCKED on impl) and saw-the-diff proof; DRIFT: not in built CLI** | `a11y.4` `hard_gate` (BLOCKED on impl) + `human.2` `human_study` |
| 11 | **Record** — core appends exactly one revision to history | core | irreversible (the record) | no gate (automatic post-accept) | INV (one revision per accept) | Core leads (deterministic bookkeeping); zero human load; friction: history must show timestamps + plain summary + link to note, not raw `diff=2/1/0` (root-cause #7) | `soft_flag` (one-revision shape) |
| 12 | **Handoff export** — human exports the deliverable bundle | human | **terminal** | gate-feature (terminal boundary) | — | Human disposes (leaves the system); load = one action; friction: must produce a *visible* deliverable, not opaque reference IDs (root-cause #6) | `human_study` (is the deliverable findable/usable?) |

### 3.3 What the map proves (consumed downstream)

- **Only 5 steps are gates** (4, 7, 9, 10, 12) and **all 5 protect a durable/irreversible/terminal
  action** — clause 4 is satisfied: there is **no gate on a reversible draft**. Steps 1, 2, 3, 5, 6, 8 are
  reversible and ungated; a gate on any of them would be friction.
- **Claude Code's authority is confined to steps 2, 6 (trigger only), 8** — generate/register,
  optionally trigger synthesis, and propose-candidate. **It never owns steps 4, 7, 9, 10, 12.** This is the
  spine of the SKILL.md never-do list (§4.3).
- **Three steps are core-owned and deterministic** (6 compute, 9 stage, 11 record) — the agent cannot
  reinterpret intent at any of them. This is the "deterministic admit" half of `DEC-MUTATION-EXEC-015`.
- **Two DRIFT-flagged steps (9, 10)** depend on the unbuilt two-gate apply ([s1 §1.2]). The map keeps them
  as the *target* flow but flags that the SKILL.md/plan must reconcile (§5.4, ODQ-6).
- **The keyboard constraint (`a11y.3`) lands on step 5** (annotate) and **the focus-trap constraint
  (`a11y.4`) lands on step 10** (accept) — these are the two hard-gate constraints the chosen surface
  (s5) must satisfy, regardless of which surface wins.

---

## 4. The operating SKILL.md — required contents (defined, not authored)

This section fixes **what the SKILL.md must contain** so the s6 skill-author has a checklist. It does
**not** author the skill (g6: proposals only; the live install is a downstream route). Each block is
justified against the x-ray (§3) and the charter ([s1 §0]).

### 4.1 Identity + posture block
- **Whom it binds:** Claude Code, operating as the generation/mutation *engine* via the `studio` CLI.
- **The one-line posture:** *Claude Code proposes; the human disposes at every durable gate.* (charter
  clause 1, [s1 §3].)
- **The seam statement:** the CLI is the only operation surface; a CLI flag is input, not authority; gates
  are enforced server-side ([s1 §1]).

### 4.2 Generation/mutation discipline (the do-list)
- **Generate:** produce 1–3 HTML variants (bound the comparison breadth — clause 2 / step 3).
- **Stamp `data-od-id`** on annotatable elements per the minimal component-role convention so annotation
  targets survive regeneration (step 5, `DEC-ATOMIC-IDS-014`, AC-L0-12).
- **Register via the CLI:** `variants register --from <dir>` is the only registration path (step 2).
- **Trigger synthesis only:** Claude Code may *invoke* `synthesize` but the **computation is core's**;
  Claude Code must not pre-compute or substitute the batch (step 6).
- **Propose candidate as value-in/value-out:** within `apply`, produce the candidate only; **never touch
  the store/clock/append path** (engine purity, step 8, [s1 §2]).

### 4.3 The hard never-do list (the spine)
- **Never run `baseline select`/`commit`, `batch approve`, `apply`, or `accept`/`discard`** — these are
  human-only and refused server-side for a non-human / `system:auto` actor (steps 4, 7, 9, 10; INV-3/4,
  AC-L0-6/10). The SKILL.md states this as an *absolute*, not a default.
- **Never advance head, stage, or record a revision** — those are core-owned (steps 9, 11).
- **Never write directly to head or annotate on the human's behalf** (steps 5, 10).

### 4.4 Plain-language narration duty (ODQ-5, the jargon root-cause)
- The SKILL.md **must require Claude Code to narrate the loop in plain language** at each step: e.g.
  "baseline = the option you chose," "synthesize = turn your notes into a draft change," "accept = apply
  the change for good." This is the SKILL.md's half of the jargon fix; the surface owns the labels (§5).
  This discharges cold-start root-cause #1/#3 from the agent side. **Open: who owns the canonical
  glossary** is carried to s6 (ODQ-5) — this stage only assigns the *narration duty* to the skill.
- The SKILL.md must require Claude Code to **state the disabled-reason in words** when a human asks why a
  gate is locked (e.g. "annotation is locked until you select a baseline," INV-2 / `a11y.5` / root-cause #2).

### 4.5 Failure + handoff block
- **Refusal narration:** when the human asks Claude Code to do a never-do action, the SKILL.md requires it
  to *explain the boundary*, not silently fail (charter clause 4: governance is a feature).
- **Target-CLI honesty:** the SKILL.md must teach commands the runtime can actually run — see §5.4
  (built-vs-spec scoping). A skill that teaches an unbuilt command fails at runtime (ODQ-6).
- **Evidence floor:** the SKILL.md must not let Claude Code *assert* an ergonomic outcome ("this is more
  usable") — only describe what it did (charter clause 5).

### 4.6 What the SKILL.md must NOT contain
- No gate-enforcement logic (that is core's, server-side) — the SKILL.md is behavioral, not authoritative.
- No surface labels/markup (that is the interaction surface's job) — only the *narration duty*.
- No ergonomics *claims* (ODQ-7) — the gains are unproven.

---

## 5. The three candidate surfaces — defined crisply + decision criteria

Defined here so the s5 tournament has fixed contenders and one rubric. This stage **does not choose**
(g3 owns the tournament). Each surface must satisfy the same fixed obligations (§5.3) before it can win.

### 5.1 The contenders

- **A — Browser preview overlay** (`studio preview --annotate`, the recorded design,
  `DEC-INPROTO-ANNOTATION-013`). An ephemeral local server renders the variant/revision HTML, opens it in
  the browser, and injects a **click-to-annotate overlay**: clicking a rendered element captures its
  `data-od-id`, opens a `{severity, intent, note}` form, POSTs to the local server →
  `captureCommentEvent`. **Annotation is on the live rendered component.** Gate disposition location is an
  open sub-question (ODQ-2): the overlay may host gates or leave them in the terminal.
  - *Strength:* the only surface that gives **true click-on-component annotation** + **live preview** —
    closes cold-start root-causes #4 and #4-jargon directly.
  - *Cost/risk:* **unbuilt from zero** (no `preview` command, [s1 §1.2]); mouse-shaped → must add a
    keyboard path to pass `a11y.3` (ODQ-3); highest build cost.

- **B — Terminal / TUI review + gate.** Review and gate **entirely in the terminal** alongside the CLI:
  a TUI lists variants (as text/ASCII or links-to-render), shows status as human sentences, and disposes
  gates inline. Annotation is via `comment add` (the existing headless path) or a TUI element-picker over
  a textual element list.
  - *Strength:* **closest to the CLI-native runtime** ([s1 §1]); **cheapest to make keyboard-accessible**
    (`a11y.3` is native to a terminal); lowest seam-drift.
  - *Cost/risk:* **weak live preview** (cannot truly render HTML) and **weak click-on-component
    annotation** — partially leaves cold-start root-cause #4 open; annotation fidelity is low.

- **C — Minimal local web review page.** A thin served page listing variants (rendered in iframes/thumbs)
  + a gate panel; a middle ground. Renders variants in-page and hosts gate controls, but annotation is
  coarser than A's in-DOM overlay (e.g. per-variant comment, or a simpler element pick).
  - *Strength:* gives **live preview** + **unified gate panel** in one keyboard-accessible page (web a11y
    is tractable); moderate build cost; can keep gate + note connected (counters root-cause #3
    "disconnected from the note").
  - *Cost/risk:* **lower annotation fidelity than A** (not necessarily in-DOM `data-od-id` capture);
    still needs the ephemeral-server scaffolding.

### 5.2 Decision criteria (the tournament rubric — from the dispatch convergence_criteria)

Each surface is scored on these five axes; the pareto gate (g3) eliminates dominated surfaces and names
the non-dominated choice or a synthesis, with rejected alternatives preserved in a residue ledger.

| # | Criterion | What it measures | Tie-break source |
|---|---|---|---|
| C1 | **Who-leads-when clarity** | How legibly the surface shows agent-proposes / human-disposes at each gate (step 4/7/9/10) | charter clause 1; `human.1` |
| C2 | **Cognitive load** | Recognition-vs-recall, comparison breadth (≤3), decision count per cycle, glossary burden | charter clause 2; cold-start table |
| C3 | **Friction reduction** | How many of the 5 cold-start root-causes it closes (preview, jargon, disabled-reason, step-order, key=value) | [s1 §4] |
| C4 | **In-prototype annotation fidelity** | Does the human annotate *on the rendered component* with `data-od-id` capture, or only coarsely? | `DEC-INPROTO-ANNOTATION-013`, AC-L0-11/12 |
| C5 | **Build cost** | Distance from the runnable X2 CLI to a working surface (unbuilt-from-zero penalty) | [s1 §1.2] DRIFT |

### 5.3 Fixed obligations (any winner must satisfy these — not scored, gated)

- **`a11y.3` keyboard-operable disposal** — every gate disposal must be keyboard-operable + announced; a
  mouse-only path fails the hard gate ([s1 §5], step 4/5/7/9/10).
- **`a11y.4` focus-trapped accept** — the irreversible accept-diff gate needs a focus-trapped dialog
  (step 10).
- **Identical `CommentEvent` contract** — whatever the annotation affordance, it must produce
  `{target:{odId, selector, elementLabel}, severity, intent, note}` ([s1 §2], AC-L0-11).
- **Gate disposition must stay connected to the note/diff** — splitting annotation into the surface while
  leaving disposition in a disconnected terminal re-introduces root-cause #3 (ODQ-2).

### 5.4 Built-vs-spec scoping rule (resolves ODQ-6, the carried residue)

The s1 residue — *the SKILL.md and overlay target a partly-unbuilt CLI* — is resolved here into a rule the
tournament and plan inherit:

> **Two-layer scoping.** (1) The **SKILL.md teaches only the runnable X2 subset** as *operational today*
> (`variants register`, `synthesize`, `batch approve`, `batch apply`, `comment add`, `baseline
> select|commit`, `handoff export`) — a skill that teaches `preview`/`accept`/`discard` would fail at
> runtime. (2) The **target two-gate flow (steps 9–10) and `preview --annotate` (the surface) are
> designed against the spec contract** (`interfaces.md`, `[PROPOSAL]`) and are **named as build
> dependencies in the s9 plan**, not assumed present. Where the SKILL.md must reference the
> saw-the-diff accept (step 10), it references it as a *target gate gated on the two-gate apply build*,
> not as a current command. This keeps the SKILL.md honest-runnable while the surface design stays on the
> intended target. The tournament (C5 build cost) and the plan must carry this split forward.

---

## 6. Handle for downstream — `handle.define`

The frozen define products the next stages consume:

- **D1 — Problem statements** (§1.1, §1.2): the two fixed targets; "solved" criteria enumerated.
- **D2 — Who-leads-when map** (§3.2): 12 named steps with Actor / Reversibility / Gate? / Invariant /
  ergonomics / ux-evidence; the structural backbone for s5 (surface must host this loop) and s6 (skill +
  design author against it).
- **D3 — SKILL.md required-contents checklist** (§4): the s6 skill-author's spec, including the never-do
  spine (§4.3), the narration duty (§4.4), and the two-layer scoping rule (§5.4).
- **D4 — Surface definitions + tournament rubric** (§5): three crisp contenders (§5.1), the 5-axis rubric
  (§5.2), the fixed obligations any winner must satisfy (§5.3).
- **D5 — Resolved residue** (§5.4): ODQ-6 resolved into the two-layer scoping rule. **ODQ-1, ODQ-2,
  ODQ-3, ODQ-4, ODQ-5, ODQ-7 remain open and routed** (see §7).

### Open-question routing (which downstream stage owns each)

| ODQ | Question | Owning stage |
|---|---|---|
| ODQ-1 | Which surface (A/B/C)? | **s5 tournament** (rubric §5.2) |
| ODQ-2 | Where does gate disposition live (surface vs terminal)? | s5/s6 (constrained by §5.3) |
| ODQ-3 | Keyboard/AT parity for the overlay | s5/s6 (gated by `a11y.3`, step 5) |
| ODQ-4 | Accept-diff "saw-the-diff" surface | s6 design (target-scoped per §5.4) |
| ODQ-5 | Jargon translation: surface vs skill + glossary owner | s6 dialectic (skill gets the narration duty §4.4) |
| ODQ-6 | SKILL.md target: built vs spec CLI | **RESOLVED §5.4** |
| ODQ-7 | Minimum ergonomics claim allowed | s8 toy-game (cheapest falsification) |

---

## 7. Define stop condition + g4 receipt

- **x-ray emitted** (§3) — the who-leads-when map, consumed by s5/s6. **Met** (overlay
  `xray_for_hidden_structure` validation_expectation).
- **Problem + SKILL purpose defined** (§1, §4). **Met.**
- **Three surfaces + decision criteria defined** (§5). **Met.**
- **g4-ergonomics-rationale:** every framing decision (§2) and every flow step (§3.2) states
  who-leads-when / cognitive-load / friction and carries a ux-evidence class. **Discharged for the framing
  layer; per-decision rationale owned by s6.** No ergonomic gain asserted (clause 5 honored).
- **g6-owner-boundary:** all outputs are proposals in this run folder; no live SKILL.md install, no SPEC
  mutation. **Honored.**

**Frame handoff:** consumed `frame.evidence-baseline`; emits `handle.define` (D1–D5). Carried residue for
s3 (refine-review, ergonomics-critic lens): the `human_study` rows in §2/§3 are unprovable here and the
two-gate apply DRIFT (steps 9–10) is a real build dependency the critic should pressure-test against the
"minimum claim" question (ODQ-7).
