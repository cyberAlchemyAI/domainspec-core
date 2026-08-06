# Decision Gate: pinned npm artifact diagnostic

- Decision ID: `DG-WCNPM-001`.
- Status: resolved.
- Resolved at: `2026-08-05T16:16:24Z`.
- Source: direct user statement, `Authorize pinned npm diagnostic.`
- Selected option: `OPT-PINNED-NPM-DIAGNOSTIC`.
- Rejected for this run: wait for corrected provenance; stop without another
  diagnostic.

## Decision

Run one isolated diagnostic of exact registry artifact
`@vijayee/wavedb@0.15.8`, pinned by:

- SHA-1: `107472e4634729de8533b68c351859ff496cc56e`;
- SRI: `sha512-o4G13W9V1jIzKOVSETUeg3oFDJde8GDDUeFF/a0nOJ1/LR0cN6pPurtdUGb+9vssUeB0B7OYbtWT+mEgI+pMnQ==`;
- registry tarball: `https://registry.npmjs.org/@vijayee/wavedb/-/wavedb-0.15.8.tgz`.

The tarball itself is the tested artifact identity. The decision does not
repair, waive, or reinterpret the stale registry `gitHead`, and it does not
bind the tarball to reviewed commit `01c77e8b...`.

## Accepted bounded effects

- exact npm registry metadata and tarball reads;
- lockfile-declared transitive dependency fetches inside one fresh attempt;
- native package install/build under Node `v26.6.0` and npm `11.18.0`;
- addon load and bounded black-box canaries;
- preserved candidate-local build/test residue.

## Boundaries

No Craft access or mutation, addon handoff, parent runtime admission, NVM
default change, Git-history change, publication, deployment, cleanup, or
production claim is authorized. A passing diagnostic proves only the exact
artifact on this local Linux x86_64 Node 26 environment and the named canaries.

## Evidence

- [Option request](decision-option-request.json)
- [Admissibility receipt](decision-option-receipt.json)
- [Original provenance result](../../../execution/wp0-provenance/RESULT.md)
- [History reconstruction](../../../execution/wp0-provenance/HISTORY-RECONSTRUCTION.md)

Remaining blocker: exact package/source provenance remains unresolved for any
route that requires a reviewed source binding. It is not an acceptance gate
for this separately authorized opaque-artifact diagnostic.
