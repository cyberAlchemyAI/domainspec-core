# Template Selection

Status: pass

## Selected family

| Stage | Selected template/profile | Reason |
| --- | --- | --- |
| Define | Invoke spell-family definition plus glossary | the primary target is revision of the public `invoke` spell |
| Design | architecture companion | the change crosses Plan, Refresh, Task Session, validators, receipts, and observability |
| Plan | standalone implementation layering plus split work-pack | complexity is high and the work crosses lifecycle owners and public/private boundaries |
| Dispatch | full Dispatch Spec | the route spans Spellcraft, Sigil Development, deterministic validation, bounded execution, and reflection |
| Distill | automatic `validate` | mutation-capable handoff requires SWU atomicity, recomposition, hidden-gap, and first-unit checks |

## Output mode

`split`

The canonical executable hierarchy is:

```text
IMPLEMENTATION-LAYERING.md
WORK-PACK.md
  -> work-pack/waves/W*.md
  -> work-pack/tasks/TASK-*.md
  -> work-pack/swu-manifest.json
```

`EXECUTION-PACK.md` owns choreography only. Task contracts own SWU detail.

## Lifecycle routing

Because the target is a spell, Invoke stops after authoring and hands the
package to Spellcraft. Task Session is not the next owner until Spellcraft and
the adjacent Sigil Development owner accept the protocol and the selected
epoch's handoff-readiness verdict is `ready`.

