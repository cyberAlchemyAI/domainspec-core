# Stage 06 — Design

## Verdict

`PASS` for a non-executed candidate-local design. All three confirmed role receipts joined and the deterministic `design-role-receipts` gate passed.

## Architecture

```text
frozen VideoSourceSnapshot
        |
        v
pure CandidateBuilder ---- prior residue ----+
        |                                     |
        v                                     |
AnimationHypothesisCandidate                 |
        |                                     |
        v                                     |
Anime.js consultation port (read-only)       |
        |                                     |
        v                                     |
precheck + contradiction gate                |
        |                                     |
        v                                     |
finite SceneTournament -> owner selection    |
        |                                     |
        v                                     |
AnimationPlan                                |
        |                                     |
        +-- later Task Session --> browser witness
                                      |
                                      v
                                WorkEpisode -> residue
                                      |
                               no automatic Lesson
```

AutoAds is not a runtime dependency. The Anime.js vault is consulted through its existing transport-neutral read audience. The first implementation may use the operational library directly or a thin consumer-owned adapter; this design does not add HTTP.

## Candidate contract

Every `AnimationHypothesisCandidate` requires:

- stable identity and exact `SceneBeat` selector;
- script, caption, image, and source-package digests;
- proposed motion statement, comprehension rationale, motion family, target elements, state machine, and bounded timeline;
- semantic invariants, negative-animation constraints, semantic end states, and a reduced-motion state machine with identical meaning;
- current consultation request, version context, returned evidence ids, status, and claim limit;
- atomic proof ledger using exactly one of `source_observed`, `documented_capability`, `planned_motion`, `executed_witness`, `subjective_evaluation`, or `owner_decision` per claim;
- explicit falsifier, known conflicts, resolution state, and reproposal requirement;
- local prototype scope, deterministic witness spec, tournament binding, owner-review state, and lineage/residue.

The machine-readable closed draft is `contracts/animation-hypothesis-candidate.schema.json`.

## Scene tournament

Hard eligibility comes first: source fidelity, reduced-motion equivalence, current consultation evidence, overlay feasibility, deterministic witnessability, and transition preservation. A hard failure cannot be compensated by a score.

| Candidate | Semantic leverage | Boundedness | Layer feasibility | Accessibility | Recomposition | Total | Disposition |
|---|---:|---:|---:|---:|---:|---:|---|
| S6 `04:29–04:39` | 4 | 5 | 4 | 5 | 5 | 23 | selected L0 |
| S7 `05:38–05:48` | 5 | 3 | 3 | 4 | 5 | 20 | retained L1 high-risk boundary witness |
| S12 `12:19–12:30` | 5 | 4 | 3 | 5 | 3 | 20 | retained later closing witness |

### Dissent and resolution

The motion lane prefers S7 because “never cross the owner gate” is the most important negative invariant. The source lane prefers S6 because it is the nearest reversible unit and exercises a reusable relation-drawing grammar with lower overlay risk. The parent selects S6 for L0 using low-cost falsification and first-unit narrowness. This is not a claim that S6 is artistically better. S7 remains the next required witness once the engine, overlay, seek, reduced-motion, and evidence contracts work on S6.

## Selected L0 prototype

- Source: Sequence 6, `images/03-arrow-is-a-contract.png` as an immutable reference/backplate.
- Beat: `04:29–04:39`, `Rule — enforces → Operation`.
- Standard motion: two typed overlay objects remain stable; a cyan SVG edge draws left to right; arrow direction becomes unambiguous; the `enforces` label remains attached to the edge; the terminal state holds.
- Reduced motion: an immediate or short dissolve to the identical static labelled relation; no path-travel dependency.
- Forbidden: morphing object identity, reversing direction, implying runtime success, editing the source image, or binding full captions into decorative text.
- Evidence ceiling before execution: `planned_motion`.

## Data and dependency boundaries

- No network, credentials, providers, voice upload, package-root creation, deployment, or public exposure.
- Use the shared Playwright runtime in a later Task Session; pin the observed runtime then.
- Prefer a consumer-owned, local static HTML/SVG prototype. The Anime.js asset must be pinned and locally resolved; the implementation route may not fetch it at runtime.
- The source package and Anime.js vault must show byte-zero delta after each mutation-capable SWU.
- WorkEpisode append is a later explicit SWU after an executed witness. It records the attempt; it does not promote a Lesson.

## Open design residue

- Recorded-voice timing is absent; current milliseconds are provisional.
- Overlay registration and visual sufficiency against flattened PNGs are untested.
- Performance thresholds and representative device profiles are unset.
- Accessibility equivalence needs executed semantic assertions and human review.
- Candidate diversity and decay defaults are deliberately deferred beyond L0.

