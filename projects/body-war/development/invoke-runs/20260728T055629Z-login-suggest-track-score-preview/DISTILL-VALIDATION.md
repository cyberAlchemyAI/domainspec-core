---
module: body-war-login-suggest-track-score-preview
version: current
status: pass-with-owned-decisions-and-schema-residue
updatedAt: 2026-07-28
docType: invoke-distill-validation
---

# Distill Validation

## Frame

Smallest target: a Body War web prototype that lets an authenticated runner
select a non-first SuggestedTrack, affirm exact track/activity/geometry
consent, derive private candidate geometry, and see an explained
`preview_only` score without promoting route or game authority.

Evidence frame expires if the current Body War auth/SuggestedTrack contracts,
Strava scope/refresh contract, ScorePolicy owner decision, geometry privacy
decision, or Invoke manifest schema changes.

## Technique Trace

| Technique | Use |
| --- | --- |
| frame the boundary | separated local fixture, moderated human, real-gateway code, hosted witness, promotion, and production claims |
| ontology mapping | mapped business nodes, system realizations, bridge evidence, drift, state, and owner ceilings |
| smallest working unit | retained nine coding/validation SWUs plus separately owned decisions and human/operator units |
| recomposition check | bound confirmation, geometry, canonical score input, score result, receipts, and lifecycle ceilings by exact selectors/digests |
| pre-mortem | tested wrong owner, circular/sparse score, split mutation, token refresh race, raw-stream sink leak, generic receipt pass, and responsive consent failure |
| governed adversarial review | two independent attack lenses, robot-talk convergence, synthesis, literal-byte verification, writer, and parent approval |

## Review Result

Dispatch `2026-07-28-body-war-login-score-plan-review` closed `resolved`.
Five registered agents produced ten verified change requests and one refuted
claim. There were no surviving CRITICAL findings. The full transcript and
accepted list are in `distill-review/attacks.md` and
`distill-review/findings.md`.

Post-review Plan reconciliation applied all six MAJOR requests and three of
four MINOR requests. The remaining MINOR request is schema-owned:
`DESIGN-SCOPE-MANIFEST.json` cannot encode contract-authored/not-run under the
live `1.0.0` enum. This is visible residue, not an execution-evidence claim.

## Recomposition

```text
DEC-JSP-001 and DEC-JSP-002
  -> L0 complete-window fixture contracts
    -> pending intent
      -> ownership validation
        -> confirmation + candidate evidence
          -> private GeometryCandidate
            -> canonical ScoreInputSnapshot
              -> preview_only ScorePreview
                -> responsive authenticated projection

DEC-JSP-003
  -> L2 real gateway code
  -> HOST admission receipt
    -> explicit parent admit/reject
      -> separately authorized L3 supervised witness
```

Every arrow has an owner, input/output contract, failure state, and evidence
ceiling. Fixture success cannot satisfy real-provider or hosted gates.

## Hidden Gaps and Pre-Mortem Disposition

| Failure | Disposition |
| --- | --- |
| Single activity manufactures a comparable 14-day score | blocked by `ScoreInputSnapshot.historyState`; L0 uses complete fixtures, incomplete history has null total/frequency |
| Evidence persists for an unowned/stale activity | ownership validation precedes confirmation/evidence |
| Multiple POSTs duplicate or return stale stages | one public command/read selector plus independent canonical stage keys |
| Raw streams leak through non-database sinks | enumerated active sinks plus per-sink sentinel tests |
| Concurrent refresh overwrites the newest token pair | real-provider SWU requires CAS/singleflight, reread, bounded retry |
| HOST admission silently executes a participant | separate steps plus explicit parent gate |
| Generic receipt passes without claim proof | generic envelope must reference a claim-specific receipt artifact and passing validator result |
| Responsive consent hides under stress | explicit width, height, 200% text, long-content, and orientation witnesses |

## Verdict

`pass-with-owned-decisions-and-schema-residue`

The Define/Design/Plan package is coherent enough for decision resolution and
later SWU selection. It is not an implemented prototype: `DEC-JSP-001` through
`DEC-JSP-003` are open, `selected_swu` is `none`, and no Task Session,
deployment, participant, or real-provider execution is authorized.
