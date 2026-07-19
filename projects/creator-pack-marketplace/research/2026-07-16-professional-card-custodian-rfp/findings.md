---
title: Creator Pack Marketplace — Professional Card Custodian RFP Findings
status: candidate-findings
created: 2026-07-16
dispatch_id: 2026-07-16-creator-pack-custodian-requirements
dispatch_type: research
jurisdiction: Brazil
---

# Goal

Define an RFP-grade, testable custody and evidence baseline for individually
allocated physical trading cards. The baseline maps one exact pre-custodied
card to one personal, non-transferable redemption claim while preserving
refunds, reversals, returns, disputes, delivery, and custodian-default paths.
This is not vendor selection, legal advice, product-route selection, or
implementation approval.

# TL;DR

The v1 RFP baseline is **Candidate A**: professional third-party, individually
allocated custody; a centralized personal non-transferable claim; signed
custodian attestations; and an append-only event log. It is **HOLD**, not
approved: the whole arrangement is precedent-clean, only partly witnessed, and
still requires counsel, insurer, auditor, PSP, security, and vendor validation.
An RFC 9162-style public-chain checkpoint is an optional **SHOULD**, never an
authority over refunds, title, custody, release, or physical truth ([Agent 1,
allocated-gold limits](research.md#2-what-transfers-from-allocated-gold), [Agent
3, registry determination](research.md#1-determination), [RFC
9162](https://www.rfc-editor.org/rfc/rfc9162.html)).

Opaque locked ERC status is deferred. A transferable authoritative ERC-721,
pooled/equivalent substitution, and creator self-custody or on-demand
procurement are killed for v1 because they fail an end-to-end exact-card and
reversal witness. Blockchain can prove scoped digital authorship, ordering,
commitment, uniqueness, authorization, and non-deletion; it cannot prove the
card exists, is authentic, has the asserted grade or condition, is legally
owned, remained insured, or was delivered intact ([Agent 3, adversarial
conclusions](research.md#5-adversarial-conclusions), [Ethereum oracle
documentation](https://ethereum.org/developers/docs/oracles/)).

# Phase 1 inherited constraints

The accepted legal/payment gate remains controlling. No real-money pilot is
authorized. Custody work may compare controls and vendors for legal candidates
A, B, D, and conditional E, but may not select or clear one. Every bidder and
pilot must preserve:

- one immutable manifest entry per exact pre-custodied card; no over-issuance,
  equivalent substitution, post-allocation substitution, or external claim
  transfer;
- separate evidence for title/owner, possession/custody, authenticity opinion,
  grade/condition, reference value, insurance/bond, manifest allocation, claim,
  payment/remedy, and delivery;
- a non-transferable claim that is redemption evidence, never title;
- mandatory withdrawal, refund, reversal, chargeback, return, loss, damage,
  authenticity, delivery, and default routes, including atomic exclusion
  between monetary reversal and physical release;
- a cash reserve for legally owed monetary remedies, separate from physical
  insurance/bond; and
- written Brazilian-counsel, PSP/acquirer, tax, insurer, and compliance decisions
  before accepting money ([Phase 1, pre-money stops](../2026-07-16-legal-payment-decision-gate/findings.md#pre-money-stops),
  [Phase 1, custodian constraints](../2026-07-16-legal-payment-decision-gate/findings.md#phase-2-professional-custodian-constraints)).

# Evidence taxonomy

Every RFP statement and vendor response must identify its class:

- **Professional precedent:** a scoped practice from allocated custody,
  warehouse security, grading, carrier, audit, cryptography, or regulation. It
  does not own this product or Brazilian legal treatment.
- **RFP requirement:** a contractual, operational, security, or evidence control
  this procurement proposes to test.
- **Product inference:** a reasoned translation from precedent to exact-card
  custody. It is neither law nor vendor proof.
- **Provisional pilot number:** a falsifiable starting threshold, frozen before
  the pilot and replaceable only by a versioned decision with the named
  validator's evidence.
- **Professional/vendor validation:** a dated decision from Brazilian counsel,
  licensed PSP/acquirer, insurer/broker, independent auditor, conservator or
  grader, security owner, privacy owner, carrier, or selected custodian.

Allocated-gold and client-asset controls support exact-object identification,
segregation, reconciliation, audit, and failure-resolution requirements, but
gold's standard identifiers, fungibility, and valuation do not transfer to
collectible cards ([Agent 1, allocated-custody comparison](research.md#2-what-transfers-from-allocated-gold),
[Bank of England allocated gold](https://www.bankofengland.co.uk/gold), [FCA
CASS 6](https://handbook.fca.org.uk/handbook/cass6)).

# Proof-boundary glossary

| Term | Proves only | Does not prove |
|---|---|---|
| **Professional custodian** | Contracted organization and described service scope | Licensing, solvency, independence, competence, or compliance |
| **Deposit/bailment analogy** | A comparative custody model and proposed restitution duty | Brazilian classification, title transfer, rapid restitution, or insolvency immunity; counsel must decide ([Agent 1, insolvency gates](research.md#4-insolvency-and-insurance-decision-gates), [Civil Code arts. 627–652](https://www2.camara.leg.br/legin/fed/lei/2002/lei-10406-10-janeiro-2002-432893-normaatualizada-pl.html)) |
| **Owner/title** | The legal conclusion and evidence accepted for a stated lifecycle moment | Possession, beneficial interest, authenticity, value, or enforceability in default |
| **Possession/custody** | Recorded physical control at a scoped time/location | Title, authenticity, continuous existence, condition, or delivery |
| **Segregation/allocation** | A specific object is separately identified and not pooled in the relevant records/space | Creditor immunity, no lien, solvency, authenticity, or sufficient insurance |
| **Provenance** | Recorded acquisition/history assertions and documents | Unbroken legal title or authenticity |
| **Grader/certification/grade** | A named expert's scoped opinion and database/holder status | Title, present condition, possession, value, insurance, or delivery; public certification numbers may be copied ([Agent 2, scope determination](research.md#scope-and-determination), [PSA certification verification](https://www.psacard.com/cert)) |
| **Reference/agreed value** | A valuation input at a date and method | Sale price, guaranteed resale, liquidity, claim payment, or legal remedy |
| **Insurance/bond** | Contractual coverage subject to policy, insured interest, limits, exclusions, deductible, and claims adjudication | Prevention, authenticity, title, reserve sufficiency, or automatic customer payment ([SUSEP FAQ](https://www.gov.br/susep/pt-br/acesso-a-informacao/perguntas-frequentes/pasta-das-perguntas-frequentes/perguntas-mais-frequentes-sobre-seguros)) |
| **Reserve** | Segregated or controlled liquidity for defined monetary exposure | Physical coverage, legal entitlement, insurer recovery, or card value |
| **Manifest/claim** | Versioned inventory assertion and personal redemption-state record | Physical truth, title, grade, insurance, or delivery |
| **Signed attestation** | A signer asserted scoped data with a valid key at a time | Truth of the physical assertion or authority beyond the signed scope |
| **Audit/reconciliation** | Tests performed, population, period, exceptions, and ledger agreement | Continuous truth outside scope or undiscovered physical substitution |
| **Merkle proof/chain anchor** | Inclusion or consistency of committed digital data by a checkpoint | Accuracy, physical existence, title, authenticity, condition, delivery, or legal finality |
| **Token** | Behavior of the token contract and recorded token state | Card ownership, custody, redemption priority, refunds, or physical truth |
| **Release/carrier delivery/finality** | Recorded authorization, handoff, carrier assertion, and closed digital transition under defined rules | Intact contents, correct recipient, no consumer remedy, legal finality, or truth beyond evidence scope |

# Candidate verdict matrix

Precedent identifies component ownership; it does not itself emit KILL.
`HOLD` means further RFP and professional evidence is required.

| Candidate | Owner/precedent | Witnessed | Sound | Verdict |
|---|---|---|---|---|
| **A — third-party allocated custody + centralized personal claim + signed attestations + append-only log** | Whole arrangement is **precedent-clean**, assembled from narrow allocated-custody, audit, warehouse, claim-registry, and signature precedents ([Agent 1, control catalog](research.md#3-testable-rfp-control-catalog), [Agent 3, required controls](research.md#3-required-controls-and-pilot-tests), [FCA CASS 6](https://handbook.fca.org.uk/handbook/cass6)). | **Partial:** success path exists; default, insolvency, remedy funding, export, step-in, and production vendor controls remain unproven. | Conditional if every proof domain stays separate and the three-machine interlocks pass. | **HOLD — RFP baseline** |
| **B — A plus periodic public-chain Merkle root** | RFC 9162-style inclusion/consistency is **build-from-owned**; public-chain anchoring itself is precedent-clean ([Agent 3, registry versus ERC](research.md#4-registry-versus-erc-standards), [RFC 9162](https://www.rfc-editor.org/rfc/rfc9162.html)). | **Partial:** requires monitor, cadence, maximum unanchored interval, proof service, privacy test, and outage witness. | Sound only as optional tamper-evidence; never gates lawful refund or redemption. | **HOLD — optional SHOULD** |
| **C — opaque locked ERC status witness** | Only a narrow status interface is owned; ERC-5192 does not own consent, custody, remedies, expiry, recovery, or this state machine ([Agent 3, ERC comparison](research.md#4-registry-versus-erc-standards), [ERC-5192](https://eips.ethereum.org/EIPS/eip-5192)). | **No production witness.** | Can only repeat opaque status; cannot become claim, title, or release authority. | **DEFER** |
| **D — authoritative transferable ERC-721** | ERC owns token behavior only ([Agent 3, ERC comparison](research.md#4-registry-versus-erc-standards), [ERC-721](https://eips.ethereum.org/EIPS/eip-721)). | **No. Zeroing fact:** original payer can reverse after transfer while transferee retains redemption. | Consumer/payment reversibility conflicts with external token finality. | **KILL v1** |
| **E — pooled/equivalent substitution** | Whole model is precedent-clean and unowned; allocated custody is exact-object, not quantity entitlement ([Agent 1, allocated custody](research.md#2-what-transfers-from-allocated-gold), [Bank of England allocated gold](https://www.bankofengland.co.uk/gold)). | **No. Zeroing fact:** no exact card is bound; identity, grade, condition, title, insurance, and remedy cannot be tested. Quantity is not allocation. | Collapses every exact-card invariant. | **KILL** |
| **F — creator self-custody/on-demand procurement** | Whole model is precedent-clean and unowned; the evidence chain begins at independent intake before manifest admission ([Agent 2, custody chain](research.md#rfp-control-evidence-sla-and-remedy-catalog), [CGC grading process](https://www.cgccards.com/card-grading/grading-process/)). | **No. Zeroing fact:** no independently verified, pre-custodied exact card exists at manifest admission. | Inventory, allocation, custody, and delivery assertions depend on the interested seller. | **KILL** |

# Baseline architecture and three-machine model

The baseline has five separated authorities: platform pack/claim registry;
professional custodian inventory and fulfillment system; PSP/remedy ledger;
independent auditor/reconciliation surface; and an optional public commitment
publisher plus independent monitor. Every event is canonicalized, sequenced,
hash-linked, idempotent, signed by the scoped authority, and exported to a
platform-controlled encrypted mirror. RFC 8785 supplies a JSON
canonicalization precedent; EIP-712 signatures still require application-level
nonce/replay controls ([Agent 3, protocol model](research.md#2-protocol-model),
[RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html),
[EIP-712](https://eips.ethereum.org/EIPS/eip-712)).

```text
CARD:    available -> allocated -> redemption-locked -> shipped -> delivered
          | quarantine | lost | damaged | dispute | custodian-default
          `-> return-pending -> returned -> quarantine

CLAIM:   none -> claimed -> suspended | consumed | cancelled | revoked

PAYMENT: authorized -> captured -> refund-pending -> refunded
                         `-> reversal-pending -> reversed
                         `-> chargeback-open
```

No machine can unilaterally imply another. Allocation requires an in-TTL
custodian attestation and atomically creates one claim. Release requires the
exact card, dual platform/custodian authorization, `redemption-locked`, and no
open refund/reversal/chargeback/dispute block. Refund or reversal suspends the
claim before payment finalization. Delivery consumes redemption but does not
erase return, defect, chargeback, or statutory rights. Every mismatch
quarantines the affected card/pack; history is never rewritten ([Agent 2,
explicit exception states](research.md#explicit-exception-states), [Agent 3,
refund and reconciliation controls](research.md#r5--refund-reversal-burnlock-and-reissue)).

# MUST/SHOULD control catalog

| Priority and control | Evidence | Provisional SLA | Acceptance / remedy | Owner and validator |
|---|---|---|---|---|
| **MUST — title, intake, exact allocation** | Seller KYB/title packet; deposit receipt; `card_id`; front/back/slab images and hashes; cert/holder/tamper ID; immutable manifest history | 100% before admission; discrepancy report ≤4h | No unresolved title, duplicate, missing field, or pooled quantity. Quarantine; block affected pack | Platform legal + custodian; Brazilian counsel and independent grader validate ([Agent 2, RFP catalog](research.md#rfp-control-evidence-sla-and-remedy-catalog)) |
| **MUST — segregation, no use, liens** | Physical zoning/container and location; per-card ledger; no use, pledge, loan, substitution, set-off, or unauthorized move; disclosed landlord/financier rights | Continuous; monthly control test; annual legal refresh | Undisclosed lien/use or commingling freezes allocation and activates count/migration | Custodian compliance + platform legal; counsel validates enforceability ([LPMCL model agreement](https://cdn.lbma.org.uk/downloads/LPMCL/1.-Allocated-Account-Agreement-2018-Clean-20231103.pdf)) |
| **MUST — collectible condition and storage** | Live grader comparison; signed condition report; macro images; dual access; CCTV; calibrated temperature/RH, intrusion/fire/water/pest logs | Recheck at intake, publication, allocation, release; proposed ≤21°C, 30–50% RH, <5% RH change/24h; alert ≤5m | Mismatch or excursion quarantines zone/card; response ≤15m and independent condition review | Custodian + approved grader/conservator; insurer validates ([Agent 2, storage controls](research.md#rfp-control-evidence-sla-and-remedy-catalog), [LOC care guidance](https://www.loc.gov/preservation/care/photo.html)) |
| **MUST — state, API, attestation** | Signed canonical event, role/key, prior hash, sequence, idempotency, evidence refs, attestation validity/revocation, dual authorization for value transitions | Attestation TTL 24h; live verification ≤15m at allocation/release; revocation propagation ≤5m | Stale, revoked, conflicting, replayed, or illegal transition rejects and quarantines; no manual bypass | Platform registry + custodian signer + security owner ([Agent 3, R2–R7](research.md#r2--issue-authority-and-one-to-one-invariant)) |
| **MUST — reconciliation and independent assurance** | Daily platform/custodian/claim/payment/shipment exception report; monthly full manifest reconciliation; quarterly surprise sample; annual physical/control examination | Zero unexplained mismatches; report ≤4h; RCA/remediation plan ≤5 business days | Mismatch freezes card/pack or facility lane until physically resolved | Independent reconciliation controller + auditor ([Agent 1, controls 5–6](research.md#3-testable-rfp-control-catalog), [CFC NBC TO 3402](https://cfc.org.br/wp-content/uploads/2018/04/5_Publicacao_NBC_TO_Assegura%C3%A7%C3%A3o.pdf)) |
| **MUST — insurance and reserve** | Full policies/endorsements, insured parties/loss payees, agreed-value schedule, insurer rating, limits, deductible, exclusions, transit and catastrophe aggregates; segregated reserve evidence | Per-card agreed-value insurance 100%; aggregate ≥100% maximum location/transit concentration; deductible ≤min(5%, R$500); quarterly adequacy | Coverage gap requires reserve/bond or inventory reduction. Customer remedy starts independently of insurer ≤1 business day after qualifying confirmed failure | Platform risk + broker/insurer + finance; counsel decides legal entitlement ([Agent 1, insurance gates](research.md#4-insolvency-and-insurance-decision-gates)) |
| **MUST — refund/release/shipping/return** | Atomic lock trace; exact pick/package scans; two approvals; insured carrier acceptance; packing video; delivery/return evidence | Release decision ≤15m; dispatch ≤2 business days after valid lock; return inspection ≤1 business day | Payment block overrides release; loss/damage preserves remedy; returns quarantine; never equivalent substitution | Platform remedy owner + custodian + PSP/carrier/insurer ([Agent 2, pack/ship control](research.md#rfp-control-evidence-sla-and-remedy-catalog), [FedEx declared-value limit](https://www.fedex.com/en-us/shipping/declared-value.html)) |
| **MUST — security, privacy, key lifecycle** | Scoped protected keys; approvals; activation/rotation/revocation log; least-privilege access; encrypted PII mapping; retention/deletion and incident evidence | Compromise pause ≤5m; revoke ≤15m; registry RTO ≤4h; adjudication ≤1 business day | Pause, revoke, quarantine since trusted checkpoint, preserve verification; privacy incident path and no public PII/location/tracking | Security governance + DPO + independent approver ([Agent 3, R6/R9](research.md#r6--key-lifecycle), [NIST SP 800-57](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final), [LGPD](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm)) |
| **MUST — continuity, export, default, exit** | Signed portable event/evidence export; encrypted daily credential/record mirror; recovery reports; location/owner list; step-in and supervised migration procedure | Logical export ≤24h; access/step-in attempt ≤24h; supervised removal ≤10 business days; quarterly recovery test | Missing export freezes intake/release; default activates records mirror, independent count, access, insurance/bond, restitution/migration | Custodian data owner + platform + replacement custodian + counsel/auditor ([Agent 1, controls 11–13](research.md#3-testable-rfp-control-catalog), [FCA CASS 10](https://handbook.fca.org.uk/handbook/cass10)) |
| **SHOULD — public checkpoint** | Signed root, inclusion/consistency proof, independent monitor, privacy test, outage queue | Hourly checkpoint; maximum 24h unanchored; proof available ≤15m | Outage alerts and backfills without rewriting; never blocks lawful refund/redemption | Platform transparency owner + independent monitor ([Agent 3, registry versus ERC](research.md#4-registry-versus-erc-standards)) |

# Frozen-before-pilot parameter registry

Every number below is provisional, not a promise or accepted vendor SLA. Before
pilot start, its version, evidence, exception policy, and named validator must
be frozen: custodian operations validates workflow timing; security validates
attestation/key/RTO timing; independent auditor validates reconciliation/export;
broker/insurer validates cover; finance and Brazilian counsel validate reserve
and remedies; conservator/grader validates environment; logistics and carrier
validate shipment timing; privacy owner validates exposure controls.

| Parameter | Provisional value |
|---|---|
| Custody attestation | TTL 24h; live verification ≤15m at allocation/release; revocation propagation ≤5m |
| Optional B checkpoint | Hourly; maximum 24h unanchored; proof available ≤15m |
| Monetary reserve | 100% of maximum legally owed remedy for every captured-undelivered order plus open refunds, chargebacks, fees, and stress buffer; never below captured-price exposure. CARD-0001 adds a R$10,000 stress amount without deciding legal entitlement |
| Insurance | Scheduled per-card agreed value 100%; aggregate ≥100% maximum location/transit concentration; deductible ≤min(5%, R$500); catastrophe aggregate separately evidenced |
| Customer remedy | Initiated ≤1 business day after qualifying confirmed loss/failure, independent of insurer payment |
| Key incident | Pause ≤5m; revoke ≤15m; registry RTO ≤4h; adjudication ≤1 business day |
| Discrepancy | Initial report ≤4h; root-cause/remediation plan ≤5 business days |
| Exit | Logical export ≤24h; step-in/access attempt ≤24h; supervised removal ≤10 business days |
| Resilience | Encrypted daily credential/record mirror; quarterly recovery test |

# Weighted RFP scorecard and disqualifiers

| Domain | Weight |
|---|---:|
| Title, segregation, liens, restitution, and exit | 20 |
| Collectible intake, identity, condition, storage, and fulfillment | 20 |
| State machine, API, attestations, and portable evidence | 15 |
| Insurance, reserve interfaces, and financial resilience | 15 |
| Audit, reconciliation, continuity, incidents, and default | 12 |
| Security, privacy, keys, and privileged change | 10 |
| Capacity, implementation feasibility, and transparent cost | 8 |

Pass requires **≥80/100**, **≥60% in every domain**, and no disqualifier.
Scores must cite bidder evidence and verified tests, not marketing assertions.
Disqualifiers are: pooled/equivalent inventory; substitution after allocation;
creator self-custody or procurement after manifest admission; authoritative or
transferable token; claim/title conflation; inability to prove exact-card
intake and location independently; undisclosed lien/use/subcustodian; refusal
to disclose full policy/limits/exclusions/deductible; insurance counted as the
refund reserve; no atomic refund-release interlock; no independent audit/direct
confirmation; no portable export, step-in, or supervised migration; chain
availability gating a lawful remedy; public PII, tracking, or exact location;
single-person record-and-removal power; or refusal to run adversarial tests.

# Due-diligence request list

Require corporate ownership, solvency and litigation; operating history;
facility and subcontractor/location register; permits and security assessments;
organization chart and role segregation; collectible-card procedures; staff
screening/training; sample title/intake/condition/movement/release/return files;
complete API/event schemas and key architecture; exception and reconciliation
reports; independent assurance and physical-count reports; incident, loss,
claim, shortage, authenticity, privacy, and outage history; full insurance
policies/endorsements and paid-claims history; catastrophe/concentration model;
BCP/DR and tested recovery reports; data retention/deletion and LGPD role;
subcontract terms; standard customer and custody agreements; lien/financing and
landlord rights; default/insolvency and access opinion; portable sample export;
capacity, implementation plan, pricing, termination fees, conflicts and related
parties; and written acceptance/counterproposal for every frozen parameter.

# Required contract and SLA clauses

The agreement must define exact-card deposit and restitution; lifecycle title
and beneficial-interest assumptions for counsel; segregation and no use,
pledge, loan, substitution, lien, set-off, retention, or unauthorized relocation;
approved sites/subcontractors with flow-down and primary custodian liability;
inspection, condition, environment and tamper evidence; signed events and
dual-control release; immutable history, records ownership/access and retention;
atomic payment/remedy interlock; insurance, loss payee, notice, deductible and
claims cooperation; incident and discrepancy timing; independent audit/count
and direct confirmation; security, keys, privacy and breach obligations;
business continuity and tested mirror; limitation-of-liability carve-outs for
fraud, wilful misconduct, gross negligence, confidentiality/security and
unauthorized release; customer-remedy cooperation independent of insurance;
change control; no unilateral sale/destruction; step-in, emergency access,
portable export, transition assistance and supervised removal; termination and
insolvency; fee transparency; evidence survival; governing law and dispute
route. Brazilian counsel must validate enforceability and any retention or
insolvency effect ([Agent 1, default and migration](research.md#3-testable-rfp-control-catalog),
[Bankruptcy Law art. 85](https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2005/lei/l11101.htm)).

# Responsibility matrix

| Activity | Accountable | Executes / supplies evidence | Independent validation |
|---|---|---|---|
| Seller/KYB, title and legal lifecycle | Platform legal/compliance | Seller/creator + custodian intake | Brazilian counsel + auditor |
| Physical intake, custody, condition and release | Custodian operations | Custodian + grader/conservator + carrier | Auditor, insurer/broker |
| Manifest, RNG result, claim and event registry | Platform inventory/registry owner | Platform + custodian co-signers | Reconciliation controller + security reviewer |
| Payment blocks, refunds and reserve | Platform remedy/finance owner | Licensed PSP/acquirer + platform | Counsel, finance audit, PSP risk |
| Insurance, loss and claims | Platform risk owner | Broker/insurer + custodian/carrier | Counsel + finance/auditor |
| Security, keys, privacy and continuity | Platform security/DPO | Platform and custodian security/data teams | Independent security/privacy assessor |
| Physical and digital reconciliation | Independent control owner | Custodian/platform/PSP/carrier supply records | Independent auditor |
| Default, step-in and migration | Platform legal/risk | Current and replacement custodians | Counsel, auditor, insurer |
| Optional public checkpoint | Platform transparency owner | Publisher + independent monitor | Security/privacy reviewer; no physical-truth claim |

# Exact CARD-0001 witness — R$10,000 stress case

**Intake and allocation success.** Before admission, platform counsel accepts
CARD-0001's dated seller/title packet and assumed tradition event; the custodian
opens it under camera/two-person control, assigns immutable ID, captures original
images/hashes, slab/cert/tamper data and condition, live-checks the grader, and
stores it in an individually addressed segregated bin. Broker/insurer supplies
a scheduled R$10,000 agreed-value binder with policy, exclusions, deductible,
loss payee and transit cover; finance separately proves the frozen reserve,
including R$10,000 stress exposure without promising that amount as legal
entitlement. Manifest admission binds that exact record. Allocation verifies a
≤24h custodian attestation live within 15 minutes, atomically changes
`available → allocated`, issues one personal claim, and rejects 9,999 racing
requests. Account recovery revokes the old credential/claim epoch and issues a
new one without changing owner/title or creating a second active claim ([Agent
3, issue/refund controls](research.md#r2--issue-authority-and-one-to-one-invariant)).

**Release and delivery success.** Redemption suspends conflicting money paths,
then dual platform/custodian authorization creates `redemption-locked`.
Two-person pick scans CARD-0001 into its exact tamper-evident package; packing
video, weight, condition, fiscal/content record, suitable R$10,000 carrier and
insurance acceptance precede handoff. Signed shipment/delivery events consume
redemption only after platform, custodian, carrier, and claim reconciliation.
Correios' published PAC declared-value ceiling is below R$10,000, so that
specific service is not an assumed route ([Agent 2, shipment control](research.md#rfp-control-evidence-sla-and-remedy-catalog),
[Correios additional services](https://www.correios.com.br/enviar/servicos-adicionais)).

**Stale/revoked attestation or compromised key.** Allocation/release rejects a
stale or revoked signature. A compromised key pauses affected transitions
within 5 minutes, revokes within 15, quarantines events since the last trusted
checkpoint, and preserves old valid verification. Registry recovery target is
4 hours; adjudication target is one business day. No history is rewritten.

**Post-shipment chargeback.** `chargeback-open` blocks further claim action but
cannot pretend the released card is still in custody. The PSP evidence packet
uses title, order, allocation, lock, exact pick/package, carrier, delivery, and
customer records. The PSP debit is absorbed first by the defined monetary
reserve, then by the counsel/contract-approved seller/platform recovery and
loss waterfall; physical insurance is not used unless a covered physical loss
also occurred. The platform neither forces a duplicate refund nor recovers
from the customer outside counsel/network rights. The result and liability
owner are recorded without mutating delivery history ([Agent 3, shipment and
delivery](research.md#r11--shipment-and-delivery), [Visa Core and Product
Rules](https://www.visa.com.br/content/dam/VCOM/download/about-visa/visa-rules-public.pdf)).

**Loss and customer remedy.** If CARD-0001 is confirmed lost, it remains `lost`;
no equivalent is substituted. The platform starts the counsel-approved
customer remedy within one business day using monetary capacity independent of
carrier/insurer payment. Carrier and agreed-value claims proceed separately;
recoveries follow the signed loss waterfall. The R$10,000 figure is a stress
and insurance amount, not a predetermined refund or admission of legal
entitlement ([Agent 2, R$10,000 loss witness](research.md#end-to-end-witnesses)).

**Custodian insolvency/default.** All affected allocations/releases freeze.
The daily mirror and ≤24h logical export reconstruct CARD-0001's location,
title packet, state and evidence; step-in/access is attempted within 24h;
independent count, counsel-led restitution, insurer/bond notices and supervised
removal/replacement-custodian migration target ≤10 business days. Segregation
supports the claim but does not guarantee insolvency immunity or timing.

# General failure witnesses

- **Counterfeit/tampered holder:** certification resolves but images/security
  differ; quarantine before manifest, preserve video/originals, independent
  review, seller remedy—never silent relabel.
- **Environment excursion/condition change:** alert, isolate zone, image exact
  cards, compare intake state, insurer/conservator review before release.
- **Duplicate allocation or refund-release race:** idempotent state predicate
  permits one allocation; refund/reversal suspension blocks pick; mismatch
  freezes pack and opens reconciliation.
- **Return substitution:** camera reopen, weight/image/cert/tamper comparison;
  return stays quarantined until named adjudication.
- **Stale oracle/anchor outage:** stale attestation blocks; optional checkpoint
  outage alerts and queues ≤24h, while lawful registry refund/redemption
  continues from verified off-chain state.
- **Missing card/custodian default:** facility allocations freeze, direct audit
  and independent count start, records mirror/step-in/insurance/restitution and
  migration activate.
- **Privacy attack:** dictionary attack must not recover PII, tracking, exact
  location, or low-entropy card identity; leakage pauses publication and starts
  LGPD incident handling ([Agent 3, privacy control](research.md#r9--privacy-and-audit-export),
  [ANPD FAQ](https://www.gov.br/anpd/pt-br/acesso-a-informacao/perguntas-frequentes/perguntas-frequentes)).

# Pilot acceptance suite

The pilot is production-equivalent but **no-money** until Phase 1 pre-money
stops close. Any failed MUST test blocks vendor qualification.

| Test | Acceptance | Failure action |
|---|---|---|
| 20-card intake cohort | 20/20 title/intake/condition/allocation records complete; all exact IDs physically located | Quarantine; no manifest |
| Seeded counterfeit/tamper | Detect 5/5 before admission | Freeze lane; retrain and rerun |
| Allocation concurrency | 10,000 races for one card; exactly one success, no duplicate claim | Disable allocation; root-cause and full rerun |
| Refund/release races | 100/100 release attempts blocked after refund/reversal lock | Disable release integration |
| Attestation/key lifecycle | Reject expired, wrong-card, wrong-manifest and revoked keys; pause/revoke/RTO meet registry | Freeze signer/integration |
| Account recovery | Old credential revoked, one new epoch, no second active claim or title change | Disable recovery |
| Post-shipment chargeback | Complete evidence packet and frozen loss waterfall reconcile without counting insurance as reserve | Stop payment launch |
| R$10,000 confirmed loss | Exact card remains lost; remedy starts ≤1 business day; policy and reserve paths remain separate | Stop high-value lane |
| Reconciliation/export/recovery | Zero unexplained IDs; export ≤24h; clean restore verifies events, keys and active invariants | Freeze all allocation; step-in |
| Optional anchor outage | Alert, ≤24h unanchored, proofs backfilled ≤15m after recovery, no remedy blocked | Disable optional publisher only |
| Insolvency tabletop | ≤24h access attempt and usable mirror/export; owners execute count, restitution, insurance and ≤10-day removal plan | Disqualify if no executable step-in |
| Privacy attack | No PII/tracking/location/unsalted identity recovered; least privilege and deletion pass | Pause publication; incident route |
| Environment alert | Alert ≤5m, response ≤15m, isolated evidence and condition review | Freeze affected zone |

# Open decisions and named owners

| Decision | Owner |
|---|---|
| Select legal candidate and define title/tradition, restitution, liens, insolvency, remedies and contract enforceability | Brazilian consumer/commercial/property + criminal/gaming counsel; SPA if applicable |
| Approve actual payment, reserve, chargeback evidence and loss waterfall | Licensed PSP/acquirer + platform finance/risk + counsel |
| Validate card identity, grading limits, conservation and environment | Independent grader/authenticator + conservator + custodian |
| Bind agreed value, policy scope, catastrophe concentration, deductible and customer-independent claim path | Broker/insurer + platform risk + counsel |
| Validate audit population/frequency, direct confirmation, discrepancy and exit evidence | Independent auditor |
| Validate event schema, signatures, attestation TTL, key lifecycle, RTO and optional checkpoint | Platform security owner + custodian security + independent assessor |
| Validate LGPD roles, retention, public commitments and incident path | DPO/privacy counsel |
| Validate R$10,000 carrier route, packing, recipient and loss evidence | Carrier/logistics owner + insurer + PSP disputes team |
| Accept or replace each provisional parameter and freeze pilot version | Named validator in the parameter registry plus product risk owner |
| Score bidders and decide whether any vendor reaches qualification | Procurement committee; no automatic product approval follows |

# Connections

- The complete verbatim custody explorer evidence and direct-source register are
  preserved in [`research.md`](research.md).
- The accepted [Phase 1 legal/payment gate](../2026-07-16-legal-payment-decision-gate/findings.md)
  owns fact-pattern classification, PSP, tax, consumer-remedy, and pre-money
  stops. This document cannot override it.
- The earlier [fair-drop findings](../2026-07-15-gradedshop-and-fair-drop-mechanics/findings.md)
  own finite-pool mathematics; custody evidence does not make a random-pack
  model legal or fair.

# Dispatch closeout

- Exit reason: `resolved`
- Agents spawned: 9 total — 3 explorers, 1 synthesizer, 3 skeptics,
  1 writer, 1 auditor, 0 helpers; 1 synthesis/reviewer loop used
- Writer: **Senge, Peter**
- Final approver: **Brandenburg, Martin**
- Auditor result: **ACCEPT**
- Parent close: **APPENDED**
- Inventory synchronization: **COMPLETE**
- This file claims no vendor selection, legal clearance, PSP acceptance,
  product-route selection, or implementation approval.
