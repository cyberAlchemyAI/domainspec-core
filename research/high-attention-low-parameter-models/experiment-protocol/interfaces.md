# Interfaces: High-Attention, Low-Parameter Experiment Protocol

## Artifact Contracts

| Contract | Producer | Consumer | Boundary |
| --- | --- | --- | --- |
| `protocol.json` | protocol owner | all stages | Frozen, content-addressed, schema-valid. |
| `decisions/*.json` | human decision gate | protocol freezer | Approval-bearing; unresolved is explicit. |
| `fixtures/*.jsonl` | generator | renderer/scorer | Immutable semantic plans and ground truth. |
| `fixture-manifest.json` | generator | admission/reviewer | Provenance, licenses, splits, hashes. |
| `model-stack.json` | platform owner | experiment harness | Immutable stack identities. |
| `capacity/*.json` | admission probe | trial planner | One model/length witness per admitted cell. |
| `trial-matrix.jsonl` | trial planner | experiment harness | Exact factor tuple and render handles. |
| `runs/*.json` | experiment harness | scorer/analysis | Raw-output and telemetry receipt. |
| `scores/*.json` | scorer | analysis | Separate answer/evidence/support fields. |
| `analysis/*.json` | analysis owner | reviewer/gate | Frozen estimands, uncertainty, verdict. |

## Internal Protocol Interface

The implementation should expose deterministic commands with equivalent
contracts; command names are illustrative until implementation:

```text
protocol validate <protocol.json>
fixtures build --protocol <protocol.json> --manifest <path>
stack admit --protocol <protocol.json> --stack <model-stack.json>
trials render --protocol <protocol.json> --matrix <trial-matrix.jsonl>
trials run --cell <trial-cell-id>
scores build --run <run-receipt>
analysis build --phase <phase-id>
protocol status --json
```

Every command is non-interactive, writes through an explicit output path, and
returns non-zero on contract or gate failure. No command name is an active
runtime contract until the implementation task materializes and validates it.
