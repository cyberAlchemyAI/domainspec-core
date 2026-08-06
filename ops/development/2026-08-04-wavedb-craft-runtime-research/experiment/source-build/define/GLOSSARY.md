# Source-build glossary

| Term | Meaning in this slice | Not implied |
| --- | --- | --- |
| Reviewed source | WaveDB root commit `01c77e8b...` plus the recursive submodule commits recorded by that tree | npm provenance or latest-branch authority |
| Source build | Native addon produced locally from the reviewed checkout and exact lockfile | registry package, distributable package, or supported release |
| Source manifest | Sorted path/mode/byte-digest inventory for admitted source inputs | publisher attestation |
| Dependency manifest | Exact resolved dependency identities from `npm ci` and the lockfile | license or vulnerability clearance |
| Build manifest | Toolchain, environment, commands, generated-source digest, addon path, and addon hash | cross-platform reproducibility |
| Source-build receipt | Terminal pass/block evidence for the selected local build SWU | authority to change Craft or publish WaveDB |
| Isolated work area | `source-build/.work/`, excluded from tracked evidence and real Craft workspaces | durable product installation |
| Parent refresh | Separate Invoke owner action that may propose/admit the built addon into a new parent-plan epoch | retroactive repair of the failed npm SWU |
