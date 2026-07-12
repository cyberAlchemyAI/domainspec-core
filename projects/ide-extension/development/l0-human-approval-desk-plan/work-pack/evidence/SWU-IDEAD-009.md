# SWU-IDEAD-009 Evidence

```yaml
swu_id: SWU-IDEAD-009
result: pass
capability_ref: task-session
receipt_kind: local-fallback
receipt_artifact: projects/ide-extension/development/l0-human-approval-desk-plan/work-pack/evidence/SWU-IDEAD-009.md
files_touched:
  - package.json
  - package-lock.json
  - .gitignore
  - playwright.config.mjs
  - tests/e2e/server-harness.mjs
  - tests/e2e/l0-approval-desk.spec.mjs
  - development/l0-human-approval-desk-plan/work-pack/evidence/SWU-IDEAD-009-assets/desktop.png
  - development/l0-human-approval-desk-plan/work-pack/evidence/SWU-IDEAD-009-assets/mobile.png
validation:
  - npm run test:e2e
  - npm run validate:schemas
  - npm run smoke
  - npm run test:adversarial
  - npm run test:recovery
  - node --test --test-concurrency=1 tests/*.test.mjs
  - npm audit --audit-level=high
  - git diff --check
blockers: []
residue:
  - The checked-in legacy state remains intentionally incompatible with event_version 1 and requires a separately governed migration or archive decision.
reroute: TASK-VERIFY-READINESS
handoff_note: Chromium proves the complete human workflow at desktop and mobile viewports with no layout overlap, unexpected console errors, or page errors.
```

## Browser Environment

| Field | Evidence |
| --- | --- |
| Test runner | `@playwright/test` 1.61.1 |
| Browser | project-scoped Playwright Chromium |
| Server | loopback-only test harness on `127.0.0.1:4177` |
| State | fresh temporary directory created and removed by the harness |
| Workers | 1, preserving deterministic event order |
| HTML report | `projects/ide-extension/output/playwright/SWU-IDEAD-009/report/index.html` |
| Result | 2/2 projects passed |

## Viewport Evidence

| Project | Viewport | Screenshot | Layout | Console |
| --- | --- | --- | --- | --- |
| desktop | 1440 x 900 | [desktop.png](SWU-IDEAD-009-assets/desktop.png) | no horizontal overflow or panel intersections | 0 unexpected console errors; 0 page errors |
| mobile | 390 x 844 | [mobile.png](SWU-IDEAD-009-assets/mobile.png) | coherent single-column stack; no horizontal overflow or panel intersections | 0 unexpected console errors; 0 page errors |

Both screenshots were visually inspected at original resolution. Long contract text wraps within queue and detail boundaries. The mobile history list preserves its scroll position while the detail and evidence sections remain fully reachable.

## Proven Workflow

Each viewport project independently proves:

1. The first page renders nonblank and reports a connected server.
2. Proposal A and proposal B are prepared and remain ID-addressable.
3. Keyboard Tab traversal reaches proposal controls and the enabled approve action with visible focus.
4. A is approved after explicit confirmation, its actions become disabled, and direct replay returns `409 already_resolved`.
5. B is rejected with a reason and receives no passed receipt.
6. History exposes both terminal proposals.
7. Reload reconstructs terminal state from the event log.
8. A remains selectable with one receipt.
9. Before, After, and Receipt controls load bounded evidence whose run, envelope, and approval IDs match A.
10. Final desktop/mobile layout and browser error checks pass.

## Full Validation

| Command | Result |
| --- | --- |
| `npm run test:e2e` | pass: desktop and mobile, 2/2 |
| `npm run validate:schemas` | pass: 7 schemas, 6 manifests, 21 fixtures |
| `npm run smoke` | pass: 1/1 |
| `npm run test:adversarial` | pass: 8/8 |
| `npm run test:recovery` | pass: persistence 6/6 and artifacts 6/6 |
| all Node tests | pass: 51/51 |
| `npm audit --audit-level=high` | pass: 0 vulnerabilities |
| syntax and `git diff --check` | pass |

No subagents or external runtime adapters were used. No experiment harness applies to this product SWU. This browser proof does not promote L1+ effects or claim cryptographic tamper evidence.
