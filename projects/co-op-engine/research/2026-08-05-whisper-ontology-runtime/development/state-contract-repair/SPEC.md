---
module: whisper-research-state-contract-repair
version: candidate-v1
status: defined
docType: specification
authority_effect: none
---

# Specification

## Objective

Repair the only load-bearing defect left by `review-final.md`: the proposed Whisper research fixture must have one closed state vocabulary, one total EV01-EV26 reducer interpretation, and byte-identical live/replay RS26 results.

## Required behavior

1. `pending_gate` is exactly `none | intent_freeze | editorial_decision | mechanical_validation | post_apply_review | corrected_intent_freeze | graph_policy_validation | comprehension_assessment`.
2. `outcome_ceiling` is exactly `not_assessed | pass | flag | block`; `absent` is rejected.
3. EV22 may resolve `COR1` only when the prior correction is open, the event binds `COR1`, corrected artifact `NE2`, their exact digests, and the second mechanical assessment is `pass`. Wrong, missing, stale, premature, or duplicate bindings reject without revision/head advance.
4. Every accepted EV01-EV26 event has exactly one expected prior revision/state and one resulting revision/state. Unlisted state changes are forbidden.
5. Closure plus EV01-EV26 reduces to one canonical RS26. Independent live append and clean replay paths produce identical canonical bytes and SHA-256 digests.
6. RP26 is derived without adding an event/revision or changing RS26.

## Acceptance

A research-only checker must pass the positive trace and fail closed for undeclared gates, `absent`, wrong correction, wrong artifact, stale digest, missing bindings, premature resolution, duplicate EV22, and projection mutation. A second identical run must emit the same semantic result. All failures are `BLOCK`.

After the SWU passes, the research route must independently rerun non-vacuity review, author exact-binding `findings.md`, audit those findings, issue a new passing evidence-closure receipt, and synchronize `RESULT.md`. Until then the research remains blocked.

## Write boundary

Allowed material writes are only new files under the current research root: `synthesis-revision-3.md`, `state-contract/`, and new receipts/review/findings closeout artifacts. Existing revision-2, final review, old receipts, and close record remain immutable.

## Non-goals

No Whisper source edit; ontology creation/admission; runtime implementation; co-op `index.html` or `infra/` edit; public/private boundary crossing; external network; publication; deployment; release; promotion; production claim; or canonical owner decision.
