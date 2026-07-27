---
template_id: invoke.ux-plan
status: authored-complete
target: co-op-engine-browser-app
---

# UX Plan: Co-Op Engine Recruitment and Meeting

## Selection Contract

`DESIGN-SELECTION-RESULT.json` selects `ux-plan` as required. Four natural
actor classes read, navigate, decide, act, recover, and use assistive operation
through five new semantic browser surfaces.

## User Goals

| Goal | Actor | Success signal |
| --- | --- | --- |
| Find a project where a bounded contribution is useful | technical builder or domain practitioner | can name the problem, current witness, limitation, contribution act, effort, and next step |
| Offer help without accidentally committing or being called matched | participant | offer state and visibility are clear; next state remains candidate pair |
| Run the weekly meeting without a separate deck | facilitator | presentation mode preserves truth and adds timing, clinic, and read-back controls |
| Correct or withdraw stale project information | project owner | card returns to draft and requires revalidation without rewriting history |
| Understand what happened after seven days | project owner and participant | terminal receipt states outcome and decision without claiming general efficacy |

## Information Architecture

### Shared content spine

1. A real friction: useful projects and useful skills fail to meet in a form
   small enough to try.
2. The reveal: Co-Op Engine exchanges bounded experiments, not vague ideas,
   jobs, or algorithmic matches.
3. The loop: inspect → signal energy → propose contribution → confirm
   bilaterally → run seven days → record a receipt.
4. The portfolio: fourteen claim-bounded project records.
5. The 45-minute route: orientation, scan, evidence-triggered clinics,
   appointments, read-back.
6. The action: offer a skill, bring a project, request clarification, refer
   someone, or listen.

Self-guided and facilitated modes share this spine. Presentation mode changes
density, sequence controls, and facilitation cues; it does not introduce
different project facts.

### Meta-narration rule

Prefer the substance itself:

- use “A seven-day experiment needs…” rather than “This section explains…”;
- use “Show projects needing a writer” rather than “Use this filter to…”;
- use the exact state label rather than “The page is telling you…”.

Orientation, state announcements, accessibility instructions, consent,
privacy, errors, and recovery directions remain allowed when the interface
cannot communicate them structurally.

## Journeys

| Journey | Start | Success | Failure/recovery | Correction/reversibility |
| --- | --- | --- | --- | --- |
| Browse and offer | orientation or project deep link | valid contribution draft with named visibility and next state | stale card disables offer; route explains owner refresh | clear filters, change project, edit or discard draft |
| Compare projects | project grid | shortlist based on domain, act, effort, and boundary | zero results explain removable filters | clear one/all filters without losing mode |
| Present meeting | facilitator route | timed scan, evidence clinic, appointment read-back | notes unavailable or timer interrupted | audience view continues; reconstruct step from URL/history |
| Confirm appointment | candidate pair | both parties confirm complete terms | missing/contradictory term names exact gap | return to candidate state, revise, or decline |
| Record outcome | appointment after seven days | one terminal receipt plus owner decision | unknown or disputed outcome remains unresolved | superseding correction preserves history |
| Recover navigation | deep link/back/refresh/mobile reflow | same permitted project/mode/action meaning | invalid ID returns to orientation with explanation | user can navigate to catalog without dead end |

## Surfaces

| Surface | Purpose | Entry | Exit |
| --- | --- | --- | --- |
| self-guided page | explain, browse, compare, recruit | `/`, project deep link | offer, refer, meeting route |
| facilitated presentation | run the 45-minute meeting | `/present` plus safe step/project state | appointment read-back, audience handoff |
| presenter view | private timing and boundary cues | authenticated `/presenter` | audience view or meeting close |
| project detail | expose bounded context and exact ask | card action or deep link | offer composer or catalog |
| offer composer | structure contribution without implying match | eligible project CTA | local draft, submitted candidate pair, discard |
| receipt view | show bounded outcome/history | appointment or owner review | keep, revise, close |

## Visible State and Evidence Meaning

| Visible state | Meaning | Allowed action | Uncertainty cue | Owner |
| --- | --- | --- | --- | --- |
| eligible | owner-verified and within policy window | inspect, offer, clinic | verification and expiry date | project/portfolio owner |
| response overdue | owner missed 72-hour response SLA | inspect only | overdue label and disabled action | project owner |
| stale | verification expired or card withdrawn | permitted history only | stale reason and refresh requirement | project owner |
| energy mark | one person's interest or signal | refine offer, refer, stop | “not a match or commitment” | participant |
| candidate pair | contribution proposed to two parties | negotiate, confirm, decline | confirmations shown separately | both parties |
| bilateral appointment | both confirmed complete seven-day terms | run, revise, stop, record receipt | exact terms and receipt date | both parties |
| receipt | dated bounded outcome | keep, revise, close | no general success claim | project owner |

## Interaction Flows

| Flow | Steps | Main risk | Recovery |
| --- | --- | --- | --- |
| filter | choose domain/act/effort → result count → inspect | zero results or lost context | clear filters; announce count |
| detail | open card → focus heading → read bounded fields → close/back | dialog focus or deep-link mismatch | Escape/close returns focus; routed fallback |
| offer | choose contribution → state evidence/availability → review visibility → submit | chat-like copy implies AI/consent | explicit recipient, state, privacy, and next-step copy |
| presentation | advance/back → select clinic → read back appointment | audience and presenter state diverge | truth digest and safe route state remain shared |
| receipt | select outcome → attach bounded evidence → owner decision | outcome inflated into efficacy | fixed outcome terms and claim warning |

## Conversational AI and Chat-Term Audit

The first artifact contains a structured offer conversation, not an AI agent
or AI matcher. Audit every label, prompt, empty state, loading state, error,
confirmation, and receipt for:

- who is speaking or acting;
- who receives the information;
- whether content is a draft, proposal, confirmation, appointment, or receipt;
- what visibility applies;
- whether a human must review or consent;
- what the system actually did;
- what it did not infer.

Reject:

- “You’ve been matched” before bilateral confirmation;
- “the AI found,” “the agent decided,” or “your collaborator” without an
  implemented and admitted capability;
- typing/thinking indicators that imply an AI interlocutor;
- generic “sent” when delivery or acknowledgement is not proven;
- warm copy that obscures privacy, effort, stop rule, or failure state.

## Content Requirements

| Content | Surface | Claim bound | Constraint | Owner |
| --- | --- | --- | --- | --- |
| meeting promise | opening | weekly exchange for small team experiments | no efficacy or autonomous-matching claim | product owner |
| project card | catalog/live | admitted record ceiling | problem, witness, limit, act, ask, owner, SLA, expiry | project owner |
| explanatory reveal | opening/loop | internal Veritasium-inspired trajectory | no public brand, imitation, or endorsement | copy owner |
| offer prompts | composer | state and privacy contracts | precise speaker/recipient/visibility/next state | workflow/privacy owner |
| project narratives | detail | owner-admitted facts | distinct voice; jargon bridged; human judgment retained | Whisper + project owner |
| error/recovery | every action | exact system state | direct, actionable, no blame or false success | UX owner |

## Accessibility and Responsive Semantics

| Consideration | Required response | Acceptance owner |
| --- | --- | --- |
| landmarks/headings | one logical heading outline and named regions in both modes | black-box owner |
| keyboard/focus | all actions operable; visible focus; dialog focus trap/return; Escape closes dismissible layers | black-box owner |
| announcements | result counts, state transitions, errors, and submission outcomes announced without duplication | accessibility reviewer |
| contrast/non-color | state and eligibility never depend on color alone | visual/accessibility reviewer |
| reduced motion | presentation and view transitions respect reduced-motion preference | UX owner |
| reflow | 320 CSS-pixel width retains content, CTA, order, and recovery without horizontal semantic loss | black-box owner |
| presenter/audience separation | presenter cues absent from audience accessibility tree and DOM | privacy auditor |

Responsive behavior may change layout density and navigation controls, but not
information meaning, action availability, reading order, state, or privacy.

## Acceptance Signals

| Signal | Polarity | Exact selector | Accountable | Validator |
| --- | --- | --- | --- | --- |
| project truth agrees across modes | positive | Poker `truth_digest` and named public fields | product owner | projection validator |
| no unilateral match | negative | one-confirmation transition fixture | workflow owner | state validator |
| no private sentinel anywhere | negative | route/DOM/network/storage/export/screenshot/trace sentinel set | privacy owner | independent privacy auditor |
| keyboard journey completes | positive | orientation → Poker detail → offer → discard | UX owner | black-box owner |
| both readers retell and transfer | positive | reader protocol and artifact version | comprehension owner | independent reader moderator |
| chat terms remain honest | mixed | adjudicated UI corpus | copy owner | copy reviewer |
| unnecessary meta-narration absent | negative | visible corpus plus allowed-exception ledger | copy owner | coherence reviewer |

## Gate Result

- Status: `pass` for authored Design.
- Selection: required by deterministic validator.
- Evidence ceiling: planned UX contract only.
- Handoff: architecture and normal Plan after acceptance review.
