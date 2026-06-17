---
id: ctx-pack-ui-ux-interaction-skill
project: ui-prototyping-studio
title: "Context Pack (s1) — UI/UX Interaction Surface + Operating SKILL.md"
status: frame
node_type: context-pack
run_id: 20260616-ui-ux-interaction-skill
dispatch_id: refine-ups-ui-ux-skill-20260616
step_id: s1-context
frame: frame.evidence-baseline
updatedAt: 2026-06-16
---

# Context Pack (s1) — UI/UX Interaction Surface + Operating SKILL.md

> The shared evidence floor every downstream stage (define → tournament → design → toy-game → plan)
> reads. It does NOT design the surface or author the skill — it states the runtime/CLI reality, the
> annotation decision, the ergonomics charter clauses, the cold-start friction findings, the ux-evidence
> model, and the open design questions. Two artifacts are being designed: (1) the operating `SKILL.md`
> (the Claude-Code operating contract), and (2) the **interaction surface** (how a human sees variants,
> annotates on components, and disposes at gates while Claude Code proposes). Everything below is
> selector-grounded; inference is labeled.

## Target (what this run designs)

1. **Operating `SKILL.md`** — the contract that makes Claude Code the generation/mutation *engine*: who-leads-when, the discipline (generate → `variants register` → stamp `data-od-id` → run `synthesize` → **never self-approve/apply** → hand the gates to the human).
2. **Interaction surface** — `studio preview --annotate` overlay + the human-agent review/gate loop: how the human *sees* variants, *clicks to annotate directly on components*, and *disposes* at the durable gates, with Claude Code proposing.

Both are **proposals**; authoring the live `SKILL.md` and building the overlay are downstream of operator approval (g6, promotion guardrails). The seed names three **candidate surfaces** to compare in the tournament (s5): **A** browser preview overlay (current design), **B** terminal/TUI review+gate, **C** minimal local web review page.

---

## 0. First Principle (non-negotiable charter) — Ergonomics

Source (verbatim): `development/deep-spec-dispatch/CONTEXT-PACK.md` §0. Design agentic tools that **improve human work** and form **synergetic, symbiotic human–agent relations.** This is the lens every kept/changed interaction decision must pass through. The dispatch enforces it as gate **g4-ergonomics-rationale** (`on_fail: flag`).

**Charter clauses (binding on every interaction decision):**

1. **Lead-when clause.** State *who leads when* — human or agent — at each decision point. Default posture: **agent proposes, human disposes** at every durable/irreversible boundary (baseline select/commit, identity confirm, apply/accept, handoff export).
2. **Cognitive-load clause.** State *what cognitive load it imposes* (recognition vs recall, comparison breadth, memory burden, decision count per cycle) and how the design keeps that load bounded.
3. **Friction-reduction clause.** State *how it reduces friction* — what manual/conversational step it removes, what it makes recognizable instead of remembered, what it makes resumable instead of repeated.
4. **Governance-is-a-feature clause.** Manual gates are **ergonomic features, not friction** — they keep the human accountable without policing the agent. **A gate is justified ONLY if it protects a durable/irreversible action; gates on reversible drafts are friction and must be challenged.**
5. **Evidence-floor clause.** No ergonomic claim is asserted; each is classified against the ux-evidence model (§5) and is either Playwright-observable or named as human-study residue.

**Carried gap — `GAP-ERGONOMICS-UNPROVEN-001`:** the first principle is *still unmeasured*. The decision gate (2026-06-16) separated it into a UX/ergonomics research track — *"the honest home for 'does this actually improve human work' — the first principle, still unmeasured"* — explicitly OFF the L0→L2 critical path. This run designs against the charter but cannot *prove* the gains; the toy-game (s8) is the cheapest available falsification, not proof.

---

## 1. Runtime + CLI reality (the surface the human/agent already drive)

Source: `SPEC.md` §2 (interaction model), `interfaces.md`, `backend/src/cli/studio.ts`.

- **Runtime = Claude Code-native, operated in VSCode, via a `studio` CLI. No MCP server, no `@anthropic-ai/sdk`, no API key, no React SPA, no agent loop** (`DEC-RUNTIME-CLAUDE-CODE-011`, `DEC-CLI-NOT-MCP-012`). The embedded assistant *is* Claude Code.
- **Division of labor:** the studio core is the **governance harness** (owns gates + determinism); **Claude Code is the generation/mutation engine**; the **CLI is the single operation surface for BOTH** Claude Code and the human. Gates (INV-3/4/5/8) are enforced **server-side in the orchestration module behind the CLI** — never in CLI args; *"a CLI flag is input, not authority."* (`interfaces.md` §3.)
- **Generator seam = the CLI.** Claude Code generates HTML + stamps `data-od-id`, registers via `studio variants register --from <dir>`; a **deterministic fake** (`--fake`) drives e2e. **Generation/mutation are the ONLY agentic actions**; everything else is deterministic + human-gated. Swapping fake↔Claude Code changes neither session contract nor any gate (AC-L0-9).
- **Internal boundary:** `Claude Code / human → studio CLI (adapter) → orchestration module (gates HERE) → StudioSessionStorePort → .data/*.json`. A REST adapter (`http-routes.ts`, 14 endpoints) shares the same core; its retention/drop is an **open choice**, not decided here (`interfaces.md` §2).

### 1.1 The built CLI surface (`backend/src/cli/studio.ts`, SWU-X2 — runnable today)

Commands present in code (grouped + dispatched in `switch (cmd)`):
`session open` · `prompt submit` · `variants generate` | `variants register` · `state` · `baseline select` · `baseline commit` · `comment add` · `synthesize` · `batch approve` · `batch apply` · `revisions` · `handoff export`.

- `comment add` reads flags `--selector`, `--label`, `--od-id`, `--severity`, `--intent`, `--note`, `--revision` → `captureCommentEvent({target:{selector, elementLabel, odId}, severity, intent, note})`. **This is the headless/scriptable annotation path and already exists.**
- `ACTOR = process.env.STUDIO_ACTOR ?? "cli-user"`; data persists to `.data/studio.json`. Errors print `{code,message,details}` to stderr, exit `2` (client/validation) or `1` (unexpected).

### 1.2 Built-vs-spec DRIFT (load-bearing — the design must not assume the spec CLI exists)

The CLI **as built** lags the spec/interfaces contract in three ways the interaction design depends on:

| Spec/interfaces says | Code (`studio.ts`) reality | Impact on this run |
|---|---|---|
| `preview <sid> [label\|revision] [--annotate]` — ephemeral server + click-to-annotate overlay (AC-L0-11/12) | **No `preview` command at all** (no case in the switch; not in usage string). | The entire surface A (overlay) is **unbuilt** — this run designs it from zero; the build plan (s9) must include it. |
| Two-gate apply: `apply`→stage→`accept`/`discard` (`DEC-MUTATION-EXEC-015`, `[PROPOSAL]`) | Only `batch apply` → `applyApprovedBatch` (single-gate L0 bookkeeping). Header drift note confirms: *"two-gate apply … is SWU-M2; here `batch apply` uses the existing applyApprovedBatch (L0 bookkeeping)."* | The "saw-the-diff" accept gate (the strongest disposal-side ergonomic, OQ-2 proxy) is **not yet in the CLI**. The loop design must say whether it leans on it. |
| `variants register --from <dir>` = real Claude Code HTML | `variants generate` and `variants register` both route to `generateVariants` (the deterministic stub). Header: *"real generation is Claude Code via `variants register`, M-later."* | The skill teaches `variants register`, but the live wiring to Claude-Code-supplied HTML is not yet real. |

> **Inference:** the SKILL.md and overlay are being designed against the *target* CLI contract (`interfaces.md`), while the *runnable* CLI is the X2 subset. The plan stage must reconcile which commands the skill may assume.

---

## 2. The annotation decision (the heart of surface A)

Source: `SPEC.md` §2 + AC-L0-11/12, `interfaces.md` `preview` row. Decisions: `DEC-INPROTO-ANNOTATION-013` (in-prototype annotation), `DEC-ATOMIC-IDS-014` (stable atomic ids).

- **`studio preview --annotate`** should: serve the variant/revision HTML from an **ephemeral local server**, open it in the browser, and **inject a click-to-annotate overlay**. Clicking a rendered element captures its **stable `data-od-id` as the PRIMARY target** (CSS selector + element label as **fallback**), opens a `{severity, intent, note}` form, and POSTs back to the local server → `captureCommentEvent` (gated by **INV-2**: blocked until a baseline exists, `ANNOTATION_GATE_LOCKED`). `--annotate` defaults on when a baseline exists.
- **No hand-typed selectors. Comments captured DIRECTLY on components.** The overlay path and `studio comment add` produce the **identical `CommentEvent` contract**: `{target:{odId, selector, elementLabel}, severity, intent, note}` (AC-L0-11). `comment add` remains the scriptable/headless path.
- **Stable annotation targets (light component identity).** The generator stamps annotatable elements with a stable `data-od-id` on a minimal component-role convention, so a comment's target **survives regeneration** (Explore→Exploit, applied mutations) instead of breaking with the DOM (AC-L0-12). Where no `data-od-id` exists, the overlay falls back to the CSS selector and **flags the target as non-durable**.
- **Deferred (named):** the full atomic-design taxonomy (atoms→organisms), component registry, and `UIElementIdentity`/conformance-delta are the **L4** realization of this idea (`BLK-IDENTITY-TYPES-002`, `GAP-COMPONENT-REGISTRY-002`) — out of scope.
- **Engine purity at the seam (`[PROPOSAL]`, `interfaces.md` §3):** the proposer (Claude Code) is **value-in/value-out** — forbidden the store/clock/append path. The overlay is the only mutation in `preview`, and it is a gated `CommentEvent`, not a write to head.

---

## 3. The human-agent loop (who acts where)

Source: `SPEC.md` §2 + §5, `interfaces.md` §4 (operating skill seam).

The canonical loop and the agent/human split:

```
human asks Claude Code for a UI
  → Claude Code GENERATES 1–3 HTML variants + stamps data-od-id, runs `variants register`   [AGENT, reversible]
  → human `preview`s, then disposes the gates via the CLI:
       baseline select|commit        [HUMAN, durable: intentional baseline]   INV-2
       comment add / preview overlay  [HUMAN authors; reversible append]       INV-7
  → `synthesize` deterministic draft batch (can be agent or human; reversible)
  → batch approve                     [HUMAN-only, INV-3]                       durable
  → apply → stage + honest diff        [HUMAN triggers; Claude Code PROPOSES candidate]  [PROPOSAL]
  → accept (saw-the-diff)             [HUMAN-only, second gate, INV-3/4/5/8]    irreversible
  → (append exactly one revision)
  → handoff export                    [HUMAN]                                   terminal
```

- **Agent proposes (generate / register / synthesize / propose candidate), human disposes (select / approve / apply / accept).** Synthesis stays **deterministic** so the agent can never reinterpret the human's intent. (`SPEC.md` §2.)
- Claude Code **NEVER** runs `batch approve`, `apply`, or `accept` — human-only; they refuse a non-human/`system:auto` actor **server-side** even if invoked (INV-3/4, AC-L0-6/10). Within `apply`, Claude Code is only the **proposer engine** (value-in/value-out) — it does not stage, accept, or advance head. (`interfaces.md` §4.)
- **Durable/irreversible boundaries** (where the gate is a feature, not friction): baseline select/commit (INV-2), batch approve (INV-3), accept-diff (the irreversible head advance), handoff export. **Reversible** (agent may act freely): generate, register, synthesize, comment-append (append-only, droppable by not synthesizing).
- **Lead-when tiers** (from the ux-evidence report's matrix): **tier-1** agent-may-act (reversible compute/render), **tier-2** human-disposes (durable), **tier-3** human+proof (deferred to L5/L6).

---

## 4. Cold-start friction findings (the naive-user evidence)

Source: `development/deep-spec-dispatch/COLD-START-USABILITY-FINDINGS.md`. A first-time user with **zero onboarding**, reacting only to on-screen labels of the (current React workbench) 7-panel layout. This is the friction baseline the new surface must beat. **Caveat:** these findings are against the *old React workbench*, not the CLI/overlay — but the **vocabulary and conceptual friction transfer directly** to any surface, including the CLI and the overlay.

**Friction ranked by severity (verbatim from the report):**

| Rank | Task | Friction | Severity |
|---|---|---|---|
| 1 | Identity evidence | "Identity Evidence Panel" has no findable, confirmable content; no preview to inspect — task effectively impossible. | **Critical** |
| 2 | Choose option | **"Baseline" is misleading** (reads as "control/original," means "the option I chose"); card not clickable; no select control for single-variant. | **Critical** |
| 3 | Apply change | Applying is a hidden 3-step Synthesize→Approve→Apply ritual in a separate "Mutation" panel, disconnected from the note, **no visual proof the change landed.** | **High** |
| 4 | Annotate | Form demands **"Target selector" / "OD ID"** (dev jargon), no click-to-annotate on a preview; "Intent" vs "Note" ambiguous. | **High** |
| 5 | Generate | **Hidden prerequisite chain** (Start Session → Submit Prompt → Generate Variants) signaled only by disabled buttons + `sessionId=pending`. | **High** |
| 6 | Handoff | "Export Handoff" produces no visible deliverable; Export vs Refresh unclear; output is opaque reference IDs. | **Medium** |
| 7 | History | Revision history is IDs + unlabeled `diff=2/1/0`, no timestamps, no plain summary, no link to originating note. | **Medium** |
| 8 | All | **Pervasive machine-status strings** (`gate=pending`, `revisionHead=pending`) as primary UI signals; no glossary, no onboarding, no step numbering. | **High (cross-cutting)** |

**Five root causes (the design must answer each):**
1. **No onboarding / no step ordering** — 7 coequal panels, but the real workflow is a strict pipeline; numbering/arrows/"next step" highlight would fix most stalls.
2. **Disabled state without reason** — most blocking buttons just grey out; only Annotation says *why*. Every disabled control needs a one-line reason. (Maps to ux-evidence `a11y.5` disabled-reason contract.)
3. **Internal jargon as user-facing labels** — "Baseline," "Mutation," "Synthesize," "Gate," "Revision head," "OD ID," "Target selector," "Identity Evidence," "Handoff bundle." None explained on screen.
4. **No live preview anywhere** — variants, selected design, annotated element, applied change, handoff output are all text references, never something the user can *see*. This single missing affordance is what the overlay directly attacks.
5. **Status shown as raw key=value strings** instead of human sentences/badges, so confirmations are easy to miss.

> **Design tension this surfaces:** the cold-start user wants Figma/v0 ("type idea → see mockups → click element → comment → done"); the studio is an **accountable, gated, expert tool**. The overlay (surface A) directly closes #4 (no preview) and #4-annotation jargon; the CLI surface (the actual runtime) inherits #3 (jargon) and #5 (key=value JSON) unless the SKILL.md / surface translates them. **The jargon root-cause is partly a SKILL.md job** (Claude Code can narrate the loop in plain language) and partly a surface job.

---

## 5. The UX-evidence model (classify every non-trivial UX claim; never assert)

Source: `UX-EVIDENCE-REPORT.md` (s6 validator lane) + `arcanum` `ux-evidence-validator` SKILL. **Every non-trivial UX claim in this run MUST be classified into one of five classes — never asserted bare** (charter clause 5, gate g4/g5).

**The five classes:**

| Class | Meaning | May it be a hard CI gate? |
|---|---|---|
| `hard_gate` | Deterministic or standards-backed failure (WCAG 2.2 / WAI-ARIA 1.2 / APG, smoke, layout overflow/target-size, scripted interaction outcome, console/network error). | **Yes** — only after fixture calibration (known-good passes, known-bad fails, false-positive trap stays silent). |
| `soft_flag` | Conservative UI proxy for a cognitive/perception/market claim; flags, does not block. | No. |
| `screenshot_review` | Human inspects a captured frame (salience, distinctiveness); no pass/fail. | No. |
| `human_study` | Workload/comprehension/trust/real-task-success; Playwright only prepares evidence (timing, traces). | No — automation cannot pass/fail it. |
| `not_automatable` | Meaning/semantic correctness; machine may check *shape* only, never *meaning*. | Shape only. |

**Five validator-safety rules (read first, from the report):**
1. Hard gates **only** for deterministic/standards-backed failures.
2. Cognitive/perception/market claims are **never** hard gates → soft_flag / screenshot_review / human_study.
3. **Every finding names a `proxy_limit`** — the gap between the Playwright observation and the human truth it cannot reach.
4. No hard gate promotes without fixture calibration.
5. Governance is **keyboard-first and universal** — every tier-2 disposal must be operable + announced for keyboard/AT users.

**Relevant evidence findings already on record (the interaction design should reuse, not re-derive):**
- `a11y.3` **hard_gate/block** — governance gates fully keyboard-operable (no mouse-only disposal). *Directly constrains surface A: a mouse-only click-to-annotate overlay would violate this — the overlay needs a keyboard path or a keyboard-equivalent (`comment add`).*
- `a11y.4` **hard_gate/high, BLOCKED on impl** — the irreversible apply gate has no dialog/focus-trap in code; design specifies one. *The accept-diff gate (surface) must decide modal vs non-modal.*
- `a11y.5` **soft_flag/medium** — disabled-reason exists in DOM but is not `aria-describedby`-associated. *The "disabled without reason" cold-start root cause #2.*
- `flow.2` **hard_gate/block** — tier-2 gates block the irreversible action until the human disposes (agent cannot actuate apply with no approval).
- `cog.1` **soft_flag/low + FX-FP-01 false-positive trap** — decision density: *the studio is an expert tool; density proxies must NOT fire on the legitimate dense layout.* Only *ungrouped* density flags.
- `cog.5` **screenshot_review** — salience of the irreversible Apply gate vs decorative regions.
- `human.1/.2/.3` **human_study/high** — does a first-time human discover the agent-proposes/human-disposes boundary (Q0)? Is the irreversible apply *registered, not rubber-stamped*? Workload vs friction-claimed. **These are the `GAP-ERGONOMICS-UNPROVEN-001` core — unprovable in this run; the toy-game prepares evidence only.**

**Net (report summary):** 11 hard gates (all deterministic/standards-backed), 10 soft flags, 2 screenshot reviews, 4 human-study residues, 1 not-automatable carve-out. Promotion status: **FLAG/seed-spec** — gates specified + source-backed but not promoted (no fixture corpus run yet).

---

## 6. Open design questions (what the downstream stages must resolve)

These are crisp, named, and tensioned for the define (s2) / tournament (s5) / dialectic (s6) stages.

- **ODQ-1 — Which surface?** A (browser overlay) vs B (TUI review+gate) vs C (minimal local web page). Tournament criteria (from dispatch): who-leads-when clarity, cognitive load, friction reduction, **in-prototype annotation fidelity**, build cost. *Tension: A is the only surface that closes cold-start root-cause #4 (no live preview) and gives true click-on-component annotation; B is closest to the CLI-native runtime and cheapest to keyboard-make-accessible (`a11y.3`); C is a middle ground. The annotation decision (`DEC-INPROTO-ANNOTATION-013`) presumes A — does the tournament get to overturn a recorded decision, or only choose the review/gate surface around it?*
- **ODQ-2 — Where does the gate disposition live?** The durable gates (`baseline`, `approve`, `apply`/`accept`) are CLI commands today. Does the chosen surface (overlay/TUI/web) *also* host the gates, or does annotation happen in the surface while disposition stays in the terminal? (Splitting them re-introduces cold-start friction #3 "disconnected from the note"; unifying them risks a mouse-only gate that violates `a11y.3`.)
- **ODQ-3 — Keyboard/AT parity for the overlay** (`a11y.3` hard_gate). A click-to-annotate overlay is mouse-shaped. What is the keyboard-equivalent path — tab-to-element + Enter, or always-available `comment add` as the AT fallback? Must be answered before A can pass the keyboard hard gate.
- **ODQ-4 — Accept-diff "saw-the-diff" surface** (OQ-2 → `DEC-OQ2-SAW-DIFF`: accept-diff is the proxy; `DEC-MUTATION-EXEC-015`). How is the honest diff (`DiffSummaryHonest`/`OdDiffFragment`) *rendered for human review* before the irreversible accept? This is `[PROPOSAL]` and **not in the built CLI** (only `batch apply` single-gate). Surface + skill must name whether they assume the two-gate apply exists.
- **ODQ-5 — Jargon translation: surface or skill?** The cold-start jargon (baseline/mutation/synthesize/gate/od-id) is the cross-cutting root cause. Is the fix a relabeling in the surface, a plain-language narration in `SKILL.md` (Claude Code explains "baseline = the option you chose"), or both? Who owns the glossary?
- **ODQ-6 — SKILL.md target: built CLI or spec CLI?** Given the §1.2 drift, does the operating skill teach the *runnable* X2 subset (`batch apply`, `variants generate`, no `preview`) or the *target* contract (`apply`/`accept`/`discard`, `preview --annotate`)? A skill that teaches unbuilt commands will fail at runtime; a skill that teaches only built commands omits the saw-the-diff gate and the overlay.
- **ODQ-7 — How is the ergonomics first principle even partially evidenced here?** `GAP-ERGONOMICS-UNPROVEN-001` is unmeasured and off the critical path. The toy-game (s8) is the cheapest falsification (dual walkthrough: naive user + Claude Code). What is the minimum claim the run is allowed to make, and what stays `human_study` residue?

---

## 7. Authority precedence + write scope (for downstream stages)

- **Authority order** when sources conflict: built code (`studio.ts`, orchestration module) for *what runs today* > `interfaces.md` for the *target CLI contract* (`[PROPOSAL]` items are not-yet-built) > `SPEC.md` for *scope/ACs* > `.craft/ledger.yml` decisions (`DEC-*`) for *rationale* > the deep-spec dispatch docs for *evidence*. The `[PROPOSAL]` tag in SPEC/interfaces means "designed, not built" — treat as target, not fact.
- **Write scope (g6, promotion guardrails):** this run folder only. The `SKILL.md` + interaction design + plan are **proposals**; no live `SKILL.md` install, no SPEC mutation, without operator approval and the requested `domainspec-subagents-strategy` review. External UX research stays `external_context` (g2).
- **Decisions in force:** `DEC-RUNTIME-CLAUDE-CODE-011` (Claude Code-native), `DEC-CLI-NOT-MCP-012` (CLI not MCP), `DEC-INPROTO-ANNOTATION-013` (in-prototype annotation), `DEC-ATOMIC-IDS-014` (stable atomic ids), `DEC-MUTATION-EXEC-015` (agentic-propose / deterministic-admit, two-gate apply), `DEC-OQ1-TRUST-METER` (no trust meter in MVP → UX research), `DEC-OQ2-SAW-DIFF` (accept-diff is the proxy). Full text in `.craft/ledger.yml`.

---

## Evidence index (selector-level)

| # | Source | Selector | Closes |
|---|---|---|---|
| E1 | `SPEC.md` | §2 "Interaction model & where the agent acts"; §5 INV-1..9; AC-L0-9/10/11/12/13/14 | runtime, loop, annotation, gates |
| E2 | `interfaces.md` | §1 CLI command table (`preview` row, `apply`/`accept`/`discard` `[PROPOSAL]`); §3 internal boundaries + engine seam; §4 operating skill seam | CLI contract, seam, drift |
| E3 | `backend/src/cli/studio.ts` | `switch (cmd)` cases (no `preview`; `batch apply`→`applyApprovedBatch`; `variants generate`==`register`); header drift note (lines 18–23) | built-vs-spec drift |
| E4 | `development/deep-spec-dispatch/COLD-START-USABILITY-FINDINGS.md` | "Friction ranked by severity" table + "Cross-cutting cold-start gaps" §1–5 | friction baseline |
| E5 | `development/deep-spec-dispatch/UX-EVIDENCE-REPORT.md` | "How to read a finding card"; findings a11y.3/.4/.5, flow.2, cog.1/.5, human.1/.2/.3; classification summary | ux-evidence model |
| E6 | `development/deep-spec-dispatch/CONTEXT-PACK.md` | §0 charter clauses 1–5 (verbatim) | ergonomics charter |
| E7 | `development/DECISION-GATE-2026-06-16.md` | "Resolved" + "Separated research tracks" §1 (ergonomics is unmeasured, off critical path) | GAP-ERGONOMICS-UNPROVEN-001 |

## Obligation coverage (s1 stop condition)

The dispatch stop condition: *"Baseline cites the SPEC interaction model, the CLI-native + annotation decisions, the ergonomics charter, and the cold-start/ux-evidence findings."*

- SPEC interaction model → §1, §3 (cited). **Covered.**
- CLI-native + annotation decisions → §1 (`DEC-011/012`), §2 (`DEC-013/014`). **Covered.**
- Ergonomics charter → §0 (verbatim clauses 1–5). **Covered.**
- Cold-start findings → §4. **Covered.**
- UX-evidence model → §5. **Covered.**
- Built-CLI reality (added) → §1.1/§1.2 drift. **Covered.**
- Open design questions (required by the seed) → §6 (ODQ-1..7). **Covered.**

**Coverage: 100% of named obligations. No blockers.** One flagged residue carried to define (s2): the **built-vs-spec CLI drift (§1.2)** means the SKILL.md and overlay target a CLI contract that is partly unbuilt — s2/s9 must reconcile (ODQ-6).
