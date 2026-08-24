# Dispatch technique trace

Full dispatch document: not required. The route is one serial local Task
Session, has no delegation, no subagents, no protected context transfer, and
no reusable multi-capability graph.

| Technique | Applied to | Concrete effect | Validation |
| --- | --- | --- | --- |
| `sequence` | metadata -> tarball -> install -> canaries -> receipt | each later stage requires the earlier identity/result | stage result order is terminal and fail closed |
| `scu_swu_reduction` | `SWU-WCND-001` | one installed opaque artifact produces one black-box verdict | partial fetch/build evidence cannot pass the SWU |
| `recomposition_proof` | SWU -> runtime research | a terminal artifact verdict informs whether a later Craft experiment is worth planning | no Craft admission occurs here |
| `validation_loop` | integrity, install, addon, canaries, scope | every obligation has an exact check or terminal BLOCK | no substitute check counts as pass |
| `owner_boundary_check` | Invoke -> Task Session -> Invoke closeout | authoring, execution, and status sync remain separately receipted | terminal and owner receipts are required |
| `handle_handoff` | artifact paths/digests | owners consume exact handles rather than copied authority claims | path/hash/size binding |
| `residue_ledger` | provenance contradiction and failed attempt | unresolved source binding and test residue remain visible | no cleanup or silent waiver |
| `execution_receipt_handoff` | Task Session closeout | Work Pack changes only from terminal evidence | one declared closeout target |

Dispatch Spec result: pass for technique trace; `subagent_strategy=none`.
