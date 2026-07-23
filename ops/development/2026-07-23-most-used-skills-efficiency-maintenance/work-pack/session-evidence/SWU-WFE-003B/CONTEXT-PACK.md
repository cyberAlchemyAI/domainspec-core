# Context Pack: SWU-WFE-003B

Status: strict coverage pass

Mode: standard

Lifecycle route: Spellcraft revision with Experiment Harness validation and
declared runtime regeneration

## Task boundary

Make Invoke Refresh consume the SWU-WFE-003A material-package receipt before an
`apply-approved` mutation or ready handoff. Preserve proposal-only phase
completion and ensure it makes no material mutation claim. Regenerate only the
declared Codex and Claude Invoke packages.

## Obligation matrix

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| INV1B-O1 | `apply-approved` requires a current material package and validator-derived receipt. | task 003B acceptance; Refresh activation and mode gates | covered |
| INV1B-O2 | Only `patchVerdict=pass` plus `mutationHandoff=ready` can admit mutation readiness. | SWU-003A receipt schema; Design authority rule | covered |
| INV1B-O3 | Approved invalid, absent, stale, or mismatched material cannot emit readiness. | task acceptance; accepted INV-1 finding | covered |
| INV1B-O4 | Proposal-only requires no material package, remains phase-complete when its artifact is complete, and returns a gated/deferred non-mutation handoff. | accepted final narrowing; Refresh status table | covered |
| INV1B-O5 | Add a deterministic handoff resolver and causal valid/invalid/proposal integration fixtures. | task integration evidence; Experiment Harness contract | covered |
| INV1B-O6 | Bind the Refresh report/output contract to the material receipt identity, digest, paths, dependencies, authority, and validation fields. | Design INV-1→TS-2 interface | covered |
| INV1B-O7 | Preserve all existing Invoke fixture regimes. | existing full harness and SWU-003A receipt | covered |
| INV1B-O8 | Regenerate exact canonical Refresh semantics into `.agents` and `.claude`. | task generated parity requirement; current equal hashes | covered |
| INV1B-O9 | Preserve unrelated dirty Orchestrate generator work and all other generated skills. | live generator diff; exact package isolation | covered |
| INV1B-O10 | Do not consume the readiness receipt in Task Session yet; that is SWU-WFE-005. | task forbidden scope and WFE-D03 | covered |

## Selected evidence

| Path | Selectors | Why selected | SHA-256 |
| --- | --- | --- | --- |
| `work-pack/tasks/TASK-WFE-003-INVOKE-MATERIAL-PACKAGE.md` | 003B dependency, acceptance, write scope, validation | complete SWU contract | `094da570f7d753e2ee412c911daf78eebf80ec23d574ba767da7728991c3f666` |
| `work-pack/swu-manifest.json` | selected SWU, dependency, scope, done criteria | machine task state | `1470b3b6bf8355dcfa70f0de7afffe6a305eeb6a4e389d24a0472e9e16fc26c9` |
| `WORK-PACK.md` | program order, selected unit, gates | executable dashboard | `bd8e5112aad49349f7f8ebf239b3982e21797b7b9f1acc5cd5bc5e01f19544c9` |
| `DESIGN.md` | material validator, readiness interface, authority rule, WFE-D03 | integration semantics | `94bcee30991e0e4ef5975a71f3d5cbb884bb468918a7c6759a02dbffb39c0b19` |
| `../2026-07-22-most-used-skills-efficiency-review/findings.md` | INV-1 verdict and proposal-only narrowing | accepted behavior boundary | `0515af8d3dd746f8b020cad3515232afe5bb5cd2f6d60a00b567ee5e314018fd` |
| `work-pack/session-evidence/SWU-WFE-003A/receipt.json` | schema/validator/fixtures and passing evidence | technical dependency receipt | `20c0b98d7e15ed75312e3fbd352dabd6d61d7f8906027e642ba1184a035b72f7` |
| `arcanum/spells/invoke/refresh.md` | activation, report, gates, statuses, output/evidence contract | canonical integration target | `9793b9bce9457397316efe9da7247f5fb95bfde2f6f63f94773eec731dc7cdec` |
| `arcanum/spells/invoke/development/material_package_validator.py` | derived material receipt behavior | receipt producer | `5012c5767f6dc0e76a0e34a63f4b65342883c7969b52e9b86e910c4c63ee1426` |
| `.agents/skills/invoke/refresh.md` | generated Codex target | declared runtime parity target | `9793b9bce9457397316efe9da7247f5fb95bfde2f6f63f94773eec731dc7cdec` |
| `.claude/skills/invoke/refresh.md` | generated Claude target | declared runtime parity target | `9793b9bce9457397316efe9da7247f5fb95bfde2f6f63f94773eec731dc7cdec` |
| `arcanum/tools/bootstrap_arcanum.sh` | ordinary generated package writer | only declared generator; dirty-overlap check | `eed93902a1941cb40eb0560de40e2361ad969cdc72388c0c471009a317f9d257` |

## Constraints and decisions

- The material validator remains the sole producer of `patchVerdict`,
  `mutationHandoff`, and `packageDigest`.
- A deterministic Refresh handoff resolver consumes that receipt. It does not
  revalidate material or accept authored outcome fields.
- For `apply-approved`, missing or non-pass material evidence returns
  `phaseStatus=block`, `handoffStatus=blocked`, and `mutationReady=false`.
- For `proposal-only`, material evidence is not required. A complete proposal
  remains `phaseStatus=pass`; its handoff may be `gated` or `deferred`, and
  `mutationReady` is always false.
- Receipt bindings are reported, not inferred: package ID/digest, validated
  paths, dependency result, owner/publication results, authority classes, and
  validation commands.
- Task Session does not consume this receipt until SWU-WFE-005.
- The existing dirty Invoke development files are exactly the closed
  SWU-WFE-003A implementation and are the intended integration dependency.
- The dirty bootstrap edits affect Orchestrate support only. Invoke generation
  will occur in an isolated target before exact package synchronization.
- No subagents or runtime delegation are used.

## Validation surface

```bash
bash arcanum/spells/invoke/development/run-material-package-fixtures.sh
bash arcanum/spells/invoke/development/run-validation-fixtures.sh
git diff --check -- arcanum/spells/invoke .agents/skills/invoke .claude/skills/invoke
```

Baseline: SWU-WFE-003A focused and full harnesses pass. Canonical and generated
Refresh contracts are currently byte-identical but do not yet require a
material-package receipt before mutation readiness.

## Context Builder result

- Files selected: 11
- Obligation coverage: 10/10
- Uncovered obligations: 0
- Contradictions: 0
- Strict coverage: pass
- Mutation gate: pass
- Runtime handoff: none; execution is local and bounded
