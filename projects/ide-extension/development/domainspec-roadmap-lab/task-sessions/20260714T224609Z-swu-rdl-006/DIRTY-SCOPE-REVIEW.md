# Dirty-Scope Review: SWU-RDL-006

## Selected Write Scope

SWU-RDL-006 would need to mutate shared IDE runtime files:

- `projects/ide-extension/src/server.mjs`;
- `projects/ide-extension/public/demo/l0.html`;
- focused IDE route/UI tests;
- package scripts only if required.

## Live Dirty State

`git status --short -- projects/ide-extension/public/demo/l0.html projects/ide-extension/src/server.mjs projects/ide-extension/tests projects/ide-extension/package.json projects/ide-extension/package-lock.json`
shows:

- `M projects/ide-extension/public/demo/l0.html`
- `M projects/ide-extension/src/server.mjs`
- `M projects/ide-extension/package.json`
- `M projects/ide-extension/package-lock.json`
- modified Canvas/Workbench tests
- many untracked Operations v1 schemas, fixtures, tests, and an E2E spec

## Overlapping Hunks

### `public/demo/l0.html`

Current dirty hunks:

- change `.workspace` minimum height;
- add full `Craft Frontier` panel and styles;
- change logo cache/alt text;
- add `state.craftFrontier`;
- add Craft DOM references;
- disable `craftRefresh` during commands;
- add `renderCraftFrontier()` and `refreshCraft()`;
- call `refreshCraft()` during boot;
- wire `craftRefresh` click handling.

Why this blocks SWU-RDL-006:

- A focused Roadmap Lab mode must hide unrelated Craft/operations context while
  preserving the Canvas event adapter.
- The dirty work adds visible Craft Frontier context to the same page and startup
  path. Any focused-mode change would have to decide whether to hide, preserve,
  or route around those new hunks.

### `src/server.mjs`

Current dirty hunks:

- add Craft frontier index validation and `GET /api/craft/frontier`;
- add Canvas blob store integration into persistence;
- add Operations v1 service, derivation, mutation, content, and error routing;
- modify canvas event validation guard;
- alter runtime initialization dependencies.

Why this blocks SWU-RDL-006:

- A dedicated Roadmap Lab route/publish witness would be added to the same
  server initialization and HTTP dispatch surface.
- The current server changes are not just adjacent formatting; they introduce
  new state services and API routes whose ownership and validation status are
  outside this SWU.

### `package.json` / tests

Current dirty hunks:

- add multiple Operations v1 scripts;
- add `parse5`;
- require Node `>=20.19.0`;
- update or add many tests/fixtures around operations and Canvas behavior.

Why this blocks SWU-RDL-006:

- SWU-RDL-006 validation requires Canvas route/UI/interaction regressions.
- Adding Roadmap Lab scripts/tests now would compose with a separate uncommitted
  Operations v1 validation surface.

## Decision

Block mutation now. The cleanest strict route is to finish or isolate the
Operations/Craft IDE work first, then rerun SWU-RDL-006 on a stable baseline.
Alternatives require explicit owner approval because they either accept merge
risk or create a duplicate route that violates the Roadmap Lab architecture.
