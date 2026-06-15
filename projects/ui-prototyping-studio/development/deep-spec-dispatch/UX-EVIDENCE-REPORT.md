---
id: ui-prototyping-studio-ux-evidence-report
feature: ui-prototyping-studio
title: "UX Evidence Report (s6): validator-safe L0-L6 findings for the seven studio surfaces"
summary: >
  s6 validator-lane translation of ergonomics / WCAG 2.2 / design-system practice into VALIDATOR-SAFE
  checks for the UI Prototyping Studio workbench (Session Controls, Variant Canvas, Identity Evidence
  Panel, Annotation Panel, Mutation Approval Panel, Revision Timeline, Handoff Summary). Every non-trivial
  UX claim is classified (hard_gate | soft_flag | screenshot_review | human_study | not_automatable),
  carries a severity (block|high|medium|low|info), and names its proxy_limit (what Playwright observes
  vs cannot prove). Hard gates are reserved for deterministic or standards-backed failures. The companion
  fixture plan lives in key_points.
status: draft
node_type: design
dispatch_id: ui-prototyping-studio-deep-spec-001
step_id: s6-ux-evidence-validator
lane: validator
owners:
  - web-core
reads:
  - handle.synthesis            # SYNTHESIZED-DEEP-DESIGN.md (s4)
  - frame.evidence-baseline     # CONTEXT-PACK.md (s0)
  - cards.ux-evidence-reference # UX-EVIDENCE-REFERENCE-CARDS.yml
  - map.ux-evidence-claim       # UX-EVIDENCE-CLAIM-MAP.md
updatedAt: 2026-06-15
---

# UX-EVIDENCE-REPORT.md — s6 Validator Lane

**Dispatch:** `ui-prototyping-studio-deep-spec-001` · **Step:** `s6-ux-evidence-validator` · **Consumes:** `handle.synthesis` (s4 deep design), `frame.evidence-baseline`, the UX reference cards and claim map. · **Produces:** this report + the fixture plan (key_points).

**First principle (non-negotiable):** ergonomics — agentic tools that improve human work and form symbiotic human-agent relations. **Governance is a feature, not friction.** Every finding below names *who leads when* (the design's tier-1/2/3 lead-when matrix, D-S0 / §2.8) and is honest about what Playwright proves vs cannot prove.

## Validator-safety contract (read first)

This report obeys five rules drawn from `UX-EVIDENCE-CLAIM-MAP.md`:

1. **Hard gates only for deterministic or standards-backed failures.** WCAG 2.2 / WAI-ARIA 1.2 / APG, smoke, layout overflow/target-size, scripted interaction outcomes, console/network errors.
2. **Cognitive / perception / market claims are never hard gates.** They become a conservative UI proxy + fixture (soft_flag / screenshot_review) or human-study residue. The first-principle ergonomic *gains* are explicitly unproven here (s4 R-5) — they are the s8 naive-user lane's job.
3. **Every finding names a `proxy_limit`** — the gap between the Playwright observation and the human truth it cannot reach.
4. **No hard gate promotes without fixture calibration** (a known-good fixture passes, a known-bad fixture fails, a false-positive trap does NOT fire). See fixture plan.
5. **Governance is keyboard-first and universal** (Q9): every tier-2 disposal (`SelectOrCommitBaseline`, `ApproveMutationBatch`, `ApplyApprovedBatch`, `ExportDesignHandoff`) must be operable and announced for keyboard + AT users, or the governance-is-a-feature clause is violated.

### Surface inventory (grounded in implemented components)

| Surface | Component (apps/web) | Key roles / locators observed | Governance tier touched |
|---|---|---|---|
| Session Controls | `SessionControlsPanel.tsx` | `section[aria-labelledby]`, `select#ups-variant-count`, `textarea#ups-prompt-input`, buttons Start/Submit/Generate | tier-1 (reversible) |
| Variant Canvas | `VariantCanvas.tsx` | `ul[data-testid=ups-variant-grid]`, per-card "Select Baseline {label}" button, `ups-selection-gate` note | tier-2 (`SelectOrCommitBaseline`) |
| Identity Evidence Panel | (design surface; conformance-delta / FitnessSignal read-model — see note) | proposed: delta chips, confidence chips, constrain-lock disabled-reason | tier-1 compute / tier-2 lock |
| Annotation Panel | `AnnotationPanel.tsx` | labelled inputs `target/elementLabel/odId/severity/intent/note`, "Capture Comment", `ups-comment-stream` | tier-2 (`ConfirmUIDecisionEvidence`) |
| Mutation Approval Panel | `MutationApprovalPanel.tsx` | Synthesize/Approve/Apply buttons, `ups-approval-status`, `ups-apply-gate`, `ups-draft-task-list` | tier-2 (`ApproveMutationBatch`, `ApplyApprovedBatch`) |
| Revision Timeline | `RevisionTimeline.tsx` | `ol[data-testid=ups-revision-list]`, per-entry diff `added/changed/removed` | read-model |
| Handoff Summary | `HandoffSummaryPanel.tsx` | Export/Refresh buttons, `ups-handoff-status`, `ups-handoff-list` | tier-2 (`ExportDesignHandoff`) |
| (cross-cutting) | `SessionStateIndicator.tsx` | `div[aria-live="polite"]` with state badge + selectionGate/applyGate/baseline notes | announces all tiers |

**Note on the Identity Evidence Panel:** the s4 design specifies the conformance-delta surface (`DiffSummary` over two `UIVisualSignature`s, `proposedChampionLabel`, confidence chips, constrain-lock blocking) but no dedicated `IdentityEvidencePanel.tsx` exists yet in the implemented tree. Findings F-ID-* below are therefore written as **forward checks against the design contract**, with the proxy_limit naming the not-yet-built status. This is honest residue, not a fabricated observation.

---

## How to read a finding card

```
finding_id: ux.finding.<surface>.<n>
surface: <one of the seven + indicator>
layer: L0..L6
class: hard_gate | soft_flag | screenshot_review | human_study | not_automatable
severity: block | high | medium | low | info
source_cards: [ux.std.*, ux.cog.*, ux.perception.*, ux.market.*, ux.pw.*]
lead_when: tier-1 (agent-may-act) | tier-2 (human-disposes) | tier-3 (human+proof)
playwright_observes: <the deterministic observation>
proxy_limit: <what the evidence cannot prove>
fixture: <fixture id from UX-FIXTURE-PLAN.md>
```

---

# Layer L0 — Smoke (load / assets / console / network)

> Calibration rule: L0 becomes a hard gate **after** a known-bad fixture (e.g., a panel whose artifact `htmlArtifactRef` 404s) is proven to fire. Source: `ux.pw.trace_viewer`, `ux.pw.assertions`.

### ux.finding.smoke.1 — Studio route + all seven panels mount without fatal error
- **layer:** L0 · **class:** hard_gate · **severity:** block
- **source_cards:** `ux.pw.trace_viewer`, `ux.pw.assertions`
- **lead_when:** tier-1 (agent renders; no durable effect)
- **playwright_observes:** navigation succeeds; the seven `section[aria-labelledby]` landmarks + the `aria-live` indicator are attached; zero uncaught console errors / failed required requests during initial mount and a first `InitializeSession`.
- **proxy_limit:** a clean console proves nothing about whether the workbench is *usable* or *comprehensible* — only that it did not crash. Cognitive legibility is L4/L6.
- **fixture:** FX-KG-01 (known-good full studio), FX-KB-01 (panel artifact 404).

### ux.finding.smoke.2 — Variant `htmlArtifactRef` previews resolve (no broken candidate)
- **layer:** L0 · **class:** hard_gate · **severity:** high
- **source_cards:** `ux.pw.assertions`, `ux.pw.trace_viewer`
- **lead_when:** tier-1
- **playwright_observes:** each Variant Canvas card's referenced artifact loads (no 404/500 on the preview iframe/asset); network panel shows no failed required request for a generated variant.
- **proxy_limit:** a resolving artifact does not prove the variant is on-brand or that the human can tell variants apart — that is the D1 conformance-delta (L1/L4), not smoke.
- **fixture:** FX-KB-01.

---

# Layer L1 — Accessibility (axe, ARIA snapshot, role/name/state, keyboard, forms)

> Hard gate + mandatory manual review. Source: `ux.std.wcag22`, `ux.std.wai_aria12`, `ux.std.aria_apg`, `ux.tool.axe_core`, `ux.pw.aria_snapshots`, `ux.pw.locators`. Maps directly to design Q9 (D-decide: hard-gate the deterministic parts; governance keyboard-first).

### ux.finding.a11y.1 — Every interactive control exposes an accessible name + correct role
- **layer:** L1 · **class:** hard_gate · **severity:** block
- **source_cards:** `ux.std.wcag22` (4.1.2), `ux.std.wai_aria12`, `ux.pw.locators`, `ux.tool.axe_core`
- **lead_when:** tier-1 (compute) / governs tier-2 disposability
- **playwright_observes:** `getByRole('button', { name: ... })` resolves for Start/Submit/Generate, Select Baseline {label}, Capture Comment, Synthesize/Approve/Apply, Export/Refresh; axe reports zero `button-name` / `select-name` / `label` violations. All `<select>`/`<textarea>`/`<input>` are programmatically labelled (observed: each is wrapped by a `<label htmlFor>` in the implemented panels).
- **proxy_limit:** axe + role locators cannot prove the *name is meaningful to a screen-reader user in task context* (e.g., is "Select Baseline B" understandable without seeing the card?). That is the WCAG-EM manual prompt → L1 manual + partly L6.
- **fixture:** FX-KG-01, FX-KB-02 (icon-only unnamed button trap).

### ux.finding.a11y.2 — Tab order across the 7 panels follows reading order
- **layer:** L1 · **class:** hard_gate · **severity:** high
- **source_cards:** `ux.std.wcag22` (2.4.3 Focus Order), `ux.std.aria_apg`, `ux.pw.assertions`
- **lead_when:** tier-2 (governance must be keyboard-reachable)
- **playwright_observes:** scripted Tab traversal visits panels in DOM/reading order (Session Controls → Variant Canvas → Identity Evidence → Annotation → Mutation Approval → Revision Timeline → Handoff); focus order log + visible-focus screenshots captured.
- **proxy_limit:** "follows reading order" is checkable; whether that order matches the *human's intended cognitive workflow* (does generate-before-annotate feel natural?) is L6.
- **fixture:** FX-KG-01, FX-KB-03 (positive `tabindex` scramble trap).

### ux.finding.a11y.3 — Governance gates are fully keyboard-operable (no mouse-only disposal)
- **layer:** L1 · **class:** hard_gate · **severity:** block
- **source_cards:** `ux.std.wcag22` (2.1.1 Keyboard), `ux.std.aria_apg`
- **lead_when:** tier-2 (the non-negotiable: governance is not a mouse-only privilege — design §2.5)
- **playwright_observes:** `SelectOrCommitBaseline` (Select Baseline button), `ApproveMutationBatch` (Approve Draft), `ApplyApprovedBatch` (Apply Approved Batch), `ExportDesignHandoff` (Export Handoff) are each reachable by Tab and actuated by Enter/Space, producing the same visible state change as a click.
- **proxy_limit:** keyboard-operability proves access, not that the keyboard path is *as low-friction* as the mouse path (number of keystrokes to dispose). Friction parity is an L4 proxy + L6 study.
- **fixture:** FX-KG-01.

### ux.finding.a11y.4 — `ApplyApprovedBatch` confirmation is a real dialog with focus trap + return-focus
- **layer:** L1 · **class:** hard_gate · **severity:** high
- **source_cards:** `ux.std.aria_apg` (Dialog (Modal) pattern), `ux.std.wai_aria12`, `ux.pw.aria_snapshots`
- **lead_when:** tier-2 (the irreversible boundary — D-S3: only `ApplyApprovedBatch`/`SelectOrCommitBaseline` are irreversible)
- **playwright_observes:** **DESIGN-VS-IMPL GAP.** The s4 design (§2.5 Q9) requires "focus trap + return-focus on the `ApplyApprovedBatch` approval modal." The implemented `MutationApprovalPanel.tsx` exposes Apply as a *plain disabled-gated button*, NOT a modal — there is no `role="dialog"`, no `aria-modal`, no focus trap, no return-focus. The check asserts: a dialog opens on Apply, focus moves into it, Tab cycles within it, Escape closes it, focus returns to the trigger.
- **proxy_limit:** Playwright proves trap mechanics; it cannot prove the human *registers* the irreversibility warning before confirming (change-blindness on the irreversible step) — that pairs with F-IND-2 (L3) and an L6 study.
- **finding:** this is a **real flag against the design contract**: the irreversible gate currently has no modal affordance. Recommend either (a) implement the dialog the design specifies, or (b) amend the design if a non-modal confirmed-gate is acceptable. Until resolved, this hard gate is **specified but not yet satisfiable** by the implementation.
- **fixture:** FX-KG-04 (compliant apply dialog), FX-KB-04 (untrapped modal trap).

### ux.finding.a11y.5 — Disabled governance buttons expose a machine-readable disabled-reason
- **layer:** L1 · **class:** soft_flag (a11y-adjacent) · **severity:** medium
- **source_cards:** `ux.std.wcag22` (3.3 / 4.1.2), `ux.market.nng_heuristics` (visibility of system status)
- **lead_when:** tier-2 (D-005 disabled-reason contract: the human is never silently prevented; they see *why*)
- **playwright_observes:** **DESIGN-VS-IMPL GAP.** Buttons disable via the `disabled` attribute (`Submit Prompt`/`Generate Variants` need `sessionId`; `Approve Draft` needs `approvalPending`; `Apply` needs `applyEnabled`). The *reason* leaks only into sibling status notes (`applyGate=pending`, "Annotation gate locked: select baseline first") that are NOT associated with the control via `aria-describedby`. Check: each disabled gate control has an associated accessible reason (`aria-describedby` → the gate note, or `title`).
- **proxy_limit:** presence of an associated reason string is deterministic; whether the reason *reads as actionable* ("select a baseline first") vs cryptic is L4 screenshot_review + L6. This is a soft_flag (not block) because the reason text exists in the DOM nearby — it is an association/discoverability gap, not a total absence. The disabled-reason contract is the design's own friction-killer; surfacing it inaccessibly silently re-introduces the friction.
- **fixture:** FX-KG-05 (gate with `aria-describedby` reason), FX-SF-01 (reason present but unassociated).

### ux.finding.a11y.6 — ARIA snapshot of each panel landmark is stable and semantically honest
- **layer:** L1 · **class:** hard_gate · **severity:** medium
- **source_cards:** `ux.pw.aria_snapshots`, `ux.std.wai_aria12`
- **lead_when:** tier-1
- **playwright_observes:** each panel is a `region`/`section` named by its `<h3>` via `aria-labelledby`; ARIA snapshot captures landmark + heading + control tree for the 7 panels and stays stable across runs.
- **proxy_limit:** a stable snapshot proves structure, not interaction completeness (e.g., the live region behavior in F-IND-1). Pair with keyboard assertions.
- **fixture:** FX-KG-01.

---

# Layer L2 — Layout Integrity (overflow / clip / overlap / target-size / responsive)

> Hard gate. Source: `ux.pw.visual_comparisons`, `ux.cog.fitts_law`. **Target-size threshold is product-context-calibrated**, never a single universal number (claim-map proxy-limit on Fitts).

### ux.finding.layout.1 — No horizontal overflow / text clipping at required viewports
- **layer:** L2 · **class:** hard_gate · **severity:** high
- **source_cards:** `ux.pw.visual_comparisons`
- **lead_when:** tier-1
- **playwright_observes:** at desktop / tablet / mobile, `scrollWidth <= clientWidth` (no horizontal overflow); no clipped text in the seven panels; the dense `ups-draft-task-list` and `ups-comment-stream` lists reflow rather than clip. Full-page + clipped screenshots captured with stable fonts/data/motion.
- **proxy_limit:** "fits the viewport" does not prove the dense seven-panel grid is *scannable* on mobile — density legibility is L4 screenshot_review.
- **fixture:** FX-KG-01, FX-KB-05 (fixed-width panel overflow trap).

### ux.finding.layout.2 — Governance controls meet the calibrated target-size floor
- **layer:** L2 · **class:** hard_gate · **severity:** medium
- **source_cards:** `ux.cog.fitts_law`, `ux.std.wcag22` (2.5.8 Target Size (Minimum), 24x24 CSS px)
- **lead_when:** tier-2 (the human disposes durable actions — those targets must be acquirable)
- **playwright_observes:** bounding boxes of Select Baseline / Approve / Apply / Export buttons meet the WCAG 2.2 SC 2.5.8 24×24 minimum (the standards-backed floor) on the touch viewport; spacing between sequential governance targets measured.
- **proxy_limit:** WCAG 24×24 is the standards floor and is enforceable; any *stricter* product target (e.g., 44px for a high-frequency apply) is a soft recommendation, not a hard gate — applying a stricter universal number without product context is the documented anti-pattern.
- **fixture:** FX-KG-06 (compliant targets), FX-KB-06 (sub-24px apply button), FX-FP-02 (dense expert toolbar with intentionally compact secondary controls — must NOT block).

### ux.finding.layout.3 — Variant cards do not overlap or collide at narrow widths
- **layer:** L2 · **class:** hard_gate · **severity:** medium
- **source_cards:** `ux.pw.visual_comparisons`
- **lead_when:** tier-1
- **playwright_observes:** `ups-variant-grid` card bounding boxes are non-overlapping at all required viewports (1, 2, and 3 variant counts); baseline-highlighted card (`is-baseline`) remains fully visible.
- **proxy_limit:** non-overlap is geometric; whether the human can *compare* variants side-by-side (comparison breadth ≤2 pairwise per D-S1) is L4.
- **fixture:** FX-KG-01.

---

# Layer L3 — Interaction Flow (user-facing locators, task completion, visible state change)

> Hard gate. Source: `ux.pw.locators`, `ux.pw.assertions`, `ux.perception.change_blindness`. These prove the governance choreography (agent proposes → human disposes) actually works.

### ux.finding.flow.1 — Happy-path governance cycle completes via user-facing locators
- **layer:** L3 · **class:** hard_gate · **severity:** block
- **source_cards:** `ux.pw.locators`, `ux.pw.assertions`
- **lead_when:** tiers 1→2 in sequence
- **playwright_observes:** Start Session → Submit Prompt → Generate Variants → Select Baseline → Capture Comment → Synthesize Draft → Approve Draft → Apply → Revision Timeline gains an entry → Export Handoff, all driven by `getByRole`/`getByLabel`. Each step asserts a visible state change (`selectionGate`, `applyGate=satisfied`, `draftStatus`, new `ups-revision-list` row, `handoff=ready`).
- **proxy_limit:** task *completion by the script* is not task completion by a *first-time human* — the s8 naive-user lane tests whether a real user discovers this sequence. Q0/Q3/Q6 friction is L6.
- **fixture:** FX-KG-01.

### ux.finding.flow.2 — Tier-2 gates block the irreversible action until the human disposes
- **layer:** L3 · **class:** hard_gate · **severity:** block
- **source_cards:** `ux.pw.assertions`, `ux.market.nng_heuristics` (error prevention)
- **lead_when:** tier-2 (D-005: gate only on irreversible steps)
- **playwright_observes:** Apply is `disabled` until both a baseline is committed AND the draft is `approved` (`applyEnabled` false → true); the agent cannot actuate Apply with no human approval; `ups-apply-gate` reads `pending` then `satisfied`. This is the type-backed "agent has an opinion, never an unaccountable action" (D2/D-S0) made observable.
- **proxy_limit:** the gate's *presence* is deterministic; whether the gate "makes delegation psychologically affordable" (§2.8 friction claim) is L6 trust evidence, not provable here.
- **fixture:** FX-KG-01, FX-KB-07 (apply enabled before approval — must FAIL).

### ux.finding.flow.3 — Failure states (D5) preserve work and offer a single safe recovery action
- **layer:** L3 · **class:** hard_gate (for the deterministic parts) + soft_flag (for "safe to retry" comprehension) · **severity:** high
- **source_cards:** `ux.pw.assertions`, `ux.perception.change_blindness`, `ux.market.nng_heuristics`
- **lead_when:** tier-1 detect/report → tier-2 dispose recovery
- **playwright_observes:** for `GenerationFailed` / `SynthesisTimedOut` / `SourceStale` / `ApplyConflicted` — the prior prompt + the append-only `ups-comment-stream` + the draft `MutationBatch` persist (assert counts unchanged); `GateState=blocked` surfaces a reason; exactly one safe recovery control (retry / re-anchor / resolve) is offered; **no path auto-applies or auto-discards** (assert no silent state mutation).
- **proxy_limit:** Playwright proves preservation and the presence of a reason string; it cannot prove the human *believes* "safe to retry" or that anxiety/recall load is actually reduced (§2.6 load claim) — that is the L6 trust/workload residue. The "safe to retry" guarantee rests on D-002 determinism, which is a backend property tested elsewhere, not a browser observation.
- **fixture:** FX-KG-02 (each failure state with preserved work + single action), FX-KB-08 (failure that silently drops comments — must FAIL).

### ux.finding.flow.4 — Async governance state changes are perceivable (no silent transition)
- **layer:** L3 · **class:** soft_flag · **severity:** medium
- **source_cards:** `ux.perception.change_blindness`, `ux.market.nng_heuristics`
- **lead_when:** tier-1 report
- **playwright_observes:** after Generate / Synthesize / Apply, a visible busy→done transition occurs (the `busy` flag drives "Starting...", disabled states) and the `SessionStateIndicator` badge text changes; before/after screenshots captured.
- **proxy_limit:** a visible DOM change does not prove the human *noticed* it (change blindness is about attention, not DOM) — soft_flag, not gate. Salience of the transition is L4.
- **fixture:** FX-KG-01, FX-SF-02 (state changes only in an off-screen region).

---

# Layer L4 — Cognitive / Attention (density, memory burden, salience, hierarchy)

> **Soft flag / screenshot review ONLY. Never a hard gate** (claim-map rule + design R-5). Each is a conservative UI proxy + a fixture, and each names what it cannot prove. This is where the false-positive trap (FX-FP-01) matters most: the studio is an **expert tool** and density/choice-count proxies must NOT block it.

### ux.finding.cog.1 — Decision density of the seven-panel workbench
- **layer:** L4 · **class:** soft_flag · **severity:** low
- **source_cards:** `ux.cog.hick_hyman_choice_complexity`, `ux.cog.cognitive_load_theory`
- **lead_when:** tier-1 surfaces; tier-2 the human still chooses
- **playwright_observes:** counts visible peer actions per scenario-defined decision region (e.g., concurrently-enabled top-level buttons). Flags only if a *single decision region* exceeds a calibrated threshold of ungrouped peer actions.
- **proxy_limit:** a count is not cognitive load. The studio deliberately exposes many controls because expert evolution work needs them (D-006 ceiling, comparison workflows). **This proxy must be calibrated against FX-FP-01 so it does NOT fire on the legitimate dense expert layout.** It can only flag *ungrouped* density, never total control count.
- **fixture:** FX-FP-01 (false-positive trap: dense-but-legitimate expert studio — proxy must stay silent), FX-SF-03 (one region with 12 ungrouped sibling buttons — proxy may flag).

### ux.finding.cog.2 — Champion nomination reduces choice from "rank-from-scratch" to "ratify/override one"
- **layer:** L4 · **class:** soft_flag · **severity:** info
- **source_cards:** `ux.cog.hick_hyman_choice_complexity`, `ux.cog.cognitive_load_theory`
- **lead_when:** tier-1 nominate → tier-2 ratify/override (D2 / Q6, D-S1)
- **playwright_observes:** the proxy the design itself names — comparison breadth ≤2 pairwise and decision count = 1 at the selection surface; that `proposedChampionLabel` is present, non-durable, and that override and ratify cost the same number of actions (D-S1 override symmetry: both = one `SelectOrCommitBaseline`).
- **proxy_limit:** equal action-cost is observable; whether override *feels* as cheap as ratify (no automation-bias rubber-stamping) is the core L6 question s8 must answer. A green proxy here is NOT proof the paralysis is gone.
- **fixture:** FX-SF-04 (override behind an extra confirm step — proxy flags asymmetry).

### ux.finding.cog.3 — Confidence honesty: no green "held" chip on an unresolved field
- **layer:** L4 · **class:** soft_flag · **severity:** medium
- **source_cards:** `ux.perception.feature_integration`, `ux.cog.cognitive_load_theory`; standards-adjacent via false-trust risk
- **lead_when:** tier-1 (the chip honesty is structural, D-S2)
- **playwright_observes:** on the Identity Evidence / conformance-delta surface, asserts that a delta on a `TypedReference`-pending field (Motion/Interaction/State/Feedback/Numeric per R-7) renders a `confidence<1.0` / `pending` chip, never a confident "held" chip. The mapping from confidence value → visual chip is deterministic and checkable.
- **proxy_limit:** Playwright can check the chip matches the confidence value (a structural invariant), but whether the human *correctly distrusts* a low-confidence chip is L6. **Surface not yet implemented** (no IdentityEvidencePanel.tsx) → this is a forward check; today's proxy_limit is "cannot observe, surface absent."
- **fixture:** FX-SF-05 (pending field shown with a confident green chip — proxy flags false trust).

### ux.finding.cog.4 — Cross-step memory burden: prior selections stay visible
- **layer:** L4 · **class:** soft_flag · **severity:** low
- **source_cards:** `ux.cog.working_memory_capacity`, `ux.cog.cognitive_load_theory`
- **lead_when:** tier-2 (recognition over recall — registry/§2.4 anchor)
- **playwright_observes:** after navigating the cycle, the committed baseline (`ups-baseline-badge`), the locked constrain fields, the open draft status, and the append-only comment stream remain visible without recall; flags if a prior durable selection is hidden after a state transition.
- **proxy_limit:** DOM visibility approximates but does not measure memory burden; chunking and expertise vary (claim-map). Soft_flag only.
- **fixture:** FX-SF-06 (baseline badge hidden after synthesize — proxy flags).

### ux.finding.cog.5 — Salience of the irreversible Apply gate vs decorative regions
- **layer:** L4 · **class:** screenshot_review · **severity:** medium
- **source_cards:** `ux.perception.saliency_model`, `ux.perception.visual_attention_review`
- **lead_when:** tier-2 (the irreversible disposal)
- **playwright_observes:** captures the Mutation Approval region; produces a salience/contrast annotation comparing the Apply gate against competing louder regions. Emits a reviewer prompt: "FLAG: is the irreversible Apply action at least as visually prominent as secondary export/refresh controls?"
- **proxy_limit:** computational salience does NOT prove where the human looks (no eye tracking) — screenshot_review, human inspects. Never a gate.
- **fixture:** FX-SR-01 (apply gate quieter than a decorative promo block — reviewer should flag).

### ux.finding.cog.6 — Distinctiveness of failure/blocked state (feature integration)
- **layer:** L4 · **class:** screenshot_review · **severity:** medium
- **source_cards:** `ux.perception.feature_integration`, `ux.perception.guided_search`
- **lead_when:** tier-1 report
- **playwright_observes:** captures each D5 failure state; flags low-distinctiveness blocked/error states (state badge `ups-state-badge--<state>` not visually distinct from the happy badge; relies on text only).
- **proxy_limit:** distinctiveness in a screenshot is not noticed-ness; needs human review. The badge currently differentiates by CSS class only — whether the failure badge is *perceptibly* different is a review judgment.
- **fixture:** FX-SR-02 (failure badge identical color to running badge).

---

# Layer L5 — Domain Practice (design-system rule packs)

> Soft flag, behind explicit domain tags. Source: `ux.market.nng_heuristics`, `ux.market.uswds_accessibility`, `ux.market.carbon_accessibility`. The studio domain tag is **authoring / data-tool**, NOT ecommerce — so `ux.market.baymard_research` is OFF (its activation would be a domain-mismatch false positive).

### ux.finding.dom.1 — NN/g heuristic checklist: status visibility, control, recovery, recognition
- **layer:** L5 · **class:** soft_flag · **severity:** low
- **source_cards:** `ux.market.nng_heuristics`
- **lead_when:** spans tiers
- **playwright_observes:** asserts the presence of system-status surfaces (`SessionStateIndicator`, gate badges), user-control affordances (cancel/discard on failures, override on champion), undo-equivalents (durable-not-irreversible reject per D-S3), and recognition aids (visible baseline/components). Produces a heuristic-review prompt, not a pass/fail.
- **proxy_limit:** heuristics guide expert review; presence of a status region is not proof of *good* status communication. Never a gate.
- **fixture:** FX-KG-01 + reviewer checklist.

### ux.finding.dom.2 — Design-system component fidelity across states (Carbon/USWDS practice)
- **layer:** L5 · **class:** soft_flag · **severity:** low
- **source_cards:** `ux.market.carbon_accessibility`, `ux.market.uswds_accessibility`
- **lead_when:** tier-1
- **playwright_observes:** for reused components (buttons, selects, the apply dialog once built), captures a state matrix (default/hover/focus/disabled/error) and verifies role/name/state + visible label persist across states; flags if a custom variant drops documented behavior.
- **proxy_limit:** design-system guidance must be mapped to *this* component library; a generic rule is not release-blocking law (anti-pattern). The studio uses bespoke `ups-button` classes, so this is advisory.
- **fixture:** FX-SF-07 (disabled state loses accessible name).

### ux.finding.dom.3 — Recognition-over-recall for reused `UIElementIdentity` nodes
- **layer:** L5 · **class:** soft_flag · **severity:** info
- **source_cards:** `ux.market.nng_heuristics` (recognition), `ux.cog.working_memory_capacity`
- **lead_when:** tier-2 (registry §2.4 ergonomic anchor)
- **playwright_observes:** asserts that `componentsUsed` labels on variant cards reuse stable identity names across cycles (same concept → same visible name), not novel strings each run.
- **proxy_limit:** name stability is observable; whether the human *recognizes* the component is L6. **Registry persistence entity is residue (R-1)** — this check can only run once that lands.
- **fixture:** FX-SF-08 (same component renamed each cycle — proxy flags).

---

# Layer L6 — Human Evidence (workload, comprehension, trust, real task success)

> **Human-study residue. Cannot be automated as pass/fail.** Playwright only *prepares supporting evidence* (scripts, timing, traces, screenshots). Source: `ux.cog.nasa_tlx`, `ux.market.govuk_user_research`, `ux.std.wcag_em`. This is the home of design R-5 (the entire ergonomics floor is unproven) and Q0/Q3/Q6.

### ux.finding.human.1 — Does a first-time human discover the agent-proposes/human-disposes boundary (Q0)?
- **layer:** L6 · **class:** human_study · **severity:** high
- **source_cards:** `ux.market.govuk_user_research`, `ux.cog.nasa_tlx`
- **lead_when:** the whole tier matrix (D-S0)
- **playwright_observes:** records the task script + timing + trace as inputs to the s8 study. Observes nothing about comprehension.
- **proxy_limit:** automation cannot tell whether the human *understands* who leads when, or *trusts* the gate enough to let the agent run free in tier-1. This is the load-bearing first-principle claim and it is **unproven by design (R-5)**; s8 is the live test.
- **fixture:** N/A (human protocol; supporting evidence = FX-KG-01 trace).

### ux.finding.human.2 — Is the irreversible Apply confirmation registered, not rubber-stamped (trust/automation bias)?
- **layer:** L6 · **class:** human_study · **severity:** high
- **source_cards:** `ux.cog.nasa_tlx`, `ux.market.nng_heuristics`
- **lead_when:** tier-2 irreversible
- **playwright_observes:** can time the dwell before Apply and capture the screen; cannot infer whether the human read the consequence.
- **proxy_limit:** dwell time is not comprehension; automation bias (D-S1 risk) is a subjective-trust claim requiring moderated observation.
- **fixture:** N/A.

### ux.finding.human.3 — Workload of the evolution cycle vs the friction it claims to remove
- **layer:** L6 · **class:** human_study · **severity:** medium
- **source_cards:** `ux.cog.nasa_tlx`
- **lead_when:** spans tiers
- **playwright_observes:** persists step count, error count, task timing as workload-study inputs.
- **proxy_limit:** perceived workload requires the NASA-TLX instrument; DOM metrics cannot infer it. The §2 "load" and "friction" claims are hypotheses until measured.
- **fixture:** N/A.

### ux.finding.human.4 — Representative-scenario coverage (WCAG-EM)
- **layer:** L6 · **class:** human_study · **severity:** medium
- **source_cards:** `ux.std.wcag_em`
- **lead_when:** N/A
- **playwright_observes:** can enforce that the scenario matrix names representative states/viewports/paths; cannot prove untested states are accessible.
- **proxy_limit:** a scenario matrix structures evidence; it does not prove unvisited panel states (e.g., every D5 failure × every viewport) are conformant. Owner: s8 + manual auditor.
- **fixture:** N/A (matrix definition lives in the fixture plan scenario list).

---

# Not-automatable / residue

### ux.finding.na.1 — Semantic correctness of enum/token binding (D-XC / R-4)
- **layer:** L1-adjacent · **class:** not_automatable · **severity:** info
- **source_cards:** `ux.std.wcag22` (informative), design D-XC
- **playwright_observes:** can prove **shape** (no raw px/color; every `UIVisualSignature` field resolves to a controlled-vocab enum or a `TypedReference`) — that is a legitimate L1/L5 shape gate.
- **proxy_limit:** which enum is *meaningfully correct* is human-confirmed (`ConfirmUIDecisionEvidence`); the W3C-DTCG caveat (token group names not semantically load-bearing) means a machine must never judge meaning. **Hard gate on shape only; meaning is not_automatable — by design.**

---

## Layer coverage + classification summary

| Layer | Hard gate | Soft flag | Screenshot review | Human study | Not automatable |
|---|---|---|---|---|---|
| L0 Smoke | 2 | — | — | — | — |
| L1 Accessibility | 4 | 1 | — | — | 1 (shape-only carve-out) |
| L2 Layout | 3 | — | — | — | — |
| L3 Interaction | 2 | 2 | — | — | — |
| L4 Cognitive | — | 4 | 2 | — | — |
| L5 Domain | — | 3 | — | — | — |
| L6 Human | — | — | — | 4 | — |

**Net:** 11 hard gates (all deterministic/standards-backed), 10 soft flags, 2 screenshot reviews, 4 human-study residues, 1 not-automatable carve-out.

## Promotion gate status (per sigil promotion-gate)
- **Status: FLAG / seed-spec.** Hard gates are *specified and source-backed* but NOT yet promoted: no fixture corpus is implemented, no calibration run has been executed, and two hard gates (a11y.4 apply-modal, and the conformance-delta surface for cog.3 / dom.3) are **blocked on missing implementation** — the `ApplyApprovedBatch` modal and the Identity Evidence Panel do not exist in the current tree.
- **Blocking residue carried forward:**
  1. **a11y.4** — irreversible Apply gate has no dialog/focus-trap (design §2.5 vs `MutationApprovalPanel.tsx`). Owner: web-core — implement the modal or amend the design.
  2. **a11y.5** — disabled-reason exists in the DOM but is not `aria-describedby`-associated to its control. Owner: web-core.
  3. **Identity Evidence Panel absent** — cog.3 (confidence honesty) and dom.3 (recognition) cannot be observed until the conformance-delta surface is built. Owner: s9.
  4. **R-5 ergonomics floor** — every L4/L6 claim is unproven; s8 naive-user lane is the live test of Q0/Q3/Q6. No ergonomic gain is asserted as proven here.
- **Next lifecycle step:** build the fixture corpus in `UX-FIXTURE-PLAN.md` (key_points), then run `calibrate` so each hard gate fires on its known-bad and stays silent on FX-FP-01 / FX-FP-02 before any gate blocks CI.
