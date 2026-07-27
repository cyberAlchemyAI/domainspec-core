# Inventory Runtime Improvement Findings

**Answer:** **Research design resolved:** select Candidate B as the implementation target, kill A standalone, and decompose/defer C; **runtime ready or accepted: no**—no Candidate B runtime receipt is in evidence, so acceptance remains withheld until named reproducible receipts prove the minimum gates below.

## Evidence and current state

The current substrate is usable but does not yet establish the proposed runtime:

- The explorer run reports updater tests at 9/9 groups, Markdown tests at 7/7, conformance fixtures at 10/10, and a dry run with unchanged projections but 72 inherited warnings. These are substrate witnesses, not witnesses of an operation-receipt implementation. [`research.md:42-53`; `ops/development/2026-07-24-inventory-runtime-research/skeptic-review.md:41-44`]
- At the explorer's observation point, full conformance was `ready` with zero failures and 72 warnings, while the live index had 212 entries. The packet's selected reflection still described 210 entries, which is direct evidence that a previously true observation can outlive the digest it described. [`research.md:46-53`; `strategy-inventory-packet.json:97-107`]
- The full validator is a two-file unit: the shell entrypoint calls its sibling Python helper. The consumer package lacks that documented validator pair even though generated native skill packages can contain it. Copying only the shell wrapper is therefore not a portable installation. [`research.md:11-15,206-212`]
- The current appender already owns timestamp input, deterministic append/no-op behavior, canonical bytes, pre-write validation, dry-run, and sequential writes of `index.json` then `index.md`. It treats any existing ID as a no-op without comparing normalized content and emits whole-index warnings rather than operation-attributable warning deltas. [`research.md:16-18,57-71`; `ops/development/2026-07-24-inventory-runtime-research/skeptic-review.md:43-44,103-112`]
- Inventory remains a discovery/read-model surface. Its receipts may prove mechanical lookup or append outcomes; they may not prove truth, semantic authority, precedent-cleanliness, severity, promotion, or approval to mutate. [`research.md:31-32`; `strategy-inventory-packet.json:137-143`]

All runtime behavior below is a selected design. **No Candidate B runtime receipt is cited or admitted by this research. Implementation evidence is pending for every Candidate B state, receipt, manifest, warning-delta, conflict, and postwrite witness.**

## Mandatory verdict matrix

| Candidate | Owner (precedent) | Witnessed? | Sound? | Verdict |
|---|---|---|---|---|
| A — lifecycle bundle | Updater owns append mechanics; validator owns readiness; Inventory `install`/`sync` owns distribution; Inventory owns lookup orchestration. | No standalone runtime witness. Existing components are witnessed, but A's identity/conflict and write-failure contracts are incomplete. | No. It duplicates existing owners, and `partial_projection_gap` contradicts fail-closed human-view conformance. | **KILL standalone.** Retain only its public-canonical/generated-installed/consumer-state boundary as a constraint on B. |
| B — operation wrapper | **Build-from-owned:** reuse updater, full validator pair, and Inventory `install`/`sync`; add only the Inventory-specific causal receipt join. | **No runtime witness.** Design cases were reconciled and substrate tests pass, but no named Candidate B receipt proves the proposed behavior. | Yes at research-design level, conditionally. Its unique responsibility does not collapse into updater, validator, observer, OIL, or distribution ownership. | **KEEP as implementation target; runtime ready/accepted: NO.** Build-from-owned, not precedent-clean; acceptance is withheld pending the named receipts below. |
| C — operator coordinator | Inventory already owns validate/lookup/sync; B owns append attribution; Signal Observer/OIL owns observation. Single-writer locking and durable two-file journal/recovery have no observed owner in the inspected precedent. | Omnibus coordinator: no. Transaction/concurrency slice: no crash or concurrency implementation witness. | Omnibus shape: no. Decomposed transaction-safety responsibility: definitionally sound but unproven. | **DECOMPOSE / DEFER.** Reject the coordinator; retain lock+journal+recovery as a later separately owned slice. |

This disposition follows the durable revised synthesis and skeptic loop, not the initial candidate averaging. [`ops/development/2026-07-24-inventory-runtime-research/synthesis.md:176-190`; `ops/development/2026-07-24-inventory-runtime-research/skeptic-review.md:73-130`]

### Runtime acceptance hold

Research has resolved the candidate design; it has **not** made the runtime ready or accepted. Acceptance requires actual, named, durable, reproducible receipt artifacts—each bound to its exact command, fixture inputs, runtime/helper digests, and observed filesystem digests—proving at least:

1. `package-relative-unrelated-cwd`: the installed package resolves its complete helper bundle and executes from an unrelated working directory without upstream-checkout or `cwd` fallback.
2. `warning-delta-attribution`: a controlled add over inherited debt reports zero introduced warnings, while a one-warning candidate reports exactly one stable introduced warning without reattributing inherited warnings.
3. `deterministic-repeat-dry-run`: two runs over identical canonical inputs emit byte-identical canonical receipts and leave byte-identical filesystem state.
4. `zero-mutation`: dry-run, missing-helper, invalid request, baseline/candidate block, identical no-op, and ID conflict witnesses show unchanged bound projection digests and no changed paths.

These names define required evidence classes; they are not references to receipts that already exist. The skeptic review reconciles expected outcomes but explicitly limits current proof to substrate behavior, not the proposed runtime. [`ops/development/2026-07-24-inventory-runtime-research/skeptic-review.md:41-71`; `ops/development/2026-07-24-inventory-runtime-research/synthesis.md:358-368`]

## Recommended minimal runtime: Candidate B

### Exact unique responsibility

Candidate B owns one deterministic, digest-bound witness of an attempted Inventory append transition:

```text
exact baseline projection bytes
+ exact normalized record
+ supplied timestamp
+ exact validator bundle
→ candidate disposition
+ introduced/resolved/inherited warning delta
+ observed mutation outcome
```

It uniquely joins conflict detection, baseline/candidate validation, helper/input/output digests, warning attribution, and actual postwrite observation into one Inventory-domain receipt. It does **not** own lookup/search orchestration, readiness semantics, install/sync, generic invocation envelopes, telemetry append, reflection routing, transaction recovery, or semantic authority. [`ops/development/2026-07-24-inventory-runtime-research/synthesis.md:184-229`; `ops/development/2026-07-24-inventory-runtime-research/skeptic-review.md:94-114`]

### Commands and states

```sh
# Existing lookup-readiness owner
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

Lookup/search remains with the Inventory sigil. B invokes the complete validator against baseline and candidate but does not introduce a new `lookup`, `validate`, or `doctor` owner. [`ops/development/2026-07-24-inventory-runtime-research/synthesis.md:192-217`]

Exact append states:

- Success: `dry-run-ready`, `applied`, `identical-no-op`.
- Request/tooling blocks: `invalid-request`, `id-conflict`, `tooling-unavailable`.
- Conformance blocks: `baseline-blocked`, `candidate-blocked`.
- Mutation failures: `write-failed`, `postwrite-digest-mismatch`.

The selected contract requires stdout to contain exactly one canonical JSON receipt and stderr to carry diagnostics. A dry run must perform no write. Deterministic receipt content contains no observed wall-clock field; the caller-supplied `timestamp_input` is part of the operation input. These are requirements, not witnessed runtime behavior. [`ops/development/2026-07-24-inventory-runtime-research/synthesis.md:231-245`; `ops/development/2026-07-24-inventory-runtime-research/skeptic-review.md:58-71`]

### Required receipt schema

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

All receipt paths are Inventory-root-relative; private checkout paths must not enter a public artifact or portable receipt. `receipt_sha256` is computed from canonical receipt bytes excluding that field. The schema is normative and does not imply that a conforming receipt exists. [`ops/development/2026-07-24-inventory-runtime-research/synthesis.md:247-305`; `research.md:73-124`]

## Ownership boundaries

| Boundary | Owned content | Mutation rule |
|---|---|---|
| Public canonical — `arcanum/arcana/inventory/` | Generalized appender, receipt emitter/schema, complete validator pair, bundle-manifest schema, focused fixtures, and template/install/sync rules. | Patch canonical public sources first. They must remain generic and contain no private checkout binding or private evidence. |
| Installed generated — `.arcanum/inventory/` runtime payload | `bin/inventory`, `lib/inventory-update.cjs`, `scripts/validate-index-json.sh`, `scripts/validate_projection_conformance.py`, and `runtime-manifest.json`. | Regenerate through existing Inventory install/sync. `sync --check` compares relative paths and digests; `sync --apply` refreshes generated payload only. |
| Consumer-owned mutable state | README/schema, `index.json`, `index.md`, tags, log, entries, queries, raw sources, derived indexes/lint, local vocabulary/configuration, source bindings, receipts, events, and declared overlays. | Never overwritten by runtime synchronization. B may mutate only the intended append projections under `--apply`; it does not acquire authority over their meaning. |

Host-native `.claude`/`.agents` packages remain separately generated mirrors under bootstrap; they are not the host-neutral consumer data package. [`research.md:14-23`; `ops/development/2026-07-24-inventory-runtime-research/synthesis.md:115-138,180-190`]

## Warning delta and conflict behavior

Warnings use stable identities:

```text
warning_id = sha256(code + NUL + subject + NUL + selector)
introduced = candidate_ids - baseline_ids
resolved   = baseline_ids - candidate_ids
inherited  = candidate_ids ∩ baseline_ids
```

IDs are sorted bytewise before set/list digests. The receipt includes full structured `introduced` and `resolved` items, plus `inherited_count` and `inherited_set_sha256`. Full validator reports continue to expose every historical warning; a clean operation receipt does not replay or attribute all inherited warnings to the operation. Uncontrolled tags remain warn-only unless a separately governed closed-vocabulary policy changes that rule. [`research.md:126-142`; `ops/development/2026-07-24-inventory-runtime-research/synthesis.md:113`]

For an existing ID, the selected design requires normalized content equality to yield `identical-no-op`, unchanged projection digests, unchanged `generated_at`, and zero writes. A differing normalized record must yield `id-conflict` and zero writes. Mere ID presence is not idempotence. These outcomes remain unwitnessed in Candidate B. [`research.md:159-166`; `ops/development/2026-07-24-inventory-runtime-research/skeptic-review.md:58-67`]

## Non-atomic writes and currentness limits

The current two projections are written sequentially. MVP staging and postwrite digest checks improve attribution but do not make the write atomic. `committed=true` means both intended projections were subsequently observed at their candidate digests; it does not mean transactional commit. On `write-failed` or `postwrite-digest-mismatch`, the receipt must report attempted write, actual changed paths/digests, `committed=false`, `possible_partial_mutation=true`, `repair_required=true`, and a concrete repair route. It must not claim rollback or success. [`ops/development/2026-07-24-inventory-runtime-research/synthesis.md:307-313`; `ops/development/2026-07-24-inventory-runtime-research/skeptic-review.md:43-44,67-71`]

A receipt is immutable, digest-bound historical evidence. It has no self-updating `currentness` field. Currentness requires a separate verifier to compare the receipt-bound digest with the live `index.json` digest and emit a separate result without rewriting the receipt. Ownership of that verifier is unresolved and outside B. [`ops/development/2026-07-24-inventory-runtime-research/synthesis.md:315-321`; `ops/development/2026-07-24-inventory-runtime-research/skeptic-review.md:65-71`]

## Implementation slices

### MVP

1. Canonicalize B's append engine, receipt schema/serializer, complete validator pair, strict root/helper resolution with no `cwd` fallback, and fixtures.
2. Implement normalized equality/conflict detection, baseline/candidate full validation, warning delta, temporary/in-memory staging, and input/helper/baseline/candidate/postwrite digest binding.
3. Implement explicit partial-mutation reporting, one-receipt stdout, stderr-only diagnostics, and every state fixture.
4. Add the generated bundle manifest and extend existing Inventory `install`/`sync`; prove `sync --check` detects missing or drifted runtime members without touching consumer state.
5. Additively sync one consumer and run the deterministic gates below. Do not alter historical warnings or legacy maps in this slice.

### Later, separately owned

- Single-writer lock.
- Durable two-file journal.
- Crash recovery and explicit recovery application.
- Concurrency, interruption, and recovery fixtures.
- Any atomic-apply claim.

If atomic two-file apply is an acceptance criterion rather than a later hardening goal, this C-derived slice becomes an MVP prerequisite. [`ops/development/2026-07-24-inventory-runtime-research/synthesis.md:323-346,358-368`]

## Deterministic validation gates

No gate below is currently a B implementation pass:

1. From an unrelated `cwd`, package-local helper/root resolution succeeds; missing or mismatched helpers/dependencies produce `tooling-unavailable` and zero writes.
2. Baseline and candidate each run the full coverage, identity, existence, derived-map, human-view, and freshness conformance gate.
3. Controlled append over historical warning set `H` produces zero introduced/resolved warnings and a stable inherited count/digest.
4. One added uncontrolled warning produces exactly one introduced stable warning identity while inherited debt remains unchanged and warn-only.
5. Repeated identical dry runs produce byte-identical receipts and byte-identical filesystem state.
6. Identical existing content produces `identical-no-op`; conflicting content produces `id-conflict`; both perform zero writes.
7. Every supported kind passes and an unsupported kind blocks before mutation.
8. Injected write failure and postwrite alteration produce the exact non-success/partial-mutation fields; neither implies rollback.
9. A receipt bound to digest A remains historical after live digest B; the separate currentness verifier, once owned, reports A≠B without mutating the receipt.
10. `sync --check` precisely reports a missing/drifted manifest member, and `sync --apply` changes generated runtime payload only.
11. Canonical JSON and `operation_fingerprint`/`receipt_sha256` are byte-stable for identical canonical inputs.
12. A boundary scan confirms no private path/evidence in public canonical files, generated payload, or receipt fixtures.

The expected witness outcomes are specified by the explorer and skeptic artifacts, but they remain implementation evidence pending. [`research.md:168-182`; `ops/development/2026-07-24-inventory-runtime-research/synthesis.md:148-161`; `ops/development/2026-07-24-inventory-runtime-research/skeptic-review.md:58-69`]

## Rejected changes

- A standalone lifecycle bundle or new runtime composer.
- C's omnibus `validate`/`lookup`/`append`/`doctor` coordinator.
- New lookup/readiness ownership or query/search synthesis.
- Observer telemetry append, OIL ownership, reflection routing, or maintenance approval inside B.
- Broad `doctor`, generic runtime profile, or auto-repair.
- Tag or duplicate-tag cleanup, legacy `by_evidence_set` migration, replace/update, or historical-debt normalization.
- UI, ingest orchestration, severity policy, provenance truth, ontology, definitions, promotion, or any other semantic authority.
- Silent `cwd` fallback, private checkout binding, or a claim of atomic apply.

These are rejected from B rather than hidden as implied future scope. [`ops/development/2026-07-24-inventory-runtime-research/synthesis.md:163-172,348-356`; `ops/development/2026-07-24-inventory-runtime-research/skeptic-review.md:114-130`]

## Remaining owner decision

The owner must decide whether a **non-atomic but fail-closed, explicitly partial-mutation-reporting MVP** is acceptable. If atomicity is required for acceptance, C's lock/journal/recovery slice must move ahead of B's apply-mode release and obtain concurrency/crash witnesses. Independently, the owner must assign the external digest-currentness verifier before anyone may claim a stored receipt describes current state. [`ops/development/2026-07-24-inventory-runtime-research/synthesis.md:315-321,340-346,358-368`]

## Claim-to-source index

| Claim | Source selector | Proof boundary |
|---|---|---|
| Current validator/updater behavior and package gap | `research.md:11-18,42-71,206-212` | Explorer-reported inspection and live reproduction; not reimplementation proof. |
| Inventory preflight status, 72 warnings, gaps, and non-authority boundary | `strategy-inventory-packet.json:1-14,97-107,125-143` | Discovery projection; explicitly not implementation or promotion authority. |
| A KILL, B KEEP/build-from-owned, C decompose/defer | `ops/development/2026-07-24-inventory-runtime-research/synthesis.md:174-190`; `ops/development/2026-07-24-inventory-runtime-research/skeptic-review.md:73-130` | Reconciled research-design verdict; not runtime acceptance. |
| B commands, unique transition, states, and receipt | `ops/development/2026-07-24-inventory-runtime-research/synthesis.md:192-305` | Selected normative contract; no receipt exists in admitted evidence. |
| Warning identity/delta and conflict behavior | `research.md:126-166`; `ops/development/2026-07-24-inventory-runtime-research/skeptic-review.md:58-67` | Reconciled expected outcomes; Candidate B implementation witnesses pending. |
| Non-atomic failure and stale-currentness limits | `ops/development/2026-07-24-inventory-runtime-research/synthesis.md:307-321`; `ops/development/2026-07-24-inventory-runtime-research/skeptic-review.md:65-71` | Explicit claim ceiling; currentness owner unresolved. |
| MVP/later split and remaining proof boundary | `ops/development/2026-07-24-inventory-runtime-research/synthesis.md:323-368` | Implementation plan, not completed evidence. |
| Deterministic witness matrix | `research.md:168-182`; `ops/development/2026-07-24-inventory-runtime-research/synthesis.md:148-161`; `ops/development/2026-07-24-inventory-runtime-research/skeptic-review.md:45-69` | Required gates; only substrate tests currently witnessed. |
