# Implementation Plan: Minto Pyramid experiment L0

Status: proposal-only execution candidate; unapproved and unexecuted.

## Objective

Produce one complete candidate-specific non-vacuity witness for a narrowly sourced Minto Pyramid composition pattern without modifying Whisper or claiming reader efficacy.

## Approved source design references

- `../findings.md` at SHA-256 `568112550ba8f73f489e1bc101ccc7d6b9b776eacd4788fc7f9dae983e9b3cd2`.
- `../matrix-repair-continuation-001/CLOSEOUT-RECEIPT.json` at SHA-256 `3247ed15974e460e00a73537a6f69535ffb099efb9b2d7c532bf162e8d8fa7ea`.
- `../minto-pyramid-experiment-decision-001/DECISION-RECEIPT.json` at SHA-256 `71869afe1d0c614f67e527f124c8b75192d1acdf99839145a19a0dd67c7117ec`.
- Bounded planning context: `PLANNING-CONTEXT.md`.

These artifacts provide an accepted research-design baseline for this experiment. They do not authorize execution or canonical integration.

## Delivery boundary

Included:

- one synthetic executive-brief fact/span set;
- one flat evidence-led baseline ordering;
- one candidate ordering with a declared governing point and supporting groups;
- mandatory content-preserving baseline, candidate, and boundary review views;
- one discovery-led counterexample where the candidate remains inactive;
- mechanics-only validation;
- one role-label-blind human semantic review with a pre-review commitment, exact response, reveal, and bounded witness verdict;
- exact experiment-local receipts and closeout choreography.

Excluded:

- reader population, comprehension, trust, clarity, persuasion, retention, or any outcome metric;
- other candidates, unit levels, transports, or framework relations;
- a generic `framework_profile` or any Whisper schema, validator, preset, core, or public Arcanum change;
- network retrieval, copyrighted example reuse, private source locators, promotion, publication, deployment, commit, or push.

## Experiment contract

### Source binding

- Identity: Barbara Minto / Minto Books International official originator site.
- URL: `https://www.barbaraminto.com/`.
- Version: site copyright 2007–2026; identifies the 1996 textbook edition.
- Selectors: `Concept, lines 21-23`; `Textbook, lines 35-37` as bound in `../research.md`.
- Supported concept: one governing point with supporting ideas organized beneath it.
- Unsupported inferences: MECE, a complete answer-first method, universal applicability, and reader efficacy.
- Attribution: name Minto accurately; paraphrase only; do not copy proprietary instructional expression.

### Controlled positive pair

`EXPERIMENT-CASE.json` will contain one synthetic `span_set` shared byte-for-byte by both positive variants. Each span has a stable ID and original text. Baseline and candidate review views are mandatory and are mechanically reconstructed from those exact spans; no variant-specific prose is permitted.

- Audience: senior decision maker.
- Purpose: decide whether to approve a reversible pilot.
- Transport: executive brief.
- Unit: whole document.
- Word budget: 300–450 words after rendering.
- Baseline: all span IDs exactly once in a coherent evidence-led order, no declared support groups, governing-point span placed after evidence.
- Candidate: the same span IDs exactly once, governing-point span placed first, with two or three declared support groups beneath it.
- Changed decision: `declared-governing-point-support-hierarchy`.
- Intended prevented structural failure: `support-association-not-declared`.
- Controlled delta: one `composition_plan` selection. Ordering, block segmentation, and declared groups are the mechanically specified consequences of that one selection, not separately scored interventions.

The baseline view is one flat block in baseline order. The candidate view contains one governing-point block followed by one block per declared support group. Both views derive every visible byte from the shared spans using the exact declared joiners. The candidate operationalization is experiment-specific. It does not claim the public source supplies a complete answer-first algorithm.

### Boundary fixture

The case also contains original synthetic spans for a discovery-led composition where delayed disclosure is intentional. It declares:

- `applicability: false`;
- `candidate_activation: false`;
- the intended non-hierarchical form;
- the failure condition that any automatic Minto transformation would suppress that form;
- a mandatory content-preserving flat review view; and
- `transformation: null`.

### Non-vacuity verdict rule

The final verdict may be `pass` only when all of the following hold:

1. source, unit, transport, owner, applicability, proof state, changed decision, and prevented failure are bound;
2. baseline and candidate use the identical positive `span_set` exactly once;
3. the only controlled decision delta is selection of the declared hierarchy composition plan; ordering, grouping, and review-block segmentation match that plan exactly;
4. the candidate has exactly one governing point and two or three nonempty support groups;
5. the counterexample remains inactive and untransformed;
6. every predecessor path, SHA-256, size, closed shape, exact check ID, and declared structural invariant is independently recomputed from actual bytes without evaluating semantics;
7. a pre-review A/B mapping commitment exists before the role-label-blind packet, the exact human response binds that packet before reveal, and the reveal recomputes the commitment after response completion;
8. one human reviewer confirms factual equivalence, fair representation, executive-transport fit, hierarchy plausibility, the named hierarchy decision change, and boundary-case non-activation; and
9. the result states `authority_effect: none`, `integration_authorized: false`, `canonical_change_authorized: false`, and `reader_outcome_claims: false`.

Otherwise the verdict is `fail` or `inconclusive`, with named residue.

## Ordered implementation rules

### SWU-MPX-001 — author the controlled case

Inputs:

- accepted source/design references;
- the experiment contract above.

Output:

- `../minto-pyramid-experiment-001/case/EXPERIMENT-CASE.json`.

Algorithm:

1. Create six to ten original synthetic spans sufficient for one reversible-pilot decision.
2. Assign stable unique span IDs and one content string per ID.
3. Designate exactly one span as the governing point.
4. Build the baseline ordering from every span ID exactly once, with the governing point after the evidence and no support groups.
5. Build the candidate ordering from the identical span IDs exactly once, with the governing point first and two or three support groups covering every non-governing span exactly once.
6. Materialize mandatory baseline and candidate review views from the shared spans: one flat baseline block; one governing-point candidate block plus one block per support group; exact text-preserving joins only.
7. Create a separate discovery-led counterexample with a mandatory flat review view, keep candidate activation false, and set its transformation to null.
8. Bind provenance, applicability, proof state, owner, the single changed decision, the single prevented failure, and forbidden claims.

Failure modes:

- span content differs between positive variants;
- a span is omitted or duplicated;
- grouping smuggles in semantic edits;
- a review view is missing or does not reconstruct from the exact spans;
- the counterexample is transformed;
- a source limitation or claim ceiling is omitted.

### SWU-MPX-002 — validate declared mechanics

Input:

- exact case artifact from SWU-MPX-001.

Output:

- `../minto-pyramid-experiment-001/mechanical/MECHANICAL-VALIDATION.json`.

Algorithm:

1. Bind the exact case SHA-256 and size.
2. Re-run the repository-local validator over the actual case bytes; do not trust receipt fields as evidence.
3. Validate the closed top-level shape and required provenance fields.
4. Compare the baseline and candidate span-ID sets for exact equality and uniqueness.
5. Verify the declared governing point appears once and candidate support groups are nonempty and cover every remaining positive span once.
6. Reconstruct all mandatory review views from shared spans and exact joiners and reject text drift.
7. Verify the baseline has no support groups and places the governing point after at least one supporting span.
8. Verify the counterexample declares both applicability and activation false and has no transformation.
9. Verify the exact nine check IDs, reader-outcome ceiling, integration ceiling, and authority neutrality.
10. Record each check separately; do not make semantic judgments.

Failure modes:

- a check is inferred but not recorded;
- semantic equivalence is marked mechanically proven;
- a later successful check masks an earlier failure;
- the receipt's case reference differs from the recomputed path, SHA-256, or size.

### SWU-MPX-003 — perform human review and issue witness verdict

Inputs:

- exact case artifact;
- passing mechanical receipt;
- one human reviewer who receives only the role-label-blind packet until after the response bytes are complete.

Outputs:

- `../minto-pyramid-experiment-001/review/BLINDING-COMMITMENT.json`;
- `../minto-pyramid-experiment-001/review/BLINDED-REVIEW-PACKET.json`;
- `../minto-pyramid-experiment-001/review/HUMAN-REVIEW-RESPONSE.json`;
- `../minto-pyramid-experiment-001/review/HUMAN-REVIEW-AND-WITNESS.json`.

Algorithm:

1. Randomize the role-to-`A`/`B` mapping and generate a fresh 32–128-hex-character nonce in volatile Task Session state.
2. Before review, persist `BLINDING-COMMITMENT.json` containing only the canonical mapping-plus-nonce digest and UTC creation time.
3. Persist `BLINDED-REVIEW-PACKET.json` with exact case/mechanical/commitment references; a role-neutral review context binding audience, purpose, transport, unit, supported concept and limits, exact decision/failure, boundary intent, and claim limits; exact reviewer instructions; generic A/B text blocks derived from the mandatory case views; the boundary view; and six fixed human-readable prompts with allowed statuses and rationale rules. Omit role mapping and nonce.
4. Give the human only the packet. Persist `HUMAN-REVIEW-RESPONSE.json` with the packet's exact path/hash/size, human attestation, start/completion times, six ordered judgments, rationales, and `mapping_known_before_completion: false`.
5. Only after response completion, reveal the mapping and nonce in `HUMAN-REVIEW-AND-WITNESS.json`; recompute the commitment and bind the actual case, mechanical, commitment, packet, and response bytes.
6. Apply the non-vacuity verdict rule exactly. The `named-decision-changed` judgment must identify the A/B label exhibiting the declared hierarchy; `pass` requires that revealed label to be the candidate.
7. Record disagreements and limitations as residue and state the authority and reader-outcome ceilings explicitly.

Failure modes:

- the reviewer sees the candidate label before recording judgments;
- the packet omits or drifts any review-context value, reviewer instruction, exact prompt, allowed-status list, rationale rule, or A/B/none instruction;
- Task Session is interrupted after commitment but before reveal; restart the entire SWU with a fresh attempt rather than reconstructing the secret;
- the result substitutes preference or reader-effect language for the named hierarchy decision;
- any predecessor reference is self-reported rather than recomputed from actual bytes;
- a human disagreement is overwritten;
- `pass` is issued with any failed or missing prerequisite.

## Layer slices

| Layer | This Work Pack | Planned evidence | Deferred decision |
|---|---|---|---|
| L0 | Three SWUs above | One controlled case, mechanics receipt, commitment/packet/human-response chain, and witness receipt | Repeat, pivot, or stop. |
| L1 | Not in frontier | Second independent case and reviewer | Whether repeatability is credible. |
| L2 | Not in frontier | Local schema/validator and negative suite | Whether governance is reliable. |
| L3 | Not in frontier | Evidence-bound owner proposal | Whether integration design should even be considered. |

## Validation strategy

- JSON syntax uses `python3 -m json.tool`; acceptance-critical structure and handoffs use `work-pack/validators/validate_minto_experiment.py` over actual files.
- Content control is validated over span IDs, exact span text, reconstructed review blocks, recomputed SHA-256, and recomputed size—not inferred prose similarity or receipt self-attestation.
- Human semantic judgments remain in the human-owned receipt.
- Every command is an argv vector with repository-root cwd, timeout, and output limit.
- Any failed acceptance-critical check blocks the unit and successors.
- No command makes network requests or writes outside the declared experiment-run scope.

## Handoff boundary

This plan prepares a three-unit Task Session frontier but does not select a unit. `EXECUTION-ENTRY.json` remains `blocked` with two explicit unsatisfied prerequisites: exact acceptance of the final plan bytes and later direct execution intent. The earlier Minto candidate-selection receipt binds candidate identity only. After proposal readiness proof, a separately authorized acceptance route must close the first prerequisite; later direct execution intent must produce a fresh selection and single-use Task Session admission.
