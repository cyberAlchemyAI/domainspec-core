# Whole-System Architecture Design — Integration & Promotion Governance

**Status:** draft for team discussion · 2026-06-10 · promotes nothing · L0 stays fixture-only.
**Scope:** the GoldenQuill grant-runtime (Victor) **and** the promotion-governance feature as one system.
**Relation to existing docs:** this consolidates and does not replace — it sits on top of
[ARCHITECTURE.md](ARCHITECTURE.md) (six-view), [runtime-design.md](runtime-design.md),
[seam-map.md](seam-map.md), [layering.md](layering.md), and the feature spec
([../SPEC.md](../SPEC.md), [../domain.md](../domain.md)). Where those are settled, this points to them;
where the design is **open**, Part II proposes a concrete design for the team to decide.

---

# Part I — The system as designed (baseline)

## 1. What the system is, in one paragraph

GoldenQuill writes grants with a six-seat AI council (Victor). Promotion governance is the
**event-sourced spine** bolted onto that council so the system can *learn* from grant outcomes
without ever silently changing shared knowledge. Every council action and every outcome becomes a
typed, source-backed **event** in a replayable journal; the journal projects into a run-graph (DAG),
lifecycle/KPI read-models, and analytics; from those the system derives **proposed** learning
candidates; and **only an operator decision** converts a candidate into approved, scope-bounded
reusable knowledge that future grant work may consume. The whole point is the one-way valve:
observation flows forward freely, but **approval flows only through the human gate.**

## 2. End-to-end spine (the load-bearing flow)

```
 COUNCIL / SOURCES            EVENT AUTHORITY PLANE                         PROMOTION LANE
 ----------------    ------------------------------------------   --------------------------------
 Scout  Scribe       AdapterProducer ──emit──▶ GrantWorkEvent
 Editor Judge                                   + Envelope
 RedTeam Logician                                  │
 Uploader CycleRcpt                                ▼
 Outcome sources ──▶  AcceptGrantWorkEvent  ──▶ Event Journal (replayable, idempotent)
 (portal/agency)        │  validate + idempotency │
                        │  emit receipt           ▼
                        └────────────▶ Projectors ──▶ DAG (GrantRunNode/Edge)
                                            │     └──▶ Lifecycle state + KPI observations
                                            │     └──▶ Analytics facts ▶ ActionKpiAssociation
                                            ▼                                   │
                                   CreatePromotionCandidate ◀────────────────────┘
                                            │  (carries proposed_allowed_uses ONLY)
                                            ▼
                                   OntologyVaultProjection (AUDIT only, mutation_allowed=false)
                                            ▼
                                   ScopeAndPrivacyGate (redaction ⟂ consent-tier)
                                            ▼
                            ╔═══════════════════════════════════╗
                            ║  RecordOwnerDecision (Ed25519)     ║  ◀── the ONLY approval gate
                            ║  sets approved_allowed_uses        ║      (operator)
                            ╚═══════════════════════════════════╝
                                            ▼
                                   ApprovedReusePacket (active)
                                            ▼
                                   HydrateFutureGrantContext ──▶ back into Scout/Scribe/Judge/Logician
```

**Read it as:** nothing downstream of `AcceptGrantWorkEvent` exists until acceptance validates and a
receipt is written (W-I5). Nothing carries *approved* uses until the owner gate. (Spec: SPEC.md:197-201,
SPEC.md:89, domain.md:216.)

## 3. Three planes (separation of authority)

```
  OBSERVABILITY plane          EVENT / GOVERNANCE plane            STORAGE plane
  (never authority)            (the only authority)                (where state lives)
  -------------------          ------------------------            -----------------------------
  Logfire spans                Event journal  (JSONL→SQLite)       per-org sovereign  (Law-3 isolated)
  session_log.jsonl            Projectors + receipts                 orgs/<slug>/vault/… (KFR, Match-DB)
                               OntologyVaultProjection (audit)     shared ontology    (owner-gated)
  CycleReceipt / Reflection      mutation_allowed=false (L0)         pipeline/cards/CIC|CLC/*
  Packet READ spans and                                            governance / audit (append-only)
  EMIT events → they are                                             approved_reuse_packets/<id>.yaml
  adapters, not the journal.
```

Rule: **only the journal is replayable + idempotent + source-backed.** Observability can be lost without
losing truth. (runtime-design §D-B.)

## 4. Component map and build layering

16 components (C1–C16); only **C2, C3, C8** are L0. Full table in [ARCHITECTURE.md](ARCHITECTURE.md)
View 3. Build sequence:

| Layer | Theme | Components | What it proves |
|-------|-------|-----------|----------------|
| **L0** | Event spine + audit projection (fixture-only) | C2, C3, C8, DAG-half of C4 | The contract: events → DAG → audit, deterministically, mutating nothing. |
| **L1** | Live capture + read-models + owner decision | C1, C4–C7, C9, C10, C13 | Real events, KPIs, candidates, and the human approval gate. |
| **L2** | Owner-gated reuse | C11, C12, C14 | Approved packets hydrate future context; per-org auto, shared-card operator-gated. |
| **L2.5** | Improvement loop | C15, C16 | Approved learning is *applied* and *verified* before it changes a live artifact. |

## 5. Authority model (the invariants the whole design rests on)

1. **One-way authority, gated by acceptance.** Adapters emit only; the journal is not approved knowledge; approval exists only on `OwnerDecision`. (A-R1/R2/R6, SPEC.md:197-201.)
2. **Source-or-nothing.** Outcomes need `source_ref`; KPIs need a denominator; everything carries `interpretation_limits`. Fail-closed otherwise.
3. **Approved uses live only on `OwnerDecision`.** Candidates/events/facts carry *proposed* uses at most. (PCS-I1, ODS-I1/2.)
4. **Privacy is gated and scope-bounded.** Org feedback stays org-private until generalized + approved; hydration use ⊆ approved uses, scope ⊆ reuse_scope. (PCS-I3, ARP-I3.)
5. **L0 mutates nothing canonical.** `mutation_allowed=false`; no org-vault/card/dashboard write.

## 6. Settled decisions (do not re-open)

D-A JSONL→SQLite journal · D-B three planes · D-C Victor owns stores / governance owns decision ·
D-D one jointly-owned promotion vocabulary (+ Ed25519 + two-layer privacy) · D-E freeze numpy+scipy
for L0 · D-F improvement applied by-target, both C16-verified. (See [ARCHITECTURE.md](ARCHITECTURE.md)
Decision Log; note D-E is folded into D-D as a sub-decision in runtime-design §6.)

---

# Part II — Open architecture design (what the team must decide)

These are the unresolved areas. Each is framed as **the question → options → a recommended design**.
None is locked; this is the agenda.

## D1. Decision vocabulary + the promotion-authority gate  *(OQ-4 / GAP-PROMO-ENFORCE — P0)*

**Question.** How are operator decisions recorded, and how do we *prove* nothing self-promotes?

**Options.**
- **(A) Three typed surfaces** — `PursuitDecision` (accept/reject/hold), `MatchFitVerdict` (confirmed_fit/rejected/declined_cycle/pending), `OwnerDecision` (approved/rejected/retired/contradicted). Lock `OwnerDecision` as the sole promotion vocabulary.
- **(B) One unified enum** across all three layers, mapping `hold`/`pending` into it.
- **(C) Status quo** — three vocabularies, no lock.

**Recommended: (A).** The three live at different layers and answer different questions; merging loses
`hold`/`pending` (which have no promotion meaning). Design:

```
  PursuitDecision  ──▶ drives ApplicationLifecycle (eligible_match → go_no_go_approved)   [NOT promotion]
  MatchFitVerdict  ──▶ evidence into outcome/lifecycle                                    [NOT promotion]
  (verdict + outcome) ──generate──▶ PromotionCandidate (proposed uses) ──human──▶ OwnerDecision (approved uses)
```

**Enforcement (closes GAP-PROMO-ENFORCE):** make "nothing self-promotes" a *deterministic gate*, not a
convention — `F-PROMOTION-NO-AUTO-APPROVE` (Logician/Cedar, fail-closed) fires if `approved_allowed_uses`
appears on any envelope, event, fact, or candidate; only `RecordOwnerDecision` with a valid operator
Ed25519 signature may set it. This is one schema constraint + one gate + one test fixture — and it is the
single highest-leverage thing to build, because it makes the central claim verifiable.

## D2. The L0→L1 mutation flip  *(GAP-L0L1-FLIP)*

**Question.** L0 is `mutation_allowed=false`. What authorizes the *first real write* to a per-org store?

**Options.**
- **(A) Operator-signed per-org flip** — `mutation_allowed` flips false→true only on an operator Ed25519 deployment sign-off, per-org, reusing the classification-register trust mechanism (publisher-pinned pubkey, byte-for-byte). Shared-card mutation stays separately gated (see D3).
- **(B) Config flag** — a deployment setting flips it.
- **(C) Automatic** — flips after N consecutive green fixture/replay runs.

**Recommended: (A).** It matches the existing white-glove Ed25519 discipline GoldenQuill already uses for
the classification register and router templates, keeps the operator in the loop, and scopes the flip
**per-org** so one client's go-live never touches another's (Law 3). The flip is recorded as an event in
the journal, so it is auditable and replayable. Per-org auto-apply after approval is fine; **shared-card**
writes never flip here.

## D3. Shared-card promotion gate + the "stay general" boundary  *(BLK-D5A-THRESHOLD / OQ-3)*

**Question.** When does cross-org/shared knowledge get promoted, and what keeps a shared card "general"
(D5a: guardposts, never overfit one funder)?

**Options for the boundary.**
- **(A) Structural, no metric** — a shared card may only carry knowledge that is (i) `redaction_status=generalized`, (ii) sourced from ≥K distinct orgs, (iii) observed across ≥2 CICs, and (iv) free of any single-funder specific. Enforced by a Logician predicate. **No optimization target at all.**
- **(B) Bounded metric** — optimize a composite, but cap it.
- **(C) Operator judgment only** — no machine rule.

**Recommended: (A).** D5a is explicit that shared cards are *guardposts, not hill-climbed toward a metric*
— so the boundary should be **structural, not a threshold on a score.** Encode the "no metric hill-climb"
rule as an assertion in `PromotionAuthorityPolicy`, and make K and the cross-CIC requirement the
machine-checkable definition of "general." **The human gate (C12):** shared-card promotion requires
`consent_tier == composable_with_others` **and** generalized redaction **and** an operator card-edit
review signed Ed25519. Never automatic. Per-org promotion (D2) is the auto path; shared is the gated path.

## D4. Improvement verification + the regression definition  *(C15/C16, RK-006)*

**Question.** An approved packet is *applied* (C15) and must be *verified* (C16) before it changes a live
artifact. What counts as "improved" vs "regressed," and on what data?

**Design.**
```
 ApprovedReusePacket ──apply(C15)──▶ candidate refined artifact
                                         │
                                         ▼
        C16: re-run a DIVERSE held-out grant set ──▶ KPI delta vs the optimization chain's expected delta
                                         │
              improved ──▶ promote (per-org auto-apply; shared-card via D3 gate)
              regressed ─▶ reject + residue   (never changes a live artifact unproven)
```

**Open sub-decisions for the team:**
- **Held-out set diversity (RK-006):** require the eval set to span ≥2 CICs and ≥2 CLCs so a refinement can't overfit one funder. *(Recommended as a hard rule.)*
- **"Regressed" definition — options:**
  - **(A)** any primary-KPI delta < 0 → reject.
  - **(B)** delta below a confidence-bounded margin, and no statistically-significant decrease on any guardrail KPI, measured across the diverse set → reject. *(Recommended — stays within L0/L1 descriptive stats, numpy/scipy; no heavy causal stack per D-E.)*
  - **(C)** composite score.
- **Recommended: (B)** with a simple floor: promote only if delta ≥ 0 on the primary KPI **and** no guardrail KPI shows a significant decrease across ≥2 CICs.

## D5. Sequencing — what to build first

```
  1. D1 enforcement gate  ──┐  (proves the central claim; also unblocks L1 candidate shape)
  2. BLK-B001 TEST-SPEC ────┼─▶  L0 build: C2/C3/C8 + projector against T1–T35 fixtures
  3. D2 flip design ────────┘
  4. D3 shared-card gate + D5a assertion   ─▶  L2 design
  5. D4 verification + regression rule      ─▶  L2.5 design
```

The two genuinely hard gates are **human, not technical** — the D1 vocabulary LOCK and the D3 shared-card
review. Everything else is mechanical once those are decided.

---

## Decision log for this session (proposals — not locked)

| Ref | Area | Recommendation | Status |
|-----|------|----------------|--------|
| D1 | Decision vocabulary + enforcement | Three surfaces; `OwnerDecision` sole approver; `F-PROMOTION-NO-AUTO-APPROVE` gate | PROPOSED — operator deciding shape (OQ-4) |
| D2 | L0→L1 flip | Operator-signed per-org Ed25519 flip, journaled | PROPOSED |
| D3 | Shared-card gate + boundary | Structural "general" rule (no metric) + operator Ed25519 card-edit | PROPOSED |
| D4 | Improvement verification | Diverse held-out (≥2 CIC/CLC); reject on neg delta or guardrail significance | PROPOSED |

*Companion: [open-questions-and-blockers.md](../team-review/open-questions-and-blockers.md) (the agenda) ·
[discovery/impl-architecture/](../discovery/impl-architecture/) (how the current architecture was derived).*
