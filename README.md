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

Path policy:

- Canonical paths only.
- No compatibility aliases or redirect files unless explicitly requested.

## Repository Structure

```
domainspec-core/
├── research/
│   ├── projects/
│   │   ├── domainspec/           # Self-contained DomainSpec project artifacts
│   │   ├── meta-meta/            # Self-contained Meta-Meta project artifacts
│   │   └── mars/                 # Self-contained MARS project artifacts
│   ├── shared/
│   │   ├── standards/            # Shared standards across projects
│   │   └── templates/            # Shared report templates
│   └── registry/                 # Cross-project index and dependency graph
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

See [PHASED-PLAN.md](implementation/domainspec/PHASED-PLAN.md) for full 8-phase roadmap.

| Phase | Focus                                             | Status             |
| ----- | ------------------------------------------------- | ------------------ |
| 1     | Hypothesis validation (E1-E5)                     | 🔄 In progress     |
| 2     | Governance foundation (E6-E8, signals)            | 🔄 In progress     |
| 3     | Composition stress testing (E9-E10)               | ✅ E9 complete     |
| 4     | Agent role definitions (PO, QA, Dev, Stakeholder) | ⏳ Starting week 3 |
| 5     | Feature discovery protocol (adversarial agents)   | ⏳ Week 4          |
| 6     | Multi-agent conversation (autonomous stories)     | ⏳ Week 5-6        |
| 7     | Autonomy & optimization (no human-in-loop)        | ⏳ Week 7          |
| 8     | Meta-governance loop (self-tuning)                | ⏳ Week 8          |

---

## Key Artifacts

- **DomainSpec paper:** `research/projects/domainspec/papers/domainspec-paper.md`
- **DomainSpec experiment index:** `research/projects/domainspec/experiments/EXPERIMENTS.md`
- **Meta-Meta experiment index:** `research/projects/meta-meta/experiments/EXPERIMENTS-META.md`
- **MARS pipeline and evidence:** `research/projects/mars/definitions/` and `research/projects/mars/results/`
- **Cross-project registry:** `research/registry/PROJECT-INDEX.md` and `research/registry/DEPENDENCY-GRAPH.md`

---

## How to Execute

1. **Design and run experiments** from `domainspec-core/research/projects/<project-id>`.
2. **Implement framework adjustments** in `implementation/domainspec` (live symlink to DomainSpec source).
3. **Validate behavior** against `validation/poker-team` feature slices and runtime signals.
4. **Analyze data** using the research analyst workflow and append results under the owning project's `results/` folder.

See canonical reusable automation assets in `implementation/domainspec/copilot`.

### Interview Capacities

The workspace now includes explicit interview-first discovery capacity for both product-domain and research scoping work.

- **Domain interview (greenfield and brownfield):** `domainspec-interview-scope`
  - Helps founders, product owners, and implementers discover or audit domain scope before specification and implementation.
  - Produces reusable baseline artifacts: project overview, initial definitions, hypotheses, and experiment candidates.
- **MARS research startpoint:** `mars-research-start`
  - Initializes or audits a MARS research-project baseline before protocol design or execution.
  - Creates or normalizes the repository-valid project contract, discovery artifacts, registry entries, and validation steps for new or incomplete projects.
- **MARS research interview (greenfield and brownfield):** `mars-research-interview`
  - Handles discovery-only scoping when you want hypotheses, definitions, and experiment candidates without invoking the full startpoint flow.

Interview assets:

- DomainSpec Type A pack: `implementation/domainspec/copilot/agents/domainspec-interviewer.agent.md` and `implementation/domainspec/copilot/skills/domainspec-interview-scope/SKILL.md`
- MARS Type B orchestration: `.github/agents/mars-research-interviewer.agent.md`, `.github/skills/mars-research-start/SKILL.md`, and `.github/skills/mars-research-interview/SKILL.md`

---

## Automation Governance (Implemented)

The multi-repo automation model is now governed by explicit ownership and drift checks:

1. **Ownership policy:** `ops/ASSET-OWNERSHIP-POLICY.md`
2. **Current triage matrix:** `ops/AGENT-SKILL-TRIAGE-MATRIX.md`
3. **Drift check script:** `tools/check_github_drift.sh`

### Asset classes

- **Type A (canonical DomainSpec pack):** source in `implementation/domainspec/copilot`
- **Type B (research orchestration):** intended root ownership in `domainspec-core/.github`
- **Type C (project-local overlays):** kept local in consumer repos (for example `validation/poker-team/.github`)

### Policy 1 pointer propagation

Only update pointers for repositories affected by the changed asset type.

- Type A changes: commit canonical source first, then update consumers that actually use the change.
- Type B changes: commit in root orchestration assets; no forced poker-team update unless consumed.
- Type C changes: stay local to the consumer repo.

### Run drift checks

```bash
./tools/check_github_drift.sh
```

Current baseline intentionally fails until Type A/Type B mismatches are resolved.

---

## Quick Links

- **DomainSpec Paper:** `research/projects/domainspec/papers/domainspec-paper.md`
- **Experiment Status:** `research/projects/domainspec/experiments/EXPERIMENTS.md` and `research/projects/meta-meta/experiments/EXPERIMENTS-META.md`
- **Live DomainSpec source:** `implementation/domainspec`
- **Architecture:** `implementation/domainspec/ARCHITECTURE.md`
- **Governance Model:** `implementation/domainspec/GOVERNANCE-ATTENUATION.md`
- **Validation Reference:** `validation/poker-team` (feature behavior and runtime evidence)

---

## Immediate Execution Focus

1. **Phase 1 execution:** finalize and run E1-E5 in `research/projects/domainspec/experiments`.
2. **Instrumentation alignment:** connect E7/E8 collection to poker-team runtime signals.
3. **Claim adjudication:** update paper sections based on fresh run evidence.
