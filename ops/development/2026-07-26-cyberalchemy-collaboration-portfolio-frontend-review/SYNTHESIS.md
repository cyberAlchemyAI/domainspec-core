# Candidate Frontend Review Findings

This is the registered synthesizer's candidate, not the final verified
`findings.md`. Verifiers may refute and drop findings.

## Candidate Findings

| ID | Artifact | Quoted evidence and source | Severity | One-line proposed fix | Transcript provenance |
| --- | --- | --- | --- | --- | --- |
| CAFR-HTML-001 | `projects/co-op-engine/index.html` | “Co-Op Engine — Project Map”; `aria-label="Co-Op Engine home"`; “The Co-Op Engine · project map / live presentation”; “Page cue”; “Public review prototype” — lines 8, 1372, 1382–1390, 2194–2202; fallbacks 2302, 2329 | CRITICAL | Fixed requirement: replace all visible and accessibility-facing Co-Op/meta-conversation identity with a plain CyberAlchemy identity and portfolio proposition; retain non-rendered presentation metadata only where it cannot leak as visitor copy. | Peirce initial 1/4, final 1/4; Alexander initial 1/3/4/9, final 1/3/4/9; Kahneman initial 4/8, final rebrand/live-region findings |
| CAFR-HTML-002 | `projects/co-op-engine/index.html` | Fourteen offers use `href="#join"`; join ends at “Copy a contribution prompt”; no `mailto:`, email address, or LinkedIn URL — lines 1541–2100, 2153–2165, 2260–2264, 2352–2360 | CRITICAL | Fixed requirement: add exact email and LinkedIn paths in one shared contact block, with every card carrying its selected public project context into that block. | Peirce initial 2/6, final 2; Alexander initial/final 2; Kahneman initial 2, final contact tension |
| CAFR-HTML-003 | `projects/co-op-engine/index.html` | Header prioritizes “Present this page” and “45 minutes”; hero explains the meeting before CyberAlchemy; full agenda precedes contact — lines 1373–1407, 2108–2147 | MAJOR | Optional structural recommendation: lead with CyberAlchemy → fields → invitation → Explore/Contact; keep the agenda presenter-only and demote presentation entry without removing presentation capability. | Peirce initial/final 3; Alexander initial 4/7, final 4/7; Kahneman final meeting placement |
| CAFR-HTML-004 | `projects/co-op-engine/index.html` | Global handler captures `PageDown`, `PageUp`, and arrows regardless of focus; ordinary hero anchors remain inside active stages — lines 1003–1017, 1400–1403, 2338–2349 | MAJOR | Let PageUp/PageDown scroll overflowing stages; gate Left/Right on non-interactive focus; make ordinary anchors stage-aware or inert while presenting. | Kahneman initial 1/5, final keyboard/presentation findings; Peirce final 3 |
| CAFR-HTML-005 | `projects/co-op-engine/index.html` | “I can see the evidence”; “Proof”; “open evidence,” but `Exists` strips are prose only; several use “research tower,” “claim ledger,” “L0 mutation loop,” “schemas, kernel, L0” — lines 1430–1451, 1590–1601, 1719–1730, 1805–1816, 1934–1945, 2111–2113 | MAJOR | Translate the 30-second layer into tangible domain language; link public-safe evidence when available, otherwise qualify it as owner-stated/non-public. | Alexander initial 5, final 5; Kahneman initial/final evidence finding |
| CAFR-HTML-006 | `projects/co-op-engine/index.html` | “Possible collaborators” and contribution action exist only inside each expansion — representative lines 1516–1542; repeated through 2101 | MAJOR | Optional structural recommendation: surface one concise “Needs now”/“Useful crafts” line and project-aware handoff in each collapsed card while preserving full boundaries in details. | Alexander initial 6, final 6; Peirce final 6; Kahneman final added finding |
| CAFR-HTML-007 | `projects/co-op-engine/index.html` | Filtering hides cards and updates only status; heading/count and fourteen jump links remain unchanged — lines 1476–1503, 2240–2257 | MINOR | Synchronize visible count, heading, and jump links with the active filter and provide an obvious “Show all fourteen” reset. | Alexander initial/final 8; Kahneman final filter finding |
| CAFR-HTML-008 | `projects/co-op-engine/index.html` | Coral focus ring is 2.306:1 on `#f4f0e7` and 2.578:1 on `#fffdf7`; “Why,” agenda items, and boundary cards lack heading elements — lines 68–71, 1421–1454, 2115–2141, 2177–2189 | MINOR | Use a ≥3:1 or dual-contrast focus indicator and give sections/articles a coherent heading hierarchy. | Kahneman initial 6/7, final focus/semantics findings |
| CAFR-PACKET-001 | `strategy-inventory-packet.json` | Gaps: “No current cold-reader evidence,” “No current conversion evidence,” and “No current black-box test covers mailto or LinkedIn destinations”; packet is explicitly non-authoritative | MAJOR | Treat comprehension/contact success as acceptance evidence still to gather, never as established by source edits or working links. | Alexander initial/final 10; Peirce surviving boundary; Kahneman human residue |

## Candidate Verdict

`FIX`

The fourteen-project chassis, progressive disclosure, craft filters,
presentation reuse, opening questions, and honest `Not yet` boundaries
survive. The current artifact cannot yet be accepted as a CyberAlchemy
collaboration portfolio because the fixed identity and contact requirements
fail.

## Dropped Or Demoted Claims

- Dropped the claim that the mobile cue demonstrably covers content. Source
  establishes risk, but cited live testing found no horizontal overflow and no
  rendered overlap proof.
- Rejected “public evidence link for every project” as absolute. Private
  authority evidence must not be leaked; explicit owner-stated/non-public
  qualification is acceptable.
- Did not treat the weekly meeting as false. Its current operation is
  unverified; remove or soften it unless dated owner confirmation is supplied.
- Demoted cold-reader and recruitment effectiveness from page defects to an
  evidence gap: the page does not prove those outcomes.
- Rejected fourteen duplicated email/LinkedIn pairs as a fixed requirement.
  Candidate resolution: one central, persistent email/LinkedIn block;
  fourteen project-aware internal entries update visible selected-project
  context and the central email subject. Verifiers must decide whether the
  dynamic handoff remains robust without JavaScript and satisfies the exact
  email-path requirement.
- Privacy observations are acceptance constraints, not standalone defects.

## Ordered Candidate Change Requests

1. Complete CyberAlchemy rebrand across title, visible copy, accessible names,
   presentation titles, and fallbacks.
2. Add central exact email/LinkedIn contact paths and project-aware
   card-to-contact routing.
3. Rebuild the hero around identity, portfolio fields, Explore, and Contact.
4. Remove browse-mode cue/meta narration; retain presentation metadata and
   controls.
5. Repair presentation keyboard, focus, and stage-link behavior.
6. Translate proof strips; link or qualify evidence without leaking private
   material.
7. Surface a concise current need while preserving every card's progressive
   disclosure and claim bounds.
8. Synchronize filter count/cards/jump navigation.
9. Correct focus contrast and heading semantics.
10. Run black-box and cold-reader acceptance.

## Candidate Acceptance Checks

1. At 390×844, first viewport names CyberAlchemy and exposes
   keyboard-reachable Explore and Contact actions without overflow.
2. Document title, visible browse copy, presentation UI, and accessibility
   snapshot contain no Co-Op or meta-conversation labels.
3. Email exposes `hello@cyberalchemize.com`; LinkedIn resolves exactly to
   `https://www.linkedin.com/company/cyberalchemyai/`, with no tracking query.
   `_blank` requires `rel="noopener noreferrer"`.
4. All fourteen card entry paths reach the shared contact block, preserve the
   public project name visibly, and set only that name in any mail subject; no
   `cc`, `bcc`, or sensitive body.
5. Exactly fourteen canonical project cards remain; browse, filter, and
   presentation reuse them.
6. PageDown scrolls an overflowing presentation stage without changing stage;
   arrows do not navigate while focus is on an interactive control; Escape
   restores focus.
7. Passive scrolling makes no live announcement; each
   filter/contact/presentation action emits at most one concise update.
8. Filtering synchronizes visible cards, count, heading, and jump links; no
   jump targets a hidden card.
9. Focus indicators meet ≥3:1 non-text contrast; controls remain unobscured and
   ≥24×24 CSS px.
10. Headings form a coherent h1→h2→h3 hierarchy and sections/articles have
    meaningful accessible names.
11. “Proof/evidence” appears only beside a public-safe link or explicit
    owner-stated/non-public qualification.
12. Cold readers can retell CyberAlchemy identity, one project's
    state/limit/need, and complete project-aware email and LinkedIn selection;
    successful contact, welcome, collaboration, and recruitment remain human
    residue.
