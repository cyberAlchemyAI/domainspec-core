# Validation Strategy

Status: planned and unexecuted.

## Evidence Layers

| Layer | Question | Evidence | Claim ceiling |
| --- | --- | --- | --- |
| L0 smoke/continuity | Does the shell load, version correctly, and remain stable? | schema, console/network, navigation and patch counters | current fixture behavior |
| L1 accessibility | Are exact semantics, names, focus, live regions, contrast, and targets correct? | role/name/state, ARIA snapshot, keyboard, computed styles, boxes | bounded named checks |
| L2 layout | Does the active task remain inspectable at both viewports? | overflow, ordering, bounding boxes, screenshots | required fixtures only |
| L3 interaction | Can the governed path complete without context loss or gate weakening? | user-facing locators, action receipts, state/version assertions | tested workflow |
| L4 cognition proxy | Is hierarchy/salience structurally plausible? | screenshot review and deterministic DOM measures | soft flag only |
| L5 domain practice | Are current/staged/history and action copy faithful? | contract review and state matrix | domain consistency |
| L6 human evidence | Do people orient, resume, understand, and feel in control? | separately owned study | human-study outcomes only |

## Required Commands

From `projects/ui-prototyping-studio/backend`:

```bash
./node_modules/.bin/tsc -p tsconfig.json --noEmit
./node_modules/.bin/tsx --test "src/**/*.test.ts"
./node_modules/.bin/playwright test --reporter=list
```

The selected Task Session may run focused specs first, but closeout must run the
full current suite. Corepack/pnpm is not an acceptance dependency.

## Positive And Negative Calibration

- Every live-region scope has a positive event fixture and an unrelated-event
  negative fixture.
- Contrast uses computed foreground/background compositing, not token names.
- Target size measures actual bounding boxes and records any claimed exception.
- Versioning includes a nullable-coercion mutant and duplicated-response mutant.
- Projection coherence includes an interleaved external-writer fixture,
  canonical golden vectors, and changed-object/unchanged-digest mutants.
- Refresh coordination includes a deferred old-poll/action/new-state fixture
  and exact trailing-refresh accounting.
- Region recovery injects a renderer failure after an earlier region has
  prepared or committed and proves full rollback.
- Copy includes a state/action/secondary-CLI disclosure matrix.
- Keyboard/focus and no-color-only behavior have bounded positive and negative
  fixtures; recoverable and separately approved blocking errors use different
  live-region expectations.
- Security includes outer-shell markup injection, sandbox-removal, and
  disallowed-route mutants.
- Governance includes missing/stale acknowledgment and browser-Export negatives.
- Continuity includes current-head-preserving and current-head-changing cases.

## Browser Evidence

Required viewports:

- 1440×900;
- 390×844.

Initial implementation evidence may remain Chromium-only if it says so.
Cross-browser generalization requires a separate explicitly owned route.

## Residue Rules

- A screenshot cannot promote a hard gate by itself.
- Axe or ARIA checks do not establish accessibility completeness.
- Stable automation does not establish comprehension, trust, workload, or delight.
- Passing implementation commands does not authorize release.
- Human-test script updates occur after behavior passes, not before.
