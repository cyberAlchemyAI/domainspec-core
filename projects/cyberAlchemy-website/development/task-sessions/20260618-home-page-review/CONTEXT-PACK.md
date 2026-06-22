# Context Pack: SWU-CAW-CONTENT-003 Home Page Review

Task session: `20260618-home-page-review`

SWU: `SWU-CAW-CONTENT-003`

Objective: review the CyberAlchemy Home page draft against source, boundary,
proof, visitor clarity, tone, and CTA gates. Return a `pass`, `flag`, or `block`
verdict with reasons.

## Scope

In scope:

- review `projects/cyberAlchemy-website/content/drafts/home.md`
- produce review evidence with pass/flag/block reasons
- preserve exact source references for any finding
- decide whether the draft is ready for acceptance, needs revision, or must be
  blocked

Out of scope:

- rewriting the Home draft
- accepting the draft as final website copy
- implementing website pages
- drafting other pages
- rendering interactive review HTML

## Selected Sources

| Source | Selectors | Obligations covered |
| --- | --- | --- |
| `projects/cyberAlchemy-website/content/drafts/home.md` | claim map lines 47-56; public draft lines 58-144; review notes lines 146-153 | review target, claim map, public body, draft self-declared boundaries |
| `projects/cyberAlchemy-website/content/page-contracts/home.md` | role/readership lines 9-23; source anchors lines 41-78; authority/status lines 80-108; allowed/forbidden lines 110-134; body/gate lines 144-214 | Home contract gates and acceptance constraints |
| `projects/cyberAlchemy-website/research/2026-06-17-content-inventory/findings.md` | editorial law lines 7-28; authority/status lines 30-52; Home matrix lines 56-60; Home sitemap lines 81-95; gates lines 204-230 | claim <= proof, public-boundary, visitor clarity, status labels |
| `projects/cyberAlchemy-website/whisper-presets/cyberalchemy-site-page.md` | required body parts lines 56-62; CTA policy lines 73-81; reader state lines 120-132; gate lines 202-236 | Whisper review rules and flag/block thresholds |
| `projects/cyberAlchemy-website/development/invoke-runs/20260618-content-production-route/INVOKE-CONTENT-ROUTE.md` | route lines 22-33; Home route lines 57-82; L0 acceptance lines 207-222 | SWU-003 acceptance evidence |
| `arcanum/framework/CYBERALCHEMY-METHOD.md` | method purpose lines 3-9; five anchors lines 11-25; thesis lines 27-43; synthesis lines 96-123 | canonical source support for method claims |
| `arcanum/docs/index.html` | public hero/method lines 440-477 | public documentation support for named workflows, governed artifacts, evidence language |

## Obligations

1. Verify every load-bearing claim has a source anchor, authority type, claim
   type, and `Built`/`Designed`/`Planned`/`Open` status.
2. Verify public copy does not include local paths, private project names,
   private session residue, raw dispatch detail, owner handoffs, token budgets,
   unaudited PDF/HTML factual authority, or over-strong runtime/security claims.
3. Verify Home remains a `public-offer` page with `method-doctrine` support, not
   an architecture-first or internal-proof page.
4. Verify the page is understandable without prior Arcanum or DomainSpec
   vocabulary.
5. Verify CTAs match the Home page role and keep pilot/demo language as planned
   offer, not proof.
6. Return one verdict: `pass`, `flag`, or `block`.

## Decision Pack

No blocker-level decision was found. The review format was treated as a safe
implementation assumption:

- selected format: Markdown review artifact
- rationale: the SWU acceptance evidence requires a verdict with reasons; the
  interactive Whisper review HTML is useful later but not necessary for this
  gate
- downstream impact: later review or implementation work can still render HTML
  from the Markdown review if needed

## Gate Check Before Mutation

- Draft exists: pass
- Home contract exists: pass
- Evidence bundle exists: pass
- Review write scope is limited to review/session artifacts: pass
- No runtime handoff requested: n/a
- No subagents requested: n/a

## Completion Criteria

- `projects/cyberAlchemy-website/content/reviews/home-review.md` exists.
- Review artifact names the verdict and reasons.
- Review artifact distinguishes pass, flag, and block findings.
- Task-session report records validation commands and next route.
