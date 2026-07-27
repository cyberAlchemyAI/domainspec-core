# Gap Ledger: Invoke Design Coverage

| ID | Scope | Gap | Owner | Repair | Readiness effect |
| --- | --- | --- | --- | --- | --- |
| DVC-G01 | worktree | planned canonical `README.md` and validation-runner paths already contain unrelated dirty changes | Spellcraft execution owner | capture per-SWU baselines and admit only declared deltas | later overlapping SWUs gated; fixture-only first SWU remains selectable |
| DVC-G02 | implementation | manifest schema does not exist | Spellcraft | SWU-DVC-002A | blocks extractor |
| DVC-G03 | implementation | denominator receipt schema does not exist | Spellcraft | SWU-DVC-002B | blocks extractor receipt |
| DVC-G04 | implementation | selection result schema does not exist | Spellcraft | SWU-DVC-002C | blocks validator result |
| DVC-G05 | implementation | independent extractor does not exist | Spellcraft | SWU-DVC-003 | blocks `design-validator-pass` |
| DVC-G06 | implementation | deterministic selection validator does not exist | Spellcraft | SWU-DVC-004 | blocks `design-validator-pass` |
| DVC-G07 | validation | frozen controls and mutation tests are not runnable | Spellcraft | SWU-DVC-001 and SWU-DVC-005 | blocks validator-backed claim |
| DVC-G08 | contracts | Design, architecture, and UX contracts do not carry the new selection model | Spellcraft | SWU-DVC-006A/B/C | blocks integrated mode |
| DVC-G09 | projections | generated runtime surfaces are not synchronized | bootstrap owner | SWU-DVC-007 | blocks parity |
| DVC-G10 | proof | no post-change generic Define → Design → Plan run exists | Spellcraft | SWU-DVC-008 | blocks promotion readiness |

None of these gaps is concealed by the authored package. They are the planned
implementation target.

## Closure update

- DVC-G01 was mitigated by exact preimage digests and scoped admissions.
- DVC-G02 through DVC-G10 are closed by the terminal SWU receipt chain.
- The DVC implementation and generated surfaces have no scoped public-scan
  hits.
- The four pre-existing local/private path findings were repaired by
  `ops/development/2026-07-26-invoke-public-hygiene-repair/`.
- Promotion remains flagged by the strengthened diagnostic: 29 historical
  `projects/ide-extension` bindings across 10 Distill/Workbench fixture,
  receipt, dispatch, and runner files require a governed consumer-adapter
  extraction. They are recorded in
  `work-pack/session-evidence/SWU-DVC-008/leakage-report.json`.
