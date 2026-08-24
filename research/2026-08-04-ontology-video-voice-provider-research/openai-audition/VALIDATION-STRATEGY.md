# Validation Strategy

## Static and deterministic checks

| ID | Scope | Check |
|---|---|---|
| V-001 | Authored package | JSON parse, Markdown-link targets, no placeholder tokens, no checkout-escaping paths. |
| V-002 | Frozen excerpt | SHA-256 `51d149...5cee`, 1,487 UTF-8 bytes excluding final newline, 1,473 code points, 237 whitespace words; exact owner-source comparison. |
| V-003 | Design | Scope extractor and two-pass selection validator pass with current digests. |
| V-004 | L0 runtime | `node --test` positive and causal negative fixtures; fake transport only. |
| V-005 | Secrets | Scan source/generated JSON/text for credential values, bearer headers, and unauthorized fields without reading or printing the real credential. |
| V-006 | Planning | Every SWU unique, one parent, dependencies acyclic, wave order closed, write scopes non-overlapping sequentially, closeout rows complete. |

## Live evidence checks

Live checks are not part of this Invoke run.

| ID | Scope | Required evidence |
|---|---|---|
| V-101 | One provider request | Explicit operator authorization, exact admitted manifest, unique attempt path, response/request metadata, raw SHA-256, no secret persistence. |
| V-102 | Second repetition | Same request digest, unique path, separately preserved raw bytes. |
| V-103 | Technical audio | Pinned tool/version/command logs; WAV rate/depth/channels/duration; two-pass loudness/peak metrics; derivative hash lineage. |
| V-104 | Fidelity | Alignment timing plus independent transcript/listening comparison and manual phrase review. |
| V-105 | Blind listening | Three locked sheets, common playback receipt, balanced orders, protected/unblinded key, median/spread. |
| V-106 | Terminal decision | Named operator outcome and reasons citing all governing hashes. |

## Negative controls

At minimum: stale excerpt, missing accent, missing account gate, alias-only model, unsupported request field, secret-shaped persisted field, existing output path, mocked timeout after write, malformed WAV, one omitted word, wrong “Body War,” exposed unblinding key, and score without owner decision.

## Stop conditions

Stop immediately on unexpected external activity, credential exposure, stale provider/source binding, undocumented control, ambiguous provider completion, overwrite risk, raw/receipt mismatch, fidelity disagreement, failed key phrase, listening bias breach, or claim inflation. Preserve evidence and route to the named owner; do not repair by retry, prose, or default.
