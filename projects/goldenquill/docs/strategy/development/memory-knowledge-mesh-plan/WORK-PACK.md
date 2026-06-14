# Work Pack: Memory / Knowledge Mesh

Date: 2026-05-31
Status: active
Complexity: medium
Gate status: pass for L0, flagged for later code/test tasks

## Objective

Make Golden Quill's memory and knowledge layer production-ready by first mapping the current repository truth, then adding parity checks, evidence-packet structure, authority classification, and Reflection Packet activation experiments.

## Scope

In scope:

- `MEMORY.md`, `lessons.md`, and institutional memory mirrors
- `pipeline/memory/*`
- `pipeline/cli/tilth_memory_query.py`
- `scripts/memory_size_check.sh`
- `pipeline/cards/*`
- `pipeline/knowledge_packs/*`
- `pipeline/seats/scribe/knowledge_packs.py`
- `pipeline/vault/*_query_skill.py`
- `golden_quill_substrate/memory.py`
- `golden_quill_substrate/contracts.py`
- Reflection Packet blueprint and policy references

Out of scope:

- client org content
- loading multiple `orgs/<slug>/PROJECT_CONTEXT.md` files
- production code changes that cannot be validated locally
- model-provider or router changes

## Task Board

| Task | Layer | Status | Output |
| --- | --- | --- | --- |
| TASK-MK-001 | L0 | completed | `docs/MEMORY_KNOWLEDGE_LAYER_INDEX.md` |
| TASK-MK-002 | L0 | completed | validation notes in task-session report |
| TASK-MK-003 | L1 | blocked | stale count parity needs test runner or approved substitute validation |
| TASK-MK-004 | L1 | pending | register-count parity test |
| TASK-MK-005 | L2 | pending | `MemoryEvidencePacket` schema fixture |
| TASK-MK-006 | L3 | pending | authority classifier design |
| TASK-MK-007 | L4 | pending | Reflection Packet activation experiment brief |
| TASK-MK-VERIFY | all | pending | readiness report |

## Ready SWUs

### SWU-MK-001: Current-Truth Layer Index

Create a repository-local index that explains each memory/knowledge surface, its authority, mutation rules, validation path, and Arcanum equivalent.

Done when:

- index file exists
- no org context is read
- live memory CLI and memory size checks pass
- static review finds no deprecated customer-facing posture vocabulary in new artifacts

### SWU-MK-002: L0 Validation

Validate the index against current files and record results in the task-session report.

Done when:

- schema/context JSON validates
- memory CLI list smoke passes
- `scripts/memory_size_check.sh` passes
- static grep has no unresolved placeholders

## Blocked / Flagged SWUs

### SWU-MK-003: Register Count Parity

Update stale documentation/docstrings that still describe the memory query surface as `13 registers` when live runtime reports 15.

Blocked reason:

- current shell has no `pytest` module and no usable project `.venv`; code-adjacent parity should wait for a runnable test surface or an explicitly accepted substitute.

Suggested unblock:

- restore the project virtualenv, or
- approve substitute validation with `python3 -m compileall` plus CLI smoke if the change remains documentation-only.

## Validation Surface

Required for L0:

- `python3 -m json.tool` for JSON artifacts
- `python3 -m pipeline.cli.tilth_memory_query --format json list-registers`
- `scripts/memory_size_check.sh`
- `rg` static review over new files

Required for L1+:

- all L0 checks
- targeted pytest once available
- compile/static checks for changed Python modules
