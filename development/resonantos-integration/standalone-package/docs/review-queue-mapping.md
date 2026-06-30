# Review Queue Mapping

## Lifecycle Map

| Candidate Stage | Host Archive Mechanism | Package Contract |
| --- | --- | --- |
| Capture | Intake-only write or ingest request | Evidence-card candidate with scope tag |
| Review | Review Queue | Candidate fixture and owner metadata |
| Decide approve | Owner decision | Provider body may perform trusted write |
| Decide reject | Owner decision | Candidate remains rejected or archived |
| Decide escalate | Owner decision | Candidate routes to narrower or higher owner |

## Rules

- One intake record has exactly one scope tag.
- Candidate records do not write trusted knowledge pages.
- The Review Queue is host-owned; the package does not add a parallel queue.
- Promotion happens only after explicit owner approval.

## Fixture

See `fixtures/review-queue/candidate-request.json`.
