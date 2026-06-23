# TROQAR UI Visual Discipline

Status: active-pattern
Steward: body-war / ui-prototyping-studio
Scope: PRIVATE (umbrella root only - TROQAR and BodyWar product surfaces)

## Purpose

Govern the TROQAR visual and interaction practice across BodyWar app source,
DomainSpec UI docs, and UI Prototyping Studio handoffs, so prototype variants
and production pages keep the same dark athletic identity, Strava-first login
posture, privacy copy, and logo system.

## Boundary

This discipline names the private TROQAR UI discipline. It does not own:

- BodyWar production source mutations or browser validation,
- canonical DomainSpec UI architecture rules,
- UI Prototyping Studio session state or handoff acceptance,
- final trademark artwork, brand registration, or marketing collateral,
- future deterministic validators or constitutions.

Production implementation routes through BodyWar task sessions. Studio
consumption routes through the Studio prototype gate profile. Enforcement beyond
prose review should route to a validator or constitution owned by the relevant
capability; this card only names the practice and its current evidence.

## Evidence

- [Visual definitions](../../projects/body-war/docs/features/troqar-product-architecture/VISUAL-DEFINITIONS.md) - the BodyWar feature-level visual contract for palette, typography, composition, and component rules.
- [UI specification](../../projects/body-war/docs/features/troqar-product-architecture/UI-SPEC.md) - maps the authenticated runner profile, Strava-only MVP login, privacy copy, and stable selectors.
- [Studio prototype handoff](../../projects/body-war/docs/features/troqar-product-architecture/prototype-handoff/STUDIO-PROTOTYPE-HANDOFF.md) - proves Studio handoff evidence is already consumed by BodyWar implementation and tests.
- [Studio export profile](../../projects/ui-prototyping-studio/development/prototype-gate/troqar-product-architecture/export-profile.json) - the Studio-facing profile that passes TROQAR source refs into handoff export.
- [Studio TROQAR UI guidelines](../../projects/ui-prototyping-studio/development/prototype-gate/troqar-product-architecture/troqar-ui-guidelines.json) - machine-readable visual discipline for future Studio prototype work.
- [Production UI login refine result](../../projects/body-war/development/refinement-runs/20260622T083402Z-troqar-production-ui-login-refine/RESULT.md) - narrows the first production page to Strava-only login and Studio-first visual hardening.

## Validation

- Mode: mixed
- Check: JSON profile parses with `python3 -m json.tool`, private discipline card/catalog prose review, and future Playwright visual checks against the real BodyWar app.
- Latest result: pass (this session: Studio guideline JSON parsed; targeted local link/reference checks passed; the private catalog has no dedicated validator yet).

## Quality Bar

A useful TROQAR UI entry must:

- preserve the dark asphalt app shell, not a white admin dashboard;
- use fire-orange for primary running/action energy and territory-green for control, connection, success, and owned-territory state;
- keep the two-accent palette balanced instead of drifting into orange-only, green-only, purple SaaS, beige, or slate dashboard themes;
- use condensed athletic display typography for TROQAR headings and DM Sans-like body text for readable app copy;
- carry the hex runner mark, split orange/green wordmark, and `CORRA. CONECTE. CONQUISTE.` tagline rules;
- make the first screen mobile-first, app-like, and login-ready with Strava as the only visible MVP authentication method;
- preserve privacy and evidence caveats: no access tokens, no raw provider payloads, no verified-geometry claims until the backend proves them;
- keep Studio handoff selectors stable with the BodyWar `data-od-id` contract.

## Promotion Guardrail

This discipline can recommend a Studio template, Playwright visual checks, or a
future UI constitution, but it cannot promote BodyWar product copy, Studio
handoff state, brand assets, registry entries, ontology, glossary, sigil, or
spell knowledge. Promotion beyond `active-pattern` requires a named validation
surface, a mutation boundary for brand assets, and evidence from at least one
fresh Studio-to-production cycle.
