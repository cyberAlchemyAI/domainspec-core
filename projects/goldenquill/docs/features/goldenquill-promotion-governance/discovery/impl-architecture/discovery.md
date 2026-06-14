---
view: discovery (layperson orientation + the heart)
audience: the team
status: draft — spec-derived 2026-06-10
source: _derivation-substrate.md (read-only derivation from goldenquill-promotion-governance spec)
---

# Discovery — the grant-learning loop, in plain language

> Plain-language orientation for the team. This view owns the story and the heart:
> what the feature IS, why owner-decision is load-bearing, and what is real today.
> The schema, the verdicts, and the stakeholder map live in the three sibling views.

## Cross-reference map

This is one of four "victor discovery pattern" views. Each owns a different altitude. Do not look here for what another view owns:

- **[ontology-view.md](ontology-view.md)** — the formal entities, enums, value objects, and the five state machines. The exact shapes and legal transitions.
- **[engineer-view.md](engineer-view.md)** — the component inventory (C1–C16) and decision-inventory with verdicts (e.g. the learning loop as D7 "designed, not built — CRITICAL").
- **[system-view.md](system-view.md)** — the stakeholder altitude and the cross-reference map between all the moving parts; the same product told as "shape."
- **discovery.md** (this file) — the story, the heart, honest build status, open questions.

---

## 1. What this is — the story

Picture a single grant. The team chases an opportunity, drafts a proposal, submits it, and months later it is awarded or declined. Today that whole experience evaporates: the win or loss is in someone's head, and the next grant starts cold.

This feature is the machine that stops the evaporation. It is **an event-sourced governance spine** (substrate §6): it watches grant work happen, writes down what it saw in a tamper-checked log, and turns that log into a picture of the run plus some numbers — and then, only with a human's say-so, lets a *lesson* from one grant feed into the next.

Follow one observation through the pipeline:

1. **An observation enters.** Something happens in a grant cycle — a portal is hit, a seat runs, an upload finishes, an outcome lands. A bounded *adapter* watches and emits one typed `GrantWorkEvent` wrapped in an envelope (substrate §1, SPEC.md:164–201). The adapter only *reports*. It has no power to decide anything.

2. **It becomes a journaled event.** The envelope is checked and written once into the **typed event journal** — the single replayable, source-backed record (substrate §1, SPEC.md:200). Same event twice? No-op. Same key, different content? Blocked (operations.md §AcceptGrantWorkEvent). Every accepted event gets a receipt.

3. **It projects into the run graph + KPIs.** From the journal, projectors build the **run graph** (`GrantRunNode`/`GrantRunEdge` — what happened, in what order, which gate allowed or blocked the path; SPEC.md:92–162) and the **lifecycle + KPI read-models** (what stage the application is in, and the metric numbers). These are *read-models*: pictures derived from the journal, never the source of truth themselves.

4. **It maybe becomes a learning candidate.** Outcomes, KPIs, feedback, and analytics associations can feed a **candidate builder** that proposes a `PromotionCandidate` — a draft lesson saying "this seemed to work, here is where it might be reusable." Crucially, a candidate carries only **proposed** reuse, never approved (domain.md:196–197).

5. **An owner decides.** A human owner reviews the candidate and records a decision: approved, rejected, retired, or contradicted (SPEC.md:89, domain.md:216). **This is the only step in the entire system where reusable knowledge becomes real.**

6. **Approved learning feeds the next grant.** An approved decision becomes an `ApprovedReusePacket` — a bounded packet of "you may reuse this, for these uses only" (SPEC.md:90). A hydrator then feeds it into the next grant's context — Scout, Scribe, Judge, Logician, the funding goal, memory — but only within the approved uses (operations.md §HydrateFutureGrantContext).

That is the whole feature: **observation → journaled event → run graph + KPIs → maybe a candidate → an owner decides → approved learning feeds the next grant.** Everything else is detail about who is allowed to write each step.

---

## 2. THE HEART — owner decision alone can approve reuse

If the team internalizes one thing, make it this:

**Nothing in this system can promote itself. Only a human owner-decision can convert a lesson into reusable knowledge.**

The system is full of things that *look* authoritative — KPIs, statistical analytics, optimization chains, the candidate builder, the governance audit. None of them can approve reuse. Concretely:

- **Adapters only report.** They cannot set approved uses (substrate §4, A-R6; domain.md:45–46).
- **The journal is not approved knowledge.** It is a faithful record of what happened, nothing more (SPEC.md:200).
- **KPIs and outcomes only describe.** Source-backed, denominator-safe — and zero promotion authority (operations.md §ProjectEventToLifecycleAndKpi).
- **Analytics and optimization chains only package evidence.** They fail closed on bias, bad samples, temporal leakage; they cannot approve reuse and cannot exceed their own method's claim label (analytics-methods.md:19–23; optimization-chains.md:21–25).
- **The candidate builder only proposes.** A `PromotionCandidate` carries `proposed_allowed_uses` and **must not** carry `approved_allowed_uses` (domain.md:196–197; invariant PCS-I1).
- **The governance vault only audits.** In L0 it checks compatibility but mutates nothing (`mutation_allowed=false`; mappings.md:108–124).

There is exactly **one** place in the data model where `approved_allowed_uses` may be set: `RecordOwnerDecision` (SPEC.md:89; domain.md:216; substrate §4). That is the load-bearing idea. The entire architecture is built so that the path from "the data suggests X" to "we will reuse X" *cannot* be walked without a human stepping through that gate.

Why it matters for the team: this is a deliberate design choice, not a missing feature. An automatic learning loop that hill-climbs KPIs would let one good-looking number quietly rewrite shared knowledge for every client — exactly the failure the GoldenQuill sovereignty model refuses. The gate is the product's spine, not its bottleneck. When you build, **the gate stays human.**

The one-way flow, stated once: `adapter_output → accepted_event → projection_receipt → DAG/read-models → proposed candidate → [OWNER DECISION] → approved reuse packet → next grant` (invariant W-I5). Everything left of the bracket is mechanical; the bracket is human; everything right of it is bounded by what the human approved.

---

## 3. Honest build status — designed, not built

Be plain with the team: **none of this runs yet.** Everything above is DESIGNED. All 16 spec files are draft/candidate. The integration design plan literally says `promotion_decision: pending` and "promotes nothing; L0 stays fixture-only and audit-only" (substrate §5). The engineer-view names the learning loop **D7 "designed, not built — CRITICAL"** — see [engineer-view.md](engineer-view.md).

What is actually in scope for the first build (**L0**) is deliberately tiny and proves the *contract* before any real data exists:

**L0 — what the first build proves (fixture-only, audit-only):** envelope fixtures, fake adapters, the acceptance validator, the event→run-graph projector, receipts, the audit-only vault projection, the T1–T35 test fixtures, deterministic tests. Only three components are L0: the event journal + idempotency index (C2), acceptance + receipts (C3), and the audit-only vault projection (C8) (substrate §1, §4).

**L0 — what is explicitly NOT built yet:** no UI or dashboard, no real importer, no production memory writes, no signed-card mutation, no org-vault mutation, **no automatic promotion**, no KPI engine, no candidate builder, **no owner-decision recorder**, no reuse packet, no improvement loop (substrate §4). The hard guarantee for L0 is `L0 → no org_vault_write and no card_write and no dashboard_write` (invariant W-I4).

Said plainly: **L0 proves the plumbing is correct with fake water, before any real water flows.** It demonstrates that an observation can become a journaled event and project into a run graph, with receipts, mutating nothing real. The owner-decision gate, the KPIs, the analytics, the reuse — all designed, all waiting behind L0. A human edits the cards by hand today; the automatic loop is the still-hypothetical value engine.

---

## 4. Open questions for the team

These are the things a teammate should weigh in on. Honest framing — these are open, not settled.

**Q1 — Vocabulary lock (OQ-4): one decision enum or three?** The loop's vocabulary is not locked, and the lock is what unblocks **L1** (not L0) (substrate §5, B-002/OQ-4). There is a PROPOSED resolution under review: instead of one unified decision enum, split into **three decision surfaces** — PursuitDecision, MatchFitVerdict, OwnerDecision (see integration/OPEN-QUESTIONS-LEDGER.md). Does the team accept the three-surface split, or hold out for one enum? This blocks L1; until it lands, L1 cannot start.

**Q2 — Who is "the owner"?** The whole heart rests on "owner decision alone can approve reuse" — but the spec does not pin down *who* the owner is operationally (in the GoldenQuill world, Josh is the sole operator today). For a single-operator deployment this is clear; for the Stage-2+ fleet it is not. Is "owner" always the org operator? Can it ever be delegated? The gate is only as trustworthy as the answer.

**Q3 — When does L0 flip to L1 (the audit→mutation flip)?** L0's vault projection is `mutation_allowed=false` — it audits but never writes (substrate §1). L1 is where it would start mutating real state. What is the gate that flips `mutation_allowed` to true? What has to be proven first? This is the single riskiest transition in the build, and it is currently just a level boundary, not a procedure.

**Q4 — TEST-SPEC stability (B-001).** The T1–T35 test fixtures are referenced load-bearingly but their stability is **unconfirmed**, and this blocks TASK-FIX (substrate §5, §6). The team needs to confirm T1–T35 are stable before the fixture-build task can proceed. Are the 35 tests pinned, or still moving?

**Q5 — CIC×CLC coupling must not sneak back in (OQ-9).** GoldenQuill forbids hardcoding client-type → funder-type couplings. The team must ensure candidate *generalization* does not quietly re-introduce that coupling through the learning loop (substrate §5, OQ-9). Worth an explicit check: can an approved learning ever encode a forbidden CIC×CLC binding?

**Q6 — Two counts, both RESOLVED 2026-06-13.** The spec prose previously said "47 KPIs" in three places; the `GrantKpiKind` enum is authoritative at **44** entries (domain.md:402–449) and the prose is now reconciled to 44. The event-count discrepancy is resolved by naming the two real axes explicitly: **9 ingestion event families** (the `GrantWorkEventKind` enum, domain.md:301–313) and **13 operation-output events** (the 13 events.md domain-event sections — events emitted by operations/projections). The "12" figure was a phantom and is struck. (Counts verified by direct enum count 2026-06-10; the earlier "47"/"49" KPI figures were miscounts.)

---

## Connections

- Sibling views: [ontology-view.md](ontology-view.md), [engineer-view.md](engineer-view.md), [system-view.md](system-view.md).
- Source of truth for every claim above: [_derivation-substrate.md](_derivation-substrate.md) (read-only spec derivation).
- Existing victor orientation pattern: [victor/discovery.md](../../../../../victor/discovery.md).
