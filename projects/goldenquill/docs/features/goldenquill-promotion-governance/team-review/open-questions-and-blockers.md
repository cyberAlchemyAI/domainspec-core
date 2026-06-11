# GoldenQuill Promotion-Governance — Open Questions & Blockers

**For team discussion.** Compiled from the Craft ledger (`projects/goldenquill/.craft/ledger.yml`) on 2026-06-10. Source of truth is the ledger; this is a shareable view.

## TL;DR

The promotion-governance feature is the **L0 build-out spec for GoldenQuill's learning loop** — the loop that turns grant outcomes into reusable, owner-approved knowledge. The architecture is sound and the core idea is settled (*owner decision alone can approve reuse*). But the loop is **designed, not built**, and five decisions need the team before L1 can start. One of them — the promotion vocabulary LOCK (OQ-4) — gates everything downstream.

**The single most important thing to agree on first:** how operators record decisions (OQ-4), because it is also the gate that proves nothing can self-promote.

---

## Blockers (must clear before L1)

> Convention: these are *raw* blockers — they are not "resolved" by discussion alone; each needs its closure condition met.

| ID | Area | Owner | Closure condition |
|----|------|-------|-------------------|
| **BLK-OQ4-VOCAB** | Governance vocabulary | Joint (grant-runtime + governance) | Operator confirms **three decision surfaces** (PursuitDecision / MatchFitVerdict / OwnerDecision) **vs one unified enum**; the canonical promotion vocabulary is LOCKED before any L1 candidate shape. |
| **BLK-B001-TESTSPEC** | Test fixtures | grant-runtime | TEST-SPEC T1–T35 confirmed authored and stable; reconcile drift before the validator task (TASK-FIX). |
| **BLK-D5A-THRESHOLD** | Shared-card safety | governance | A machine-checkable "general guardpost" threshold + a "no metric hill-climb" assertion encoded in `PromotionAuthorityPolicy`. Today "shared cards stay general, never overfit one funder" is a verdict with no enforceable boundary. |
| **BLK-OQ13-EDGES** | Ontology promotion | governance | File GQ-AMD-001/002 and author `goldenquill-edge-amendments/discovery.md` so the 16 coined edges + `gq_kind` can graduate to the vault. |

---

## Open decision (blocking)

### DEC-OQ4 — How do operators record decisions?  *(operator: "let me think")*

There are **three different operator-decision vocabularies** in the system today, loosely all called "operator action":

| Layer | Question it answers | Vocabulary today |
|-------|---------------------|------------------|
| Pursuit gate (Scout) | Chase this discovered opportunity? | `accept / reject / hold` |
| Fit verdict (Match-DB) | Is this (client × funder) a real match? | `confirmed_fit / rejected / declined_cycle / pending` |
| Promotion gate (OwnerDecision) | Approve this insight for reuse? | `approved / rejected / retired / contradicted` |

**Proposed (under review):** keep them as **three typed surfaces**, not one merged enum — collapsing loses meaning (`hold` and `pending` have no promotion equivalent). Lock `OwnerDecision` as the *sole* promotion vocabulary; nothing upstream may set approved uses. This also doubles as the enforcement point for "nothing self-promotes."

**Decision needed:** three surfaces (recommended) vs one unified enum. This blocks the L1 candidate shape.

---

## Gaps (designed-not-built / unresolved)

| ID | Severity | Owner | Summary |
|----|----------|-------|---------|
| **GAP-DESIGNED-NOT-BUILT** | block | grant-runtime | The learning loop (outcome → insight → owner-approved → card update) is designed but not built; a human edits cards by hand today. This is the load-bearing gap. |
| **GAP-PROMO-ENFORCE** | block | grant-runtime | No centralized enforcement spec/test proving an adapter's `approved_allowed_uses` is rejected. The "nothing self-promotes" rule is stated everywhere but unproven in code. (Closes together with OQ-4.) |
| **GAP-L0L1-FLIP** | flag | governance | No gate spec for flipping per-org `mutation_allowed` from false→true at the L0→L1 transition. Who/what authorizes the first real write? |
| **GAP-REDACTION-TABLES** | flag | governance | Per-CIC redaction/generalization rule tables (C14) are unauthored; blocks workspace reuse at L2. |
| **GAP-KPI-COUNT** | flag | grant-runtime | Spec prose says "47 KPIs" but the enum has **44** (verified) — a 3-entry gap to reconcile. |
| **GAP-EVENT-COUNT** | flag | grant-runtime | Event count "13 vs 12" unresolved; the canonical event enumeration is undefined. |

---

## What's already settled (so we don't re-litigate)

- **Owner decision is the sole approver of reuse** — adapters, the event journal, KPIs, analytics, candidates, and the vault projection provably cannot self-promote. *(Spec-backed: SPEC.md:89, domain.md:216.)*
- **L0 is fixture-only and audit-only** (`mutation_allowed=false`) — proves the contract before any real data, dashboard, or memory write.
- **Substrate is LOCKED** (Pydantic AI, Logfire, Cedar, Ollama/vLLM, DSPy+GEPA); the only open vendoring is the event-journal store (JSONL→SQLite) + numpy/scipy.
- **Runtime topology** (three planes) and the integration decisions D-A…D-F are resolved — see the companion architecture design.

---

## Suggested discussion order

1. **DEC-OQ4** — lock the decision vocabulary (unblocks L1 + the enforcement gate).
2. **BLK-B001** — confirm TEST-SPEC T1–T35 stability (unblocks the L0 validator build).
3. **BLK-D5A-THRESHOLD** + **GAP-L0L1-FLIP** — the two human-gate designs (when does shared knowledge get promoted, and who flips the first real write).
4. **BLK-OQ13** — file the edge amendments (unblocks vault graduation).
5. Housekeeping: reconcile the KPI (47→44) and event (13 vs 12) counts.

*Companion document: the whole-system integration & promotion-governance architecture design.*
