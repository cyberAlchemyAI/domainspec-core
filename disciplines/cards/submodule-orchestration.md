# Submodule Orchestration Discipline

Status: candidate
Steward: umbrella maintainer
Scope: PRIVATE (umbrella root only — must not migrate into the public arcanum catalog)

## Purpose

Govern how the `domainspec-core` umbrella composes and advances its submodules: **submodule-first, parent-last** commit ordering, branch-tracking (no detached HEADs), pushing a submodule commit before bumping the parent gitlink, and preserving the **open/private boundary** (public `arcanum` vs the private parent + `implementation/domainspec` + `validation/*`).

## Boundary

This discipline names the multi-repo orchestration practice. It does not own:

- the content of any individual submodule,
- per-submodule build tooling or language defaults,
- the `.gitignore` tracked-vs-ignored decision (public [gitignore discipline](../../arcanum/disciplines/cards/gitignore.md) owns that),
- secret management beyond keeping private content out of the public submodule.

Enforcement routes through the Makefile targets and a future constitution; mutation of this card routes through the private discipline catalog.

## Evidence

- [SUBMODULE-DISCIPLINE.md](../../SUBMODULE-DISCIPLINE.md) - the full prose rules (submodule-first/parent-last, branch tracking, open/private boundary, setup/diagnose).
- [Makefile](../../Makefile) - `bump-check` (refuses a parent gitlink pointing at an unpushed submodule commit), `sync`, `doctor`, `config` — the de-facto validator for this discipline.
- [CLAUDE.md](../../CLAUDE.md) - the same rules restated as agent instructions (evidence the practice recurs across surfaces and has caused drift: stale gitlinks, detached HEADs, the uninitialized nested submodule).

## Validation

- Mode: mixed
- Check: `make bump-check` and `make doctor` (deterministic), plus review against SUBMODULE-DISCIPLINE.md for the open/private boundary (prose).
- Latest result: pass (this session: a submodule commit was pushed before the parent gitlink was bumped; `make bump-check` passed).

## Quality Bar

A useful submodule-orchestration entry must:

- name the commit ordering (submodule-first, parent-last) and the push-before-bump rule,
- require branch-tracking (no detached HEAD) and name the `make sync` recovery,
- preserve the open/private boundary (never private content into public `arcanum`),
- cite the Makefile targets as the deterministic check,
- name the next hardening move (consolidate duplicated prose; route to a constitution).

## Promotion Guardrail

This discipline can recommend a constitution + validator route, but it cannot promote any submodule's content, registry, ontology, glossary, sigil, or spell. Advancing beyond `candidate` requires the duplicated rules to be consolidated behind the Makefile validator and a named constitution with a mutation boundary.
