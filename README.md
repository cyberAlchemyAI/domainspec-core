# DomainSpec Research Hub (Unified 3-Project Workspace)

This repository contains two intertwined research projects:

1. **DomainSpec** — Domain-driven software development through structured meta-types, deterministic test derivation, and layered governance
2. **Meta-Meta Framework** — Generalization of DomainSpec principles to any agentic system requiring autonomous coordination, self-improvement, and knowledge navigation

## Canonical Operating Model

This workspace runs as a unified 3-project system:

1. **DomainSpec implementation (source of truth):** `/home/vrondelli/projects/poker-team/domainspec`
2. **Research orchestration hub:** `/home/vrondelli/projects/domainspec-core`
3. **Validation harness:** `/home/vrondelli/projects/poker-team`

Ownership rules:

- **Implementation changes** happen in the DomainSpec repository (`poker-team/domainspec`).
- **Research design, data, and analysis** happen in `domainspec-core/research`.
- **Runtime validation and case-study evidence** come from poker-team behavior and feature slices.

## Repository Structure

```
domainspec-core/
├── research/
│   ├── experiments/              # E1-E10 (DomainSpec) + E11-E20 (Meta-Meta)
│   ├── data/                     # Raw JSONL experiment data (append-only)
│   ├── results/                  # Structured analysis outputs
│   ├── sources/                  # SOURCE-CATALOG + inventory
│   ├── inventory/                # Extracted knowledge entries (generalized)
│   ├── EXPERIMENTS.md            # DomainSpec experiments (E1-E10)
│   ├── EXPERIMENTS-META.md       # Meta-Meta framework experiments (E11-E20)
│   └── domainspec-paper.md       # Research paper (evolving)
├── implementation/
│   ├── domainspec/               # Git submodule to live DomainSpec implementation source-of-truth
│   ├── ARCHITECTURE.md           # Local mirror for research reference
│   ├── TAXONOMY.md               # Local mirror for research reference
│   ├── RELATIONSHIPS.md          # Local mirror for research reference
│   ├── GOVERNANCE-ATTENUATION.md # Local mirror for research reference
│   ├── CONSTITUTION.md           # Local mirror for research reference
│   ├── TEST-PIPELINE.md          # Local mirror for research reference
│   └── PHASED-PLAN.md            # Execution roadmap
└── validation/
    └── poker-team/               # Validation repository (git submodule)
```

## Three Research Tracks

### Track 1: Validate DomainSpec (E1-E10)
**Claims:** C1–C4 in the research paper

- **E1–E5:** Derivation determinism, test coverage, mutation testing
- **E6–E10:** Vocabulary sufficiency, cross-feature composition, governance effectiveness

**Validation gates:** All success criteria PASS per experiment; analyst 10-step review

### Track 2: Build Meta-Meta Framework (E11-E20)
**Claims:** CM1–CM4 about generalizing governance to any agentic system

- **E11–E15:** Governance signals, outer-loop feedback, multi-agent conversation
- **E16–E20:** Agent specialization, cost accounting, human-agent alignment, cross-domain transfer

**Validation gates:** Signal extraction works; agents improve based on feedback; human agreement > 80%

### Track 3: Integration & Scaling (E21+)
**Apply both frameworks to:**
- Non-software research domains (supply chain optimization, policy analysis)
- Production-scale poker-team system with full agentic ADLC

---

## Phased Development Plan (DomainSpec)

See [PHASED-PLAN.md](implementation/PHASED-PLAN.md) for full 8-phase roadmap.

| Phase | Focus | Status |
|-------|-------|--------|
| 1 | Hypothesis validation (E1-E5) | 🔄 In progress |
| 2 | Governance foundation (E6-E8, signals) | 🔄 In progress |
| 3 | Composition stress testing (E9-E10) | ✅ E9 complete |
| 4 | Agent role definitions (PO, QA, Dev, Stakeholder) | ⏳ Starting week 3 |
| 5 | Feature discovery protocol (adversarial agents) | ⏳ Week 4 |
| 6 | Multi-agent conversation (autonomous stories) | ⏳ Week 5-6 |
| 7 | Autonomy & optimization (no human-in-loop) | ⏳ Week 7 |
| 8 | Meta-governance loop (self-tuning) | ⏳ Week 8 |

---

## Key Artifacts

- **Research paper:** `research/domainspec-paper.md` (evolving, synced with experiments)
- **Source catalog:** `research/sources/SOURCE-CATALOG.md` (validated external sources)
- **Knowledge inventory:** `research/inventory/INVENTORY-INDEX.md` + per-entry files (generalized domain models, papers, tools, frameworks)
- **Experiment protocols:** `research/experiments/EX-*.md` (one per experiment)
- **Experiment results:** `research/results/EX-results.md` (10-step Wohlin analysis)
- **Raw data:** `research/data/*.jsonl` (append-only, never edited)

---

## How to Execute

1. **Design and run experiments** from `domainspec-core/research`.
2. **Implement framework adjustments** in `implementation/domainspec` (live symlink to DomainSpec source).
3. **Validate behavior** against `validation/poker-team` feature slices and runtime signals.
4. **Analyze data** using the research analyst workflow and append results under `research/results`.

See the skill definitions in `poker-team/.github/skills/domainspec-*` for details.

---

## Quick Links

- **DomainSpec Paper:** Start at `research/domainspec-paper.md` § 1 (Hypothesis)
- **Experiment Status:** `research/EXPERIMENTS.md` + `research/EXPERIMENTS-META.md`
- **Live DomainSpec source:** `implementation/domainspec`
- **Architecture (mirror):** `implementation/ARCHITECTURE.md`
- **Governance Model (mirror + live):** `implementation/GOVERNANCE-ATTENUATION.md` and `implementation/domainspec/GOVERNANCE-ATTENUATION.md`
- **Validation Reference:** `validation/poker-team` (feature behavior and runtime evidence)

---

## Immediate Execution Focus

1. **Phase 1 execution:** finalize and run E1-E5 in `research/experiments`.
2. **Instrumentation alignment:** connect E7/E8 collection to poker-team runtime signals.
3. **Claim adjudication:** update paper sections based on fresh run evidence.
