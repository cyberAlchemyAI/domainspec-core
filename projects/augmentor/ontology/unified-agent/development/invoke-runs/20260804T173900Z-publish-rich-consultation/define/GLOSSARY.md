# Publication Glossary

| Term | Plain meaning | Boundary |
| --- | --- | --- |
| Release bundle | The complete folder of page, API code, reviewed consultation data, schemas, and server configuration installed together. | It is a delivery unit, not source authority. |
| Release closure | The check that every file required at runtime is included and bound to the expected version and digest. | A file list without runtime loading proof is insufficient. |
| Candidate release | A complete release assembled for testing before it becomes current. | It is not deployed merely because local tests pass. |
| Production switch | The single change that makes a candidate the current served generation. | It is an external privileged effect. |
| Rollback | Restoring the previously served complete generation after a failed switch or acceptance check. | It does not repair the failed candidate. |
| Deployed byte proof | Hash evidence that production contains the same files that were validated locally. | Equal hashes prove identity, not correct behavior by themselves. |
| Neutral projection | The reviewed, consumer-safe consultation data bundle. | It is read-only evidence and does not carry ontology authority. |
| Explanation profile | `brief`, `guided`, or `deep`, selecting how much structured teaching support the API returns. | It changes detail, never truth, permission, or authority. |
| Agent API document | The protected page section and reference that explain how an agent calls and uses the API. | It documents the interface; it does not grant access. |

