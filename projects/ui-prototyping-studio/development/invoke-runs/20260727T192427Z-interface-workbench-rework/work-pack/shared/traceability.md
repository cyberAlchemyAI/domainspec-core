# Inverse SWU → Design → Assertion Traceability

Status: `planned-unexecuted`

`SWU-ACCEPTANCE-MATRIX.json` is the canonical exact matrix, including spec
paths, greps/selectors, positive assertions, negative mutants, primary owners,
receipt fields, and lawful shared witnesses.

| SWU | Design / witness refs | Primary assertion |
| --- | --- | --- |
| 001 | Projection canonicalization; FIX-001/019 | UPW-A-001-DIGEST |
| 002 | DDR-01; FIX-016 | UPW-A-002-COHERENCE |
| 003 | Projection compatibility; FIX-001/019 | UPW-A-003-STATE |
| 004 | Stable Shell; FIX-002 | UPW-A-004-INERT |
| 005 | DDR-03; FIX-004/005/018 | UPW-A-005-TRAILING |
| 006 | Context Reconciler; FIX-003/006 | UPW-A-006-CONTEXT-PLAN |
| 007 | DDR-02; FIX-015/017 | UPW-A-007-ATOMIC-COMMIT |
| 008 | UX lifecycle/action spine | UPW-A-008-SPINE |
| 009 | UX active canvas | UPW-A-009-CANVAS |
| 010 | UX contextual inspector; FIX-008 | UPW-A-010-INSPECTOR |
| 011 | UX staged review; FIX-007 | UPW-A-011-REVIEW |
| 012 | UX interactions; FIX-009/014 | UPW-A-012-ACTIONS |
| 013 | UX historical lineage; FIX-013 shared | UPW-A-013-HISTORY |
| 014 | Responsive contract; FIX-013 primary | UPW-A-014-RESPONSIVE |
| 015 | Content rules/FR-14; FIX-020 | UPW-A-015-COPY |
| 016 | A11y interaction; FIX-008/009/010/021/022 urgency | UPW-A-016-INTERACTION |
| 017 | A11y visual; FIX-011/012/022 non-color | UPW-A-017-VISUAL |
| 018 | Security route boundary; FIX-024 | UPW-A-018-ROUTES |
| 019 | Security render boundary; FIX-023 | UPW-A-019-RENDERING |

Shared fixture use is regression/recomposition only. It never changes the
primary owner recorded in the JSON matrix. In particular, the two independent
assertions inside FIX-022 have separate primary owners: urgency/live semantics
in 016 and non-color perceivability in 017.
