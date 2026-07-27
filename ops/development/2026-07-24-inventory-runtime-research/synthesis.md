## Candidate matrix

| Candidate | Unique responsibility | Surface | MVP machinery | Strength | Kill exposure |
|---|---|---|---|---|---|
| A — Ashby lifecycle bundle | Own generic lookup/append mechanics and their installation lifecycle | Two verbs: `lookup`, `append` | validator pair, generalized appender, receipt emitter, digest manifest | Clean public-canonical versus consumer-state boundary; reuses Inventory `install`/`sync` | Command and transaction semantics are underspecified; `partial_projection_gap` risks legitimizing non-conformance |
| B — Spivak operation wrapper | Attribute one operation to exact inputs, validator bundle, warning delta, digests, and mutation outcome | Existing lookup gate plus wrapped `append` | baseline/candidate validation, in-memory staging, conflict detection, canonical receipt | Smallest functional delta; closed deterministic witnesses; no new authority | Must prove it is more than renamed updater/validator: unique responsibility is cross-owner binding and receipt attribution |
| C — Wiener operator coordinator | Make the runtime operable from an installed package independent of upstream checkout/cwd | `validate`, `lookup`, `append`, `doctor`; profile | strict root resolution, dependency preflight, lock, staging, journal, recovery | Strongest portability and crash/concurrency story | Larger than the reflection-approved proposal; `doctor`, lock, and journal are presently unwitnessed scope expansion |

Sources: A [Agent 1, `research.md:20-38`], B [Agent 2, `research.md:42-71,126-166`], C [Agent 3, `research.md:200-258`]. The live tree confirms the underlying gap: `.arcanum/inventory/scripts/` is absent, while the complete pair exists in `.claude/skills/inventory/scripts/`; the current index is 212 entries at digest `6ccb0d3c…3d60c7f`, so the reflection’s 210-entry count is already historical, exactly as Agent 2 warned [Agent 2, `research.md:46-53`; reflection `:17-29`].

## Recommendation: Candidate B

Recommend B, constrained by A’s ownership/install boundary. This is selection, not averaging: B owns the runtime behavior; A supplies verified lifecycle constraints. C remains a later hardening candidate.

### Proposed exact commands

```text
.arcanum/inventory/bin/inventory lookup --index index.json --json
.arcanum/inventory/bin/inventory append --record <record.json> \
  --timestamp <ISO-8601> (--dry-run | --apply) --json
inventory sync --check
inventory sync --apply        # only through the existing approved sync lifecycle
```

`lookup` means “prove package lookup readiness and return its receipt”; it does not synthesize queries or promote matches. It runs the full package-relative two-file gate required by the canonical contract [Inventory `SKILL.md:112-123,230-241`; shell-to-sibling-Python dependency `validate-index-json.sh:99-104`].

Exact lookup states:

- `ready`
- `blocked`
- `inventory-unavailable`
- `machine-index-gap`
- `human-fallback`
- `tooling-unavailable`
- `invalid-request`

Exact append states:

- `dry-run-ready`
- `applied`
- `identical-no-op`
- `invalid-request`
- `id-conflict`
- `tooling-unavailable`
- `baseline-blocked`
- `candidate-blocked`
- `write-failed`
- `postwrite-digest-mismatch`

Only `ready`, `dry-run-ready`, `applied`, and `identical-no-op` are successful states. `human-fallback` is explicit residue, never lookup-ready proof. Same ID plus identical normalized content is a no-op; same ID plus different normalized content is `id-conflict`, repairing the current blind existing-ID behavior [updater `inventory-update.cjs:130-159`; Agent 2 `research.md:159-166`].

Stdout is one canonical JSON receipt; stderr carries human diagnostics. Dry-run performs no write. No wall-clock fields are permitted in the deterministic payload.

### Receipt schema

```json
{
  "schema_version": "inventory.operation-receipt.v1",
  "operation": "lookup|append",
  "mode": "read-only|dry-run|apply",
  "status": "...",
  "reason_code": null,
  "operation_fingerprint": "sha256(canonical operation inputs)",
  "timestamp_input": null,
  "inventory_root": ".arcanum/inventory",
  "runtime": {
    "profile_version": "...",
    "bundle_sha256": "...",
    "helpers": [
      {"path": "lib/validate-index-json.sh", "sha256": "..."},
      {"path": "lib/validate_projection_conformance.py", "sha256": "..."},
      {"path": "lib/inventory-update.cjs", "sha256": "..."}
    ]
  },
  "inputs": {
    "index_sha256": "...",
    "human_index_sha256": "...",
    "record_sha256": null,
    "normalized_record_sha256": null
  },
  "baseline": {
    "report_sha256": "...",
    "lookup_readiness": "ready|blocked",
    "failure_count": 0,
    "warning_count": 72
  },
  "candidate": {
    "disposition": "added|identical-no-op|id-conflict",
    "index_sha256": "...",
    "human_index_sha256": "...",
    "report_sha256": "...",
    "lookup_readiness": "ready|blocked"
  },
  "warning_delta": {
    "introduced": [],
    "resolved": [],
    "inherited_count": 72,
    "inherited_set_sha256": "..."
  },
  "write": {
    "attempted": false,
    "committed": false,
    "changed_paths": [],
    "postwrite_index_sha256": null,
    "postwrite_human_index_sha256": null
  },
  "authority_boundary": "inventory-read-model-only",
  "residue": [],
  "receipt_sha256": "sha256(canonical receipt excluding receipt_sha256)"
}
```

Warning identity is `sha256(code + NUL + subject + NUL + selector)`; introduced/resolved/inherited are deterministic set differences [Agent 2, `research.md:126-142`]. Full validation still reports all historical warnings; operation receipts enumerate only introduced/resolved warnings and summarize inherited debt [reflection `:121-152`]. The canonical validator already returns digest, readiness, check-level errors/warnings, and counts [validator `validate_projection_conformance.py:383-402`].

## Ownership and synchronization

Public canonical owner, under `arcanum/arcana/inventory/`:

- coordinator/receipt emitter;
- generalized appender derived from the local updater;
- complete validator pair;
- receipt schema;
- runtime manifest schema;
- focused fixtures;
- template plus `install`/`sync` rules.

Installed consumer-owned state:

- `.arcanum/inventory/{README.md,schema.md,index.json,index.md,tags.md,log.md,entries/,queries/,raw/,indexes/,lint/}`;
- local vocabulary/configuration, source bindings, receipts, and observability events.

Installed generated payload:

- `.arcanum/inventory/bin/inventory`;
- `.arcanum/inventory/lib/*`;
- `.arcanum/inventory/runtime-manifest.json`.

The manifest records canonical logical source, profile/schema version, each relative runtime path and digest, and a bundle digest. `sync --check` reports missing/drifted/generated files; `sync --apply` refreshes only generated runtime payload, never indexes, entries, tags, logs, raw sources, or local configuration. Host-native `.claude`/`.agents` packages remain separately regenerated mirrors: bootstrap already copies all support directories except `development/` and marks them regenerate-only [bootstrap `bootstrap_arcanum.sh:795-875`; generated proof `.claude/skills/inventory/SKILL.md:1-15`]. No private checkout path enters public artifacts or receipts.

## Lock, staging, journal

- In-memory or temporary candidate staging: **MVP**, because candidate conformance and dry-run non-mutation require it [Agent 2, `research.md:68-70`].
- Digest manifest and pre/post digest binding: **MVP**, because portability and stale-observation prevention are core gaps [reflection `:83-99,141-164`].
- Single-writer lock: **later**; no current fixture proves concurrent writers.
- Durable transaction journal/recovery: **later**; required before claiming crash-safe or atomic two-file apply, but outside the bounded reflection scope.
- Therefore MVP must claim only fail-closed outcome attribution, not transactional atomicity. A write failure or postwrite mismatch emits no success receipt and may require explicit manual repair.

## Deterministic test matrix

1. Package-local lookup from unrelated cwd → `ready`.
2. Missing shell helper/Python/Node/`jq` → `tooling-unavailable`, zero writes.
3. Controlled append over inherited warnings → zero introduced; stable inherited count/digest.
4. One new unknown tag → exactly one introduced warning; still warn-only.
5. Repeated dry-run → byte-identical receipt and filesystem.
6. Identical existing ID/content → `identical-no-op`, unchanged digests.
7. Same ID/different content → `id-conflict`, zero mutation.
8. Seven accepted kinds pass; unsupported kind blocks before mutation [current witness `test-inventory-update.cjs:124-179,182-239`].
9. Each conformance class drift—coverage, identity, existence, maps, human view, freshness—blocks baseline or candidate [validator `:170-306,308-402`].
10. Receipt for digest A after index B exists → historical, never current.
11. Write failure/postwrite mismatch → no success claim.
12. Missing/drifted manifest member → `sync --check` fails precisely.

## Migration phases

1. Obtain explicit approval; the current reflection approved no mutation [reflection `:220-237`].
2. Canonicalize B’s engine, validator pair, schema, and fixtures publicly.
3. Extend templates/install/sync with generated runtime payload and manifest.
4. Additively sync one consumer; do not alter its data.
5. Route maintenance/preflight lookup and append through receipts; observer consumption remains optional and cannot change the primary result.
6. Consider C’s lock/journal/doctor only after concurrency/crash witnesses exist.

Explicit exclusions: tag cleanup, duplicate-tag cleanup, legacy `by_evidence_set` migration, replace/update, query synthesis, ingest orchestration, auto-repair, UI, ontology/definition/promotion authority, severity policy, provenance truth, private bindings, and any claim of atomic apply. These exclusions match the reflection’s rejected changes [reflection `:182-207`] and Inventory’s authority rule [Inventory `SKILL.md:318-322`].

# Revised Synthesis After The Skeptic Loop

## Revised verdict matrix

| Candidate | Skeptic verdict | Final disposition | Retained responsibility |
|---|---|---|---|
| A — lifecycle bundle | Rittel: `build-from-owned`; Wittgenstein: **KILL standalone** | **KILL as a runtime owner** | Retain only its ownership constraint: canonical public payload, generated installed copies, consumer-owned mutable state, existing Inventory `install`/`sync` distribution |
| B — operation wrapper | Rittel: `build-from-owned`; Popper: no KILL; Wittgenstein: **KEEP** | **KEEP; recommended MVP** | Unique Inventory state-transition receipt: exact baseline + normalized record + exact validator bundle → candidate disposition + warning delta + observed mutation outcome |
| C — operator coordinator | Rittel: mostly existing precedent; Wittgenstein: **DECOMPOSE/DEFER** | Reject omnibus coordinator; defer transaction component | Later single-writer lock plus durable two-file journal/recovery, with dedicated concurrency/crash witnesses |

A collapses because append, readiness validation, install/sync, and lookup
orchestration already have owners; its `partial_projection_gap` also contradicts
fail-closed human-view conformance. B remains distinct because neither updater,
validator, Signal Observer, OIL, nor install/sync binds a causal Inventory
transition into one deterministic domain receipt. C's `validate`, `lookup`,
`append`, `doctor`, observer handoff, and profile mostly duplicate existing
owners; only transaction/concurrency safety survives decomposition.

## Final minimal runtime contract

The installed Inventory package contains existing lookup validation plus B's
append-transition runtime. It does not create a new lifecycle bundle or omnibus
CLI owner.

```text
# Existing Inventory lookup-readiness owner
.arcanum/inventory/scripts/validate-index-json.sh \
  .arcanum/inventory/index.json

# New B responsibility
.arcanum/inventory/bin/inventory append \
  --record <record.json> \
  --timestamp <ISO-8601> \
  (--dry-run | --apply) \
  --json

# Existing Inventory lifecycle owner
inventory sync --check
inventory sync --apply
```

Lookup search/orchestration remains the Inventory sigil's responsibility. B
consumes the full validator twice—baseline and candidate—but does not redefine
readiness.

The B transition is:

```text
exact baseline bytes
+ exact normalized record
+ supplied timestamp
+ exact validator bundle
→ candidate disposition
+ introduced/resolved/inherited warning delta
+ actual mutation outcome
```

Append states:

- `dry-run-ready`
- `applied`
- `identical-no-op`
- `invalid-request`
- `id-conflict`
- `tooling-unavailable`
- `baseline-blocked`
- `candidate-blocked`
- `write-failed`
- `postwrite-digest-mismatch`

Same ID plus identical normalized content is `identical-no-op`; same ID plus
different normalized content is `id-conflict`.

## Required receipt

```json
{
  "schema_version": "inventory.operation-receipt.v1",
  "operation": "append",
  "mode": "dry-run|apply",
  "status": "...",
  "reason_code": null,
  "operation_fingerprint": "sha256(canonical operation inputs)",
  "timestamp_input": "ISO-8601",
  "inventory_root": ".arcanum/inventory",
  "runtime": {
    "bundle_sha256": "...",
    "helpers": [
      {"path": "lib/inventory-update.cjs", "sha256": "..."},
      {"path": "scripts/validate-index-json.sh", "sha256": "..."},
      {"path": "scripts/validate_projection_conformance.py", "sha256": "..."}
    ]
  },
  "inputs": {
    "baseline_index_sha256": "...",
    "baseline_human_index_sha256": "...",
    "record_sha256": "...",
    "normalized_record_sha256": "..."
  },
  "baseline": {
    "report_sha256": "...",
    "lookup_readiness": "ready|blocked",
    "failure_count": 0,
    "warning_count": 72
  },
  "candidate": {
    "disposition": "added|identical-no-op|id-conflict",
    "index_sha256": "...",
    "human_index_sha256": "...",
    "report_sha256": "...",
    "lookup_readiness": "ready|blocked"
  },
  "warning_delta": {
    "introduced": [],
    "resolved": [],
    "inherited_count": 72,
    "inherited_set_sha256": "..."
  },
  "write": {
    "attempted": false,
    "committed": false,
    "observed_changed_paths": [],
    "expected_postwrite_digests": {},
    "actual_postwrite_digests": {},
    "possible_partial_mutation": false,
    "repair_required": false
  },
  "authority_boundary": "inventory-read-model-only",
  "residue": [],
  "receipt_sha256": "sha256(canonical receipt excluding receipt_sha256)"
}
```

`committed=true` means both intended projections were subsequently observed at
candidate digests; it does not imply an atomic transaction.

For `write-failed` or `postwrite-digest-mismatch`, the receipt must record
`write.attempted=true`, `committed=false`, actual changed paths and digests,
`possible_partial_mutation=true`, `repair_required=true`, and a concrete repair
route. It may not claim success or rollback.

## Stale-currentness contract

The receipt is digest-bound historical evidence, not self-updating current
state. It has no `currentness` field. An external digest verifier compares the
receipt's bound digest with the current `index.json` digest and emits a separate
verification result. It never rewrites the original receipt. The verifier owner
remains unresolved and outside B.

## Exact MVP/later split

MVP:

- B's transition receipt and canonical JSON serialization;
- normalized equality versus `id-conflict`;
- baseline and candidate full-conformance validation;
- introduced/resolved/inherited warning attribution;
- input/helper/baseline/candidate/postwrite digest binding;
- in-memory or temporary candidate staging;
- package-local complete validator pair;
- strict helper/root binding with no `cwd` fallback;
- installed bundle manifest and `sync --check` under existing Inventory lifecycle;
- explicit partial-mutation reporting;
- stdout receipt only, diagnostics on stderr;
- deterministic fixtures for all B states.

Later, separately owned:

- C's single-writer lock;
- durable journal;
- crash recovery and explicit recovery application;
- concurrency, interruption, and recovery fixtures;
- any atomic-apply claim.

Rejected rather than deferred into B:

- broad `doctor`;
- new lookup/validate ownership;
- telemetry append or reflection routing;
- query/search synthesis;
- auto-repair;
- tag cleanup, legacy-map migration, replacement/update;
- ontology, definitions, promotion, or truth authority.

## Remaining proof boundary

- B is `build-from-owned`, not precedent-clean; novelty is only the
  Inventory-specific causal receipt join.
- Existing updater and conformance tests prove substrate behavior, not the
  proposed runtime receipt. Every B witness remains implementation evidence
  pending.
- External currentness-verifier ownership is unresolved.
- MVP deliberately lacks atomicity. If atomic two-file apply is an acceptance
  requirement, C's transaction slice becomes a prerequisite rather than later.
- A's ownership boundary survives only as a constraint.
