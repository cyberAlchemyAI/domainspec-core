# Events

| Event | Required fields | Meaning |
| --- | --- | --- |
| `package_gate_checked` | registry identity, SRI, gitHead, reviewed source commit, verdict | Provenance decision before install |
| `fixture_frozen` | parser/serializer pins, hashes, key count, manifest digest | Independent input closure |
| `batch_submitted` | generation, batch ID, operation count, barrier | Candidate write observation |
| `generation_readback` | complete key set, value digests, aggregate hashes | Verification evidence |
| `query_admitted` | fresh YAML digest, manifest digest, query ID | Legal complete output |
| `query_refused` | stable failure code, zero row count | Fail-closed behavior |
| `generation_quarantined` | generation, reason, external receipt | Suspect store is never served |
| `experiment_stopped` | first failed gate, remaining frontier, owner route | Bounded terminal control evidence |

Events are evidence records in the experiment package. They are not Craft
domain events and never enter WaveDB.
