# SWU-IRO-002 strict context

- Stream: `IRO-FULL-STREAM`
- Epoch label: `20260802T021738Z`
- Frozen epoch ID: `epoch-a696eda26311d39018e7ac8f`
- Task: `TASK-IRO-CANDIDATE-001`
- Unit: `SWU-IRO-002`
- Capability allowlist: `task-session`, `sigil-development`
- Lifecycle owner: `candidate-lifecycle-owner`
- Authorization: the direct owner instruction `just implement, our authorization gate is only at merge` authorizes local candidate material under the exact scope below. It does not authorize merge, push, canonical publication, release, deployment, or production claims.

## Exact material scope

`ops/development/2026-08-01-intent-route-arcanum-addon/candidate-sigil/**`

The material package must bind a staged closure inventory containing every
candidate file and digest. No `arcanum/**`, generated runtime mirror, consumer,
or private runtime mutation is admitted by this unit.

## Required result

Author a fresh, project-neutral, public-safe contract closure containing the
sigil contract, schemas, zero-authority add-on manifest, synthetic fixtures,
JSON entrypoint contract, public-boundary scan mechanics, experiment profile,
and a source/license/API receipt. The accepted behavior may be compared with a
bounded existing interface, but no source code or private prose may be copied.

## Validation

1. Parse and validate every candidate schema and manifest binding.
2. Scan candidate bytes and imports for private identifiers, path escapes,
   network imports, ambient authority, and non-project-neutral dependencies.
3. Verify the PolyForm Noncommercial 1.0.0 license, Required Notice, fresh-source
   declaration, protocol IDs, and zero-authority API receipt.
4. Run the scoped whitespace/diff check.

## Evidence ceiling and successor

A pass proves only a sanitized candidate contract closure. It does not prove
resolver behavior, portability, canonical acceptance, generated-package parity,
consumer admission, release, deployment, or production readiness. Project
exactly `SWU-IRO-003` after joined closeout.
