---
scope: workspace-wide
inherits: none
inherited_by: all agents entering this workspace
last_updated: 2026-04-14
---

# Workspace AGENTS — Wake-Up Sequence

Every agent entering this workspace — Tilth seats (Scout, Scribe, Editor, Judge, Logician), Sentinel, any future agent — runs the same wake-up sequence before accepting its first task. Agent-specific AGENTS.md files add role-specific overrides but do NOT re-state this sequence.

## Wake-Up Sequence (every session start)

Run in order. Each step is non-optional.

1. **Read `/SOUL.md`** — workspace-wide operating principles. The Five Laws and Four Autonomy Rules are canonical from this file.
2. **Read `/USER.md`** — Josh's identity, working style, decision framework, locked decisions, active client ecosystem.
3. **Read `/router.yaml`** — current seat-to-model bindings. Never hardcode model names from memory; always consult this file.
4. **Read the last two entries in `/daily_logs/`** — recent decisions, corrections, and context that has not yet crystallized into a lesson or a memory file.
5. **Read `/lessons.md`** — accumulated operational lessons. High-frequency + high-severity lessons are mandatory pre-checks.
6. **Read MEMORY.md** (the index under the Cowork memory path, or the agent's own memory index if operating outside Cowork) — scan titles and one-line hooks; open the specific memory files relevant to the current task. Then run `scripts/memory_size_check.sh` (or `python -m pipeline.cli.tilth_memory auto-trigger`) as a preflight against the early-warning threshold (default 200 lines / 12 KiB). Exit code 10 means the file has grown past the early-warning band — invoke the `consolidate-memory` skill, or re-run with `--run` to consolidate inline before continuing. Exit code 0 means under threshold; proceed. The trigger logs every fired event to `pipeline/institutional_memory/memory_consolidation_log.jsonl`.
7. **Read agent-specific overrides** — if the task is scoped to an agent folder (e.g., `HeartbeatQAfiles/` for Sentinel, `Sovereign_Node_Handoff/` for Tilth council seats), read that folder's SOUL.md / USER.md / AGENTS.md. Those files layer on top of the workspace files — they do not replace them.
8. **Read the task-specific PROJECT_CONTEXT.md** — if the task touches a client org, read ONLY that org's PROJECT_CONTEXT.md under `/orgs/<org>/`. Law 3: never cross-reference other orgs.

Only after steps 1–8 does the agent respond to the first task.

## Compaction Survival

On any mid-session compaction event, the immediate next action is to re-run steps 1, 2, and 3 (SOUL, USER, router) verbatim before proceeding. Compaction summaries are narrative; these three files are canonical. Do not trust a compacted recollection of a law or a model binding — re-read.

## Save-On-Decide

On any new decision, correction, or non-obvious judgment call from Josh, write it IN THE SAME TURN to one of:

- `/daily_logs/YYYY-MM-DD.md` — append a bullet under today's date
- `/lessons.md` — add or increment an L-NNN entry if this is a repeat pattern
- Cowork memory file — if the fact is user/feedback/project/reference shaped and will apply to future conversations

Do not batch to end-of-session. What isn't written isn't remembered.

## Model References

Never write "Claude Sonnet 4.6" or "Gemini 2.5 Pro" into an identity, memory, or plan document. Always write the seat name and point the reader to `/router.yaml`. When providers ship flagships or Josh changes a paid tier, only `router.yaml` changes — everything else stays stable.

## Deployment Posture Vocabulary

Per architecture v7.0.10 LOCKED 2026-05-11, Tilth's customer-facing deployment-posture vocabulary is exactly three values: **Frontier-Eligible**, **Split-Context Hybrid**, **Local-Only / Sovereign** (the last carries an under-validation caveat until SN-LLC quarterly validation flips the deployment-manifest `local_only_validated` flag). The earlier "Sanitized" / opaque-slot-token posture is deprecated. The `F-CLASS-SLOT-ID-NON-OPAQUE` + `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED` gates remain live as defense-in-depth (firing = bug or attack). When writing for any customer-facing or engineer-facing surface, use the three-posture vocabulary; do not revive "Sanitized" except as a deprecation footnote. Full spec in `pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md`.

## Agent Invocation Hygiene

Three rules govern how agents in this workspace invoke other agents (Cowork → OpenClaw, OpenClaw → OpenClaw, any agent → any provider API). They are enforced by whoever is composing the invocation, not by whoever is receiving it.

### Path references, never content dumps

Agents with file access read files from disk via their file tools. Never paste file contents into a prompt, a `--message` body, or a system-prompt preamble to "save the agent a step." Pasted content inflates input tokens every turn and burns provider rate limits. The migration-plan incident of 2026-04-14 consumed most of the 30K input-TPM ceiling in a single call and rate-limited the next call to zero output.

Rule: reference by path. Let the agent read. Exception: snippets under ~50 lines where the content is genuinely the subject of the turn.

### Cross-family review — reviewer's model family must differ from author's

When a document, plan, draft, or output is reviewed adversarially, the reviewer's model family must not match the author's. Cowork (Anthropic / Claude) authored → review through Groq (meta-Llama, alibaba-Qwen, openai-oss-GPT-OSS), Google (Gemini 2.5 Pro / 2.5 Flash), or OpenAI direct (GPT-5.1). OpenClaw Scribe (Anthropic) drafted → review through Judge (Gemini 2.5 Pro, Google family, as of 2026-04-19) and Red Team (GPT-OSS 120B, OpenAI-OSS family), per `router.yaml`. Moonshot / Kimi K2 paths are deprecated (Groq removed them 2026-03-23).

Default agent-invocation paths (`openclaw agent --agent tilth`) hit the agent's *primary* model, which for Tilth is Anthropic. That silently bypasses the cross-family routing. For adversarial reviews, override explicitly. The real CLI shape as of OpenClaw 2026.4.14 is:

    openclaw infer model run --gateway --model <provider/model-id> --prompt "<text>" --json

(The older `--provider X --model Y --role Z` form is obsolete; the `--model` value now carries the provider prefix.) Examples:

    openclaw infer model run --gateway --model groq/openai/gpt-oss-120b --prompt "..."  --json  # Red Team
    openclaw infer model run --gateway --model google/gemini-2.5-pro      --prompt "..."  --json  # Judge
    openclaw infer model run --gateway --model groq/llama-3.3-70b-versatile --prompt "..." --json # Editor

Alternatively, invoke a dedicated adversary agent whose primary model is pinned to a non-Anthropic family. Always use full `provider/model-id`; the `--model <alias>` form currently resolves incorrectly to `anthropic/<alias>` (known upstream bug).

Before requesting pushback, ask: what model family wrote this, and what model family is about to critique it? If they match, the review is stylistic variance, not an audit.

### Cross-family review — bridge pattern (Cowork → Mac → openclaw gateway)

The Cowork sandbox is Linux-cloud and cannot reach the Mac-local `openclaw` CLI directly (separate filesystems, no localhost reach, no `~/.openclaw/` mount). The bridge from a Cowork session into the Mac shell is `mcp__Control_your_Mac__osascript`:

    osascript -e 'do shell script "/bin/bash -lc '\''PATH=$HOME/.npm-global/bin:$PATH openclaw infer model run --gateway --model google/gemini-2.5-pro --prompt \"…\" --json'\''" with timeout of 600 seconds'

Two non-obvious bits the bridge requires:
- **PATH prefix.** The osascript shell does not inherit Josh's interactive PATH; prefix `PATH=$HOME/.npm-global/bin:$PATH` (extend with `/opt/homebrew/opt/node/bin:/opt/homebrew/bin:/usr/local/bin` if calling node-backed tools too).
- **Timeout extension.** Default `do shell script` timeout (~120s) is exceeded by Gemini 2.5 Pro thinking-mode runs. Extend with `with timeout of 600 seconds`.

**Three model IDs proven live on the gateway** (per WS-D v7.0.5 cross-family Thesis round, 2026-05-10 — six successful cycle-1+cycle-2 calls captured at `pipeline/validation/v7_0_5_thesis_2026-05-09/audit_v{1,2}_{editor,judge,red_team}.raw.json`, all bearing `"transport": "gateway"` and `"ok": true`):

- Editor (Meta family): `groq/llama-3.3-70b-versatile`
- Judge (Google family): `google/gemini-2.5-pro`
- Red Team (OpenAI-OSS family): `groq/openai/gpt-oss-120b`

**Working dispatch templates on disk:**

- `pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v1.sh` — Cycle 1 dispatcher (per-seat prompt build → openclaw call → JSON-text extraction → `audit_v1_<seat>.md` writer)
- `pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v2.sh` — Cycle 2 verification dispatcher (same shape, post-fix prompt body)

Clone these to a sibling `pipeline/validation/<your_round>/` directory; only the AMENDMENT path, the per-seat task tail, and the output filenames change. Both scripts already encode the three live model IDs above.

### Section E carve-out — invocation discipline

The Section E single-Claude carve-out (per architecture v7.0.4 LOCK precedent) is for **logged dispatch failures**, not a default fallback. Cross-family is the default posture for every Thesis round.

To invoke Section E, the session must first attempt cross-family dispatch and document the failure in the audit trail. Acceptable evidence: the captured `curl` / `openclaw infer model run` error output, gateway HTTP status, key-rotation note, or LaunchAgent down indicator — written into the audit-trail directory before the carve-out is invoked, with a one-line note in the daily log naming the failure mode.

Default-without-attempt is a posture violation. WS-C v7.0.4 today reflexively defaulted to Section E citing "multi-provider routing may not yet be live" — but routing has been live since 2026-04-19, was proven live the same day by WS-D's six successful gateway calls, and the carve-out should not have fired. If a session reaches for Section E, the bar is: document why cross-family was unreachable, then proceed.

### API key separation — one key per context

For Josh's dev node: Cowork and OpenClaw maintain distinct Anthropic keys, even within the same Anthropic org. Separate keys give separate billing tracks, independent rotation, and narrower leak blast radius. The org-level TPM ceiling is still shared, which is the deeper reason to route OpenClaw's routine turns through non-Anthropic providers by default — only call Anthropic when Scribe is actually drafting.

For every client Golden Quill: BYOK is strict. Each client provides their own keys for Anthropic, Groq, Google, and OpenAI. Those keys live in the client's `~/.openclaw/.env` and nowhere else. No cross-environment reuse — not between Josh's dev node and a client, not between two clients, not between development and production. If one client's key leaks, the blast radius is that one client.

## Org Isolation at Wake-Up

If the first task names an org, the agent reads ONLY that org's PROJECT_CONTEXT.md at step 8. If the task attempts to pull from a second org (for boilerplate, EIN, prior grants, match sources, partnerships), refuse and ask Josh. This is Law 3 and it is strict.

## Session Efficiency — Agent-to-Agent

These rules reduce token waste and round-trip overhead in agent-to-agent handoffs (Cowork → OpenClaw, OpenClaw → OpenClaw, seat → seat).

### Bootstrap, don't re-explain

Handoff prompts reference `pipeline/SESSION_BOOTSTRAP.md` for project orientation. Do not re-encode the project universe, product naming chain, Five Laws, locked decisions, or hardware constraints into every handoff. One line: `Read pipeline/SESSION_BOOTSTRAP.md for project orientation.`

### Reference templates, don't repeat framework

Component analyses, Thesis Team audits, and seat-binding reviews state `Framework: per pipeline/templates/component_analysis_template.md` and write only component-specific delta. The template carries the Five Laws table, Four Rules table, failure modes, hardenings checklist, dev-vs-prod context, standard interface pattern, and audit cycle reference.

### Batch file operations

Plan reads/writes before executing. Read multiple files in one turn. Write multiple outputs in one turn. Minimize tool-call round trips.

### Batch questions to the operator

When multiple things need Josh's input, collect all questions into a single message. Do not ask one question, wait, ask another.

### Compact handoff payloads

A handoff prompt should contain: (1) task definition with input/output paths, (2) scope boundaries, (3) done-definition, (4) pointer to SESSION_BOOTSTRAP.md, (5) pointer to any task-specific files. Not the contents of those files.

## Caching Discipline

Anthropic prompt caching is enabled on `anthropic/*` model refs (see `router.yaml` — `cacheRetention: long` set on Sonnet 4.6 + Opus 4.6 + Opus 4.7). Cache keys = exact prompt prefix. Two pieces of discipline are non-negotiable when any seat issues a cacheable call.

### 1. Org-namespacing preamble (Law 3)

Every cached system block starts with a two-line prefix before any substantive content:

    ORG:<orgSlug>
    TRACE:<sessionId>
    <the rest of the preamble…>

`<orgSlug>` is the exact slug of the client folder under `orgs/` — never an alias, never the legal name, never "default". `<sessionId>` is a per-invocation UUID (for trace-back; it does not need to be stable across calls).

Why: without the `ORG:` prefix, two orgs with otherwise-identical preamble bodies collide on the same cache key. That is a cross-org side channel — a direct Law 3 violation. The `TRACE:` line does not affect isolation on its own (it changes every call, so it would defeat caching if it were the only prefix) but gives post-hoc traceability when paired with the stable `ORG:` line. Anthropic's Feb 2026 workspace-isolation change mitigates at the workspace level; the prefix is defense-in-depth and survives future BYOK arrangements where two clients share one workspace.

Enforcement this round is convention-level. A Logician POST-gate predicate on the cached prefix shape is tracked as a v0.2 work item, not yet live.

### 2. OAuth paths strip cache_control

`claude-cli/*` model refs go through an OAuth auth path that drops the `cache_control` marker before the upstream call. Caching never fires on those. Route cost-sensitive reusable flows (Scribe preambles, Judge rubric scoring, cross-family audits) through `anthropic/*` api-key refs only. Check `router.yaml` before relying on caching for a specific seat.

### 3. Telemetry ledger

Every cached call made through the Tilth scripts logs to `tilth/logs/<org>/cache-ledger.jsonl` (per-call) and `tilth/logs/<org>/cache-tally.json` (rolling totals). Use `tilth/bin/tilth-infer-cached.mjs` for cached inference (see `tilth/bin/README.md` for the three common patterns). Batch-mode caching compounds inside a batch — each request in a `tilth-batch.mjs submit` payload can carry its own `cache_control` on its own system block.

## Session Close — Mandatory

Every agent closes its session with these steps, in order. This is the counterpart to the Wake-Up Sequence — non-optional.

1. **Run the Session Close Self-Check** per `CLAUDE.md` → "Session Close Self-Check" section. Note any failures.
2. **Write session metrics** — append one JSON line to `pipeline/metrics/session_log.jsonl` per the schema in `pipeline/metrics/SESSION_METRICS_SPEC.md`. Include any self-check failures.
3. **Save-On-Decide** — if any decisions, corrections, or lessons emerged during the session that haven't been written yet, write them now (daily_log, lessons.md, or memory file).
4. **Sign off.**

Sessions under 3 turns with no files read/written and no handoff may skip the metrics entry. The self-check still runs.

## Before Acting on a Memory

A memory that names a specific file, function, flag, or endpoint is a claim frozen in time. Before recommending or acting on it, verify the current state. If the memory conflicts with observed reality, trust the observation and update or remove the stale memory.
