# SWU-BWVA-003 — Pinned Atlas Browser Evidence

Status: `blocked-by-dependency`

Depends on: `SWU-BWVA-002`

## Primary behavior

Validate the exact generated atlas through the shared Playwright/Chromium
runtime and emit a durable structural receipt and bounded screenshots.

## Material write scope

- `projects/body-war/ontology/business/scripts/validate-view-atlas-browser.mjs`

## Execution output scope

- `projects/body-war/ontology/business/receipts/view-atlas-browser-receipt.json`
- `projects/body-war/ontology/business/receipts/view-atlas-overview.png`
- `projects/body-war/ontology/business/receipts/view-atlas-portal.png`

## Acceptance

The harness pins atlas, catalog, projection, generator, source, coverage
receipt, Node, Playwright, Chromium revision, executable path/hash, viewport,
DPR, JavaScript/no-JavaScript/reduced-motion/print modes, fresh-context
isolation, loopback serving, assertions, screenshots, console errors,
teardown, timestamps, and claim ceiling.

Assertions cover:

- exact six-lens overview;
- search to one canonical node;
- keyboard activation and visible focus;
- actor/boundary portal to another lens with unchanged direction;
- Back/fragment recovery;
- all portal/node/relation anchors resolve uniquely;
- no-JavaScript complete content;
- 390px no horizontal document overflow;
- reduced-motion and print structure;
- zero console/page errors;
- zero comprehension, release, or production claim.

## Validation

```text
node projects/body-war/ontology/business/scripts/validate-view-atlas-browser.mjs
node projects/body-war/ontology/business/scripts/generate-views.mjs --check
node --test projects/body-war/ontology/business/tests/business-view-atlas-projection.test.mjs projects/body-war/ontology/business/tests/business-view-atlas-render.test.mjs projects/body-war/ontology/business/tests/business-views.test.mjs
node projects/body-war/ontology/business/scripts/validate.mjs
```

## Closeout

Write terminal receipts under
`projects/body-war/development/task-sessions/SWU-BWVA-003/`, then Invoke Refresh
may mark the frontier complete and set continuation to `null`.

