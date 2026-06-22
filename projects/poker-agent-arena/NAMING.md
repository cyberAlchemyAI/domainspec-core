# Poker Agent Arena Naming

Status: project naming convention
Purpose: keep route, artifact, and fixture names descriptive without making every identifier carry the whole design.

## Core Rule

Route names describe the durable arena surface. Fixture names describe the game or proof case.

That means the first executable route is:

- Route id: `local-arena-cli-v0`
- Human label: `Local Arena CLI v0`

Kuhn is the first fixture gate inside that route. Leduc is the next fixture expansion. Neither game should own the route id.

## Route Id Shape

Use:

```text
<scope>-<surface>-<interface>-<version>
```

Examples:

- `local-arena-cli-v0`
- `holdem-adapter-cli-v1`

Guidelines:

- Prefer 3-4 dense tokens.
- Aim for 18-24 characters; 30 is the soft ceiling.
- Avoid `mvp` in repeated artifact ids; use it in prose when needed.
- Avoid fixture names in route ids unless the whole durable surface is fixture-specific.
- Avoid `engine` for v0 route naming; reserve engine language for Hold'em engine parity and adapters.

## Artifact Names

| Artifact kind | Convention | Example |
| --- | --- | --- |
| Route id | Durable surface | `local-arena-cli-v0` |
| Route label | Title case route id | `Local Arena CLI v0` |
| Work pack title | Route label + work pack | `WP-PAA-001: Local Arena CLI v0 Work Pack` |
| Repair SWU | Repair + route label + handoff | `SWU-PAA-001R: Repair Local Arena CLI v0 Handoff` |
| Contract SWU | Freeze + route label + contract | `SWU-PAA-001: Freeze Local Arena CLI v0 Contract` |
| Fixture SWU | Game/proof-specific | `SWU-PAA-002: Add Kuhn Fixture Gate` |
| Expansion SWU | Game/proof-specific extension | `SWU-PAA-003: Add Leduc Board-Reveal Extension` |
| Spec folders | Layer/version root | `spec/l0/` |
| Fixture folders | Game/proof-specific | `fixtures/l0/kuhn_hidden_info/` |

## Naming Layers

- Route: `Local Arena CLI v0`, the first local executable arena surface.
- Fixture gate: `Kuhn Hidden Info`, the first proof that protocol, hidden-information, fallback, replay, and diagnostics work.
- Fixture expansion: `Leduc Board Reveal`, the next proof that public board reveal and two-street transitions hold.
- Engine parity: Hold'em adapter work after toy fixtures prove the route.

## Terms To Demote

- `local-kuhn-cli-mvp`: use only as historical review evidence. Replace with `local-arena-cli-v0`.
- `kuhn-leduc-cli-mvp`: avoid unless both games are truly required in the first executable route.
- `local-engine-cli-v0`: close but misleading here; `engine` belongs to the later adapter layer.
- `MVP0`: acceptable in prose, but not as the repeated route id.

## Clarity Balance

Good names answer three questions:

1. Where does it run?
2. What surface does it expose?
3. What interface/version is being frozen?

They do not need to answer every fixture, gate, and validation detail. Put that density in the artifact body.
