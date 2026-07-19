---
tags: [inventory, strategy-result, dispatch, subagents, research, claim-proof, operational-evidence, non-collapse, open-question, promotion-guardrail]
node_type: synthesis
is_session: false
layer: strategy
nature: synthesis
status: verified
created: 2026-07-16
dispatch_id: 2026-07-16-creator-pack-custodian-requirements
dispatch_type: research
working_folder: projects/creator-pack-marketplace/research/2026-07-16-professional-card-custodian-rfp/
sources: [projects/creator-pack-marketplace/research/2026-07-16-professional-card-custodian-rfp/research.md, projects/creator-pack-marketplace/research/2026-07-16-professional-card-custodian-rfp/findings.md, projects/creator-pack-marketplace/research/2026-07-16-legal-payment-decision-gate/findings.md, telemetry/agents/subagents-dispatch.yaml]
---

# Creator Pack Marketplace Professional Card Custodian RFP

This is a non-authority Inventory read model of the resolved research dispatch
`2026-07-16-creator-pack-custodian-requirements`. It preserves an
auditor-accepted procurement and pilot baseline. It selects no custodian,
vendor, legal route, insurer, PSP, blockchain, or production architecture.

## P1 Trigger Decision

Dispatch was required because professional custody is a multi-party evidence
system, not a warehouse feature. The work crossed exact-object allocation,
title and insolvency, collectible handling, insurance, cash reserves,
attestations, state-machine reversals, fulfillment, privacy, key management,
audit, continuity, and optional blockchain commitments.

## Lanes And Subagents

- Three explorers compared allocated custody and insolvency controls, physical
  collectible custody and delivery evidence, and registry/attestation/chain
  architectures.
- One synthesizer produced the RFP and pilot model.
- Three skeptics attacked legal/insolvency, physical/insurance/logistics, and
  protocol/security evidence boundaries.
- One writer produced `findings.md`; one independent auditor returned
  `ACCEPT`.

The dependency flow was
`explorers -> synthesizer <-> reviewers -> writer -> auditor`; one bounded loop
was used and no helper roles were used.

## Gate And Ledger State

- Phase 2 ran only after Phase 1 closed with an accepted `HOLD/KILL` gate.
- Two independent tension checks returned `PASS` and the user confirmed the
  frozen dispatch sheet.
- The ledger contains one dispatch row and one resolved close row.
- Closeout recorded nine governed roles, zero helpers, one loop, and final
  auditor result `ACCEPT`.

## Accepted Result

The v1 RFP baseline is professional third-party custody with one individually
allocated exact card, a centralized personal non-transferable claim registry,
signed custodian attestations, and an append-only event log. It remains `HOLD`
pending counsel, insurer, auditor, PSP, security, and vendor validation.

The candidate matrix is:

- **A — allocated custody + personal registry + signed attestations:** `HOLD`,
  the RFP baseline.
- **B — A plus periodic public-chain Merkle commitments:** `HOLD`, an optional
  `SHOULD` for inclusion, order, consistency, and non-deletion evidence only.
- **C — opaque locked ERC status witness:** `DEFER`; it cannot become the
  authoritative claim, title, or release control.
- **D — authoritative transferable ERC-721:** `KILL v1`.
- **E — pooled inventory or equivalent-card substitution:** `KILL`.
- **F — creator self-custody or procurement after allocation:** `KILL`.

A chain can verify scoped digital authorship, ordering, commitment inclusion,
authorization, and non-deletion. It cannot verify physical existence, title,
authenticity, grade, condition, insurance, continuous custody, or intact
delivery. Lawful refunds and redemption must continue during chain outage.

## RFP And Pilot Boundary

The accepted findings define a weighted 100-point RFP: title/segregation/exit
20; collectible custody/fulfillment 20; state/API/attestations 15;
insurance/reserve 15; audit/continuity/default 12; security/privacy/keys 10;
capacity/cost 8. Passing requires at least 80/100, at least 60% in every domain,
and no disqualifier.

Disqualifiers include pooled or substitutable inventory, creator self-custody,
an authoritative or transferable token, claim/title conflation, no independent
exact-card witness, undisclosed liens/subcustodians, insurance treated as the
refund reserve, no atomic refund-release interlock, no independent audit, no
portable export/step-in path, chain availability gating a lawful remedy, public
PII/location, single-person removal power, or refusal to run adversarial tests.

Provisional pilot numbers include 24-hour attestation TTL, live checks within
15 minutes, key pause within 5 minutes, revocation within 15 minutes, registry
RTO within 4 hours, logical export within 24 hours, supervised removal within
10 business days, 100% scheduled per-card insurance, and a separately funded
monetary reserve. The `CARD-0001` R$10,000 case is a stress/insurance witness,
not a promised payout or legal-entitlement decision.

## Source Refs

- `projects/creator-pack-marketplace/research/2026-07-16-professional-card-custodian-rfp/research.md`
  preserves the three explorer returns verbatim.
- `projects/creator-pack-marketplace/research/2026-07-16-professional-card-custodian-rfp/findings.md`
  contains the accepted proof glossary, scorecard, due-diligence list, contract
  clauses, responsibility matrix, parameters, state machines, and pilot suite.
- `projects/creator-pack-marketplace/research/2026-07-16-legal-payment-decision-gate/findings.md`
  supplies the controlling pre-money and non-transferable-claim boundary.
- `telemetry/agents/subagents-dispatch.yaml` records the confirmed dispatch and
  resolved closeout.

## Next Human Action

Issue a market-sounding RFI, then the evidence-scored RFP, to professional
custody candidates. Require proof against the exact CARD-0001 success, refund,
chargeback, loss, key-compromise, and custodian-default witnesses. Do not run a
real-money pilot until the legal/payment gate closes independently.
