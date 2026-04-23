# MARS Claim Evidence Status

This file is maintained by `mars-research-evidence-auditor`.

## Claim Status Matrix

| Claim ID | Claim Summary | Evidence Strength | Status | Supporting Experiments | Conflicting Experiments | Next Recommended Experiment |
|---|---|---|---|---|---|---|
| MARS-C1 | Dual-track layered meta-architecture (L0-L7) improves traceability between domain semantics, governance, and implementation outcomes. | weak | insufficient evidence | E9 | none | E5 |
| MARS-C2 | Deterministic derivation T = f(C, R, Delta) from typed ontology yields reproducible obligations and high domain coverage. | moderate | partially supported | E6, E9 | none | E11 (manual evidence-grade adjudication run) |
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
- E11 manual D4 packet artifacts were started on 2026-04-23 (`run-lock`, manual run data, subset manifest, dual-rater files, third-rater resolution log section, confirming rerun, decision packet); strict policy preserved and claim statuses unchanged.
- E7 longitudinal instrumentation started on 2026-04-23 with kickoff run artifact in the E7 bundle; this is accumulation-only evidence and does not yet change C3/C4 or MARS-C3/C4 status.
