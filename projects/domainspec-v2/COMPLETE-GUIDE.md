# DomainSpec v2 User Guide (Pre-release)

A game team begins with a simple idea: a player with the right key can unlock a door.
The idea sounds complete until the team asks what counts as the right key, what allows
the unlock, what changes, and what gets recorded.

## What is DomainSpec?

Different people may answer those questions differently. DomainSpec calls the part of
the game they are describing—the player, key, door, and rules around unlocking—the
**domain**. It gives the team a shared way to name its parts, record the roles they
play, explain how they relate, and state the rules the implementation must respect.

From that description, the team can make implementation **obligations** explicit,
derive test material from supported declarations, connect results to code evidence,
and state precisely what each result proves.

**DomainSpec is the system that supports this process. A DomainSpec specification is
the description the team creates.** DomainSpec is not the game or its application
framework, and it does not decide whether the feature is correct.

```text
shared specification
  -> obligations
  -> derived test material
  -> code evidence
  -> bounded proof
```

**Proof has a precise limit here.** It says what named inputs, checks, and results
support. It does not prove the whole game, approve the implementation, or authorize a
release.

**Today these stages are not one finished path.** The selected JSON authoring route
and the current test-derivation route remain separate, and architecture enforcement is
still candidate and partial.

> ## DomainSpec works like grammar for a system description
>
> A language is easier to share when it has known words, roles, and sentence patterns.
> DomainSpec does a similar job for a system description.
>
> - **Concepts are the vocabulary:** The named parts of the feature.
> - **Meta-types are the roles:** What job each named part performs in the description.
> - **Relationships are the verbs:** How two parts connect, including direction.
> - **The graph is the sentence map:** It shows who connects to what, and in which
>   direction.
>
> **Where the analogy stops:** A grammar checker can find a malformed sentence, but it
> cannot prove the sentence is true. In the same way, DomainSpec can reject some
> malformed descriptions; it cannot by itself prove the business meaning or the
> running software.
>
> DomainSpec helps a team make feature decisions explicit and carry them toward checks
> and evidence. It does not build the feature or decide whether the feature is correct.

That is the feature we will follow. The request below captures the team's starting
point. From there, we'll make each decision with them and see how DomainSpec gives
every part of the mechanic a clear place.

> **New feature · Key & Door**
>
> ### Unlock a door with a key
>
> As a player, I want to unlock a locked door when I have the right key.
>
> - **Player need:** Open a locked door.
> - **Condition:** The player has the right key.
> - **Expected result:** The door is unlocked and the successful action is recorded.
>
> The request tells us what the player needs. It does not yet tell the team how to
> describe every part or how those parts connect.

## A player, a key, and a door

A player with the right key should unlock a door. Everyone understands that sentence
until the team must agree on four details:

1. Which thing keeps its identity?
2. Which thing decides yes or no?
3. Which action changes the system?
4. What records that the change happened?

The **Key and Door** feature has four named parts:

- `Player`: the person in the game who tries to open the door.
- `HasKeyRule`: the yes-or-no question asked before unlocking.
- `UnlockDoor`: the action the player wants to perform.
- `DoorUnlocked`: the fact recorded after a successful unlock.

Now decide what each part is and how the four parts connect. Those choices turn the
familiar sentence into a description the team can check together.

DomainSpec gives a team a shared way to name those parts, connect them, and check
whether the description follows selected structural rules. The team still decides
whether the description means the right thing. A structural check does not prove that
the running game behaves correctly.

## How the current source is organized

In the selected current source direction, people edit JSON:

```text
project.json -> feature.json -> nodes/*.json
             -> generated graph + source links + human-readable view + build record
```

The generated files are read-only views of that source. The older Markdown engine is
a separate legacy path. A planned direct JSON-to-test bridge does not exist today.
Those details matter when you work with the repository, but they are not prerequisites
for understanding the Key-and-Door story.

## Help the team define Key & Door

The request sounds complete, but the team still has to settle six decisions: what
belongs in the mechanic, how the player is identified, what the key requirement
controls, what success changes and records, what a check can support, and how a later
change should be handled.

In the interactive HTML, your choices change only the page. They do not edit source
files or run repository checks. Today, people carry out the work through files and
commands in a prepared private checkout.

### 1. Choose what the team is deciding

The request includes a player, a key, a locked door, and a successful unlock. The game
also contains combat, exploration, animation, inventory, and quests.

**What should the team settle together before anyone implements the mechanic?**

The entire level would include several different behaviors. The door's appearance and
sound would omit the mechanic itself. The team therefore keeps **who acts, what permits
the action, what changes, and what records success** in this conversation.

In this guide, that decision is called the **feature boundary**. It contains one unlock
from actor and permission to change and recorded result. “Feature boundary” is guide
language, not an official DomainSpec meta-type.

<details>
<summary>See the current feature source</summary>

The current fixture already groups four node files under one Key-and-Door feature.
Choosing that boundary through the interactive screen is a teaching simulation, not
an implemented authoring tool.

</details>

### 2. Keep track of the player

The player picks up a key, moves to another room, loses health, and reloads the game.
Those details can change while the game still recognizes the same player. A room or
carried key cannot provide that continuity because both can change. The value that
continues identifying the player is the unique `player_id`.

**Which value should continue identifying that player?**

DomainSpec calls `Player` an **Entity**: a concept whose identity continues while its
other information can change. A Rule decides, an Operation changes state, and an Event
records what happened. **Meta-type** is DomainSpec’s name for one of these roles.

<details>
<summary>See the Player declaration</summary>

The current fixture declares `Player` as `Entity` and marks `player_id` as its identity
field. This is one checked example under the experimental profile, not a rule for every
possible game model.

</details>

### 3. Place the key decision

Before a locked door can open, the game needs a yes-or-no answer about whether the
player has the required key. That answer does not determine whether the player remains
the same person, and it cannot be controlled by a record that exists only after
success. It controls whether the unlock attempt may proceed.

**Where should that decision sit in the mechanic?**

DomainSpec calls `HasKeyRule` a **Rule**. The source gives it a boolean result and uses
a directed **relationship** to say what the decision controls:

```text
HasKeyRule --enforces--> UnlockDoor
Player ------performs--> UnlockDoor
UnlockDoor ---produces--> DoorUnlocked
```

The first two relationships settle the permission decision: `HasKeyRule` enforces the
action, while `Player` performs it. Reversing an arrow changes the statement.

<details>
<summary>See the connection declarations</summary>

Each outgoing connection lives in its source node file. The current experimental
profile admits these exact endpoint roles and relationship directions; it is not a
catalogue of every future DomainSpec relationship.

</details>

### 4. Describe a successful unlock

The key decision permits the attempt. Immediately before success, the door is locked;
immediately afterward, it is unlocked, and the game records that the unlock happened.
Permission without a changed door would stop too early. A success record while the door
remains locked would make the record disagree with the described outcome.

**Which account matches the team’s mechanic?**

DomainSpec calls `UnlockDoor` an **Operation** and `DoorUnlocked` an **Event**. The
Operation performs the change and declares `state_change: yes`. The Event records the
completed result and declares `temporal: past`.

```text
UnlockDoor --produces--> DoorUnlocked
```

<details>
<summary>See the Operation and Event declarations</summary>

The current formation schemas and fixture support this description. They can reject a
malformed declaration, but the selected JSON check does not run the game to observe the
state change.

</details>

### 5. Read the result

Before the check, the team has selected JSON source. Afterward, that exact source and
its generated results have been evaluated against the selected profile and structural
rules. The new fact is: **the exact description follows the structural rules that were
checked**. No game execution or release decision occurred, so neither running behavior
nor release approval follows from this result.

**Which fact follows from that result?**

In this guide, the **evidence boundary** is the line between what this exact result
supports and what still needs different evidence or authority. The generated map shows
normalized concepts and connections. The source manifest links them to source files and
digests. The build record names the source and generated results used in that build.

### 6. Change the decision

The existing source and generated results belong to the earlier decision: the player
needs the required key. The team now decides that a master key should work as well. The
accountable sequence is: **change project-owned source → regenerate the results → review
the new result**. Editing generated `SPEC.md` would separate the view from its source,
and the current workflow cannot discover the new requirement automatically.

**Which sequence keeps the changed decision connected to its result?**

In this guide, a **revision-bound result** speaks only about the exact source revision
and check that produced it.

Today, people change JSON source, rerun repository commands, and compare files or build
records. A proposed difference view would make the changed revision visible while
preserving the earlier result. That interface is not implemented, and people still
decide whether the new meaning is right.

### The loop closes, then starts again

```text
Scope -> Identity -> Permission -> Outcome -> Evidence -> Revision
  ^                                                       |
  +-------------------------------------------------------+
```

A later change can reopen the boundary or raise a new question. This is a
user-initiated loop, not a continuous service that exists today.

The same feature can now be viewed from four perspectives:

- **Story:** what the team means.
- **DomainSpec model:** the roles and directed connections.
- **Source:** the files people edit.
- **Evidence:** what the exact check supports and where its conclusion stops.

### What exists today and what is proposed

- **Current:** a prepared private checkout, independent JSON node files, one
  experimental profile, internal compiler and contract tests, generated read-only
  views, source links, and a build record.
- **Proposed experience:** supported setup, guided questions, local explanations, a
  unified review package, revision history, and a human-owned difference inbox.
- **Not promised:** the proposed experience is neither implemented capability nor an
  approved roadmap, release date, or production commitment.

This guide is a repository-local, pre-release documentation candidate. There is no
stable external installation path, public package, or production authorization. It
cannot change a definition, approve a code form or release, or change official project
status (`authority_effect: none`). When this guide and a responsible source disagree,
the responsible source wins. Guide revision: 2026-08-16; metrics snapshot: 2026-08-12.

## The consumer source package and generated views

The owner-selected consumer default is a machine-readable JSON package. A root project
record points to feature records, and each feature record points to independent concept
nodes. The current registered profile is still experimental; selection as the default
source direction is not release admission.

### Before you begin: what works today

- This is a private, repository-local workflow. Running its internal tools requires a
  maintainer-prepared checkout.
- The only registered consumer profile is experimental. It is not admitted for
  release.
- No stable external command exists yet to initialize or build a consumer project.
- `project.json` binds exact profile and registry digests. Use values supplied by the
  owned project or tooling; do not guess them or copy them from an older result.

```text
project.json                                      # project-owned source
specs/key-and-door/feature.json                   # project-owned source
specs/key-and-door/nodes/player.json              # Entity source
specs/key-and-door/nodes/has-key-rule.json        # Rule source + outgoing edge
specs/key-and-door/nodes/unlock-door.json         # Operation source + outgoing edge
specs/key-and-door/nodes/door-unlocked.json       # Event source
.domainspec/generated/graph.json                  # generated read model
.domainspec/generated/source-manifest.json        # generated provenance
.domainspec/generated/SPEC.md                     # generated human view
.domainspec/generated/markdown-view.json          # generated view record
.domainspec/generated/build-receipt.json          # generated evidence
```

The source records have different jobs:

| Record | What it owns |
| --- | --- |
| `project.json` | Project ID, selected profile and registry digests, feature paths, and generated-output root. The digests bind exact registry bytes; do not guess or copy stale values. |
| `specs/<feature>/feature.json` | Feature ID, source layout, and the list of node source paths. |
| `nodes/*.json` | One concept's stable ID, feature, kind, plain-language intent, required body, and outgoing connections. |
| `.domainspec/generated/*` | Read-only graph, source map, human view, and build evidence. Regenerate these; never repair them by hand. |

The current profile, `feature-with-independent-node-files`, supports only:

- Entity, Event, Operation, and Rule;
- `enforces`, `performs`, and `produces`; and
- one source JSON file per node, with connections owned by the source node.

The feature record for the checked example makes the node set explicit:

```json
{
  "schema_version": "minted-feature/v1",
  "feature_id": "key-and-door",
  "source_layout": "per-node-connections",
  "node_sources": [
    "nodes/door-unlocked.json",
    "nodes/has-key-rule.json",
    "nodes/player.json",
    "nodes/unlock-door.json"
  ]
}
```

The file containing the connection supplies its `from` endpoint when DomainSpec builds
the consistent map. Every target must resolve to a node in the compiled source set, and
source paths must remain inside the project. The compiler generates the system map,
source list, Markdown view, and build record (receipt).

Study the complete, internally checked four-concept example:

- [Project record](impl/test-derivation-engine/__fixtures__/minted-project/contract/positive/key-and-door/project.json)
- [Feature record](impl/test-derivation-engine/__fixtures__/minted-project/contract/positive/key-and-door/specs/key-and-door/feature.json)
- [Player Entity](impl/test-derivation-engine/__fixtures__/minted-project/contract/positive/key-and-door/specs/key-and-door/nodes/player.json)
- [HasKeyRule Rule](impl/test-derivation-engine/__fixtures__/minted-project/contract/positive/key-and-door/specs/key-and-door/nodes/has-key-rule.json)
- [UnlockDoor Operation](impl/test-derivation-engine/__fixtures__/minted-project/contract/positive/key-and-door/specs/key-and-door/nodes/unlock-door.json)
- [DoorUnlocked Event](impl/test-derivation-engine/__fixtures__/minted-project/contract/positive/key-and-door/specs/key-and-door/nodes/door-unlocked.json)
- [Generated `SPEC.md`](impl/test-derivation-engine/__fixtures__/minted-project/contract/positive/key-and-door/expected/SPEC.md)

The source contract and generated-output roles are indexed in
[impl/spec/minted-project/INDEX.md](impl/spec/minted-project/INDEX.md). There is no
stable public CLI for this workflow, and the profile has not been admitted for release.

## What the two repository paths generate

Two implemented paths coexist in the repository, but they do not yet join.

### Selected JSON source path

The minted-project compiler resolves the project, feature, and node sources and then
builds deterministic read-only results:

```text
project.json -> feature.json -> nodes/*.json
             -> graph.json + source-manifest.json
             -> generated SPEC.md + markdown-view.json
             -> build-receipt.json
```

Internal tests exercise schema validation, profile and registry bindings, connection
endpoints, path containment, determinism, provenance, and stale generated bytes. This
is implemented repository machinery, not yet a supported external command or a released
product workflow.

### Legacy Markdown derivation path

The older check generator follows the same steps every time for the same inputs:

```text
parse docs -> normalized graph G -> pure derivation rules
           -> stable IDs for each generated check
           -> test specification and runnable structural tests
```

It accepts:

- legacy aspect documents such as `states.md` and `operations.md`; or
- a normalized v2 `SPEC.md` when aspect documents are absent, as explicit legacy input.

It generates focused checks—officially called **obligations**—for declared concepts,
fields, attributes, and relationships. It does not work out business behavior or equations
from prose. This path uses no LLM and no network, so the same inputs produce the same
result.

Markdown remains useful here and as generated documentation. The planned
`machine-v1` route must not read Markdown or use it as a fallback. Its route from the
minted JSON artifacts into machine-view test generation is designed but not
implemented; the legacy engine must not be described as silently filling that gap.

For maintainers working in a prepared checkout, these existing commands exercise the
legacy validators and repository test surface. They are not a user CLI for the selected
JSON package:

```bash
npm --prefix projects/domainspec-v2/impl run validate:content
npm --prefix projects/domainspec-v2/impl run validate:rels
npm --prefix projects/domainspec-v2/impl run validate
```

To create a legacy-engine result record (receipt) from a supported feature directory:

```bash
cd projects/domainspec-v2/impl/test-derivation-engine
pnpm exec tsx src/cli.ts receipt <feature-directory>
```

The result record lists which declarations and relationships were processed, skipped,
or rejected, plus the exact source references used. It proves only that those inputs
were structurally accounted for; it does not prove that the business meaning is
correct and it does not generate an application. See the
[engine README](impl/test-derivation-engine/src/README.md).

## Walk one complete checked feature

Key and Door is the smallest complete example of the selected source layout. This is a
reading walkthrough, not a promise that a supported onboarding command exists. It lets
you see the whole current boundary before studying the wider type catalogue.

### Start at the project boundary

The package has six editable source files:

| File | Question it answers |
| --- | --- |
| `project.json` | Which project, profile, registry versions, features, and generated directory belong to this build? |
| `specs/key-and-door/feature.json` | Which node files make up the Key and Door feature? |
| `nodes/player.json` | Which identity-bearing Entity can act? |
| `nodes/has-key-rule.json` | Which boolean Rule gates the action? |
| `nodes/unlock-door.json` | Which state-changing Operation happens? |
| `nodes/door-unlocked.json` | Which past-tense Event records the result? |

The feature record lists all four nodes. The node files carry the meaning. DomainSpec
does not recover a missing node from generated Markdown or silently invent one.

### Read the four nodes as one story

```text
Player ---------[performs]--------> UnlockDoor ---------[produces]--------> DoorUnlocked
                                         ^
                                         |
                                     [enforces]
                                         |
                                     HasKeyRule
```

Each node uses one of the four kinds supported by the current profile:

| Node | Kind | Required body signal | Contribution to the story |
| --- | --- | --- | --- |
| `Player` | Entity | At least one field has `identity: true`. | Names the identity-bearing actor. |
| `HasKeyRule` | Rule | `formal_return_type` is `boolean`. | Decides whether unlocking is allowed. |
| `UnlockDoor` | Operation | `state_change` is `yes`. | Performs the state-changing action. |
| `DoorUnlocked` | Event | `temporal` is `past`. | Records that the action happened. |

The node containing a connection owns its outgoing edge. `player.json` owns
`performs`, `has-key-rule.json` owns `enforces`, and `unlock-door.json` owns
`produces`. During normalization, the containing node supplies the `from` endpoint;
the connection record names the `to` endpoint.

### Know where to make a change

| You need to change… | Edit… | Do not edit… |
| --- | --- | --- |
| Project profile, registry bindings, feature list, or generated root | `project.json` | A build receipt copied from another revision. |
| Which nodes belong to the feature | `feature.json` | The generated graph's node list. |
| A concept's name, kind, meaning, required body, or outgoing connections | That concept's `nodes/*.json` file | Generated `SPEC.md` or `graph.json`. |
| A generated result that is stale | The responsible source, then regenerate all bound outputs | The generated result in place. |

### Read the five generated results

| Generated result | Review question it answers |
| --- | --- |
| `graph.json` | Which normalized nodes and directed connections did DomainSpec build? |
| `source-manifest.json` | Which exact source file and digest produced each graph record? |
| `SPEC.md` | What does the normalized graph look like in a human-readable view? |
| `markdown-view.json` | Which graph digest, Markdown digest, and generator version bind that view? |
| `build-receipt.json` | Which profile, registries, source set, generated artifacts, generator, and build result were checked together? |

### Review the result

For the checked fixture, confirm all of the following:

- the project points to one feature and that feature lists all four node files;
- the graph contains the four expected nodes and three expected connections;
- every graph node and edge traces back to its owning source file in the source
  manifest;
- the generated Markdown says to edit machine sources and rebuild;
- the Markdown-view record binds the exact graph and Markdown bytes;
- the build receipt says `status: pass` and binds the exact profile, registries,
  source set, outputs, and generator; and
- the conclusion stops at structural formation, normalization, provenance, and
  repeatable generation for this exact fixture.

`status: pass` does not establish that a player really owns a key, that running code
unlocks a door, that the domain policy is correct, or that the profile is released.

### If the current profile cannot express your concept

Do not invent a new `kind`, improvise a body for one of the other nine active backend
types, or use one of the other language relationships as though the profile supported
it. Keep the intended distinction in project notes, bring a concrete example that the
current profile cannot represent, state which validation or generated result should
change, and route the proposal to the responsible definitions or profile owner. The
full language catalogue is a reference; it is not hidden source-format support.

### Find the layer that failed

| Failure category | First place to inspect | Safe response |
| --- | --- | --- |
| Unsupported profile | `project.json` and the supported-profile registry | Select only an admitted profile binding or ask the profile owner; do not bypass the check. |
| Kind outside the profile | The node's `kind` | Use one of the current four kinds only when it preserves the meaning; otherwise raise the missing profile capability. |
| Invalid body shape | The node's `body` and its formation schema | Correct the source body. Do not ask generated Markdown to supply missing semantics. |
| Unsupported or inactive relationship | The source node's outgoing connection and the relationship registry | Choose a supported connection only when it expresses the intended relation; otherwise raise a profile proposal. |
| Missing endpoint | The connection target and `feature.json` node list | Add or correct the owned source node and feature membership. |
| Path escapes the project | `project.json`, `feature.json`, or the offending relative path | Keep every source and generated path inside the consumer root. |
| Stale generated bytes | Source manifest, view binding, or receipt | Regenerate the complete bound output set from source; never patch one generated file. |

The authority contract requires unsupported profile, unsupported kind, invalid shape,
and inactive relationship failures to remain distinguishable. Current tools may use
different exact wording, so this table identifies the repair boundary rather than
promising a diagnostic message.

## Turn one team decision into a concept

The team has decided that an unlock attempt is allowed only when the player holds the
required key. That decision now needs a stable place in the project so everyone can
name it, connect it to the unlock action, and review the same meaning later.

A **concept** is one named part of the system description. Here, `HasKeyRule` is the
team's name for the decision that allows or blocks `UnlockDoor`.

### Answer six questions

The questions begin with the team's meaning. Their answers become the fields of one
source record.

| Question | The team's answer | Where it goes |
| --- | --- | --- |
| What does this decision mean? | Allow unlocking only when the player holds the required key. | `intent` |
| What job does it perform? | It returns a yes-or-no decision that allows or blocks an action. | `kind: Rule` |
| Which feature owns it? | Key & Door. | `feature_id: key-and-door` |
| What is its stable name? | `HasKeyRule` inside that feature. | `node_id: key-and-door.HasKeyRule` |
| What must every Rule state? | Its formal result is boolean: yes or no. | `body.formal_return_type` |
| What does it govern? | The `UnlockDoor` action. | `enforces -> key-and-door.UnlockDoor` |

### Assemble the answers into one source node

The checked Key & Door fixture stores those answers in
`nodes/has-key-rule.json`:

```json
{
  "schema_version": "minted-node/v1",
  "node_id": "key-and-door.HasKeyRule",
  "feature_id": "key-and-door",
  "kind": "Rule",
  "intent": "Allow the unlock operation only when the player holds the key.",
  "body": {
    "formal_return_type": "boolean"
  },
  "connections": [
    {
      "edge_id": "key-and-door.edge.has-key-rule-enforces-unlock-door",
      "type": "enforces",
      "to": "key-and-door.UnlockDoor"
    }
  ]
}
```

### What the current check can establish

Under the selected experimental profile, a check can confirm that this record has the
required Rule body and that a Rule may `enforce` an Operation. It cannot decide whether
the rule expresses the right game design, inspect the game's code, or prove that the
player is blocked at runtime.

This record is not a complete project. It belongs beside `project.json`, the Key & Door
feature record, and every node it references—including `UnlockDoor`. See
[The consumer source package and generated views](#the-consumer-source-package-and-generated-views)
for the complete package.

> **The language is larger than this source profile.** The current experimental
> profile accepts source nodes for Entity, Event, Operation, and Rule. DomainSpec has
> other active types, but this profile does not define their JSON bodies. Choose from
> the type catalogue; if no active type preserves the distinction you need, follow the
> separate new-meta-type proposal path instead of inventing a body.

There is no supported external authoring command yet. Today this example lives in
project-owned JSON and is exercised by repository-internal compiler and contract tests.
Generated views are read-only: change the source, rebuild the results, and review them
again. This guide does not turn those internal APIs into a promised user command.

## The 25 kinds of concepts tracked by DomainSpec v2

DomainSpec calls these categories **meta-types**. The DS-D1 list keeps 25 IDs, but only
24 are non-retired labels. `DS-D1.10 Saga` is a retired historical ID and is not part
of the usable or proposed set.

### Active backend types

| Category | ID | Meta-type | Core distinction |
| --- | --- | --- | --- |
| Structural | DS-D1.1 | Entity | Keeps a stable identity as it changes. |
| Structural | DS-D1.2 | Value Object | Equality by the complete value; no designated identity. |
| Structural | DS-D1.3 | Enum | Fixed list of named values. |
| Behavioral | DS-D1.4 | Operation | A business action that changes state. |
| Behavioral | DS-D1.5 | Query | Read-only retrieval. |
| Behavioral | DS-D1.6 | Calculation | Calculates a value without side effects. |
| Behavioral | DS-D1.7 | Rule | True/false block-or-allow decision. |
| Behavioral | DS-D1.8 | Policy | Selects a strategy or branch. |
| Behavioral | DS-D1.9 | Workflow | Coordinates several operations in order. |
| Connective | DS-D1.11 | Interface | Exposes behavior that internal or external callers can use. |
| Connective | DS-D1.12 | Event | Reports something that already happened. |
| Connective | DS-D1.13 | Mapping | Converts one data shape into another. |
| Lifecycle | DS-D1.14 | State Machine | States plus allowed transitions. |

### Proposed and postponed UI types

| ID | Meta-type | Status | Plain description |
| --- | --- | --- | --- |
| DS-D1.15 | Page | candidate | A screen with its own route and main content. |
| DS-D1.16 | Layout | candidate | A reusable page shell with named slots. |
| DS-D1.17 | Component | candidate | A reusable visual unit with no route of its own. |
| DS-D1.18 | View Model | candidate | Data shaped for display without owning domain decisions. |
| DS-D1.19 | Hook | candidate | Reusable reactive behavior and effects. |
| DS-D1.20 | Form | candidate | Fields, validation, errors, and submission as one unit. |
| DS-D1.21 | Action | candidate | One user intention, its trigger, and its outcomes. |
| DS-D1.22 | Guard | candidate | A UI check that mirrors an authoritative Rule. |
| DS-D1.23 | Binding | candidate | A lasting record of a UI/backend interaction and cache behavior. |
| DS-D1.24 | Adapter | deferred | May be the same concept as Mapping. |
| DS-D1.25 | State Indicator | deferred | May combine two ideas: domain-state display and async request state. |

### Retired type

| ID | Meta-type | Rule |
| --- | --- | --- |
| DS-D1.10 | Saga | Replaced by Workflow. Keep the ID for history; never write a new Saga or reuse the number. |

The human definition cards are in
[definitions/meta-types/meta-types.md](definitions/meta-types/meta-types.md). The
machine index is
[definitions/meta-types/meta-types.yml](definitions/meta-types/meta-types.yml). For
active backend types, the referenced `.schema.yml` files are the official required
shapes used by the checker.

## How each active backend type is defined

Each type requires specific information. DomainSpec calls this its **formation
criterion**. Passing the criterion proves that the declaration has the required
shape; it does not prove that its prose is true or that the described behavior works.

Only four active types currently have JSON body schemas in the selected
consumer profile:

| JSON node kind | Required `body` shape |
| --- | --- |
| **Entity** | `fields` is non-empty; every field has `name`, `type`, and boolean `identity`; at least one field has `identity: true`. |
| **Event** | `temporal` is exactly `past`. |
| **Operation** | `state_change` is exactly `yes`. |
| **Rule** | `formal_return_type` is exactly `boolean`. |

The full catalogue below explains all active language types. For the other nine, the
required-shape links describe the language and the older checker, not a supported JSON
authoring form. Do not improvise a new node `body` from those links.

### Structural types

| Meta-type | Use it when | Formation rule | Current JSON source | Use another type when |
| --- | --- | --- | --- | --- |
| **Entity** | Each item must keep the same ID while its other fields change. | Typed fields with at least one identity field. | **Included in the profile.** Use `body.fields[].name`, `type`, and boolean `identity`. | With no identity and equality by fields, use Value Object. |
| **Value Object** | All fields together determine equality, and there is no separate ID. | Typed fields, no identity, and an explicit equality rule. | **Not in the profile.** Do not invent a JSON body. | If equal-looking items still need distinct IDs, use Entity. |
| **Enum** | The concept is a fixed list of allowed names. | A non-empty fixed value set. | **Not in the profile.** Do not invent a JSON body. | If values carry fields, use Entity/Value Object; if they move through transitions, use State Machine. |

Official required-shape files:

- [Entity](impl/spec/meta-types/structural/entity.schema.yml)
- [Value Object](impl/spec/meta-types/structural/value-object.schema.yml)
- [Enum](impl/spec/meta-types/structural/enum.schema.yml)

### Behavioral types

| Meta-type | Use it when | Formation rule | Current JSON source | Use another type when |
| --- | --- | --- | --- | --- |
| **Operation** | Running the behavior changes domain state. | `state_change = yes` | **Included in the profile.** Use `body.state_change`. | If it only reads, use Query. |
| **Query** | The behavior retrieves a view without changing state. | `state_change = no` | **Not in the profile.** Do not invent a JSON body. | If it mutates, use Operation. |
| **Calculation** | A named function calculates a value without side effects. | `formal_return_type = value` | **Not in the profile.** Do not invent a JSON body. | If it returns block/allow, use Rule. |
| **Rule** | The result is a true/false block-or-allow decision. | `formal_return_type = boolean` | **Included in the profile.** Use `body.formal_return_type`. | If it selects a strategy, use Policy. |
| **Policy** | The result chooses a strategy or branch. | `formal_return_type = strategy` | **Not in the profile.** Do not invent a JSON body. | If it only blocks/allows, use Rule. |
| **Workflow** | One concept coordinates multiple ordered Operations. | `scope` is exactly `intra-feature` or `cross-feature` | **Not in the profile.** Do not invent a JSON body. | One state-changing action is an Operation; former Saga concepts are Workflow. |

Official required-shape files:

- [Operation](impl/spec/meta-types/behavioral/operation.schema.yml)
- [Query](impl/spec/meta-types/behavioral/query.schema.yml)
- [Calculation](impl/spec/meta-types/behavioral/calculation.schema.yml)
- [Rule](impl/spec/meta-types/behavioral/rule.schema.yml)
- [Policy](impl/spec/meta-types/behavioral/policy.schema.yml)
- [Workflow](impl/spec/meta-types/behavioral/workflow.schema.yml)

An Operation that creates a new Entity uses a `creates` connection:

```text
CreatePlayer --[creates]--> Player
```

In the full relationship model, DomainSpec fills `creation_targets` from outgoing
`creates` connections. Authors must not write that field separately. The rule allows
an Operation to create at most one kind of Entity in the same feature, and each Entity
type to have at most one creating Operation. This limit applies to concept types in
the design, not to the number of objects the running application may create. The
current independent-node profile does **not** support `creates` yet.

### Connective types

| Meta-type | Use it when | Formation rule | Current JSON source | Use another type when |
| --- | --- | --- | --- | --- |
| **Interface** | The concept exposes behavior that internal or external callers can use. | `interface_kind` is present; guidance uses `internal` or `external`. | **Not in the profile.** Do not invent a JSON body. | A field-by-field shape conversion is Mapping. |
| **Event** | The concept announces a fact that already happened. | `temporal = past` | **Included in the profile.** Use `body.temporal`. | A request to make something happen is an Operation or command. |
| **Mapping** | The concept converts fields from one data shape to another. | `direction` is present; guidance uses `inbound`, `outbound`, or `bidirectional`. | **Not in the profile.** Do not invent a JSON body. | The exposed boundary itself is Interface. |

Official required-shape files:

- [Interface](impl/spec/meta-types/connective/interface.schema.yml)
- [Event](impl/spec/meta-types/connective/event.schema.yml)
- [Mapping](impl/spec/meta-types/connective/mapping.schema.yml)

### Lifecycle type

| Meta-type | Use it when | Formation rule | Current JSON source | Use another type when |
| --- | --- | --- | --- | --- |
| **State Machine** | The concept defines how something may move from one state to another. | `has_transitions = yes` | **Not in the profile.** Do not invent a JSON body. | A flat list without transitions is Enum. |

Official required-shape file: [State Machine](impl/spec/meta-types/lifecycle/state-machine.schema.yml).

## The proposed shape of each UI type

The nine UI labels below are proposals, not active DomainSpec types. Their schemas are
marked `development-profile`, which means they are for experiments. They can help test
whether the proposed distinctions are useful, but they do not approve the types or
prove that they work across frameworks.

| Proposed type | Proposed required information | What keeps it different |
| --- | --- | --- |
| **Page** | Non-empty `route_path`, `access_context`, `primary_content`, `layout_ref`, and `unit_inventory`; `terminal = true`. | A Page owns a route and main content; a Component has no route of its own. |
| **Layout** | Non-empty `slots` and `shared_chrome`; `page_specific_content = false`; `wrap_target = Page`. | A Layout is a reusable page shell; a Page owns content for one destination. |
| **Component** | Typed inputs and outputs; `independent_route`, `domain_data_authority`, `validation_authority`, and `access_authority` are all `false`. | A Component is a reusable visual unit; Page, Form, and Guard own more specific jobs. |
| **View Model** | Typed fields, source references, display context and roles; `domain_authority = false`. | A View Model shapes data for one screen; a Value Object defines equality in the domain. |
| **Hook** | Typed inputs and returns plus declared reactive behavior, timing, and effects. | A Hook owns reusable reactive behavior; a Binding records a lasting endpoint and cache interaction. |
| **Form** | Typed fields plus validation, errors, submission action, target interface, and error mapping. | A Form groups fields, validation, errors, and submission. |
| **Action** | Intent, trigger, target kind, effect boundary, success outcome, and error outcome. | An Action defines one complete user intention and its outcomes, not just an event handler. |
| **Guard** | Protected screen, source Rule, conditions, fallback, scope, and `decision_authority = false`. | A Guard copies a backend Rule but does not make the real authorization decision. |
| **Binding** | Mode, target kind and reference, trigger, parameter/result mapping, cache key, and invalidation. | A Binding records a lasting UI/backend interaction; a simple endpoint link stays a connection. |

Experimental required-shape files:

- [Page](impl/spec/meta-types/ui/page.schema.yml)
- [Layout](impl/spec/meta-types/ui/layout.schema.yml)
- [Component](impl/spec/meta-types/ui/component.schema.yml)
- [View Model](impl/spec/meta-types/ui/view-model.schema.yml)
- [Hook](impl/spec/meta-types/ui/hook.schema.yml)
- [Form](impl/spec/meta-types/ui/form.schema.yml)
- [Action](impl/spec/meta-types/ui/action.schema.yml)
- [Guard](impl/spec/meta-types/ui/guard.schema.yml)
- [Binding](impl/spec/meta-types/ui/binding.schema.yml)

### Deferred UI distinctions

**Adapter** does not currently have its own approved shape rule. Current tests show
that Mapping already covers the same source shape, target shape, direction, and field
conversion. Use Mapping with UI-boundary details until a concrete example shows that
a separate Adapter type would change a check.

**State Indicator** also has no approved shape rule. One proposed meaning maps
every value from an Enum or State Machine to a visual representation; another branch
models asynchronous loading/error/empty request state. Those may be two different
concepts, so the proposal remains unresolved.

## A practical decision tree for choosing a meta-type

```text
Does the concept primarily describe data?
  |
  +-- Does it have stable identity? ----------------------> Entity
  +-- Is equality the complete field tuple? -------------> Value Object
  +-- Is it a closed list of named values? --------------> Enum
  +-- Does it own legal transitions between states? -----> State Machine

Does the concept primarily describe behavior?
  |
  +-- Does it change state? ------------------------------> Operation
  +-- Is it read-only retrieval? -------------------------> Query
  +-- Does it return a derived value? --------------------> Calculation
  +-- Does it return block/allow? ------------------------> Rule
  +-- Does it choose a strategy? -------------------------> Policy
  +-- Does it coordinate ordered Operations? ------------> Workflow

Does the concept primarily connect boundaries?
  |
  +-- Does it expose callable behavior? ------------------> Interface
  +-- Does it announce a past fact? ----------------------> Event
  +-- Does it transform one shape into another? ----------> Mapping
```

If none fits, do not invent a new label inside a feature. Bring a concrete example
that existing types handle incorrectly, show which validation or generated result
would change, and ask the definitions owner to review the proposal.

## The 31 allowed ways to connect concepts

A connection is allowed only when:

- DomainSpec recognizes the verb as an active DS-D8 relationship;
- the two concept types may be connected in that direction;
- the connection is allowed in that location—for example, inside one feature or
  across features;
- the number of source and target concepts stays within the rule; and
- authors are meant to write the connection rather than generate it automatically.

The official term **multiplicity** means how many source and target concepts a
connection may have.

> **Full language registry versus current JSON profile:** the tables below document
> all active DS-D8 connections. The selected independent-node profile currently
> supports only `Entity --[performs]--> Operation`,
> `Rule --[enforces]--> Operation`, and
> `Operation --[produces]--> Event`. Do not put another connection type in a current
> node source just because it appears in the full language registry.

### When does a connection deserve its own relationship type?

Give a connection its own type only when removing it would change validation, a
generated check, ownership, a workflow path, or an output file. If removing it only
changes a diagram label or adds convenient reverse navigation, keep it as metadata or
generate it automatically.

### Backend connections

| Allowed connection | Where allowed | How many | Meaning |
| --- | --- | --- | --- |
| `Entity --[performs]--> Operation` | same feature | many-to-many | An entity or actor initiates an operation. |
| `Operation --[produces]--> Event` | same feature | one-to-many | Successful completion causes an event. |
| `Operation --[produces-for]--> Entity` | cross feature | many-to-many | An Operation writes to or creates a view of an Entity in another feature. |
| `Operation --[creates]--> Entity` | same feature | partial one-to-one | An operation owns creation of one Entity type. |
| `Event --[triggers-cross]--> Operation` | cross feature | many-to-many | An event activates behavior in another feature. |
| `Rule --[enforces]--> Operation` | same or cross feature | many-to-many | A boolean Rule gates an Operation. |
| `Calculation --[calculates]--> Operation` | same feature | many-to-many | A Calculation supplies a derived value. |
| `Event --[transitions]--> State Machine` | same or cross feature | many-to-many | An Event advances a lifecycle. |
| `Interface --[exposes]--> Operation or Query` | same or cross feature | one-to-many | A boundary makes behavior callable. |
| `Workflow --[orchestrates]--> Operation[]` | same or cross feature | ordered one-to-many | A Workflow coordinates ordered Operations. |
| `Policy --[applies]--> Operation or Calculation` | same feature | many-to-many | A Policy selects behavior. |
| `Mapping --[maps]--> Entity or Interface` | same or cross feature | many-to-many | A Mapping transforms a boundary/entity shape. |
| `Entity --[contains]--> Value Object` | same feature | one-to-many | An Entity embeds a Value Object. |
| `Query, Calculation, or Operation --[queries]--> Entity` | same feature | many-to-many | Read-capable behavior reads Entity data. |
| `Entity --[emits]--> Event` | same feature | one-to-many | An Entity is the subject/source of an Event. |
| `Entity --[owns]--> Entity` | same or cross feature | one-to-many | The source has lifecycle/custody/write ownership. |
| `Entity --[belongs-to]--> Entity` | same or cross feature | many-to-one | The source is a member of or assigned to the target. |

### UI connections

These connection verbs are active, but the UI types at their ends remain proposed or
deferred. An active connection does not make its endpoint types active.

| Allowed connection | How many | Meaning |
| --- | --- | --- |
| `Page --[renders]--> Component[]` | one-to-many | A Page renders Components. |
| `Layout --[wraps]--> Page[]` | one-to-many | A Layout wraps Pages. |
| `Component --[composes]--> Component[]` | one-to-many | A Component includes children. |
| `Component --[consumes]--> Hook` | many-to-many | A Component consumes reactive behavior. |
| `Form --[submits]--> Action` | many-to-one | A Form delegates submission. |
| `Adapter --[shapes]--> View Model` | many-to-many | A deferred Adapter shapes display data. |
| `Guard --[protects]--> Page` | many-to-many | A Guard controls UI access behavior. |
| `Component --[displays]--> View Model` | many-to-many | A Component displays data prepared for the screen. |

### UI-to-backend connections

| Allowed connection | How many | Meaning |
| --- | --- | --- |
| `Binding --[fetches]--> Query` | many-to-one | A Binding retrieves data through a Query. |
| `Binding --[mutates]--> Operation` | many-to-one | A Binding invokes a state-changing Operation. |
| `State Indicator --[reflects]--> State Machine` | many-to-one | A deferred indicator reflects domain lifecycle state. |
| `View Model --[derives]--> Entity` | many-to-many | Display data derives from Entity fields. |
| `Form --[contracts]--> Interface` | many-to-one | A Form aligns with an Interface contract. |
| `Guard --[mirrors]--> Rule` | many-to-one | A client Guard mirrors a backend Rule. |

### Generated, postponed, and retired connections

- `owned-by` is generated reverse navigation for `owns`; never write it in source.
- `depends-on` remains postponed because no concrete example shows that it needs
  different validation.
- An Operation returning a Value Object remains a property of the relationship rather
  than a separate connection.
- Separating Event publisher and payload remains postponed for the same reason.
- `enforces-cross` is retired. Use `enforces`; the source and target feature locations
  already show whether the connection crosses features.

See the machine registry
[definitions/relationships/relationships.yml](definitions/relationships/relationships.yml)
and the human guide
[definitions/relationships/relationships.md](definitions/relationships/relationships.md).

## How to propose a new DomainSpec meta-type

Most projects should never need a new meta-type. A meta-type changes the vocabulary
available to every specification, so a new label begins as a question—not as an
official type.

- A **new concept** uses the language. `HasKeyRule` belongs to one project and uses the
  existing Rule meta-type.
- A **new meta-type** changes the language for many projects. It changes what counts as
  a well-formed declaration, where that declaration may connect, and what later checks
  can distinguish.

> **Try to disprove the proposal first.** If an active type plus its properties and
> relationships preserves the distinction, stop. A different framework word, class
> name, or diagram label is not enough. The proposal must change a check or another
> tracked result.

### Follow a real proposal: should Page be different from Component?

A product team keeps describing `InventoryPage` and `MapPage` as Components. It
proposes Page as a separate role because a Page owns a destination: a route, primary
content, layout, access context, and the units placed on it. A reusable Component does
not own a route.

That difference is promising, but it is still a candidate. The current Page evidence
has not yet been reproduced independently across route frameworks, so Page is not
active or promotion-ready.

### Author the candidate as a question the evidence can answer

1. **Show where the language fails.** Try the active types first. Then name the exact
   failure and compare the closest neighbour. For Page, the question is whether a
   routeless Component could wrongly satisfy the description of a terminal destination.
   Page owns the destination; Component does not.
2. **Make the difference testable.** Write the separating formation rule, place the
   candidate in one category, and propose its incoming and outgoing relationship roles.
   Test a valid Page, a deliberately invalid neighbour, and at least one real project
   example. Record the exact check or tracked result that changes.
3. **Submit evidence, not a verdict.** The human card, candidate schema, fixtures,
   automated tests, and known limitations form a review packet. They do not allocate an
   official ID or choose a permanent file home. The definitions owner decides maturity.
   Even activation does not add the type to every source profile or approve a code form,
   release, or production use.

### Keep four decisions separate

| Question | What a positive result means | What it still does not grant |
| --- | --- | --- |
| Is the idea a candidate? | There is a concrete distinction worth testing. | Permission to use it as active DomainSpec vocabulary. |
| Is the formation rule checkable? | Valid and invalid declarations can be distinguished structurally. | Proof that the type is necessary, meaningful, or implemented. |
| Is the meta-type active? | The definitions owner accepted the type under its evidence and challenge contracts. | Automatic support in every DomainSpec source profile. |
| Does a profile support authoring it? | That profile defines the source shape and admitted connections for the type. | Runtime behavior, implementation conformance, release approval, or production readiness. |

Current proposals show why this is a real gate. Adapter remains a deferred
merge-candidate because its tested structure still collapses into Mapping with extra
UI-boundary details. State Indicator remains deferred because domain-state
visualization and loading, error, or empty request state may be two different ideas.

The current contracts are recorded in the
[meta-type definition and challenge contract](definitions/DEFINITIONS.md#domainspec-v2-d6-meta-type),
[human definition cards](definitions/meta-types/meta-types.md),
[machine-readable registry](definitions/meta-types/meta-types.yml),
[formalization contract](development/meta-type-formalization/DEFINE.md), and
[candidate adjudication results](development/ui-meta-type-formalization/adjudication/verdicts.yml).
This is a repository-governed proposal path, not a supported end-user command. A
schema, fixture, experiment, relationship entry, or code mapping may support review;
none can approve itself.

## From a specification to checks—and from code back to evidence

The Key and Door description says that `HasKeyRule` gates `UnlockDoor`. The next
questions are different: what must eventually be checked, and what should the code
preserve?

### First: make the checklist

The **Test Derivation Engine** turns supported declarations into stable
**obligations**: small, named items that later tests or implementation evidence must
account for. In this guide, think of it as the **checklist maker**. It does not invent
missing behavior, generate the application, or decide whether the business meaning is
right.

The current engine reads legacy aspect documents or an explicit normalized `SPEC.md`.
It can render obligations into test material. Supported bindings and formal expressions
can become real assertions; unsupported behavior remains a visible gap rather than a
silent success.

The selected JSON source package used by this guide does not feed that general engine
path directly. A narrower JSON-to-node-logic projection now exists for explicitly
admitted logic-bearing nodes, but it is not the test bridge for the four-kind Key and
Door profile. The direct selected-JSON-to-obligations path remains planned and must use
verified machine views rather than treating generated Markdown as new source.

### Then: inspect the code shape

**Architecture type enforcement** compares selected expectations for a DomainSpec type
with facts gathered from exact code. The repository calls the wider program
**Architecture-Pattern Enforcement**.

A DomainSpec type can look different in TypeScript, Python, and Rust while keeping the
same meaning. Architecture enforcement separates what must remain true everywhere from
conventions that belong to one language or project. It reports matches, differences,
missing evidence, and unsupported cases. It does not approve the implementation.

The terms name different jobs:

- an **obligation** names something that must be accounted for;
- an **architecture mapping** proposes how a type may appear in code;
- a **profile** lists selected shared or language-specific expectations;
- a **provider** gathers facts from the exact **target**;
- a **finding** explains a match or difference; and
- a **receipt** records the inputs, results, and limits.

Examples:

- A Rule remains a true/false guard in every language, while its callable syntax may be
  an arrow function, a Python function definition, or a Rust function item.
- An Enum must preserve its owned list of values, but TypeScript, Python, and Rust need
  not use the same syntax.
- A Value Object must compare every owned field and keep its values unchanged, but hash
  bytes do not need to be equal across languages.

### From one description to a decision the evidence can support

```text
source description
  -> derived obligations
  -> expected code shape
  -> exact code target and observed facts
  -> findings and receipt
  -> owner decision
```

The current checks are grouped by the kind of meaning they preserve:

| Meaning preserved | Meta-type or connection |
| --- | --- |
| finite vocabulary | Enum |
| complete value | Value Object |
| identity lifecycle | Entity |
| value computation | Calculation |
| read model | Query |
| strategy selection | Policy |
| outcome function | Rule |
| state change | Operation |
| effects and connections | Mapping, Interface, Event, Operation |
| orchestration and lifecycle | Workflow, State Machine |
| relation composition | Rule `enforces` Operation |

### How the code-shape inspector records what it checked

One factory run is an isolated experiment:

1. a request names the checks and repository-owned inputs;
2. each evidence collector lists every file and tool the check needs;
3. planning records exact file contents and tool versions so they cannot change during
   the run;
4. execution copies those locked inputs and lets later steps use only checked
   references from the same run;
5. replay repeats each check in a separate process;
6. the relevant result is kept separate from paths, clocks, process IDs, and other
   machine-only details;
7. the result is verified before it is written; and
8. the repeatability check compares two isolated copies.

`inspect` and `init` consume the experimental `FactoryKitPackage/v1`. They stop
instead of guessing when a code mapping is still only a proposal, a type is not
active, a referenced file has changed or is missing, or an identifier is invalid.
There is no `--allow-candidate` shortcut. All 13 current mappings are still
`candidate-mapped`, so a proposed mapping alone is not enough to initialize an
approved implementation kit.

The isolated code-checking process—called the factory—reports evidence; it cannot
approve the result. See the
[factory README](impl/architecture-conformance/factory/README.md).

### Where the two mechanisms meet—and where they stop

```text
specification
  -> obligations
  -> expected code shape
  -> observed code facts
  -> findings + receipt
  -> human decision
```

Derived obligations say what needs evidence. Architecture expectations say what the
implementation should preserve. Observations and findings show what one exact code
target actually supports.

These pieces are not one supported end-to-end path for the selected Key and Door JSON
profile yet. The current derivation input and the selected authoring input remain
separate, and architecture enforcement is candidate and partial. Limited local factory
checks exist for selected types and one `Rule enforces Operation` composition;
they do not establish complete type coverage or production behavior.

Generated tests are not test executions. Passing tests and receipts are evidence, not
implementation acceptance or release authorization. Experimental `architecture.*`
connections also belong to the implementation model; they cannot redefine DomainSpec's
domain relationships.

For the implementation boundary, read the
[Architecture-Pattern Enforcement specification](development/architecture-pattern-enforcement/SPEC.md)
and the [factory README](impl/architecture-conformance/factory/README.md). The older
[implementation-model experiment](development/implementation-conformance/ontology-experiment/README.md)
shows how expected properties and reported facts are represented; it does not define
DomainSpec's canonical types or relationships.

## Worked feature example: Financial Settlement

The Financial Settlement feature illustrates several active types without pretending
to cover the whole language. Its hand-written normalized Markdown remains useful as a
broad **legacy language example**. It is classified for migration to a consumer
example and must not be used as authority for the selected minted-project source
format.

| Concept | Meta-type | Required information shown here |
| --- | --- | --- |
| SettlementTransaction | Entity | `transactionId` is its declared identity. |
| SettlementResult | Value Object | No identity; equality is declared over its fields. |
| SettlementTransactionType | Enum | Finite `MAKEUP_APPLIED` and `PAYOUT` vocabulary. |
| GenerateSettlement | Operation | `state_change = yes`. |
| GetSettlementPreview | Query | `state_change = no`. |
| DealSplitCalculation | Calculation | `formal_return_type = value`. |
| NoDuplicateMakeupRule | Rule | `formal_return_type = boolean`. |

Its authored graph includes:

```text
NoDuplicateMakeupRule --[enforces]--> GenerateSettlement
DealSplitCalculation  --[calculates]--> GenerateSettlement
GenerateSettlement    --[creates]--> SettlementTransaction
GenerateSettlement    --[queries]--> SettlementTransaction
GetSettlementPreview  --[queries]--> SettlementTransaction
```

The same repository feature also has a generated view with Calculation, Operation,
Event, and Rule concepts. Compare the
[legacy normalized feature pack](impl/spec/features/financial-settlement/SPEC.md) with
its [generated human view](impl/spec/features/financial-settlement/generated/SPEC.md),
but do not copy this pair as the future consumer package. Use Key and Door for the
current independent-node source layout.

One feature is an example, not proof that every possible domain has the same structure.

## What DomainSpec v2 is—and is not

### It is

- a small, defined vocabulary for system concepts;
- clear rules for the information each type must contain;
- a list of allowed connections between types;
- repeatable tools for supported inputs that produce normalized graphs, read-only
  views, or focused structural checks;
- focused checks of the declared structure generated from that map;
- experiments for comparing the design with selected facts from code;
- a way to expose disagreements between sources instead of hiding them; and
- a private implementation project whose decisions apply only inside this
  repository.

### It is not

- a general-purpose programming language;
- a proof that a written description is true in the real world;
- an LLM that guesses domain meaning;
- a universal compiler from requirements to applications;
- a claim that all meta-types have production implementations;
- an implementation model that can approve DomainSpec definitions by itself;
- a reason to treat one passing test as proof that the running application is
  correct; or
- the Saturn control loop. DomainSpec supplies the structured description; Saturn is
  the separate private loop that compares the design with observed reality.

The useful result today is a checked map of part of a system. The project's official
term is a **typed composable graph fragment**. It is not a mathematical proof of the
whole domain, a complete account of behavior, or a universal code generator. The
[definition registry](definitions/DEFINITIONS.md) and
[authority model](authority/AUTHORITY-MODEL.md) preserve that boundary explicitly.

## Place in the wider private system

The wider private architecture uses three complementary ideas:

- **DomainSpec is the what:** the system concepts, their connections, and checks
  derived from that description.
- **Arcanum is the how:** reusable steps and tools for work with explicit checks and
  decision owners.
- **Saturn is the loop:** the separate idea for comparing the design with reality
  and routing a correction when they differ.

This repository contains the DomainSpec v2 implementation. DomainSpec and Saturn are
private and are not publicly shipped. Only Arcanum is the public pillar, so private
DomainSpec or Saturn text must not be copied into it.

For orientation only, see the candidate
[framework concept map](../framework-unification/CONCEPT-MAP.md),
[Saturn layer map](../../ops/development/2026-06-21-paper-saturn-explainer/SATURN-LAYER-MAP.md),
and [agentic-system deep dive](../../cyberAlchemy/agentic-system-deep-dive.md).
These are private draft architecture views. They do not define DomainSpec v2 and do
not prove that anything has been deployed.

## Who owns each decision

Different sources answer different questions. Keeping them separate prevents a test
result or generated document from making a decision it is not allowed to make.

| Surface | What it owns | What it cannot do |
| --- | --- | --- |
| Local definitions | The DomainSpec labels, the rules for forming each type, the allowed relationships, and local project rules. | Claim that code or production behavior exists without evidence and an owner decision. |
| Project source | The meaning of a project, feature, concept, field, rule, and connection. | Redefine the shared DomainSpec language simply by using it. |
| JSON compiler and legacy check generator | The JSON compiler checks the experimental consumer package and builds read-only views. The separate legacy engine derives obligations and tests from Markdown input. | Join those paths automatically, prove all business behavior, or establish production correctness. |
| Generated views | System maps, source lists, Markdown, test descriptions, and result summaries. | Replace the source files people are meant to edit. |
| Experimental implementation model | Terms for describing code forms, expected properties, observations, and differences. | Approve a DomainSpec definition or an implementation. |
| Implementation or release owner | The final decision about implementation acceptance, deployment, release, and production use. | Be replaced by an experimental result record. |

The [source-spine file](authority/source-spine.md) lists which sources take
precedence. The central rule in the
[authority model](authority/AUTHORITY-MODEL.md) is simple: DomainSpec may describe,
derive, check, and report differences. It may not approve an implementation or
production use without direct evidence and the responsible owner's decision.

DomainSpec v1 and CyberAlchemy v2 are older references only. They can explain history,
but they do not decide what DomainSpec v2 means.

## Five different things that are easy to confuse

| Thing | Example | Meaning |
| --- | --- | --- |
| Meta-type | `Rule` | An official DomainSpec label plus the information required to use it. |
| Domain concept | `PayoutEligibilityRule` | One project-owned use of a meta-type in a feature. |
| Runtime instance | one settlement transaction | A value or object created while software runs; it is not a graph concept. |
| Architecture concept type | `architecture.RuleImplementation` | An experimental label for how a domain concept may appear in code. |
| Native language form | a TypeScript arrow function | One language-specific code form; it does not redefine `Rule`. |

Two more distinctions matter:

- A **property type** such as `callable.form` describes a fact expected or observed
  in code; it is
  not a DomainSpec meta-type.
- An **observation** reports what a tool saw in code. It is an input to a comparison,
  not a fact that approves itself.

## Ask six separate status questions

A single label such as “complete” hides important gaps. Ask these six questions
separately:

| Axis | Typical values | Question answered |
| --- | --- | --- |
| Definition status | active; candidate (proposed); deferred (postponed); superseded (replaced) | Is this label officially available in DomainSpec? |
| Code mapping | candidate-mapped (proposed); not-admitted (not formally accepted); superseded (replaced) | Has the experiment proposed how this type may appear in code? |
| Language implementation | proposed; selected; provider-absent (no evidence tool yet); bounded proof (limited recorded result) | Is there a form for a target language and a tool that can check it? |
| Validation | pass; fail; expected-red (an intentionally invalid case failed as expected) | Did the exact current inputs satisfy a particular check? |
| Next-step readiness | ready, blocked, excluded | May the next controlled implementation step begin? |
| Approval and release | none, owner-decided, release-authorized | Who may approve the result or release it? |

For example, `Entity` is an active DomainSpec type. The current experiment proposes
a way to represent it in code, and a test built from artificial examples passes. But
no tool has inspected real target code yet, and no language-level test covers
construction, reconstruction, or the full lifecycle. There is also no cross-language
comparison or approval for release or production. These statements do not conflict
because they answer different questions.

## Current working-tree snapshot

This is a dated picture of a changing working tree, captured on 2026-08-12. Run the
linked validators again before using these numbers for a current decision.

| Area | What was observed | What this proves—and no more |
| --- | --- | --- |
| Type list (DS-D1 registry) | 24 non-retired labels: 13 active backend, 9 candidate UI, and 2 deferred UI; plus the retired Saga ID, for 25 retained records. | The available language inventory only. |
| Allowed connections (DS-D8 registry) | 31 allowed connections, one generated reverse view, three postponed proposals, and one retired alias. | The currently supported graph connections, not a complete mathematical law. |
| Experimental type-to-code mapping | 25 records: all 13 active types have a proposed code mapping (`candidate-mapped`); 11 non-active types are `not-admitted`; Saga is `superseded`. | An experimental read-only mapping that cannot approve anything (`authority_effect: none`). |
| Experimental code-property vocabulary | 27 concept types, 99 property definitions, 18 relation definitions, 8 operators, and 3 language views. | An experimental vocabulary for describing code properties. |
| Implementation readiness queue | 0 ready, 13 blocked, and 12 excluded. | No meta-type is currently implementation-ready through this queue. |
| Experimental factory tasks | MTF-001 through MTF-029 recorded complete. | Completion of this limited experimental task list, not implementation of every type. |
| Same-host repeatability | Two isolated runs on the same host produced the same relevant result for the fixed nine-node example. | Repeatability on one host and toolchain only. |
| Project and release status | Project stage `build`, gate `flag`; first-production-release stage `plan`, gate `block`. | Production remains unauthorized. |

The live counts come from
[meta-types.yml](definitions/meta-types/meta-types.yml),
[relationships.yml](definitions/relationships/relationships.yml),
[domain-meta-types.projection.json](development/implementation-conformance/ontology-experiment/domain-meta-types.projection.json),
[ontology.json](development/implementation-conformance/ontology-experiment/ontology.json), and
[IMPLEMENTATION-QUEUE.json](development/ontology-form-decisions/IMPLEMENTATION-QUEUE.json).

## Current development status and known failures

The derivation engine and limited architecture checks exist separately. The general
selected-JSON-to-evidence bridge described below remains planned.

### August 13: machine-view test generation was designed, not implemented

The latest refinement run defines a possible future route from an owner-approved machine
view to generated structural checks. It produced a design and an 11-unit work pack.
No work unit was selected or executed, and the engine does not yet read this machine
view. The route still depends on repairing and admitting the ontology candidate,
independent expected-result evidence, causal negative cases, independent replay, and
an explicit CLI migration.

This is planning evidence, not a product capability. See the
[refinement result](development/refinement-runs/20260813T025311Z-ontology-machine-view-test-generation/RESULT.md)
and [work pack](development/refinement-runs/20260813T025311Z-ontology-machine-view-test-generation/stages/09-invoke-plan/WORK-PACK.md).

### Component check snapshot: August 13, 2026

- The Test Derivation Engine suite passes 241 tests across 29 test files.
- The engine's standalone TypeScript check still fails. Its current errors include
  imports that cross the package's configured source boundary and strict typing errors.
  This prevents a clean typecheck claim even though the tests pass.
- The architecture factory passes its TypeScript check and 69 tests across 19 test
  files.

These are local component results. They do not create the missing end-to-end bridge,
establish a supported user command, accept an implementation, or authorize a release.

### August 7: repeatable same-host code-comparison run

The experiment's MTF work list records MTF-001 through MTF-029 complete. The limited
nine-node example includes two TypeScript Enum checks, Rule checks in
TypeScript/Python/Rust, matching Rule results across languages, a TypeScript Operation,
the Rule-enforces-Operation connection, and a readiness summary that cannot approve
anything.

Two isolated runs on the same host produced the same relevant result while recording
different process details. This proves repeatability on that host and
toolchain for the locked graph. It does not prove behavior on other hosts, every
meta-type, formal approval, release, deployment, or production readiness.

Evidence:

- [execution state](development/meta-type-realization-factory/EXECUTION-STATE.json)
- [prototype validation report](development/meta-type-factory-reproducibility/PROTOTYPE-VALIDATION-REPORT.md)

### August 12: remaining active meta-type candidate work

The newest working-tree result records (receipts) add local experimental findings
about code structure and language behavior:

| Result record (receipt) | What this result shows | What it does not show |
| --- | --- | --- |
| [RMT-ENUM-006](development/remaining-meta-types/receipts/RMT-ENUM-006.json) | TypeScript, Python, and Rust keep the same owned values and matching serialization and parsing behavior on one fixed host. | A separate source of expected answers, proof on other hosts, readiness, approval, or release. |
| [RMT-CALC-007](development/remaining-meta-types/receipts/RMT-CALC-007.json) | NetSettlement matches on four fixed safe-integer inputs and reports no external effects. | Every possible input or caller, a separate expected-answer source, or proof on other hosts. |
| [RMT-POLICY-008](development/remaining-meta-types/receipts/RMT-POLICY-008.json) | Five fixed inputs return the expected strategy name, that strategy belongs to the catalogue, and it is not executed. | Whether the policy or strategy is correct for the business, arbitrary inputs, or production behavior. |
| [RMT-QUERY-007](development/remaining-meta-types/receipts/RMT-QUERY-007.json) | One exact success example, ordered reads, a result containing only its declared fields, none of the explicitly disallowed side effects, and matching compared-language results. | Failure behavior, general business correctness, a separate expected-answer source, or proof on other hosts. |
| [RMT-VO-007](development/remaining-meta-types/receipts/RMT-VO-007.json) | Equality over every owned field, matching project-defined hashes for equal values, validation, immutability, and extension restrictions. | Identical hash bytes across languages, freedom from collisions, arbitrary inputs, or proof on other hosts. |
| [RMT-ENTITY-001](development/remaining-meta-types/receipts/RMT-ENTITY-001.json) | An experimental model and language rules, stable identity, artificial valid cases, and intentionally invalid cases. | A tool that inspects real code, real code targets, language-level proof of construction or reconstruction, cross-language comparison, or an implementation candidate. |

These result records have `authority_effect: none`: they can report results but cannot
approve or promote anything. They have not made the code-form decision queue ready or
authorized production.

### Effects and connections; workflows and lifecycles

The live W3 validator passes its limited Mapping, Interface, Event, and Operation
experiment: 30 properties, typed code connections, 12 links to language-specific
protocols, and four links between descriptor records.

The live W4 validator passes its limited Workflow and State Machine experiment: 16
properties, typed code connections, six links to language-specific protocols, and two
links between descriptor records.

Both validators explicitly say their results do not approve promotion, release,
deployment, or production use.

## Captured validation state and known drift

The following table was captured on 2026-08-12. The working tree is changing. Some focused experimental checks pass, while broader
checks and checks tied to earlier accepted files fail. This disagreement is useful to
see; it is not permission to rewrite old result records or call the latest additions
approved.

| Command, run 2026-08-12 | Live result | Why |
| --- | --- | --- |
| `node validate-ontology.mjs` | fail | New `architecture.constructed_by` and `architecture.validated_by` connections violate the experiment's current no-cycle rule. |
| `node validate-implementation-architecture-types.mjs` | fail | The stored view expects 6 two-way mappings and 10 visible types; current data has 13 and 17. |
| `node semantic-slices/validate-meta-type-semantic-slices.mjs` | fail | The stored type slice differs from what the current repeatable extraction produces. |
| `node validate-rmt-enum.mjs` | fail | Recorded file hashes are stale and the TypeScript status changed. |
| `node validate-rmt-calculation.mjs` | fail | Calculation properties changed and some recorded material references are stale. |
| `node validate-rmt-policy.mjs` | fail | Recorded file hashes no longer match. |
| `node validate-rmt-query.mjs` | fail | Recorded file hashes no longer match. |
| `node validate-rmt-value-object.mjs` | fail | Connection rules and hashes tied to earlier accepted files no longer match current data. |
| `node validate-rmt-entity.mjs` | pass | Artificial 5/5 valid cases, 7/7 intentionally invalid cases, 4/4 modeled routes, and 5/5 structural controls pass; no tool has inspected real code and no language-level lifecycle proof exists. |
| `node validate-w3-effects-connections.mjs` | pass | This limited effects-and-connections experiment only. |
| `node validate-w4-orchestration-lifecycle.mjs` | pass | This limited workflow-and-lifecycle experiment only. |

These commands live in
[development/implementation-conformance/ontology-experiment](development/implementation-conformance/ontology-experiment/).

### Documentation snapshots that are behind the live JSON

The experiment README still reports 72 properties, 14 connections, and an older split
of 9 mapped types, 1 type with a language profile, and 3 unsupported types. The live
JSON now contains 99 properties, 18 connections, and proposed mappings for all 13
active types.

The Beginner Guide describes an even earlier five-mapped snapshot. The ontology map
and the form-decision matrix also lag the current modified JSON. In particular, the
form matrix records older mapping statuses and old hashes for the implementation model
and generated type-to-code view. The live implementation queue still reports zero
ready types.

Treat those documents as dated explanations. For current counts, query the machine
files and run validators. Do not silently update files covered by an older approval.
Their owners must review the changes, rerun the required checks, and request a new
approval.

## Eight conclusions the evidence does not support

Most mistakes happen when evidence from one step is treated as proof of a different
step.

### “The class name says Entity, so it is an Entity”

No. The declared fields and identity rule make it an Entity, not a class suffix or
framework decorator.

### “The code returns a boolean, so the prose must be a Rule”

No. The DomainSpec source must declare `formal_return_type = boolean`. What a tool sees
in code cannot rewrite the intended meaning.

### “A passing derived test proves the application is correct”

No. It proves only that one exact generated check passed on the recorded inputs. It
does not prove the application's full behavior, business correctness, deployment, or
owner acceptance.

### “Candidate-mapped means the code-checking process is ready”

No. `candidate-mapped` means only that a possible code representation has been
proposed. The process still needs an approved mapping, language rules, a tool that
inspects code, an exact target, sufficient evidence, queue readiness, and owner
approval.

### “Every connection deserves a relationship type”

No. Imports, field references, reverse navigation, and drawing convenience often
belong in properties, metadata, or generated views. A connection deserves its own
type only when removing it changes validation, ownership, a generated check, or an
output.

### “An active UI relationship makes Page or Guard active”

No. The connection's status and each endpoint type's status are separate. The nine UI
labels remain proposed and two remain deferred.

### “Generated Markdown is the source”

No. In the selected consumer path, edit `project.json`, the feature record, or a node
record and rebuild. In the separate legacy path, edit the explicit legacy input.
Never repair a generated Markdown view by hand.

### “Saga is available because it is no longer active”

No. It is a permanently retired historical ID. Use Workflow and never reuse DS-D1.10.

## Troubleshooting the current repository workflow

### `npx --no-install` cannot find `tsx`

The checkout is not prepared. The guide does not yet have an approved clean-install
procedure. Do not remove `--no-install` just to download an unreviewed tool. Ask the
maintainer for the supported local setup.

### pnpm stops with `ERR_PNPM_IGNORED_BUILDS`

The current pnpm workspace leaves the esbuild `allowBuilds` decision unresolved. That
is a dependency-policy decision, not a reason for a user to run `pnpm approve-builds`
blindly. The setup owner must decide and document the allowed build scripts.

### Legacy content validation passes but engine `lint` fails

These commands belong to the legacy Markdown route and check different boundaries.
Content and relationship validators check type shapes and DS-D8 connections. Engine
`lint` also checks the parser's canonical table form and formal cells. On 2026-08-13,
Financial Settlement passed the broad content/relationship checks but its engine lint
reported one non-canonical graph table. This says nothing about whether a minted JSON
package passes its compiler. Use `agent-execution-orchestrator` when you need a
parser-clean legacy example.

### A receipt contains parser rejections

A receipt records what was accepted, omitted, or rejected. It is not a pass badge.
Run `lint` first and inspect `summary.parser_rejections` in the receipt. Do not infer
success from the presence of a receipt or from a zero process exit alone.

### `npm run validate` passed, so every DomainSpec check passed

No. The current `validate` script runs documentation links, relationships, content,
tool tests, and the sample engine lint. It does not include every engine test,
typecheck, tag, instance, factory, experiment, browser, release, or production check.
Name the exact command whose result you are reporting.

## How to extend DomainSpec responsibly

Add a type or connection only when an existing one cannot express an important
distinction, and show exactly which check or generated result would change. Writing a
required-shape file or experimental code-mapping record does not make it approved.

### Add a domain concept

Use an active meta-type, add the required information and allowed connections, then
check both the concept and graph.

### Propose a new meta-type

Use [How to propose a new DomainSpec meta-type](#how-to-propose-a-new-domainspec-meta-type):
disprove the need first, separate the nearest neighbour, add discriminating evidence,
and preserve the definitions-owner gate. An experimental required-shape file or
code-mapping record cannot approve itself.

### Add a relationship

Specify source and target types, direction, quantity limits, allowed location,
examples, invalid examples, the failure to report, and the validation or output it
changes. Show that removing the connection changes at least one tracked result.

### Add a language-specific code form

Keep the shared meaning with the type's owner and executable code observations with
the owner of the code being inspected. Add a versioned evidence collector (called a
provider) with exact inputs, components, tools, dependencies, generated checks,
deliberately altered cases, expected failures, the ability to rerun the check, checks
that detect changed inputs or results, and an exact statement of what the result can
prove. Do not change the shared runner merely because a new type is added.

## Source map

Use this source map when a claim needs confirmation. The guide does not define the
DomainSpec language; if it disagrees with an authoritative source below, the source
wins.

### Files that define the DomainSpec language

- [Project README](README.md) — project scope and where the implementation lives.
- [Axioms](authority/AXIOMS.md) — the project's basic rules.
- [Authority model](authority/AUTHORITY-MODEL.md) — who may make each decision.
- [Source spine](authority/source-spine.md) — which files take precedence.
- [Definitions](definitions/DEFINITIONS.md) — official definition cards and IDs.
- [Meta-type cards](definitions/meta-types/meta-types.md) — human-readable guide to every DS-D1 type.
- [Meta-type index](definitions/meta-types/meta-types.yml) — machine-readable type index.
- [Allowed connection registry](definitions/relationships/relationships.yml) — official machine-readable DS-D8 connections.
- [Relationship guide](definitions/relationships/relationships.md) — human-readable connection guide.
- [Required-shape files](impl/spec/meta-types/) — official type rules used by validation.

### Files used to write, generate, and check specifications

- [Minted-project owner decision](authority/decisions/2026-07-14-minted-project-node-package.md) — selects project, feature, and independent-node JSON as the consumer default while withholding release admission.
- [Supported profile registry](definitions/minted-project/supported-profiles.yml) — experimental four-type, three-relationship profile and its exact registry bindings.
- [Consumer-source contract index](impl/spec/minted-project/INDEX.md) — source and generated record roles.
- [Key and Door source fixture](impl/test-derivation-engine/__fixtures__/minted-project/contract/positive/key-and-door/project.json) — complete checked independent-node example.
- [Guide schema](COMPLETE-GUIDE.schema.json) and [guide manifest](COMPLETE-GUIDE.lanes.json) — reader journey, example posture, source boundaries, and documentation validation contract; neither defines DomainSpec or grants authority.
- [Financial Settlement](impl/spec/features/financial-settlement/SPEC.md) — broad legacy Markdown type example and migration candidate, not minted-project authority.
- [Check generator](impl/test-derivation-engine/src/README.md) — legacy document-to-obligation path.
- [Implementation package scripts](impl/package.json) — current repository validation commands, not a released consumer CLI.

### Experimental files for comparing specifications with code

- [Architecture-Pattern Enforcement specification](development/architecture-pattern-enforcement/SPEC.md) — candidate program for comparing typed architecture expectations with observed implementation evidence.
- [Implementation-model experiment README](development/implementation-conformance/ontology-experiment/README.md) — purpose, limits, and date.
- [Current experimental model data](development/implementation-conformance/ontology-experiment/ontology.json) — machine-readable code-property vocabulary.
- [Experimental type-to-code view](development/implementation-conformance/ontology-experiment/domain-meta-types.projection.json) — proposed mappings that cannot approve themselves.
- [Property comparison model](development/implementation-conformance/ontology-experiment/PROPERTY-EVALUATION-MODEL.md) — how expected and reported values are compared.
- [Traceability and drift](development/implementation-conformance/ontology-experiment/TRACEABILITY-AND-DRIFT.md) — how results link to inputs and report disagreements.
- [Code-form decision process](development/ontology-form-decisions/PROCESS.md) — how an owner reviews a proposed code form.
- [Code-form decision matrix](development/ontology-form-decisions/FORM-DECISION-MATRIX.json) — dated mapping decisions.
- [Implementation queue](development/ontology-form-decisions/IMPLEMENTATION-QUEUE.json) — ready, blocked, and excluded types.
- [Isolated code-checking process](impl/architecture-conformance/factory/README.md) — how fixed inputs are checked and repeated.
- [MTF task progress](development/meta-type-realization-factory/EXECUTION-STATE.json) — recorded state of MTF-001 through MTF-029.
- [Same-host repeatability report](development/meta-type-factory-reproducibility/PROTOTYPE-VALIDATION-REPORT.md) — what repeated successfully on one host, and no more.
- [Machine-view test-generation refinement](development/refinement-runs/20260813T025311Z-ontology-machine-view-test-generation/RESULT.md) — a validated design and work pack; no implementation unit was selected or executed.

## Key terms in plain language

**Concept** — a named thing the project needs to describe.

**Consumer source package** — the project-owned JSON records a future user edits:
the project record, feature records, and independent concept nodes.

**Source profile** — the versioned rule that says which node kinds, body shapes, and
connections one source package may use. The current profile is experimental.

**Meta-type** — the category assigned to a concept, such as Entity, Rule, or
Operation.

**Formation criterion** — the information a declaration must contain to count as one
type.

**Relationship signature** — an allowed connection, including its direction, endpoint
types, location, and quantity limits.

**Typed concept graph** — the map of concepts declared in a specification and the
connections allowed between their types.

**Obligation** — one stable, named item derived from a supported declaration that later
tests or implementation evidence must account for.

**Code comparison profile** — the shared or language-specific expectations selected
for one experimental code comparison. It is separate from the source profile.

**Architecture type enforcement** — the candidate process of comparing selected
expectations for a DomainSpec type with facts gathered from exact code.

**Realization** — one proposed way a DomainSpec type appears in a programming
language.

**Observation** — what an evidence-gathering tool reported about code.

**Finding** — a recorded match or difference between an expectation and an
observation.

**Receipt** — a record of the exact inputs, checks, results, and limits.

**Candidate-mapped** — a possible code representation has been proposed; it is not
approved or implementation-ready.

**Drift** — two files, expectations, or results that no longer agree. Detecting the
difference does not correct it.

**Authority effect** — whether a file or result record may change official project
status. Most experiments and receipts here say `none`.

## Guide composition contract

This guide has a machine-checkable documentation contract:

- [COMPLETE-GUIDE.schema.json](COMPLETE-GUIDE.schema.json) defines the required guide
  identity, reader contract, source boundary, entry paths, section jobs, example
  posture, and validation expectations.
- [COMPLETE-GUIDE.lanes.json](COMPLETE-GUIDE.lanes.json) is the current manifest. It
  also preserves the visual lanes used by the HTML page.
- [COMPLETE-GUIDE.md](COMPLETE-GUIDE.md) and
  [COMPLETE-GUIDE.html](COMPLETE-GUIDE.html) are the two reader-facing renderings.

The schema protects the guide's composition and claim boundaries. It does not define a
meta-type, admit a source profile, make a code form official, approve a release, or
prove that readers understand the page. In particular, it validates the shape of the
manifest's profile summary rather than encoding the current profile catalogue. A
separate required check compares that summary with
`definitions/minted-project/supported-profiles.yml`. When a section, example, or
product status is added, its manifest entry must name the reader's job, availability,
claim class, evidence, and strongest supported conclusion. Visible prose must still
label planned, legacy, generated, and experimental material where readers encounter
it.

## Four questions to ask before trusting a claim

For every DomainSpec claim, be able to answer four questions:

1. **Meaning:** what does this concept mean, and which project defines that meaning?
2. **Rules:** which type and connection rules apply?
3. **Evidence:** which exact check ran on which exact files?
4. **Decision:** who is allowed to approve the next step?

If one answer is missing, report the gap. Do not fill it with confidence language.
