# TASK-WCP-01: Input closure

## Objective and layer

Close the exact external package/source boundary and then freeze the independent
fixture/codec constants. Layer L0, slice S-WCP-01, wave W0.

## Sources

- `../../WORK-PACK.md`
- `../../../design/ARCHITECTURE.md#provenance-gate-algorithm`
- `../../../../../findings.md#wp-0--freeze-inputs-and-environment`
- `../../../../../research.md` frozen L0/C0 fixture

## SWU-WCP-001: exact package/source provenance

- Selected: yes.
- Primary behavior: decide whether one exact WaveDB package artifact corresponds
  to one reviewed source tree.
- Inputs: registry metadata, tarball, SRI/SHA-1, declared gitHead, reviewed
  commit, source archives, local Node/npm/OS/compiler identities.
- Algorithm: download without install; verify registry hashes; resolve both
  commits; compare version metadata; compare every shipped binding/core source
  byte under an explicit line-ending rule; emit pass only for a single
  non-contradictory identity.
- Edge/failure cases: missing commit, stale gitHead, version mismatch, tarball
  hash mismatch, normalized-only similarity, unavailable toolchain. All block.
- Write scope: `experiment/execution/wp0-provenance/**` and
  `experiment/execution/task-sessions/SWU-WCP-001/**`; Work Pack status fields
  only through closeout.
- Forbidden: dependency resolution, install scripts, native compile, addon load,
  Craft mutation, broad cleanup.
- Done: exact terminal receipt records evidence, verdict, zero install/build
  artifacts, blocker and unique successor/stop.
- Validation: re-fetch metadata; hash tarball; inspect source package versions;
  compare tree manifests; scan target for `node_modules`, `.node`, and build
  artifacts.
- Execution owner: Task Session local.

## SWU-WCP-002: fixture and codec freeze

- Selected: no; depends on SWU-WCP-001 pass.
- Primary behavior: independently materialize exact parser/serializer pins,
  L0/C0, S0/I0, key/value payload manifests, counts, and H_L/H_S/H_P/H_I/H_C.
- Algorithm: extract frozen fixture blocks; validate Craft references; parse
  under exact options; canonicalize; enumerate all allowed keys; compile twice
  from clean inputs; compare every byte and digest.
- Edge/failure cases: parser coercion drift, missing/extra key, wrong ordering,
  newline drift, duplicate ID/reference, manifest self-reference. All block.
- Write scope: `experiment/runtime/fixtures/**`,
  `execution/wp0-fixture/**`, and session evidence.
- Done: two independent compilations produce byte-identical manifests and the
  frozen H_L/H_C constants match research.
- Validation: fixture compiler/validator twice plus source digest audit.
- Execution owner: Task Session local.

## Split analysis

Provenance and fixture closure can pass/fail independently and are therefore
separate SWUs. Parser pinning and fixture constants remain together because
each constant is meaningless without its exact parser/serializer contract.
