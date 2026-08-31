# W0 Compatibility Decision

Date: 2026-08-26

Result: `pass-for-isolated-candidate-authoring`

## Selected encoding

| State | Package schema | Mode | State token | Approval | Receipt |
| --- | --- | --- | --- | --- | --- |
| empty proposal | v1 or v2 | `proposal-only` | `proposal-only` | `none`, empty | `not-applicable + deferred` |
| exact staged candidate | v2 only | `proposal-only` | `staged` | `none`, empty | `candidate-pass + gated` |
| apply-authorized material | v1 or v2 | `apply-approved` | `materialized` | exact `explicit-apply` | `pass + ready` |

Add parallel v2 package and receipt schemas. Do not broaden the existing v1 schema
IDs or generic v1 filenames. Dispatch validation by the document's explicit
`schema_version`; unknown versions fail nonzero without fabricating a v1 receipt.

The v2 receipt schema admits only closed verdict/handoff pairs. A valid staged
candidate must bind its package digest, nonempty validated paths and validation
commands, passing dependency/owner/publication boundaries, and empty reasons. It can
never emit `ready`. A rejection must use `reject + blocked` with nonempty reasons.

## Why this fails closed

- Capability Status and both Task Session mutation gates require exact
  `pass + ready`; `candidate-pass + gated` cannot open them.
- The generic prerequisite classifier may inspect only `patchVerdict`; its accepted
  `pass` predicate does not match `candidate-pass`.
- Refresh stays in run-level `proposal-only` mode and must validate an explicitly
  supplied staged receipt while reporting `mutationReady=false`.
- No new run-level candidate mode is introduced into continuation, WPRA, precloseout,
  or owner-prerequisite vocabularies.

## Version and CLI boundary

- Historical v1 packages and receipts remain readable under v1 only.
- New staged candidates require v2.
- Preacceptance adds parallel v2 manifest and receipt schemas; v1 schemas and v1
  `rehearse` return codes remain unchanged.
- V2 `rehearse` returns the first normalized stage failure, records it in the
  receipt, uses `1` for a closure blocker without stage failure, `2` for pre-receipt
  input/schema/IO failure, `124` for timeout, and `128 + signal` for signals.
- A dependent v2 stage has `result=not_evaluable`, `exit_code=null`, and causal
  blocker stage IDs.

## Authority ceiling

This decision authorizes only construction and validation in the isolated candidate
clone. It grants no canonical apply, generated sync, Git/publication, external
effect, Body War admission, deployment, provider, privacy, geometry, or scoring
authority.
