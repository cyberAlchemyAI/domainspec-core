# Invoke Refresh: Fresh `-03` Staged-Filter Repair

- Mode: `refresh`
- Mutation mode: `apply-approved`
- Result: `pass`
- Activation source: direct user authorization `CAPI-AUTH-SWU-CAPI-000-03-STAGED-FILTER`
- Scope: exactly `WORK-PACK.md` and `work-pack/tasks/TASK-RUNTIME.md`

The refresh admitted one fresh immutable attempt,
`wcli-20260805-node26-0.15.9-03`. Its builder contract may differ from the
immutable `-02` builder only by the attempt identity and by adding literal
`staged` to the directory-exclusion set. The selected snapshot contract remains
28 ledgers and 57 records. The failed `-01` and `-02` attempts remain unchanged.
No successor, API implementation, canonical Craft-source mutation, network
integration, publication, or deployment was authorized.

The material package passed schema, dependency, owner, publication-boundary,
and handoff validation with canonical package digest
`89248579083220a9c21faeaf8b6f4b0fbd55166560c3b8f66b21caf429bed0da`.
The applied target hashes were:

- `WORK-PACK.md`: `c3f5469818acccab319d82efa6d2de9f1b7d6935405203bad297622c733e5ea7`
- `TASK-RUNTIME.md`: `9fd826b1086b9647e665438d16e70662a3da3107d755740505e1f44937543cc6`

This report records planning mutation only. It is not runtime admission,
snapshot acceptance, or API readiness evidence.
