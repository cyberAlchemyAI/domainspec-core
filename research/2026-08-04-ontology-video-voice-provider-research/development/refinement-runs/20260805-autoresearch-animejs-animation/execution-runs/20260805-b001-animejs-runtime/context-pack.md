# Runtime Handoff Pack

## Identity

- Task/SWU: `B-001 dependency acquisition`
- Source task/work-pack: `../../WORK-PACK.md#B-001`
- Session/run id: `20260805-b001-animejs-runtime`
- Session evidence path: `execution-runs/20260805-b001-animejs-runtime`
- Runtime handoff: `runtime`
- Repository revision: `ab46061bf14db23a01054c2fd3fafec60fb5eb2f`
- Evidence date: `2026-08-05`

## Obligation Coverage

| Obligation | Status | Selected Evidence | Resolution |
| --- | --- | --- | --- |
| `OB-001` | `covered` | `../../WORK-PACK.md#Blockers` | Acquire the separately authorized exact Anime.js v4.5.0 bytes. |
| `OB-002` | `covered` | `../../work-pack/tasks/TASK-OAVA-PROTOTYPE.md#SWU-OAVA-003` | Admit only a local asset; no CDN, package auto-update, implicit install, or runtime network. |
| `OB-003` | `covered` | `https://registry.npmjs.org/animejs/-/animejs-4.5.0.tgz` | npm `latest` resolves to 4.5.0 with the recorded registry integrity and shasum. |
| `OB-004` | `covered` | `package/dist/bundles/anime.esm.js` and `package/LICENSE.md` | Vendor the self-contained ESM bundle and the package's MIT license. |
| `OB-005` | `resolved` | `../../WORK-PACK.md#SWUs` | This run resolves B-001 only; OAVA-003 manifest, validator, and test remain a later admitted SWU. |

Strict coverage: `pass`

## Selected Sources

- `../../WORK-PACK.md`
  - Selectors: `SWUs`, `Blockers / unresolved dependencies`
  - Obligations: `OB-001`, `OB-002`, `OB-005`
  - Evidence excerpt: OAVA-003 expects `prototype/vendor/anime.esm.js`; B-001 requires exact v4.5.0 bytes plus origin, license, path, and SHA-256 with no CDN.
- `../../work-pack/tasks/TASK-OAVA-PROTOTYPE.md`
  - Selector: `SWU-OAVA-003`
  - Obligations: `OB-002`, `OB-005`
  - Evidence excerpt: no CDN, package auto-update, implicit install, or runtime network.
- `../../../../../../../projects/animejs/ontology/agent-knowledge-vault/README.md`
  - Selector: `Version context`
  - Obligations: `OB-003`
  - Evidence excerpt: the ontology snapshot is pinned to Anime.js v4.5.0.
- `https://registry.npmjs.org/animejs/-/animejs-4.5.0.tgz`
  - Selectors: npm registry metadata and package members `package.json`, `dist/bundles/anime.esm.js`, `LICENSE.md`
  - Obligations: `OB-003`, `OB-004`
  - Evidence excerpt: package `animejs@4.5.0`, MIT, zero package dependencies; registry integrity `sha512-NQimYX+lz8WaXonGS9zVVoviCIAjONeJayxacUditaivYLqyXgGjFKjuyl0aUUhFKm5MriX9ty1TGovNzoJQWA==`.

## Architecture Guidance

The dependency is a candidate-local vendored runtime input. It does not become ontology authority, prove animation behavior, or complete OAVA-003.

## Related Feature Context

The ontology snapshot and the package both resolve to v4.5.0, so no version refresh or compatibility decision is required.

## Constraints And Non-Goals

- Preserve exact upstream bytes.
- Keep runtime use offline; do not add a CDN or runtime network dependency.
- Do not add a repository package root or dependency lockfile for this acquisition.
- Do not claim OAVA-003 complete in this run.
- Do not alter the ontology snapshot.

## Write Scope

- `../../prototype/vendor/anime.esm.js`
- `../../prototype/vendor/LICENSE.animejs.md`
- `./acquisition-receipt.json`
- `./context-pack.md`
- `./context-pack.json`
- `./validation-receipt.json`

## Validation Surface

- Verify tarball SHA-512 against npm registry integrity.
- Verify vendored files byte-for-byte against the unpacked package.
- Verify ESM header reports v4.5.0 and MIT.
- Verify no URL or dynamic network primitive appears in the vendored bundle.
- Verify recorded SHA-256 values against installed files.

## Gaps And Blockers

- None for B-001 acquisition.
- OAVA-003 remains dependent on OAVA-002 and separate Task Session admission.

## Authority Precedence

1. User authorization to install the latest release.
2. Work Pack B-001 and OAVA-003 constraints.
3. Official npm registry package metadata and bytes.
4. Ontology vault version context.

## Fallback Exploration Rule

Broad repository exploration is allowed only for obligations listed in `Gaps And Blockers` or for a gap explicitly named before exploring. Extra sources must be reported in the runtime result.

## Provenance

- Source refs: `WORK-PACK.md:18-33`; `TASK-OAVA-PROTOTYPE.md:3-5`; vault `README.md` version context; official npm package metadata and tarball.
- Content hashes: Work Pack `7d064d9b56e59c94db31650f06e6d318738b3e64cb9a344ce9f70a9d6b2eb87d`; task `7e840bff126055a29d2389b835a99fe428cc128b977f22554993f29aeb7ea7cf`; vault README `fce7b1a7ad13846c03861138b92a7e38d08294066b92fd622e0d50339306d83b`.
- Builder mode: `lean`

## Output Paths

- Markdown: `execution-runs/20260805-b001-animejs-runtime/context-pack.md`
- JSON/index: `execution-runs/20260805-b001-animejs-runtime/context-pack.json`
