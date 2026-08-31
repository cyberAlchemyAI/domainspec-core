# Chapter 1 Reader-Discovery Review Findings

## Review boundary

The current candidate and Voice Guide exist and were attacked by three independent passage methodologies. Findings cite the admitted task results in attacks.md. Inventory material shaped the project-local boundary but is not review proof.

## editorial/VOICE-GUIDE.md

| # | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| CR-01 | projects/lucifers-lights/editorial/VOICE-GUIDE.md | The guide has a tether rule and pacing test but no explicit distinction between mechanics that must be stated and meanings that should be discovered. All three tracks needed that distinction to judge passages consistently. | MAJOR | Add the project-local reader-discovery rule, including evidence → gap → choice → payoff and a guardrail for agency, consent, causality, time, and consequences. |

Verdict: **FIX**

## Chapter 1 candidate

| # | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| CR-02 | candidate/chapter-01.md | “Even desperate people deserve to know the cost before someone saves them.” interprets Lucifer's morality immediately after the request-price-choice mechanics already show it. PS-01 independently flags the opening explanation cluster. | MINOR | Remove the self-certifying final sentence; preserve the complete app mechanics and lock parable. |
| CR-03 | candidate/chapter-01.md | “Good. Thinking for herself was the entire point” and the later plural/singular humanity essay explain the meaning of Mara's own rejection. SR-01, DR-03, and PS-02 converge on this passage. | MAJOR | Remove the explanatory approval and generalized essay; retain Mara's line and Lucifer's unsettling smile, then pay the fascination off when she cuts the tracker without looking to him. |
| CR-04 | candidate/chapter-01.md | “Your future self is the one who discovers where you left the key” closes the contract parable before the literal key, locker, train, and later choices arrive. DR-04 identifies the delayed-payoff opportunity. | MINOR | Keep only “A contract is a door you lock from this side.” |
| CR-05 | candidate/chapter-01.md | “A Light is seldom magnificent” is immediately restated as “boiling coffee, nine stolen seconds...” after Ruth's action and debt have already demonstrated both claims. SR-02 identifies the duplicate meaning and double joke. | MINOR | Keep Ruth's debt-and-coffee-pot line; remove the explanatory restatement and “sacrifice for humanity” question while retaining the sunrise-tethered shoe joke. |
| CR-06 | candidate/chapter-01.md | Elena's scheduled timestamp already proves preparation. “She had planned...” and “I began to like her” reconstruct and approve what the reader can infer. SR-03 identifies both echoes. | MINOR | Retain the timestamp and “Elena had known”; remove the plan restatement and approval. |
| CR-07 | candidate/chapter-01.md | “Of course she did” recognizes Mara's agency but remains too short and risks sounding like approval. DR-03 supplies a later, character-specific payoff to the earlier cut. | MAJOR | Replace it with “She did not look at me first. Of course she didn't.” |
| CR-08 | candidate/chapter-01.md | The mouth metaphor appears before the impossible compensation field proves the system violation. SR-04 favors compression; DR-05 favors delayed recomposition; PS-05's interactive alternative invents risky UI behavior. | MAJOR | Keep “The screen was presentation. The promise behind it was mine.” at Elena's warning; move the mouth metaphor after the impossible compensation mechanic; remove the redundant qualification after Lucifer says “I don't know.” |

Verdict: **FIX**

## Refuted or dropped

- No change to the temporal Vesper line: it already states that the city chose its new name later.
- No full deletion of the opening lock parable: later keys and choices give it a traceable payoff.
- No new status-label taps, compensation-field interaction, or produce-market geometry: those proposals exceed the admitted continuity evidence.
- No claim that these changes create a particular reader emotion. The tournament proves bounded editorial reasoning, not reader response.

## Ordered change requests

1. Add CR-01 to the project Voice Guide.
2. Apply CR-03 and CR-08 as the highest-convergence manuscript changes.
3. Apply CR-02, CR-04, CR-05, CR-06, and CR-07 as bounded supporting changes.
4. Recompute the candidate digest and update only the candidate-local factory config.
5. Run complete marker, clock, word-count, continuity, whitespace, and review-render validation.
6. Keep projects/lucifers-lights/drafts/chapter-01.md byte-identical pending an exact author decision on the new candidate.

## Apply verification

The parent accepted the complete ordered change-request list after joining all three admitted receipts. The candidate and Voice Guide were updated; dropped proposals were not smuggled into the prose.

| Artifact | Before SHA-256 | After SHA-256 | Result |
| --- | --- | --- | --- |
| `candidate/chapter-01.md` | `8b33827b68d2761381cdc0f61b4c3f92bb2b4a80fea55137174424c358cb8d7d` | `d3eadd32eecf7da002bfe61d32fa0615c22dd7157ee53f8d5d5b127c4408b1bd` | candidate updated; author gate pending |
| `editorial/VOICE-GUIDE.md` | `ca0326544e8948da7761b828bc4d2878d4f3d21b2a576f993d3ee6f0dc9a25b3` | `b1c8259c263730977573420478395b0f1b3352b405f0e90eec1dc696c961ddfb` | reader-discovery rule added |
| `drafts/chapter-01.md` | `eb89135bb53d2c8106b26e8005a1c45738bd84a3a2b06b9e64518c9c64fbe2a5` | `eb89135bb53d2c8106b26e8005a1c45738bd84a3a2b06b9e64518c9c64fbe2a5` | unchanged |

Validation passed: Chapter Factory deterministic review, 29 Chapter Pipeline tests, Python compilation, exact digest binding, whitespace, review rendering, all three clocks, all ten required markers, and all five forbidden-marker absences. Reader effect remains unproven; manuscript acceptance remains an exact author decision.
