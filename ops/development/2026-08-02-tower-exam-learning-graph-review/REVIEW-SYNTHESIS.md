# Tower-to-exam delegated review synthesis

Status: `pass-with-design-repairs`; implementation remains unauthorized.

## Converged findings

1. The graph knowledge layer starts from persisted Research Tower records, not
   DomainSpec ontology records and not inferred topic labels.
2. Initial authority-bearing families are `Source`, `Tower`, `Claim`,
   `DefinitionCard`, `WorkedExample`, `OpenResidue`, and `PageCitation`.
3. `Topic`, `StudyRoute`, prerequisites, and semantic cross-links are derived
   views until an explicit persisted contract exists.
4. `ExamQuestion`, `ExpectedAnswerElement`, `LearnerAttempt`, `KnowledgeGap`, and
   `NextReviewRoute` form a separate learner-session overlay.
5. Every supported element and assertion relation carries source hash, tower
   artifact selector, PDF page/range, evidence taxonomy, and OCR/extraction
   status. Missing or unverified bindings abstain.
6. Stable IDs use source hash + tower slug + artifact path + record kind + local
   ID or deterministic selector. Input order is never identity.
7. The first meaningful learner witness is not free graph browsing. It is a
   deterministic transformation from one missing expected element to one exact
   evidence target and one grammatical next question.

## Preserved tensions

- The structure lane blocks implementation planning until identity and
  provenance are specified. The falsification lane permits a specification-only
  eight-question toy game now. Reconciliation: design the schema and toy
  evidence contract together, but keep source mutation and HTML implementation
  blocked until deterministic fixtures exist.
- The old HTML demonstrates useful interaction mechanics, but its DomainSpec
  data is forbidden. Reconciliation: reuse interaction grammar only and require
  new browser evidence against tower-derived data.
- Cases 6 and 7 are useful operator prompts but lack proposition-level answer
  keys. Reconciliation: test issue-slot completion and abstention, never invent
  case facts or doctrine.

## Design consequences

- Reduce the seed schema before planning.
- Define a two-layer data contract: tower projection plus learner session.
- Make provenance a required record, not inspector decoration.
- Use an eight-question deterministic element-completion game with one
  unsupported control.
- Preserve `local-research-only`; do not claim comprehension, mastery, exam
  effectiveness, promotion, publication, release, or deployment.

## Receipts

- `receipts/structure-explorer.json`
- `receipts/falsification-reviewer.json`
- `receipts/memory-residue-reviewer.json`
