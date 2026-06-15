# Arcanum Sigil: x ray

<!-- arcanum:capability-id x-ray -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command x-ray -->

<!-- arcanum:runtime codex -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-x-ray-<UTC timestamp>`.
- `capability.id`: `x-ray`
- `capability.kind`: `sigil`
- `capability.tier`: `arcana`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.


## Objective

Run the installed Arcanum sigil `x-ray` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `x-ray`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/x-ray/README.md

````markdown
# x-ray

`x-ray` is an Arcana sigil seed for turning a target object, artifact, architecture, codebase, process, or mixed context into a visual layered HTML explanation page.

It is meant for moments when the important structure is present but hard to see: dependencies hidden in prose, concepts spread across a plan, modules buried in a codebase, or process steps implied by an operational description.

## Status

Status: seed.

This package defines the revised lane model, renderer ladder, and validation direction for `x-ray`. It is not promoted and does not yet include reusable behavior evidence from live examples.

## Problem It Solves

Raw context can be hard to inspect because structure is often implicit. A system description may hide actors, transformations, data flow, dependencies, decisions, and open questions inside prose, code, diagrams, or planning notes.

`x-ray` makes that structure visible by splitting a target into explanation lanes. Each lane gives one vision of the target, such as properties, components, internal dependencies, external dependencies, flow, lifecycle, or risk questions. The lane handles compose into a local HTML page where layers can be stacked, isolated, compared, or traced.

`x-ray` should also make the structure learnable. The output must not assume the reader already knows the target's domain vocabulary. Important concepts need a small on-ramp: what the thing is in ordinary language, why it matters here, what it changes or depends on, and only then the local technical label.

## Modes

| Mode | Use When |
| --- | --- |
| `object` | Explain a bounded conceptual, data, or domain object. |
| `artifact` | Explain a document, spec, plan, deck, or generated artifact. |
| `architecture` | Explain a system, subsystem, component graph, or design architecture. |
| `codebase` | Explain a repository, package, module, or source subtree. |
| `process` | Explain an operational, human, or system workflow. |
| `mixed` | Explain a target that legitimately combines multiple shapes. |

## Canonical Lanes

| Lane | What It Shows |
| --- | --- |
| `surface` | What the target appears to be and why it is being inspected. |
| `properties` | Important attributes, invariants, metadata, constraints, and state. |
| `components` | Internal parts and their purposes. |
| `internal_dependencies` | Dependencies among parts inside the target. |
| `external_dependencies` | Services, libraries, APIs, people, policies, or artifacts outside the target. |
| `flow` | Data, control, work, or meaning movement. |
| `lifecycle` | Creation, operation, mutation, validation, failure, and retirement states. |
| `risk_questions` | Ambiguity, missing evidence, contradictions, risks, and open questions. |
| `visual_composition` | How lane handles map into the HTML/SVG layer stack and optional adapters. |

## Output Model

The target output is a single local HTML explanation page.

The first renderer level is intentionally simple:

- semantic HTML,
- inline CSS,
- inline SVG,
- layer controls,
- source evidence and inference markers,
- internal and external dependency sections.

Each page should declare a reader baseline:

| Reader Baseline | Use When | Explanation Style |
| --- | --- | --- |
| `newcomer` | The reader may not know the domain or target vocabulary. | Define terms at first use, explain why each layer matters, and show cause/effect step by step. |
| `working-reader` | The reader knows the general domain but not this target's local structure. | Keep local terms compact but explain target-specific boundaries, dependencies, and failure points. |
| `expert` | The reader knows the domain and needs a fast structural inspection. | Use compact labels while preserving evidence, inference, and local boundary clarity. |
| `unknown` | The prompt does not reveal the audience. | Default prose to `newcomer` and visual labels to `working-reader`. |

Later renderer levels may add Mermaid diagrams, CSS 3D transforms, Three.js, or Kroki-generated SVG, but those are optional adapters. A valid baseline `x-ray` result must not depend on remote rendering or 3D.

## Visual Library

The starter visual library lives in [library/](library/). It is a YAML-backed catalog for HTML/SVG x-rays, not a renderer engine.

- [components.yml](library/components.yml) is the canonical source for starter shapes, connectors, and tiny charts: node, boundary, layer panel, risk marker, arrow, branch, feedback loop, timeline strip, and risk matrix.
- [patterns.yml](library/patterns.yml) is the canonical source for starter compositions: process branch, dependency boundary, lifecycle stack, and evidence/inference split.
- [user-shapes-template.yml](library/user-shapes-template.yml) is the canonical template for custom shapes, charts, and patterns when the target has a domain-specific form.
- Markdown files in [library/](library/) are companion docs for reading and navigation.

Add your own shape, chart, or pattern when the starter set cannot represent the target honestly. Custom visuals should name the lane served and the source evidence or inference they represent.

## Use When

- a user supplies context and wants to understand it step by step,
- the target is an object, artifact, architecture, codebase, process, workflow, plan, or mixed system,
- an HTML explanation page is a useful output format,
- properties, components, internal dependencies, external dependencies, flow, lifecycle, and open questions matter,
- visual or diagram-like structure would clarify the target.

## Do Not Use When

- the user only wants a short text summary,
- the task is direct implementation rather than explanation,
- the source context is too sensitive to transform into a generated artifact,
- the target is too broad and no bounded scope is provided,
- the output needs a production-grade visual renderer,
- live experiment evidence is required but has not been collected.

## Ownership Model

| Capability | Owner |
| --- | --- |
| Seed execution | Task Session |
| Sigil lifecycle | Sigil Development |
| Experiment mechanics | Experiment Harness |
| Runtime handoff | Codex Goal adapter when strict coverage passes |
| Promotion readiness | Sigil Development after live examples |

## Development

The original seed work-pack lives at [development/WORK-PACK.md](development/WORK-PACK.md).

The visual layered revision artifacts live under [development/invoke-runs/20260529T112301Z-visual-layered-xray](development/invoke-runs/20260529T112301Z-visual-layered-xray).

Promotion requires live examples for at least one object or component, one process, one architecture or codebase, one generated L0 HTML/SVG output, and one insufficient-context block or flag.

````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/x-ray/SKILL.md

````markdown
---
name: x-ray
description: "Use when: turning user-supplied context about an object, artifact, architecture, codebase, process, or system into a visual layered HTML explanation page with properties, components, flows, dependencies, and evidence boundaries."
argument-hint: "<context-or-path> [--mode object|artifact|architecture|codebase|process|mixed] [--depth quick|standard|deep] [--output <html-path>]"
tier: arcana
domain: context-explanation
version: 0.2.0-seed
origin: revised from visual layered x-ray refine and invoke define/design/plan artifacts
allowed-tools: Read, Write, Glob, Grep, AskQuestions, Bash
---

# Sigil: x-ray

<objective>
Dissect a target object, artifact, architecture, codebase, process, or mixed context into explanation lanes, then compose those lanes into a local visual HTML x-ray page where layers can be stacked, isolated, compared, or traced.
</objective>

<logic-type>
Arcana: dispatch-spec governed explanation and visual-structure orchestration for hidden target structure.
</logic-type>

<status>
Seed. This contract defines the revised lane model, renderer ladder, and validation surface. It is not promoted and does not yet prove live reusable behavior.
</status>

<modes>
Supported inspection modes:

| Mode | Use When | Required Emphasis |
| --- | --- | --- |
| `object` | The target is a bounded conceptual, data, or domain object. | properties, relationships, lifecycle, dependencies |
| `artifact` | The target is a document, spec, plan, deck, or generated artifact. | intent, structure, claims, evidence, gaps |
| `architecture` | The target is a system, subsystem, component graph, or design architecture. | components, boundaries, flows, internal dependencies, external dependencies |
| `codebase` | The target is a repository, package, module, or source subtree. | entrypoints, modules, internal dependencies, external dependencies, tests, flows |
| `process` | The target is an operational, human, or system workflow. | actors, steps, decisions, transformations, handoffs |
| `mixed` | The target combines more than one shape. | explicit lane selection and omitted-lane reasons |
</modes>

<canonical-lanes>
Every run selects a bounded lane set. A lane is one vision of the target and must emit a handle that later composition can consume.

| Lane | Vision | Output Handle |
| --- | --- | --- |
| `surface` | What the target appears to be and why the user is inspecting it. | `surface.summary` |
| `properties` | Important attributes, invariants, metadata, constraints, and state. | `properties.catalog` |
| `components` | Internal parts and their purposes. | `components.map` |
| `internal_dependencies` | Dependencies among internal parts, modules, sections, stages, or concepts. | `dependencies.internal` |
| `external_dependencies` | Services, libraries, APIs, people, policies, documents, or systems outside the target. | `dependencies.external` |
| `flow` | Data, control, work, or meaning movement through the target. | `flow.graph` |
| `lifecycle` | Creation, operation, mutation, validation, failure, and retirement states. | `lifecycle.timeline` |
| `risk_questions` | Ambiguity, missing evidence, contradiction, risk, and open questions. | `risk.questions` |
| `visual_composition` | Instructions for mapping lane handles to HTML, SVG, Mermaid, and optional 3D layers. | `visual.model` |
</canonical-lanes>

<renderer-ladder>
Use the smallest renderer that can explain the target clearly.

1. L0: single local static HTML page with semantic HTML, CSS, and inline SVG.
2. L1: conservative Mermaid source blocks for flow, dependency, and architecture diagrams.
3. L2: in-browser Mermaid rendering only when artifact policy allows it.
4. L3: CSS 3D transforms for depth-separated layer panels.
5. L4: optional Three.js or CSS3DRenderer for spatial exploration when a target genuinely benefits from 3D.
6. Optional external adapter: Kroki-generated SVG only when privacy, network, and local policy allow it.

L0 is the default proof path. Remote or 3D rendering must never be required for a valid `x-ray` result.
</renderer-ladder>

<applicability>
Use this sigil when:

- the user provides context and wants to understand what it is about,
- the target is an object, artifact, architecture, codebase, process, plan, workflow, or mixed system,
- important structure is hidden inside prose, code, diagrams, plans, or repository layout,
- the explanation should expose properties, components, flows, dependencies, transformations, assumptions, and open questions,
- a local HTML explanation page is the desired output surface,
- visual layers or diagram-like structure would make the target easier to inspect.
</applicability>

<non-applicability>
Do not use this sigil when:

- a short plain-language summary is enough,
- the user wants direct implementation instead of explanation,
- the source context is too sensitive to transform into a generated artifact,
- the target is too large and the user has not provided a bounded scope,
- a production renderer or polished design system is required immediately,
- there is not enough context to identify the object under inspection.
</non-applicability>

<inputs>
Expected inputs:

- supplied context text or a path to local context,
- optional inspection mode: `object`, `artifact`, `architecture`, `codebase`, `process`, or `mixed`,
- optional user question or intent,
- optional output path for the HTML page,
- optional depth, audience, privacy, or visual style constraints.
</inputs>

<reader-onramp>
An `x-ray` page must teach the target to a reader who may not already know the domain.

Before composing the visual page, identify the likely reader baseline from the user request or source context:

- `newcomer`: needs plain definitions, why-it-matters framing, and step-by-step causality.
- `working-reader`: understands the domain category but not this target's local structure.
- `expert`: can handle compact terms, but still needs local evidence and boundary clarity.
- `unknown`: default to `newcomer` for explanation text and `working-reader` for labels.

For every important lane, provide an on-ramp before the detail:

1. Name the thing in ordinary language.
2. Say why it matters in this target.
3. Explain what changes, moves, depends on it, or can fail because of it.
4. Only then introduce local terms, handles, or technical labels.

When the target has dense vocabulary, use a local reader glossary pattern: plain term, plain meaning, why it matters here, source or lane, and misuse warning. Keep this glossary explanatory; do not promote local x-ray terms into canonical project definitions.

When the page has multiple visual layers, give each layer a reader outcome: what the reader should understand after inspecting that layer and why the layer matters to the target.

Avoid explanations that require prior knowledge of the target's domain vocabulary. If a technical term is unavoidable, define it where the reader first needs it. Visual labels may be compact, but adjacent text must make the label understandable.
</reader-onramp>

<process>
1. Resolve the input context and identify the target boundary.
2. Select an inspection mode or ask one clarification question when mode ambiguity changes the lane set.
3. Identify the reader baseline and explanation depth from the request; when unknown, default to newcomer-friendly prose.
4. Build an evidence boundary that separates source-backed facts from inference.
5. Select the required lanes for the mode and record omitted-lane reasons.
6. Produce lane handles for surface, properties, components, internal dependencies, external dependencies, flow, lifecycle, risk questions, and visual composition as relevant.
7. Add reader on-ramps for important lane content: plain name, why it matters, causal role, then local or technical term.
8. Select YAML-backed visual library components and patterns from `arcana/x-ray/library/` that fit the lane handles.
9. Nudge the user to add a custom shape, chart, or pattern when the target has a domain-specific form that the starter library cannot represent honestly.
10. Compose the lane handles into an HTML page model with selectable visual layers, local reader glossary entries, layer reader outcomes, and scan-friendly explanatory blocks.
11. Use L0 static HTML/SVG by default; add Mermaid or 3D adapters only when they clarify the target and validation remains available.
12. Validate that every visual element maps back to source evidence or an explicit inference, and that every important technical label has a nearby plain-language explanation.
13. Report missing context, unsupported visual adapters, or target-size blockers honestly.
</process>

<output-contract>
Return:

```markdown
## x-ray Result

- Status: pass | flag | block
- Mode: object | artifact | architecture | codebase | process | mixed | unknown
- Target boundary: <resolved scope or blocked reason>
- User intent: <resolved intent or open question>
- Reader baseline: newcomer | working-reader | expert | unknown
- Output: <html path or planned output>
- Lane handles:
  - surface: <handle or omitted reason>
  - properties: <handle or omitted reason>
  - components: <handle or omitted reason>
  - internal_dependencies: <handle or omitted reason>
  - external_dependencies: <handle or omitted reason>
  - flow: <handle or omitted reason>
  - lifecycle: <handle or omitted reason>
  - risk_questions: <handle or omitted reason>
  - visual_composition: <handle or omitted reason>
- Layer interaction: stacked | isolate | compare | trace | planned
- Renderer level: L0 | L1 | L2 | L3 | L4 | blocked
- Visual library: <YAML components/patterns used and custom shape/chart/pattern nudge if relevant>
- Evidence boundary: <source-backed facts vs inference>
- Reader on-ramp: <plain-language definitions, why-it-matters framing, or omitted reason>
- Validation: <checks performed or blocked reason>
```
</output-contract>

<quality-bar>
A successful `x-ray` run must:

- identify the mode and target boundary,
- preserve the user's inspection intent,
- produce a structured explanation rather than a loose summary,
- teach prerequisite concepts before relying on target-specific jargon,
- make each important technical label understandable to a reader without assumed prior domain knowledge,
- include properties, components, flows, internal dependencies, external dependencies, assumptions, and open questions when relevant,
- emit lane handles that can be consumed by the visual composition step,
- use reusable YAML-backed visual components and patterns only when they preserve the evidence/inference boundary,
- make the HTML visual layer model inspectable without requiring remote services,
- keep generated visual structure tied to the source context,
- distinguish evidence from inference,
- report blockers when context is insufficient or the target is too broad,
- preserve seed status until Sigil Development and Experiment Harness evidence support promotion.
</quality-bar>

<anti-patterns>
Avoid:

- inventing system structure not grounded in supplied context,
- producing decorative visuals that do not explain the target,
- skipping the user's intent and defaulting to generic documentation,
- using expert shorthand where the reader needs a plain-language bridge,
- drawing labels, arrows, or layers whose meaning is only clear to someone who already understands the target,
- treating every target as software architecture,
- claiming production renderer readiness from seed artifacts,
- requiring Mermaid, Three.js, Kroki, or remote rendering for baseline success,
- using 3D to make the page impressive when simple SVG would explain better,
- analyzing an entire codebase when the user provided no bounded scope,
- promoting the sigil before live examples exist.
</anti-patterns>

<observability>
For meaningful executions, record:

- mode,
- target boundary,
- input size and source shape,
- clarification needed or not,
- selected lanes and omitted-lane reasons,
- renderer level,
- output path or blocked reason,
- evidence/inference boundary quality,
- internal and external dependency coverage,
- missing-context gaps,
- user correction signals.
</observability>

<promotion-gate>
Promotion requires Sigil Development review plus Experiment Harness evidence for:

- one object or component example,
- one process example,
- one architecture or codebase example,
- one generated L0 HTML/SVG output body,
- one blocked or flagged example showing insufficient context handling,
- one validation pass that checks lane presence, evidence boundaries, and HTML structure.
</promotion-gate>

````
