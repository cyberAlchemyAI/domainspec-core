# Traceability And Recomposition Map

## Spec To Execution

| Spec capability | Architecture components | Layer/wave | Task | SWUs | Acceptance evidence |
| --- | --- | --- | --- | --- | --- |
| Protocol Governance | protocol-validator, decision records | L0/W0 | DECISIONS, CONTRACTS | 001–006 | approvals and validator fixtures |
| Fixture Materialization | fixture-generator, prompt-renderer, scorer | L0/W1 | FIXTURES, WITNESS | 007, 008, 010 | deterministic offline witness |
| Stack Admission | stack-admitter, capacity-prober | L1/W2 | ADMISSION | 009 | compatibility and capacity receipts |
| Trial Execution | matrix-builder, run-adapter, telemetry-capture | L1/W2; L2/W3 | MEASURE | 011, 012 | smoke and paired run receipts |
| Scoring And Inference | scorer, analysis-runner | L0/W1; L2/W3 | FIXTURES, ANALYZE | 008, 013 | scorer fixtures and paired analysis |
| Budgeted Promotion | frontier-builder, readiness-reporter | L2/W3; L3/W4 | ANALYZE, VERIFY | 014; VERIFY exemption | frontier, phase decision, audit |

## Research Obligations To SWUs

| Research obligation | SWU coverage |
| --- | --- |
| Claim/estimand repair and typed KILLs | 001, 013 |
| Numeric thresholds/N/repetitions/multiplicity | 002 |
| Workload/arms/positions/lengths/retrieval | 003, 007, 008 |
| Exact stack/template/backend/KV admission | 004, 009 |
| Energy/cost/frontier/storage/license boundary | 005, 014 |
| Versioned generator/provenance/splits | 007 |
| Renderer/output grammar/scorer validation | 008, 010 |
| Run/raw-output/resource receipts | 011, 012 |
| Paired analysis and false support | 013 |
| Value-of-information promotion/stop | 014 |

## Recomposition Proof

`SWU -> parent task -> wave -> L0–L3 decision -> architecture component ->
spec capability` is total for every non-exempt SWU. The VERIFY task is exempt
from SWU decomposition because it owns closure review only.
