# CyberAlchemy Collaboration Portfolio Frontend Review

Dispatch:
`2026-07-26-cyberalchemy-collaboration-portfolio-frontend-review`

Review status: verified candidate for parent approval

The review is read-only over the frontend. `FIX` means the accepted
change-request list contains at least one surviving MAJOR finding; it does not
mean the fixes have been implemented.

## Artifact: `projects/co-op-engine/index.html`

| # | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| CAFR-HTML-001 | `projects/co-op-engine/index.html` | The artifact says `"Co-Op Engine — Project Map"` at line 8, uses `aria-label="Co-Op Engine home"` at line 1372, renders `"Page cue"` and `"The Co-Op Engine · project map / live presentation"` at lines 1382–1390, places `"Co-Op Engine"` in the hero diagram at line 1417, calls itself a `"Public review prototype"` at lines 2194–2196, and retains Co-Op presentation fallbacks at lines 2201, 2302, and 2329. The live page is byte-identical to this source. Provenance: `attacks.md`, Peirce initial 1/4 and final 1/4; Alexander initial 1/3/4/9 and final 1/3/4/9; Kahneman initial 4/8 and final rebrand/live-region findings; Popper and Quine final PASS receipts. | MAJOR | Replace browse-visible and accessibility-facing Co-Op/meta identity with a clear CyberAlchemy collaboration-portfolio identity. Preserve presentation-operational metadata only when it cannot become visitor copy; this finding does not require deleting the meeting or presentation capability. |
| CAFR-HTML-002 | `projects/co-op-engine/index.html` | Every project action is an internal `href="#join"` route, from line 1541 through line 2100. The join region ends at `"Copy a contribution prompt"` at lines 2153–2165; the script changes only selected-project text at lines 2260–2264 and copies the prompt at lines 2352–2360. The literal and live DOM contain no `mailto:`, email address, or LinkedIn link. Provenance: `attacks.md`, all three attackers' initial/final contact findings and both verifier PASS receipts. | MAJOR | Add one shared progressively enhanced contact region with static query-free `href="mailto:hello@cyberalchemize.com"` and exact `href="https://www.linkedin.com/company/cyberalchemyai/"`. Every card must reach static visible project context there without JavaScript. Frame contact as a non-binding inquiry, never an open role, owner-confirmed welcome, or open ask. |
| CAFR-HTML-004 | `projects/co-op-engine/index.html` | The global key handler at lines 2338–2349 consumes `ArrowRight`, `ArrowLeft`, `PageDown`, and `PageUp` without checking focused controls or overflowing stage content. Verifiers reproduced PageDown changing an overflowing project stage and ArrowRight firing from the focused Next control. Escape focus recovery works and must be preserved. Provenance: `attacks.md`, Kahneman initial 1/5 and final keyboard finding, Peirce final 3, and both verifier PASS receipts. | MAJOR | Let PageUp/PageDown scroll overflowing stages; prevent stage shortcuts while focus is inside an interactive control; preserve explicit Back/Next controls, ordinary link behavior, and Escape focus restoration. |
| CAFR-HTML-005 | `projects/co-op-engine/index.html` | The copy promises `"I can see the evidence"` at lines 1430–1433, labels a mechanism `"Proof"` at lines 1440–1442, and says visitors can `"open evidence"` at lines 2111–2113. The fourteen `Exists` strips and details contain current-state prose but no adjacent public witness or provenance qualification. Provenance: `attacks.md`, Alexander initial/final 5, Kahneman initial/final evidence finding, and both verifier PASS receipts. | MAJOR | Where authorized public-safe evidence exists, link it. Otherwise describe the statement as owner-stated current artifact state and say that evidence is non-public or unavailable. Do not treat technical vocabulary as defective merely because it is technical. |
| CAFR-HTML-007 | `projects/co-op-engine/index.html` | Filtering changes project-card visibility and the live status at lines 2240–2257, but the heading/count and all fourteen jump links at lines 1476–1503 remain unchanged; verifiers reproduced one visible music project with thirteen jump targets pointing at hidden cards. Provenance: `attacks.md`, Alexander initial/final 8, Kahneman final filter finding, and both verifier PASS receipts. | MINOR | Synchronize the visible count, contextual heading/status, and jump links with the active filter; ensure `All 14` restores the complete project surface. |
| CAFR-HTML-008A | `projects/co-op-engine/index.html` | The global `:focus-visible` color is coral at lines 68–71. Measured contrast is 2.306:1 against the paper background and 2.578:1 against card white, affecting the keyboard focus indication across the primary surface. Provenance: `attacks.md`, Kahneman initial/final focus finding and both verifier PASS receipts. | MAJOR | Use an ink or dual-contrast focus indicator that reaches at least 3:1 against every adjacent surface. |
| CAFR-HTML-008B | `projects/co-op-engine/index.html` | Retained agenda sections use styled `<strong>` labels rather than headings at lines 2115–2141; boundary articles do the same at lines 2177–2189. The broader claim that the document's h1/h2/h3 sequence is incoherent was refuted. Provenance: `attacks.md`, Kahneman initial/final semantics finding and both verifier PASS receipts. | MINOR | Give retained agenda items and boundary articles meaningful semantic headings or accessible names without changing the coherent document-level heading sequence. |
| CAFR-HTML-009 | `projects/co-op-engine/index.html` | The `page-cue` is `aria-live="polite"` at lines 1382–1385. Details toggles and passive IntersectionObserver scrolling mutate its text at lines 2267–2284, so merely scrolling can trigger narrated state. Provenance: `attacks.md`, Kahneman initial/final live-region finding, Alexander final 3, and both verifier PASS receipts. | MINOR | Remove live semantics from passive-scroll narration. Retain at most one concise announcement for explicit filter, contact, and presentation actions. |

Artifact verdict: **FIX**

The artifact has five surviving MAJOR findings and three surviving MINOR
findings. Its fourteen-project structure, progressive disclosure, filters,
plain-language opening questions, presentation reuse, `Not yet` boundaries,
skip link, native details, mobile no-overflow behavior, and Escape focus
recovery survive the attack.

## Acceptance Evidence Surface

| # | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| CAFR-EVIDENCE-001 | `projects/co-op-engine/index.html`; `output/playwright/ux-validator/co-op-showcase-20260726/deployment/live-acceptance.json` | The page itself says `"People must establish"` understanding, trust, project welcome, collaboration, and recruitment at lines 2187–2188. The live acceptance receipt proves reachability, layout/runtime behavior, project count, presentation behavior, and security headers, but contains no cold-reader, completed contact, current welcome, or recruitment evidence. Provenance: `attacks.md`, all three attackers' evidence boundaries and both verifier PASS receipts. | MAJOR acceptance gap | Require automated contact-path evidence and separate human comprehension evidence before calling the revised page accepted for its recruitment purpose. Never report working links as successful contact, collaboration, or recruitment. |

Evidence-surface verdict: **FIX before acceptance**

## Refuted And Dropped Findings

| Candidate | Disposition | Reason |
| --- | --- | --- |
| CAFR-HTML-001/002 at CRITICAL | Demoted to MAJOR | Identity and contact fixed requirements fail, but the page and fourteen-project surface remain functional; the house CRITICAL threshold is not met. |
| CAFR-HTML-003 | Dropped as an independent finding | Hero/agenda ordering was not independently proven harmful once identity and contact are repaired. Presenter-only agenda placement and CTA demotion remain optional design advice. |
| CAFR-HTML-005 universal jargon rewrite | Dropped | Source-bound technical terms are permitted when bridged by an ordinary-domain act. Only unsupported inspectability/provenance survives. |
| CAFR-HTML-006 | Dropped | Progressive disclosure works; collaborator information is one native disclosure away. `"Needs now"` would overstate welcome without an owner-bound open-ask state. |
| Original CAFR-HTML-008 | Split and narrowed | Global focus contrast survives as MAJOR; bounded structural naming survives as MINOR; blanket heading incoherence is refuted. |
| CAFR-PACKET-001 | Replaced | Inventory is non-authoritative. The accepted evidence gap is grounded in the current page and live acceptance receipt. |
| Mobile cue overlap | Dropped | Source establishes risk, but no rendered overlap was demonstrated and mobile no-overflow was reproduced. |
| Public evidence link for every project | Dropped | Private authority material must not be exposed; an explicit owner-stated/non-public qualifier is acceptable. |
| Weekly meeting is false | Dropped | Current operation was not independently verified, but the review does not establish falsity and the user asked to remove Co-Op branding, not meeting capability. |
| Fourteen duplicated email/LinkedIn pairs | Dropped | One static shared contact surface plus fourteen no-JavaScript context routes satisfies the task with less drift. |
| Automation proves recruitment | Dropped | Browser automation can prove paths and behavior, not understanding, welcome, contact success, collaboration, or recruitment. |

## Verified Change Requests

1. Replace all visible and accessibility-facing Co-Op/meta identity with a
   CyberAlchemy collaboration-portfolio identity.
2. Add the static shared contact contract:
   - query-free `mailto:hello@cyberalchemize.com`;
   - exact `https://www.linkedin.com/company/cyberalchemyai/`;
   - fourteen static project-context destinations that work without
     JavaScript;
   - optional email subject containing only the exact public project name;
   - no `cc`, `bcc`, body, private context, inferred welcome, role, or open ask;
   - `rel="noopener noreferrer"` whenever LinkedIn uses `_blank`.
3. Qualify evidence/proof language without exposing private authority
   material.
4. Repair presentation keyboard behavior while preserving presentation,
   explicit controls, ordinary links, and Escape recovery.
5. Replace the global low-contrast focus indication.
6. Remove passive-scroll live-region updates and consolidate explicit action
   announcements.
7. Synchronize filtered cards, count, heading/status, and jump links.
8. Add meaningful headings or accessible names to retained agenda and boundary
   structures.
9. Run automated black-box acceptance, then separate human comprehension and
   contact tests.

## Automatable Acceptance

1. Document title, rendered text, accessible names, live regions,
   presentation UI, and script fallbacks contain none of the legacy denylist:
   case-insensitive `Co-Op`/`CO—OP`, `Page cue`,
   `project map / live presentation`, or `Public review prototype`.
2. At 390×844, the first viewport names CyberAlchemy and exposes
   keyboard-reachable Explore and Contact actions without horizontal overflow.
3. Exactly the canonical fourteen project articles remain, each with one
   native disclosure and Vision / What exists now / Not yet / Next experiment
   / Possible collaborators.
4. Browse, every filter, and presentation reuse those same nodes, and
   disclosure content survives transitions.
5. With JavaScript disabled, every project contact entry reaches the shared
   region and visibly identifies its canonical public project name.
6. The contact region contains the exact query-free mailto and LinkedIn hrefs.
   Any enhanced mail query contains only an exact public-name `subject`, never
   `cc`, `bcc`, or `body`.
7. Contact copy says inquiry is non-binding and owner-confirmed; it does not
   claim a role, current need, welcome, or open ask.
8. Every filter synchronizes visible cards, count, heading/status, and jump
   targets; `All 14` restores everything.
9. PageDown scrolls overflowing presentation content without changing stage;
   stage-navigation keys do nothing while focus is interactive; Escape restores
   trigger focus.
10. Passive scrolling causes zero `aria-live` mutations; explicit filter,
    contact, and presentation actions cause at most one concise announcement.
11. Visible focus reaches at least 3:1; controls remain unobscured; intended
    regions and articles have meaningful accessible names.
12. Every evidence/proof claim has either an authorized public link or an
    explicit owner-stated/non-public qualifier.

## Human-Only Acceptance

- Cold readers from technical and domain-practitioner audiences can retell
  CyberAlchemy's identity and one selected project's current state, limit, and
  contribution status.
- Visitors can select a project and complete both inquiry paths without
  interpreting them as an open role or owner-confirmed welcome.
- Trust, current welcome, successful contact, collaboration, usefulness, and
  recruitment remain human evidence and cannot be inferred from automation.

## Final Review Verdict

**FIX**

The change-request list is verifier-accepted. Parent approval remains pending
until the downstream coverage auditor confirms full lens and target coverage,
verbatim transcript preservation, dropped-finding discipline, and the
zero-findings rule.
