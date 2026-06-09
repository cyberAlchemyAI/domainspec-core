---
node_type: discovery
status: exploratory
topic: GoldenQuill / Tilth — engineer-view (the mechanics and the verdicts)
last_updated: 2026-06-09
created_by: victorboscaro@gmail.com
---

# Engineer-view — GoldenQuill / Tilth

> This is the **engineer-view** of a two-view pair. Its companion, [`system-view.md`](system-view.md),
> explains the *shape* one conceptual layer at a time and **names** the load-bearing stances
> without deciding them. This view **refines** that one down to the contracts, schemas, and the
> decision inventory — and it is where every named stance gets its **single owning verdict**.
> Nothing is decided twice: where a stance is relevant to both altitudes, system-view points
> here, and the verdict lives only here.
>
> For the plain-language orientation and the open *business* questions, see
> [`discovery.md`](discovery.md) (the layperson walkthrough + eligibility ladder + Q1–Q6).
> Every factual claim below points to the file it came from.

---

## What this view owns

Four things system-view defers here:

1. The **decision inventory** — every load-bearing decision with its verdict and status
   (RESOLVED / OPEN / CRITICAL), including the designed-but-not-built rows.
2. The **schemas and contracts** — the Scout candidate + VERIFY record, the Match Database +
   REVIEW action, the classification register, the CIC card structure, the failure-code families.
3. The **runtime match mechanics** — exactly how the two axes are joined under announcement
   precedence, and how the coupling guard is enforced.
4. The **eligibility ladder** — how discovery, volume-trimming, live verification, and the
   human review gate wire together, and where the dedicated eligibility filter sits (and why it
   is not yet wired in).

---

## 1. Decision inventory

Status legend: **RESOLVED** (decided and enforced) · **OPEN** (named, not decided) ·
**CRITICAL** (OPEN *and* blocks the value thesis until built).

| # | Decision / stance | Verdict | Status | Authority |
|---|---|---|---|---|
| D1 | **CIC×CLC coupling** — is any design-time link between the axes admissible? | **No.** Any hardcoded CIC→CLC subset (even advisory) is a category error; matching is opportunity-driven at runtime. Enforced fail-closed. | **RESOLVED** | `F-CIC-CLC-COUPLING-VIOLATION`, architecture v7.0.8 (2026-05-08); [CLAUDE.md](../CLAUDE.md) L260 |
| D2 | **Substrate** — train per-client weights, or improve context? | **Improve context, never weights.** Substrate LOCKED (Pydantic AI + Logfire + Ollama/vLLM + DSPy/GEPA offline card refinement + Logician). | **RESOLVED** | ADR-001, architecture v7.0.3 (2026-05-08); [CLAUDE.md](../CLAUDE.md) §"What NOT to Do" |
| D3 | **Cloud-vs-local routing** — how is confidential data protected? | **Three customer-selected postures** (Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign), per-field classification register drives each call; fail-closed to LOCAL when indeterminate. | **RESOLVED** | architecture v7.0.10 (2026-05-11); [CLAUDE.md](../CLAUDE.md) §"Beta Model Strategy" |
| D4 | **Eligibility decision point** — cache or live? | **Live synopsis only.** Cache (`fit_score_cached`) never decides eligibility; only Scout VERIFY against the live announcement. | **RESOLVED** | L-001; `section_03_scout.md` L141/L168 |
| D5 | **Calibration discipline** — how to tune per-seat posture, variants, model team against outcomes? | *Designed-but-not-built.* No enforced practice exists for calibrating execution parameters against grant outcomes. | **OPEN** | [discovery.md](discovery.md) §5; no running gate in repo |
| D5a | **Optimization target for shared cards** — what single metric does the card-refinement loop maximize toward? | **None.** Shared cards are **guardposts** kept deliberately general; no global north-star metric. Two optimization surfaces, neither subordinate: the shared card (general/compounding) and the per-org/per-project layer (specific/sovereignty). Does not constrain per-proposal scoring — Judge/Red Team still optimize a single draft toward the funder rubric, per proposal, not card hill-climbing. | **RESOLVED** (Josh) | [discovery.md](discovery.md) §8 Q1, §6 |
| D6 | **Eligibility filter productization** — the zero-token hard-disqualifier filter. | *Not wired in, and hardcoded to one client.* Must move the eligibility profile out of code into per-client data (PROJECT_CONTEXT + KFR) before it can serve any client but MycoSymbiotics. | **OPEN** | `logician/filters/eligibility_filter.py` (zero callers; profile baked at L8) |
| D7 | **The learning loop** — does each outcome auto-improve the shared cards? | *Designed, not built.* Today a human edits cards by hand; the whole automatic loop (shared-card refinement **and** per-org accumulation feedback) is design-only. The value thesis is a **per-org compounding engine**: each org's accumulated context (KFR + Match DB) deepens inside the guardposts, while shared-card refinement is **bounded to a general guardpost level, not hill-climbed toward any single metric** (per D5a — no global north-star, no guardrailed-composite / expected-dollars-won objective function over the shared corpus). That thesis does not hold until the loop is built with governance. | **CRITICAL** | [system-view.md](system-view.md) §"learning loop"; [discovery.md](discovery.md) §3; D5a |
| D8 | **Moat vs sovereignty** — is the accumulated corpus a defensible moat? | **No lock-in moat by design.** The client owns and can walk with everything; per-client corpora are Law-3-isolated; the only cross-client asset (funder intelligence) is the least defensible (public-derived). The defensible asset, if any, is the *rate* of improvement — and per D5a that edge lives in the **per-org** accumulated context (KFR + Match DB) plus each org's work *within* the general guardposts; cross-client shared-card improvement is **bounded to a general guardpost level, not maximized toward a metric**. The Funder Intelligence DB stays on the shared/cross-org side (least defensible), never folded into the per-org bucket. | **OPEN** (business) | [discovery.md](discovery.md) §5 + Q3; D5a; [CLAUDE.md](../CLAUDE.md) §"Sovereignty Promise" |
| D9 | **Business model** — what is owned outright vs subscribed? | Stance: separate "what the client owns" (machine, data, today's snapshot) from "the shared-intelligence subscription" (the *stream* of improvements). Unresolved tension with "nothing is held hostage." | **OPEN** (business) | [discovery.md](discovery.md) Q3 |
| D10 | **v0.2 post-award agents** — Data Collector + Report Generator. | Spec LOCKED (§13/§14, v1, 2026-05-10) but **not active in v0.1**; partial code on disk only. | **OPEN** (horizon) | [CLAUDE.md](../CLAUDE.md) §"v0.1 vs v0.2 boundary" |

The OPEN/CRITICAL rows (D5–D9) are the ones a stakeholder must weigh to judge soundness. **D7
is the single decision that gates the value thesis** — see §6.

---

## 2. Schemas and contracts

### 2.1 Scout candidate record + VERIFY
Source: `pipeline/blueprint/v0.1/section_03_scout.md` (LOCKED 2026-04-17).

Candidate record carries: `candidate_id` (sha3_512), `channel` (`"A"`–`"F"`), `feed_or_adapter_id`,
`funder`, `funder_kind`, `url`, `close_date_utc`, `award_ceiling`/`award_floor`, `applicant_types`,
content hashes, and:
- **`fit_score_cached: int`** — range `0..100`, "cache-only heuristic; **NOT a VERIFY decision**" (L141).

**VERIFY verdict enum** (L155) — eligibility is decided *here* and only here:
```
"VERIFIED_FIT" | "VERIFIED_NOT_FIT" | "UNVERIFIED" | "VERIFICATION_FAILED"
```
- `VERIFIED_FIT` — live synopsis matches eligibility + scale. **Only this state elevates to
  CRITICAL-fit for REVIEW** (L168).
- `VERIFIED_NOT_FIT` — live mismatch. `UNVERIFIED` — no live endpoint. `VERIFICATION_FAILED` — fetch error.

**Pre-VERIFY truncation** (does NOT decide eligibility): sort by `fit_score_cached` desc with a
per-run-seeded tiebreak, truncate to `SCOUT_CANDIDATE_VERIFY_CAP = 1000` (L660/L1408). Overflow
recorded via `F-SCOUT-V-05`; overflow >25% of cap flips VERIFY to DEGRADED.

**Operator REVIEW enum at the Scout stage** (L212):
```
operator_decision: "ACCEPT" | "REJECT" | "HOLD" | None
```
Only `ACCEPT` flows to Scribe. ⚠️ Note the vocabulary differs from the Match-DB action enum
(§2.2) — two source files use different operator-decision words; reconcile before either is
surfaced externally.

### 2.2 Match Database + REVIEW action
Source: `pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md` (LOCKED 2026-05-10).

Record fields: `match_id`, `funder_doc_id`, `proposed_at`, `match_score` (0.0–1.0),
`match_reasoning` (structured booleans: sector/funding-world/eligibility/scale/identity/geography +
narrative with its own classification), and:
```
operator_action.action: confirmed_fit | rejected | declined_cycle | pending   (L143)
consent_tier: my_eyes_only | matchable_to_opportunities | composable_with_others
```
**Scope (Law 3):** per-org at `orgs/<slug>/match_database/`; cross-org reads blocked by
`F-MATCH-DB-CROSS-ORG` (L159). This is the layer that does **not** compound across clients.

### 2.3 Classification register (the routing primitive)
Four per-field values (architecture v7.0.10): `public | shareable | confidential | operator_flagged`.
Routing per posture (D3):
- **Frontier-Eligible** → public/shareable → cloud; confidential/operator_flagged → local.
- **Split-Context Hybrid** → cloud sees structure/framing on a signed allow-list only; substance local.
- **Local-Only/Sovereign** → everything local.
Indeterminate class → fail-closed LOCAL (`F-CLASS-ROUTING-INDETERMINATE`).

### 2.4 CIC card structure
Source: `pipeline/cards/CIC/food_systems.yaml`. Top-level keys: `search_vocabulary`,
`evidence_signals`, `kfr_fact_classes`, `provenance_requirements`, `register_defaults`,
`dialect_routing_table`, `admin_risk_term_register`, `reporting_cadence_typical`,
`metrics_table_template`, `narrative_sections_typical`, `capacity_signals_required`,
`compliance_burdens`, `common_risk_register_entries`, `common_funders_observed`, `lifecycle`.

`provenance_requirements` (the CIC's "how to prove each fact" defaults), verbatim:
- `annual_revenue` → `"Schedule F or audited P&L or signed self-attestation with backing tax doc"`
- `buyer_relationships` → `"signed letter, LOI, or invoice — verbatim buyer name + commitment terms"` (`verbatim_quote_required: true`)
- `certifications_held` → `"certifying body letter or audit report with cert ID + expiration"`

`dialect_routing_table` (Law 4): `conservative→scribe.formal_commercial`,
`centrist→scribe.technical_precise`, `progressive→scribe.movement_aligned`,
`soul_fire→scribe.cooperative_solidarity`.

> Note for the orthogonality argument (§4): the card carries both provenance defaults *and*
> `sub_register_selection_rule`/`dialect_routing_table` — i.e. emphasis machinery driven by the
> runtime CLC lives inside the CIC artifact. This is why §4 calls the runtime answer a **join
> under precedence**, not a clean axis split.

### 2.5 Failure-code families
Source: [CLAUDE.md](../CLAUDE.md).
- **F-CLASS-*** — 16 primitives (v7.0.10 LOCKED 2026-05-11): 10 legitimate-runtime + 2
  repurposed defense-in-depth + 4 new (POSTURE-MID-CYCLE-CHANGE, SPLIT-CONTEXT-ALLOWLIST,
  SPLIT-CONTEXT-LEAK, HEAVY-JUDGE-CLOUD-DOWNLOAD).
- **F-WPFA-*** — 12 primitives (§17 v1 LOCKED 2026-05-11; predicate bodies LIVE).
- **F-PACKET-*** — 19 signatures registered (1 LIVE META; 18 `NotImplementedError` at v0.1 hook).
- **F-CIC-CLC-COUPLING-VIOLATION** — architecture v7.0.8 (2026-05-08); enforces D1.
- **F-PIPE-TRACK-NOT-SHIPPABLE** — refuses `report_mode` until v0.2 LOCK flips `shippable_in`.

---

## 3. The eligibility ladder

Cheapest → most expensive. Eligibility is decided only at VERIFY (D4).

1. **DISCOVER** — six parallel channel families, all primary (none a fallback):
   A Grants.gov `search2`/`fetchOpportunity` + SAM.gov + USASpending · B curated cached datasets
   via `vault_read` · C seeded state/foundation portal fetchers · D federal program pages (ALN) ·
   E RSS/Atom/newsletter watchlists · F client-material web search (SearxNG default; Brave BYOK opt-in).
2. **Pre-VERIFY truncation** — `fit_score_cached` sort → top `1000`. Trims volume only; explicitly
   not an eligibility decision.
3. **VERIFY** — live synopsis → one of the four states (§2.1). `VERIFIED_FIT` elevates.
4. **REVIEW (human)** — operator `ACCEPT`/`REJECT`/`HOLD` (Scout stage) → Match-DB
   `confirmed_fit`/`rejected`/`declined_cycle` (§2.2).

**Where the dedicated eligibility filter sits — and why it's not wired in (D6).**
`logician/filters/eligibility_filter.py` is a zero-token hard-disqualifier filter
(`filter_opportunity` / `filter_batch`). It has **zero callers** anywhere in Scout (verified) and
its profile is **hardcoded to MycoSymbiotics Cooperative** (docstring L8): `HARD_DISQUALIFIERS`
(e.g. `"state governments only"`, `"tribal governments only"`, `"nonprofits only"`),
`POSITIVE_SIGNALS` (e.g. `"cooperative"`, `"mushroom"`, `"pennsylvania"`, `"remediation"`),
`AGENCY_WHITELIST` (`USDA-NIFA`, `NSF`, `SBA`, `EPA`, …). To productize, this profile must move
out of code into per-client data (PROJECT_CONTEXT + KFR). The root-level `logician/` copy was
flagged as a possible stale shim duplicating `pipeline/logician/`.

---

## 4. Runtime match mechanics + the coupling guard (D1)

The match is **computed, never looked up.** Per opportunity:

1. Scout/Logician read the live announcement and name the **CLC** (funder-side).
2. The client's classified **CIC** sets the seat configuration (search vocabulary, provenance
   defaults, register).
3. The answer is a **join under precedence**, not a table lookup:
   - **Provenance** = announcement (RFA) first, CIC default second (Law 1: solicitation > card).
     The CIC `provenance_requirements` only fill the silence.
   - **Emphasis** = the CLC's priority logic applied to *the facts the client actually holds*
     (funder logic ∩ KFR) — not a pure funder-side projection.
4. **Coupling guard:** no CIC→CLC subset may be baked into any card, schema, prompt, or weight —
   `F-CIC-CLC-COUPLING-VIOLATION` fail-closes. Two lists (6 + 8 = 14 authored units) instead of one
   48-cell table is a normalization decision (linear authoring cost, independent evolution, no
   update anomalies), **not** a claim that the axes are statistically independent — some pairs are
   common, some rare; none is forbidden.

This is the practical defense of system-view's "protagonist claim," and the Logician is the seat
that enforces it.

---

## 5. The named stances — verdicts

- **Coupling (D1)** — RESOLVED: no design-time coupling; guard enforced. See §4.
- **Calibration discipline (D5)** — OPEN: there is no built practice for tuning execution
  parameters against outcomes. Until there is, "execution parameters are optimized" is aspirational.
- **Moat vs sovereignty (D8)** — Verdict: **no lock-in moat by design.** Sovereignty is a
  deliberate anti-moat; retention must come from continuous value, never captivity. Per D5a, the
  rate-of-improvement edge lives in the **per-org** accumulated context (KFR + Match DB) plus each
  org's work *within* the general guardposts; cross-client shared-card improvement is **bounded to
  a general guardpost level, not maximized toward a metric.** The Funder Intelligence DB stays the
  shared/cross-org (least-defensible) asset, never per-org. Business framing remains OPEN (D9).
- **Learning-loop criticality (D7)** — **CRITICAL.** The value thesis is a **per-org compounding
  engine** (each org's KFR + Match DB deepening inside the guardposts); shared-card refinement is
  **bounded to a general guardpost level, not hill-climbed toward any single metric** (per D5a —
  no guardrailed-composite / expected-dollars-won objective function over the shared corpus). That
  thesis does not hold until the outcome→insight→operator-approved→card-update loop is built *with
  governance* (no auto-promotion: one noisy outcome must not corrupt a shared card for every
  same-CIC client). This is the highest-priority build gap in the product.
- **Business model (D9)** — OPEN: separate owned-outright from the shared-intelligence
  subscription, and resolve the subscription-vs-"nothing held hostage" tension before pricing.
  Also unpriced: the operator-approval throughput ceiling and BYOK support cost (neither compounds
  down) — see [discovery.md](discovery.md) Q6.

---

## 6. Cross-reference map

- **Shape / stakeholder altitude:** [`system-view.md`](system-view.md) — names these stances; this
  doc owns their verdicts.
- **Layperson orientation + open business questions (Q1–Q6):** [`discovery.md`](discovery.md).
- **Canon:** [CLAUDE.md](../CLAUDE.md), [README.md](../README.md), and the architecture/blueprint
  files cited inline above.

To keep the three docs from drifting on shared claims, each load-bearing claim has one authored
home: the **shape** in system-view, the **plain-language walkthrough** in discovery, the
**verdict + contract** here.
