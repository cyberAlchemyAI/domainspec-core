# TASK-TTP-005L - Lean Setup And Formal Scope

Status: `pending`
Layer: L1 formal-validation lane

## Objective

Verify Lean tooling, scaffold a repo-owned Lean/Lake project under the paper
package, and create the formal validation report skeleton.

## Write Scope

- `research/projects/mars/papers/triton-top2-backward-kernel/formal/`

## Implementation Detail

1. Record local versions for `lean`, `lake`, and `elan`.
2. Create `formal/lean-toolchain` pinned to the active Lean version unless a
   repository convention requires another version.
3. Create `formal/lakefile.toml`.
4. Create an initial Lean module namespace such as `TritonTop2`.
5. Create `FORMAL-VALIDATION-REPORT.md` with:
   - scope;
   - supported theorem targets;
   - explicit non-theorems;
   - validation command.

## Smallest Working Units

| SWU ID | Goal | Done Criteria | Verification |
| --- | --- | --- | --- |
| SWU-TTP-005L-A | Verify Lean tooling and pin version. | version commands recorded and toolchain file exists. | `lean --version && lake --version` |
| SWU-TTP-005L-B | Scaffold Lake project. | `lake build` succeeds in `formal/`. | `cd .../formal && lake build` |
| SWU-TTP-005L-C | Create formal report skeleton. | report names scope and non-theorems. | `test -f .../FORMAL-VALIDATION-REPORT.md` |

## Validation

```sh
lean --version
lake --version
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

