# States: SuggestedTrack Route Expansion

## SuggestedTrackLifecycle

| State | Meaning | Entry |
| --- | --- | --- |
| needs_evidence | Suggestion exists but has no accepted source-backed evidence. | Seed or runner creation. |
| evidence_submitted | One or more redacted evidence candidates exist. | `AttachActivityEvidenceCandidate`. |
| operator_review | Operator is actively reviewing candidate evidence. | Operator-only future action. |
| source_backed | Source or geometry evidence has been accepted. | Operator-only future action. |
| retired | Suggestion is no longer active. | Operator-only future action. |

## Allowed Transitions

| From | To | Trigger | In This Build |
| --- | --- | --- | --- |
| none | needs_evidence | Seed or runner creates suggestion. | yes |
| needs_evidence | evidence_submitted | Runner consents and attaches a redacted activity summary. | yes |
| evidence_submitted | operator_review | Operator starts review. | no |
| operator_review | source_backed | Operator accepts source-backed evidence. | no |
| any active state | retired | Operator retires suggestion. | no |

## EvidenceCandidateLifecycle

| State | Meaning | In This Build |
| --- | --- | --- |
| submitted | Candidate is stored for later review. | yes |
| operator_review | Candidate is under review. | no |
| accepted | Candidate is accepted as useful evidence. | no |
| rejected | Candidate is rejected. | no |
