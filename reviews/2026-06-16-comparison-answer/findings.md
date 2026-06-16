# findings.md — review of the dispatch-spec vs domainspec-subagents-strategy comparison answer

Dispatch: `2026-06-16-comparison-answer-review` · target: `reviews/2026-06-16-comparison-answer/target.md`
Verified against literal artifacts in `.claude/skills/dispatch-spec/SKILL.md`, `.claude/skills/domainspec-subagents-strategy/SKILL.md`, `.claude/skills/review/SKILL.md`, `.claude/skills/check-tension/SKILL.md`.

Findings cluster into two classes: **(A) non-licensing / misattributed cites** and **(B) framing overreach** (peer relationship rendered as hierarchy). Severity: CRITICAL = contradicts governing law / corrupts a record; MAJOR = load-bearing overreach or substantive cite error; MINOR = wording.

## Surviving findings

| # | class | quoted target evidence | what the artifact actually says (file) | severity | proposed fix |
|---|---|---|---|---|---|
| 1 | A | "That handoff is **precisely where domainspec-subagents-strategy takes over** and runs its gated lifecycle." | dispatch-spec L104-106: "it does **not** execute subagents. The orchestrating capability, **usually Refine**, must show the strategy … and ask permission." dispatch-spec never names domainspec-subagents-strategy as the handoff target. | **MAJOR** | "…hands off to the orchestrating capability (usually **Refine**), which shows the strategy and asks permission. A subagent fan-out it then triggers would separately be governed by domainspec-subagents-strategy." |
| 2 | B | "two layers of the same pipeline … dispatch-spec → governs the PIPELINE … domainspec-subagents-strategy → governs ONE STAGE inside that pipeline"; "dispatch-spec is the **outer contract**, domainspec-subagents-strategy is the **governed engine for one step in it**" | Neither SKILL establishes containment. dispatch-spec "does not decide which sigils should be used" (L31); domainspec-subagents-strategy "defines no field and no type-specific judgment — it routes" (L3). They are **peers under a shared register-dispatch/constitution stack**, joined only by a recommend→handoff-to-orchestrator seam. | **MAJOR** *(verifier: MAJOR/MINOR boundary — the target half-hedges this under "the mental model that makes it click"; FIX verdict unaffected since #1/#3 are unambiguous MAJORs)* | Mark as analogy, not fact: "One way to *picture* the relation (stated by neither skill): …". Replace "outer contract / governed engine for one step" with "peers under a shared constitution; dispatch-spec can recommend a subagent strategy that a separate dispatch then governs." |
| 3 | A | "Does it execute? No — it only validates shape; **returns pass/flag/block (L31-32)**" | dispatch-spec L31-32 is scope prose ("does not decide which sigils … checks whether a composition is explicit enough"). The pass/flag/block contract is at **L148 (Output Contract)** and **L166-169 (Failure Policy)**. | **MAJOR** | Re-point the cite to L148 / L166-169. (Same class as #1: a line-accurate-looking cite that does not license the claim.) |
| 4 | B | "domainspec-subagents-strategy **governs** a subagent dispatch"; "the **governed engine**" | Self-describes as a ROUTER (L3); type judgment owned by research/review/experiment, fields by constitution §5 / register-dispatch. | MINOR | "routes/gates a subagent dispatch (judgment owned by the type skill)". |
| 5 | A | "Quality mechanism: **The check-tension gate** …" listed as domainspec-subagents-strategy's own | check-tension is a **separate skill** the router points to (sub-strat L56 Pointers → `check-tension/SKILL.md`; check-tension L12: "owns no field and no type judgment"). The router *invokes* it. | MINOR | "invokes the check-tension gate (a separate skill it points to)". |
| 6 | A | "Formulae — a deterministic validator **(SKILL L11-29)**" | tier is at L11; the "Deterministic Validator" section is **L56-68**. L11-29 is frontmatter + Identity/Purpose. | MINOR | Cite "(tier: L11; Deterministic Validator: L56-68)". |
| 7 | B | "Human gate: **None inherent — it's a linter**" (dispatch-spec) | Substantially true for invoking the skill, but Rule 22 (L93) mandates `authorization=requires_user_permission` on any subagent block — dispatch-spec **flags/blocks** routes that bypass the human gate on subagents. | MINOR | Footnote: "still a linter, but it *enforces* `requires_user_permission` on subagent routes (Rule 22)." |

## Dropped / not findings (verified accurate — claim ≤ proof upheld)

- **"25 numbered validation rules + a Python validator script"** — VERIFIED: exactly 25 rules (dispatch-spec L72-96); validator exists at BOTH `.claude/skills/dispatch-spec/scripts/validate-dispatch.py` and `arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py` (byte-identical, 28.2K). The claim is **true**; the initial "wrong path" suspicion was withdrawn after empirical ls.
- **"A router — routes a dispatch to a type skill (L1-4)"** — accurate (sub-strat L3).
- **"synthesis / context-protection / isolation / parallelism (P1) (L10)"** — accurate (L10).
- **"one mandatory human confirm before agents run (L17)"** — accurate (L17).
- **"subagent_strategy block (L98-120)"** — line range accurate (the *attribution chained to it* is finding #1, not the cite of the block's existence).
- **"research/review/experiment LIVE"** — accurate (L43/45/48), incl. the RESERVED set.

## Per-artifact verdict

**target.md → FIX** (≥ 1 MAJOR survives: findings #1, #2, #3).

The answer's *facts* are largely sound (tier, 25 rules, human-gate contrast, P1 triggers, LIVE table, the "A router" row). The defects cluster on **one invented structure**: target.md renders two peer skills as an outer/inner pipeline hierarchy (#2, #4) and, at the load-bearing "connection point," misattributes dispatch-spec's handoff — which goes to the orchestrator (usually Refine) — to domainspec-subagents-strategy (#1), citing a line that proves only the block's existence. A parallel non-licensing cite (#3, pass/flag/block at L31-32) confirms the authoring pattern was cite-from-memory.

## Change-request list (ordered by severity)

1. **[MAJOR #1]** Fix the handoff sentence: dispatch-spec hands off to the orchestrator (usually **Refine**), not to domainspec-subagents-strategy; the latter separately governs a subagent fan-out the orchestrator may trigger.
2. **[MAJOR #2]** Demote the "two layers / outer-contract / governed engine for one step" framing from asserted fact to explicit analogy; state the skills are peers under a shared constitution.
3. **[MAJOR #3]** Re-point the "pass/flag/block" cite from L31-32 to L148 / L166-169.
4. **[MINOR #4]** "governs / governed engine" → "routes / gates" for the router.
5. **[MINOR #5]** check-tension: "invokes (a separate skill it points to)", not owns.
6. **[MINOR #6]** Fix the "deterministic validator" cite to L56-68.
7. **[MINOR #7]** Footnote the dispatch-spec Rule 22 subagent gate.

Net: the comparison is *directionally correct and useful* (the core "validates a route" vs "governs a subagent dispatch" distinction holds), but three MAJOR fixes are needed before it should be reused as reference — chiefly the Refine-handoff misattribution.
