# Risks and Decisions

| ID | Decision or risk | Resolution |
| --- | --- | --- |
| D-01 | Reuse site or create another service? | Reuse the existing protected route and two-container topology. |
| D-02 | Publish page and API separately? | No. Package page, runtime, bundle, and config as one release generation. |
| D-03 | Replace shared Basic Auth? | No. Preserve the current hash and auth behavior; auth redesign is out of scope. |
| D-04 | Is the current deploy script ready for `1.1.0`? | No. It omits the glossary and schemas and its smoke still sends `1.0.0`. Repair is mandatory before upload. |
| D-05 | Can the release claim a reasoning engine? | No. It publishes deterministic consultation retrieval and explanation support only. |
| R-01 | Mixed page/API generation | Closed by one immutable release and whole-generation rollback. |
| R-02 | Plaintext credential leakage | No credential input in artifacts; preserve the existing hash; do not print environment values. |
| R-03 | Switch succeeds but rich API fails | Require `1.1.0` guided internal smoke with bundle-digest and boundary assertions; rollback on fail. |
| R-04 | Exact bytes work internally but public browser session is not replayed | Record exact byte, proxy, internal response, and denial proofs separately; leave human authenticated replay as explicit residue if unavailable. |
| R-05 | User-owned untracked changes overlap release inputs | Freeze exact hashes at Task Session admission; block on drift rather than overwriting. |

