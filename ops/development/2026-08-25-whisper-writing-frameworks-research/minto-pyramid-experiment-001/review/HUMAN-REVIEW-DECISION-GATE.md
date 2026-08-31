---
decisionGateId: DG-MPX-HUMAN-REVIEW-002
attemptId: attempt-002
targetScope: minto-pyramid-experiment-001/SWU-MPX-003
profile: pilot
status: blocked
createdAt: 2026-08-26T16:21:57Z
updatedAt: 2026-08-26T16:28:58Z
reviewStartedAt: 2026-08-26T16:28:58.214735Z
sourcePacketSha256: 06b04618d7050798d74d86afa4d96636c1dcb5b9ba682cc7589d1ad8f50e1d2c
authorityEffect: none
---

# Decision Gate: blinded Minto human review — attempt 002

## Gate result

- Result: `BLOCK`
- Admissible routing: `gate`
- Decisions resolved: `0`
- Blockers remaining: `8`
- Override: not requested
- Reveal permitted: `false`
- Human response persistence permitted: `false` until all eight human-owned decisions are resolved.
- Consequential next step: obtain R00 human attestation against the fresh blinded packet.

## Scope and authority

This gate records the human-owned inputs required by the fresh role-label-blind review. It does not decide whether a judgment is pass, fail, or inconclusive, does not reveal the A/B assignment, and does not establish reader outcomes, canonical integration, promotion, publication, or any authority effect.

The exact source is `BLINDED-REVIEW-PACKET.json` at SHA-256 `06b04618d7050798d74d86afa4d96636c1dcb5b9ba682cc7589d1ad8f50e1d2c`.

Attempt 001 is preserved under `attempts/attempt-001/`. Its answers are historical communication evidence only and are not inputs to attempt 002.

## Admissibility receipts

| Gate | Decision | Route | Admissible choices | Rejected | Receipt SHA-256 |
|---|---|---|---:|---:|---|
| R00 | Human attestation | gate | 3 | 0 | `4b565463cc36b46a8bdd9777f464723d5de3462f53d072bad3413b828ea90e51` |
| R01 | Factual equivalence | gate | 5 | 0 | `53c7473fa00817fa34afd4ababb172b02891ef1800ea3ba7d59a84126cf7f702` |
| R02 | Fair representation | gate | 5 | 0 | `ff61c28aa16ea6944a085e6cb6502cd6566a15169ce9142c1ee51fb5d359cede` |
| R03 | Executive transport fit | gate | 5 | 0 | `a152574aa1fb583e34c7de82aea4834f6dbd5136085740a2b2037b84f7f896cf` |
| R04 | Hierarchy plausibility | gate | 5 | 0 | `2766d4b2ca2a7d42d245d9ecfd98e3ef325e53b533b230105d86b50e311c91ed` |
| R05 | Named decision changed | gate | 5 | 0 | `d1770a17746bf52ee26668482639bde266d56eb41088d70a94e850102462a9ea` |
| R05L | Exhibiting variant label | gate | 5 | 0 | `6ced7f8f305f78c0d07f47a67dee4366573b04a6d76491a92031feb0b224fde5` |
| R06 | Boundary case inactive | gate | 5 | 0 | `e0fb15e34281ed91d149f9fe342a2cf0ce5c5684d28ff22789f00c2662e82125` |

Canonical request and receipt pairs are under `decision-gate/requests/` and `decision-gate/receipts/`.

## Common judgment options

These options apply to R01–R06. R05L instead records `A`, `B`, or `none`.

| Option | Kind | Benefit | Cost or risk | Choose when | Downstream impact |
|---|---|---|---|---|---|
| Pass | action | Records that the packet evidence supports the exact prompt. | An unsupported pass would overstate the human evidence. | The prompt is affirmatively satisfied and the rationale identifies why. | Continues the gate; the final witness can pass only if every judgment passes and the revealed label is the candidate. |
| Fail | action | Preserves an observed contradiction or failure without pressure to upgrade it. | The completed experiment verdict becomes fail. | The packet evidence contradicts the prompt. | Continues the gate with a valid negative experiment outcome. |
| Inconclusive | action | Preserves genuine uncertainty. | The completed experiment cannot receive a pass verdict unless another judgment already forces fail. | The packet is insufficient for a responsible yes or no. | Continues the gate with an inconclusive human judgment. |
| Defer | defer | Preserves blinding and avoids a forced answer. | The review and witness remain blocked. | More time or context is required, without opening forbidden source artifacts. | Stops this gate run with unresolved blockers. |
| Stop | stop | Ends the current attempt without fabricating evidence or revealing the assignment. | This review transaction cannot be resumed; a later attempt requires fresh blinding. | The reviewer cannot or does not want to complete the review. | Terminates the current review attempt with no human response or witness. |

`Explain / more context` is always available but is not a decision answer. It leaves the gate blocked and triggers an aligned explanation before the same options are presented again.

## Decision ledger

| Order | Gate | Question | Classification | Selected option | Rationale | Decision source | Status |
|---:|---|---|---|---|---|---|---|
| 1 | R00 | Can the reviewer attest that they are human and reviewed only the fresh blinded packet? | blocker | — | — | — | unresolved |
| 2 | R01 | Do variants A and B preserve the same factual content without adding, omitting, or changing a claim? | blocker | — | — | — | unresolved |
| 3 | R02 | Does the declared hierarchy avoid claiming more than the supported concept and explicit limits allow? | blocker | — | — | — | unresolved |
| 4 | R03 | Is the declared hierarchy a plausible structural fit for this executive brief? | blocker | — | — | — | unresolved |
| 5 | R04 | Does one variant plausibly present one governing point with support blocks beneath it? | blocker | — | — | — | unresolved |
| 6 | R05 | Does exactly one variant exhibit the declared hierarchy rather than the flat evidence-led plan? | blocker | — | — | — | unresolved |
| 7 | R05L | Which view exhibits that hierarchy: A, B, or none? | blocker | — | — | — | unresolved |
| 8 | R06 | Should the candidate remain inactive and leave the discovery-led boundary view untransformed? | blocker | — | — | — | unresolved |

## Deferred decisions and assumptions

- Deferred decisions: none.
- Assumptions: none. No prior-attempt answer, secret, timestamp, response, or witness will be inferred or reconstructed.

## Fresh-attempt state

- Attempt: `attempt-002`.
- Review started: `2026-08-26T16:28:58.214735Z`.
- Attempt 001 archive: `attempts/attempt-001/` with its commitment, packet, Markdown projection, gate, and all request/receipt pairs preserved.
- A fresh random mapping and nonce are held only by the active in-memory blinding process.
- The fresh commitment and packet are persisted; neither contains the mapping or nonce.
- `HUMAN-REVIEW-RESPONSE.json` and `HUMAN-REVIEW-AND-WITNESS.json` do not exist.
- Reveal remains forbidden until the response is complete and frozen.

## Current question

### R00 — Human attestation

Can you attest that you are a human reviewer and that, for attempt 002, you reviewed only the fresh blinded packet?

Admissible answers:

1. `confirm — reviewer_id: <identifier> — I am a human reviewer and reviewed only the fresh blinded packet.`
2. `defer`
3. `stop`

`explain` is also available and leaves R00 unresolved.
