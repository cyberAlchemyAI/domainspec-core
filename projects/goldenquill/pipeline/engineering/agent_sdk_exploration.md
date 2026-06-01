# Claude Agent SDK — Tilth Exploration

**Created:** 2026-04-19
**Context:** Josh exploring whether the Claude Agent SDK fits the Tilth v0.1 architecture
**Status:** Research note, not a commitment

---

## 1. What Is the Claude Agent SDK?

The Agent SDK is an open-source library (Python and TypeScript) that wraps the same agent loop, tools, and context management that power Claude Code into a programmable package. It is *not* a new model — it's orchestration infrastructure that runs on your machine and calls LLM APIs remotely.

**What it gives you over the raw Anthropic API:**

- **Automatic agent loop.** You don't write the `while stop_reason == "tool_use"` cycle. The SDK handles tool dispatch, result injection, retries, and streaming.
- **14+ built-in tools.** Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch — referenced by name string, no JSON schema authoring.
- **Automatic context compaction.** When the conversation approaches the context limit, the SDK compacts and re-reads instruction files (CLAUDE.md equivalent). This is the A4/A7 token-windowing problem partially solved at the infrastructure layer.
- **Subagents.** A parent agent can spawn child agents with isolated context windows. Each subagent gets its own system prompt, tools, and scope. The parent only receives the subagent's final output — natural context isolation.
- **Hooks.** Callback events (PreToolUse, PostToolUse, Stop, SubagentStart, SubagentStop, PermissionRequest, etc.) that let you intercept and gate agent behavior with your own code.
- **MCP support.** Connect any MCP server — databases, APIs, file systems — and the agent uses those tools alongside built-in ones.
- **Permissions system.** Fine-grained control over which tools an agent can use, with runtime approval callbacks.
- **Session management.** Session IDs for resume/continuation. State persists across calls when you pass the session_id back.

**Languages:** Python (`claude-agent-sdk-python`) and TypeScript (`claude-agent-sdk-typescript`). Both on GitHub under `anthropics/`.

**Cost:** SDK is free. You pay only for API tokens consumed.

**Provider lock-in (critical for Tilth):** The SDK is built around the Anthropic Messages API. It does NOT natively support Groq, Ollama, Google, or OpenAI endpoints. However, **LiteLLM proxy** can sit between the SDK and non-Anthropic providers, translating the Anthropic wire format to other providers. This is documented and community-tested. Custom tools work through LiteLLM; built-in tools like WebSearch do not.

---

## 2. How Could Tilth Use It?

Mapping SDK capabilities to the locked architecture (v7 A1-A12):

### Council Seats as Agent SDK Agents

| Seat | SDK fit | Notes |
|------|---------|-------|
| **Scribe** | Strong | Primary is `anthropic/claude-sonnet-4-6` — native SDK target. Section-by-section drafting maps to a long-running agent with file tools + MCP access to vault/orgs. Subagent per section is natural. |
| **Editor** | Partial | Primary is `groq/llama-3.3-70b-versatile`. Requires LiteLLM proxy. The SDK's built-in tools (Read, Grep) are useful for cross-referencing drafts, but the tool-use protocol depends on the model supporting Anthropic's tool format — Llama 3.3 through LiteLLM may have rough edges. |
| **Judge** | Partial | Primary is `groq/qwen/qwen3-32b`. Same LiteLLM constraint as Editor. The SFR verdict format (A3) and rubric scoring could be enforced via hooks (PostToolUse validation). |
| **Scout** | Weak | Primary is `ollama/mistral:7b` local. The SDK was not designed for local Ollama models. LiteLLM can proxy Ollama, but a 7B model's tool-use reliability is low — Scout's channel-family discovery is better served by deterministic scripts that *call* the LLM for classification, not by giving the LLM autonomous tool access. |
| **Red Team** | Partial | Primary is `groq/openai/gpt-oss-120b`. Same LiteLLM story. Cross-family rigor is preserved since GPT-OSS is non-Anthropic. |
| **Logician** | None | Deterministic Python + Cedar. Zero tokens. The SDK is an LLM orchestrator — Logician is explicitly NOT an LLM. Logician stays as Python code that runs *alongside* or *wraps* SDK agents, not as one. |

**Verdict:** Scribe is a natural fit. Editor/Judge/Red Team are *possible* through LiteLLM but add a translation layer that may introduce tool-use reliability issues with non-Anthropic models. Scout and Logician don't fit the SDK pattern.

### Thesis Audit Cycle

The multi-model audit (Editor → Judge → Red Team, cross-family) could use the subagent pattern: a parent "Thesis Conductor" agent spawns three subagents (one per reviewer), each pointed at a different provider via LiteLLM. Subagents run in parallel with isolated context. The parent collects verdicts and applies the all-pass/retry/escalate logic.

**Advantage:** Parallel execution, context isolation, structured result collection.
**Risk:** LiteLLM translation fidelity for tool-use with Qwen/Llama/GPT-OSS models. If tool-use fails, the reviewer can still score via pure text completion, but you lose the structured extraction that hooks provide.

### Logician as Hook Layer

This is the most architecturally interesting mapping. Instead of Logician being an Agent SDK agent, **Logician's gates become SDK hooks**:

- `PreToolUse` hooks enforce PRE-gates (F-ROUTER-STALE-API, F-CONTEXT-PLACEMENT, F-INTAKE-ELIGIBILITY-FAIL, etc.) before any tool executes.
- `PostToolUse` hooks enforce POST-gates (F-VERDICT-CERT-MALFORMED, F-P-COHERE-1/2/3, etc.) after tool results return.
- `SubagentStop` hooks validate subagent output before the parent consumes it.
- The `canUseTool` permission callback enforces Law 3 (org isolation) — block file reads outside the active org's directory.

This preserves Logician's zero-token deterministic nature while integrating it directly into the SDK's execution flow. The hooks are Python callbacks — exactly where Cedar policy evaluation already lives.

### GPP as an Agent

GPP-DET (Tier 1) is deterministic Python — stays as-is, invoked via Bash tool or directly. GPP-COUNCIL (Tier 2) is two API calls (Red Team + Reasoner, cross-family) — could be two subagents. GPP-SYNTHESIS (Tier 3) is operator signature — stays manual. The SDK adds structure but limited value here since GPP is already well-defined.

### Router Dispatch

The SDK's subagent dispatch is *similar* to what `router.yaml` + `routing.yaml` already define, but more dynamic. Today: router picks a model, calls the API, returns text. With the SDK: router spawns a subagent with the right model binding, that agent has autonomous tool access (file reads, web search, bash), and returns structured output. The agent loop handles retries, context management, and compaction automatically.

**Key difference:** current routing is single-turn API calls. SDK agents are multi-turn autonomous loops. This is a significant upgrade for seats that need to read multiple files, cross-reference, and iterate (Scribe, Judge), but overkill for seats that do one-shot classification (Scout discovery).

---

## 3. 8GB M1 Constraints

The SDK itself is lightweight Python/TypeScript orchestration code. Resource profile:

- **SDK process:** ~50-100 MB RAM. It's a thin event loop + HTTP client.
- **Docker not required.** Runs as a normal Python process.
- **No local inference.** All LLM computation happens at the API provider (Anthropic, Groq, etc.). The SDK only sends/receives HTTP.

**Current stack on 8GB M1 (from router.yaml):**

| Component | Approx RAM |
|-----------|-----------|
| Ollama + mistral:7b | ~4.5 GB |
| ChromaDB (MemPalace) | ~200 MB |
| OpenClaw daemon | ~100 MB |
| SQLite | Negligible |
| macOS overhead | ~2 GB |
| **Remaining** | **~1.2 GB** |

**Adding Agent SDK:** ~100 MB for the Python process + overhead per subagent (each subagent is a lightweight async task, not a separate process — they share the same Python runtime). Five concurrent subagents might add 50 MB total.

**Verdict:** Comfortably fits. The SDK is ~150 MB total, well within the 1.2 GB headroom. The bottleneck on 8GB remains Ollama's model weight, not orchestration code. On the 128 GB production Golden Quill, this is invisible.

---

## 4. Comparison to Current Approach

| Dimension | Current (manual coordination) | Agent SDK |
|-----------|-------------------------------|-----------|
| Session orchestration | Josh manually opens Cowork/Code/Dispatch sessions | Parent agent spawns subagents programmatically |
| Context isolation | Josh enforces mentally + CLAUDE.md | Subagents get isolated context windows by design |
| Cross-seat handoff | Copy-paste paths, handoff prompts | Subagent returns structured output to parent |
| Policy enforcement | Logician scripts run separately | Hooks intercept every tool call inline |
| Parallel execution | One session at a time | Multiple subagents run concurrently |
| Resume after interruption | Manual session bootstrap | session_id resumes from last state |
| Audit trail | Daily logs, manual | Hooks can auto-log every tool call and result |
| Error handling | Manual retry | SDK handles retries, compaction, fallback |

**What the SDK automates that Josh currently does manually:**

1. Spinning up the right model for each seat (subagent with model binding).
2. Routing questions to Josh only at P-surface decision points (hooks fire only at defined interrupts).
3. Running audits autonomously (Thesis Conductor spawns Editor/Judge/Red Team subagents, collects verdicts, applies merge criteria).
4. Persisting state across context-window boundaries (A7 windowing — SDK's session management + compaction).
5. Enforcing org isolation at the file-access level (canUseTool callback).

**What it does NOT automate:**

- Multi-provider routing (requires LiteLLM layer).
- Deterministic policy enforcement (Logician stays Python, integrated via hooks).
- Operator sign-off gates (P-surfaces still interrupt to Josh).
- Local inference dispatch (Ollama/Scout stays outside the SDK).

---

## 5. Recommended First Prototype

**Start with Scribe.**

Rationale:

1. **Native provider.** Scribe's primary is `anthropic/claude-sonnet-4-6` — zero LiteLLM complexity. The SDK works without translation.
2. **Highest tool-use value.** Scribe needs to read RFA dissections, PROJECT_CONTEXT, prior drafts, rubrics, and vault artifacts. The SDK's built-in file tools (Read, Grep, Glob) map directly. Today this is manual file-path handoff; with the SDK, Scribe autonomously navigates the file tree.
3. **Natural subagent decomposition.** Each grant section is a subagent task: read the RFA section, read PROJECT_CONTEXT fields, draft, validate KGIE. Parent Scribe collects sections and assembles.
4. **Logician integration test.** Wire Scribe's PreToolUse/PostToolUse hooks to Logician gates (F-CONTEXT-PLACEMENT, F-INTAKE-ELIGIBILITY-FAIL, Law 3 file-access restriction). This validates the hooks-as-Logician pattern before scaling to other seats.
5. **Immediate ROI.** Scribe is the seat Josh uses most in active grant work. Autonomous section drafting with built-in validation reduces the most manual coordination overhead.

**Prototype scope:**

```
Input:  orgs/{slug}/PROJECT_CONTEXT.md + pipeline/rfa/{rfa_slug}/rfa_dissection.json
Output: pipeline/drafts/{rfa_slug}/sections/*.md (one per grant section)
Gates:  PreToolUse → Law 3 org isolation; PostToolUse → KGIE check
Model:  anthropic/claude-sonnet-4-6 (direct, no proxy)
```

**Second prototype:** Thesis Conductor — parent agent that spawns Editor + Judge + Red Team subagents (via LiteLLM) against Scribe's draft. This validates multi-provider subagent orchestration and the cross-family rigor pattern.

---

## Thesis outcome — 2026-04-19

This exploration was debated by a simulated Thesis round on 2026-04-19. Outcome:

- **EN-001** (deferred engineering queue entry for a Scribe-SDK spike) — `LOCKED-internal-simulated`, queued behind §6 Operating Envelope blueprint LOCK, §4 Logician v2.2 LOCK, §0.5 v4 refresh, real-engineer validator gate. Not on current queue.
- **EN-002** (SDK lifecycle vocabulary reference table) — `LOCKED-internal-simulated`, zero-code, immediate. Reference file lives at `pipeline/engineering/references/sdk_lifecycle_map.md`.
- **Explicit rejections** — `canUseTool` displacing Cedar, skills semantic dispatch displacing `router.yaml`, permission-modes-as-gears, SDK reload replacing A4, subagent isolation displacing Cedar Law 3, `session_id` replacing A7 calibration artifact. All rejected with reasoning in the audit trail.

Audit trail: `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/00_debate_and_consensus.md`.

Both amendments require operator sign-off and live cross-family re-audit for promotion from `LOCKED-internal-simulated` to `LOCKED-sealed`.

## Key Sources

- [Agent SDK Overview (Anthropic docs)](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Subagents documentation](https://platform.claude.com/docs/en/agent-sdk/subagents)
- [Hooks documentation](https://platform.claude.com/docs/en/agent-sdk/hooks)
- [MCP integration](https://platform.claude.com/docs/en/agent-sdk/mcp)
- [Permissions](https://platform.claude.com/docs/en/agent-sdk/permissions)
- [Python SDK reference](https://platform.claude.com/docs/en/agent-sdk/python)
- [TypeScript SDK reference](https://platform.claude.com/docs/en/agent-sdk/typescript)
- [LiteLLM + Agent SDK integration](https://docs.litellm.ai/docs/tutorials/claude_agent_sdk)
- [GitHub: claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python)
- [GitHub: claude-agent-sdk-typescript](https://github.com/anthropics/claude-agent-sdk-typescript)
- [Building agents with the Claude Agent SDK (Anthropic engineering)](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
