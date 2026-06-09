# Task Session Surface 001

Date: 2026-05-31
Task: `TASK-SURFACE-001`
SWU: `SWU-SURFACE-001`
Result: PASS

## Context Pack

Source count: 5 controlling artifacts:

- `ops/ARCANUM-SURFACE-MAP-AND-PLAN.md`
- `docs/decisions/install-profile-contract.md`
- `ops/development/TASK-SESSION-RUNTIME-006.md`
- `arcanum/tools/bootstrap_arcanum.sh`
- `arcanum/tools/arcanum`

Controlling constraints:

- Native runtime packages are the primary capability discovery and execution surface.
- `tools/arcanum` remains deterministic support for handles, adapter metadata, provenance, install profiles, and receipts.
- `tools/arcanum --exec` with native adapters prepares handoff/receipt contracts and must not spawn nested model-backed CLIs.
- `codex-exec` and `codex-bypass` remain explicit legacy opt-in only.
- Machine-global Codex home mutation is outside this SWU.

Strict coverage: pass.

## Decisions

Decision count: 1.

Accepted decision: native runtime skill surfaces are primary. The active/default contract must not say that `context-builder`, `invoke`, `interrogation`, or `distill` resolve through `tools/arcanum`.

Decision artifact:

- `docs/decisions/native-runtime-skill-surface.md`

## Runtime

Runtime: local
Adapter: none

## Gate Verdict

Pass.

This SWU only freezes the native-first contract and records it as a decision. It does not mutate machine-global Codex skills, root GitHub/Copilot skill packages, or generated runtime caches.

## Files Updated

- `docs/decisions/native-runtime-skill-surface.md`
- `ops/development/TASK-SESSION-SURFACE-001.md`

## Validation

Commands:

```bash
bash -n arcanum/tools/arcanum arcanum/tools/bootstrap_arcanum.sh arcanum/tools/install_arcanum.sh
rg -n "command-backed stage execution|resolve through tools/arcanum|tools/arcanum --exec --output|\\.codex/commands.*required|repository-local Arcanum command surface|deterministic Arcanum command dispatch" ops docs arcanum/arcana/refine arcanum/arcana/task-session arcanum/spells/invoke arcanum/tools -g "*.md" -g "*.sh"
```

Results:

- Shell syntax passed.
- Stale command-backed phrases remain in historical development evidence and install-wrapper areas; they are not rewritten by this SWU.
- The active decision record now states native runtime skills/packages first and `tools/arcanum` support second.

## Synchronized Records

- `TASK-SURFACE-001 / SWU-SURFACE-001` recorded as pass.

## Follow-Up

- Continue to `TASK-SURFACE-002 / SWU-SURFACE-002` for personal Codex staging only.
- Run a decision gate before promoting staged files into `/mnt/c/Users/vlad_/.codex/skills`.
