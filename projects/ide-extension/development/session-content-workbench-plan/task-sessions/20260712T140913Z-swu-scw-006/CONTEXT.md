# Context Pack: SWU-SCW-006

## Selection

- Task/SWU: `TASK-INTERACTION-RETURN / SWU-SCW-006`
- Mode: standard, local Task Session
- Dependency: SWU-SCW-005 PASS

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Accept only fixed-type messages from the current iframe window. | Task algorithm steps 1 and 2. | covered |
| O2 | Enforce bounded generic interaction input and 16 KiB HTTP request cap. | Existing schema and SPEC contract. | covered |
| O3 | Bind admission to current surface/revision and commit one event. | Task algorithm step 3. | covered |
| O4 | Expose sending, sent, failed, and explicit retry browser states. | Task algorithm step 4. | covered |
| O5 | Return ordered, non-destructive cursor polls including empty polls. | Task algorithm steps 5 and 7. | covered |
| O6 | Add exact one-shot CLI polling and preserve all prior commands. | Task algorithm step 6. | covered |
| O7 | Prove stale/invalid/oversized/append failure/restart behavior. | SWU edge cases and validation. | covered |

## Execution Decisions

- Use `ide-extension.canvas.event` as the fixed postMessage type and map
  `eventName` to the server's canonical `event_name` field.
- Preserve the existing schema; enforce exact serialized request bytes in the
  server body reader before JSON parsing.
- Assign event id, receive time, and cursor inside the serialized mutation
  queue after checking projected current bindings.
- Keep polling non-destructive; the same `after` cursor returns the same stable
  event ids, while a cursor beyond the end returns an empty successful poll.

## Gates

- Dependency/context/write scope/validation: pass.
- Blocker decisions: none.
- Strict coverage: pass, seven of seven obligations.

## Required Evidence

- API/projector tests cover bindings, cursor order, limits, append failure, and restart.
- CLI emits the exact API poll response and rejects invalid cursor input.
- Browser tests prove source filtering, generic postMessage forwarding, status,
  retry, and no regressions in existing Canvas/Approval Desk flows.
