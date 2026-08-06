# Stage 07 Design Attacks

Exactly three confirmed, read-only critics reviewed the initial design. Their
normalized native returns are preserved verbatim in `critic-receipts/`.

## API contract critic

Receipt: `critic-receipts/api-contract-critic.json` — `fail`.

- Row routes lacked explicit actions, resource identities, authorization order,
  and concealed-denial behavior.
- Space and row cursors did not fully bind principal/policy/snapshot/route state.
- Space-ID input bytes were ambiguous.
- Manifest, record, YAML, time, response, and concurrency ceilings were absent.
- Error precedence, duplicate behavior, snapshot preconditions, and freshness
  validity were ambiguous.

## Craft authority critic

Receipt: `critic-receipts/craft-authority-critic.json` — `fail`.

- Unkeyed path-derived IDs allowed offline guessing of private source paths.
- List/read metadata exposed exact content digests and sizes without a separate
  provenance authorization.
- Freshness incorrectly blurred the manifest digest with each entry's source
  digest.
- `409 capability_unavailable` and `422 unsupported_schema` overlapped.

## WaveDB runtime critic

Receipt: `critic-receipts/wavedb-runtime-critic.json` — `fail`.

- The passing witness demonstrated same-process reopen, not a separately
  launched reader or production durability.
- Expected-key closure did not prove absence of extra physical keys.
- Writer-less interfaces provided logical, not OS-enforced, immutability.
- Locking, concurrent opens, replacement, crash recovery, and post-start
  corruption were unproven.
- String/Buffer normalization and the npm/Node pairing had a narrower evidence
  envelope than the initial wording implied.

## What survived

All critics agreed that source ledgers remain authoritative; the WaveDB snapshot
and API remain derived; partial expected-record serving stays forbidden; raw
bytes can remain L0; rows remain conditional L1; the failed atomic-batch path is
not positive evidence; refresh, mutation, deployment, and publication stay out
of scope.
