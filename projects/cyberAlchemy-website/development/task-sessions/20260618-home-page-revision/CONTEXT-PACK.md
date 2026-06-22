# Context Pack: SWU-CAW-CONTENT-003R Home Page Revision

Task session: `20260618-home-page-revision`

SWU: `SWU-CAW-CONTENT-003R`

Objective: revise the CyberAlchemy Home draft narrowly using the
`SWU-CAW-CONTENT-003` review findings, then rerun the Home review gate.

## Scope

In scope:

- edit `projects/cyberAlchemy-website/content/drafts/home.md`
- address the four flag findings from
  `projects/cyberAlchemy-website/content/reviews/home-review.md`
- rerun source/boundary/proof/visitor-clarity checks
- write a new review verdict for the revised draft
- write a task-session report

Out of scope:

- website implementation
- drafting Method, Trust, How It Works, Examples, Architecture, or guide pages
- changing source inventory, strategy, or public `arcanum` files
- promoting any claim to operating implementation
- adding private examples or unaudited PDF/HTML factual claims

## Selected Sources

| Source | Selectors | Obligations covered |
| --- | --- | --- |
| `projects/cyberAlchemy-website/content/reviews/home-review.md` | F1 lines 42-72; F2 lines 74-98; F3 lines 99-123; F4 lines 125-144; acceptance recommendation lines 170-182 | revision requirements |
| `projects/cyberAlchemy-website/content/drafts/home.md` | claim map lines 47-56; public draft lines 58-144 | mutation target |
| `projects/cyberAlchemy-website/content/page-contracts/home.md` | target public lines 13-23; allowed/forbidden lines 110-134; body/gates lines 144-214 | Home contract limits |
| `projects/cyberAlchemy-website/research/2026-06-17-content-inventory/findings.md` | editorial law lines 7-28; Home matrix lines 56-60; Home sitemap lines 81-95; preset gates lines 204-230 | claim <= proof and visitor clarity rules |
| `projects/cyberAlchemy-website/whisper-presets/cyberalchemy-site-page.md` | body parts lines 56-62; CTA policy lines 73-81; reader state lines 120-132; gate lines 202-236 | Whisper review gates |
| `arcanum/framework/CYBERALCHEMY-METHOD.md` | purpose lines 3-9; anchors lines 11-25; thesis lines 27-43; synthesis lines 96-123 | canonical support for revised examples |
| `arcanum/docs/index.html` | public framing lines 440-477 | public support for named workflows, governed artifacts, and evidence language |

## Obligations

1. Replace or soften internal artifact vocabulary in `What Changes`.
2. Add claim-map coverage for revised example output shapes, or keep examples so
   generic that they are not load-bearing product claims.
3. Add a plain audience sentence naming builders, founders, research teams, and
   careful adopters.
4. Ground the bounded pilot CTA in one concrete deliverable while preserving
   `Planned` status.
5. Preserve all prior pass gates: source anchors, authority types, claim types,
   status labels, no private residue, no `Built` claims, no runtime/security
   guarantee, no architecture-first Home copy.

## Decision Pack

No blocker-level decision was found.

Implementation assumptions:

- Mutate the existing Home draft instead of creating a parallel duplicate,
  because the review requested a narrow revision to the draft itself.
- Add one claim-map row for revised example output shapes to preserve the
  claim-map discipline even after softening the examples.
- Treat the rerun review as Markdown evidence, not interactive review HTML.

## Gate Check Before Mutation

- Review artifact exists: pass
- Draft exists: pass
- Home contract exists: pass
- Required source anchors exist: pass
- Write scope limited to Home draft, review, and session evidence: pass
- No runtime handoff requested: n/a
- No subagents requested: n/a

## Completion Criteria

- `projects/cyberAlchemy-website/content/drafts/home.md` addresses F1-F4.
- `projects/cyberAlchemy-website/content/reviews/home-review-003R.md` exists.
- Rerun review verdict is recorded.
- Task-session report records changed files and validation commands.
