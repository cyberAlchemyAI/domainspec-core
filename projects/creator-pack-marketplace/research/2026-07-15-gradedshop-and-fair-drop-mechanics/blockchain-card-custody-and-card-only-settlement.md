---
tags: [research-program, research, findings, claim-proof, operational-evidence, schema, open-question, promotion-guardrail, public-private-boundary]
node_type: research
is_session: false
layer: architecture
nature: reference
status: candidate
created: 2026-07-16
sources: [projects/creator-pack-marketplace/research/2026-07-15-gradedshop-and-fair-drop-mechanics/findings.md, https://www.lbma.org.uk/publications/the-otc-guide/precious-metal-accounts, https://www.royalmint.com/faqs/storage/what-is-the-allocated-storage-for-coins-and-bars/, https://eips.ethereum.org/EIPS/eip-721, https://eips.ethereum.org/EIPS/eip-1155, https://eips.ethereum.org/EIPS/eip-6956, https://eips.ethereum.org/EIPS/eip-7578, https://docs.chain.link/vrf, https://chain.link/proof-of-reserve, https://docs.openzeppelin.com/contracts/5.x/access-control, https://www.gov.br/fazenda/pt-br/composicao/orgaos/secretaria-de-premios-e-apostas/promocao-comercial/promocao-comercial, https://www.planalto.gov.br/ccivil_03/leis/l5768compilado.htm, https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14478.htm, https://www.gov.br/cvm/pt-br/acesso-a-informacao-cvm/perguntas-frequentes-da-cvm/criptoativos-quando-se-aplicam-as]
---

# Blockchain Card Custody And Card-Only Settlement

This is a source-backed design addendum to the creator-pack marketplace
research. It records a candidate custody and settlement model; it is not
implementation authorization, legal clearance, or a promise that the flow is
permitted in Brazil.

## Executive decision

The strongest model is **allocated physical custody plus a card-redemption
NFT**:

> One physical card is identified, inspected, insured, and held by a
> professional custodian. One digital token represents the holder's claim to
> redeem that exact card. A finite pack contract selects the card using
> verifiable randomness. The token is locked or burned when delivery is
> completed.

The customer-facing settlement is card-only. Customers may pay for an opening,
receive a card claim, and redeem a physical card, but the platform does not
promise buybacks, cash prizes, internal wallet withdrawals, or monetary return.

This removes the platform's customer cash-out and buyback obligation. It does
**not** mean that money can never leave the business: the custodian, creator,
payment provider, carrier, insurer, tax authorities, and refund processes still
need to be paid. “No customer cash-out” is the correct boundary.

## Scope assumption

“Custodian” means a professional third party that holds the physical cards in a
segregated, insured facility, maintains an item register, and accepts defined
redemption and delivery obligations. The blockchain records digital ownership,
rules, attestations, and state transitions; it does not physically hold the
cards.

## Gold custody analogy: allocated, not unallocated

The useful gold-market pattern is **allocated custody**. LBMA describes an
allocated account as backed by specific bars with unique numbers and assay
details; it is not an undifferentiated credit against the operator. The Royal
Mint similarly assigns each stored item a unique serial number and a vault
location ([LBMA allocated accounts](https://www.lbma.org.uk/publications/the-otc-guide/precious-metal-accounts),
[Royal Mint allocated storage](https://www.royalmint.com/faqs/storage/what-is-the-allocated-storage-for-coins-and-bars/)).

| Model | Card interpretation | Risk posture |
|---|---|---|
| Allocated | A named card commitment, grade, evidence set, and one-to-one token claim | Recommended for unique and high-value cards |
| Unallocated | A promise to deliver an equivalent card or category later | Counterparty, substitution, and insolvency exposure |
| Fractional / over-issued | More claims than controlled cards | Reject; violates the finite inventory invariant |

The card register should contain a private physical location but expose only a
commitment or redacted reference publicly:

```text
card_commitment = hash(serial + grade + evidence_hash + pack_version)
```

The same commitment must appear in the custodian register, the pack manifest,
the NFT metadata commitment, and the redemption record.

## Token and contract roles

### NFT standard

- **ERC-721**: one token for one unique physical card. This is the default for
  graded, rare, serialized, or individually redeemable cards.
- **ERC-1155**: repeated card types or common inventory where several identical
  units can be represented and transferred in batches.

ERC-721 standardizes unique token ownership and transfer; it does not itself
create a legal title to the physical card ([EIP-721](https://eips.ethereum.org/EIPS/eip-721)).
ERC-1155 supports multiple token types and batch operations ([EIP-1155](https://eips.ethereum.org/EIPS/eip-1155)).

### Contract components

1. **CustodyRegistry** — card commitment, custodian, reserve status, evidence
   hash, audit timestamp, and redemption terms.
2. **CardNFT** — the ERC-721 claim for an individually allocated card, or the
   ERC-1155 inventory representation for repeated cards.
3. **PackController** — immutable pack manifest, finite remaining inventory,
   purchase state, randomness request, and deterministic selection.
4. **RedemptionEscrow** — locks the claim while packing, shipping, and delivery
   evidence are completed.
5. **AttestationRegistry** — verifies authorized custodian, carrier, auditor,
   and buyer signatures.
6. **DisputeAndRemedy** — timeout, damage, failed-delivery, refund, insurance,
   and custodian-bond routes.

Role-based access, delayed administration, and an emergency pause are required
for privileged actions; OpenZeppelin documents `AccessControl`, `AccessManager`,
and related control patterns ([OpenZeppelin Access Control](https://docs.openzeppelin.com/contracts/5.x/access-control)).

## Card lifecycle

```text
Deposited → Inspected → Allocated → Reserved
→ Drawn → Claimed → Packed → Shipped → Delivered → Redeemed
```

Required invariants:

- no token is minted without a corresponding controlled card commitment;
- a card commitment cannot be assigned to two live claims;
- manifest and odds cannot change after first sale;
- a draw decrements the finite state atomically;
- a redeemed card cannot be drawn again;
- the claim remains live if shipping fails;
- the physical card leaves custody only through the redemption process.

## Random selection

The pack should commit an immutable manifest before sales. A verifiable random
source such as Chainlink VRF can supply a proof-backed random value that the
contract verifies before consuming it ([Chainlink VRF](https://docs.chain.link/vrf)).

At state `s`, the verifier maps the random value to the canonical ordered list
of remaining card commitments. The mapping must use rejection sampling or an
equivalent method so modulo reduction does not introduce bias. The draw record
should bind:

```text
manifest_hash
state_root_before
randomness_request_id
randomness_proof
draw_number
selected_card_commitment
state_root_after
```

This proves selection integrity. It does not prove that the custodian's card,
grade, or valuation is honest.

## Delivery evidence

The NFT should not be burned when it is merely selected. It should be locked in
redemption escrow until the delivery workflow reaches its defined terminal
state.

A delivery attestation can contain:

```text
delivery_id
token_id
card_commitment
custodian_id
carrier_id
tracking_hash
package_seal_hash
timestamp
recipient_confirmation
```

The contract emits a `DeliveryAttested` event only after the authorized
attestation is verified. A stronger rule requires two of three confirmations:

```text
custodian + carrier
custodian + buyer
carrier + buyer
```

If delivery fails, the claim remains redeemable and the custodian's insurance,
bond, or remedy reserve handles the failure. The exact remedy must be specified
before sale.

The blockchain can prove that the required signatures and state transitions
were recorded. It cannot independently prove that a courier handed over an
authentic card. That remains a custodian, carrier, and dispute-system
responsibility.

## Reserve and physical-anchor controls

For cards, a reserve count alone is insufficient. The custodian should publish
or attest to a versioned inventory root over individual card commitments. A
reserve failure or stale attestation should pause minting and new draws.

Proof-of-reserve systems illustrate this pattern: off-chain reserve data is
relayed on-chain and can trigger a circuit breaker when backing falls below
requirements ([Chainlink Proof of Reserve](https://chain.link/proof-of-reserve)).
This remains an oracle and custodian trust boundary, not a replacement for an
independent audit.

Physical cards should use tamper-evident serialized packaging and inspection
evidence. The proposed asset-bound NFT model describes physical anchors and
oracle attestations, while warning that ordinary barcodes and NFC tags can be
replicated ([EIP-6956](https://eips.ethereum.org/EIPS/eip-6956)). The physical
anchor is therefore evidence, not a standalone guarantee.

## Card-only settlement boundary

### Allowed

- fiat payment for an opening through an approved payment flow;
- card claim or NFT transfer;
- in-platform card/NFT exchange if allowed by policy;
- redemption of the claim for the corresponding physical card;
- refunds and consumer remedies where legally required.

### Not part of the v1 model

- user cash-out;
- platform buyback;
- internal wallet balance or reusable money-like credits;
- guaranteed RTP or return percentage;
- promise that reference value equals cash proceeds;
- creator or platform profit claim attached to token appreciation.

Do not call the initial reference-value ratio “RTP.” Existing research defines
that ratio as a descriptive estimate, not a funded cash guarantee. A card-only
system can still have a low-value outcome below the opening price; removing
cash-out does not remove the need to disclose odds, shortfall frequency, fees,
shipping, and condition.

If NFTs are transferable to public wallets, owners may sell them for money in an
external market. A strict closed loop therefore needs either platform-scoped
transfers or an explicit statement that external resale is outside platform
control.

## Legal and consumer boundary

No-cash settlement reduces payment, stored-value, and liquidity complexity. It
does not automatically turn paid random selection into an ordinary sale.

Brazil’s Ministry of Finance describes commercial promotions involving draws,
“vale-brinde,” contests, or similar modalities and provides the authorization
route through SCPC ([SPA commercial promotions](https://www.gov.br/fazenda/pt-br/composicao/orgaos/secretaria-de-premios-e-apostas/promocao-comercial/promocao-comercial)).
Law 5.768/1971 requires prior authorization for certain prize distributions by
draw or similar operation ([Law 5.768/1971](https://www.planalto.gov.br/ccivil_03/leis/l5768compilado.htm)).

Law 14.478/2022 includes custody or administration of virtual assets among
virtual-asset services while excluding some product/service-access instruments;
classification depends on the rights and operation ([Law 14.478/2022](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14478.htm)).
The CVM emphasizes that token classification depends on the rights and public
offering structure, not on the label “NFT” ([CVM cryptoasset guidance](https://www.gov.br/cvm/pt-br/acesso-a-informacao-cvm/perguntas-frequentes-da-cvm/criptoativos-quando-se-aplicam-as)).

This is issue spotting, not legal advice. Before taking payment, obtain a
written classification of the exact pack, custodian, token-transfer, and
redemption flow.

## Recommended v1 boundary

Build after legal/payment gating:

- finite pre-custodied inventory;
- allocated card commitments;
- ERC-721 claims for unique cards;
- immutable manifest and append-only state;
- verified randomness and replay verifier;
- redemption escrow and delivery attestations;
- custody audits, insurance, reserves, and dispute remedies;
- plain-language odds and no-cash-guarantee disclosures.

Do not build for launch:

- unallocated “we will find an equivalent card later” promises;
- more claims than controlled cards;
- arbitrary post-sale odds changes;
- cash-out, buyback, or guaranteed RTP;
- creator self-purchases or wash trading;
- mutable metadata as the only authenticity evidence;
- public marketing that implies investment appreciation.

## Open residue

- Which legal entity is merchant, promoter, custodian, and redemption obligor?
- Does SPA classify the paid randomized pack as a promotion, lottery, ordinary
  aleatory sale, or another operation?
- Is the NFT transfer restricted to the platform or open to public wallets?
- What custody agreement, insurance, insolvency segregation, and audit standard
  will bind the professional custodian?
- What exact buyer, carrier, and custodian signatures are sufficient for
  delivery, and what is the timeout/dispute path?
- What refund treatment applies after an irreversible reveal?
- What card-anchor technology survives duplication, replacement, and damage?
- Which payment provider can support customer payment without an internal
  wallet or cash-out balance?

## Source boundary

The gold sources supply the allocated-custody analogy. Ethereum EIPs and
OpenZeppelin supply token and access-control interfaces. Chainlink sources
describe implementation patterns for randomness and reserve attestations.
Brazilian government and regulator sources supply issue-spotting boundaries.
The local [fair-drop findings](findings.md) remain the primary project synthesis
for probability, economics, and prior legal blockers.
