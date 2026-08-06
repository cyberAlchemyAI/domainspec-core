# The Intent Route System: A Beginner's Guide

## The short version

This system is a **GPS for agent work, not a self-driving car**.

You tell it what you want. It compares that intent with a small, fixed catalog
of possible routes. Then it returns one of four answers:

- **candidate** — one route fits;
- **ambiguous** — more than one route may fit, so it asks a precise question;
- **no-match** — none of the known routes fit;
- **invalid** — the request or catalog is malformed or inconsistent.

Even when it finds a candidate, it does not start work. A person must confirm
the route, and the existing runtime must authorize and bind the work. The
router never approves, schedules, spawns, writes product state, or claims that
an effect happened.

That is the central design rule:

> The resolver can point. It cannot grant permission or act.

## Why build this?

An agentic system can have many ways to handle a request: answer directly,
clarify the request, invoke an Arcanum capability, use an existing Augmentor
handler, or stop because no safe route exists.

Without a small routing contract, every runtime may invent its own hidden
decision logic. That creates three problems:

1. the same intent can take different routes in different hosts;
2. uncertainty is often hidden instead of presented to the user;
3. a routing suggestion can accidentally become permission to execute.

The intent route system separates those concerns. It makes the routing answer
deterministic and inspectable while leaving approval and execution with their
existing owners.

## Five terms to learn first

### Intent

The user's goal in plain language, plus any facts needed to distinguish one
route from another. For example: “Research whether this architecture is safe”
may include a discriminator such as `work_kind = research`.

### Request

The closed, versioned JSON record built from the intent. “Closed” means unknown
extra fields are rejected instead of silently ignored.

### Catalog

A finite list of routes the current host is willing to show the resolver. The
catalog is read-only and carries a content digest—a SHA-256 fingerprint—so the
request and response can be tied to the exact catalog bytes that were used.

### Disposition

The resolver's answer: `candidate`, `ambiguous`, `no-match`, or `invalid`. A
disposition always has `authority_effect: none`.

### StrategyProposal

A ResonantOS-owned proposal assembled only after a verified candidate returns.
It adds the product information needed for a possible launch, such as the
current profile, grants, expiry, gates, children, and expected results. It is
still a proposal, not approval.

## Meet the components

### 1. Augmentor — the conversational surface

Augmentor is where the user sees and shapes the interaction. It can capture
intent, display a candidate, show a clarification question, and render a
`StrategyProposal`.

Augmentor does **not** edit the route catalog, fill in unresolved facts, choose
between ambiguous routes, treat a candidate as approval, bind a workflow, or
start owner operations.

Think of Augmentor as the dashboard and conversation—not the engine or the
traffic authority.

### 2. ResonantOS request normalizer — the form builder

The normalizer turns the user's current intent into the exact
`intent-route.request@1` shape. If required information is missing or malformed,
it rejects the request instead of guessing.

### 3. ResonantOS catalog projector — the menu builder

The projector builds the finite `intent-route.catalog@1` menu for this product
context. It decides which product routes are visible to the generic resolver,
but it does not decide which route wins and does not grant execution.

### 4. The host adapter — the guarded doorway

The adapter is the safety boundary between an agent runtime and the standalone
resolver process. Before starting that process, it checks the pinned executable,
entrypoint, version bindings, and package closure. It then:

- sends one size-bounded JSON request;
- exposes only a minimal process environment;
- enforces a timeout;
- accepts exactly one stdout JSON document and zero stderr;
- verifies protocol versions and the package closure digest;
- verifies that the response names the exact request and catalog submitted.

The current orchestrator policy is deliberately disabled until the add-on is
installed at the pinned location.

### 5. The public Arcanum resolver — the pure comparison

The public `intent-route-resolver` is a standalone, zero-dependency ECMAScript
module. It compares the normalized request with the digest-bound catalog and
returns a disposition.

It has no permissions and no side effects. Its manifest explicitly forbids
discovery, repair, ranking, registration, approval, authorization, persistence,
dispatch, scheduling, execution, spawning, network use, and filesystem writes.

### 6. ResonantOS proposal owner — the product translator

If and only if the disposition is a verified candidate, ResonantOS maps the
candidate route ID through its own route table and may build a
`StrategyProposal`. This is where product-owned launch fields are added. The
generic resolver never owns those fields.

### 7. Human confirmation — the decision gate

A person confirms the exact candidate route. If the confirmed route, Dispatch,
group, or seat differs from the existing workflow binding, the adapter stops.

### 8. Existing host runtime — the only execution path

The existing runtime retains authorization, workflow binding, launch,
at-most-once run registration, child management, artifacts, lifecycle,
security, and effect receipts. The router does not create a second execution
system beside it.

### 9. The private CAV2 lineage edge — the reference keeper

The private candidate mapper can preserve two immutable references:

- the intent-route request artifact and its digest;
- the intent-route disposition artifact and its digest.

This lets the reasoning-engine entry seam remember exactly which routing
artifacts were involved without copying them into a new authority identity.
The mapper rejects ACI command IDs, compatibility claims, journal spans, effect
identities, namespace swaps, embedded schemes, and path-normalization tricks.

It does not yet prove integrated ACI conformance or advance the semantic
evaluator itself. It advances only the safe lineage seam entering that future
work.

## The complete runtime flow

```text
User intent
    |
    v
Augmentor captures the conversation
    |
    v
ResonantOS creates a closed request + digest-bound catalog
    |
    v
Authenticated host adapter checks the resolver package
    |
    v
Public Arcanum resolver returns one disposition
    |
    +--> ambiguous --> ask the exact clarification --> new request
    |
    +--> no-match  --> stop visibly
    |
    +--> invalid   --> show stable failure and stop
    |
    +--> candidate --> ResonantOS builds StrategyProposal
                           |
                           v
                     human confirmation
                           |
                           v
                  existing Dispatch/group/seat
                           |
                           v
                   existing host execution
```

The CAV2 lineage edge sits beside this flow. It records digest-bound references
to the request and disposition; it does not sit in the authorization or
execution path.

## A concrete example

Suppose the user says:

> “Research whether the new adapter preserves our authority boundaries.”

1. Augmentor captures the sentence and any declared context.
2. ResonantOS normalizes it into a request with discriminators such as
   `work_kind = research`.
3. ResonantOS projects a catalog that may include routes such as `research`,
   `design`, and `implementation`.
4. The host adapter authenticates the resolver and sends the exact request and
   catalog.
5. The resolver returns `candidate: research` if it is the unique eligible
   route.
6. ResonantOS can now build a `StrategyProposal` for the research route.
7. The user confirms or declines it.
8. Only after confirmation can the existing runtime bind and launch the work.

If `work_kind` were unresolved and both research and design remained possible,
the resolver would return `ambiguous` with a clarification question. It would
not guess based on conversational tone.

## What happens when something goes wrong?

The system prefers a visible stop over a clever recovery:

| Problem | Result |
| --- | --- |
| malformed request JSON | reject before trusted routing |
| request/catalog digest mismatch | reject |
| resolver executable or package changed | reject before launch |
| timeout | stop with a typed adapter error |
| extra stdout document or any stderr | reject |
| stale response from another request | reject |
| candidate has no human confirmation | stop before runtime binding |
| confirmation conflicts with workflow seat | reject |
| downstream authorization fails | no host spawn |
| host execution fails | preserve the failure; do not fabricate success |
| effect receipt is missing | do not claim the effect happened |

There is intentionally no semantic fallback that quietly chooses another route.

## What is working now?

The current evidence supports these local candidate claims:

- the public package's contract and boundary scan pass;
- its Node test suite passes 23 cases;
- its browser witness passes 6 of 6 deterministic cases in the recorded
  Chromium binary, with no console errors or external requests;
- the orchestrator adapter passes the frozen 27-case acceptance matrix,
  18 focused tests, and the 111-test runtime suite;
- the real public Node package was invoked through the adapter and returned the
  expected `route.special` candidate with `authority_effect: none`;
- the CAV2 lineage mapper passes its positive and adversarial tests;
- the ResonantOS consumption design preserves existing ownership and passes its
  documentation checks.

## What is not working as an integrated product yet?

These are important limits, not footnotes:

- the public source is not a released production package;
- the orchestrator policy is disabled and the add-on is not installed there;
- the ResonantOS worktree contains a validated integration plan, not product
  runtime changes;
- the private CAV2 mapper is candidate-local and does not prove integrated ACI
  conformance, artifact availability, or owner-receipt verification;
- none of the candidate branches has been committed, pushed, merged, deployed,
  or released.

## How installation fits in

Installation is separate from routing. The public Arcanum directory is the
canonical source. A generator/installer can project it into a host-native
package for Codex or Claude. The host then pins the generated entrypoint and
closure before enabling its adapter.

Installing files does not authorize a route. Enabling the adapter does not
approve work. A candidate still requires the same product proposal, human
confirmation, and existing runtime binding.

## The ownership rule to remember

Each component owns one kind of decision:

- **Augmentor:** what the user sees and says;
- **ResonantOS:** how product intent and proposals are represented;
- **Arcanum resolver:** which finite routes are eligible under the supplied
  facts;
- **human:** whether the proposed route should continue;
- **existing runtime:** whether and how work is authorized, bound, executed,
  persisted, and evidenced;
- **CAV2 candidate edge:** which immutable routing references are preserved for
  future reasoning lineage.

Keeping those owners separate is what makes the add-on composable with Codex,
Claude, ResonantOS, the cyberalchemy orchestrator, or another agentic runtime.

## The one-sentence retell

> The system turns intent into a deterministic, zero-authority route
> suggestion; Augmentor explains it, a human confirms it, and the existing
> runtime remains the only owner that can execute it.

## Evidence used for this guide

- Public add-on: `/home/vrondelli/projects/arcanum-intent-route-resolver/arcana/intent-route-resolver/`
- Orchestrator adapter receipt:
  `/home/vrondelli/projects/cyberalchemy-orchestrator-intent-route-adapter/docs/features/agent-provenance-telemetry/integration/stage-f/intent-route-adapter-execution-receipt.md`
- ResonantOS ownership contract:
  `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha-arcanum-addon-plan/development/arcanum-addon/ROUTER-CONSUMPTION.md`
- Private CAV2 lineage package:
  `/home/vrondelli/projects/domainspec-core-intent-route-cav2-edge/cyberAlchemy-v2/implementation/agent-reasoning-engine/packages/aci-binding-contract/`
- Browser receipt:
  `/home/vrondelli/projects/domainspec-core/.arcanum/invoke/refresh/iro-full-stream-20260802T021738Z-swu005/generated-browser-acceptance.json`
