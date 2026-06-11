---
view: system (shape, altitude, runtime planes, cross-reference map — owns anti-drift)
audience: the team
status: draft — spec-derived 2026-06-10
source: _derivation-substrate.md (read-only derivation from goldenquill-promotion-governance spec)
---

# System-view — goldenquill-promotion-governance (the shape, the planes, the map)

> This is the **system-view** of a four-view pack on the *current implementation architecture* of
> the promotion-governance feature — the L0 buildout spec for GoldenQuill's learning loop (the runtime
> "Victor"). It carries the **shape** (the load-bearing model + the invariants everything recomposes
> from), the **runtime-plane topology**, the **authority boundaries** at system altitude, the
> **stakeholder map**, and — first-class — the **cross-reference map** that says which view owns each
> claim. It is the **shortest** of the four on purpose: it is the map, not the territory.
>
> It does **not** tell the plain-language story or name "the heart" (that is [discovery.md](discovery.md)),
> does **not** state decision/component verdicts or build status (that is [engineer-view.md](engineer-view.md)),
> and does **not** carry the formal entity/enum/state-machine schema (that is [ontology-view.md](ontology-view.md)).
> Where those views own a verdict, this view **names the area and points across** — nothing is decided twice.

---

## The shape at a glance — the spine everything recomposes from

**One load-bearing sentence** (substrate §6): the feature is *an event-sourced governance spine
that turns bounded-adapter observations into a replayable journal, projects that journal into a
grant-run DAG plus lifecycle / KPI / analytics read models, derives only **proposed** learning
candidates, and lets **owner decision alone** convert a candidate into approved, scope-bounded
reusable knowledge that future grant work may consume.*

The whole architecture is **one entity sequence** — `GrantWorkEvent → EventProjectionReceipt →
{GrantRunNode/Edge, GrantOutcomeEvent→ApplicationLifecycleState, GrantKpiObservation} → analytics
facts/windows/associations/chains → PromotionCandidate → OntologyVaultProjection →
RedactionGeneralizationGate → OwnerDecision → ApprovedReusePacket → HydrateFutureGrantContext* —
plus the rule for *who may write each step*. Everything below is that sequence viewed from a
different altitude. (Recomposition argument: substrate §6 "Recomposition".)

**The five invariants** — the system's spine. Each one recomposes a whole region of the design, so
if you hold these five you can regenerate the rest (substrate §6):

| # | Invariant | Selectors | What it recomposes |
|---|---|---|---|
| **1** | **Authority flows one way, gated by acceptance** — `adapter_output → accepted_event → projection_receipt → DAG/read-models`. | W-I5; A-R7 | The entire ingress half: adapters, journal, acceptance, projectors, receipts. |
| **2** | **Source-or-nothing** — outcomes need `source_ref`, KPIs need a safe denominator, everything carries `interpretation_limits`; fail-closed otherwise. | ALS-I2, A-R1/R2 | Outcome / lifecycle / KPI / analytics, and all fail-closed behavior. |
| **3** | **Approved uses live only on OwnerDecision; candidates carry only *proposed* uses.** | PCS-I1, ODS-I1/I2, A-R3, A-R6; SPEC.md:89; domain.md:216 | The whole promotion lane and *why nothing self-promotes*. |
| **4** | **Privacy is gated and scope-bounded** — org feedback stays org-private until generalized + owner-approved; hydration use ⊆ approved uses, scope ⊆ reuse_scope. | PCS-I3, A-R5, ARP-I3 | Redaction / scope gates, Law-3 isolation, reuse packet, hydrator. |
| **5** | **L0 is fixture-only and audit-only — projection mutates nothing canonical** (`mutation_allowed=false`). | W-I4 | Build posture: what L0 is vs L1 / L2 / L2.5. |

The five state machines (ontology-view owns the schema) are exactly the *legal transitions* of the
sequence above; the three runtime planes (below) are the *same sequence projected onto where state
lives*. Same spine, three altitudes.

---

## The three runtime planes — the system-altitude topology

The system separates into three planes that **must not be confused** (substrate §1 "Runtime topology";
runtime-design §1, §3; ARCHITECTURE Views 2–3; D-B). The separation is the load-bearing structural
choice: it is what lets the journal be the *only* source of governance authority while observability
stays cheap and storage stays sovereign.

**Plane A — Observability (`⟂` authority).** Logfire spans (LOCKED substrate) + `pipeline/metrics/session_log.jsonl`.
This plane is **never authority**: it is not replayable, has no idempotency, and grants no promotion
power. CycleReceipt and Reflection Packet *read* Logfire and *emit* events — they are **adapters into
plane B, not the journal itself** (runtime-design §2.4 lines 99–104; seam-map Seam 1). The discipline
that observability is never authority is why "Logfire-as-journal" is a rejected store option (D-A).

**Plane B — Event / governance authority.** The typed event journal — the *only* replayable,
idempotent, source-backed store — plus the projectors, the **audit-only** `OntologyVaultProjection`
(`mutation_allowed=false` at L0), and `approved_reuse_packets/`. This is the plane that holds the
spine: acceptance gates ingress, receipts witness every projection, and `approved_allowed_uses` can
only ever appear at the OwnerDecision step inside it.

**Plane C — Storage (three sovereign zones, mutually `⟂`).**
- **Per-org sovereign** — `orgs/<slug>/vault/…`, Law-3 isolated (`F-MATCH-DB-CROSS-ORG`), append-only;
  hydration auto-applies *only after approval*.
- **Shared ontology** — `pipeline/cards/CIC|CLC/*`, owner-gated, guardpost-level only (D5a), **never auto-promotes**.
- **Governance / audit** — the journal + audit projection + `vault_shared/promotion_governance/approved_reuse_packets/<id>.yaml`, append-only.

**Why the separation matters (system altitude):** authority lives in **exactly one** plane (B). Plane A
is disposable telemetry; plane C is where state rests but never where promotion is *decided*. Collapsing
A into B (journal-as-Logfire) or letting C mutate without a B-plane receipt would break invariants 1
and 5 simultaneously. Store technology for plane B is an engineer-view concern (D-A: JSONL + in-memory
idempotency index → SQLite `INSERT OR IGNORE` at ~50k events/cycle → DuckDB only at L2+); named here for
topology, **verdict owned by [engineer-view.md](engineer-view.md)**.

---

## Authority boundaries at system altitude — what the system guarantees structurally

The promotion-governance feature is, at its core, a set of **structural guarantees about who may write
what**. These are "given" — true by construction, not by optimization or good behavior.

**The one-way authority flow (given).** `adapter_output → accepted_event → projection_receipt → DAG`
(W-I5, invariant 1). Adapters *observe and emit only*; they cannot reach the DAG except through an
accepted event, and acceptance refuses any envelope missing producer / source / idempotency /
interpretation_limits — or one that tries to set approved uses (operations.md §AcceptGrantWorkEvent
R1–R7; A-R6). The journal is **not** approved knowledge (SPEC.md:200): being in the journal grants
nothing.

**Who may write what (given).**
- **Adapters** → typed events only; never DAG, never promotion, never `approved_allowed_uses` (A-R6).
- **Projectors** → read models (DAG / lifecycle / KPI) *and a receipt for every projection* (A-R7);
  they cannot bypass a blocked DAG traversal (GRT-I1).
- **Analytics / optimization / candidate builder** → may *create* `PromotionCandidate`s carrying
  `proposed_allowed_uses` (W-I2, PCS-I1) — and **cannot promote** (analytics-methods, OCR-005/007).
- **OwnerDecision** → the **sole** setter of `approved_allowed_uses` (invariant 3; SPEC.md:89;
  domain.md:216). This is the *first and only* point in the entire system where approved reuse exists.

**The L0 fixture-only / audit-only boundary (given).** At L0, `mutation_allowed=false` (W-I4): the audit
`OntologyVaultProjection` *checks* governance compatibility but **mutates nothing canonical** — no
org-vault write, no card write, no dashboard write (invariant 5; mappings.md:108–124;
operations.md §ValidatePromotionGovernance R4; architecture.md A-R4). L0's in-scope surface is exactly
envelope fixtures + fake adapters + acceptance validator + event→DAG projector + receipts + audit-only
vault projection + the T1–T35 fixtures (substrate §4).

**What is structurally *optimized* vs *given*.** The *given* layer is everything above — the authority
flow, the source-or-nothing gates, the privacy isolation, the L0 mutation ban — guaranteed by construction.
The *optimized* layer (which seat posture, which analytics method, which KPI window) rides *inside* these
guarantees and never relaxes them; its calibration verdicts are not this view's to state.

**Privacy as a structural boundary (given).** Law 3 — org-scoped feedback is org-private until
generalized **and** approved (RedactionGeneralizationGate R1–R3; W-I3; A-R5) — is enforced *structurally*
by per-org store isolation plus a cross-org KPI-window block (operations.md §BuildKpiResponseWindow R4),
not by policy alone. The integration design adds a two-layer privacy split (Classification Register for
routing `⟂` RedactionStatus for reuse, joined by ScopeAndPrivacyGate; seam-map Seam 4, D-D) — named here,
mechanics owned by [engineer-view.md](engineer-view.md).

---

## Stakeholder altitude map — who cares about what

Each stakeholder reads the system at a different altitude. This map names the *stance* each one takes;
it does **not** decide verdicts that belong to other views.

| Stakeholder | Altitude they read at | What they care about (stance) | Where their verdict lives |
|---|---|---|---|
| **Operator / owner** (Josh) | The promotion gate | "Does nothing reach a shared card or a future cycle without my decision?" — invariant 3 is *their* guarantee. They are the **sole setter** of approved uses. | Authority boundary above (given); criticality of the gap → [engineer-view.md](engineer-view.md). |
| **Engineer** | Component / contract | "Which of C1–C16 are actually L0, what's the build status, what's the store tech?" Cares whether the spine is *built*, not just designed. | **[engineer-view.md](engineer-view.md)** — owns all decision + component + build-status verdicts. |
| **Grant runtime "Victor"** | The consuming surface | "What approved learning may I hydrate into Scout / Scribe / Judge / Logician / Funding-Goal / memory?" Constrained by invariant 4: requested use ⊆ approved uses, scope must fit, retired/contradicted cannot hydrate. | Boundary given here; the loop is **designed-not-built** — verdict + criticality → [engineer-view.md](engineer-view.md). |
| **Future-context consumer** | The hydrator output | "Is what I'm about to read source-backed, scope-bounded, and non-leaking?" — invariants 2 + 4. | Hydration rules given here; schema → [ontology-view.md](ontology-view.md). |
| **Auditor / governance reader** | The journal + audit projection | "Can I replay every projection and see which gate allowed/blocked, with a receipt each time?" — invariants 1 + 5. | Plane B topology given here; state-machine schema → [ontology-view.md](ontology-view.md). |

The biggest cross-stakeholder fact — that the whole learning loop is **designed, not built** — is a
*build-status verdict*; it is named across the pack but **owned by [engineer-view.md](engineer-view.md)**
(it calls the loop D7 "designed, not built — CRITICAL"). This view only records that L0 is the buildout
spec for that unbuilt loop (invariant 5).

---

## Cross-reference map — the nothing-decided-twice ledger

**This is the anti-drift spine for the whole pack.** For each load-bearing area, exactly one view is the
**authoring owner** of the verdict; the other three may *reference* it but must not restate or re-decide
it. If two views disagree, the owning view wins. (This view owns this table.)

| Load-bearing area | Authoring owner | The other views may… |
|---|---|---|
| The plain-language story / "the heart" of the loop | **discovery** ([discovery.md](discovery.md)) | reference the orientation; not re-narrate |
| Why grant learning needs a governed loop (business motivation) | **discovery** | point to it |
| The one-sentence load-bearing model | **system** (this view, §"shape at a glance") | quote it verbatim |
| The 5 recomposition invariants | **system** (this view) | cite by number (W-I5 / source-or-nothing / approved-uses / privacy-scope / L0-audit) |
| The three runtime planes + why separation matters | **system** (this view) | reference plane names |
| System-altitude authority boundaries (given vs optimized, W-I5 flow, L0 mutation ban) | **system** (this view) | cite the flow; not redefine the boundary |
| Stakeholder altitude map | **system** (this view) | reference stances |
| **This cross-reference map** | **system** (this view) | treat as the drift ledger |
| Decision inventory (D-A…D-F, D-001…D-007) + verdicts | **engineer** ([engineer-view.md](engineer-view.md)) | name a decision, point across for the verdict |
| Component inventory C1–C16 + which are L0 + build status | **engineer** | reference C-numbers; not assign verdicts |
| "Designed, not built" / D7 criticality of the learning loop | **engineer** | acknowledge the gap; not state its verdict |
| Store-tech choice (JSONL → SQLite → DuckDB) | **engineer** | name it for topology only |
| Blockers (B-001, B-002/OQ-4, OQ-9) + open-question resolutions | **engineer** | reference; not resolve |
| Integration two-layer privacy *mechanics* (Classification Register ⟂ RedactionStatus join) | **engineer** | name the seam; mechanics live there |
| Formal entity definitions (GrantWorkEvent, …, ApprovedReusePacket) | **ontology** ([ontology-view.md](ontology-view.md)) | reference entity names |
| Enum rosters + counts (GrantKpiKind, AllowedUse, ValidationState, …) | **ontology** | cite an enum; not enumerate it |
| The five state machines + their invariants (GRT/ALS/PCS/ODS/ARP) | **ontology** | reference a transition; not restate the machine |
| VO definitions (envelope, SourceRef, MemoryEvidencePacketRef, StageProfile) | **ontology** | reference by name |

**Drift rule:** if you find yourself about to *state* (not reference) anything in a row you don't own,
stop and link to the owning view instead.

---

## Honest gaps (system altitude)

- **Whole feature is designed, not built.** Every spec file is draft/candidate; all tasks are not-started.
  This view describes the *intended* shape; build-status verdict is [engineer-view.md](engineer-view.md)'s.
- **Out-of-derivation-set sources.** TEST-SPEC.md (T1–T35), glossary.md, and OPEN-QUESTIONS-LEDGER.md are
  cited load-bearingly but were outside the read set; **B-001** flags T1–T35 stability as *unconfirmed*.
- **Open counting residue.** "47 vs 44" KPIs (spec prose vs enum, verified 2026-06-10) and "13 vs 12" event kinds are unreconciled; resolution is engineer/ontology territory, not settled here. (GrantRunNodeKind, once flagged 15-vs-~14, resolved to 16.)
- **Integration C-numbers + D-A…D-F are proposed-resolved-but-unbuilt** — topology named, verdicts deferred to [engineer-view.md](engineer-view.md).
