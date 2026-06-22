# Agent Process Lifecycle

Status: frozen for MVP implementation

## Lifecycle

1. Start one local process for each occupied seat.
2. Send one line-delimited JSON decision envelope to the acting process stdin.
3. Flush stdin and start a monotonic deadline timer.
4. Accept only the first complete stdout JSON line before the deadline.
5. Classify invalid, timeout, crash, or EOF outcomes as diagnostic events.
6. Apply deterministic legal fallback when no valid action is accepted.
7. Terminate a timed-out, crashed, or EOF process before the next decision for
   that seat; a later process restart is allowed inside the same match.

## Captured Streams

- stdout is gameplay-candidate material.
- stderr is diagnostic material only.
- stderr JSON never affects gameplay legality.

## Timeout

Default `decision_timeout_ms` is `5000`. The timer starts after the decision
envelope is flushed to stdin and stops at the first complete stdout JSON line.
The runner may terminate a timed-out process immediately after classification,
but no late output can be accepted.
