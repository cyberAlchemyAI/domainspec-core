# Anime.js Agent Knowledge API

This directory contains the candidate-local, transport-neutral core for agents
to consult the neutral Anime.js knowledge projection and record immutable work
episodes. It is a local library and validation surface, not a public server or
production deployment.

## Capabilities

| Exact audience | Operation boundary | Durable effect |
| --- | --- | --- |
| `animejs-knowledge-consult-read` | bounded neutral-projection queries | none |
| `animejs-work-episode-append` | five closed episode commands | append at most one validated event |
| `animejs-work-episode-receipt-read` | scoped ambiguous-commit recovery | none |
| `animejs-work-episode-project-read` | reducer/projection status reads | none |

The audiences are non-substitutable. Authorization happens before request-body
target parsing. Host identity, workspace, policy, vault scope, request identity,
Task snapshots, VersionContext snapshots, and Evidence bindings are injected by
host ports and cannot be asserted by an agent body.

## Library surfaces

- `src/consultation-service.mjs` performs bounded reads and returns
  `ok`, `abstain`, `stale`, `denied`, `invalid_request`, or
  `temporary_failure`.
- `src/episode-service.mjs` resolves host handles, invokes the pure transition
  oracle, and appends through the atomic journal.
- `src/journal.mjs` owns digest-chained events, scoped idempotency, optimistic
  concurrency, and receipt recovery. Its included store is an in-memory
  contract implementation, not a production database.
- `src/reducer.mjs` validates and replays exact journal order into
  version-keyed immutable snapshots.
- `src/overlay.mjs` and `src/projection.mjs` emit only isolated episode records
  and allowlisted neutral records. They do not write the canonical vault.
- `src/capability-adapters.mjs` binds the four exact host audiences to their
  named service ports.

Consumers instantiate these modules with their own authorization, persistence,
resolver, projection-reader, scheduler, audit, clock, and identity ports. No
module fetches remote URLs, executes record text, reads arbitrary filesystem
paths, or changes Task state.

## Validation

Run the complete deterministic acceptance surface from the repository root:

```sh
node projects/animejs/ontology/agent-knowledge-vault/operational/scripts/validate.mjs --verify-repeat
```

The validator parses all contract and fixture JSON, checks cross-contract
algebras, runs every suite twice in fixed order, maps TS-01 through TS-30 to a
passing suite, and proves byte-zero delta across the existing `nodes/`,
`relations/`, `sources/`, and `views/` directories. Its deterministic receipt
is written to `receipts/validation-receipt.json` only after validation passes.

Every append and read result declares:

```json
{
  "semantic_effect": "none",
  "task_state_unchanged": true,
  "truth_status": "not_assessed"
}
```

## Evidence ceiling and exclusions

The evidence proves a candidate-local L0-L2 transport-neutral core against the
declared fixtures. It does not prove HTTP behavior, durable production storage,
consumer integration, TLS, retention, deployment, promotion, publication,
release, or production readiness. Closing an episode creates no verified
Lesson, canonical node, canonical relation, authority effect, or Task-state
transition. Evidence revocation changes only derived eligibility; it never
rewrites event history.
