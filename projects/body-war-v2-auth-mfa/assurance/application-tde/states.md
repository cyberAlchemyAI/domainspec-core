# Application lifecycles

## SuggestedTrack

### Transition Table

| From | Event | To | Guard | Effect |
| --- | --- | --- | --- | --- |
| needs_evidence | attach | evidence_submitted | true | generated transition |
| evidence_submitted | attach | evidence_submitted | true | generated transition |
| operator_review | attach | operator_review | true | generated transition |
| source_backed | attach | source_backed | true | generated transition |
| retired | attach | retired | true | generated transition |
| needs_evidence | last-evidence-removed | needs_evidence | true | generated transition |
| evidence_submitted | last-evidence-removed | needs_evidence | true | generated transition |
| operator_review | last-evidence-removed | needs_evidence | true | generated transition |
| source_backed | last-evidence-removed | needs_evidence | true | generated transition |
| retired | last-evidence-removed | needs_evidence | true | generated transition |
## Open Questions

See ../../README.md#open-questions.
