# Revised Candidate Frontend Review Findings

This is the one allowed synthesizer revision after verifier objections. It is
not final until both verifiers return no blocking objection.

## Active Findings

| ID | Artifact | Verified evidence | Severity | Revised fix | Verifier reconciliation |
| --- | --- | --- | --- | --- | --- |
| CAFR-HTML-001 | `projects/co-op-engine/index.html` | “Co-Op Engine — Project Map”; `aria-label="Co-Op Engine home"`; “Page cue”; “project map / live presentation”; “Public review prototype”; Co-Op presentation fallbacks — lines 8, 1372, 1382–1390, 1417, 2194–2202, 2302, 2329 | MAJOR | Fixed requirement: replace browse-visible and accessibility-facing Co-Op/meta identity with a clear CyberAlchemy portfolio identity; preserve operational presentation metadata only when it cannot become visitor copy. | The project corpus remains functional, so CRITICAL is not sustained. This does not require deleting the meeting or presentation capability. |
| CAFR-HTML-002 | `projects/co-op-engine/index.html` | All fourteen offers target `#join`; the shared region only copies text; no email or LinkedIn link exists — lines 1541–2100, 2153–2165, 2260–2264, 2352–2360 | MAJOR | Fixed requirement: provide one shared, progressively enhanced contact region containing exact static base email and LinkedIn links; every card must reach static visible project context there without JavaScript. | Contact is a non-binding inquiry and must not imply an owner-authorized opening. |
| CAFR-HTML-004 | `projects/co-op-engine/index.html` | Global handler unconditionally consumes PageDown/PageUp and arrows; verifier reproduced PageDown changing an overflowing stage and ArrowRight firing from focused Next — lines 1003–1017, 2338–2349 | MAJOR | Let PageUp/PageDown scroll overflowing stages; prevent stage shortcuts from interactive focus; preserve explicit controls, ordinary links, and working Escape focus restoration. | Both verifiers confirmed. |
| CAFR-HTML-005 | `projects/co-op-engine/index.html` | “I can see the evidence,” “Proof,” and “open evidence” promise inspectability, but `Exists` strips provide prose without adjacent provenance/limit — lines 1430–1451, 1515–2074, 2111–2113 | MAJOR | Rename or qualify unsupported proof claims as owner-stated current artifact state; link only authorized public-safe evidence and explicitly identify unavailable or non-public evidence. | Technical vocabulary is not inherently defective when bridged by an ordinary-domain act. |
| CAFR-HTML-007 | `projects/co-op-engine/index.html` | Filtering changes card visibility/status only; count, “Fourteen…” heading, and fourteen jump links remain — lines 1476–1503, 2240–2257 | MINOR | Synchronize count, contextual heading, and jump links with visible cards; ensure “All 14” restores the complete surface. | Both verifiers reproduced. |
| CAFR-HTML-008A | `projects/co-op-engine/index.html` | Global `:focus-visible` uses coral at 2.306:1 against paper and 2.578:1 against card white — lines 68–71 | MAJOR | Use an ink or dual-contrast focus indicator meeting at least 3:1 against every adjacent surface. | Split from the original mixed finding; the global rule affects the primary keyboard surface. |
| CAFR-HTML-008B | `projects/co-op-engine/index.html` | Agenda sections and boundary articles use styled `<strong>` labels rather than semantic headings — lines 2115–2141, 2177–2189 | MINOR | Give retained agenda items and boundary articles meaningful headings or names without changing the coherent document-level h1/h2/h3 sequence. | Blanket heading-hierarchy incoherence was refuted. |
| CAFR-HTML-009 | `projects/co-op-engine/index.html` | `page-cue` is `aria-live="polite"` and its content is mutated by details toggles and passive IntersectionObserver scrolling — lines 1382–1385, 2267–2284 | MINOR | Remove live semantics from passive-scroll narration; retain only one concise announcement for explicit filter, contact, and presentation actions. | This behavior remains explicit even if removal of visible meta-copy cures it. |
| CAFR-EVIDENCE-001 | Current HTML plus cited live verifier behavior | The page itself says “People must establish” understanding, trust, welcome, collaboration, and recruitment — lines 2177–2189; live verification found no cold-reader/contact-outcome evidence | MAJOR acceptance gap | Require human comprehension evidence and black-box contact-path evidence before acceptance; never report working links as successful contact or recruitment. | Replaces the Inventory-derived candidate with primary and live evidence. |

## Dropped Or Replaced

- `CAFR-HTML-003` is dropped as an independent defect. Meeting prominence is
  not independently proven harmful once identity and contact are repaired.
  Presenter-only placement or CTA demotion remains optional advice.
- `CAFR-HTML-006` is dropped. Progressive disclosure works, and “Needs now”
  would exceed proof without an owner-bound open-ask state.
- Original `CAFR-HTML-008` is split into focus contrast and bounded structural
  semantics.
- `CAFR-PACKET-001` is replaced by `CAFR-EVIDENCE-001`; Inventory is not
  evidence authority.
- Demonstrated mobile overlap, mandatory public evidence links for every
  project, meeting falsity, duplicated email/LinkedIn pairs, and automated
  recruitment proof remain dropped.

## Progressive-Enhancement Contact Contract

- Static query-free `href="mailto:hello@cyberalchemize.com"`.
- Static exact
  `href="https://www.linkedin.com/company/cyberalchemyai/"`.
- Fourteen static, addressable project-context anchors or captions within one
  shared region, so every card reaches visible canonical project context with
  JavaScript disabled.
- Optional JavaScript may select that context and offer a secondary email link
  whose only query parameter is `subject=<exact public project name>`.
- No `cc`, `bcc`, `body`, private context, inferred welcome, open role, or
  implied open ask.
- `_blank` LinkedIn requires `rel="noopener noreferrer"`.

## Ordered Change List

1. Complete visible and accessibility-facing CyberAlchemy identity
   replacement.
2. Implement the static shared contact contract and fourteen no-JavaScript
   project-context routes.
3. Qualify evidence/proof language without exposing private authority
   material.
4. Repair presentation keyboard behavior while preserving presentation and
   Escape recovery.
5. Replace the global low-contrast focus indicator.
6. Remove passive-scroll live-region updates and consolidate explicit
   announcements.
7. Synchronize filter cards, count, heading, and jump links.
8. Add meaningful headings or names to retained agenda and boundary
   structures.
9. Run automated browser checks, then human comprehension and contact testing.

## Automatable Acceptance

1. Title, rendered text, accessible names, live regions, presentation UI, and
   fallbacks contain none of: case-insensitive `Co-Op`/`CO—OP`, “Page cue,”
   “project map / live presentation,” or “Public review prototype.”
2. First viewport at 390×844 names CyberAlchemy and exposes
   keyboard-reachable Explore and Contact actions without horizontal overflow.
3. Exactly the canonical fourteen project articles remain, each with one
   native disclosure and Vision / What exists now / Not yet / Next experiment
   / Possible collaborators.
4. Browse, filters, and presentation reuse those same nodes; disclosure
   content survives transitions.
5. With JavaScript disabled, every project contact entry reaches the shared
   region and visibly identifies its canonical public project name.
6. The region contains exact query-free mailto and LinkedIn hrefs. Any enhanced
   mail query contains only an exact public-name `subject`; never `cc`, `bcc`,
   or `body`.
7. Contact copy frames inquiry as non-binding and owner-confirmed; it does not
   claim a role, need, welcome, or open ask.
8. Every filter synchronizes visible cards, count, heading/status, and jump
   targets; “All 14” restores everything.
9. PageDown scrolls overflowing presentation content without changing stage;
   navigation keys do nothing from interactive focus; Escape restores trigger
   focus.
10. Passive scroll causes zero `aria-live` mutations; explicit actions cause
    at most one concise announcement.
11. Visible focus meets at least 3:1; controls are unobscured; accessibility
    snapshots meaningfully name intended regions and articles.
12. Evidence/proof claims have either an authorized public link or an explicit
    owner-stated/non-public qualifier.

## Human-Only Acceptance

- Cold readers can retell CyberAlchemy's identity and one selected project's
  current state, limit, and contribution status.
- Visitors can choose a project and complete both inquiry paths without
  interpreting them as an open role or owner-confirmed welcome.
- Trust, current welcome, successful contact, collaboration, usefulness, and
  recruitment remain human evidence and cannot be inferred from automation.

## Candidate Verdict

`FIX`

Preserve the fourteen-project truth surface, progressive disclosure, filters,
low-jargon openings, presentation reuse, meeting support, claim boundaries,
and working Escape recovery.
