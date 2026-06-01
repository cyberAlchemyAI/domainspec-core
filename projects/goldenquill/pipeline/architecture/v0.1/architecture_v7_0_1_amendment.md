---
title: Tilth Architecture — Amendment v7.0.1 (Governance Plan Preflight — Section E.P)
filed: 2026-04-19
operator: Josh
amendment_status: LOCKED 2026-05-08 — Tier 1 GPP-DET PASS (10/10 checks), Tier 2 GPP-COUNCIL live dispatch (Red Team groq/openai/gpt-oss-120b + Reasoner google/gemini-2.5-pro; 14 findings, 3 BLOCKING dispositioned 1 REJECTED + 2 DEFERRED, 9 RECOMMEND-FOLD-IN deferred to v7.1/v7.2, 2 INFORMATIONAL), Tier 3 GPP-SYNTHESIS signed manifest (Ed25519 + ML-DSA-65 stub-hybrid; ephemeral keypair pending real-engineer-gate persistent key per §13). L-005 two-audit completed 2026-04-19 thought-experiment Thesis round (predecessor_audits 01_audit_pass_1_editor_judge.md + 02_audit_pass_2_red_team_reasoner.md → 03_synthesis_fixes_verdict.md Audit #2 PASS); 2026-05-08 GPP three-tier closes the dispatch_mode_disclaimer Phase-0 wiring precondition. Paired commit: §4 v2.1.1 + §0.5 v5.
parent_lock: pipeline/architecture/v0.1/tilth_architecture_locked.md  (v7 A1-A12 LOCKED 2026-04-19)
supersedes_relationship: inserts BEFORE the planned v7.1 (Privacy Router) and v7.2 (Canary + Runtime Integrity) amendments. v7.0.1 is non-disruptive to A1-A12 — it adds a new Section E.P subsection and a new failure-code family without modifying any A-letter mechanism.
companion_blueprint_amendment: pipeline/blueprint/v0.1/section_04_v2_1_1_amendment.md  (§4.14a — GPP deterministic PRE-gate)
companion_index_amendment: pipeline/blueprint/v0.1/section_00_5_v5_amendment.md  (27 paired-commit §0.5 rows — decision recorded in thesis_round_gpp_2026-04-19/03_synthesis_fixes_verdict.md Fix F-2)
scope_source: pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_spec_v1.md
tool_implementation: pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_det.py
future_lock_citations:
  - pipeline/blueprint/v0.1/section_04_v2_1_1_amendment.md  # paired; LOCKs together with this file
  - pipeline/blueprint/v0.1/section_00_5_v5_amendment.md    # paired
version_wording_discipline: "LOCKED" refers to on-disk LOCKED state only. Forward-looking version targets use "target-LOCK at" wording.
---

# Amendment intent

Close the gap that produced the 2026-04-19 post-compaction finding: six scope-close plan artifacts were authored by operator + Opus 4.7 synthesis and dispatched to Thesis rounds without themselves being audited. Plan-layer artifacts are load-bearing — they determine which amendments happen in what order with what blockers — but no mechanism existed to audit them before dispatch.

This amendment inserts **Section E.P — Governance Plan Preflight (GPP)** into the locked architecture without disturbing A1-A12. GPP is a three-tier meta-audit that runs on plan-layer artifacts (scope-close plans, sequencing plans, dispatch plans, preflight existence audits, handoff contracts) before they gate any Thesis round or engineering phase. The full spec lives at `pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_spec_v1.md`; this amendment pins the architecture-level commitments.

# Proposed insertion — new subsection after Section E and before A1

## Section E.P — Governance Plan Preflight (GPP)

### E.P.1 — Purpose

Plan-layer artifacts are audited before dispatch with the same discipline the blueprint sections they gate already enjoy. GPP is the preflight mechanism. It is scoped narrowly: GPP does not replace L-005 Thesis rounds on blueprint or architecture sections; it does not replace L-006 existence audits on individual mechanisms; it adds a tier of audit specifically at the plan-layer.

### E.P.2 — Tiered structure

GPP has three ordered tiers. Each tier must pass or be explicitly disposed before the next begins.

**Tier 1 — GPP-DET (deterministic).** Zero-token, pure-Python, Logician-family discipline. Runs in seconds on operator hardware. Implements ten deterministic checks (CITE-RESOLVE, VERSION-RESOLVE, XDOC-REF, ROW-COUNT-ARITHMETIC, HASH-PIN, INDEX-STALE-DRYRUN, FAMILY-TAXONOMY, SCOPE-FREEZE-BACKDOOR-FLAG, VERSION-SKEW-DISCLOSURE, BLOCKER-CARRY-CHECK). Fail-closed.

**Tier 2 — GPP-COUNCIL (model-backed, bounded, cross-family).** Exactly two seats: Red Team (`red_team` row in `router.yaml`) and Reasoner (`reasoner_review` row in `router.yaml`). **Tier 2 is unconditional** — both seats dispatch on every plan run regardless of Check 8 SCOPE-FREEZE-BACKDOOR-FLAG state. Two API calls per plan run. Editor and Judge are explicitly not at this tier — GPP is a meta-audit, not a clarity-polish pass. Specific model-to-seat bindings live in `router.yaml`, never in this architecture file (A-letter discipline: architecture names roles, router names bindings).

**Tier 3 — GPP-SYNTHESIS (operator + Opus 4.7).** Operator reviews Tier 1 and Tier 2 outputs, folds findings or logs rejection-with-rationale, emits a signed GPP manifest. Signature uses the A12 crypto-agility hybrid (Ed25519 + ML-DSA-65).

### E.P.3 — Scope of application

A file is a plan-layer artifact and therefore subject to GPP if any of:

1. It is under `pipeline/validation/` or `pipeline/handoffs/` and dispatches one or more Thesis rounds by naming scope, seat assignments, or round-open gates.
2. It is a scope-close, sequencing plan, dispatch plan, preflight existence audit, or handoff contract by front-matter or filename convention.
3. It carries `blocker` tags that downstream rounds must clear before dispatch.
4. It declares §0.5 paired-commit row counts that are consumed by F-INDEX-STALE at commit time.

Blueprint sections, architecture documents, `router.yaml`, and grant-drafting artifacts are out of GPP scope — they have their own L-005 / L-006 discipline.

### E.P.4 — Manifest

GPP emits a signed manifest per plan. Manifest schema is pinned in `pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_spec_v1.md` §3 Tier 3. The manifest is the dispatch input for any downstream round; a round that dispatches without a valid signed manifest violates `F-GPP-MANIFEST-MISSING`.

### E.P.5 — Failure code family

The architecture commits to a new `F-GPP-*` failure code family of 12 codes (enumerated in `pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_spec_v1.md` §5 and pinned in §0.5 v5). This family is coordinate with existing `F-PRE-*`, `F-POST-*`, `F-RUNTIME-*`, and the forthcoming `F-PRIVACY-*`, `F-CANARY-*`, `F-ROUTER-FAMILY-COLLISION`, `F-RUNTIME-DRIFT-*`, and `F-KEY-PRESENCE-*` families from v7.1 and v7.2.

### E.P.6 — Sovereignty + efficiency

- Tier 1: zero external dependency beyond stdlib + PyYAML. Runs on operator hardware.
- Tier 2: BYOK-only API calls via seats already named in `router.yaml`. No metered backchannel.
- Tier 3: one operator + Opus 4.7 session-envelope per plan (A2 Block 2 budget).
- No new infrastructure. Reuses `router.yaml` dispatch paths, §0.5 canonical-bytes hashing, A12 signature primitives, §4 Logician PRE-gate machinery.

### E.P.7 — Cross-family rigor

Tier 2 dispatches Red Team + Reasoner. Their seat-to-model bindings in `router.yaml` resolve to two distinct provider families, both distinct from the Anthropic-family synthesis in Tier 3. This preserves Section E cross-family rigor at the plan-audit layer by construction: the mechanism guarantees three distinct families across Tiers 2 and 3 regardless of how bindings shift in future `router.yaml` revisions, because the red_team and reasoner_review rows are required to be cross-family with each other and with Tier 3 synthesis.

### E.P.8 — Law-map addition

**Law 1 — RFA Is the Source of Truth.** N/A. GPP audits plan-layer artifacts (internal governance) — it does not generate grant content and does not consume funder RFA text.

**Law 2 — No Boundary Drift.** GPP is the mechanism that catches scope-drift at the plan layer (Check 8 SCOPE-FREEZE-BACKDOOR-FLAG + unconditional Tier 2 Red Team adversarial pass). Plans that widen scope through implementation-shape slip without operator disposition are now gated.

**Law 3 — Org Isolation.** Not directly touched by GPP; Privacy Router amendment coverage at v7.1 remains the canonical Law 3 gate.

**Law 4 — Apolitical Sector Language + Admin-Risk Term Scanning.** N/A. GPP operates on internal-governance artifacts; dialect code-switching and admin-risk term scanning apply to client-facing grant text, not to plan-layer architecture.

**Law 5 — Applicant Brings the Substance.** N/A. GPP does not interact with client-provided substance — no fabrication surface exists at the plan-audit layer.

### E.P.8a — Sovereignty Promise (separate from Law-map)

Sovereignty Promise is a workspace-wide invariant, not one of the Five Operating Laws. GPP's compliance: Tier 2 calls stay BYOK; manifest + reports live workspace-local; Tier 1 runs fully offline on operator hardware; no phone-home; no metered backchannel. A client whose Tilth has GPP LOCKed retains full sovereignty over every plan-layer audit artifact.

### E.P.9 — Interaction with other A1-A12 mechanisms

- **A2 (Code Thesis Committee / session-envelope discipline):** Tier 3 synthesis budget is one session-envelope per plan. Bundled plans share one envelope.
- **A11 (Telemetry Commons):** GPP output does not enter the k-anonymity envelope. Plan-layer artifacts are internal governance, not client-mirror telemetry.
- **A12 (Crypto-agility):** Manifest signature uses the hybrid Ed25519 + ML-DSA-65 envelope. Non-negotiable.
- **A1-A10:** no modification.

### E.P.10 — Versioning

- Spec version is pinned in `pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_spec_v1.md` (currently `v1`).
- Tool version is pinned in `gpp_det.py` (currently `v1`).
- Manifest records both. A spec revision that breaks manifest parity with LOCKed plans is a fresh amendment, not an inline update.

# Proposed failure-code family registration (architecture-level)

| Code | Tier | Trigger |
|---|---|---|
| `F-GPP-CITATION-UNRESOLVED` | DET | Check 1 CITE-RESOLVE |
| `F-GPP-VERSION-UNRESOLVED` | DET | Check 2 VERSION-RESOLVE |
| `F-GPP-CROSSDOC-BROKEN` | DET | Check 3 XDOC-REF |
| `F-GPP-ROW-COUNT-MISMATCH` | DET | Check 4 ROW-COUNT-ARITHMETIC |
| `F-GPP-CANONICAL-HASH-MISMATCH` | DET | Check 5 HASH-PIN |
| `F-GPP-INDEX-STALE-ON-PROPOSED-ROWS` | DET | Check 6 INDEX-STALE-DRYRUN |
| `F-GPP-FAMILY-TAXONOMY-MISMATCH` | DET | Check 7 FAMILY-TAXONOMY |
| `F-GPP-SCOPE-FREEZE-BACKDOOR-UNREVIEWED` | DET→COUNCIL | Check 8 fires only if Tier 2 does not dispose |
| `F-GPP-VERSION-SKEW-UNDISCLOSED` | DET | Check 9 VERSION-SKEW-DISCLOSURE |
| `F-GPP-BLOCKER-UNCARRIED` | DET | Check 10 BLOCKER-CARRY-CHECK |
| `F-GPP-MANIFEST-MISSING` | dispatch | No signed manifest at round-open |
| `F-GPP-FINDING-UNDISPOSED` | SYNTHESIS | Tier 2 finding without Tier 3 disposition |

Blueprint §4 v2.1.1 pins the PRE-gate rows that map to these codes; §0.5 v5 pins all 12 as failure-code primitives.

# Boot-strap path — how this amendment LOCKs without circular dependency

GPP gates plans. This amendment is a plan-gated artifact. The boot-strap:

1. `gpp_det.py` is authored and runs zero-token.
2. GPP-DET runs against the scope-close plan + `pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_spec_v1.md` + this v7.0.1 amendment + the paired §4 v2.1.1 and §0.5 v5 amendments. Emits report.
3. Any DET failures are resolved by amending the plan or hardening the tool. (Current frontier: see `pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_spec_v1.md` front-matter `tool_bugs_to_fix_phase_0` and the Phase 0 queue in `pipeline/engineering/da_vinci_engineer_prompt_v2.md` §7.)
4. Tier 2 GPP-COUNCIL runs on this amendment + paired blueprint amendments. Two API calls (Red Team + Reasoner).
5. Tier 3 GPP-SYNTHESIS — operator reviews, signs manifest.
6. L-005 two-audit + domain-split Thesis round LOCKs v7.0.1 + §4 v2.1.1 + §0.5 v5 as a paired commit.
7. Subsequent plans (v7.1 Privacy Router, v7.2 Canary + Runtime Integrity) MUST pass GPP at dispatch.

Boot-strap is logged in daily log + lessons.md as a one-time exception pattern. Future plans never boot-strap because GPP is LOCKed.

# What this amendment does not do

- Does not modify A1-A12.
- Does not introduce any new council seat (Red Team and Reasoner are existing seats per `router.yaml`).
- Does not touch A11 R.6 ALLOWED list.
- Does not add a CI hook (operator-run in v0.1; Phase 2b may add CI integration).
- Does not introduce a UI / dashboard (text + JSON only per v0.1 discipline).
- Does not require new BYOK provider keys.
- Does not require a new infrastructure deploy.

# Predecessor blocker carry-forward exemption (BLOCKER-CARRY-CHECK disposition)

GPP-DET's Check 10 BLOCKER-CARRY-CHECK scans predecessor existence audits under `pipeline/validation/blueprint_sequencing_preflight_2026-04-19/existence_audit.md` and `pipeline/validation/integration_scope_close_2026-04-19/05_preflight_existence_audit.md`. These audits enumerate ASPIRATIONAL-LOAD-BEARING and PROPOSED-NOT-EXISTS blockers that are explicitly out of scope for this v7.0.1 paired commit. v7.0.1 narrowly inserts Section E.P (Governance Plan Preflight) without modifying A1-A12 and without consuming the v7.1 Privacy Router or v7.2 Canary + Runtime Integrity blocker sets.

The predecessor blockers below are documented as **carried to v7.1 / v7.2 scope, NOT consumed by v7.0.1**:

- **§5 telemetry-record hook** (per-seat invocation emits a record) — ASPIRATIONAL-LOAD-BEARING, carried to §5 next-LOCK + v7.1.
- **Content-scan classifier technology candidate** (runs locally, 128GB ceiling, classifies payloads for local-only-vs-cloud-eligible) — ASPIRATIONAL-LOAD-BEARING, carried to v7.1 Privacy Router scope (the classifier is the Privacy Router's classifier).
- **§5 per-invocation record schema** (`token_count_input`, `token_count_output`, `success_flag`, `seat`, etc.) — ASPIRATIONAL-LOAD-BEARING, carried to §5 telemetry hook landing.
- **STR derivation formula** (ratio of success_flag to token sum, aggregated as rolling distribution) — PROPOSED-NOT-EXISTS, carried to §5 telemetry hook landing.
- **`F-RAILS-REPORT-EMISSION-FAIL` failure code** — PROPOSED-NOT-EXISTS, carried to §5 next-LOCK.
- **`F-KEY-PRESENCE-PREFLIGHT-FAIL` failure code** — PROPOSED-NOT-EXISTS, carried to v7.1 / §4 v2.5 (Key Presence PRE-gate).
- **`F-RUNTIME-DRIFT-FROM-LOCKED-ROUTER` failure code** — PROPOSED-NOT-EXISTS, carried to v7.2 / §4 v2.5 (Drift-from-Locked-Router PRE-gate).
- **`F-ROUTER-FAMILY-COLLISION` failure code** — PROPOSED-NOT-EXISTS, scope of v7.0.1 architecture E.P.7 (cross-family rigor preserved by router-binding constraints) but not introduced as a code in v7.0.1; carried to v7.1 router-amendment for code registration.

**Disposition.** v7.0.1 narrow-scope is preserved by construction: Section E.P adds GPP without mechanism modification to A1-A12 and without consuming any of the carried blockers. The paired §4 v2.1.1 amendment registers only the F-GPP-* family. This carry-forward note is the canonical record that the v7.0.1 LOCK does not silently absorb v7.1/v7.2 scope. Each carried blocker remains tracked in its predecessor existence audit and will be consumed by its target amendment round (v7.1 Privacy Router for content-classifier + key-presence + router-family-collision; v7.2 Canary + Runtime Integrity for runtime-drift; §5 next-LOCK for telemetry record + rails-report-emission).

# Paired-commit reminder

This v7.0.1 amendment LOCKs atomically with:
- `pipeline/blueprint/v0.1/section_04_v2_1_1_amendment.md` (§4.14a)
- `pipeline/blueprint/v0.1/section_00_5_v5_amendment.md` (27 §0.5 rows — Thesis-round F-2 decision)

The F-INDEX-STALE PRE-gate in §0.5 v4 fails-closed if any of the 27 rows is missing at commit time.

# Thesis round expectations (for the eventual L-005 audit pass)

- **Audit pass 1 (Editor + Judge):** Editor audits clarity of E.P.1-E.P.10 subsection copy, failure-code naming consistency, law-map integration. Judge scores against Section E rubric (cross-family rigor) + A12 rubric (crypto-agility) + §4 v2.1 rubric (PRE-gate family additions).
- **Audit pass 2 (Red Team + Reasoner):** Red Team adversarial on circular-dependency boot-strap, hidden scope-creep (does GPP accidentally pull scope from blueprint sections?), family-taxonomy assumptions. Reasoner audits the decision journal (was "CI hook at v0.1" rejected with rationale? was "Editor at Tier 2" rejected with rationale? was "Ed25519-only, no PQC" rejected with rationale?).
- **Cross-family composition:** same roster pattern as §4 v2.1 round.
- **Synthesis:** operator + Opus 4.7 emits LOCK + signed GPP manifest atomically.

# End of amendment
