# Worktree Cleanup Publication Strategy

Date: 2026-08-25
Status: pending owner decision
Decision ID: `DG-WORKTREE-CLEANUP-20260825`

## Question

How should the remaining red or admission-sensitive DomainSpec-core work be preserved while completing the requested worktree cleanup?

## Current evidence

- Arcanum `main` is validated, clean, and pushed at `b07a03d95e4c8bd4d98c05a8eb2916ad7f8341d9`.
- xDivina `main` is clean and pushed at `21d61135fec6f2a5d50a34c9317a2100bcfed412`; its explicitly reverted agent-control feature remains on a separate branch.
- DomainSpec v2 validation has 17 remaining failures: 14 admission-sensitive minted-profile failures, one immutable SFOL-baseline failure, and two Saga-classification failures covering 315 unclassified files.
- Cyberalchemy-orchestrator has a repaired validator invocation defect, but real source/digest drift remains and four runtime abuse tests expose removed fail-closed handoff checks.
- A redundant, clean `domainspec-commercialization` worktree was removed only after proving it had zero unique commits; its branch remains.

## Options

### LOCAL-WIP-PRESERVATION — recommended

Commit the blocked bundles to clearly named local WIP branches, do not push or promote them, restore default branches to validated bytes, and finish the safe parent gitlink publication.

- Benefit: produces clean worktrees while preserving every byte and every gate.
- Cost or risk: blocked work is local-only until later exact publication authority.
- Choose when: repository cleanliness is urgent but semantic admission work should remain separate.
- Downstream impact: later work can resume from exact WIP commits without treating them as master-ready.

### CONTINUE-RECONCILIATION

Continue the profile compatibility decision, SFOL versioning, Saga classifications, RWO ontology rebinding, and runtime handoff reconciliation until every default-branch gate passes.

- Benefit: aims for a genuinely master-ready integration rather than parking work.
- Cost or risk: materially larger scope and additional owner gates; it will not be a quick Git cleanup.
- Choose when: completing the semantic/lifecycle work now matters more than immediate cleanliness.
- Downstream impact: each accepted bundle can then be committed and published in dependency order.

### DEFER-CLEANUP

Leave the remaining worktrees dirty, retain the current validation evidence, and resume later.

- Benefit: no additional mutation or publication.
- Cost or risk: the original cleanup objective remains incomplete.
- Choose when: the owner wants to decide the individual product gates later.

### STOP-CLEANUP

End the cleanup with Arcanum and xDivina completed and all remaining bytes untouched.

- Benefit: clear terminal stop with no inferred decisions.
- Cost or risk: DomainSpec-core and both cyberalchemy-orchestrator worktrees remain dirty.

## Rejected option

`FORCE-ALL-TO-MASTER` is structurally inadmissible: it would publish a profile whose registry says `release_admission: not-granted`, rewrite historical acceptance boundaries, and knowingly merge red fail-closed tests.

## Selection

Pending user choice.

## Remaining blockers

- DomainSpec profile compatibility/admission.
- SFOL historical baseline versioning.
- Classification of 315 Saga-reference files.
- RWO ontology renewed acceptance after validator and source-byte changes.
- RWO sequential-handoff fail-closed behavior.
