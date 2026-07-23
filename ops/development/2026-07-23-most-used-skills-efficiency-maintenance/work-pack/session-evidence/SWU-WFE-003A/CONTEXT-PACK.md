# Context Pack: SWU-WFE-003A

Status: strict coverage pass

Mode: standard

Lifecycle route: Spellcraft revision with Experiment Harness validation

## Task boundary

Build the deterministic material-package schema, validator, receipt, and causal
fixture matrix inside Invoke's development harness. This SWU proves package
validity only. It does not yet change Refresh handoff admission, generated
runtimes, target applications, or proposal-only phase semantics.

## Obligation matrix

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| INV1A-O1 | Structurally validate the material package and a stable machine receipt. | task inputs/output; existing Invoke schema conventions | covered |
| INV1A-O2 | Resolve staged source, output, and dependency bytes and compare exact digest and size claims. | task acceptance boundary; existing provenance validator | covered |
| INV1A-O3 | Reject missing output and an empty declared change. | task acceptance boundary | covered |
| INV1A-O4 | Reject absolute, traversing, or resolved escaping artifact paths and destination paths. | task path/owner escape boundary; repository containment convention | covered |
| INV1A-O5 | Reject target-inventory, lifecycle-owner, authority, publication, or approval-scope mismatch. | task inputs; Design owner/publication component | covered |
| INV1A-O6 | Reject a missing or stale dependency frontier. | task inputs; Design readiness interface | covered |
| INV1A-O7 | Validate canonical/generated mirror membership and declared exact parity. | task inputs; generated/canonical maintenance boundary | covered |
| INV1A-O8 | Derive verdict and handoff fields in the validator; authored approval never changes invalid material to valid. | accepted INV-1 finding; Design authority rule | covered |
| INV1A-O9 | Return `not-applicable`/`deferred` for a valid proposal-only non-mutation input. | task positive control; accepted final disposition | covered |
| INV1A-O10 | Add focused causal fixtures and compose them into the existing Invoke harness without replacing it. | task validation; Experiment Harness contract | covered |
| INV1A-O11 | Change only Invoke development files and leave Refresh/runtime integration for SWU-WFE-003B. | manifest write scope and program order | covered |

## Selected evidence

| Path | Selectors | Why selected | SHA-256 |
| --- | --- | --- | --- |
| `work-pack/tasks/TASK-WFE-003-INVOKE-MATERIAL-PACKAGE.md` | SWU-003A objective, inputs, output, acceptance, scope | complete SWU contract | `553d15aaa71741f1b440494f13347cdd8927b985c86ee435244412a8dc821aa5` |
| `work-pack/swu-manifest.json` | selected SWU, dependency, write scope, done criteria | machine task state | `4bff3b164bd443a0f26ffd1effb9331743b4ad28a085571170be670b2f9c17c0` |
| `WORK-PACK.md` | task/SWU rows, gates, gaps, current route | program order and lifecycle boundary | `93561208c3c151f66d187bafe7bb1189e0c4143fca11cc38d63df1e7a8c510fa` |
| `DESIGN.md` | material validator, readiness interface, authority rule, WFE-D01/D03 | implementation and non-framework semantics | `94bcee30991e0e4ef5975a71f3d5cbb884bb468918a7c6759a02dbffb39c0b19` |
| `../2026-07-22-most-used-skills-efficiency-review/findings.md` | INV-1 verdict and final narrowing | accepted defect; proposal-only exclusion | `0515af8d3dd746f8b020cad3515232afe5bb5cd2f6d60a00b567ee5e314018fd` |
| `arcanum/spells/invoke/refresh.md` | activation, mutation modes, mode gates, output semantics | current consumer contract preserved in this SWU | `9793b9bce9457397316efe9da7247f5fb95bfde2f6f63f94773eec731dc7cdec` |
| `arcanum/spells/invoke/development/run-validation-fixtures.sh` | fixture composition and report behavior | existing Experiment Harness integration point | `290d1a52cfae47ab5fdd4e0ece280bb1148afa2de257892dd15f8be4a54631c3` |
| `arcanum/spells/invoke/schemas/distill-execution-receipt.schema.json` | Draft 2020-12 and exact-artifact reference style | current Invoke schema convention | `2b4131f9eefeab81ab20962e1389961719387c26d3a61ed7d7cd12519d117a85` |
| `arcanum/spells/invoke/development/distill_provenance_validator.py` | digest resolution, schema errors, derived handoff | current Invoke validator convention | `bec51c363c4783237d21334d911d99206f30a9d4bbd650c7b9fe308e421a024e` |

## Constraints and decisions

- Package bytes live in an explicit staging root; target paths describe intended
  repository destinations and cannot be used to read arbitrary host paths.
- Both artifact and target paths reject absolute forms, `..`, and resolved
  containment escape.
- Exact references bind `path`, SHA-256, and byte size.
- Materialized packages require `apply-approved`, explicit approval, at least
  one non-empty change, at least one validation command, and complete target
  inventory coverage.
- Approval scope is exact-path based for this first contract; no glob language
  or inferred prefix authority is introduced.
- Public output rejects any private source artifact. Publication and authority
  classifications are declared per target and must be admitted by approval.
- Every required dependency ID must resolve to a validated dependency artifact.
- Exact mirror groups require canonical and generated output bytes to match.
  No overlay semantics are added in this SWU.
- Proposal-only carries no material changes and returns `patchVerdict:
  not-applicable`, `mutationHandoff: deferred`, and no package digest.
- The validator derives all outcome fields. Approval is an input authorization,
  never a validity override.
- The existing full Invoke harness remains the owner composition surface.
- Current scoped worktree overlap: none.

## Validation surface

```bash
bash arcanum/spells/invoke/development/run-material-package-fixtures.sh
bash arcanum/spells/invoke/development/run-validation-fixtures.sh
git diff --check -- arcanum/spells/invoke/development
```

Baseline: the full Invoke validation report at
`development/runs/20260723T013510Z.md` passes. The focused material-package
runner, schemas, validator, and fixtures are absent, which is the declared red
baseline.

## Context Builder result

- Files selected: 9
- Obligation coverage: 11/11
- Uncovered obligations: 0
- Contradictions: 0
- Strict coverage: pass
- Mutation gate: pass
- Runtime handoff: none; execution is local and bounded
