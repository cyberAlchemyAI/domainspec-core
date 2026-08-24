# Architecture: reviewed-source WaveDB build

## Architecture intent

Produce one locally verifiable WaveDB Node addon from a single reviewed Git
tree without treating that addon as a registry package, a supported release,
or a Craft runtime decision. Every build input and output is hash-bound, all
bulky state stays in an ignored disposable work area, and the parent experiment
can consume the result only through a separate Invoke Refresh.

## Closed scope

- Target: `wavedb-reviewed-source-build`.
- Root source commit:
  `01c77e8b70f71de9b72480e73a3a179f6e93a009`.
- Design manifest digest:
  `2ccc27373c388cea6d1ed8cfac8502968f43fcd805d74035993b83813fb246f0`.
- Denominator receipt digest:
  `20536742cd4149143a2a10180d9363f1a8b993c86cf5011f2e6f52c6cde2bb5c`.
- Selection result digest:
  `2817bca9ae6921725b8aa64c6192f1141dd2a9acf164ac5e1f0c93ce9a28bfe9`.
- Evidence state: `design-validator-pass`.
- Plan evidence: `plan-evidence-pending`.

## View 1: Context

```text
reviewed WaveDB Git identity
  + recursive submodule identities
  + package-lock and build scripts
                |
                v
       source-build Task Session
        in source-build/.work/
                |
                v
   source/dependency/build/test receipts
                |
                v
       SourceBuildReceipt ----------> parent Invoke Refresh
                                              |
                                              v
                              parent experiment may admit or block

Craft source and real ledgers -------------------- never read or written
npm registry package ----------------------------- never repaired or published
```

Owners remain distinct. WaveDB Git owns upstream source facts. Invoke owns this
authoring package. Task Session owns one bounded local execution. The parent
experiment owns any later consumption decision. Craft and publication owners
retain their existing authority.

## View 2: High-level structure

| Component | Responsibility | Authority/effect |
| --- | --- | --- |
| Source resolver | Materialize exactly the reviewed root commit and recursive submodules | May fetch source; cannot select a different revision |
| Source manifest builder | Enumerate tracked paths, modes, Git objects, file digests, submodules, lockfile, and build scripts | Evidence only |
| Dependency materializer | Run lockfile-driven `npm ci --ignore-scripts` | Writes only ignored `node_modules`; blocks on drift/failure |
| Generated-source verifier | Run `copy-sources.js` and digest complete `c_src` | Writes only ignored checkout; no upstream edit |
| Native builder | Run the reviewed build script with explicit OpenSSL configuration | Produces local platform-specific build output |
| Test controller | Load addon, run upstream Node tests and empty-value canary against temporary stores | Observation only; first failure blocks |
| Evidence writer | Emit exact JSON manifests, logs, terminal receipt, and claim ceiling | Filesystem receipt owner; no registry/Craft authority |
| Parent handoff | Bind the terminal receipt and addon digest for Invoke Refresh | Cannot update parent plan by itself |

## View 3: Low-level components

### Source closure algorithm

1. Require the work-area target to be absent before the attempt.
2. Clone or materialize the upstream repository into
   `source-build/.work/wavedb` without using a moving branch as identity.
3. Checkout detached root commit `01c77e8b...`.
4. Initialize recursive submodules and require every checked-out submodule SHA
   to equal the superproject-pinned gitlink, including nested submodules.
5. Require an empty tracked status before dependency writes.
6. Enumerate tracked root files and recursively tracked submodule files. Record
   repository-relative path, Git mode/object, byte size, SHA-256, and one
   canonical aggregate digest.
7. Bind the reviewed `package.json`, `package-lock.json`, `binding.gyp`,
   `scripts/build.js`, and `scripts/copy-sources.js` digests separately.

### Dependency closure algorithm

```text
cd bindings/nodejs
npm ci --ignore-scripts --no-audit --fund=false
npm ls --all --json
```

The exact lockfile is controlling. `npm install`, semver-only resolution,
package substitution, lifecycle scripts during materialization, and lockfile
rewrite are forbidden. Registry tarball integrity failures or an unavailable
dependency block the attempt.

### Build algorithm

1. Run `node scripts/copy-sources.js` from the reviewed checkout.
2. Enumerate and digest the generated `c_src` tree.
3. Record the local toolchain: Node, npm, Python, GCC/G++, make, linker,
   OpenSSL, kernel, OS, architecture, and relevant environment.
4. Set `WAVEDB_OPENSSL=1` and `OPENSSL_ROOT=/usr` for the observed Linux host.
5. Run `node scripts/build.js`; the reviewed script invokes local
   `node-gyp rebuild`.
6. Require exactly one expected addon at
   `bindings/nodejs/build/Release/wavedb.node` and record its size and SHA-256.

There is no fallback to a different Node, node-gyp, Python, compiler, OpenSSL
mode, source commit, or npm package. A compatibility failure is an experiment
result, not permission to repair upstream.

### Verification algorithm

1. Load `lib/wavedb.js` from the isolated checkout and prove it resolves the
   just-built addon.
2. Run the upstream test files directly with the lockfile-resolved Mocha so the
   addon is not rebuilt implicitly.
3. Run the reviewed publish canary behavior: create a temporary store, write
   and read an empty value, close, and remove only that exact temporary store.
4. Require no real Craft path access and no changes outside
   `source-build/.work/` plus declared execution receipts.
5. Emit the terminal receipt last. Only a complete passing receipt may be
   offered to the parent refresh.

## View 4: Workflow process

```text
authorized
  -> source-closing
     -> mismatch: BLOCK
  -> dependency-materializing
     -> lock/integrity/script violation: BLOCK
  -> generated-source-verifying
     -> mismatch: BLOCK
  -> native-building
     -> compile/link failure: BLOCK
  -> addon-loading
     -> load failure: BLOCK
  -> upstream-testing
     -> test/canary/scope failure: BLOCK
  -> receipt-binding
     -> source-build PASS
  -> parent-refresh-pending
```

No implicit retry is legal. A retry receives a fresh attempt ID and an absent
work-area target. A passing source build does not automatically advance the
parent Work Pack.

## View 5: Decision flow

| Decision | Pass branch | Failure branch |
| --- | --- | --- |
| User authorized alternate route? | Design/Plan source build | stop at npm decision |
| Exact root and recursive submodules? | build source manifest | `SOURCE_IDENTITY_MISMATCH` |
| Exact lockfile and no install scripts? | materialize dependencies | `DEPENDENCY_CLOSURE_FAILED` |
| Generated `c_src` complete? | capture toolchain | `GENERATED_SOURCE_MISMATCH` |
| Native compile/link succeeds? | hash addon | `NATIVE_BUILD_FAILED` |
| Addon loads and tests pass? | emit pass receipt | `ADDON_VERIFICATION_FAILED` |
| Scope scan clean? | offer parent refresh | `FORBIDDEN_EFFECT_DETECTED` |
| Parent refresh admits local artifact? | select new parent frontier | preserve source-build pass but keep parent blocked |

## View 6: Dependency interfaces

| Dependency/interface | Exact contract | Failure behavior |
| --- | --- | --- |
| WaveDB root Git tree | commit `01c77e8b...` detached | block on missing/different commit |
| Recursive submodules | gitlinks from the reviewed root and nested submodules | block on missing/different SHA |
| Node package lock | lockfile v3 SHA-256 bound in execution context | block on rewrite or resolution failure |
| npm registry | fetch only lockfile-declared dependency tarballs and verify integrity | block; no alternate registry/package |
| Local Node toolchain | Node `v22.12.0`, npm `10.9.0`; exact live identities rechecked at execution | block on drift unless a new plan epoch is authored |
| Native toolchain | Python 3.12, GCC/G++ 13.3, make 4.3, binutils 2.42, OpenSSL 3.0.13, Linux x86_64 baseline | block on drift or build failure |
| Filesystem | ignored `.work` plus source-build execution receipts | block on any out-of-scope write |
| Parent experiment | hash-bound `SourceBuildReceipt`; separate Invoke Refresh | no direct Work Pack mutation |
| Craft | no interface in this source-build slice | any access is fatal |

## Selected concerns and evidence ceiling

The deterministic selector requires architecture, authority/trust,
security/abuse, state/event, persistence, failure/compensation, reliability,
integration/versioning, data lifecycle, and validation contracts. Migration
and rollout are not applicable to this local build; performance observations
are recommended but not selected as acceptance outputs.

This Design proves only that the authored source-build architecture is total
for the closed manifest and stable across two selection passes. It does not
prove dependency availability, native compatibility, addon correctness, parent
experiment readiness, Craft suitability, publication, or production fitness.
