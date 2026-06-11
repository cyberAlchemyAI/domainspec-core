# Promotion-Governance × Victor — Open Questions, Blockers & Gaps

Status: draft · 2026-06-10 · scope: `goldenquill-promotion-governance` feature + `victor/` product docs

Victor (GoldenQuill/Tilth) is the product; promotion-governance is the DomainSpec feature
that governs its learning loop. Both doc sets describe two sides of one surface, so items
below are merged and de-duplicated. IDs reuse the source IDs where they already exist
(OQ-*, B-*, D-*).

## The single load-bearing gap

**The learning loop is designed but not built.** Outcome → Insight → operator-approved
promotion gate → shared-card / per-org update. Today a human edits cards by hand after each
grant. Every victor view (engineer D7 "CRITICAL", discovery §3, system-view, ontology OQ-2)
agrees this gates the value thesis. Promotion-governance agrees: L0 is fixture-only — no
production memory writes, no org-vault mutation, no dashboard. Everything below is what must
be settled before that loop can run with governance.

## Blockers (P0 — block L1 / external surface)

| ID | Issue | Source |
|----|-------|--------|
| OQ-4 | Operator-decision vocabulary split across 3 layers (Scout `ACCEPT/REJECT/HOLD`, Match-DB `confirmed_fit/rejected/declined_cycle/pending`, OwnerDecision `approved/rejected/retired/contradicted`), loosely called "operator action." Must name the layers + LOCK canonical enums before L1 candidate shape. See proposed resolution below. | engineer §2.1; ontology OQ-4; seam-map:153 |

### OQ-4 — proposed resolution (PROPOSED, shape under review 2026-06-10)

Frame: the three vocabularies are **three decision surfaces at three layers**, not one
enum to unify. Collapsing them loses meaning (Scout `HOLD` and Match-DB `pending` have no
`OwnerDecision` equivalent — `OwnerDecision` is near-terminal). Proposed fix: stop calling
all three "operator action," type each surface, and LOCK `OwnerDecision` as the *sole*
promotion vocabulary.

| Layer | Question | Typed name | Canonical enum | Maps into |
|-------|----------|-----------|----------------|-----------|
| Pursuit gate | Chase this discovered opportunity? | `PursuitDecision` (Scout REVIEW) | `accept · reject · hold` | lifecycle `eligible_match → go_no_go_approved`; `hold` stays `eligible_match`. NOT promotion. |
| Fit verdict | Is this (client × funder) a real match? | `MatchFitVerdict` (Match-DB row) | `confirmed_fit · rejected · declined_cycle · pending` | evidence into lifecycle/outcome record. NOT promotion. |
| Promotion gate | Approve this insight for reuse? | `OwnerDecision` | `approved · rejected · retired · contradicted` | sole authority that may set `approved_allowed_uses`. |

LOCK = three assertions (not one enum):
1. `OwnerDecision` is the only promotion vocabulary; nothing upstream may emit into it or
   set `approved_allowed_uses`. (Also closes the promotion-authority enforcement blocker —
   same gate.)
2. Pursuit and fit decisions are typed *non-promotion* on their own layers. The seam-map
   `confirmed_fit→approved` / `declined_cycle→retired` rows are cross-layer category errors
   to be deleted once shape is confirmed.
3. One named cross-layer derivation: a `MatchFitVerdict` + outcome may *generate* a
   `PromotionCandidate` that a human decides via `OwnerDecision`. Generation ≠ approval.

OPEN (why still PROPOSED, not LOCKED): whether to keep three surfaces or force a single
unified enum (operator preference pending).
| B-001 | TEST-SPEC T1–T35 must be confirmed authored/stable before the deterministic validator (SWU-GQDAG-007). All 8 SWUs `not-started`. | WORK-PACK:78–82 |
| D5a / OQ-3 | "Shared cards stay at a general guardpost level, never overfit one funder" is resolved as a verdict, but has **no machine-checkable threshold**, and the "no metric hill-climb" assertion isn't encoded in `PromotionAuthorityPolicy`. | engineer D5a; ontology OQ-3; layering:49 |
| OQ-13 | 16 coined edges + GoldenQuill-local `gq_kind` are honest violations of DomainSpec's "do not invent edges" rule. Amendment discoveries GQ-AMD-001/002 are PROPOSED-UNFILED; no `goldenquill-edge-amendments/discovery.md` exists. Blocks vault promotion. | ontology OQ-13 |
| — | Promotion-authority enforcement: every doc repeats "KPIs/evidence/adapters cannot approve reuse — only OwnerDecision can," but there is **no centralized enforcement spec or test** proving an adapter's `approved_allowed_uses` is rejected. | SPEC:169; domain; operations |

## Open questions (P1 — design decisions not yet made)

### Loop & promotion mechanics
- **L0→L1 mutation flip:** what gate flips per-org `mutation_allowed` false→true? Operator? Config? No criteria. (architecture; runtime-design D-C)
- **OQ-2:** the consent-tier arm is already LIVE while the rest of the loop is dormant — stable v0.1 posture, or does the live gate force the rest to wire sooner?
- **C16 regression definition:** what delta margin counts as "regressed" vs "improved"? In what units? Held-out eval-set diversity unspecified (flagged overfit risk RK-006).
- **Shared-card promotion human gate:** who is "owner" (applicant/operator/funder)? Gate signature (manual form / code-review / Ed25519)? Appeal process? (layering; seam-map)

### Vocabulary & schema
- **`ApprovedReusePacket`** referenced as "new" in seam-map but the domain.md schema exists — reconcile seam-map against domain.md (no longer fully open). (seam-map:85 vs domain.md:218)
- **Allowed-use / `reuse_scope` vocabulary** (`workspace_safe_after_generalization`, `suggest_review_focus`, …) is free-string everywhere; no enum or registry; fixtures reference IDs no registry validates.
- **Event count:** 13 vs 12 domain events unresolved; canonical enumeration missing. (runtime-design residue)
- **OQ-11 / Five-Laws map:** consent-tier gate filed under Law 4 on disk but reasoned as Law 3; no canonical Five-Laws→failure-code map.

### Conflict handling (unspecified in states/operations)
- Concurrent outcomes: `awarded` and `declined` same day, equal source strength — no tiebreaker. (states ALS table)
- `consent_tier` (applicant input) vs `OrgScope` (system derived) — orthogonal, but no precedence rule if they disagree. (seam-map:154)
- Contradiction detection: "application stage ≠ outcome truth" stated as principle, but detection/logging/surfacing unspecified. (discovery:104–112)

## Gaps (designed-not-built / productization debt)
- **D6 — eligibility filter:** `eligibility_filter.py` has zero callers, hardcoded to MycoSymbiotics; profile must move to per-client data before serving any other client.
- **F-CARDS-\* gates** (coupling, cross-org namespace leak, private-data-in-card): registered-dormant, `NotImplementedError`, not imported. (OQ-12)
- **D10 — v0.2 post-award agents** (Data Collector, Report Generator): spec LOCKED but inactive, partial code only.
- **Calibration discipline (D5):** "execution parameters are optimized" is aspirational — no tuning gates, no outcome-vs-parameter feedback.
- **Analytics implementations** not vendored (numpy/scipy frozen but exact methods unlisted); **JSONL→SQLite migration trigger** (>50k events) has no runbook.
- **CIC political-axis mid-migration (OQ-10):** all six signed CIC bodies still carry `funder_political_axis`; Wave-2 re-sign ceremony deferred; PNG cards still display retired capital-logic footer.
- **Missing artifacts:** docs say "carry into `invoke plan` then `task-session`" but no plan/task-session artifacts exist — a design→execution gap.

## Unresolved business tensions (won't block code, block go-to-market)
- **D8/D9 — moat vs sovereignty:** verdict is "no lock-in moat; charge for the *stream* of improvements," but pricing is unresolved and in tension with "nothing held hostage."
- **Grant-count contradiction:** README says "six competitive grants," CLAUDE.md says "three" — reconcile before external use.

## Change log
- 2026-06-10 — initial draft synthesized from promotion-governance spec docs + victor views.
