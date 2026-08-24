# Stage 02 — Define

## Problem

The video package describes motion but has no repeatable mechanism for asking: “Which bounded motion should we try, what Anime.js evidence supports the implementation path, what would disprove it, and what did we learn after trying?” Jumping directly from prose to a whole-film implementation would hide source drift, untestable layering assumptions, accessibility failures, and false runtime claims.

## Unit of value

One `AnimationHypothesisCandidate` links one frozen scene beat to one proposed semantic transformation, exact evidence, a contradiction path, reduced-motion behavior, and a finite acceptance witness. A candidate is useful before it is selected and remains non-authoritative after selection until later execution produces evidence.

## Minimum component catalog

- `VideoSourceSnapshot`: hashes and selectors for script, captions, images, validation, and timing posture.
- `SceneBeat`: one spoken anchor, time window, visual transformation, on-screen text, sound note, and semantic constraints.
- `VaultConsultationReceipt`: bounded query input, version context, returned evidence identities, status, and abstention/staleness posture.
- `AnimationHypothesisCandidate`: the reviewable proposed mapping from a beat to motion.
- `SceneTournament`: finite comparison, scores, rejection reasons, and owner-selected candidate.
- `AnimationPlan`: implementation-neutral sequence of layers, primitives, timings, reduced-motion states, and acceptance checks.
- `BrowserWitness`: later Task Session evidence; absent in this refinement.
- `WorkEpisode`: append-only record of a later attempt and outcome; closing one does not create a `Lesson`.
- `ResidueEntry`: rejected hypothesis, failure, contradiction, missing evidence, or stale context with an owner and next route.

## Lifecycle

`source-frozen -> proposed -> prechecked -> consulted -> tournament-eligible -> selected|rejected|blocked -> planned -> [later Task Session] attempted -> witnessed|failed -> episode-closed -> lesson-eligible|residue`

Selection authorizes planning only. A later Task Session authorizes bounded implementation only. Neither automatically admits an ontology Lesson or modifies the source video package.

## Success definition

The design succeeds when an agent can recover why one scene was selected, which exact evidence informed its Anime.js plan, how reduced motion preserves meaning, what browser evidence would falsify the plan, and how later work residue re-enters consultation without silently becoming truth.

