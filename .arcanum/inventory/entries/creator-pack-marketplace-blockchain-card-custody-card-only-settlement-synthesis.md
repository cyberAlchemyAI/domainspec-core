---
tags: [inventory, research-program, research, findings, claim-proof, operational-evidence, schema, open-question, promotion-guardrail, public-private-boundary]
node_type: synthesis
is_session: false
layer: strategy
nature: synthesis
status: candidate
created: 2026-07-16
sources: [projects/creator-pack-marketplace/research/2026-07-15-gradedshop-and-fair-drop-mechanics/blockchain-card-custody-and-card-only-settlement.md, projects/creator-pack-marketplace/research/2026-07-15-gradedshop-and-fair-drop-mechanics/findings.md, projects/creator-pack-marketplace/README.md, https://www.lbma.org.uk/publications/the-otc-guide/precious-metal-accounts, https://www.royalmint.com/faqs/storage/what-is-the-allocated-storage-for-coins-and-bars/, https://eips.ethereum.org/EIPS/eip-721, https://eips.ethereum.org/EIPS/eip-1155, https://eips.ethereum.org/EIPS/eip-6956, https://eips.ethereum.org/EIPS/eip-7578, https://docs.chain.link/vrf, https://chain.link/proof-of-reserve, https://docs.openzeppelin.com/contracts/5.x/access-control, https://www.gov.br/fazenda/pt-br/composicao/orgaos/secretaria-de-premios-e-apostas/promocao-comercial/promocao-comercial, https://www.planalto.gov.br/ccivil_03/leis/l5768compilado.htm, https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14478.htm, https://www.gov.br/cvm/pt-br/acesso-a-informacao-cvm/perguntas-frequentes-da-cvm/criptoativos-quando-se-aplicam-as]
---

# Creator Pack Marketplace Blockchain Card Custody And Card-Only Settlement

> **Supersession notice (2026-07-16):** the accepted legal/payment gate and
> custodian RFP research reject an authoritative transferable ERC-721 for v1.
> The current RFP baseline is a personal non-transferable claim registry with
> signed custodian attestations; periodic public-chain Merkle anchoring is only
> optional tamper-evidence. See
> `creator-pack-marketplace-transferable-nft-custody-hypothesis-contradiction.md`.
> This page remains historical hypothesis evidence.

This is a non-authority Inventory read model. It captures the reusable result of
the card-custody research and does not approve implementation, legal
classification, payment architecture, or public launch.

## Core result

The strongest candidate is **allocated physical custody plus a card-redemption
NFT**. A professional custodian holds a specific inspected and insured card;
one digital claim maps to that card; a finite pack contract selects the claim
with verifiable randomness; the claim is locked or burned when delivery is
complete.

“Card-only settlement” means no customer cash-out, platform buyback, internal
wallet balance, guaranteed RTP, or monetary-return promise. It does not mean
that the business has no expenses or that external NFT resale is impossible.

## Build-from-owned analogy

LBMA’s allocated-account model identifies specific bars by unique number and
assay rather than giving an undifferentiated credit. The Royal Mint gives each
stored item a serial number and vault location. The card analogue is an
allocated card commitment:

```text
card_commitment = hash(serial + grade + evidence_hash + pack_version)
```

The commitment should be shared by the custodian register, manifest, NFT
metadata commitment, and redemption record. Unallocated “we will deliver an
equivalent card later” claims remain counterparty and substitution exposure.

## Candidate architecture

1. `CustodyRegistry`: commitment, custodian, reserve state, evidence hash,
   audit time, and redemption terms.
2. `CardNFT`: ERC-721 for unique cards; ERC-1155 for repeated identical units.
3. `PackController`: immutable manifest, finite inventory, purchase snapshot,
   randomness request, deterministic draw, and atomic decrement.
4. `RedemptionEscrow`: locks the claim through packing, shipping, and delivery.
5. `AttestationRegistry`: verifies custodian, carrier, auditor, and buyer
   signatures.
6. `DisputeAndRemedy`: timeout, damage, failed delivery, insurance, bond, and
   refund routes.

The proposed ERC-6956 and ERC-7578 patterns are useful design references for
physical anchors, oracle attestations, legal-owner disclosure, storage
information, and redemption terms. They are proposals, not a universal legal
standard.

## Verifiable lifecycle

```text
Deposited → Inspected → Allocated → Reserved
→ Drawn → Claimed → Packed → Shipped → Delivered → Redeemed
```

The draw record should bind `manifest_hash`, `state_root_before`, randomness
request/proof, draw number, selected commitment, and `state_root_after`.
Chainlink VRF is a possible proof-backed randomness source. Rejection sampling
or equivalent logic is required to avoid modulo bias.

For delivery, an attestation can bind `token_id`, `card_commitment`, custodian,
carrier, tracking hash, package-seal hash, timestamp, and recipient
confirmation. A two-of-three custodian/carrier/buyer confirmation is a stronger
candidate rule. The chain proves the attestation and state transition, not the
physical handoff by itself.

## Proof boundary

| Blockchain can verify | External custody still must establish |
|---|---|
| Token ownership and transfer | Card existence and authenticity |
| Manifest and odds commitment | Grade, condition, and provenance |
| Valid randomness and deterministic mapping | Segregated physical custody |
| No double allocation or double redemption | Insurance, damage, theft, and delivery |
| Signed delivery state transition | Honest custodian, carrier, and buyer attestations |

Reserve roots and circuit breakers can pause minting/draws when attestations are
stale or inventory is insufficient. They do not eliminate oracle, custodian, or
auditor trust.

## Product and money boundary

The intended customer result is a card or a redeemable card claim. The platform
should not expose cash-out, buyback, reusable wallet credit, RTP, or investment
appreciation claims. Reference value remains an estimate and may be below the
opening price; odds, shortfall, fees, shipping, and condition must be disclosed.

Public NFT transfer creates an external resale route even if the platform never
pays cash. A strict closed loop therefore needs platform-scoped transfers or an
explicit external-resale boundary.

## Legal residue

No-cash settlement reduces stored-value, payout, and liquidity complexity but
does not automatically remove paid-randomness risk. Brazil’s Ministry of
Finance describes authorization for commercial promotions involving draws,
“vale-brinde,” contests, or similar modalities, and Law 5.768/1971 covers
certain prize distributions. Law 14.478/2022 and CVM guidance make rights and
operation—not the label “NFT”—material to classification. Counsel must classify
the exact pack, custodian, token-transfer, and redemption flow before payment.

## Required controls

- no mint without a corresponding controlled card commitment;
- no two live claims for one commitment;
- immutable manifest and odds after first sale;
- append-only state and atomic decrement;
- tamper-evident serialized packaging;
- segregated inventory, audits, insurance, and remedy reserves;
- multisig, delayed administration, emergency pause, and no unilateral
  post-sale substitution;
- plain-language no-cash-guarantee disclosure;
- consumer refund, failed-delivery, dispute, and Article 49 treatment;
- no creator self-purchases, insider allocation, or wash trading.

## Open residue

- merchant/promoter/custodian/redemption-obligor identity;
- SPA classification and authorization path;
- public-wallet transfer policy;
- custody agreement, insolvency segregation, insurance, and audit standard;
- sufficient delivery signatures and timeout/dispute logic;
- post-reveal refund treatment;
- physical-anchor technology and replacement procedure;
- payment provider without an internal wallet or cash-out balance.

## Task fit

This entry supports a future finite-pool compiler, custody-registry design,
redemption state machine, delivery-attestation schema, verifier, legal/payment
decision gate, and custodian RFP. It does not promote a new canonical
definition or authorize a launch.

## Authority boundary

The project addendum and cited sources remain the evidence boundary. Inventory is
a compiled read model; Definitions Governance, Ontology Vault, legal counsel,
payment owners, and implementation/task-session routes retain their respective
authority.
