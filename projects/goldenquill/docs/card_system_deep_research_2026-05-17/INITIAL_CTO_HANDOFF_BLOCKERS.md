# INITIAL_CTO_HANDOFF_BLOCKERS

**Phase 3 of the Tilth Card System Deep Research run, 2026-05-17.**

| Field | Value |
|---|---|
| Filed | 2026-05-17 |
| Workspace | `/Users/goldenquill/Downloads/GoldenQuill/` |
| Scope | Initial enumeration of items a CTO would need resolved before owning the Tilth Card System. P0 = blocking; P1 = should resolve before any sustained dev work; P2 = good to clean up. |
| Phase boundary | Composed from Phase 1 + Phase 2 findings. Final CTO handoff dispatch (Phase 8.6-8) is OUT of Run 1 scope; this is the "initial" enumeration only. |
| What this is NOT | A complete operational runbook. A full release-readiness checklist. A funding-pitch CTO brief. Those land in later phases / dispatches. |
| Run cap | Run 1 of operator's controlled-batch sequence. |

---

## §0. The big picture (in one paragraph)

The Tilth Card System has 14 signed, schema-conformant, lifecycle-coherent card YAMLs on disk; a loader that does the right preflight enforcement on lifecycle + coupling at the field-name layer; nine F-CARDS-* gate modules in the right places; and a 50+-amendment LOCK-history audit trail. The on-disk reality is BETTER than the planning documents describe — the master prompt §5 lifecycle-gap claim has already been resolved, and the cards' lifecycle blocks are correctly in `signed/loaded/runtime_loadable=true` state. **However** the planning layer has run ahead of the implementation layer on three concurrent amendments — §18 v1.2 dialect-routing-table re-keying, §18.6 v2 dual-track CLC restructure, and §4 v2.x.7 coupling-violation value-position scan — all three carry `LOCKED` frontmatter but their companion code / schema / card patches were either deferred or never applied. The card-system runtime is also intentionally half-wired at v0.1: lifecycle/coupling preflight is LIVE, seat-registration is `NotImplementedError`, Ed25519 signature verification is not invoked anywhere, and several of the eight F-CARDS-* gate modules raise `NotImplementedError` even when their owner-amendment claims they're live. A CTO needs to (a) reconcile the amendment-vs-disk drift via the deferred cards-ceremony, (b) graduate the v0.2 first-wave loader + gate-body bodies, and (c) clarify the deprecation path + signature-verification ownership. Roughly four ceremonies + ~30 operator hours plus one engineering sprint of gate-body work would get the system into a state where v0.2 first-wave shipping is unblocked.

---

## §1. P0 — blocking (must resolve before handoff)

### P0-1. Three LOCKed-but-not-applied amendments

**Surfaces:** `pipeline/blueprint/v0.1/section_18_v1_2_amendment.md`, `pipeline/blueprint/v0.1/section_18_6_v2_dual_track_amendment.md`, `pipeline/blueprint/v0.1/section_04_v2_x_7_card_coupling_value_position_amendment.md`.

**Evidence (Phase 1 + 2):** All three amendments carry `amendment_status: LOCKED` frontmatter. The on-disk schemas / cards / gate module bodies are in pre-LOCK state for each:

| Amendment | LOCK timestamp claimed | Pre-LOCK state of companion artifact today |
|---|---|---|
| §18 v1.2 (`section_18_v1_2_amendment.md:5`) | 2026-05-16T14:00:00Z | CIC schema `dialect_routing_table` still has `funder_political_axis` enum (4-axis); 6 CIC cards still have 26 `funder_political_axis` rows |
| §18.6 v2 (master prompt §2.5/§2.6/§2.7 references) | 2026-05-17T16:00:00Z | CLC-05/06/07 still single-track shape (no `track_a:` / `track_b:` blocks); CLC schema has no `$defs.track_container` or `oneOf` branch |
| §4 v2.x.7 (`section_04_v2_x_7_*.md:5`) | 2026-05-17 (per OD-C ceremony) | `pipeline/logician/gates/f_cards_coupling_violation_extension.py:78-82` body still `raise NotImplementedError` |

**Downstream risk.** A reader who treats the amendment-of-record as authoritative will write code/guidance for a system that doesn't exist. The §18 v1.2 case is the most consequential — Scribe currently keys dialect routing on the retired political axis. Any decision Scribe makes about register selection per CLC dialect is keying on `funder_political_axis: "progressive" | "centrist" | …` regardless of the operator's documented intent to retire that axis.

**Recommended owner.** Operator (who has authoritative call on which CLC each routing row should re-key to; the §18 v1.2 amendment FI-9 REVISED at line 209 estimates 18-30 hours for the per-row content-judgment work). Engineering executes the schema + card YAML patches once operator decisions land.

**Resolution shape (full ceremony in Phase 8.1-5):**

1. Operator decides per-CIC-card the row-by-row re-keying for §18 v1.2 (no heuristic mapping; content-judgment per FI-9 REVISED). 18-30 hours.
2. Operator decides per-CLC-card the track_a / track_b content split for §18.6 v2 (CLC-05/06/07; CLC-06 Track B is minimal-stub per master prompt §6 + L-024 directive). ~12 hours.
3. Engineering lands schema + card YAML patches; re-signs cards per OD-C/OD-E precedent.
4. Engineering graduates `f_cards_coupling_violation_extension.py` body per §4 v2.x.7 spec.
5. Compound LOCK ceremony pins all three amendments' companion artifacts at a single `lock_timestamp_utc` per §6.17 Option-B (modeled on the OD-E 5-row compound at master prompt §2.5 row 274).

### P0-2. Lifecycle enum drift across architecture / schema / models / loader

**Surfaces:** `pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md:82` vs. `pipeline/cards/_schema/card_cic.schema.json:391-398` vs. `pipeline/cards/models.py:71` vs. `pipeline/cards/loader.py:63-68`.

**Evidence:** Architecture v7.0.11 §1.4 declares 6 values (`draft | reviewed | thesis_passed | signed | loaded | deprecated`); schema + models + loader unanimously declare 4 values (`draft | review_passed | signed | deprecated`). The schema/models/loader trio is the on-disk truth; the architecture amendment is stale (the consolidation likely happened at §18 v1.1 but the architecture text was never updated).

**Downstream risk.** Any reader citing architecture v7.0.11 §1.4 as authoritative — including the master prompt §5, this audit's own opening read, future CTO/eng onboarding docs, customer-facing trust documentation — will write to a 6-value enum that the loader will reject. This is a teaching-and-onboarding hazard more than a runtime hazard.

**Recommended owner.** Documentation / architecture-amendment editor. Engineering reviews.

**Resolution shape.** New §18 v1.x amendment that:

1. Reconciles architecture v7.0.11 §1.4's lifecycle enum to the on-disk 4-value set.
2. Explicitly documents the two state machines (`draft_status` vs `runtime_load_status`) and the binding boolean `runtime_loadable`.
3. Maps the retired states (`reviewed`, `thesis_passed`, `loaded`) to the fields they were consolidated into (`review_status: passed`, `cross_family_thesis_status: passed`, `runtime_load_status: loaded`).
4. Documentation-only LOCK; no schema/models/loader change.

### P0-3. Master prompt §5's stale lifecycle-gap claim

**Surface:** `docs/cic_clc_unified_master_prompt_2026-05-17.md:394-420`.

**Evidence (Phase 1 §3.2):** Master prompt says all 14 cards carry `draft_status: "draft"`. Disk says all 14 carry `draft_status: "signed"`. Master prompt proposes a 14-card supersession-re-sign ceremony to flip them. That work is unnecessary because it's already done.

**Downstream risk.** Any per-card researcher dispatched against the master prompt §5 will surface a false-positive concern. The supervisor synthesis (per `docs/cic_clc_unified_batch_supervisor_prompt_2026-05-17.md:160-172`) will roll up 14 false-positives into a single proposed §CC-N ceremony recommendation that doesn't need to fire. Operator time wasted.

**Recommended owner.** Operator (master prompt amendment). Engineering verifies.

**Resolution shape.** Edit `docs/cic_clc_unified_master_prompt_2026-05-17.md` §5: replace the "Verified on disk 2026-05-17. All 14 card YAMLs carry `draft_status: 'draft'`" claim with "Verified on disk 2026-05-17. All 14 card YAMLs carry `draft_status: 'signed'`; the supersession-re-sign ceremony for draft_status normalization has already fired (verify by grep `^  draft_status:` in `pipeline/cards/`)." Then either remove the proposed §CC-N normalization recommendation from the supervisor prompt, or repurpose it as a "lifecycle-comment-header normalization" item to address Phase 1 §5 stale-header-comment drift (a smaller and real cleanup).

---

## §2. P1 — should resolve before sustained development

### P1-1. F-CARDS-COUPLING-VIOLATION-EXTENSION value-position regex not live anywhere

**Surface:** `pipeline/logician/gates/f_cards_coupling_violation_extension.py:78-82` (stub) + `pipeline/cards/loader.py:309-344` (only field-name layer, no regex).

**Evidence (Phase 1 §6.3, Phase 2 §5.4):** The OD-C value-position scan amendment (§4 v2.x.7) specifies four regex patterns + a path-level allowlist. The amendment LOCKed. The gate module body is `NotImplementedError`. The loader does not implement value-position scanning. The runtime is therefore unprotected against the coupling-language drift class that motivated OD-C (Wave 1 + Wave 2 fix-in-place precedents on `food_systems.yaml` and `sponsorship_corporate.yaml`).

**Downstream risk.** A researcher who reintroduces `TILTH-CLC-03` literal in `sponsorship_corporate.yaml.underwriting_criteria[*].description` (the OD-C row-272 motivating case) gets through silently today.

**Recommended owner.** Engineering. Operator approves the patch against §4 v2.x.7 amendment text.

**Resolution shape.** Graduate the `f_cards_coupling_violation_extension.py` body per the §4 v2.x.7 amendment's §2.1/§2.2/§2.3 pseudocode. Add the legacy "Customer Information" pattern per Phase 2 L2-F3. Add the backfill-scan script (currently in `outputs/od_c_backfill_scan.py` per amendment cross-references) to `pipeline/scripts/od_c_backfill_scan.py`. Pre-stage tests at `tests/logician/gates/test_f_cards_coupling_violation_extension.py` (the amendment's §6 references a 36-test surface; that's the target). Engineering sprint scope.

### P1-2. Ed25519 signature verification is not invoked at load time

**Surface:** `pipeline/cards/loader.py:127` (`publisher_pubkey: Optional[bytes] = None` parameter is unused) + `pipeline/logician/gates/f_cards_signature_invalid.py:26-41` (stub).

**Evidence (Phase 1 §6.4):** Architecture v7.0.11 §1.5 step 3 declares signature verification a production requirement. The loader doesn't do it. The gate stub raises `NotImplementedError`. The trust model currently relies on `content_hash` (SHA-256 of canonical bytes; loader-checked) and the LOCK-history audit trail — but the embedded `_research_metadata.ed25519_signature` is never cryptographically verified.

**Downstream risk.** A card whose embedded signature was issued with a now-rotated publisher key would not be detected. A card silently re-signed by someone with access to a stale or compromised publisher key would not be detected (because the loader has nothing to compare against). The trust boundary the architecture spec defines exists only on paper.

**Recommended owner.** Engineering. Operator confirms publisher-pubkey location and rotation policy.

**Resolution shape.** Per Phase 1 §6.4: add `publisher_pubkey: bytes` as required (not optional) for production environment; add `enforce_signature_validity()` step between Step 3 and Step 5 of the loader contract; graduate `f_cards_signature_invalid.py` body in parallel; graduate `f_cards_unsigned_production_load.py` body to wrap `enforce_signature_validity()` invocation under the production/development branch. The publisher pubkey lives at `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml` per the README — engineering wires the load path. Pin the rotation window per v7.0.7 §6.1 precedent.

### P1-3. CLC-side Law-5 `common_funders_observed` discipline not confirmed

**Surface:** `pipeline/cards/CLC/*.yaml` (8 files) — `common_funders_observed:` state per card unconfirmed.

**Evidence (Phase 2 §6.4):** Grep across CLC cards for `^common_funders_observed:` or `draft_funder_candidates_pending_operator_engagement_confirmation` returned ZERO matches. The 6 CIC cards uniformly apply the operator's v2.1 Law-5 split. The CLC cards either omit the field entirely (no Law-5 violation), have populated subagent-speculative funder lists (Law-5 violation), or have operator-engagement-confirmed lists (Law-5 compliant). Phase 2 hit the grep wall and didn't read each CLC card's full body.

**Downstream risk.** If CLC cards do carry subagent-speculative funder rosters, every Scout/Scribe/Judge call that consumes `common_funders_observed:` will be operating on fabricated data — a direct Law 5 violation. The runtime impact is wrong funder recommendations or wrong reviewer-profile inference.

**Recommended owner.** Phase 4-CLC per-card researcher dispatch (Run 2 work; see continuation prompt). Operator decides per-card whether each currently-populated funder is engagement-confirmed.

**Resolution shape.** Phase 4-CLC dispatches must include a `common_funders_observed:` audit step in the handback. Each CLC card's handback either (a) confirms the field is empty/absent (no action needed), or (b) lists the populated funders with operator-engagement-confirmed status per funder, surfacing any unconfirmed entries for relocation to `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation`. Schema patch (Phase 2 §6.5 option B) lands at v0.2 first wave to make the draft block schema-known.

### P1-4. Stale header comments across at least 4 cards (and probably more)

**Surface:** `pipeline/cards/CIC/food_systems.yaml:28`, `pipeline/cards/CIC/public_agency.yaml:36`, `pipeline/cards/CIC/cooperative.yaml:45`, `pipeline/cards/CIC/ecosystem_intermediary.yaml:113`.

**Evidence (Phase 1 §5):** Four cards' header comments still read `# Lifecycle: draft. NO Ed25519 signature.` while their lifecycle bodies declare `draft_status: signed`. Header comments lie. Comments are not in canonical-bytes, so updates don't invalidate `content_hash` — pure cosmetic patch.

**Downstream risk.** Confusion for any human or automated reader who reads only the header. Onboarding hazard. Possibly the source of the master prompt §5 stale claim (if its author was reading headers, not lifecycle blocks).

**Recommended owner.** Engineering (mechanical patch). Operator reviews wording.

**Resolution shape.** Documentation-only edits to all 14 card headers; bundle in the cards-ceremony per P0-1.

### P1-5. F-CARDS-* gate module / loader-implementation ownership clarity

**Surface:** The F-CARDS-MALFORMED-LIFECYCLE gate (`f_cards_malformed_lifecycle.py`) is LIVE — it correctly delegates to `loader.py:enforce_lifecycle_truth`. But the F-CARDS-COUPLING-VIOLATION-EXTENSION gate, by the same pattern, *should* delegate to `loader.py:enforce_no_forbidden_coupling`, but it doesn't — it raises `NotImplementedError` instead. The runtime check on coupling is happening in the loader anyway, with the gate's own gate-ID string embedded in the error message (`loader.py:325`). So the named gate module is dead code for runtime purposes; the loader does the gate's job.

**Evidence (Phase 1 §6.3 + Phase 2 §5.3):** Two parallel ownership patterns coexist. The malformed-lifecycle pattern (gate-delegates-to-loader) is the cleaner shape; the coupling-violation pattern (gate-stubs-while-loader-does-it) is brittle and confusing.

**Downstream risk.** Future testing or auditing tool that mocks the gate module to verify a specific behavior would not be testing the live enforcement path. Future engineer onboarding to the F-CARDS-* family hits a parallelism inconsistency immediately.

**Recommended owner.** Engineering.

**Resolution shape.** In the same v0.2 first-wave graduation that lands P1-1 + P1-2: refactor `f_cards_coupling_violation_extension.py` to delegate its `evaluate()` body to `loader.py:enforce_no_forbidden_coupling` (or to a shared helper that both call). Mirror the `f_cards_malformed_lifecycle.py` ownership pattern. Add an integration test that exercises the gate's `evaluate()` directly and asserts violations.

### P1-6. The two-coupling-gate vocabulary fork (`F-CIC-CLC-COUPLING-VIOLATION` vs `F-CARDS-COUPLING-VIOLATION-EXTENSION`)

**Surface:** `pipeline/logician/gates/f_cic_clc_coupling_violation.py` (v7.0.8, LIVE, 4 layers) vs `pipeline/logician/gates/f_cards_coupling_violation_extension.py` (v7.0.11, stub, extends predecessor in spirit).

**Evidence (Phase 2 §5.5 / L2-F8):** The progenitor uses `CouplingFinding.subcode` with layer suffix (`F-CIC-CLC-COUPLING-VIOLATION.layer1_lexical`). The successor uses `GateOutcome.violations` with `sub-tag` prefix (`forbidden_field_name:CIC:clc_allowlist (sub-tag .forbidden_field_name_for_axis)`). Different output shapes; different sub-tag conventions; complementary but un-reconciled coverage.

**Downstream risk.** A CTO onboarding to the F-CARDS-* family has to learn two parallel vocabularies and infer the relationship from prose. Tooling that aggregates findings across both gates has to handle two formats.

**Recommended owner.** Engineering + amendment author (joint).

**Resolution shape.** A new §4 v2.x amendment that:

1. Pins the canonical `GateOutcome` + `sub-tag` vocabulary for the F-CARDS-* family.
2. Maps the F-CIC-CLC-COUPLING-VIOLATION 4-layer outputs into the F-CARDS-* vocabulary OR documents the two as deliberate parallel surfaces with clear scope boundaries (e.g., "F-CIC-CLC-COUPLING-VIOLATION operates on knowledge packs + Pydantic schemas + vault YAML; F-CARDS-COUPLING-VIOLATION-EXTENSION operates only on cards under `pipeline/cards/`").
3. Eventually one absorbs the other; preference is to keep the v7.0.8 surface (broader scope, LIVE) and have F-CARDS-* re-export its outputs with a card-focus filter.

### P1-7. Cards README naming-collision typography (Cards/Cards both rendered as **Cards**)

**Surface:** `pipeline/cards/README.md:9-11`, `pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md:51-53`.

**Evidence (Phase 2 §4.1 / L2-F2):** Both layers (visual + runtime) rendered as `**Cards**` in bold. The "load-bearing" naming distinction the architecture amendment claims cannot be honored visually.

**Downstream risk.** Reader confusion at the literal-first-impression layer. Minor relative to the others above, but every new contributor or auditor hits this on day 1.

**Recommended owner.** Documentation editor.

**Resolution shape.** Adopt either typography ("Cards" capitalized for visual, "cards" lowercase for runtime; current intent per architecture text) consistently across the README + architecture amendment, OR adopt a new disambiguating term for the runtime artifact ("card cartridge" or "card YAML"). Editor's call.

---

## §3. P2 — good to clean up

### P2-1. lock_history_row / lock_timestamp_utc / supersession_lock_history_row lifecycle field disposition

**Surface:** CIC schema `card_cic.schema.json:458-466`, CLC schema `card_clc.schema.json:308-316`.

Per Phase 1 §3.4 (L1-F8): three optional schema fields with no corresponding `models.py` declaration and no `loader.py` consumption. Either graduate (add to dataclass + loader + canonical-bytes-exclusion set) or remove from schema. Decision is operator-driven (do you want lock-history pointers stored in the card body, or only in `lock_history.v1.jsonl`?).

### P2-2. `coverage_axis` 1:1 redundancy

**Surface:** CIC schema `card_cic.schema.json:57-67` + `models.py:47-54`. Six CICs, six coverage_axis values. The slug already implies the axis.

Decision: either derive from slug (drop schema field) or document as deliberate human-readability redundancy. Cosmetic.

### P2-3. Deprecation procedure undocumented

**Surface:** Both schemas allow `draft_status: "deprecated"` + `signature_status: "revoked"` + `runtime_load_status: "disabled"` but no document explains the transition sequence. The loader at `loader.py:302-306` fail-closes on `runtime_loadable=false AND runtime_load_status='loaded'` — a half-deprecated card would trip this. Per Phase 1 §7.

Resolution: write a "Deprecating a card" section in README or as a new §18 v1.x amendment. Cover the field-flip ordering + registry.yaml update + the supersession lock-history-row pattern.

### P2-4. Schema `additionalProperties: true` at root

**Surface:** `card_cic.schema.json:594`, `card_clc.schema.json:415`. Per Phase 2 §5.2 (L2-F6).

The `not.anyOf` block catches the named forbidden fields but accepts any other unknown field (including typo-renamed forbidden fields). Defense-in-depth weakness. Mitigated by Layer 3 (loader recursive scan against FORBIDDEN_FIELD_REGISTRY) but not closed at the schema level.

Consider tightening to `additionalProperties: false` after a survey of every legitimate field in the 14 cards. The `_research_metadata` exception means the survey is non-trivial.

### P2-5. Missing `pipeline/cards/validators.py` (referenced in README)

**Surface:** `pipeline/cards/README.md:21` references `validators.py` ("auxiliary self-validation checks (Phase 4 card-research-time gates)"). Glob check on `pipeline/cards/validators.py`: not found in initial filesystem scan.

If the file was intended to exist, it should be created. If the README is documenting a not-yet-built artifact, remove the reference or mark as DRAFT.

### P2-6. README "NEEDED — Phase D research" comments are stale

**Surface:** `pipeline/cards/README.md:24-39`. The README still annotates 12 cards as "NEEDED — Phase D research" while only `food_systems.yaml` and `operating_capacity.yaml` are marked "fixture stub at v7.0.11 LOCK." All 14 cards are now Wave 1 or Wave 2 LOCKed + signed.

Mechanical doc edit; bundle with P1-7.

---

## §4. Cross-cutting risks

### CR-1. LOCK-vs-disk amendment hygiene

Three concurrent amendments (P0-1) all carry `LOCKED` frontmatter but pre-LOCK on-disk companion state. The pattern smells like a workflow where amendment LOCK ceremonies and companion-code ceremonies are decoupled but the amendment frontmatter doesn't reflect the pending companion work.

**Recommended workflow change:** add an `amendment_status:` value `LOCKED_TEXT_PENDING_COMPANION_CEREMONY` (or similar) that distinguishes amendments whose text is ratified from amendments whose full implementation has shipped. Today both states show `LOCKED`. A reader cannot distinguish amendment-of-record from amendment-fully-implemented.

Alternative: keep the binary `LOCKED` state but add a new mandatory frontmatter field `companion_ceremony_status:` (`pending` | `completed` | `not_applicable`) that surfaces in every amendment file's top block. A CTO scanning the amendment chain would see at a glance which amendments still have outstanding work.

### CR-2. The "Cowork workspace outputs/" pattern leaves artifacts outside the repo

The §4 v2.x.7 amendment cross-references `outputs/od_c_backfill_scan.py` (line 238) as the backfill-scan script. This file is not in `pipeline/scripts/` and not in the workspace's tracked tree. The Cowork session outputs directory is ephemeral relative to repo state.

If the script is operationally important (and it is — it's the only way to scan cards against the value-position regex while the gate body is stubbed), it should be checked in.

**Recommended:** define a `pipeline/scripts/` directory convention. Any operator-runnable script referenced from an amendment must live under `pipeline/scripts/`, with a path-pinned cross-reference. This protects the audit trail against Cowork-session-outputs ephemerality.

### CR-3. v0.1 → v0.2 graduation surface is broad

Phase 1 catalogued at least eight things the loader and gate family do NOT do today that are spec'd to land at v0.2 first wave:

1. `load_card()` actually returning a `LoadedCard` instead of `NotImplementedError`.
2. F-CARDS-COVERAGE-INCOMPLETE meta-gate firing in production.
3. F-CARDS-UNSIGNED-PRODUCTION-LOAD gate body.
4. F-CARDS-SIGNATURE-INVALID gate body.
5. F-CARDS-SCHEMA-INVALID gate body (status unconfirmed; gate stub likely).
6. F-CARDS-PRIVATE-DATA-IN-CARD gate body (status unconfirmed; gate stub likely).
7. F-CARDS-CROSS-ORG-NAMESPACE-LEAK gate body (status unconfirmed; gate stub likely).
8. Ed25519 signature verification at loader time.

That's a meaningful engineering sprint, not a quick patch. A v0.2 first-wave engineering plan needs to enumerate and sequence these. Phase 8.1-5 begins this enumeration but the full plan is a Phase 8.6-8 deliverable (CTO Handoff full).

### CR-4. Test surfaces referenced but not audited

Initial filesystem scan showed:

- `tests/cards/test_models_and_schemas.py`
- `tests/cards/test_lifecycle_truth.py`
- `tests/logician/gates/test_f_cards_malformed_lifecycle.py`

These were not read for Run 1. They may either confirm the live behavior (good — supports the on-disk findings) or expose additional drift (bad — needs surfacing).

The §4 v2.x.7 amendment claims a 36-test surface at `tests/logician/gates/test_f_cards_coupling_violation_extension.py`. Existence and pass-status of that file is unconfirmed.

**Recommended:** Phase 6 of the (reverse-engineered) 8-phase plan likely covers test-surface audit. Or Phase 8.6-8 CTO Handoff plus tests as a "go/no-go" handoff criterion.

### CR-5. Architecture amendment text is the most-cited authority but the least-updated artifact

Per P0-2 (lifecycle enum drift) + P0-1 + the Cards/Cards naming collision (P1-7) + the lock_history_row/lock_timestamp_utc field disposition (P2-1): the architecture v7.0.11 amendment is repeatedly the source of truth for *intent* but the surface where reconciliation patches have not been applied. A documentation-only architecture-amendment-update pass that brings v7.0.11 in line with the §18 v1.1/v1.2 + §4 v2.x.7 + §18.6 v2 reconciliations would yield outsized clarity for a CTO. This is a single doc-only ceremony.

---

## §5. Recommended sequencing

If a CTO took this list and asked "what do I do in what order," the operator-confirmation-cost-minimizing sequence is:

1. **Documentation-only patches (no LOCK ceremony; sidecar edits).**
   - Master prompt §5 stale-claim correction (P0-3).
   - README typography fix (P1-7).
   - Stale header-comment updates across 14 cards (P1-4 — though this is a card-body comment edit, comments are not in canonical-bytes so it's not a re-sign).
   - README "NEEDED — Phase D research" stale annotation fix (P2-6).
   - Architecture v7.0.11 §1.4 lifecycle-enum reconciliation (a §18 v1.x amendment, but LOCK-light per the documentation-only carve-out at OD-D row 270 precedent).

2. **The big cards-ceremony.** Bundles:
   - §18 v1.2 schema delta + 6 CIC card dialect_routing_table re-keying (P0-1, item §18 v1.2).
   - §18.6 v2 CLC schema delta + 3 CLC card multi-track restructure (P0-1, item §18.6 v2).
   - Per Phase 4-CLC findings, any CLC-side `common_funders_observed` Law-5 relocation patches (P1-3).
   - Re-sign all 9 patched cards (6 CIC + 3 CLC) per OD-E precedent.
   - One §6.17 Option-B compound LOCK ceremony at one `lock_timestamp_utc`.
   - 30-40 operator hours (18-30 for §18 v1.2, ~12 for §18.6 v2 + Law-5 relocation).

3. **The gate-body graduation sprint.** Engineering work, parallel to operator's cards-ceremony prep:
   - Graduate `f_cards_coupling_violation_extension.py` body per §4 v2.x.7 (P1-1).
   - Refactor coupling enforcement so gate module delegates to loader (or vice versa) for ownership clarity (P1-5).
   - Reconcile the two-coupling-gate vocabulary (P1-6).
   - Add the legacy "Customer Information" pattern to the value-position regex set.
   - Pre-stage backfill scan at `pipeline/scripts/od_c_backfill_scan.py` (CR-2).
   - Engineering sprint scope: 1-2 weeks.

4. **The v0.2 first-wave loader graduation.** Engineering work:
   - Ed25519 signature verification at loader time (P1-2).
   - F-CARDS-UNSIGNED-PRODUCTION-LOAD + F-CARDS-SIGNATURE-INVALID gate bodies (P1-2 dependent).
   - Other F-CARDS-* gate bodies (CR-3 items 2, 5, 6, 7).
   - `load_card()` graduation past the `NotImplementedError` boundary (CR-3 item 1).
   - Engineering sprint scope: 2-3 weeks.

5. **Deferred cleanup.** P2 items, bundled when convenient:
   - lock_history_row field disposition (P2-1).
   - `coverage_axis` derivation (P2-2).
   - Deprecation procedure (P2-3).
   - Schema `additionalProperties: false` tightening (P2-4).
   - `validators.py` creation or README reference removal (P2-5).

**Total runway from this state to v0.2-first-wave-shipping-ready** = roughly 4-6 weeks operator + engineering parallel, with the cards-ceremony being the longest single bottleneck (operator-availability-bound).

---

## §6. What this audit does NOT cover (in-scope for later phases)

- **Phase 4-CIC (per-CIC card researcher dispatch)** — content quality of search_vocabulary, evidence_signals, kfr_fact_classes, register_defaults, admin_risk_term_register, dialect_routing_table (post-§18 v1.2 cards-ceremony), common_funders_observed (post-engagement confirmation), etc.
- **Phase 4-CLC (per-CLC card researcher dispatch)** — underwriting_criteria, evidence_weights, scoring_weight_patterns, common_red_flags, commitment_tracking_pattern, reviewer_profile_typical, common_application_forms, common_portals, etc.
- **Phase 5 (admin-risk register consolidation)** — the OD-A v2.4 → v3.0 scrub workflow (per master prompt §7).
- **Phase 6 (test surface audit)** — `tests/cards/`, `tests/logician/gates/test_f_cards_*.py`, and the §4 v2.x.7 36-test surface claim.
- **Phase 7 (batch supervisor synthesis)** — cross-card vocabulary drift, dialect-routing-table cross-CIC consistency, regression-test coverage gaps, state-overlay separation, OD-G coordination.
- **Phase 8.6-8 (full CTO handoff)** — funder-pitch readiness, customer-facing trust documentation, release-readiness checklist, on-call runbook, observability story.

This Run-1 audit is the foundation. The rest of the program builds on it.

---

## §7. Files cited (consolidating Phase 1 + Phase 2)

See `CARD_LIFECYCLE_AND_LOADER_GOVERNANCE_AUDIT.md` §9 and `CANONICAL_NAMING_AND_ORTHOGONALITY_AUDIT.md` §8.

Additional file referenced in this phase only:

| File | Lines referenced | Purpose |
|---|---|---|
| `SOUL.md` | 38 | Law 5 statement (Phase 2 §6 cross-ref) |

---

*End of Phase 3 deliverable.*
