# Refine Seed Proposal - Auth User Management Strava Foundation

- Run id: `20260621T025133Z-auth-strava-foundation`
- Dispatch id: `refine-20260621-auth-strava-foundation`
- Owner: `refine`
- Date: 2026-06-21
- Preset: `standard`
- Research mode: `research-if-gap-appears`

## Target

`projects/auth-user-management`, a reusable private auth/user-management
foundation that can be copied into later projects. Body War is the first
intended consumer: login, auth/session, user identity, and Strava connection
before track geometry or game mechanics.

## Refinement Objective

Turn the operator's auth-first pivot into a production-ready, non-executed
plan:

1. Define the reusable auth/user-management package boundary.
2. Decide the first production session transport profile.
3. Map `validation/poker-team` auth-access-control into reusable domain,
   use-case, permission, token, session, and validation expectations.
4. Map the useful Savvy cookie/session proof into browser-session and CSRF
   expectations while excluding mock/client-auth weaknesses.
5. Define Strava as the first provider connection adapter for Body War.
6. Produce a copy/adoption checklist that later projects can use without
   inheriting Body War or Savvy-specific assumptions.

## Source Context

- `validation/poker-team` has an implemented auth-access-control DomainSpec,
  use cases, token/session entities, login, logout, token introspection,
  authentication, authorization, role definitions, tests, and observability.
- `projects/savvy_legal-studio-ai` has browser cookie/session guard evidence in
  `lib/auth/savvy-auth.ts` and tests, but earlier production-readiness findings
  warn against client-supplied `authStatus`, mock 2FA, and localStorage session
  persistence.
- `projects/body-war` already has an active Strava evidence blocker. The new
  priority is to establish login/auth and Strava connection first; track
  geometry and game mechanics are intentionally deferred.

## Write Scope

This strategy packet writes only under:

`projects/auth-user-management/`

Read-only references:

- `validation/poker-team/`
- `projects/savvy_legal-studio-ai/`
- `projects/body-war/`

No app runtime code is changed by this refine strategy proposal.

## Done Criteria

- A validated `REFINE-DISPATCH.json` exists before runtime-backed stage
  execution.
- The final design distinguishes reusable core, app adapter, storage adapter,
  provider adapter, migrations, tests, and adoption docs.
- The first session transport decision is explicit and threat-modelled.
- Strava provider connection includes OAuth state/PKCE, callback, token custody,
  refresh/revocation, scope minimization, redacted audit, and fixture tests.
- Body War receives a first-consumer handoff for login and Strava connection.
- Track geometry and game mechanics remain out of scope for the first
  implementation route.

## Validation Surface

- `dispatch-spec` route validation for this refine packet.
- Markdown and JSON parse checks for the run artifacts.
- Evidence references must remain local paths and must not copy private
  submodule content into public Arcanum surfaces.
- Follow-up implementation must prove deny-by-default behavior, session expiry,
  revocation, CSRF for unsafe browser calls, permission denial, Strava callback
  state validation, token redaction, and logout/revocation.

## Planned Stage Configuration

| # | Stage | Capability | Mode |
|---|-------|------------|------|
| 1 | Context baseline | `context-builder` | `standard` |
| 2 | Invoke Define | `invoke` | `define` |
| 3 | Interrogation | `interrogation` | `refine-review` |
| 4 | Research decision | `refine` | `research-if-gap-appears` |
| 5 | Distill | `distill` | `standard` |
| 6 | Invoke Redefine / Design | `invoke` | `design` |
| 7 | Interrogation | `interrogation` | `refine-design-review` |
| 8 | Distill Repair | `distill` | `validate` |
| 9 | Invoke Plan | `invoke` | `plan` |
| 10 | Final Interrogation + Synthesis | `interrogation` -> `refine` | `refine-final` |

## Selected Technique Overlays

- `baseline_sequence` - canonical ten-stage refine loop with explicit
  handoffs, validation, owner boundaries, and observability.
- `route_menu_for_auth_boundary` - several session/auth packaging choices are
  plausible and need an explicit decision.
- `xray_for_hidden_structure` - auth hides identity, session, token,
  permission, provider-link, storage, browser, and audit components.
- `protected_context_for_sensitive_auth_evidence` - OAuth secrets, Strava
  tokens, private validation evidence, and prior Savvy security findings must
  stay bounded to private context.
- `memory_residue_for_context_recovery` - prior Body War and Savvy planning
  evidence should inform the run without becoming implementation proof.
