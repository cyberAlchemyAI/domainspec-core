# EXECUTION-CONTRACT-PROFILE-001

- Owner: WP-ORRI-001 execution caller
- Classification: blocker
- Status: BLOCK — no option selected
- Recorded at: 2026-08-25T21:13:00Z
- Consequential work blocked: execution-contract projection, chain/supervisor admission, Task Session entry, and every WP-ORRI-001 SWU
- Projection evidence: `governance-repair/EXECUTION-CONTRACT-PROJECTION-COVERAGE-RECEIPT.json` (`sha256:7c18009bea9c3d911f208f8c15f454390e1489e790cf1b9b1ca248726e299599`)
- Admissibility request: `admissibility-request.json` (`sha256:7f78f13bd7b27f2eac1e97a399ead6d07f1f1e1431f6d5d2fc6c446bd2545a75`)
- Admissibility receipt: `admissibility-receipt.json` (`sha256:5c3d65107079ef4be813793392076af633baf285f43e2f0336f285c01a89dd74`)
- Canonical prefilter result: `gate`; A, B, C, and D are structurally admissible; none is selected or executed.

## Decision question

How should WP-ORRI-001 resolve the accepted plan's mechanically incomplete mapping to the public Task Session execution-contract profile?

## A — Regenerate the accepted plan in the supported wrapper profile (recommended)

- Kind: action
- Benefit: uses the already supported selected-unit execution-contract wrapper and keeps ORRI-specific semantics inside the private accepted plan.
- Cost/risk: produces a new candidate; the 36-artifact accepted set must be regenerated, independently revalidated, and receive renewed exact owner acceptance before execution.
- Choose when: the goal is to unblock WP-ORRI-001 with the smallest public-surface change.
- Downstream impact: repeat refinement/readiness/acceptance, then rebuild projection and chain/supervisor preflight from the newly accepted bytes.
- Reversibility: reversible before acceptance/apply.
- Hazard: authority.
- Owning gate: `wp-orri-plan-owner:exact-candidate-acceptance-renewal`.

## B — Design and accept a public project-agnostic adapter profile

- Kind: action
- Benefit: creates an explicit reusable semantic bridge for closure-style plans beyond ORRI.
- Cost/risk: larger Spellcraft/public-contract surface; gate, terminal, lifecycle-owner, write-order, inventory, validation, and continuation semantics must be designed rather than inferred.
- Choose when: multiple projects demonstrably require this source profile and the public abstraction is worth owning.
- Downstream impact: separately design, test, review, and accept the public profile; then build the run-local projection and rerun admission without adding private ORRI semantics to Arcanum.
- Reversibility: reversible before public acceptance/apply.
- Hazard: authority.
- Owning gate: `arcanum-public-contract-owner:adapter-semantics-and-profile-acceptance`.

## C — Defer

- Kind: defer
- Benefit: preserves every accepted byte and the current safe state.
- Cost/risk: WP-ORRI-001 remains blocked with all nine SWUs unexecuted.
- Choose when: neither plan regeneration nor public adapter design should start now.
- Downstream impact: none; resume only through a later explicit decision.

## D — Stop

- Kind: stop
- Benefit: terminates the current execution attempt cleanly without semantic invention.
- Cost/risk: the work pack remains accepted-planning evidence only, not execution-admitted or implemented.
- Choose when: WP-ORRI-001 execution is no longer desired.
- Downstream impact: no continuation in this run.

## Explain / more context (standing, non-committal)

`Explain` remains available. It has decision effect `none`; if requested, present aligned low-, medium-, and complex examples for A and B, then re-present this same A/B/C/D gate without selecting an option.

## Decision state

- Selected option: none
- Rationale: full public-field coverage is not mechanically complete, and the caller has not selected a semantic repair route.
- Source of decision: pending explicit human-owner selection.
- Remaining blocker: `EXECUTION_CONTRACT_SOURCE_PROFILE_UNSUPPORTED` / `GATE_CONTRACT_MAPPING_ABSENT`.
- Assumptions: none.
- Authority effect: none.
