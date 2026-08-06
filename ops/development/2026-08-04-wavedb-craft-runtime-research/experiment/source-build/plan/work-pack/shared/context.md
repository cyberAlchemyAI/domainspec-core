# Shared execution context

## Controlling identities

- Reviewed root commit: `01c77e8b70f71de9b72480e73a3a179f6e93a009`.
- Package lock SHA-256:
  `26fbf0839106a0521f1ad6785764cefa3d39aedd9ff8412c982689c09b109f95`.
- `package.json` SHA-256:
  `82e87aaaac10113cb1294732bf149356f6f7df76ecde0259181999c6a3fe9dc3`.
- `binding.gyp` SHA-256:
  `5a326bf16ce349808572fcd213344868edeabf70fb75a10f56c1c9f429d5b90f`.
- `scripts/build.js` SHA-256:
  `ff00fe3c9c3dbfc5401c611feac70a8148a92f158bfaa6ec30acbfade214d1bc`.
- `scripts/copy-sources.js` SHA-256:
  `466f86b07e370a4cfcde0ff3d4f4639564344247f08d480ba6ed4d2c6b3e420a`.

Every identity is re-derived live; this list is an expected contract, not
execution evidence.

## Boundaries

- Allowed material paths: `source-build/.gitignore` and
  `source-build/runtime/**` in SWU-WCSB-001 only.
- Allowed generated paths: `source-build/.work/**`,
  `source-build/execution/source-build/**`, and exact Task Session evidence.
- Forbidden: both Craft trees, real `.craft/`, parent plan before separate
  refresh, Git commits/tags/branches, npm publication, deployment, production.
- Network: exact WaveDB Git source and lockfile-declared npm dependency
  tarballs only during SWU-WCSB-002.
- Credentials: never request, read, print, store, or transmit.

## Claim ceiling

A pass proves one local source build on the recorded Linux x86_64 toolchain.
It does not prove npm provenance, reproducible binaries, cross-platform
support, license/security closure, Craft runtime suitability, release, or
production readiness.
