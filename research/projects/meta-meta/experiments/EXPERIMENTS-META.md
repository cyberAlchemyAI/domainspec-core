# Meta-Meta Framework — Experiment Design & Data Collection Plan

This document indexes experiments E11-E20 designed to validate the **agentic research framework** — a generalization of DomainSpec principles to any research or engineering problem involving multi-agent coordination, self-improving governance, and knowledge navigation.

Each experiment maps to claims about how the layered governance architecture (inner loop, outer loop, meta loop) can drive system optimization.

---

## Meta-Meta Framework Claims

| Claim | Description |
|-------|------------|
| CM1 | Governance signals (inner loop fidelity metrics) can be extracted from any agentic system |
| CM2 | Layered feedback (outer loop intervention) improves system behavior without re-tuning agents |
| CM3 | Agent role specialization/generalization can be driven by performance signals |
| CM4 | Multi-agent conversation structures enable knowledge reuse across domains |

---

## Experiment Index (E11-E20)

| ID  | Experiment                            | Meta-Meta Claim                               | Priority | Effort | Status       | File                                                 |
| --- | ------------------------------------- | ----------------------------------------- | -------- | ------ | ------------ | ---------------------------------------------------- |
| E11 | Governance Signal Extraction          | CM1 — signals generalizable across domains | P0       | Medium | not started  | [E11](experiments/E11-governance-signal-extraction.md)       |
| E12 | Outer Loop Intervention Effectiveness | CM2 — governance feedback improves behavior  | P0       | High   | not started  | [E12](experiments/E12-outer-loop-intervention.md)         |
| E13 | Multi-Agent Conversation Patterns     | CM4 — agent roles converge on decisions | P1       | Medium | not started  | [E13](experiments/E13-multi-agent-conversation.md)             |
| E14 | Agent Specialization Under Pressure   | CM3 — roles specialize/generalize adaptively | P1       | High   | not started  | [E14](experiments/E14-agent-specialization.md) |
| E15 | Knowledge Reuse Across Domains        | CM4 — inventory enables cross-domain transfer | P1       | High   | not started  | [E15](experiments/E15-knowledge-reuse-transfer.md) |
| E16 | Adversarial Agent Disagreement        | CM4 — conflict resolution strengthens output | P2       | Medium | not started  | [E16](experiments/E16-adversarial-agents.md)       |
| E17 | Cost Attribution per Agent Role       | CM1 — token/cost metrics per role | P2       | Medium | not started  | [E17](experiments/E17-cost-attribution.md)       |
| E18 | Human-Agent Decision Alignment        | CM2/CM4 — humans agree with agent recommendations | P2       | High   | not started  | [E18](experiments/E18-human-agent-alignment.md)     |
| E19 | Meta-Governance Convergence           | CM2/CM3 — self-tuning stabilizes | P3       | High   | not started  | [E19](experiments/E19-meta-governance-convergence.md) |
| E20 | Cross-Domain Generalization          | CM1-CM4 — principles transfer to non-software domains | P3       | High   | not started  | [E20](experiments/E20-cross-domain-generalization.md) |

---

## Experiment Boundaries & Dependencies

```
E1–E5 (DomainSpec)         → Derivation Determinism & Foundation
     ↓
E6–E10 (DomainSpec)        → Vocabulary, Composition, Governance
     ↓
E11–E15 (Meta-Meta)        → Signal Extraction, Feedback, Conversation
     ↓
E16–E20 (Meta-Meta)        → Specialization, Cost Accounting, Human Alignment
     ↓
E21+ (Integration)         → Cross-project validation, scaling to non-software
```

**Key Dependencies:**
- E11 requires E6-E10 data (governance signals derived from completed features)
- E12 requires E11 (need signal baseline before testing intervention)
- E13-E14 require E1-E5 (determinism ensures agent reproducibility)
- E15 requires inventory generalization (Task 2a complete)
- E16-E20 require agent role definitions (Phase 4 complete)

---

## Execution Rules

Same as E1-E10 (see poker-team EXPERIMENTS.md):
- Append-only JSONL data storage
- Structured results per experiment
- Session isolation + reproducibility metadata
- Wohlin 10-step analysis for all experiments
- Branch isolation per experiment bundle: `experiment/<project-id>/<experiment-key>` (for example `experiment/meta-meta/E13-multi-agent-conversation-patterns`)

---

## Integration Gates

| Gate | Condition | Approval |
|------|-----------|----------|
| After E10 | DomainSpec derivation validated | Proceed to Phase 2 (governance instrumentation) |
| After E15 | Knowledge reuse works across 3+ domains | Proceed to Phase 4 (agent roles) |
| After E18 | Human-agent alignment > 80% | Proceed to Phase 6 (full autonomy) |
| After E20 | Non-software domain principles validated | Publish meta-meta framework paper |
