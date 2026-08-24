# Agent orchestration: a beginner’s guide to the controlled relay

Suppose one agent is asked to inspect a repository, challenge its own conclusion, change the code, and approve the result. The problem is not effort. Planning, permission, execution, and judgment have collapsed into one voice, so the work can look complete before the evidence supports that conclusion.

Adding more agents does not automatically fix this. It can merely spread the confusion across more conversations. Orchestration starts when every handoff becomes answerable: what changed, what proves it, who owns the next move, and what still does not follow?

That is the main lesson from the orchestration machinery in this repository. Think of the system as a controlled relay, not a crowd of autonomous workers. Each participant has a bounded responsibility. Each handoff carries evidence. A named owner decides whether that evidence is enough for the next transition.

The relay metaphor has a limit: passing the baton proves that a handoff occurred; it does not prove that the message carried by the baton is true.

## Start with the smallest coordination need

Before designing a multi-agent workflow, ask whether one bounded helper is enough.

A helper is usually enough when the task has one clear output, fits inside the parent’s existing scope, and can be inspected directly. Examples include locating a definition, checking one failing test, or summarizing one file. The parent still owns the objective and the decision about what happens next.

A governed dispatch becomes useful when the work needs something a single helper cannot provide responsibly:

- genuinely independent viewpoints;
- separation between production and review;
- parallel work whose results must later be combined;
- stages that must remain blocked until earlier evidence passes;
- isolation between contexts, tools, or write scopes.

This is a cost-benefit decision. A dispatch buys differentiation, isolation, and controlled dependency. In return, it creates more obligations: a material strategy, an exact route, confirmation, execution records, receipts, joins, gates, and closeout.

More agents do not create more authority. They create more boundaries that must be made explicit.

## The last-proven-step loop

Here is a compact teaching device for reading any orchestration state. It is not canonical repository vocabulary; it is a way to apply the repository’s evidence model.

At every handoff, ask four questions:

1. Where is the workflow now?
2. What direct evidence supports that state?
3. Who owns the next transition?
4. What still does not follow?

Call this the **last-proven-step loop**. Its smallest useful form is:

```text
admitted state
  -> named owner transition
    -> attributable evidence
      -> bounded next state + explicit residue
```

“Residue” is what remains incomplete, uncertain, excluded, or owned elsewhere. Naming it is not pessimism. It is how the system avoids turning a partial result into a larger claim.

One loop is small, but repeating it rebuilds the whole lifecycle. The output of one step becomes the input to another only after the relevant evidence boundary passes.

## A dispatch is a chain of different decisions

Imagine a team preparing a compatibility note for a repository. One worker may inspect the implementation, another may challenge the conclusion, and another may prepare the final text. This is a generic example, not proof that any particular historical run completed this way.

Before anyone runs, the strategy explains why the work is divided, where disagreement belongs, and what each lane may establish. An exact route then binds the roles, inputs, outputs, dependencies, gates, and stop conditions.

Those artifacts are still proposals. A human confirms the material route. Dispatch Spec checks whether the route is structurally coherent. Orchestrate then handles native execution. These are separate decisions because they answer separate questions:

- **Strategy:** Why should the work be divided this way?
- **Human confirmation:** Is this exact material proposal authorized?
- **Dispatch Spec:** Does the route have a valid shape?
- **Orchestrate:** What exact action may the host attempt now?
- **Delegated worker:** What result does the bounded task produce?
- **Gate owner:** Is the admitted evidence enough to open the next transition?

The lifecycle can be read as one controlled relay:

```text
coordination need
  -> strategy -> exact route -> human confirmation
  -> route validation -> preflight -> persisted action
  -> host work -> terminal observation -> logical close
  -> receipt admission -> join -> gate
  -> dependent-wave plan or explicit stop
  -> terminal closeout
```

The arrows matter more than the boxes. Every arrow has an owner, an evidence requirement, and a claim ceiling.

## Follow one action through the runtime

The runtime path is easiest to understand by following one bounded action.

### 1. Preflight and compilation prepare, but do not execute

At the host boundary, preflight checks whether the required native operations are currently available and records zero spawn attempts. Separately, the route must validate and its authorization must pass before the coordinator compiles a plan for the first eligible wave.

What changed: host availability and the first eligible action plan have separate evidence.

What still does not follow: no worker has started.

### 2. A persisted action becomes the work ticket

The action binds the run, wave, role, capability, target, inputs, outputs, and write boundaries for one job. Persisting it before the host call gives later evidence a stable identity.

What changed: one precise job now exists.

What still does not follow: the host has not accepted or executed it.

### 3. The attempt is recorded before the native call

The causal record marks the action as attempted before the parent invokes the host once. The host returns either a real worker binding or a failure; `record-spawn` persists that result.

What changed: the system can distinguish “we intended to run this” from “we actually called the host” and “the host started a worker.”

What still does not follow: a started worker has not necessarily completed.

### 4. Waiting, terminal observation, and logical close stay separate

The driver registers each expected worker and prepares a mailbox-wide wait. The parent performs the native wait and reconciles only known identifiers; a returned result becomes a terminal observation, followed by one logical close so the worker is accounted for exactly once.

What changed: the host work has reached a known terminal branch and the worker is accounted for.

What still does not follow: its returned receipt has not necessarily been admitted or joined.

### 5. A receipt must be admitted before it can be joined

A receipt is one attributable action result. Admission checks the exact expected receipt files, their required shape and action/run identity, and records which receipt bytes were admitted. It does not prove the contents of artifacts merely referenced inside a receipt. A non-passing receipt can be valid evidence; it simply blocks dependent work.

Joining is the next step. It admits the checked receipt into the wave’s reduction. Waiting for a worker, receiving text, admitting a receipt, and joining it are four different states.

What changed: a checked result may now participate in a gate decision.

What still does not follow: the gate has not necessarily passed, and the result has not become semantic truth.

### 6. A gate decides whether the next transition opens

The gate owner reduces the declared receipts and returns a bounded decision. A passed gate makes a dependent wave eligible. It does not execute that wave. The next actions still need their own persisted plan before another spawn can occur.

What changed: the route permits one declared transition.

What still does not follow: the dependent work has not yet run.

### 7. Closeout accounts for the bounded lifecycle

Closeout binds the terminal history and its outcome. It tells later readers whether the run resolved, blocked, or ended for another declared reason.

What changed: the lifecycle has terminal accounting.

What still does not follow: closeout does not make the result canonical, published, deployed, production-ready, or semantically true.

## What the code actually does

The conceptual relay becomes concrete through small JSON artifacts and deterministic Python stages. The artifacts are the shared interface: strategy describes roles and waves; compilation creates exact work tickets; the event stream records causal order; receipts carry bounded results; reduction decides whether another wave becomes eligible.

Four public code surfaces divide those responsibilities:

- `native_dispatch_coordinator.py` validates a dispatch, compiles one eligible wave into state, a run plan, and action files, then reduces receipts. It does not launch or wait for agents.
- `native_dispatch_driver.py` checks persisted artifacts, prepares exact host requests, records host results, admits receipts, and advances a live wave. It does not invoke `collaboration.*` itself.
- `hosts/codex-native.md` maps abstract operations to Codex-native collaboration tools. The active host tool catalog, not the file alone, determines availability.
- `validate_run_evidence.py` replays `events.jsonl` as a causal state machine. Valid order does not prove that a worker’s claim is true.

The coordinator’s `reduce` command is useful for deterministic offline reduction. Live advancement is stricter: the driver’s `advance-wave` path admits the exact receipt directory, appends joins and a gate event, validates the complete event stream, and only then exposes downstream actions. Treating offline reduction as live closeout would skip evidence that the runtime requires.

### The artifacts are code-level boundaries

The public two-wave fixture compiles its first wave into three actions. Here is a shortened excerpt from one of them:

```json
{
  "action_id": "spawn-0001",
  "wave_id": "checks",
  "role": "beta-check",
  "agent_ordinal": 0,
  "agent_count": 2,
  "capability_ref": "sigil-development",
  "mode": "observe",
  "mutation_policy": "lifecycle-owned",
  "write_scope": ["tmp/native-dispatch/receipts/beta.json"],
  "forbidden_write_scopes": ["arcana/"]
}
```

This is an explanatory excerpt, not a schema-valid action by itself. The complete action also binds dispatch, run, step, target, input, and output identities. The action schema rejects additional fields and restricts mutation policy to a declared set. That rigidity is useful: the host request is derived from an admitted work ticket rather than rebuilt from conversational memory.

The code path recomposes like this:

```text
dispatch JSON
  -> validate-dispatch.py
     -> validation receipt
  -> native_dispatch_coordinator.py compile
     -> state.json + run-plan.json + actions/*.json
  -> native_dispatch_driver.py prepare / host call / record
     -> events.jsonl + native agent bindings
  -> terminal cleanup + exact receipts
  -> native_dispatch_driver.py advance-wave
     -> joined receipts + gate decision + next actions or explicit stop
```

The prepare/host/record split is deliberate. `prepare-spawn` first proves that the persisted action exactly matches the current run plan, appends `action_attempted`, and writes an exact host request. The parent invokes that returned request once through the active native host. `record-spawn` then binds either the returned agent identifier or a spawn failure. A failed spawn is not given a fabricated worker receipt or an implicit retry.

## Try the public fixture without spawning an agent

You can inspect the deterministic half of the runtime without opening a live dispatch. These commands validate and compile repository-owned test data only.

First validate the route shape:

```bash
python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py \
  arcanum/runtime/orchestrate/tests/fixtures/compile/valid-two-wave.json \
  --json
```

The current fixture returns `validation: pass`. Next compile its dependency-free first wave into a temporary directory:

```bash
orchestration_run_dir="$(mktemp -d)"

python3 arcanum/runtime/orchestrate/scripts/native_dispatch_coordinator.py compile \
  arcanum/runtime/orchestrate/tests/fixtures/compile/valid-two-wave.json \
  --run-id beginner-local-001 \
  --output-dir "$orchestration_run_dir"

python3 -m json.tool "$orchestration_run_dir/run-plan.json"
```

Compilation currently produces:

- `validation.json`;
- `state.json`;
- `run-plan.json`;
- three `actions/spawn-*.json` files.

It does not call a host operation. The dependent artifact-writing role is absent because its wave still waits for the checks gate.

You can also validate a complete public event stream:

```bash
orchestration_evidence="$(mktemp)"

python3 arcanum/runtime/orchestrate/scripts/validate_run_evidence.py \
  arcanum/runtime/orchestrate/tests/evidence-order/fixtures/valid-ordered.jsonl \
  --output "$orchestration_evidence"

python3 -m json.tool "$orchestration_evidence"
```

Finally, run the implementation’s focused tests directly. They use Python’s built-in `unittest` entry point; no `pytest` installation is required:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  arcanum/runtime/orchestrate/tests/test_compile_actions.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  arcanum/runtime/orchestrate/tests/test_reduce_receipts.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  arcanum/runtime/orchestrate/tests/evidence-order/test_evidence_order.py
```

At this guide’s latest validation, those files passed 5, 12, and 5 tests respectively. The 22 tests support the deterministic compile, reduction, schema, and causal-order claims above. They do not exercise a live host, prove every driver command end to end, or establish production behavior.

## Read evidence without leaping

Many orchestration errors are not missing data. They are invalid jumps between evidence states.

| Evidence says | It does not yet say |
|---|---|
| The route validated | A human authorized it or a worker ran |
| The material route was confirmed | The dispatch was registered or executed |
| An action was persisted | The host call happened |
| The action was attempted | The host started a worker |
| The host returned a worker binding | The worker completed |
| The worker reached a terminal result | The worker was logically closed or its receipt admitted |
| A receipt exists | The receipt was admitted or joined |
| A receipt was admitted | It participated in reduction |
| A receipt was joined | The gate passed or the content is true |
| The gate passed | A dependent wave executed |
| The run closed | The artifact was promoted, published, deployed, or accepted in production |

This table is a practical debugging tool. When a claim feels too large, move left until you find the last row directly supported by evidence. Then name the missing transition instead of smoothing it over.

## Fail closed: let missing transitions stay missing

Good orchestration does not make failure disappear. It keeps failure from silently changing shape.

If a dependent-wave plan is missing, the next worker does not start. If a spawn fails partway through a wave, the system accounts for workers that did start, fabricates no receipt for work that never ran, and closes the wave through its declared blocked path. If a receipt has the wrong identity or shape, it is not joined merely because useful-looking text exists.

This is what **fail closed** means here: preserve the last supported state and refuse to invent the next one.

The event validator makes several of those refusals executable:

| Invalid event history | Validator error | Boundary protected |
|---|---|---|
| A host result appears without an earlier attempt | `missing_action_attempt` | A host result cannot create its own cause |
| A terminal result appears before a registered wait | `terminal_without_wait` | Later prose cannot synthesize the missing observation |
| A receipt is joined before close or timeout-interrupt cleanup | `join_before_terminal_cleanup` | Returned work is not trusted before worker accounting |
| A gate is decided before every required receipt joins | `gate_missing_joined_receipt` | Eligibility cannot outrun admitted evidence |
| A dependent action is attempted before its gate passes | `dependent_action_before_gate` | A dependency declaration remains an execution barrier |

These error codes are exercised by the public evidence-order fixture matrix. They are more than logging labels: an invalid stream produces a blocking validation receipt, and the CLI returns a non-zero status.

Several useful rules follow:

- Record attempts before side effects so intent cannot be confused with host success.
- Preserve partial evidence at its real scope instead of erasing it or promoting it.
- Keep a non-pass receipt as evidence while blocking its dependents.
- Never reconstruct missing causal events from later prose.
- Treat discovery indexes as leads; direct current evidence controls the claim.
- Separate cleanup from success. Accounting for started workers does not make a failed wave pass.

The result is sometimes less dramatic than “the agents solved it.” It is also far more useful: you know what happened, what did not happen, and where a responsible recovery may begin.

## Keep neighboring capabilities in their lanes

Orchestration becomes easier to reason about when adjacent capabilities keep distinct jobs.

- **Inventory** is a discovery-oriented knowledge read model. It helps locate likely sources, but it is not execution proof or dispatch authority.
- **Craft** owns project work-ledger state. A runtime closeout does not silently update the project ledger.
- **Task Session** executes one bounded task or work unit. It is not the multi-agent scheduler.
- **Continuation Router** selects one explicit next-owner hop. It is not recursive or parallel orchestration.
- **Signal Observer** derives post-run behavior signals. Observation does not become authority over the dispatch.
- **Whisper** composes an accepted evidence package into meaningful text. It does not accept the research, prove the runtime, or authorize publication.

The same rule applies inside a dispatch: a role is a responsibility slot, not an identity and not a grant of wider authority. A worker owns its bounded result. It does not self-approve the collective outcome.

You will also encounter the words **capability**, **sigil**, and **spell** in Arcanum’s descriptive documentation. Treat them as useful descriptive vocabulary while checking the public definitions for terms that actually have formal entries. Do not invent a canonical definition merely because a word is widely used.

## A practical orchestration checklist

Use this sequence when considering a real multi-agent task:

1. **Bound the objective.** Name the artifact or decision you actually need.
2. **Choose helper or dispatch.** Add governance only when differentiation, isolation, parallelism, or dependency gates justify it.
3. **Design disagreements.** Give different workers genuinely different responsibilities instead of cloning the same prompt.
4. **Name every owner transition.** Planning, confirmation, validation, execution, admission, review, and closeout should not collapse into “approved.”
5. **Bind the route.** State inputs, outputs, write scopes, dependencies, stops, and claim ceilings before execution.
6. **Obtain material confirmation.** Authorization applies to the exact proposal presented, not to every nearby variation.
7. **Persist actions before host calls.** Make each attempted job identifiable and bounded.
8. **Separate terminal work from trusted evidence.** Close workers, admit receipts, and join them as distinct steps.
9. **Open dependents only through their gate.** Eligibility still requires a fresh action plan before execution.
10. **Close honestly.** Record resolution, blockage, or residue without converting closeout into truth or release status.

At each step, write one sentence beginning with “What changed” and another beginning with “What still does not follow.” If those sentences are hard to write, the boundary is probably doing hidden work.

## Practice the retell chain

Consider a hypothetical case: one worker returns a compatibility analysis, and a second worker is meant to change the code.

Can the second worker begin merely because the first response looks convincing? No. Apply the last-proven-step loop:

1. Where is the workflow now: was the first action merely attempted, or did it reach a terminal result?
2. What proves the state: does an expected receipt exist, and was it admitted and joined?
3. Who owns the next move: which gate decides whether implementation becomes eligible?
4. What still does not follow: even after a gate pass, is there a persisted bounded action for the second worker?

Now retell the mechanism in four parts:

- **Input:** a bounded task and its current admitted state.
- **Transformation:** a named owner applies one evidence rule.
- **Immediate consequence:** the next state opens or the chain stops explicitly.
- **Later limit:** the transition proves only its own scope, not truth, publication, deployment, production, or human understanding.

If you can retell those four parts, you can inspect a much larger orchestration without memorizing its entire implementation.

For a coding exercise, open the compiled `run-plan.json` from the public fixture and choose one action. Identify its input references, write scope, forbidden scopes, and expected output. Then find the event that would have to exist before each later statement becomes valid: “the host returned,” “the worker finished,” “the receipt joined,” and “the gate passed.” This turns the four-question loop into a source-level debugging method.

## The real change in perspective

Return to the opening task. One agent was asked to inspect, challenge, change, and approve the same work. The solution is not simply to replace that agent with four agents. The solution is to separate the decisions and make each handoff accountable.

When you encounter an agent workflow now, do not begin with “How many agents are running?” Begin with four better questions:

1. What is the last owner-controlled transition that direct evidence supports?
2. What evidence makes that state admissible?
3. Who owns the next decision?
4. What remains unproved even if that decision passes?

That is orchestration’s practical discipline: not maximizing activity, but controlling what each piece of activity is allowed to mean.

## Public source trail

These public Arcanum sources are the next places to inspect in the repository:

- `arcanum/arcana/subagent-strategy/SKILL.md` — dispatch trigger, material confirmation, and lifecycle boundaries.
- `arcanum/formulae/dispatch-spec/SKILL.md` — draft route-shape validation and its non-execution boundary.
- `arcanum/runtime/orchestrate/SKILL.md` — preflight, persisted actions, native execution handshakes, joins, gates, and fail-closed recovery.
- `arcanum/runtime/orchestrate/hosts/codex-native.md` — the Codex-native host operation profile.
- `arcanum/runtime/orchestrate/scripts/native_dispatch_coordinator.py` — deterministic first-wave compilation and receipt reduction.
- `arcanum/runtime/orchestrate/scripts/native_dispatch_driver.py` — exact prepare/record handshakes, live receipt admission, and wave advancement.
- `arcanum/runtime/orchestrate/scripts/validate_run_evidence.py` — causal event-stream validation.
- `arcanum/runtime/orchestrate/schemas/action.schema.json`, `arcanum/runtime/orchestrate/schemas/run-plan.schema.json`, `arcanum/runtime/orchestrate/schemas/receipt.schema.json`, and `arcanum/runtime/orchestrate/schemas/run-event.schema.json` — typed runtime artifacts.
- `arcanum/runtime/orchestrate/tests/fixtures/compile/valid-two-wave.json` and `arcanum/runtime/orchestrate/tests/evidence-order/fixture-matrix.json` — public learning fixtures for valid and blocked paths.
- `arcanum/runtime/orchestrate/tests/test_compile_actions.py`, `arcanum/runtime/orchestrate/tests/test_reduce_receipts.py`, and `arcanum/runtime/orchestrate/tests/evidence-order/test_evidence_order.py` — executable contracts for compilation, reduction, and event order.
- `arcanum/arcana/inventory/SKILL.md`, `arcanum/arcana/craft/SKILL.md`, `arcanum/arcana/task-session/SKILL.md`, `arcanum/arcana/continuation-router/SKILL.md`, and `arcanum/arcana/signal-observer/SKILL.md` — adjacent capabilities with distinct scopes.
- `arcanum/spells/whisper/README.md` — the downstream composition lifecycle and reader-movement guidance.
- `arcanum/definitions/DEFINITIONS.md` — public normative definitions that currently exist.
- `arcanum/README.md` — descriptive vocabulary, including terms whose formal definition work remains open.

This learning guide is a repository-local candidate. It has not been tested for human comprehension, promoted as canonical documentation, published, deployed, or accepted as production evidence.
