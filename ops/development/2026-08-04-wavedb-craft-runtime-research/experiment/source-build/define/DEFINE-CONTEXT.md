# Define context receipt

- Task: author a separately authorized WaveDB reviewed-source build route.
- Context Builder mode: `standard`, strict.
- Files selected: 10.
- Obligation coverage: 8/8 (`100%`).
- Noise ratio: `0.00`; every selected source closes a named obligation.
- Runtime handoff: none at Define.
- Readiness: `ready` for Design; not build admission.

## Obligations and selected evidence

| ID | Obligation | Evidence selector | Status |
| --- | --- | --- | --- |
| D1 | Preserve the user's exact route authorization | current user answer plus `../../execution/decisions/PACKAGE-PROVENANCE.md#opt-redesign-source-build` | covered |
| D2 | Bind one immutable reviewed source tree | `../../../findings.md#immutable-source-identity`; WaveDB root commit and `.gitmodules` | covered |
| D3 | Bind the exact Node dependency graph | reviewed `bindings/nodejs/package-lock.json` root and direct dependency records | covered |
| D4 | Define the generated-source boundary | reviewed `bindings/nodejs/scripts/copy-sources.js` | covered |
| D5 | Define build/toolchain behavior | reviewed `package.json`, `binding.gyp`, and `scripts/build.js` | covered |
| D6 | Preserve Craft authority | parent `define/SPEC.md#what-this-module-owns` and Inventory WaveDB result `#authority-boundary` | covered |
| D7 | Preserve the npm failure instead of rewriting history | `../../execution/wp0-provenance/HISTORY-RECONSTRUCTION.md#gate-effect` | covered |
| D8 | Require an auditable execution handoff | Invoke Plan and Task Session contracts | covered |

## Excluded candidates

- WaveDB `master`: excluded because a moving branch cannot bind this build.
- npm `latest`: excluded as the build source because it is the already-blocked
  artifact, retained only as historical provenance evidence.
- `arcanum/development/craft/`: excluded from semantic authority; historical
  comparison only.
- Real `.craft/` workspaces: excluded because the source-build SWU needs no
  Craft data.

## Authority precedence

User authorization controls route choice; the parent Work Pack controls the
experiment boundary; reviewed Git bytes control source facts; WaveDB build
scripts control build mechanics; canonical Craft contracts control Craft
authority. Inventory is discovery evidence only.
