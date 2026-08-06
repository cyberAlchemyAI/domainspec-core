---
module: wavedb-craft-projection-experiment
version: current
status: candidate
updatedAt: 2026-08-04
docType: implementation-layering
---

# Implementation Layering: WaveDB Craft Projection Experiment

## Purpose

Keep the first layer a reversible, candidate-local trust test and prevent a
passing projection experiment from silently becoming a canonical runtime,
writer, release, or durability claim.

## Target and scope

- Target: candidate-local WaveDB projection of one synthetic Craft ledger
- Scope: research-to-experiment infrastructure
- Current state: Design complete; exact npm/source provenance currently blocked;
  no native package installed or loaded

## Layer decision table

| Layer | Decision question | Minimum working unit | Included | Deferred | Exit evidence | Promotion decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether one exact WaveDB artifact can safely hold and fail-closed query a complete disposable projection of one frozen Craft fixture. | Provenance gate, frozen codec, one isolated adapter, exact normal path, iterator observation, negative controls, rebuild, bounded receipt | WP-0 through WP-6 as atomic SWUs; single platform; synthetic data; isolated stores | platform matrix, multiwriter, power loss, migration, encryption lifecycle, publication | exact Task Session receipts for every SWU and zero unresolved L0 oracle | continue to owner review, pivot, or stop |
| L1 | After this layer, we know whether the projection behavior is repeatable across declared supported platforms and repeated clean runs. | repeated full L0 regime on an approved matrix | reproducibility, build matrix, repeated pass streak | canonical adoption, dual write, power durability | platform-specific immutable run bundles | harden, narrow, or stop |
| L2 | After this layer, we know whether owned reliability and governance protocols hold. | first-party fault seam plus lease/CAS/recovery contracts | true mid-apply witness, process ownership, security lifecycle | scale and distribution | owner-approved degraded-mode, recovery, and governance receipts | consider integration proposal or stop |
| L3 | After this layer, we know whether packaging/distribution or scale claims are credible. | publication-ready package closure or representative scale harness | SBOM/license, supported matrix, release controls, declared performance thresholds | canonical Craft replacement remains separate | publication/release/scale owner evidence | publish candidate, defer, or reject |

## Active layer boundary

After L0, we know only whether the bounded candidate projection works on this
exact environment and fixture. We do not know that it is portable, durable
under power loss, safe for multiple writers, migratable, publishable, or fit to
replace Craft storage.

## Non-regression guardrails

- YAML authority, fresh admission, full key enumeration, zero-output failures,
  external-only receipts, and no database-to-YAML path survive every later
  layer.
- Later layers require new owner decisions; passing L0 cannot auto-promote.
- Any new active pointer, writer, migration, encryption, deployment, package,
  performance, or durability claim invalidates the current layer identity.
- All destructive tests remain scoped to exact isolated copies.

## Recommended next layer

- Next layer: L0
- First unit: `SWU-WCP-001`, exact package/source provenance decision
- Current decision: expected `stop` unless a single non-contradictory mapping is
  proven
- Major deferral: everything in L1-L3 and every HOLD/KILL item in the research
  verdict
