# Body War Business View Novice-Comprehension Attacks

## Gate and dispatch summary

Dispatch:
`2026-07-29-body-war-business-view-novice-comprehension-review`

The review was admitted under P1 because measurement validity, ontology
authority, generated-interface mechanics, and cold-reader usability required
independent judgments. The schema `0.8.0` sheet passed deterministic validation,
two independent tension checks passed against sheet digest
`366bc26411575eb3c3eac698c69f560b795a8a0adb6cf66b96641128da0edc8a`,
the user confirmed that exact digest, and the append-only dispatch ledger
registered seven agents across four groups.

This was a review, not an experiment. Every target agent was read-only. No
novice run, human witness, ontology mutation, generated-view implementation,
promotion, release, or production action occurred.

## Initial attacks

### Simon, Herbert — measurement validity

Simon attacked transfer validity, blindness, contamination, identical-task
comparability, stall classification, and the agent-versus-human evidence
ceiling.

Reusable controls from the historical DomainSpec instrument include:

- exact learner allow/deny scope
  (`projects/domainspec-v2/development/comprehension-novice-test/novice-agent.md:12-23`);
- learner task and reviewer answer-key separation
  (`task-coverage-audit.md:7-18`);
- byte-identical task and prompt within a comparison
  (`DESIGN.md:50-56`);
- contamination invalidation and separately recorded stall severity
  (`DESIGN.md:26-30,59-60`); and
- agent execution as structural pre-test evidence only, with human evidence
  deferred (`DEFINE.md:45-59`).

The original CampusRead authoring task, its type-coverage quotas, its complete
stall taxonomy, and its minimum-stall acceptance rule do not transfer to a
Body War reading surface. The current cleaned historical task no longer
contains the old answer key, but `task.md:50-52` still exposes reviewer-facing
leakage history and contaminated-run metadata, so those bytes are not suitable
for a fresh blind learner instrument.

The measurement attack proposed new reading loci:
`locate`, `trace`, `retell`, `distinguish`, `boundary`, and `vocabulary`.
Correctness must be scored from exact relation, branch, and boundary keys rather
than from self-reported hesitation or paraphrase overlap. Zero observed stalls
must remain valid data.

### Gadamer, Hans-Georg — ontology authority and interpretation

Gadamer attacked semantic collapse, invented edges, provenance loss, hidden
sequence, and authority overclaim.

The current journey tone logic collapses blocked authority and explicit
`does_not_promote` into the same `boundary / Claim limit` presentation
(`projects/body-war/ontology/business/scripts/generate-views.mjs:482-505`).
Blocked endpoints can be labelled `Owner gate visible`, but the details show
only `relation.owner_route` (`generate-views.mjs:531-540`). The actual blocking
owner and next gate remain in residue—for example score policy and geometry
privacy (`projects/body-war/ontology/business/residue.json:7-40`).

This creates two distinct defects:

1. a classification defect between blocked owner decision, explicit
   non-promotion, and projection; and
2. a routing/provenance omission between Relation owner and Blocking
   owner / Next gate.

The attack also found learner-facing copy that can be retold as verified or
realized behavior:

- `Confirmed evidence supports...`
  (`authoring/view-catalog.mjs:127-140`);
- `Candidate geometry becomes ... then produces...`
  (`authoring/view-catalog.mjs:143-157`); and
- `chain` / `affect` wording for relations the journey itself describes as
  sibling branches (`authoring/view-catalog.mjs:173-183,326-332`).

Defended zero-findings:

- story relation IDs resolve to admitted relations and repeat none within a
  story (`tests/business-views.test.mjs:120-159`);
- learner and navigation fields remain projection data outside semantic nodes
  and relations;
- `GeometryCandidate` and `ScorePreview` retain explicit non-promotion
  boundaries (`authoring/view-catalog.mjs:159-168`); and
- the package remains `candidate-local`, `authority_effect: none`,
  `release_admission: not-granted`
  (`profile.json:5-10`; `receipts/validation-receipt.json:52-53`).

### Shannon, Claude — generated interface and cold-reader path

Shannon traced the canonical path from catalog through generator, Markdown, two
HTML projections, and tests.

The interface attack found:

- current tests assert generated strings and structures but do not provide a
  durable browser receipt (`tests/business-views.test.mjs:102-118,161-196`);
- sibling branches carry A/B markers in the catalog but numeric 3/4 navigation
  in the generated page (`view-catalog.mjs:209-239`;
  `generate-views.mjs:580-589`);
- relation collections use ordered-list semantics despite the explicit
  non-runtime-sequence disclaimer (`generate-views.mjs:546-563,589`);
- both stories are present before JavaScript establishes tab visibility, so the
  no-JavaScript surface retains misleading tab semantics and copy
  (`generate-views.mjs:657-680`);
- the exact package ceiling is absent from the journey projection; and
- the printable gallery has an unverified small-screen legibility risk, but the
  declared corpus contains no durable browser receipt supporting exact numeric
  measurements.

Shannon recommended a separate learner projection. The journey remains the
reference stimulus; the printable gallery remains exhaustive review material.
Neither should embed a reviewer key or scoring rubric.

## Robot-talk confrontation

The three attackers converged on these repairs:

1. Create a separate generated learner task and keep reviewer artifacts
   unshipped.
2. Distinguish blocked decision, explicit non-promotion, and projection.
3. Preserve Relation owner and separately expose every matching Blocking owner
   and Next gate.
4. Remove unsupported verified, causal, temporal, and branch-feeding prose.
5. Align A/B navigation, use unordered relation collections, and make the
   no-JavaScript surface semantically valid.
6. Surface the exact package ceiling.
7. Require durable browser evidence before admitting a generated view as a
   novice-test stimulus.

The confrontation resolved the major disagreements:

- The historical answer-key leak is removed, but current `task.md:50-52`
  remains unsuitable as blind learner input because it exposes reviewer
  history.
- The blocked-versus-boundary tone defect and the missing blocking-owner route
  are separate findings; fixing one does not fix the other.
- The sibling-branch note does not neutralize contradictory `chain`, `affect`,
  `becomes`, or `then` prose elsewhere.
- The printable small-screen risk survives, but the unreceipted `390px`,
  `scrollWidth 574`, and approximately `5px` claims do not.

## Verifier verdicts

| Change request | Final verdict | Verifier constraint |
| --- | --- | --- |
| CR-1 | HIGH — accept with fixes | Only learner task data may enter the learner generator. Reviewer allow/deny, keys, audit, rubric, correctness, stalls, results, and human records remain unshipped. Task/loci/prompt/stimulus are preregistered once and byte-identical across arms. |
| CR-2 | HIGH — keep, authority-constrained | Join all residue matching either endpoint through `affected_concepts`; preserve Relation owner; never synthesize relations, status, authority, or decisions; preserve semantic digests. |
| CR-3 | HIGH — accept with authority fix | Remove only unsupported causal, temporal, or proof prose; preserve legitimate literal state and authority terms; use A/B parity, unordered relation groups, and native no-JavaScript navigation. |
| CR-4 | MEDIUM — scope-narrowed blocker | A pinned browser receipt blocks admission of a particular stimulus to the novice protocol, not ontology validation or deterministic generation. |

No change request was dropped.

## Dropped and narrowed claims

- Dropped exact unreceipted mobile width, overflow, and text-size numbers.
- Narrowed printable-gallery status to an unverified responsive/legibility
  risk outside the initial protocol.
- Rejected any claim that current tests establish browser usability or
  comprehension.
- Rejected embedding answer keys, relation keys, rubrics, or results into
  learner-visible HTML.
- Rejected using an agent pre-test as human-comprehension evidence.

`scripts/generate-views.mjs --check` and the existing Node suite passing `8/8`
establish generated-artifact currency only.

## Boundary

No target source file was edited. These attacks do not run the proposed
instrument or authorize implementation, human witnessing, runtime behavior,
ontology promotion, release, or production.

