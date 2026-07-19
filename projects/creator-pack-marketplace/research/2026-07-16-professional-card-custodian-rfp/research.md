---
title: Professional Card Custodian RFP Explorer Returns
status: collected
created: 2026-07-16
dispatch_id: 2026-07-16-creator-pack-custodian-requirements
dispatch_type: research
---

# Explorer Returns

The sections below preserve the three explorer returns verbatim. They are raw
research evidence, not accepted findings, vendor selection, or legal advice.

## Agent 1 — Goldratt, Eliyahu

# Allocated Custody for Individually Identified Trading Cards

## 1. Scope and inherited constraints

Status: research and RFP design, not vendor selection or legal clearance. Sources checked 16 July 2026.

The accepted Phase 1 model requires:

- one exact card per immutable manifest entry;
- no pooled or equivalent-card entitlement;
- no post-allocation substitution;
- a non-transferable claim that is redemption evidence, not title;
- separate evidence for title, possession, grade/condition, authenticity opinion, value, insurance, allocation, and claim state;
- support for refund, reversal, return, loss, damage, authenticity dispute, delivery dispute, and custodian default;
- atomic exclusion between monetary reversal and physical release.

`[P]` means control precedent; `[R]` proposed RFP requirement; `[I]` inference for cards; `[C]` requires Brazilian counsel, auditor, or insurer confirmation.

## 2. What transfers from allocated gold

The Bank of England describes allocated custody as the customer retaining title to specific bars rather than holding a claim for equivalent weight; the bars do not appear on the Bank’s balance sheet. The LPMCL model allocated-account agreement separately records ownership, location, segregation, and subcontracted custody. These are useful control precedents, not Brazilian card law.

Transferable controls:

- `[P→R]` Exact-object rather than quantity entitlement.
- `[P→R]` Custodian books identify owner and specific object.
- `[P→R]` Customer assets segregated from custodian and other-customer assets.
- `[P→R]` Fixed approved storage locations and recorded movements.
- `[P→R]` No custodian use, pledge, lending, substitution, or negative inventory.
- `[P→R]` Internal, physical, and third-party reconciliation.
- `[P→R]` Auditable instructions, access, incidents, discrepancies, and releases.
- `[P→R]` Failure-resolution pack and transfer to a replacement custodian.

Controls that do **not** transfer automatically:

- Gold bars have standardized identifiers, weights, fineness, accepted vault practices, and fungible market valuation. Cards require evidence of edition, language, printing, serial/slab number, provenance, authenticity opinion, grade, surface condition, tampering, environmental damage, and image continuity.
- A bar list does not prove a card’s grade or authenticity. A grader’s slab does not prove title, present condition, possession, insurance, or delivery.
- Insurance advertised as “full value” does not prove cards, unexplained shortage, employee dishonesty, fraud, gradual deterioration, infestation, humidity, or transit are covered.
- Digital state cannot prove continued physical existence or condition.
- The LPMCL model permits subcustodian liability limits, custodian liens/set-off, and eventual sale after termination. Those clauses are unsuitable defaults for consumer cards.

## 3. Testable RFP control catalog

| Control | Evidence requested | Frequency / SLA | Acceptance and failure remedy | Owner |
|---|---|---|---|---|
| **1. Title and deposit basis** `[R,C]` | Seller invoice/acquisition chain; exact-card deposit receipt; agreement distinguishing owner, depositor, custodian and claim-holder; Brazilian opinion on deposit, tradition/title event, restitution and consumer remedies | Before intake; refresh on model change | No unresolved title gap, conflicting owner, or claim-title conflation. Quarantine card; block allocation | Platform legal + custodian |
| **2. Individually allocated property** `[P→R]` | Unique `card_id`; front/back/slab images; grader/cert number if any; tamper-evident package ID; exact vault location; owner account | At intake; immutable history | One physical object maps to one active manifest entry. Duplicate/missing ID stops the entire affected pack | Custodian operations |
| **3. Segregation and no use** `[P→R,C]` | Physical zoning/container scheme; per-owner/card ledger; contract prohibition on use, pledge, lending, substitution, commingling and unauthorized relocation | Continuous; monthly control test | Custodian inventory and platform inventory never become custodian assets or pooled equivalents. Breach triggers allocation freeze, independent count and removal right | Custodian compliance |
| **4. Liens and creditor exposure** `[R,C]` | Contractual no-lien/no-set-off/no-retention language; financing/security-interest search; disclosed landlord/warehouse/financier rights; counsel opinion on enforceability | At diligence; annual and on financing change | No undisclosed lien. Counsel must address Civil Code retention rights and insolvency effects. Adverse change triggers migration | Platform legal |
| **5. Reconciliation** `[P→R]` | Daily platform–custodian–claim-state exception report; signed movement ledger; physical cycle-count records | Digital daily; high-value cards monthly; all cards at least quarterly | Zero unexplained shortage, duplicate allocation or state conflict. Same-day freeze; preliminary incident report in 4 hours; root cause and remediation in 5 business days | Custodian control owner |
| **6. Independent physical assurance** `[P→R]` | Direct custodian confirmations; independent count/inspection report; sample images and package IDs; control-assurance report under NBC TO 3402 or equivalent | Annual full count plus quarterly surprise risk sample | Auditor has direct access and tests existence and condition, not records alone. Exceptions remain open until physically resolved | Independent auditor |
| **7. Access and release security** `[P→R]` | Named-role matrix; segregation of duties; two-person vault/release control; access logs; CCTV policy; visitor and key inventories | Every access; quarterly access review | No single person can alter records and remove a card. Unauthorized access freezes affected zone and invokes incident response | Custodian security |
| **8. Release and reversal interlock** `[R]` | API/manual procedure showing `claimed → redemption-locked` before pick; exact-card/package scans; two approvals; carrier handoff; blocked-release and refund tests | Every release; decision response ≤15 minutes | No release while refund, chargeback, return, dispute or reversal state is incompatible. Failed interlock stops fulfillment | Platform + custodian |
| **9. Insurance and bond** `[R,C]` | Full policy, schedule, endorsements, insurer identity/rating, insured parties/loss payees, limits, aggregate and sublimits, deductibles, valuation method, territorial/transit scope, exclusions, claims procedure and paid-claims history | Before intake; quarterly value/limit adequacy; 30-day advance notice of change/cancellation | Cards and third-party property expressly included; storage and transit separately evidenced; maximum foreseeable concentration and high-value card stress test covered. Gap requires reserve/bond or inventory reduction | Platform risk + broker/insurer |
| **10. Subcontractors** `[P→R,C]` | Complete subcontractor/location register; due diligence; insurance; flow-down controls; audit and access rights; liability allocation | Prior written approval; annual review; notice before change | Custodian remains contractually responsible; no broad insolvency/act-of-subcustodian disclaimer. Unauthorized delegation triggers suspension/migration | Custodian contract owner |
| **11. Incident and continuity** `[P→R]` | Incident taxonomy/runbook; contact tree; backup-power/environmental controls; disaster-recovery tests; physical salvage plan | Critical notice ≤1 hour; initial facts ≤4 hours; daily updates; annual exercise | Allocation/release can be isolated without losing records. RPO zero for custody transitions; tested record-system RTO ≤4 hours; physical-service recovery target contractually stated | Custodian incident commander |
| **12. Records and audit access** `[P→R]` | Exportable signed event ledger, images, title/deposit evidence, access/release records, insurance and audit reports; platform-controlled mirror | Event-synchronous plus daily immutable export; retain custody life + 10 years | Records remain readable without custodian systems. Missing export freezes intake/release. Platform and auditor receive direct access | Custodian data owner |
| **13. Default and migration** `[P→R,C]` | Resolution pack; current card/location/owner list; replacement-custodian procedure; transport insurance; step-in/access authorization; termination assistance and fee schedule | Annual tabletop; sampled migration yearly | Data/documents export ≤2 business days; emergency physical access plan; agreed bulk migration deadline. No unilateral sale, substitution or destruction after termination | Platform legal + both custodians |

## 4. Insolvency and insurance decision gates

Brazil’s Civil Code defines deposit as receipt of a movable object for safekeeping and requires care and restitution; it also restricts use or redeposit without authorization. Bankruptcy Law 11.101/2005 art. 85 permits an owner to request restitution of property found in the debtor’s possession. `[C]` Neither provision guarantees successful or rapid recovery. Counsel must determine:

1. who owns each card at intake, allocation, cancellation, delivery and return;
2. whether individualized records and physical segregation support restitution;
3. whether any custodian, warehouse, landlord, insurer or financier can assert retention, lien or set-off;
4. who can enter the facility and remove cards after insolvency;
5. whether platform/customer records are admissible and usable when the custodian is unavailable.

Insurance must be evidenced policy-by-policy. SUSEP warns that high-value/rare objects and third-party property may be excluded unless expressly included, and that deductibles and exclusions control recovery. Required underwriting questions include unexplained disappearance, employee dishonesty, fraud, counterfeit/authenticity dispute, gradual deterioration, humidity/fire/flood, packaging damage, transit, card-specific agreed value, aggregate catastrophe limits, and who receives proceeds. Physical insurance cannot replace the cash reserve for refunds.

## 5. Predicted cross-angle disagreements

- **Goldratt–Forrester:** allocated-title and reconciliation controls survive; gold-style identity and condition controls do not. The collectible workflow must independently witness intake grade, tamper state, preservation, exact-card picking, packing, delivery, and returns.
- **Goldratt–Hewitt:** contracts and audits may prove custody at sampled times but remain unsynchronized with claim state. Dispatch 2 must require an atomic physical/digital release protocol and daily three-ledger reconciliation; blockchain alone is insufficient.

## 6. Primary-source register

- Bank of England, allocated gold custody, updated 12 March 2026: https://www.bankofengland.co.uk/gold
- LPMCL/LBMA Model Allocated Account Agreement, segregation, ownership, subcustodians, liens and termination: https://cdn.lbma.org.uk/downloads/LPMCL/1.-Allocated-Account-Agreement-2018-Clean-20231103.pdf
- LBMA Vault Best Practice, validation, insurance, audits and trained staff: https://www.lbma.org.uk/market-standards/vaulting/vaults-best-practice-guidelines
- Perth Mint Depository terms, identified allocated property, bailment, segregation, no use and insurance: https://www.perthmint.com/globalassets/assets/documents/depository/tcs/25-10-21-depository-online-terms-and-conditions.pdf
- FCA CASS 6, client distinction, physical/external reconciliations, discrepancy and failure controls; current text checked 16 July 2026: https://handbook.fca.org.uk/handbook/cass6
- FCA CASS 10, failure-resolution records and transfer access: https://handbook.fca.org.uk/handbook/cass10
- CVM Resolution 32 consolidated through Resolution 209/2024; securities-only Brazilian control precedent: https://conteudo.cvm.gov.br/export/sites/cvm/legislacao/resolucoes/anexos/001/resol032consolid.pdf
- CFC NBC TO 3402, Type 1/Type 2 service-organization assurance: https://cfc.org.br/wp-content/uploads/2018/04/5_Publicacao_NBC_TO_Assegura%C3%A7%C3%A3o.pdf
- PCAOB AS 2510, physical counts and outside-custodian evidence: https://pcaobus.org/oversight/standards/auditing-standards/details/AS2510
- Brazilian Civil Code arts. 627–652, official Chamber text: https://www2.camara.leg.br/legin/fed/lei/2002/lei-10406-10-janeiro-2002-432893-normaatualizada-pl.html
- Bankruptcy Law 11.101/2005, especially art. 85: https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2005/lei/l11101.htm
- SUSEP insurance exclusions, uninsured property and deductibles: https://www.gov.br/susep/pt-br/acesso-a-informacao/perguntas-frequentes/pasta-das-perguntas-frequentes/perguntas-mais-frequentes-sobre-seguros
- SUSEP transport-insurance scope and storage extension: https://homolog2.susep.gov.br/menuatendimento/Transportes.asp

## Agent 2 — Forrester, Jay

# Forrester Explorer — Collectible-Card Custody Operating Chain

## Scope and determination

Currentness: 16 July 2026. This report inherits Phase 1’s constraints: one exact physical card per manifest entry; one personal, non-transferable claim; no over-issuance or post-allocation substitution; claim, title, custody, authenticity, grade, value and insurance remain separate; every refund, return, loss and default state remains reversible until lawfully closed.

The custodian must be an evidence-producing bailee, not a physical-truth oracle. A grader’s label is an expert opinion with contractual limits. PSA excludes tampered holders, environmental deterioration, loss and damage from its guarantee; its verification guidance warns that public certification numbers can be reused fraudulently ([PSA guarantee](https://www.psacard.com/financialguarantee/), [PSA certification verification](https://www.psacard.com/cert)). CGC similarly conditions coverage on an intact holder and active certification, while its process provides useful operational precedent: camera-recorded opening, paperwork reconciliation, unique ID/barcode, vaulting, imaging, quality control and final count ([CGC guarantee](https://www.cgccards.com/card-grading/cgc-guarantee/), [CGC grading process](https://www.cgccards.com/card-grading/grading-process/)). None proves legal title.

## RFP control, evidence, SLA and remedy catalog

Thresholds below are pilot acceptance baselines; bidders must accept them or counter-propose with insurer, conservator and operational evidence.

| Control and owner | Required evidence and SLA | Failure remedy |
|---|---|---|
| **Seller KYB/title/provenance — platform owns approval; custodian enforces intake hold.** Verify legal identity, beneficial owner, acquisition document, seller warranty, invoice/receipt, prior custodian release and sanctions/fraud flags. Museum provenance practice is an analogy, not a title safe harbor ([ICOM Code](https://icom.museum/en/resources/standards-guidelines/code-of-ethics/)). | Versioned `owner_id`, title packet, reviewer, decision and hash before acceptance; 100% required fields; decision within two business days. | `pending-title`/`provenance-dispute`; no manifest admission, allocation or return to an unverified destination. Escalate to platform counsel. |
| **Intake chain — custodian.** Open under continuous camera coverage and two-person control; reconcile shipper seal, declared contents and paperwork; assign immutable internal `card_id`; record grader, certification number, slab type, dimensions, weight, front/back/edge/label macro images and visible defects. | Timestamped intake event, operator IDs, original files plus hashes, seal and package IDs, scale calibration and discrepancy report within four hours of receipt. | `intake-exception`; reseal in quarantine, preserve packaging/video and notify platform within one hour. |
| **Identity/authentication/condition — custodian plus approved grader or specialist.** Live-query the issuer’s certification database and compare description, grade, images, label, QR/serial and holder security. Treat database match as corroboration only. Raw, questionable, altered, cleaned, recolored, trimmed or tampered cards require specialist disposition; PSA and CGC expressly recognize such exception classes ([PSA standards](https://www.psacard.com/gradingstandards), [CGC grading terms](https://www.cgccards.com/card-grading/cards-we-grade/)). | Signed condition report and comparison images; zero unexplained mismatches. Recheck certification at intake, manifest publication, allocation and release. | `auth-question`, `holder-tamper` or `condition-change`; freeze, notify within one hour, obtain independent review, then reject, regrade or preserve dispute state. Never silently relabel. |
| **Storage/security — custodian.** Individually addressed bins; no fungible bulk allocation; dual-controlled vault access; CCTV, intrusion/fire/water monitoring, visitor and key logs, backup power, pest controls and disaster plan. Require current TAPA FSR certification or control-by-control equivalent, while recognizing it is a warehouse-security baseline rather than collectible proof ([TAPA FSR 2023](https://tapaemea.org/wp-content/uploads/2023/08/FSR-2023-Standard.pdf)). | Provisional conservation baseline: ≤21°C, 30–50% RH and <5% RH movement/24h, continuous sensors with annual calibration; validate against each slab/card material. Library of Congress guidance supports these ranges by analogy for paper/photo materials ([LOC care guidance](https://www.loc.gov/preservation/care/photo.html)). | Alert within five minutes; human response within 15 minutes; isolate affected zone, image cards and open `environment-excursion`; independent condition review before release. |
| **Moves/reconciliation — custodian.** Every receipt, quarantine, bin move, allocation, pick, pack, return and destruction is a signed event containing what/when/where/why/how, consistent with GS1 EPCIS 2.0.1’s event dimensions ([GS1 EPCIS](https://ref.gs1.org/standards/epcis/2.0.1/)). | Event committed within five minutes; daily logical/physical exception reconciliation; monthly 100% certification/manifest reconciliation; zero unexplained cards or duplicate active IDs. | Freeze affected card and pack; unresolved mismatch after four hours freezes the facility’s new allocations and triggers incident response. |
| **Manifest/allocation/release — platform authorizes; custodian independently enforces.** One live `card_id` may appear once in one manifest. Allocation must atomically move it from `available` to `allocated`; redemption lock must precede pick. | Idempotency key, manifest version, allocation signature, claim ID, lock, picker/scanner IDs and reconciliation receipt. Custodian rejects stale, duplicate or unsigned commands. | `duplicate-id` or `release-blocked`; no movement; freeze pack and reconcile. Refund/reversal state always overrides release until the state-machine owner resolves it. |
| **Pack/ship/deliver — custodian, carrier and insurer.** Scan exact slab into exact package; capture condition, tamper seal, packing video, package weight, fiscal/content document, tracking and recipient rule. Require door-to-door collectible coverage and written exclusions. Carrier declared value is not automatically insurance; FedEx states this explicitly ([FedEx declared value](https://www.fedex.com/en-us/shipping/declared-value.html)). | Dispatch within two business days after valid lock. For Correios, use appropriate declared value, AR/CEE and `Mão Própria`; as of 12 April 2026 PAC’s published cap is R$4,668.29 while SEDEX is R$39,680.48, so a R$10,000 card cannot use PAC at full declared value ([Correios services](https://www.correios.com.br/enviar/servicos-adicionais)). | No shipment without accepted value/commodity coverage. On loss/damage: `lost`/`damaged`, notify within one hour of confirmation, file carrier and insurance claims, preserve customer remedy; no equivalent-card substitution. |
| **Return/dispute — platform authorizes; custodian receives.** Provide seller-funded reverse logistics; returned cards never go directly to available stock ([Correios reverse logistics](https://www.correios.com.br/enviar/encomendas/logistica-reversa)). | New seal/tracking; camera-recorded reopening; compare slab, certification, weight, images and condition within one business day. | `returned-quarantine`, `return-substitution`, `authenticity-dispute` or `damage-dispute`; preserve evidence, independent review and counsel-approved refund/recovery path. |
| **Audit/default/exit — custodian, independent auditor and platform.** Daily exception export, monthly full manifest reconciliation, quarterly surprise sample and annual independent control plus physical-inventory examination. SOC for Supply Chain can evidence scoped controls but does not itself prove card balance, title or value ([AICPA SOC for Supply Chain](https://www.aicpa-cima.com/cpe-learning/publication/aicpa-guide-soc-for-supply-chain-reporting-on-an-examination-of-controls-relevant-to-security-availability-processing-integrity-confidentiality-or-privacy-in-a-production-manufacturing-or-distribution-system)). | Auditor gets read-only events, originals, hashes, sensor/access logs, insurance and location map. Contract requires complete portable export within 24 hours and supervised inventory transfer within ten business days after termination/default. | Any unexplained deficit freezes allocations; activate insurer/bond, payout hold and restitution plan. Platform retains independent records and step-in rights. |
| **Privacy/retention — platform controller; custodian’s role contractually fixed.** Minimize recipient identity/address, access, CCTV and ID-document data; segregate operational card data from personal data; encrypt and log access. | Retention schedule by evidence purpose; deletion certificate when lawful purpose ends; incident record and notification workflow. LGPD/ANPD require purpose limitation, security and accountable incident handling ([LGPD](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm), [ANPD FAQ](https://www.gov.br/anpd/pt-br/acesso-a-informacao/perguntas-frequentes/perguntas-frequentes)). | Disable access, preserve incident evidence, notify platform immediately and execute the counsel-approved ANPD/data-subject route. |

## Explicit exception states

```text
pending-title
intake-exception
provenance-dispute
auth-question
holder-tamper
condition-change
environment-excursion
duplicate-id
allocated
redemption-locked
release-blocked
in-transit
delivery-dispute
lost
damaged
return-pending
returned-quarantine
return-substitution
authenticity-dispute
custodian-default
```

No exception state may automatically become `available`, `delivered` or `refunded`. A named owner, evidence review and authorized transition are required.

## End-to-end witnesses

**Success:** approved seller/title packet → sealed intake under cameras → exact slab ID, images and hashes → live grader comparison → segregated bin → manifest admission → atomic allocation → redemption lock → two-person scan/pick/pack → insured carrier with declared value and named-recipient evidence → delivered → claim closed only after custodian, carrier and platform reconcile.

**Failure — forged or substituted slab:** certification number resolves but holder/image/security comparison fails. Custodian quarantines; no manifest admission; originals and video remain immutable; independent authentication and seller remedy follow.

**Failure — refund race:** refund begins after allocation but before release. Custodian rejects pick because `refund-pending` supersedes the lock. Card returns to an authorized state only after payment and claim registries reconcile.

**Failure — R$10,000 card lost:** card remains `lost`; customer receives the lawful remedy through the monetary reserve while carrier/physical insurer claims proceed separately. No replacement card is inserted and no grader guarantee is misrepresented as transit coverage.

**Failure — custodian deficit/default:** daily or surprise count finds one missing exact ID. All affected packs freeze; independent export and surveillance/access evidence are preserved; step-in, bond/insurance and supervised restitution activate.

## Pilot acceptance tests

| Test | Owner; evidence | Threshold/timing | Failure remedy |
|---|---|---|---|
| Intake identity/title | Platform compliance + custodian; title packet/intake video | 20/20 cards, zero missing fields, ≤4h | Quarantine; no manifest |
| Counterfeit/tamper injection | Custodian + independent grader; comparison report/images | Detect 5/5 seeded exceptions before admission | Freeze intake lane; retrain/retest |
| Environment excursion | Facility manager; sensor/calibration/alert logs | Alert ≤5m, response ≤15m | Isolate zone; condition review |
| Concurrent duplicate allocation | Platform + custodian; signed event log | 10,000 races, zero double success | Freeze pack/API; root-cause review |
| Refund-versus-release race | Platform, PSP simulator + custodian; state trace | 100/100 releases blocked after refund lock | Disable release integration |
| High-value lost shipment | Logistics/insurer; policy, declaration, claim packet | Coverage accepted before tender; claim opened ≤1 business day | Stop carrier lane; customer remedy |
| Return substitution | Custodian; reopen video/image/weight comparison | Detect 5/5 substitutions ≤1 business day | Return quarantine/dispute |
| Audit/export/default | Independent auditor + custodian; full export/count | 100% IDs located; export ≤24h | Freeze all allocations; step-in |
| Privacy deletion/access | DPO + custodian; access and deletion logs | Least-privilege pass; deletion by schedule | Revoke access; incident workflow |

## Cross-layer disagreements

**Forrester–Hewitt:** operational records can prove that a custodian recorded a scan, move or release; they do not by themselves prove smart-contract finality, prevent stale-oracle use or guarantee one-time redemption. Protocol acceptance must separately reconcile signed custodian state with the claim registry.

**Forrester–Goldratt:** gold-style segregation helps with ownership and quantity but is insufficient for collectibles. Cards require item-level image/holder identity, changing condition, grader-scope limits, tamper detection, fulfillment evidence and substitution-resistant returns.

## Agent 3 — Hewitt, Carl

# Hewitt Explorer Report — Verifiable Custodian/Claim Interface

## 1. Determination

For v1, use a **centralized personal-claim registry with independently signed custodian attestations, an append-only transparency log, and optionally periodic Merkle-root anchoring on a public chain**. Do not make an ERC token the authoritative claim.

This gives the required privacy, refunds, disputes, returns, recovery, and non-transferability without forcing customers to hold wallets. A chain anchor can prove that a particular signed event existed by a checkpoint and was not silently removed; it cannot prove the event’s physical assertion was true.

If a public on-chain object is later required, use an opaque non-transferable status witness, not a transferable NFT and not legal title. The accepted Phase 1 rule remains controlling: claim, title, custody, authenticity, grade, condition, insurance, value, and delivery are separate evidence domains.

## 2. Protocol Model

Maintain three linked but separate machines:

- **Card:** `available → allocated → redemption-locked → shipped → delivered`; exceptions: `return-pending → returned → quarantine`, `lost`, `damaged`, `dispute`, `custodian-default`.
- **Claim:** `none → claimed → suspended|consumed|cancelled|revoked`. A delivered card consumes redemption but may still enter return/dispute.
- **Payment/remedy:** `authorized → captured → refund-pending → refunded`, or `reversal-pending → reversed`, with `chargeback-open` as a blocking state.

An event envelope must contain `schema_version`, globally unique `event_id`, opaque `card_id`, `claim_id`, `manifest_version`, salted card-record commitment, customer-subject commitment, `from_state`, `to_state`, per-object `sequence`, `previous_event_hash`, event and recording times, reason code, evidence hashes/retention references, attestation expiry, signer/key IDs, and signatures. Canonicalize JSON before hashing ([RFC 8785, June 2020](https://www.rfc-editor.org/rfc/rfc8785.html)). EIP-712 is suitable only where Ethereum-compatible signatures are useful; it explicitly provides no replay protection, so sequence/nonces and idempotency remain application obligations ([EIP-712, Final](https://eips.ethereum.org/EIPS/eip-712)).

## 3. Required Controls and Pilot Tests

### R1 — Manifest and card identity

**Owner:** platform inventory controller + custodian. **Input:** inspected intake record, issuer/serial/grader IDs, images, sealed-container/tamper ID, manifest version. **Predicate:** one opaque `card_id`, one leaf, no duplicate physical identifiers, current custodian signature. **Emit:** salted canonical-record hash, manifest inclusion proof, jointly signed manifest root. **Failure/remedy:** duplicate or changed leaf → entire affected manifest quarantined; never substitute. **Pilot:** inject duplicate serials, altered images, and an old root; all must fail.

### R2 — Issue authority and one-to-one invariant

**Owner:** platform claim issuer; custodian co-authorizes allocation. **Input:** committed manifest leaf, allocation result, non-expired custody attestation, personal customer binding. **Predicate:** card is `available`; no active claim; subject has accepted required terms; allocation event is unique. **Emit:** `allocated`, then one signed `claimed` event. **Failure/remedy:** concurrent issue or unknown card → atomic rejection and card quarantine. **Pilot:** 100 parallel issue attempts against one card produce exactly one claim.

### R3 — Custodian attestation

**Owner:** custodian operations/compliance signer. **Input:** warehouse scan, location-class record, seal/image/inspection evidence and prior event. **Predicate:** exact card is controlled by custodian, state/evidence agree, attestation is within `validFrom/validUntil`. **Emit:** signed custody statement with scope and expiry; no public location or PII. **Failure/remedy:** stale/missing/conflicting attestation → block allocation/release, open mismatch incident. **Pilot:** expired, revoked-key, wrong-card, and wrong-manifest attestations all fail.

### R4 — Value-changing transitions and dual authorization

**Owner:** platform and custodian using separate organizational keys. **Input:** expected current state and transition-specific evidence. **Predicate:** both authorized roles sign the identical event; irreversible release requires `redemption-locked`; emergency pause may be single-party but unpause is dual. **Emit:** ordered proof set/chain and new state. W3C Data Integrity explicitly supports multiple proofs and ordered proof chains ([Recommendation, 15 May 2025](https://www.w3.org/TR/vc-data-integrity/)). **Failure/remedy:** one signature, divergent payloads, or forbidden edge → reject/quarantine. **Pilot:** attempt every illegal edge and split-signature payload.

### R5 — Refund, reversal, burn/lock and reissue

**Owner:** platform remedy owner + custodian; PSP evidence is an input, not an oracle of physical state. **Input:** refund/chargeback case and custodian no-release confirmation. **Predicate:** claim is suspended and card cannot ship before refund/reversal finalizes. **Emit:** `refund-pending|reversal-pending`, then `refunded|reversed` plus claim `revoked/cancelled`; retain history. **Failure/remedy:** shipment already released → dispute/recovery path, never silent refund-and-redemption. Burn is evidence disposal, not a refund. Recovery/reissue atomically revokes the old claim and increments claim epoch; a returned card requires reinspection and a new claim ID. **Pilot:** race refund versus shipment and lose/recover customer credentials.

### R6 — Key lifecycle

**Owner:** security governance. **Input:** scoped platform/custodian/admin keys in protected signing systems, key registry, approvals. **Predicate:** signer role, purpose, validity interval and revocation state match event time. **Emit:** signed key activation/rotation/revocation events and historical verification material. **Failure/remedy:** compromise → pause, revoke, quarantine events since last trusted checkpoint, investigate; never rewrite history. Follow lifecycle, backup, compromise and split-knowledge guidance in [NIST SP 800-57 Part 1 Rev.5, May 2020](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final). **Pilot:** rotate each key, simulate compromise and restore verification of old valid events.

### R7 — Ordering, replay and idempotency

**Owner:** registry service. **Input:** signed event with expected sequence/state, nonce and idempotency key. **Predicate:** exact next sequence, matching `previous_event_hash`; duplicate `event_id` returns the original result; reused signature cannot cause a second effect. **Emit:** append receipt and signed checkpoint. **Failure/remedy:** gap/fork/replay → reject and quarantine object. **Pilot:** reorder, duplicate and concurrently submit events.

### R8 — Reconciliation and mismatch quarantine

**Owner:** independent reconciliation controller. **Input:** platform claims, custodian inventory, payment blocks, shipment ledger and signed checkpoints. **Predicate:** one card/one active claim; states and counts agree; no release while refund/reversal/dispute is open. **Emit:** signed reconciliation report and mismatch list. **Failure/remedy:** any mismatch stops affected pack/card and release. **Pilot:** omit a shipment, clone a claim, alter one ledger and verify automatic stop.

### R9 — Privacy and audit export

**Owner:** privacy owner + auditor. **Input:** encrypted PII mapping and public opaque commitments. **Predicate:** public surfaces contain no name, address, tracking number, exact vault location, or unsalted low-entropy identifier. **Emit:** role-filtered export containing events, signatures, key history, evidence references, manifest inclusion proofs and checkpoint-consistency proofs. W3C requires data minimization and warns that credential verification does not establish truth ([VC Data Model 2.0, 15 May 2025](https://www.w3.org/TR/vc-data-model-2.0/)). **Failure/remedy:** leakage → pause publication, rotate commitments where possible, incident process. **Pilot:** privacy review plus dictionary attack against published commitments.

### R10 — Pause, upgrade and disaster recovery

**Owner:** security governance + independent approver. **Input:** versioned transition table, migration proof, backups and signed checkpoints. **Predicate:** upgrades cannot rewrite prior events or silently widen transfer/admin powers; privileged actions are multisig/timelocked; recovery reproduces the last trusted root. **Emit:** public version/admin/pause events and recovery report. **Failure/remedy:** bad migration or root mismatch → remain paused and restore from immutable export. **Pilot:** corrupt a replica, restore in a clean region, reconcile root and every active invariant.

### R11 — Shipment and delivery

**Owner:** custodian fulfillment; platform remains remedy coordinator. **Input:** redemption lock, exact-card pick scan, package/seal ID, carrier event and delivery evidence reference. **Predicate:** exact card and claim match; no monetary block; evidence is retained for PSP dispute periods. **Emit:** signed `shipped` and `delivered|lost|damaged|dispute` events. **Failure/remedy:** carrier assertion conflicts, package damage, return or substitution → freeze claim/card, preserve evidence, invoke remedy/insurance. **Pilot:** wrong-card pick, lost parcel, refused delivery, damaged return and forged carrier webhook.

## 4. Registry Versus ERC Standards

| Mechanism | Fit |
|---|---|
| Signed registry + Merkle transparency | **Best v1 fit.** Supports personal identity, recovery and reversible remedies. Periodic inclusion/consistency proofs can follow the append-only pattern of [RFC 9162, Experimental, Dec. 2021](https://www.rfc-editor.org/rfc/rfc9162.html). Trust remains in signers and monitors. |
| [ERC-721, Final](https://eips.ethereum.org/EIPS/eip-721) | Default transfer and approval surfaces contradict v1. Its token ID identifies a token, not a physical fact. Killed branch. |
| [ERC-5192, Final](https://eips.ethereum.org/EIPS/eip-5192) | Adds a minimal locked flag to ERC-721. It does not specify consent, custody attestations, remedies, expiry, recovery or the required state machine. At most a public non-transferability signal. |
| [ERC-5484, Final](https://eips.ethereum.org/EIPS/eip-5484) | Receiver consent and immutable burn authority help, but immutable metadata/ownership and burn semantics do not own dynamic disputes, returns or physical evidence. Optional overlay only. |
| [ERC-4973, Review](https://eips.ethereum.org/EIPS/eip-4973) | Account-bound issuance/unequip is relevant, but exception/recovery handling is expressly unstandardized and status is Review. Not a production foundation. |
| [ERC-6956, Review](https://eips.ethereum.org/EIPS/eip-6956) | Explores 1:1 asset anchors and oracle attestations, but enables control-driven NFT operations and still trusts an off-chain oracle. Its “inseparable” physical anchor assumption is not proven by chain data. Quarantined research input. |

## 5. Adversarial Conclusions

A valid signature can still attest to a phantom, substituted or damaged card. A Merkle proof proves inclusion, not truth. A carrier webhook proves a sender’s assertion, not recipient identity or intact contents. An on-chain transaction cannot observe warehouse possession without an oracle, and Ethereum’s own documentation states contracts cannot natively access off-chain information and identifies oracle correctness/availability risks ([ethereum.org Oracles, current page accessed 16 July 2026](https://ethereum.org/developers/docs/oracles/)).

Therefore chain data can verify **digital authorship, ordering, commitment, uniqueness, authorization and non-deletion**. It can never independently prove **physical existence, legal title, authenticity, grade, condition, continuous custody or actual delivery**. Those require custodian controls, independent audit, carrier evidence, insurance, dispute processes and legal contracts.
