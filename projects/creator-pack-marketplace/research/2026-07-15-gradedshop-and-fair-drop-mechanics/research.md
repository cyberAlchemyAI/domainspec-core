---
title: GradedShop And Fair Drop Mechanics Explorer Returns
status: collected
created: 2026-07-15
dispatch_id: 2026-07-15-creator-pack-marketplace-mechanics
dispatch_type: research
---

# Explorer Returns

The sections below preserve the three explorer returns verbatim. They are raw
research evidence, not accepted findings.

## Agent 1 — Shannon, Claude

## Shannon explorer report — GradedShop public mechanics

Evidence captured 2026-07-15. No files were written.

### Source table

| Source | Public evidence supported | Limits |
|---|---|---|
| [Whitepaper](https://www.gradedshop.com.br/whitepaper) | Pack lifecycle; standard vs tiered selection; HMAC formula; EV-margin model; sellback/voucher distinction; on-demand fulfillment; shipping; reference-price policy | First-party claims, not an audit; no digest-to-item algorithm |
| [Provably Fair](https://www.gradedshop.com.br/provably-fair) | SHA-256 server-seed commitment, client seed, nonce, seed rotation/reveal, HMAC recomputation | Verifies the HMAC value, but does not publish how that value selects an item |
| [FAQ](https://www.gradedshop.com.br/faq) | Rarity labels, payment, withdrawal, delivery, marketplace, physical-card threshold | Conflicts with the whitepaper/terms on fees, withdrawal, and delivery timing |
| [How it works](https://www.gradedshop.com.br/como-funciona) | Simple user flow: fund → choose → open → vault → sell/list/deliver | High-level marketing summary |
| [Terms](https://www.gradedshop.com.br/termos) | 18+ eligibility; random packs; reference values; on-demand fulfillment; vouchers/PIX; marketplace commission | Several current terms conflict with FAQ and whitepaper |
| [Public pack catalogue API](https://www.gradedshop.com.br/api/packs) | Price, type, configured target RTP, open count/cap, remaining openings, item/tier count | Live mutable snapshot; not a committed historical manifest |
| [Standard pack snapshot](https://www.gradedshop.com.br/api/packs/1474) | Exact item odds, rounded displayed percentages, market value, sellback value, quantities | No pack-version hash or historical state |
| [Tiered pack snapshot](https://www.gradedshop.com.br/api/packs/1489) | Tier odds, value ranges, item quantities, available counts, market/sellback values | No empty-tier or normalization rule |
| [RFC 2104](https://www.rfc-editor.org/info/rfc2104/) | HMAC is a keyed message-authentication mechanism | HMAC alone does not define random-number conversion or economic fairness |
| [Stake game-event documentation](https://stake.com/provably-fair/game-events) | Comparator showing that full verification publishes digest-to-float and float-to-outcome mappings plus the outcome table | Casino comparator, not a product/legal model to copy |

### Mechanics map

```text
Deposit
  → platform balance
  → select pack with displayed price/items/odds
  → open
      → HMAC(server_seed, client_seed + ":" + nonce)
      → undisclosed digest-to-roll conversion
      → standard: one weighted item roll
        OR
        tiered: tier roll → equal-probability item inside tier
  → won item enters virtual vault
      ├─ physical delivery
      ├─ sellback
      ├─ marketplace listing
      ├─ battle
      └─ upgrade
```

Observed facts and target claims:

- The whitepaper claims **standard packs** use one roll over individually weighted items.
- It claims **tiered packs** use two rolls: tier first, then equal selection among items in that tier.
- A live standard example, “Pack Blastoise,” costs R$60 and publishes exact odds totaling 100%. Its configured market-value EV is approximately R$48.60, matching its `target_rtp` of 81%; the sellback EV is approximately R$43.74, or 72.9% of price. This is an observed API calculation, not proof of long-run realized returns.
- The same API exposes exact `odds` but rounded `percentage`; rounded display values total 99.98% in that example.
- A live tiered example publishes tier percentages of 48%, 22%, 23%, 6%, 1%, and 0.10%, totaling 100.1%. This may be rounding or server normalization, but the public documentation does not say.
- The tiered pack exposes `quantity`, `card_count`, and `available_count`, indicating a finite-looking availability model. It does **not** prove physical custody.
- The whitepaper expressly says products are not held in GradedShop’s own physical stock; they are acquired from suppliers only after delivery is requested. If unavailable, the user may receive a voucher or substitute item.
- Values are first-party reference estimates that the platform reserves the right to change without notice. Sellback follows the platform’s current value.

### Cryptographic boundary

The supported part is narrow:

1. The site shows a hash of a secret server seed.
2. A client seed and nonce enter `HMAC-SHA256(server_seed, "client_seed:nonce")`.
3. Seed rotation reveals the server seed.
4. A user can recompute the HMAC and verify the revealed seed matched the earlier commitment.

That establishes seed/HMAC integrity if correctly implemented. It does **not**, from the published material, establish:

- how digest bytes become an unbiased number;
- how that number maps to cumulative item or tier ranges;
- item ordering;
- which pack configuration/version applied at opening time;
- that contents, weights, values, or quantities were committed before purchase;
- what happens when a selected tier has no stock;
- that an item exists, is custodied, or can be fulfilled;
- that valuations, RTP, creator margin, or reserves are fair.

Therefore the target’s claim that the platform “could not choose what you received” is broader than the published proof. A mutable outcome table can change the selected item while the same HMAC remains valid.

### Material disclosure conflicts

These should be treated as evidence-quality warnings, not reconciled by inference:

| Topic | FAQ | Whitepaper / Terms |
|---|---|---|
| Marketplace fee | Currently no fee; seller receives 100% | Commission is a revenue source / marketplace sales incur commission |
| Withdrawal minimum | R$20 | Terms say R$100 |
| Withdrawal timing | Manual review up to 3 business days, then PIX within 24h | Terms say up to 24 business hours |
| Withdrawable balance | FAQ says only deposited balance | Whitepaper says sellback balance is not withdrawable, marketplace vouchers are; terms say inventory can become withdrawable vouchers |
| Delivery | Preparation up to 3 business days, Correios 5–15 days | On-demand procurement and 15–45 business days |
| Payment | FAQ says PIX and card | Homepage emphasizes PIX; whitepaper names Mercado Pago/PIX |

### Transferable patterns

Useful for a multi-creator system, after hardening:

- Show every outcome, value, sellback value, and exact probability before purchase.
- Support standard weighted packs and tiered packs as distinct, explainable schemas.
- Show finite supply, remaining openings, and remaining item quantities where genuinely inventory-backed.
- Use server-seed commitment, user-controlled client seed, nonce, reveal, and a public verifier.
- Give winners explicit post-draw choices: delivery, marketplace sale, or clearly labeled platform credit.
- Separate deposited cash, non-withdrawable promotional/sellback credit, and withdrawable sale proceeds in both UI and ledger.
- Publish a creator margin/RTP calculation alongside price.
- Extend the target pattern with an immutable **pack-version manifest hash** covering item IDs, quantities, weights, tier rules, values, valuation timestamps, fulfillment terms, and creator identity.

### Non-transferable assumptions

- A central operator can revise values or substitute products without compromising trust.
- Supplier availability is equivalent to custody.
- “Provably fair” randomness makes the economics or fulfillment fair.
- Platform-assigned market value is realizable value.
- Equal choice within a tier stays fair while creators can change membership or quantities.
- A no-fee marketplace can be assumed as a durable business model.
- The current operator-controlled anti-abuse policy is sufficient for creator self-dealing, creator purchases, wash trades, or strategically changing inventory.
- Conflicting terms can be deferred until launch.

### Open questions for the synthesis

1. What exact byte-to-uniform-number and cumulative-range algorithms are used?
2. Is the complete pack manifest committed before the first sale and retained historically?
3. Are creator odds immutable after launch? If updates are allowed, do they create a new version?
4. Are rolls with and without replacement, and how do published odds change after depletion?
5. What happens when a tier is selected but no eligible item remains?
6. Are tier percentages normalized when they do not total exactly 100%?
7. What do standard-pack `quantity`, `max_opens`, and `shared_pool` each mean?
8. Who owns and custodies each item at sale time, especially a R$10,000 item?
9. Which value—market reference, sellback, realizable marketplace bid, or replacement cost—drives RTP and collateral?
10. Can creators buy/open their own packs or related accounts’ packs?
11. What reserve/collateral guarantees delivery or cash-equivalent restitution?
12. Which balance is legally and operationally withdrawable, and under what fee/refund policy?
13. Can a verifier reconstruct the exact won item from public inputs without trusting the platform API?
14. How are valuation sources, timestamps, disputes, substitutions, and condition/language differences disclosed?

Core conclusion: GradedShop demonstrates a compelling user loop and transparent-looking odds, but its public cryptographic proof stops at seed/HMAC integrity. A creator marketplace must additionally commit the economic state and fulfillment state of every pack version.

## Agent 2 — Laplace, Pierre-Simon

## Laplace explorer report — probability and marketplace economics

### Executive finding

For creator-authored packages containing unique physical items, the clearest and most controllable model is a **finite, prefunded inventory drawn without replacement**.

The public formula can be reduced to:

```text
Current item chance = remaining quantity of that item / remaining openings

Current tier chance = remaining items in that tier / remaining openings

Current expected value = total disclosed value of remaining items / remaining openings
```

A replenished weighted pool can keep constant odds, but it creates unbounded future supply/liability unless sales are capped or every possible prize can genuinely be replenished. It is unsuitable for a one-off R$10,000 collectible unless the platform can supply another identical prize after every win.

Cryptographic draw integrity and economic fairness must be separate claims. GradedShop says its HMAC-SHA256 construction commits a server seed and lets the buyer verify the draw afterward, but that does not prove the mapping, inventory, valuations, RTP, or solvency were fair. [GradedShop Provably Fair](https://www.gradedshop.com.br/provably-fair). NIST’s random-bit standards similarly address the construction of random generators, not marketplace economics. [NIST SP 800-90A](https://csrc.nist.gov/pubs/sp/800/90/a/r1/final).

### 1. Definitions and notation

For each item `i`:

- `q_i(t)`: quantity remaining at state `t`
- `w_i`: weight in a replenished pool
- `d_i`: disclosed/reference market value
- `g_i`: guaranteed realizable value—cash, credit, or binding buyback
- `a_i`: creator procurement/replacement cost
- `c_i`: fulfillment/settlement cost
- `tier(i)`: published tier
- `P`: buyer price, excluding separately disclosed shipping
- `αP + β`: payment processing cost
- `φP`: platform fee
- `o_i`: actual creator obligation cost for outcome `i`

`d_i`, `g_i`, and `a_i` are not interchangeable. If a card is advertised as “worth R$10,000,” but the platform guarantees only R$7,000 buyback, buyer-facing calculations must show both.

Use:

```text
Reference-value return = E[d] / P
Guaranteed-value RTP = E[g] / P
```

If there is no cash, credit, or binding buyback, call the first measure “expected reference-value ratio,” not RTP. An official regulatory definition treats theoretical RTP as the designed prize return and distinguishes it from observed actual RTP; volatility is commonly represented by standard deviation. [UK Gambling Commission definitions](https://www.gamblingcommission.gov.uk/licensees-and-businesses/guide/page/key-terms-relating-to-live-return-to-player-performance-monitoring-of-games).

### 2. Finite inventory without replacement

Let:

```text
N_t = Σ q_i(t)
p_i(t) = q_i(t) / N_t
p_tier,k(t) = Σ[i in tier k] q_i(t) / N_t
μ_d(t) = Σ p_i(t)d_i
μ_g(t) = Σ p_i(t)g_i
RTP_g(t) = μ_g(t) / P_t
```

After outcome `j`:

```text
q_j(t+1) = q_j(t) - 1
N_(t+1) = N_t - 1
```

All other quantities remain unchanged. Odds change only because actual inventory changed.

For a buyer purchasing `b` openings at once, the probability of receiving at least one item from a group with `Q` remaining copies is:

```text
1 - C(N_t - Q, b) / C(N_t, b)
```

At full exhaustion:

```text
Total disclosed value delivered = Σ q_i(0)d_i
Total guaranteed value delivered = Σ q_i(0)g_i
```

Those totals are deterministic. The order is random; the full-pool payout is not.

Advantages:

- unique prizes are natural;
- exact remaining inventory and liabilities are knowable;
- one jackpot is guaranteed to occur if the entire pool is opened;
- full-pool economics are exactly auditable.

Trade-off: later buyers face different odds. If the jackpot remains after 1,000 of 10,000 openings, its chance rises from `1/10,000` to `1/9,000`; if it was drawn, the chance is zero. Therefore initial odds alone are insufficient.

Safe options are:

1. Fixed price, with live odds, EV, and RTP displayed.
2. Deterministic dynamic price, for example `P_t = μ_g(t) / target_RTP`, with fees and margin constraints included.
3. Close the pool and issue a new version.

Manual creator edits after the first sale are unsafe. Quantity, values, tiers, mapping, price rule, and seed-to-outcome algorithm should be immutable under one configuration hash.

### 3. Replenished weighted pool

```text
W = Σ w_i
p_i = w_i / W
p_tier,k = Σ[i in tier k] w_i / W
μ = Σ p_i v_i
```

Probabilities stay constant between independent openings. Inventory must be replenished after every draw.

With a jackpot probability of `1/10,000`, after 10,000 openings:

```text
Expected jackpots = 1
P(no jackpot) = (9,999 / 10,000)^10,000 ≈ 36.79%
P(at least one jackpot) ≈ 63.21%
```

Thus “one expected jackpot” does not mean one jackpot will appear. In a finite 10,000-item pool with exactly one jackpot, full exhaustion guarantees exactly one.

An unlimited weighted pool has no finite worst-case monetary liability: an arbitrarily long sequence of jackpots is possible. A platform must therefore use at least one of:

- truly replenishable, prefunded inventory;
- a finite sales horizon `H`;
- a maximum sales cap;
- a per-opening admission check that pauses sales unless reserve covers the maximum next claim;
- third-party custody or enforceable creator collateral.

### 4. Buyer loss and volatility

For value basis `v_i`, where `v` must be labeled as reference or guaranteed:

```text
Buyer net X_i = v_i - P
Buyer loss L_i = max(0, P - v_i)

P(loss) = Σ[i: v_i < P] p_i
E[X] = μ - P
Variance(V) = Σ p_i(v_i - μ)^2
Standard deviation = sqrt(Variance)
```

The full loss distribution should be shown as probability atoms or buckets, not hidden behind EV. A high RTP can coexist with a 99.99% probability of losing money because a rare jackpot dominates the mean. The UK regulator likewise warns that RTP is a long-run average, not what an individual should expect in one session. [UK Gambling Commission RTP explanation](https://www.gamblingcommission.gov.uk/public-and-players/guide/return-to-player-how-much-gaming-machines-payout).

### 5. Creator and platform economics

Expected creator gross margin per opening:

```text
m = P - (αP + β) - φP - Σ p_i o_i
margin_rate = m / P
```

For a target minimum creator margin rate `ρ`:

```text
P ≥ (β + E[o]) / (1 - α - φ - ρ)
```

For a buyer guaranteed-RTP floor `R_min`:

```text
P ≤ E[g] / R_min
```

A configuration is feasible only if:

```text
(β + E[o]) / (1 - α - φ - ρ) ≤ E[g] / R_min
```

This is a useful validator: some combinations of prize pool, fees, buyer return, and creator margin are mathematically impossible.

Platform gross revenue is `φP`, but platform net must separately subtract fraud, refunds, customer support, warehousing, dispute, tax, payment, and replacement costs it bears.

### 6. Complete BRL witness

Assumptions:

- finite pool of 10,000 physical items;
- one item per R$20 opening;
- all items are custodied before launch;
- disclosed values are substantiated reference-market values;
- creator procurement cost averages 70% of disclosed value;
- payment cost is 3% + R$0.50 per opening;
- platform fee is 5%;
- average fulfillment/handling allocation is R$1.20 per opening;
- no shipping fee is silently deducted from prize value.

| Quantity | Value each | Initial chance | EV contribution |
|---:|---:|---:|---:|
| 1 | R$10,000 | 0.01% / 1 in 10,000 | R$1.00 |
| 9 | R$2,000 | 0.09% | R$1.80 |
| 90 | R$200 | 0.90% | R$1.80 |
| 900 | R$40 | 9.00% | R$3.60 |
| 1,000 | R$18 | 10.00% | R$1.80 |
| 8,000 | R$10 | 80.00% | R$8.00 |

Results:

```text
Total pool reference value = R$180,000
Reference EV per opening = R$18
Reference-value ratio = 90%
Jackpot EV contribution = R$10,000 × 0.0001 = R$1
Expected buyer net by reference value = R$18 - R$20 = -R$2
Probability reference value is below price = 90%
Variance = 13,892.40 BRL²
Standard deviation ≈ R$117.87
```

Buyer reference-value net distribution:

- 80%: lose R$10
- 10%: lose R$2
- 9%: gain R$20
- 0.9%: gain R$180
- 0.09%: gain R$1,980
- 0.01%: gain R$9,980

If guaranteed buyback is only 70% of displayed value:

```text
Guaranteed EV = R$12.60
Guaranteed-value RTP = 63%
Jackpot contribution to guaranteed EV = R$0.70
```

That contrast must be visible before purchase.

Provider economics under the physical procurement assumptions:

```text
Revenue = 10,000 × R$20 = R$200,000
Prize procurement = 70% × R$180,000 = R$126,000
Payment processing = 10,000 × R$1.10 = R$11,000
Platform fees = 10,000 × R$1.00 = R$10,000
Fulfillment allocation = 10,000 × R$1.20 = R$12,000
Creator gross margin = R$41,000 = 20.5% of sales
```

This is solvent only because the creator can procure the pool below its substantiated reference value. If “R$10,000” is merely an inflated listing price, both the 90% ratio and buyer fairness collapse.

### 7. Reserve and remaining liability

For finite inventory:

```text
Remaining stated-value liability = Σ q_i(t)d_i
Remaining guaranteed liability = Σ q_i(t)g_i
Remaining operational cost = Σ q_i(t)c_i
```

If physical inventory is custodied, prize liability is secured in kind; cash reserves still need to cover handling, replacement, refunds, and guaranteed buyback.

Without custody, reserve should not be based only on EV. If net sale proceeds available to settle one claim are `s`, deterministic worst-order prefunding is:

```text
K* = max over prefixes after sorting outcomes descending by
     (g_i + c_i - s)
     of the positive cumulative deficit
```

This asks whether the pool survives the jackpot arriving first, not merely on average.

For weighted unlimited pools, deterministic worst-case liability is unbounded. For a cap of `H` future openings, a conservative bound is:

```text
K ≥ H × max(0, g_max + c_max - s)
```

A less capital-intensive system can admit one sale only when current collateral plus its net proceeds covers the maximum next settlement, then pause if reserve is depleted.

### 8. Candidate guardrails

- Prefer finite pools for unique physical collectibles.
- Creator dials operate pre-launch only; post-launch changes create a new version.
- Publish initial and current odds as fraction, percentage, and “1 in N.”
- Publish both reference-value return and guaranteed-value RTP.
- Show probability of loss and at least one volatility measure.
- Require a valuation source, timestamp, transaction basis, and refresh/expiry rule.
- Custody all finite-pool prizes before launch, or collateralize replacement liability.
- Require the margin/RTP feasibility inequality to pass.
- Price and odds updates must be automatic consequences of a published formula.
- Do not allow a weighted outcome unless stock or cash settlement can be replenished.
- Stop sales when inventory, reserve, valuation freshness, or settlement SLA fails.
- Keep tier names cosmetic: probabilities derive only from quantities or weights.
- Commit the configuration hash, mapping algorithm, inventory version, and randomness inputs before accepting a purchase.
- Describe randomness integrity, economic return, solvency, and legal permissibility as four separate properties.
- Treat Brazil’s clear-information requirements as a legal-review input, not proof of permissibility: Articles 6, 30, and 31 require adequate, clear, precise offer information and make sufficiently precise advertising binding. [Brazil Consumer Defense Code](https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm).

### 9. Machine-testable invariants

```text
quantities are non-negative integers
weights are non-negative and not all zero
sum(item probabilities) = 1
sum(tier probabilities) = 1
tier probability = sum(member item probabilities)
finite remaining count = sum(remaining quantities)
one draw decrements exactly one quantity and total count by one
no draw occurs when remaining count = 0
finite EV = remaining total value / remaining count
full-pool delivered totals equal committed configuration totals
configuration hash is unchanged after first sale
state changes only through accepted draw/settlement transitions
displayed odds equal state-derived odds
displayed EV and RTP recompute exactly from disclosed values
guaranteed value never exceeds enforceable settlement terms
creator stress margin is non-negative
collateral >= required reserve rule
sold openings never exceed finite pool count or weighted sales cap
random integer mapping has no modulo bias
every outcome index is reachable
draw record binds seed commitment, nonce, config hash, and state version
```

### 10. Failure cases

- HMAC is valid but the seed-to-item mapping was not committed.
- Jackpot is already gone while stale initial odds remain displayed.
- Creator silently changes quantities, weights, tiers, or values after purchases.
- “RTP” uses aspirational marketplace listings instead of guaranteed settlement value.
- Shipping, fees, or withdrawal friction reduce realized value but are excluded.
- A finite pool has positive EV but no custodied inventory or replacement reserve.
- A weighted pool offers a unique item it cannot replenish.
- A high average conceals a 90–99.99% loss probability.
- Dynamic price is discretionary rather than formula-derived.
- Creator can buy from or inspect its own pool using nonpublic state.
- The pool remains for sale after a valuation source expires or fulfillment fails.

The strongest candidate is therefore a **versioned finite-pool contract with prefunded inventory, automatic live odds, dual value/RTP disclosure, explicit loss distribution, and deterministic price/reserve validators**. This is computationally feasible; legal classification and permissibility remain separate questions for Sunstein’s lane.

## Agent 3 — Sunstein, Cass

## Sunstein explorer report — Brazil legal and responsible-design lens

Current through 15 July 2026. This is issue-spotting research, not legal advice. I do not conclude that the product is legal or illegal as a whole.

### Bottom line

Do not accept money for creator-authored randomized packages until Brazilian counsel classifies the exact transaction and, ideally, the Secretariat of Prizes and Betting (SPA) gives written direction.

The central unresolved question is whether each purchase is:

1. an ordinary sale of an unidentified but guaranteed physical product;
2. a sale plus a regulated commercial promotion;
3. an unauthorized lottery or game of chance;
4. an authorized fixed-odds online betting product; or
5. some combination with regulated payment or stored-value services.

A transparent HMAC draw and a solvent expected-value formula do not answer that question. They prove, at most, one aspect of random-selection integrity.

### Classification map

**Ordinary aleatory sale — lower regulatory risk, still uncertain.** This characterization is strongest when every purchase transfers a genuine, pre-existing physical item; the purchaser is paying for that item rather than an entry or separate prize; the pool is fully owned and reserved; there is a meaningful guaranteed floor; there is no platform-guaranteed cash-out; and values are not represented as guaranteed investment returns.

**Commercial promotion.** [Law 5.768/1971](https://www.planalto.gov.br/ccivil_03/leis/l5768compilado.htm), [Decree 70.951/1972](https://www.planalto.gov.br/ccivil_03/decreto/antigos/d70951.htm), and [Portaria SEAE/ME 7.638/2022](https://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer?captchafield=firstAccess&data=20%2F10%2F2022&jornal=515&pagina=25) regulate free prizes used as advertising through draws, instant gifts, contests, and analogous operations. Purchasing a product can be the participation condition, so “free” does not necessarily mean “no purchase required.” An instant gift placed inside a product is expressly recognized as `vale-brinde`.

If classified this way:

- prior SPA authorization is required;
- only eligible legal persons may be authorized—natural-person creators cannot independently run it;
- requests are normally filed 40–120 days before the promotion;
- prizes cannot be converted into cash;
- total prizes are generally capped relative to operating revenue;
- ownership of instant prizes must be proven before launch;
- tax and post-campaign accounting apply.

The current [SPA promotion FAQ](https://www.gov.br/fazenda/pt-br/composicao/orgaos/secretaria-de-premios-e-apostas/promocao-comercial/promocao-comercial) is especially problematic for this concept: plans cannot stimulate gambling, create exaggerated expectations of prizes, become a revenue source from the chance mechanic, harm minors, or condition awards on assembling series or collections. Collectible-card packs and prominent “R$10,000 hit” marketing can touch several of those factors. This does not prove classification, but it makes a promotion-based route structurally difficult.

**Unauthorized lottery or game of chance.** [Decree-Law 3.688/1941 arts. 50–51](https://www.planalto.gov.br/ccivil_03/decreto-lei/del3688.htm) defines a game of chance as one in which gain and loss depend exclusively or mainly on luck. It also defines an unauthorized lottery broadly as an operation using tickets, lists, coupons, symbols, or analogous means where a draw determines receipt of money or goods. A web purchase that chiefly buys a tiny chance at a high-value card, particularly with a low-value floor and cash exit, is exposed to this characterization. The fact that everyone receives *something* reduces but does not eliminate the issue if economic gain or loss still depends mainly on chance.

**Fixed-odds online betting.** [Law 14.790/2023](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14790.htm) defines a bet as placing value at risk expecting a prize and defines online games through future random events generated electronically. But fixed-odds betting also uses a fixed multiplier for a monetary stake and prize. Physical card delivery does not fit that model cleanly. Classification is therefore uncertain, not safely excluded. If it did apply, operating without SPA authorization and the regulated betting structure would be a blocker.

### Main risk findings

| Risk | Authority and proposition | Facts that increase risk | Uncertainty and required confirmation |
|---|---|---|---|
| Chance-product classification | Laws and regulations above distinguish commerce, promotions, lotteries, and betting by substance rather than product label. | Tiny floor, emphasized jackpot, repeat openings, platform RNG, direct payment for each chance, buyback. | **High.** Brazilian gaming/promotions counsel plus written SPA direction. |
| Creator-authored packs | Promotion authorization is available only to eligible legal persons; collective promotions impose responsibilities on participating entities. | Natural-person creators, instant self-service launch, creator-controlled odds or inventory. | **High.** Promotions counsel must determine whether creator, platform, or both are promoter/supplier/operator. |
| Consumer information | [CDC arts. 6, 30–31, 36–38](https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm) require adequate, correct, clear, prominent Portuguese-language information; precise offers bind; misleading omission is prohibited; the advertiser bears proof of claims. | “Provably fair” used without economic disclosures; unverifiable R$10,000 value; hidden margin, quantities, replacement policy, fees, or loss probability. | **Medium-high.** Consumer counsel should approve every disclosure and valuation method. |
| Excessive advantage | CDC arts. 39 and 51 prohibit manifestly excessive advantage and clauses producing exaggerated disadvantage or conflicting with good faith. | Very low redeemable EV, inflated reference values, discretionary substitutions, unilateral odds changes, waiver of refunds. | **Medium-high:** open-ended, fact-specific standards; consumer economist and counsel needed. |
| Withdrawal after reveal | [CDC art. 49](https://consumidor.gov.br/pages/conteudo/publico/102) and [Decree 7.962/2013](https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/decreto/d7962.htm) generally provide seven days to withdraw from online purchases with full refund and same-channel cancellation. Official guidance does not establish a general mystery-pack exception. | Instant reveal lets consumers retain winners and cancel losers; terms attempt to waive withdrawal; card is shipped immediately. | **High and economically load-bearing.** Consumer/e-commerce counsel must determine when the contract is performed and what rights survive reveal/opening. |
| Marketplace responsibility | CDC supplier-chain rules can create objective or solidary responsibility. [STJ REsp 1.836.349](https://www.stj.jus.br/websecstj/cgi/revista/REJ.cgi/ITA?dt=20220624&formato=HTML&nreg=201901346226&salvar=false&seq=2181939&tipo=0) says platform liability depends on its concrete role. | Platform sets rules, approves configurations, supplies RNG, processes money, holds goods, advertises value, or resolves fulfillment. | **Medium-high.** Calling content “user-generated” will not itself remove platform responsibility. Marketplace counsel required. |
| Inventory, title, and fulfillment | The CDC makes offers binding and requires delivery as promised. Under promotion rules, instant-prize ownership is proven before launch; see [SPA ownership guidance](https://www.gov.br/fazenda/pt-br/composicao/orgaos/secretaria-de-premios-e-apostas/promocao-comercial/promocao-comercial/quando-a-propriedade-dos-premios-deve-ser-comprovada). | Creator custody, counterfeit cards, double-listing, substitution after sales, unfunded R$10,000 item. | **Medium.** Commercial, insurance, tax, and promotions counsel must approve custody/title model. |
| Payment and cash-out | [Law 12.865/2013](https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/lei/l12865.htm) defines payment arrangements, payment accounts, and electronic money. [Resolution BCB 494/2025](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?numero=494&tipo=Resolu%C3%A7%C3%A3o+BCB) now requires payment institutions to seek authorization before starting regulated payment services. BCB guidance recognizes that marketplaces receiving and repassing funds may act as sub-acquirers. | Internal wallet, reusable credits, creator balances, withdrawals, customer-fund escrow, transfers between users, instant platform buyback. | **High.** Payments counsel and a licensed PSP/acquirer must classify the flow before build. |
| Minors and child-directed design | [ECA arts. 80–81](https://www.planalto.gov.br/ccivil_03/leis/l8069.htm) restrict minors’ access to gambling and lottery equivalents. [CDC art. 37](https://consumidor.gov.br/pages/conteudo/publico/102) and [CONANDA Resolution 163](https://www.gov.br/mdh/pt-br/acesso-a-informacao/participacao-social/conselho-nacional-dos-direitos-da-crianca-e-do-adolescente-conanda/resolucoes/resolucao-163-_publicidade-infantil.pdf/view) treat exploitation of children’s judgment as abusive advertising. | TCG imagery, influencers popular with children, countdowns, collections, near misses, repeat-opening prompts. | **High.** Child-rights and advertising counsel; provisional adults-only treatment is prudent. |
| ECA Digital and age assurance | [Law 15.211/2025](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/l15211.htm) applies to digital services directed to or probably accessed by minors. [Decree 12.880/2026](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/decreto/d12880.htm) requires protective design and age measures for prohibited content. Paid loot boxes are expressly barred for minors in electronic games, though physical-card mystery packs are outside that definition’s clear core. | Minor-accessible platform, randomized purchase resembling loot boxes, self-declared age only, behavioral ads. | **High.** ANPD guidance is still evolving; use child/privacy counsel and monitor [ANPD’s 2026 age-assurance process](https://www.gov.br/anpd/pt-br/assuntos/eca-digital). |
| Personal data | [LGPD art. 14](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm) requires children’s and adolescents’ best interests; general LGPD principles require lawful basis, necessity, transparency, security, and rights handling. | Identity/KYC, age documents, behavioral spend profiles, fraud scoring, targeted jackpot ads. | **Medium-high.** Privacy counsel and a DPIA/RIPD before collecting age or identity evidence. |

### Effects of the specific design choices

- **Guaranteed physical value:** helps only if it is genuine, liquid, objectively valued, and meaningfully close to price. A nominal “R$50 card” with no realistic buyer may still represent economic loss.
- **Platform-guaranteed buyback:** materially raises gambling, lottery, payment, liquidity, and solvency risk; it also makes the advertised value closer to cash.
- **Independent peer-to-peer resale:** weaker cash-equivalence signal, but creates marketplace, fraud, counterfeit, tax, and wash-trading risks.
- **Creator custody:** reduces platform warehousing but increases non-delivery, substitution, counterfeit, and double-sale exposure.
- **Platform custody:** improves proof and fulfillment but strengthens the inference that the platform is functionally part of the supply/promotion chain.
- **Creator-selected odds:** does not transfer compliance away from the platform if the platform supplies the engine, approval, money flow, or marketing.
- **A tiny R$10,000 chance:** no probability is a legal safe harbor. The smaller and more heavily advertised the chance, the stronger the “exaggerated expectation” and chance-profit concerns.

### Hard blockers before taking payment

1. Obtain a written classification memorandum from Brazilian gaming/promotions and criminal-regulatory counsel; approach SPA for written direction on the exact flow.
2. Resolve the seven-day withdrawal problem after digital reveal. Do not assume terms can waive it.
3. Freeze wallet, balance, withdrawal, platform buyback, or creator payout flows until payments counsel and a licensed PSP approve the architecture.
4. Decide and implement a minors policy. Until cleared, use reliable 18+ age assurance, no child-directed promotion, and no self-declaration-only gate.
5. Require documented title, custody, authenticity, and reservation of every item before the first sale.
6. Determine whether creators must all be verified legal persons and how invoices, ordinary sales taxes, promotion taxes, and seller reporting work.
7. Define who legally contracts with the buyer: creator, platform, or both. Terms cannot simply disclaim supplier-chain obligations.

### Configurable guardrails

- Permit only finite, pre-custodied pools at launch.
- Make pool contents, quantities, tier mapping, odds, and seed commitments immutable after the first sale.
- Show both percentage and “1 in N” odds before payment.
- Disclose remaining inventory and recalculated odds when drawing without replacement.
- Show package price, all fees, shipping, creator/platform margin, expected nominal value, expected realistically redeemable value, floor, maximum, and loss probability.
- Date every valuation and use completed-market transactions or a funded buyback—not optimistic listing prices.
- Ban creator purchases of their own packs, insiders, wash trades, artificial sales, and inventory substitution.
- Separate the RNG statement from economic claims: “draw reproducible” must not become “economically fair.”
- Add spending caps, cooling-off periods, purchase history, loss summaries, voluntary exclusion, and friction before repeat purchases.
- Ban autoplay, near misses, countdown pressure, “almost won,” loss-chasing prompts, and influencer campaigns likely to reach minors.
- Use a licensed PSP for per-transaction payments and direct settlement; avoid an internal wallet in the first version.
- Provide Portuguese-language contract summaries, same-channel cancellation, complaint channels, fulfillment deadlines, return procedures, and auditable dispute logs.

### Questions public sources cannot answer conclusively

- Does SPA consider a paid randomized physical-card package an ordinary sale, `vale-brinde`, analogous promotion, lottery, or betting product?
- Does guaranteed delivery of a physical item remove “gain and loss” from article 50 when values vary dramatically?
- Does a platform buyback turn a card prize into prohibited cash conversion or evidence of a wager?
- How does CDC article 49 operate after an irreversible digital reveal but before physical shipment?
- Is every creator a promoter/supplier, or can the platform act as sole merchant/promoter?
- Can a continuously self-service creator marketplace fit the promotion authorization timetable?
- Which valuation method would authorities accept for thinly traded collectible cards?
- Does the proposed wallet/escrow/cash-out structure make the platform a payment institution, sub-acquirer, or merchant of record?
- What state and municipal tax, invoice, warehouse, and second-hand-goods obligations apply?
- Which final ANPD age-assurance requirements will govern this service after the current preliminary 2026 guidance is replaced?

The strongest legally conservative first hypothesis is therefore: verified adult legal-person sellers, pre-custodied finite physical inventory, no wallet or guaranteed cash-out, no credit, no child-directed marketing, exhaustive odds/value disclosure, and no launch until the classification and withdrawal questions are resolved.
