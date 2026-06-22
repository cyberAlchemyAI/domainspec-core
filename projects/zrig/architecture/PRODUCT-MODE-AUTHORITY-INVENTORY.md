# Product-Mode Authority Inventory

Status: private observed-architecture/gap inventory
Scope: Z-Rig product-mode authority surfaces
This is not declared integration architecture and not product-mode proof.

## Inventory Summary

Z-Rig has the right named authority surfaces for a governed orchestration engine, but several surfaces currently report success through fallback, underdocumented, non-authoritative, or non-fatal paths.

## Authority Surfaces

| Surface | Findings | Observed Behavior | Missing Proof | Required Remediation | Check Surface |
| --- | --- | --- | --- | --- | --- |
| Gates | F1 | `W4/W5/W8/W8.5/W9/W10/W11` map to gate IDs, but only `G0/G1/G2/G3/G5.5/G6/G7` have evaluators. Unknown gates fall to `_generic_gate`. | Failed semantic payloads cannot pass because they are non-empty. | Add specific evaluators or fail-closed policy for spec-governed missing gates. | Focused tests for failed W10/W11 payloads. |
| Dry-run assurance | F2 | Default executor returns passing stub outputs and CLI labels live as non-default. | Operators cannot confuse stub completion with product assurance. | Strengthen output/docs around proof class. | CLI/help/docs review plus dry-run output check. |
| Residue | F3 | Pipeline passes `entries=` into `PerWaveResidue`, whose dataclass lacks that field; exception is logged non-fatal. | Product/live policy for failed residue persistence. | Align schema and fatality/degraded-assurance behavior. | Residue write test and run-status policy test. |
| Live identity | F4 | W2 parser reads `model_actual` and `family_actual` from bridge output before trusted seat fallback. | Bridge output cannot spoof identity used by G2. | Derive identity from assigned seat/signed metadata. | Spoofing regression test. |
| Bridge contract docs | F5 | QuickStart documents `--live` at high level but not manifest/envelope contract. | Operator-facing live contract. | Add bridge contract docs and non-deploy verification. | Docs review and import/check command. |
| Deploy/sentinel reachability | F6 | Direct W10/W11 only run when top-level `deploy_config`/`sentinel_config` exist; pipeline context does not supply them. | Normal product pipeline can reach or intentionally block side-effectful waves. | Thread config deliberately or fail closed when absent. | Context test and CLI validate/preview path. |
| Deploy command trust | F7 | Config accepts arbitrary strings and adapter executes them over SSH. | Arbitrary command trust boundary is controlled. | Replace with constrained operations or explicit approval policy. | Schema tests and no-execution safety review. |
| Dependencies | F8 | `pyproject.toml` has metadata/script only; tests/runtime imports need undeclared packages. | Verification environment is reproducible. | Declare runtime/test extras and install commands. | `python3 -m pytest --version`; import checks. |
| Failover cap | F9 | Wave failover count is passed as a per-seat list, so concurrency can exceed cap. | Shared per-wave cap under concurrent seats. | Shared counter/lock or central authority. | Concurrent-seat regression test. |
| Clean-run policy | F10 | W5-only scan logs W4+W5 and skips W5.5/W8.5. | Policy/log/test agreement. | Align implementation and language. | Clean/contaminated path tests. |
| FULL routing | F11 | G6/G7 exist but W6/W7 failure routes use defaults. | FULL-mode route semantics intentional and tested. | Add routes or document/test default escalation. | Route tests for W6/W7 failures. |
| Skipped accounting | F12 | `RunResult` has skipped list, but skipped waves are appended to completed. | Completed and skipped lists mean different things. | Append skipped waves to `waves_skipped`. | Pipeline result test. |
| `AUTO` mode | F13 | Code/docs accept `AUTO`; extracted PDF only names MICRO/STANDARD/FULL. | `AUTO` is either spec-promoted or explicitly an implementation extension. | Spec/docs reconciliation. | Config/docs review. |
| Metrics | F14 | Metrics store/triggers exist but pipeline does not use them. | Product metrics status is true. | Wire metrics or mark prototype/non-product. | Search plus pipeline completion test. |

## Priority Order

1. F1 gate coverage and fail-closed behavior.
2. F4-F7 live identity, bridge docs, deploy/sentinel reachability, deploy command trust.
3. F3/F8 auditability and dependency declaration.
4. F9-F12 runtime authority/accounting.
5. F13/F14 spec drift and non-wired lifecycle features.

## Review Rule

Do not collapse proof classes:

- spec evidence says what should be true;
- source evidence says what code currently does;
- runtime evidence says what a command or focused reproduction proved.

Dry-run success cannot prove live bridge, deploy, sentinel, identity, residue, side effects, public promotion, or product-mode assurance.
