# SuggestedTrack Testable-Prototype Gap Research Strategy

## Status

- Dispatch type: `research`
- Schema: `0.7.0`
- State: closed `resolved`
- Sheet SHA-256:
  `28dfc735cf9b04711fa6fa97e688c23bbf827122b475a25efc7acb5b8467ff80`
- Form validation: `pass`; schema `0.7.0`; ledger mutation `none`
- Check-tension: `PASS + PASS` on the exact sheet digest
- Human confirmation:
  `body-war-suggested-track-prototype-gap-confirmation-20260727`
- Registration: one append-only dispatch row
- Execution: completed; nine agents; one synthesis/reviewer revision loop
- Evidence closure: `ready` for research writing
- Audit: `RECOMMEND_ACCEPT`
- Parent verdict: `ACCEPT`
- Closeout: one append-only close row; `exit_reason: resolved`
- Authority effect: none

## P1 Trigger

Dispatch is warranted because the question requires synthesis across at least
three independent evidence lenses: current contract/runtime parity, visible
participant testability, and hosted real-provider operations. The lenses can
run in parallel and are expected to disagree about which gaps belong before
the first test.

## Lanes And Subagents

### Explorers

Three agents run in parallel under a composite methodology and source-corpus
axis:

- `van Lamsweerde, Axel` reconciles current ledger, specification,
  implementation, persistence, and tests into an exact gap matrix.
- `Alexander, Christopher` inspects visible usability, affirmative consent,
  route-selection affordances, error recovery, and participant-test scope.
- `Beer, Stafford` maps deployment, DNS, Traefik, secret ownership, real Strava,
  Postgres, consent, and redacted receipt dependencies.

The group is designed to disagree on whether a gap is required for local
testing, real-friend testing, or only a later product frontier.

### Synthesis

`Simon, Herbert` reconciles the explorer returns into one
`test-now / must-fix / defer` frontier, bounded work units, acceptance checks,
and separate local and hosted test routes.

### Review

Three skeptics run in parallel and then confront the synthesis:

- `Rittel, Horst`: precedent and current-owner gate.
- `Popper, Karl`: non-vacuity and executable-witness gate.
- `Lakatos, Imre`: definitional soundness and claim-collapse gate.

Their attack vectors are distinct by construction.

### Persistence And Approval

- `Shannon, Claude` writes `findings.md` only after cited-synthesis evidence
  closure returns `ready`.
- `Brandenburg, Martin` audits only `findings.md` and returns an independent
  acceptance recommendation.
- The live registrar's P12 rule requires `final_approver: parent` because it
  rejects every in-sheet agent, including the dedicated auditor, as a working
  agent. The parent retains final acceptance.
- The strategist, not the writer, appends verbatim explorer returns to
  `research.md`.

## Dependency Flow

```text
explorers -> synthesizer <-> reviewers -> evidence closure -> writer -> auditor
                 |                                            |
                 +-> explorers feedback                       +-> writer revision
```

- Synthesizer/reviewer zig-zag: one loop.
- Synthesizer/explorer evidence feedback: one loop.
- Auditor/writer revision: one loop.
- Whole-dispatch ceiling: two loops.

## Inventory Preflight

- Lookup readiness: `ready`; machine validation passed with zero failures and
  88 tag warnings.
- Selected discovery leads:
  - `ontology-working-prototype-gap-research-result-synthesis`
  - `domainspec-v2-fpr02-integrated-consumer-proof-refresh`
- Excluded as non-load-bearing: Mint/Body War convergence findings and Studio UX
  research.
- Gap: no direct current SuggestedTrack/BWOI completion entry exists.
- Design consequence: current Body War bytes are load-bearing, and Inventory
  fields are routed narrowly as non-authority guardrails.

## Expected Result

The research returns:

1. a direct answer about which test frontier already works;
2. an exact gap and owner matrix;
3. the smallest bounded implementation units needed before real-person
   testing;
4. runnable acceptance commands and a participant test protocol;
5. a hosted real-Strava dependency and receipt route; and
6. explicit deferred claims for geometry, promotion, pilot readiness, release,
   and production.

Research does not change the application, deploy it, access secrets, promote
ontology, release DomainSpec, or authorize production.

## Next Human Action

Research is closed. If implementation is separately authorized, select LP-01
alone as the smallest bounded next route. The research result does not itself
select LP-01 or authorize any application, participant, deployment, real
Strava, promotion, release, or production action.
