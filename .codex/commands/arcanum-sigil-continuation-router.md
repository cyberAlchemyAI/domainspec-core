# Arcanum Sigil: continuation router

<!-- arcanum:capability-id continuation-router -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command arcanum-sigil-continuation-router -->

<!-- arcanum:runtime codex -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-arcanum-sigil-continuation-router-<UTC timestamp>`.
- `capability.id`: `continuation-router`
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

Run the installed Arcanum sigil `continuation-router` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `continuation-router`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/continuation-router/README.md

````markdown
# Continuation Router

Continuation Router is an Arcana sigil for the boundary between one terminal capability run and its next owner. It turns a receipt into visible probable routes, checks exact authorization, dispatches at most one owner capability, joins that owner's receipt, and returns the next route.

It exists because route advice and route execution are different contracts. A blocked Task Session can correctly name `invoke-refresh`, yet a later run may still repeat the blocked task when the handoff is only free text. The router makes that handoff typed and auditable without expanding Task Session into a general workflow engine.

## Use When

- a terminal receipt names or implies a next owner,
- the source capability should not be repeated with unchanged evidence,
- one to three probable routes should be visible before dispatch,
- one exact capability and mode may be authorized for a bounded hop,
- the selected owner must return a separate receipt.

## Do Not Use When

- there is no terminal receipt,
- several independent routes should run in parallel,
- the target needs broad discovery or design,
- a multi-node Craft graph belongs to Goal,
- the caller expects recursive continuation.

## One-Hop Boundary

```text
terminal source receipt
  -> continuation-router ranks 1-3 owner routes
  -> exact authorization and owner gates
  -> at most one owner dispatch
  -> joined owner receipt
  -> returned next route, not auto-executed
```

The router may run in one bounded helper or subagent so the parent receives a clean route result. The helper is an execution strategy, not an authority boundary. The selected owner still owns all semantic work and mutation.

## Authorization

Use an exact route tuple:

```text
--authorize-route invoke:refresh:apply-approved
```

That grant authorizes only that capability, mode, and mutation mode for the declared target and write scope. It does not authorize a different owner, recursive continuation, destructive cleanup, or a broader mutation.

Without exact authorization, the router may still return probable routes, but it does not dispatch a consequential route.

## Common Routes

- planning drift -> `invoke:refresh`;
- blocker-level human choice -> `decision-gate:blocker`;
- one ready task or SWU -> `task-session:execute`;
- vague target -> `refine:standard` or an Invoke authoring mode;
- broad Craft graph -> `goal:execute`;
- missing evidence or unsafe scope -> `stop:user-input`.

These are candidate patterns only. Installed owner contracts and the source receipt remain authoritative.

## Artifacts

- [SKILL.md](SKILL.md) defines routing, authorization, dispatch, and receipt behavior.
- [continuation-route.schema.json](continuation-route.schema.json) defines the durable machine receipt.
- `development/` holds Experiment Harness evidence and route-specific fixtures.

## Why This Is Arcana

Continuation Router coordinates evidence, authority, dispatch, helper lifecycle, and owner receipts across capabilities. It is not a deterministic formatter and it does not perform the selected owner's work.


````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/continuation-router/SKILL.md

````markdown
---
name: continuation-router
description: "Use when: a terminal capability receipt names or implies a next owner route and the caller needs ranked probable routes, explicit authorization checks, one bounded dispatch, and a returned owner receipt without re-running the blocked source capability."
argument-hint: "--receipt <path> [--authorize-route <capability>:<mode>[:<mutation-mode>]] [--dispatch] [--dry-run] [--output <path>]"
tier: arcana
domain: continuation-routing
version: 0.1.0
origin: extracted from repeated Task Session terminal receipts whose next-owner advice was not consumed
allowed-tools: Read, Write, Glob, Grep, Task, Bash
---

# Sigil: Continuation Router

<objective>
Turn one terminal capability receipt into an auditable one-hop continuation: expose one to three probable owner routes, dispatch at most one exactly authorized route, join its terminal receipt, and return the next route without performing the owner's mutation itself.
</objective>

<logic-type>
Arcana: bounded cross-capability routing with explicit authorization, owner isolation, receipt joining, and cycle prevention.
</logic-type>

<flags>
- `--receipt <path>`: load the terminal source receipt to normalize and route.
- `--authorize-route <capability>:<mode>[:<mutation-mode>]`: grant only the exact route tuple named by the caller. It does not grant any other mode, target, write scope, destructive action, cost, or nested continuation.
- `--dispatch`: execute one selected route after all route and owner gates pass.
- `--dry-run`: return probable routes and selection reasoning without dispatch.
- `--output <path>`: persist the human result and adjacent machine route receipt when the runtime supports it.
</flags>

<applicability>
Use this sigil when:

- a completed, blocked, or flagged capability run produced a terminal receipt,
- the receipt names a next capability or contains enough evidence to rank probable owners,
- repeating the source capability would reproduce an unchanged blocker,
- the caller wants the next owner route made visible before any dispatch,
- one bounded owner handoff is sufficient.
</applicability>

<non-applicability>
Do not use this sigil when:

- no terminal receipt or equivalent evidence exists,
- the request is a broad multi-node Craft objective that belongs to `goal`,
- the target is still vague and needs `refine` or Invoke authoring,
- a human choice must be resolved by `decision-gate`,
- several independent routes should run in parallel,
- the caller expects recursive autonomous continuation.
</non-applicability>

<inputs>
Required:

- terminal receipt or equivalent structured run evidence,
- source capability, mode, result, target scope, blockers or residues, and next-route advice when present,
- installed capability catalog or canonical registry evidence,
- current caller intent.

Required for dispatch:

- exact selected capability and mode,
- all inputs required by the selected owner,
- exact target and write scope for a mutating route,
- explicit route authorization when the owner mode is consequential,
- expected terminal receipt shape,
- bounded runtime or helper lifecycle that can be joined.
</inputs>

<route-catalog>
Use installed contracts as authority. These are common candidates, not hardcoded permission:

| Evidence pattern | Probable owner route | Dispatch gate |
| --- | --- | --- |
| Planning artifact drift, contradictory work-pack state, or post-run plan synchronization | `invoke:refresh` | `proposal-only` by default; `apply-approved` only with exact authorization plus target inventory, delta scope, and validation. |
| Consequential unresolved human choice | `decision-gate:blocker` | Never auto-select a consequential option from route confidence alone. |
| Exactly one dependency-ready task or SWU | `task-session:execute` | Fresh context pack and no unchanged blocker fingerprint. |
| Vague target, unclear concept boundary, or missing design convergence | `refine:standard` or an Invoke authoring mode | No target mutation through the router. |
| Broad Craft-backed graph with several dependent nodes | `goal:execute` | Goal approval, graph frontier, and staged-delta rules apply. |
| Missing evidence, unavailable owner, or unsafe scope | `stop:user-input` | Return the exact unblock evidence; do not dispatch. |
</route-catalog>

<process>
## Step 1 - Normalize The Source Receipt

1. Read the terminal receipt and preserve its source path.
2. Normalize source capability, mode, result, target scope, blocker class, residues, explicit next route, and required unblock actions.
3. Compute a stable blocker fingerprint from the source capability, source mode, target scope, blocker class, controlling evidence identities or digests, and requested continuation.
4. If required receipt fields are missing, adapt legacy text conservatively and mark inferred fields. Never infer apply authorization.

## Step 2 - Detect Repeated Or Cyclic Continuation

5. Compare the blocker fingerprint with any supplied previous continuation receipt.
6. If the same fingerprint would re-enter the same source capability and mode, reject that candidate.
7. If the route history already contains the same capability, mode, target, and fingerprint tuple, return `BLOCK` with `cycle-detected`.
8. Limit one invocation to one owner dispatch. A returned next route is reported, not recursively executed.

## Step 3 - Build Probable Routes

9. Resolve candidate owners from, in order: an explicit receipt handoff, an owner-defined downstream contract, installed capability evidence, then semantic fit.
10. Normalize route aliases, such as `invoke-refresh`, to a capability and mode tuple such as `invoke:refresh`.
11. Rank one to three candidates by controlling evidence, owner fit, required-input completeness, authorization state, mutation risk, and expected receipt strength.
12. For each candidate record capability, mode, optional mutation mode, owner, evidence, required and missing inputs, mutation risk, approval requirement, authorization state, expected receipt, and fallback.
13. Show probable routes before selection or dispatch.

## Step 4 - Select And Gate One Route

14. Select one candidate only when its evidence is unambiguous and all required inputs are present.
15. Treat `--authorize-route` as an exact tuple. A grant for `invoke:refresh:apply-approved` does not authorize Task Session execution, a different target, a broader write scope, or another hop.
16. For a consequential or mutating route, require the owner contract's own approval, inventory, scope, and validation gates in addition to route authorization.
17. If authorization is missing, return the ranked routes with selection status `not-authorized`; do not dispatch.
18. If candidates remain ambiguous, return selection status `ambiguous`; do not choose from ranking score alone.

## Step 5 - Dispatch Through The Owner

19. When `--dispatch` is set and the selected route passes, invoke the canonical owner capability through the native runtime surface.
20. Prefer one bounded helper or subagent when isolation is available; otherwise invoke inline with the same route packet and receipt contract.
21. Pass only the selected target, required inputs, exact authorization evidence, declared write scope, and validation surface.
22. The router must not edit owner target artifacts, reinterpret owner gates, or report owner work as router work.
23. Join the helper and require a separate terminal owner receipt. An open, hidden, timed-out-without-residue, or unjoined helper is `BLOCK`.

## Step 6 - Return The Joined Result

24. Validate the owner receipt against the expected receipt shape and selected route tuple.
25. Preserve the source result; a successful continuation does not rewrite the source `BLOCK` as Task Session success.
26. Return continuation status, selected owner route, owner receipt, mutations attributed to the owner, validation, and the owner's returned next route.
27. Persist a machine receipt conforming to `continuation-route.schema.json` when an output path is requested or repository conventions require durable evidence.
</process>

<authority-rule>
The router owns route ranking, exact authorization matching, bounded dispatch, and receipt joining. It never owns the selected capability's semantic work or mutation. A route string is evidence of destination, not authority to mutate.
</authority-rule>

<observability>
A meaningful execution is a terminal receipt that produces ranked routes, a route selection, a dispatch attempt, or an owner receipt.

Emit:

- source capability, mode, result, receipt, and blocker fingerprint,
- candidate count and ranked capability/mode tuples,
- authorization requested, matched, or missing,
- selection status and rejection reasons,
- dispatch status and runtime isolation,
- helper spawned, joined, closed, blocked, timed out, and open counts,
- owner receipt path and validation,
- returned next route,
- cycle detection and owner-boundary violations,
- quality-bar status, anti-pattern hits, workflow gaps, and reflection trigger.

Reflect after five meaningful executions, three related routing gaps, or immediately after unauthorized dispatch, repeated-route cycling, direct owner mutation, or an unjoined helper.
</observability>

<quality-bar>
A successful execution must:

- consume exactly one terminal source receipt,
- preserve the source result and owner boundaries,
- compute and expose a stable blocker fingerprint,
- return one to three probable routes before dispatch,
- identify capability, mode, owner, evidence, inputs, approval, risk, and expected receipt for every candidate,
- dispatch at most one route,
- require an exact authorization tuple for consequential owner modes,
- run the selected owner's own gates without weakening them,
- prevent unchanged source re-entry and repeated route cycles,
- join a separate terminal owner receipt,
- return the owner's next route without recursively executing it,
- emit a schema-valid machine receipt when persisted,
- keep public examples product-neutral.
</quality-bar>

<anti-patterns>
Avoid:

- treating free-text `next_route` as mutation approval,
- performing owner mutation inside the router,
- ranking more than three routes,
- selecting an ambiguous route because it scored first,
- re-running an unchanged blocked source capability,
- recursive continuation or more than one dispatch per invocation,
- using Goal for a deterministic one-hop owner handoff,
- using the router for independent parallel work,
- hiding missing inputs, approvals, helper lifecycle gaps, or owner validation failures,
- reporting the source task as successful because the continuation owner succeeded,
- leaking consuming-project names or private evidence into the public package.
</anti-patterns>

<output-contract>
Return:

```markdown
## Continuation Route Result

- Source: <capability>:<mode> — <result>
- Source receipt: <path>
- Blocker fingerprint: <stable identifier>
- Probable routes:
  1. <capability>:<mode>[:<mutation-mode>] — <owner, evidence, missing inputs, risk, approval, authorization, expected receipt>
- Selection: selected | ambiguous | not-authorized | blocked | none
- Selected route: <exact tuple | none>
- Dispatch: not-requested | not-authorized | blocked | completed | flagged
- Owner boundary: pass | block
- Helper closeout: n/a | pass | flag | block, <counts and residue>
- Owner receipt: <path | none>
- Owner validation: <summary | none>
- Returned next route: <capability>:<mode> <target | none>
- Follow-up: <one exact action | none>
```

When persisted, also emit a JSON receipt conforming to `continuation-route.schema.json`.
</output-contract>


````
