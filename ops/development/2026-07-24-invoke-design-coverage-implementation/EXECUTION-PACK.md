# Execution Pack: Invoke Design Coverage

Complexity: high. Baseline wave: W0.

## Choreography

| Wave | Layer | Outcome | SWUs | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0.md) | L0 | freeze independent denominator | DVC-001 | dispatch and authoring package validation | fixture corpus receipt and digest |
| [W1](work-pack/waves/W1.md) | L1 | prove schemas and deterministic selection | DVC-002A/B/C, 003, 004, 005 | W0 receipt | complete L1 fixture and mutation receipt set |
| [W2](work-pack/waves/W2.md) | L2 | integrate Design and companion contracts | DVC-006A/B/C/D/E | W1 receipts | canonical contract validation, aggregate validation, and leakage scan |
| [W3](work-pack/waves/W3.md) | L3 | synchronize, prove live, and audit | DVC-007, 008, VERIFY | W2 receipt | parity, live proof, recomposition, and audit receipts |

## Program order

```text
DVC-001
  -> DVC-002A
  -> DVC-002B
  -> DVC-002C
  -> DVC-003
  -> DVC-004
  -> DVC-005
  -> DVC-006A
  -> DVC-006B
  -> DVC-006C
  -> DVC-006D
  -> DVC-006E
  -> DVC-007
  -> DVC-008
  -> VERIFY
```

The order is intentionally serial because each stage fixes the contract used
by the next and later canonical paths overlap. No implementation fan-out is
authorized.

## Stage coverage

- Spellcraft: every public canonical source change and lifecycle receipt.
- bootstrap owner: generated runtime synchronization after canonical pass.
- Invoke: authoring package and later generic example input/output only.
- human maintainer: promotion, publication, commit, push, and public boundary.

## Closure obligations

- DVC-R01..R14 have exact receipt evidence.
- Every frozen expected result passes unchanged.
- No mutation test survives.
- Generated surfaces match canonical sources.
- Generic live proof preserves the evidence ceiling.
- Public scan contains no private package identifiers, paths, or witnesses.
- Dirty pre-existing changes are preserved and excluded from task receipts.

## Stop conditions

- fixture expectation changed merely to satisfy implementation;
- source digest changed outside an admitted SWU;
- stale, self-issued, or unbound receipt accepted;
- N/A without negative detector evidence;
- pass two changes any selected field;
- generated surface edited before canonical validation;
- private content enters public Arcanum;
- any result implies promotion or Plan evidence from Design validation.
