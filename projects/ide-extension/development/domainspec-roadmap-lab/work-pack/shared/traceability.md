# Traceability

| Accepted outcome | Design handle | Slice | SWUs | Exit evidence |
| --- | --- | --- | --- | --- |
| Newcomer sees correct boundary and learns FPR-01 | RDL-C01, UX moments 1–2 | S-002 | 003–006 | deterministic packet and focused browser witness |
| Newcomer restates and inspects source trail | RDL-O02, UX moments 3–4 | S-002/S-003 | 005–008 | stored restatement/source event and representative coverage |
| Proposal is durable and bound to what was seen | RDL-CN04/05/07 | S-001/S-002 | 002, 004–006 | exact stored event with dual binding/original value |
| Revisions and restart do not silently retarget proposals | proposal state machine | S-003 | 007–008 | restart, republish, stale-review evidence |
| Proposal reaches correct owner without direct effects | RDL-C05, RDL-O03 | S-004 | 009–011 | class packets, unsupported denial, receipt-reference checks |
| Victor finds the lab understandable/useful | UX comprehension gate | S-005 | 013 | real 30-minute trial report and actionable proposal |
| One accepted copy improvement closes with proof | RDL-O04 | S-005 | 012 | acceptance, diff, tests, fingerprint, revision, before/after |
| Claim remains bounded to local pilot | layering L3 | S-005 | 014 | no-overclaim closeout and retained gaps |

Every accepted outcome has at least one machine or human validation surface and
a named evidence owner. No row treats proposal submission as application.

## Execution Evidence

- `SWU-RDL-001`: [PASS](../../task-sessions/20260714T215441Z-swu-rdl-001/TASK-SESSION-RESULT.md) —
  presentation-only copy oracle, dynamic manifest target checks, six negative
  fixture reasons, and unchanged brownfield inputs.
- `SWU-RDL-002`: [PASS](../../task-sessions/20260714T215923Z-swu-rdl-002/TASK-SESSION-RESULT.md) —
  private semantic-event oracle, five event names, five proposal classes,
  parent-owned Canvas bindings, size/canvas-composition checks, and no IDE
  runtime registration.
- `SWU-RDL-003`: [PASS](../../task-sessions/20260714T221718Z-swu-rdl-003/TASK-SESSION-RESULT.md) —
  generated roadmap copy now comes from a validated 67-field presentation-only
  data file, coverage failures are builder errors, and migrated template
  fallbacks are gone.
- `SWU-RDL-004`: [PASS](../../task-sessions/20260714T222610Z-swu-rdl-004/TASK-SESSION-RESULT.md) —
  generated roadmap identity now includes `roadmap-build-inputs.v1`, relative
  input digests, rendered target selectors, FPR-01 copy fields, mutation proof,
  and deterministic regenerated outputs.
- `SWU-RDL-005`: [PASS](../../task-sessions/20260714T223345Z-swu-rdl-005/TASK-SESSION-RESULT.md) —
  FPR-01 guided surface now produces exact orientation, restatement, source
  request, and improvement proposal messages without direct mutation or false
  storage/application claims.
- `SWU-RDL-006`: [BLOCK](../../task-sessions/20260714T224609Z-swu-rdl-006/TASK-SESSION-RESULT.md) —
  real Canvas route/poll proof is blocked by dirty shared IDE runtime hunks;
  no later history, handoff, roundtrip, or human-trial claim may advance past
  this point until the owner decision is resolved.
