---
module: augmentor-rich-consultation-publication
version: candidate-0.1.0
status: designed
updatedAt: 2026-08-04
docType: ux-plan
---

# UX Plan: Published Agent API Document

## User outcome

A signed-in person can open one protected page, understand what the consultation
API does, ask a question at a chosen explanation depth, read the returned
evidence and teaching support, and see the important limit without learning
internal architecture first. A browser agent can perform the same flow through
the stable page controller.

## Semantic surface

The production page changes from the previously deployed Agent API document to
the current local `1.1.0` document. The page adds explanation depth and renders
current state, ordered process, a clearly labeled scenario, a bounded analogy,
and only the glossary terms used.

## Required language

- Say “Ask what Augmentor says,” not “Run the reasoning engine.”
- Say “reviewed information” or “evidence,” not “truth.”
- Say “How detailed should the explanation be?” not “profile” in primary UI.
- Keep `brief`, `guided`, and `deep` available as API values and explain them in
  plain language beside the control.
- Put “This does not decide or grant permission” next to results, not only in a
  distant technical section.
- Label scenarios as illustrative and place an analogy’s limit immediately
  after the analogy.

## Flow

1. Sign in through the existing browser Basic Auth prompt.
2. Open `#agent-api` or choose “Use the Agent API.”
3. Read the short purpose and limit.
4. Enter a question; the default remains the reasoning-engine question because
   it exposes the important current-state qualification.
5. Choose explanation depth and information areas.
6. Submit; cancellation replaces an older in-flight request.
7. Read the answer-policy message before evidence and explanation support.
8. Copy the evidence brief or inspect raw JSON if needed.

## Accessibility and responsive contract

- Keyboard-only completion of the form and details controls.
- Visible focus and persistent labels.
- Status and errors announced through live regions without stealing focus.
- 320 px layout with no horizontal overflow.
- Reduced motion honored.
- All returned text inserted as text, never HTML.
- Explanation headings describe content: Current state, How it works,
  Illustrative scenario, Analogy, Important boundary, Glossary.

## Agent-control contract

- Page hash: `#agent-api`
- Controller: `window.augmentorConsultationPage`
- Primary method: `ask(question, options)`
- Completion event: `augmentor:consultation-complete`
- Stable selectors remain under `data-testid`.
- Controller and UI expose the same structured response and answer action.

## Acceptance

- Exact candidate page passes the existing desktop, 320 px, reduced-motion,
  keyboard, cancellation, safe-text, and automation scenarios.
- Deployed page hash equals candidate hash.
- A production authenticated browser replay is recorded by the human operator
  if a plaintext credential is intentionally available to that person. Its
  absence is residue, not a reason to request or expose a credential.

