---
name: mars-research-emit-signals
description: "Emit structured MARS telemetry signals after startpoint, discovery, planning, execution, analysis, adjudication, or retrospective work. Use for workflow gaps, contract gaps, evidence gaps, decision friction, overhead, proposals, and reusable patterns that should inform later reflection."
argument-hint: "<project-key> [--experiment <experiment-key>] [--mode startpoint|discovery|planning|execution|analysis|adjudication|retrospective] [--source session-epilogue|fast-observer|async-observer|manual-retrospective] [--dry-run]"
agent: mars-research-scientist
allowed-tools: Read, Write, Bash, Glob, Grep, AskQuestions
---

<objective>
Append structured telemetry signals to `research/projects/<project-key>/telemetry/signals.jsonl` so MARS can learn from workflow friction, governance blind spots, evidence gaps, and recurring improvement opportunities.

This skill is the signal-emission counterpart to later reflection and tuning workflows.
</objective>

<context>
Primary artifacts:
- `research/projects/<project-key>/telemetry/SIGNAL-SCHEMA.md`
- `research/projects/<project-key>/telemetry/signals.jsonl`
- `research/projects/<project-key>/PROJECT.yaml`
- `research/projects/<project-key>/experiments/EXPERIMENTS.md`
- `research/projects/<project-key>/results/*.md`
- `research/projects/<project-key>/registry/TRACEABILITY-MATRIX.md`

Supporting MARS references:

- `implementation/mars/definitions/MARS-PIPELINE.md`
- `implementation/mars/templates/telemetry-signal-schema-template.md`

This skill is append-only. It never edits experiment data, claim status files, or paper text.
</context>

<process>
1. Load the target project's telemetry schema and execution context.
   - Resolve whether the signal set is project-scoped or experiment-scoped.
   - If `--mode` is omitted, infer the highest-confidence mode from changed artifacts.

2. Build signal candidates from session or artifact evidence.
   - Emit `stage-verdict` for the major stages or skills that were executed.
   - Emit `gate-decision` for every applicable gate or startpoint check.
   - Emit `workflow-gap` when operator intent exposed a missing structured workflow, startpoint, or handoff path.
   - Emit `contract-gap` when required project or experiment artifacts were missing, incomplete, or unregistered.
   - Emit `evidence-gap` when analysis, adjudication, claim propagation, or evidence linkage is missing or blocked.
   - Emit `decision-friction` when blocker-level ambiguity, repeated clarification, or competing options slowed progress.
   - Emit `rework` when a stage had to be retried, redirected, or structurally repaired.
   - Emit exactly one aggregate `overhead` signal per session when any stage-verdict signal exists.
   - Emit `proposal` for concrete framework, skill, template, or contract changes suggested by the session.
   - Emit `pattern` for reusable insights that should persist across projects.
   - Emit `evidence-update` when claim or status propagation actually changed.
   - Emit `retrospective` when summarizing the session as a whole.

3. Populate the envelope.
   - Required top-level fields: `id`, `timestamp`, `session`, `project_id`, `source`, `type`, `severity`, `category`, `stage`, `data`.
   - Include `experiment_id` only for experiment-scoped signals.
   - Include `run_id` only for run-scoped signals.

4. Enforce signal invariants before append.
   - If any `stage-verdict` is emitted, emit exactly one `overhead` signal.
   - Every applicable gate emits one `gate-decision` signal.
   - Every blocked `workflow-gap`, `contract-gap`, or `evidence-gap` signal includes `shouldHaveBeenCaughtBy`, `remediation`, and `blocking: true|false`.
   - Every `evidence-update` signal references claim ID and source artifact path.

5. Append JSONL lines to `telemetry/signals.jsonl`.
   - One signal per line.
   - Preserve append-only ordering.
   - If `--dry-run`, return the signals without writing.

6. Return a compact emission summary and recommended follow-up.
   </process>

<quality-bar>
- Signals must be specific enough to support later thresholding and proposal generation.
- `workflow-gap` should name the missing workflow or command explicitly.
- `contract-gap` should name the exact missing artifact class or registry target.
- `proposal` should include exact target file and change intent.
- This skill should prefer fewer high-signal records over many vague ones.
</quality-bar>

<output-contract>
Return:

```markdown
## MARS Signal Emission Summary

- Project: <project-key>
- Experiment: <experiment-key | none>
- Mode: <mode>
- Source: <source>
- Signals emitted: <n>

| Type | Count | Notes |
| ---- | ----- | ----- |

### Follow-Up

1. <action>
2. <action>
```

</output-contract>

<authority-rule>
- This skill only appends telemetry signals.
- It never mutates raw experiment data, evidence status, or paper artifacts.
- Blocking decisions remain owned by the stage or gate that produced the signal; this skill only records them.
</authority-rule>
