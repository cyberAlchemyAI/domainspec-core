# Glossary

| Term | Meaning in this experiment |
| --- | --- |
| Canonical YAML | The exact bytes of the selected `.craft/ledger.yml`; the only Craft source of truth. |
| Projection generation | A disposable WaveDB keyspace addressed by the canonical YAML SHA-256. |
| Closed manifest | The sole manifest key plus a complete ordered list and digest of every other stored key/value. |
| Fresh admission | Re-reading, validating, and hashing YAML immediately before selecting or querying a generation. |
| Zero-output failure | A failure that returns no projected row, index, derived view, or stale fallback. |
| Quarantine | An externally recorded decision never to serve a suspect isolated generation. |
| Rebuild | Construction of a fresh sibling generation from fresh canonical YAML; never in-place repair. |
| Exact provenance | A registry artifact, integrity digest, source commit, and source tree correspondence that do not contradict each other. |
| Observation receipt | Externally owned evidence of inputs, environment, barriers, outputs, and verdict; never stored in WaveDB. |
| Candidate-local | Evidence confined to this experiment package with no canonical, promotion, release, or deployment effect. |

These are Invoke-local terms. They do not redefine Arcanum-wide vocabulary.
