# TASK-WHISPER-RSCH-STATE-001

## Identity

- task id: `TASK-WHISPER-RSCH-STATE-001`
- SWU id: `SWU-WHISPER-RSCH-STATE-001`
- owner: `task-session`
- effect: repository-local reversible candidate research
- authority effect: `none`

## Behavior

Materialize the exact Design oracle as a closed schema, positive EV01-EV26 sequence, named negative matrix, pure Node reducer/replay checker, revision-3 synthesis, and deterministic validation receipt.

## Inputs

- `SPEC.md`
- `ARCHITECTURE.md`
- `VALIDATION-CONTRACTS.json`
- `../../synthesis-revision-2.md`
- `../../review-final.md`

## Writes

Exactly the six material paths listed in `WORK-PACK.md`, plus Task Session evidence under `development/state-contract-repair/execution/`.

## Done

1. every event has one prior/result tuple and revision advances exactly once;
2. every state uses declared enum values;
3. EV22 passes only under all exact bindings;
4. every declared negative rejects without state advance;
5. canonical live/replay RS26 bytes and digests match;
6. RP26 derivation leaves RS26/event count/revision unchanged;
7. all validation commands pass twice with an identical deterministic result;
8. terminal receipt records exact files, commands, boundaries, and remaining research-closeout cursor.

## Stop

Stop on any unexpected pre-existing target, stale source digest, failed acceptance check, undeclared write, required network/credential, public/private crossing, or authority/promotion/deployment effect.
