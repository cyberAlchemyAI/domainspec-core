# Stage 4 — Research decision

- **Owner:** `refine` · mode `research-if-gap-appears` · receipt: native-stage · **verdict: pass**

## Named gap

Interrogation item 5: how real ad networks (Meta, Google, TikTok, etc.) expose outcome metrics,
attribution windows, data export, and identifier sensitivity — external to the repository.

## Decision: **defer external research; design system-agnostic**

- A DEFINE/DESIGN/PLAN **seed** does not require committing to any one network's metric schema. The
  design uses `system_agnostic_standard`: a network-neutral outcome interface (an adapter contract)
  with concrete fields marked [H] to validate against a real network during the MVP pilot.
- This honors `research-if-gap-appears` (external research requires explicit confirmation, not yet
  given) without stalling the seed.
- **Recommended next route:** a `bounded-research` pass on one target network's outcome API + attribution
  model, run before the MVP pilot. Recorded as a next-route recommendation, not executed here.

## Confirmation status

External research **not run**. No user confirmation requested for an external pass; the gap is handled
by a system-agnostic adapter contract in Design. Operator may request the bounded pass at any time.
