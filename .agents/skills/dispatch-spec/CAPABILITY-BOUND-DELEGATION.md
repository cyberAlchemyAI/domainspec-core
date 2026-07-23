# Capability-Bound Delegation

Status: contract implemented and fixture-validated in Dispatch Spec 0.3.0;
native subagent runtime integration proof remains pending.

## Problem

The earlier subagent strategy could name useful roles, but it could not prove
which Arcanum capability governed each worker, when a dependent worker was
allowed to start, or where each worker could write. That was sufficient for a
recommendation and insufficient for an executable parent-owned dispatch.

## Decision

Keep Dispatch Spec as a deterministic route contract. Add an opt-in
`binding_mode: capability-bound` for routes that a parent orchestrator will
execute through native subagents.

The change is additive. Existing descriptive `subagent_strategy` documents
remain valid. Capability-bound routes carry stricter proof:

| Contract part | What it establishes in the validated route |
| --- | --- |
| Role capability, target, and mode | Which lifecycle or execution contract governs the worker |
| `agent_count` | How many runtime workers must appear in closeout |
| Inputs and outputs | Which exact receipts cross worker boundaries |
| Mutation policy and scopes | What the worker may and may not change |
| Role dependencies | Which producer receipts a consumer requires |
| Execution waves | Which roles may run together and which must wait |
| Wave join and gate | What must pass before a later wave starts |
| Lifecycle capability, target, mode, wave, and scope | Which runtime agent satisfied which declared role and mutation boundary |

## Concrete Route

The passing fixture models this workflow:

```text
operator approval
       |
       v
wave: lifecycle-updates (parallel, join all)
  +-- Sigil Development -- target: x-ray  -- writes: arcana/x-ray/
  |      returns receipts/xray-iteration.json
  |
  +-- Spellcraft -------- target: whisper -- writes: spells/whisper/
         returns receipts/whisper-iteration.json
       |
       v
gate: both workers passed, joined, and closed
       |
       v
wave: artifact-repair
  Task Session -- artifact-only
  consumes both lifecycle receipts
  writes only examples/architecture-explainer/index.html
  returns receipts/artifact-repair.json
```

The two lifecycle workers may run concurrently because their write scopes do
not overlap. The artifact worker cannot run concurrently with either producer:
it declares both roles and both receipts as dependencies.

## Runtime Boundary

Dispatch Spec validates the graph; it does not spawn agents. The generated
Orchestrate skill is the parent execution contract. It must:

1. validate the dispatch document;
2. require approved authorization;
3. spawn the declared native workers with capability, target, mode, inputs, and scopes;
4. join each wave and enforce its gate;
5. pass exact receipt artifacts into dependent roles;
6. close all workers and populate `subagent_lifecycle`.

The lifecycle skills retain authority over their own artifacts. The final
Task Session worker cannot rewrite X-Ray or Whisper lifecycle surfaces.

## Validator Evidence

- [capability-bound-artifact-repair.json](examples/capability-bound-artifact-repair.json)
  validates the complete synthetic three-worker, two-wave route and closeout shape.
- `block-capability-bound-dependency-same-wave.json` checks that a receipt consumer
  cannot share an execution wave with its producer.
- `run-capability-bound-mutation-tests.py` checks that missing dependency receipts,
  overlapping concurrent writes, missing authorization, incomplete agent
  closeout, capability mismatch, non-receipt outputs, duplicate receipt
  producers, runtime scope drift, failed or absent native receipts, unrelated
  wave gates, aliased paths, and blocked required spawns all block.
- The full fixture runner preserves compatibility with existing descriptive
  subagent strategies.

Run:

```bash
formulae/dispatch-spec/development/run-validation-fixtures.sh
```

## Deliberate Limits

- Dispatch Spec does not choose worker roles; the caller or a routing skill does.
- Dispatch Spec does not decide that lifecycle receipts are semantically good;
  each owning capability supplies its own validation.
- Dispatch Spec does not merge simultaneous edits. Concurrent write-scope
  overlap is blocked instead.
- Runtime thread limits remain parent-owned residue. A blocked spawn must be
  recorded and rerouted rather than silently treated as success.
- These fixtures do not prove native agent spawning. Integration proof still
  requires a host-runtime run that observes spawn, join, gate withholding on a
  failed receipt, dependent launch, and closeout.
