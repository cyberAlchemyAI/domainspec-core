# Source Systems

ID: source-systems
Type: source
Status: active
Tags: repo-map, knowledge-system, submodule-boundary, arcanum-runtime, research-program
Confidence: high

## Summary

`domainspec-core` is a private umbrella repository that composes public Arcanum,
private DomainSpec implementation, validation harnesses, project workspaces,
research towers, generated runtime skill surfaces, observability, and dispatch
telemetry. Inventory should optimize lookup across these systems without
turning any generated read model into canonical authority.

## Detected Systems

| System | Source refs | Authority note |
| --- | --- | --- |
| Parent umbrella governance | `AGENTS.md`, `CLAUDE.md`, `SUBMODULE-DISCIPLINE.md` | Private parent owns composition and submodule discipline. |
| Public Arcanum source | `arcanum/README.md`, `arcanum/arcana/README.md` | Public capability framework; do not write private parent evidence into public artifacts. |
| Generated runtime skills | `.agents/skills/`, `.claude/skills/`, `.codex/commands/`, `.github/skills/` | Runtime mirrors/adapters; canonical sources usually remain under `arcanum/arcana/` or repo-local owner files. |
| Private DomainSpec implementation | `implementation/domainspec/`, `.gitmodules` | Submodule; v1 evidence source and private implementation surface. |
| Validation harness | `validation/poker-team/`, `.gitmodules` | Submodule; behavior and case-study validation surface. |
| Research program | `research/`, `projects/domainspec-v2/research/` | Research towers and experiment evidence; outputs are not canonical until promoted. |
| Local docs and decisions | `docs/`, `ops/`, `sessions/` | Parent-level governance and operational records. |
| Necronomicon harness | `.arcanum/necronomicon/README.md` | Local route/session/capability state; not a copied Arcanum definition store. |
| Observability | `.arcanum/observability/README.md`, `.arcanum/observability/config.json` | Runtime signals, run envelopes, hook evidence, and reflections. |
| Subagent dispatch | `implementation/domainspec/internal_tools/subagents-dispatch-hooks/`, `telemetry/agents/subagents-dispatch.yaml` | Governed dispatch lifecycle; explicit human confirm required before registered runtime dispatch. |
| Imported house_project vault | `cyberAlchemy-v2/authority/imports/house_project/docs/vault/`, `.arcanum/inventory/raw/manifests/2026-06-21-house-project-vault-import.md` | Private imported source snapshot for ontology, definition, constitution, axiom, graph, and lifecycle precedent. Inventory treats it as source evidence only; downstream owners must re-author any promotion. |

## Task Fit

- Use this entry when a downstream sigil needs to know where to look first.
- Use it to keep v2 repository structure work from mixing research, runtime,
  public framework, and private implementation authority.
- Use it to decide whether a source belongs in the private parent, public
  Arcanum, private implementation, validation harness, or a project-local tower.

## Residue

- The exact future v2 repository boundary is not yet selected.
- The dispatch ledger is dirty in the current worktree, so this inventory does
  not append or edit dispatch rows.
- Selector-level evidence-cards should be added after the cartographer research
  dispatch, if confirmed.
