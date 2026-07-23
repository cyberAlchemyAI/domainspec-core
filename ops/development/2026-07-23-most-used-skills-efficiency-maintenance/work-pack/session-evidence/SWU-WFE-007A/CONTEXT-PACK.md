# Context Pack: SWU-WFE-007A

Status: strict coverage pass

Mode: standard

Lifecycle route: private tooling and Sigil Development revision with focused
appender validation

## Task boundary

Extend new dispatch rows to schema 0.7.0 with one closed evidence binding that
proves the live sheet bytes match two independent PASS verdict handles and an
explicit human-confirmation handle. Preserve all historical ledger rows and
duplicate-close behavior. Do not synchronize strategy runtimes yet; classified
composition belongs to SWU-WFE-007B.

## Obligation matrix

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| DSS2A-O1 | New dispatch schema/version extension is explicit. | task rule; current 0.6.0 appender | covered |
| DSS2A-O2 | Evidence stores handles and digests, never full chat returns. | task minimum extension | covered |
| DSS2A-O3 | Exactly two unique tension verdicts must both be PASS. | owner lifecycle; task acceptance | covered |
| DSS2A-O4 | Explicit confirmation must be true and have a handle. | owner lifecycle; task acceptance | covered |
| DSS2A-O5 | Both verdicts and confirmation bind the same sheet digest. | accepted DSS-2 finding | covered |
| DSS2A-O6 | The appender independently hashes the live repo-contained sheet. | post-confirmation mutation control | covered |
| DSS2A-O7 | Missing/failing/partial/mismatched evidence rejects before append with ledger byte safety. | task acceptance | covered |
| DSS2A-O8 | A complete matching binding appends and persists as one JSON column. | task positive control | covered |
| DSS2A-O9 | Historical rows remain structural-grandfathered and duplicate close remains idempotent. | DSS-1 compatibility | covered |
| DSS2A-O10 | Private canonical strategy/form guidance changes without premature runtime copying. | task split and private/public boundary | covered |

## Selected evidence

| Path | Selectors | Why selected | SHA-256 |
| --- | --- | --- | --- |
| `work-pack/tasks/TASK-WFE-007-DSS-SHEET-BINDING.md` | 007A behavior, compatibility, scope | complete SWU contract | `546fb961a6db2a33fd1d77ef5d8fae4f63cf8bb99c5eba8a630551f8ed210623` |
| `DESIGN.md` | dispatch evidence binder and authority boundaries | architecture boundary | `94bcee30991e0e4ef5975a71f3d5cbb884bb468918a7c6759a02dbffb39c0b19` |
| `../2026-07-22-most-used-skills-efficiency-review/findings.md` | DSS-2 accepted finding | source requirement | `0515af8d3dd746f8b020cad3515232afe5bb5cd2f6d60a00b567ee5e314018fd` |
| `implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/register-dispatch/append-dispatch.cjs` | schema, validation, emission, ledger grandfathering | deterministic owner target | `ae2800d8f5c1443f4bd356a578e04740c4b1b75fcc6bd68ca2000430182aaef4` |
| `implementation/domainspec/internal_tools/subagents-dispatch-hooks/tests/test-append-dispatch.cjs` | full appender battery | compatibility and causal fixture target | `1ff9a6408bd23584d3a5e15950ca9f12a4db8a78def55efbde430228c6e1e552` |
| `implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md` | propose, double tension, confirm, freeze, register | private owner contract | `bd4266169fad55999fe6cfe941a04d18a9a7858a1818eeeea20a25dcb818ed74` |
| `work-pack/session-evidence/SWU-WFE-001/receipt.json` | hardened admission dependency | technical dependency | `b260f55d6527bd039f8c898aafdbcee007893dd177474e4a7f2ba0a48db72273` |
| `work-pack/session-evidence/SWU-WFE-006B/receipt.json` | serial predecessor | program-order dependency | `5d1d7582c569c62428999db21c2456fb4a7acd67311c8651ce794655fcf0e66e` |

## Schema/version decision

- New dispatch input version: `0.7.0`.
- Historical ledger rows: unchanged and structurally grandfathered.
- New required top-level field: `evidence_binding`.
- Binding fields:
  - `sheet_path`: repository-relative live sheet file;
  - `sheet_sha256`: lowercase SHA-256 of current sheet bytes;
  - `tension_verdicts`: exactly two unique `{handle, verdict, sheet_sha256}`
    objects, both `verdict=pass`;
  - `confirmation`: `{handle, confirmed, sheet_sha256}` with
    `confirmed=true`.
- The appender resolves containment, requires a regular file, hashes the live
  bytes, and compares every digest.
- The ledger emits the complete binding as one JSON flow column. It contains
  handles, not conversation bodies.

## Validation surface

```bash
node implementation/domainspec/internal_tools/subagents-dispatch-hooks/tests/test-append-dispatch.cjs
git diff --check -- implementation/domainspec/internal_tools/subagents-dispatch-hooks
```

## Context Builder result

- Files selected: 8
- Obligation coverage: 10/10
- Uncovered obligations: 0
- Contradictions: 0
- Strict coverage: pass
- Mutation gate: pass
- Runtime handoff: none; execution is local and bounded
