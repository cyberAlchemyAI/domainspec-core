# Define v2 Documentation Tournament — Private Governance Envelope

This directory contains DomainSpec-private dispatch governance for the public
Invoke documentation tournament. It must not be copied into `arcanum`.

The first candidate is an `experiment/propose` sheet. Its two agents review the
already-proposed public `CRITERION.md`; they do not run the six trials. A passing
proposal still requires exact human confirmation, registration, execution,
typed closeout, and an exact criterion reference before an `experiment/run`
sheet can become confirmation-ready.

Pre-registration no-effect readiness snapshot:

- sheet SHA-256: `d4a7357a10928df11b382d0fe864ef8e9fbb500fe267aee76903afc0f964506f`
- material SHA-256: `5749dc5a4b513390e5b97832ac6221b690f8393cbf5cd33e003c1a1c248fd00a`
- schema: `0.9.0`
- ledger read: `none`
- ledger mutation: `none`

These receipts prove form readiness only. This sheet has no subject group under
the v0.9.1 predicate, so it spawns no tension agents. After readiness, its
mechanical disposition is the exact digest-bound pair:

- `check-tension:no-subject:checker:d4a7357a10928df11b382d0fe864ef8e9fbb500fe267aee76903afc0f964506f`
- `check-tension:no-subject:reviewer:d4a7357a10928df11b382d0fe864ef8e9fbb500fe267aee76903afc0f964506f`

Those handles are gate slots, not independent judgments. They do not satisfy
human confirmation, registration, execution, or criterion freeze.

## Criterion Proposal Outcome

The exact sheet was human-confirmed, registered once, executed through the
capability-bound native two-wave route, and closed `resolved` with experiment
proposal status `invalid`.

- native run: `criterion-propose-20260827-01`
- native event validation: PASS, 16 causal events
- designer result: completed; revised only `CRITERION.md`
- candidate criterion SHA-256:
  `fd46783c9ab935f611561b7a02fb03bc40aa66be2ebdefe3ae2f785b9926c4ec`
- validity result: `INVALID`
- ledger close: `resolved` / `experiment/propose` / `invalid`
- agents: one writer and one read-only skeptic; zero feedback loops

The fatal criterion defect is cardinality wording: the Mechanical Outcome Rule
says to compare four candidate aggregate tuples even though the design has
exactly three candidates and four metrics. The remaining material coverage gap
is that no independent pre-freeze owner is assigned the bounded read scope and
receipt needed to verify guide section-inventory and section-byte equality.

Repair requires a fresh designer receipt, a fresh validity review, and renewed
human freeze confirmation on the revised criterion candidate. No criterion was
frozen, and the six-trial run was not started or authorized. Exact evidence is
under `criterion-propose.execution/`.

The public tournament protocol, guides, cases, oracle, and scorer remain under
`arcanum/spells/invoke/development/define-v2-documentation/tournament/`. A
private readiness or closeout receipt grants no publication or promotion
authority over those public artifacts.

## Machine-First Successor Candidate

The historical v0.9.0 sheet, dispatch, receipts, closeout, and ledger rows above
remain unchanged. New `criterion-successor-propose.*` files define a separate
schema v0.10.0 candidate:

- `CRITERION.json` is canonical; `CRITERION.md` is a deterministic generated
  view;
- wave one contains independent singleton criterion-design and
  guide-equivalence roles and their bound read-only validators;
- wave two contains the blind validity skeptic;
- execution contract v0.2 gives both waves exact gates and maps final `valid`
  to `gate_pass` and `invalid` to terminal `gate_resolved`;
- the preconfirmation compiler collects all reachable checks and records zero
  spawn attempts, but the current receipt is deliberately blocked only on the
  missing independently frozen subject-tension pair. That evidence has not
  been fabricated or inferred from this implementation run.

Validate the unconfirmed successor without writes:

```sh
python3 ops/development/2026-08-27-invoke-define-v2-documentation-tournament/validate_criterion_successor.py
```

Its state is intentionally `proposal_readiness:
block_pending_subject_tension`, `confirmation: not_requested`, and
`registration: not_started`. After the separately authorized subject-tension
check passes, regenerate the exact closure before requesting human
confirmation. A later run also requires the canary gate, a register/close pair,
and execution authority. Neither the live canary nor the six tournament trials
are authorized by these candidate bytes.

## Runtime Reconciliation Status

The profile-driven registrar reconciliation is implemented and its public and
private validation matrices pass. Registration v0.3 changes the executable
registration reference, so the earlier terminal-canary confirmation cannot be
reused. A bounded same-task review found no remaining P0-P2 issue in the
reconciliation candidate. No replacement confirmation has been requested.

The required single native Experiment Harness example produced a real passing
Invoke Define result for `invoke-define-live-pass` under `LIVE-DEFINE-001`.
However, the aggregate Invoke harness report is `VALIDATION=block` because two
existing consumers are stale: one Design fixture expects obsolete status prose,
and the preacceptance closure fixture omits the now-required
`joined_driver_digest`. The native attempt also records the generic Quality Bar
as `not_checked`, so there is no admitted Quality Bar pass. The acceptance-
critical whitespace scan found 18 whitespace-only lines with trailing spaces
in the generated raw report. The report remains unchanged as evidence. Per the
accepted stop rule, this run did not rewrite either consumer, rematerialize the
canary, request confirmation, register a dispatch, or start the six tournament
trials.
