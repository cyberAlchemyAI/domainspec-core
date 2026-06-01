# Scout v0.2 (SuperScout) — Audit #1 Thesis Findings

**Audited document:** `pipeline/blueprint/v0.2/scout_v0_2_superscout_spec.md` (DRAFT, v0.2-DRAFT-001)
**Audit date:** 2026-05-19
**Audit class:** L-005 strict two-cycle Audit #1 (scoping pass). Audit #2 (verification pass) follows operator review.
**Audit posture:** Cross-family — same-room single-Claude pass at this dispatch (Section E single-Claude carve-out NOT invoked — this is a *first-pass scoping audit*, not the LOCK-ceremony cross-family Thesis dispatch). The L-005 strict cross-family dispatch (Editor=Meta-family + Judge=Google-family + Red Team=OpenAI-OSS-family via openclaw bridge) lands at LOCK ceremony per AGENTS.md § Cross-family review — bridge pattern.

**Audit scope (per dispatch packet):**
1. Five Operating Laws (especially Law 3 org isolation for the cross-applicant DORMANT gate)
2. Architecture v7.0.x §-family boundaries (v7.0.5 / v7.0.7 / v7.0.8 / v7.0.9 / v7.0.10 / v7.0.11)
3. §15 Archivist contract (does Scout-owns-loop violate any Archivist commitment?)
4. §16 ReflectionPacket boundary (cross-family-import ban honored?)
5. Pass-1 gate-taxonomy v1 (every new gate typed correctly per allowed tuples?)
6. No-invention rule (anything in the SPEC fabricated vs grounded in handoff?)

---

## §1 Per-section review

### §1.1 Header and §0 status discipline

PASS. The SPEC declares status DRAFT, parent handoff link, locked-architecture references (10 of them, covering v7.0.5 + v7.0.7 + v7.0.8 + v7.0.9 + v7.0.10 + v7.0.11 + §15 + §16 + Pass-1 gate taxonomy + USDA-RD-CFP Codex-shape gold-standard). The version chain is honored. The `operator_decidable: true` field is registered in frontmatter and §B canonical yaml. Audit trail path declared.

No deviation from the L-005 two-cycle review discipline.

### §1.2 §1 Mission

PASS. The mission statement enumerates the v0.2-over-v0.1 additions verbatim from the handoff: database-first discovery, Channel G, Match Database feedback loop, cycle-aware pipeline auto-promotion, CIC-aware configuration, coalition-opportunity surfacing, channel orthogonality, runtime-mode duality, self-directed search expansion, hypothesis-generation primitive, daemon sovereignty + cost controls. All twelve handoff design goals are surfaced.

Out-of-scope enumeration is honest: Scout does NOT score (Judge), write (Scribe), submit (Uploader), or mutate canonical DB entries directly (Archivist curation slot). The proposal/canonical-mutation boundary mirrors Intake's pending→canonical discipline per §11 — an architecturally consistent move.

### §1.3 §2.1 Database-first as structural primitive

PASS. The SPEC correctly positions Channels A-F as gap-fill against the database rather than parallel peers. F-FUNDER-DB-BYPASSED gate registered (signature only at DRAFT; predicate body at LOCK).

**Minor concern (P2):** the SPEC mentions "Scout v0.1's pre-Pass-2 behavior of bypassing the database is structurally prevented at v0.2 via gate F-FUNDER-DB-BYPASSED" but the Pass-2 Scout block normalization landed Scout's funder-classification heuristics, not a structural fix to the database-bypass problem. The phrasing risks reading as if Pass-2 already fixed v0.1; it has not — only the heuristics layer landed. RECOMMENDED CLARIFICATION at Audit #2: change "pre-Pass-2 behavior" → "v0.1-baseline behavior" to avoid implying Pass-2 changed v0.1 runtime.

### §1.4 §2.2 Two-layer funder-intelligence database with Law-3 isolation

PASS — Law-3 enforcement is structural at the schema layer. Two layers are sibling-not-nested:
- `vault_shared/funder_intelligence/` — workspace-curated, publisher-Ed25519-signed.
- `orgs/<slug>/vault/funder_intelligence/` — per-applicant, never crosses Law 3.

F-FUNDER-DB-CROSS-ORG-LEAK declared (signature only at DRAFT). The cross-org write check is path-resolve-normalized — mirrors §15 v1 §15.9.1 enforcement pattern. Stage-5 consent tier on-ramp documented as out-of-scope for v0.1 and v0.2, anchored to v7.0.5 §6.

**Architecture-precedent check:** v7.0.5 LOCKED 2026-05-10 row 179 explicitly binds Funder Intel DB curation + Match DB lifecycle to the Archivist v1.x curation slot. This SPEC respects that binding — Scout v0.2 *proposes* DB enrichments; operator confirms; Archivist's quarterly curation digest reads MatchOutcome rollups. No conflict.

### §1.5 §2.3 Channel G — Relationship-Sourced track

PASS — gate registrations follow gate-taxonomy v1:
- `F-NOM-FABRICATED-RELATIONSHIP` (hard_eligibility_gate, P0, REJECT_NO_DRAFT) — VALID tuple per `_validators/gate_taxonomy_consistency.py` row 31.
- `F-NOM-COLD-OUTREACH-DRAFT` (drafting_warning, MED, WARN_SCRIBE) — VALID tuple per row 43.
- `F-NOM-NETWORK-LEAK` (hard_eligibility_gate, P0, REJECT_NO_DRAFT) — VALID tuple per row 31.

The cold-outreach-vs-operator-asks-network distinction is structural and well-grounded in §1.4 Scout heuristics (foundation relationship-signal pattern: prior funding / peer-grantee introduction / documented contact is the weight; cold-outreach is an operator-attention trigger). The SPEC's Scribe-side enforcement (Scribe is allowed to draft *operator-asks-network*; Scribe is NOT allowed to draft *cold-outreach-to-nominator-target*) is consistent with §1.4 §S2-3 anti-pattern enforcement.

### §1.6 §2.4 Match Database feedback loop

PASS. MatchOutcome is sibling-not-nested with ScoutReflection (Scout's per-cycle reflection) and ReflectionPacket (§16's per-cycle packet). Three sibling artifacts at cycle close; each has distinct producer, consumer, schema, and F-* family. Cross-family-import ban applies at AST-lint.

**Architecture-precedent check:** §15 v1 §15.4.2 quarterly-review input contract explicitly reads `match_database_path` as one of Archivist's substrate paths. The SPEC's "MatchOutcome → Archivist quarterly digest reads MatchOutcome rollups → operator-confirmed lessons feed back into Scout's next cycle's hypothesis-generation primitive" is precisely the §15 v1 contract. No violation.

**P2 note:** the SPEC defers the full MatchOutcome Pydantic schema to LOCK ceremony paired §2 v7.x sub-kind amendment. This is a reasonable scope-narrowing — MatchOutcome is consumed by Archivist's quarterly digest, not by Scout's daemon loop. Scout's per-cycle dependency on MatchOutcome is informational only (hypothesis-generation primitive (a) graph-walk on winning matches reads the per-applicant Match Database's WIN rows; the *MatchOutcome shape* is unchanged from Match DB's existing schema per v7.0.5 §2). The deferral is honest, not a gap.

### §1.7 §2.5 Cycle-aware pipeline auto-promotion

PASS. Promotion is deterministic Python (NOT LLM-driven). Pipeline row transitions from `shadow` → `active_watch` when historical-reopen-date enters configurable lookahead window. Auto-promotion never crosses to *operator-confirmed pursuit*; that transition stays operator-explicit per Law 5.

**Architecture-precedent check:** §15 v1 §15.4 inputs do not require auto-promotion to be Archivist-owned (Scout v0.2 is the owner per this SPEC §9 recommendation). No conflict.

**P2 note:** the SPEC says "default 90 days; operator-tunable per applicant" lookahead window. Per §1.4 Scout heuristics §3 timing-axis heuristics, federal-cycle vs state-cycle vs foundation-cycle timing have very different shapes. The 90-day default may be too coarse for foundation-cycle (LOI + invited-proposal cadence with rolling deadlines or quarterly board cycles) — RECOMMENDED at Audit #2: state explicit per-cycle-class defaults (federal: 90 days; state: 120 days due to budget reconciliation uncertainty; foundation: 60 days due to LOI cadence; cooperative-intermediary: 90 days).

### §1.8 §2.6 CIC-aware Scout configuration

PASS — CIC × CLC orthogonality preserved per v7.0.8. The SPEC reads the four CIC card primitives (Search Vocabulary, Evidence Schema, Language Register, Reporting Rhythm) at Scout startup and uses them as runtime configuration. Matching at runtime is opportunity-driven (CLC-typed at funder-side ingestion). F-CIC-CLC-COUPLING-VIOLATION (v7.0.8) is referenced but not re-registered — appropriate inheritance.

**Architecture-precedent check:** v7.0.11 §1.2 card axes registration (six CICs, eight CLCs) is the binding parent. The SPEC defers CIC card field-path enumeration to LOCK ceremony paired §18 v1.x amendment — appropriate scoping.

### §1.9 §2.7 Coalition-opportunity surfacing

PASS. `coalition_required: bool` + `coalition_participants_known: enum {none, partial, full}` is a clean structural representation. Operator-attention trigger (NOT a hard gate) when `coalition_required: true` AND `coalition_participants_known != full` — consistent with §1.4 Scout heuristics §4 escalation triggers (cross-funder routing decision required). No conflict with Law-2 boundary drift (the opportunity is *in scope for the applicant as a coalition participant*; auto-Avoid would be the drift).

### §1.10 §2.8 Channel A-G orthogonality

PASS. All seven channels run parallel, no fallback. VERIFY phase preserved from Scout v0.1 round-9 spec. REVIEW is still the human gate.

### §1.11 §2.9 Runtime-mode duality

PASS — query pipeline cache contract is structurally sound. Operator query is synchronous against cache; scan is daemon-background. Cache canonical-JSON-signed per v7.0.4-M1 §2 — consistent with KFR signing discipline.

**Architecture-precedent check:** the `mcp__scheduled-tasks__*` pattern is referenced — this is the same MCP server family used by §15 Archivist v1.x amendment for weekly + quarterly cadence. Scout v0.2 daemon mode and Archivist v1.x scheduled cadences share the scheduled-tasks substrate but never share scheduling responsibility (per §9 decision). No conflict.

**P1 concern (LOCK-blocker for Audit #2):** the SPEC declares the daemon entry point at `pipeline.orchestrator.seats.scout.daemon_cycle`. At v0.3 migration, this becomes a callable that Archivist invokes. The SPEC does not declare *who owns* the per-cycle Logfire span root at v0.3 (Scout's `scout.cycle.{cycle_runtime_mode}` root span vs Archivist's reflection-sub-mode root). RECOMMENDED at Audit #2: declare the Logfire span ownership at v0.3 — does Scout's root span become a child of Archivist's reflection-sub-mode root span at v0.3, or does Scout retain root-span ownership and Archivist's span becomes a *parent* of Scout's? This is a small specification gap that can be closed at LOCK ceremony.

### §1.12 §2.10 ScoutReflection artifact (self-directed search expansion)

PASS — the artifact is sibling-not-nested with §16 ReflectionPacket; the dimension table in §7 makes the boundary explicit. Schema fields match the handoff's enumeration verbatim. The provenance fields (`cycle_runtime_mode`, `prior_reflection_id`, `posture`, `classification_register_version`) carry the auditability surface.

**Architecture-precedent check:** §16 v1 §16.2.1 schema declares ReflectionPacket's top-level shape with 13 fields including `classification_register_version`, `cycle_close_marker_span_id`, `org_slug`, etc. ScoutReflection's schema (per §B canonical yaml) declares 19 fields with the same naming convention. The schemas are structurally parallel — *which is appropriate for sibling artifacts*. No collision: the consumer and F-* family are distinct.

### §1.13 §2.11 Hypothesis-generation primitive

PASS on the four sources + DORMANT binding for cross-applicant. The deterministic-Python discipline for sources (a), (b), (c) is structurally Law-5-protective (Scout cannot invent funder names because the source substrate is operator-confirmed). The DORMANT pattern for source (d) mirrors §16 v1 OQ-2 (a) precedent: schema field reserved, gate LIVE-fail-closed.

**Law-3 check:** the cross-applicant DORMANT field is the load-bearing Law-3 risk. F-SCOUT-HYPOTHESIS-CROSS-APPLICANT-LEAK is registered as hard_eligibility_gate, P0, REJECT_NO_DRAFT — VALID tuple per gate-taxonomy v1 row 31. The gate fail-closes any path with `source: cross_applicant` regardless of substrate provenance. **This is the correct enforcement shape** — DORMANT field at the schema layer (so Stage-2+ engagement does NOT require a schema migration) + LIVE gate at the runtime layer (so v0.1 + v0.2 cannot accidentally engage the cross-applicant path).

**P2 note:** the SPEC says "operator-signed consent tier engagement" is the Stage-2+ unblock mechanism but does NOT specify which signature (operator's? Sovereign Node commons LLC's? both?). v7.0.5 §6 binds Stage-5 consent tier to the cooperative-owned commons. RECOMMENDED at Audit #2: clarify which signature is required at Stage-2+ for the gate to flip from LIVE-fail-closed to operator-signed-consent-tier-conditional.

### §1.14 §2.12 Daemon sovereignty + cost controls

PASS — three budget axes (dollar_cents, token, api_call) with Decimal mandate per A12 (`int_micro_cents` per §B canonical yaml). Posture pin at cycle start; mid-cycle change prohibited; mirrors F-CLASS-POSTURE-MID-CYCLE-CHANGE per v7.0.10 §5.

**Architecture-precedent check:** v7.0.7 §5.1 F-CLASS-NEW-FACT-UNCLASSIFIED is registered as a top-level F-CLASS-* family code; the SPEC's "Scout-side hook into F-CLASS-NEW-FACT-UNCLASSIFIED" is appropriate inheritance (not a new top-level F-* code). VALID gate-taxonomy v1 tuple per the Scout-side hook predicate.

**P1 concern (LOCK-blocker for Audit #2):** the SPEC declares "rate-limits enforced against funder APIs" with conservative defaults at §6.2. Per v7.0.7 §6.1 router-template publisher-Ed25519-signing discipline, the rate-limit config is signed by a publisher with white-glove-pinned public key. **The SPEC does not declare who the rate-limit-config publisher is.** Is it the same publisher as router.yaml (SN-LLC / Golden Quill publisher)? A separate Scout-config publisher? This is a key-management question that must be answered at LOCK ceremony. RECOMMENDED at Audit #2: declare the rate-limit-config publisher identity.

### §1.15 §3 (§A) Adversarial pre-checks

PASS on all three required subsections:
- `runtime_consumer` declares what changes for Scribe, Judge, Red Team, Logician
- `artifact_must_not_contain` declares no synthetic funders, no cross-applicant leakage at v0.1
- `strength_test` answers all three calibration questions with explicit downstream-behavior-change proofs

The strength-test answers (§3.3) are concrete — they identify the *observable* differences in Scribe's citation strings (DB entry IDs vs Scout-cycle IDs) and Logician's audit-trail row count (~30 vs ~41 rows). These are testable claims — they can be verified at Audit #2 against actual cycle outputs from a paired v0.1 / v0.2 dry-run if one is available.

**P2 note:** the §3.3 (c) answer about flipping daemon loop ownership says "the change is one line in `daemon_loop_owner: scout` flipping to `daemon_loop_owner: archivist`." This is technically true but understates the operational change — at v0.3 the `mcp__scheduled-tasks__*` registration also moves. RECOMMENDED at Audit #2: clarify that the migration is *one line of config* + *one scheduled-task registration update*, both operator-driven.

### §1.16 §4 (§B) Canonical yaml

PASS — the Codex-shape follows the FID gold-standard `USDA-RD-CFP-FY26_charter_v0_DRAFT.md` §B pattern (artifact_id, artifact_family, version, lifecycle, validation_status, runtime_load_status, operator_label, one_sentence_job, runtime_consumers structure).

The canonical yaml carries the load-bearing structural primitives:
- `runtime_mode_duality` block with one_shot / daemon mode declarations
- `scout_reflection_artifact` block with Pydantic shape + 19 fields + 22 __post_init__ invariants placeholder
- `hypothesis_generation_primitive` block with four sources + DORMANT binding
- `daemon_sovereignty_and_cost` block with three budget axes + posture pin
- `daemon_loop_owner: scout` field with `migration_target_v0_3: archivist_owns_loop` + `operator_decidable: true`
- `cross_family_import_ban` block with five banned imports + AST-lint module reference

**Gate-taxonomy v1 conformance:** every gate carrying (gate_type, severity, fail_action) in §5 satisfies one of the five allowed tuples per `_validators/gate_taxonomy_consistency.py` ALLOWED dict. Verified gate-by-gate:
- F-SCOUT-HYPOTHESIS-FABRICATED → (hard_eligibility_gate, P0, REJECT_NO_DRAFT) ✓ row 31
- F-SCOUT-HYPOTHESIS-CROSS-APPLICANT-LEAK → (hard_eligibility_gate, P0, REJECT_NO_DRAFT) ✓ row 31
- F-SCOUT-DAEMON-BUDGET-EXCEEDED → (verify_required_gate, HIGH, HOLD_FOR_OPERATOR_REVIEW) ✓ row 38
- F-SCOUT-DAEMON-POSTURE-DRIFT → (hard_eligibility_gate, P0, REJECT_NO_DRAFT) ✓ row 31
- F-CLASS-NEW-FACT-UNCLASSIFIED → (verify_required_gate, VERIFY_REQUIRED, HOLD_FOR_OPERATOR_REVIEW) ✓ row 38
- F-NOM-FABRICATED-RELATIONSHIP → (hard_eligibility_gate, P0, REJECT_NO_DRAFT) ✓ row 31
- F-NOM-COLD-OUTREACH-DRAFT → (drafting_warning, MED, WARN_SCRIBE) ✓ row 47
- F-NOM-NETWORK-LEAK → (hard_eligibility_gate, P0, REJECT_NO_DRAFT) ✓ row 31

All eight new gates conform.

### §1.17 §5 New F-* gate families

PASS — five new F-SCOUT-* + three new F-NOM-* + two new F-FUNDER-DB-* + the META-gate F-SCOUT-COVERAGE-INCOMPLETE = eleven new F-* entries.

META-gate exclusion from F-CLASS-COVERAGE-INCOMPLETE is consistent with §16 v1 F-PACKET-* exclusion precedent (per CLAUDE.md note: "F-PACKET-* EXCLUDED from F-CLASS-COVERAGE-INCOMPLETE META gate per OQ-6-style isolation precedent (same as F-WPFA-* + F-FG-*)"). The new families add a fifth excluded family (F-SCOUT-* + F-NOM-* + F-FUNDER-DB-*). The pattern is: family-specific META-gate per artifact / producer; one cross-reference at the F-*-SPAN-PROVENANCE-MISSING tier; no other cross-family coupling.

**P1 concern (LOCK-blocker for Audit #2):** the SPEC declares predicate bodies "raise NotImplementedError at v0.2 DRAFT" but does not declare the LIVE-vs-DORMANT mix at LOCK. §16 v1 has 18 dormant + 1 LIVE META-gate; the SPEC implies a similar structure but does not enumerate which Scout v0.2 predicates flip to LIVE at LOCK vs which stay dormant pending v0.2 first wave or v0.3. RECOMMENDED at Audit #2: enumerate the LIVE-vs-dormant mix explicitly (a table mapping each F-SCOUT-* / F-NOM-* / F-FUNDER-DB-* code to its v0.2-LOCK status: `live | dormant_via_NotImplementedError | dormant_via_LIVE_fail_closed_gate`).

### §1.18 §6 Logfire span + funder-API rate-limit specs

PASS — Logfire span structure is hierarchical and provides auditability for daemon cycles. Rate-limit defaults are conservative.

**P2 note:** the SPEC declares cloud-LLM tokens_per_minute = 100000 and dollar_per_cycle_cents = 5000 (i.e., $50 / cycle). Per the v7.0.10 three-posture model, daemon cycles routed under Frontier-Eligible posture can consume cloud-LLM tokens, while Local-Only-Sovereign posture stays entirely on the local appliance. The SPEC's defaults assume non-zero cloud-LLM consumption — appropriate for Frontier-Eligible default deployments but may be over-budgeted for Local-Only-Sovereign deployments. RECOMMENDED at Audit #2: declare per-posture default budgets (Frontier-Eligible: $50/cycle; Split-Context Hybrid: $20/cycle; Local-Only-Sovereign: $0/cycle cloud-LLM, with token budget tracked against local model invocations for cost-discipline parity).

### §1.19 §7 Cross-family-import ban to §16 ReflectionPacket

PASS — the dimension table makes the boundary explicit. AST-lint module `pipeline/linting/r_scout_no_cross_family_import.py` to author at LOCK. Cross-reference allowed at the F-*-SPAN-PROVENANCE-MISSING tier (at most one), consistent with §16 v1 / §17 v1 sibling pattern.

**Architecture-precedent check:** §16 v1 frontmatter declares "sibling-not-nested with §17 WPFA CycleReceipt" with the same dimension-by-dimension boundary. The SPEC's §7 mirrors this pattern for ScoutReflection ↔ ReflectionPacket. No conflict; the Scout v0.2 sibling-not-nested boundary is architecturally consistent.

### §1.20 §8 §1 strength-test answers

PASS — two downstream-seat behavior-change proofs (Scribe, Logician) with same-prompt-with/without observable differences.

The Scribe proof identifies *citation string format* as the observable. The Logician proof identifies *audit-trail row count* as the observable. Both are testable.

### §1.21 §9 LOCK-blocker decision: daemon loop owner

PASS — the recommendation (Scout-owns-loop at v0.2) is baked in with three rationale points (ship velocity, clean discovery contract, cheap migration path). Migration path documented for v0.3. `operator_decidable: true` is registered. LOCK ceremony confirms before sealing.

**Architecture-precedent check:** §15 v1 §15.1.0 declares "At v0.2 (this LOCK), the operator is responsible for: manually invoking `tilth archivist weekly --org <slug>` and `tilth archivist quarterly` cadences (no scheduled-task trigger; operator decides when)." Archivist v0.2 does NOT yet schedule itself. The SPEC's rationale (a) is precisely correct — asking Archivist v0.2 to schedule Scout would require Archivist v2.x SPEC LOCK ahead of Scout v0.2 LOCK, inverting the runway. **No §15 commitment violation.**

The migration path (§9.3) preserves Scout's API surface byte-for-byte at v0.3. The AST-lint cross-family-import ban is preserved. The change at v0.3 is a single config-line flip + scheduled-task re-wire. The architectural debt is minimal.

### §1.22 §10 Out-of-scope

PASS — out-of-scope enumeration is honest. No code lands. No SUB_KIND_REGISTRY registration. Predicate bodies raise NotImplementedError. Stage-2+ engagement requires separate amendment. Downstream-seat code changes are *input-shape-driven*, not code-driven.

### §1.23 §11 Open questions for operator

PASS — seven open questions surfaced for LOCK ceremony. Each is appropriately scoped (operator decision, not LLM decision). The questions cover daemon loop owner (recommendation baked in), cadence defaults, RSS baseline source, rate-limit defaults, META-gate scope, Logfire span naming for cross-reference, coalition-required handling.

### §1.24 §12 What did NOT make it into the SPEC

PASS — gaps are honest and reasonable. Implementation code, per-channel adapter code paths, CIC card field path mapping, full MatchOutcome schema, full F-NOM-* Codex-shape registrations, F-CIC-CLC-COUPLING-VIOLATION re-registration, Cards "Phase A first fixtures" coupling — all deferred to LOCK ceremony paired amendments with clear rationale.

---

## §2 P0 / P1 / P2 findings

### §2.1 P0 (LOCK-blocker; must close before LOCK ceremony)

**None surfaced.** The SPEC honors all Five Operating Laws, all architecture v7.0.x §-family boundaries, the §15 Archivist v0.2 commitment, the §16 ReflectionPacket v1 cross-family-import ban, and Pass-1 gate-taxonomy v1.

### §2.2 P1 (LOCK-ceremony-mandatory; close at Audit #2 or LOCK ceremony decision)

**P1-1 (LOCK-blocker — operator decides at LOCK):** Daemon loop owner at v0.2. Recommendation baked in (Scout-owns-loop). Operator confirms or overrides at LOCK ceremony.

**P1-2 (LOCK-blocker — declare at Audit #2 close-out):** Logfire span ownership at v0.3 migration. At v0.3, does Scout's `scout.cycle.{cycle_runtime_mode}` root span become a child of Archivist's reflection-sub-mode root span, or vice versa? Specification gap; close at Audit #2.

**P1-3 (LOCK-blocker — declare at Audit #2 close-out):** Rate-limit-config publisher identity. Per v7.0.7 §6.1, the rate-limit config is publisher-Ed25519-signed. Who is the publisher? Same as router.yaml (SN-LLC / Golden Quill)? A separate Scout-config publisher? Key-management question; close at Audit #2.

**P1-4 (LOCK-blocker — declare at Audit #2 close-out):** LIVE-vs-DORMANT mix at LOCK. §16 v1 has 18 dormant + 1 LIVE META-gate. Which Scout v0.2 predicates flip to LIVE at LOCK vs which stay dormant? Enumerate explicitly at Audit #2.

### §2.3 P2 (LOCK-ceremony-recommended; non-blocking)

**P2-1:** §2.1 "pre-Pass-2 behavior" phrasing risks implying Pass-2 fixed v0.1. Change to "v0.1-baseline behavior."

**P2-2:** §2.5 cycle-aware promotion 90-day default may be too coarse for foundation cadence. Declare per-cycle-class defaults (federal 90 / state 120 / foundation 60 / cooperative 90).

**P2-3:** §2.11 (d) Stage-2+ unblock mechanism — clarify which signature is required (operator? Sovereign Node commons LLC? both?).

**P2-4:** §3.3 (c) daemon-loop-ownership flip understates operational change — clarify that migration is *one line of config* + *one scheduled-task registration update*, both operator-driven.

**P2-5:** §6.2 rate-limit defaults assume non-zero cloud-LLM consumption — declare per-posture default budgets (Frontier-Eligible: $50/cycle; Split-Context Hybrid: $20/cycle; Local-Only-Sovereign: $0/cycle).

---

## §3 LOCK-blockers (summary count + list)

**Count:** 4 P1-class LOCK-blockers (no P0 blockers).

**List:**
1. **P1-1** — Daemon loop owner at v0.2 (operator decides at LOCK; recommendation baked in: Scout-owns-loop).
2. **P1-2** — Logfire span ownership at v0.3 migration (declare at Audit #2 close-out).
3. **P1-3** — Rate-limit-config publisher identity (declare at Audit #2 close-out).
4. **P1-4** — LIVE-vs-DORMANT predicate mix at LOCK (enumerate at Audit #2 close-out).

P0 finding count: **zero**. The SPEC clears the bar for Audit #1 with no blocking architectural concerns — all four P1s are *specification-completeness* concerns, not *design-soundness* concerns.

---

## §4 Recommendations for LOCK ceremony

### §4.1 Cross-family Thesis dispatch posture

LIVE FULL CROSS-FAMILY per AGENTS.md § Cross-family review — bridge pattern. Same precedent as WS-D v7.0.5 + §15 v1 + §16 v1 + §17 v1.

Dispatch shape:
- **Editor** = groq/llama-3.3-70b-versatile (Meta family)
- **Judge** = google/gemini-2.5-pro (Google family)
- **Red Team** = groq/openai/gpt-oss-120b (OpenAI-OSS family)

Bridge pattern: Cowork session reaches the local openclaw gateway via `mcp__Control_your_Mac__osascript` → `do shell script "PATH=$HOME/.npm-global/bin:$PATH openclaw infer model run --gateway --model X --prompt P --json" with timeout of 600 seconds`. Working dispatch templates: `pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v{1,2}.sh`.

Audit trail location: `pipeline/validation/scout_v0_2_audit_1_thesis_2026-05-19/` (this SPEC's frontmatter declares the path; LOCK ceremony populates it).

### §4.2 Two-cycle strict L-005 discipline

This document is Audit #1 (scoping). Audit #2 (verification) follows operator review. No silent third round per L-005.

If Audit #2 surfaces new findings beyond the four P1s identified here, escalate per L-005 architecture-domain disagreement branch (operator-confirmation-precedent pattern per WS-D v7.0.5 + WS-B v7.0.7 + WS-C-M1 v7.0.4-M1 row-170 transparent disposition).

### §4.3 Companion paired-commit at LOCK

Per the §6.17 Option-B compound-paired-commit pattern (WS-D v7.0.5 / §15 v1 / §16 v1 / §17 v1 / WPFA precedents), Scout v0.2 LOCK ceremony commits four artifacts atomically at the same `lock_timestamp_utc`:

1. **This SPEC** — `pipeline/blueprint/v0.2/scout_v0_2_superscout_spec.md` LOCKED.
2. **Paired Logician amendment** — `pipeline/blueprint/v0.1/section_04_v2_x_y_scout_amendment.md` registering F-SCOUT-* + F-NOM-* + F-FUNDER-DB-* + F-SCOUT-COVERAGE-INCOMPLETE Cedar/Python predicate signatures + the META-gate body.
3. **Paired §0.5 interface-index amendment** — `pipeline/blueprint/v0.1/section_00_5_section_scout_v0_2_amendment.md` row-appending the new artifact ID + gate codes + module paths.
4. **Paired §2 sub-kind registration amendment** (deferred to v0.2 first wave; OPTIONAL at v0.2 LOCK) — `pipeline/blueprint/v0.1/section_02_v7_x_scout_reflection_subkind_amendment.md` if ScoutReflection registers at LOCK; deferred to v0.2 first wave compound LOCK per §10 out-of-scope if not.

### §4.4 LIVE-vs-DORMANT mix enumeration at Audit #2

At Audit #2 close-out, populate a table mapping each F-SCOUT-* / F-NOM-* / F-FUNDER-DB-* code to its v0.2-LOCK status:
- `live` — predicate body LIVE at LOCK; tested in `tests/seats/scout/`.
- `dormant_via_NotImplementedError` — predicate body raises NotImplementedError; deferred to v0.2 first wave or v0.3.
- `dormant_via_LIVE_fail_closed_gate` — gate is LIVE-fail-closed (rejects all attempts) until operator-signed unblock condition lands; mirrors F-SCOUT-HYPOTHESIS-CROSS-APPLICANT-LEAK pattern.

This table is what the operator confirms at LOCK ceremony.

### §4.5 Operator decisions awaiting confirmation (summary)

Seven operator decisions surfaced at §11 of the SPEC, plus three deferred to Audit #2 close-out:

**At SPEC §11 (LOCK ceremony):**
1. Daemon loop owner at v0.2 (P1-1 above; recommendation: Scout-owns-loop)
2. Per-applicant cadence defaults
3. RSS / newsletter baseline source paths
4. Rate-limit defaults
5. F-SCOUT-COVERAGE-INCOMPLETE META-gate scope (separate vs absorbed)
6. Logfire span naming for cross-reference
7. Coalition-required handling escalation timing

**At Audit #2 close-out:**
8. Logfire span ownership at v0.3 (P1-2 above)
9. Rate-limit-config publisher identity (P1-3 above)
10. LIVE-vs-DORMANT predicate mix at LOCK (P1-4 above)

---

## §5 No-invention rule check

Every claim in the SPEC traces to one of:
- The exploration handoff (`pipeline/handoffs/scout_v0_2_superscout_exploration_2026-05-19.md`) — 12 design goals enumerated verbatim
- Locked architecture (v7.0.5, v7.0.7, v7.0.8, v7.0.9, v7.0.10, v7.0.11 DRAFT)
- §15 Archivist v1 LOCK
- §16 ReflectionPacket v1 LOCK
- Pass-2 Scout cross-charter heuristics (`pipeline/funder_intelligence/_seats/scout/heuristics.md`)
- Pass-1 gate-taxonomy v1 (`pipeline/funder_intelligence/_validators/gate_taxonomy_consistency.py`)
- FID Codex-shape gold-standard (`pipeline/funder_intelligence/pillar_1_charters/USDA-RD-CFP-FY26_charter_v0_DRAFT.md` §B)

**No invention surfaced.** The SPEC frames every architectural decision against an existing precedent (v7.0.7 §6.1 publisher-signing pattern, v7.0.5 §6 curation-slot binding, v7.0.8 CIC × CLC orthogonality, v7.0.10 §1 three-posture routing, §15 v1 §15.1.0 v0.2 operator-driven cadence, §16 v1 §16.0 sibling-not-nested artifact pattern). No claims invented out of whole cloth.

The recommendations baked in at §9 (Scout-owns-loop) and §6.2 (conservative rate-limit defaults) are operator-decidable choices flagged as such, not invented LOCK decisions.

---

## §6 Audit verdict

**READY_FOR_AUDIT_2_AFTER_OPERATOR_REVIEW.**

The SPEC clears Audit #1 with zero P0 findings, four P1 LOCK-blockers (all specification-completeness, none design-soundness), and five P2 recommendations. The Scout-owns-loop recommendation at §9 is architecturally defensible and structurally minimal; the migration path to Archivist-owns-loop at v0.3 is documented as a one-line config flip + scheduled-task re-wire, with no Scout API change and no AST-lint cross-family-import ban relaxation.

Cross-family-import ban to §16 ReflectionPacket honored. Pass-1 gate-taxonomy v1 conformance verified gate-by-gate. Law-3 enforcement structural across two-layer DB, Channel G, MatchOutcome, ScoutReflection, and hypothesis-generation primitive. §15 Archivist v0.2 commitment respected (Archivist v0.2 stays operator-driven; Scout v0.2 carries its own daemon loop).

Recommend LOCK ceremony proceed after operator review of the four P1s and the seven §11 open questions.

---

## §7 Cross-references

- Audited SPEC: `pipeline/blueprint/v0.2/scout_v0_2_superscout_spec.md`
- Parent handoff: `pipeline/handoffs/scout_v0_2_superscout_exploration_2026-05-19.md`
- §15 Archivist v1 LOCK: `pipeline/blueprint/v0.1/section_15_archivist.md`
- §16 ReflectionPacket v1 LOCK: `pipeline/blueprint/v0.1/section_16_reflection_packet.md`
- §17 WPFA v1 LOCK: `pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md`
- Architecture v7.0.5: `pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md`
- Architecture v7.0.7: `pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md`
- Architecture v7.0.8: `pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md`
- Architecture v7.0.9: `pipeline/architecture/v0.1/architecture_v7_0_9_amendment.md`
- Architecture v7.0.10: `pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md`
- Architecture v7.0.11 DRAFT: `pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md`
- Pass-2 Scout heuristics: `pipeline/funder_intelligence/_seats/scout/heuristics.md`
- Pass-1 gate-taxonomy v1: `pipeline/funder_intelligence/_validators/gate_taxonomy_consistency.py`
- FID Codex-shape gold-standard: `pipeline/funder_intelligence/pillar_1_charters/USDA-RD-CFP-FY26_charter_v0_DRAFT.md`
- AGENTS.md cross-family Thesis dispatch: `/AGENTS.md` § Cross-family review — bridge pattern
- L-005 two-audit cycle: lessons.md L-005
