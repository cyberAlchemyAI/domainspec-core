# WaveDB 0.15.8 publication-history reconstruction

## Outcome

The official npm artifact is completely content-mapped, but the exact
package/source provenance gate remains blocked.

A clean checkout of reviewed commit
`01c77e8b70f71de9b72480e73a3a179f6e93a009`, including its four pinned
submodules, was passed through the repository's `copy-sources.js` and
`npm pack --ignore-scripts` steps. The resulting package has exactly the same
226-file path set as the official artifact. After converting CRLF to LF, every
file matches: all 192 packaged `c_src` files and all 34 binding/package files.
The normalized content-manifest digest for both trees is
`2befdea1559d3bfed47d96121a8d56aefcaa21bb5c2bd2009317324d8d4a40cc`.

This closes the earlier evidence gap around the packaged C/C++ subtree. It does
not satisfy `SWU-WCP-001`, whose declared edge cases make normalized-only
similarity, stale `gitHead`, and version mismatch blocking.

## Chronology

| Event | UTC | Identity |
| --- | --- | --- |
| Registry package published | 2026-07-28 12:42:01.802 | `@vijayee/wavedb@0.15.8` |
| First post-`gitHead` Node fix committed | 2026-07-28 12:49:36 | `9851cef6905e06debc4d62b9d2e9b77c8b835673` |
| Windows export fix committed | 2026-07-28 12:49:45 | `c5f2e0517e4c3f3e7accf07dbb01688cd3fe6678` |
| Version 0.15.8 commit recorded | 2026-07-28 12:49:48 | `01c77e8b70f71de9b72480e73a3a179f6e93a009` |

The registry's declared `gitHead` is
`54832130f408c44637ad84f35cb93003b0f238c4`, whose Node package version is
`0.15.7`. The registry publication precedes the later content-equivalent commit
by 466.198 seconds. No tag points at that reviewed commit.

The narrow inference supported by these observations is that the package was
likely published from an uncommitted working tree whose content was committed
minutes later. That reconstruction is not an owner-signed provenance statement
and cannot replace the package's contradictory registry metadata.

## Exact comparison

| Property | Official artifact | Clean reproduction |
| --- | --- | --- |
| File count | 226 | 226 |
| SHA-1 | `107472e4634729de8533b68c351859ff496cc56e` | `4985a7776542066c7f8893c67fb426af59129370` |
| Exact-byte file matches | 11 | 11 |
| Additional CRLF-normalized matches | 215 | 215 |
| Normalized content mismatches | 0 | 0 |
| File-set differences | 0 | 0 |
| Script modes | both scripts `0644` | both scripts `0755` |

The official SRI, SHA-1, file count, unpacked size, and registry signature were
verified from registry metadata. The registry signature authenticates the
published registry artifact; it does not bind that artifact to the later Git
commit.

## Gate effect

- New evidence: the complete official package content, including `c_src`, is
  explainable by the reviewed commit and pinned submodules under CRLF
  normalization.
- Remaining contradiction: exact tarball bytes and modes differ, the package
  declares an older `gitHead` with version `0.15.7`, and the content-equivalent
  commits postdate publication.
- Verdict: `PACKAGE_PROVENANCE_MISMATCH` remains `block`.
- Control flow: no fresh Task Session attempt, dependency resolution, native
  build, addon load, Craft mutation, or successor SWU was admitted.

The machine-readable evidence is in `history-reconstruction.json`. This
addendum narrows the open decision but does not modify the already-closed
terminal or owner receipts.
