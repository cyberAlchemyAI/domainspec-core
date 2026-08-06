# TASK-OAIA-DECIDE — Blind evidence and owner outcome

## Objective

Produce bias-controlled listening evidence and a bounded human decision without allowing scores to become provider, public-use, release, or production authority.

## Mapping

- Slices: S-VERIFY and S-DECIDE
- Layers: L2 and L3
- Waves: W3 and W4
- Sources: `../../UX-PLAN.md`, `../../OPERATIONS.md#blindcandidate`, `../../OPERATIONS.md#recordoperatordecision`
- Dependencies: SWU-OAIA-006 and B-007 closure.
- Current gate: blocked.

## SWU-OAIA-007 — Blind listening evidence

- Primary behavior: collect valid comparable scores without revealing candidate identity/order.
- Independent boundary: emits locked score evidence but no decision.
- Split analysis: opaque packaging, balanced order, and score validation must close together before unblinding.
- Write scope: `runtime/lib/blind-listening.mjs`; `runtime/test/blind.test.mjs`; run-scoped opaque assets, order manifests, sheets, and key locator.
- Done criteria: UUID labels; two repetitions separated; three listeners; common playback receipt; one replay; fixed rubric/weights; valid weighted formula; locked sheets; protected key; median and spread.
- Acceptance evidence: balanced-order positive fixture and exposed-key, adjacent-repetition, duplicate-label, malformed-score, early-unblind negatives plus human receipts.
- Validation: `node --test runtime/test/blind.test.mjs`; listener/order/key audit.
- Execution owner: manual.
- Handoff: hide provider, model, voice, price, marketing, gender labels, and official recommendations until sheets lock.

## SWU-OAIA-008 — Terminal audition decision

- Primary behavior: record the named production operator's `approve|reject|defer` outcome against governing hashes.
- Independent boundary: closes the audition and creates a bounded separate-route handoff, not production artifacts.
- Split analysis: the human decision and its disclosure/claim-ceiling documentation form one terminal contract.
- Dependencies: SWU-OAIA-007.
- Write scope: `runtime/lib/decision.mjs`; `runtime/test/decision.test.mjs`; `runtime/README.md`; one run-scoped decision receipt.
- Done criteria: named owner; legal enum; reasons; manifest/raw/derivative/verification/score/key hashes; tie rule honored; disclosure obligation explicit; unresolved production gates listed; no automatic next action.
- Acceptance evidence: valid signed decision and negatives for score-only, missing owner/hash, illegal outcome, missing disclosure, and release claim.
- Validation: `node --test runtime/test/decision.test.mjs`; manual owner/hash/claim review.
- Execution owner: manual.
- Handoff: any full narration or publication request returns to Invoke with the decision receipt as non-authority evidence.

## Synchronization and completion

007 closes before 008. The task completes at the audition decision only. No successor is automatic, and no video, narration, release, or deployment claim is emitted.
