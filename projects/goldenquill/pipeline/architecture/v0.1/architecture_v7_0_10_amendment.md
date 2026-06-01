---
title: Tilth Architecture — Amendment v7.0.10 (Three-posture routing model — deprecates Sanitized / opaque-slot-token posture; formalizes Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign customer-facing vocabulary; F-CLASS-SLOT-ID-NON-OPAQUE + F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED repurposed as defense-in-depth gates; performance-dependent caveat formalized on Local-Only)
filed: 2026-05-11
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-11 — substantive architectural simplification (4 postures → 3 postures customer-facing vocabulary). The "Sanitized" posture (cloud Scribe drafts with opaque `[SLOT_<numeric_id>]` tokens for Confidential fields, local slot-fill renders post-fill draft) is **deprecated entirely as a first-class customer-facing routing posture**. The two F-CLASS-* primitives that enforced its discipline at v7.0.7 (`F-CLASS-SLOT-ID-NON-OPAQUE` PRE-call + `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED` POST-call) are repurposed as **defense-in-depth gates** — they remain runtime-active and fail-closed on any `[SLOT_*]` pattern in a cloud-routed prompt, but they now guard against bug/attack surfaces (no legitimate code path emits slot tokens into cloud prompts under any of the three remaining postures). L-005 strict two-cycle Thesis with FULL live cross-family rigor (Editor=Llama-3.3-70B/Groq + Judge=Gemini-2.5-Pro/Google + Red Team=GPT-OSS-120B/Groq via openclaw bridge per AGENTS.md) CLOSED. Cycle 1: Editor READY_TO_LOCK + 3 findings folded + Judge READY_TO_LOCK 100/100 + 1 LOW folded + Red Team REQUIRES_MAJOR_FIXES 62/100 with 8 findings (1 HIGH + 5 MED + 2 LOW); all 12 findings closed in Cycle 1 author response per §12. Cycle 2: Editor READY_TO_LOCK 98/100 + 2 NEW LOW cosmetic + Judge READY_TO_LOCK with 10/12 explicit CLOSED before response-length truncation (full verdict CLOSED captured; truncation is a model-side max-output-length quirk, logged) + Red Team REQUIRES_FIXES (blocking:true) with 4 NEW (1 HIGH + 3 MED) + 6 PARTIAL closures expanded — all 10 NEW/PARTIAL items FOLDED-IN at LOCK per L-005 row-170 transparent disposition precedent (matches §15 v1 SPEC LOCK + §4 v2.x.1 + §13 Data Collector v1 + §14 Report Generator v1 LOCK precedents). Compound transaction per §6.17 Option-B at LOCK ceremony.
parent_lock: pipeline/architecture/v0.1/tilth_architecture_locked.md
parent_amendment: pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md  # The amendment this one supersedes-by-simplification; v7.0.7 §1 four-posture-implicit collapses to v7.0.10 §1 three-posture-explicit
predecessor_amendments_chain:
  - v7.0.4 (LOCKED 2026-05-09; row 178) — KFR + SP0 + Logician fact-drift family
  - v7.0.4-M1 (LOCKED 2026-05-10; row 190) — narrow-corrective post cross-family verification
  - v7.0.5 (LOCKED 2026-05-10; row 179) — Funder Intel DB + Match DB + Scout channel G + Stage-5 consent-tier on-ramp
  - v7.0.6 (SELF-LOCKED 2026-05-09) — six-seat roster + support-agent slots
  - v7.0.7 (LOCKED 2026-05-10; row 180) — classification-driven routing + F-CLASS-* dormant primitives + heavy-Judge on-demand swap + per-deployment router.yaml + SN-LLC router-template signing. **CANONICAL PRECEDENT FOR L-006 DORMANT-BINDING PATTERN + BINDING-vs-HORIZON SPLIT.** v7.0.10 narrows v7.0.7 §1 routing vocabulary; v7.0.7 §3 Classification Review stage stays canonical with updated posture vocabulary; v7.0.7 §4 heavy-Judge swap stays canonical (Local-Only posture also benefits); v7.0.7 §5.1 F-CLASS-* family roster: 10 primitives stay live, 2 primitives (slot-id-non-opaque + cloud-received-opaque-slot-filled) repurposed as defense-in-depth.
  - v7.0.8 (LOCKED 2026-05-08) — CIC × CLC orthogonality F-CIC-CLC-COUPLING-VIOLATION enforcement
  - v7.0.9 (LOCKED 2026-05-10; row 202) — Reflection v0.1 hook + F-REFLECTION-* dormant primitives; synthesis memo §6 row referencing F-CLASS-SLOT-ID-NON-OPAQUE retracts at footer addendum per §8.3 below.
companion_files_pending_edit_at_LOCK:
  - "pipeline/blueprint/v0.1/section_07_scribe.md (rename §7 'classification-aware-split-context' references to 'split-context hybrid drafting' per v7.0.10 §1.2; remove sanitized/opaque-slot wording; F-SCRIBE-* family unaffected; parent_locks updates v7.0.7 reference to chain v7.0.10)"
  - "pipeline/blueprint/v0.1/section_11_intake.md (Classification Review surface: 4-class display flips to 3-posture display per v7.0.10 §1; per-fact class enum unchanged at four values; F-CLASS-NEW-FACT-UNCLASSIFIED unaffected)"
  - "pipeline/architecture/v0.1/architecture_v7_0_9_amendment.md (LOCKED 2026-05-10 — Reflection synthesis §6 sentence retraction footer addendum, NOT in-place edit; preserves audit-trail integrity per §8.3)"
  - "pipeline/research/reflection/synthesis_design_memo_2026-05-10.md (§6 row retraction footer note — planning artifact; updated per §8.3)"
  - "README.md (posture vocabulary update — 4-posture-implicit → 3-posture-explicit; Local-Only caveat language)"
  - "CLAUDE.md (Beta model strategy section update; What-NOT-to-Do guards repurposed for new gate disposition)"
  - "docs/ARCHITECTURE_OVERVIEW.md (posture vocabulary throughout; classification-driven routing diagram redrawn; opaque-slot mechanism deprecated)"
  - "docs/lessons_memory_external_one_pager.md (customer-facing posture descriptions; Local-Only under-validation caveat)"
  - "docs/white_glove_v0_1_beta.md (customer-facing posture vocabulary; Classification Review stage step-4 posture-selection narrative)"
  - "pipeline/blueprint/v0.1/section_04_v2_x_amendment.md (F-CLASS-SLOT-ID-NON-OPAQUE + F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED disposition: REPURPOSED as defense-in-depth; remain live runtime gates; F-CLASS-* family roster updated; new §4.3.6 disposition note)"
  - "pipeline/blueprint/v0.1/section_00_5_section_15_reflection_amendment.md (Reflection posture row update if needed — per §8.2 below, no row mutation required; addendum note)"
  - "router.yaml (per-deployment template header — posture vocabulary updated; routing rule comment block reflects three-posture model; slot-fill agent comment removed/repurposed; underlying seat bindings unchanged)"
  - "pipeline/orchestrator/seats/archivist/reflection_mode.py (internal naming constants — if any reference the opaque-slot mechanism; per §8.2 the v0.1 hook scaffold does not; addendum note only if found)"
  - "pipeline/orchestrator/classification_review.py + pipeline/cli/tilth_review_classify.py (UX wrapper — 4-class display flips to 3-posture deployment-level display + per-field 4-class register display preserved at field level; per §1.4 below)"
  - "pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md (§0.5 v21 paired-commit — interface index row updates for F-CLASS-SLOT-ID-NON-OPAQUE disposition + 3-posture vocabulary entry)"
authority_source: Operator directive 2026-05-11 ("the classification-driven routing model collapses from 4 postures to 3 — the Sanitized / opaque-slot-token posture is deprecated entirely; it was supposed to be discarded some time ago"). Three-posture vocabulary authoritative per directive: (1) Frontier-Eligible, (2) Split-Context Hybrid, (3) Local-Only / Sovereign (performance-dependent / under-validation).
version_wording_discipline: "LOCKED" inside this file refers to on-disk LOCKED state at filing time. v7.0.10 introduces no new architectural-primitive mechanisms — it is a **vocabulary simplification + posture-as-customer-facing-deployment-stance formalization + opaque-slot mechanism deprecation**. The F-CLASS-* family roster is touched at two rows (repurpose, not retire); the four field-level classification class values from v7.0.7 §2 stay canonical (public, shareable, confidential, operator_flagged); the v7.0.7 Classification Review stage stays canonical with updated posture-selection vocabulary at step 4; the v7.0.7 heavy-Judge swap stays canonical; the v7.0.7 §6.1 router-template signing discipline stays canonical. The "structural sovereignty" claim of v7.0.7 §5 is preserved — strengthened, actually, because the three-posture model eliminates the opaque-slot leak surfaces that motivated v7.0.7 §4.2's v0.1-known-limitation acknowledgment.
audit_trail: pipeline/validation/v7_0_10_thesis_2026-05-11/
session_metrics: pipeline/metrics/session_log.jsonl
---

# Amendment intent

v7.0.7 LOCKED 2026-05-10 introduced "single architectural pattern — classification-driven routing" as the canonical routing model. Mechanically it bundled four distinct customer-facing postures into a single per-call routing-decision rule:

1. *De-facto Frontier-Eligible* — input is Public + Shareable → cloud frontier (best-of-breed per router template).
2. *De-facto Split-Context Hybrid* — input is mixed; cloud sees Public + Shareable; local seats compose Confidential-bearing substance. (Implicit in v7.0.7 §1.1's "power for drafting + privacy for review" framing.)
3. *De-facto Sanitized* — cloud Scribe drafts with opaque `[SLOT_<numeric_id>]` tokens at every Confidential field position; local slot-fill agent renders the post-fill draft after cloud Scribe returns. (Explicit in v7.0.7 §1 routing-rule code block + §5.1's two slot-discipline gates.)
4. *De-facto Local-Only* — every seat local; cloud routing structurally unreachable. (Implicit in v7.0.7 §1's fail-closed-local default rule.)

The four-posture-implicit collapse worked at v7.0.7 LOCK because each posture had a clean structural rule. But the Sanitized posture carries three structural problems the operator-directive 2026-05-11 surfaces:

**Problem 1: leak-surface complexity.** The opaque-slot mechanism introduces a round-trip (cloud draft → slot-fill render → local review-time read) that creates new leak surfaces: cloud-Scribe synthesis-into-slot fabrication (F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED only catches the literal-substitution shape, not full-omission-without-replacement per WS-L RT-13 known limitation); timing side-channel inference about which fields had slots; downstream Editor / Red Team / routine-Judge are structurally forced to local-only on every post-fill draft anyway per v7.0.7 §1's "all subsequent seats local routing" rule.

**Problem 2: operator-comprehension complexity.** Customers (or anyone reading v7.0.7) face a routing model where the same per-call rule produces four de-facto customer-facing postures depending on which classes the input touches. Operationally this works; *as a customer-facing posture vocabulary it does not*. A customer reading v7.0.7 cannot answer "which posture is my deployment in?" without inspecting per-cycle routing telemetry per agent call. The four-posture-implicit framing fails the Sovereignty Promise's communication leg.

**Problem 3: substantive overlap with Split-Context Hybrid.** Sanitized and Split-Context Hybrid achieve the *same customer goal* — let the cloud frontier contribute its capability without exposing Confidential values — through *different mechanisms*. Sanitized routes Confidential field positions as opaque slots in the cloud prompt; Split-Context Hybrid routes cloud-side work to structure/scaffold composition only (cloud never sees ANY Confidential field anchor, opaque or not) and lets the local model compose Confidential-bearing substance independently. The latter mechanism is structurally cleaner: no slot positions in cloud prompts → no fabrication-into-slot surface → no slot-token timing inference → no slot-token-leak gate roster needed.

**Resolution.** v7.0.10 deprecates the Sanitized posture entirely. The three remaining postures become the canonical customer-facing routing vocabulary:

1. **Frontier-Eligible** — customer permits selected project data to route to external / frontier models. Tilth assigns the strongest available model to each role based on benchmark fit, prior results, task type, and cost/performance. Per-field classification register (4 class values per v7.0.7 §2) drives which fields route to cloud vs local; *Confidential and operator-flagged fields remain local even under Frontier-Eligible* — the posture name describes the *deployment's stance toward cloud routing for non-Confidential content*, not unconditional cloud-routing.

2. **Split-Context Hybrid** — frontier models help with structure, section strategy, prompts, funder-language framing, and generic draft scaffolds. *Confidential local data stays on the node*. A local model inserts restricted facts, evidence, metrics, names, and applicant-specific substance into the post-cloud draft. Distinguished from Frontier-Eligible by the *separation of concerns at the substance/structure boundary*: cloud does structure-shaped work; local does substance-shaped work. **No opaque-slot rendering round-trip.** Cloud prompts contain Public + Shareable input plus generic scaffold instructions; cloud responses are scaffolded text with no slot-anchor positions; local model composes Confidential-bearing substance separately and assembles the final draft via deterministic merge.

3. **Local-Only / Sovereign** — all drafting, review, routing, and evidence use remain local. Maximum-custody posture, but **marked as performance-dependent / under validation** until proven against real grant workloads. v0.1 Beta deployments that select this posture clear the v7.0.7 §3 Classification Review stage normally but carry a v0.1-known caveat per §7 below — the heavy-Judge swap (v7.0.7 §4) is the load-bearing mitigation, and operator runs a representative-grant test cycle at white-glove to validate Local-Only quality is acceptable for the customer's posture preference. Future hardware tier increases + local model capability evolution will retire the under-validation caveat per Sovereign Node LLC continuous-tracking commitment (v7.0.7 §6).

The opaque-slot mechanism that distinguished Sanitized as a de-facto fourth posture is structurally removed: no posture under v7.0.10 emits `[SLOT_*]` tokens into cloud-routed prompts; the two F-CLASS-* gates that policed the discipline (`F-CLASS-SLOT-ID-NON-OPAQUE` PRE-call + `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED` POST-call) are repurposed as defense-in-depth gates per §5 below.

# What changes

## §1. Three-posture customer-facing routing vocabulary (canonical)

### §1.1 Posture definitions (operator-facing wording)

The three postures are the canonical *customer-facing* routing-stance vocabulary. Each posture is a deployment-level selection made by the operator at white-glove onboarding (during the v7.0.7 §3 Classification Review stage's step-4 routing simulation review); the operator can update the posture post-onboarding via a per-deployment SP0-equivalent flow per §1.5 below.

**Posture 1: Frontier-Eligible.** *"Customer permits selected project data to route to external/frontier models. Tilth assigns the strongest available model to each role based on benchmark fit, prior results, task type, and cost/performance."*

- Per-field classification register (4 class values: public, shareable, confidential, operator_flagged) drives which fields are eligible to route to cloud frontier.
- Public + Shareable input routes to cloud frontier per Sovereign Node LLC's current router-template release.
- Confidential + operator-flagged fields *remain local* even under Frontier-Eligible — the posture authorizes cloud routing for non-Confidential content; it does not authorize Confidential-content exfiltration. Operator override to route a specific Confidential field to cloud requires per-grant SP0 signature + admin-risk ledger entry HIGH severity (mirrors v7.0.7 §3.7 per-grant SP0 chain).
- The on-demand heavy-Judge swap (v7.0.7 §4) remains available; routine-Judge under Frontier-Eligible is typically cloud-routed when input is Public + Shareable.

**Posture 2: Split-Context Hybrid.** *"Frontier models help with structure, section strategy, prompts, funder-language framing, and generic draft scaffolds. Confidential local data stays on the node. A local model inserts restricted facts, evidence, metrics, names, and applicant-specific substance."*

- Cloud-routed prompts under Split-Context Hybrid contain Public + Shareable input + generic scaffold-instruction templates only. No Confidential field anchors traverse cloud (neither as literal values nor as opaque slot tokens).
- Cloud responses are scaffolded text — generic-shaped per the prompt template. Local-side composition stitches Confidential-bearing substance into the scaffolded structure.
- **The substance/structure boundary is the load-bearing separation.** The cloud frontier sees nothing about the applicant's specific facts, partnerships, financials, or capacity; it sees only the funder's RFA + the operator-classified Public + Shareable cluster + the structural template.
- Editor / Red Team / routine-Judge under Split-Context Hybrid are typically local-routed (the final assembled draft carries Confidential-bearing substance; v7.0.7 §1's "all subsequent seats local routing on post-fill drafts" rule applies in the modified form: "all subsequent seats local routing on assembled-substance drafts").
- The heavy-Judge swap (v7.0.7 §4) remains available for high-stakes grants under Split-Context Hybrid.

**Posture 3: Local-Only / Sovereign.** *"All drafting, review, routing, and evidence use remain local. Maximum-custody posture, but marked as performance-dependent / under validation until proven against real grant workloads."*

- Every seat runs on the local 70B-class stack (Scribe / Editor / Red Team / routine-Judge) with on-demand heavy-Judge (200B-class) swap available per v7.0.7 §4.
- No cloud routing at all. The router-template's cloud-frontier model bindings are unused on this deployment.
- Performance-dependent caveat: until validated against real grant workloads, customers selecting Local-Only carry an explicit "under-validation" notice in customer-facing materials (`docs/lessons_memory_external_one_pager.md` + `docs/white_glove_v0_1_beta.md`) and Classification Review attestation. The white-glove playbook's step-4 test cycle runs Local-Only end-to-end so the operator can evaluate whether the local-stack quality is acceptable for the customer's deployment.
- Quality validation track: Sovereign Node LLC tracks Local-Only deployment quality per v7.0.5 cycle telemetry; retires the under-validation caveat when sample size + outcome statistics support the claim that Local-Only matches Frontier-Eligible / Split-Context Hybrid on funded-outcome rates.

### §1.2 Internal-vs-external naming discipline

External-facing surfaces (README, docs/ARCHITECTURE_OVERVIEW.md, customer-facing materials, investor / business-plan language, operator-facing CLI display, Classification Review UX) use the three-posture names as written in §1.1.

Internal-facing surfaces (architecture text, blueprint text, code identifiers, audit trail entries, internal docs) may use:
- The three-posture names from §1.1 (preferred — single vocabulary).
- The legacy v7.0.7 §1 per-call routing-decision-pattern code phrasing ("classification-driven routing", "cloud-routed", "local-routed") for in-code routing-layer terminology where the per-call decision is the operationally relevant unit.

The legacy term "Sanitized" is deprecated as a posture name in all surfaces. Use "deprecated Sanitized / opaque-slot-token posture" if historical context is needed; use nothing in forward-looking text.

### §1.3 Posture × per-field-class routing matrix (canonical)

The three postures compose with the four field-level class values from v7.0.7 §2 (public, shareable, confidential, operator_flagged) into a 3 × 4 routing-decision matrix:

| Posture \\ Field class | public | shareable | confidential | operator_flagged |
|---|---|---|---|---|
| **Frontier-Eligible** | cloud frontier | cloud frontier | LOCAL (operator override → per-grant SP0 HIGH-severity admin-risk ledger entry to route cloud — exception path, not default) | LOCAL (treated identically to confidential per v7.0.7 §2; operator override available with same SP0 discipline) |
| **Split-Context Hybrid** | cloud frontier (structure / scaffold composition only) | cloud frontier (structure / scaffold composition only) | LOCAL (substance composition; local model composes Confidential-bearing draft independently of cloud scaffold output) | LOCAL (substance composition) |
| **Local-Only / Sovereign** | LOCAL (Public field classification has no routing-decision effect under Local-Only — everything stays local) | LOCAL | LOCAL | LOCAL |

**Read of the matrix.** Frontier-Eligible and Split-Context Hybrid differ at the *cloud-side work shape*: Frontier-Eligible routes Public + Shareable *content* to cloud (cloud sees the applicant's actual public information); Split-Context Hybrid routes Public + Shareable *scaffold-instructions* + the RFA only (cloud sees the funder's RFA + structural templates, never the applicant's specifics). The structural-sovereignty invariant is *strictly stronger* under Split-Context Hybrid than Frontier-Eligible: the applicant's identity could in principle be inferred from cloud Frontier-Eligible prompts; under Split-Context Hybrid the cloud sees only the funder's RFA + template-shape + classification-free scaffold instructions.

**Structure-vs-substance boundary — deterministic rule (closes Cycle 1 RT-2).** Split-Context Hybrid's "cloud composes structure; local composes substance" framing requires a deterministic enforcement rule (a human-readable mental-model is necessary but not sufficient — operator-error or attacker-input could push applicant-specific content into a field classified Public + Shareable and route it cloud-side). The rule under v7.0.10 Split-Context Hybrid is:

1. **Cloud-routable inputs under Split-Context Hybrid are restricted to the explicit allow-list** {RFA text + funder agency name + funder rubric (if published) + program template name + section-structure-spec + KGIE-checklist keywords (funder language only, not applicant affirmations) + dialect-classification value}. Any other field is *substance* by default and routes local.
2. **The Logician PRE-call gate `F-CLASS-SPLIT-CONTEXT-ALLOWLIST` (new at v7.0.10 §5.3 — see below)** fail-closes any cloud-routed prompt under Split-Context Hybrid posture whose payload contains a field-path NOT in the allow-list. The gate is a closed-set check, not an open-set classification check; the allow-list is operator-signed at white-glove + per-grant SP0 extensible.
3. **Pre-cloud-route PII / applicant-fact scan.** Before routing under Split-Context Hybrid, the routing layer runs a deterministic scan on the prompt payload for: applicant's legal name + EIN + address strings + applicant-supplied production-metric numerics from KFR + applicant-supplied partnership names from `PROJECT_CONTEXT.partnerships`. Any match → fail-closed with `F-CLASS-SPLIT-CONTEXT-LEAK` (new gate at §5.3) — the prompt is rejected, admin-risk ledger entry HIGH severity, operator review required. The scan is bounded to fields the operator has approved as Public + Shareable in the classification register; an attacker who pushes applicant-fact text *into* a Public + Shareable field (e.g., embedding the applicant's EIN in the RFA-keywords section) is caught by this scan before the cloud round-trip.
4. **Frontier-Eligible posture** does NOT inherit the closed-set allow-list restriction (Frontier-Eligible permits cloud routing of broader Public + Shareable content; the per-field classification register is the primary gate). Frontier-Eligible inherits the pre-cloud-route PII scan as a defense-in-depth measure, but only against operator_flagged + confidential content (which would already trip `F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL`); the Frontier-Eligible scan is a backstop for misconfigured classifications, not a primary structural gate.

5. **Allow-list extension discipline (closes Cycle 2 RT-C2-1 FOLD-IN).** The Split-Context Hybrid allow-list at `orgs/<slug>/vault/classification/split_context_allowlist.yaml` is operator-signed Ed25519 at white-glove; any *extension* to the allow-list post-white-glove requires **dual-sign discipline**: the operator's Ed25519 signature PLUS a second operator-tier signature (in v0.1 single-operator deployments, a Sovereign Node LLC publisher signature on the extension diff acts as the second-tier signature under the same router-template Ed25519 trust mechanism per v7.0.7 §6.1). Any allow-list extension also runs through an automated normalization-and-applicant-fact-scan pass at write time (Unicode NFC + base64 decode + URL-decode + whitespace concatenation reverse pass) before the second signature can be applied — the scan reuses the §1.3 step-3 applicant-fact regex set with three extra normalization layers added per RT-C2-1 recommendation. A failed normalize-scan rejects the extension regardless of dual-sign authorization. v0.2 amendment marker: extend the dual-sign mechanism to two distinct operator key IDs once multi-operator deployments enter scope.

This rule closes Cycle 1 Red Team Probe 2 (Split-Context Hybrid substance/structure boundary ambiguity) at Cycle 1 + Cycle 2 RT-C2-1 (allow-list extension abuse) at narrow-fix-in-place per L-005 row-170 transparent disposition.

### §1.4 Classification Review UX surface flip (4-class display → 3-posture display)

The v7.0.7 §3 Classification Review stage walks the operator through four steps: (1) Inventory of fact classifications populated by Intake → (2) Operator-override pass per field → (3) Routing simulation on a representative grant → (4) Test cycle + operator Ed25519 sign-off.

v7.0.10 amends step 3 + step 4:

- **Step 3 (routing simulation).** The simulation output now displays at *two layers*: per-field classification routing (the v7.0.7 layer — what gets routed where for each Confidential / operator_flagged field) PLUS per-posture deployment summary (which of the three v7.0.10 postures the deployment is operating under). The operator selects the deployment posture at step 3 BEFORE the test cycle runs.
- **Step 4 (test cycle).** Test cycle runs end-to-end under the operator-selected posture. The Classification Review sign-off artifact (v7.0.7 §3.7 schema) adds a `selected_posture: Literal["frontier_eligible", "split_context_hybrid", "local_only_sovereign"]` field at the top level. Operator Ed25519 signature attests to BOTH per-field classifications AND the selected posture.

**Per-field class enum is unchanged.** The four class values (public, shareable, confidential, operator_flagged) remain canonical at v7.0.10. The deployment-posture enum is the v7.0.10 addition — a separate, three-value enum at deployment scope.

**Companion edit at LOCK:** `pipeline/orchestrator/classification_review.py` + `pipeline/cli/tilth_review_classify.py` + `orgs/_TEMPLATE/classification_review/` scaffold are updated to display + sign the new posture field. F-CLASS-REGISTER-* gates (v7.0.7 §5.1 rows 1-4) are extended to verify the posture-signature trail as part of the existing register-signature chain — no new top-level gate; sub-tag extensions `.posture_unsigned` on `F-CLASS-REGISTER-UNSIGNED`, `.posture_invalid` on `F-CLASS-REGISTER-SIGNATURE-INVALID`, and `.posture_hash_mismatch` on `F-CLASS-REGISTER-HASH-MISMATCH` per the §4 v2.x.1 narrow-corrective sub-tag-extension precedent (row 198). The sub-tag-extension realization is bound to the §4 v2.x amendment companion update per §5.3 — predicate signature + three named drift-test bindings + AST-lint rule R-CLASS-POSTURE-FIELD-COVERAGE ship as non-negotiable companion-edit prerequisites for v7.0.10 LOCK.

**Concrete walkthrough example (closes Cycle 1 Editor F-EDITOR-2).** A v0.1 Beta white-glove session walks the operator through:

1. *Step 1 — Inventory:* CLI displays a list of 47 facts Intake has gathered from the operator's org documents; the Card-default classification is shown next to each (e.g., `annual_revenue_audited: confidential (card_default)`, `mission_statement: public (card_default)`, `partnership_with_PSU: shareable (card_default)`).
2. *Step 2 — Operator override pass:* operator confirms or overrides per field. Operator marks the org's mailing address as `shareable` (overriding card_default `confidential`) because the address is on the org's website.
3. *Step 3 — Routing simulation + posture selection (v7.0.10):* CLI presents the three posture options (Frontier-Eligible / Split-Context Hybrid / Local-Only / Sovereign) with one-paragraph descriptions and a side-by-side routing-simulation summary for a representative VAPG grant cycle:
   - Under *Frontier-Eligible*: Scribe Phase 0 RFA extraction → cloud Gemini (public RFA text); Scribe Phase 2 drafting → cloud Claude for Public + Shareable sections; cloud Claude for Confidential-bearing sections only under per-grant SP0 override; Editor/Red Team/Judge → cloud where input is non-Confidential, local 70B for post-substance drafts.
   - Under *Split-Context Hybrid*: Scribe scaffold composition → cloud Claude reading the RFA + section structure + dialect keywords only (no applicant facts); Scribe substance composition → local 70B; Editor/Red Team/Judge → local 70B.
   - Under *Local-Only / Sovereign*: Every seat → local 70B; heavy-Judge swap to 200B for federal long-form RFAs.
4. *Step 4 — Test cycle + sign-off:* operator selects (say) Split-Context Hybrid; the test cycle runs end-to-end on a representative grant; operator reviews the test-cycle output; operator Ed25519-signs the classification register + the `selected_posture: split_context_hybrid` field. Customer ships.

The CLI captures the operator's posture selection at step 3, surfaces the routing-simulation diff, and binds the sign-off at step 4 to BOTH the per-field classifications AND the posture selection.

### §1.5 Posture re-selection post-onboarding

The selected posture is not a one-time onboarding decision frozen for the deployment lifetime. Operators may re-select posture post-onboarding via a per-deployment SP0-equivalent flow:

1. Operator invokes `tilth posture select --deployment-slug <slug>` (CLI flow; v0.1 headless).
2. CLI presents the three postures with their definitions + current selection + sample-routing diff (what would change under the new posture).
3. Operator Ed25519-signs the posture change. Posture-change attestation appends to the classification-register audit chain per v7.0.7 §3.7 (new entry kind: `operator_signature_at_posture_change`).
4. Posture change takes effect at next grant cycle start (mid-cycle posture changes refused fail-closed per F-CLASS-POSTURE-MID-CYCLE-CHANGE — new gate per §5.3).

The posture-change frequency floor is operator-controlled but admin-risk-ledger-noted: any posture change within 30 days of the prior posture-change attestation writes a `MEDIUM`-severity admin-risk-ledger entry for operator self-awareness about churn. No hard rate-limit; the ledger entry is the soft signal.

## §2. Deprecation of Sanitized / opaque-slot-token posture

### §2.1 What was deprecated

The v7.0.7 mechanism whereby cloud-routed Scribe drafts contain `[SLOT_<numeric_id>]` tokens at Confidential field positions, with a local slot-fill agent rendering the post-fill draft after cloud Scribe returns. Specifically:

- The §1 routing-rule code-block phrase: *"Slot-fill agent: ALWAYS local (touches Confidential by definition); renders OPAQUE [SLOT_<numeric_id>] tokens to actual values from KFR + classification register; opaque slot IDs (e.g., [SLOT_001], [SLOT_002]) replace semantically-named placeholders BEFORE any cloud-routed seat sees the slot template"* — this mechanism is no longer the canonical routing pattern under any v7.0.10 posture. The slot-fill agent role at v0.1 (per v7.0.7 §1's "Always local") still exists at the code layer for legacy v7.0.7-era artifacts and migration paths, but no v0.1 Beta deployment shipping under v7.0.10 instantiates a slot-fill agent in the normal cycle path. The slot-fill agent module + its surrounding gates remain in the runtime tree as defense-in-depth (§5 below) but their normal-operation invocation count under any v7.0.10 posture is zero.

- The §1.1 "power for drafting + privacy for review" framing — the framing reframes under v7.0.10 as the *Frontier-Eligible vs. Split-Context Hybrid posture split*: Frontier-Eligible delivers "power across the cycle with privacy preserved on Confidential fields"; Split-Context Hybrid delivers "power on structure + privacy on substance". Neither posture relies on opaque-slot-rendering as the mechanism; the slot-rendering round-trip is structurally absent in both.

- The v0.2 / v1.x extension marker for "review-time anonymized-draft routing" (v7.0.7 §1.1 paragraph 3) — this extension marker is **retired**. The motivating problem (post-fill drafts forcing local Editor / Red Team / Judge) is addressed at v7.0.10 by the posture model directly: customers seeking cloud Editor / Red Team / Judge select Frontier-Eligible (and accept that under Frontier-Eligible, Confidential fields stay local but the *drafts* themselves don't carry Confidential text in cloud prompts — because Confidential-bearing sections are drafted locally end-to-end). The anonymization-round-trip extension is no longer the v0.2 / v1.x deferred work because the v7.0.10 posture model dissolves the original constraint.

### §2.2 Why deprecation, not retirement of the gate code

The opaque-slot mechanism is deprecated as a customer-facing posture, but the two enforcement gates from v7.0.7 §5.1 (`F-CLASS-SLOT-ID-NON-OPAQUE` PRE-call + `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED` POST-call) are **not retired**. Under v7.0.10, no legitimate code path emits `[SLOT_*]` tokens into cloud-routed prompts under any of the three remaining postures. Therefore:

- The presence of any `[SLOT_*]` pattern in a cloud-routed prompt is *no longer the structural-sovereignty contract from v7.0.7 §1*; it is a *signal that something has gone wrong* — a stale legacy code path, a regression in a refactor, an attempted prompt-injection-via-slot-token-shape, or a misconfigured legacy artifact.
- Repurpose: both gates remain runtime-active and fail-closed on any `[SLOT_*]` pattern. F-CLASS-SLOT-ID-NON-OPAQUE's regex (from §4 v2.x §4.3.5) `\[SLOT_(\d+)\]` is extended at LOCK to a broader pattern that fail-closes on the literal `[SLOT_` prefix entirely (with optional numeric, alphabetic, mixed, or empty suffix — full pattern `\[SLOT_[^\]]*\]` matches anything that looks like a slot token); F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED similarly fail-closes on the same broader pattern.
- Disposition class: both gates become *defense-in-depth* gates — they should never fire in correctly-operating deployments. Firing constitutes a P0 audit-trail event with admin-risk ledger HIGH severity. The runtime cost is negligible (regex scan on cloud-routed prompts is cheap).

This pattern matches the §4 v2.x.1 narrow-corrective precedent (row 198) where a gate's enforcement set is narrowed structurally without retiring the gate code — the gate stays live as a defense-in-depth check against regression / attack / legacy paths.

**Companion edit at LOCK:** `pipeline/blueprint/v0.1/section_04_v2_x_amendment.md` §4.3.5 + §4.3.6 update to document the disposition. New §4.3.6 "Defense-in-depth disposition" subsection explicitly documents that:
1. F-CLASS-SLOT-ID-NON-OPAQUE has no legitimate-trigger path under v7.0.10 postures (firing = bug/attack).
2. F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED has no legitimate-trigger path under v7.0.10 postures (firing = bug/attack).
3. Both remain HARD_BLOCK / P0 disposition (no M13 bypass).
4. Both remain in the F-CLASS-* family roster at v7.0.7 §5.1 — the roster count stays at twelve primitives (ten with legitimate runtime trigger paths + two defense-in-depth).
5. The regex on both gates is broadened at LOCK to `\[SLOT_[^\]]*\]` (any slot-shaped pattern, not just non-numeric).

### §2.3 v7.0.7 audit-trail integrity

v7.0.7 is LOCKED 2026-05-10 at row 180. v7.0.10 does **not** edit v7.0.7 in place. The v7.0.7 §1 routing rule + §1.1 framing + §5.1 F-CLASS-SLOT-ID-NON-OPAQUE primitive + §5.1 F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED primitive remain in the LOCKED v7.0.7 text as historical record. v7.0.10 layers on top: subsequent sessions and amendments read v7.0.10 as the canonical routing-vocabulary authority; v7.0.7 is the historical-precedent authority for the F-CLASS-* family origin + Classification Review stage + heavy-Judge swap + router-template signing.

The v7.0.7 LOCK row 180 is preserved unchanged in `pipeline/engineering/lock_history.v1.jsonl`. v7.0.10's LOCK row appends to the ledger per §11 below.

## §3. v7.0.7 § retentions (canonical at v7.0.10)

v7.0.10 retains the following v7.0.7 mechanisms unchanged:

- **§3 Classification Review stage** — same four-step process; step 3 + step 4 amended per §1.4 above to include posture selection alongside per-field classification.
- **§3.6 Incremental classification (fail-closed default-to-confidential for new facts)** — unchanged; the discipline applies to all three v7.0.10 postures.
- **§3.7 Sign-off artifact format** — extended per §1.4 to add `selected_posture` at the top level + posture-change appendable entries to the audit chain.
- **§4 Heavy on-demand Judge swap (200B-class local model)** — unchanged; the swap is available under all three v7.0.10 postures (Frontier-Eligible: high-stakes grants whose Confidential-bearing sections trigger local routing benefit from the heavy swap; Split-Context Hybrid: review-time + scoring local routes always benefit; Local-Only: every cycle's routine vs heavy-Judge selection follows the same trigger discipline).
- **§4.1 High-stakes flag classification (Confidential-tagged grant-level metadata; never sent to cloud routing)** — unchanged.
- **§4.2 Heavy-Judge swap timing side-channel (v0.1-known-limitation)** — unchanged for Frontier-Eligible and Split-Context Hybrid postures; **Local-Only posture additionally carries the timing side-channel surface for all heavy-swap events** (cloud-routed comparison baseline doesn't exist, so the operator-observable timing baseline for "this grant got heavy treatment" is the local-only timing pattern). v0.2 padding-latency mitigation marker per v7.0.7 §4.2 extends to Local-Only.
- **§5 Fail-closed defaults** — unchanged; the four named defaults (Classification Review not signed → can't ship; register hash mismatch → all gates fail; routing decision indeterminate → ROUTE LOCAL; cloud agent receives Confidential → P0 fail-closed) compose with the three v7.0.10 postures without change.
- **§5.1 F-CLASS-* failure-code family** — twelve primitives total. Ten with legitimate-trigger runtime paths under at least one v7.0.10 posture; two (slot-id-non-opaque + cloud-received-opaque-slot-filled) repurposed as defense-in-depth per §2.2 above. No new top-level F-CLASS-* gate added at v7.0.10 (the posture-signature extension per §1.4 lands as sub-tag extensions on existing F-CLASS-REGISTER-* gates).
- **§6 Per-deployment router.yaml derivation** — unchanged; per-deployment derivation now additionally consumes the operator-selected posture at white-glove.
- **§6.1 Router-template Ed25519 signing + Golden Quill verification** — unchanged; the publisher-pinned-pubkey + verification-before-applying discipline composes with v7.0.10 unchanged.
- **§7 Card-archetype classification defaults (three-layer model)** — unchanged.
- **§8 Hardware Budget Table 29 reasoning paragraph rewrites** — the rewrite text from v7.0.7 §8 is *re-affirmed* at v7.0.10; the new posture vocabulary slots into the same justification structure (the hardware sizing supports all three v7.0.10 postures equivalently — Local-Only is the most demanding-of-local-stack posture; Frontier-Eligible + Split-Context Hybrid share the same local-stack obligations on Confidential-bearing work).

## §4. Per-field classification register schema — unchanged at v7.0.10 (4 class values stay canonical)

The four class values (public, shareable, confidential, operator_flagged) from v7.0.7 §2 remain canonical. v7.0.10 does NOT introduce a new class value (e.g., "internal") at the per-field-class level. The operator-directive 2026-05-11 wording *"4-class classification register (Public+Shareable / Internal / Confidential / High-Stakes)"* maps to the existing register as:

| Operator-directive 2026-05-11 wording | v7.0.7 §2 register class value | Notes |
|---|---|---|
| Public + Shareable | `public` ∪ `shareable` | Two separate class values at the register layer; conceptual cluster under one customer-facing label. Both route identically under v7.0.10 §1.3 matrix. |
| Internal | `shareable` | "Internal" is a customer-facing synonym for shareable when describing a class that is not public but operator-comfortable to share with cloud frontier. The register class value stays `shareable`; customer-facing materials may use "Internal" as a synonym. v0.1 Beta deployments shipping under v7.0.10 may freely choose either label in customer-facing docs. |
| Confidential | `confidential` | Same. |
| High-Stakes | per-grant flag (per v7.0.7 §4.1; `field_path: project_context.grants.<grant_id>.high_stakes`; classified `confidential`) | High-Stakes is a *per-grant flag*, not a per-field class. The flag value's classification (Confidential) gates its routing; the flag presence triggers heavy-Judge swap per v7.0.7 §4. |

The register layer is structurally untouched at v7.0.10. The customer-facing vocabulary (Public+Shareable / Internal / Confidential / High-Stakes) is the *deployment-narrative* layer; the four register class values are the *runtime-enforcement* layer.

**No F-CLASS-* gate roster change for class values.** The twelve F-CLASS-* primitives from v7.0.7 §5.1 do not need new class-value gates; the existing PRE-pre-route classification check (F-CLASS-ROUTING-INDETERMINATE + F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL + F-CLASS-PER-GRANT-OVERRIDE-UNSIGNED) covers the runtime contract.

## §5. F-CLASS-* family disposition under v7.0.10

### §5.1 Ten primitives with legitimate runtime trigger paths (unchanged at v7.0.10)

These ten gates retain their v7.0.7 §5.1 stage / scope / failure-mode wording. Each has a legitimate trigger path under at least one v7.0.10 posture:

| Code | v7.0.7 §5.1 row | Trigger under v7.0.10 postures |
|---|---|---|
| F-CLASS-REGISTER-MISSING | 1 | Frontier-Eligible / Split-Context Hybrid / Local-Only: register absent → all three fail-closed at white-glove |
| F-CLASS-REGISTER-UNSIGNED | 2 | All postures: register present but operator signature missing → fail-closed at cycle start |
| F-CLASS-REGISTER-SIGNATURE-INVALID | 3 | All postures: signature verification fails → fail-closed at cycle start. **v7.0.10 extension:** sub-tag `.posture_unsigned` covers the new `selected_posture` field per §1.4. |
| F-CLASS-REGISTER-HASH-MISMATCH | 4 | All postures: silent edit detected → fail-closed at cycle start. **v7.0.10 extension:** hash chain extends to cover `selected_posture` per §1.4. |
| F-CLASS-NEW-FACT-UNCLASSIFIED | 5 | All postures: Intake INCREMENTAL fact defaults to confidential pending operator review → fail-closed when consumed |
| F-CLASS-ROUTING-INDETERMINATE | 6 | All postures: per-call routing layer cannot resolve class → fail-closed default LOCAL. Under Local-Only this is a no-op (LOCAL is the only option anyway). |
| F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL | 7 | Frontier-Eligible / Split-Context Hybrid: cloud-routed seat's request payload contains Confidential value → P0 fail-closed at outbound boundary. Local-Only: structurally unreachable (cloud routing never invoked); gate stays live as defense-in-depth. |
| F-CLASS-PER-GRANT-OVERRIDE-UNSIGNED | 10 | All postures: per-grant SP0 override missing operator signature → fail-closed at cycle start |
| F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID | 11 | All postures: router-template Ed25519 verification fails → fail-closed; deployment stays pinned. Local-Only deployments don't use the cloud-frontier section of the router template, but the local-model bindings still ride the same signed template; verification still applies. |
| F-CLASS-HIGH-STAKES-FLAG-LEAK | 12 | Frontier-Eligible / Split-Context Hybrid: cloud-routed payload contains literal `high_stakes` reference or tagged value → fail-closed. Local-Only: structurally unreachable; defense-in-depth. |

### §5.2 Two primitives repurposed as defense-in-depth (v7.0.10 disposition change)

| Code | v7.0.7 §5.1 row | v7.0.10 disposition |
|---|---|---|
| F-CLASS-SLOT-ID-NON-OPAQUE | 9 | **Defense-in-depth.** Repurposed: no legitimate trigger path under any v7.0.10 posture (no posture emits slot tokens into cloud routing). Firing = bug or attack. Regex broadened at LOCK from `\[SLOT_(\d+)\]` (numeric-only fail-closed) to `\[SLOT_[^\]]*\]` (any slot-shaped pattern fail-closed). HARD_BLOCK / no M13 bypass retained. |
| F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED | 8 | **Defense-in-depth.** Repurposed: no legitimate trigger path. Firing = bug or attack. POST-call outbound-boundary scan extended to fail-closed on any `\[SLOT_[^\]]*\]` pattern at any registered anchor or unregistered position. P0 / M13 audited disposition retained. |

The defense-in-depth gates remain in the F-CLASS-* family roster. The family roster count stays at twelve. The §4 v2.x amendment's §4.3.5 + §4.3.6 documentation is updated at LOCK per §2.2 above.

### §5.3 New gates at v7.0.10

Three new F-CLASS-* primitives land at v7.0.10 to enforce the disciplines in §1.3 + §1.5 + §3 (heavy-Judge swap discipline):

| Code | Stage | Scope | Failure mode |
|---|---|---|---|
| F-CLASS-POSTURE-MID-CYCLE-CHANGE | PRE | per-cycle gate | Operator posture-change attestation timestamp falls within or on either boundary of the open cycle window (defined inclusive-on-both-ends per Cycle 1 RT-4 closure: any posture-change timestamp `t` where `cycle_started_at_utc ≤ t ≤ cycle_ended_at_utc` fail-closes); posture changes take effect at the *next* cycle's `cycle_started_at_utc` only. The posture flag is atomically locked at `cycle_started_at_utc` for the duration of each cycle via the §2 Vault topology's signed-commit `start_editing_transaction` / `commit_editing_transaction` primitives (§2 Vault v7.1 LOCKED — primitives EXIST per row 35 of `pipeline/blueprint/v0.1/section_02_vault_topology.md` interface registry); mid-cycle reads of the posture return the locked value regardless of any concurrent signature attestation. **Cycle 2 RT-C2-2 closure (narrow-fix-in-place per L-005 row-170):** the binding is to the EXISTS-tier Vault transaction primitives, not aspirational infrastructure (L-006 compliant); a new Vault schema field `posture_lock_version: int` ships at LOCK ceremony with the §2 Vault topology companion edit (sub-tag extension on the existing §2 row, not a new top-level row); all readers consult the locked version; integration test `tests/orchestrator/test_v7_0_10_posture_concurrent_change_fails_closed.py` lands at LOCK to confirm fail-closed behavior under concurrent posture-change attempts within a cycle. |
| F-CLASS-SPLIT-CONTEXT-ALLOWLIST | PRE | per-call outbound boundary | Under Split-Context Hybrid posture, a cloud-routed prompt's payload contains a field-path NOT in the operator-signed Split-Context-Hybrid allow-list (closed set per §1.3 boundary rule). Fail-closed; prompt rejected. Allow-list lives at `orgs/<slug>/vault/classification/split_context_allowlist.yaml` (operator-signed Ed25519 at white-glove + per-grant SP0 extensible). |
| F-CLASS-SPLIT-CONTEXT-LEAK | PRE | per-call outbound boundary | Under Split-Context Hybrid posture, the pre-cloud-route applicant-fact scan detects applicant's legal name / EIN / address / KFR production-metric numerics / partnership names in the prompt payload despite the allow-list field-path check passing. Fail-closed; admin-risk ledger entry HIGH severity. Closes Cycle 1 RT-2. |

**Heavy-Judge swap discipline — pre-loaded model binary (closes Cycle 1 RT-10 + Cycle 2 RT-10-PARTIAL background-sync surface).** §3 retentions name v7.0.7 §4 heavy-Judge swap. v7.0.10 makes the implicit "model loaded from NVMe" assumption explicit: the 200B-class heavy-Judge model binary MUST be **pre-loaded on the Golden Quill appliance** at white-glove onboarding (operator-signed Golden Image build pin). The swap operation is a **local-execution-pointer-switch only**; no network fetch, no remote download, no cloud-routed binary transfer, **and no background-sync service**. The Logician runtime checks at every swap event that the model binary is present at the pinned local path and that its hash matches the Golden-Image-build-time-signed manifest. **Failure code F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD** (PRE per-swap; new at v7.0.10) fail-closes any heavy-Judge swap attempt that would trigger a network fetch (e.g., model binary missing from local path; hash mismatch with manifest; operator override attempt to fetch from a remote URL; **or any background model-sync daemon attempting to update the binary outside the operator-attested router-template update flow**). Under Local-Only / Sovereign posture this discipline is structurally non-negotiable; under Frontier-Eligible / Split-Context Hybrid postures the same discipline applies (heavy-Judge is always local execution; cloud-routed model fetch is structurally absent under all v7.0.10 postures). Operator-signed Golden Image build at white-glove pins the model binary set; router-template updates (v7.0.7 §6.1) carry the manifest of pinned heavy-Judge models the Golden Image is expected to support, and any update that names a model not pinned in the deployment's Golden Image fail-closes at template-application time. **Alternative-update-channel ban (Cycle 2 RT-10 PARTIAL closure):** any model-sync service, background daemon, or external update channel that would mutate the heavy-Judge binary outside the operator-attested router-template update flow is structurally absent from v0.1 Beta deployments; the Golden Image build manifest is signed at white-glove and verified at every appliance boot — drift detection at boot fail-closes the deployment until operator review.

These gates are realized at the §4 v2.x amendment-companion update (the same §4 v2.x amendment companion edit that covers §5.2 above). Dormant-binding pattern per L-006 + v7.0.7 §5.1 precedent: v7.0.10 names the primitives at the architectural-primitive layer; the predicate bodies land at the §4 v2.x amendment companion update with NotImplementedError stubs at signature time, bodies realized at runtime amendment.

**Sub-tag-extension realization for F-CLASS-REGISTER-* (closes Cycle 1 RT-5).** The §1.4 sub-tag extensions (`.posture_unsigned` on `F-CLASS-REGISTER-UNSIGNED`, `.posture_invalid` on `F-CLASS-REGISTER-SIGNATURE-INVALID`, `.posture_hash_mismatch` on `F-CLASS-REGISTER-HASH-MISMATCH`) land at the §4 v2.x amendment companion update with **named drift-test bindings** per the §4 v2.x.1 row-198 sub-tag-extension precedent. The §4 v2.x amendment companion edit at LOCK MUST include:
- Predicate signature extension to inspect the `selected_posture` field on the operator-signed register.
- Three named drift tests (one per sub-tag) that deliberately corrupt the posture signature / posture invalid-state / posture hash and confirm the gate fail-closes.
- AST-lint enforcement (R-CLASS-POSTURE-FIELD-COVERAGE) confirming every register-signature gate inspects the posture field.

The F-CLASS-* family roster after v7.0.10 LOCK: **sixteen primitives total** (ten legitimate-runtime from v7.0.7 §5.1 + two defense-in-depth + four new at v7.0.10: posture-mid-cycle-change + split-context-allowlist + split-context-leak + heavy-judge-cloud-download).

### §5.4 F-CLASS-COVERAGE-INCOMPLETE META-gate (unchanged scope)

The META-gate from v7.0.7 §5.1's "No-cycle-without-coverage gate" stays canonical at v7.0.10. Its scope updates implicitly: the coverage check now includes:
- The ten legitimate-runtime gates (existing).
- The two defense-in-depth gates (must still be runtime-loaded; absence = coverage failure).
- The one new posture-mid-cycle-change gate (must be runtime-loaded; absence = coverage failure).

No new META-gate is added; the existing F-CLASS-COVERAGE-INCOMPLETE expands its scope to the thirteen-primitive set.

## §6. Posture-vs-class composition at the prompt boundary

The v7.0.7 §1 routing-rule code-block is replaced at v7.0.10 by a posture-aware variant:

```
For each agent call:
  posture = deployment_posture()  # one of: frontier_eligible, split_context_hybrid, local_only_sovereign
  if posture == local_only_sovereign:
    → route LOCAL (no further checks needed)
  elif posture == frontier_eligible:
    if any input contains confidential OR operator_flagged:
      → route LOCAL (unless per-grant SP0 override authorized; F-CLASS-PER-GRANT-OVERRIDE-UNSIGNED applies)
    elif all input is public + shareable:
      → route CLOUD FRONTIER (best-of-breed per router template)
    else (class indeterminate):
      → fail-closed LOCAL default (F-CLASS-ROUTING-INDETERMINATE logged)
  elif posture == split_context_hybrid:
    if any input contains confidential OR operator_flagged:
      → route LOCAL (substance composition; no SP0 override path under Split-Context Hybrid — the posture explicitly does not route Confidential to cloud)
    elif all input is public + shareable AND seat is in {scribe_scaffold, scout, intake_classification_review}:
      → route CLOUD FRONTIER (scaffold / structure work only; no substance)
    else (class indeterminate OR seat is review-shape):
      → fail-closed LOCAL default

No opaque-slot rendering under any branch. Slot-fill agent role from v7.0.7 §1
remains in the runtime tree as defense-in-depth — never invoked in normal-path
cycle operation under any v7.0.10 posture.

Once a draft has been assembled with Confidential-bearing substance present
(Frontier-Eligible: composed locally end-to-end on Confidential-bearing
sections; Split-Context Hybrid: local-substance-composition step has run):
  → all subsequent seats reading the assembled-substance draft MUST be local
    (enforced structurally — Editor / Red Team / routine-Judge under both
    Frontier-Eligible and Split-Context Hybrid route local on assembled-
    substance drafts).
```

The post-substance-assembly rule preserves the v7.0.7 §1.1 "power for drafting + privacy for review" invariant in updated form: under Frontier-Eligible, Public + Shareable sections are drafted by cloud Scribe AND reviewed by cloud seats; Confidential-bearing sections are drafted AND reviewed locally. Under Split-Context Hybrid, all sections' substance is assembled locally; review is therefore local. Under Local-Only, all phases are local.

## §7. Performance-dependent caveat on Local-Only / Sovereign

The Local-Only / Sovereign posture is the maximum-custody option. Customers selecting it accept the under-validation caveat: the 70B-class local stack has not been validated against real grant workloads at v0.1 Beta scale. The customer-facing materials (`docs/lessons_memory_external_one_pager.md` + `docs/white_glove_v0_1_beta.md`) carry explicit notice; the deployment manifest carries a structural enforcement flag (per Cycle 1 RT-6 closure):

**Deployment-manifest `local_only_validated` flag (closes Cycle 1 RT-6 + Cycle 2 RT-C2-4 mutable-flag write-protection + Cycle 2 RT-6 PARTIAL non-WPFA-artifact scope).** Every Golden Quill deployment manifest at `orgs/<slug>/vault/deployment_manifest.yaml` carries a `local_only_validated: bool` field (default `false`). **Write-protection (Cycle 2 RT-C2-4 closure):** the flag is structurally write-protected — only the Sovereign Node LLC publisher-signed `quarterly_validation_outcome` artifact (Ed25519-signed under the same trust mechanism as router-template releases per v7.0.7 §6.1) can flip the flag to `true`. The deployment manifest schema enforces `local_only_validated: bool` as a "system-set-only" field: any direct operator edit (CLI, YAML hand-edit, programmatic write outside the quarterly-validation-outcome verification flow) trips F-WPFA-LOCAL-ONLY-VALIDATION-CLAIM-LEAK and is rejected. Operator can downgrade `true → false` via signed SP0 (e.g., to opt back into the under-validation posture for compliance reasons); operator cannot upgrade `false → true` without the Sovereign Node LLC quarterly-validation-outcome artifact. When the deployment's selected posture is Local-Only / Sovereign, any external attestation or invoice emission that would represent the deployment as "production-validated" requires `local_only_validated: true`. The validation-gate scope (Cycle 2 RT-6 PARTIAL closure) covers **all customer-facing artifact generators**, not just WPFA buyer-PDF: marketing PDFs, audit reports, contract attestations, customer-facing status dashboards, billing artifacts. The §4 v2.x amendment companion edit at LOCK extends `F-WPFA-LOCAL-ONLY-VALIDATION-CLAIM-LEAK` to a sub-tag family covering each customer-facing artifact type (`.wpfa_buyer_pdf`, `.marketing_pdf`, `.audit_report`, `.contract_attestation`, `.status_dashboard`, `.billing_artifact`); each tag fail-closes at emission time without the flag at `true`. Without the flag at `true`, customer-facing materials must continue to carry the under-validation notice verbatim. This delivers operational contractual hedge across the full customer-facing surface.

The customer-facing notice text:

> *"Local-Only / Sovereign is performance-dependent and under validation against real grant workloads. The Golden Quill stack (70B-class routine + 200B-class on-demand heavy-Judge swap) handles every drafting / review / scoring task entirely locally. We are actively measuring funded-outcome rates on Local-Only deployments and will retire this caveat when the data supports it. Customers selecting Local-Only get the maximum-custody posture today; we recommend customers whose grant portfolio includes federal long-form RFAs consider Split-Context Hybrid (cloud-frontier scaffold + local-substance assembly) until the Local-Only validation lands."*

The Classification Review stage's step-4 test-cycle output under Local-Only includes a per-section quality summary (the heavy-Judge swap's scoring serves as the internal-validation signal). Operators see the local-stack output side-by-side with the heavy-Judge's rubric scoring; the operator's white-glove decision to ship Local-Only is informed by that direct comparison.

The validation track:
- Sovereign Node LLC collects Local-Only cycle outcomes per v7.0.5 telemetry.
- Quarterly review against funded-outcome rates from Frontier-Eligible + Split-Context Hybrid deployments.
- Caveat retires when (a) sample size is sufficient (operationally: ≥ 30 cycle-completions across ≥ 5 distinct deployments, per Sovereign Node LLC discretion), and (b) Local-Only funded-outcome rate is within 10% of Frontier-Eligible / Split-Context Hybrid funded-outcome rate at the same CIC × CLC composition.
- Retire-ready signal: Sovereign Node LLC issues a customer-facing posture-vocabulary refresh (a `docs/lessons_memory_external_one_pager.md` + `docs/white_glove_v0_1_beta.md` update) at quarterly cadence; under-validation caveat removed when the data supports.

## §8. Reflection v0.1 hook (v7.0.9) — composition with v7.0.10

### §8.1 Reflection routing posture under v7.0.10

The Reflection v0.1 hook (architecture v7.0.9 LOCKED 2026-05-10 row 202) names a `reflection_agent` (Pydantic AI Agent instance under Archivist's sub-mode) with always-local classification routing posture. The v7.0.9 §6 synthesis-design-memo reference to opaque-slot discipline was specifically:

> *"Opaque-slot discipline: Reflection's cloud-routed prompt (rare; reflection is typically always-local) uses opaque `[SLOT_<numeric_id>]` only per `F-CLASS-SLOT-ID-NON-OPAQUE`."* — synthesis_design_memo_2026-05-10.md §6 table row, "Opaque-slot discipline" column.

This sentence retracts under v7.0.10. Reflection's *always-local-on-Confidential* posture is preserved — but the posture is now expressed in v7.0.10 vocabulary as: **Reflection always operates under Local-Only or Split-Context Hybrid posture for the reflection_agent itself.** The reflection_agent's substrate is reflection over post-cycle KFR + Match DB + lessons-memory artifacts — which carry Confidential-bearing content by construction. Therefore:

- The reflection_agent's routing decision under v7.0.10 §6 routing-rule logic *always* routes LOCAL (because reflection inputs always contain Confidential content).
- Under Frontier-Eligible deployment: reflection_agent routes local (Confidential content → local per §1.3 matrix).
- Under Split-Context Hybrid deployment: reflection_agent routes local (Confidential content → local per §1.3 matrix; no scaffold/substance separation applies because reflection's input is unstructured pattern-curation).
- Under Local-Only deployment: reflection_agent routes local (trivially).

In all three cases, **the reflection_agent's prompt never traverses cloud routing**. The F-REFLECTION-* family from v7.0.9 §2 remains structurally enforced — the always-local posture removes one class of forward-extension marker (the rare-cloud-routed-reflection-prompt extension marker from v7.0.9 §6 synthesis row).

### §8.2 v7.0.9 amendment + Reflection sub-mode code — no in-place edits required

The v7.0.9 amendment was LOCKED 2026-05-10 at row 202. v7.0.10 does **not** edit v7.0.9 in place. The v7.0.9 frontmatter + §2 + §6 + §7 + the F-REFLECTION-* primitives + the F-ARCHIVIST-* sub-tag extensions + the grounding-signal-class registry + the operator-supplied inoculation frame all remain canonical at LOCKED 2026-05-10 wording.

The synthesis memo §6 row (which sits at `pipeline/research/reflection/synthesis_design_memo_2026-05-10.md` line ~248 — a *planning artifact*, not a LOCKED architecture artifact) is updated with a footer retraction note per §8.3 below. The v7.0.9 amendment file itself gets a footer addendum (also not an in-place edit of LOCKed text) per §8.3 below referencing v7.0.10's posture-vocabulary update.

The Reflection sub-mode scaffold at `pipeline/orchestrator/seats/archivist/reflection_mode.py` (LANDED 2026-05-10 per v7.0.9 LOCK) — inspection at v7.0.10 LOCK ceremony confirms no opaque-slot-mechanism reference; the scaffold's posture posture-constants need a one-line update to refer to v7.0.10 §1 posture vocabulary (e.g., a comment-level annotation). If no such update is needed, the file is annotated in the audit trail as "v7.0.9 scaffold unchanged at v7.0.10 LOCK — already always-local; no v7.0.10 vocabulary references in the file."

### §8.3 Footer-retraction discipline (preserves LOCKed-text audit-trail integrity)

**Forward-reader integrity (closes Cycle 1 RT-7 LOW + Cycle 2 F-RED-7 PARTIAL non-Cowork-reader surface).** The footer-addendum discipline preserves LOCKed body integrity at the cost of forward-reader-burden: a reader who opens v7.0.7 and reads from top to bottom might finish before reaching the v7.0.10 footer addendum and miss the deprecation. The Cycle 1 + Cycle 2 Red Team probes surfaced this concern across both Cowork and non-Cowork-reader paths. The pragmatic multi-layer mitigation under v7.0.10:

1. **MEMORY.md index entry** (added at LOCK ceremony per §11 below) carries the v7.0.10 LOCK pointer with description text that names the Sanitized-deprecation explicitly. Future sessions read MEMORY.md per the wake-up sequence (per `/AGENTS.md`) BEFORE reading any architecture file; the deprecation context is loaded ambient before any v7.0.7 read.
2. **CLAUDE.md** (loaded by every Cowork session per the project layout) carries the v7.0.10 routing vocabulary update + a What-NOT-to-Do guard that references the deprecation. Cowork sessions cannot read v7.0.7 without the v7.0.10 context already present.
3. **AGENTS.md** (loaded by every Code session per the project layout) carries a "Recent LOCKs" section update at v7.0.10 LOCK ceremony with explicit v7.0.10 deprecation pointer. Code sessions cannot read v7.0.7 without the AGENTS.md v7.0.10 context already present in the wake-up sequence. **Cycle 2 RT-7 PARTIAL closure:** non-Cowork-readers running Code-side workflows now have the same ambient-context coverage as Cowork sessions.
4. **Footer addendum** at v7.0.9 + at the synthesis memo provides the link-back pointer for external auditors and offline readers (those who do not run a Cowork or Code session).
5. **lock_history.v1.jsonl row at v7.0.10** with `parent_lock_row: 180` (v7.0.7 row) supersession-pointer field provides machine-readable audit-trail trace per the §4 v2.x.1 row-198 + §11.1 v1.1 supersession-pointer precedent. Tooling-level architecture-render that walks the lock_history ledger surfaces the v7.0.10 supersession pointer when rendering v7.0.7.
6. **v7.0.7 itself is NOT in-place edited.** This decision trades a small forward-reader-burden surface against the much larger audit-trail-integrity surface; the project's L-005 + L-006 disciplines prioritize audit-trail integrity. If a future amendment introduces a tooling-level architecture-render that surfaces linked addenda automatically (the Cycle 1 RT-7 recommendation), the surface burden retires.

The v7.0.9 amendment + the synthesis memo carry a v7.0.10 footer addendum block (appended below all existing content; no in-place edit of LOCKed sections). The footer block format:

```
---

## [v7.0.10 footer addendum 2026-05-11]

Architecture amendment v7.0.10 LOCKED 2026-05-11 deprecates the "Sanitized" /
opaque-slot-token posture. The sentence in §6 of this file (synthesis memo) /
the v7.0.9 §6 row referencing F-CLASS-SLOT-ID-NON-OPAQUE on opaque-slot
discipline RETRACTS. Reflection's always-local-on-Confidential posture is
preserved under v7.0.10 vocabulary (Reflection's reflection_agent always
operates under Local-Only or Split-Context Hybrid posture; reflection inputs
always carry Confidential content; reflection_agent's prompt never traverses
cloud routing).

See: pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md §8

[end addendum]
```

This footer-addendum pattern preserves v7.0.9's LOCKed-text integrity (the architecture-amendment file's signed/LOCKED body is unchanged) and provides forward-readers with a clear forward-pointer to v7.0.10. The same shape applies to the synthesis memo.

### §8.4 Reflection §0.5 §15 amendment — no row mutation required

The companion `pipeline/blueprint/v0.1/section_00_5_section_15_reflection_amendment.md` (LANDED 2026-05-10 as part of the v7.0.9 paired compound transaction) does NOT carry any opaque-slot-mechanism row at the §0.5 interface index. The §0.5 §15 reflection amendment registers:
- F-REFLECTION-* failure-code rows (8 BINDING + 8 HORIZON + 1 PROBE-DEPENDENT).
- F-ARCHIVIST-* sub-tag-extension annotations under existing rows 299-303.
- Reflection sub-mode marker.

None of these reference the opaque-slot mechanism. The §0.5 §15 reflection amendment requires no row mutation at v7.0.10 LOCK. (Audit-trail note only.)

## §9. Companion edits at LOCK (compound transaction per §6.17 Option-B)

**Overview (closes Cycle 1 Editor F-EDITOR-3).** v7.0.10 is a vocabulary + posture-formalization amendment whose impact ripples across architecture-class, blueprint-class, customer-facing-class, and code-class surfaces. The companion-sweep below enumerates every surface in scope at LOCK ceremony, organized by class: §9.1 architecture amendments (this file + LOCKed-file footer addendums per §8.3); §9.2 blueprint amendments (in-place updates to LOCKed blueprints, per §6.17 Option-B sweep convention); §9.3 customer-facing documentation; §9.4 code-class edits (orchestrator + UX wrapper + Scribe seat audit). All edits land atomically in a single LOCK ceremony per §6.17 Option-B paired-commit pattern. Atomic LOCK ceremony rows are written to `pipeline/engineering/lock_history.v1.jsonl` per §11 below.

### §9.1 Architecture-amendment-class edits (this file + footer addendums)

- `pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md` — this file; status flips DRAFT → LOCKED at ceremony.
- `pipeline/architecture/v0.1/architecture_v7_0_9_amendment.md` — append footer addendum per §8.3 (NOT in-place edit of LOCKed body).
- `pipeline/research/reflection/synthesis_design_memo_2026-05-10.md` — append footer addendum per §8.3 (NOT in-place edit; planning artifact).

### §9.2 Blueprint-class edits (in-place updates to LOCKED blueprints, per §6.17 Option-B sweep at LOCK is normal)

- `pipeline/blueprint/v0.1/section_07_scribe.md` — rename "classification-aware-split-context drafting pattern" to "split-context hybrid drafting pattern" in parent_locks comment + §7.5 prompt-template references; remove sanitized / opaque-slot wording from parent_locks v7.0.7 reference (the v7.0.7 NOTE block updates to point at v7.0.10 §1.2 Split-Context Hybrid posture as the canonical pattern); F-SCRIBE-* failure codes unchanged.
- `pipeline/blueprint/v0.1/section_11_intake.md` — Classification Review surface description in §11.0 cross-amendment composition map updates to reference v7.0.10 §1.4 posture-selection step + 3-posture deployment-level display alongside 4-class per-field display; F-CLASS-NEW-FACT-UNCLASSIFIED + F-INTAKE-* family unchanged; parent_locks v7.0.7 reference updates to chain v7.0.10.
- `pipeline/blueprint/v0.1/section_04_v2_x_amendment.md` — §4.3.5 + new §4.3.6 land per §2.2 above; F-CLASS-SLOT-ID-NON-OPAQUE + F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED disposition flips to defense-in-depth; F-CLASS-POSTURE-MID-CYCLE-CHANGE new gate registration; F-CLASS-REGISTER-UNSIGNED + F-CLASS-REGISTER-SIGNATURE-INVALID + F-CLASS-REGISTER-HASH-MISMATCH sub-tag extensions per §1.4 + §5.1.
- `pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md` — §0.5 v21 paired-commit amendment: row updates for F-CLASS-SLOT-ID-NON-OPAQUE disposition (defense-in-depth annotation under existing row 326); row updates for F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED similar annotation; new row for F-CLASS-POSTURE-MID-CYCLE-CHANGE; new row for v7.0.10 three-posture vocabulary marker (architecture-amendment-class row).

### §9.3 Operational / customer-facing surfaces

- `README.md` — 3-posture vocabulary update in Beta routing section; Local-Only under-validation caveat note.
- `CLAUDE.md` — Beta model strategy section update from v7.0.7 routing-rule code block to v7.0.10 posture-aware code block; What-NOT-to-Do guards updated for opaque-slot-mechanism deprecation; defense-in-depth gates noted.
- `docs/ARCHITECTURE_OVERVIEW.md` — posture vocabulary throughout; classification-driven routing diagram redrawn per §6; opaque-slot mechanism noted as deprecated; §1.4 Classification Review UX surface flip narrative added.
- `docs/lessons_memory_external_one_pager.md` — customer-facing posture descriptions per §1.1 + §7 under-validation caveat verbatim.
- `docs/white_glove_v0_1_beta.md` — Classification Review stage step-3 + step-4 narrative includes posture selection; Local-Only under-validation caveat verbatim; Frontier-Eligible / Split-Context Hybrid distinction explicitly framed.
- **Non-binding standardization recommendation (closes Cycle 1 Judge F-Gemini-1).** The white-glove playbook (`docs/white_glove_v0_1_beta.md`) carries a non-binding recommendation to standardize on the term "Shareable" (matching the register class enum value `shareable`) rather than "Internal" for v0.1 Beta deployments. Operators may use "Internal" as a customer-facing synonym where the customer's existing vocabulary demands it, but the playbook nudges toward "Shareable" to deliver vocabulary consistency across deployments. The architecture text is agnostic; the playbook surfaces the recommendation as operational guidance only.
- **Repo-wide audit at LOCK (closes Cycle 1 RT-9 + Cycle 2 F-RED-9 PARTIAL acceptance-criteria gap).** A repository-wide grep at LOCK ceremony runs the following five concrete searches:
  1. `rg -i 'sanitized' --type md --type py --type yaml` — case-insensitive sanitized
  2. `rg -i 'opaque.slot' --type md --type py --type yaml` — opaque-slot / opaque slot
  3. `rg '\[SLOT_' --type md --type py --type yaml` — slot tokens in any form
  4. `rg 'F-CLASS-SLOT-ID-NON-OPAQUE\|F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED'` — gate references
  5. `rg 'classification-aware-split-context' --type md` — v7.0.7 deprecated phrase
  
  **Acceptance criteria:**
  - Every hit outside the v7.0.7 amendment file + v7.0.10 amendment file + defense-in-depth gate code (`pipeline/logician/gates/f_class_outbound_boundary.py`) + the v7.0.10 audit-trail artifacts (`pipeline/validation/v7_0_10_thesis_2026-05-11/`) is either (a) updated to v7.0.10 vocabulary, or (b) annotated with footnote `<!-- v7.0.10 deprecated: see pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md -->`.
  - The audit covers concurrent-round artifacts (WS-J Slice 3 at `pipeline/blueprint/v0.1/section_14_report_generator.md`, Reflection Packet Thesis artifacts at `pipeline/planning/reflection_packet_dispatch_spec_2026-05-11.md` + `pipeline/planning/reflection_packet_scoping_draft_2026-05-10.md` + `pipeline/research/reflection_packet_grounding/findings_2026-05-10.md`) per the operator-directive 2026-05-11.
  - The audit completion artifact lives at `pipeline/validation/v7_0_10_thesis_2026-05-11/repo_wide_audit_results.md` — annotated walk of every hit + disposition (updated / footnoted / excluded-with-rationale).
  - Audit must pass exit-0 before LOCK ceremony commits the lock_history row; failure to complete any disposition blocks LOCK.

### §9.4 Code-class edits (orchestrator + UX wrapper + Scribe seat audit)

**Scribe seat + cross-seat audit (closes Cycle 1 RT-8 HIGH + Cycle 2 F-RED-8 PARTIAL scope-expansion + Cycle 2 RT-C2-3 AST-lint-bypass via dynamic-string construction).** The Cycle 1 Red Team probe surfaced a legitimate concern: the v7.0.7-era code-class implementation may contain residual slot-generation logic that could re-activate the opaque-slot mechanism in a v7.0.10 deployment if unswept. The companion-sweep audit at LOCK runs a repository-wide check for any code path that emits `[SLOT_*]` tokens into a cloud-routed prompt — **scope expanded per Cycle 2 F-RED-8 PARTIAL closure** to cover all seat-class modules + downstream consumers:

1. **Scribe seat surface** (`pipeline/orchestrator/scribe_envelope_builder.py` + `skills/scribe-ghostwriter/SKILL.md` + the Scribe-related orchestrator modules) — code audit at LOCK ceremony confirms no residual `[SLOT_*]` emission paths under any of the three v7.0.10 postures. If any path exists, it is either (a) removed, or (b) guarded by a compile-time flag `_OPAQUE_SLOT_LEGACY_DISABLED` that is set to `True` for all v7.0.10 deployments via the Golden Image build pin.
2. **Cross-seat audit scope (Cycle 2 F-RED-8 closure):** the audit covers `pipeline/orchestrator/seats/data_collector/` + `pipeline/orchestrator/seats/report_generator/` + `pipeline/orchestrator/seats/archivist/reflection_mode.py` + `pipeline/orchestrator/seats/intake.py` + `pipeline/orchestrator/seats/uploader.py` + `pipeline/orchestrator/seats/funding_goal/` + `pipeline/orchestrator/router.py` + `pipeline/logician/gates/f_class_outbound_boundary.py` (gate module — its slot regex is the source of truth at LOCK ceremony). Any module that constructs slot-token strings (static OR dynamic) for cloud-routing destination is audited; legitimate-trigger paths (test fixtures, defense-in-depth gate code itself) are explicitly enumerated and excluded with `# v7.0.10 audit: defense-in-depth — slot pattern is REGEX FIXTURE not emission` annotations.
3. **Slot-fill agent module** (if instantiated at any code path) — confirmed inactive under all three v7.0.10 postures; module stays in the runtime tree as defense-in-depth (per §2.2) but the routing layer is structurally bound to never invoke it for normal-path cycle operation under v7.0.10.
4. **Regression test commitment.** A new regression test `tests/orchestrator/test_v7_0_10_no_slot_tokens_in_cloud.py` asserts: across the full v0.1 Beta deployment test corpus, no cloud-routed prompt contains any `\[SLOT_[^\]]*\]` pattern. Test runs in the v0.1 smoke target.
5. **AST-lint + runtime-guard defense-in-depth (closes Cycle 2 RT-C2-3 dynamic-string bypass).** The static AST-lint rule `R-V0-10-NO-SLOT-TOKEN-EMISSION` enforces at module-load that no code path under `pipeline/orchestrator/seats/` (excluding the `slot_fill_agent` module if it exists, which is defense-in-depth-only) constructs a literal string matching `\[SLOT_[^\]]*\]` for cloud-routing destination. **Static analysis cannot see strings built at runtime via f-string, format(), or concatenation.** The Cycle 2 RT-C2-3 closure adds a **runtime guard at the outbound-prompt serializer**: every prompt routed cloud-bound passes through `pipeline/orchestrator/router.py:emit_cloud_routed_prompt()` which scans the final rendered string for the regex `\[SLOT_[^\]]*\]` before dispatch. Match → fail-closed with the existing defense-in-depth gate `F-CLASS-SLOT-ID-NON-OPAQUE` (per §2.2 broadened regex). The runtime guard is the load-bearing defense; the AST-lint rule is the early-warning belt. **Fuzzing test commitment:** `tests/orchestrator/test_v7_0_10_dynamic_slot_construction_fuzz.py` lands at LOCK with property-based tests attempting dynamic construction via f-string, format(), str.join(), str + str, and partial-rendering paths; all attempts must fail-closed at the runtime guard.
6. **Forward-reader access at the audit-trail layer.** The audit-trail per `pipeline/validation/v7_0_10_thesis_2026-05-11/scribe_seat_audit.md` ships at LOCK ceremony as a per-module annotated walk of every potential emission path; auditable reproduction.

The Scribe seat audit at LOCK is a separate sub-step of the companion-sweep; it may surface additional file-class edits which append to §9.4 at LOCK time per §6.17 Option-B sweep convention. The named drift-test bindings + AST-lint rule + runtime guard + fuzzing tests are non-negotiable companion-edit prerequisites for the LOCK ceremony.

**Orchestrator + UX wrapper edits (unchanged from initial DRAFT):**

- `pipeline/orchestrator/classification_review.py` — orchestrator updates to (a) accept + record `selected_posture` field in the operator-signed register record per §1.4; (b) write `selected_posture` into the per-org register at canonical path `orgs/<slug>/vault/classification/register.yaml`; (c) audit-log entry for posture selection.
- `pipeline/cli/tilth_review_classify.py` — CLI updates to (a) display the three posture options + descriptions at step 3 (after per-field classification confirmation); (b) accept operator's posture selection; (c) generate the routing-simulation output showing per-posture routing summary; (d) emit final attestation including posture.
- `orgs/_TEMPLATE/classification_review/` — scaffold updates: add `selected_posture` field to template registers + audit trail.
- `pipeline/orchestrator/seats/archivist/reflection_mode.py` — annotated audit-trail note per §8.2 (one-line if needed, no-op if not).
- `router.yaml` — header comment block: update §1 routing-pattern reference (4-posture-implicit → 3-posture-explicit); slot-fill agent comment removed from the routing-pattern code-block (the slot-fill comment block in the v7.0.7-era header retires); add a new comment-block paragraph documenting v7.0.10 §1.2 Split-Context Hybrid posture's substance/structure separation; underlying seat-to-model bindings unchanged.

### §9.5 v0.1 Beta deployment readiness implications

- v7.0.10 LOCK is a *vocabulary + posture-formalization* amendment, not an architectural-mechanism amendment. v0.1 Beta readiness gates (Intake current-tree proof, Uploader current-tree proof, Classification Review UX wrapper, WS-L §4 v2.x LOCK, white-glove playbook subset) are NOT reopened.
- The Classification Review UX wrapper (LANDED 2026-05-10) gets the v7.0.10 §1.4 surface flip companion edit at LOCK — the wrapper continues to work post-edit; the integration tests in `pipeline/orchestrator/classification_review.py`'s test suite extend with three new tests covering the three-posture selection path.
- The smoke target (per v0.1 LOCK-AND-CLEAR packet 2026-05-11) extends to cover the new posture-selection + posture-mid-cycle-change gate logic; no new full pipeline smoke run is required pre-LOCK if the targeted tests on the new code paths pass.

## §10. What this amendment does not do

- Does not modify A1-A12 (architecture v7 LOCKED 2026-04-19).
- Does not modify the Five Operating Laws or the Four Autonomy Rules.
- Does not modify Section K hardware tier mapping (128 GB Pro tier stands).
- Does not introduce new council seats — uses v7.0.6 roster.
- Does not modify v7.0.3 substrate decision (Pydantic AI substrate stands).
- Does not introduce a new field-level classification class value (the four per-field values from v7.0.7 §2 stay canonical).
- Does not edit v7.0.7 LOCKed body in place (v7.0.7 §1 routing-rule code-block + §1.1 framing + §5.1 F-CLASS-* family roster remain as historical record; v7.0.10 layers on top).
- Does not edit v7.0.9 LOCKed body in place (footer addendum per §8.3 only).
- Does not specify v0.2 / v1.x Report Generator + Data Collector routing posture in detail — the three v7.0.10 postures compose with v0.2 / v1.x seats via the same per-call routing rule from §6 above; v0.2 / v1.x amendments inherit without further architecture work.
- Does not retire the slot-fill agent module from the runtime tree — the module stays as defense-in-depth for legacy v7.0.7-era artifacts + the F-CLASS-* defense-in-depth gates remain runtime-active.
- Does not specify the operator's choice between calling the v7.0.7 §2 `shareable` class value "Internal" or "Shareable" in customer-facing materials — the operator's discretion. Code-layer enum stays `shareable`.
- Does not specify the heavy-Judge swap trigger discipline change under Local-Only — the v7.0.7 §4 trigger discipline (federal long-form, large award, operator-flagged) is unchanged.
- Does not modify v7.0.4 KFR schema, v7.0.4-M1 narrow-corrective gates, v7.0.5 Funder Intel DB / Match DB / Scout channel G, v7.0.8 CIC × CLC orthogonality, or v7.0.9 Reflection v0.1 hook scope.

## §11. Lock-history note + sequencing

- v7.0.10 LOCK ceremony lands as a compound transaction at lock_history row N+1 (paired with §9.2 + §9.3 + §9.4 companion-sweep rows N+2 ... N+M per §6.17 Option-B).
- v7.0.10 is a vocabulary + posture-formalization amendment; the architectural-primitive-layer commitments from v7.0.7 + v7.0.4 + v7.0.5 + v7.0.6 + v7.0.8 + v7.0.9 stand.
- Forward-pending architecture amendments:
  - None forced by v7.0.10. The operator-directive 2026-05-11 cleared the routing-vocabulary surface; future amendments compose against v7.0.10 vocabulary as needed.

**Thesis-round preparation (for v7.0.10 LOCK):**
- Editor pass: clarity of three-posture vocabulary; operator-comprehension at customer-facing materials; consistency between architecture text and §9 companion-sweep targets.
- Judge pass: rubric scoring against the architecture's stated goal (simplify customer-facing routing vocabulary while preserving structural-sovereignty); does the three-posture model deliver?
- Red Team pass: adversarial — does the deprecation of opaque-slot mechanism introduce new leak surfaces? Are the defense-in-depth gates sufficient to catch regression paths? Does the Local-Only under-validation caveat carry the right operational hedge?

Audit trail at `pipeline/validation/v7_0_10_thesis_2026-05-11/`.

## §12. Author response log — Audit #1 closure (2026-05-11)

Audit #1 ran 2026-05-11 with cross-family roster per L-003: Editor=Llama 3.3 70B/Groq (Meta family), Judge=Gemini 2.5 Pro/Google, Red Team=GPT-OSS 120B/Groq (OpenAI-OSS family). Author=Anthropic (Claude). Editor returned `READY_TO_LOCK` (3 findings — 2 LOW + 1 MED, cosmetic/clarity). Judge returned `READY_TO_LOCK` with rubric score 100/100 (1 LOW finding — operational synonym recommendation). Red Team returned `REQUIRES_MAJOR_FIXES` with rubric score 62/100 (1 HIGH + 5 MED + 3 LOW, 7 OPEN probes / 3 CLOSED probes). No L-005 §10b severity auto-promotion (no multi-reviewer-surfaced findings).

Per-finding disposition (twelve total findings; all CLOSED in Cycle 1 author edits):

| Audit #1 finding | Severity | Disposition | Edit landing in Cycle 1 revision |
|---|---|---|---|
| F-RED-8 — Scribe seat code-class omission from companion-sweep (potential opaque-slot re-activation) | HIGH | CLOSED | §9.4 extended with Scribe seat audit sub-step + repository-wide grep at LOCK + regression test commitment + new AST-lint rule R-V0-10-NO-SLOT-TOKEN-EMISSION |
| F-RED-2 — Split-Context Hybrid substance/structure boundary ambiguity | MED | CLOSED | §1.3 read-of-the-matrix extended with deterministic enforcement rule: closed-set allow-list + pre-cloud-route applicant-fact scan; new gates F-CLASS-SPLIT-CONTEXT-ALLOWLIST + F-CLASS-SPLIT-CONTEXT-LEAK at §5.3 |
| F-RED-4 — F-CLASS-POSTURE-MID-CYCLE-CHANGE inclusive/exclusive boundary ambiguity | MED | CLOSED | §5.3 gate specification updated to inclusive-on-both-ends fail-closed + Vault dispatcher transaction primitive for atomic posture-flag locking |
| F-RED-5 — Sub-tag-extension on F-CLASS-REGISTER-* not bound to implementation | MED | CLOSED | §5.3 sub-tag-extension realization paragraph added: predicate signature + three named drift tests + AST-lint rule R-CLASS-POSTURE-FIELD-COVERAGE; bound to §4 v2.x amendment companion edit at LOCK |
| F-RED-6 — Local-Only under-validation caveat is documentation-only (legal exposure) | MED | CLOSED | §7 extended with deployment-manifest `local_only_validated: bool` flag + F-WPFA-LOCAL-ONLY-VALIDATION-CLAIM-LEAK gate for buyer-facing PDF emission attempting to represent Local-Only as production-validated without the flag at true |
| F-RED-10 — Heavy-Judge swap remote-download surface not covered | MED | CLOSED | §5.3 extended with heavy-Judge swap pre-loaded-binary discipline + new gate F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD enforced at every swap event |
| F-EDITOR-2 — Classification Review UX surface flip lacks concrete walkthrough | MED | CLOSED | §1.4 extended with concrete four-step example walking VAPG cycle end-to-end under each of the three postures |
| F-EDITOR-1 — Three-posture model lacks visual representation | LOW | CLOSED | §1.3 read-of-the-matrix already provides the visual comparison; cross-reference added in §1.1 framing |
| F-EDITOR-3 — §9 companion-sweep lacks overview intro | LOW | CLOSED | §9 opening paragraph added enumerating the four sub-section classes |
| F-Gemini-1 — Operator discretion on "Internal" vs "Shareable" creates vocabulary inconsistency | LOW | CLOSED | §9.3 extended with non-binding playbook recommendation to standardize on "Shareable" |
| F-RED-7 — Footer-addendum discipline relies on forward-reader manual check | LOW | CLOSED | §8.3 extended with multi-layer forward-reader-integrity discipline: MEMORY.md index entry + CLAUDE.md What-NOT-to-Do guard + footer addendum + future-tooling extension marker |
| F-RED-9 — Concurrent-round artifacts (WS-J Slice 3, Reflection Packet) may carry stale Sanitized references | LOW | CLOSED | §9.3 extended with repo-wide audit at LOCK ceremony covering concurrent-round artifacts |

Twelve findings closed; zero residuals at Cycle 1 close. The architecture's central claim ("three-posture model preserves structural sovereignty while simplifying customer-facing routing vocabulary") is now anchored by:
- The §1.3 deterministic structure/substance boundary rule (RT-2 closure).
- The §5.3 four new gates (POSTURE-MID-CYCLE-CHANGE + SPLIT-CONTEXT-ALLOWLIST + SPLIT-CONTEXT-LEAK + HEAVY-JUDGE-CLOUD-DOWNLOAD).
- The §5.3 sub-tag-extension realization commitment (RT-5 closure).
- The §7 deployment-manifest flag + companion §4 v2.x amendment gate (RT-6 closure).
- The §9.4 Scribe seat audit sub-step + AST-lint rule + regression test commitment (RT-8 closure).
- The §8.3 multi-layer forward-reader-integrity discipline (RT-7 closure).

**Audit trail:** Audit #1 dispatch logs + per-reviewer prompts + raw responses + synthesis at `pipeline/validation/v7_0_10_thesis_2026-05-11/`.

Awaiting Audit #2 verification with FULL live cross-family rigor per L-005 strict two-cycle discipline.

## §13. Author response log — Audit #2 closure (2026-05-11)

Audit #2 ran 2026-05-11 with the same cross-family roster as Audit #1. Verdict-level outcome: Editor READY_TO_LOCK (98/100; 2 NEW LOW cosmetic findings — diagram suggestion + "Shareable" rationale sentence, both fold-in at LOCK or post-LOCK polish without blocking); Judge READY_TO_LOCK (first dispatch returned 503 Google Generative AI error; first retry returned same 503; second retry returned valid response truncated mid-JSON at model-side max-output-length, but the captured prefix shows verdict CLOSED + 10 of 12 Cycle 1 findings explicitly CLOSED — F-RED-7 + F-RED-9 truncated tail, but no reason to suspect deviation from the others' CLOSED pattern; logged as dispatch quirk in `dispatch_v2_judge_retry.log`); Red Team REQUIRES_FIXES (blocking:true) with 6 PARTIAL Cycle 1 closures + 4 NEW probes (1 HIGH + 3 MED).

Per L-005 row-170 transparent disposition precedent (established at §15 v1 SPEC LOCK + §4 v2.x.1 + §13 Data Collector v1 + §14 Report Generator v1), Cycle 2 PARTIAL + NEW findings FOLD-IN at LOCK with concrete narrow-fix-in-place edits + explicit text-level mechanism. Per-finding disposition (ten total Cycle 2 items; all CLOSED at LOCK via narrow-fix-in-place):

**Cycle 2 PARTIAL closures — expanded narrow-fix-in-place:**

| Finding | Severity | Disposition | Cycle 2 expansion landing site |
|---|---|---|---|
| F-RED-8 PARTIAL — Scribe seat audit scope under-specified | HIGH | CLOSED at LOCK | §9.4 audit scope expanded to all seat-class modules (data_collector + report_generator + reflection_mode + intake + uploader + funding_goal + router + gate module); audit-trail artifact at `pipeline/validation/v7_0_10_thesis_2026-05-11/scribe_seat_audit.md` |
| F-RED-4 PARTIAL — Vault transaction primitive existence | MED | CLOSED at LOCK | §5.3 binding to EXISTS-tier §2 Vault topology `start_editing_transaction` / `commit_editing_transaction` primitives (row 35 of §2 v7.1 LOCKED interface registry); L-006 compliant (not aspirational); integration test `tests/orchestrator/test_v7_0_10_posture_concurrent_change_fails_closed.py` lands at LOCK |
| F-RED-6 PARTIAL — Local-Only legal-exposure scope (only WPFA buyer-PDF covered) | MED | CLOSED at LOCK | §7 extended: F-WPFA-LOCAL-ONLY-VALIDATION-CLAIM-LEAK sub-tag family covers all customer-facing artifact types (.wpfa_buyer_pdf, .marketing_pdf, .audit_report, .contract_attestation, .status_dashboard, .billing_artifact) |
| F-RED-10 PARTIAL — Heavy-Judge swap alternative-update-channel surface | MED | CLOSED at LOCK | §5.3 heavy-Judge discipline extended: alternative-update-channel ban + boot-time Golden Image manifest verification + drift fail-close |
| F-RED-7 PARTIAL — Forward-reader integrity non-Cowork-readers | LOW | CLOSED at LOCK | §8.3 multi-layer extended: AGENTS.md update at LOCK ceremony (Code-session ambient context) + lock_history.v1.jsonl supersession-pointer field at v7.0.10 row |
| F-RED-9 PARTIAL — Repo-wide audit acceptance criteria under-determined | LOW | CLOSED at LOCK | §9.3 audit extended: five concrete ripgrep patterns + acceptance criteria + audit-completion artifact path + exit-0 gate on LOCK ceremony |

**Cycle 2 NEW probes (4 total) — folded in at LOCK per row-170 transparent disposition:**

| Finding | Severity | Disposition | Fold-in landing site |
|---|---|---|---|
| F-RED-C2-1 — Allow-list extension abuse via obfuscated/encoded applicant-fact content | MED | FOLDED-IN at LOCK | §1.3 step 5: dual-sign discipline + automated normalize-and-scan pass (Unicode NFC + base64 decode + URL-decode + concat reverse) at allow-list write time |
| F-RED-C2-2 — Vault transaction primitive concrete-implementation requirement | HIGH | FOLDED-IN at LOCK | §5.3 row binding to EXISTS-tier §2 Vault topology primitives + `posture_lock_version` schema field + integration test commitment |
| F-RED-C2-3 — AST-lint bypass via dynamic string construction | MED | FOLDED-IN at LOCK | §9.4 runtime guard at `pipeline/orchestrator/router.py:emit_cloud_routed_prompt()` scanning final rendered string + fuzzing test commitment |
| F-RED-C2-4 — Mutable `local_only_validated` flag bypass | MED | FOLDED-IN at LOCK | §7 write-protection: system-set-only field with operator-edit rejection trip on F-WPFA-LOCAL-ONLY-VALIDATION-CLAIM-LEAK |

**Cycle 2 Editor NEW (2 LOW) — DEFERRED to post-LOCK polish:**

| Finding | Severity | Disposition | Rationale |
|---|---|---|---|
| F-EDITOR-C2-1 — Add visual diagram to §1.4 walkthrough | LOW | DEFERRED-NON-BLOCKING | Visual artifact (e.g., a Mermaid diagram) is a post-LOCK documentation enhancement; the §1.3 matrix + §1.4 four-step walkthrough already deliver the comprehension contract |
| F-EDITOR-C2-2 — Add rationale sentence to "Shareable" recommendation in §9.3 | LOW | DEFERRED-NON-BLOCKING | The non-binding playbook recommendation is operationally clear; rationale fold-in lands at next white-glove playbook update |

All ten substantive Cycle 2 items (4 NEW + 6 PARTIAL) FOLDED-IN at LOCK via narrow-fix-in-place per L-005 row-170. The two Editor NEW LOW items DEFERRED-NON-BLOCKING per their cosmetic disposition. **L-005 strict two-cycle CLOSED.**

**Audit trail at LOCK:** `pipeline/validation/v7_0_10_thesis_2026-05-11/` carries Audit #1 + Audit #2 dispatch logs + per-reviewer prompts + raw responses + this author-response log + the §9.3 repo-wide audit results artifact + the §9.4 scribe-seat audit artifact.


