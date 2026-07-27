# UX Evidence Validator Result

- Status: `seed-only` for browser evidence; `pass` for Design specification
- Mode: `spec` plus `fixture-plan`
- Target: future `projects/co-op-engine/` browser application
- Evidence cards: accepted research sections “Proposed Acceptance
  Specifications,” “Black-box browser contract,” “Copy and chat-language
  audit,” and “Ease and coherence audit”
- Browser evidence: not run; no frontend exists
- Fixture calibration: not run
- Next lifecycle step: acceptance review, then Invoke Plan

## Evidence Boundary

| Lane | What may be claimed now | What remains residue |
| --- | --- | --- |
| source-backed contract | required behavior and claim ceilings are traceable to accepted research and Define | implementation conformance |
| browser-observable | route, DOM, accessibility tree, keyboard, history, network, storage, screenshots, and traces can be specified | actual browser findings |
| proxy | structural and language rules can flag risk | understanding, trust, ease, and coherence |
| domain heuristic | portfolio and meeting patterns can guide review | universal UX truth |
| human study | protocol and exact threshold can be authored | real-reader comprehension and transfer |

No single UX score is permitted.

## Validator Layers L0–L6

| Layer | Contract | Evidence class | Status |
| --- | --- | --- | --- |
| L0 | fixture identity, build/version, route, viewport, reduced-motion, data/policy digest | hard prerequisite | planned |
| L1 | semantic document structure, headings, landmarks, names, state text, truth fields | hard gate when deterministic | planned |
| L2 | keyboard traversal, focus order/return, Escape, announcements, direct-link/back/refresh behavior | hard gate when deterministic | planned |
| L3 | responsive preservation, overflow, clipping, target visibility, controlled screenshots | hard gate for measurable loss; screenshot review for hierarchy | planned |
| L4 | jargon bridges, paragraph/heading load, meta-narration, reference clarity, CTA competition | soft flags plus human review | planned |
| L5 | recruitment-page, project-portfolio, and live-presentation heuristics | domain-tagged review | planned |
| L6 | two-profile retell, transfer, repair, and leakage protocol | human study | planned |

## Claim Classification

### Hard gates

- exact Poker record fields and claim ceiling render from the admitted fixture;
- self-guided and facilitated views share the same truth digest;
- a unilateral signal never renders `matched` or a bilateral appointment;
- stale and overdue cards cannot enter a new pair or clinic;
- unclassified and disallowed sentinels are absent from route, DOM,
  accessibility tree, network, browser storage, exports, screenshots, console,
  and traces;
- presenter notes are absent from the audience DOM and accessibility tree;
- keyboard users can browse, open/close details, draft an offer, and discard;
- focus is visible and returns to the invoking control;
- Escape, back, refresh, and direct links preserve or safely recover semantic
  state;
- mobile reflow preserves content, action, order, and recovery;
- console and network contain no unexpected errors or private payloads.

Hard gates require calibrated fixtures before reusable promotion.

### Soft flags

- unbridged first-use internal terms;
- missing problem, witness, limitation, ask, action, owner, SLA, or expiry;
- paragraph/heading structure that raises scanning risk;
- repeated project-card phrasing that erases domain voice;
- unresolved pronouns or unclear action recipient;
- unnecessary meta-narration;
- chat-like warmth without concrete invitation, visibility, consent, and next
  state;
- CTA competition or unclear primary action.

Soft flags route to human review and cannot alone prove failure.

### Screenshot review

- opening hierarchy and misconception-to-reveal pacing;
- project-grid differentiation without decorative causality;
- presentation legibility at room scale;
- mobile density and meaningful grouping;
- dialog/composer relationship to the selected project;
- reduced-motion and non-color state distinctions.

### Human-study residue

- ease of understanding;
- coherent mental model of the Experiment Exchange;
- trust in privacy and state labels;
- technical-builder and writer/musician retellability;
- transfer to a new story-state or project-state example;
- real recruitment or meeting efficacy.

Automation must not claim these outcomes.

## Fixture Plan

| Fixture | Expected role | Seeded condition | Required observation |
| --- | --- | --- | --- |
| `FG-POKER-GOOD` | known-good | exact admitted Poker record and reciprocal confirmations | all deterministic record, route, state, projection, keyboard, and privacy checks pass |
| `FB-POKER-HIDDEN-CARD` | known-bad | owner-private hidden-card sentinel enters candidate record | admission or projection blocks; sentinel absent everywhere |
| `FB-POKER-ONE-SIDED-MATCH` | known-bad | one confirmation plus UI label `matched` | state and language rules fail for intended reason |
| `FF-PRETTY-WRONG-DOM` | false-positive | screenshot resembles good state while DOM/network contains private or wrong state | screenshot cannot override deterministic failure |
| `FG-WRITER-AS-OF` | domain known-good | admitted Mira/Ivo story assertions and spoiler-safe reader scope | permitted projection passes |
| `FB-WRITER-FUTURE-LEAK` | domain known-bad | future/rejected/proposed assertion in reader projection | negative privacy/temporal test fails |
| `FF-DENSE-EXPERT` | false-positive guard | dense but valid technical project record with bridges and operability | density alone does not hard-fail |
| `FB-META-NARRATION` | copy known-bad | repeated “this section/page/filter…” that replaces substantive labels | soft flag and human adjudication |
| `FG-TWO-VOICES` | copy known-good | Poker and Music use distinct domain acts and ceilings | duplication heuristic stays below review threshold; humans can distinguish |

## Scenario Shape

Each browser scenario must bind:

- artifact commit and build digest;
- admitted-record, policy, and fixture digests;
- route/mode/project/step;
- browser, viewport, input method, color scheme, and reduced-motion state;
- expected hard findings and seeded failure reason;
- output root under
  `output/playwright/ux-validator/<run-id>/`;
- screenshots, traces, ARIA snapshots, accessibility output, DOM
  measurements, console/network record, findings, and residue ledger.

## Required Browser Evidence Outputs

The implemented validator must produce:

- `run-metadata.json`;
- `summary.md`;
- `findings.json`;
- `console-network.json`;
- `accessibility/*.json`;
- `aria/*.yml`;
- `screenshots/*.png`;
- `measurements/*.json`;
- interaction `traces/*.zip`;
- `residue-ledger.yml`.

## Calibration and Promotion Boundary

The Design specification passes because every requested audit has a claim
class, fixture family, observable surface, owner, and evidence output. The UX
Evidence Validator itself remains seed-only. It cannot validate the future
interface until the browser artifact and fixture harness exist.

Promotion of reusable hard gates requires known-good, known-bad, accessibility,
keyboard, layout, interaction, cognitive-risk, domain, and false-positive
fixture runs plus Experiment Harness and Sigil Development review.
