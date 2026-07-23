# Context Pack: SWU-WFE-008B

Status: strict coverage pass

Mode: standard

Lifecycle route: Spellcraft for Whisper plus the existing Arcanum bootstrap
generator owner

## Task boundary

Add one optional manifest hook to the existing bootstrap spell-package path.
Generate Whisper in an isolated target, apply only its admitted additive
fragments and copied files, validate both runtime packages, then synchronize
only `.agents/skills/whisper/` and `.claude/skills/whisper/` into the live
repository. Preserve all unrelated bootstrap changes.

## Obligation matrix

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| WH1B-O1 | `bootstrap_arcanum.sh` remains the sole runtime generator. | WFE-D08; task scope | covered |
| WH1B-O2 | Overlay hook is optional and activates only for an admitted manifest. | 008A receipt and manifest validator | covered |
| WH1B-O3 | Canonical package is generated before any overlay mutation. | bootstrap spell loop | covered |
| WH1B-O4 | Overlay may insert only declared fragments and copy only declared files. | 008A manifest contract | covered |
| WH1B-O5 | Codex and Claude receive the same admitted semantic body and preset payloads. | task transaction boundary | covered |
| WH1B-O6 | All six canonical gate/status/authority controls survive. | manifest protected controls | covered |
| WH1B-O7 | `business_plan` and `live_presentation` remain canonical support. | canonical package source | covered |
| WH1B-O8 | `product_research_blueprint` comes only from the private payload source. | private manifest and payload digests | covered |
| WH1B-O9 | Generated packages contain no undeclared body or preset difference. | validator `--check-generated` | covered |
| WH1B-O10 | Unrelated generated skills and pre-existing Orchestrate bootstrap edits are preserved. | isolated generation and scoped package copy | covered |

## Selected evidence

| Path | Selectors | Why selected |
| --- | --- | --- |
| `work-pack/tasks/TASK-WFE-008-WHISPER-RUNTIME-COMPOSITION.md` | 008B behavior and transaction boundary | complete SWU contract |
| `work-pack/session-evidence/SWU-WFE-008A/receipt.json` | admitted composition dependency | producer receipt |
| `arcanum/tools/bootstrap_arcanum.sh` | `write_runtime_skill_packages` and current dirty diff | sole generator and overlap boundary |
| `arcanum/runtime/overlays/scripts/validate_runtime_overlay.py` | admission and generated parity | deterministic guard |
| `.arcanum/runtime/overlays/whisper/manifest.json` | targets, fragments, files, controls | private machine authority |
| `.agents/skills/whisper/` | current local overlay witness | generated target |
| `.claude/skills/whisper/` | stale canonical witness | generated target |

## Mutation strategy

The bootstrap `--force` path can clear a complete runtime skill root, and its
sigil selector does not support `none`. It will therefore run only against an
isolated temporary target with `--spells whisper`; unrelated generated
packages remain disposable in that target. After full generated parity passes,
only the two Whisper package directories are synchronized to the live
repository.

## Validation surface

```bash
python3 arcanum/runtime/overlays/tests/test_runtime_overlay.py
bash arcanum/tools/bootstrap_arcanum.sh \
  --target <isolated-target> \
  --spells whisper \
  --profiles repo-codex,claude \
  --force
python3 arcanum/runtime/overlays/scripts/validate_runtime_overlay.py \
  --manifest <isolated-target>/.arcanum/runtime/overlays/whisper/manifest.json \
  --target whisper \
  --repo-root <isolated-target> \
  --check-generated
```

## Context Builder result

- Files selected: 7
- Obligation coverage: 10/10
- Uncovered obligations: 0
- Contradictions: 0
- Strict coverage: pass
- Mutation gate: pass
- Runtime handoff: none; generation is deterministic and isolated
