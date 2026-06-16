# TASK-W1-FRIEND-FLOW

## Objective

Implement the friend-facing Strava flow, activity submission, and preview
controller state according to W0 contracts.

## Layer And Slice

- Layer: L1.
- Slice: S-002.
- Wave: W1.

## Source Contracts

- `../../interfaces.md`
- `../../operations.md`
- `../../queries.md`
- `../../mappings.md`
- `../../ui-spec.md`
- `../../TEST-SPEC.md`

## Dependencies

- SWU-BWPT-007.
- Hosted storage contract is available from W0.

## Smallest Working Units

| SWU | Goal | Write Scope | Done Criteria | Validation |
| --- | --- | --- | --- | --- |
| SWU-BWPT-008 | Implement auth/activity/submission/controller flow. | `projects/body-war/app/` | Friend can connect, see activity, submit to track, and see preview controller update in pre-host or hosted dev mode. | Smoke checks from `TEST-SPEC.md`. |

## Implementation Detail

Input:

- Strava OAuth callback.
- Redacted activity summaries.
- Selected `PilotTrack`.

Output:

- `EvidenceSubmission` in `preview-accepted` state.
- Updated `PreviewControllerState`.

Rules:

1. Reject submission without connected friend session.
2. Accept only visible run-like activity summaries.
3. Require a preview-visible Parque track.
4. Store token references, not tokens, in app-visible data.
5. Update controller read model from preview-accepted evidence only.

## Blockers

Blocked until W0 and scaffold pass.

