# Glossary consistency

| Term | Define meaning | Design use | Status |
| --- | --- | --- | --- |
| Reviewed source | exact root plus recursive submodule identities | immutable source closure algorithm | linked |
| Source build | local native addon from reviewed checkout and lockfile | isolated build workflow | linked |
| Source manifest | sorted path/mode/byte identity | first execution gate | linked |
| Dependency manifest | lockfile-resolved dependency identities | `npm ci` output and `npm ls` receipt | linked |
| Build manifest | toolchain, commands, generated sources and addon | native-build output contract | linked |
| Source-build receipt | terminal evidence without publication authority | sole parent handoff | linked |
| Parent refresh | separate owner evaluation | post-pass route only | linked |

No term is promoted outside this candidate slice. `Package provenance` remains
the failed npm relationship; it is not redefined as `source build`.

Verdict: `pass`.
