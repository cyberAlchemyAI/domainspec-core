# TASK-OAVA-RUNTIME-ADMISSION — Exact local Anime.js runtime binding

## Task objective

Provide one deterministic, consumer-owned gate that binds the already-acquired Anime.js `4.5.0` ESM bundle and MIT license to their exact provenance receipts and refuses local runtime admission on any identity, path, byte, receipt, import, or network drift.

Portfolio layer: L1. Captured unit: `SWU-OAVA-003` only.

## Source contracts

- `work-pack/tasks/TASK-OAVA-PROTOTYPE.md#SWU-OAVA-003` — local-only runtime admission requirement.
- `EXECUTION-PACK.md` — W2 entry and `003 → 004 → 005` ordering.
- `stages/06-design.md#Data-and-dependency-boundaries` — local pinned runtime, no runtime fetch, immutable source/vault boundaries.
- `stages/09-plan.md#L1--S6-ten-second-prototype` — admit runtime before scene or timeline work.
- `IMPLEMENTATION-LAYERING-OAVA-003.md` — current L1 slice and deferrals.
- `execution-runs/20260805-b001-animejs-runtime/acquisition-receipt.json` — official package and installed-asset provenance.
- `execution-runs/20260805-b001-animejs-runtime/validation-receipt.json` — passing byte, syntax, header, self-containment, and network checks.
- `execution-runs/20260806-oava002/task-session/governance-terminal-receipt.json` and `work-pack/closeouts/SWU-OAVA-002.json` — completed predecessor.

## Dependencies and blocker state

- `SWU-OAVA-002`: completed and joined.
- `B-001`: resolved with exact current receipts and live byte identities.
- Product/semantic decisions: none.
- B-002 browser discovery and B-003 human reviewer are later-unit gates and do not block runtime admission.

## Primary behavior and atomicity

The unit implements three collaborating pieces as one atomic admission behavior:

1. A closed runtime manifest pins package identity, provenance receipts, local paths, file sizes, hashes, static constraints, and the claim ceiling.
2. A pure/read-only verifier loads that manifest and the two receipts, checks exact live bytes and static source constraints, and returns one stable result without importing Anime.js.
3. Causal tests prove the exact positive case and each one-cause failure while mutating only temporary copies outside the repository.

Plausible children are manifest projection, verifier implementation, and causal tests. The manifest alone is untrusted prose; the verifier without a closed manifest has no stable identity; either without causal tests can fail open. Scene construction and timeline execution have independent acceptance boundaries and therefore remain OAVA-004 and OAVA-005.

## Inputs

- Repository/refinement root supplied by the host, not by the manifest.
- Current B-001 acquisition receipt: 1927 bytes, SHA-256 `57f76981d2b1e885f54a3d30f9d3fd6621f3c0e05cca371bec23f5791acfaf1d`.
- Current B-001 validation receipt: 2089 bytes, SHA-256 `1f657a551cb2ec3f74228fd00f3949a7002417205e7cbd8322971d7f025a2204`.
- Runtime: `prototype/vendor/anime.esm.js`, 408414 bytes, SHA-256 `a88ebfb5bd290f25215692edce71a74c0fc37bdb9e0ff70bd17135c5c3ef33b6`.
- License: `prototype/vendor/LICENSE.animejs.md`, 1075 bytes, SHA-256 `3f3e835a9952cfc2a6ca836fb95b3257c981f24fa3ef51249055acb09931897b`.
- Package identity: `animejs@4.5.0`, MIT, repository `https://github.com/juliangarnier/anime.git`, official npm tarball and integrity fields already captured by B-001.

## Exact material writes

- `prototype/runtime/animejs-runtime-manifest.json`
- `prototype/lib/verify-animejs-runtime.mjs`
- `prototype/test/runtime-admission.test.mjs`

No directory glob is authorized. No project-tree execution output other than the terminal Task Session receipt is authorized.

## Runtime manifest contract

The manifest uses schema version `oava.animejs-runtime-manifest.v1` and is closed at every object level. It contains:

- package name, version, license, repository, registry tarball, registry integrity, tarball SHA-512, and package-json SHA-256;
- exact runtime and license package-member names, repository-relative paths, sizes, and SHA-256 values;
- exact path/size/SHA-256 references for the acquisition and validation receipts;
- constraints `cdn_used=false`, `runtime_network_dependency_added=false`, `auto_update_added=false`, and `repository_package_root_added=false`;
- verification policy requiring relative-contained paths, exact receipts, byte equality, version/license header, no top-level external import, no runtime-network primitive, and no dynamic import/execution;
- claim limit: local provenance-bound runtime admission only.

The manifest cannot choose the repository root, supply an alternate path, loosen verification, or authorize runtime execution.

## Verification algorithm and failure precedence

`verifyAnimeJsRuntime({ manifestPath, refinementRoot })` returns one immutable result and does not mutate inputs or files.

1. Parse the manifest and reject unknown/missing fields or the wrong schema as `MANIFEST_INVALID`.
2. Require the two receipt references to equal the exact approved repository-relative paths, sizes, and hashes; parse their expected schemas as `RECEIPT_INVALID` on any mismatch.
3. Require package name/version/license/repository/tarball/integrity and both installed-asset records to agree across manifest and acquisition receipt; otherwise `PACKAGE_IDENTITY_MISMATCH`.
4. Require validation receipt subject/status and every required check ID to be present with `pass`; otherwise `VALIDATION_RECEIPT_NOT_PASS`.
5. Reject absolute paths, backslashes, traversal, alternate locations, or real paths escaping the refinement root as `RUNTIME_PATH_INVALID`.
6. If the runtime is missing, return `RUNTIME_MISSING`; if size differs, `RUNTIME_SIZE_MISMATCH`; if SHA-256 differs, `RUNTIME_HASH_MISMATCH`.
7. If the license is missing, return `LICENSE_MISSING`; if size differs, `LICENSE_SIZE_MISMATCH`; if SHA-256 differs, `LICENSE_HASH_MISMATCH`.
8. Require the declared Anime.js `v4.5.0` and MIT header; otherwise `VERSION_LICENSE_HEADER_MISMATCH`.
9. Reject a top-level external import/export-from dependency as `RUNTIME_EXTERNAL_IMPORT`.
10. Reject executable-source identifiers `fetch`, `XMLHttpRequest`, `WebSocket`, or `EventSource` after comment stripping as `RUNTIME_NETWORK_PRIMITIVE`.
11. Return `RUNTIME_ADMITTED` only after every gate passes.

The verifier may read text and compute hashes. It must not call `import()`, `eval`, `Function`, process execution, package managers, HTTP clients, or the Anime.js API.

## Expected result shape

```json
{
  "admitted": true,
  "code": "RUNTIME_ADMITTED",
  "runtime": {
    "package": "animejs",
    "version": "4.5.0",
    "path": "prototype/vendor/anime.esm.js",
    "sha256": "a88ebfb5bd290f25215692edce71a74c0fc37bdb9e0ff70bd17135c5c3ef33b6"
  },
  "license": {
    "id": "MIT",
    "path": "prototype/vendor/LICENSE.animejs.md",
    "sha256": "3f3e835a9952cfc2a6ca836fb95b3257c981f24fa3ef51249055acb09931897b"
  },
  "provenance_receipts": [
    "execution-runs/20260805-b001-animejs-runtime/acquisition-receipt.json",
    "execution-runs/20260805-b001-animejs-runtime/validation-receipt.json"
  ],
  "semantic_effect": "none",
  "claim_limit": "local runtime admission only; no runtime execution or conformance proof"
}
```

Negative results set `admitted` to `false`, use exactly one stable code at the earliest failing gate, return no executable runtime handle, and preserve `semantic_effect: none`.

## Causal cases

- Repeated verification against equal inputs returns byte-equivalent results and changes no input.
- The current repository bytes and receipts return exactly `RUNTIME_ADMITTED`.
- Unknown manifest fields, wrong schema, wrong package/repository/tarball/integrity/license/version, and missing required constraints each fail causally.
- Missing/tampered acquisition receipt and missing/tampered/non-pass validation receipt each fail before live asset admission.
- Absolute, traversal, backslash, alternate, and symlink-escape paths fail before file use.
- Missing, size-drifted, and hash-drifted runtime and license copies each return their dedicated code.
- Wrong runtime header, top-level external import, and each forbidden network primitive return their dedicated code.
- CDN or nonlocal runtime locations never become fallbacks.
- Static source scan of the verifier proves no dynamic import, process execution, network client, vendor write, source write, vault write, or Anime.js API invocation.
- Before/after SHA-256 maps for `prototype/vendor/`, the source video package, AutoAds, and the canonical Anime.js vault are identical.

## Validation and acceptance evidence

Run from the refinement-run root:

```text
node --test prototype/test/runtime-admission.test.mjs
node --test prototype/test/consultation.test.mjs
node --test prototype/test/candidate.test.mjs
node --check prototype/vendor/anime.esm.js
```

All obligations are acceptance-critical. Tests may create and remove temporary directories through the operating-system temp facility; they may not write inside the repository beyond the three admitted material files and Task Session evidence outputs.

## Execution owner and handoff

Task Session owns the single-use material execution and terminal evidence. `invoke:refresh:apply-approved` owns closeout synchronization. The terminal handoff may expose exactly `SWU-OAVA-004` with `successor_executed=false`; it may not create DOM/SVG or execute Anime.js.

Expected execution-owner result shape:

```yaml
swu_id: SWU-OAVA-003
result: pass | flag | block | interrupted
capability_ref: task-session
receipt_kind: native-stage | local-fallback | blocked
receipt_artifact: <task-session terminal receipt or none>
files_touched:
  - <only the three admitted material paths>
validation:
  - <each declared command and result>
blockers:
  - <blocker or none>
residue:
  - <noncritical residue or none>
reroute: invoke:refresh:apply-approved | none
handoff_note: <closeout and successor boundary>
```

