# Context Pack — SWU-WEG-003 Run 001

## Execution gate

- Task: `SWU-WEG-003` only.
- Mode: `standard`.
- Gate: `pass`.
- Dependency: SWU-WEG-002 receipt is `pass` and supplies the typed input schema.
- Runtime: local; no runtime handoff pack.
- Mutation boundary: one public evaluator and its status-ceiling fixture subtree.

## Decision pack

No blocker-level decision remains.

| Decision | Classification | Resolution | Reason |
| --- | --- | --- | --- |
| Status precedence | assumption | `pass < flag < block` by strictness | Exact task algorithm. |
| Reason ordering | assumption | proof, audition, comprehension, post-apply, correction, machine blocks, generation block, requested status | Preserves algorithm order and makes combined output deterministic. |
| Binding mismatch | deferred | SWU-WEG-004 supplies digest/reference admissibility | Implementing it here would absorb the next SWU. |
| Correction meaning | assumption | top-level `correction_refs` are active invalidators; `intent.correction_refs` is lineage | The v0.1 schema contains both fields but no separate open-state field. |
| Existing computed status | assumption | ignored as input and recomputed | Prevents a stale optimistic value from self-certifying. |
| Generation decision | assumption | an existing `block` lowers final status but generation policy is not computed here | Preserves separate decision ownership while respecting an explicit blocking gate. |

## Obligations

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| O1 | Execute exactly the selected SWU. | SWU manifest and W0 order | covered |
| O2 | Require a schema-valid receipt; invalid envelopes block. | task algorithm; SWU-WEG-002 schema | covered |
| O3 | Compute the strictest ceiling and final status deterministically. | task algorithm; proof model | covered |
| O4 | Candidate and unproven transports cannot exceed `flag`. | task edge case; canonical Whisper | covered |
| O5 | Required editorial audition, newcomer comprehension, and post-apply review independently lower the ceiling. | task algorithm | covered |
| O6 | Open correction references lower the ceiling. | task algorithm | covered |
| O7 | Explicit blocking axes or generation gate produce `block`. | task algorithm | covered |
| O8 | Source/render passes never fill missing human axes. | WEG-R1; task acceptance | covered |
| O9 | Requested `block` remains block; multiple reasons retain rule order. | task edge cases | covered |
| O10 | Accept `not_required` only through the transport-profile/schema contract. | task edge case; receipt schema | covered |
| O11 | Do not score language or comprehension semantics. | task handoff note; proof boundaries | covered |
| O12 | Do not implement exact digest/reference binding. | CTD-02; SWU-WEG-004 ownership | covered |
| O13 | Preserve the existing draft validator. | task done criteria | covered |
| O14 | Record evaluator version/hash and causal fixture report. | task synchronization | covered |
| O15 | Preserve public/private and unrelated dirty-submodule boundaries. | Submodule Discipline | covered |

## Selected sources

| Source | Digest | Selectors and purpose |
| --- | --- | --- |
| `work-pack/tasks/TASK-WEG-003-STATUS-CEILING.md` | `sha256:4d567a22e303c3752e89269d24ec1af6ef9c3fccc544a648de85aabbff44a1cf` | Full algorithm, scope, acceptance, and edge cases. |
| `work-pack/swu-manifest.json` | `sha256:a4d636cd96959f3d3b546f469abd5e36be3230c8f0e93727fbc92a883f14edf7` | Selected unit and expected receipt shape. |
| `work-pack/waves/W0.md` | `sha256:91c976813c317a2feb29daa2898d965600bbdfdfe505e02e64e91283c207de01` | Wave order and exit boundary. |
| `work-pack/session-evidence/SWU-WEG-002-RUN-001/receipt.json` | `sha256:4b284a208fe6b4b6b2d9cf3812e795aaa3703e30f1eb037a4ae081e9c2831539` | Passing schema dependency and policy residue. |
| `arcanum/spells/whisper/schemas/editorial-run-receipt.schema.json` | `sha256:e1b65e56dbdebaf13356ec46252fe748ff7ab6917826072f9b0b3860d57973bf` | Executable input shape and closed enums. |
| `arcanum/spells/whisper/schemas/examples/editorial-admission/bases/run-good-complete-newcomer.json` | `sha256:35eedbb29c5c61dd2e3d45da10cbcaa19b24f1a55a287276b8fc86d04c65c868` | Schema-valid positive base for causal mutations. |
| `arcanum/spells/whisper/development/fixtures/editorial-admission/manifest.json` | `sha256:a6c989e8db2368d2d12c517369ff3e48a8bae7c3864d6d148e684e0086fe43b4` | Frozen baseline control identities. |
| `.../WEG-RED-001-candidate-pass.json` | `sha256:86ecb04e77b74c03f23d66217414da466300b9cada36c0c6746b9fc63f40409e` | Candidate-with-human-pass expected ceiling. |
| `.../WEG-RED-002-comprehension-absent.json` | `sha256:be4b1461a7ac17df0ca7bfc1b0b05d0df9cdcc06b0ecd23eb0f11bad32b5c038` | Non-substitution expected ceiling. |
| `DESIGN.md` | `sha256:89dcf14c1e07bc74acc052625d5d1e203ab10bcda35830c778972861c4171b9e` | Final-status algorithm and failure behavior. |
| `DEFINE.md` | `sha256:60c0327180aa2e53a3cd7ea11dfd00d8d1e3f7d33b423127462e1beafd439d5e` | WEG-R1/R2 and proof model. |
| `work-pack/shared/cross-task-decisions.md` | `sha256:df5ffd80a4400ec7cdbab1bf298ab539da063c8e2e364b10381fc70c68eff803` | Decision separation and digest-binding ownership. |
| `arcanum/spells/whisper/README.md` | `sha256:20d430873a07ebc9ec02b89e77c94982168827755dced06f46685e70bea88f13` | Canonical candidate ceiling and human-judgment boundary. |
| `SUBMODULE-DISCIPLINE.md` | `sha256:b64a62ca8a95845b82ad60c2839b3dd51858a16e80096252e8f178dc8c74fb17` | Public boundary and dirty-submodule preservation. |

## Write and forbidden scope

Allowed:

- `arcanum/spells/whisper/tools/validate-whisper-run-receipt.py`
- `arcanum/spells/whisper/development/fixtures/editorial-admission/status-ceiling/**`

Forbidden:

- canonical `arcanum/spells/whisper/README.md`
- receipt or correction schemas
- evidence-binding and generation-admission fixture subtrees
- existing draft validator
- generated runtime
- private integration prose
- commits, pushes, or parent gitlink updates

## Exit rule

Pass only when schema-invalid input blocks, every table case returns the exact ceiling/final/reasons in deterministic order, candidate-with-all-human-pass returns `flag`, machine passes cannot replace absent comprehension, requested block stays block, the checked report replays exactly, the draft validator still loads, and the diff remains inside the allowed paths. Digest/reference mismatches remain explicit Experiment Harness residue until SWU-WEG-004.
