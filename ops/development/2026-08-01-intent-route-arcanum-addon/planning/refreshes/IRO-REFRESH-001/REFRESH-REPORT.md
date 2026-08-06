# IRO-REFRESH-001 — Planning contract repair

Status: `pass`

## Applied scope

The direct operator request activated Invoke Refresh in `apply-approved` mode
for 15 exact internal planning targets. The staged material package passed
dependency, owner, publication-boundary, and byte-parity validation before the
targets were applied.

The repair:

- reconciled the Work Pack, Execution Pack, first-unit Dispatch, six task
  contracts, and closeout prose;
- added the authoritative full-stream execution contract, three receipt
  schemas, and a fail-closed validator;
- fixed the order and unique successor of all ten units;
- froze coordinator outputs, owner material declarations, commands, budgets,
  admitted closeout deltas, and pause gates;
- preserved the boundary that the outer stream coordinates owners but does not
  inherit their mutation or promotion authority.

## Material receipts

| Artifact | SHA-256 | Result |
|---|---|---|
| `material/material-package.json` | `5c74e12ac4cfa6659e347f3b1acbbdc70b184ccc794bab5afeba2cc99a86342b` | 15 exact targets |
| `material/material-package-receipt.json` | `e8093d6548ca03d0b73af9340f5cfb6bfd8265ff397474ba3f5b91dd54f5bb27` | `patchVerdict=pass` |
| `material/refresh-handoff-result.json` | `c7405e81bf6d77e25b5632d76fc241a352039b517903f22f53b140e320de99aa` | `mutationReady=true` |
| `material/material-apply-receipt.json` | `4bff1f5561b4928220cb41a29d22f447edef00273c8a120d8aaccf1b7d2a507a` | staged/live byte parity |

Package digest: `41f9ef8771eb9bde09f99eba980471031377a92b6ca0399369b13895a3905c68`.

## Live validation

- Dispatch Spec: `pass`.
- Execution-contract self-test: `pass`.
- Live execution contract: `pass`.
- JSON parse and scoped whitespace validation: `pass`.

## Claim ceiling

This proves a repaired planning contract only. It does not prove that the Goal
has started, any SWU has executed, any owner has approved later material, or
the add-on is candidate, canonical, generated, installed, admitted, released,
deployed, or production-ready.
