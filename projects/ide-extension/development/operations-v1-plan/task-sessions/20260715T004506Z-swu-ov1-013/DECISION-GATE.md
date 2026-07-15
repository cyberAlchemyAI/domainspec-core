# Decision Gate: Operations V1 Workbench Usefulness

```yaml
decision_id: DEC-IDEEXT-OV1-VALUE-USEFULNESS
status: selected
blocking: false
scope: SWU-OV1-013
selected_option: 1
selected_at: 2026-07-15T01:05:47Z
source: user reply "1"
evidence: MACHINE-WITNESS-REPORT.md
```

## Decision

After reviewing the retained desktop/mobile workbench result, is the proven
agent-to-workbench workflow useful enough to proceed to the integrated
Operations V1 closeout?

## What The Machine Already Proved

- An agent can publish project HTML, derive it, replace it, append to it, and
  select it for display through one-shot JSON CLI commands.
- The workbench loads the final complete revision on desktop and mobile.
- A person can interact with controls inside the iframe and the generic event
  returns to the durable V4 projection.
- Restart recovers the same selected immutable content.

Machine correctness cannot answer whether this is a useful way for a person to
work. That product judgment belongs to the operator.

## Option 1: Useful Enough - Proceed To Integrated Audit

Record that the current create, operate, display, interact, and recover flow is
useful enough for the Operations V1 claim. This passes SWU-OV1-013 and unblocks
SWU-OV1-014. It does not approve deferred regions, remote control, providers,
or IDE embedding.

## Option 2: Useful With Required Changes

Record the concrete changes needed before closeout. SWU-OV1-013 stays blocked
while those bounded changes are implemented and the witness is reviewed again.
This is appropriate when the underlying flow has value but the retained
workbench is not yet usable enough.

## Option 3: Not Useful Enough

Reject the current value claim and route back to product/UX refinement. The
machine evidence remains valid engineering evidence, but Operations V1 does
not enter integrated closeout.

## Recommendation Boundary

Choose Option 1 only if the retained page demonstrates the intended experience:
ask an agent for HTML, see the complete result in the local workbench, interact
with it, and keep the result across restart. The machine run cannot recommend a
human usefulness verdict on the operator's behalf.

## Selection

The user selected Option 1. The retained create, operate, display, interact,
and recover workflow is useful enough for the bounded Operations V1 claim.
This selection does not approve deferred regions, remote control, provider
execution, protected effects, or IDE embedding.

## Decision Gate Result

- Result: PASS
- Decisions resolved: 1
- Blockers remaining: 0
- Selected option: Useful enough - proceed to integrated audit
- Resume evidence: `../20260715T010547Z-swu-ov1-013-resume/TASK-SESSION-RESULT.md`
- Next step: run `SWU-OV1-014`
