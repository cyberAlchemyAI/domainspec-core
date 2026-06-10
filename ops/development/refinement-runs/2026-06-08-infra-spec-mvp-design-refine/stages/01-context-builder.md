# Stage 01 — Context Builder Evidence Baseline

Capability: `context-builder` · Mode: `standard` · Runtime: native · Status: **pass**
Request frame: `--strict --emit both --handoff runtime --persist <run-folder>/context-builder`

## Task Frame

Build the evidence baseline for refining the infra-spec research synthesis into an MVP-ready design + plan. The research run already produced the corpus; this baseline selects the obligation-linked excerpts the Define/Design stages reduce into a candidate schema.

## Selectors and Obligation-Linked Excerpts

| Selector | Source | Obligation for the design |
| --- | --- | --- |
| Winning reading + candidate definition | `infra-spec-research-brief.md` | Design must be an *evidence substrate* (R3) with an operational-contract surface (R2); never let runtime evidence self-promote. |
| MVP critical path | `infra-spec-candidate-dag.md` | MVP spine = N1 runtime_profile → N2 services → N3 boundaries → N4 state_namespaces + N11 promotion_gate + N5 status floor. |
| Kept axes + minimal record | `infra-spec-schema-taxonomy-ledger.md` | 12 keep / merge actor→owner / drop event-queue from MVP; required floor fields enumerated. |
| Reuse substrate | `.claude/skills/dispatch-spec/dispatch.schema.yml` | Reuse `boundary`/`authority_map`/`receipt_expectation`/`state_namespace`/`promotion_split`/`gate` `$defs`; redefine only `boundary.kind` (network/secret/data/tenant). |
| Discipline constraints | `infra-spec-lean-transfer-ledger.md` | schema≠instance; specified/implemented/deployed/observed/validated/reflected/promoted as distinct; block≠fail; label analogies. |
| Net-new gap | `infra-spec-gap-hunt-ledger.md` (N12) | Add reversal/lifecycle obligations (rollback/migration/backup/retention) — absent today. |
| Promotion precedent | `infra-spec-cross-project-pattern-catalog.md`, `…-runtime-atlas.md` | goldenquill 7-state maturity + fail-closed signed gates = concrete model for N5/N11. |
| **Primary-source preset ladder (newly available)** | `implementation/domainspec/INFRA-SETUP.md` | Dev(0 tokens)/Single-VPS/Split-VPS/HA graduated presets — confirms N1 `runtime_profile` enum from a source, not just project-template copies. |

## Coverage Assessment

- **Strong**: every MVP node has source-backed evidence; the reuse substrate and discipline constraints are concrete.
- **Newly closed (vs research run)**: `implementation/domainspec` + `validation/poker-team` are now initialized → the preset ladder and a real exemplar are inspectable. The prior F1/F2 deferrals no longer bind this design.
- **Bounded gap (residue)**: the evidence layer (receipts/drift) still depends on real running instances; only goldenquill produces them → MVP ships the contract spine, evidence layer phased.

## Runtime Handoff Pack

- Target artifact: this run's `RESULT.md` + a candidate `infra-spec.schema.yml` and fixtures **inside the run folder** (no `formulae/` promotion).
- Write boundary: `ops/development/infra-spec-*` + this run folder (parent-owned). Submodule contents read-only.
- Frame handle: `context-builder-frame`; Evidence handle: this file.

## Verdict

`pass` — coverage sufficient to define the MVP design problem; one bounded evidence-layer gap recorded.
