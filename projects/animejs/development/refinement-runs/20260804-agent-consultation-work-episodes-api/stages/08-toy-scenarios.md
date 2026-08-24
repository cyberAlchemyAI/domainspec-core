# Stage 08 — Planned Toy Scenarios

Evidence state for every row: `planned_not_executed`.

| ID | Scenario | Required observation |
| --- | --- | --- |
| TS-01 | bounded consultation success | admissible source-linked records within result, hop, and byte caps |
| TS-02 | ambiguous consultation | typed abstention and no guessed choice |
| TS-03 | stale expected projection digest | `stale`, no partial records |
| TS-04 | denied consultation | opaque denial and no private existence leak |
| TS-05 | projection field leak | forbidden owner/path/policy/prompt-role field blocks projection |
| TS-06 | instruction-shaped record | returned as inert data or rejected; never changes capability behavior |
| TS-07 | append body under read token | denied before target parsing; journal delta zero |
| TS-08 | foreign-principal episode probe | opaque denial without revision, digest, or existence disclosure |
| TS-09 | identical idempotent retry | original receipt replayed; exactly one event |
| TS-10 | same key, different body | `IDEMPOTENCY_MISMATCH`; event delta zero |
| TS-11 | two stale writers | exactly one accepted compare-and-append |
| TS-12 | crash before commit | recovery says `not_committed`; retry may append once |
| TS-13 | crash after commit before receipt | scoped recovery returns original committed receipt |
| TS-14 | raw path/URL or forged evidence | evidence rejected; event delta zero |
| TS-15 | cross-attempt evidence rebind | rejected against immutable producer/target bindings |
| TS-16 | revoked evidence after outcome | history unchanged; derived success eligibility becomes `unconfirmed` |
| TS-17 | duplicate outcome | closed diagnostic; event delta zero |
| TS-18 | close with dangling attempt | `DANGLING_ATTEMPT`; episode remains open |
| TS-19 | post-close ordinary command | `EPISODE_TERMINAL`; event delta zero |
| TS-20 | reopen attempt | `REOPEN_FORBIDDEN`; new superseding episode required |
| TS-21 | supersession cycle | `SUPERSESSION_CYCLE`; no episode opened |
| TS-22 | journal gap | quarantine affected episode; do not synthesize missing event |
| TS-23 | journal fork | quarantine affected episode; do not select a winning branch |
| TS-24 | shuffled journal order | `JOURNAL_ORDER_INVALID`; no auto-sort |
| TS-25 | event digest mismatch | `EVENT_DIGEST_MISMATCH`; no snapshot emitted |
| TS-26 | reducer-version drift | old snapshot retained; new keyed snapshot plus migration receipt |
| TS-27 | projection pending | accepted append receipt is stable; read reports `pending` |
| TS-28 | projection corrupt | affected episode quarantined; unaffected records remain readable |
| TS-29 | episode closure | zero verified Lesson records and relations |
| TS-30 | semantic closure | receipt says effect none; Task state and truth status unchanged |

These scenarios are design contracts for later executable fixtures. Their
presence proves coverage intent, not runtime behavior.

