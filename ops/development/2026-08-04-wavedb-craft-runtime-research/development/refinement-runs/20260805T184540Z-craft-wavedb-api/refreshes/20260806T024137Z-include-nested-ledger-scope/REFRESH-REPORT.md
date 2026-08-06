# Invoke Refresh: Include Nested Craft Ledger

- Mode: `refresh`
- Mutation mode: `apply-approved`
- Result: `pass`
- Activation source: direct user decision `CAPI-SCOPE-INCLUDE-28`
- Scope: exactly `WORK-PACK.md` and `work-pack/tasks/TASK-RUNTIME.md`

The refresh changed the snapshot contract from 27 ledgers/55 records to the
owner-selected 28 ledgers/57 records and admitted only immutable attempt
`wcli-20260805-node26-0.15.9-02`. The failed `-01` attempt remained
unchanged. No successor, API implementation, canonical Craft-source mutation,
publication, or deployment was authorized.

The material package passed schema, dependency, owner, publication-boundary,
and handoff validation with canonical package digest
`942fe12cf91ea15a84e829790458765f57bee1b3a49343c7a85020461fc6313f`.
The applied target hashes were:

- `WORK-PACK.md`: `5d5b236923b1cdb12c70ccb6c77086ca4e8b766023dec287de13f90811a945c9`
- `TASK-RUNTIME.md`: `1087301916e2fd77dc94fa46fab68c59b4d30ba8c419e802a9432aa7938321e7`

This report records planning mutation only. It is not snapshot acceptance or API
readiness evidence.
