# DomainSpec Research & Meta-Meta Framework

This repository contains two intertwined research projects:

1. **DomainSpec** — Domain-driven software development through structured meta-types, deterministic test derivation, and layered governance
2. **Meta-Meta Framework** — Generalization of DomainSpec principles to any agentic system requiring autonomous coordination, self-improvement, and knowledge navigation

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
│   ├── ARCHITECTURE.md           # Meta-model: 24 types + 26 relationships
│   ├── TAXONOMY.md               # Meta-type vocabulary
│   ├── RELATIONSHIPS.md          # Relationship topology + proposed extensions
│   ├── GOVERNANCE-ATTENUATION.md # Fidelity loss model (C3)
│   ├── GOVERNANCE-SIGNALS.md     # Signal schema for feedback loops (TBD Task 2c)
│   ├── CONSTITUTION.md           # Framework governance rules
│   ├── TEST-PIPELINE.md          # Deterministic test derivation (C2)
│   └── [more framework docs]
└── validation/
    └── poker-team/               # Reference implementation (symlink)
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

## How to Contribute

1. **Running experiments:** Delegate to the research scientist agent in `poker-team`
2. **Analyzing data:** Use the research analyst agent (10-step pipeline)
3. **Discovering sources:** Use the research sourcer agent (generalized)
4. **Managing inventory:** Use the research inventorist agent (generalized)

See the skill definitions in `poker-team/.github/skills/domainspec-*` for details.

---

## Quick Links

- **DomainSpec Paper:** Start at `research/domainspec-paper.md` § 1 (Hypothesis)
- **Experiment Status:** `research/EXPERIMENTS.md` + `research/EXPERIMENTS-META.md`
- **Architecture:** `implementation/ARCHITECTURE.md`
- **Governance Model:** `implementation/GOVERNANCE-ATTENUATION.md` + `implementation/GOVERNANCE-SIGNALS.md`
- **Validation Reference:** `validation/poker-team` (see docs/features/ for implemented specs)

---

## Next Steps

1. **Task 2a (this week):** Generalize sourcer & inventorist skills to support any knowledge entry type
2. **Task 2b (this week):** Expand paper with hypothesis & governance context (§1)
3. **Task 2c (this week):** Define governance signal schema (GOVERNANCE-SIGNALS.md)
4. **Task 3 (next week):** Finalize phased plan with detailed phase gates
5. **Phase 1 execution:** Begin E1-E5 protocols (parallel with current E6-E10)
