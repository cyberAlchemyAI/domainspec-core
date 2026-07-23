# Context Pack: SWU-WFE-003B after Option 1

Status: strict coverage pass

Mode: standard

Lifecycle route: Spellcraft revision with Experiment Harness validation and
exact generated-runtime synchronization

## Task boundary

Require an Invoke Refresh `apply-approved` handoff to consume a current passing
material-package receipt. Promote executable validation support to top-level
`scripts/` and its schemas to top-level `schemas/` so generated Invoke packages
are self-contained. Keep fixtures, reports, and runners under `development/`.

## Obligation matrix

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| INV1B-O1 | `apply-approved` requires a current material package and validator-derived receipt. | task 003B acceptance; accepted INV-1 finding | covered |
| INV1B-O2 | Only `patchVerdict=pass` plus `mutationHandoff=ready` can admit mutation readiness. | SWU-003A receipt schema; Design authority rule | covered |
| INV1B-O3 | Approved invalid, absent, stale, or mismatched material cannot emit readiness. | task acceptance; accepted INV-1 finding | covered |
| INV1B-O4 | Proposal-only remains phase-complete without a material package and never claims mutation readiness. | accepted INV-1 narrowing; Refresh status model | covered |
| INV1B-O5 | Runtime validator and schemas live outside generator-excluded `development/`. | Decision Gate Option 1; bootstrap generic support-copy contract | resolved |
| INV1B-O6 | Fixtures, reports, and test runners remain development-only. | Decision Gate Option 1 | resolved |
| INV1B-O7 | Add one deterministic handoff resolver plus causal valid, invalid, stale, absent, and proposal fixtures. | task integration evidence; Experiment Harness contract | covered |
| INV1B-O8 | Bind output to package identity/digest, paths, dependency, owner/publication, and validation fields. | Design INV-1 to TS-2 interface | covered |
| INV1B-O9 | Preserve existing Invoke regimes and exact generated runtime semantics. | SWU-003A receipt; generated parity boundary | covered |
| INV1B-O10 | Leave Task Session consumption, bootstrap implementation, other generated skills, promotion, and target applications untouched. | task forbidden scope; Option 1 boundary | covered |

## Selected evidence

| Path | Selectors | Why selected | SHA-256 |
| --- | --- | --- | --- |
| `WORK-PACK.md` | control fields, task board, SWU table, GAP-WFE-06, next action | live execution authority | `1b69130490548a89ccc70b5e36c997116d35995659831b510a21480ca74aa702` |
| `work-pack/swu-manifest.json` | SWU-WFE-003A/003B/004A | machine task state and exact scope | `257bf95b395944ba89e3d8aa308b2da8cf63fc641f4eab7135586628aaf74ee4` |
| `work-pack/tasks/TASK-WFE-003-INVOKE-MATERIAL-PACKAGE.md` | 003B dependency, boundary, scope, validation | bounded implementation contract | `15173d77ff38c31518da5536a3cd6dda16a47dcdf291236318eac93ef5a1a9ae` |
| `work-pack/session-evidence/SWU-WFE-003B/DECISION-GATE.md` | Option 1 and Gate result | resolves the only prior blocker | `4b8f13b80e0289892827aff449e66b034690785bdcf5379dedf3b0ccae9577f6` |
| `work-pack/session-evidence/SWU-WFE-003A/receipt.json` | producer paths and passing 13-case/full-harness evidence | technical dependency receipt | `20c0b98d7e15ed75312e3fbd352dabd6d61d7f8906027e642ba1184a035b72f7` |
| `DESIGN.md` | component table; INV-1 to TS-2 interface; WFE-D03 | integration semantics and owner split | `94bcee30991e0e4ef5975a71f3d5cbb884bb468918a7c6759a02dbffb39c0b19` |
| `../2026-07-22-most-used-skills-efficiency-review/findings.md` | finding 3; Invoke KEEP + FIX; final narrowing | accepted causal behavior | `0515af8d3dd746f8b020cad3515232afe5bb5cd2f6d60a00b567ee5e314018fd` |
| `arcanum/spells/invoke/refresh.md` | activation, report, mode gates, statuses, evidence contract | canonical integration target | `9793b9bce9457397316efe9da7247f5fb95bfde2f6f63f94773eec731dc7cdec` |
| `arcanum/spells/invoke/development/material_package_validator.py` | validator producer behavior before promotion | implementation source to relocate unchanged | `5012c5767f6dc0e76a0e34a63f4b65342883c7969b52e9b86e910c4c63ee1426` |
| `arcanum/tools/bootstrap_arcanum.sh` | `copy_generated_skill_support` only | proves top-level support is copied and `development/` excluded | `eed93902a1941cb40eb0560de40e2361ad969cdc72388c0c471009a317f9d257` |
| `.agents/skills/invoke/refresh.md`; `.claude/skills/invoke/refresh.md` | generated Refresh baselines | exact runtime targets before synchronization | `9793b9bce9457397316efe9da7247f5fb95bfde2f6f63f94773eec731dc7cdec` |

## Constraints and decisions

- The material validator is the only producer of the material verdict and
  package digest.
- The handoff resolver consumes that receipt; it does not revalidate staged
  bytes or trust authored status fields.
- `apply-approved` returns `block`/`blocked`/`mutationReady=false` unless the
  receipt is schema-valid, current, identity-matched, pass/ready, and has passing
  dependency/owner/publication results plus nonempty paths and validations.
- Proposal-only needs no material package and always has
  `mutationReady=false`.
- Runtime support moves to canonical `scripts/` and `schemas/`; tests remain
  under `development/`.
- Generate into an isolated target, inspect it, and synchronize only changed
  Invoke runtime files. Do not replace whole generated packages.
- Do not edit the already-dirty bootstrap, Task Session, other generated
  skills, lifecycle promotion state, or target applications.
- No subagents or delegated runtime are involved.

## Write scope

- `arcanum/spells/invoke/refresh.md`
- `arcanum/spells/invoke/scripts/`
- `arcanum/spells/invoke/schemas/`
- `arcanum/spells/invoke/development/`
- `.agents/skills/invoke/`
- `.claude/skills/invoke/`
- this SWU's session evidence and declared work-pack closeout inventory

## Validation surface

```bash
bash arcanum/spells/invoke/development/run-material-package-fixtures.sh
bash arcanum/spells/invoke/development/run-validation-fixtures.sh
isolated bootstrap generation for Invoke Codex and Claude packages
git diff --check -- arcanum/spells/invoke .agents/skills/invoke .claude/skills/invoke
```

## Context Builder result

- Files selected: 11
- Obligation coverage: 10/10
- Uncovered obligations: 0
- Contradictions: 0
- Strict coverage: pass
- Mutation gate: pass
- Runtime handoff: none; execution is local and bounded
