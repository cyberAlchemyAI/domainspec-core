# MARS Telemetry Schema

Append-only signals for MARS orchestration, startpoint initialization, experiment execution, evidence closure, and framework retrospection.

Signal log:

- `telemetry/signals.jsonl`

This schema exists so MARS can learn from recurring workflow blind spots, governance friction, evidence blockers, and structural improvement opportunities rather than only from final experiment outcomes.

## Envelope

Required top-level fields:

| Field           | Required    | Notes                                                                            |
| --------------- | ----------- | -------------------------------------------------------------------------------- |
| `id`            | yes         | UUID or stable unique signal ID                                                  |
| `timestamp`     | yes         | ISO-8601 UTC time                                                                |
| `session`       | yes         | session or run grouping key                                                      |
| `project_id`    | yes         | owning research project                                                          |
| `source`        | yes         | `session-epilogue`, `fast-observer`, `async-observer`, or `manual-retrospective` |
| `type`          | yes         | signal type from this schema                                                     |
| `severity`      | yes         | `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`                                              |
| `category`      | yes         | `execution`, `governance`, `evidence`, `discovery`, `pattern`, `operations`      |
| `stage`         | yes         | lifecycle stage or workflow slice that produced the signal                       |
| `data`          | yes         | type-specific payload                                                            |
| `experiment_id` | conditional | required for experiment-scoped signals                                           |
| `run_id`        | conditional | required for run-scoped signals                                                  |

## Categories

- `execution` — how a stage or experiment run progressed
- `governance` — missing controls, contract drift, or required framework hardening
- `evidence` — data, analysis, adjudication, or claim-propagation gaps
- `discovery` — startpoint, scoping, and decision-friction issues
- `pattern` — reusable operational lessons and summaries
- `operations` — cost, latency, and interaction overhead

## Signal Types

| Type                | Category   | Emit When                                                                              | Required `data` Fields                                                             |
| ------------------- | ---------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `stage-verdict`     | execution  | a MARS stage, skill, or major task completes                                           | `stageKey`, `verdict`, `retries`, `artifactsTouched`                               |
| `gate-decision`     | governance | a gate or startpoint check is evaluated                                                | `gate`, `decision`, `blocking`, `remediation`                                      |
| `workflow-gap`      | discovery  | user intent exposed a missing structured workflow, startpoint, or handoff              | `gapClass`, `requestedIntent`, `shouldHaveBeenCaughtBy`, `remediation`, `blocking` |
| `contract-gap`      | governance | required artifacts, registry edges, or structural contracts were missing or incomplete | `artifactClass`, `missingPath`, `remediation`, `blocking`                          |
| `evidence-gap`      | evidence   | data, analysis, adjudication, or claim update could not advance                        | `gapStage`, `claimIds`, `blockedBy`, `remediation`, `blocking`                     |
| `decision-friction` | discovery  | repeated clarification, unresolved options, or decision ambiguity slowed progress      | `decisionClass`, `optionsCount`, `resolutionState`, `followUpNeeded`               |
| `rework`            | execution  | work had to be retried, redirected, or structurally repaired                           | `stageKey`, `iterations`, `rootCause`, `resolution`                                |
| `overhead`          | operations | a session or run completes and aggregate cost/friction is known                        | `stagesExecuted`, `agentDelegations`, `humanQuestions`, `retries`, `overheadRatio` |
| `proposal`          | governance | a concrete framework or skill improvement was identified                               | `targetFile`, `changeDescription`, `rationale`, `priority`                         |
| `pattern`           | pattern    | a reusable lesson or cross-session pattern is worth persisting                         | `summary`, `context`, `applicability`                                              |
| `evidence-update`   | evidence   | claim or evidence status was actually updated                                          | `claimId`, `previousStatus`, `newStatus`, `sourceArtifact`                         |
| `retrospective`     | pattern    | a session-level or experiment-level summary is emitted                                 | `summary`, `wins`, `risks`, `nextActions`                                          |

## Key Modeling Rules

### 1. Workflow-Gap Signals

Use `workflow-gap` when the framework itself lacked a structured response to the user intent.

Typical cases:

- greenfield project requested, but no dedicated startpoint exists
- handoff between interview and protocol design is underspecified
- brownfield normalization depends on undocumented manual steps

Required fields:

- `gapClass` — for example `startpoint-missing`, `handoff-missing`, `workflow-not-modeled`
- `requestedIntent` — what the operator actually asked for
- `shouldHaveBeenCaughtBy` — skill, command, or contract that should own the case
- `remediation` — exact next control or artifact to add
- `blocking` — whether the gap blocked progress

### 2. Contract-Gap Signals

Use `contract-gap` when the workflow existed in principle but the required artifact contract was incomplete.

Typical cases:

- missing `PROJECT.yaml`
- project not added to `research/registry/PROJECT-INDEX.md`
- telemetry schema present but too weak to support reflection

### 3. Evidence-Gap Signals

Use `evidence-gap` when experimentation advanced to a point where data or governance closure was the blocker.

Typical cases:

- analysis missing after data capture
- adjudication policy not strong enough for claim movement
- claim update deferred because source artifact linkage is incomplete

### 4. Decision-Friction Signals

Use `decision-friction` when the operator or agent repeatedly encountered unresolved choices that should be modeled as explicit decision packs, defaults, or templates.

## Example: Greenfield Startpoint Gap

```json
{
  "id": "4de71fd8-bb1b-43d2-a77c-7a6f1c2a4011",
  "timestamp": "2026-04-27T22:10:00Z",
  "session": "greenfield-mogt-init-2026-04-27",
  "project_id": "mars",
  "source": "manual-retrospective",
  "type": "workflow-gap",
  "severity": "HIGH",
  "category": "discovery",
  "stage": "startpoint",
  "data": {
    "gapClass": "startpoint-missing",
    "requestedIntent": "create a new greenfield research project",
    "shouldHaveBeenCaughtBy": "mars-research-start",
    "remediation": "add a dedicated MARS startpoint skill and route interviewer start-intent to it",
    "blocking": true
  }
}
```

## Reflection Threshold Candidates

These are candidate conditions for a future MARS reflection loop or telemetry analyzer.

| ID  | Condition                                                                      | Suggested Action                                            |
| --- | ------------------------------------------------------------------------------ | ----------------------------------------------------------- |
| MT1 | Same `workflow-gap.shouldHaveBeenCaughtBy` appears in 2 or more sessions       | create or harden the owning startpoint or bridge skill      |
| MT2 | Same `contract-gap.artifactClass` appears in 3 or more project initializations | update `mars-research-start` and the relevant template      |
| MT3 | Same `decision-friction.decisionClass` appears in 3 or more sessions           | add AskQuestions pack or decision artifact guidance         |
| MT4 | Same gate BLOCK appears in 3 or more sessions                                  | create a remediation skill or harden the gate prerequisites |
| MT5 | Same `evidence-gap.gapStage` appears in 2 or more experiments                  | update analysis/adjudication workflow and templates         |
| MT6 | `overhead.overheadRatio` > 0.5 for 3 consecutive sessions                      | simplify orchestration or add better defaults               |
| MT7 | 3 or more `proposal` signals target the same file                              | bundle a framework patch                                    |
| MT8 | Any `workflow-gap` with severity `CRITICAL`                                    | immediate framework patch and follow-up retrospective       |

## Invariants

1. Every session that emits `stage-verdict` emits exactly one `overhead` signal.
2. Every applicable gate emits one `gate-decision` signal.
3. Blocked `workflow-gap`, `contract-gap`, and `evidence-gap` signals include remediation details.
4. `evidence-update` references a claim ID and source result artifact.
5. Signal logs are append-only.

## Why This Helps MARS Improve

This schema separates three kinds of learning:

- workflow learning — did MARS have the right command or startpoint for the user's intent?
- governance learning — did the project or experiment contract block progress in a predictable way?
- evidence learning — did the research program fail because of real evidence weakness or because the framework lacked a closure path?

That separation makes later reflection actionable: MARS can improve the framework itself, not just the current project state.
