---
decisionGateId: DG-MPX-HUMAN-REVIEW-001
targetScope: minto-pyramid-experiment-001/SWU-MPX-003
profile: pilot
status: blocked
createdAt: 2026-08-26T15:35:45Z
updatedAt: 2026-08-26T16:16:57Z
sourcePacketSha256: 0ee4f4c5da27885ce8048dcb614f9b9a04de93b1f4f3aa3ce2be2acab4862a1d
authorityEffect: none
---

# Decision Gate: blinded Minto human review

## Gate result

- Result: `BLOCK`
- Admissible routing: `block`
- Decisions resolved: `8`
- Blockers remaining: `1`
- Override: not requested
- Reveal permitted: `false`
- Human response permitted: `false` for attempt 001 because the volatile review-start and committed-secret state is absent before response persistence.
- Consequential next step: restart the whole SWU with a fresh mapping, nonce, commitment, packet, and human review; do not reuse these answers as a new attempt's response.

## Scope and authority

This gate records the human-owned inputs required by the role-label-blind review. It does not decide whether a judgment is pass, fail, or inconclusive, does not reveal the A/B assignment, and does not establish reader outcomes, canonical integration, promotion, publication, or any authority effect.

The exact source is `BLINDED-REVIEW-PACKET.json` at SHA-256 `0ee4f4c5da27885ce8048dcb614f9b9a04de93b1f4f3aa3ce2be2acab4862a1d`.

## Admissibility receipts

| Gate | Decision | Route | Admissible choices | Rejected | Receipt SHA-256 |
|---|---|---|---:|---:|---|
| R00 | Human attestation | gate | 3 | 0 | `db77ce3d8d923c2ffc9df8d0d6d3a1e800a363a4aa5692fd69dfc4775ddb7d7b` |
| R01 | Factual equivalence | gate | 5 | 0 | `fc8adaf41b6d83536bd529422db116c3074e35052371ad8d953783058bd6a731` |
| R02 | Fair representation | gate | 5 | 0 | `c203deb401da4578458a91409bad47860c2c3c61d5a60f2af9179d7ab05dc09b` |
| R03 | Executive transport fit | gate | 5 | 0 | `7d937e496af7988f122167290a9a2ff002e450fa98848d131f0dbfed983702f8` |
| R04 | Hierarchy plausibility | gate | 5 | 0 | `16f1ef7aec009e1ddebcb988f152dcb3bbe5c2e7c9db885285dfc8c27696a791` |
| R05 | Named decision changed | gate | 5 | 0 | `63f9562a978fad478e9f4567874efcecdf66cefe446654a28aa3465a2cf47ab8` |
| R05L | Exhibiting variant label | gate | 5 | 0 | `0b90b9cdda9ae85381a25f14d2b7333b2118bb478e7a8c9b3277ab1147b35ebc` |
| R06 | Boundary case inactive | gate | 5 | 0 | `1ff318fddaf663436f4439f76e11417607c7135439be642c80f63ad9a491f365` |

Canonical request and receipt pairs are under `decision-gate/requests/` and `decision-gate/receipts/`.

## Common judgment options

These options apply to R01–R06. R05L instead records `A`, `B`, or `none`.

| Option | Kind | Benefit | Cost or risk | Choose when | Downstream impact |
|---|---|---|---|---|---|
| Pass | action | Records that the packet evidence supports the exact prompt. | An unsupported pass would overstate the human evidence. | The prompt is affirmatively satisfied and the rationale identifies why. | Continues the gate; the final witness can pass only if every judgment passes and the revealed label is the candidate. |
| Fail | action | Preserves an observed contradiction or failure without pressure to upgrade it. | The completed experiment verdict becomes fail. | The packet evidence contradicts the prompt. | Continues the gate with a valid negative experiment outcome. |
| Inconclusive | action | Preserves genuine uncertainty. | The completed experiment cannot receive a pass verdict unless another judgment already forces fail. | The packet is insufficient for a responsible yes or no. | Continues the gate with an inconclusive human judgment. |
| Defer | defer | Preserves blinding and avoids a forced answer. | The review and witness remain blocked. | More time or context is required, without opening forbidden source artifacts. | Stops this gate run with unresolved blockers. |
| Stop | stop | Ends the current attempt without fabricating evidence or revealing the assignment. | This review transaction cannot be resumed; a later attempt requires fresh blinding state. | The reviewer cannot or does not want to complete the review. | Terminates the current review attempt with no human response or witness. |

`Explain / more context` is always available but is not a decision answer. It leaves the gate blocked and triggers an aligned low-, medium-, and complex-example explanation before the same options are presented again.

## Decision ledger

| Order | Gate | Question | Classification | Selected option | Rationale | Decision source | Status |
|---:|---|---|---|---|---|---|---|
| 1 | R00 | Can the reviewer attest that they are human and reviewed only the blinded packet? | blocker | `DG-MPX-R00-CONFIRM` | I am a human reviewer and reviewed only the blinded packet. | user chat; `reviewer_id=vlad`; 2026-08-26T15:38:18Z | resolved |
| 2 | R01 | Do variants A and B preserve the same factual content without adding, omitting, or changing a claim? | blocker | `DG-MPX-R01-PASS` | the two variants present the same content, the only difference is that the variant B starts to dry, it says APPove and then describe what | user chat; `reviewer_id=vlad`; 2026-08-26T15:41:31Z | resolved |
| 3 | R02 | Does the declared hierarchy avoid claiming more than the supported concept and explicit limits allow? | blocker | `DG-MPX-R02-PASS` | everything is described correctly in one bounded chain | user chat; `reviewer_id=vlad`; 2026-08-26T15:45:58Z | resolved |
| 4 | R03 | Is the declared hierarchy a plausible structural fit for this executive brief? | blocker | `DG-MPX-R03-PASS` | it explained weel | user chat; `reviewer_id=vlad`; 2026-08-26T15:52:03Z | resolved |
| 5 | R04 | Does one variant plausibly present one governing point with support blocks beneath it? | blocker | `DG-MPX-R04-PASS` | the second does it first and then explain why, but its start already requesting the approval, instead of saying what needs approval | user chat; `reviewer_id=vlad`; 2026-08-26T15:59:07Z | resolved |
| 6 | R05 | Does exactly one variant exhibit the declared hierarchy rather than the flat evidence-led plan? | blocker | `DG-MPX-R05-PASS` | B does it | user chat; `reviewer_id=vlad`; 2026-08-26T16:00:30Z | resolved |
| 7 | R05L | Which view exhibits that hierarchy: A, B, or none? | blocker | `DG-MPX-R05L-B` | B | user chat; `reviewer_id=vlad`; 2026-08-26T16:04:07Z | resolved |
| 8 | R06 | Should the candidate remain inactive and leave the discovery-led boundary view untransformed? | blocker | `DG-MPX-R06-PASS` | The boundary view is good as written because it preserves the unresolved evidence instead of forcing a premature governing conclusion. | user chat confirmation of exact proposed rationale; `reviewer_id=vlad`; 2026-08-26T16:16:57Z | resolved |

## Deferred decisions and assumptions

- Deferred decisions: none yet.
- Assumptions: none. All eight human decisions are resolved; no missing secret, timestamp, response, or witness will be inferred or reconstructed.

## Attempt 001 interruption

- Structural result: `BLOCK_RESTART_REQUIRED`.
- Both volatile state keys required to close attempt 001 are absent: the review-start marker and mapping/nonce secret.
- `HUMAN-REVIEW-RESPONSE.json` and `HUMAN-REVIEW-AND-WITNESS.json` were not created.
- The persisted commitment is a one-way digest and cannot supply the original mapping or nonce.
- `TASK-MPX-003-REVIEW.md` and `IMPLEMENTATION-PLAN.md` require the whole SWU to restart after interruption before reveal; reconstruction or reuse of the old packet-bound answers is invalid.
- Independent helper audit verdict: `BLOCK_RESTART_REQUIRED`; read-only; files changed: none.

## Current question

No human decision remains. Attempt 001 cannot proceed to response persistence or reveal and must be replaced by a fresh complete SWU attempt.
