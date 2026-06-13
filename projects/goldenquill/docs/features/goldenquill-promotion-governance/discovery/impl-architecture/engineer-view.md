---
view: engineer (decisions, components, build status — owns the verdicts)
audience: the team
status: draft — spec-derived 2026-06-10
source: _derivation-substrate.md (read-only derivation from goldenquill-promotion-governance spec)
---

# Engineer-view — promotion-governance implementation architecture

> This is the **verdict** view of a victor-pattern quad. It owns three things and
> nothing else: the **component inventory + build status**, the **decision
> inventory** (every implementation decision, resolved once, here), and the
> **blockers + residue ledger**. Nothing is decided twice.
>
> The one fact that frames everything below: **the whole feature is designed, not
> built.** Sixteen spec files are draft/candidate; `integration/ARCHITECTURE.md`
> reads `promotion_decision: pending`, "promotes nothing; L0 stays fixture-only
> and audit-only." This doc is the L0 buildout spec for victor's D7 learning loop —
> the loop victor's own engineer-view names **"designed, not built — CRITICAL."**

## Cross-reference map

- **Plain-language story / "the heart" narrative + open business questions** →
  [discovery.md](discovery.md). Do not look here for the why-it-matters telling.
- **Formal entity / enum / state-machine schema** → [ontology-view.md](ontology-view.md).
  The 13 entities, the enum cardinalities (the 47-vs-44 KPI residue is RESOLVED — prose corrected to 44), the five
  state machines live there.
- **Stakeholder-altitude shape + cross-reference map of the whole feature** →
  [system-view.md](system-view.md). It names the load-bearing stances; the
  **verdict** for each lives here.
- **Spine wiring + the four integration decisions** → `../../integration/runtime-design.md`.
- **Merged open-questions / proposed OQ-4 resolution** → `../../integration/OPEN-QUESTIONS-LEDGER.md`.
- **L0 executable plan** → `../../integration/WORK-PACK.md`.

This view points *down* into those for shape and story; they point *here* for the verdict.

---

## 1. Component inventory C1–C16 — and what is actually built

**Verdict up front: nothing is built. Only C2, C3, C8 are L0 (the fixture-only
slice in flight). Every other component is L1/L2/L2.5 design.** "Built status" is
honest: today the entire column is *designed* or *fixture-only* — there is no
production code behind any row. The L0 column means "in the current
[WORK-PACK.md](../../integration/WORK-PACK.md)," not "shipped."

| # | Component | Layer | Substrate | Build status |
|---|---|---|---|---|
| C1 | AdapterProducer wrappers (one per seat + outcome sources) | L1 | Pydantic | designed |
| **C2** | **Event journal store + idempotency index** | **L0** | **JSONL (→SQLite) (D-A)** | **fixture-only (TASK-EVT / SWU-002)** |
| **C3** | **`AcceptGrantWorkEvent` + projection receipts** | **L0** | **Pydantic + Logician** | **fixture-only (TASK-EVT / SWU-001..003)** |
| C4 | DAG + lifecycle/KPI projectors | L0/L1 | Pydantic | DAG half fixture-only (TASK-DAG / SWU-004,005); lifecycle/KPI half L1 designed |
| C5 | KPI engine (44 KPIs — enum is authoritative; prose reconciled, residue §1 RESOLVED) | L1 | numpy/scipy | designed |
| C6 | Analytics method registry (L0-descriptive only) | L1 | numpy/scipy | designed |
| C7 | Promotion candidate builder | L1 | Pydantic | designed |
| **C8** | **`OntologyVaultProjection` (audit-only)** | **L0** | **Pydantic + Cedar** | **fixture-only (TASK-VAULT / SWU-006); `mutation_allowed=false`** |
| C9 | `ScopeAndPrivacyGate` (consent-tier ∧ redaction) | L1 | Cedar + Python | designed |
| C10 | `RecordOwnerDecision` + Ed25519 validation | L1 | Python + Ed25519 | designed |
| C11 | ApprovedReusePacket store + future-context hydrator | L2 | Pydantic/YAML | designed |
| C12 | Victor operator card-edit gate (shared-card apply) | L2 | Python + operator UX | designed |
| C13 | `F-PROMOTION-*` failure-code family | L1 | Logician | designed (no centralized enforcement spec/test yet — see B-enf) |
| C14 | Per-CIC redaction/generalization rule tables | L2 | YAML (signed) | designed; rules unauthored (residue §3) |
| C15 | Improvement engine (per-org auto-refine; shared-card operator edit) | L2.5 | DSPy+GEPA / operator UX | designed (D-F) |
| C16 | Improvement verification (held-out eval, KPI-delta gate) | L2.5 | experiment-harness + numpy/scipy | designed; eval-set composition + passing-delta undefined (residue §5) |

Source: [runtime-design.md](../../integration/runtime-design.md) §5; ARCHITECTURE View 3.

**The L0 cut (what fixture-only buys):** envelope fixtures, fake adapters, the
acceptance + idempotency validator, the event→DAG projector, receipts, and the
audit-only vault projection — proven deterministically over T1–T35 in pytest.
**Deferred out of L0** (W-I4 `L0 → no org_vault_write ∧ no card_write ∧ no
dashboard_write`): UI/dashboard, real importer, production memory writes,
signed-card mutation, org-vault mutation, automatic promotion, the KPI engine, the
candidate builder, owner decision, reuse packet, and the improvement loop. So the
L0 proof is the *seam shape* — not the loop.

> [RESOLVED 2026-06-13] C5/C6 prose previously said "47 KPIs"; the `GrantKpiKind` enum
> in domain.md is authoritative at **44** entries (verified by direct count 2026-06-10).
> Prose reconciled to 44 — see [ontology-view.md](ontology-view.md) and residue §1.

---

## 2. Decision inventory — verdict-first

Status legend: **RESOLVED** (decided, recorded) · **PROPOSED** (resolution
drafted, under review) · **OPEN** (named, not decided). This is the
"nothing-decided-twice" home for *implementation* decisions; [system-view.md](system-view.md)
names the stances and defers the verdict here.

### 2.1 Integration decisions D-A…D-F (runtime-design §6)

> Note: the two integration docs letter this differently. [runtime-design.md](../../integration/runtime-design.md)
> §6 enumerates **five** decisions (D-A/B/C/D/F) and folds the numpy+scipy freeze into
> D-D as a sub-decision — so its lettering jumps A→B→C→D→F. [ARCHITECTURE.md](../../integration/ARCHITECTURE.md)
> Decision Log surfaces that same freeze as a sixth row, **D-E** ("freeze numpy+scipy for
> L0; defer heavy causal stack"). So D-E is not missing — it is the analytics-library
> freeze, recorded as D-D's sub-decision in runtime-design and as D-E in ARCHITECTURE. Both
> are right; the lettering gap is a doc-sync residue.

| # | Decision | Verdict + why | Status |
|---|---|---|---|
| D-A | Event-journal vendor | **JSONL for v0.1** — append-only `orgs/<slug>/vault/event_journal/<cycle_id>.jsonl` + in-memory idempotency index. Zero new deps, transparent replay, fixture-testable. Migrate to **SQLite** (`INSERT OR IGNORE` = native idempotency) at ~50k events/cycle; **DuckDB** only if analytics reach L2+. Rejected: Logfire-as-journal (no replay/idempotency), `session_log` extension (wrong schema), embedded store (violates no-marketplace). | RESOLVED |
| D-B | Journal vs Logfire boundary | **Three distinct planes.** Logfire = observability (never authority); `session_log.jsonl` = agent-CI metrics (unrelated); event journal = the sole replayable authority store. `CycleReceipt` / `Reflection Packet` *read* Logfire and *emit* events — they are adapters, not the journal. | RESOLVED |
| D-C | Ontology storage location | **Victor owns the stores; governance owns the decision (hybrid apply).** Production knowledge stays in victor's files; `ApprovedReusePacket` lands in `vault_shared/promotion_governance/approved_reuse_packets/`. Per-org targets auto-apply (append-only); shared-card targets pass a Victor operator card-edit gate. `mutation_allowed=false` in L0; flips true **per-org only** in L1. | RESOLVED |
| D-D | Vocabulary owner | **One jointly-owned PromotionGovernance vocabulary.** Adopt the 4-value `OwnerDecision` enum; separate `consent_tier` (applicant input, 3) from `OrgScope` (system-derived, 4) with an explicit map; upgrade `decision_source: SourceRef` to accept Ed25519; two-layer privacy (Classification Register ⟂ RedactionStatus, joined by `ScopeAndPrivacyGate`); add `F-PROMOTION-*` codes. Sub-decision: freeze numpy+scipy for L0, defer the heavy causal stack to v0.2. | RESOLVED (but see B-002/OQ-4 — the LOCK is what blocks L1) |
| D-F | Improvement application | **Both, by target** (closes D5/D7). Per-org context auto-refines via DSPy+GEPA (cheap, low blast radius); shared CIC/CLC cards refine by **operator edit** (one card touches every same-CIC org). **Both** must pass C16 held-out verification (KPI delta vs the optimization chain's expected delta) before going live; a regression is rejected + logged. Rejected: auto-refine shared cards (overfit/cross-org risk, violates D5a); manual-only per-org (wastes the locked engine). | RESOLVED |

### 2.2 Architecture Decision Log D-001…D-007 (architecture.md:337–345)

| # | Decision | Verdict (one line) | Status |
|---|---|---|---|
| D-001 | Companion-schema topology | GoldenQuill local model + **Ontology Vault governance layer** via a bridge artifact — local grant semantics, Vault owns promotion safety. | RESOLVED |
| D-002 | First executable slice | Lives in GoldenQuill **`grant_dag`** — lifecycle/KPI semantics need local test pressure first. | RESOLVED |
| D-003 | Allowed-use split | **Split proposed vs approved** allowed uses — candidate intent and authorized reuse stay separate (the load-bearing PCS-I1 / A-R3 invariant). | RESOLVED |
| D-004 | KPI authority | **Selected KPIs may create candidates only**, never promote — learning without false authority; owner approval always required. | RESOLVED |
| D-005 | Feedback privacy | **Redaction/generalization gate** — feedback stays org-scoped until the gate *and* owner approval pass. | RESOLVED |
| D-006 | Stage baseline | **Global stage baseline with optional funder-family override** — comparison now, accuracy later (ALS-I3). | RESOLVED |
| D-007 | Ingress shape | **Event-first via bounded adapters** — preserves replay, idempotency, source truth, adapter isolation, promotion-governance boundaries. Rejected: direct DAG writers, command/API-only, batch import, memory-first. | RESOLVED |

All thirteen implementation decisions are resolved-on-paper. **Resolved ≠ built** —
see §1.

---

## 3. Blockers & residue

### 3.1 Blockers

| ID | Blocks | Status / verdict |
|---|---|---|
| **B-001** | TASK-FIX (the deterministic validator, SWU-GQDAG-007) | **OPEN.** TEST-SPEC T1–T35 stability is *unconfirmed* — must be read and any drift reconciled before W2. All 8 SWUs are `not-started`. Owner: grant-runtime. (WORK-PACK:78–82) |
| **B-002 / OQ-4** | **L1** candidate shape — **not L0** | **PROPOSED resolution, under review.** The operator-decision vocabulary is split across three layers (Scout `ACCEPT/REJECT/HOLD`, Match-DB `confirmed_fit/rejected/declined_cycle/pending`, OwnerDecision `approved/rejected/retired/contradicted`). A three-surface resolution is drafted in [OPEN-QUESTIONS-LEDGER.md](../../integration/OPEN-QUESTIONS-LEDGER.md): type each as **`PursuitDecision` / `MatchFitVerdict` / `OwnerDecision`** (not one unified enum) and LOCK `OwnerDecision` as the *sole* promotion vocabulary. Still PROPOSED because the keep-three-vs-force-one choice is operator-pending. **Does not block L0.** |
| **OQ-9** | vault promotion (residue §4) | **OPEN constraint.** The CIC×CLC matrix coupling (a resolved category error, `F-CIC-CLC-COUPLING-VIOLATION`) must not re-enter through candidate *generalization*. No machine check exists yet. |
| B-enf | external surface / L1 | **OPEN.** Promotion-authority enforcement is asserted everywhere ("only OwnerDecision sets `approved_allowed_uses`") but there is **no centralized enforcement spec or test** proving an adapter's `approved_allowed_uses` is rejected. C13 covers this when built. |

### 3.2 Residue ledger (runtime-design §7 — carried to plan, none may promote until resolved)

1. **Event-count canonicalization** — 13 vs "12"; does a Logician blocked-gate emit `GrantWorkEventRejected`?; `CycleReceipt` `trace_id` existence check. *(owner: grant-runtime)*
2. **Card-edit versioning/rollback** — mutation ordering when two packets touch one card field; new-Insight consent-tier default. *(grant-runtime)*
3. **JSONL replay at scale** — per-CIC redaction rules unauthored (C14); analytics-method implementations not vendored. *(grant-runtime)*
4. **OQ-4 enum unification** (see B-002); **D5a "no metric hill-climb"** assertion not encoded in `PromotionAuthorityPolicy`; **OQ-9** matrix coupling. *(joint vocabulary owner)*
5. **C16 held-out eval-set composition** (diverse enough to lift a guardpost, not one funder); calibration-param search space (D5); what counts as a passing KPI delta per optimization chain. *(grant-runtime + experiment-harness)*

---

## 4. Work-pack reality

Source: [WORK-PACK.md](../../integration/WORK-PACK.md) (`gq-victor-promotion-integration-L0`).

**Verdict: the L0 plan is gate-passed and ready, and not one line is written.**

- **Gate status:** `pass` — all 8 SWUs carry dependencies, source anchors, write
  scope, done criteria, acceptance evidence, validation surface, execution owner.
- **Complexity:** `low` (fixture-only, deterministic, single write-scope tree) →
  `executionPackRef = n/a` is permitted; L1+ will need a split + execution-pack.
- **Readiness profile:** `pilot` — fixture proof, **not production**.
- **Status:** **every task and SWU is `not-started`.** TASK-EVT / TASK-DAG /
  TASK-VAULT / TASK-FIX / TASK-VERIFY all `ready`; SWU-GQDAG-001…008 all `ready`.
- **Write scopes are disjoint** — all target `pipeline/grant_dag/`, partitioned
  `event_spine/` ⟂ `execution/` ⟂ `ontology_vault/` ⟂ `fixtures/+validate/`, so
  parallel workers don't collide (gate checks 7–8).

**Build sequence — L0 → L1 → L2 → L2.5:**

- **L0** (this work-pack): C2/C3/C8 + the DAG half of C4 as fixture-only proof —
  envelope, idempotent accept, receipts, DAG projector, audit-only vault
  projection, T1–T35 deterministic validator. Proves the *seam shape*.
- **L1**: C1, C5, C6, C7, C9, C10, C13 + lifecycle/KPI half of C4 — live capture,
  real KPI engine, candidate builder, scope/privacy gate, owner decision,
  `F-PROMOTION-*`. **Gated by B-002/OQ-4 vocabulary LOCK.** `mutation_allowed`
  flips true **per-org only** here (D-C).
- **L2**: C11, C12, C14 — reuse-packet store + hydrator, shared-card operator
  edit gate, signed per-CIC redaction tables.
- **L2.5**: C15, C16 — the DSPy+GEPA improvement engine + held-out KPI-delta
  verification. This is the layer that actually *closes* victor's D7 loop from
  "promotion" (lesson available) to "improvement" (lesson proven better).

Each layer escalates complexity; only L0 is `low`. The L1–L3 work-packs don't
exist yet — flagged in OQ-4 as a design→execution gap ("docs say carry into
`invoke plan` then `task-session`, but no plan/task-session artifacts exist").

---

*Every load-bearing claim above cites a spec selector. Where a decision is genuinely
open it says OPEN/PROPOSED, not a fabricated verdict. For the shape, the schema, and
the story, follow the cross-reference map.*
