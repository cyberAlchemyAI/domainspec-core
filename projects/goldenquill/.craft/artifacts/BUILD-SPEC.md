# BUILD-SPEC — Promotion Governance (REPO-ROOT Craft space)

- **Ledger:** `.craft/ledger.yml` · `ledger_id: craft.goldenquill.promotion_governance`
- **Human view:** `CRAFT.md`
- **Status:** implementation-ready spec · authored 2026-06-13 · planning/spec only — promotes nothing, mutates no canonical enum/architecture
- **Scope:** the GoldenQuill (Victor) learning loop — outcome → insight → owner-approved → card/per-org update — as an event-sourced governance spine.
- **Sources read in full:** `.craft/ledger.yml`, `CRAFT.md`, `docs/features/goldenquill-promotion-governance/integration/{whole-system-architecture-design.md,OPEN-QUESTIONS-LEDGER.md,runtime-design.md}`, `docs/features/goldenquill-promotion-governance/discovery/impl-architecture/drift-check-ledger.md`, and the feature spec set (`SPEC.md`, `domain.md`, `events.md`).

## Guardrails (non-negotiable, apply to every item below)

1. **No CIC→CLC coupling.** No item may encode a CIC→CLC subset binding in schema, table, predicate, or fixture. `F-CIC-CLC-COUPLING-VIOLATION` fail-closed (architecture v7.0.8). CIC and CLC are orthogonal; matching is opportunity-driven runtime.
2. **Substrate LOCKED.** Pydantic AI + Logfire + curated Python parsers + Ollama/vLLM + DSPy+GEPA (offline) + Cedar/Logician. No substrate proposals. Event journal = JSONL→SQLite per D-A. No new deps beyond numpy/scipy (frozen for L0 per D-E).
3. **Law 3 (Org Isolation).** No `orgs/` reads in this spec. Per-org isolation is a build constraint, not a read target. Cross-org leak is structurally fail-closed.
4. **Planning/spec only.** Do NOT mutate canonical enums or locked architecture. Where a count drifts, this spec specs the *reconciliation procedure* and which doc is authoritative — it does not edit the enum.
5. **Promotion authority is sole.** `OwnerDecision` is the only place `approved_allowed_uses` may be set (SPEC.md:89; domain.md:216). Every build item preserves the one-way valve: observation flows forward, approval flows only through the human gate.

---

# Part A — Decision framing (author for ratification)

Each decision is framed `question → options → tradeoffs → recommendation → ratification path`. **Owner: Vlad (domain modeler) proposes; Josh ratifies.** None is locked here.

## DEC-OQ4 [BLOCKING] — Promotion decision vocabulary: three typed surfaces vs one unified enum

**Question.** Does GoldenQuill keep three typed decision surfaces, or collapse them into one unified enum? This blocks the L1 candidate shape and the promotion-authority semantics (BLK-OQ4-VOCAB).

**The three surfaces in play** (today loosely all called "operator action"):

| Layer | Question answered | Proposed typed name | Enum (from spec) | Promotion meaning |
|---|---|---|---|---|
| Pursuit gate (Scout REVIEW) | Chase this discovered opportunity? | `PursuitDecision` | `accept · reject · hold` | NONE — drives lifecycle `eligible_match → go_no_go_approved`; `hold` stays `eligible_match`. |
| Fit verdict (Match-DB row) | Is this (client × funder) a real match? | `MatchFitVerdict` | `confirmed_fit · rejected · declined_cycle · pending` | NONE — evidence into lifecycle/outcome. |
| Promotion gate | Approve this insight for reuse? | `OwnerDecision` | `approved · rejected · retired · contradicted` (domain.md:464 OwnerDecisionStateValue) | SOLE — only setter of `approved_allowed_uses`. |

**Option A — Three typed surfaces (recommended).** Type each surface; LOCK `OwnerDecision` as the sole promotion vocabulary. One named cross-layer derivation only: `MatchFitVerdict + outcome → generate PromotionCandidate → human OwnerDecision`. Generation ≠ approval.
- *Pros:* preserves `hold`/`pending` (no `OwnerDecision` equivalent — `OwnerDecision` is near-terminal); aligns with the seam-map's three-layer reality; makes "nothing self-promotes" expressible as one schema constraint on one type. Deletes the seam-map `confirmed_fit→approved` / `declined_cycle→retired` rows as cross-layer category errors.
- *Cons:* three enums to maintain; readers must learn which layer a decision belongs to; the cross-layer derivation must be documented or it looks like coupling.

**Option B — One unified enum across all three layers.**
- *Pros:* single vocabulary, fewer types, one place to look.
- *Cons:* loses `hold` and `pending` (no promotion meaning, no clean target value); forces a lossy mapping; weakens the promotion-authority gate because "approved" could now be emitted from a pursuit/fit context, making the sole-setter invariant harder to enforce deterministically.

**Option C — Status quo (three vocabularies, no lock).**
- *Pros:* zero work now.
- *Cons:* keeps BLK-OQ4-VOCAB active; blocks L1 candidate shape indefinitely; the "operator action" ambiguity persists. Not recommended.

**Recommendation: Option A.** The three live at different layers and answer different questions; Option A is also the cheapest path to the GAP-PROMO-ENFORCE gate (the `approved_allowed_uses` setter constraint attaches to exactly one type). LOCK = three assertions: (1) `OwnerDecision` is the only promotion vocabulary and only `RecordOwnerDecision` may set `approved_allowed_uses`; (2) pursuit + fit decisions are typed non-promotion on their own layers; (3) one named derivation `MatchFitVerdict + outcome → PromotionCandidate → OwnerDecision`.

**Ratification path.** Vlad confirms the three-surface model (or selects B/C) → Josh ratifies → set `DEC-OQ4.selected`, flip BLK-OQ4-VOCAB to closed, and the L1 candidate-shape work (C7/C13) unblocks. Until then this is the single highest-leverage P0 gate.

## DEC-D2-FLIP — L0→L1 `mutation_allowed` authorization

**Question.** L0 is `mutation_allowed=false` (nothing canonical mutates). What authorizes the *first real per-org write*?

**Option A — Operator-signed per-org Ed25519 flip (recommended).** `mutation_allowed` flips false→true only on an operator Ed25519 deployment sign-off, **per-org**, reusing the classification-register trust mechanism (publisher-pinned pubkey, byte-for-byte). The flip is journaled as an event (auditable, replayable). Shared-card mutation stays separately gated (DEC-D3).
- *Pros:* matches existing white-glove Ed25519 discipline; keeps operator in loop; per-org scope means one client's go-live never touches another (Law 3); journaled = auditable.
- *Cons:* requires the Ed25519 verify path live before any L1 write; per-org ceremony overhead.

**Option B — Config flag.** A deployment setting flips it.
- *Pros:* trivial.
- *Cons:* no operator-in-loop guarantee; no per-org scope by default; not auditable as a journaled event; weakens sovereignty posture.

**Option C — Automatic after N green fixture/replay runs.**
- *Pros:* no human step.
- *Cons:* removes the human gate entirely — violates the one-way-valve thesis; "green replay" proves determinism, not promotion-readiness. Not recommended.

**Recommendation: Option A.** Per-org auto-apply *after* approval is fine; shared-card writes never flip here (they go through DEC-D3). Gate spec: see GAP-L0L1-FLIP.

**Ratification path.** Vlad proposes A → Josh ratifies → DEC-D2-FLIP `selected` set; feeds GAP-L0L1-FLIP gate build.

## DEC-D3-SHARED-GATE — keep shared cards general / prevent metric hill-climbing

**Question.** When does cross-org/shared knowledge get promoted, and what keeps a shared card "general" (D5a: guardposts, never overfit one funder)?

**Option A — Structural rule, no metric (recommended).** A shared card may only carry knowledge that is (i) `redaction_status = generalized` (domain.md:532), (ii) sourced from ≥K distinct orgs, (iii) observed across ≥2 CICs, (iv) free of any single-funder-specific. Enforced by a Logician predicate. **No optimization target at all.** Human gate (C12): shared-card promotion requires `consent_tier == composable_with_others` AND generalized redaction AND an operator Ed25519 card-edit review. Never automatic.
- *Pros:* D5a is explicit that shared cards are guardposts, not hill-climbed toward a metric — a structural boundary matches the intent and is machine-checkable; closes BLK-D5A-THRESHOLD via a `PromotionAuthorityPolicy` assertion rather than a tunable score; cannot be gamed by metric optimization.
- *Cons:* K and "single-funder-specific" need crisp definitions; structural rules can be over-conservative (block legitimately-general cards that happen to come from one org).

**Option B — Bounded metric (optimize a composite, but cap it).**
- *Pros:* lets a quality signal drive promotion.
- *Cons:* directly contradicts D5a "no metric hill-climb"; a cap is still a hill to climb toward; invites overfitting. Not recommended.

**Option C — Operator judgment only, no machine rule.**
- *Pros:* maximal human control.
- *Cons:* leaves BLK-D5A-THRESHOLD open (no machine-checkable boundary); not reproducible; relies entirely on operator vigilance.

**Recommendation: Option A.** Encode "no metric hill-climb" as a `PromotionAuthorityPolicy` assertion; make K + the cross-CIC requirement the machine-checkable definition of "general." Per-org promotion (DEC-D2) is the auto path; shared is the gated path. **Open sub-parameter for Josh: the value of K** (recommend K ≥ 3 distinct orgs as a starting floor).

**Ratification path.** Vlad proposes A + a K value → Josh ratifies K and the structural rule → BLK-D5A-THRESHOLD closes through the policy assertion.

## DEC-D4-VERIFY — verify improvement without overfitting (C15 apply / C16 verify, RK-006)

**Question.** An approved packet is *applied* (C15) and must be *verified* (C16) before it changes a live artifact. What counts as "improved" vs "regressed," and on what data?

**Held-out set diversity (recommended as a hard rule, both options below):** the eval set must span ≥2 CICs and ≥2 CLCs so a refinement cannot overfit one funder (RK-006). The proof is a held-out re-run, NOT the grant that produced the lesson.

**"Regressed" definition options:**

- **Option A — Any primary-KPI delta < 0 → reject.** Simple, strict.
  - *Pros:* trivial to implement and explain.
  - *Cons:* brittle to noise; a tiny negative delta from sampling variance triggers rejection; ignores guardrail KPIs.
- **Option B — Confidence-bounded margin + no statistically-significant guardrail-KPI decrease, across the diverse set (recommended).** Promote only if delta ≥ 0 on the primary KPI AND no guardrail KPI shows a significant decrease across ≥2 CICs. Descriptive stats only (numpy/scipy per D-E; no heavy causal stack).
  - *Pros:* tolerates noise; protects guardrail KPIs; stays inside the L0/L1 descriptive-analytics envelope; prevents single-funder overfit.
  - *Cons:* needs a defined significance threshold and a named guardrail-KPI set; "significant" must be a fixed, documented test (not tunable per run, or it becomes hill-climbing).
- **Option C — Composite score.**
  - *Pros:* one number.
  - *Cons:* a composite IS a metric to hill-climb — conflicts with DEC-D3/D5a; opaque. Not recommended.

**Recommendation: Option B** with a simple floor (delta ≥ 0 primary + no significant guardrail decrease across ≥2 CICs), descriptive stats only. A change that passes the OwnerDecision gate but fails C16 is rejected and logged as residue — never assumed live.

**Ratification path.** Vlad proposes B + names the guardrail-KPI set + the significance test → Josh (with validator lane) ratifies → feeds C16 acceptance criteria. Owner of the encoded rule: validator lane.

---

# Part B — REFINE-solvable build gaps (Define → Design → Plan + Acceptance)

Owner **Vlad** unless noted. Each follows Define (what/why) → Design (how) → Plan (build steps) → Acceptance (machine-checkable done). All respect the Part-0 guardrails.

## GAP-DESIGNED-NOT-BUILT [block] — build the learning-loop enforcement

**Define.** The loop (outcome → insight → owner-approved → card/per-org update) is fully designed but unbuilt; a human edits cards by hand today. Every Victor view agrees this gates the value thesis. L0 is fixture-only. *Owner: grant-runtime.*

**Design.** Build the L0 event spine that makes the contract executable while mutating nothing canonical (`mutation_allowed=false`):
- C2 — Event journal store + idempotency index. Append-only JSONL at `orgs/<slug>/vault/event_journal/<cycle_id>.jsonl` (path is a build target, not a read); in-memory index `idempotency_key → {offset, content_hash}` (D-A).
- C3 — `AcceptGrantWorkEvent` single ingress + `EventProjectionReceipt` (`created_refs`, `updated_refs`, `skipped_reason`, `blocked_reason`, `validation_state`). Idempotency: same key + same hash → no-op `skipped_reason=idempotent_replay`; same key + different hash → fail-closed `blocked_reason=duplicate_conflict`.
- DAG-half of C4 — `ProjectEventToDag` building `GrantRunNode`/`GrantRunEdge` (16 node kinds, 7 edge kinds per domain.md:329–360).
- C8 — `OntologyVaultProjection` audit-only (Pydantic + Cedar), `mutation_allowed=false`.

**Plan.** (1) Author the envelope fixture schema (12 required fields per SPEC.md:174–188). (2) Fake adapter fixtures (positive + negative). (3) Event acceptance validator (source-or-nothing; outcome events require `source_ref`). (4) DAG projector + receipts. (5) Negative fixtures incl. *adapter event attempting to set approved uses* (must reject — ties to GAP-PROMO-ENFORCE). (6) Deterministic pytest via `scripts/run_tests.sh` (pinned 3.14 interpreter). Build sequence is L0 only; L1+ deferred.

**Acceptance.** All ten First-Slice fixtures (SPEC.md ~615) pass deterministically: valid event→expected DAG; idempotent replay no-op; changed-content replay → contradiction/residue; adapter-sets-approved-uses → reject; pass path `run_context→delivery_envelope`; blocked path `kgie_preflight` blocked by `logician_gate_result`; declined-after-review; awarded-for-less; submitted-but-not-reviewed; report/closeout. No org-vault/card/dashboard write occurs (assert `mutation_allowed=false` honored). `scripts/run_lint.sh` clean.

## GAP-PROMO-ENFORCE [block] — centralized promotion-authority enforcement test

**Define.** Every doc repeats "KPIs/evidence/adapters cannot approve reuse — only `OwnerDecision` can," but there is **no centralized enforcement spec or test** proving an adapter's `approved_allowed_uses` is rejected. The central claim is unverified. *Owner: grant-runtime.*

**Design.** Make "nothing self-promotes" a **deterministic gate**, not a convention: `F-PROMOTION-NO-AUTO-APPROVE` (Logician/Cedar, fail-closed). It fires if `approved_allowed_uses` appears on ANY envelope, event, fact, candidate, or vault projection. Only `RecordOwnerDecision` carrying a valid operator Ed25519 signature may set it. This is one schema constraint (the field is absent on every type except `OwnerDecision`/`ApprovedReusePacket`) + one Cedar/Logician predicate + one test fixture. Depends on DEC-OQ4 Option A (single-type setter) for the cleanest form.

**Plan.** (1) Schema: assert `approved_allowed_uses` is `conditional`-required ONLY on `OwnerDecision` (domain.md:210) and present on `ApprovedReusePacket` only via a decision ref (domain.md:229). (2) Author the `F-PROMOTION-NO-AUTO-APPROVE` predicate (fail-closed) in the Logician gate family (C13). (3) Author the negative test: construct an `AdapterProducer`-emitted envelope/event with `approved_allowed_uses` populated → assert `AcceptGrantWorkEvent` rejects with `blocked_reason = premature approved use` (events.md:41). (4) Positive test: `RecordOwnerDecision` with valid Ed25519 + `decision=approved` sets it and emits `OwnerDecisionRecorded`. (5) Register in the F-PROMOTION-* family so coverage is enforced.

**Acceptance (spec the test).**
- `TEST-PROMO-ENFORCE-NEG`: any of {envelope, GrantWorkEvent, GrantOutcomeEvent, GrantKpiObservation, PromotionCandidate, OntologyVaultProjection} carrying `approved_allowed_uses` → gate fires `F-PROMOTION-NO-AUTO-APPROVE`, event rejected, receipt `blocked_reason` set. Asserted for all six producer surfaces.
- `TEST-PROMO-ENFORCE-POS`: `RecordOwnerDecision(decision=approved, Ed25519 valid)` → `approved_allowed_uses` accepted, `ApprovedReusePacketPublished` follows.
- `TEST-PROMO-ENFORCE-SIG`: `RecordOwnerDecision` with absent/invalid Ed25519 → fail-closed, no approved use set.
- Coverage gate refuses the cycle if the F-PROMOTION-* module/test is missing (mirrors `F-CLASS-COVERAGE-INCOMPLETE`).

## GAP-REDACTION-TABLES [flag] — per-CIC redaction/generalization rule table schema (C14)

**Define.** The per-CIC redaction/generalization rule tables (C14) are unauthored. Without them, `redaction_status=generalized` cannot be machine-determined per customer world, and the DEC-D3 shared-card gate has nothing to check generalization against. *Owner: governance.*

**Design.** Author the **table schema only** (not the populated tables — those are a governance-authoring task). YAML, signed (publisher Ed25519, white-glove-pinned pubkey, byte-for-byte trust mechanism per router-template discipline). One table per CIC (six CICs). **HARD GUARDRAIL: NO CIC→CLC coupling** — the table keys on CIC only and maps to redaction/generalization rules; it must not reference, key on, or imply any CLC. `F-CIC-CLC-COUPLING-VIOLATION` fail-closes if a CLC appears.

Proposed schema (per CIC table):
```yaml
cic_id: TILTH-CIC-0N            # closed set, the six canonical CICs only
version: <int>
publisher_signature: <ed25519>  # verified against pinned pubkey at load
rules:
  - rule_id: <stable>
    target_field: <field name in candidate/evidence>   # e.g. applicant_name, dollar_amount
    detect: <pattern|classifier ref>                    # how a direct identifier is recognized
    action: redact | generalize | block                # → maps to RedactionStatus values
    generalization_template: <string|null>              # required when action=generalize
    interpretation_limits: [<string>]                   # what the generalized form cannot prove
# NO clc_id, NO capital_logic, NO CIC→CLC mapping anywhere in this file.
```
Output of applying a table to a candidate → a `RedactionStatus` value (domain.md:525): `not_required | required | redacted | generalized | blocked`.

**Plan.** (1) Author the YAML schema + JSON-schema validator. (2) Author a signature-verify loader (reuse Ed25519 chain). (3) Author a lint rule `R-REDACTION-NO-CLC` that fails closed if any `clc`/`capital_logic` key appears. (4) Provide one fixture table (synthetic CIC, fixture data only — Law 3, no real org) proving load + apply + signature-verify. Populating the six real tables is a follow-on governance task, out of this spec's scope.

**Acceptance.** Schema validates; signed fixture table loads and verifies; tampered signature fails closed; a table containing any CLC reference fails `R-REDACTION-NO-CLC`; applying the fixture table to a candidate yields a correct `RedactionStatus`.

## GAP-L0L1-FLIP [flag] — gate spec for per-org `mutation_allowed` false→true

**Define.** No gate spec exists for flipping per-org `mutation_allowed` at the L0→L1 transition. *Owner: governance. Gated by DEC-D2-FLIP ratification.*

**Design (per DEC-D2-FLIP Option A).** A per-org flip authorized by operator Ed25519 sign-off, journaled as an event, reusing the classification-register trust mechanism. Gate `F-PROMOTION-MUTATION-UNAUTHORIZED` (fail-closed): any write to a per-org store with `mutation_allowed=false` OR without a valid journaled flip event → reject. Shared-card writes never flip here (they go via DEC-D3 / C12).

**Plan.** (1) Define a `MutationFlipRecorded` event kind (or reuse `owner_decision_recorded` with a flip sub-type — reconcile under GAP-EVENT-COUNT). (2) Author the flip operation: verify operator Ed25519 against pinned pubkey → append flip event to the per-org journal → set per-org `mutation_allowed=true`. (3) Author `F-PROMOTION-MUTATION-UNAUTHORIZED` predicate. (4) Per-org scope assertion (Law 3): a flip for org A cannot enable a write to org B.

**Acceptance.** Write with `mutation_allowed=false` → reject. Write after valid journaled flip → accepted (per-org only). Flip with invalid/absent Ed25519 → fail-closed. Cross-org write after a different org's flip → reject (Law 3). Flip event is replayable from the journal. **Blocked-on:** DEC-D2-FLIP ratified.

## GAP-KPI-COUNT [flag] — reconcile "47 KPIs" prose vs 44-entry GrantKpiKind enum

**Define.** Integration prose says "47 KPIs" (`integration/ARCHITECTURE.md:81`, `runtime-design.md:146` and `:162`) but the canonical `GrantKpiKind` enum has **44** entries (`domain.md:402–449`, verified by direct count). A 3-entry gap. *Owner: grant-runtime. Spec the reconciliation — do NOT mutate the enum.*

**Design.** The canonical source of truth is the `GrantKpiKind` enum in `domain.md` (44 entries). The "47" in integration prose is unverified and must be reconciled to one of two resolutions, decided by grant-runtime:
- **(R1) Prose is wrong → 44 is canonical.** Update the three prose sites to "44 KPIs." Lowest-risk; the drift-check already verified 44 by direct count. **Recommended.**
- **(R2) Three KPIs are genuinely missing from the enum.** Grant-runtime names the 3 intended-but-absent KPIs; they enter the enum via a normal domain-model amendment round (NOT in this spec). Only choose R2 if the 3 are real and identifiable.

**Plan.** (1) Grant-runtime confirms whether 3 KPIs are genuinely missing. (2) If no → adopt R1 (prose edit, out of this spec's mutation scope but specced here as the action). (3) If yes → file a domain.md amendment listing the 3; reconcile prose to the new count. (4) Either way, add a single-source-of-truth note: integration docs cite the enum count, never restate a number.

**Acceptance.** Prose count == enum count across all sites; a doc-lint (or review checklist item) asserts no integration doc states a KPI count that disagrees with `len(GrantKpiKind)`. No enum mutation performed inside this spec.

## GAP-EVENT-COUNT [flag] — reconcile event-count 13 vs 12 vs GrantWorkEventKind enum (9)

**Define.** Three numbers float: `events.md` has **13** top-level event sections (verified: 13 `##` headers); `GrantWorkEventKind` enum has **9** values (`domain.md:301–313`); a "12" appears in residue with no identified source. *Owner: grant-runtime. Spec the reconciliation — do NOT mutate the enum.*

**Design.** The three counts measure **three different things** — the reconciliation is to name each axis, not to force one number:
- **13** = operation-output events in `events.md` (GrantWorkEventAccepted, GrantWorkEventRejected, DagProjectionUpdated, GrantRunNodeRecorded, GrantOutcomeEventRecorded, KpiObservationComputed, KpiProjectionUpdated, PromotionCandidateCreated, PromotionCandidateProjected, GovernanceProjectionValidated, OwnerDecisionRecorded, ApprovedReusePacketPublished, FutureGrantContextHydrated). These are events the *operations* emit downstream.
- **9** = `GrantWorkEventKind` ingestion families (`run_node_recorded`, `run_edge_recorded`, `gate_result_recorded`, `outcome_event_recorded`, `kpi_observation_recorded`, `cycle_receipt_recorded`, `reflection_packet_recorded`, `owner_decision_recorded`, `approved_reuse_available`). These are what *adapters emit into* the journal.
- **12** = unidentified. Most likely a stale intermediate count (e.g., 13 minus one merged section, or an early enum draft). Treat as a phantom until grant-runtime identifies its origin.

**Plan.** (1) Adopt the two-axis framing in a canonical note: "ingestion event kinds (9, `GrantWorkEventKind`)" vs "operation-output events (13, `events.md`)" — distinct, both correct. (2) Grant-runtime searches for the "12" origin (git history / prior drafts); if found stale → strike it; if it names a real third axis → document that axis. (3) Reconcile `runtime-design.md:271` residue item 1 to the two-axis statement. No enum mutation.

**Acceptance.** A canonical note distinguishes the 9 ingestion kinds from the 13 operation-output events with both citations; the "12" is either explained or struck as stale; no doc restates a bare "event count" without naming which axis. No enum mutation performed inside this spec.

---

# Part C — Build sequencing (from D5)

```
1. DEC-OQ4 LOCK (vocabulary)          ─┐ proves the central claim; unblocks L1 candidate shape
2. GAP-PROMO-ENFORCE (F-PROMOTION gate) ┼─▶ highest-leverage; makes "nothing self-promotes" verifiable
3. BLK-B001 TEST-SPEC T1–T35 stable   ─┤
4. GAP-DESIGNED-NOT-BUILT (L0: C2/C3/C8 + DAG-half C4) against T1–T35 fixtures
5. DEC-D2-FLIP ratify ─▶ GAP-L0L1-FLIP gate (L1)
6. DEC-D3-SHARED-GATE ratify ─▶ shared-card gate + D5a assertion (L2); GAP-REDACTION-TABLES schema feeds it
7. DEC-D4-VERIFY ratify ─▶ C15 apply + C16 verification (L2.5)
   (GAP-KPI-COUNT, GAP-EVENT-COUNT: doc-reconciliation, run in parallel — no build dependency)
```

The two genuinely hard gates are **human, not technical**: the DEC-OQ4 vocabulary LOCK and the DEC-D3 shared-card review. Everything else is mechanical once those are decided.

---

# Verdict lines

```
DEC-OQ4              | Vlad proposes / Josh ratifies | decision-gated  | Vlad confirms three-surface (rec. A) vs unified enum; Josh ratifies; then BLK-OQ4-VOCAB closes + L1 candidate shape unblocks
DEC-D2-FLIP          | Vlad proposes / Josh ratifies | decision-gated  | Vlad proposes operator-signed per-org Ed25519 flip (rec. A); Josh ratifies; feeds GAP-L0L1-FLIP
DEC-D3-SHARED-GATE   | Vlad proposes / Josh ratifies | decision-gated  | Vlad proposes structural no-metric rule + K value (rec. A); Josh ratifies K; closes BLK-D5A-THRESHOLD
DEC-D4-VERIFY        | Vlad proposes / Josh ratifies | decision-gated  | Vlad proposes Option B (margin + guardrail-significance) + guardrail-KPI set; Josh+validator ratify; feeds C16
GAP-DESIGNED-NOT-BUILT | grant-runtime             | refine-solvable | Build L0 spine (C2/C3/C8 + DAG-half C4) against ten First-Slice fixtures; mutate nothing canonical
GAP-PROMO-ENFORCE    | grant-runtime               | refine-solvable | Build F-PROMOTION-NO-AUTO-APPROVE gate + neg/pos/sig tests proving adapter approved_allowed_uses is rejected
GAP-REDACTION-TABLES | governance                  | refine-solvable | Author signed per-CIC redaction table schema + NO-CLC lint + fixture; populate-six is follow-on governance
GAP-L0L1-FLIP        | governance                  | refine-solvable (blocked on DEC-D2-FLIP) | Spec F-PROMOTION-MUTATION-UNAUTHORIZED gate + journaled per-org Ed25519 flip
GAP-KPI-COUNT        | grant-runtime               | refine-solvable | Reconcile to enum (44) via R1 prose-fix or R2 named-amendment; doc-lint enforces; no enum mutation here
GAP-EVENT-COUNT      | grant-runtime               | refine-solvable | Adopt two-axis framing (9 ingestion kinds vs 13 op-output events); identify/strike the phantom 12; no enum mutation here
```

**Output file:** `.craft/artifacts/BUILD-SPEC.md`
