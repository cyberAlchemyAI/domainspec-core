# Distill Result

Stage: `s05-distill-gap-unit`
Owner: `distill`
Status: `pass`
Mode: `standard`

## Target Context

BodyWar auth integration gap/blocker review before mutation-capable
`task-session` execution.

## Objective And Output Artifact

Objective: select the smallest coherent blocker-repair unit that can start now.

Output artifact: this Distill stage receipt and final Refine synthesis input.

## Mode And Budget

`standard`: one proposal track, Proposer/Balancer role simulation, two
reduction rounds.

## Role Conversation Trace

| Role | Claim Or Objection | Reconciliation |
| --- | --- | --- |
| Proposer | Start with `SWU-BWAUTH-001`, adding generic trusted-session support to the auth package. | Accepted. It repairs the package contract without touching BodyWar browser/OAuth details. |
| Balancer | The BodyWar app still does not compile, so perhaps `SWU-BWAUTH-003` is the real first unit. | Rejected as first unit because `SWU-BWAUTH-003` depends on the package use case and BodyWar schema path. |
| Balancer | VPS/Strava/friend blockers could block all work. | Rejected for L0/L1 local integration; accepted for L3 online proof. |

## Current Smallest Coherent Unit

`SWU-BWAUTH-001`: add generic trusted-session support to the auth package.

Responsibility: enable a consumer that has already proven an external identity
to create an auth session/token without embedding OAuth, cookies, Strava, or UI
logic in the reusable package.

## Optimization Point

This unit is small enough to execute without deployment, real Strava credentials,
friend activity evidence, DNS, or VPS access. It is large enough to recompose
into BodyWar OAuth callback handling, browser session creation, profile routes,
and local E2E.

## Concept Layer Map

```text
Production online TROQAR auth proof
  -> Local BodyWar auth/profile integration
    -> BodyWar-owned browser and Strava adapters
      -> Auth package generic trusted-session use case
```

## Closure And Recomposition Proof

Closure:

- owns one package use case and exports;
- can be verified with auth package check/validate;
- does not require BodyWar routes, cookies, Strava gateway, or database profile
  tables.

Recomposition:

- `SWU-BWAUTH-003` uses the package session/token use case through BodyWar
  browser session adapter;
- `SWU-BWAUTH-004` creates trusted sessions after Strava identity proof;
- `SWU-BWAUTH-005` uses the session/profile state for route wiring;
- `SWU-BWAUTH-006` proves local Docker-backed E2E;
- `SWU-BWAUTH-007` syncs docs and deploy readiness.

## Tension Ledger

| Tension | Status | Route |
| --- | --- | --- |
| Package reuse versus BodyWar-specific OAuth/browser behavior | resolved | package gets only generic trusted session; BodyWar owns adapters |
| Current app compile failure versus first SWU start | resolved | compile failure is planned residue, not a pre-SWU blocker |
| Local proof versus online production proof | unresolved for L3 | existing VPS decision gate |
| Activity summary versus Taquaral geometry/scoring authority | unresolved for game proof | active Craft gap |

## Next Route

`invoke design-review`

## Receipt

```yaml
run_id: 20260621T141252Z-auth-integration-gap-blocker-refine
session_id: session-20260621T141252Z
capability_ref: distill
receipt_kind: native-stage
artifact: stages/05-distill-gap-unit.md
status: pass
validation_result: SWU-BWAUTH-001 selected as smallest coherent executable unit
blockers:
  - none for selected unit
handoff_note: Review design against the selected package/BodyWar boundary.
```
