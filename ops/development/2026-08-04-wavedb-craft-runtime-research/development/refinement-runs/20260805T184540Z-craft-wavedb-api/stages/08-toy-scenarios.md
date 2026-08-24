# Stage 08 — Required Toy and Negative Scenarios

These are planned executable witnesses, not test results.

| Area | Positive boundary | Negative/counter-example boundary |
| --- | --- | --- |
| Space ID | Fixed key + manifest/path bytes match a published vector. | Guessed paths cannot be confirmed without key; collision/key rotation invalidates snapshot/cursors. |
| Authorization | Authorized row list/read succeeds for the exact family/resource. | Denied and absent resources are indistinguishable before schema, family, count, or lookup observation. |
| Metadata | List-only caller sees base fields. | Digest, exact size, and path never appear without their distinct permission. |
| Space cursor | One policy/snapshot traversal has no skip/duplicate. | Principal, policy, visible set, snapshot, limit, expiry, or signature change yields one concealed invalidation. |
| Row cursor | Same family/index traversal resumes in canonical order. | Cross-family/space/adapter replay and tamper fail. |
| Errors | Each route follows the fixed decision order. | Every competing-error pair, especially unauthorized plus malformed family/schema, discloses nothing extra. |
| Snapshot pin | Exact `X-Craft-Snapshot-Match` succeeds; ETag can yield 304. | Snapshot mismatch yields 412 only after target authorization; ETag mismatch yields a normal representation. |
| Freshness | Complete authorized observation compares each source digest with its own manifest entry. | Partial, expired, wrong-snapshot, extra-path, or unauthorized observation yields unknown. |
| Manifest limits | Exact-at-limit manifest/entry/byte set closes. | One-over-limit fails the whole snapshot without partial serve. |
| YAML limits | Bounded, alias-free valid YAML enables an adapter candidate. | Alias, custom tag, depth, node, size, or time breach disables rows/fails closed. |
| Normalization | Empty, large, and multibyte lossless UTF-8 string and Buffer values hash identically. | Null, unsupported type, malformed/non-string-origin value fails closed. |
| Expected closure | All manifest-derived keys exist and match. | Missing/mismatched key invalidates snapshot; extra physical key is unreachable from any route. |
| Runtime corruption | Repeated verified reads remain stable. | Post-open truncation, bit flip, missing value, or WaveDB exception invalidates the entire handle and all data routes return 503. |
| Process lifecycle | Separately launched reader verifies the closed store under the pinned pairing. | Builder/service overlap, lock contention, crash interruption, or multi-process ambiguity blocks admission. |
| HTTP read-only | GET/HEAD work within concurrency and response limits. | POST/PUT/PATCH/DELETE, request body, range, or ninth concurrent raw response cannot reach a writer or partial response. |

Legacy adapters require separate fixtures for `0.3.0`, `0.2.0`, and the requested
but still unproven `0.1`. Duplicate family identity must disable all rows for the
space and expose only `capability_unavailable`.
