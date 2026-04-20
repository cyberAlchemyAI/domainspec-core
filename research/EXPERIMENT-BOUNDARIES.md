# Experiment Boundary & Traceability Matrix

This document clarifies which experiments belong to which research project and how claims flow through experiments to paper sections.

---

## Project Alignment

### DomainSpec Project (poker-team + domainspec-core)
**Goal:** Validate that domain structure (meta-types + relationships) → deterministic test derivation → better decisions

**Paper:** domainspec-paper.md § 1-9

**Experiments:** E1-E10 (10 experiments over 2-3 months)

| Exp | Name | Claims | Data Source | Deliverable | Status |
|-----|------|--------|-------------|-------------|--------|
| E1 | Derivation Determinism | C2 | poker-team features | Same spec → same tests (≥95% match) | not started |
| E2 | Derivation vs Manual Coverage | C2 | poker-team + manual tester | Derived tests ≥ manual (coverage, assertions) | not started |
| E3 | Mutation Testing Effectiveness | C2 | Stryker plugin | Derived tests catch real faults (mutation kill rate) | not started |
| E4 | Governance Attenuation Curve | C3 | Multi-layer poker-team | Fidelity vs layer count (exponential decay) | not started |
| E5 | Observer-Executor Separation | C3 | Intervention experiment | Separation restores fidelity (before/after) | not started |
| **E6** | **Vocabulary Sufficiency** | **C2** | **18 external domains** | **24 types cover 36 features (99.87%)** | **✅ complete** |
| E7 | Signal Emission Rate | C3/C4 | poker-team live system | Inner-loop signals measure attenuation (empirical) | not started |
| E8 | Meta-Health Convergence | C4 | Signal data E7 | Orphan rate → 0 over time (trend analysis) | not started |
| **E9** | **Cross-Feature Composition** | **§9.2** | **6 external domains** | **Composition gaps & patterns** | **✅ complete (run-2 rerun)** |
| E10 | Developer Productivity | §9.4(d) | External devs | DomainSpec vs freeform (time, quality, decisions) | not started |

### Meta-Meta Framework Project (agentic-research-framework)
**Goal:** Generalize DomainSpec governance to any multi-agent system requiring self-improvement

**Paper:** meta-meta-paper.md (future) § 1-8

**Experiments:** E11-E20 (10 experiments, parallel to DomainSpec Phase 2-3)

| Exp | Name | Claims | Data Source | Deliverable | Status |
|-----|------|--------|-------------|-------------|--------|
| E11 | Governance Signal Extraction | CM1 | Any agentic system (3 domains) | Signals generalizable across domains | not started |
| E12 | Outer Loop Intervention | CM2 | E11 signals + intervention | Feedback improves behavior (before/after) | not started |
| E13 | Multi-Agent Conversation | CM4 | 3-5 agent roles debating | Roles converge on decision (agreement rate) | not started |
| E14 | Agent Specialization | CM3 | Performance signals → role tuning | Specialization improves efficiency (time/cost) | not started |
| E15 | Knowledge Reuse Transfer | CM4 | Inventory across 3+ domains | Transfer enables faster convergence | not started |
| E16 | Adversarial Agent Disagreement | CM4 | Conflicting agent proposals | Conflict→synthesis improves quality | not started |
| E17 | Cost Attribution per Role | CM1 | Token accounting E7+E13 | Cost metrics per agent role | not started |
| E18 | Human-Agent Alignment | CM2/CM4 | Agent recommendations vs human judgment | Alignment > 80% | not started |
| E19 | Meta-Governance Convergence | CM2/CM3 | Self-tuning feedback loops | System stabilizes (signal variance → 0) | not started |
| E20 | Cross-Domain Generalization | CM1-CM4 | Non-software domain (e.g., supply chain) | Principles transfer | not started |

---

## Claim-to-Experiment Traceability

### C1: Dual-track meta-architecture (L0–L7) organizes domain → governance → tuning
**Paper section:** §3 (Architecture)
**Supporting experiments:** 
- E4, E5 (governance layers' effectiveness)
- E7, E8 (meta-health signals)
- E11, E12 (generalized feedback)

### C2: Deterministic derivation T = f(C, R, Δ) from 24 meta-types + 26 relationships
**Paper section:** §5 (Derivation)
**Supporting experiments:**
- ✅ E6 (vocabulary coverage)
- E1, E2, E3 (determinism, coverage, mutation)
- 🔄 E9 (composition patterns, Δ = cross-context edges)

**Revision note:** E9 run-2 rerun suggests derivation is per-feature; composition requires T_composed with Δ_cross (see §5.1 revision)

### C3: Governance attenuation — fidelity decreases with layer count, bounded by Shannon capacity
**Paper section:** §6 (Governance)
**Supporting experiments:**
- E4, E5 (attenuation curve + intervention)
- E7 (signal emission rate empirical)
- E11, E12 (generalized attenuation)

### C4: Meta-circular self-governance via bounded strange loop
**Paper section:** §7 (Meta-governance)
**Supporting experiments:**
- E8 (orphan rate convergence)
- E7 (meta-signals)
- E14, E19 (agent self-tuning)

---

## Data & Results Cross-Reference

| Experiment | Raw Data | Results File | Notes |
|---|---|---|---|
| E1-E5 | `data/E1-EX.jsonl` | `results/E1-results.md` | TBD |
| E6 | `data/E6-vocabulary-sufficiency.jsonl` | `results/E6-results.md` | ✅ 99.87% coverage, 5/5 SC PASS |
| E7-E8 | `data/E7-E8-signals.jsonl` | `results/E7-E8-results.md` | TBD (live instrumentation) |
| E9 | `data/E9-run2-rerun-2026-04-20.jsonl` | `results/E9-run2-rerun-results.md` | ✅ 94 edges, 5/5 SC PASS, C2 strengthened |
| E10 | `data/E10-productivity.jsonl` | `results/E10-results.md` | TBD (requires external devs) |
| E11-E15 | `data/E11-E15-meta.jsonl` | `results/E11-E15-results.md` | TBD (meta-meta framework) |
| E16-E20 | `data/E16-E20-meta.jsonl` | `results/E16-E20-results.md` | TBD (roles + generalization) |

---

## Execution Sequencing

```
Timeline:  Week 1-2          Week 3-4          Week 5-6          Week 7-8
           ─────────────────────────────────────────────────────────────

DomainSpec E1-E5 (Phase 1)   E6-E8 (Phase 2)   E9-E10 (Phase 3)   Agent Roles (Phase 4)
           ✅ planning        🔄 executing       ✅ E9 done         ⏳ prep

Meta-Meta  Research setup    ─────────────────────────────────────────────────
           (sources, etc)    E11-E15 start      E16-E20 start      Integration gates

Parallel   Sourcer/          Generalization    GOVERNANCE-        Phased plan
Tasks      Inventorist       complete          SIGNALS.md         finalized
           refactor (2a)     Paper deepen      ready (2c)
                             (2b)
```

---

## Integration Gates

**After E10:** Approve Phase 2 (governance instrumentation, E6-E8)
- [ ] All 5 E1-E5 success criteria PASS
- [ ] C2 (derivation) supported or revised
- [ ] C3, C4 sufficient evidence from E7-E8

**After E15:** Approve Phase 4 (agent roles)
- [ ] E11-E15 success criteria met
- [ ] Inventory generalization proven (cross-domain reuse)
- [ ] CM1, CM4 empirically validated

**After E18:** Approve Phase 6 (full autonomy)
- [ ] E16-E18 complete
- [ ] Human-agent alignment > 80%
- [ ] Agent role definitions stable

**After E20:** Publish meta-meta framework paper
- [ ] E20 cross-domain validation complete
- [ ] CM1-CM4 supported across 3+ domains
- [ ] Integration with DomainSpec validated
