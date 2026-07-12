# SWU-IDEAD-008 Evidence

```yaml
swu_id: SWU-IDEAD-008
result: pass
capability_ref: task-session
receipt_kind: local-fallback
receipt_artifact: projects/ide-extension/development/l0-human-approval-desk-plan/work-pack/evidence/SWU-IDEAD-008.md
files_touched:
  - src/server.mjs
  - public/demo/l0.html
  - tests/l0-smoke.test.mjs
  - tests/l0-workbench-ui.test.mjs
  - package.json
validation:
  - npm run test:workbench
  - npm run smoke
  - node --test --test-concurrency=1 tests/*.test.mjs
  - npm run validate:schemas
  - npm audit --audit-level=high
  - git diff --check
blockers: []
residue:
  - The checked-in .ide-extension/state event history predates event_version 1 and fails closed; use an isolated IDE_EXTENSION_STATE_DIR until migration is separately governed.
reroute: SWU-IDEAD-009
handoff_note: The Approval Desk exposes stable queue, detail, disposition, history, receipt, and evidence selectors; Playwright should use a temporary state directory.
```

## Browser Contract

The first screen is the working Approval Desk. It provides:

- pending and history tabs with selectable proposal buttons;
- complete selected envelope, approval, grants, context, actor, timestamp, and rejection details;
- guarded approve and reject commands for pending proposals only;
- terminal proposal inspection with disabled disposition controls;
- receipt-level Before, After, and Receipt evidence controls;
- visible connection, announcement, and persistent error states;
- responsive three-pane, two-pane, and single-column layouts;
- keyboard-native semantic controls and visible focus styling;
- dynamic server values rendered only with `textContent` and DOM creation APIs.

The UI says `local operator action` and `unattested assurance`. It never claims a verified human identity.

## Bounded Read API

- `GET /api/proposals/:envelopeId` returns one authoritative envelope, approval, and UI-safe receipt projection.
- `GET /api/receipts/:receiptId/evidence/:kind` accepts only committed receipt IDs and the closed `before|after|receipt` vocabulary.
- Receipt projections replace physical before/after paths with bounded API links.
- Missing or invalid evidence returns `404 evidence_unavailable` without exposing a filesystem path.
- `IDE_EXTENSION_STATE_DIR` selects an explicit state root for normal CLI startup and isolated browser runs.

## Stable Selectors

| Purpose | Selector |
| --- | --- |
| Prepare task | `[data-field="task-input"]` |
| Prepare command | `[data-action="prepare"]` |
| Pending/history tabs | `[data-view="pending"]`, `[data-view="history"]` |
| Proposal item | `[data-proposal-id]` |
| Detail panel | `[data-panel="detail"]` |
| Grant list | `[data-list="grants"]` |
| Reject reason | `[data-field="reject-reason"]` |
| Approve/reject | `[data-action="approve"]`, `[data-action="reject"]` |
| Receipt list | `[data-list="receipts"]` |
| Evidence controls | `[data-evidence-kind="before|after|receipt"]` |
| Evidence viewer | `[data-viewer="evidence"]` |
| Error state | `#error-strip[role="alert"]` |
| Status announcement | `#announcement[role="status"]` |

## Playwright Flow

1. Start the server with a temporary `IDE_EXTENSION_STATE_DIR`.
2. Prepare proposal A, change the task, and prepare proposal B.
3. Select A by `[data-proposal-id]`; approve and accept the confirmation.
4. Select B; enter a reason, reject, and accept the confirmation.
5. Open History and verify both terminal states remain selectable with disabled actions.
6. Select A and open Before, After, and Receipt evidence controls.
7. Reload and confirm the event-derived history and evidence remain reachable.
8. Repeat layout and keyboard checks at desktop and mobile viewports.

## Validation Results

| Command | Result |
| --- | --- |
| `npm run test:workbench` | pass: 3/3 UI/API contract cases |
| `npm run smoke` | pass: 1/1 including bounded detail and after-evidence reads |
| all Node tests | pass: 51/51 |
| `npm run validate:schemas` | pass: 7 schemas, 6 manifests, 21 fixtures |
| `npm audit --audit-level=high` | pass: 0 vulnerabilities |
| syntax, forbidden-string, and `git diff --check` checks | pass |

No subagents or external runtime adapters were used. No experiment harness applies to this product SWU. Real browser screenshots and viewport evidence remain owned by SWU-IDEAD-009.
