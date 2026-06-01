# OpenClaw Handoff — Cross-Family Re-Audit of TSIP v0.1

**Purpose:** Promote the Tilth Self-Improvement Protocol (TSIP) from `LOCKED-internal-simulated` to `LOCKED-sealed` by running live cross-family audits on OpenClaw. The bootstrap Thesis was ventriloquized from a single Anthropic-family voice; L-003 requires reviewer family ≠ author family.

**Author family:** Anthropic (Cowork / Claude)
**Reviewer families required:** three distinct non-Anthropic families per the seven-family taxonomy (Anthropic, OpenAI, OpenAI-OSS, Alibaba, Meta, Moonshot, Google — defined in A2 addendum at `pipeline/architecture/v0.1/tilth_architecture_locked.md` + `router.yaml`).

---

## Orientation (every reviewer runs these first, by path, not content dump)

- `pipeline/SESSION_BOOTSTRAP.md`
- `/SOUL.md`
- `/USER.md`
- `/router.yaml`
- `/AGENTS.md`
- `/lessons.md`
- `/CLAUDE.md`
- `pipeline/engineering/da_vinci_engineer_prompt_v2.md` (§13 real-engineer validator gate)

## Input artifacts to audit (by path)

- `pipeline/engineering/protocols/tilth_self_improvement_protocol_v0.1.md` — the canonical protocol
- `pipeline/engineering/protocols/tsip_v0.1_thesis_2026-04-19/00_bootstrap_thesis.md` — the simulated bootstrap Thesis trail

## Per-reviewer task

### Editor (clarity, accessibility)

**Invocation:** `openclaw infer model run --gateway --model groq/llama-3.3-70b-versatile --prompt "<prompt>" --json`
**Output:** `pipeline/engineering/protocols/tsip_v0.1_thesis_2026-04-19/cross_family_audit/editor_verdict.md`
**Format:** structured feedback (not verdict format — Editor is exempt per A3).
**Focus:** Is this readable to someone who does not build LLM systems? Are the eight phases distinguishable? Do the resolved-decisions map cleanly to the prose? Any jargon unglossed? Is the bootstrap-exception clause self-consistent?

### Judge (rubric scoring, SFR three-block)

**Invocation:** `openclaw infer model run --gateway --model google/gemini-2.5-pro --prompt "<prompt>" --json` *(Judge swapped from groq/qwen/qwen3-32b to google/gemini-2.5-pro on 2026-04-19; see router.yaml commentary + lessons.md L-009)*
**Output:** `pipeline/engineering/protocols/tsip_v0.1_thesis_2026-04-19/cross_family_audit/judge_verdict.md`
**Format:** A3 SFR — Premises (with file:line citations) / Execution trace (citing premises by ID) / Conclusion (grounded only in declared premises + trace).
**Rubric:** 5 dimensions × 20 pts = 100 — scope clarity, self-consistency, discipline alignment (L-002 / L-003 / L-005 / Da Vinci §13 / Sovereignty Promise), enforceability, completeness.
**Benchmark:** simulated Cycle 2 score was 95/100. Disagreement welcome; flag any dimension where a live reviewer scores lower.

### Red Team (adversarial challenge, SFR three-block)

**Invocation:** `openclaw infer model run --gateway --model groq/openai/gpt-oss-120b --prompt "<prompt>" --json`
**Output:** `pipeline/engineering/protocols/tsip_v0.1_thesis_2026-04-19/cross_family_audit/red_team_verdict.md`
**Format:** A3 SFR, severity-tagged findings (HIGH / MED / LOW).
**Focus areas:**
- Self-referential safety: does TSIP's bootstrap exception create a loophole for future self-modifications?
- Enforceability: anti-patterns are declared but not gated — is operator-discipline sufficient, or does this need Logician gates?
- Scope creep: does any phase's output path risk polluting areas outside `pipeline/engineering/`?
- Sovereignty drift: does any channel in Phase 1 Surveillance create a phone-home risk?
- Cross-family rigor: does Phase 5 correctly forbid same-family reviewer selection, or can it be gamed?
- Completeness: what's missing? What breaks when TSIP is actually used on a real candidate?

## Synthesis step (after all three verdicts land)

**Output:** `pipeline/engineering/protocols/tsip_v0.1_thesis_2026-04-19/cross_family_audit/synthesis.md`

Columns:
- Agreement with simulated Thesis: items all three reviewers confirmed
- Dissent: items reviewers flagged that the simulated Thesis did not
- Revision required: specific text-level fixes in `tilth_self_improvement_protocol_v0.1.md`
- Promotion recommendation: `LOCK-SEALED` / `CYCLE-2-REQUIRED` / `ESCALATE-TO-OPERATOR`

## Promotion gate

- All three reviewers READY + zero dissent + zero revision required → `LOCK-SEALED`, awaiting operator signature
- Any REQUIRES_FIX → Cycle 2 re-simulation + second cross-family pass
- Any BLOCKING → escalate to operator; no auto-retry

## Budget

- Each verdict ≤ 1000 output tokens
- Use `pipeline/templates/component_analysis_template.md` as structural reference
- Per L-002: reference files by path, never paste content

## CLI shape notes (verified 2026-04-19 against OpenClaw 2026.4.14)

- Always pass `--gateway`. The `--local` path hangs; default (no flag) path hits a stale CLI-local allowlist.
- Use **full provider/model ids**. The alias system (e.g., `--model editor`) currently resolves incorrectly to `anthropic/<alias>`. Known issue; use model ids until fixed.
- The `--provider <X> --role <Y>` form in AGENTS.md is obsolete in 2026.4; the `--model` value carries the provider prefix.
- Allowlist prerequisite: `agents.defaults.models` in `~/.openclaw/openclaw.json` includes the three Groq reviewer model ids. Verify with `openclaw config get agents.defaults.models --json`.

## Done definition

- Three Cycle-1 verdicts written
- Synthesis written
- Protocol header updated with cross-family-audit footer row
- If LOCK-SEALED reached: operator-signature line prepared (signature is Josh's to apply)
