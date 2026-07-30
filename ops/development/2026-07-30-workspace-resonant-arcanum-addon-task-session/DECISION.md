# Decision Gate: Resume Arcanum Add-on Implementation

## Control

- Decision: `DEC-ARC-TS-001`
- Target: Arcanum add-on Task Session over the current
  `workspace-resonant` work pack
- Status: `PASS`
- Source request: implement through a working browser-tested version; use the
  private decision profile when a decision is encountered
- Admissibility request digest:
  `sha256:17d35106e9bac71aa46d667551af98dc90bb97afb381df4767f13ab0d5d412a0`
- Admissibility route: `gate`
- Selected option: `OPT-REVALIDATE`
- Decision source: explicit user reply `OPT-REVALIDATE`

## Blocker Question

How should the blocked Task Session proceed now that the reconciled Plan bytes
have no independent passing revalidation receipt?

## Admissible Options

### OPT-REVALIDATE — authorize fresh independent Plan validation

- Kind: action
- Consequence: consequential routing choice; the validation run itself is
  read-only
- Reversibility: reversible
- Benefit: tests whether the reconciled planning repairs actually close
  `B-DESIGN-001`, which is required before an SWU can be admitted
- Cost/risk: requires a new digest-bound, two-reviewer dispatch, two tension
  checks, exact confirmation, registration, joined receipts, and closeout; it
  may return new blocking findings
- When to choose: when the objective remains implementation and browser proof
- Downstream impact: a pass removes only `B-DESIGN-001`; governance,
  Bootstrap, owner, adapter, and retention gates remain independent

### OPT-DEFER — preserve the blocked Plan

- Kind: defer
- Consequence: non-mutating
- Reversibility: reversible
- Benefit: preserves the authored work without spending review capacity
- Cost/risk: no SWU can be selected and no working or browser-testable version
  can be produced
- When to choose: when implementation is intentionally paused
- Downstream impact: Task Session remains blocked at the same evidence
  fingerprint

### OPT-STOP — stop the add-on objective

- Kind: stop
- Consequence: non-mutating
- Reversibility: reversible only through a later new objective
- Benefit: ends further work and prevents additional coordination cost
- Cost/risk: the untracked planning package remains only authored evidence
- When to choose: when the integration should not continue
- Downstream impact: no revalidation, governance binding, implementation, or
  browser witness

## Rejected Option

`OPT-BYPASS-VALIDATION` is structurally inadmissible. Treating the parent’s
authored reconciliation as independent validation would contradict
`DISTILL-VALIDATION.md`, bypass an authority gate, and inflate the claim beyond
the receipts.

## Recommendation

Choose `OPT-REVALIDATE`. It is the smallest safe next step and matches the
requested implementation outcome. This recommendation is not confirmation.

The private operator profile was consumed only as policy parameters:
reconcile before acting, prefer the smallest reliable testable slice, fail
closed on unknown authority, and gate each mutation separately. The profile
does not supply consent for this consequential route.

## Standing Context Choice

`EXPLAIN` requests more context and does not resolve the gate.

## Remaining Blockers After A Hypothetical Revalidation Pass

- `B-GOV-001`: governing issue and Project 2 acceptance are absent.
- `B-BOOT-001`: no current no-write Bootstrap compatibility receipt.
- `B-OWNER-001`: product and lifecycle owners are not repository-bound.
- `B-ADAPTER-001`: stable public Strategy/Whisper operations are unproven.
- `B-RETENTION-001`: uninstall retention/disposal policy is unresolved.

No product mutation or browser launch is authorized by this decision record.

## Resolution

`OPT-REVALIDATE` was selected. This resolves only the Task Session routing
decision. A fresh review sheet must still pass schema-0.8.0 readiness and both
digest-bound tension checks before its exact human confirmation can authorize
registration or execution.
