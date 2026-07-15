# Browser Evidence: SWU-RDL-005

## Focused Playwright Run

Command:

```bash
cd projects/ide-extension
npx playwright test --config ../domainspec-v2/development/first-production-release/visibility/tests/e2e/playwright.config.mjs
```

Result: PASS, 2 tests.

Covered:

- keyboard focus/Enter activation for orientation;
- exact `postMessage` capture for:
  - `roadmap.orientation.acknowledged`;
  - `roadmap.restatement.submitted`;
  - `roadmap.source.requested`;
  - `roadmap.improvement.proposed`;
- exact top-level message keys: `type`, `eventName`, `payload`;
- participant label and `sha256:*` input fingerprint on every event;
- FPR-01 restatement binding;
- presentation-copy proposal binding to `copy.node.FPR-01.title`;
- source request binding to `roadmap-copy.json`;
- local status waits for Canvas storage acknowledgment;
- explicit parent result can move status to `Stored by Canvas.`;
- blank participant and missing graph/claim evidence preserve draft and emit no
  semantic event.

## Screenshots

- `output/playwright/roadmap-lab-swu005-desktop.png`
  - size: 1280x6779
  - sha256: `0775ad667b3fd91def45d91cd81bbeebd87fdf69ad1e5ba805db974e513f07c4`
- `output/playwright/roadmap-lab-swu005-mobile.png`
  - size: 776x13796
  - sha256: `8aa7ae16bb3f57d46d8bffceb27f0139310917fa2150fc86e4aa266ec0c103f5`

## Generated Output

- `roadmap-data.json`: `b77f26be55a8e1a41d580fba9da10bb4f417a8adbdedfc3c189993c013768832`
- `roadmap.html`: `4adfff27b062082f46b6f3bfefc050b25f49d1927a9b563ca95945788498aa12`

The data digest did not change in this SWU because the guided UI is a template
addition. The HTML digest changed as expected.

## Boundary Checks

- No `/api/canvas/events`, `fetch`, `XMLHttpRequest`, `localStorage`, or
  `sessionStorage` calls are present in generated HTML or template.
- The page can say `Stored by Canvas.` only after an explicit
  `ide-extension.canvas.event.result` message.
- SWU-RDL-006 still owns the real parent route, storage API call, and cursor
  polling proof.
