# Hellbender Research Strategy

Status: candidate strategy, public-source only. This strategy is designed to produce an offering seed;
it is not itself a client-facing proposal.

## Objective

Understand all plausible CyberAlchemy/Ontologize synergy points with Hellbender, then narrow them into
a first offer that is small enough to validate with a discovery call and one governed pilot.

## Source Frame

Hellbender publicly positions itself as a modular full-lifecycle partner for complex edge AI,
robotics, and computer vision systems. Its process page names Architect, Prototype, Productize,
Manufacture, and Evolve, and says teams can engage for the full journey or plug Hellbender into a
specific bottleneck. The same page describes DFM, DVT, BOM lock, high-mix onshore manufacturing,
advanced PCBA, perception calibration, field-data feedback, sustaining engineering, and RaaS/CVaaS.

Additional public signals:

- Design and development emphasizes fast MVPs, IP building blocks, integrated engineering, in-house
  testing, supplier partnerships, camera/sensor expertise, and multi-camera calibration.
- Manufacturing emphasizes PCBA through end-of-line integration/testing, cobotic work cells, quick
  production-line setup, automated production processes, secure U.S. production, CMMC Level 3
  practices, ISO Class 7 clean room assembly, automated inspection, environmental testing, RF testing,
  and calibration.
- CVaaS emphasizes custom computer vision systems spanning hardware, software, deployment,
  integration, field maintenance, customized models, and problem-specific solutions.
- Case studies show Industry 4.0 instrumentation and automation as a native Hellbender practice:
  selective instrumentation, barcode-linked traceability, work-instruction improvement, real-time
  quality gates, and root-cause analysis moving from days to minutes.
- The May 19, 2026 seed announcement describes a transition from custom engineering and manufacturing
  into commercial physical AI platforms, with new camera systems and scaling across product, growth,
  and hardware manufacturing.

## Fanout Lanes

The research should run as role-bound fanout under one dispatch id:
`ontologize-hellbender-client-research-20260615`.

| Lane | Role | Questions | Required Output |
| --- | --- | --- | --- |
| L1 | Hellbender process reader | Where do lifecycle handoffs, DFM/DVT, QA/calibration, CVaaS, and field feedback create knowledge loss or metric ambiguity? | Source-grounded process observations plus discovery questions. |
| L2 | Ontologize fit mapper | How do evidence-linked BI, operational ontology, data boundary register, promotion graph, and optimization chains map to Hellbender? | Synergy map, candidate proof metrics, assumptions, confidence. |
| L3 | Sales/offering strategist | Which wedge can be sold first without sounding like generic AI strategy? | Offer wedges, buyer roles, pitch narrative, objections, first pilot. |
| L4 | Risks/gaps adversary | What could make this a bad or premature offer? | Risk ledger, hard stops, discovery evidence needed, guardrails. |

## Research Questions

1. Which Hellbender lifecycle stage most needs a defensible metric and governed learning loop?
2. Which operational event boundary is clean enough for a first pilot: design decision, prototype
   build, DFM loop, DVT cycle, production lot, calibration batch, field incident, or retrain window?
3. Which metric is already used but not fully trusted: DVT pass rate, DFM closure time, calibration
   yield, EOL QA escape rate, root-cause cycle time, field incident resolution, retrain/deploy latency,
   or value-engineering savings?
4. Which data classes must fail closed: customer IP, raw images/video, design files, BOM/vendor
   pricing, regulated project data, field logs, model artifacts, or shareable aggregate metrics?
5. Who owns promotion decisions: manufacturing, quality, product, ML/software, customer success,
   security/compliance, or an executive sponsor?
6. Which lessons can become reusable across product lines or customers, and which must stay
   customer-local?

## Candidate Synergy Surface

| Hellbender surface | CyberAlchemy/Ontologize fit | Possible sell |
| --- | --- | --- |
| Architect and silicon downselection | Ontology cards for payload, compute, sensor, environment, customer use case, and design constraint. | Architecture decision ledger that traces choices to DVT, EOL, and field outcomes. |
| Prototype loops | Source-backed run nodes and evidence-linked prototype metrics. | Prototype evidence chain that makes concept-to-validation learning inspectable. |
| Productize, DVT, DFM, BOM lock | Promotion graph with owner decisions and contradiction paths. | DFM/DVT learning loop that turns test and rework evidence into approved build rules. |
| PCBA, cobotic assembly, EOL QA, calibration | Evidence-linked BI with denominator semantics and confidence grades. | Manufacturing quality intelligence for yield, defects, calibration, escapes, and root cause. |
| Field deployment and sustaining engineering | Fleet-to-factory promotion graph. | Field data to next-generation hardware governed reuse loop. |
| CVaaS/RaaS active management | Data boundary register plus governed model/update decisions. | CVaaS trust layer for retraining, uptime, customer telemetry, and reusable service learning. |
| Secure onshore manufacturing | Fail-closed data classification and owner-approved reuse. | Compliance-friendly evidence and reuse map for regulated or IP-sensitive work. |

## First Offer Hypothesis

Name: **Physical AI Lifecycle Intelligence Pilot**.

Scope: one product line, production loop, or CVaaS deployment; one priority metric; one evidence
chain; one boundary register; one promotion graph.

Most promising wedge: EOL QA/calibration to field performance to sustaining engineering. This touches
manufacturing quality, customer-visible reliability, CVaaS value, and Hellbender's Evolve story
without requiring raw customer data or replacing their tools.

## Discovery Call Agenda

1. Pick one lifecycle stage where the team loses context or distrusts a metric.
2. Pick one metric and force the denominator: what counts, what is excluded, and what real-world event
   creates the record?
3. Identify the source systems and data classes needed for a metadata-first sample.
4. Name the owner who can approve a lesson as reusable, rejected, private residue, or retired.
5. Decide whether the first pilot is Lane A, Lane B, or Hybrid. Default recommendation is Hybrid.

## Hard Stops

- No executive or functional sponsor.
- No approved data class or security review path.
- No agreed run boundary.
- No priority metric that changes a decision.
- Requirement to touch raw images, customer IP, controlled data, or sensitive design files before a
  boundary register exists.
- Any request to claim compliance, certification, autonomous decision-making, or cross-client reuse.

## Next Route

Use [SUMMARY.md](SUMMARY.md) as the seed for an `invoke` design/plan bundle for the first offering.
The next bundle should produce: client-facing one-page offer, discovery call script, assessment
questionnaire, sample data request, pilot acceptance criteria, and risk/guardrail appendix.
