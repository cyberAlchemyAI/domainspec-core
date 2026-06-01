---
title: Tilth Architecture — Amendment v7.0.11 (Card System — DRAFT, pending L-005)
filed: 2026-05-15
operator: Josh Inklovich
amendment_status: DRAFT — LOCK-READY. Pending L-005 strict two-cycle Thesis dispatch (Editor=Llama-3.3-70B/Groq + Judge=Gemini-2.5-Pro/Google + Red Team=GPT-OSS-120B/Groq via openclaw bridge per AGENTS.md). Not authoritative until LOCK ceremony completes with audit trail at pipeline/validation/v7_0_11_thesis_<date>/ and lock_history row appended.
parent_lock: pipeline/architecture/v0.1/tilth_architecture_locked.md
parent_amendments_chain:
  - v7.0.4 (LOCKED 2026-05-09; row 178) — KFR + SP0 + Logician fact-drift family
  - v7.0.4-M1 (LOCKED 2026-05-10; row 190) — narrow-corrective post cross-family verification
  - v7.0.5 (LOCKED 2026-05-10; row 179) — Funder Intel DB + Match DB + Scout channel G + Stage-5 consent-tier on-ramp
  - v7.0.6 (SELF-LOCKED 2026-05-09) — six-seat roster + support-agent slots
  - v7.0.7 (LOCKED 2026-05-10; row 180) — classification-driven routing + F-CLASS-* dormant primitives + heavy-Judge on-demand swap + per-deployment router.yaml + SN-LLC router-template signing. CANONICAL PRECEDENT FOR L-006 DORMANT-BINDING PATTERN + BINDING-vs-HORIZON SPLIT + signed-asset publisher trust mechanism.
  - v7.0.8 (LOCKED 2026-05-08) — CIC × CLC orthogonality F-CIC-CLC-COUPLING-VIOLATION enforcement. **LOAD-BEARING PRECEDENT for §1.6 below — F-CARDS-PATTERN-READ-DURING-ELIGIBILITY extends v7.0.8's orthogonality discipline into the card runtime read path.**
  - v7.0.9 (LOCKED 2026-05-10; row 202) — Reflection v0.1 hook + F-REFLECTION-* dormant primitives
  - v7.0.10 (LOCKED 2026-05-11; row 215) — three-posture routing vocabulary. **LOAD-BEARING PRECEDENT for §1.7 below — signed cards are public/shareable by construction (the loader rejects private-org-data cards), so they ride cloud-routable seats unconditionally under all three postures.**
companion_amendments_pending_LOCK:
  - pipeline/blueprint/v0.1/section_18_card_system.md                  # §18 v1 (paired DRAFT)
  - pipeline/blueprint/v0.1/section_00_5_section_18_card_amendment.md  # §0.5 v?? paired-commit (DRAFT)
  - pipeline/blueprint/v0.1/section_04_logician_v2_x_card_hardening.md           # §4 v2.x F-CARDS-* + F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY family (DRAFT)
revised_feedback_reconciliation_2026-05-15: docs/post_alpha/post_alpha_card_system_revised_2026-05-15.md preserves the operator-blessed revised source doc. This amendment frontmatter has been updated to reflect the three resolved decisions from that revised doc: (a) `common_clc_patterns_observed` is removed entirely from the CIC schema (§6.1 resolved Option A); (b) matrix cards are forward-compat schema only with `_FORWARD_COMPAT_ONLY.md` directory marker (§6.2 resolved Option A); (c) Phase A first fixtures are `food_systems` + `operating_capacity` (§6.3 resolved Option A). The pattern-read-during-eligibility gate is named `F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY` (extends v7.0.8's F-CIC-CLC-COUPLING-VIOLATION family, not F-CARDS-*) per the revised feedback's clearer ancestry.
authority_source: Operator directive 2026-05-15 ("with Beta locked, I want to integrate as much of this ideation as possible now"). Source ideation: docs/post_alpha/post_alpha_card_system_source_doc.md (verbatim author text, preserved for reference). This amendment reconciles the source ideation against the locked architecture (v7.0.10), the locked CIC/CLC orthogonality discipline (v7.0.8), the locked Logician F-CLASS-* family format pattern (§4 v2.x), and the §0.5 interface index conventions; identifies and surfaces three decisions-pending for resolution at L-005 round (see §6 below).
section_8_pending_resolution_note: Per memory/project_capital_logic_cards_v9_state.md, the long-pending §8 Cards-vs-Cards architectural reconciliation is resolved at the visual layer (Cards wins for drawings) but the §8/architecture-lock formalization of the runtime-machine-readable layer has been outstanding. **This amendment is that §8 formalization.** LOCK of v7.0.11 closes the pending §8 row.
version_wording_discipline: "DRAFT" inside this file means "not yet LOCKED via L-005 two-cycle audit." The file shape, frontmatter, and section structure are LOCK-ready — Editor / Judge / Red Team can run the cross-family Thesis round directly against this file. Any LOCK ceremony updates this frontmatter to "amendment_status: LOCKED <date> ..." with cycle-1 + cycle-2 dispositions, appends a lock_history row, and triggers the companion-amendment paired-commit per §6.17 Option-B.
audit_trail: pipeline/validation/v7_0_11_thesis_<date>/  # populated when L-005 round dispatches
session_metrics: pipeline/metrics/session_log.jsonl
---

# Amendment intent

The architecture has carried, since pre-Alpha, two paired conceptual axes — Customer Identity Cards (CIC, applicant-side) and Capital Logic Cards (CLC, funder-side) — as visual planning assets. v7.0.8 locked the orthogonality discipline (no hardcoded CIC→CLC subset coupling; F-CIC-CLC-COUPLING-VIOLATION fail-closes). The visual cards exist at `assets/cards/customer_identification/` and `assets/cards/capital_logic/` as PNGs. The Six CICs and Eight CLCs are locked names per drawings TILTH-CIC-REVIEW-01 (2026-05-08) and TILTH-CLC-00.

**What has been outstanding** — and what `memory/project_capital_logic_cards_v9_state.md` flags as the pending §8 architecture-lock formalization — is the runtime-machine-readable layer. The visual cards are not consumed by Scout, Scribe, Judge, Logician, Archivist, Report Generator, or the model router at runtime. Their semantic content (search vocabulary, evidence schema, register defaults, admin-risk patterns, reviewer logic, reporting cadence) lives in operator memory and skill prompts, not in a signed, versioned, machine-readable artifact.

**v7.0.11 introduces the Card System.** A Card is a signed, versioned, machine-readable YAML/JSON knowledge artifact that translates a Card into executable runtime behavior. Cards are the read-side artifact consumed by every relevant seat; the visual Cards remain the human-readable communication surface.

The amendment is intentionally narrow:

- **§1 (this amendment)** defines the card as an architectural primitive — schema layer, lifecycle, loader contract, memory namespace, signed-asset publisher trust mechanism, routing-posture interaction, F-CARDS-* failure-code family roster.
- **§18 (paired blueprint section, DRAFT)** specifies the full schemas, phase sequence, milestones, testing requirements, research process, starter content requirements.
- **§4 v2.x.y (paired Logician amendment, DRAFT)** authors the F-CARDS-* predicate signatures and modules.
- **§0.5 (paired interface-index amendment, DRAFT)** registers the new entities.

All four LOCK atomically at the same `lock_timestamp_utc` per §6.17 Option-B (the compound-paired-commit pattern established by §17 WPFA + §16 Reflection Packet + §13 Data Collector + §14 Report Generator).

# What changes

## §1. Card as architectural primitive

### §1.1 Definition

A **Card** is a signed, versioned, machine-readable knowledge artifact (YAML on disk; JSON canonical-bytes for signing) that encodes the runtime semantics of one Card (one CIC or one CLC, or one CIC×CLC matrix intersection). One card per Card. Cards live under `pipeline/cards/` on disk per §18 directory layout.

A **Card** is the human-readable visual asset; a **Card** is the machine-readable runtime artifact. The naming distinction is load-bearing: any code path, prompt, or seat instruction that says "load the Card" is structurally wrong — it must say "load the Card." The visual Cards are inputs to operator and customer reasoning; cards are inputs to seat runtime behavior.

### §1.2 Card axes (binding enumeration)

Two axes are canonical at v7.0.11 LOCK:

1. **CIC — Customer Identity Card.** Applicant-side. Six canonical entries: `food_systems`, `educator`, `public_agency`, `arts_culture`, `cooperative`, `ecosystem_intermediary`. Slugs match the §0.5-pinned CIC roster.
2. **CLC — Capital Logic Card.** Funder-side. Eight canonical entries: `public_purpose_works`, `catalytic_change`, `operating_capacity`, `research_evidence`, `market_access`, `credit_underwriting`, `sponsorship_corporate`, `shared_assets`. Slugs match the §0.5-pinned CLC roster.

A third axis — **CIC × CLC matrix intersection** — is reserved at v7.0.11 LOCK as a forward-compat schema only (see §1.8 below); matrix cards remain v1.x scope and ship zero matrix content at v7.0.11 LOCK.

### §1.3 Card schema layer (architectural shape)

Each axis has its own schema:

- `pipeline/cards/_schema/cic_card.schema.json` — CIC card schema
- `pipeline/cards/_schema/clc_card.schema.json` — CLC card schema
- `pipeline/cards/_schema/matrix_card.schema.json` — matrix card schema (forward-compat, v1.x content scope)

Pydantic models mirror each JSON schema at `pipeline/cards/models.py`. Schema versions are tracked in the card body: `schema_version: "1.0-cic"`, `schema_version: "1.0-clc"`, `schema_version: "1.0-cic-clc-matrix"`. Schema evolution follows the §2 v7.x SUB_KIND_REGISTRY versioning discipline — additive non-breaking changes bump minor; field removal or semantic redefinition bumps major and triggers a paired §0.5 amendment.

Full schema field-by-field listings are at §18 (paired blueprint section).

### §1.4 Card lifecycle (binding states)

Every card carries lifecycle metadata:

```yaml
lifecycle:
  draft_status: draft | reviewed | thesis_passed | signed | loaded | deprecated
  review_status: pending | passed | changes_requested
  cross_family_thesis_status: pending | passed | failed
  signature_status: unsigned | signed | revoked
  runtime_load_status: not_loaded | loaded | disabled
```

These five states are independent. A card can be `draft_status: thesis_passed` but `signature_status: unsigned` and `runtime_load_status: not_loaded`. The loader (§1.5) enforces lifecycle-gate-to-environment correspondence.

### §1.5 Loader contract (architectural)

The loader at `pipeline/cards/loader.py` MUST, in this order:

1. Read YAML card from disk.
2. Validate against the relevant `*_card.schema.json` (CIC, CLC, or matrix).
3. Verify lifecycle state matches the deployment environment:
   - Development: `draft_status` MAY be any of `draft | reviewed | thesis_passed | signed`; `signature_status` MAY be `unsigned`.
   - Production: `draft_status` MUST be `signed`; `review_status` MUST be `passed`; `cross_family_thesis_status` MUST be `passed`; `signature_status` MUST be `signed` and the signature MUST verify against the operator-pinned Ed25519 publisher public key.
4. Reject any card that contains private-organization-specific data (architectural invariant: cards are workspace-shared knowledge; never per-org). The "private-org-data" check at the architectural layer is a structural prohibition on certain field shapes (no `org_slug`, no `client_name`, no PROJECT_CONTEXT-shaped fields). §4 v2.x.y F-CARDS-* family enforces with predicate-level checks.
5. Reject any card that encodes CIC × CLC eligibility subset coupling (per §1.6 below).
6. Resolve card to its memory namespace per §1.9 below.
7. Build the memory profile (concept graph nodes + edges) per §18 §16.
8. Register runtime defaults with the consuming seats (Scout, Scribe, Judge, Logician, Archivist, Report Generator, Model Router).
9. Record the load event in the audit log.

Loader pseudocode is normative at §18 §16.2.

### §1.6 F-CARDS-* failure-code family (extends F-CIC-CLC-COUPLING-VIOLATION discipline)

v7.0.11 introduces the F-CARDS-* family. Full predicate signatures + modules + drift tests are authored in the paired §4 v2.x.y amendment (DRAFT). Family roster (v7.0.11 LOCK content):

1. **F-CARDS-COVERAGE-INCOMPLETE** — META PRE-cycle gate. **Mode-sensitive per revised feedback §11.7:** WARN-in-development; FAIL-in-production when a required runtime component depends on a missing card field; WARN-in-production when the missing field is nonessential or explicitly marked forward-compatible. Structurally mirrors F-CLASS-COVERAGE-INCOMPLETE (v7.0.7 §5.1) and F-REPORT-COVERAGE-INCOMPLETE (§4 v2.x.3) for the coverage-completeness aspect; the WARN/FAIL bifurcation is unique to the card case because card fields vary in essentiality (a missing `search_vocabulary.core_terms` is FAIL — Scout cannot operate; a missing `nickname` is WARN — purely cosmetic). The "depends-on-missing-field" introspection mechanism is captured in a per-seat declaration registered at `pipeline/cards/loader.py` seat-defaults registration step (§1.5 step 8) — see §7 open structural question on Cedar-evaluable determinism.
2. **F-CARDS-UNSIGNED-PRODUCTION-LOAD** — production loader gate. Fails closed if a card with `signature_status != signed` is loaded in production environment.
3. **F-CARDS-SIGNATURE-INVALID** — production loader gate. Fails closed if Ed25519 signature verification fails against the operator-pinned publisher public key.
4. **F-CARDS-SCHEMA-INVALID** — loader gate. Fails closed if the card does not validate against `*_card.schema.json` for its declared axis.
5. **F-CARDS-PRIVATE-DATA-IN-CARD** — loader gate. Fails closed if the card body contains any field matching the private-org-data shape (org_slug, client_name, PROJECT_CONTEXT keys, EIN, UEI, address). Cards are workspace-shared; per-org data lives at `orgs/<slug>/` only.
6. **F-CARDS-COUPLING-VIOLATION** — extends v7.0.8 F-CIC-CLC-COUPLING-VIOLATION to the card file format. Fails closed if a CIC card declares an `eligible_clc_subset` (or any equivalent-shape field), or if a CLC card declares an `eligible_cic_subset`, or if a matrix card declares `binding_eligibility: true`. The OBSERVATIONAL ONLY label on matrix files is the only admissible posture.
7. **F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY** — runtime read-path gate. **Extends v7.0.8's F-CIC-CLC-COUPLING-VIOLATION family** (not F-CARDS-*) — the prefix carries the orthogonality ancestry. Fails closed when Scout, Scribe, Judge, or eligibility-evaluation code attempts to read matrix or historical pattern fields during opportunity eligibility, fit gating, opportunity exclusion, or ranking suppression. Allowed reader during v1.x matrix phase: Archivist, retrospectively. Possible future reader after explicit amendment: Match DB advisory layer, if and only if the result is labeled as a non-binding suggestion and cannot suppress or exclude opportunities. **Note:** since `common_clc_patterns_observed` is removed entirely from the CIC schema at v7.0.11 LOCK (§6.1 resolved Option A), this gate's primary fire surface at v0.1 Beta is schema-violation-introduction defense; matrix-read-defense activates when matrix content begins to ship in v1.x.
8. **F-CARDS-CROSS-ORG-NAMESPACE-LEAK** — memory retrieval gate. Fails closed if a request originating from `orgs:<org_slug>:*` retrieval context attempts to read a card namespace that mixes org-specific and cards-shared scopes in a single call (per §1.9 namespace rule).
9. **F-CARDS-MALFORMED-LIFECYCLE** — loader gate. Fails closed if the card lifecycle block is missing required fields, or contains values outside the binding enumerations at §1.4.
10. **F-CARDS-LOAD-IN-WRONG-NAMESPACE** — loader gate. Fails closed if the card declares one card_axis (e.g., CIC) but the loader is asked to load it into a namespace for a different axis (e.g., `cards:clc:*`).

Per L-005 round expectation, the §4 v2.x.y amendment expands this list by 0-3 entries from Cycle 1 / Cycle 2 Red Team findings; ten entries is the v7.0.11 LOCK floor.

### §1.7 Card interaction with v7.0.10 routing postures

**Cards are public/shareable by construction.** §1.5 step 4 architecturally rejects any card containing private-org-data; §1.6 F-CARDS-PRIVATE-DATA-IN-CARD enforces. Therefore signed cards have classification register value `shareable` (workspace-shared knowledge, not org-confidential), independent of the deploying customer's posture selection.

Routing implications (per v7.0.10 §1):

- **Frontier-Eligible.** Card content rides alongside any cloud-routed seat call when the call's classification permits. Scout vocabulary expansion, Scribe register-defaults application, Judge underwriting-criteria reference, Report Generator commitment-template lookup — all cloud-routable under this posture.
- **Split-Context Hybrid.** Card content rides cloud-frontier alongside the scaffold/structure work (Scribe scaffold composition, Scout fan-out generation) per v7.0.10 §1.2's closed-set allow-list. The local-side substance composition reads card content from the same on-disk source; no separate routing decision needed for the card layer itself.
- **Local-Only / Sovereign.** All card reads stay local. The card layer adds no new cloud-routing surface under this posture.

**No F-CARDS-* gate fires on routing posture per se** — the architectural property (cards are public/shareable by construction) makes them routable everywhere. The routing gates that DO apply are the existing F-CLASS-* family (v7.0.7 §5.1 + v7.0.10), which evaluate the per-call input classification independently of whether card content is present in the prompt.

### §1.8 Matrix cards (forward-compat at v7.0.11 LOCK)

The matrix axis is reserved at v7.0.11 LOCK as schema-only. Mirrors the §5 v8 report_mode track FORWARD-COMPAT pattern (`shippable_in: v1.x`; runtime dispatch raises `F-CARDS-MATRIX-NOT-SHIPPABLE` until the future LOCK flips the flag).

Matrix cards, when populated at v1.x, are advisory-only: `binding_eligibility: false` is the only admissible value (F-CARDS-COUPLING-VIOLATION enforces). Matrix observations can be used by the Match DB as a ranking signal but never as an eligibility gate.

Zero matrix cards ship at v7.0.11 LOCK. The schema exists for forward-binding consistency.

### §1.9 Memory namespace layer (architectural)

Card content lives in a workspace-shared memory namespace, distinct from per-org namespaces:

```
cards:cic:food_systems
cards:cic:educator
cards:cic:public_agency
cards:cic:arts_culture
cards:cic:cooperative
cards:cic:ecosystem_intermediary
cards:clc:public_purpose_works
cards:clc:catalytic_change
cards:clc:operating_capacity
cards:clc:research_evidence
cards:clc:market_access
cards:clc:credit_underwriting
cards:clc:sponsorship_corporate
cards:clc:shared_assets
cards:matrix:<intersection_id>     # forward-compat per §1.8; zero entries at LOCK
```

**Per-intersection matrix namespace.** The source ideation proposed a single `cards:matrix:cic_x_clc` namespace; v7.0.11 normalizes this to `cards:matrix:<intersection_id>` (e.g., `cards:matrix:food_systems__market_access`) to enable per-pair retrieval, mirroring the per-pair file layout at §18 §7. The single-namespace form was an internal inconsistency in the source ideation; the per-intersection form is correct.

**Law 3 cross-org isolation interaction.** A request originating from `orgs:<org_slug>:*` retrieval context MAY read from:

- `orgs:<same_org_slug>:*`
- `cards:cic:*`
- `cards:clc:*`
- `cards:matrix:*`
- `tilth:rubrics`, `tilth:funders`, `tilth:programs`, `tilth:lessons`, `tilth:forms`, `tilth:policy`

A request from `orgs:<org_slug>:*` MUST NOT read from `orgs:<different_org_slug>:*` (Law 3, unchanged from prior locks). A single retrieval call MUST NOT mix `cards:*` and `orgs:<org_slug>:*` scopes opaquely — it must declare each namespace explicitly. F-CARDS-CROSS-ORG-NAMESPACE-LEAK (§1.6 #8) enforces.

### §1.10 Signed-asset publisher trust mechanism

Cards are signed by an operator-controlled Ed25519 publisher key, following v7.0.7 §6.1's router-template signing discipline byte-for-byte (and §17 v1 §17.6's Coefficient Registry signing discipline). The trust mechanism:

- **Publisher private key** lives on the operator's secure key store (offline-signing-capable; never on the Golden Quill appliance).
- **Publisher public key** is white-glove-pinned at appliance setup, written to a manifest at `appliance/publisher_pubkey.signed.yaml`, write-protected post-pin, and verified at boot-time per the v7.0.7 §6.1 boot-time-manifest-verification pattern.
- **Signing canonical bytes**: card YAML → canonical-JSON byte sequence (deterministic key ordering, no signature fields included) → Ed25519 sign → signature written to card `lifecycle.ed25519_signature`.
- **Verification at load**: production loader reads canonical-JSON bytes from card body, verifies signature against pinned publisher pubkey, fail-closes F-CARDS-SIGNATURE-INVALID if verification fails.

Publisher key rotation follows v7.0.7 §6.1 rotation-window watcher pattern; cards signed under prior pubkey versions remain valid for a configurable rotation window after pubkey rotation, then must be re-signed.

# §2 — Section 8 pending-reconciliation: CLOSED at v7.0.11 LOCK

Per `memory/project_capital_logic_cards_v9_state.md`, the §8 architectural reconciliation between Cards (visual) and Cards (runtime) was resolved at the visual layer but the §8 architecture-lock formalization remained pending. **v7.0.11 LOCK is that §8 formalization.** The pending row in the v9_state memory file flips to resolved when v7.0.11 enters lock_history.

# §3 — Heavy-Judge swap interaction (v7.0.7 §4)

The on-demand heavy-Judge swap (200B-class local model loaded for federal long-form / large award / operator-flagged grants) consumes CLC card underwriting-criteria + scoring-weight-patterns identically to routine-Judge. Card load is one-time-per-cycle; the heavy-Judge swap does not re-load. F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD (v7.0.10 §1.4) is unaffected — cards are static on-disk artifacts shipped with the Golden Quill appliance + publisher-signed update channel; no network fetch occurs at swap time.

# §4 — Section 0.5 paired-commit (DRAFT shape)

A new §0.5 amendment row family registers:

- **cards** (top-level kind) — directory family with five sub-axes: `cic`, `clc`, `matrix`, `_schema`, `_models`.
- **cards:cic:<slug>** — six rows, one per CIC.
- **cards:clc:<slug>** — eight rows, one per CLC.
- **cards:_schema:<axis>** — three rows (cic, clc, matrix).
- **cards:_models** — one row (pipeline/cards/models.py).
- **cards:loader** — one row (pipeline/cards/loader.py).
- **F-CARDS-* family** — ten rows (per §1.6), each a `failure_code` kind.

Total runtime-live row count: 28 (excluding any v0.2 / v1.x extension paths). §0.5 v?? paired-commit lands at the same `lock_timestamp_utc` as this amendment per §6.17 Option-B.

# §5 — v0.1 Beta vs. v0.2 / v1.x binding (explicit version-arc mapping)

The source ideation labels this work "Post-Alpha" — a fuzzy term that doesn't bind to the locked version-arc vocabulary. v7.0.11 LOCK normalizes:

- **v0.1 Beta scope (lock-and-clear active 2026-05-11):** §1 (architectural primitive), §18 §A (schema + directory + Pydantic models + schema validation CLI + two starter fixture stubs), §1.6 F-CARDS-* family roster + module skeletons, §1.9 memory namespace registration in the existing memory layer, §1.10 publisher signing infrastructure (mirrors v7.0.7 §6.1 patterns already in the v0.1 codebase).
- **v0.2 first wave scope:** §18 §B runtime context injection (CardRuntimeContext + Scout/Scribe/Judge/Logician/Report Generator wiring), §18 §C memory integration full wiring, §18 §D research dispatch pipeline (Paul's research skill or equivalent producing card content for the 14 cards), F-CARDS-* predicate bodies graduated NotImplementedError → LIVE.
- **v1.x scope:** §18 §E UI exposure (Funding Profile, Funding Logic, etc. — requires the not-yet-shipped v1.x UI surface; v0.1 is headless), §18 milestone 5 matrix card content, §18 milestone 6 outcome learning loop, optional pattern-signal cross-Tilth sharing per Sovereign Node commons consent tiers.

This split is binding at v7.0.11 LOCK. Source-ideation "Post-Alpha" language is preserved in the source doc reference but does not appear in the canonical amendment / blueprint files.

# §6 — RESOLVED DECISIONS (revised feedback 2026-05-15 PM)

The three operator decisions flagged in the morning DRAFT are **resolved in the revised feedback PDF** (preserved at `docs/post_alpha/post_alpha_card_system_revised_2026-05-15.md`). Resolutions baked into this amendment:

### §6.1 RESOLVED — `common_clc_patterns_observed` field on CIC cards → **KILLED**

The field is removed entirely from the CIC card schema. CIC cards MUST NOT include `common_clc_patterns_observed` or any equivalent field that embeds CLC preference, frequency, win-rate, or recommended pairings inside the CIC itself. Observed CIC × CLC pattern knowledge belongs only in future Archivist lessons memory + forward-compatible matrix files (v1.x), never in CIC cards.

Rationale: the field's existence would invite the exact category error it claims to disclaim — Scout / Scribe / Judge would deprioritize observationally-rare CIC×CLC pairs at runtime even under the OBSERVATIONAL-ONLY label. Schema-level removal is structurally cleaner than a runtime read-fence and is what the revised feedback adopts.

`F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY` remains in the gate family roster as defense-in-depth against any future re-introduction (§1.6 #7) and as the runtime gate that will fire when matrix content begins shipping in v1.x.

### §6.2 RESOLVED — Matrix cards → **FORWARD-COMPAT SCHEMA ONLY, ZERO CONTENT AT v7.0.11 LOCK**

Matrix schema lands at v7.0.11 LOCK as forward-compat shape per §1.8 + §18 §9. `pipeline/cards/matrix/` directory contains exactly one explanatory file at LOCK: `pipeline/cards/matrix/_FORWARD_COMPAT_ONLY.md` and the schema at `pipeline/cards/matrix/_schema/card_matrix.schema.json`. Zero matrix cards ship at LOCK. v1.x explicit amendment authorizes content population.

Matrix files MUST carry `status: "FORWARD_COMPAT_ONLY"` and `binding_eligibility: false`. Loader fails closed (F-CARDS-COUPLING-VIOLATION-EXTENSION) on any attempt to ship populated matrix content before the v1.x amendment lands.

### §6.3 RESOLVED — Phase A first fixtures → **`food_systems` (CIC) + `operating_capacity` (CLC)**

Confirmed. Rationale: `food_systems` matches FIT Farms LLC's customer identity directly; `operating_capacity` is a CLC FIT Farms plausibly engages. Both fixture stubs ship at v7.0.11 LOCK as schema-valid but content-incomplete (every required content field carries `_note: "NEEDED — research or review"`); Paul's research dispatch populates them in v0.2 Phase D.

# §7 — Resolved decisions (post-2026-05-15-PM operator review)

Three open questions from the morning DRAFT carried into the operator review session were resolved:

**§7.1 Publisher key rotation → mirror v7.0.7 §6.1 byte-for-byte.** Cards share the publisher Ed25519 signing discipline with router-templates (v7.0.7 §6.1) and the Coefficient Registry (§17 v1 §17.6). No parallel rotation cadence; one operator-pinned publisher key family, one white-glove-pinned pubkey manifest, one boot-time verification path, one rotation-window watcher. Reuses the trust machinery already proven across two prior families. Operator directive 2026-05-15 PM.

**§7.2 CIC-06 display name → keep slash form AND add `display_name_short` field.** The CIC card schema gains a new optional `display_name_short` field. CIC-06's `display_name` retains "Ecosystem Intermediary / Regenerative Systems Supplier"; its `display_name_short` carries "Ecosystem Intermediary" for downstream consumers that cannot safely render slashes (audit-log canonical-bytes formatting, future Match-DB grid display, terminal-pipeline-CLI table rendering). Slug-level (`ecosystem_intermediary`) is unaffected. Other five CIC cards set `display_name_short == display_name` (or omit the field entirely, in which case the loader resolves it to `display_name`). Operator decision 2026-05-15 PM, "ok? not sure" — resolution: cover both shapes structurally so downstream consumers never face a slash-ambiguity decision.

**§7.3 `F-CARDS-COVERAGE-INCOMPLETE` introspection → per-seat dependency registry at loader step 8, NOT Cedar-evaluable runtime introspection.** Per operator directive 2026-05-15 PM ("whatever is best most solid most reliable most honest least error pronne"). Each consuming seat (Scout / Scribe / Judge / Logician-as-consumer / Archivist / Report Generator / Model Router) declares its card-field dependencies in a static registry at `pipeline/cards/seat_dependencies.py` (the `SEAT_CARD_FIELD_DEPENDENCIES` `MappingProxyType` constant). Loader step 8 (per §1.5) reads this registry and registers per-seat dependencies with the F-CARDS-COVERAGE-INCOMPLETE gate at startup. AST-lint rule `R-CARDS-SEAT-DEPS-DRIFT` cross-checks that every seat's declared dependencies match the seat's actual card reads (drift-test pattern, mirrors §4 v2.x.1 row-198 R-ARCHIVIST-NO-CANONICAL-MUTATE FORBIDDEN_PRIMITIVES `MappingProxyType` wrapper byte-for-byte). The runtime introspection alternative is structurally rejected: it depends on runtime instrumentation, fails closed only after a card has been used, and cannot be drift-tested at build time.

Carried for L-005 audit round:

- v0.1 Beta honest-claim caveat — card files exist on disk and validate at LOCK but no seat consumes them until v0.2 first wave. Customer-facing docs need explicit "schema-ready, runtime wiring v0.2" wording.

# §8 — Compound transaction at LOCK ceremony (§6.17 Option-B)

When L-005 LOCKs this amendment, the following files paired-commit at the same `lock_timestamp_utc`:

- `pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md` (this file)
- `pipeline/blueprint/v0.1/section_18_card_system.md`
- `pipeline/blueprint/v0.1/section_04_v2_x_y_cards_amendment.md`
- `pipeline/blueprint/v0.1/section_00_5_section_18_card_amendment.md`
- `pipeline/cards/_schema/cic_card.schema.json`
- `pipeline/cards/_schema/clc_card.schema.json`
- `pipeline/cards/_schema/matrix_card.schema.json`
- `pipeline/cards/models.py`
- `pipeline/cards/loader.py`
- `pipeline/cards/CIC/food_systems.yaml` (fixture stub)
- `pipeline/cards/CLC/operating_capacity.yaml` (fixture stub)
- `lock_history.yaml` (new row appended)
- `MEMORY.md` + new memory file at `memory/project_card_system_v7_0_11_locked.md`

Pre-LOCK DRAFT state (the current state of this file as of 2026-05-15) lands the architecture + blueprint + §0.5 amendment + cards directory scaffold; the F-CARDS-* §4 amendment authors at L-005 round Cycle 0 (pre-audit setup); the Pydantic loader and AST-lint rules author at LOCK Cycle 2 author-response per RT-C2 fold-in pattern (§14 v1 + §16 v1 row-170 precedent).
