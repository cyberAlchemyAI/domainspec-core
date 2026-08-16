---
node_type: research
is_session: false
status: candidate
created: 2026-08-07
updated: 2026-08-07
promotion_boundary: private calibration example
---

# Worked Round-Trip Example: Claim Calibration

This example is private calibration evidence. Replace it with a synthetic public case before paper publication.

## Concrete case

A toy freshness check is described with a distinctive mechanism label. Red-team review later shows that replacing the label with ordinary content hashing leaves the verdict unchanged, while the claimed concurrency behavior is not implemented.

## Baseline prompt

Using only the prose case, state:

1. what the toy demonstrates;
2. what it does not demonstrate;
3. what evidence would distinguish the named mechanism from a simpler hash check;
4. whether the current result authorizes a stronger capability claim.

## Treatment instrument

Provide the same evidence through a horizontal set:

- plain-language explanation;
- mechanism-versus-witness comparison;
- executable contract with claim ceiling;
- authority/approval boundary;
- causal-careful statement.

If a participant still cannot distinguish the named mechanism from the witness, record the residue. Repair the existing forms first. Add a richer layer only if the participant lacks vocabulary for a required distinction such as mechanism identity, observational equivalence, or concurrency semantics.

## Required return

The participant must return from the richer vocabulary to the toy and conclude:

> The executable witness demonstrates freshness wiring. It does not yet demonstrate value distinctive to the named mechanism, and it does not demonstrate concurrency behavior.

## Scoring

| Measure | Pass signal | Failure signal |
|---|---|---|
| Claim-ceiling retention | Names freshness wiring only | Claims mechanism-specific correctness |
| Counterfactual discrimination | Notes that label substitution preserves verdict | Treats the label as proof |
| Missing-evidence detection | Requests discriminating behavior and concurrency implementation | Requests only more prose |
| Authority boundary | Says stronger claim remains unapproved/unsupported | Treats review closure as repair |
| Transfer | Applies the same rule to an unfamiliar labeled mechanism | Repeats the answer without generalizing |
| Confidence calibration | Confidence falls when discriminating evidence is absent | High confidence tracks persuasive terminology |

## Why this is a useful cognitive test

The correct answer cannot be obtained by remembering the attractive label. It requires returning to the concrete executable witness and keeping “implemented,” “observed,” “inferred,” and “unshown” distinct. This is a candidate test design, not evidence that the treatment works.

