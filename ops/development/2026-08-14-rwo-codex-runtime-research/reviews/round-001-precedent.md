# Round 1 — Precedent and Owner Placement

Verdict: `FLAG_UNTIL_REPAIRED`.

The selected topology survives if `framework/runtime` remains projection-only and the private RWO journal remains the sole provider-delivery recovery source. Required repairs:

| Claim | Verdict | Repair |
|---|---|---|
| `SP-01-OUTER-ENVELOPE` | accept, specified-unexecuted | Outer `events.jsonl` contains only RWO record references/digests; no second App Server run folder, raw store, cursor, reconciliation loop, or terminal truth. |
| `SP-02-SEMANTIC-COMMIT` | reject wording | Rust owns semantic decisions; Go owns synchronized persistence and projection of Rust-authored semantic commit records. |
| `SP-03-TERMINAL-OWNER` | reject sole-owner attribution | Translator/validator owns provider-evidence closure; Go coordinator owns physical convergence and durable admission recording; Rust owns semantic acceptance and no-successor. |
| `SP-04-TASK-SESSION` | qualify | Task Session coordinates and validates closeout synchronization; the routed owner mutates its artifact; the capability owner supplies acceptance. |
| `SP-05-CONTROL-OWNERS` | repair | State separate Craft-ledger, Goal-frontier, Orchestrate-dispatch, Experiment-Harness-test, OIL-observation, and Signal-Observer-telemetry authority. |
| `SP-06-RETRY-SCOPES` | repair | RWO same-attempt provider retries, provider reconciliation, Task Session task recovery, Orchestrate fresh-run rules, and Goal rounds are distinct. |
| `SP-07-ADAPTER-PRECEDENT` | flag | Prove current runtime adapter surface insufficient before extending its existing owner; do not create a second registry/controller. |
| `SP-08-CURRENT-WIRING` | accept blocker | CLI currently lacks attempt, provider, terminal, and delivery-worker wiring. |

Primary selectors: `synthesis.md:9-33,47-52,62-68,75,110-118`; `arcanum/framework/runtime/README.md:3-33,89-118`; current `durable_runtime.go`, `terminal.go`, `attempts.go`, Task Session, Craft, Goal, Orchestrate, Experiment Harness, OIL, and Signal Observer selectors listed in the returned review.

No topology restart is required. No files were changed by the reviewer.
