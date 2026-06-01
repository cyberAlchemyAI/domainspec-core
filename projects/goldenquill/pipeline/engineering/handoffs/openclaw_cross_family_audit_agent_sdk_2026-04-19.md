# OpenClaw Handoff — Cross-Family Re-Audit of Agent SDK Thesis (2026-04-19)

**Purpose:** Promote the Agent SDK amendment set from `LOCKED-internal-simulated` to `LOCKED-sealed` by running live cross-family audits on OpenClaw. The simulated Thesis was ventriloquized from a single Anthropic-family voice; L-003 requires reviewer family ≠ author family.

**Author family:** Anthropic (Cowork / Claude)
**Reviewer families required:** any non-Anthropic per `router.yaml` seven-family taxonomy — Meta (Llama), Alibaba (Qwen), OpenAI-OSS (GPT-OSS), Moonshot (Kimi), Google (Gemini), Mistral, OpenAI. Three reviewers drawn from three distinct non-Anthropic families satisfies L-003.

---

## Orientation (every reviewer runs these first, by path, not content dump)

- `pipeline/SESSION_BOOTSTRAP.md`
- `/SOUL.md`
- `/USER.md`
- `/router.yaml`
- `/AGENTS.md`
- `/lessons.md`

## Input artifacts to audit (by path)

- `pipeline/engineering/agent_sdk_exploration.md` — the original exploration
- `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/00_debate_and_consensus.md` — the simulated Thesis trail
- `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/EN-001_sdk_scribe_spike_2026-04-19.md` — deferred queue entry
- `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/EN-002_sdk_lifecycle_vocabulary_2026-04-19.md` — documentation hygiene amendment
- `pipeline/engineering/references/sdk_lifecycle_map.md` — the version-pinned mapping table

## Per-reviewer task

### Editor (clarity, accessibility)

**Invocation:** `openclaw infer model run --gateway --model groq/llama-3.3-70b-versatile --prompt "<prompt>" --json`
**Output:** `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/cross_family_audit/editor_verdict_cycle1.md`
**Format:** structured feedback (not verdict format — Editor is exempt per A3).
**Focus:** Is this readable to a grant writer who does not code? Is any jargon unexplained? Is the amendment surface declarative and present-tense? Are the rejected-patterns declared plainly or hidden behind hedging?

### Judge (rubric scoring, SFR three-block)

**Invocation:** `openclaw infer model run --gateway --model google/gemini-2.5-pro --prompt "<prompt>" --json` *(Judge swapped from groq/qwen/qwen3-32b to google/gemini-2.5-pro on 2026-04-19; see router.yaml commentary + lessons.md L-009 + pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/EN-003_code_thesis_committee_kimi_replacement_2026-04-19.md)*
**Output:** `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/cross_family_audit/judge_verdict_cycle1.md`
**Format:** A3 SFR — Premises (with file:line citations) / Execution trace (citing premises by ID) / Conclusion (grounded only in declared premises + trace).
**Rubric:** 5 dimensions × 20 pts = 100 — scope clarity, reversibility cost, cross-family rigor preservation, Cedar/Logician integration, sovereignty/BYOK preservation. Flag disagreement with simulated Cycle 2 score of 96/100.

### Red Team (adversarial challenge, SFR three-block)

**Invocation:** `openclaw infer model run --gateway --model groq/openai/gpt-oss-120b --prompt "<prompt>" --json`
**Output:** `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/cross_family_audit/red_team_verdict_cycle1.md`
**Format:** A3 SFR, severity-tagged findings (HIGH / MED / LOW).
**Focus:** What did the simulated Red Team miss? Premature optimization, vendor lock-in, sovereignty leaks, reversibility costs, dependency surface drift, Cedar-displacement risk, queue-jump risk. If the simulated Cycle 2 closed all findings as zero-in-scope, challenge that specifically — a live reviewer should find things a ventriloquized one did not.

## Synthesis step (after all three verdicts land)

**Output:** `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/cross_family_audit/synthesis.md`

Columns:
- Agreement with simulated debate: items all three reviewers confirmed
- Dissent: items reviewers flagged that the simulated debate did not
- Revision required: specific text-level fixes in EN-001, EN-002, or `sdk_lifecycle_map.md`
- Promotion recommendation: `LOCK-SEALED` / `CYCLE-2-REQUIRED` / `ESCALATE-TO-OPERATOR`

## Promotion gate

- All three reviewers READY + zero dissent + zero revision required → `LOCK-SEALED`, awaiting operator signature.
- Any REQUIRES_FIX → Cycle 2 re-simulation + second cross-family pass.
- Any BLOCKING → escalate to operator; no auto-retry.

## Budget

- Each verdict ≤ 1000 output tokens.
- Use `pipeline/templates/component_analysis_template.md` as structural reference.
- Per L-002: reference files by path, never paste content.

## CLI shape notes (verified 2026-04-19 against OpenClaw 2026.4.14)

- Always pass `--gateway`. The `--local` path hangs; default (no flag) path hits a stale CLI-local allowlist.
- Use **full provider/model ids**. The alias system (e.g., `--model editor`) currently resolves incorrectly to `anthropic/<alias>`. Known issue; use model ids until fixed.
- The `--provider <X> --role <Y>` form in AGENTS.md is obsolete in 2026.4; the `--model` value carries the provider prefix.
- Allowlist prerequisite: `agents.defaults.models` in `~/.openclaw/openclaw.json` includes the three Groq reviewer model ids. Verify with `openclaw config get agents.defaults.models --json`.

## Done definition

- Three cycle-1 verdicts written to the paths above.
- Synthesis written.
- Status of each amendment updated in `00_debate_and_consensus.md` with a cross-family-audit footer row.
- If LOCK-SEALED reached: operator-signature line appended to each amendment (signature is Josh's to apply; the line is prepared, not signed).
