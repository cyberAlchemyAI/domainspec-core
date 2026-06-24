---
tags: [ide, product, arcanum, unified-spine, research, collected-returns]
node_type: research
is_session: false
layer: product
nature: collected-returns
status: draft
created: 2026-06-24
---

# Research: Collected Explorer Returns (verbatim)

Dispatch `2026-06-24-unified-ide-ergonomics-product-view`. These are the three
`spine-explorers` returns, preserved **verbatim** as their initial positions —
kept for collapse detection (P14 spirit) and so the synthesis in
[findings.md](findings.md) can be audited against the material it rests on (P9).
Each explorer argued a distinct organizing-spine hypothesis on the declared
`source-corpus × methodology × temporal-prior` composite axis.

---

## E1 — Operator-grammar spine (initial position)

# E1 Brief — The Dispatch Object as the Federation's Spine

## 1. Thesis

The IDE Ergonomics federation reads as eleven loosely related widgets only because its unifying object is implicit. Make it explicit and the federation collapses into one thing: **every card is a partial view onto a single Arcanum dispatch document.** The dispatch object is defined as "the missing middle between poetic operator language and executable sigil sequences" (`ARCANUM-DISPATCH-SYNTHESIS.md:13`), and the product is defined in the exact same negative space — "the missing moment between noticing useful work and safely sending that work to the right place" (`PRODUCT-VIEW.md:17-18`). These are the same gap named twice. The IDE surface is the *human-facing renderer* of the dispatch grammar: each primitive exposes one vocabulary layer (`ARCANUM-DISPATCH-SYNTHESIS.md:19-28`) or one composition-taxonomy entry (`:31-123`), and the product's own five-step path — span → transition candidate → route menu → owner-safe preview → choice → draft/handoff/approved route (`PRODUCT-VIEW.md:129-136`) — is structurally identical to the dispatch lifecycle `intent → capability menu → selected sequence → gated execution → frame handoffs → synthesis → evaluation` (`README.md:28`). The spine is real because both ends were independently designed against the same `route → call → interpret → answer → execute` Weaver lifecycle (`WEAVER-EXTRACTION.md:23`).

## 2. Primitive → Grammar Mapping

| UX primitive (source) | Vocabulary layer (`SYNTHESIS:19-28`) | Composition taxonomy (`SYNTHESIS:31-123`) | Weaver concept (`README:35-46`) |
|---|---|---|---|
| **Transition card** (`PRODUCT-VIEW.md:84-94`) | Operator phrase → structured slots (`SYNTHESIS:208-219`) | the whole dispatch document; `sentence_grammar` technique (`TECHNIQUE-CATALOG.md:28`) | — (it *is* the dispatch) |
| **Route menu** (`PRODUCT-VIEW.md:160-167`) | Route pattern | `route_menu` (`TECHNIQUE-CATALOG.md:29`); bounded 3-7 choices | `ChoiceCard` / `SelectableItem` (`README:37-38`, `WEAVER:43-48`) |
| **Route-ambiguity branch** (`PRODUCT-VIEW.md:191`) | Capability reference (`invoke`/`dispatch-spec`/`task-session`) | — | `RoutingDecision` / `Capability` (`README:39-40`) |
| **Side node** (`ERGONOMICS:96-118`) | Residue | `residue_ledger` / `memory_loop` (`TECHNIQUE-CATALOG.md:27,32`) | `Frame` candidate, no promotion (`WEAVER:65-73`) |
| **Handoff draft / Teammate memo** (`ERGONOMICS:60-94`, `:255-296`) | Frame handoff | `frame_handoff` / `handle_handoff` (`TECHNIQUE-CATALOG.md:30-31`); `delegation_boundary` (`:83`) | `Frame` + `Handle` (`README:43-44`) |
| **Subagent preview** (`ERGONOMICS:120-151`) | Route pattern + Gate | `dialectic`/`tournament`/`fanout`; `subagent_strategy` (`SKILL.md:92-114`) | `CapabilityToken` permission scope (`README:41`) |
| **Knowledge-entry popup / Field hover** (`ERGONOMICS:212-253`, `:397-452`) | Capability reference + Residue | `entity_component_reference` (`TECHNIQUE-CATALOG.md:48`); `memory_promotion_split` (`:117`) | `Handle` to inventory/ontology entry (`WEAVER:77-87`) |
| **Spell/sigil nudge** (`ERGONOMICS:153-171`) | Spell candidate | `spell_candidate` (`TECHNIQUE-CATALOG.md:33`); validation-loop before promotion (`SYNTHESIS:106-113`) | ChainWeaver→Spellcraft graph (`README:46`) |
| **Evidence/receipt rail** (`ERGONOMICS:20`) | Gate + Residue | `observability_grouping` (`TECHNIQUE-CATALOG.md:37`); `execution_receipt_handoff` (`:100`) | `TraceEvent` under `dispatch_id` (`README:45`, `WEAVER:91-97`) |
| **Craft control panel** (`ERGONOMICS:298-345`) | Capability ref + Gate | `scu_swu_reduction` (`TECHNIQUE-CATALOG.md:23`); route to interrogation/decision-gate/refine | `Frame` read-model + `PolicyDecision` (`README:42-43`) |
| **Connective task manager** (`ERGONOMICS:347-396`) | Gate (Pareto) | `pareto_gate` + `tournament` over lanes (`TECHNIQUE-CATALOG.md:34`, `SYNTHESIS:64-73`) | `PolicyDecision` allow/defer/block (`README:42`) |
| **Intent-latitude tag** (`ERGONOMICS:173-211`) | Operator phrase (input-side) | `sentence_grammar` slot annotation; gate via post-hoc validator | `PolicyDecision` (literal/goal/constraint) |
| **Self-assembling action** (`ERGONOMICS:454-498`) | Spell candidate + Gate | `validation_loop` + `toy_game` (`SYNTHESIS:95-113`); frozen criterion | full ChainWeaver DAG, human-gated (`README:46`) |

Every primitive lands on exactly one vocabulary layer and one (sometimes two) taxonomy entries — none is orphaned, which is itself the `orphan_record_check` passing (`TECHNIQUE-CATALOG.md:69`).

## 3. What the IDE Surface Exposes

The IDE exposes the **dispatch document under construction**, rendered layer-by-layer as the conversation produces material:

- The **transition card is the dispatch's `intent` block** being authored live — raw span preserved beside structured slots (`SYNTHESIS:208-219`).
- The **route menu is the `ChoiceCard`** — bounded 3-7 capability cards, *not* full schema injection (`WEAVER:43-48`, invariant `:115`).
- The **owner-safe preview is the `Frame`/`gate` pair**: every option names owner, artifact preview, permission state, blocked actions (`PRODUCT-VIEW.md:160-167`) — the product's four boundary questions (`:85-87`) are exactly dispatch rules 9/20 (no false promotion authority, `SKILL.md:74,85`).
- The **side rail is the `observability`+`residue` layer**: receipts grouped by one `dispatch_id` (`WEAVER:91-97`), gaps and rejected candidates kept as ledgers (`SYNTHESIS:334`).
- **Connective is the dispatch-level `pareto_gate`** rendered as ranked lanes with reasons and expected receipts (`ERGONOMICS:372-373`).

Why this is *the* spine and not just a metaphor: the dispatch object is the only artifact in the system that already carries all five things every card needs — owner, frame handoff, gate, residue, and a `dispatch_id` to tie siblings together. The cards don't each need their own data model; they each need one *projection* of the dispatch document. That is what makes federation→unification real rather than cosmetic.

## 4. Residue / Risks (my weak point)

- **Exposing grammar can overwhelm the user — my strongest counter-evidence.** The Weaver invariant "routing does not require full schema injection" (`WEAVER:115`) and the rule that route menus stay 3-7 items (`SYNTHESIS:22`) exist precisely because surfacing the full dispatch vocabulary is cognitively hostile. If the IDE renders all seven vocabulary layers and twelve taxonomy entries as visible controls, it becomes "a dashboard with no next action" — an explicit fail condition (`PRODUCT-VIEW.md:251`). The spine must stay *latent*: the dispatch document is the internal model; the card shows one bounded slice at a time. My thesis is strongest as an *architecture* claim, weakest if read as a *UI* claim.
- **Two primitives resist the mapping.** (a) **Intent-latitude** is input-side — it annotates the user's message *before* the agent acts (`ERGONOMICS:174-176`), whereas dispatch grammar models agent-produced routes; it fits `sentence_grammar` only by analogy, and its own doc flags overlap with the route-ambiguity branch as unresolved debt (`ERGONOMICS:208-210`). (b) **Field-hover popover** is pure LSP "peek" with no route, gate, or handoff (`ERGONOMICS:441-442`) — it maps to `entity_component_reference` only as a read, stretching the spine.
- **Authority risk.** The dispatch object explicitly *does not* execute or promote (`SKILL.md:74`, `README:60`). The unification must not let the IDE imply the card *owns* the route — Connective "recommends and explains; it does not execute" (`ERGONOMICS:391-392`) mirrors dispatch-spec's "validates; it does not execute sigils" (`WEAVER:117`). If marketing collapses this, the spine breaks the very owner-boundary invariant that makes it coherent.
- **Unverified claim:** I did not open `dispatch.schema.yml` (not in my read set); the layer/field mapping rests on the prose docs, which may lag the schema enum (`SKILL.md:68` lists patterns that should be cross-checked against the schema before this brief becomes load-bearing for build).

---

## E2 — Restraint/owner-boundary spine (initial position)

# E2 RESTRAINT-CONTRACT BRIEF — The spine is owner-safe restraint, not dispatch grammar

## 1. Thesis

The unifying spine of IDE Ergonomics is a single **restraint contract**: *a conversation moment may become a candidate, a draft, a preview, or a recorded intent, but it may not become a canonical change, an execution, or a route switch without an explicit human gate.* Every primitive in the product is the *same boundary* re-applied to a different transition type. The product's own one-sentence definition names this directly: it is "the missing moment between noticing useful work and safely sending that work to the right place" (`PRODUCT-VIEW.md` §"One-Sentence Product"). The load-bearing word is *safely*. The route menu is the visible surface; the restraint is the product.

The rival operator-grammar view — that the spine is a composition grammar of routes/owners/handoffs the user selects from — mistakes the *menu* for the *guarantee*. Necronomicon already states the priority order: "capture first and switch only when the user intends to switch" (`necronomicon/README.md` §"Interaction State Model"). Capture-before-switch is a restraint primitive, not a grammar primitive. The grammar is how options are *named*; the contract is what is *forbidden* between noticing and committing. Unification means **one boundary model, not one grammar**.

## 2. Shared restraint-contract invariants

Each MVP primitive enforces the identical contract — *block the consequential mutation, hold promotion with a named owner* — over a different transition. Sourced from `PRODUCT-VIEW.md` §"MVP Shape" table and the matching Guardrails in `ERGONOMICS-OPPORTUNITIES.md` §"Core Interaction Patterns":

| Primitive | What is BLOCKED (the restraint) | Who owns promotion / the gate |
| --- | --- | --- |
| Definition candidate | "No canonical definition promotion" (MVP Shape); button "must not write to canonical definitions" (Pattern 1 Guardrail) | `definitions-governance` — "explicit promotion later, if ever" |
| Side node | "Does not switch the active route"; "Side nodes cannot silently switch the active route" (Pattern 3 Guardrail) | Necronomicon `side_note_queue`; user intent owns the switch |
| Handoff draft | "Handoff is not execution proof" (MVP Shape; Pattern 2 Guardrail) | Next owner; handoff is "a durable start point," not a receipt |
| Route ambiguity | "Selection records intent; it does not execute" (MVP Shape) | `dispatch-spec` route recorded; the owner executes later |
| Delegated-run preview | "No subagent spawn without explicit approval"; "runtime cannot spawn them without explicit authorization" (Pattern 4 Guardrail) | `dispatch-spec` strategy + explicit user approval |
| Park / ignore | "No write by default" (MVP Shape) | No owner acts; default is inert |
| Self-assembling action | "assembled and green is not shipped"; criterion "frozen before the run" (Pattern 12) | `decision-gate` + the real lifecycle owner; "this loop is author and tester, not owner" |

The vertical regularity is the proof: **preview-is-not-execution, candidate-not-promotion, side-note-cannot-switch-route, handoff-is-not-execution-proof, recommendation-not-execution** are five surface phrasings of one invariant. The Anti-Patterns list (`ERGONOMICS-OPPORTUNITIES.md` §"Anti-Patterns") is the contract stated as its violations — "Button that directly mutates canonical definitions," "Side note capture that changes the active route," "Subagent action that skips permission," "Notification that reports 'done'…instead of 'ready for your test and approval'." Every anti-pattern is a *breach of restraint*, none is a breach of grammar. This is the strongest single piece of evidence: the document defines failure by lost restraint, not by malformed routes.

Necronomicon supplies the institutional backbone: its §"No-Promotion Guardrails" enumerates exactly what the harness *may create* (candidates, gap records, handoff packets) versus what it *must not promote by itself*, with promotion routed to the owning capability. IDE Ergonomics is that guardrail lifted to the IDE surface.

## 3. Why grammar stays backend

The composition grammar is real but belongs *behind* the card, for three flow/agency reasons grounded in the sources:

- **The card is "a bounded menu, not an open tool drawer"** (`PRODUCT-VIEW.md` §Step 3). Surfacing the full operator grammar is the explicit Fail/Anti-Pattern: "a generic agent launcher," "a route menu whose owner or boundary is unclear," "Generic 'run agent' button with no bounded route menu." The grammar's job is to *populate* the bounded menu, not to *be* the surface.
- **The product solves a memory/agency problem, not a syntax problem.** "The work is blocked because the right structure is hidden behind the user's memory" (`PRODUCT-VIEW.md` §"The Story"). Exposing grammar re-imposes the memory tax the product exists to remove. Necronomicon's target is identical: "the user should not need to remember which sigil owns every workflow" (§"Day-To-Day Use"). Restraint preserves flow; grammar exposure breaks it.
- **Unification = one boundary, many owners.** The "What Necronomicon Is Not" and the §"Governed Knowledge Substrate" promotion table show many distinct grammars (inventory, ontology, premise, axiom) already exist with *different* promotion rules. They do not unify into one grammar — they unify only under one rule: *Necronomicon does not promote by itself.* A single grammar is impossible here; a single restraint contract is the only thing all primitives can actually share.

## 4. Residue / risks — my own weak point

**Where pure restraint under-serves a power user.** A fluent operator who already holds the owner map in their head experiences candidate-first, preview-first, gate-on-everything as *latency tax*. The contract that protects a novice's flow throttles an expert's. The sources concede the pressure: `PRODUCT-VIEW.md` keeps "Explicit `invoke define` should route directly" (echoing Necronomicon §"Discovery-To-Definition Funnel": "Explicit `invoke define` should route directly… when enough context exists"). That escape hatch is *grammar leaking back to the surface* — the power user wants to name the route, not be handed a restraint card. So restraint-as-spine is incomplete: it needs a graduated-trust dial (explicit command bypasses the candidate stage) or it becomes friction theater. This is the rival view's genuine residue: **the grammar must be reachable on demand even though it stays backend by default.** My thesis holds only if "backend" means *default-hidden, expert-summonable* — not *absent*.

**Second risk:** "park/ignore — no write by default" means the spine's most-used state produces *no evidence*, which quietly contradicts the product's "more workflow evidence" gain. Restraint and observability can conflict; the contract should log the *non-action*, or the evidence claim weakens.

---

## E3 — Lifecycle/phase-graph spine (initial position)

# E3 Brief — The Spine Is the Governed Lifecycle Phase-Graph

## 1. Thesis

The IDE Ergonomics product is not organized by a card grammar, nor by a single minimal MVP card. Both are *renderings* of a deeper object: **one governed lifecycle phase-graph**. Necronomicon already names the canonical funnel — `Discover → Research → Decide → Define → Design/Plan → Execute` (necronomicon/README.md, "Discovery-To-Definition Funnel" table, lines 134-141) — and Spellcraft already names the canonical *contract* every node in such a graph must satisfy: each phase carries `input / output / gate / failure-policy`, plus named `handoff` artifacts and `observability` (spellcraft/SKILL.md, `<spell-contract>` lines 141-159; `Execution Phases` realized form in necronomicon/README.md lines 380-391). Fuse them and you get the spine: a directed graph of governed stages, each a Spellcraft-shaped phase, with `decide` as an explicit gate node (`decision-gate`) between research and define. Every IDE Ergonomics primitive is a **node, a gate, or a handoff edge** in this one graph — not a freestanding widget. Connective is the flagship because it is the only surface that *reads the whole graph's current state* and recommends the next lane with expected receipts (PRODUCT-VIEW.md line 119; ERGONOMICS-OPPORTUNITIES.md §10).

## 2. Primitive → Lifecycle-Stage + Phase-Contract Mapping

Each row maps an ERGONOMICS-OPPORTUNITIES primitive to its funnel stage and to the Spellcraft phase-contract fields it instantiates.

| Primitive (source §) | Lifecycle stage (necro funnel) | input | gate | output / handoff | failure-policy | observability |
|---|---|---|---|---|---|---|
| Side node capture (§3) | Discover | conversation aside | "does not switch active route" | `side_note_queue` entry / gap-ledger candidate | stays queued if non-blocking | route ledger |
| Knowledge-entry popup (§7) | Discover/Research | inventory/ontology query | stale ⇒ refresh; candidate≠canonical | reusable entry handle / context-pack insert | mark stale, offer refresh | search cache |
| Referenced-field hover (§11) | Discover/Research | hovered governed token | read-only; `unresolved`/`ambiguous` never fabricated | resolved authority body | report unresolved | — |
| Subagent fanout preview (§4) | Research | role tension / parallel lanes | explicit permission before spawn | role cards + receipts / dispatch-spec route | fallback if declined | receipt rail |
| Intent-latitude annotation (§6) | (input-side) Decide-adjacent | selected span | STRONG only for `[literal]`; unenforced never passed | latitude verdict | report `unenforced` | post-hoc validator |
| Route-ambiguity card (PRODUCT §MVP) | Decide | unsure-owner span | "selection records intent, not execution" | owner choice (`invoke`/`dispatch-spec`/`task-session`) | — | route record |
| Candidate definition card (§1) | Define | stable term | "no canonical promotion" | definitions-governance candidate packet | — | optional drift audit |
| Handoff composer (§2) | Design/Plan (split) | `handoff-ready` interaction | "handoff ≠ execution proof" | owner-specific handoff artifact | — | observer signal |
| Craft control panel (§9) | Execute (selection) | `.craft/ledger.yml` | "ledger stays source of truth; no direct blocker close" | owner route (interrogation/decision-gate/refine/export/defer) | defer | source freshness |
| Spell/sigil nudge (§5) | Maintain | repeated route miss | "suggest, not author/promote" | spellcraft / sigil-development route | — | telemetry threshold |
| Self-assembling action (§12) | Maintain (meta-loop over all stages) | map entry + friction telemetry | "assembled+green ≠ shipped"; criterion frozen pre-run | candidate artifacts + bounded user test | FALSIFIED leaves residue | experiment-harness |
| **Connective (§10)** | **reads ALL stages** | Craft export + indicators + tests + domain lens | "recommends, never executes/surveils" | ranked lanes w/ **expected receipt + owner route** | low-load comfort never hides critical work | full evidence rail |

The mapping is exhaustive: every primitive lands on exactly one stage (or, for Connective and self-assembly, on the *whole graph*), and every primitive's stated guardrail is literally a `gate` or `failure-policy` in Spellcraft's contract vocabulary. That coincidence is the argument — the product's own boundary language *already is* the phase-contract.

## 3. Connective as Flagship

Connective is the surface that proves the spine, because a card grammar can only describe one transition while the phase-graph describes *all pending state at once*. Connective's owner-safe route reads as a phase pipeline: `Craft state export → task candidates → human indicator snapshot → user-executed test evidence → domain priority lens → ranked execution lanes → interactive choice → selected owner route with receipt → governed write path` (ERGONOMICS-OPPORTUNITIES.md §10, lines 377-387). Each arrow is a phase with an input and a gate; the terminal node emits an **expected receipt** and **expected owner route** per lane (line 374) — exactly Spellcraft's `output`+`handoff`+`observability` triple. PRODUCT-VIEW.md states the same gain plainly: "Connective recommends the next lane by balancing human indicators, user-run evidence, Craft state, and domain priority" (line 119). Connective is "lifecycle state read + next-lane recommend with receipts" made into a UI — which is precisely Necronomicon's role ("working memory and routing desk… name its confidence," lines 48-72) lifted to the IDE. The card MVP is then a *degenerate single-node view* of Connective: one span, one transition. The flagship is the full graph reader; the MVP is one node lit up.

## 4. Residue / Risks (named weak point)

**Where the full lifecycle control surface over-builds vs the MVP.** The PRODUCT-VIEW is explicit that the MVP is *one bounded card*, and that "a definition card, handoff composer, and subagent preview… [are] too broad as the first proof" (lines 178-184). The phase-graph thesis, taken literally, demands a surface that reads Craft state, human indicators, user tests, and a domain lens — a far larger build than the static-fixture toy proof the PRODUCT-VIEW actually sanctions (lines 196-224, 270-274). So the spine over-builds the MVP: the first falsifiable question is "can a user choose the right governed route from *one* conversation moment?" — a single edge, not the graph. My hypothesis is strongest as the *organizing model* and weakest as the *build order*; if validation only ever exercises one card, the phase-graph remains an asserted backbone, not a demonstrated one.

**Two further seams.** (a) The funnel is explicitly *not mandatory* — "Explicit `invoke define` should route directly… The funnel is not mandatory for every request" (necronomicon/README.md line 143). A spine you can legally bypass is a strong *default path*, not a hard control-flow graph; a rival "minimal-card" reading can claim the graph is just one optional preset. (b) `Maintain` and the input-side `intent-latitude` primitive sit awkwardly: maintain is a meta-loop *over* the lifecycle rather than a stage *in* the funnel (necro funnel has no Maintain row; it appears only in the substrate/maintenance loop, lines 368-376), and intent-latitude acts on the user's message *before* the agent — neither is a clean linear node, which is the main place the "every primitive is one node" claim strains.
