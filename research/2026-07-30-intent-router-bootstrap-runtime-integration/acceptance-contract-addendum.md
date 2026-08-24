# Final Acceptance-Contract Addendum

dispatch_id: `2026-07-30-intent-router-bootstrap-runtime-integration`  
step_id: `s2`  
capability_ref: `research`  
capability_target: `dispatch-sheet.json`  
capability_mode: `synthesize`  
wave_id: `synthesize`  
write_scope: `[]`  
status: `repaired-candidate-final`  
artifacts: `[]`  
validation: `Read-only mechanical repair using synthesis-revised.md, reviews/round-2/nonvacuity.md, and receipts/reviewer-nonvacuity-round-2.json only. No source inspection, execution, generation, installation, or mutation.`  
observer_status: `not-invoked-read-only-synthesis-repair`  
blockers: `[]`

residue:

- `All commands, runner paths, schemas, fixture values, and case expectations below are future contract design, not current evidence.`
- `No canonical public source, generated wrapper, release archive, consumer installation, or orchestrator adapter currently supplies these surfaces.`
- `Exact future version strings and lowercase 64-hex digests must be frozen in each fixture manifest before execution.`
- `Topology, authority ownership, public-private boundary, and reasoning-engine claim ceiling remain unchanged.`

reroute: `Replace only the prior FUTURE acceptance-command section with this addendum; implement and execute it only after the separately gated authority transitions.`  
handoff_note: `This addendum freezes timeout, numeric exits, target output forms, machine schemas, fixture fields, rollback isolation, all case scalars, and zero-call counters. Only an already confirmed canonical Dispatch/group/seat may cross the workflow-binding seam.`

Everything below is **future acceptance design and non-evidence**. A path or
expected value named here does not establish that the executable, package,
adapter, release, or witness exists.

## 1. Frozen constants and sentinel rules

```text
request_byte_ceiling       = 262144
target_stdout_byte_ceiling = 1048576
target_stderr_byte_ceiling = 0
adapter_timeout_ms         = 5000
timeout_injected_delay_ms  = 5001
not_started_or_no_exit     = -1
```

`-1` is the only sentinel. It is permitted only when the relevant target or
adapter was not started, is not applicable on that surface, or was terminated
without an exit status. It must never represent an unknown numeric exit after
a process exited.

Runner exits:

```text
0 = every declared case emitted exactly once and passed
1 = at least one declared case completed but failed expectation
2 = fixture, CLI, schema, or harness configuration failure
3 = runner could not complete or emit a valid summary
```

The runner itself emits no stderr bytes. A summary is required for runner exits
`0` and `1`. For exits `2` or `3`, stdout is empty and no acceptance claim may
be made.

## 2. Required fixture-manifest fields

Every future case manifest is a closed object: unspecified properties are
forbidden.

| Field | Type and constraint |
|---|---|
| `schema` | Exact string `intent-route.acceptance-fixture@1` |
| `surface` | Closed enum: `json-port`, `public-core`, `codex-wrapper`, `claude-wrapper`, `orchestrator-adapter` |
| `expected_core_version` | String matching `^[0-9]+\.[0-9]+\.[0-9]+$` |
| `expected_manifest_version` | String matching `^[0-9]+\.[0-9]+\.[0-9]+$` |
| `expected_request_protocol_version` | Exact string `intent-route.request@1` |
| `expected_port_protocol_version` | Exact string `intent-route.runtime-port@1` |
| `expected_disposition_protocol_version` | Exact string `intent-route.disposition@1` |
| `expected_catalog_digest` | Lowercase SHA-256 matching `^[0-9a-f]{64}$` |
| `expected_closure_digest` | Lowercase SHA-256 matching `^[0-9a-f]{64}$` |
| `expected_fixture_digest` | Lowercase SHA-256 matching `^[0-9a-f]{64}$`; computed with this field omitted |
| `mismatch_catalog_digest` | Lowercase 64-hex; differs from `expected_catalog_digest` |
| `mismatch_closure_digest` | Lowercase 64-hex; differs from `expected_closure_digest` |
| `prior_release_id` | Nonempty string matching `^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$` |
| `prior_release_archive` | Repository-relative regular immutable fixture archive; no absolute path, `..`, symlink, or network URI |
| `expected_prior_release_archive_digest` | Lowercase 64-hex SHA-256 of `prior_release_archive` |
| `expected_prior_closure_digest` | Lowercase 64-hex |
| `expected_restored_closure_digest` | Lowercase 64-hex equal to `expected_prior_closure_digest` |
| `isolated_install_root_mode` | Exact string `mkdtemp` |
| `request_byte_ceiling` | Exact integer `262144` |
| `target_stdout_byte_ceiling` | Exact integer `1048576` |
| `target_stderr_byte_ceiling` | Exact integer `0` |
| `adapter_timeout_ms` | `5000` for orchestrator-adapter; `null` otherwise |
| `cases` | Closed object keyed by exactly the declared case IDs |
| `expected_target_stdout_bytes_by_case` | Closed object with one exact integer entry for each case expected to emit stdout |

For one-document outputs, each exact byte count is `1..1048576`; `A21` is
`2..1048576`; `A22` is exactly `1048577`. Zero-document cases omit the map
entry and require zero bytes.

Before use, the runner verifies all version fields and digests. A mismatch is a
fixture/harness error unless the case explicitly injects that mismatch.

## 3. Machine schema: `intent-route.acceptance-case@1`

Each case line is one canonical JSON object with all fields required and no
additional properties.

### Top-level fields

| Field | Type, nullability, and closed values |
|---|---|
| `schema` | Exact string `intent-route.acceptance-case@1` |
| `surface` | Enum `json-port`, `public-core`, `codex-wrapper`, `claude-wrapper`, `orchestrator-adapter` |
| `case_id` | Enum `J01`–`J13`, `P01`–`P08`, `W01`–`W15`, `A01`–`A27`; must belong to surface |
| `condition` | Closed enum below |
| `status` | Enum `pass`, `fail` |
| `expected` | Required expectation object |
| `observed` | Required observation object with identical shape |
| `fixture_digest` | Lowercase 64-hex |
| `closure_digest` | Lowercase 64-hex |
| `case_record_digest` | Lowercase 64-hex SHA-256 of canonical line with this field omitted |

Closed `condition` enum:

```text
candidate-unconfirmed
candidate-confirmed
ambiguous
no-match
invalid-request
malformed-json
malformed-catalog
capability-denied
request-version-mismatch
port-version-mismatch
core-version-mismatch
manifest-version-mismatch
catalog-digest-mismatch
content-digest-mismatch
integration-disabled
rollback-verified
rollback-digest-mismatch
timeout
unavailable-executable
nonzero-target-exit
multiple-stdout-documents
oversized-stdout
stderr-violation
dispatch-binding-conflict
authorization-denied
execution-error
effect-receipt-missing
core-tests
private-content-scan
private-import-scan
zero-authority-manifest
package-version-binding
protocol-version-binding
closure-digest-binding
fixture-digest-binding
```

### Exact `expected` and `observed` object shape

Both objects require all fields and forbid additional properties.

| Field | Type and closed constraint |
|---|---|
| `target_exit_code` | Integer enum `-1, 0, 2, 3, 4, 5, 7, 10` |
| `adapter_exit_code` | Integer enum `-1, 0, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22` |
| `target_stdout_document_count` | Integer enum `0, 1, 2` |
| `target_stdout_schema` | `null` or enum `intent-route.runtime-port@1`, `intent-route.error@1`, `intent-route.public-check@1` |
| `target_stdout_bytes` | Integer `0..1048577` |
| `target_stdout_byte_ceiling` | Exact integer `1048576` |
| `target_stderr_bytes` | Integer enum `0, 1` |
| `target_stderr_byte_ceiling` | Exact integer `0` |
| `result_kind` | `null` or enum `candidate`, `ambiguous`, `no-match`, `invalid` |
| `reason_code` | Closed enum below |
| `authority_effect` | `null` or exact string `none` |
| `post_rollback_closure_digest` | `null` or lowercase 64-hex |
| `workflow_bind_calls` | Integer enum `0, 1` |
| `dispatch_open_or_appender_calls` | Exact integer `0` |
| `aci_journal_dispatch_open_calls` | Exact integer `0` |
| `compatibility_fallback_calls` | Exact integer `0` |
| `host_spawn_calls` | Integer enum `0, 1` |

Closed `reason_code` enum:

```text
IR_CANDIDATE
IR_AMBIGUOUS
IR_NO_MATCH
IR_INVALID_REQUEST
IR_TRANSPORT_MALFORMED_JSON
IR_INVALID_CATALOG
IR_CAPABILITY_DENIED
IR_REQUEST_VERSION_UNSUPPORTED
IR_PORT_VERSION_UNSUPPORTED
IR_CORE_VERSION_MISMATCH
IR_MANIFEST_VERSION_MISMATCH
IR_CATALOG_DIGEST_MISMATCH
IR_CONTENT_DIGEST_MISMATCH
IR_INTEGRATION_DISABLED
IR_ROLLBACK_VERIFIED
IR_ROLLBACK_DIGEST_MISMATCH
IR_ADAPTER_TIMEOUT
IR_ADAPTER_UNAVAILABLE
IR_ADAPTER_NONZERO_EXIT
IR_ADAPTER_MULTIPLE_OUTPUT
IR_ADAPTER_STDOUT_OVERSIZE
IR_ADAPTER_STDERR_VIOLATION
CONFLICT
AUTHORIZATION_DENIED
RUNTIME_ERROR
READ_INTEGRITY_FAILURE
PUBLIC_CORE_TESTS_PASS
PRIVATE_CONTENT_SCAN_PASS
PRIVATE_IMPORT_SCAN_PASS
ZERO_AUTHORITY_MANIFEST_PASS
PACKAGE_VERSION_BINDING_PASS
PROTOCOL_VERSION_BINDING_PASS
CLOSURE_DIGEST_BINDING_PASS
FIXTURE_DIGEST_BINDING_PASS
```

`status="pass"` iff `observed` is scalar-for-scalar equal to `expected`; no
post-observation normalization is allowed.

`authority_effect` is exactly `"none"` for every resolver disposition and for
`A24`–`A27`, which begin with a valid candidate. It is `null` for public checks
and adapter/wrapper/transport failures that do not yield a trusted disposition.

Output consistency:

- zero documents requires null schema and zero bytes;
- one document requires non-null schema and exact fixture-bound bytes, except
  `A22`, exactly `1048577`;
- two documents is allowed only for `A21`, with runtime-port schema and exact
  fixture-bound bytes;
- one stderr byte is allowed only for injected `A23`; every other target emits
  zero stderr bytes.

## 4. Machine schema: `intent-route.acceptance-summary@1`

The final stdout line is canonical JSON with all fields required and no
additional properties.

| Field | Type and constraint |
|---|---|
| `schema` | Exact string `intent-route.acceptance-summary@1` |
| `surface` | Closed surface enum |
| `case_ids` | Ordered array exactly matching command-declared IDs |
| `declared_cases` | Exact surface count: `13`, `8`, `15`, `15`, or `27` |
| `passed` | Integer `0..declared_cases` |
| `failed` | Integer `0..declared_cases`; `passed + failed = declared_cases` |
| `fixture_digest` | Lowercase 64-hex equal to fixture manifest |
| `closure_digest` | Lowercase 64-hex equal to expected closure, or restored closure for rollback observation |
| `case_records_digest` | Lowercase 64-hex over ordered canonical case lines |
| `stdout_lines` | Exact integer `declared_cases + 1` |
| `stderr_bytes` | Exact integer `0` |
| `runner_exit_code` | Enum `0, 1`; `0` iff `failed=0` |
| `request_byte_ceiling` | Exact `262144` |
| `target_stdout_byte_ceiling` | Exact `1048576` |
| `target_stderr_byte_ceiling` | Exact `0` |
| `adapter_timeout_ms` | `5000` for adapter; `null` otherwise |
| `isolated_install_root_mode` | `mkdtemp` for wrappers/adapter; `null` otherwise |

The runner exit equals `runner_exit_code`. Runner exit `2` or `3` emits no
summary and cannot be interpreted as acceptance.

## 5. Exact future commands

### JSON port — 13 cases

```bash
node arcanum/arcana/intent-route-resolver/package/test/run-json-port-acceptance.mjs \
  --cases arcanum/arcana/intent-route-resolver/fixtures/json-port-acceptance-v1.json \
  --case-ids J01,J02,J03,J04,J05,J06,J07,J08,J09,J10,J11,J12,J13 \
  --request-byte-ceiling 262144 \
  --stdout-byte-ceiling 1048576 \
  --stderr-byte-ceiling 0
```

Exactly 14 stdout JSONL lines; runner exit `0`; runner stderr zero bytes.

### Public core/private scan — 8 cases

```bash
node arcanum/arcana/intent-route-resolver/scripts/run-public-core-acceptance.mjs \
  --root arcanum/arcana/intent-route-resolver \
  --cases arcanum/arcana/intent-route-resolver/fixtures/public-core-acceptance-v1.json \
  --case-ids P01,P02,P03,P04,P05,P06,P07,P08 \
  --request-byte-ceiling 262144 \
  --stdout-byte-ceiling 1048576 \
  --stderr-byte-ceiling 0
```

Exactly 9 stdout JSONL lines; runner exit `0`; runner stderr zero bytes.

### Codex wrapper — 15 cases

```bash
node .agents/skills/intent-route-resolver/scripts/run-wrapper-acceptance.mjs \
  --entry .agents/skills/intent-route-resolver/scripts/invoke-json-port.mjs \
  --cases .agents/skills/intent-route-resolver/fixtures/wrapper-acceptance-v1.json \
  --case-ids W01,W02,W03,W04,W05,W06,W07,W08,W09,W10,W11,W12,W13,W14,W15 \
  --request-byte-ceiling 262144 \
  --stdout-byte-ceiling 1048576 \
  --stderr-byte-ceiling 0 \
  --prior-release-id-field prior_release_id \
  --prior-release-archive-field prior_release_archive \
  --prior-release-archive-digest-field expected_prior_release_archive_digest \
  --expected-prior-closure-digest-field expected_prior_closure_digest \
  --expected-restored-closure-digest-field expected_restored_closure_digest \
  --isolated-install-root-mode mkdtemp
```

Exactly 16 stdout JSONL lines; runner exit `0`; runner stderr zero bytes.
`W15.observed.post_rollback_closure_digest` equals both expected prior and
restored closure digests.

### Claude wrapper — 15 cases

```bash
node .claude/skills/intent-route-resolver/scripts/run-wrapper-acceptance.mjs \
  --entry .claude/skills/intent-route-resolver/scripts/invoke-json-port.mjs \
  --cases .claude/skills/intent-route-resolver/fixtures/wrapper-acceptance-v1.json \
  --case-ids W01,W02,W03,W04,W05,W06,W07,W08,W09,W10,W11,W12,W13,W14,W15 \
  --request-byte-ceiling 262144 \
  --stdout-byte-ceiling 1048576 \
  --stderr-byte-ceiling 0 \
  --prior-release-id-field prior_release_id \
  --prior-release-archive-field prior_release_archive \
  --prior-release-archive-digest-field expected_prior_release_archive_digest \
  --expected-prior-closure-digest-field expected_prior_closure_digest \
  --expected-restored-closure-digest-field expected_restored_closure_digest \
  --isolated-install-root-mode mkdtemp
```

Exactly 16 stdout JSONL lines; runner exit `0`; runner stderr zero bytes. The
same rollback equality applies. Case response bytes equal the corresponding
Codex case bytes. Only declared provenance and Claude tool-token normalization
may differ in wrapper source.

### Orchestrator adapter — 27 cases

```bash
python projects/cyberalchemy-orchestrator/implementations/tests/runtime/run_intent_route_adapter_acceptance.py \
  --cases projects/cyberalchemy-orchestrator/implementations/tests/runtime/fixtures/intent-route-adapter-acceptance-v1.json \
  --case-ids A01,A02,A03,A04,A05,A06,A07,A08,A09,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22,A23,A24,A25,A26,A27 \
  --request-byte-ceiling 262144 \
  --stdout-byte-ceiling 1048576 \
  --stderr-byte-ceiling 0 \
  --timeout-ms 5000 \
  --prior-release-id-field prior_release_id \
  --prior-release-archive-field prior_release_archive \
  --prior-release-archive-digest-field expected_prior_release_archive_digest \
  --expected-prior-closure-digest-field expected_prior_closure_digest \
  --expected-restored-closure-digest-field expected_restored_closure_digest \
  --isolated-install-root-mode mkdtemp
```

Exactly 28 stdout JSONL lines; runner exit `0`; runner stderr zero bytes.
`A18.cases.injected_delay_ms` is exactly `5001`.

## 6. Complete scalar case mapping

Notation:

```text
exit = target_exit_code/adapter_exit_code
docs = target_stdout_document_count
schema = target_stdout_schema
bytes = expected_target_stdout_bytes_by_case.<ID>, or literal
stderr = target_stderr_bytes
kind = result_kind
auth = authority_effect
calls = workflow_bind/dispatch-open-or-appender/ACI-dispatch-open/compatibility-fallback/host-spawn
```

All rows use stdout ceiling `1048576` and stderr ceiling `0`. `zero` in the
calls column means `0/0/0/0/0`.

### JSON-port cases

| ID | Condition; reason | exit | docs/schema/bytes/stderr | kind/auth | calls |
|---|---|---:|---|---|---|
| J01 | candidate; `IR_CANDIDATE` | `0/-1` | `1/runtime-port/J01/0` | `candidate/none` | zero |
| J02 | ambiguous; `IR_AMBIGUOUS` | `0/-1` | `1/runtime-port/J02/0` | `ambiguous/none` | zero |
| J03 | no-match; `IR_NO_MATCH` | `0/-1` | `1/runtime-port/J03/0` | `no-match/none` | zero |
| J04 | invalid request; `IR_INVALID_REQUEST` | `0/-1` | `1/runtime-port/J04/0` | `invalid/none` | zero |
| J05 | malformed JSON; `IR_TRANSPORT_MALFORMED_JSON` | `2/-1` | `1/error/J05/0` | `null/null` | zero |
| J06 | malformed catalog; `IR_INVALID_CATALOG` | `0/-1` | `1/runtime-port/J06/0` | `invalid/none` | zero |
| J07 | capability denied; `IR_CAPABILITY_DENIED` | `3/-1` | `1/error/J07/0` | `null/null` | zero |
| J08 | request version; `IR_REQUEST_VERSION_UNSUPPORTED` | `4/-1` | `1/error/J08/0` | `null/null` | zero |
| J09 | port version; `IR_PORT_VERSION_UNSUPPORTED` | `4/-1` | `1/error/J09/0` | `null/null` | zero |
| J10 | core version; `IR_CORE_VERSION_MISMATCH` | `4/-1` | `1/error/J10/0` | `null/null` | zero |
| J11 | manifest version; `IR_MANIFEST_VERSION_MISMATCH` | `4/-1` | `1/error/J11/0` | `null/null` | zero |
| J12 | catalog digest; `IR_CATALOG_DIGEST_MISMATCH` | `5/-1` | `1/error/J12/0` | `null/null` | zero |
| J13 | closure digest; `IR_CONTENT_DIGEST_MISMATCH` | `5/-1` | `1/error/J13/0` | `null/null` | zero |

`runtime-port` is exact schema `intent-route.runtime-port@1`; `error` is
`intent-route.error@1`; the byte-column case ID means the exact corresponding
fixture field.

### Public-core cases

All have `exit=0/-1`, one document, schema
`intent-route.public-check@1`, exact case-bound bytes, zero stderr, null
kind/authority, and zero counters.

| ID | Condition | Reason |
|---|---|---|
| P01 | core-tests | `PUBLIC_CORE_TESTS_PASS` |
| P02 | private-content-scan | `PRIVATE_CONTENT_SCAN_PASS` |
| P03 | private-import-scan | `PRIVATE_IMPORT_SCAN_PASS` |
| P04 | zero-authority-manifest | `ZERO_AUTHORITY_MANIFEST_PASS` |
| P05 | package-version-binding | `PACKAGE_VERSION_BINDING_PASS` |
| P06 | protocol-version-binding | `PROTOCOL_VERSION_BINDING_PASS` |
| P07 | closure-digest-binding | `CLOSURE_DIGEST_BINDING_PASS` |
| P08 | fixture-digest-binding | `FIXTURE_DIGEST_BINDING_PASS` |

### Codex and Claude wrapper cases

`W01`–`W13` use the same scalar mapping as `J01`–`J13`, with the wrapper case
byte-field key. `adapter_exit_code=-1` for every wrapper case.

| ID | Condition; reason | exit | docs/schema/bytes/stderr | kind/auth | rollback digest | calls |
|---|---|---:|---|---|---|---|
| W14 | disabled; `IR_INTEGRATION_DISABLED` | `10/-1` | `0/null/0/0` | `null/null` | `null` | zero |
| W15 | rollback; `IR_ROLLBACK_VERIFIED` | `0/-1` | `1/runtime-port/W15/0` | `candidate/none` | `expected_restored_closure_digest` | zero |

For both wrappers:

```text
prior_release_id                  = fixture.prior_release_id
prior_release_archive             = fixture.prior_release_archive
archive SHA-256                   = fixture.expected_prior_release_archive_digest
pre-rollback expected closure     = fixture.expected_prior_closure_digest
post-rollback observed closure    = fixture.expected_restored_closure_digest
expected_restored_closure_digest  = expected_prior_closure_digest
isolated_install_root_mode        = "mkdtemp"
```

Rollback never mutates the source repository or any package outside the
runner-created isolated directory.

### Orchestrator adapter cases

| ID | Condition; reason | exit | docs/schema/bytes/stderr | kind/auth | calls |
|---|---|---:|---|---|---|
| A01 | candidate-unconfirmed; `IR_CANDIDATE` | `0/0` | `1/runtime-port/A01/0` | `candidate/none` | zero |
| A02 | candidate-confirmed; `IR_CANDIDATE` | `0/0` | `1/runtime-port/A02/0` | `candidate/none` | `1/0/0/0/1` |
| A03 | ambiguous; `IR_AMBIGUOUS` | `0/0` | `1/runtime-port/A03/0` | `ambiguous/none` | zero |
| A04 | no-match; `IR_NO_MATCH` | `0/0` | `1/runtime-port/A04/0` | `no-match/none` | zero |
| A05 | invalid; `IR_INVALID_REQUEST` | `0/0` | `1/runtime-port/A05/0` | `invalid/none` | zero |
| A06 | malformed JSON; `IR_TRANSPORT_MALFORMED_JSON` | `2/11` | `1/error/A06/0` | `null/null` | zero |
| A07 | malformed catalog; `IR_INVALID_CATALOG` | `0/0` | `1/runtime-port/A07/0` | `invalid/none` | zero |
| A08 | capability denied; `IR_CAPABILITY_DENIED` | `-1/20` | `0/null/0/0` | `null/null` | zero |
| A09 | request version; `IR_REQUEST_VERSION_UNSUPPORTED` | `4/11` | `1/error/A09/0` | `null/null` | zero |
| A10 | port version; `IR_PORT_VERSION_UNSUPPORTED` | `4/11` | `1/error/A10/0` | `null/null` | zero |
| A11 | core version; `IR_CORE_VERSION_MISMATCH` | `4/11` | `1/error/A11/0` | `null/null` | zero |
| A12 | manifest version; `IR_MANIFEST_VERSION_MISMATCH` | `4/11` | `1/error/A12/0` | `null/null` | zero |
| A13 | catalog digest; `IR_CATALOG_DIGEST_MISMATCH` | `5/12` | `1/error/A13/0` | `null/null` | zero |
| A14 | closure digest; `IR_CONTENT_DIGEST_MISMATCH` | `5/12` | `1/error/A14/0` | `null/null` | zero |
| A15 | disabled; `IR_INTEGRATION_DISABLED` | `-1/10` | `0/null/0/0` | `null/null` | zero |
| A16 | rollback; `IR_ROLLBACK_VERIFIED` | `0/0` | `1/runtime-port/A16/0` | `candidate/none` | zero |
| A17 | rollback mismatch; `IR_ROLLBACK_DIGEST_MISMATCH` | `-1/12` | `0/null/0/0` | `null/null` | zero |
| A18 | timeout; `IR_ADAPTER_TIMEOUT` | `-1/13` | `0/null/0/0` | `null/null` | zero |
| A19 | unavailable; `IR_ADAPTER_UNAVAILABLE` | `-1/14` | `0/null/0/0` | `null/null` | zero |
| A20 | target nonzero; `IR_ADAPTER_NONZERO_EXIT` | `7/15` | `0/null/0/0` | `null/null` | zero |
| A21 | multiple stdout; `IR_ADAPTER_MULTIPLE_OUTPUT` | `0/16` | `2/runtime-port/A21/0` | `null/null` | zero |
| A22 | oversized stdout; `IR_ADAPTER_STDOUT_OVERSIZE` | `0/17` | `1/runtime-port/1048577/0` | `null/null` | zero |
| A23 | stderr violation; `IR_ADAPTER_STDERR_VIOLATION` | `0/18` | `1/runtime-port/A23/1` | `null/null` | zero |
| A24 | binding conflict; `CONFLICT` | `0/19` | `1/runtime-port/A24/0` | `candidate/none` | zero |
| A25 | authorization denied; `AUTHORIZATION_DENIED` | `0/20` | `1/runtime-port/A25/0` | `candidate/none` | `1/0/0/0/0` |
| A26 | execution error; `RUNTIME_ERROR` | `0/21` | `1/runtime-port/A26/0` | `candidate/none` | `1/0/0/0/1` |
| A27 | missing effect receipt; `READ_INTEGRITY_FAILURE` | `0/22` | `1/runtime-port/A27/0` | `candidate/none` | `1/0/0/0/1` |

For `A18`, `adapter_timeout_ms=5000` and
`cases.A18.injected_delay_ms=5001`. Target exit `-1` means termination after
the deadline without an exit status.

For rollback:

- `A16.observed.post_rollback_closure_digest` equals both expected prior and
  expected restored closure digests;
- `A17.post_rollback_closure_digest=null`, and a mismatched archive or restored
  digest is rejected before target invocation;
- archive digest first equals `expected_prior_release_archive_digest`;
- both cases use a fresh `mkdtemp` install root.

## 7. Seam and zero-call invariant

Only an already confirmed canonical Dispatch/group/seat may cross the
workflow-binding seam.

Across all 78 logical IDs:

- `dispatch_open_or_appender_calls=0`;
- `aci_journal_dispatch_open_calls=0`;
- `compatibility_fallback_calls=0`.

`workflow_bind_calls=1` only for `A02`, `A25`, `A26`, and `A27`.

`host_spawn_calls=1` only for `A02`, `A26`, and `A27`.

The adapter may reuse the confirmed Dispatch; it may never open one, append a
substitute record, synthesize an ACI `dispatch-open`, or invoke compatibility
fallback. Human confirmation, Dispatch binding, authorization, execution
attempt, observed effect, and required receipt remain non-substitutable and
independently fail closed.
