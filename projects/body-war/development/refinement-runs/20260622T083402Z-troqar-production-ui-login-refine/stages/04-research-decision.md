# Stage 04 - Research Decision

Status: pass
Capability handle: `refine`
Mode: `research-if-gap-appears`
Receipt kind: parent-native-stage-artifact

## Decision

Use local repository evidence only for this pass. External research is not
required yet.

## Rationale

- The product direction, current UI, Studio handoff, test runner, and visual
  definitions are all local.
- The immediate decision is not "what do modern login pages look like" but
  "which production route fits this app and current codebase."
- If implementation later needs package-specific API details, that should be a
  bounded research step in the Task Session or a follow-up refine.

## Trigger For Future Bounded Research

Ask before external research if any of these become blockers:

- selecting a component package or icon integration path;
- Strava OAuth UX compliance beyond local fake flow;
- accessibility pattern uncertainty not covered by Playwright/local evidence.
