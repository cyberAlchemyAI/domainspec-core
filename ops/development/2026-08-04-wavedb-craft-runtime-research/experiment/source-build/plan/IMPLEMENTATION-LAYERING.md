---
module: wavedb-reviewed-source-build
version: candidate-local-1
status: active-l0
updatedAt: 2026-08-04
docType: implementation-layering
---

# Implementation Layering: WaveDB reviewed-source build

## Purpose

Sequence a local source-build proof separately from repeatability, security and
license hardening, and distributable packaging. Only L0 is authorized by this
Work Pack.

## Target and scope

- Target: one hash-bound WaveDB addon built from reviewed commit `01c77e8b...`.
- Scope: candidate-local infrastructure experiment.
- Current state: Design is `design-validator-pass`; no source-build runner or
  admitted local addon exists.

## Layer decision table

| Layer | Decision question | Minimum working unit | Included scope | Deferred scope | Exit evidence | Promotion decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether the reviewed commit can produce one loadable, upstream-tested addon on the observed Linux toolchain. | Deterministic runner plus one isolated source-build attempt | exact source/submodules, lockfile dependencies, generated `c_src`, build, load, upstream tests, canary, scope scan, receipt | repeat build, other platforms, licenses, vulnerabilities, packaging | two Task Session receipts and terminal `source-build-receipt.json` | offer a separate parent Invoke Refresh, or stop |
| L1 | After this layer, we know whether clean source builds repeat on the same declared platform. | two fresh attempt directories with independently equal semantic inputs and passing tests | clean-work repeatability, output comparison, deterministic manifest schema | security policy, cross-platform output equality | two complete receipts and explained binary differences | harden, narrow, or stop |
| L2 | After this layer, we know whether the build route has adequate supply-chain, license, and degraded-mode governance for broader internal use. | dependency SBOM/license/vulnerability review plus failure-path controls | registry policy, dependency closure, toolchain custody, audit logs, cleanup owner | public packaging and platform matrix | owner-reviewed security/license receipts | package internally, remediate, or stop |
| L3 | After this layer, we know whether a distributable package and supported platform matrix are credible. | reproducible release candidate across explicitly supported platforms | release tarball, attestations, CI matrix, support policy, publication checks | production adoption and Craft authority | package/publication owner receipts | publish separately or defer |

## Boundary heuristic

L0 stops when one complete local addon receipt exists because another build
answers repeatability rather than basic feasibility. L1 stops before security
and license ownership. L2 stops before distribution. L3 remains a separately
authorized package lifecycle.

## Non-regression guardrails

- Later layers preserve exact source identity, lockfile-only resolution,
  fail-closed tests, Craft non-access, and separate parent refresh.
- A locally passing addon never becomes npm provenance or publication evidence.
- Each new commit, lockfile, submodule, toolchain, OS, architecture, or OpenSSL
  mode starts a new identity and receipt.
- No layer modifies canonical Craft or a real ledger.

## Recommended next layer

- Next layer: L0.
- Key decision: whether the reviewed source can build and pass its Node tests on
  the currently pinned Linux x86_64 toolchain.
- Major deferred scope: repeatability, platform matrix, licenses/SBOM,
  vulnerabilities, packaging, publication, deployment, and production.
