# Context Pack — SWU-WEG-002 Run 001

## Execution gate

- Task: `SWU-WEG-002` only.
- Mode: `standard`.
- Gate: `pass`.
- Dependency: SWU-WEG-001 receipt is `pass`.
- Lifecycle owner: Spellcraft acceptance remains valid for the ordered work pack.
- Runtime: local; no runtime handoff pack.
- Mutation boundary: two public schemas and their editorial-admission example subtree.

## Decision pack

No blocker-level choice remains.

| Decision | Classification | Resolution | Reason |
| --- | --- | --- | --- |
| JSON Schema dialect | assumption | Draft 2020-12 | Existing Arcanum JSON Schemas and validators use it. |
| Validation engine | assumption | Python `jsonschema` 4.10.3 | Already available and used in the public repository. |
| Supporting record schemas | assumption | `$defs` inside the run-receipt schema | The task declares two schema files; local definitions preserve that boundary. |
| Fixture execution | assumption | bounded runner under `schemas/examples/editorial-admission/` | Keeps replay evidence inside the declared example write scope and adds no runtime evaluator. |
| Policy checks | deferred | SWU-WEG-003 through SWU-WEG-005 | This unit validates shape only, not decision correctness or digest equality. |

## Obligations

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| O1 | Execute exactly the selected SWU. | SWU manifest and W0 order | covered |
| O2 | SWU-WEG-001 must pass first. | prior Task Session receipt | covered |
| O3 | Require stable run, transport, audience, and intent identity. | task data rule 1 | covered |
| O4 | Require four separate evidence-axis objects; absence is explicit. | task rules 2 and failure mode | covered |
| O5 | Bind present human evidence to artifact/surface SHA-256 fields. | task rule 3; CTD-02 | covered |
| O6 | Require typed approval and comprehension records without semantic scoring. | task rules 4 and 5; glossary | covered |
| O7 | Require producer and review stages for post-apply evidence. | task rule 6 | covered |
| O8 | Require computed decision fields but do not enforce policy consistency. | task rule 7; CTD-03 | covered |
| O9 | Permit residue; reject unknown statuses and malformed digests. | task rule 8 | covered |
| O10 | Allow `not_required` comprehension only when the profile does not require it. | task edge case | covered |
| O11 | Multiple approvals identify one selected approval. | task edge case | covered |
| O12 | Positive and negative fixtures must produce expected schema results. | acceptance boundary | covered |
| O13 | Use an available schema validator; do not add a standard-library substitute. | task handoff note; repository convention | covered |
| O14 | Preserve public/private and dirty-submodule boundaries. | Spellcraft receipt; Submodule Discipline | covered |

## Selected sources

| Source | Digest | Selectors and purpose |
| --- | --- | --- |
| `work-pack/tasks/TASK-WEG-002-RECEIPT-SCHEMA.md` | `sha256:053ed748e54d9f2539c24896582e8836fbc446866bfd07f32482ef5d013adf29` | Full task contract, rules, scope, and done criteria. |
| `work-pack/swu-manifest.json` | `sha256:10c79bccfba6a12c8075ea3a19448028d60ec88d5330317662701fdd58fb358c` | Selected unit, dependency, and expected receipt shape. |
| `work-pack/waves/W0.md` | `sha256:62c02a0f1ba81d931968bb0c186dd4e0c1566f40663b5afb3cc37a771eec447f` | Order and wave exit boundary. |
| `work-pack/session-evidence/SWU-WEG-001-RUN-002/receipt.json` | `sha256:beb80b621e4da925d7f331df660d465de2bddea5183c532d50c8f51394ee489c` | Passing dependency and frozen fixture baseline. |
| `work-pack/session-evidence/SWU-WEG-001/S2-SPELLCRAFT-ACCEPTANCE.md` | `sha256:a5040f5369631ddd7aa178e67f2c048e3f975851624edb9056299e9d2a08503c` | Lifecycle owner and public/private conditions. |
| `DESIGN.md` | `sha256:89dcf14c1e07bc74acc052625d5d1e203ab10bcda35830c778972861c4171b9e` | Sections 3.1–3.6 and decision separation. |
| `GLOSSARY.md` | `sha256:8d78da8bf4c076cb4b12fd42631d5154333b4c596dc2f9e6d876efabed1e78fd` | Evidence-axis and record meanings. |
| `work-pack/shared/cross-task-decisions.md` | `sha256:df5ffd80a4400ec7cdbab1bf298ab539da063c8e2e364b10381fc70c68eff803` | Digest binding and evaluator separation. |
| `arcanum/spells/whisper/development/editorial-admission-baseline.json` | `sha256:16265ac773749e71329cb585e5304dd204cc3c45d33ee2efdb532f61a4f87706` | Honest pre-schema state. |
| `arcanum/spells/whisper/development/fixtures/editorial-admission/manifest.json` | `sha256:a6c989e8db2368d2d12c517369ff3e48a8bae7c3864d6d148e684e0086fe43b4` | Stable baseline IDs and expected causal controls. |
| `arcanum/spells/whisper/schemas/README.md` | `sha256:78d0275256c944775caaf5cb94e5a5726c685032e45667f7d29d50fda2640166` | Existing Whisper schema-home authority. |
| `arcanum/runtime/orchestrate/schemas/receipt.schema.json` | `sha256:8eeb4acb6274a7343aa4ad3d89f1705af660dc8b82883028927eb15198e694e4` | Public Draft 2020-12 schema convention. |
| `arcanum/runtime/orchestrate/tests/preflight/test_preflight_contract.py` | `sha256:011bad859313e39cf1991632b2daeb8bc3c268c48e3bc25a0ccedd7acf54663e` | Existing `Draft202012Validator` execution convention. |
| `SUBMODULE-DISCIPLINE.md` | `sha256:b64a62ca8a95845b82ad60c2839b3dd51858a16e80096252e8f178dc8c74fb17` | Public boundary and dirty-submodule preservation. |

## Write and forbidden scope

Allowed:

- `arcanum/spells/whisper/schemas/editorial-run-receipt.schema.json`
- `arcanum/spells/whisper/schemas/editorial-correction-event.schema.json`
- `arcanum/spells/whisper/schemas/examples/editorial-admission/**`

Forbidden:

- canonical `arcanum/spells/whisper/README.md`
- existing draft validator and other tools
- status or generation policy evaluation
- generated native runtime
- private integration prose
- commits, pushes, or parent gitlink updates

## Exit rule

Pass only when both schemas are valid Draft 2020-12 documents, all expected-good cases validate, all expected-bad cases fail for their recorded schema reason, the corpus contains no semantic scoring field, the public privacy sweep is empty, and the submodule diff remains inside the declared paths. Schema success must not mark status or generation enforcement complete.
