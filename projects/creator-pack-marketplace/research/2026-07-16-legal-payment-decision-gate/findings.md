---
title: Creator Pack Marketplace — Legal And Payment Decision Gate
status: candidate-findings
created: 2026-07-16
dispatch_id: 2026-07-16-creator-pack-legal-payment-gate
dispatch_type: research
jurisdiction: Brazil
---

# Goal

Define the legal, payment, tax, consumer-remedy, and operational decisions that
must be recorded before the creator-pack marketplace accepts money. The object
is a finite, versioned, pre-custodied inventory of physical cards allocated by
randomness. These findings do not provide legal advice, legal clearance, PSP
acceptance, tax advice, vendor selection, or implementation approval.

# TL;DR

No researched path is cleared to take money. The surviving paths are four
different fact patterns, not interchangeable labels:

- **A:** the platform sells one unidentified physical card from a finite
  pre-custodied manifest and issues a non-transferable exact-card redemption
  claim after allocation;
- **B:** a creator is the real seller through a PSP-approved connected
  marketplace settlement flow;
- **D:** a genuinely free, non-binding random offer is generated before an
  optional purchase of the identified card; and
- **E:** an independently valuable base product carries a gratuitous prize
  under an actually authorized SPA plan.

All four remain **HOLD**. A is precedent-clean as a composite, B is materially
weaker because the seller label must survive the actual money and remedy flow,
D has an unowned safe-harbor theory, and E exists only inside the exact
authorized plan. A Civil Code aleatory-contract category is not permission for
a paid random pack. “Everyone receives a card,” professional custody,
blockchain transparency, and no voluntary cash-out do not decide the legal
classification ([Agent 1, Central classification tension](research.md#central-classification-tension),
[Civil Code arts. 458–461](https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm),
[Contraventions Law arts. 50–51](https://www.planalto.gov.br/ccivil_03/decreto-lei/del3688.htm),
[SPA commercial-promotion guidance](https://www.gov.br/fazenda/pt-br/composicao/orgaos/secretaria-de-premios-e-apostas/promocao-comercial/promocao-comercial)).

Transferable NFT/external-transfer path C and money-like path F are **KILL for
v1**. Mandatory refunds and reversals are not cash-out and cannot be designed
away. Legal classification, PSP acceptance, consumer remedies, tax treatment,
and custody evidence are independent gates ([Agent 2, Central finding](research.md#1-status-legend-and-central-finding),
[Agent 3, Explicit disagreement findings](research.md#explicit-disagreement-findings)).

# Evidence boundary

The primary local evidence is the three verbatim explorer returns in
[`research.md`](research.md): Agent 1 maps Brazilian doctrine and current
official authority; Agent 2 stress-tests transaction variants, title, and
classification-changing facts; Agent 3 reconstructs payment, reversal, and PSP
operations. This synthesis uses the following evidence classes:

- **Binding authority:** enacted legislation or regulation. It binds within
  its scope but does not, by citation alone, classify this untested product.
- **Regulator guidance:** an official regulator explanation or administrative
  surface; useful for the authority's present position, not a substitute for a
  decision on the exact facts.
- **PSP/network policy:** private underwriting, coding, settlement, or dispute
  rules. Acceptance can be stricter than legal permissibility.
- **Inference:** a reasoned application of those materials to a specified
  candidate. It remains unapproved.
- **Unknown:** the source corpus does not resolve the question.
- **Professional decision:** a dated written answer required from Brazilian
  counsel, a licensed PSP/acquirer, tax counsel, SPA, or another named owner.

Currentness is 16 July 2026. In particular, STF Theme 924 remains a live-docket
dependency and must be checked again immediately before counsel signs the
classification; this file does not freeze its status ([Agent 1, Central
classification tension](research.md#central-classification-tension), [STF Theme
924 docket](https://portal.stf.jus.br/jurisprudenciaRepercussao/verAndamentoProcesso.asp?classeProcesso=RE&incidente=4970952&numeroProcesso=966177)).

# Corrected invariant

> Customers receive no reusable monetary balance and cannot voluntarily convert a platform claim into money through platform cash-out, cash redemption, resale, or buyback. The exact-card claim is non-transferable. This does not restrict mandatory refunds, withdrawal remedies, chargebacks, reversals, taxes, creator/vendor payments, or operating expenses. No expected-value disclosure is called or guaranteed as RTP.

This corrects the earlier phrase “money never leaves the system.” Refunds,
chargebacks, supplier payments, taxes, custody, insurance, and delivery all
move money; the controlled boundary is the absence of a voluntary customer
monetization loop ([Agent 2, Central finding](research.md#1-status-legend-and-central-finding),
[Agent 3, Executive determination](research.md#executive-determination),
[CDC arts. 18, 35 and 49](https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm)).

# Exact candidate fact patterns

## A — Platform seller, paid random physical-card sale

The platform sells one as-yet-unidentified physical card from a versioned,
finite, pre-custodied manifest. Allocation occurs without replacement. After
allocation, the platform records a personal, non-transferable, single-use claim
to that exact card. The **sale object is the physical card**; the claim is
redemption evidence, not legal title, custody, possession, grade, authenticity,
or value. Title and tradition require their own event and evidence under the
selected contract structure ([Agent 2, Fact-pattern decision tree §6](research.md#2-fact-pattern-decision-tree),
[Civil Code arts. 481, 1,226 and 1,267](https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm)).

## B — Creator seller, paid random marketplace sale

B has the same paid random allocation, but each creator is the actual owner,
offeror, invoice issuer, remedy obligor, and seller. Checkout and settlement use
a PSP-approved connected marketplace architecture; platform and creator money
must never be pooled and manually repassed. The creator-seller classification
survives only when offer, ownership, PSP merchant record, fiscal document,
payout, refund, chargeback, and delivery evidence all agree. Otherwise B
collapses to A. STJ passive-classifieds cases are rejected as analogies because
the proposed platform approves inventory, controls RNG, participates in
checkout, and operates claims/remedies ([Agent 1, Consumer and marketplace
responsibility](research.md#consumer-and-marketplace-responsibility), [STJ REsp
1.836.349/SP](https://www.stj.jus.br/websecstj/cgi/revista/REJ.cgi/ITA?CodOrgaoJgdr=&SeqCgrmaSessao=&dt=20220624&formato=HTML&nreg=201901346226&salvar=false&seq=2181939&tipo=0),
[Agent 3, Fund-flow candidate B](research.md#b-creator-is-the-seller-platform-is-marketplace)).

## C — Transferable NFT or external claim transfer

C permits the claim to move to an external wallet or another holder. The token
may own token/service components; it cannot prove card existence, title,
authenticity, condition, custody, or delivery. Product-access exclusion,
virtual-asset treatment, and securities treatment depend on rights and actual
operation, not the NFT label ([Agent 1, Scenario-sensitive classification
matrix](research.md#scenario-sensitive-classification-matrix), [Law
14.478/2022](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14478.htm),
[CVM Guidance Opinion 40](https://conteudo.cvm.gov.br/export/sites/cvm/legislacao/pareceres-orientacao/anexos/Pare040.pdf)).

## D — Free offer before optional identified-card purchase

The platform generates and immediately reveals a free, non-binding randomized
offer before any payment authorization, deposit, fee, balance, credit,
membership consideration, or buyer entitlement. The customer may reject it
without paid reroll, lost entitlement, economic cooldown, reduced future
access, or penalty. A seller-funded reservation may temporarily hold the card;
no title, token, claim, redemption right, or buyer entitlement exists until the
optional ordinary checkout for the identified card ([Agent 2, Fact-pattern
decision tree §1](research.md#2-fact-pattern-decision-tree)).

## E — Independently valuable base product plus gratuitous prize

The buyer purchases an independently valuable base product; a gratuitous prize
is distributed only under the actual SPA-approved modality, certificate, and
plan. The promoter must have the required status and prize ownership evidence,
and the sale and prize use separate ledgers. The instant-random or collection-
series mechanics must remain within the published authorized modality; an
“analogous to vale-brinde” operation cannot simply substitute arbitrary RNG
([Agent 1, Central classification tension](research.md#central-classification-tension),
[Law 5.768/1971](https://www.planalto.gov.br/ccivil_03/leis/l5768compilado.htm),
[SPA legislation index](https://www.gov.br/fazenda/pt-br/composicao/orgaos/secretaria-de-premios-e-apostas/promocao-comercial/legislacao/promocoes-comerciais)).

## F — Monetary promise or reusable value

F includes stored value, reusable credit, voluntary cash-out, cash redemption,
platform buyback, or guaranteed RTP. Each is separate from mandatory refund or
chargeback. A descriptive reference-value ratio is not RTP. This path has no
authorized, funded, evidence-backed owner in the current record and contradicts
the corrected invariant ([Agent 3, Wallet, stored-value and NFT boundary](research.md#wallet-stored-value-and-nft-boundary),
[Law 12.865/2013](https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/lei/l12865.htm)).

# Candidate verdict matrix

Precedent only determines ownership; it does not itself emit KILL. `HOLD`
means unresolved professional and operational decisions, never approval or a
preferred route.

| Candidate | Owner/precedent | Witnessed | Sound | Verdict |
|---|---|---|---|---|
| **A — platform seller** | Composite is precedent-clean. Civil Code aleatory categories are context, not approval; card sale, custody, consumer, payment, and claim components do not own the whole arrangement ([Agent 1, Central classification tension](research.md#central-classification-tension)). | Partial. Needs the complete state and reversal witness below, platform cash reserve, physical insurance/bond, title/tradition proof, and authenticity/condition remedies. | Conditional only if claim, title, custody, grade, authenticity, value, insurance, and money remedies remain distinct. | **HOLD** |
| **B — creator seller** | Build-from-owned only for BCB payment-role and connected-settlement components; passive-classifieds STJ precedents do not own this controlled marketplace ([Agent 3, Fund-flow candidate B](research.md#b-creator-is-the-seller-platform-is-marketplace)). | Partial. Requires charge type, payout delay, collateral/recovery, platform backstop, loss waterfall, and a complete reversal witness. | Materially weaker. Seller identity must agree across ownership, offer, invoice, PSP flow, remedies, and ledger or B collapses to A. | **HOLD** |
| **C — transferable NFT** | Only token/regulatory components are owned. Counsel must live-check BCB Resolutions [519](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?numero=519&tipo=Resolu%C3%A7%C3%A3o+BCB), [520](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?numero=520&tipo=Resolu%C3%A7%C3%A3o+BCB), [521](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?numero=521&tipo=Resolu%C3%A7%C3%A3o+BCB), later amendments including [580](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?numero=580&tipo=Resolu%C3%A7%C3%A3o+BCB), and the CVM perimeter; none proves physical facts. | **No. Exact zeroing fact:** no evidenced enforceable owner-controlled transition prevents monetary reversal by the original payer plus physical redemption by another holder after transfer. | Transferable-token finality and consumer/payment reversibility conflict in the supplied witness. | **KILL v1** |
| **D — free offer first** | Ordinary identified-card checkout is owned; the free-allocation safe-harbor theory is unowned ([Agent 2, Scenario comparison](research.md#3-scenario-comparison)). | Partial. Requires proof of no pre-allocation consideration or entitlement and seller-funded reservation only. | Conditional; any fee, hold, credit, paid reroll, membership consideration, access loss, economic cooldown, or penalty restores the unresolved paid-random facts. | **HOLD** |
| **E — base product plus prize** | Owned only by an actual SPA certificate and exact accepted plan, not by generic promotion guidance ([Agent 1, Hard-stop conditions](research.md#hard-stop-conditions)). | Partial. Requires promoter, title/custody, separate sale/prize ledgers, withdrawal/chargeback/loss/default remedies, reserve, and insurance. | Conditional. KILL trigger if the base product is nominal, the buyer substantively pays for chance, or RNG falls outside the authorized modality. | **HOLD** |
| **F — stored value/cash-out/buyback/RTP** | Payment and financial rules describe possible regulated components; they do not permit a pack or own its monetary promise ([Agent 3, Wallet boundary](research.md#wallet-stored-value-and-nft-boundary)). | **No. Exact zeroing fact:** no authorized owner or funded evidence-backed mechanism exists for the monetary promise, and the promise contradicts the invariant. | Collapses card-only settlement into a reusable or voluntary monetary exit. Mandatory refunds remain separate. | **KILL v1** |

# Authority and classification matrix

| Question | Evidence class and current finding | Required decision |
|---|---|---|
| Paid random allocation | **Binding authority + regulator guidance:** Civil Code arts. 458–461 recognize aleatory contracts; Contraventions Law arts. 50–51 and Law 14.790 use chance/value concepts; SPA presents commercial promotion as free prize distribution. None classifies A or B ([Agent 1, Central classification tension](research.md#central-classification-tension), [Law 14.790/2023](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14790.htm)). | Brazilian consumer and criminal/gaming counsel classify each exact witness; SPA decides only where its authority/modalities apply. |
| Consumer withdrawal and defects | **Binding authority:** CDC offers/remedies and distance-sale withdrawal remain applicable; no source establishes an irreversible-reveal exception. Required refund is not voluntary cash-out ([Agent 1, Scenario matrix](research.md#scenario-sensitive-classification-matrix), [CDC](https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm), [Decree 7.962/2013](https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/decreto/d7962.htm)). | Consumer counsel fixes cancellation, reveal, return, authenticity/condition, failed-delivery, and refund rules per state. |
| Seller/platform role | **Authority + inference:** supplier responsibility follows actual functional participation; passive listings precedent does not match platform-run RNG/payment/remedy control ([Agent 1, Consumer responsibility](research.md#consumer-and-marketplace-responsibility)). | Consumer/tax counsel and PSP record one consistent merchant, seller, supplier, invoice issuer, and loss bearer. |
| Payment architecture | **Regulator guidance + PSP policy:** receiving and repassing seller money can trigger subcredenciador treatment; the actual payer relationship controls. PSP acceptance remains independent ([Agent 3, Executive determination](research.md#executive-determination), [BCB centralized-settlement FAQ](https://www.bcb.gov.br/estabilidadefinanceira/faq-liquidacao-centralizada), [BCB Resolution 150](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?numero=150&tipo=Resolu%C3%A7%C3%A3o+BCB)). | Licensed PSP/acquirer approves merchant role, MCC/coding, split, reserves, payout, dispute evidence, and change triggers in writing. |
| Token/claim | **Binding/regulator perimeter + unknown:** a non-transferable exact-product claim may support the product-access exclusion; external transfer materially changes the analysis. CVM classification is functional ([Agent 1, Payment/virtual assets](research.md#payment-virtual-assets-and-amlkyc)). | BCB/CVM counsel records the rights, transfer controls, administrator powers, marketing, wallet, and secondary-market perimeter before any token issuance. |
| Tax/fiscal treatment | **Binding authority + professional unknown:** platform control, sale/service role, physical-goods documents, commissions, and 2026 IBS/CBS transition affect duties ([Agent 1, Tax](research.md#tax-fiscal-documents-and-invoicing), [LC 214/2025 compiled](https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp214compilado.htm), [NF-e portal](https://www.nfe.fazenda.gov.br/portal/informe.aspx)). | Tax counsel fixes entity, supply, NCM/ICMS, invoice/document, title-transfer timing, commission, prize withholding if any, and DeCripto applicability. |
| Minors/marketing | **Binding authority + unresolved scope:** youth-access and child-directed collectible appeals create additional restrictions; physical-card scope is not resolved by the corpus ([Agent 1, Scenario matrix](research.md#scenario-sensitive-classification-matrix), [Law 15.211/2025](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/l15211.htm), [Decree 12.880/2026](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/d12880.htm)). | Specialist counsel approves age assurance, access, advertising, disclosures, and launch territory. |

# Payment architecture

Only two coherent architectures continue to professional review:

1. **A/platform seller:** buyer pays a licensed PSP; the PSP settles the
   platform's receivable subject to fees/reserve; platform pays creators as
   vendors and separately pays custodian, carrier, insurer, and taxes. Refunds
   return through the original payment rail; chargebacks debit the platform.
2. **B/creator seller:** buyer uses a PSP-hosted connected-seller/marketplace
   flow; the PSP settles the creator's approved net amount and the disclosed
   platform fee while preserving the agreed reversal reserve. The PSP contract
   names who bears negative balances and when the platform backstop applies.

The rejected hybrid calls the creator the seller while the platform receives
pooled proceeds, controls the descriptor and refunds, and later repasses money
from its bank account. That structure contradicts the factual role test and
raises unauthorized payment-service/omnibus-account concerns ([Agent 3,
Executive determination](research.md#executive-determination), [BCB warning on
unauthorized payment services and contas-bolsão](https://www.bcb.gov.br/detalhenoticia/20906/nota)).

Before selection, the record must bind `order_id`, candidate, seller, merchant,
manifest version, price/fees, PSP charge type, authorization, and applicable
cancellation state. B additionally binds `connected_seller_id`, seller bank
account, payout delay, reserve/collateral, recovery right, invoice, platform
backstop, and loss-waterfall version. Network/PSP underwriting sees the real
jackpot, custody, claim, and refund UI; no generic collectibles account is used
as a trial ([Agent 3, Minimum PSP/acquirer question set](research.md#minimum-pspacquirer-question-set),
[Visa Core and Product Rules](https://www.visa.com.br/content/dam/VCOM/download/about-visa/visa-rules-public.pdf),
[Stripe restricted businesses](https://stripe.com/br/legal/restricted-businesses)).

# Lifecycle and reversal model

The minimum success state machine for A/B is:

```text
available → allocated → claimed → redemption-locked → shipped → delivered
```

It must also implement explicit `cancelled`, `refund-pending`, `refunded`,
`chargeback-open`, `reversed`, `return-pending`, `returned`, `lost`, `damaged`,
`authenticity-dispute`, `delivery-dispute`, and `custodian-default` states. No
state is terminal merely because a card was revealed.

| Transition or failure | Atomic rule | Evidence and remedy owner |
|---|---|---|
| `available → allocated` | One exact card is removed once from the versioned manifest; no over-issuance or substitution. | Platform pack ledger plus custodian allocation evidence. |
| `allocated → claimed` | Issue one non-transferable personal claim; it is not title. | Platform claim registry; seller/title evidence remains separate. |
| `claimed → redemption-locked` | Lock claim before the card can leave custody. | Platform/custodian reconciliation. |
| Refund, withdrawal, or reversal | **Atomic refund-vs-redemption exclusion:** a refund cannot finalize while shipment/redemption can proceed, and a redeemed/delivered card cannot silently produce a duplicate refund. Statutory/network rights still govern exceptions. | PSP/payment ledger, platform cash reserve, counsel-approved return/recovery route. |
| `redemption-locked → shipped → delivered` | Shipment requires exact-card, package, carrier, and custody-release evidence; delivery evidence must also satisfy PSP/network disputes. | Custodian/carrier records; seller/platform remains the named consumer-remedy obligor. |
| Loss, damage, authenticity/condition dispute | Preserve claim/dispute state; never substitute an “equivalent” card without an expressly lawful remedy choice. | Physical insurance/bond and seller/platform remedy; **not** the refund cash reserve. |
| Creator or custodian default | Stop new allocation, preserve all records, activate payout hold/backstop/loss waterfall, and offer the counsel-approved physical remedy or monetary reversal. | Platform, PSP, insurer/bond, custodian, and named seller according to signed allocation. |

The cash reserve backs purchase-price refunds, reversals, disputes, fees, and
negative balances. Physical insurance/bond backs loss, damage, theft, and the
insured card obligation. One cannot be counted as the other ([Agent 3,
Transaction lifecycle](research.md#transaction-lifecycle-and-obligations)).

# Counsel, PSP, and tax decision record

The launch record must be dated, versioned, signed, and tied to UI, terms,
money/title/custody diagrams, one success witness, and every failure path. A
change in price, odds, jackpot, seller type, territory, token rights, custody,
or refund behavior reopens the applicable decision.

| Decision | Owner | Required recorded output |
|---|---|---|
| Classify A, B, D, and conditional E; state KILL triggers | Brazilian consumer + criminal/gaming counsel; SPA where applicable | Authority, facts assumed, conclusion per candidate, restrictions, expiry, and change triggers; live STF Theme 924 check. |
| Fix seller, supplier, promoter, title/tradition event, redemption obligor, and Article 49/defect/failure remedies | Consumer/commercial counsel | State-by-state legal lifecycle and exact contract/UI clauses. |
| Classify claim/token and administrator functions | Virtual-asset/securities counsel; BCB/CVM route as required | Written treatment of non-transferability, product-access exclusion, BCB Resolutions 519–521 and later amendments including 580, CVM perimeter, AML/KYC, and prohibited changes. |
| Approve payment flow | Licensed PSP/acquirer | Merchant role, MCC/coding, charge model, seller onboarding, centralized settlement, reserves, payout delay, refunds, chargebacks, evidence, volume/territory limits, and change triggers. |
| Fix fiscal treatment | Brazilian tax counsel/accounting owner | Invoice issuer and description, title/supply timing, NCM/ICMS, service commission, IBS/CBS transition, prize withholding if E, DeCripto, creator/custodian/carrier treatment, and reconciliation fields. |
| Approve custody constraints | Counsel plus later custodian diligence—not Phase 1 | Agreement requirements for title separation, allocated possession, evidence, insurance, audit, release, incidents, default, return, and PSP dispute support. |

# Pre-money stops

No pilot may accept real money until all applicable items are evidenced:

1. A dated written classification exists for the exact chosen fact pattern and
   failure paths; SPA authorization and exact plan exist if E is used.
2. Seller, supplier, promoter, merchant, invoice issuer, title-transfer event,
   redemption obligor, and loss bearer agree across terms, PSP records, fiscal
   documents, and ledgers.
3. Consumer counsel has approved cancellation, reveal, withdrawal, return,
   defect/authenticity, loss, delivery failure, and refund handling; no
   “revealed means non-refundable” shortcut exists.
4. A licensed PSP/acquirer has approved the production-equivalent UI, odds,
   jackpot, custody, token/claim, merchant category, transaction coding,
   settlement, seller onboarding, reserves, payout, and dispute flow in writing.
5. Tax counsel has fixed invoices, supply/title timing, commissions, applicable
   taxes/withholding, and reconciliation.
6. One exact card maps to one manifest entry and one non-transferable claim;
   title, custody, authenticity, grade, value, insurance, and claim fields are
   separately evidenced. No external transfer, substitution, or over-issuance.
7. Cash reserves and physical insurance/bond are separately funded and
   stress-tested for concurrent refund, chargeback, loss, damage, seller
   default, and custodian default.
8. The complete state machine, atomic refund-vs-redemption exclusion, return
   route, payout hold/recovery, delivery evidence, and loss waterfall pass a
   no-money production-equivalent test.
9. No reusable balance, cross-seller credit, cash-out, cash redemption,
   platform resale/buyback, guaranteed RTP, transferable NFT, pooled third-party
   account, or investment/appreciation claim exists.
10. Launch territory, age assurance, marketing, privacy/KYB/KYC, and
    responsible-use controls have named professional approval.

# Phase 2 professional-custodian constraints

Phase 2 may research custody for A, B, D, and conditional E. It may compare
controls, evidence, contracts, and vendors; it **may not choose, approve, or
legally clear a route**. Every proposal must inherit these constraints:

- allocate one exact physical card; prohibit over-issuance, unallocated
  equivalents, post-allocation substitution, and external token/claim transfer;
- keep distinct fields and evidence for title/owner, custody/possessor,
  authenticity opinion, grade/condition, reference value, insurance/bond,
  manifest allocation, and non-transferable personal claim;
- support the full refund, withdrawal, chargeback, reversal, return, loss,
  damage, dispute, and default state machine, including atomic
  refund-vs-redemption exclusion and production of PSP/network evidence;
- treat the claim as redemption evidence, not title; define the actual
  tradition/title event and custodian restitution obligation for counsel;
- maintain a cash reserve for monetary reversals separately from physical
  insurance/bond for the card; neither is proof of authenticity or title;
- for B, preserve seller owner, offer, invoice, connected PSP account, charge
  type, payout delay, collateral/recovery, backstop, and loss-waterfall fields;
- for D, create no buyer right, claim, token, title, redemption entitlement, or
  buyer-funded reservation before the optional identified-card purchase; and
- for E, preserve a separate SPA-plan/prize ledger and exact certificate,
  promoter, prize-ownership, custody, fulfillment, withdrawal/chargeback, loss,
  and default evidence.

Blockchain, signatures, and immutable records may evidence digital transitions;
they cannot independently prove that the physical card exists, is authentic,
has the asserted grade, remained undamaged, or reached the recipient. Those
remain allocated-custody, audit, carrier, insurance, dispute, and legal evidence
boundaries ([Agent 2, Fact-pattern decision tree §4–6](research.md#2-fact-pattern-decision-tree),
[CVM Guidance Opinion 40](https://conteudo.cvm.gov.br/export/sites/cvm/legislacao/pareceres-orientacao/anexos/Pare040.pdf)).

# Open questions and decision owners

| Open question | Decision owner |
|---|---|
| Does A or B qualify as an ordinary aleatory sale, unauthorized lottery/game, fixed-odds overlap, commercial promotion, or another regulated operation on the complete facts? | Brazilian consumer + criminal/gaming counsel; SPA if applicable |
| What exact withdrawal/refund/return rule applies before allocation, after reveal, after claim, after shipping, and after delivery? | Consumer counsel plus PSP/acquirer |
| Can B remain creator-seller given platform RNG, inventory approval, custody coordination, claims, and remedies? | Consumer/commercial + tax counsel and PSP/acquirer |
| Does D have no consideration before identified-card checkout under every UI and access rule? | Consumer/criminal-gaming counsel |
| Which SPA modality, certificate, and exact RNG/collection-series rules could own E, if any? | SPA-facing promotions counsel and SPA |
| Is the non-transferable claim excluded product access, and which BCB/CVM/AML duties remain? | Virtual-asset/securities counsel; BCB/CVM path as required |
| What merchant category, charge architecture, reserve, payout delay, dispute evidence, and volume cap will a PSP accept? | Licensed PSP/acquirer risk and legal teams |
| When does title/tradition occur, and what evidence survives refund, return, custodian default, or insolvency? | Commercial/property counsel with Phase 2 custodian candidates |
| What invoice/tax event describes A, B, D, or E during the 2026 transition? | Brazilian tax counsel/accounting owner |
| What age, marketing, jurisdiction, privacy, KYB/KYC, and responsible-use boundary is required? | Specialist counsel plus compliance owner |

# Connections

- The complete explorer evidence and direct-source register are preserved in
  [`research.md`](research.md).
- The earlier [fair-drop findings](../2026-07-15-gradedshop-and-fair-drop-mechanics/findings.md)
  own the finite-pool mathematics, without-replacement mechanics, and the
  distinction between reference-value ratio and guaranteed RTP. This gate
  supersedes its broad legal assumptions where the present fact patterns are
  more exact.
- The earlier [blockchain/custody addendum](../2026-07-15-gradedshop-and-fair-drop-mechanics/blockchain-card-custody-and-card-only-settlement.md)
  remains a hypothesis source for allocated custody and digital evidence. Its
  transferable NFT default is rejected for v1 here; Phase 2 inherits the
  non-transferable exact-card claim and reversal constraints in this document.

# Dispatch closeout

- Exit reason: `resolved`
- Agents spawned: 9 total — 3 explorers, 1 synthesizer, 3 skeptics,
  1 writer, 1 auditor, 0 helpers; 1 synthesis/reviewer loop used
- Final approver: **Loregian, Fosco**
- Auditor result: **ACCEPT**
- Inventory synchronization: **COMPLETE**
- This file claims no legal clearance, PSP acceptance, tax approval, vendor
  selection, or implementation approval.
