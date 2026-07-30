# Execution Pack: One-shot admission prototype

## Execution Rule

Run the frozen SWUs in order. Stop at the first acceptance-critical failure.
Do not absorb newly discovered work. Record one receipt per SWU under
`receipts/`.

## Waves

| Wave | Layer | SWUs | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0.md) | L0 | OAP-001, OAP-003 | Handoff Notice published; Distill pass | Both public schema families parse |
| [W1](work-pack/waves/W1.md) | L0/L1 | OAP-002, OAP-004, OAP-005 | OAP-001 and OAP-003 pass | Both deterministic suites pass |
| [W2](work-pack/waves/W2.md) | L2 | OAP-006 | OAP-002 and OAP-005 pass | 19 private fixtures pass |
| [W3](work-pack/waves/W3.md) | L2 | OAP-007, OAP-008 | OAP-006 pass | Generated mirrors match canonical packages |
| [W4](work-pack/waves/W4.md) | L2 | OAP-009 | OAP-007 and OAP-008 pass | Consolidated validation report |

## Receipt Shape

```yaml
swu_id:
result: pass | block
execution_mode: candidate-local-fast-lane
files_touched: []
validation: []
blockers: []
residue: []
```

## Stop Conditions

- write outside a declared SWU scope;
- acceptance-critical test or schema failure;
- private literal in public Arcanum;
- unexpected Task Session source mutation;
- package-wide bootstrap instead of package-specific sync;
- promotion, registry, Git, deployment, or network boundary.
