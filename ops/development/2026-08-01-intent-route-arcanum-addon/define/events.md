# Events

| Event | Producer | Meaning |
|---|---|---|
| `candidate_authored` | sigil-development | Public-safe candidate exists outside canonical source. |
| `candidate_witnessed` | acceptance harness | Candidate core and scans pass the frozen matrix subset. |
| `canonical_accepted` | public Arcanum authority | Canonical source admission is explicitly approved. |
| `runtime_package_generated` | Bootstrap | One profile projection was generated from a bound closure. |
| `runtime_parity_passed` | parity harness | Claude/Codex behavior parity passed. |
| `consumer_admitted` | consumer owner | One consumer adapter passed its own authority and integration gates. |

None of these events means deployed, production-ready, authorized to execute,
or reasoning-engine complete.

