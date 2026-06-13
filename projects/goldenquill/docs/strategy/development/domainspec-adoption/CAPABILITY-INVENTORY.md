# DomainSpec Capability Inventory + First-Spec Recommendation

- Dispatch: `gq-domainspec-capability-inventory-2026-06-13` (route: `DISPATCH-CAPABILITY-INVENTORY.json`, validated pass)
- Date: 2026-06-13 · Mode: fanout, 5 readers, parent synthesis · Read-only (no repo mutated)
- Question answered: *"What can I already build a first spec with `../domainspec-core/implementation/domainspec`, and what tools/skills/agents are available?"*

## Bottom line

**Yes — a first DomainSpec spec is buildable now.** The framework, templates, worked examples, skills, agents, and a working stdlib validator all exist. The cheapest first target is **`goldenquill-promotion-governance`** — it already carries a near-complete DomainSpec doc set; the highest-value next move is to validate + complete it with DomainSpec tooling rather than author from scratch.

## 1. What a DomainSpec "first spec" is + minimal path

A spec is a **feature vertical slice**: `docs/features/<feature>/SPEC.md` (the index) carrying a **Concept Registry** (every concept typed to one of the ~24 meta-types `TAXONOMY.md`, namespaced `<feature>.<Concept>`) and a typed **Feature Concept Graph** (`From | Edge | To` using the 26 relationships in `RELATIONSHIPS.md`), plus only the aspect files the feature needs. Minimal slice per the template: **`SPEC.md` + `domain.md` + `queries.md`** (README line 421).

**Minimal authoring path** (source: `domainspec-firstspec-reader`):
1. **Project baseline (once)** — `domainspec-start` / `domainspec-interview-scope` → `PROJECT-OVERVIEW.md`, `INITIAL-DEFINITIONS.md`, `PROJECT-DECISIONS.md`, `HYPOTHESES.md`, `EXPERIMENT-CANDIDATES.md`; `domainspec-init` scaffolds `docs/registry.md`, `docs/glossary.md`, `docs/shared/governance-baseline.md` (mandatory prerequisite, ID G0).
2. **Discovery (soft gate)** — `domainspec-research-writer` → `domainspec-findings-writer` → `domainspec-discovery-writer`. Spec authoring HALTs without a discovery doc unless `--skip-discovery "<reason>"`.
3. **Author SPEC.md** — `domainspec-spec-feature` / `domainspec-spec-writer` + `templates/SPEC.md`: name + type every concept, fill the Concept Graph.
4. **Companions/aspects** — `architecture.md`, `glossary.md`, `STORIES.md` (default companions) + only-needed aspect files (`domain.md`, `operations.md`, `states.md`, `events.md`, `queries.md`, `workflows.md`, `mappings.md`, optional `rules.md`).
5. **Sync** — `domainspec-sync-registry` folds the concept table into the global registry/glossary.
6. **Derive tests / verify** — `domainspec-generate-tests` → `domainspec-verify-feature` / `domainspec-audit-alignment`.
Route everything via `domainspec-orchestrate`, or run end-to-end via `domainspec-pipeline`. Governance binds at every step: `AXIOMS.md` (A1 spec-before-code), `CONSTITUTION.md`, `governance-baseline.md` Feature Readiness Gate, folder-structure-constitution v3.0.0.

## 2. Skills (HIGH cluster for spec authoring)

DomainSpec engine skills live in `domainspec-core/implementation/domainspec/.claude/skills/` (NOT in the generic Arcanum suite):
- **domainspec-start / domainspec-init / domainspec-interview-scope** — baseline + scaffold + discovery.
- **domainspec-spec-feature** — author/evolve the feature SPEC.
- **domainspec-feature-glossary / domainspec-definitions-governance / domainspec-sync-registry** — concept/glossary/registry coherence.
- **domainspec-generate-tests / domainspec-verify-feature / domainspec-audit-alignment** — derive tests + verify.
- **domainspec-orchestrate (router) / domainspec-pipeline (end-to-end) / domainspec-brownfield-translation (lift existing content)**.
- **domainspec-decision-gate / domainspec-interview-kits** — resolve decisions, pressure-test.
Generic Arcanum complements (in both repos' `.claude/skills/`): **invoke, dispatch-spec, residuality-spec, constitution-governance, definitions-governance, feature-glossary** (HIGH); context-builder, scope-interview, decision-gate, distill, craft (MED). GoldenQuill's suite == domainspec-core's minus `close-session`; **no `domainspec-*` skills are installed in GoldenQuill** (engine lives only in domainspec-core).

## 3. Agents (HIGH cluster)

In `domainspec-core/implementation/domainspec/.claude/agents/` (45 defs; 25 `domainspec-*`, 18 generic `gsd-*`, 1 `mars-researcher`):
- **domainspec-orchestrator** (route) · **domainspec-interviewer** (discovery) · **domainspec-research-writer → domainspec-findings-writer → domainspec-discovery-writer** (fan-out discovery chain) · **domainspec-spec-writer** (authors SPEC + aspects) · **domainspec-registry-sync** · **domainspec-interviewer-kits** (grill/readiness pressure-test) · **domainspec-context-builder** (task context).
- Downstream (after a spec exists): planner, task-executor, test-designer, verifier, L1/L2/Δ categorical extractors, alignment/layering/tagging auditors, infra/UI/OTel agents.
- **GoldenQuill has no DomainSpec agents** — only `arcanum-stage-worker.md`. Running `domainspec-*` agents "inside" GoldenQuill requires wiring the definitions in (submodule/symlink) — see §6.

## 4. Tools / validators (with runnable status)

- **`audit_richness.py`** (`DS/scripts/`) — canonical L1 spec-richness audit (injectivity, faithfulness, fullness, M6 residue, cardinality, perturbation). **Pure stdlib — runs now**: `python3 audit_richness.py <spec-dir> [--json]`. **The primary "is my spec good enough" gate.**
- **`categorical-tooling-guard`** (`DS/internal_tools/`) — Gate-1 CI wrapper over the richness audit → `pass|flag|block`. Needs `pip install -e DS/internal_tools` (typer).
- **`tower-explorer`** (`DS/internal_tools/`) — Gate-0 vault/graph structural + origin-rung check.
- **TS validators** (`DS/tools/*.ts`, via `pnpm dlx tsx`): `generate-registry.ts` (→ registry.json), `validate-relationships.ts`, `validate-work-pack-coverage.ts`, `validate-orphans.ts`, `validate-doc-links.ts`, `validate-governance-chain.ts`.
- **`@domainspec/test-derivation-engine`** (`DS/tools/`) — deterministic docs→tests compiler; **currently an L0 skeleton (parser/δ stubbed)** — target-state.
- **`validate-dispatch.py`** (`GQ/.agents/skills/dispatch-spec/scripts/`) — Arcanum dispatch validator; **deps present, runs now** (used to validate both dispatch routes here).
- **Install note:** the Python `internal_tools` CLIs are **not installed** (`typer` absent). `audit_richness.py` works without install; for the rest run `pip install -e DS/internal_tools` (pydantic≥2.5, typer≥0.12, py≥3.11) or `pnpm dlx tsx` for the TS set.

## 5. First-spec target — ranked recommendation

| Rank | Target | Score | Why |
|---|---|---|---|
| **1 (recommended)** | **goldenquill-promotion-governance — L0 fixture-only event spine** | **9.5** | Already has a 14-file DomainSpec doc set (`SPEC.md`, `domain.md`, `events.md`, `operations/states/mappings/workflows.md`, `TEST-SPEC.md` T1–T35). Self-contained event-sourced contract; First Slice is `mutation_allowed=false`, zero canonical writes, Law-3 clean. Gates are human-ratification (DEC-OQ4 gates **L1 only**, not L0). |
| 2 | capital-logic-library — CIC×CLC card + rule-pack schema | 7 | Bounded, evidence-rich (taxonomy in CLAUDE.md), Law-3 clean, anti-coupling test load-bearing. But **no existing domain.md/events.md** — from-scratch; content is expert-gated. Strong second / first *net-new* spec. |
| 3 | tilth grant pipeline / council seats | 4 | Richest domain but largest/least bounded (13 work packs); WP-9/10/12 decision-gated on DEC-BC-POSTURE-VOCAB / DEC-BC-UI-BOUNDARY. Too big for first. |
| 4 | F-CLASS / classification routing | 3 | Cross-cutting, not standalone; inherits DEC-BC-POSTURE-VOCAB blocker. |
| 5 | WPFA CycleReceipt | 3 | Well-defined in CLAUDE.md but no `docs/features/` seed; sibling-coupled. |

Seed files for #1: `docs/features/goldenquill-promotion-governance/{SPEC,domain,events,operations,states,mappings,workflows,TEST-SPEC}.md` + `.craft/artifacts/BUILD-SPEC.md` (the L0 build-gap Define→Design→Plan) + CLAUDE.md anchors.

## 6. To apply to GoldenQuill (feeds route #2)

- **Validation needs no install:** `audit_richness.py` (stdlib) can run against `docs/features/goldenquill-promotion-governance/` from GoldenQuill today → baseline verdict.
- **Adoption-mode decision (operator):** to make the `domainspec-*` skills/agents resident in GoldenQuill, wire domainspec-core in as a **git submodule** (its intended consumption model) vs. run tooling in-place from `../domainspec-core`. Needed only for the agent/skill-driven authoring path, not for the first validation.
- **Two doc nits to reconcile** (from the promotion-governance BUILD-SPEC): `GAP-KPI-COUNT` (prose 47 vs enum 44 — enum authoritative) and `GAP-EVENT-COUNT` (name the 9-ingestion / 13-op-output axes; strike phantom 12).
- **DEC-OQ4** (three decision surfaces vs unified enum; rec. Option A) — surface to Josh; gates L1 only.

## Residue
- TAXONOMY meta-type count drift in domainspec-core (README 24 vs TAXONOMY.md 25) — upstream doc issue, not ours.
- `test-derivation-engine` is stubbed (can't auto-derive tests at full strength yet).
- Internal-tools Python CLIs need `pip install -e` before use.
