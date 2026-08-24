# Stage 07 Consolidated Findings

Parent verdict: **FIX**. The original design did not pass unchanged. All critic
findings were accepted; none were refuted.

| Severity | Consolidated change request | Sources | Disposition |
| --- | --- | --- | --- |
| CRITICAL | Define row-list/row-read authorization resources and concealment before capability, parsing, lookup, count, or page observations. | API-CRITIC-001 | fixed in stage 08 |
| CRITICAL | Add bounded manifest, record, YAML, validation-time, response, and concurrency limits. | API-CRITIC-005 | fixed as candidate tested defaults |
| CRITICAL | Remove implied WaveDB concurrency safety and prohibit builder/service overlap. | WRC-005 | claim narrowed; deployment experiment remains |
| MAJOR | Replace unkeyed path-derived IDs with a byte-exact secret-keyed construction and collision behavior. | API-CRITIC-004, AUTH-PRIV-001 | fixed; vectors remain |
| MAJOR | Gate path, digest, and exact size behind distinct permissions. | AUTH-PRIV-002 | fixed |
| MAJOR | Fully bind and authenticate space and row cursors. | API-CRITIC-002, API-CRITIC-003 | fixed; executable tests remain |
| MAJOR | Publish route-specific error precedence and one external duplicate/schema behavior. | API-CRITIC-006, API-CRITIC-007, AUTH-SCHEMA-004 | fixed |
| MAJOR | Separate ETag revalidation from explicit snapshot pinning. | API-CRITIC-008 | fixed |
| MAJOR | Define freshness against each manifest entry's `source_sha256`, with complete scope, provenance, expiry, and invalidation. | API-CRITIC-009, AUTH-FRESH-003 | fixed; L0 defaults unknown |
| MAJOR | Narrow reopen evidence to same-process and expected-key closure to reachable expected keys. | WRC-001, WRC-003 | fixed; fresh-process/store exclusivity unproven |
| MAJOR | Call the handle logically immutable and globally invalidate it on any runtime read anomaly. | WRC-004, WRC-006 | fixed; OS enforcement remains deployment work |
| MAJOR | Keep replacement and recovery outside L0 until a tested state machine exists. | WRC-007, WRC-008 | fixed by explicit exclusion |
| MINOR | Limit normalization and runtime claims to the exact evidenced data/runtime pairing. | WRC-002, WRC-009 | fixed; environment matrix remains |

The orchestrated review gate is `gate_block` because all three receipts are
non-pass. That gate blocks the *initial design*, not the authorized parent repair
stage. No unconfirmed feedback loop or additional critic was started.
