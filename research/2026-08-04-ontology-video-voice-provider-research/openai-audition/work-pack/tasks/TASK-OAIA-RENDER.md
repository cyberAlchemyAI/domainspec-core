# TASK-OAIA-RENDER — Bounded provider effect

## Objective

For one explicitly admitted candidate, produce exactly two immutable raw WAV attempts with identical request bytes, safe metadata, and no credential persistence or silent retry.

## Mapping

- Slice: S-RENDER
- Layer: L1
- Wave: W2
- Sources: `../../DESIGN.md#view-4--operation-and-flow`, `../../IMPLEMENTATION-DETAILS.md#render-algorithm`, `../../INTERFACES.md`
- Dependencies: SWU-OAIA-002 and closure of B-001 through B-005.
- Current gate: blocked.

## SWU-OAIA-003 — One explicit speech request

- Primary behavior: execute one bounded external request for an exact admitted manifest.
- Independent boundary: injected fake transport proves request/auth/error behavior; one separately authorized live attempt proves the configured provider route.
- Split analysis: credential read, HTTPS request, and bounded response are inseparable parts of the one external effect.
- Write scope: `runtime/lib/openai-speech-transport.mjs`; `runtime/test/render.test.mjs`; one unique run-scoped live attempt/diagnostic path.
- Done criteria: fixed origin/path; no redirects/SSE; credential read only inside request; no credential persistence; no automatic retry; response/status/IDs redacted safely; provider docs refreshed immediately before live use.
- Acceptance evidence: fake success/failure/ambiguous fixtures and one explicit live receipt only when separately authorized.
- Validation: `node --test runtime/test/render.test.mjs`; manual review of admitted digest, outbound allowlist, and live receipt.
- Execution owner: manual.
- Handoff: exact manifest and separate authorization are mandatory; never infer permission from this Plan.

## SWU-OAIA-004 — Two immutable attempts

- Primary behavior: bind exactly two repetition attempts to one admitted request digest without overwrite.
- Independent boundary: local fake byte streams prove crash/no-clobber/join behavior without another provider request.
- Split analysis: attempt storage and two-attempt completion jointly answer the repeatability claim.
- Dependencies: SWU-OAIA-003.
- Write scope: `runtime/lib/attempt-store.mjs`; `runtime/test/attempt-store.test.mjs`; two unique run-scoped attempt paths.
- Done criteria: per-manifest lock; UUID paths; exclusive create; close-before-hash; raw immutability; separate derivative namespace; identical request digest; success event only after both validate.
- Acceptance evidence: no-overwrite, crash-before-bind, mismatched-request, duplicate-ID, and two-valid-attempt fixtures plus actual hashes if live.
- Validation: `node --test runtime/test/attempt-store.test.mjs`; receipt/hash review.
- Execution owner: local-fallback for code, manual for provider repetitions.
- Handoff: preserve every raw/ambiguous artifact; do not delete, replace, or retry without a new explicit attempt.

## Synchronization and completion

003 closes before 004. W2 exits only with two valid attempts and their same request digest, or a bounded stop/rejection receipt. It cannot open W3 until B-006 closes and the verification owner accepts the raw evidence.
