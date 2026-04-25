# MARS Claim Evidence Status

This file is maintained by `mars-research-evidence-auditor`.

## Claim Status Matrix

| Claim ID | Claim Summary | Evidence Strength | Status | Supporting Experiments | Conflicting Experiments | Next Recommended Experiment |
|---|---|---|---|---|---|---|
| MARS-C1 | Dual-track layered meta-architecture (L0-L7) improves traceability between domain semantics, governance, and implementation outcomes. | weak | insufficient evidence | E9 | none | E5 |
| MARS-C2 | Deterministic derivation T = f(C, R, Delta) from typed ontology yields reproducible obligations and high domain coverage. | moderate | partially supported | E6, E9 | none | E11 (human evidence-grade adjudication replacement run) |
| MARS-C3 | Governance attenuation increases as governance density grows, and structural interventions restore fidelity. | insufficient | insufficient evidence | none | none | E4 |
| MARS-C4 | Meta-circular governance (signals plus tuning loop) converges over time and reduces orphan/governance drift. | insufficient | insufficient evidence | none | none | E8 |

## Claim Definitions

- MARS-C1 maps to paper claim C1.
- MARS-C2 maps to paper claim C2.
- MARS-C3 maps to paper claim C3.
- MARS-C4 maps to paper claim C4.

## Evidence Notes

- Use ratings: strong, moderate, weak, insufficient, contradicted.
- Use status: supported, partially supported, insufficient evidence, contradicted.
- Use experiment IDs from `research/projects/domainspec/experiments/EXPERIMENTS.md` (E1-E11).
- Update this file after each completed experiment analysis.
- E11 bootstrap run artifacts were produced on 2026-04-22 for execution-pipeline validation; claim status remains unchanged pending manual dual-rater adjudication quality.
- E11 D4-clearance preparation artifacts were produced on 2026-04-22 (manual run plan, adjudication worklist/template, inventory freshness check); claim status remains unchanged until manual evidence-grade run plus confirming rerun complete.
- E11 manual run plus manual rerun artifacts were produced on 2026-04-22 and D4 packet was re-evaluated as no-go because adjudication mode remained provisional AI; claim status remains unchanged until human adjudication replaces provisional labels.
- DomainSpec framework contracts were updated on 2026-04-25 to incorporate E9 composition semantics (25 meta-types, 29 relationships, and composed derivation qualification); this reduces contract drift for C2 interpretation while preserving current MARS-C2 status pending human-adjudicated E11 closure.
