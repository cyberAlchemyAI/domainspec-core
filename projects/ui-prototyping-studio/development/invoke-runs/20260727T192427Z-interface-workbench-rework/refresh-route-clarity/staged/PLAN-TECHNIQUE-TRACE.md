# Invoke Plan Dispatch Technique Trace

## Result

Status: `flag-current-plan-blocked`

The original direct handoff is no longer admissible. The current route is:

`invoke refresh status sync -> invoke plan remediation -> fresh governed Plan
Distill -> explicit SWU choice -> task-session`.

The completed Plan Distill found nine MAJOR and one MINOR issue. The remediation
pass remains non-mutating with respect to product code. It must reconsider the
selected techniques against regenerated SWU boundaries and choreography before
the Plan gate can pass.

## Selected Techniques

| Technique | Activation | Applied artifact or gate | Validation expectation |
| --- | --- | --- | --- |
| `sequence` | projection identity precedes refresh; refresh precedes regions; regions precede hardening | `EXECUTION-PACK.md`, wave files | every non-first SWU consumes a declared predecessor receipt |
| `scu_swu_reduction` | the UI rework contains independently verifiable mechanics and regions | `SWU-MANIFEST.json`, task files | one primary behavior and one independent acceptance boundary per SWU |
| `recomposition_proof` | atomic SWUs must still close the approved six-region Design | `PLAN-DISTILL.md` | every SWU maps to DDR, view, and witness obligations |
| `validation_loop` | each behavior needs positive and negative evidence before promotion | task validation tables, `PLAN-VALIDATION-STRATEGY.md` | each SWU has a runnable check and expected receipt |
| `owner_boundary_check` | Invoke cannot execute or select implementation | `WORK-PACK.md`, `PLAN-TRANSPORT.md` | `selected_swu: none`; Task Session owns later mutation |
| `handle_handoff` | runtime context must be bounded | task source anchors and design links | Task Session/Context Builder receives handles, not copied repository context |
| `residue_ledger` | human/cross-browser/release and shared-Inventory gaps remain | `work-pack/shared/cross-task-gaps.md` | every gap has an owner and route |
| `execution_receipt_handoff` | Task Session closeout must be deterministic | `WORK-PACK.md` closeout table | every mutation SWU declares source receipt, targets, baseline, deltas, owner validation, receipt, and successor |

## Skipped Techniques

- Full execution dispatch JSON: still skipped because no implementation
  execution is authorized. The completed Plan Distill validation dispatch is
  recorded separately; its findings now feed `invoke plan` remediation.
- `fanout`, `tournament`, and `dialectic`: skipped for execution; overlapping
  runtime files require serial SWUs.
- `authority_split_gate`: represented directly by `owner_boundary_check`
  because no authority transfer or promotion is proposed.
