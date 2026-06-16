# Refine Result — Decentralized Living Library Architecture

- Run id: `2026-06-15-arch-refine` · Dispatch id: `refine-2026-06-15-arch-refine`
- Target: `projects/alpha-grant/decentralized-living-library-summary.md`
- Status: **pass** (one operator decision surfaced, not blocking)
- Preset: `standard` · Research: `no-research` (local-first held)
- Owner: `refine` · Synthesized from stage artifacts (gate g9 satisfied)

## What the refinement produced

The initial *prose* architecture became an explicit **spine-and-extensions
architecture** with an ownership/authority graph and structural boundary gates.

### 1. A keystone, not a flat list of seven lanes

The seven lanes collapse to **one spine + extensions**. The spine is **N1
Library** (the mission-locked public collection) funded by **A1 Bridge +
A2 Infrastructure**, living in one **entity-home**. Everything else attaches.
This replaces "seven parallel fundable lanes" with "one keystone the rest hang
from" — which also matches the source's own #1 risk (entity confusion) and its
recommended first move.

### 2. Authority separated from ownership (the decisive fix)

The single most important structural change: **N5 Funding-OS (Inklovich / FIT
Farms / Golden Quill) holds coordination authority but never owns public assets,
never directs the N1 board, and never binds a partner or pitches a funder without
N1 sign-off.** Operational involvement is a written service contract, not title.
This is what keeps the public-benefit thesis fundable and un-commingled (O4).

### 3. The entity-home fork is now an approvable decision

The source deferred the entity-home to a 90-day step; the refinement makes it the
**keystone gate (g7)** with a bounded menu and a converged recommendation:
**fiscal sponsor now → new nonprofit as the bridge-funded destination**, with
FIT Farms as operator-by-contract and the co-op as an extension home only.
Both dialectic roles (public-benefit advocate, funding-pragmatist) converged here.

### 4. Boundaries are encoded, not just warned

O1–O6 each attach to a specific node/asset/ask with a named owner and a
fail-action: **O2 (unverified partners), O4 (commingling), O6 (funder exposure)
are blocking**; O1/O3/O5 flag. A `verification_status` field gates any partner
name in any outward ask.

### 5. Extensions recompose through three connectors

Every extension lane plugs in via (C1) shared accession/verification standard,
(C2) declared asset-ownership lane, (C3) entity-home relationship. Tested against
the hardest lane (Houston) — recomposes O3-safe via MTA. A lane that can't
declare all three is flagged.

## Stage evidence

| Stage | Capability | Status | Artifact |
|-------|-----------|--------|----------|
| Context baseline | context-builder | pass | stages/s1-context-builder/context-pack.md |
| Invoke Define | invoke | pass | stages/s2-invoke-define/DEFINE.md |
| Interrogation refine-review | interrogation | flag | stages/s3-interrogation-define/REVIEW.md |
| Research decision | refine | pass (no-research) | stages/s4-research-decision/RESEARCH-DECISION.md |
| Distill | distill | pass | stages/s5-distill/DISTILL.md |
| Invoke Redefine / Design | invoke (+4 subagents) | pass | stages/s6-invoke-design/DESIGN.md |
| Interrogation refine-design-review | interrogation | flag | stages/s7-interrogation-design/DESIGN-REVIEW.md |
| Distill Repair | distill | pass | stages/s8-distill-repair/REPAIR.md |
| Invoke Plan | invoke | pass | stages/s9-invoke-plan/PLAN.md |
| Final Interrogation + Synthesis | interrogation → refine | pass | stages/s10-final/FINAL-REVIEW.md + this file |

Subagent receipts (Design stage): structure-mapper `pass`, public-benefit-advocate
`pass`, funding-pragmatist `pass`, boundary-auditor `pass` — all joined via
parent_synthesis.

## The one decision this surfaces for you

**Approve the entity-home route** (gate g7): the recommended staged route is
`fiscal-sponsor` now → `new-nonprofit` (bridge-funded). Until you approve it, no
ask is drafted and no funder is contacted (Z1 guard). This is the single action
that unblocks the whole plan.

## Open residue (carried with owners, none silently promoted)

- **Z1 outreach timing** → converted to a guarded default (prepare in parallel;
  no funder contact before g7 + verification ≥ written).
- **Z2 endowment timing** → deferred post-spine (N1 board + N5).
- **Z3 contribution threshold** for private→public material → N1 board via
  service-agreement template.

## Recommended next routes (not executed by refine)

1. **Decision-gate** on the entity-home route (g7) — resolve the one blocker
   before planning continues.
2. **Task-session** to author the Phase-1 governance substrate (accession
   standard + verification-status field + partner-permission/claims sheet) once
   the entity-home is approved.
3. Optional **bounded research** later, *only* if a specific funder-eligibility
   fact is needed — never to assert partner commitments or KU/INVAM status.

## Final synthesis (one line)

The Decentralized Living Library is strongest as a **single mission-locked
collection spine, owned separately from its operator and its commercial IP, with
boundaries encoded as gates and extensions that recompose through three
connectors — pending one operator decision: the entity-home route.**
