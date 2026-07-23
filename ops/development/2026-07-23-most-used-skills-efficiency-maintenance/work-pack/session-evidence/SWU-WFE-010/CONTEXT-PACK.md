# Context Pack: SWU-WFE-010

Status: strict coverage pass

Mode: standard

Lifecycle route: Spellcraft for Invoke

## Task boundary

Add one machine resolver that reports Invoke artifact authoring, registry
release, and mutation-runtime readiness as independent evidence axes. Preserve
the existing per-run active-mode evaluator and material-package integration,
but prevent either from being mistaken for a collapsed capability status.
Keep `full` and `validate` deferred and non-mutation-capable.

## Obligation matrix

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| INV2-O1 | Resolver emits exactly three independent machine axes. | TASK-WFE-010 data contract | covered |
| INV2-O2 | Artifact status is `pass`, `flag`, `block`, or `unsupported` from its own typed receipt. | rule 1 and deferred rule | covered |
| INV2-O3 | Registry release is true only from a current owner receipt bound to the capability table digest. | rule 2 | covered |
| INV2-O4 | Runtime readiness is true only from a valid material receipt plus current mode-specific runtime gates. | rule 3 and INV-1 receipt | covered |
| INV2-O5 | Plan can be authored while registry and runtime remain false. | acceptance boundary | covered |
| INV2-O6 | Evidence for one axis never changes either other axis. | split analysis and fixture matrix | covered |
| INV2-O7 | `full` and `validate` remain unsupported/deferred and runtime false despite supplied receipts. | rule 4 | covered |
| INV2-O8 | Requests using a legacy collapsed capability field fail explicitly. | rule 5 | covered |
| INV2-O9 | Existing active-mode evidence and Refresh material-package suites remain green. | compatibility boundary | covered |
| INV2-O10 | Canonical and both generated Invoke runtime packages remain synchronized. | generated-runtime policy | covered |

## Selected evidence

| Path | Selectors | Why selected |
| --- | --- | --- |
| `work-pack/tasks/TASK-WFE-010-INVOKE-STATUS-CEILINGS.md` | objective, axes, precedence, acceptance | complete SWU contract |
| `arcanum/spells/invoke/mode-capabilities.json` | seven mode states and handoff rules | machine capability base |
| `arcanum/spells/invoke/development/invoke_mode_capabilities.py` | active/deferred per-run evaluator | compatibility consumer |
| `arcanum/spells/invoke/plan.md` | active L2 authoring boundary | target witness |
| `arcanum/spells/invoke/refresh.md` | material receipt and runtime readiness | INV-1 integration |
| `arcanum/spells/invoke/scripts/material_package_validator.py` | material-package receipt semantics | runtime evidence producer |
| `work-pack/session-evidence/SWU-WFE-003B/receipt.json` | passing INV-1 dependency | producer receipt |

## Baseline and overlap

- The seven-mode table is current; five modes are active and `full`/`validate`
  are deferred.
- Existing focused mode fixtures pass 13/13 and 5/5.
- Current `refresh.md`, material schemas/scripts, validation runner, and their
  generated mirrors contain earlier SWU-WFE-003B work. Preserve it.
- No three-axis production resolver or status schemas exist.

## Mutation strategy

Add production request/result schemas and resolver under canonical Invoke
`schemas/` and `scripts/`. Extend the mode table with axis definitions and
per-mode runtime gates. Add a focused causal matrix under `development/` and
include it in the existing validation runner. Clarify the status-axis contract
in README, Plan, Refresh, and validation documentation. Generate Invoke in an
isolated target and synchronize only the two Invoke runtime directories.

## Validation surface

```bash
bash arcanum/spells/invoke/development/run-capability-status-fixtures.sh
bash arcanum/spells/invoke/development/run-validation-fixtures.sh
git diff --check -- \
  arcanum/spells/invoke \
  .agents/skills/invoke \
  .claude/skills/invoke
```

## Context Builder result

- Files selected: 7
- Obligation coverage: 10/10
- Uncovered obligations: 0
- Contradictions: 0
- Strict coverage: pass
- Mutation gate: pass
- Runtime handoff: isolated canonical regeneration for Invoke only
