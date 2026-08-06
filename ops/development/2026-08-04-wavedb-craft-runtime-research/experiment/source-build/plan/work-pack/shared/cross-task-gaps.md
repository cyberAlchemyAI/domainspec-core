# Cross-task gaps and residue

| Gap | Current effect | Owner/route |
| --- | --- | --- |
| Node 22 concurrent-write stall | preserved acceptance block for SWU-WCSB-002 | WaveDB source owner diagnosis |
| Node 26 concurrent-write livelock | separately reproduced at the same test case; no addon handoff | WaveDB source owner instrumentation/debugger trace |
| Root cause | not established by CPU/file liveness observation | WaveDB source owner; reviewed diagnosis or fix required |
| Runner-level liveness termination | operator SIGTERM was required after 338.233 seconds; `-15` is not crash proof | source-build protocol owner before any new attempt |
| Node 26 is non-LTS | prevents general support recommendation | platform/package owner after passing evidence |
| Upstream test completion and empty-value canary | absent, so compatibility and empty-value claims remain blocked | new immutable attempt only after source-owner unblock |
| Same-platform repeatability | deferred because L0 has no passing build/test result | new L1 Work Pack after promotion decision |
| dependency license/SBOM/vulnerability closure | no publication/internal-package claim | package/security/license owners at L2 |
| other OS/architecture/Node/OpenSSL configurations | no support claim | platform/package owner at L3 |
| npm `0.15.8` provenance contradiction | remains failed historical evidence | upstream publisher/corrected release only |
| parent experiment addon admission | cannot advance from either block receipt | separate Invoke Refresh only after a source-build pass |
| Craft adoption, publication, deployment, production | out of scope | separately authorized owners |

Preserved residue includes both immutable attempts, their evidence directories,
and the Node 26 temporary store `/tmp/wavedb-integration-1785944869024-2isb9brlg`.
No destructive cleanup is authorized.
