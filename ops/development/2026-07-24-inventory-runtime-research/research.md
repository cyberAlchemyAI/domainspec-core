# Inventory Runtime Improvement Research Transcript

Verbatim explorer returns from dispatch
`2026-07-24-inventory-runtime-improvement`. These returns are evidence inputs,
not accepted findings or implementation authority.

## Agent 1 — Ashby, W. Ross

Ashby contract archaeology (read-only). Evidence and inference are separated; Inventory remains a non-authority read model.

**Evidence — present ownership and gaps**
- Public canonical owner is `arcanum/arcana/inventory/`: the sigil requires machine-index-first lookup and the package-relative gate, with any source-coverage/identity/existence/map/human/freshness failure blocking readiness (`arcanum/arcana/inventory/SKILL.md:112-123`, `:230-241`). The gate is a two-file unit: shell calls sibling Python (`arcanum/arcana/inventory/scripts/validate-index-json.sh:99-104`), so copying only the wrapper is invalid.
- The public validator already returns the essential lookup receipt: `lookup_readiness`, `index_sha256`, per-check errors/warnings, and counts (`arcanum/arcana/inventory/scripts/validate_projection_conformance.py:383-402`); projection freshness is digest- and generated-at-bound (`:314-363`). Tags are deliberately warn-only in this implementation (`:365-381`).
- The default consuming package is `.arcanum/inventory/`, whose declared/template layout omits `scripts/` and `tools/` (`arcanum/arcana/inventory/SKILL.md:37-56`; `arcanum/arcana/inventory/templates/package-readme.md:7-23`). The live package indeed has `tools/` but no `scripts/`; the reflection records that portability defect and the incomplete-one-file-copy risk (`.arcanum/observability/reflections/20260724T152503Z-inventory-maintenance-reflection.md:83-90`).
- Do not invent a runtime composer. Bootstrap already copies every support directory except `development/`, explicitly including `scripts`, into generated native skill packages (`arcanum/tools/bootstrap_arcanum.sh:821-875`), and generated mirrors record canonical source plus regenerate-only policy (`arcanum/tools/bootstrap_arcanum.sh:795-806`; live proof `.claude/skills/inventory/SKILL.md:1-15`). Thus `.claude/skills/inventory/scripts/` exists; the missing surface is the host-neutral consuming data package, not the native skill package.
- Existing append implementation is consuming-repo-owned: `.arcanum/inventory/tools/inventory-update.cjs`. It requires an input timestamp, is append-only/idempotent, and canonicalizes bytes (`.arcanum/inventory/tools/README.md:13-30`; implementation `.arcanum/inventory/tools/inventory-update.cjs:136-163`). Invalid input blocks before write (`:315-349`); candidate validation runs before mutation (`:364-374`); dry-run does not write and changed writes occur at `:376-394`.
- Current warning attribution is not operation-specific: validation scans every entry and deduplicates unknown tags globally (`.arcanum/inventory/tools/inventory-update.cjs:181-215`), then prints all warnings after each changed add (`:364-369`). Reflection confirms this repeatedly conflates package debt with invocation quality (`.arcanum/observability/reflections/20260724T152503Z-inventory-maintenance-reflection.md:72-81`).
- Current local appender carries explicit historical debt/boundaries: 13 legacy `by_evidence_set` keys are left untouched (`.arcanum/inventory/tools/README.md:32-35`); unknown path prefixes update JSON but require manual human-row handling, and human `Last updated` remains human-owned (`:37-51`); migration and replace are deferred (`:71-75`). This must remain visible, not be silently normalized during genericization.

**Inference — smallest generic runtime boundary**
1. Public canonical runtime payload should contain only: (a) the existing complete lookup-validator pair; (b) a generalized deterministic append engine derived from the local updater; (c) a thin receipt emitter/schema covering both operations; (d) focused fixtures. No ontology/definition/promotion logic, historical cleanup, query synthesis, or UI.
2. Consuming repository owns all mutable/contextual state: `.arcanum/inventory/{README,schema,index.md,index.json,tags.md,log.md,entries,...}`, local projection configuration, raw sources, controlled vocabulary policy, local append records, observability events, and declared overlays. Package-local runtime files should be generated copies with canonical digest/provenance, never locally edited authority.
3. Reuse Inventory `install`/`sync` as the data-package installer/synchronizer (modes already exist at `arcanum/arcana/inventory/SKILL.md:26-35`, install steps `:59-84`), and reuse bootstrap’s support-copy mechanism for host-native skill mirrors. Add `scripts/` (validator pair + append runtime/receipt schema) to default templates/install/sync. A small manifest should bind copied runtime files to canonical digests; `sync` reports drift and refreshes only generated runtime payload, never consumer data.
4. One runtime, two verbs is enough: `lookup` (read-only) and `append` (`--dry-run` or apply). Higher-level ingest/query/lint remains agent orchestration, not deterministic runtime.

**Proposed invocation states/receipt**
- Shared: `tooling_blocked` (missing jq/python/node/helper), `invalid_input`, with zero mutation.
- Lookup: `inventory_unavailable` / `machine_index_gap` / `human_fallback` as explicit residue; `blocked` on any conformance failure; `ready` with validator path+digest, timestamp, `index_sha256`, `generated_at`, warning/failure counts. Existing strategy semantics make unavailable/no-match nonblocking discovery residue, never proof (`.arcanum/inventory/entries/domainspec-subagents-research-review-inventory-preflight-synthesis.md:77-85`).
- Append: `rejected` before mutation; `dry_run_changed`; `applied`; `already_present`; `human_projection_repaired`; `partial_projection_gap` only if JSON changed but an intentionally unsupported human row remains explicit. Receipt must bind baseline/candidate/final index digests, supplied timestamp, record ID/path, `mutation_status`, files changed, introduced-warning set, inherited-warning count/digest, full post-state readiness, and residue. Reflection’s exact desired delta semantics are `:121-139`, deterministic witnesses `:166-180`.

**Authority exclusions**
- Raw sources remain immutable; material claims cite sources or are labeled inference/synthesis/open (`arcanum/arcana/inventory/SKILL.md:318-322`). Inventory owns read models/lint/handoffs only; Ontology Vault owns governed meaning/promotion and Definitions Governance owns canonical definitions (`:318-322`). EvidenceSets cannot imply ontology, definition, ledger, or Context Builder authority (`:257-269`). Runtime receipts prove mechanical lookup/append outcomes only, never truth, precedent-cleanliness, severity, or promotion (`.arcanum/inventory/entries/domainspec-subagents-research-review-inventory-preflight-synthesis.md:55-75`).

**Compatibility risks**
- Three dependencies (jq, Python, Node) reduce portability; either declare all and fail precisely, or implement append in Python to reduce to jq+Python. Do not silently fall back.
- Two installed locations (`.claude/.agents/.../inventory/scripts` and `.arcanum/inventory/scripts`) can drift; digest manifest + sync is mandatory. Runtime overlays are additive only and cannot replace canonical controls (`arcanum/runtime/overlays/README.md:3-15`).
- Promoting the local updater verbatim would freeze repo-specific debt and its weaker self-check (duplicate IDs/by_id/generated_at/tags only). Generic append should preserve its deterministic semantics but run the full candidate/post-state conformance gate.
- Full candidate validation may expose already-stale projections; classify inherited failure separately but do not claim applied lookup readiness. Never weaken conformance or migrate the 72 warnings in this slice (`.arcanum/observability/reflections/20260724T152503Z-inventory-maintenance-reflection.md:182-207`).

## Agent 2 — Spivak, David

## Finding

The smallest generic runtime is a deterministic **operation wrapper** around the existing appender plus the complete two-file conformance validator. It should add structured receipts, warning-delta attribution, digest binding, and conflict detection—not new Inventory authority or historical cleanup.

Live reproduction:

- Appender tests: 9/9 groups pass.
- Markdown tests: 7/7 pass.
- Conformance fixtures: 10/10 pass.
- Dry run: exit `0`, unchanged index/Markdown digests, but 72 inherited warnings emitted.
- Live conformance: `ready`, 0 failures, 72 warnings, index digest `6ccb0d…c7f`.
- Reflection’s “210 entries” is already historical; the inspected live index had 212 before the candidate dry run.

## Current behavior vs proposal

**Current**

- Timestamp-input, canonical serialization, append-only map updates, and byte-stable repeat behavior exist.
- Any existing ID is silently treated as `already-present`, without comparing record content.
- Appender validation checks duplicate IDs, `by_id`, `generated_at`, and uncontrolled tags only.
- Full conformance separately checks source coverage, identity, existence, exact derived maps, human projection, and freshness.
- No structured append receipt exists; stderr conflates candidate warnings with inherited debt.
- Installed `.arcanum/inventory/scripts/` validator pair is absent.

**Proposed**

- Package the appender and both validator files.
- Run baseline validation, construct candidate in memory/staging, run candidate validation, compute warning delta, then optionally commit.
- Keep full historical warnings in validator reports; summarize them in operation receipts.
- Reject same-ID/different-content as `id-conflict`.

## Exact receipt schema

```json
{
  "schema_version": "inventory.operation-receipt.v1",
  "operation_fingerprint": "sha256(canonical operation inputs)",
  "mode": "dry-run|apply",
  "operation": "add",
  "timestamp_input": "ISO-8601",
  "inventory_root": ".arcanum/inventory",
  "inputs": {
    "index": {"path":"index.json","sha256":"..."},
    "human_index": {"path":"index.md","sha256":"..."},
    "record": {"path":"...","sha256":"...","normalized_sha256":"..."},
    "validator": {
      "entrypoint":"scripts/validate-index-json.sh",
      "bundle_sha256":"sha256(canonical ordered file-path/file-digest list)"
    }
  },
  "baseline": {
    "report_sha256":"...",
    "index_sha256":"...",
    "lookup_readiness":"ready|blocked",
    "failure_count":0,
    "warning_count":72
  },
  "candidate": {
    "disposition":"added|identical-no-op|id-conflict",
    "index_sha256":"...",
    "human_index_sha256":"...",
    "report_sha256":"...",
    "lookup_readiness":"ready|blocked"
  },
  "warning_delta": {
    "introduced":[],
    "resolved":[],
    "inherited_count":72,
    "inherited_set_sha256":"..."
  },
  "write": {
    "attempted":false,
    "committed":false,
    "postwrite_index_sha256":null,
    "postwrite_human_index_sha256":null
  },
  "status":"dry-run-ready",
  "authority_boundary":"inventory-read-model-only",
  "receipt_sha256":"sha256(canonical receipt excluding receipt_sha256)"
}
```

All paths are inventory-root-relative; no checkout-specific absolute paths enter the portable receipt.

## Warning-delta algorithm

Represent each warning by stable identity:

```text
warning_id = sha256(code + "\0" + subject + "\0" + selector)
```

Sort IDs bytewise, then:

```text
introduced = candidate_ids - baseline_ids
resolved   = baseline_ids - candidate_ids
inherited  = candidate_ids ∩ baseline_ids
```

Emit full structured details for `introduced` and `resolved`; emit `inherited_count` plus the digest of the sorted inherited-ID list. This keeps debt visible without replaying 72 unrelated lines. Uncontrolled tags remain warn-only unless the repository separately declares closed-vocabulary blocking.

## Status/failure states

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

Only `applied` and `identical-no-op` are successful apply outcomes. `ready` means lookup-ready read model, never authoritative truth or promotion.

## Idempotence rules

- Same baseline bytes + normalized record + timestamp + validator bundle ⇒ identical candidate bytes and semantic receipt.
- Existing ID with identical normalized entry ⇒ byte-identical no-op; do not bump `generated_at`.
- Existing ID with different normalized entry ⇒ fail `id-conflict`; never hide it as idempotence.
- Dry runs never mutate.
- After apply, rerun produces `identical-no-op` under the same `operation_fingerprint`; output files remain byte-identical.
- Receipt validity is digest-bound: dry-run/no-op binds current files to baseline digests; apply binds them to candidate/postwrite digests.

## Deterministic fixture matrix

| Fixture | Required result |
|---|---|
| Historical unknown tags + controlled add | ready; 0 introduced; stable inherited count/digest |
| Same baseline + one new unknown tag | ready; exactly 1 introduced |
| Repeated dry run | identical output/receipt; no file changes |
| Identical existing ID | `identical-no-op` |
| Conflicting existing ID | `id-conflict`; no mutation |
| Seven accepted kinds / unsupported kind | all accepted / blocked before mutation |
| Missing shell, Python, or `jq` | `tooling-unavailable` |
| Each conformance dimension drift | `candidate-blocked` with exact failing check |
| Stale projection digest/timestamp | freshness blocked |
| Receipt digest A after index becomes B | receipt A historical, never current |
| Apply interrupted/postwrite mismatch | fail closed; no success claim |

## Exact selectors

- Appender determinism and deferred debt: `.arcanum/inventory/tools/inventory-update.cjs:10-22`
- Normalization: `inventory-update.cjs:76-115`
- Existing-ID blind no-op: `inventory-update.cjs:136-159`
- Narrow validator/warning scan: `inventory-update.cjs:165-215`
- CLI dry-run/write behavior: `inventory-update.cjs:315-394`
- Lookup wrapper: `arcanum/arcana/inventory/scripts/validate-index-json.sh:99-112`
- Conformance checks/report: `validate_projection_conformance.py:170-263`, `265-306`, `308-402`
- Current deterministic tests: `.arcanum/inventory/tools/test/test-inventory-update.cjs:46-179`, `182-239`
- Causal conformance fixtures: `arcanum/arcana/inventory/development/test_projection_conformance.py:99-200`
- Proposed warning/digest requirements: `.arcanum/observability/reflections/20260724T152503Z-inventory-maintenance-reflection.md:121-180`
- Explicit authority/debt exclusions: same reflection `182-207`

## Agent 3 — Wiener, Norbert

## Wiener return: smallest operator-portable Inventory runtime

### Verdict

The smallest defensible runtime is a **deterministic coordinator over existing Inventory mechanics**, not a renamed validator/updater and not a new authority layer. Its unique job is to bind an operation to an installed package root, exact helper paths, baseline/candidate digests, warning attribution, mutation outcome, and observer handoff.

Current gaps are structural:

- The public contract requires `<inventory-root>/scripts/validate-index-json.sh`, but the default package layout omits `scripts/` entirely (`arcanum/arcana/inventory/SKILL.md:37-56`; `arcanum/arcana/inventory/templates/package-readme.md:7-23`).
- Canonical skill generation copies runtime support directories (`arcanum/tools/bootstrap_arcanum.sh:821-875`), so host skill packages can contain both validator files, but nothing installs them into `.arcanum/inventory/scripts/`.
- The shell validator resolves a sibling Python helper (`arcanum/arcana/inventory/scripts/validate-index-json.sh:99-104`); copying only the shell file is incomplete.
- The deterministic appender exists only in this consumer at `.arcanum/inventory/tools/`, not canonical Inventory. It validates and writes `index.json` and `index.md` sequentially, without a receipt or transaction journal (`.arcanum/inventory/tools/inventory-update.cjs:339-394`).
- Path resolution is not fail-closed: the conformance helper falls back to `cwd` when declared-root derivation fails (`arcanum/arcana/inventory/scripts/validate_projection_conformance.py:59-67`).

### Smallest CLI/profile surface

Install one package-local executable:

```text
.arcanum/inventory/bin/inventory
.arcanum/inventory/lib/inventory-update.cjs
.arcanum/inventory/lib/validate-index-json.sh
.arcanum/inventory/lib/validate_projection_conformance.py
.arcanum/inventory/runtime-profile.json
```

Expose only:

```text
inventory validate [--json]
inventory lookup --query <text> [filters...] [--json]
inventory append --record <json> --timestamp <ISO-8601> [--dry-run] [--json]
inventory doctor [--json]
```

No generic `observe` verb: emit a receipt that the existing Signal Observer may consume. Observation is non-authority and must not change the primary result (`arcanum/arcana/signal-observer/SKILL.md:82-90`).

No automatic `repair` verb: `doctor` returns a bounded repair plan and exact approved `inventory sync` route. Auto-repair would hide provenance and compete with install/sync ownership. The one exception is interrupted local transaction recovery, admitted only from an exact runtime journal and requiring explicit `--apply`.

### Resolution and dependency contract

- Resolve the Inventory root from the executable’s own location; `--root` may override only after canonicalization and containment checks.
- Derive repository root from declared `index.json.inventory_root`; mismatch blocks. Never fall back to `cwd`.
- Bind helper digests/version in `runtime-profile.json`; missing or mismatched sibling blocks.
- Preflight `bash`, `jq`, `python3`, and `node` before any operation. Preserve the existing tested updater instead of rewriting it merely to reduce runtimes.
- `append` acquires a package-local single-writer lock, validates baseline, stages candidate JSON/Markdown, validates candidate, then commits with a recoverable journal. Baseline failures block; historical warnings do not.

### Fail-closed operator messages

Use stable reason codes plus concrete paths:

- `runtime_incomplete`: expected helper, resolved runtime root, profile version, `inventory sync --check`.
- `dependency_missing`: executable, consumer helper, searched `PATH`, no mutation.
- `inventory_root_mismatch`: declared root, resolved root, repository boundary.
- `baseline_invalid`: index digest, failed conformance classes, no mutation.
- `candidate_invalid`: candidate digest, failures, no mutation.
- `transaction_incomplete`: journal path, committed files, exact recovery command.
- `lookup_blocked`: conformance verdict and failed subchecks; never return matches as ready.
- `inventory_unavailable` / `no_inventory_match`: explicit non-mutating residues, consistent with maintenance lookup behavior (`arcanum/spells/sigil-maintenance-loop/README.md:104-127`).

### Receipt UX

Stdout should be one deterministic JSON receipt; diagnostics go to stderr. Persist only when the caller explicitly requests a path, so lookup remains read-only.

Required fields:

```text
schema, operation, status, reason_code, non_authority_notice
inventory_root, runtime_profile, helper_paths, helper_digests
baseline_index_sha256, candidate_index_sha256
lookup_readiness, validation_checks
introduced_warnings[], inherited_warning_count
mutation_requested, mutation_status, changed_paths[]
timestamp_input, operation_fingerprint
observer: {status, ledger_ref, residue}
```

`validate` reports every historical warning. `append` prints only newly introduced warning lines plus one stable inherited count. That preserves debt without attributing all 72 warnings to every clean operation, exactly the observed failure (`.arcanum/observability/reflections/20260724T152503Z-inventory-maintenance-reflection.md:70-108,121-152`).

### Installation/sync migration

1. Canonicalize coordinator, updater, validator pair, profile, and focused tests under public `arcanum/arcana/inventory/`.
2. Extend default package/template contract with `bin/`, `lib/`, and profile.
3. Inventory `install` copies the exact runtime bundle; `sync --check` compares manifest digests; mutation still requires proposed/approved sync.
4. Existing repositories continue using current indexes unchanged; first sync is additive.
5. Do not migrate 72 historical tags, four duplicate tag names, or legacy `by_evidence_set` keys in this slice (`.arcanum/inventory/tools/README.md:32-35,71-74`; reflection lines 101-108,182-195).
6. Regenerate host skill surfaces from canonical source; never hand-edit generated copies (`.claude/skills/inventory/SKILL.md:1-15`).

### Portability falsification matrix

- Fresh install from unrelated `cwd`; package-local validate passes.
- Missing Python helper, missing `jq`, missing Node: precise block, zero writes.
- Declared/resolved root mismatch and path escape: block.
- Clean add over two historical unknown tags: zero introduced, stable inherited count.
- Add one new unknown tag: exactly one introduced warning, warn-only under open vocabulary.
- Unsupported kind: block before mutation (existing witness: `.arcanum/inventory/tools/test/test-inventory-update.cjs:160-239`).
- Repeated dry-run: byte-identical receipt/output and filesystem.
- No-op append: unchanged digest and explicit `mutation_status=no-op`.
- Crash between staged projections: journal detected; lookup/append block until explicit recovery.
- Conformance regressions for source coverage, identity, existence, maps, human view, freshness (`arcanum/arcana/inventory/development/test_projection_conformance.py:99-200`).
- Observer absent/failing: receipt records residue; primary operation unchanged.
- Digest A failure followed by digest B pass: A is historical, never current (`reflection:154-180`).

The authority boundary remains unchanged: Inventory owns read models and evidence projections, not governed meaning or promotion (`arcanum/arcana/inventory/SKILL.md:318-337`).
