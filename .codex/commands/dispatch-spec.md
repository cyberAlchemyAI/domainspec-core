# Arcanum Sigil: dispatch spec

<!-- arcanum:capability-id dispatch-spec -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier formulae -->
<!-- arcanum:command dispatch-spec -->

<!-- arcanum:runtime codex -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-dispatch-spec-<UTC timestamp>`.
- `capability.id`: `dispatch-spec`
- `capability.kind`: `sigil`
- `capability.tier`: `formulae`
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

Run the installed Arcanum sigil `dispatch-spec` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `dispatch-spec`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/formulae/dispatch-spec/README.md

````markdown
# Dispatch Spec

Status: draft Formulae package.

`dispatch-spec` is a deterministic contract for describing how Arcanum sigils and spells are chained, fanned out, debated, validated, and handed off inside a larger spell or bounded route.

It is inspired by Weaver's separation between routing, execution, safe result frames, orchestration, and audit traces. In Arcanum terms, it gives Necronomicon, Spellcraft, Invoke, Task Session, and related owner capabilities a shared object for answering:

- which sigils are being offered or selected,
- what order they run in,
- whether a step is sequential, fan-out, tournament, dialectic, validation, or synthesis,
- which output frame from one step becomes the input substrate for the next,
- what gates, stop conditions, and residue ledgers must exist,
- whether the proposed order should be evaluated before execution,
- which dispatch techniques justify the route shape.

## Purpose

The package turns user language such as:

```text
use dialectics to explore/exploit, then distill, x-ray the architecture, run toy games, and use a Pareto-aware decision process to find the best abstraction
```

into an inspectable dispatch document:

```text
intent -> capability menu -> selected sequence -> gated execution -> frame handoffs -> synthesis -> evaluation
```

The Formulae role is validation, not interpretation. A synthesizing capability such as Necronomicon, Invoke, Spellcraft, Distill, or Structured Interview Kits may propose a dispatch document. `dispatch-spec` checks whether the document is well formed.

## Weaver Mapping

| Weaver Concept | Arcanum Dispatch Concept |
| --- | --- |
| `SelectableItem` | Candidate sigil/spell/mode offered to the operator |
| `ChoiceCard` | Bounded route menu, usually 3-7 viable next sigils or patterns |
| `RoutingDecision` | Selected sigil, spell, mode, or dispatch pattern |
| `Capability` | Named Arcanum sigil, spell, owner capability, or deterministic transform |
| `CapabilityToken` | Permission/approval scope for an execution step |
| `PolicyDecision` | Gate result: allow, deny, ask, defer, or block |
| `Frame` | Safe output summary from a sigil/spell run |
| `Handle` | Reference to a raw artifact, report, HTML page, work-pack, or ledger |
| `TraceEvent` | Observability signal tied to `dispatch_id` and step id |
| ChainWeaver DAG | Spellcraft/Necronomicon dispatch graph |

## Relationship To Arcanum

`dispatch-spec` does not replace the owner capabilities:

- Necronomicon owns repository memory, route selection, and no-promotion guardrails.
- Invoke owns define/design/plan/handoff authoring.
- Spellcraft owns reusable spell composition and lifecycle judgment.
- Distill owns optimization-point selection, tournament reasoning, and recomposition proof.
- Task Session owns bounded execution.
- Experiment Harness owns repeatable validation runs.
- Signal Observer and Workflow Reflect own observed invocation learning.

`dispatch-spec` only validates the shape of a proposed composition.

## Technique Catalog

[TECHNIQUE-CATALOG.md](TECHNIQUE-CATALOG.md) names reusable route-shaping techniques that dispatch documents may cite through `techniques` at the dispatch or step level.

The catalog currently has three source families:

- Arcanum dispatch synthesis techniques such as sequence, zig zag, dialectic, tournament, SCU/SWU reduction, x-ray, toy-game validation, memory loops, frame/handle handoffs, residue ledgers, Pareto gates, and recomposition proof.
- POLE-inspired standards techniques adapted from the 2023 NPCC / Police Digital Services "Minimum POLE Data Standards Dictionary", such as entity classing, minimum component catalogs, component descriptors, conditional obligations, validation rule catalogs, owner/steward metadata, version/status metadata, data-quality dimensions, and orphan-record checks.
- Boundary and evidence techniques for naming delegation boundaries, route projection, execution receipt handoff, approval semantics mapping, artifact contract bridging, state namespace separation, and memory/promotion splits.

The POLE techniques are used as standards-catalog discipline, not policing-domain semantics. They help `dispatch-spec` keep routes system-agnostic, componentized, validated, and traceable.
Boundary and evidence techniques help dispatch documents describe cross-capability and evidence boundaries without making dispatch-spec an execution engine or granting lifecycle promotion authority.

When a route cites boundary/evidence techniques, it can add an optional
`boundary_evidence` block:

```json
{
  "boundary_evidence": {
    "boundaries": [
      {
        "boundary_id": "b1",
        "kind": "capability_handoff",
        "from_owner": "invoke",
        "to_owner": "task-session",
        "applies_to_steps": ["s2"],
        "contract": "Task Session consumes the handoff and returns validation evidence.",
        "on_violation": "block"
      }
    ],
    "authority": {
      "lifecycle": "dispatch-spec",
      "execution": "task-session",
      "validation": "dispatch-spec",
      "promotion": "owning capability"
    },
    "receipts": [
      {
        "receipt_id": "r1",
        "producer": "task-session",
        "required_fields": ["run_id", "artifacts", "validation_result", "residue"],
        "on_missing": "flag"
      }
    ],
    "promotion_splits": [
      {
        "source": "execution evidence",
        "target": "inventory knowledge",
        "rule": "requires owner review before canonical promotion",
        "on_violation": "block"
      }
    ]
  }
}
```

This block validates boundary claims. It does not perform execution or promote
knowledge.

## Files

| File | Purpose |
| --- | --- |
| [dispatch.schema.yml](dispatch.schema.yml) | Draft JSON Schema for dispatch documents. |
| [SKILL.md](SKILL.md) | Formulae execution contract for validating a dispatch document. |
| [WEAVER-EXTRACTION.md](WEAVER-EXTRACTION.md) | Extracted useful concepts from `dgenio/weaver-spec`. |
| [ARCANUM-DISPATCH-SYNTHESIS.md](ARCANUM-DISPATCH-SYNTHESIS.md) | Synthesis, taxonomy, sentence grammar, and example sigil sequences. |
| [TECHNIQUE-CATALOG.md](TECHNIQUE-CATALOG.md) | Reusable dispatch, POLE-inspired standards, and boundary/evidence techniques. |
| [scripts/validate-dispatch.py](scripts/validate-dispatch.py) | Deterministic schema, route-rule, and technique-catalog validator. |

## Validation

Validate one dispatch document:

```bash
formulae/dispatch-spec/scripts/validate-dispatch.py <dispatch.json>
```

Run the package fixtures:

```bash
formulae/dispatch-spec/development/run-validation-fixtures.sh
```

The validator emits `VALIDATION=pass|flag|block` and blocks on schema errors, impossible step dependencies, missing validation evidence, invalid technique references, and false promotion authority claims. It flags weak-but-usable route evidence such as unused technique citations or missing stop conditions.

Technique overlays can be represented with `technique_overlays` when a route needs named profiles such as dialectic review, tournament selection, x-ray explanation, toy-game validation, memory recovery, or protected-context handling. Overlays must name their trigger, techniques, affected steps, and validation expectation.

When a route implies role-bound sibling agents, use `subagent_strategy` to make
the strategy explicit before runtime execution. Dispatch Spec validates the
strategy shape, roles, join policy, receipts, and authorization state; the
orchestrating capability shows the strategy and asks permission before spawning
subagents or running delegated stages.

## First Integration Target

The first useful integration is Necronomicon route planning:

```text
user intent
  -> Necronomicon extracts Arcanum vocabulary and candidate capabilities
  -> dispatch-spec validates the proposed route graph
  -> Spellcraft uses the route graph when the sequence should become a reusable spell
  -> Invoke emits authoring artifacts when define/design/plan material is needed
  -> Observed Invocation Loop records dispatch_id across all steps
```

````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/formulae/dispatch-spec/SKILL.md

````markdown
---
name: dispatch-spec
description: "Use when: validating or designing an Arcanum dispatch route that chains sigils, spells, owner capabilities, handoffs, gates, observability, techniques, and optional boundary/evidence contracts."
argument-hint: "<dispatch.json|route intent> [--validate] [--fixtures]"
tier: formulae
domain: dispatch-governance
version: 0.2.0
origin: Formulae package for Arcanum route-shape validation and boundary/evidence contracts
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Dispatch Spec Skill

## Identity

- Canonical ID: `dispatch-spec`
- Tier: Formulae
- Status: draft
- Scope: repository-local validation package

## Purpose

Validate a dispatch document that describes a sequence, fan-out, tournament, dialectic, validation loop, or synthesis graph over Arcanum sigils and spells.

This skill does not decide which sigils should be used. It checks whether a proposed composition is explicit enough for Spellcraft, Necronomicon, Invoke, Task Session, Experiment Harness, and observability tooling to consume safely.

## Use When

- A user wants to chain sigils by name into a repeatable route.
- Necronomicon proposes an execution route and needs a schema-valid handoff.
- Spellcraft is designing a spell and needs a phase/step contract before lifecycle work.
- Robot-Talks, Distill tournament, or another multi-agent pattern needs sibling steps tied by one `dispatch_id`.
- A run should record how outputs from one sigil become inputs to another.
- A route needs to cite reusable techniques from [TECHNIQUE-CATALOG.md](TECHNIQUE-CATALOG.md), including Arcanum composition techniques or POLE-inspired standards-catalog techniques.
- Refine needs a route artifact for its canonical ten-stage loop without making the Refine process itself the orchestrator.
- Refine or another orchestrating capability needs a visible subagent strategy before asking permission to run delegated or parallel stage work.
- A route needs optional `boundary_evidence` for cross-capability handoffs, authority owners, receipts, state namespaces, or promotion splits.

## Do Not Use When

- The task needs interpretation but no reusable dispatch artifact.
- The user asks for immediate execution of a single, obvious sigil.
- A blocker decision exists about the route itself; use `decision-gate` first.
- The workflow would copy sigil internals instead of referencing sigils by id.

## Required Input

A JSON document conforming to [dispatch.schema.yml](dispatch.schema.yml).

## Deterministic Validator

Use the repository-local validator when available:

```bash
formulae/dispatch-spec/scripts/validate-dispatch.py <dispatch.json>
```

For package fixtures:

```bash
formulae/dispatch-spec/development/run-validation-fixtures.sh
```

## Validation Rules

1. The document must include `dispatch_id`, `intent`, `mode`, `steps`, and `gates`.
2. Each step must reference a known or candidate `capability_ref`.
3. Each step must declare a `pattern`: `route`, `sequential`, `fanout`, `dialectic`, `tournament`, `distill`, `xray`, `decision`, `validation`, `toy_game`, `synthesis`, or `handoff`.
4. Non-first steps must name at least one input source: prior `frame`, `handle`, `decision`, `ledger`, `human_answer`, or `external_context`.
5. Any step with `parallel: true` must declare `join_policy`.
6. Tournament and dialectic steps must declare proposal roles and convergence criteria.
7. Validation and toy-game steps must declare an expected evidence artifact.
8. The dispatch must name stop conditions and at least one observability event.
9. The dispatch must not claim promotion authority for inventory, ontology, glossary, sigil, or spell artifacts.
10. Any cited technique must either appear in `TECHNIQUE-CATALOG.md` or include a local-extension source and validation note.
11. A dispatch that cites techniques without connecting them to steps, gates, evidence, or validation should return `flag`.
12. Technique overlays must name a trigger, technique ids, affected steps, and validation expectation.
13. Dialectic and tournament techniques require roles and convergence criteria even when they are used as step techniques rather than step patterns.
14. X-ray techniques require a handle or artifact output; toy-game techniques require an evidence artifact.
15. Boundary/evidence techniques should be backed by `boundary_evidence`; otherwise the route should return `flag`.
16. `boundary_evidence.boundaries[].applies_to_steps` must reference existing step ids.
17. `state_namespace_boundary` should include `boundary_evidence.state_namespaces`.
18. `memory_promotion_split` should include `boundary_evidence.promotion_splits`.
19. `execution_receipt_handoff` should include `boundary_evidence.receipts`.
20. Execution evidence must not directly promote Inventory, Ontology, glossary, sigil, or spell knowledge.
21. `subagent_strategy.status=recommended|required` must name roles, join policy, authorization, and the reason subagents fit the problem shape.
22. Recommended or required subagent execution should default to `authorization=requires_user_permission` until the operator approves the run.
23. Recommended or required subagent execution must include lifecycle receipt fields: `agent_id`, `role_id`, `spawn_status`, `join_status`, `close_status`, `residue`, and `reroute`.
24. A `subagent_lifecycle.status=pass` ledger must prove every spawned agent reached a terminal join state and terminal close state.
25. Blocked spawn, timed-out join, blocked join, or thread-cap failure only passes as named residue with a reroute or handoff.

## Subagent Strategy

Use `subagent_strategy` when the route shape implies role-bound sibling agents,
parallel critique, tournament comparison, x-ray exploration, memory recovery, or
delegated verification.

Dispatch Spec may recommend or require the strategy, but it does not execute
subagents. The orchestrating capability, usually Refine, must show the strategy
with context and ask permission before runtime execution.

Minimum fields:

- `status`: `none`, `recommended`, `required`, or `blocked`.
- `trigger`: the problem-shape signal that caused the strategy.
- `explanation`: why these roles are useful for this target.
- `context`: target-specific evidence or uncertainty that informed the choice.
- `roles`: role id, purpose, ownership, and affected steps.
- `parallelism`: `none`, `fanout`, `dialectic`, `tournament`, or `mixed`.
- `join_policy`: how returned receipts are joined.
- `authorization`: `not_needed`, `requires_user_permission`, `approved`, or `blocked`.
- `permission_prompt`: the prompt the orchestrator should show before execution.
- `receipt_requirements`: evidence each subagent must return.

## Subagent Lifecycle

Use `subagent_lifecycle` only after a runtime or parent route has attempted
delegated execution. It is the closeout ledger for AFK-safe dispatches: the
parent cannot report success while a spawned sibling agent remains open,
unjoined, hidden, or only implicitly abandoned.

Minimum fields:

- `status`: `none`, `pass`, `flag`, or `block`.
- `agents`: one entry per attempted delegated agent.
- `agent_id`: stable runtime or parent-assigned identifier.
- `role_id`: matching role from `subagent_strategy.roles`.
- `spawn_status`: `spawned` or `blocked`.
- `join_status`: `completed`, `timed_out`, `blocked`, `handed_off`, `closed_without_result`, `pending`, or `not_needed`.
- `close_status`: `closed`, `already_closed`, `handed_off`, `blocked`, `pending`, or `not_needed`.
- `receipt_artifact`: required when `join_status=completed`.
- `residue`: required for blocked spawn, timed-out join, blocked join, or other non-happy-path closeout.
- `reroute`: required when work is handed off, blocked, timed out, or capped by runtime/thread limits.

`status=pass` is only valid when every spawned agent has a terminal join and
terminal close state. Hidden open subagents, pending joins, and pending close
states return `block`.

## Output Contract

```markdown
## Dispatch Spec Result

- Dispatch ID: <dispatch_id>
- Status: pass | flag | block
- Mode: <mode>
- Step count: <n>
- Patterns: <patterns found>
- Gates: <pass | flag | block with reasons>
- Handoffs: <frame/handle/decision/ledger summary>
- Subagent strategy: <none | recommended | required | blocked, roles, join policy, authorization>
- Subagent lifecycle: <n/a | pass | flag | block, open agents, residue, reroute>
- Observability: <dispatch_id coverage and trace events>
- Promotion guardrail: pass | flag | block
- Required repairs: <none or list>
- Next route: necronomicon | spellcraft | invoke | task-session | experiment-harness | decision-gate | deferred
```

## Failure Policy

- Return `block` when required fields are missing, step dependencies are impossible, promotion authority is falsely claimed, or delegated subagents remain unjoined/unclosed.
- Return `flag` when the document is usable but has weak evidence names, candidate capabilities, or incomplete observability metadata.
- Return `pass` only when the route is explicit, gated, observable, and handoff-ready.

````
