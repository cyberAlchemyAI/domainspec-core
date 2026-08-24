---
module: wavedb-pinned-npm-diagnostic
version: candidate-local-1
status: active-l0
updatedAt: 2026-08-05
docType: implementation-layering
---

# Implementation Layering: WaveDB pinned npm diagnostic

## Target and scope

- Target: exact `@vijayee/wavedb@0.15.8` registry artifact.
- Scope: candidate-local runtime research.
- Current state: exact source provenance blocked; source builds load but stall
  in concurrent writes; npm artifact is untested.

## Layer decision table

| Layer | Decision question | Minimum working unit | Included | Deferred | Exit evidence | Promotion |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether the pinned npm artifact installs, loads, and passes the named local canaries under Node 26. | one integrity-bound isolated install and black-box test run | metadata, tarball integrity, install/build, addon identity/load, basic, empty-value, batch/reopen, concurrent writes | Craft, source binding, other platforms, performance | terminal Task Session receipt | stop on any failure; offer a separate Craft prototype decision only on pass |
| L1 | After this layer, we know whether the L0 result is repeatable. | second fresh attempt with identical inputs | clean repeatability and residue comparison | support matrix | two passing immutable receipts | harden or stop |
| L2 | After this layer, we know whether package/security governance is acceptable. | package, license, dependency, vulnerability, and provenance-owner review | SBOM/security/provenance policy | rollout and packaging | owner receipts | approve bounded internal use or reject |
| L3 | After this layer, we know whether a Craft-side package/runtime posture is supportable. | separately designed Craft adapter/package proof | platform matrix, packaging, recovery, release controls | production scale | Craft/package/release receipts | pilot, package, or defer |

## Non-regression guardrails

- A tarball verdict never becomes exact Git-source provenance.
- A passing addon canary never becomes Craft compatibility or production proof.
- Later work must preserve the exact tarball integrity and terminal evidence.
- No layer changes Craft authority or writes into either Craft tree implicitly.

Recommended next layer: L0 only. Major deferred scope: Craft integration and
all promotion/publication/deployment decisions.
