# Continuous Construction Examples

The generated examples exercise the four decision values through the candidate
CLI:

| Attempt | Expected decision |
| --- | --- |
| `attempts/continue.json` | `CONTINUE` |
| `attempts/continue-with-owner-gate.json` | `CONTINUE` |
| `attempts/stop.json` | `STOP` |
| `attempts/ready-for-human-test.json` | `READY_FOR_HUMAN_TEST` |
| `attempts/request-terminal-confirmation.json` | `REQUEST_TERMINAL_CONFIRMATION` |

The ready and terminal attempts reference the same frozen human-test packet;
only the terminal attempt additionally references an immutable passing
observation bound to that packet's exact ref and digest. `authorizations/`,
`artifacts/`, and `observations/` provide the exact repository-local evidence
consumed by the evaluator. `mutations/` covers predecessor, authorization,
artifact, owner-gate, packet-basis, packet-completeness, observation-binding,
and routine-confirmation attacks. Rebuild the deterministic fixtures with
`scripts/build-examples.ts`.

These are behavior fixtures, not owner decisions or authorized work attempts.
