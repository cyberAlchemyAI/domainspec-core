---
scope: Reflection design research — lane 4 of 5
purpose: Pydantic AI's idiomatic memory + evals + tool composition patterns; constraints the Reflection Packet must respect
substrate_baseline: Pydantic AI (LOCKED per ADR-001, v7.0.3 substrate amendment); pydantic_evals; Logfire instrumentation
docs_version: ai.pydantic.dev as of 2026-05-10 (matches current main branch of github.com/pydantic/pydantic-ai)
research_window: ~45 min, WebSearch-driven (live web_fetch restricted by provenance set)
status: research only — no code edits, no LOCK ceremony
created: 2026-05-10
---

# Lane 4 — Pydantic AI's Native Memory + Evals + Tool Composition Patterns

## 0. Why this lane exists

The substrate is LOCKED. Per ADR-001 and architecture v7.0.3, Tilth's runtime is Pydantic AI (agent primitives + structured output + dependency injection) + Logfire (observability) + curated Python parsing tools + Ollama/vLLM (local inference) + Logician (deterministic Cedar + Python gates). LangGraph and OpenClaw are removed. The Reflection Packet therefore cannot invent a parallel orchestration / state framework — it must compose with Pydantic AI's idiomatic shape or it will fight the substrate at every PRE/POST gate boundary.

This lane answers six questions about Pydantic AI's native idioms so the Reflection Packet design can be expressed as a thin layer over them, not as an alternative.

---

## 1. Pydantic AI's native memory model

**Short answer: there is no first-class long-term "memory" primitive. Pydantic AI exposes message history as a typed list, and treats anything beyond that as operator-supplied state plumbed through dependency injection.**

### 1.1 Message history is the only built-in "memory"

The canonical mechanism is the `message_history` keyword on `Agent.run`, `run_sync`, and `run_stream`. After a run, the result object exposes two accessors:

- `RunResult.all_messages()` — returns the complete list (`list[ModelMessage]`) including any messages passed in via `message_history` plus those produced during the current run.
- `RunResult.new_messages()` — returns only the messages produced during the current run. Anything passed in via `message_history` is excluded.

Both accessors have JSON counterparts: `all_messages_json()` and `new_messages_json()`. The companion deserializer is `ModelMessagesTypeAdapter` (exported from `pydantic_ai`).

Round-trip pattern from the official docs:

```python
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessagesTypeAdapter
from pydantic_core import to_jsonable_python

agent = Agent('openai:gpt-5.2', system_prompt='Be a helpful assistant.')

# Run 1.
result1 = agent.run_sync('Tell me a joke.')
history = to_jsonable_python(result1.all_messages())

# Persist `history` to disk / SQLite / blob store however you like.
# ...

# Reload, validate against the typed schema, resume conversation.
restored = ModelMessagesTypeAdapter.validate_python(history)
result2 = agent.run_sync('Now another one.', message_history=restored)
```

Source: [`pydantic-ai/docs/message-history.md`](https://github.com/pydantic/pydantic-ai/blob/main/docs/message-history.md) and the Chat App with FastAPI example which stores `message_list as TEXT` in a SQLite messages table ([ai.pydantic.dev/examples/chat-app](https://ai.pydantic.dev/examples/chat-app/)).

### 1.2 What the message types actually are

The objects in the list are typed subclasses of `ModelMessage`:

- `ModelRequest` (carries `UserPromptPart`, `SystemPromptPart`, `ToolReturnPart`, `RetryPromptPart`)
- `ModelResponse` (carries `TextPart`, `ToolCallPart`, plus token-usage on the response object)

These are dataclasses, fully serializable through Pydantic. They are *the* canonical shape for "what the agent saw and produced." Any reflection or evals tooling that wants to "look at what the agent did" should be reading these, not re-deriving from logs.

Source: [`ai.pydantic.dev/api/messages/`](https://ai.pydantic.dev/api/messages/).

### 1.3 There is no built-in long-term memory

There is no `Agent.memory`, no `MemoryStore`, no built-in vector-DB hook. Articles like [Hindsight's "Pydantic AI Persistent Memory: Add It in 5 Lines"](https://hindsight.vectorize.io/blog/2026/03/09/pydantic-ai-persistent-memory) and [the Medium MongoDB guide](https://learnitnow.medium.com/unlock-your-ais-memory-a-practical-guide-to-pydantic-ai-agents-mongodb-09476ddc2963) exist precisely *because* the framework is unopinionated here — operator wires their own store, passes references in via `deps`, and reads/writes through tools.

This is a feature, not a gap, from Pydantic AI's design POV: the agent is intended to be stateless and global, and all state is supplied per-run through dependency injection (see §2.2 below). Source: [`ai.pydantic.dev/dependencies/`](https://ai.pydantic.dev/dependencies/).

### 1.4 `history_processors` — the message-history transformation hook

Pydantic AI provides one inbound hook on the message stream: `history_processors`. This is a list of callables that intercept `list[ModelMessage]` *before each model request*, and can reshape it.

```python
from pydantic_ai import Agent, ModelMessage, RunContext

def context_aware_processor(
    ctx: RunContext[None],
    messages: list[ModelMessage],
) -> list[ModelMessage]:
    if ctx.usage.total_tokens > 1000:
        return messages[-3:]
    return messages

agent = Agent('openai:gpt-5.2', history_processors=[context_aware_processor])
```

Processors can be sync or async, are applied in sequence, and can optionally receive `RunContext` for access to current usage/deps. This is the framework's idiomatic seam for "transform what the agent sees of its past" — exactly the kind of seam reflection-derived summaries would feed into.

Source: [pydantic-ai message-history.md](https://github.com/pydantic/pydantic-ai/blob/main/docs/message-history.md), [Medium: Smart Context Engineering with Pydantic AI](https://medium.com/dream-ai/smart-context-engineering-with-pydantic-ai-part-1-history-processing-for-long-running-tasks-f06926241503).

---

## 2. Idiomatic pattern for storing extracted patterns between sessions

**Short answer: persist the structured artifact (e.g. a `BaseModel`/`@dataclass` Reflection record) yourself, and on next run inject a reference to the store through `deps` and let a `system_prompt` or `tool` read from it.**

### 2.1 The agent is stateless; state lives in `deps`

> *Since agents are stateless and designed to be global, you do not need to include the agent itself in agent dependencies. Rather than using global state, Pydantic AI provides dependency injection without global state, offering a type-safe pattern for injecting database connections, API clients, and session data at runtime via a RunContext, keeping agent definitions clean and tests easy.*
>
> — searched paraphrase of [`ai.pydantic.dev/dependencies/`](https://ai.pydantic.dev/dependencies/)

The pattern:

```python
from dataclasses import dataclass
import httpx
from pydantic_ai import Agent, RunContext

@dataclass
class MyDeps:
    api_key: str
    http_client: httpx.AsyncClient
    # for Tilth this is where ReflectionStore would live:
    # reflection_store: ReflectionStore

agent = Agent('openai:gpt-5.2', deps_type=MyDeps)

@agent.system_prompt
async def get_system_prompt(ctx: RunContext[MyDeps]) -> str:
    response = await ctx.deps.http_client.get(
        'https://example.com',
        headers={'Authorization': f'Bearer {ctx.deps.api_key}'},
    )
    response.raise_for_status()
    return f'Prompt: {response.text}'
```

So "extracted reflection patterns" should be:

1. A `BaseModel` or `@dataclass(kw_only=True, frozen=True)` schema authored alongside the seat blueprint (Tilth already builds these for every classification register entry — same idiom).
2. Serialized through Pydantic to disk (JSON/YAML) or to a per-org SQLite, the same way Tilth already persists KFR entries.
3. Reloaded on next run, wrapped in a small `ReflectionStore` accessor, and handed in via `deps`.

Pydantic AI does not need to be told this exists. It just needs the `deps_type` set and a tool or `system_prompt` decorator that pulls from it.

### 2.2 Dynamic system prompts as the binding point

The seam between persisted reflection state and a new run is `@agent.system_prompt` (or its `@agent.instructions` cousin). This is invoked at run-start and receives `RunContext[Deps]`. It is the right place to inject "here is the prior-run reflection summary that applies to this cycle." No frame mutation, no global state, no race condition.

```python
@agent.system_prompt
async def with_reflections(ctx: RunContext[TilthSeatDeps]) -> str:
    rfx = ctx.deps.reflection_store.load_for(
        seat="scribe", org_slug=ctx.deps.org_slug, grant_id=ctx.deps.grant_id,
    )
    if not rfx:
        return base_seat_prompt
    return base_seat_prompt + "\n\n## Reflections from prior cycles\n" + rfx.render_block()
```

### 2.3 Persistence — `ModelMessagesTypeAdapter` for raw transcripts; bespoke Pydantic models for derived facts

There is a clean two-tier separation Pydantic AI implicitly endorses:

- **Tier A — raw transcript persistence:** `ModelMessagesTypeAdapter` round-trips the agent's literal message history for replay / debugging / eval-dataset construction.
- **Tier B — distilled artifact persistence:** operator-defined Pydantic models (e.g. `Reflection`, `LessonInstance`, `PatternFact`) serialized with `model_dump()` / `model_validate()` are how you store derivatives — what was *learned*, not what was *said*.

Tilth should keep this two-tier shape. The raw transcript is evidence for the reflection step; the distilled `Reflection` model is what gets stored, retrieved, and injected next run. (This also matches Law 1 — RFA Is Truth — because the transcript is auditable provenance for any reflection-derived claim.)

---

## 3. The Pydantic AI evals story

**Short answer: `pydantic_evals` is a real, opinionated package — Dataset / Case / Evaluator / EvaluatorContext / EvaluationReport, with first-class Logfire integration. It is the substrate-native answer to "run agent → eval → store outcome → reflect."**

### 3.1 Core primitives

From [`ai.pydantic.dev/evals/`](https://ai.pydantic.dev/evals/) and the [PyPI page for `pydantic-evals`](https://pypi.org/project/pydantic-evals/):

- **`Case`** — one test scenario: `inputs`, optional `expected_output`, optional `name`, `metadata`, and case-scoped `evaluators`.
- **`Dataset`** — a collection of `Case`s plus dataset-scoped evaluators. Generic over (`InputT`, `OutputT`, `MetadataT`). Can be authored in Python or loaded from YAML / JSON (with generated JSON schemas alongside for editor type-checking).
- **`Evaluator[InputT, OutputT]`** — base class with one method `evaluate(ctx: EvaluatorContext[...]) -> float | bool | dict[str, float|bool|EvaluationReason]`. Can be sync or async.
- **`EvaluatorContext`** — the sole argument to `evaluate`. Holds `inputs`, `output`, `expected_output`, `metadata`, plus Logfire span / telemetry data when integration is wired.
- **`ReportEvaluator`** — variant that analyzes a full experiment's worth of cases, not one at a time.
- **`Experiment` / `EvaluationReport`** — `dataset.evaluate_sync(task_fn)` or `evaluate(task_fn)` runs the task across all cases and returns an `EvaluationReport` object with per-case scores plus aggregate stats.

### 3.2 Code shape

```python
from typing import Any
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import Evaluator, EvaluatorContext, EqualsExpected, IsInstance

class MatchAnswer(Evaluator[str, str]):
    def evaluate(self, ctx: EvaluatorContext[str, str]) -> float:
        if ctx.output == ctx.expected_output:
            return 1.0
        if isinstance(ctx.output, str) and ctx.expected_output.lower() in ctx.output.lower():
            return 0.8
        return 0.0

dataset = Dataset[str, str, Any](
    name='my_eval_suite',
    cases=[
        Case(name='test_1', inputs='What is the capital of France?', expected_output='Paris'),
        Case(name='test_2', inputs='Who wrote Romeo and Juliet?',  expected_output='William Shakespeare'),
    ],
    evaluators=[IsInstance(type_name='str'), EqualsExpected(), MatchAnswer()],
)

report = dataset.evaluate_sync(my_task_fn)   # my_task_fn: (input) -> output
```

Source: [`ai.pydantic.dev/evals/`](https://ai.pydantic.dev/evals/), [`ai.pydantic.dev/api/pydantic_evals/dataset/`](https://ai.pydantic.dev/api/pydantic_evals/dataset/), [`ai.pydantic.dev/api/pydantic_evals/evaluators/`](https://ai.pydantic.dev/api/pydantic_evals/evaluators/).

### 3.3 LLMJudge — an evaluator that calls a model

For subjective rubric scoring, `LLMJudge` is provided out of the box. It accepts `rubric`, `model`, `include_input`, `include_expected_output`, `model_settings`, plus `score` and `assertion` config dicts. With `score={'include_reason': True}` you get `{'LLMJudge_score': EvaluationReason(value=0.85, reason='...'), 'LLMJudge_pass': EvaluationReason(value=True, reason='...')}`. This is the native substrate for Judge-seat-style rubric scoring inside an eval loop.

Source: [`ai.pydantic.dev/evals/evaluators/llm-judge/`](https://ai.pydantic.dev/evals/evaluators/llm-judge/), [`ai.pydantic.dev/evals/evaluators/built-in/`](https://ai.pydantic.dev/evals/evaluators/built-in/).

### 3.4 Logfire integration — the native "store outcome → reflect" loop

Two integration points matter for reflection:

1. **`logfire.instrument_pydantic_ai()`** captures every agent run as a span with attributes like `all_messages_json` and `agent_name`. These are queryable via SQL in the Logfire UI.
2. **Pydantic Evals uses OpenTelemetry internally** to record traces of the evaluation process itself. The Logfire UI renders an `EvaluationReport` table view on the evaluation root span, with full access to underlying execution traces.

Crucially, GitHub issue [#4340 "Support building eval datasets from Logfire production traces"](https://github.com/pydantic/pydantic-ai/issues/4340) confirms the intended direction: production runs → spans → harvested into eval cases. That is *exactly* the prod → reflect loop.

Source: [`ai.pydantic.dev/evals/how-to/logfire-integration/`](https://ai.pydantic.dev/evals/how-to/logfire-integration/), [`pydantic.dev/articles/q2-2025-summary`](https://pydantic.dev/articles/q2-2025-summary).

### 3.5 Span-based evaluation

`pydantic_evals` supports a span-based evaluator mode where you assert conditions on which tools were called, code paths executed, timing, errors, and execution structure — not just final output. This is directly usable for Tilth-style "did the seat call the gate it was supposed to call?" checks.

Source: [`ai.pydantic.dev/evals/evaluators/span-based/`](https://ai.pydantic.dev/evals/evaluators/span-based/).

---

## 4. Tool composition for reflection

**Short answer: use `@agent.tool` for the reflection tool, type the deps so it has access to the reflection store and prior transcript, return a typed Pydantic model. Do not use `@agent.tool_plain` if you need run context.**

### 4.1 `@tool` vs `@tool_plain`

- `@agent.tool` (or `@toolset.tool`) — tool function takes `RunContext[Deps]` as its **first** parameter. This is the only way to access dependencies, usage, retry count, or messages-so-far.
- `@agent.tool_plain` — tool function does *not* take `RunContext`. Use this only for pure functions where state injection is unnecessary.

> *Common errors include using RunContext annotations with @agent.tool_plain (which is not allowed), failing to make RunContext the first parameter of tools that take context, and placing RunContext out of order rather than as the first parameter.*

Source: [`ai.pydantic.dev/tools/`](https://ai.pydantic.dev/tools/), [pydantic-ai-common-pitfalls](https://lobehub.com/skills/existential-birds-beagle-pydantic-ai-common-pitfalls).

### 4.2 Idiomatic reflection-tool shape

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

class Reflection(BaseModel):
    seat: str
    grant_id: str
    org_slug: str
    pattern: str = Field(description="What pattern was observed across cases?")
    evidence_msg_ids: list[str] = Field(description="Message UUIDs that ground this claim.")
    confidence: float = Field(ge=0.0, le=1.0)

@agent.tool
async def record_reflection(
    ctx: RunContext[TilthSeatDeps],
    reflection: Reflection,
) -> str:
    # PRE-gate: F-REFLECTION-EVIDENCE-MISSING (see §5).
    # Persist.
    ctx.deps.reflection_store.write(reflection)
    return f"recorded {reflection.pattern!r}"
```

Pydantic AI auto-derives the tool schema from the function signature (it reads the docstring for parameter descriptions; can be configured with `docstring_format='google'` and `require_parameter_descriptions=True`). Tool return values can be anything Pydantic can serialize to JSON.

### 4.3 Tool composition across seats

For seat-to-seat reflection (e.g. Judge reflects on Scribe), there are two idiomatic options:

- **Same-agent multi-tool** — one Pydantic AI `Agent` registers multiple tools (`record_reflection`, `read_reflection`, `score_evidence`, etc.); they share `Deps` and `RunContext`. Cheapest, type-safe, single observability span.
- **Programmatic agent hand-off** — per [Multi-Agent Patterns](https://ai.pydantic.dev/multi-agent-applications/), one agent calls another inside a tool; the outer agent's `RunContext` is the bridge. Use this when the seat boundaries are real (cross-family routing, different model bindings).

For the Reflection Packet specifically, the cleaner shape is probably the **second** pattern: a small dedicated `reflection_agent` with its own deps, called from inside seat agents' tool implementations. That keeps reflection's classification, gates, and storage isolated from per-seat concerns.

---

## 5. Where F-REFLECTION-* gates plug in

Pydantic AI exposes four real seams. Each maps cleanly to a v0.1 gate category and they all sit "above the runtime" so the gate code can stay deterministic Python + Cedar, with zero token cost (matches Logician's discipline).

| Seam | When it fires | Best use for F-REFLECTION-* |
|------|---------------|------------------------------|
| **`history_processors`** | Before every model request, before tokens are spent | PRE-gate: scrub or reject reflection-bearing context that violates Law 3 (cross-org leak) or Law 5 (fabrication risk). |
| **`@agent.system_prompt` / `@agent.instructions`** | Run-start | PRE-gate: refuse to inject a reflection that fails signature check, hash check, or classification mismatch. Cleanest place to raise a `CriticalPolicyError`. |
| **`@agent.tool` body (entry)** | When the model invokes the reflection tool | PRE-gate (in-tool): refuse to record a reflection whose evidence list is empty, points to messages outside this run's transcript, or names content classified `confidential` while the run is cloud-routed. |
| **`@agent.output_validator`** | After the model produces the final structured output | POST-gate: assert the output, if it claims a reflection, references one we actually have on file. |

The `output_validator` seam is particularly important because it can raise `ModelRetry` to ask the model to try again — this is the substrate-native way to "fail-closed with a chance to recover" without operator intervention. Worked example from the docs:

```python
from pydantic_ai import RunContext
from pydantic_ai.exceptions import ModelRetry

@agent.output_validator
async def output_validator_deps(ctx: RunContext[TilthSeatDeps], data: ProposalDraft) -> ProposalDraft:
    if not ctx.deps.reflection_store.evidence_matches(data.reflection_id):
        raise ModelRetry("reflection_id does not resolve to recorded evidence; re-draft without unverified pattern.")
    return data
```

Source: [`ai.pydantic.dev/api/agent/`](https://ai.pydantic.dev/api/agent/) (output_validator overloads), [`ai.pydantic.dev/output/`](https://ai.pydantic.dev/output/).

### 5.1 Where deterministic gates *must* live, not the agent

Per Logician's invariant (always-local, fail-closed, zero-token), the Cedar/Python `F-REFLECTION-*` gates themselves must NOT be Pydantic AI agents or LLM-backed evaluators. They live as plain Python functions called from inside the seams above. Pydantic AI just provides the **call sites**:

- `history_processors[0]` body — calls `logician.check_reflection_law_3(...)` directly.
- `@agent.system_prompt` body — calls `logician.verify_reflection_signature(...)` directly.
- `@agent.tool` body — calls `logician.check_reflection_evidence_present(...)` directly.
- `@agent.output_validator` body — calls `logician.check_reflection_id_resolves(...)` directly.

The agent never *interprets* the gate; it just routes to it. This preserves "zero-token cost, deterministic" while staying fully inside Pydantic AI's idioms.

---

## 6. What Pydantic AI prohibits or makes awkward

### 6.1 Hard prohibitions / errors

- **`RunContext` annotation on `@tool_plain`** — raises at agent build time. If a reflection tool needs context, it must be `@tool`.
- **`RunContext` not as the first parameter** — same error class.
- **Returning non-JSON-serializable objects from tools** — Pydantic AI tries to serialize for the model and crashes loudly. See GH issue [#1859](https://github.com/pydantic/pydantic-ai/issues/1859) for a real `PydanticSerializationError` example from this.

### 6.2 Awkward but doable

- **Mid-run state mutations and side effects.** Per GitHub issue [#4679 "Agentic Two-Phase Commits"](https://github.com/pydantic/pydantic-ai/issues/4679): if a tool mutates external state and then the run later fails output validation or hits a token limit, the mutation persists while the agent crashes. There is no built-in transactional boundary. **Implication for the Reflection Packet:** the `record_reflection` tool must write through a journal that supports rollback, or write only on `output_validator` success. Tilth already has audit-log discipline that fits this; the Reflection store needs the same write-on-commit pattern.
- **Dynamic system prompts that depend on tool outputs from the same run** — works, but the prompt is re-evaluated only per-run, not per-step. If reflection needs to be re-injected mid-run, use `history_processors` instead.
- **No native long-term memory abstraction** — has to be modeled as `deps`-injected store, which is fine, but means there is no "official" library pattern to point reviewers at. Tilth's existing KFR store pattern is the right reference shape.

### 6.3 Not-built-in (must be authored)

- Vector retrieval, embeddings, semantic memory.
- Cross-run "agent state" beyond what is serialized via `ModelMessagesTypeAdapter` or in operator-supplied stores.
- Multi-tenant isolation. Pydantic AI is single-tenant by default. **Law 3 (Org Isolation) must be enforced in the `Deps` plumbing**, not assumed from the framework. Specifically: each org gets its own `TilthSeatDeps` instance with its own `reflection_store` handle; nothing in Pydantic AI prevents you from accidentally sharing a store across orgs — that's on Tilth's wiring.

### 6.4 Anti-pattern callouts

> *Hardcoding database connections or API clients makes testing difficult, creates tight coupling, and reduces reusability; dependency injection solves these issues by allowing you to pass a runtime context (RunContext) to your agents and tools, which Pydantic AI provides as a type-safe pattern.*
>
> — paraphrased from [`ai.pydantic.dev/dependencies/`](https://ai.pydantic.dev/dependencies/)

Translation for Reflection: never reach for a module-level `REFLECTION_STORE = ...` global. Always inject through `Deps`. (Same reason Tilth's Cedar-policy engine is module-level singleton with a `BaseException`-derived `CriticalPolicyError` per §13 v1 RT-C2-04 hardening — different problem, same anti-global discipline.)

---

## 7. Tilth implications — recommendations for the Reflection Packet's Pydantic AI shape

These are *recommendations* derived from this lane's research, not LOCKs. They are framed to feed Reflection-design synthesis after all five lanes return.

### 7.1 Native shape: `Reflection` is a Pydantic model in a per-org store, injected via `deps`

- Author `pipeline/seats/reflection/models.py` with `Reflection(BaseModel)` and `LessonInstance(BaseModel)` (already a v1.x Archivist concept) using the same `@dataclass(frozen=True, kw_only=True)` / Pydantic discipline as the rest of the codebase.
- Per-org store at `orgs/<slug>/vault/reflection/store.{yaml,sqlite}` — matches the canonical-gate-checked path pattern already used for classification register (`orgs/<slug>/vault/classification/register.yaml`).
- Each seat's `Deps` gets a `reflection_store: ReflectionStore` field. `ReflectionStore` is org-bound at construction time; F-REFLECTION-CROSS-ORG-LEAK fail-closes if the bound org_slug doesn't match the run's org_slug.

### 7.2 Reflection is a *separate Pydantic AI agent*, not a Scribe/Editor extension

Run a small dedicated `reflection_agent` with three tools: `read_priors`, `record_reflection`, `score_against_priors`. Seats call it via the multi-agent hand-off pattern, never embed it inline. This keeps:

- Classification-driven routing simpler (Reflection agent has its own routing posture — likely always-local, since reflections derive from confidential post-fill drafts).
- Logfire spans clean per seat.
- §4 Logician v2.x gate ownership unambiguous — F-REFLECTION-* gates live entirely on this one agent.

### 7.3 Use `pydantic_evals.Dataset` as the storage shape for prior-cycle reflections

Each grant cycle's outcome becomes a `Case`:

- `inputs` = the seat input (PROJECT_CONTEXT slice + RFA fingerprint).
- `output` = the draft produced.
- `expected_output` = the *funded* version (when known), or the strongest version produced.
- `metadata` = `{seat, grant_id, org_slug, cycle_id, funded: bool, score: float}`.
- `evaluators` = `[LLMJudge(rubric=...)]` for rubric-style scoring, plus deterministic checks (`EqualsExpected` for KGIE preflight comparisons, custom `Evaluator[...]` subclasses for SMART-outcome shape).

This reuses substrate the framework already builds, ships its own Logfire UI for, and supports YAML/JSON round-trip with generated JSON schemas. Reflection becomes "iterate over the dataset, derive patterns, write `Reflection` records."

### 7.4 Use `history_processors` as the inbound seam for reflection injection

A reflection-aware history processor on the Scribe/Editor/Judge agents:

```python
async def inject_reflections(ctx: RunContext[TilthSeatDeps], messages: list[ModelMessage]) -> list[ModelMessage]:
    rfx = await ctx.deps.reflection_store.relevant_for(
        seat=ctx.deps.seat_name,
        rfa_fingerprint=ctx.deps.rfa_fingerprint,
    )
    if not rfx:
        return messages
    # Prepend a synthetic system note carrying signed reflection block.
    return [build_reflection_system_message(rfx), *messages]
```

This is fail-closed via the Logician call inside `build_reflection_system_message` — if signature verification fails, raise `CriticalPolicyError(BaseException)` per the §13 Cedar-engine-mandatory-at-module-load discipline.

### 7.5 Gate placement (mapping to architecture v7.0.4-M1 + §4 v2.x.1 conventions)

Proposed F-REFLECTION-* gate placement, all deterministic Python + Cedar, called from Pydantic AI seams (not authored as agents):

| Failure code (proposed) | Seam | Phase |
|---|---|---|
| `F-REFLECTION-CROSS-ORG-LEAK` | `Deps` construction + `history_processors[0]` | PRE-deps-build + PRE-request |
| `F-REFLECTION-SIGNATURE-INVALID` | `@agent.system_prompt` | PRE-run |
| `F-REFLECTION-EVIDENCE-MISSING` | `@agent.tool record_reflection` body | PRE-tool-write |
| `F-REFLECTION-EVIDENCE-OUT-OF-RUN` | `@agent.tool record_reflection` body | PRE-tool-write |
| `F-REFLECTION-CLASSIFICATION-LEAK` | `history_processors[1]` | PRE-request |
| `F-REFLECTION-ID-UNRESOLVED` | `@agent.output_validator` | POST-output |
| `F-REFLECTION-WRITE-WITHOUT-COMMIT` | `output_validator` success → commit; failure → rollback | COMMIT |

The COMMIT-gate is the substrate-aware response to GH #4679: write to a journal in `record_reflection`, commit only when `output_validator` returns clean. This mirrors the prepare-and-stage discipline §12 Uploader uses for funder-portal submissions.

### 7.6 Avoid

- Inventing a parallel "ReflectionMemory" runtime concept. Pydantic AI's `deps` + custom `BaseModel` schema is sufficient and idiomatic.
- Putting reflection logic inside `system_prompt` body itself. The seam is for *injecting* the reflection block, not deriving it.
- Persisting reflections via `ModelMessagesTypeAdapter`. That adapter is for raw transcripts (Tier A). Reflections are derived artifacts (Tier B) and need their own Pydantic model.
- A module-level reflection store global. Always inject through `Deps`.

### 7.7 Open questions for synthesis (not answered in this lane)

- How does the Reflection store's content classification interact with v7.0.7 classification-driven routing? *Default expectation: always-local, since reflections derive from post-fill (Confidential-bearing) drafts. Confirm in synthesis.*
- Does the COMMIT-gate journal pattern need its own architecture-amendment row, or does it fold under §12 Uploader's prepare-and-stage discipline?
- Where does reflection generation sit in the v0.2 horizon — Archivist-owned (§15 v1 LOCKED), Data Collector / Report Generator (§13/§14), or a new §16 seat? **Note:** §15 Archivist v1 is SPEC-ONLY and already names "lessons memory" as one of its v1.x duties. Likely fold here, not new seat.

---

## 8. Sources

Primary docs (cited inline above):

- [Messages and chat history](https://ai.pydantic.dev/message-history/) — `ai.pydantic.dev/message-history/`
- [pydantic-ai/docs/message-history.md](https://github.com/pydantic/pydantic-ai/blob/main/docs/message-history.md) (source-of-truth markdown)
- [pydantic_ai.messages](https://ai.pydantic.dev/api/messages/)
- [pydantic_ai.agent](https://ai.pydantic.dev/api/agent/)
- [Dependencies](https://ai.pydantic.dev/dependencies/)
- [Function Tools](https://ai.pydantic.dev/tools/)
- [Output](https://ai.pydantic.dev/output/)
- [Multi-Agent Patterns](https://ai.pydantic.dev/multi-agent-applications/)
- [Chat App with FastAPI example](https://ai.pydantic.dev/examples/chat-app/)
- [Pydantic Evals — top-level](https://ai.pydantic.dev/evals/)
- [pydantic_evals.dataset](https://ai.pydantic.dev/api/pydantic_evals/dataset/)
- [pydantic_evals.evaluators](https://ai.pydantic.dev/api/pydantic_evals/evaluators/)
- [LLM Judge evaluator](https://ai.pydantic.dev/evals/evaluators/llm-judge/)
- [Built-in Evaluators](https://ai.pydantic.dev/evals/evaluators/built-in/)
- [Span-Based evaluation](https://ai.pydantic.dev/evals/evaluators/span-based/)
- [Logfire Integration with Pydantic Evals](https://ai.pydantic.dev/evals/how-to/logfire-integration/)
- [pydantic-evals on PyPI](https://pypi.org/project/pydantic-evals/)

Secondary / supporting:

- [Smart Context Engineering with Pydantic AI — history processors](https://medium.com/dream-ai/smart-context-engineering-with-pydantic-ai-part-1-history-processing-for-long-running-tasks-f06926241503)
- [Extending Pydantic AI Agents with Chat History](https://dev.to/hamluk/extending-pydantic-ai-agents-with-chat-history-messages-and-chat-history-in-pydantic-ai-d4f)
- [Hindsight: Pydantic AI Persistent Memory in 5 Lines](https://hindsight.vectorize.io/blog/2026/03/09/pydantic-ai-persistent-memory)
- [Pydantic AI Long-Term Memory via MongoDB (Medium)](https://learnitnow.medium.com/unlock-your-ais-memory-a-practical-guide-to-pydantic-ai-agents-mongodb-09476ddc2963)
- [pydantic-ai-common-pitfalls (LobeHub Skills)](https://lobehub.com/skills/existential-birds-beagle-pydantic-ai-common-pitfalls)
- [Q2 2025 Logfire + Evals roundup](https://pydantic.dev/articles/q2-2025-summary)

GitHub issues referenced for anti-pattern grounding:

- [#4679 — Agentic Two-Phase Commits](https://github.com/pydantic/pydantic-ai/issues/4679) — side-effects after failed validation
- [#1859 — new_messages_json serialization error](https://github.com/pydantic/pydantic-ai/issues/1859) — non-JSON tool returns
- [#2050 — history_processor messages contain current-run messages](https://github.com/pydantic/pydantic-ai/issues/2050)
- [#3983 — new_messages() wrong when processors prune](https://github.com/pydantic/pydantic-ai/issues/3983) — implementation gotcha if pruning current-run messages
- [#4340 — building eval datasets from Logfire production traces](https://github.com/pydantic/pydantic-ai/issues/4340) — confirms the prod-trace → eval-dataset loop

---

## 9. Method notes

- Live `web_fetch` was unavailable for `ai.pydantic.dev` deep pages due to provenance-set restriction. The `ai.pydantic.dev/llms-full.txt` consolidated dump fetched successfully but exceeded read-tool token limits; content was extracted via targeted `WebSearch` queries instead. Quoted material is paraphrased from search-result snippets unless rendered in fenced code blocks (where the snippet was rendered as verbatim by the search tool).
- Where this lane summarizes code shapes, those shapes are taken directly from the docs' canonical examples (system_prompt with `MyDeps`, history_processors with `context_aware_processor`, evals with `Dataset[str, str, Any]`). They are not invented for this report.
- This is research only. No LOCK ceremony, no code edits to Tilth modules, no engineering-spec updates. Synthesis across all five lanes happens separately.
