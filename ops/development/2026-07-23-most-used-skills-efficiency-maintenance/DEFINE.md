# Define: Evidence-Bound Workflow Efficiency Maintenance

Status: approved authoring baseline

Discovery: accepted audit and reflection; no discovery waiver

Implementation status: complete; [terminal audit](work-pack/session-evidence/TASK-WFE-VERIFY/FINAL-AUDIT.md)

## Problem

Six frequently used capabilities carry safety rules, but some rules are only
prose, some validation happens after a costly handoff, some generated runtimes
mix stale copies with local extensions, and some status labels collapse
different proofs. This creates governance theater: humans repeat approval while
machines still admit states that should have failed earlier.

## Objective

Move each falsifiable check to the earliest owner-controlled material boundary,
bind downstream handoffs to machine-verifiable receipts, and retain a human gate
only where it grants consequential authority that deterministic validation
cannot establish.

## Required outcomes

| ID | Required outcome | Accepted source finding |
| --- | --- | --- |
| WFE-R01 | consequential or irreversible choices cannot be auto-selected, and unmet acceptance-critical validation cannot finish as a usable `FLAG` | TS-1 |
| WFE-R02 | routed or reusable mutation admission consumes a current digest-bound readiness receipt while live validation remains | TS-2 |
| WFE-R03 | mutation-capable Invoke handoff proves the material package before emitting a handoff receipt | INV-1 |
| WFE-R04 | Invoke exposes artifact-authored, registry-released, and mutation-runtime-ready as separate ceilings | INV-2 |
| WFE-R05 | dispatch registration rejects new RESERVED rows, orphan closes, working-agent self-approval, and destination escape while preserving history and duplicate-close idempotence | DSS-1 |
| WFE-R06 | dispatch registration binds two tension verdicts and explicit confirmation to the same sheet digest; runtime differences are classified | DSS-2 |
| WFE-R07 | structurally invalid options never reach Decision Gate, and override authority is typed, target-bound, protected, and one-use | DG-1 |
| WFE-R08 | the Inventory machine index, updater, rows, validator, and consumers agree on the supported kind vocabulary | INT-1 |
| WFE-R09 | Inventory checks source, machine, human, derived, and enabled projections bidirectionally for identity, coverage, and freshness | INT-2 |
| WFE-R10 | Whisper runtimes assemble from a current canonical base plus declared local preset overlays and reject undeclared semantic drift | WH-1 |

## Scope

Included:

- current canonical contracts, deterministic validators, negative fixtures, and
  generated runtime composition needed by WFE-R01 through WFE-R10;
- private DomainSpec dispatch tooling and its tests for DSS-1/DSS-2;
- public Arcanum lifecycle changes only through their owning sigil or spell;
- migration of the exact 15 currently invalid Inventory kind values and a
  producer guard that prevents recurrence;
- evidence receipts, observability, and parity checks required to prove each
  change.

Excluded:

- changing the accepted review findings;
- implementing a central workflow-governance framework;
- removing consequential human approval;
- automatic promotion of a spell, sigil, template, Inventory record, or local
  preset;
- DomainSpec v2 product/BTE work;
- cross-repository rollout or public release;
- execution inside Invoke.

## Actors and authority

| Actor/capability | Authority |
| --- | --- |
| Invoke | authors this Define/Design/Plan package only |
| Sigil Development | owns Task Session, Decision Gate, Inventory, and sigil-level Subagents contract revisions |
| Spellcraft | owns Invoke and Whisper spell lifecycle revisions |
| private DomainSpec tooling owner | owns private dispatch appender and adapter behavior |
| Task Session | executes one lifecycle-accepted SWU when its owner routes it |
| validators/fixtures | prove only their declared structural or behavioral axis |
| human maintainer | owns consequential semantic, authority, promotion, and publication decisions |

## Behavioral law

For every accepted change:

```text
current bad state
  -> deterministic negative fixture
  -> earliest owning validator rejects it
  -> lifecycle owner accepts the bounded repair
  -> one SWU mutates only its declared scope
  -> positive and negative controls run
  -> receipt binds artifact, verdict, residue, and next owner
  -> generated/read-model surfaces synchronize without gaining authority
```

An approval receipt cannot repair an invalid package. A validator pass cannot
grant promotion. A generated runtime cannot redefine its canonical base. A
non-authoritative Inventory result cannot establish correctness.

## Decisions

1. The ten findings remain ten independently closable maintenance requests.
2. Shared vocabulary and receipt fields live in this planning package first;
   there is no shared runtime library until repeated implementation proves one
   is necessary.
3. Existing historical dispatch rows remain readable; stricter admission
   applies to new rows.
4. The 15 invalid Inventory kinds are normalized to existing supported kinds by
   path/record role, rather than widening the enum with four redundant aliases.
5. Canonical/generated differences are classified as canonical base,
   runtime metadata, or declared overlay. Blind byte-copy and silent drift are
   both rejected.
6. `SWU-WFE-001` is the first unit because it turns existing Subagents rules
   into machine rejection without changing record shape or public content.

## Acceptance

- Every WFE-R requirement maps to at least one task, SWU, negative control, and
  closure receipt.
- No SWU mixes independently reviewable behavior.
- Every public Arcanum mutation follows submodule-first ownership and generated
  mirrors are synchronized from canonical source.
- Private evidence and tooling remain outside public Arcanum.
- The full route validates with Dispatch Spec.
- Automatic Distill returns pass before any mutation-capable handoff.

## Define-stage trace

- Techniques: `sequence`, `owner_boundary_check`, `residue_ledger`,
  `artifact_contract_bridge`, `concrete_path_evidence`.
- Distill sanity check: pass; the coherent definition is the ten accepted
  evidence-bound changes, not a new universal framework.
- Layering seed: prove admission and false-ready rejection at L0; add receipt
  composition at L1; harden projections at L2; close and package at L3.
- Next route: Design.
