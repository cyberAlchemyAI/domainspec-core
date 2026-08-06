# Traceability

| Define/Design obligation | SWU | Planned or observed evidence |
| --- | --- | --- |
| fail-closed build protocol | SWU-WCSB-001 | passed runner fixture and Task Session receipts |
| Node 22 comparison observation | SWU-WCSB-002 | preserved `execution/source-build/**` and terminal block receipt |
| exact reviewed source and recursive submodules under Node 26 | SWU-WCSB-003 | `execution/source-build-node26/source-manifest.json` |
| lockfile-only dependencies with scripts disabled | SWU-WCSB-003 | `execution/source-build-node26/dependency-manifest.json` |
| deterministic generated `c_src` | SWU-WCSB-003 | `execution/source-build-node26/generated-source-manifest.json` |
| exact Node 26 and native addon hash | SWU-WCSB-003 | `execution/source-build-node26/dependency-manifest.json`; `build-manifest.json` |
| addon load, same upstream tests, canary | SWU-WCSB-003 | `execution/source-build-node26/test-manifest.json` |
| no previous-attempt, NVM-default, Craft, publication, or out-of-scope effects | SWU-WCSB-003 | Task Session baselines and scope audits |
| separate parent consumption decision | SWU-WCSB-003 closeout | terminal receipt returns parent Invoke Refresh route only on pass |
