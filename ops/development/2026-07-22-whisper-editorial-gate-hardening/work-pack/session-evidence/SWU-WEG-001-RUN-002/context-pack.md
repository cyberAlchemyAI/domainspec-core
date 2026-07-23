# Context Pack — SWU-WEG-001 Run 002

## Execution gate

- Task: `SWU-WEG-001` only.
- Mode: `standard`.
- Gate: `pass`.
- Owner entry receipt: `../SWU-WEG-001/S2-SPELLCRAFT-ACCEPTANCE.md`.
- Mutation boundary: the three public Whisper development surfaces declared by the task.
- Runtime changes: forbidden in this unit.

## Decision pack

No unresolved design choice is required for this unit.

The fixture format is a provisional JSON contract. It describes the future decisions and their expected reasons, but it is not the receipt schema or evaluator delivered by later units. Synthetic digests express exact-match and mismatch conditions without claiming that digest integrity is implemented.

## Obligations

| ID | Obligation | Evidence selector | Status |
| --- | --- | --- | --- |
| O1 | Execute exactly one selected unit. | `WORK-PACK.md` task board; `swu-manifest.json#/selected_swu` | covered |
| O2 | Restrict writes to the fixture baseline surfaces. | `TASK-WEG-001-FIXTURE-BASELINE.md#Smallest Working Unit` | covered |
| O3 | Include one green control and all seven named red controls. | `TASK-WEG-001-FIXTURE-BASELINE.md#Implementation detail` | covered |
| O4 | Give every case a stable ID, regime, expected verdict, and reason. | task done criteria | covered |
| O5 | Record absent enforcement as `not-enforced`. | task implementation detail; Spellcraft conditions | covered |
| O6 | Keep public fixtures product-neutral. | Spellcraft acceptance conditions | covered |
| O7 | Preserve the current candidate transport ceiling. | canonical Whisper candidate transport contract; `W0.md` promotion gate | covered |
| O8 | Inventory and parse fixtures and run an empty private-language sweep. | task verification | covered |
| O9 | Do not synchronize work-pack completion until acceptance evidence exists. | task synchronization | covered |
| O10 | Preserve unrelated submodule changes and do not publish. | `SUBMODULE-DISCIPLINE.md` | covered |

## Selected sources

| Source | Digest | Why selected |
| --- | --- | --- |
| `WORK-PACK.md` | `sha256:9f59837e54c24c017402ce0553965f6f2b2eaeb47f513d842c623c33cf6f0e3f` | Selected unit, order, and completion model. |
| `work-pack/tasks/TASK-WEG-001-FIXTURE-BASELINE.md` | `sha256:c525d9843392c58220ad3eabd4188575dffd7f258cfec3b97ccf262d2f6996b2` | Exact scope, cases, acceptance, and verification. |
| `work-pack/waves/W0.md` | `sha256:3ef3367f74016d9b5b15caed6df40943192b4b16632379026fce02462986b906` | Wave entry, order, exit, and candidate ceiling. |
| `work-pack/session-evidence/SWU-WEG-001/S2-SPELLCRAFT-ACCEPTANCE.md` | `sha256:a5040f5369631ddd7aa178e67f2c048e3f975851624edb9056299e9d2a08503c` | Lifecycle-owner acceptance and write conditions. |
| `work-pack/shared/context.md` | `sha256:114c4dab212e3d996fae028f4e4a473ad0c3f5b5711cf1c5a741974b2280bffe` | Shared language and project boundary. |
| `work-pack/shared/traceability.md` | `sha256:3ffa96f5a922f50e49d7f2785fe1c9b31331ef23bf1a66376bf96fe81e35d1b7` | Requirement-to-evidence mapping. |
| `arcanum/spells/whisper/README.md` | `sha256:20d430873a07ebc9ec02b89e77c94982168827755dced06f46685e70bea88f13` | Current candidate, intent, audition, and ceiling semantics. |
| `arcanum/spells/sigil-maintenance-loop/development/VALIDATION-EXPERIMENT.md` | `sha256:bd5db3bd5573e1329b0e770a7b1dfc4175a8d17f6774e85175729536552bc114` | Existing public Experiment Harness definition convention. |
| `.agents/skills/experiment-harness/SKILL.md` | `sha256:b753a8336dfea254f9180be44e40f2e0efb3e3990206e786e5fb15f8ea91752c` | Harness lifecycle and honest incomplete-state reporting. |
| `SUBMODULE-DISCIPLINE.md` | `sha256:b64a62ca8a95845b82ad60c2839b3dd51858a16e80096252e8f178dc8c74fb17` | Public submodule boundary and preservation rules. |

## Write and forbidden scope

Allowed:

- `arcanum/spells/whisper/development/VALIDATION-EXPERIMENT.md`
- `arcanum/spells/whisper/development/fixtures/editorial-admission/**`
- `arcanum/spells/whisper/development/editorial-admission-baseline.json`

Forbidden:

- canonical Whisper `README.md`
- schemas, evaluator tools, and generated runtime
- private integration prose
- commits, pushes, or parent submodule-pointer updates

## Exit rule

Pass only if all fixture JSON parses, every required case is inventoried, expected reason codes are present, the baseline says `not-enforced`, the privacy sweep is empty, and the diff stays inside the allowed public paths. A complete baseline makes `SWU-WEG-002` selectable; it does not validate or promote the revised spell.
