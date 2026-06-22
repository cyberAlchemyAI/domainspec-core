# TROQAR Product Architecture Packet

Status: `draft-pass`
Owner scope: `projects/body-war`
Invoke mode: `define+design`
Craft context: `CTX-BODY-WAR-ROOT`

## Purpose

This packet defines the app-wide TROQAR product architecture above the existing
Parque Taquaral hosted-preview slice. It lists operations and capabilities
first, then derives DomainSpec domain, state, interface, UI/UX, visual, and
backend definitions.

The packet is non-mutating: it does not authorize app implementation by itself.
It makes the next implementation or refinement route context-ready.

## Artifact Order

1. [Operations And Capabilities](OPERATIONS-CAPABILITIES.md)
2. [DomainSpec Feature Spec](SPEC.md)
3. [Domain Model](domain.md)
4. [Operations](operations.md)
5. [Queries](queries.md)
6. [States](states.md)
7. [Interfaces](interfaces.md)
8. [Events](events.md)
9. [Mappings](mappings.md)
10. [Architecture](ARCHITECTURE.md)
11. [UI/UX Spec](ui-spec.md)
12. [Visual Definitions](VISUAL-DEFINITIONS.md)
13. [Backend Spec](backend.md)
14. [Online Auth/Profile Infra Slice](ONLINE-AUTH-PROFILE-INFRA.md)
15. [Gap And Blocker Review](GAP-BLOCKER-REVIEW.md)
16. [Invoke Transport](INVOKE-TRANSPORT.md)

## Source Authority

| Source | Role |
| --- | --- |
| `docs/PROJECT-OVERVIEW.md` | TROQAR identity and audience baseline. |
| `docs/INITIAL-DEFINITIONS.md` | Seed glossary, contexts, entities, rules, and interfaces. |
| `docs/features/game-rules/SPEC.md` | Territory, score, XP, clan, season, and anti-cheat rule baseline. |
| `docs/research/source-notes/troqar-visual-identity.md` | Visual guide and page concept source. |
| `docs/research/source-notes/troqar-gamificacao-jsx.md` | Gamification operations and scoring source. |
| `docs/features/parque-taquaral-online-mvp/` | First executable hosted-preview slice and known blockers. |
| `projects/auth-user-management/` | Current reusable TypeScript core auth boundary. |
| `domainspec/templates/` | Project-local DomainSpec artifact shape. |

## Readiness Boundary

This packet may be used for architecture, UI/UX, backend, and future work-pack
authoring. Runtime mutation still needs a bounded Task Session or work-pack
selection.
