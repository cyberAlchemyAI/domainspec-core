# Asset Ownership Propagation Discipline

Status: active-pattern
Steward: ops
Scope: PRIVATE (umbrella root only)

## Purpose

Govern asset classes across the 3-repo topology with a single source of truth per asset and explicit pointer-propagation rules, so a generated/copied asset never silently diverges from its canonical owner.

## Boundary

Names the asset-ownership/propagation practice. It does not own the asset content itself, per-repo build tooling, or the submodule commit ordering (the [submodule-orchestration discipline](submodule-orchestration.md) owns that).

## Evidence

- [ops/ASSET-OWNERSHIP-POLICY.md](../../ops/ASSET-OWNERSHIP-POLICY.md) - the asset-class / source-of-truth / propagation policy.
- [tools/check_github_drift.sh](../../tools/check_github_drift.sh) - the drift checker that fails until mismatches resolve (the de-facto validator).

## Validation

- Mode: validator
- Check: `tools/check_github_drift.sh` (deterministic drift detection).
- Latest result: not-run (validator exists; not executed this session)
- Promotion (2026-06-21, exec #5): candidate -> active-pattern — used by active ops capability with a real validator (check_github_drift.sh) + policy doc as cross-capability evidence (satisfies the v0.2.1 active-pattern evidence rule). Canonical still gated on running the validator in CI.

## Quality Bar

A useful entry must: name each asset class and its single source of truth, define the propagation rule, cite the drift checker as its validator, and keep the practice private to the umbrella.

## Promotion Guardrail

Can recommend promoting the drift checker to the named validator; cannot promote any asset, registry, ontology, glossary, sigil, or spell. Candidate until each asset class maps to one source of truth with the checker enforcing it.
