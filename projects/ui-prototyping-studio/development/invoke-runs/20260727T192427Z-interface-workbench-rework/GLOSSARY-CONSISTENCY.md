# Glossary Consistency Check

## Result

- Status: pass
- Scope: Define specification, architecture, UX Plan, witness contracts, and
  validation strategy
- Revision basis: accepted DDR-01–DDR-05 wording and UPW-FIX-001–024
- Definition promotion: none

## Checks

| Term | Required meaning | Result |
| --- | --- | --- |
| current head | application-owned current revision/document | consistent |
| staged candidate | inspected non-current candidate | consistent |
| stable shell | document preserving named context across unchanged polls and keyed updates | consistent |
| update | application of an unseen server projection version | consistent |
| coherent projection snapshot | one accepted read epoch from which projection and compatibility fields derive | consistent |
| trailing refresh | one queued fetch required when action completion joins an older in-flight poll | consistent |
| recoverable region commit | prepared keyed update that either commits fully or restores prior mounts, context, and applied versions | consistent |
| canonical JSON | exact server/test encoding used for opaque whole and region digests | consistent |
| acknowledgment | actor-neutral binding to live identity/action/target state | consistent |
| Revert | append-only correcting revision | consistent |
| Export | terminal-only explicitly confirmed handoff | consistent |
| history | secondary non-current lineage evidence | consistent |
| ready | always qualified by exact predicate/owner | consistent |
| accessible | not used as an unqualified completion claim | consistent |

## Forbidden Collapses

No artifact equates:

- staged with current;
- acknowledged with authorized identity;
- Export confirmed with evidence complete;
- implementation ready with release ready;
- bounded accessibility checks with certification;
- automation with human evidence; or
- Plan candidate with selected SWU.
