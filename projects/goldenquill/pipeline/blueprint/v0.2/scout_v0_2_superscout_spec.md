---
spec_id: SCOUT-V0.2-SUPERSCOUT
version: v0.2-DRAFT-001
status: DRAFT (not LOCKED; LOCK ceremony separate; two-audit cycle per L-005)
filed: 2026-05-19
operator: Josh Inklovich
parent_handoff: pipeline/handoffs/scout_v0_2_superscout_exploration_2026-05-19.md
locked_architecture_references:
  - pipeline/architecture/v0.1/tilth_architecture_locked.md                  # v7 LOCKED 2026-04-19 — A1-A12; A1 single-client, A4 operator-trusted preflight, A12 Decimal mandate
  - pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md              # v7.0.5 LOCKED 2026-05-10 row 179 — Funder Intel DB + Match DB + Scout channel G + Stage-5 consent-tier on-ramp (LOAD-BEARING parent for §2 two-layer DB + §3 Channel G + §4 MatchOutcome)
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md              # v7.0.7 LOCKED 2026-05-10 row 180 — classification-driven routing + F-CLASS-* family + heavy-Judge swap; CANONICAL PRECEDENT for L-006 DORMANT-BINDING PATTERN
  - pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md              # v7.0.8 LOCKED 2026-05-08 — CIC × CLC orthogonality (F-CIC-CLC-COUPLING-VIOLATION); LOAD-BEARING for §6 CIC-aware configuration
  - pipeline/architecture/v0.1/architecture_v7_0_9_amendment.md              # v7.0.9 LOCKED 2026-05-10 row 202 — Reflection v0.1 hook + F-REFLECTION-* dormant primitives (sibling-producer to §16 Reflection Packet)
  - pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md             # v7.0.10 LOCKED 2026-05-11 row 215 — three-posture routing (Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign)
  - pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md        # v7.0.11 DRAFT — card system as architectural primitive (CIC + CLC machine-readable cards)
  - pipeline/blueprint/v0.1/section_15_archivist.md                          # §15 v1 LOCKED 2026-05-10 — Archivist between-cycle preservation; v1.x curation-slot binding (relevant to §9 LOCK-blocker)
  - pipeline/blueprint/v0.1/section_16_reflection_packet.md                  # §16 v1 LOCKED 2026-05-15 — ReflectionPacket artifact + F-PACKET-* family (sibling-not-nested with ScoutReflection)
  - pipeline/funder_intelligence/_seats/scout/heuristics.md                  # Pass-2 Scout cross-charter heuristic library (5 funder classes, 4 routing axes, 3 timing axes, 5 escalation triggers, 5 anti-patterns)
  - pipeline/funder_intelligence/_validators/gate_taxonomy_consistency.py    # Pass-1 gate_taxonomy v1 (5 allowed gate-type tuples; AST-enforced)
audit_trail: pipeline/validation/scout_v0_2_audit_1_thesis_2026-05-19/  # populated when L-005 round dispatches
session_metrics: pipeline/metrics/session_log.jsonl
amendment_class: new-spec-with-DRAFT-status-and-DORMANT-cross-applicant-binding-and-OPERATOR-DECIDABLE-loop-ownership
review_discipline: L-005 strict two-cycle (Audit #1 scoping landed at docs/scout_v0_2_audit_1_thesis_2026-05-19.md → operator review → Audit #2 verification → LOCK or escalate)
cross_family_posture: LIVE FULL CROSS-FAMILY (no Section E carve-out) at LOCK ceremony per WS-D v7.0.5 + §15 v1 + §16 v1 precedent (Editor=Meta-family + Judge=Google-family + Red Team=OpenAI-OSS-family via openclaw bridge)
operator_decidable_at_lock:
  - daemon_loop_owner_v0_2  # recommended Scout-owns-loop (see §9); flips to Archivist-owns-loop at v0.3 when §15 matures; OPERATOR CONFIRMS AT LOCK CEREMONY
not_yet_committed:
  - SUB_KIND_REGISTRY entry for ScoutReflection (deferred to v0.2 first wave compound LOCK paired with §15 v2.x SPEC)
  - F-SCOUT-* gate predicate bodies (NotImplementedError stubs at SPEC DRAFT; Cedar/Python realization paired with §4 v2.x.y amendment at LOCK)
---

# Scout v0.2 (SuperScout) — Specification

## §0 Header and scope

This SPEC defines **Scout v0.2 (SuperScout)** — the second-generation Scout seat that upgrades the v0.1 request-response discovery loop into a continuously-operating, database-first, hypothesis-generating discovery system. Scout v0.1 (`pipeline/orchestrator/seats/scout.py`) stays LOCKED and continues to operate; v0.2 is a forward-design SPEC, not a refactor of v0.1 code.

**Status discipline.** This document is `DRAFT`. The LOCK ceremony is separate and follows the L-005 strict two-cycle Thesis dispatch pattern (cross-family openclaw bridge per AGENTS.md). At LOCK, the operator confirms (a) the daemon-loop-ownership decision pre-baked in §9 and (b) the F-SCOUT-* predicate signatures registered at §A and §B. Until then, no Scout v0.2 code lands; existing v0.1 Scout serves all live cycles.

**Naming reconciliation.** "Scout v0.2" and "SuperScout" name the same artifact. SuperScout is the working title in the exploration handoff; Scout v0.2 is the canonical SPEC ID per the version chain.

## §1 Mission

Scout v0.2 is the **continuously-fresh opportunity-discovery surface** of the Tilth pipeline. Where Scout v0.1 answers "is this opportunity worth pursuing right now?" on operator demand, Scout v0.2 maintains a self-refreshing pipeline state that the operator can query at any time and receive the current cached result — no synchronous scan blocks the query path. Scout v0.2 adds:

- **Database-first discovery** — the two-layer Funder Intelligence Database (operator-curated workspace layer + per-applicant vault layer) is the structural spine of DISCOVER. Channels A-F (federal APIs / curated caches / portals / program pages / RSS / client-driven web search) are *gap-fill against the database*, not parallel peers to it.
- **Channel G — Relationship-Sourced track** — nomination-only / invitation-only / advisory-sourced programs become a discovery channel rather than fail-closed-to-Avoid, governed by F-NOM-* gates that prevent fabricated relationships and cold-outreach drafting.
- **Match Database feedback loop** — every cycle's win/loss outcome feeds a typed `MatchOutcome` artifact that enriches the per-applicant DB; cross-applicant aggregation is DORMANT at v0.1 and engages at Stage-2+ via Sovereign-Node consent tiers.
- **Cycle-aware pipeline auto-promotion** — FY-N+1 rows promote to active tier automatically when historical-cycle reopening dates approach.
- **CIC-aware configuration** — Search Vocabulary, Evidence Schema, Language Register, and Reporting Rhythm per CLAUDE.md Customer Identity Category cards configure Scout per-applicant; CLC-typing happens at opportunity ingestion (funder-side), CIC-typing at applicant configuration (applicant-side); matching is opportunity-driven, not archetype-driven (v7.0.8 binding; F-CIC-CLC-COUPLING-VIOLATION fail-closed).
- **Coalition-opportunity surfacing** — NSF Engines / EDA Tech Hubs / large-coalition NOFOs flagged *coalition-required* with sub-status *coalition-participants-known*; Scout does not auto-Avoid because the applicant cannot solo.
- **Channel A-G orthogonality** — no channel is a fallback; all run parallel.
- **Runtime-mode duality** — `ONE_SHOT` (operator-triggered scan, current v0.1 shape) plus `DAEMON` (scheduled / event-driven, continuously-fresh pipeline state). Operator queries pipeline state at any time and receives current cached result.
- **Self-directed search expansion** — each cycle emits a typed `ScoutReflection` Pydantic artifact capturing queries run, channel-by-channel hits, matches scored, near-misses, novel-hypothesis candidates, and search-vector deltas vs prior reflection. Subsequent cycles consume the prior reflection as input to direct what to search next.
- **Hypothesis-generation primitive** — new search-vector candidates surface from (a) winning matches' funder-adjacent funders (graph-walk on funder portfolios + co-grantee patterns), (b) losing matches' near-miss vocabulary, (c) funder-announcement RSS / newsletter delta vs prior baseline, (d) cross-applicant patterns at Stage-2+ via Sovereign-Node consent tiers (DORMANT at v0.1).
- **Daemon sovereignty + cost controls** — Daemon operation respects v7.0.10 posture per call; new-finding classification defaults to `confidential` (F-CLASS-NEW-FACT-UNCLASSIFIED); per-cycle dollar/token/API-call budget operator-configured at white-glove (F-SCOUT-DAEMON-BUDGET-EXCEEDED fail-closes); posture-drift fail-closes (F-SCOUT-DAEMON-POSTURE-DRIFT); daemon cycles emit Logfire spans for auditability; rate-limits enforced against funder APIs.

What Scout v0.2 does NOT do: it does NOT score drafts (Judge / Red Team), does NOT write proposal text (Scribe), does NOT submit (Uploader), does NOT mutate KFR or Funder Intelligence Database canonical entries directly (Archivist owns curation slot per v7.0.4 §9 + v7.0.5 §6). Scout v0.2 *proposes* new pipeline state and DB enrichments; operator confirms canonical mutations.

## §2 Design goals (12, restated SPEC-grade from the handoff)

The handoff (`pipeline/handoffs/scout_v0_2_superscout_exploration_2026-05-19.md`) enumerates twelve binding design goals (eight existing + four daemon-mode additions). Each is restated here SPEC-grade with the runtime-consumer link.

### §2.1 Database-first as structural primitive

Layer 1 (the two-layer Funder Intelligence Database) is the spine of DISCOVER. Channels A-F are gap-fill against the database, not parallel peers to it. Concretely: every DISCOVER cycle starts by scanning the operator-curated workspace DB and the per-applicant vault DB for fit before any external channel is invoked. Channels A-F fire to fill known database gaps (e.g., a funder is on the operator's radar but the program-page details have not been fetched yet) and to surface novel candidates that the database does not yet carry. Channel-A-through-F output is *proposed* into the per-applicant DB for operator confirmation; promotion to operator-curated workspace is operator-gated (mirrors Intake's pending→canonical discipline per §11).

**Runtime consumer:** all subsequent seats (Scribe, Judge, Red Team, Logician) read funder profile data from the two-layer DB rather than from Scout's per-cycle scratch. Scout v0.1's pre-Pass-2 behavior of bypassing the database is structurally prevented at v0.2 via gate F-FUNDER-DB-BYPASSED (registered at §A; predicate body realized at §B paired §4 v2.x.y amendment).

### §2.2 Two-layer funder-intelligence database with Law-3 isolation

Two layers, both signed and audit-trailed:

(a) **`vault_shared/funder_intelligence/`** — operator-curated workspace layer. Ships at Golden Image build. Refreshed via publisher-Ed25519-signing parallel to v7.0.7 §6.1 router-template + §17 v1 Coefficient Registry trust mechanism. White-glove publisher-pubkey pin at onboarding (mirrors §17 v1 §3 byte-for-byte). Cross-applicant pattern, not per-applicant.

(b) **`orgs/<slug>/vault/funder_intelligence/`** — per-applicant vault layer. Never crosses Law 3. Additively enriched by that applicant's Scout cycles. `F-FUNDER-DB-CROSS-ORG-LEAK` enforces structural prohibition on per-org content writing to any other org's layer.

The two layers are sibling-not-nested. Operator-curated workspace is the architectural ground truth across the fleet (Stage 2+); per-applicant vault is the Law-3-isolated learning that one Tilth accumulates for one applicant. Stage-5 cross-Tilth contribution-back happens via Sovereign Node consent tier (out-of-scope for v0.1 and v0.2; the on-ramp is documented at v7.0.5 §6).

**Schema authority:** the per-layer Pydantic schemas are defined at §B (canonical yaml); the field-by-field listings live in the paired Logician amendment at LOCK ceremony.

### §2.3 Channel G — Relationship-Sourced track

Nomination-only / invitation-only / advisory-sourced programs (Skoll-pattern, Echoing Green, MacArthur Fellows-class) are a discovery channel, not Avoid. Channel-G output shape is *nominator-pathway prospect*, depending on KFR-resident relationship facts (Intake BULK_INGEST / INCREMENTAL_INGEST at v0.1; field set declared at §B).

Three governing gates (full predicate registrations at §A):

- `F-NOM-FABRICATED-RELATIONSHIP` (hard_eligibility_gate, P0, REJECT_NO_DRAFT) — fail-closed when a nominator-pathway prospect carries a relationship-fact field that does NOT trace to an operator-confirmed KFR entry with `validation.confirmed_by` populated.
- `F-NOM-COLD-OUTREACH-DRAFT` (drafting_warning, MED, WARN_SCRIBE) — flag-and-warn when Channel-G prospect lacks any documented prior contact AND Scribe is invoked to draft a nominator-pathway email. Scribe is allowed to draft *operator-asks-network* outreach; Scribe is NOT allowed to draft *cold-outreach-to-nominator-target*. The distinction is structural (operator-asks-network targets KFR-resident relationship facts; cold-outreach targets a stranger).
- `F-NOM-NETWORK-LEAK` (hard_eligibility_gate, P0, REJECT_NO_DRAFT) — fail-closed when a Channel-G prospect's nominator-network is shared across orgs (Law 3 structural prohibition; one applicant's network is one applicant's asset).

### §2.4 Match Database feedback loop

Each cycle's win/loss outcome feeds the per-applicant DB as a typed `MatchOutcome` Pydantic artifact. Cycle close → MatchOutcome emit → Archivist quarterly digest reads MatchOutcome rollups (per §15 v1 §15.4.2 input contract; Archivist proposes lessons-delta integrations) → operator-confirmed lessons feed back into Scout's next cycle's hypothesis-generation primitive (§2.11).

Stage-2+ aggregates across the fleet via consent tier (DORMANT at v0.1 and v0.2, same pattern as Reflection Packet §16 v1 OQ-2 (a) — schema authored, predicates dormant, META-gate LIVE).

The `MatchOutcome` schema is sibling-not-nested with `ScoutReflection` (this SPEC) and `ReflectionPacket` (§16 v1). All three are cycle-close artifacts; each has its own producer, consumer, schema, and F-* family. Cross-family-import ban applies at AST-lint (see §7).

### §2.5 Cycle-aware pipeline auto-promotion

FY-N+1 pipeline rows promote to active tier automatically when historical-cycle reopening dates approach. Calendar-driven, not LLM-driven — the promotion logic is deterministic Python reading the operator-curated workspace DB's `historical_cycle_pattern` field (e.g., USDA-RD CFP rolling, USDA-AMS VAPG annual ~July, PA-DEPT-AG-AGINNOV biennial-with-annual-adjustments per §1.3 Scout heuristics).

Promotion shape: pipeline row transitions from `tier: shadow` → `tier: active_watch` when the cycle's historical-reopen-date enters a configurable lookahead window (default 90 days; operator-tunable per applicant). Operator is notified via the daemon-cycle digest surface (§2.10).

Auto-promotion never crosses to *operator-confirmed pursuit*; that transition stays operator-explicit per Law 5 (applicant brings the substance). Auto-promotion is a Scout-side hint, not a decision.

### §2.6 CIC-aware Scout configuration

Per CLAUDE.md Customer Identity Category cards and architecture v7.0.11 §1.2 card axes, Scout v0.2 reads the applicant's CIC card at startup and configures four runtime primitives per the card:

- **Search Vocabulary** — the term set Scout uses against external channels (Channels A-F) for that applicant.
- **Evidence Schema** — the operator-confirmed substance fields Scout cross-references when scoring fit.
- **Language Register** — funder-dialect setting that downstream Scribe inherits (Law 4 axis (a)).
- **Reporting Rhythm** — cadence preference Scout uses when scheduling the applicant's daemon cycles (§2.9).

CLC-typing happens at opportunity ingestion (funder-side), CIC-typing at applicant configuration (applicant-side). The two axes are orthogonal — there is no CIC→CLC subset binding (architecture v7.0.8). Matching at runtime is opportunity-driven: Scout/Logician identify the CLC the opportunity belongs to; the applicant's CIC determines the *seat configuration* that processes it; the CLC determines the *underwriting logic* and example sources. `F-CIC-CLC-COUPLING-VIOLATION` (v7.0.8) fail-closes any code path that hardcodes a subset coupling.

The CIC-aware configuration is read-only at Scout v0.2; Scout does not mutate the CIC card. Card amendment is operator-driven per v7.0.11 §1.4 lifecycle.

### §2.7 Coalition-opportunity surfacing

Large-coalition NOFOs (NSF Engines, EDA Tech Hubs, USDA Climate-Smart Commodities-class) carry a structural reality: the applicant cannot solo. Scout v0.1's default behavior of fail-closed-to-Avoid on such opportunities is a Law-2-boundary-drift failure mode (the opportunity is *in scope for the applicant as a coalition participant*; only the solo-applicant variant is out of scope).

Scout v0.2 flags coalition-required opportunities with two sub-statuses:

- `coalition_required: true` (Boolean) — the program structurally requires a coalition.
- `coalition_participants_known: <enum>` — values `{none, partial, full}` indicating whether the applicant has named coalition partners in KFR.

When `coalition_required: true` AND `coalition_participants_known != full`, Scout surfaces an operator-attention trigger (NOT a hard gate; operator decides whether to pursue coalition formation). When `coalition_required: true` AND `coalition_participants_known: full`, Scout treats the opportunity as standard MUST_READ / MAYBE / DECLINED triage per the applicant's CIC + the funder's CLC.

### §2.8 Channel A-G orthogonality

No channel is a fallback. All seven channels run parallel:

- A — Federal APIs (Grants.gov search2 / fetchOpportunity, SAM.gov, USASpending)
- B — Curated cached datasets (subscription feeds, prior rosters, seeded foundation spreadsheets)
- C — Seeded state / foundation portals
- D — Federal program pages
- E — RSS / newsletter watchlists
- F — Client-material-driven web search
- G — Relationship-Sourced (new at v0.2 per §2.3)

VERIFY phase (per Scout v0.1 round 9 spec) still gates promotion of any candidate to CRITICAL-fit status — VERIFY fetches the live synopsis before elevation; assigns VERIFIED_FIT / VERIFIED_NOT_FIT / UNVERIFIED / VERIFICATION_FAILED. REVIEW is still the human gate.

### §2.9 Runtime-mode duality — Scout-OneShot + Scout-Daemon

Scout v0.2 supports two runtime modes:

- **`ONE_SHOT`** — operator-triggered scan, current v0.1 shape preserved. CLI: `tilth scout one-shot --org <slug>` (preserves v0.1 invocation). Returns the same `radar.json` shape as v0.1 for backward compatibility, plus a `scout_reflection_id` field linking to the emitted ScoutReflection artifact (§2.10).
- **`DAEMON`** — scheduled / event-driven, continuously-fresh pipeline state. Cadence operator-configured per applicant via the `schedule` skill pattern (`mcp__scheduled-tasks__*`). Per-applicant cadence-config schema declared at §B.

**Query pipeline cache contract.** Operator queries pipeline state at any time via `tilth scout pipeline-state --org <slug>` and receives the *current cached* result — no synchronous scan blocks the query path. The cache lives at `orgs/<slug>/vault/scout/pipeline_state.yaml` (canonical-JSON-signed per v7.0.4-M1 §2). Cache freshness is exposed (`last_refreshed_utc: <iso8601>`, `next_scheduled_refresh_utc: <iso8601>`) so the operator can decide whether to trigger an immediate one-shot refresh.

The two modes share the same channel taxonomy, the same VERIFY phase, the same ScoutReflection emit shape, the same Logician gate family. They differ only in *trigger* (operator vs scheduled) and *cadence* (single-fire vs continuous).

### §2.10 Self-directed search expansion — ScoutReflection artifact

Each cycle (DAEMON cycle or ONE_SHOT cycle) emits a typed `ScoutReflection` Pydantic artifact. Full schema at §B; summary fields:

- `cycle_id: str` — opaque caller-minted UUID.
- `org_slug: str` — Law-3 binding.
- `cycle_runtime_mode: enum {one_shot, daemon}` — provenance for the cycle.
- `posture: enum {frontier_eligible, split_context_hybrid, local_only_sovereign}` — the v7.0.10 deployment posture in force at cycle start.
- `queries_run: tuple[QueryAttempt, ...]` — every external query attempted, with channel attribution, term set, timestamps, response status.
- `hits: tuple[HitRecord, ...]` — channel-by-channel raw matches before VERIFY.
- `matches_scored: tuple[ScoredMatch, ...]` — post-VERIFY ranked matches.
- `near_misses: tuple[NearMiss, ...]` — candidates that scored below threshold; *what was Scout almost right about*. Feeds §2.11 vocabulary mining.
- `novel_hypotheses: tuple[Hypothesis, ...]` — proposed new search vectors for the next cycle. Sources at §2.11.
- `search_vector_deltas: tuple[VectorDelta, ...]` — diffs vs prior reflection: new vectors added, retired vectors retired, vector weights adjusted.
- `budget_spent: BudgetSpent` — dollar / token / API-call totals for the cycle (per §2.12 daemon sovereignty).
- `logfire_span_root_id: str` — root span for this cycle's full Logfire trace (per §8).

Subsequent cycles consume the prior reflection as input — concretely, the daemon-loop entry point reads the most-recent ScoutReflection from `orgs/<slug>/vault/scout/reflections/` and passes its `novel_hypotheses` and `search_vector_deltas` into the next cycle's plan-builder.

**Sibling-not-nested with §16 ReflectionPacket.** ScoutReflection and ReflectionPacket are sibling artifacts: both consume Logfire span tree as shared substrate, both emit at cycle close, but they have distinct producers (Scout vs §15 Archivist Reflection sub-mode), distinct consumers (Scout-Daemon next-cycle vs Archivist learning loop), distinct schemas, and distinct F-* gate families (F-SCOUT-REFLECTION-* and F-PACKET-*). Cross-family-import ban applies at AST-lint (see §7).

### §2.11 Hypothesis-generation primitive

New search-vector candidates surface from four sources:

(a) **Graph-walk on winning matches' funder-adjacent funders.** When the per-applicant Match Database carries a WIN row for funder F, Scout walks the operator-curated workspace DB to surface funders whose program portfolio overlaps F's. The walk is deterministic Python over operator-curated graph structure (NOT LLM-driven). Output: novel hypotheses tagged `source: graph_walk`.

(b) **Near-miss vocabulary.** When a prior cycle's `near_misses` field carries candidates that scored 60-79 (the operator-tunable just-below-MUST_READ band), Scout extracts the candidate's program-page vocabulary (terms present in the program page that are absent from the applicant's current Search Vocabulary). Tagged `source: near_miss_vocabulary`. Vocabulary candidates surface as operator-review-required hypotheses, never auto-merged into Search Vocabulary (Law 5).

(c) **Funder-announcement RSS / newsletter delta.** Channel E (RSS / newsletter watchlists) carries a per-applicant baseline of subscribed announcements. Cycle-over-cycle delta surfaces (i) new announcements published since the prior cycle and (ii) recurring-program announcements whose terms have changed cycle-over-cycle. Tagged `source: rss_delta`.

(d) **Cross-applicant patterns at Stage-2+ via Sovereign-Node consent tiers** — DORMANT at v0.1 and v0.2. Schema field reserved (`source: cross_applicant`) but production-blocked by `F-SCOUT-HYPOTHESIS-CROSS-APPLICANT-LEAK` (hard_eligibility_gate, P0, REJECT_NO_DRAFT) until operator-signed consent tier engages at Stage 2+. The DORMANT pattern mirrors §16 ReflectionPacket OQ-2 (a) and v7.0.7 §1.4 DORMANT-BINDING discipline.

Two governing gates:

- `F-SCOUT-HYPOTHESIS-FABRICATED` (hard_eligibility_gate, P0, REJECT_NO_DRAFT) — every hypothesis MUST carry a non-empty `source` field whose value names an operator-curated substrate or a workspace-curated graph traversal. Hypotheses with `source: null` OR `source` referencing a non-existent / non-operator-confirmed substrate fail-close at gate time. Fabrication prevented structurally — Scout cannot invent funder names.
- `F-SCOUT-HYPOTHESIS-CROSS-APPLICANT-LEAK` (hard_eligibility_gate, P0, REJECT_NO_DRAFT) — until Stage 2+ consent tier engages, any hypothesis with `source: cross_applicant` fail-closes regardless of substrate provenance. The DORMANT field is reserved at the schema layer; the gate is LIVE-fail-closed.

### §2.12 Daemon sovereignty + cost controls

Daemon operation respects v7.0.10 posture per call. The cycle-start handshake reads the operator-signed deployment manifest (`orgs/<slug>/vault/classification/register.yaml` per v7.0.7 §1.4) and pins the cycle's posture to the operator-signed value. Mid-cycle posture change is prohibited (mirrors F-CLASS-POSTURE-MID-CYCLE-CHANGE per v7.0.10 §5).

**Classification of newly-discovered programs** defaults to `confidential` per `F-CLASS-NEW-FACT-UNCLASSIFIED` (verify_required_gate, VERIFY_REQUIRED, HOLD_FOR_OPERATOR_REVIEW). Operator confirms classification at the next pipeline-state review; until confirmed, newly-discovered program data does NOT route cloud regardless of posture.

**Per-cycle budget operator-configured at white-glove.** Three budget axes:

- `daemon_dollar_budget_per_cycle_cents: int` (Decimal mandate per A12; int micro-dollars-or-cents)
- `daemon_token_budget_per_cycle: int`
- `daemon_api_call_budget_per_cycle: int` (per-API call ceilings: Grants.gov, SAM.gov, USASpending, cloud-LLM)

`F-SCOUT-DAEMON-BUDGET-EXCEEDED` (verify_required_gate, HIGH, HOLD_FOR_OPERATOR_REVIEW) fail-closes any in-flight cycle that breaches *any* of the three axes. The cycle freezes at the gate; partial cycle state persists to disk per Rule 1 (Save State Always); operator is alerted via the daemon-cycle digest surface.

`F-SCOUT-DAEMON-POSTURE-DRIFT` (hard_eligibility_gate, P0, REJECT_NO_DRAFT) fail-closes any cycle that would route differently than the operator-signed posture allows. Drift detection: cycle-start posture hash vs per-call routing decision; mismatch → fail-close.

**Daemon cycles emit Logfire spans for auditability** per §8.

**Rate-limits enforced against funder APIs.** Channel-A APIs (Grants.gov, SAM.gov, USASpending) have published rate limits; Channel-G nominator-pathway lookups have informal-courtesy norms. Rate-limit enforcement is per-channel: each channel-adapter carries a per-channel token bucket configured at white-glove with operator-tunable defaults. Breach → backoff, not retry-storm. Logfire span captures rate-limit-near-breach as a per-cycle observation.

## §3 §A Adversarial pre-checks

Per Codex framing + Pass 1 gate taxonomy v1, three required strength-checks on this SPEC:

### §3.1 runtime_consumer

What changes for each downstream seat under Scout v0.2:

- **Scribe.** Reads funder profile from the two-layer Funder Intelligence Database (§2.2) rather than from Scout's per-cycle scratch. Channel-G nominator-pathway prospects unlock a new Scribe drafting context (`nominator_pathway_outreach`) that Scribe must render under `F-NOM-COLD-OUTREACH-DRAFT` discipline. Under Split-Context Hybrid posture, Scribe's scaffold composition still routes cloud-frontier on RFA + section structure only (v7.0.10 §2 unchanged); the per-funder substance read from the DB is local-only. **Same-prompt-with/without behavior change:** under v0.1, Scribe receives a Scout-scratch funder summary as part of the prompt; under v0.2, Scribe receives a structured funder-profile read from the DB with provenance fields. The Scribe prompt template changes to consume the structured shape; the *change is observable* in Scribe's output (citation strings now reference DB entry IDs rather than Scout-cycle IDs).
- **Judge.** Reads the funder's rubric and CLC underwriting logic from the workspace-curated DB (§2.2(a)). Under v0.1, Judge had no structured CLC underwriting logic to read; under v0.2, Judge's cross-check against related rubrics from the library uses the workspace DB's CLC-tagged rubric set. **Same-prompt-with/without behavior change:** Judge's rubric cross-check changes from "Judge's prior-cycle memory" to "Judge's structured CLC rubric library read"; the change is observable in Judge's scoring rationale (rationales now cite the CLC rubric library entry).
- **Red Team.** Reads the funder's red-team probes from the workspace DB (§2.2(a)). Under v0.1, Red Team had no structured probe library; under v0.2, Red Team's adversarial challenge reads the workspace DB's per-funder probe set. Cross-family rigor with Judge and Scribe is preserved (v7 §A11 + v7.0.7 §4 unchanged).
- **Logician.** Consumes the F-SCOUT-* family (§A registrations) + F-NOM-* family (§2.3) + F-FUNDER-DB-CROSS-ORG-LEAK as PRE/POST gates on Scout v0.2 outputs. **Same-prompt-with/without behavior change:** Logician's gate roster gains five new top-level F-SCOUT-* + three new F-NOM-* + one new F-FUNDER-DB-* entries; the META-gate `F-CLASS-COVERAGE-INCOMPLETE` does NOT include F-SCOUT-* (per OQ-6-style isolation precedent and §16 v1's F-PACKET-* exclusion). The change is observable in Logician's audit trail (new gate codes appear in cycle outputs).

### §3.2 artifact_must_not_contain

Hard structural prohibitions on every ScoutReflection artifact and every Funder-Intelligence-Database write at v0.1 and v0.2:

- **No synthetic funders.** A funder name in a ScoutReflection hypothesis OR a Funder Intelligence Database entry MUST trace to an operator-confirmed substrate (workspace-curated DB, per-applicant DB after operator promotion, KFR-resident relationship fact, or a verifiable external authority — Grants.gov, SAM.gov, USASpending, foundation 990-PF / Form 990, IRS GuideStar / Candid, or operator-confirmed RSS source). Fabricated funder names (LLM-hallucinated, name-rhymes-with-real-funder, etc.) fail-close at F-SCOUT-HYPOTHESIS-FABRICATED.
- **No cross-applicant leakage at v0.1 and v0.2.** Any field whose value would expose another applicant's vault data, network, KFR fact, or Scout reflection MUST NOT appear in this applicant's ScoutReflection or Funder Intelligence Database write. Cross-applicant aggregation is DORMANT until Stage 2+ consent tier engages. F-SCOUT-HYPOTHESIS-CROSS-APPLICANT-LEAK + F-FUNDER-DB-CROSS-ORG-LEAK + F-NOM-NETWORK-LEAK structurally prevent.

### §3.3 strength_test

Three calibration questions this SPEC must answer cleanly:

(a) **What does a daemon cycle output differently than a one-shot cycle?** A daemon cycle output's ScoutReflection carries `cycle_runtime_mode: daemon` provenance, a non-null `prior_reflection_id` field (linking to the prior daemon-cycle reflection that fed its hypothesis-generation primitive), and a `search_vector_deltas` field that diffs *against the prior reflection* rather than against the cold-start baseline. A one-shot cycle output's ScoutReflection carries `cycle_runtime_mode: one_shot`, a `prior_reflection_id: null` field (no prior reflection feeding), and a `search_vector_deltas` field that diffs *against the operator's last-confirmed pipeline-state* rather than against a prior daemon-cycle. Both shapes use the same Pydantic schema; the provenance fields are the differentiators. *This is the answer that downstream Archivist and operator-facing surfaces use to distinguish the two modes.*

(b) **What does the hypothesis-generation primitive add beyond keyword search?** Four things: (i) graph-walk on funder-adjacent funders surfaces *workspace-curated structural neighbors* that pure keyword search cannot reach (USDA-RD-CFP → USDA-RD-RBDG / USDA-RD-RCDG / USDA-RD-B&I lateral routing per Scout heuristics §2.2); (ii) near-miss vocabulary surfaces *terms the applicant's current Search Vocabulary lacks* that program pages adjacent to scored-just-below candidates carry (e.g., a "value-added producer" candidate that scored 65/100 because the program page used "agricultural commodity producer" — surfaces the synonym for operator review); (iii) RSS / newsletter delta surfaces *time-axis change* (a recurring program's renamed sub-track, a new program announcement from a previously-subscribed funder) that one-shot keyword search would not detect; (iv) cross-applicant patterns at Stage 2+ surface *fleet-level patterns* that no single applicant's vault could see. The DORMANT v0.1+v0.2 binding for (iv) preserves the design surface without engaging the cross-applicant data path.

(c) **What changes if the daemon loop owner flips from Scout to Archivist?** Under Scout-owns-loop (the §9 recommendation), Scout's daemon code carries the cadence-scheduler call into `mcp__scheduled-tasks__*` and the per-cycle entry point. Under Archivist-owns-loop (the v0.3 migration target), Archivist's §15 Reflection sub-mode owns the cadence-scheduler call and *invokes Scout* per cycle as a sub-operation. The Scout API surface (what callers pass into Scout) is unchanged in either case; the daemon loop entry point moves between seats. This is the migration path documented at §9 — minimal API change at v0.3.

## §4 §B Canonical yaml (FID gold-standard Codex-shape)

The structured runtime contract for Scout v0.2. Following the §B Codex-shape pattern from `pipeline/funder_intelligence/pillar_1_charters/USDA-RD-CFP-FY26_charter_v0_DRAFT.md` (gold-standard) plus the FID Pass-1 gate-taxonomy v1 (`pipeline/funder_intelligence/_validators/gate_taxonomy_consistency.py`).

```yaml
artifact_id: SCOUT-V0.2-SUPERSCOUT
artifact_family: seat_spec
version: v0.2-DRAFT-001
lifecycle: draft
validation_status: pre_audit_2
runtime_load_status: do_not_load_as_signed_logic
operator_label: scout_v0_2_superscout_draft

one_sentence_job: |
  Maintain a continuously-fresh, database-first opportunity discovery surface
  per applicant; emit typed ScoutReflection artifacts that drive self-directed
  search-vector expansion across grant cycles; respect v7.0.10 routing posture
  per call; enforce Law-3 isolation structurally; never fabricate.

runtime_mode_duality:
  modes:
    - ONE_SHOT
    - DAEMON
  one_shot:
    invocation: operator_explicit_cli
    cli_surface: tilth scout one-shot --org <slug>
    return_shape: radar_json_v0_1_plus_scout_reflection_id
    cycle_budget_inherits_from: per_org_daemon_budget_config  # mirrors daemon budget enforcement
  daemon:
    invocation: scheduled_tasks_mcp
    scheduled_tasks_mcp_pattern: mcp__scheduled-tasks__create_scheduled_task
    cadence_config_location: orgs/<slug>/vault/scout/daemon_config.yaml
    cadence_config_owner: operator
    cadence_signature: ed25519_operator_signed
    cycle_entry_point: pipeline.orchestrator.seats.scout.daemon_cycle  # at v0.2; flips to pipeline.orchestrator.seats.archivist.reflection_submode.invoke_scout at v0.3 per §9
    rate_limit_enforcement: per_channel_token_bucket
    rate_limit_config_location: vault_shared/scout/rate_limits.yaml
    rate_limit_publisher_signing: ed25519_publisher_signed_like_v7_0_7_section_6_1
  query_pipeline_cache_contract:
    operator_query_surface: tilth scout pipeline-state --org <slug>
    cache_location: orgs/<slug>/vault/scout/pipeline_state.yaml
    cache_canonical_json_signing: per_v7_0_4_M1_section_2
    cache_returns_synchronously: true
    cache_returns_synchronously_rationale: "Operator query MUST NOT block on a scan; scan happens in daemon background"
    cache_freshness_fields:
      - last_refreshed_utc
      - next_scheduled_refresh_utc
      - cycle_runtime_mode_of_last_refresh

scout_reflection_artifact:
  schema_module: pipeline/vault/sub_kinds/scout_reflections.py  # NOT REGISTERED in SUB_KIND_REGISTRY at v0.2 DRAFT; registration at v0.2 first wave compound LOCK
  schema_version_at_draft: 1.0.0-scout-reflection
  pydantic_shape:
    dataclass_frozen: true
    kw_only: true
    canonical_json_codec: true
    sha3_512_hash: true
    ed25519_signature_required: true  # producer-seat signed at emit
    post_init_invariants_count: 22  # length / grammar / type / closed-set / signature-shape; populated at LOCK
  fields:
    cycle_id: str                                                  # opaque caller-minted UUID
    org_slug: str                                                  # Law-3 binding
    schema_version: str                                            # "1.0.0-scout-reflection" at v0.2
    classification_register_version: str                           # SHA3-512 hash of operator-signed classification register at cycle start
    cycle_runtime_mode: enum                                       # {one_shot, daemon}
    posture: enum                                                  # {frontier_eligible, split_context_hybrid, local_only_sovereign}
    prior_reflection_id: str | None                                # null when one_shot OR daemon-cold-start
    emitted_at_utc: str                                            # iso8601 'Z'
    emitted_by_seat: str                                           # closed registry set; v0.2 = {"scout.one_shot", "scout.daemon"}
    cycle_close_marker_span_id: str                                # Logfire span ID of the cycle-close marker (per §8)
    queries_run: tuple                                             # tuple[QueryAttempt, ...]
    hits: tuple                                                    # tuple[HitRecord, ...]
    matches_scored: tuple                                          # tuple[ScoredMatch, ...]
    near_misses: tuple                                             # tuple[NearMiss, ...]
    novel_hypotheses: tuple                                        # tuple[Hypothesis, ...]
    search_vector_deltas: tuple                                    # tuple[VectorDelta, ...]
    budget_spent: BudgetSpent                                      # see daemon_sovereignty_and_cost block
    logfire_span_root_id: str                                      # per §8
    cycle_grounding_signal_classes: frozenset                      # ≥1 of {workspace_db_read, per_applicant_db_read, kfr_read, channel_a_to_g_response, logfire_observation}

hypothesis_generation_primitive:
  sources:
    - source_id: graph_walk
      source_substrate: vault_shared/funder_intelligence/  # workspace-curated layer (operator-curated; publisher-Ed25519-signed)
      determinism: deterministic_python_graph_walk
      operator_review_required_for_promotion_to_search_vocabulary: true
      gate_refs:
        - F-SCOUT-HYPOTHESIS-FABRICATED
    - source_id: near_miss_vocabulary
      source_substrate: orgs/<slug>/vault/scout/reflections/<prior_cycle_id>.json  # prior ScoutReflection.near_misses
      determinism: deterministic_python_term_extraction
      operator_review_required_for_promotion_to_search_vocabulary: true
      gate_refs:
        - F-SCOUT-HYPOTHESIS-FABRICATED
    - source_id: rss_delta
      source_substrate: vault_shared/scout/rss_baseline.yaml  # workspace-curated baseline + per-applicant subscription set
      determinism: deterministic_python_delta_detection
      operator_review_required_for_promotion_to_search_vocabulary: true
      gate_refs:
        - F-SCOUT-HYPOTHESIS-FABRICATED
    - source_id: cross_applicant
      source_substrate: sovereign_node_consent_tier_layer  # OUT-OF-SCOPE at v0.1 + v0.2; DORMANT
      determinism: not_implemented_until_stage_2
      operator_review_required_for_promotion_to_search_vocabulary: true
      dormant_at: [v0.1, v0.2]
      gate_refs:
        - F-SCOUT-HYPOTHESIS-FABRICATED
        - F-SCOUT-HYPOTHESIS-CROSS-APPLICANT-LEAK   # LIVE fail-closed gate until Stage-2+ consent tier engages

daemon_sovereignty_and_cost:
  posture_per_call:
    posture_source: orgs/<slug>/vault/classification/register.yaml
    posture_pin_at_cycle_start: true
    posture_mid_cycle_change_prohibited: true
    posture_drift_gate: F-SCOUT-DAEMON-POSTURE-DRIFT
  classification_of_newly_discovered_programs:
    default: confidential
    gate_ref: F-CLASS-NEW-FACT-UNCLASSIFIED
    operator_confirmation_surface: tilth scout pipeline-state --org <slug>  # operator confirms classification at next pipeline-state review
  per_cycle_budget_config:
    config_location: orgs/<slug>/vault/scout/daemon_config.yaml
    config_signing: ed25519_operator_signed
    axes:
      - axis_id: daemon_dollar_budget_per_cycle_cents
        type: int_micro_cents              # Decimal mandate per A12; int micro-cents-or-cents (NO FLOAT)
        gate_ref: F-SCOUT-DAEMON-BUDGET-EXCEEDED
      - axis_id: daemon_token_budget_per_cycle
        type: int
        gate_ref: F-SCOUT-DAEMON-BUDGET-EXCEEDED
      - axis_id: daemon_api_call_budget_per_cycle
        type: int
        sub_axes:
          - grants_gov
          - sam_gov
          - usaspending
          - cloud_llm_total
        gate_ref: F-SCOUT-DAEMON-BUDGET-EXCEEDED
  budget_exceeded_behavior:
    in_flight_cycle_action: freeze_at_gate_persist_partial_state_alert_operator
    partial_state_path: orgs/<slug>/vault/scout/partial_cycles/<cycle_id>.yaml
    operator_alert_surface: daemon_cycle_digest
  logfire_span_emission: per_cycle_root_plus_per_channel_children  # §8

daemon_loop_owner: scout                                            # SEE §9 LOCK-BLOCKER DECISION
migration_target_v0_3: archivist_owns_loop                         # §15 Archivist Reflection sub-mode absorbs scheduling responsibility at v0.3 when §15 v2.x matures
operator_decidable: true                                            # OPERATOR CONFIRMS AT LOCK CEREMONY
operator_decidable_rationale: |
  Two architecturally-defensible options. Scout-owns-loop ships faster + Scout
  already has a clean discovery contract. Archivist-owns-loop is structurally
  cleaner long-run (Archivist is the between-cycle curator). v0.3 migration
  is documented at §9. Operator confirms at LOCK ceremony.

cross_family_import_ban:
  reference_section: §7
  banned_imports:
    - "from pipeline.vault.sub_kinds.reflection_packets import *"   # §16 ReflectionPacket family — sibling-not-nested
    - "from pipeline.orchestrator.seats.archivist import *"         # §15 Archivist — Scout v0.2 does not import Archivist
    - "from pipeline.orchestrator.seats.scribe import *"            # Scribe — Scout v0.2 does not import Scribe
    - "from pipeline.orchestrator.seats.judge import *"             # Judge — Scout v0.2 does not import Judge
    - "from pipeline.orchestrator.seats.red_team import *"          # Red Team — Scout v0.2 does not import Red Team
  ast_lint_module: pipeline/linting/r_scout_no_cross_family_import.py  # to author at LOCK
```

## §5 New F-* gate families

Per Pass-1 gate-taxonomy v1 (allowed tuples enforced by `pipeline/funder_intelligence/_validators/gate_taxonomy_consistency.py`):

```yaml
eligibility_gates:
  - gate_id: F-SCOUT-HYPOTHESIS-FABRICATED
    gate_type: hard_eligibility_gate
    predicate: "Every hypothesis in ScoutReflection.novel_hypotheses MUST carry a non-null source field whose value names an operator-curated substrate (workspace DB, per-applicant DB, KFR fact) OR a deterministic-Python source (graph_walk, near_miss_vocabulary, rss_delta). Hypotheses with null source OR source referencing a non-existent / non-operator-confirmed substrate fail-close."
    machine_check:
      field: scout_reflection.novel_hypotheses[*].source
      operator: in
      threshold: [graph_walk, near_miss_vocabulary, rss_delta, cross_applicant]
      additional_check: "source MUST resolve to operator-confirmed substrate read OR deterministic-Python execution trace"
    on_fail: REJECT_NO_DRAFT
    severity: P0
    source_required: true
    corpus_ref: "this SPEC §2.11 + §3.2 + §4 hypothesis_generation_primitive"
    confidence:
      level: high
      reason: "Hypothesis fabrication is the load-bearing Law-5 + Law-1 violation surface for Scout v0.2; structural enforcement at gate time prevents LLM-hallucinated funder names from reaching the Funder Intelligence Database."
      promotion_requirement: "predicate body realized at §4 v2.x.y paired Logician amendment at LOCK"
    v0_2_status: spec_only_NotImplementedError

  - gate_id: F-SCOUT-HYPOTHESIS-CROSS-APPLICANT-LEAK
    gate_type: hard_eligibility_gate
    predicate: "ScoutReflection.novel_hypotheses[*].source != 'cross_applicant' AT v0.1 + v0.2. Stage-2+ consent tier engagement is the only operator-signed pathway to unblock; until that signature lands, any hypothesis with source 'cross_applicant' fail-closes regardless of substrate provenance."
    machine_check:
      field: scout_reflection.novel_hypotheses[*].source
      operator: not_equal
      threshold: cross_applicant
    on_fail: REJECT_NO_DRAFT
    severity: P0
    source_required: true
    corpus_ref: "this SPEC §2.11 (d) + §3.2 + CLAUDE.md Sovereign Node Stage-2+ consent tiers"
    confidence:
      level: high
      reason: "Cross-applicant leakage is the load-bearing Law-3 violation surface for v0.2 hypothesis generation; DORMANT-binding mirrors §16 OQ-2 (a) and v7.0.7 §1.4 DORMANT-BINDING pattern."
      promotion_requirement: "predicate body realized at §4 v2.x.y paired Logician amendment at LOCK; flips to operator-signed-consent-tier-conditional at Stage-2+ deployment"
    v0_2_status: spec_only_NotImplementedError_with_LIVE_dormant_binding

  - gate_id: F-SCOUT-DAEMON-BUDGET-EXCEEDED
    gate_type: verify_required_gate
    predicate: "Daemon cycle in-flight resource consumption MUST stay ≤ operator-signed budget across all three axes (dollar_cents, token, api_call). Any axis breach fail-closes the in-flight cycle; partial cycle state persists; operator alerted via daemon-cycle digest."
    machine_check:
      field: scout_reflection.budget_spent.<axis>
      operator: less_or_equal
      threshold_source: orgs/<slug>/vault/scout/daemon_config.yaml
    on_fail: HOLD_FOR_OPERATOR_REVIEW
    severity: HIGH
    source_required: true
    corpus_ref: "this SPEC §2.12 + §4 daemon_sovereignty_and_cost"
    confidence:
      level: high
      reason: "Budget overrun on a continuously-running daemon is a structural cost-sovereignty risk; fail-close + alert is the operator-protection surface."
      promotion_requirement: "predicate body realized at §4 v2.x.y paired Logician amendment at LOCK"
    v0_2_status: spec_only_NotImplementedError

  - gate_id: F-SCOUT-DAEMON-POSTURE-DRIFT
    gate_type: hard_eligibility_gate
    predicate: "Daemon cycle posture MUST remain pinned to operator-signed value at cycle start through cycle close. Per-call routing decisions MUST match cycle-start posture. Mid-cycle drift fail-closes."
    machine_check:
      field: scout_reflection.posture
      operator: equals_throughout_cycle
      threshold_source: orgs/<slug>/vault/classification/register.yaml.posture_at_cycle_start
    on_fail: REJECT_NO_DRAFT
    severity: P0
    source_required: true
    corpus_ref: "this SPEC §2.12 + architecture v7.0.10 §5 (F-CLASS-POSTURE-MID-CYCLE-CHANGE precedent)"
    confidence:
      level: high
      reason: "Posture drift on a daemon cycle is a structural Law-3 + v7.0.10 routing-discipline violation; mirrors F-CLASS-POSTURE-MID-CYCLE-CHANGE precedent."
      promotion_requirement: "predicate body realized at §4 v2.x.y paired Logician amendment at LOCK"
    v0_2_status: spec_only_NotImplementedError

  - gate_id: F-CLASS-NEW-FACT-UNCLASSIFIED
    gate_type: verify_required_gate
    predicate: "Newly-discovered program data ingested via Scout DAEMON OR ONE_SHOT cycle defaults to classification = 'confidential' until operator confirms classification via the next pipeline-state review. Until confirmed, the data does NOT route cloud regardless of posture."
    machine_check:
      field: per_applicant_funder_db_entry.classification
      operator: equals
      threshold: confidential
      until_operator_action: tilth scout classify --entry <entry_id> --classification <public|shareable|confidential|operator_flagged>
    on_fail: HOLD_FOR_OPERATOR_REVIEW
    severity: VERIFY_REQUIRED
    source_required: true
    corpus_ref: "v7.0.7 §1.4 classification register + v7.0.10 §1 three-posture routing"
    confidence:
      level: high
      reason: "Default-confidential on new findings is the load-bearing Law-3 + posture-routing protection; operator confirmation is the only path to cloud-routable status."
      promotion_requirement: "Already LIVE at v7.0.7 §5.1 F-CLASS-* family; this gate REGISTERS the Scout-side application of the existing F-CLASS-NEW-FACT-UNCLASSIFIED primitive (not a new top-level F-* code; it is the Scout-side hook into the v7.0.7 family)."
    v0_2_status: LIVE_via_v7_0_7_family_with_scout_hook
```

The three F-NOM-* gates from §2.3 (`F-NOM-FABRICATED-RELATIONSHIP`, `F-NOM-COLD-OUTREACH-DRAFT`, `F-NOM-NETWORK-LEAK`) are registered in the parent §2.3 enumeration; their full Codex-shape registrations land at the same LOCK ceremony.

The F-FUNDER-DB-CROSS-ORG-LEAK gate from §2.2 is a Law-3 structural gate that fires on any per-applicant DB write whose path slug differs from the entry's `org_slug` field; full predicate registration lands at the LOCK ceremony Logician amendment.

The F-FUNDER-DB-BYPASSED gate from §2.1 is a v0.2-specific gate that fires on any Scout cycle whose channel-A-through-F invocations did not first scan the two-layer DB; full predicate registration lands at the LOCK ceremony Logician amendment.

**META-gate scope exclusion.** Per OQ-6-style isolation precedent (and §16 v1's F-PACKET-* exclusion from F-CLASS-COVERAGE-INCOMPLETE), the new F-SCOUT-* + F-NOM-* + F-FUNDER-DB-* families are EXCLUDED from `F-CLASS-COVERAGE-INCOMPLETE` META gate scope. A separate `F-SCOUT-COVERAGE-INCOMPLETE` META-gate is registered at LOCK ceremony paired §4 v2.x.y amendment (signature only at this DRAFT; predicate body realized at LOCK).

## §6 Logfire span + funder-API rate-limit specs (for daemon auditability)

### §6.1 Logfire span structure

Every Scout cycle (DAEMON or ONE_SHOT) emits a Logfire span tree rooted at `logfire_span_root_id` (per §4 ScoutReflection schema). The root span has the shape:

- `scout.cycle.{cycle_runtime_mode}` — root span; attributes include `org_slug`, `cycle_id`, `posture`, `cadence_config_hash`, `prior_reflection_id`.
- Children:
  - `scout.discover.channel.{a|b|c|d|e|f|g}` — one child per channel invoked, with attributes `terms_queried`, `hits_count`, `rate_limit_near_breach: bool`, `api_call_count`, `tokens_spent`, `dollar_spent_cents`.
  - `scout.verify` — verify-phase span, with attributes `candidates_verified`, `verified_fit`, `verified_not_fit`, `unverified`, `verification_failed`.
  - `scout.review` — operator-gate handoff span (no LLM call; just the audit-trail marker).
  - `scout.reflection.emit` — ScoutReflection emit span, with attributes `reflection_id`, `signature_status`.
  - `scout.budget.gate_check` — budget enforcement span, fires per gate-check, with attributes `axis`, `consumed`, `threshold`, `pass: bool`.

Logfire trace IDs are persisted in the ScoutReflection.queries_run + hits + matches_scored + budget_spent fields for cross-reference. Provenance gate `F-SCOUT-SPAN-PROVENANCE-MISSING` (signature-only at DRAFT; cross-references `F-WPFA-SPAN-PROVENANCE-MISSING` and `F-PACKET-SPAN-PROVENANCE-MISSING` per the sibling pattern §16 v1 §16.2 / §17 v1 §17.6 — naming reconciliation pending at LOCK).

### §6.2 Funder-API rate-limit specs

Per §2.12 rate-limit enforcement. Per-channel token bucket configuration at `vault_shared/scout/rate_limits.yaml`:

- **Grants.gov search2 / fetchOpportunity** — operator-tunable; default `requests_per_minute: 30, requests_per_day: 5000` (conservative under published Grants.gov terms-of-use; rates checked at LOCK ceremony against current Grants.gov API documentation).
- **SAM.gov entity-search** — operator-tunable; default `requests_per_minute: 10, requests_per_day: 1000` (conservative under published SAM.gov rate guidance).
- **USASpending** — operator-tunable; default `requests_per_minute: 60, requests_per_day: 10000` (USASpending's published rates are generous; conservative defaults preserve burst budget).
- **Cloud-LLM** (Anthropic / Google / Groq / OpenAI per `/router.yaml` provider tier) — operator-tunable; default `tokens_per_minute: 100000, dollar_per_cycle_cents: 5000` (operator-tunable per applicant per posture).

Near-breach signal (90% of any axis threshold within a 1-minute window) emits a Logfire span attribute `rate_limit_near_breach: true` and triggers a daemon-cycle backoff (not retry-storm). Hard breach (axis threshold exceeded) fails the channel-call with explicit error; cycle does NOT crash, but the channel-call returns a `channel_unavailable` hit with the breach noted in the ScoutReflection.queries_run record.

Rate-limit config is **publisher-Ed25519-signed** (mirrors v7.0.7 §6.1 router-template + §17 v1 Coefficient Registry trust mechanism); white-glove pins the publisher public key at onboarding; runtime verification on every rate-limit-config load.

## §7 Cross-family-import ban to §16 ReflectionPacket

`ScoutReflection` and `ReflectionPacket` (§16 v1) are **sibling-not-nested artifacts** with a shared substrate (the per-cycle Logfire span tree) but otherwise zero overlap:

| Dimension | ScoutReflection | ReflectionPacket |
|---|---|---|
| **Producer** | Scout v0.2 (this SPEC) | §15 Archivist Reflection sub-mode (v7.0.9 / §4 v2.x.2) |
| **Consumer** | Scout-Daemon next-cycle hypothesis-generation primitive | §15 Archivist learning loop |
| **Emit timing** | Cycle close (every DAEMON cycle + every ONE_SHOT cycle) | Cycle close PENDING + decision-observed BACKFILL |
| **Schema** | This SPEC §B (22 invariants TBD) | §16 v1 §16.2 (19 invariants LIVE at LOCK) |
| **F-* family** | `F-SCOUT-REFLECTION-*` + `F-SCOUT-*` | `F-PACKET-*` |
| **Cross-org write?** | No (Law-3 structural; F-FUNDER-DB-CROSS-ORG-LEAK + F-SCOUT-HYPOTHESIS-CROSS-APPLICANT-LEAK) | No (Law-3 structural; F-PACKET-* family) |
| **Shared substrate** | Logfire span tree | Logfire span tree |
| **Cross-reference at AST?** | NONE (cross-family-import ban; AST-lint at LOCK) | NONE (cross-family-import ban; AST-lint at §16 v1) |

**The cross-family-import ban is structural.** Implementation discipline:

1. **No import from §16 in Scout v0.2 code.** `pipeline/orchestrator/seats/scout/` MUST NOT import from `pipeline/vault/sub_kinds/reflection_packets` or `pipeline/orchestrator/seats/archivist/`. AST-lint module at `pipeline/linting/r_scout_no_cross_family_import.py` (to author at LOCK ceremony) enforces.
2. **No shared Python type aliases.** Type aliases that would couple Scout's runtime to ReflectionPacket's schema (e.g., a shared `PatternObservation` type) are prohibited. Each family carries its own type definitions.
3. **One cross-reference at the F-* family layer, at most.** Per the §16 v1 / §17 v1 sibling pattern, a single F-* code MAY cross-reference (e.g., `F-SCOUT-SPAN-PROVENANCE-MISSING` ↔ `F-WPFA-SPAN-PROVENANCE-MISSING` ↔ `F-PACKET-SPAN-PROVENANCE-MISSING` per the §16 v1 §16.2 sibling pattern). At MOST one such cross-reference; the naming reconciliation lands at LOCK ceremony per the §16 v1 / §17 v1 / Path-B precedent.

**Shared substrate is fine; shared output / consumer / schema / F-* code is prohibited.**

## §8 §1 strength-test answers (same-prompt-with/without proof for ≥2 downstream seats)

Restating §3.3 with explicit downstream-seat behavior-change proofs.

### §8.1 Scribe — same-prompt-with/without behavior change

Under Scout v0.1, Scribe receives a Scout-scratch funder summary as part of the cycle-start prompt. The summary is a multi-paragraph free-text dump produced by Scout's LLM call.

Under Scout v0.2, Scribe receives a structured funder-profile read from the two-layer Funder Intelligence Database. The profile is a typed Pydantic shape with provenance fields (`source_substrate_path`, `source_entry_id`, `audit_chain`, `classification`).

**The change is observable in Scribe's output.** Under v0.1, Scribe's citation strings reference Scout-cycle IDs (`per Scout cycle 2026-05-19_1734`). Under v0.2, Scribe's citation strings reference DB entry IDs (`per Funder Intel DB entry usda-rd-cfp-fy26 audit_chain head_hash 0x4f3a...`). The behavior change is detectable at output-string-comparison time.

**Why this matters for downstream review.** Judge cross-checks rubrics against the workspace-curated rubric library (§8.2). Red Team probes against the workspace-curated probe library. Logician validates that every Scribe citation traces to an audit-chain entry. The downstream chain depends on Scout v0.2 emitting structured DB-grounded funder profiles rather than free-text scratch; same-prompt-with-v0.1-input produces v0.1 behavior; same-prompt-with-v0.2-input produces v0.2 behavior. The Scribe code path is unchanged; the *input shape* changes; the *output citation pattern* changes.

### §8.2 Logician — same-prompt-with/without behavior change

Under Scout v0.1, Logician runs the v0.1 PRE/POST gate roster (F-LAW-1 through F-LAW-5 + F-KFR-* + F-CLASS-* + F-WPFA-* + F-PACKET-* + F-ARCHIVIST-* + F-REFLECTION-*).

Under Scout v0.2, Logician runs the v0.1 roster PLUS the new F-SCOUT-* family (5 codes at this SPEC: `F-SCOUT-HYPOTHESIS-FABRICATED`, `F-SCOUT-HYPOTHESIS-CROSS-APPLICANT-LEAK`, `F-SCOUT-DAEMON-BUDGET-EXCEEDED`, `F-SCOUT-DAEMON-POSTURE-DRIFT`, plus the Scout-side hook into `F-CLASS-NEW-FACT-UNCLASSIFIED`) + F-NOM-* (3 codes: `F-NOM-FABRICATED-RELATIONSHIP`, `F-NOM-COLD-OUTREACH-DRAFT`, `F-NOM-NETWORK-LEAK`) + F-FUNDER-DB-* (2 codes: `F-FUNDER-DB-CROSS-ORG-LEAK`, `F-FUNDER-DB-BYPASSED`) + the META-gate `F-SCOUT-COVERAGE-INCOMPLETE`.

**The change is observable in Logician's audit trail.** Under v0.1, Logician's cycle output enumerates ~30 gate-check rows. Under v0.2, Logician's cycle output enumerates ~30 + 11 = ~41 gate-check rows. The 11 new gate codes appear in audit trail JSON with their typed `gate_type`, `severity`, `fail_action` per gate-taxonomy v1. The behavior change is detectable at audit-trail-row-count time.

**Why this matters for downstream review.** Cross-family Thesis dispatch at LOCK ceremony (Editor + Judge + Red Team via openclaw bridge) reads Logician's audit trail as a structural cross-reference. The new gates' presence/absence in the audit trail is a binary check at audit time — every Scout v0.2 cycle emits all 11 new gate rows (PASS or FAIL); zero new rows means Logician wasn't actually wired to the v0.2 family.

## §9 LOCK-blocker decision: daemon loop owner (operator_decidable: true)

The handoff identifies one explicit open architectural question requiring operator decision before LOCK:

> **Does Scout v0.2 own the daemon loop directly, or does Archivist's Reflection sub-mode (v7.0.9 hook) own the loop and invoke Scout?**

### §9.1 Recommendation (baked in; subject to operator final confirm)

**Scout-owns-loop in v0.2.**

### §9.2 Rationale

Three reasons:

(a) **Ship velocity.** The v0.2 first wave is on the runway; Scout v0.2 spec needs to LOCK without waiting on §15 v2.x Archivist Reflection sub-mode SPEC. Per the §15 v0.2 disposition (`section_15_archivist.md` frontmatter): "**At v0.2 (this LOCK), the operator is responsible for: manually invoking `tilth archivist weekly --org <slug>` and `tilth archivist quarterly` cadences (no scheduled-task trigger; operator decides when).**" Archivist v0.2 does NOT yet schedule itself; asking it to schedule Scout would require Archivist v2.x SPEC LOCK ahead of Scout v0.2 LOCK, which inverts the ship order on the runway. Path of least architectural debt: Scout v0.2 ships its own scheduler, Archivist v2.x absorbs scheduling responsibility at v0.3.

(b) **Scout has a clean discovery contract; Archivist does not yet have a clean scheduling contract.** Scout v0.1 already has a deterministic radar-emit shape (`radar.json`); Scout v0.2 extends it with `ScoutReflection`. Archivist v0.2 is SPEC-only with operator-driven cadence; the scheduled-task hook lands at v1.x amendment. Putting Scout's scheduling responsibility inside Archivist v0.2 would force Archivist v0.2's scope to expand mid-runway; ship-discipline says keep the scope at SPEC-only for Archivist v0.2 and let Scout v0.2 carry its own daemon loop.

(c) **Migration path is cheap.** At v0.3 when §15 v2.x Archivist Reflection sub-mode LOCKs with scheduled-task discipline, Scout's daemon-loop entry point becomes an "invoke Scout" call from Archivist's loop. The Scout API surface (what callers pass into Scout) is unchanged. The change is one line in `daemon_loop_owner: scout` flipping to `daemon_loop_owner: archivist`, plus a re-wire of `mcp__scheduled-tasks__create_scheduled_task` from Scout's invocation to Archivist's. The operator decision at v0.3 is a small structural flip, not a refactor.

### §9.3 Migration path (documented for v0.3)

When §15 v2.x Archivist Reflection sub-mode LOCKs with scheduled-task discipline (operator-signed migration trigger per v7.0.4 §9.1 J-06 closure pattern + v7.0.5 §6 curation-slot binding):

1. **Archivist absorbs scheduling.** The daemon-loop entry point at `pipeline/orchestrator/seats/scout/daemon_cycle.py` becomes a callable function that Archivist's Reflection sub-mode invokes per scheduled tick (instead of `mcp__scheduled-tasks__*` invoking Scout directly).
2. **Scout's per-cycle entry point is unchanged.** The Scout API surface (`scout.daemon.cycle(org_slug: str, cycle_id: str, posture: enum, ...) -> ScoutReflection`) is preserved byte-for-byte; what changes is *who calls it*.
3. **`daemon_loop_owner: scout` → `daemon_loop_owner: archivist`.** Single-line change in `orgs/<slug>/vault/scout/daemon_config.yaml` (operator-signed update).
4. **`migration_target_v0_3` field deprecates.** At v0.3 LOCK, the field is removed (transitive — was a marker pointing to this migration).
5. **No Scout-side code refactor required.** AST-lint cross-family-import ban (§7) preserved unchanged — Archivist still does not import from Scout; Scout still does not import from Archivist; the scheduling-vs-invocation boundary is a runtime-orchestration concern, not an import-graph concern.

### §9.4 Operator override

`operator_decidable: true` is registered in the SPEC frontmatter and in §B canonical yaml. The LOCK ceremony confirms before sealing. If the operator overrides to Archivist-owns-loop at v0.2 LOCK, the §15 v2.x SPEC LOCK must precede Scout v0.2 LOCK; the runway re-orders accordingly. If the operator confirms Scout-owns-loop, the migration path lands at v0.3 as documented.

## §10 Out-of-scope (explicit non-goals at v0.2 DRAFT)

- **Implementation.** Scout v0.2 code does not land at this SPEC DRAFT. The existing `pipeline/orchestrator/seats/scout.py` (v0.1) continues to serve all live cycles until v0.2 LOCK + paired Logician amendment + paired §0.5 interface-index amendment land.
- **SUB_KIND_REGISTRY registration.** ScoutReflection schema module at `pipeline/vault/sub_kinds/scout_reflections.py` is NOT registered in SUB_KIND_REGISTRY at this SPEC DRAFT. Registration lands at v0.2 first wave compound LOCK paired with §15 v2.x Archivist Reflection sub-mode SPEC.
- **F-SCOUT-* + F-NOM-* + F-FUNDER-DB-* predicate bodies.** All new gate predicates raise NotImplementedError at this SPEC DRAFT. Cedar/Python realization lands at LOCK ceremony paired §4 v2.x.y amendment.
- **Stage-2+ cross-applicant consent tier engagement.** The DORMANT field (`source: cross_applicant`) is reserved at the schema layer; the LIVE gate (`F-SCOUT-HYPOTHESIS-CROSS-APPLICANT-LEAK`) fail-closes any path that would engage it at v0.1 + v0.2. Stage-2+ engagement requires the Sovereign Node commons LLC to exist, operator-signed consent tier registration, and a separate architecture amendment — none of which fall in v0.1 or v0.2 scope.
- **Scribe / Judge / Red Team / Logician code changes.** Scout v0.2 ships its own seat code; downstream seats consume Scout v0.2 outputs per the §3.1 runtime_consumer block but do NOT receive code changes as part of this SPEC. Their behavior change is *input-shape-driven*, not code-driven.
- **No applicant-organization names anywhere in Scout v0.2 architecture, schema, prompt, knowledge pack, scoring weight, or config.** Per Law-3 structural binding inherited from the handoff Constraints section.

## §11 Open questions for operator (surfaced for LOCK ceremony)

1. **Daemon loop owner at v0.2** (per §9). Recommendation: Scout-owns-loop. Operator confirms or overrides.
2. **Per-applicant cadence defaults.** What is the default daemon-cycle cadence at white-glove? Proposed: `weekly` per applicant; operator-tunable per Reporting Rhythm (CIC card field per §2.6). Operator confirms or sets a different default.
3. **RSS / newsletter baseline source.** Channel-E RSS baseline lives at `vault_shared/scout/rss_baseline.yaml` per §4 sources block; per-applicant subscription set lives at `orgs/<slug>/vault/scout/rss_subscriptions.yaml`. Operator confirms paths or proposes different layout.
4. **Rate-limit defaults.** §6.2 defaults are conservative. Operator confirms or tunes for the specific live deployment.
5. **F-SCOUT-COVERAGE-INCOMPLETE META-gate scope.** Per §5 exclusion note, F-SCOUT-* + F-NOM-* + F-FUNDER-DB-* are excluded from F-CLASS-COVERAGE-INCOMPLETE. A separate META-gate is proposed. Operator confirms scope (separate META-gate vs absorption into F-CLASS-COVERAGE-INCOMPLETE).
6. **Logfire span naming for cross-reference.** §6.1 proposes `F-SCOUT-SPAN-PROVENANCE-MISSING` as a cross-reference to `F-WPFA-SPAN-PROVENANCE-MISSING` and `F-PACKET-SPAN-PROVENANCE-MISSING`. Operator confirms the cross-reference naming or proposes a Path-B-style separate family naming reconciliation.
7. **Coalition-required handling.** §2.7 surfaces the `coalition_required` flag at operator-attention-trigger level. Operator confirms whether `coalition_participants_known: none` should escalate to operator immediately at daemon-cycle close or wait until pipeline-state review.

## §12 What did NOT make it into the SPEC (and why)

- **Implementation code.** Per §10 out-of-scope and the handoff's "What this is NOT" section; this is a SPEC, not a refactor.
- **Per-channel adapter code paths.** Channel A-G adapter Python interfaces are deferred to LOCK ceremony paired blueprint amendment; this SPEC enumerates the channel taxonomy (§2.8) and rate-limit defaults (§6.2) but does not author adapter code.
- **CIC card field mapping for Scout v0.2.** §2.6 declares the four CIC card primitives Scout reads (Search Vocabulary, Evidence Schema, Language Register, Reporting Rhythm) but does NOT enumerate the specific YAML field paths from `pipeline/cards/_schema/cic_card.schema.json`. Field-path enumeration lands at LOCK ceremony paired §18 v1.x amendment (Card System integration).
- **MatchOutcome full schema.** §2.4 declares the artifact and the feedback loop; full Pydantic schema is sibling to ScoutReflection and lands at LOCK ceremony paired §2 v7.x sub-kind amendment. Held back to keep this DRAFT focused on Scout v0.2's surface; MatchOutcome is consumed by Archivist's quarterly digest, not directly by Scout's daemon loop.
- **F-NOM-* full Codex-shape registrations.** §2.3 declares the three gates and their gate-taxonomy-v1 tuples; full Codex-shape registrations (predicate bodies, machine_check fields, corpus_refs) land at LOCK ceremony paired §4 v2.x.y amendment.
- **F-CIC-CLC-COUPLING-VIOLATION re-registration.** The v7.0.8 gate is referenced (§2.6) but not re-registered; it already lives at v7.0.8 §1 and §4 v2.x. Scout v0.2 inherits it.
- **Cards "Phase A first fixtures" coupling.** v7.0.11 §6.3 resolves Phase A first fixtures as `food_systems` + `operating_capacity` per the revised feedback. Scout v0.2 CIC-aware configuration consumes whatever fixtures are loaded; the fixture-loading-order coupling is v7.0.11's concern, not this SPEC's.

## §13 Cross-references

- Parent handoff: `pipeline/handoffs/scout_v0_2_superscout_exploration_2026-05-19.md`
- Scout v0.1 orchestrator: `pipeline/orchestrator/seats/scout.py`
- Scout cross-charter heuristics: `pipeline/funder_intelligence/_seats/scout/heuristics.md`
- §15 Archivist v1 LOCK: `pipeline/blueprint/v0.1/section_15_archivist.md`
- §16 ReflectionPacket v1 LOCK: `pipeline/blueprint/v0.1/section_16_reflection_packet.md`
- Pass-1 gate-taxonomy v1: `pipeline/funder_intelligence/_validators/gate_taxonomy_consistency.py`
- Architecture v7.0.5 (Funder Intel DB + Scout channel G): `pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md`
- Architecture v7.0.7 (classification routing): `pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md`
- Architecture v7.0.8 (CIC × CLC orthogonality): `pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md`
- Architecture v7.0.9 (Reflection sub-mode hook): `pipeline/architecture/v0.1/architecture_v7_0_9_amendment.md`
- Architecture v7.0.10 (three-posture routing): `pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md`
- Architecture v7.0.11 (Card System DRAFT): `pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md`
- USDA-RD-CFP-FY26 Codex-shape gold-standard: `pipeline/funder_intelligence/pillar_1_charters/USDA-RD-CFP-FY26_charter_v0_DRAFT.md` §B
- Audit #1 thesis findings: `docs/scout_v0_2_audit_1_thesis_2026-05-19.md`
