# TASK-MPX-001-CASE — Author the controlled case

## Objective

Create one exact, source-bound experiment case containing an otherwise-controlled executive-brief pair and one inactive discovery-led counterexample.

## Mapping

- Slice: S-MPX-01
- Layer: L0
- Wave: W0
- SWU: SWU-MPX-001
- Source contracts: `../../IMPLEMENTATION-PLAN.md#SWU-MPX-001--author-the-controlled-case`; `../../PLANNING-CONTEXT.md#Bound-design-decisions`

## Dependencies

None. Execution still requires exact plan acceptance, direct execution intent, selection, and Task Session admission.

## Smallest Working Unit: SWU-MPX-001

- Primary behavior: materialize one controlled experiment input contract.
- Independent acceptance boundary: the case alone passes its closed shape, provenance, exact span-set, ordering, grouping, counterexample, and claim-ceiling checks.
- Candidate child units: source binding; positive pair; boundary fixture.
- Retained-boundary rationale: none is an executable candidate-specific case without the other two; splitting would create partial inputs that cannot pass independently.
- Write scope:
  - `ops/development/2026-08-25-whisper-writing-frameworks-research/minto-pyramid-experiment-001/case/EXPERIMENT-CASE.json`
  - `ops/development/2026-08-25-whisper-writing-frameworks-research/minto-pyramid-experiment-001/precloseout/SWU-MPX-001.json`
  - `ops/development/2026-08-25-whisper-writing-frameworks-research/minto-pyramid-experiment-001/receipts/SWU-MPX-001.task-session.json`
- Invoke-owned closeout output, excluded from Task Session write scope:
  - `ops/development/2026-08-25-whisper-writing-frameworks-research/minto-pyramid-experiment-001/closeouts/SWU-MPX-001.invoke-refresh.json`
- Immutable inputs: accepted findings, decision receipt, research/source receipts, and all plan artifacts except the exact lifecycle-owner closeout targets.
- Done criteria:
  - original synthetic prose only;
  - source identity/version/selectors and attribution limitations present;
  - whole-document executive transport and current owner present;
  - positive variants reference the identical stable span set exactly once;
  - the single changed decision is `declared-governing-point-support-hierarchy` and the single prevented failure is `support-association-not-declared`;
  - baseline and candidate share one span set, while their exact order, grouping, and block segmentation match the declared flat-versus-hierarchy composition plans;
  - exactly one governing point and two or three candidate support groups;
  - every support group is nonempty and together they cover every non-governing span once;
  - mandatory baseline, candidate, and boundary review views reconstruct exactly from the shared spans;
  - counterexample applicability and activation are false and its transformation is null;
  - proof state and forbidden claims are explicit.
- Acceptance evidence: exact case SHA-256 and size plus both validation commands passing.
- Execution owner: subagent preferred; Task Session local fallback allowed.
- Handoff note: use only the accepted selectors in `PLANNING-CONTEXT.md`; do not browse, copy proprietary examples, add MECE/reader claims, or touch Whisper.

## Proposed case shape

Required top-level keys:

`schema_version`, `experiment_id`, `candidate`, `source_binding`, `placement`, `decision_contract`, `positive_case`, `boundary_case`, `claim_boundary`, `authority_effect`.

The positive case contains one `spans` array and two composition plans that reference those span IDs. `review_views` is mandatory: the baseline has one flat block, while the candidate has one governing-point block followed by one block per declared support group. Each block's text and each full view must be an exact join of the referenced shared span text. The boundary case likewise carries one mandatory flat view and `transformation: null`.

## Validation

Use `work-pack/shared/VALIDATION-CONTRACTS.json#/units/0`. Its repository-local validator enforces closed shape and exact content reconstruction over the actual case bytes. No validation command may claim semantic equivalence; that remains SWU-MPX-003.

## Synchronization

On Task Session pass, emit the precloseout and terminal receipts, then route only the declared closeout target inventory through `invoke:refresh:apply-approved`. The unique successor is SWU-MPX-002.
