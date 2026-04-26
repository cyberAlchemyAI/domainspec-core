# Research Knowledge Stack Contract

Purpose: standardize how definitions, references, context, and resources become executable research assets.

Scope: all new and modified experiments in this project.

## Knowledge Stack Model

| Layer | Artifact | Purpose |
|---|---|---|
| Definitions | `definitions/DEFINITIONS-INDEX.md` | stable meaning for claim, metric, and protocol terms |
| References | `sources/REFERENCE-LEDGER.md` | authoritative citations with source IDs and pin metadata |
| Context | `experiments/<experiment-key>/context.md` | experiment-scoped synthesis across definitions and references |
| Resources | `experiments/<experiment-key>/sources.md` + `inventory/*.md` | executable source set for data capture and analysis |

## Contract Rules

| Rule ID | Rule | Enforcement |
|---|---|---|
| RK1 | Claims and protocols must use terms declared in the definitions index. | G1 blocks on undefined critical terms. |
| RK2 | Any reference used as decision authority must appear in the reference ledger with pin metadata or explicit waiver. | G2 blocks on unpinned authoritative references. |
| RK3 | Every experiment must include a context bundle at `experiments/<experiment-key>/context.md`. | Execution blocked before S7 when context bundle is missing. |
| RK4 | Context bundle must map claim IDs, key definitions, primary references, and open conflicts. | G1 or S6 returns NEEDS-REVISION on missing mappings. |
| RK5 | Primary references must be source-cataloged and inventory-linked before execution. | G3 blocks when primary references lack inventory coverage. |
| RK6 | Conflicts between references must be logged explicitly in context bundle. | Analysis stage flags conclusion validity risk if conflicts are hidden. |

## Required Fields By Artifact

### Definitions index
- definition_id
- term
- scope
- canonical meaning
- linked claims

### Reference ledger
- reference_id
- citation
- source_id (if cataloged)
- pin metadata (DOI/ISBN/commit/hash/archive)
- authority level (primary/supporting/fallback)
- usage scope (paper/protocol/analysis)

### Context bundle
- experiment scope and claim target
- source role matrix
- terminology normalization map
- metric definition map
- conflict log
- open risks and follow-up actions

## Gate Coupling

| Gate | Additional Knowledge-Stack Obligation |
|---|---|
| G1 | protocol includes definition anchors + context bundle path |
| G2 | authoritative references are pinned and ledgered |
| G3 | primary references/resources have inventory linkage |
| G4 | run metadata references context bundle version when applicable |

## Related Artifacts

- `definitions/MARS-PIPELINE.md`
- `protocols/MARS-PROTOCOL-CHECKLIST.md`
- `definitions/EXPERIMENT-BUNDLE-CONTRACT.md`
- `templates/definitions-index-template.md`
- `templates/reference-ledger-template.md`
- `templates/context-bundle-template.md`
