# Security and abuse cases

| Abuse or failure | Required defense |
|---|---|
| candidate treated as authorization | `authority_effect: none`, zero-call counters, separate confirmed Dispatch input |
| catalog spoofing or drift | owner/revision/content digest binding and fail-closed validation |
| wrapper divergence | one canonical closure, per-case byte comparison, no hand edits |
| prompt/private content leakage | JSON-only core, synthetic public fixtures, private-content/import scans |
| process smuggling | one bounded stdin/stdout document, zero stderr, exact exits, timeout and size limits |
| semantic fallback after rejection | no retry, repair, enrichment, ranking, or compatibility fallback |
| rollback leaves partial package | isolated preimage digest and exact durable restoration |
| adapter opens Dispatch or binds workflow | static dependency audit plus negative call counters |

The authenticated confirmed-Dispatch interface is outside the resolver. The
adapter accepts it only as a separate host-owned input after human confirmation.

