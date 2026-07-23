# Experiment Report: SWU-WFE-010

- Verdict: `PASS`
- Capability-status tests: 13/13
- Active-mode matrix: 5/5 authored-only and 5/5 all-axis controls
- Deferred-mode matrix: 2/2 unsupported and runtime-false
- Material-package regression suite: 19/19
- Full Invoke deterministic suite: pass
- Generated Codex/Claude parity: exact

## Independent axis proof

| Evidence supplied | Artifact authored | Registry released | Runtime ready |
| --- | --- | --- | --- |
| Plan artifact receipt only | `pass` | `false` | `false` |
| registry owner receipt only | `block` | `true` | `false` |
| material plus mode-runtime receipts only | `block` | `false` | `true` |
| all matching receipts | `pass` | `true` | `true` |
| any receipts for `full` or `validate` | `unsupported` | `false` | `false` |

Registry receipts bind the current capability-table SHA-256 and require both
deterministic-validation and live-regime pass evidence. Runtime receipts bind
the same digest, the material-package identity/digest, and the exact
mode-specific gate set.

## Causal controls

Stale registry/runtime digests, missing runtime gates, a material receipt
without a mode-runtime receipt, and cross-mode artifact evidence cannot open
their target axis. A request containing a legacy collapsed `status` field is
schema-rejected.

The first full-suite run correctly detected stale generated `refresh.md`
mirrors. Invoke was regenerated in an isolated target, only the two Invoke
runtime directories were synchronized, and the full suite then passed.

## Boundary

This proof exposes evidence ceilings; it does not issue a registry owner
receipt, release Invoke, enable `full` or `validate`, execute a mutation, or
promote a capability.
