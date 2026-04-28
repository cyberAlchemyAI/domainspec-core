# Paper Design Workflow Pilot Proposal (MARS)

Date: 2026-04-28
Status: proposed pilot with live application in `research/projects/mogt-agentic-conversation`
Objective: apply a DomainSpec-style design workflow to the MARS paper lifecycle without prematurely turning it into a hard gate.

## Problem

MARS already has paper integration at S12, but until now paper work has mostly existed as:

- a narrative stub under `papers/`
- traceability links from claims and experiments
- implicit section intent in protocol files and the traceability matrix

The new research taxonomy and typed relationships make paper structure explicit enough that we can now design the paper before the prose is fully written.

## Proposed Working Model

Pilot a lightweight paper-design contract made of four artifacts:

1. `papers/PAPER-SPEC.md`
2. `papers/PAPER-STORIES.md`
3. `papers/PAPER-TEST-SPEC.md`
4. `papers/PAPER-REVIEW.md`

These artifacts should be derived from `registry/RESEARCH-GRAPH.md` rather than authored independently from it.

## Why This Is Option 2 Plus Option 3 Rules

This pilot adopts the practical artifact model from the paper-as-feature idea:

- spec-like paper contract
- section-scoped stories
- test-like evidence checks
- lightweight review artifact

At the same time, it records the graph-derivation rules needed for a later reusable or automated workflow.

That makes the pilot concrete now while preserving the path to a later graph-native compiler model.

## MOGT Pilot Target

Pilot project: `research/projects/mogt-agentic-conversation`

Pilot success means:

1. The MOGT paper can be reviewed as a design artifact before evidence-backed prose is complete.
2. Result sections clearly show when they are blocked on missing evidence.
3. The pilot surfaces which paper-contract artifacts were useful and which were overhead.

## Reusable Framework Assets Created In This Wave

- `implementation/mars/definitions/PAPER-DERIVATION-RULES.md`
- `implementation/mars/templates/paper-spec-template.md`
- `implementation/mars/templates/paper-stories-template.md`
- `implementation/mars/templates/paper-test-spec-template.md`
- `implementation/mars/templates/paper-review-template.md`

## Deliberate Non-Goals For This Pilot

1. No new hard gate in `MARS-PIPELINE.md` yet.
2. No dedicated `mars-research-paper-design` skill yet.
3. No automatic file generation from the graph yet.
4. No claim that the paper workflow is finalized before MOGT produces evidence and lessons.

## Evaluation Questions After MOGT

1. Which pilot artifacts actually reduced ambiguity during paper writing?
2. Which sections benefited from stories versus direct graph tracing?
3. Were the paper test checks specific enough to prevent overclaiming?
4. Which derivation rules were stable enough to automate?
5. Should paper design become a distinct stage or a sub-stage inside S12?

## Candidate Follow-Up Changes After The Pilot

1. Create `mars-research-paper-design` as a specialist skill.
2. Introduce an S12a paper-design sub-stage before narrative integration.
3. Add graph-to-paper derivation automation for the four pilot artifacts.
4. Add a paper readiness checklist analogous to protocol validation.

## Iteration Rule

Do not harden this into a mandatory framework gate until the MOGT pilot has completed a live evidence cycle and produced explicit lessons learned.
