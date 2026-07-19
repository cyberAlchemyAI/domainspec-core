---
title: Creator Pack Marketplace — GradedShop and Fair-Drop Findings
status: candidate-findings
created: 2026-07-15
dispatch_id: 2026-07-15-creator-pack-marketplace-mechanics
---

# Executive answer

The strongest candidate is a **finite, pre-custodied pack drawn without replacement** ([A2 §2](research.md#2-finite-inventory-without-replacement); [A3 §Inventory, title, and fulfillment](research.md#inventory-title-and-fulfillment)). A creator may choose the item set, quantities, tier names, pre-launch price, and documented fulfillment terms. After the first sale, the initial manifest and transition rules are immutable; the changing inventory is represented by an append-only state log. Item and tier odds derive from remaining quantities, not from arbitrary creator-selected percentages. Every purchase state must expose the current odds, reference-value distribution, fees, and settlement conditions.

This can make the arithmetic understandable and the obligations auditable. It cannot, by itself, establish that a package is fair, legal, liquid, solvent, or comprehensible. HMAC replay supports only **random-selection integrity** when the complete manifest, state, mapping algorithm, and inputs are committed and replayable ([A1 §Cryptographic boundary](research.md#cryptographic-boundary)). It is not economic or legal proof. A disclosed expected-value ratio is not RTP; a reference estimate is not cash; and arithmetic feasibility is conditional on custody, valuation, costs, reserves, and fulfillment.

No money should be accepted until the legal classification, withdrawal treatment, payment architecture, seller eligibility, custody/authenticity, and reserve model are cleared in writing ([A3 §Hard blockers before taking payment](research.md#hard-blockers-before-taking-payment); [A3 §Main risk findings](research.md#main-risk-findings)).

# Evidence boundary

The source corpus is the three explorer returns preserved verbatim in `research.md`: Shannon’s public GradedShop reconstruction ([A1]), Laplace’s probability and economics model ([A2]), and Sunstein’s Brazilian legal/responsible-design issue map ([A3]). Rosen’s synthesis and reviewer corrections are dispatch-stage interpretations of that corpus; they do not add an independent source of truth. Current findings therefore distinguish:

- **Observed:** a public page, API field, or cited legal text supports the statement.
- **Derived:** arithmetic follows from stated assumptions and equations.
- **Hypothesis:** a candidate product rule that still needs policy, legal, or operational approval.
- **Unknown:** public evidence cannot answer the question.

The product is not a clone of GradedShop, and no claim here establishes that GradedShop’s implementation is audited or legally approved. External claims use the direct sources named by the explorers: [GradedShop whitepaper](https://www.gradedshop.com.br/whitepaper), [Provably Fair](https://www.gradedshop.com.br/provably-fair), [FAQ](https://www.gradedshop.com.br/faq), [pack API](https://www.gradedshop.com.br/api/packs), [standard pack snapshot](https://www.gradedshop.com.br/api/packs/1474), [tiered pack snapshot](https://www.gradedshop.com.br/api/packs/1489), and the authorities listed in the legal map below.

# GradedShop reference model

Shannon observed a flow of deposit → pack selection → HMAC-based opening → virtual vault → delivery, sellback, marketplace listing, battle, or upgrade ([A1 §Mechanics map](research.md#shannon-explorer-report--gradedshop-public-mechanics)). The whitepaper describes standard packs as one weighted item roll and tiered packs as a tier roll followed by equal selection within the tier. Public API snapshots expose prices, item odds, tier data, values, quantities, and remaining openings ([A1 §Source table](research.md#source-table)).

The transferable pattern is not the whole business model. Showing exact outcomes and odds, separating post-draw choices, and offering a verifier are useful patterns. The non-transferable assumptions are supplier availability as custody, reference listing price as realizable value, mutable values or substitutions, and the idea that a seed commitment proves the economics. Shannon found that the published HMAC flow commits a server seed, accepts a client seed and nonce, and allows recomputation after reveal, but public material does not show the digest-to-number mapping, item ordering, historical pack manifest, stock behavior, or fulfillment commitment ([A1 §Cryptographic boundary](research.md#cryptographic-boundary)).

Whatnot is useful only as a precedent for a finite seller-created random-assignment form, consistent with the finite-pool model ([A2 §2](research.md#2-finite-inventory-without-replacement)). Its policy also illustrates that marketplace rules may prohibit floor, ceiling, or average-value claims; that makes reference-EV disclosure a design hypothesis requiring explicit policy and legal review, not an established marketplace norm.

That boundary is decisive: “provably fair” must not be used as an umbrella for the random draw, price, value, reserves, delivery, or law.

# Vocabulary and assurance boundaries

| Term | Operational meaning | What it does not prove |
|---|---|---|
| Random-selection integrity | At accepted state `s`, the verifier reconstructs the selected index from a committed manifest/state version, declared mapping algorithm, server-seed commitment, client seed, nonce, and draw record. | Honest value, custody, solvency, consumer understanding, or legality. |
| Economic disclosure completeness | Before payment, the buyer can identify price, fees, odds, value basis, remaining state, shortfall probability, and settlement terms. | That the disclosed distribution is fair or non-exploitative. |
| Economic policy thresholds | Platform-owned constraints, such as a minimum guaranteed-value ratio, maximum shortfall probability, jackpot concentration, or reserve floor. | A mathematical or legal fact; policy values require an owner and review. |
| Legal clearance on record | A dated professional classification for a named entity, transaction, jurisdiction, assumptions, restrictions, expiry, approver, and change triggers. | Cryptographic proof that conduct is legal. |
| Operational solvency | Evidence that every delivery, freight, refund, reversal, damage/loss, and guarantee obligation maps to controlled inventory, available funds, process capacity, and a remedy. | Custody alone, positive EV, or a bond alone. |
| Reference value | A dated, sourced estimate computed under a disclosed valuation policy. | Cash, a redemption promise, or guaranteed proceeds. |
| Reference-value ratio | `initial reference EV / price`. | RTP. Call it RTP only when an enforceable, funded redemption right exists and redemption costs are included. |

# Candidate verdict matrix

Precedent ownership routes a candidate to its owner; it never emits a KILL. KILL is reserved here for a non-vacuous economic failure or a definitional collapse. “Hold” means unresolved policy, legal, or operational work—not approval.

| Candidate | Owner / precedent | Witnessed / non-vacuity | Sound / definition | Verdict |
|---|---|---|---|---|
| Finite pool, draw without replacement | Build-from-owned: Laplace finite-pool equations ([A2 §2](research.md#2-finite-inventory-without-replacement)); Whatnot’s [Surprise Set feature](https://help.whatnot.com/hc/en-us/articles/34545407302797-Surprise-Set-Feature-for-Sellers) and [policy](https://help.whatnot.com/hc/en-us/articles/34107510260237-Surprise-Sets-Policy) provide a finite seller-created, one-time-random-assignment precedent. GradedShop’s public finite-looking fields are only a reference, not proof of custody ([A1 §Mechanics map](research.md#mechanics-map)). | Complete BRL witness below; requires purchase-state snapshot, reservations, and atomic decrement. | Sound conditional. | **Conditional v1 candidate** |
| Quantity-derived tiers | Build-from-owned: tier probability is the sum of member quantities ([A2 §2](research.md#2-finite-inventory-without-replacement)). | Witnessed by the same pool; no empty-tier ambiguity if tiers contain remaining quantities only. | Sound conditional; tier names are cosmetic. | **Conditional v1 candidate** |
| Arbitrary creator tier probabilities | No sufficient owner in the supplied corpus; GradedShop’s tier snapshot leaves normalization/empty-tier behavior unknown ([A1 §Open questions](research.md#open-questions-for-the-synthesis)). | No complete depletion witness that preserves item odds. | Definitional/non-vacuity failure: percentages can hide item probability and undefined depletion. | **KILL current candidate** |
| Unlimited replenished unique-jackpot pool | Weighted-pool equations are supplied by Laplace ([A2 §3](research.md#3-replenished-weighted-pool)). | A unique jackpot can recur indefinitely; worst-case liability is unbounded. | Sound rejection of this v1 form. | **KILL current candidate (non-vacuity/solvency)** |
| Capped replenished pool | Precedent-clean candidate, but no supplied operational proof. | Needs hard sales cap, replenishment proof, and reserve stress witness. | Sound as a deferred form. | **HOLD / defer** |
| Creator bond | Build-from-owned as a supplemental control; no evidence that a bond proves custody or authenticity. | Requires amount, beneficiary, triggers, exclusions, and collection path. | Sound only as supplemental backstop. | **HOLD / supplement** |
| Platform or verified custodian control | Build-from-owned operational requirement derived from [A1 §Non-transferable assumptions](research.md#non-transferable-assumptions) and [A3 §Inventory, title, and fulfillment](research.md#inventory-title-and-fulfillment). | Must identify the exact item, title, segregation, transfer authority, and double-listing prevention. | Requires explicit custody test; custody is not solvency. | **Required control** |
| 70% buyback / guaranteed RTP | Laplace computes the hypothetical ([A2 §6](research.md#6-complete-brl-witness)); Sunstein identifies cash-conversion, payment, liquidity, and classification risks ([A3 §Effects of the specific design choices](research.md#effects-of-the-specific-design-choices)). | Arithmetic is possible, but no funded enforceable redemption witness or clearance exists. | Sound only if the guarantee is contractual, funded, and cleared. | **KILL current candidate (definitional/non-vacuity); revisit only after legal/PSP clearance** |
| Internal wallet or platform cash-out | Sunstein’s payment and stored-value issue map ([A3 §Payment and cash-out](research.md#main-risk-findings)). | No licensed PSP or regulated-flow witness. | No settled definition of the payment or stored-value obligation. | **KILL current v1 candidate (non-vacuity); revisit only after legal/PSP clearance** |
| Fixed price with permanent “90% RTP” or “90% ratio” | Laplace’s finite-state equations ([A2 §2](research.md#2-finite-inventory-without-replacement)). | Jackpot-first state changes remaining EV from R$18 to approximately R$17.0017 at 9,999 openings. | Definitional/arithmetic collapse: a fixed initial ratio is not a live invariant. | **KILL the permanent claim** |
| Deterministic dynamic price | Derived from Laplace’s price and margin inequalities ([A2 §5](research.md#5-creator-and-platform-economics)). | Needs stress runs for jackpot-first, depletion, refunds, chargebacks, and operations. | Sound but not yet witnessed. | **HOLD** |
| Immutable initial manifest plus append-only state log | Build-from-owned cryptographic boundary ([A1 §Cryptographic boundary](research.md#cryptographic-boundary)); corrected by reviewer definition. | Requires hash binding, state version, atomic transitions, draw, settlement, and audit records. | Sound after correcting “immutable live state” to immutable initial rules plus changing append-only state. | **Required control** |
| Responsible-use controls | Sunstein guardrails ([A3 §Configurable guardrails](research.md#configurable-guardrails)). | Must have enforceable adults-only treatment, age assurance, limits, cooling-off, and no child-directed or loss-chasing design. | Sound conditional on tests and enforcement. | **Required control** |

# Formulas and complete R$10,000 witness

For a finite pool, let `q_i(t)` be remaining quantity, `N_t = Σq_i(t)`, `d_i` reference value, `g_i` guaranteed realizable value, `P` price, `c_i` settlement cost, `φP` platform fee, and `αP+β` payment cost. Then:

```text
item chance p_i(t)       = q_i(t) / N_t
tier chance p_k(t)       = Σ[i in tier k] q_i(t) / N_t
reference EV μ_d(t)      = Σ p_i(t)d_i
guaranteed EV μ_g(t)     = Σ p_i(t)g_i
reference-value ratio     = μ_d(t) / P
guaranteed RTP            = μ_g(t) / P  (only with an enforceable funded guarantee)
buyer net                 = value_i - P
shortfall probability     = Σ[i: reference value_i < P] p_i
variance                  = Σ p_i(value_i - μ)^2
creator margin            = P - (αP + β) - φP - Σ p_i o_i
remaining liability       = Σ q_i(t)d_i  (or Σ q_i(t)g_i for guarantees)
```

Witness assumptions: 10,000 physical items are controlled before launch; price is R$20 per opening; values are substantiated dated reference estimates; creator procurement averages 70% of disclosed total; payment cost is 3% + R$0.50; platform fee is 5%; handling allocation is R$1.20; shipping is separate and not silently deducted.

| Tier | Quantity | Reference value | Initial chance | EV contribution |
|---|---:|---:|---:|---:|
| Mythic | 1 | R$10,000 | 0.01% (1 in 10,000) | R$1.00 |
| Legendary | 9 | R$2,000 | 0.09% | R$1.80 |
| Epic | 90 | R$200 | 0.90% | R$1.80 |
| Rare | 900 | R$40 | 9.00% | R$3.60 |
| Uncommon | 1,000 | R$18 | 10.00% | R$1.80 |
| Common | 8,000 | R$10 | 80.00% | R$8.00 |

Derived results:

```text
total reference value       = R$180,000
initial reference EV        = R$18 per opening
initial reference ratio     = 90% (not RTP)
reference-value shortfall   = 90% of outcomes below R$20
jackpot EV contribution     = R$10,000 × 0.0001 = R$1
variance                    = 13,892.40 BRL²
standard deviation          ≈ R$117.87
```

Provider arithmetic is conditionally solvent: R$200,000 revenue − R$126,000 procurement − R$11,000 payment − R$10,000 platform fee − R$12,000 handling = R$41,000 conditional gross margin (20.5%). It still needs separate reserves for refunds, chargebacks, damage, failed delivery, and remedies. If the jackpot is drawn first, fixed R$20 pricing leaves approximately R$17.0017 remaining reference EV over 9,999 openings, a current ratio of approximately 85.0085%. Therefore “90%” is an initial descriptive ratio only.

Plain-language disclosure:

> This pack has 10,000 openings. One item has a stated reference value of R$10,000, so its initial chance is 0.01% (1 in 10,000). At R$20, the initial expected reference-value ratio is 90%. This does not mean you should receive R$18, and it is not a cash guarantee. In 90% of outcomes, the stated reference value is below R$20. Odds and expected values change after each item is drawn. Shipping is separate. Reference values are estimates, not guaranteed resale prices.

# Mechanics and controls

1. **Finite-pool compiler:** validate non-negative integer quantities, non-empty reachable outcomes, exact tier membership, valuation timestamps, price, costs, and policy thresholds; reject invalid configurations before publication.
2. **Manifest commitment:** hash item IDs, quantities, tier mapping, value records, algorithm/version, allowed transitions, creator identity, fulfillment terms, and first-sale state. Commit before payment and retain the historical manifest.
3. **Append-only state:** each accepted draw atomically binds the previous state hash, manifest hash, nonce, selected index, quantity decrement, settlement status, and timestamp. Live state changes; the initial manifest and rules do not.
4. **Custody and reserves:** verify title, authenticity, segregation, transfer authority, and no double-listing. Hold handling, refund, chargeback, and failure-remedy reserves separately from item custody. A bond supplements but does not replace custody.
5. **Settlement and audit:** define delivery SLA, shipping, condition/grade disputes, cancellation/refund handling, failed-delivery remedy, payout ledger, and independent replay/audit access. “Public log” is useful only if the verifier can reconstruct the same result.
6. **Anti-self-dealing:** prohibit creator, employees, insiders, related accounts, and colluding marketplace accounts from buying their own packs or manufacturing reference sales; log identity relationships and freeze suspicious settlement.
7. **Responsible use:** adults-only pending clearance, reliable age assurance, spend caps, cooling-off, voluntary exclusion, purchase/loss history, no autoplay, near-miss, countdown, loss-chasing, or child-directed marketing ([A3 §Configurable guardrails](research.md#configurable-guardrails)).

# Legal issue map (not legal advice)

This is Brazilian issue spotting, not a legal opinion. Counsel and, where appropriate, the Secretaria de Prêmios e Apostas (SPA), must classify the exact flow.

| Issue | Primary source and relevance | Launch implication |
|---|---|---|
| Consumer offer and disclosure | [CDC arts. 6, 30–31, 36–38](https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm); precise Portuguese offers bind and misleading omission is prohibited ([A3 §Consumer information](research.md#main-risk-findings)). | Approve price, odds, value policy, fees, substitutions, and claims with consumer counsel. |
| Commercial promotion | [Law 5.768/1971](https://www.planalto.gov.br/ccivil_03/leis/l5768compilado.htm), [Decree 70.951/1972](https://www.planalto.gov.br/ccivil_03/decreto/antigos/d70951.htm), [Portaria SEAE/ME 7.638/2022](https://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer?captchafield=firstAccess&data=20%2F10%2F2022&jornal=515&pagina=25), [SPA promotion FAQ](https://www.gov.br/fazenda/pt-br/composicao/orgaos/secretaria-de-premios-e-apostas/promocao-comercial/promocao-comercial). | Paid randomized packs may be a promotion or analogous operation; authorization/entity eligibility and prize ownership need written confirmation. |
| Lottery/game of chance | [Decree-Law 3.688/1941 arts. 50–51](https://www.planalto.gov.br/ccivil_03/decreto-lei/del3688.htm). | A tiny floor plus chance of a high-value item can increase exposure; no probability is a safe harbor. |
| Betting classification | [Law 14.790/2023](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14790.htm). | Physical delivery does not cleanly fit fixed-odds betting, but counsel must test the substance. |
| Online withdrawal | [CDC art. 49](https://consumidor.gov.br/pages/conteudo/publico/102), [Decree 7.962/2013](https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/decreto/d7962.htm). | Do not assume a digital reveal waives seven-day withdrawal rights; resolve before payment. |
| Platform and supplier liability | CDC supplier-chain rules; [STJ REsp 1.836.349](https://www.stj.jus.br/websecstj/cgi/revista/REJ.cgi/ITA?dt=20220624&formato=HTML&nreg=201901346226&salvar=false&seq=2181939&tipo=0). | The platform’s RNG, payments, custody, approval, or fulfillment role may create responsibility. |
| Payment/stored value | [Law 12.865/2013](https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/lei/l12865.htm), [BCB Resolution 494/2025](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?numero=494&tipo=Resolu%C3%A7%C3%A3o+BCB). | No internal wallet, reusable credit, or cash-out until payment counsel and a licensed PSP approve. |
| Minors and advertising | [ECA arts. 80–81](https://www.planalto.gov.br/ccivil_03/leis/l8069.htm), [CDC art. 37](https://consumidor.gov.br/pages/conteudo/publico/102), [CONANDA Resolution 163](https://www.gov.br/mdh/pt-br/acesso-a-informacao/participacao-social/conselho-nacional-dos-direitos-da-crianca-e-do-adolescente-conanda/resolucoes/resolucao-163-_publicidade-infantil.pdf/view), [ECA Digital Law 15.211/2025](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/l15211.htm). | Adults-only and no child-directed marketing are prudent pending specialist review and age-assurance guidance. |
| Data protection | [LGPD art. 14](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm). | Age/KYC, behavioral spend data, and fraud scoring require privacy design and counsel. |

# Required blockers before taking payment

1. Written classification memo and, if needed, SPA direction/authorization.
2. Written treatment of CDC Article 49 after reveal.
3. Licensed PSP/payment-flow approval; no wallet or guaranteed cash-out by default.
4. Verified seller entity, title, authenticity, custody, invoices, taxes, and reservation of every finite-pool item.
5. Reserve schedule covering handling, refunds, reversals, chargebacks, failed delivery, and remedies.
6. Approved Portuguese disclosure and valuation policy, including shortfall probability and no-cash-guarantee language.
7. Adults-only/age-assurance and responsible-use controls tested in the actual product.
8. Replayable verifier and immutable-manifest/state-transition tests, including concurrent purchases and jackpot-first depletion.

# Build/no-build boundary

**Build after blockers:** a finite-pool compiler, manifest/state ledger, replay verifier, custody/settlement controls, disclosure UI, and abuse/responsible-use controls.

**Do not build for launch:** unlimited unique-jackpot replenishment, arbitrary post-sale odds, internal wallet/cash-out, platform buyback or guaranteed RTP, creator self-purchases, value claims based only on optimistic listings, or a permanent 90% return promise.

These are scope and evidence boundaries, not a legal conclusion or a promise that the remaining candidate will be approved.

# Open questions

- What exact digest-to-uniform mapping and item ordering will the verifier use?
- Which state is snapshotted for simultaneous purchases and reservations?
- What valuation source, freshness window, condition equivalence, and dispute policy make a reference value reproducible?
- What platform thresholds define acceptable shortfall, concentration, margin, and reserve?
- Who is merchant/promoter/supplier for a creator-authored pack?
- Does SPA classify this flow as ordinary aleatory sale, promotion, lottery/game, betting, or a combination?
- How does Article 49 apply after an irreversible reveal?
- What custody, insurance, authenticity, tax, and invoice evidence is required?
- Which licensed PSP and settlement architecture can support the chosen flow?
- What stress witness validates dynamic pricing, or should the product pause rather than reprice?
- What comprehension test shows buyers can identify price, jackpot odds, below-price frequency, value basis, and no-cash-guarantee status?

## Dispatch closeout

- Final approver: **Vlachopulos, Ioannis**.
- Audit status: **pending parent close-row append or ACCEPT after this revision**; this file does not claim final acceptance.
- Synthesizer → explorers feedback revision required: **no**.
- Auditor → writer revision count: **1**.
- Dispatch role counts: `explorer=3`, `synthesizer=1`, `skeptic=3`, `writer=1`, `auditor=1`, `helpers=0`, `total=9`.
- `loops_used=1`.
- `exit_reason` will be finalized by the parent after audit.
- No implementation approval or legal approval is implied.
