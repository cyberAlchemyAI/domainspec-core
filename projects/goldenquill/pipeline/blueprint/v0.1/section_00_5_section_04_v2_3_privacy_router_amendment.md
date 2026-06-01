---
title: §0.5 Blueprint Interface Index — §4 v2.3 Privacy Router rows amendment
filed: 2026-05-08
operator: Josh
status: LOCKED 2026-05-08 — paired with §4 v2.3 (LOCKED 2026-05-08); 4 rows promoted PARENT_UNLOCKED → STABLE at compound commit. GPP three-tier closure: Tier 1 PASS, Tier 2 live (12 findings dispositioned), Tier 3 signed manifest Ed25519+ML-DSA-65-stub valid.
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md                      # §0.5 v5 LOCKED 2026-05-08 — 27 GPP rows compound-LOCKed with v7.0.1
  - pipeline/blueprint/v0.1/section_04_v2_3_amendment.md                                # §4 v2.3 LOCK-READY since 2026-04-19; this companion lands as paired commit at v2.3 LOCK
companion_blueprint_amendment: pipeline/blueprint/v0.1/section_04_v2_3_amendment.md  (§4.14 — Privacy Router content-scan PRE-gate)
kind_of_amendment: pure row-append (4 new rows). NO vocabulary extension — every row's `primitive_kind` resolves against existing §0.5 closed vocabulary (mechanism, pre-gate-check, failure-code).
row_count: 4
companion_file_pattern: matches §0.5 §6 + §0.5 §7 + §0.5 §10 amendment-companion precedent (2026-04-21 / 2026-05-02 cycles).
parent_wins_discipline: each row's parent_lock_version + parent_lock_commit_hash fields populated at commit time from §4 v2.3's sha3-512 prefix. Row source_section field cites §4 v2.3 §4.14 + §6 sub-sections.
f_index_stale_preflight: F-INDEX-STALE PRE-gate (§4.2.1 Row 19) fires at commit time; all 4 rows must be present in the index or the commit fails closed.
version_wording_discipline: "LOCKED" refers to on-disk LOCKED state only.
---

# Amendment intent

§4 v2.3 introduces the Privacy Router content-scan PRE-gate at §4.14 (LOCK-READY since 2026-04-19; was blocked on GPP three-tier mechanism which LOCKed 2026-05-08 via v7.0.1 + §4 v2.1.1 + §0.5 v5). Per §0.5 paired-commit discipline, four primitives introduced by §4 v2.3 must land as §0.5 rows in the same commit that LOCKs §4 v2.3.

The four rows enumerate: the Privacy Router mechanism (1), the §5 step-21 PRE-gate row (1), and the two new failure codes that §4 v2.3 §6 registers (2). No interface-contract row is included — the `PrivacyRouteResult` dataclass is part of the production-code spec card (`pipeline/engineering/spec_cards/phase2a_privacy_router.md` LOCKED) and is not a §0.5-tier primitive per the §4 v2.3 author's declared scope (front-matter `paired_commit_sec00_5: §0.5 v6 — 4 new rows`).

# §0.5 v6 row table (4 rows)

| Row | Primitive name | Kind | Source section | Parent lock version |
|---|---|---|---|---|
| 1 | `privacy_router_mechanism` | mechanism | §4 v2.3 §4.14 | v2.3 |
| 2 | `privacy_router_content_scan_pregate` | pre-gate-check | §4 v2.3 §4.14 + §5 step 21 | v2.3 |
| 3 | `F-PRIVACY-CLASSIFIER-ERROR` | failure-code | §4 v2.3 §6 | v2.3 |
| 4 | `F-PRIVACY-PAYLOAD-TAGGED-LOCAL-ONLY-BYPASSED` | failure-code | §4 v2.3 §6 | v2.3 |

## Row 1 — `privacy_router_mechanism` (mechanism)

- **Description:** Content-scan PRE-gate that classifies inbound payloads as LOCAL_ONLY / CLOUD_ELIGIBLE / CLASSIFIER_ERROR before any seat invocation routes to a cloud endpoint. Fail-closed: classifier error or low-confidence verdict routes local. PII / PHI / client-identifying grant data / raw financials / Law-3-bound org boundaries are LOCAL_ONLY by default.
- **Defined at:** `pipeline/blueprint/v0.1/section_04_v2_3_amendment.md` §4.14
- **Production implementation:** `pipeline/privacy/_classifier.py` + `pipeline/privacy/_router.py` (pipeline.privacy module v1 LOCKED)
- **Parent lock version:** v2.3
- **Parent lock commit hash:** populated at commit time from §4 v2.3 sha3-512 prefix
- **Stability tier:** PARENT_UNLOCKED → STABLE at compound LOCK
- **Introduced in index version:** v6

## Row 2 — `privacy_router_content_scan_pregate` (pre-gate-check)

- **Description:** §4.2.1 PRE-gate table row 21. Calls `run_privacy_pregate(payload, seat, default_routing) -> PrivacyRouteResult`. If `routed_local=True`, override seat routing to local. If any cloud dispatch attempted after local override, abort hard with F-PRIVACY-PAYLOAD-TAGGED-LOCAL-ONLY-BYPASSED.
- **Defined at:** `pipeline/blueprint/v0.1/section_04_v2_3_amendment.md` §4.14 + §5 step 21
- **Production implementation:** `pipeline.privacy.run_privacy_pregate`
- **Parent lock version:** v2.3
- **Parent lock commit hash:** populated at commit time
- **Stability tier:** PARENT_UNLOCKED → STABLE at compound LOCK
- **Introduced in index version:** v6

## Row 3 — `F-PRIVACY-CLASSIFIER-ERROR` (failure-code)

- **Description:** Classifier returned ambiguous or error verdict. Fail-closed: routes payload local-only and emits the failure code. Recoverable — next invocation retries the classifier.
- **Defined at:** `pipeline/blueprint/v0.1/section_04_v2_3_amendment.md` §6
- **Family:** F-PRIVACY-* (new in v2.3)
- **Severity:** RECOVERABLE
- **Parent lock version:** v2.3
- **Parent lock commit hash:** populated at commit time
- **Stability tier:** PARENT_UNLOCKED → STABLE at compound LOCK
- **Introduced in index version:** v6

## Row 4 — `F-PRIVACY-PAYLOAD-TAGGED-LOCAL-ONLY-BYPASSED` (failure-code)

- **Description:** Payload classified LOCAL_ONLY but a downstream caller attempted cloud dispatch. Fail-closed: aborts the invocation hard. Non-recoverable for the current invocation; structural defect in routing logic if it fires.
- **Defined at:** `pipeline/blueprint/v0.1/section_04_v2_3_amendment.md` §6
- **Family:** F-PRIVACY-*
- **Severity:** STRUCTURAL
- **Parent lock version:** v2.3
- **Parent lock commit hash:** populated at commit time
- **Stability tier:** PARENT_UNLOCKED → STABLE at compound LOCK
- **Introduced in index version:** v6

# Parent_lock_commit_hash population

At compound LOCK time, all 4 rows' `parent_lock_commit_hash` field is populated with the SHA-3-512 canonical-bytes hash of `section_04_v2_3_amendment.md` post-LOCKED-status edit. The paired commit binds §4 v2.3 + §0.5 v6 atomically.

# Non-goals for this amendment

- Does not modify any existing §0.5 row (v4, v5, or earlier amendments).
- Does not introduce a new primitive kind. All 4 rows use existing kinds: mechanism, pre-gate-check, failure-code.
- Does not declare a `privacy_route_result_v1` schema row — the dataclass is production-code-internal per the §4 v2.3 author's scope decision.
- Does not pin the classifier technology choice — that is captured in `pipeline/validation/integration_scope_close_2026-04-19/classifier_research_note.md` and consumed by `pipeline/privacy/_classifier.py`.

# Paired-commit reminder

This §0.5 v6 amendment LOCKs atomically with `pipeline/blueprint/v0.1/section_04_v2_3_amendment.md`. F-INDEX-STALE PRE-gate fails-closed if the 4 rows are not in the index at the moment of compound commit.

# GPP three-tier expectations (2026-05-08 LOCK)

The compound LOCK runs through the GPP three-tier mechanism that LOCKed 2026-05-08 (v7.0.1):

- **Tier 1 GPP-DET** — already PASS (`gpp_det_report_2026-05-08.md`); plan_sub_docs scope unchanged.
- **Tier 2 GPP-COUNCIL** — fresh live dispatch on §4 v2.3 + this §0.5 v6 companion. Carries forward four DEFERRED v7.0.1 findings (RT F001/F002 + Reasoner GGRR-002/005) for §4 v2.3-context disposition.
- **Tier 3 GPP-SYNTHESIS** — operator dispositions + signed manifest. Ephemeral keypair (B1 not yet LOCKed; persistent key pending advisor S8 + S11 PASS).

# Thesis round expectations (already cleared 2026-04-19)

§4 v2.3 cleared L-005 two-audit on 2026-04-19; this §0.5 v6 amendment is additive row-append against that cleared scope. No new Thesis round required — GPP three-tier substitutes per §0.5 paired-commit discipline.

# End of amendment
