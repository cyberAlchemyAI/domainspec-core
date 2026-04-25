# Equalizator

## Summary

Equalizator is a natural language to equalization system that helps creators and listeners transform subjective audio requests into safe, measurable EQ plans. It serves producers, content creators, and non-expert users who know how audio should feel but cannot directly express filter parameters. The immediate goal is to turn domain research into a deterministic product architecture that can be tested and improved quickly.

## Discovery Mode

- Mode: greenfield
- Project state: idea
- Interview date: 2026-04-25
- Operator / owner: equalizator project owner

## Problem Framing

- Primary user or customer: independent creators, mix engineers, and quality reviewers
- Core problem: users describe tone in words, but existing EQ tools require expert parameter control
- Value proposition: convert intent language into explainable and safe EQ settings with fast feedback loops
- Business goal: improve audio quality outcomes and reduce trial-and-error time in tonal correction
- Non-goals: full autonomous mastering, replacement of critical listening, genre-specific artistic automation

## Current State

| Item | Status | Evidence Type | Notes |
|---|---|---|---|
| Product scope | partial | observed | Research dossier exists with multi-source quality pillars and operational definitions. |
| Domain boundaries | partial | hypothesized | Candidate boundaries are visible but not yet formalized in feature artifacts. |
| Existing implementation | partial | observed | There are project assets and simulators in workspace, but no dedicated NL to EQ domain feature model yet. |
| Metrics baseline | unknown | stated | No agreed baseline yet for translation quality, safety pass rate, or user acceptance. |

Evidence type:
- observed = seen in repository or artifacts
- stated = given by operator
- hypothesized = inferred but not yet validated

## Actors And Stakeholders

| Actor | Goal | Pain Point | Frequency | Evidence Type |
|---|---|---|---|---|
| Creator / Producer | Improve tonal balance quickly | Knows desired sound but not exact frequency moves | daily | stated |
| Audio Reviewer | Verify technical quality before release | Inconsistent quality language across people | weekly | hypothesized |
| End Listener Profile | Better playback on target device | Device playback differences are hard to predict | daily | hypothesized |
| Product Owner | Deliver reliable recommendation engine | Hard to prove recommendation quality and safety | weekly | observed |

## Candidate Bounded Contexts

| Context | Responsibility | Key Concepts | Status | Evidence Type |
|---|---|---|---|---|
| Intent Interpretation | Parse natural language into structured intent vectors | descriptor token, confidence, intent vector | candidate | observed |
| Program Material Analysis | Extract measurable audio features from source | spectrum profile, masking risk, loudness metrics | candidate | observed |
| EQ Synthesis | Generate constrained candidate EQ plans | EQ band, gain, Q, filter type, objective score | candidate | hypothesized |
| Safety And Compliance | Enforce technical and platform constraints | true peak guard, gain bound, headroom policy | candidate | observed |
| Learning Loop | Capture outcome signals and retrain priors | feedback event, acceptance score, adjustment delta | candidate | hypothesized |

## Core Workflows

| Workflow | Trigger | Main Steps | Failure Mode | Evidence Type |
|---|---|---|---|---|
| Prompt to EQ Plan | User submits tonal request | parse intent -> analyze material -> synthesize plan -> validate safety -> publish | low confidence parse, invalid safety constraints | hypothesized |
| Plan Simulation | User requests predicted impact | compute response delta -> estimate risks -> return explanation | simulation mismatch with perceived quality | hypothesized |
| Feedback Refinement | User accepts or edits plan | record deltas -> classify mismatch -> update priors | sparse or noisy feedback data | hypothesized |

## Constraints

| Constraint | Type | Why It Matters | Evidence Type |
|---|---|---|---|
| Recommendation latency under 500 ms (without full render) | technical | Needed for interactive user workflow | hypothesized |
| Hard safety bounds for gains and true peak risk | technical | Prevents harmful or unstable EQ recommendations | observed |
| Explainable output (what changed and why) | business | Required for trust and professional adoption | stated |
| Device-aware adaptation | operational | Recommendations should hold across playback contexts | observed |

## Success Signals

| Signal | Why It Matters | Current Baseline | Target Direction |
|---|---|---|---|
| First-pass acceptance rate | Measures recommendation usefulness | unknown | improve |
| Median user revisions per plan | Measures precision of intent capture | unknown | reduce |
| Safety validation pass rate | Measures reliability and policy compliance | unknown | stabilize high |
| Perceived tonal match score (1-5) | Measures subjective alignment to prompt | unknown | improve |

## Risks And Unknowns

| Risk | Why Risky | Severity | What Would Reduce It |
|---|---|---|---|
| Language ambiguity in tonal descriptors | Same term can imply different spectral moves | high | Controlled vocabulary mapping + confidence thresholds |
| Overfitting to one genre/device profile | Recommendations may fail in other contexts | high | Stratified experiments across genres and devices |
| Misalignment between measurable proxies and perception | Objective metrics may miss listener preference | high | Human rating loop + counterfactual comparisons |
| Unsafe edge recommendations | Excessive boosts or narrow Q can degrade audio | medium | Strict guardrail policies and pre-publish validation |

## Recommended Next Artifacts

1. docs/INITIAL-DEFINITIONS.md
2. docs/HYPOTHESES.md
3. docs/EXPERIMENT-CANDIDATES.md
4. docs/features/nl-eq-translation/SPEC.md

## Open Questions

1. Should Equalizator optimize for creator intent first, platform compliance first, or a weighted blend by use case?
2. Which minimum audio feature set is sufficient for first release without overcomplicating inference?