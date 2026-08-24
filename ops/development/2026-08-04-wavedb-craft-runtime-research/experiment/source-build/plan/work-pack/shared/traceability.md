# Traceability

| Define/Design obligation | SWU | Observed evidence |
| --- | --- | --- |
| fail-closed build protocol | SWU-WCSB-001 | passed runner fixture and Task Session receipts |
| Node 22 comparison observation | SWU-WCSB-002 | preserved `execution/source-build/**` and terminal block receipt |
| exact reviewed source and recursive submodules under Node 26 | SWU-WCSB-003 | `execution/source-build-node26/source-manifest.json`, SHA-256 `d86e7615...` |
| lockfile-only dependencies with scripts disabled | SWU-WCSB-003 | `execution/source-build-node26/dependency-manifest.json`, SHA-256 `bd0983eb...` |
| deterministic generated `c_src` | SWU-WCSB-003 | `execution/source-build-node26/generated-source-manifest.json`, SHA-256 `75887675...` |
| exact Node 26 and native addon hash | SWU-WCSB-003 | Node `v26.6.0`, npm `11.18.0`; `build-manifest.json`; addon SHA-256 `cbd5ebda...` |
| addon load | SWU-WCSB-003 | command 19 passed |
| same upstream tests | SWU-WCSB-003 | command 20 blocked at concurrent writes; log SHA-256 `012e05ee...`; controlled SIGTERM after 338.233-second liveness observation |
| empty-value canary | SWU-WCSB-003 | not run after upstream blocker |
| no previous-attempt or NVM-default mutation | SWU-WCSB-003 | Task Session terminal receipt binds unchanged Node 22 hashes and `22 -> v22.13.0` default alias |
| no Craft admission/publication/deployment | SWU-WCSB-003 | `addon_handoff: null`, pass receipt absent, scoped closeout audit |
| owner closeout | SWU-WCSB-003 | terminal receipt plus `invoke-refresh-receipt.json`; no successor returned |

The comparison supports only: the same local runtime test location stalls under
both tested Node versions. It does not identify the responsible WaveDB thread,
lock, native function, or root cause.
