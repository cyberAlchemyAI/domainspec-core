---
title: §0.5 Blueprint Interface Index — §5 v6 Pipeline rows amendment (InvocationRecord schema + STR derivation)
filed: 2026-05-08
operator: Josh
status: LOCKED 2026-05-08 — paired with §5 v6 (LOCKED 2026-05-08); 2 rows promoted PARENT_UNLOCKED → STABLE at compound commit. GPP three-tier closure: Tier 1 PASS, Tier 2 live (14 findings; SCHEMA-MISMATCH-02 caught by reasoner FOLDED_IN pre-LOCK with 8-field schema description corrected to match §5.7.1 canonical), Tier 3 signed manifest Ed25519+ML-DSA-65-stub valid. Closes the final 3 v7.0.1 carry-forwards.
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md                                       # §0.5 base
  - pipeline/blueprint/v0.1/section_05_v6_amendment.md                                                   # §5 v6 LOCK-READY since 2026-04-19; this companion lands as paired commit at LOCK
companion_blueprint_amendment: pipeline/blueprint/v0.1/section_05_v6_amendment.md  (§5.7 InvocationRecord schema + §5.8 STR derivation/aggregation + §5 GPP wiring absorption)
kind_of_amendment: pure row-append (2 new rows). NO vocabulary extension — both rows use existing §0.5 closed vocabulary (schema, mechanism).
row_count: 2
companion_file_pattern: matches §0.5 §6 + §0.5 §7 + §0.5 §10 + §0.5 §4 v2.3 + §0.5 §4 v2.4/v2.5 amendment-companion precedent.
parent_wins_discipline: each row's parent_lock_version + parent_lock_commit_hash fields populated at commit time from §5 v6's sha3-512 prefix.
f_index_stale_preflight: F-INDEX-STALE PRE-gate fires at commit time; both 2 rows must be present in the index or the commit fails closed.
version_wording_discipline: "LOCKED" refers to on-disk LOCKED state only.
---

# Amendment intent

§5 v6 introduces (a) the `InvocationRecord` per-seat-call telemetry schema at §5.7 (8 typed fields: token_count_input, token_count_output, success_flag, seat, session_date, run_id, model_string, timestamp) and (b) the STR (Success-to-Token Ratio) derivation rule at §5.8 (per-record STR = success_flag / (token_count_input + token_count_output) when token sum > 0; aggregated per-seat via rolling-window quantile distribution, k=5 W=30d per A11 R.6). Plus §5 absorbs the GPP wiring paragraph from §4 v2.1.1 (already LOCKed today as part of v7.0.1).

LOCK-READY since 2026-04-19; was blocked on GPP three-tier mechanism which LOCKed 2026-05-08 via v7.0.1. Per §0.5 paired-commit discipline, both primitives introduced by §5 v6 must land as §0.5 rows in the same commit that LOCKs §5 v6.

This LOCK closes the **last 3 of 8 v7.0.1 carry-forward items** that were carried to "§5 next-LOCK": the §5 telemetry-record hook (per-seat invocation emits a record), the §5 per-invocation record schema (`InvocationRecord` 8 fields), and the STR derivation formula. v7.0.1 carry-forward closure full at this LOCK.

# §0.5 row table (2 rows)

| Row | Primitive name | Kind | Source section | Parent lock version |
|---|---|---|---|---|
| 1 | `per_invocation_telemetry_record_schema` | schema | §5 v6 §5.7 | §5 v6 |
| 2 | `str_derivation_and_aggregation` | mechanism | §5 v6 §5.8 | §5 v6 |

## Row 1 — `per_invocation_telemetry_record_schema` (schema)

- **Description:** Per-seat-invocation telemetry record emitted at the §5 run-lifecycle inner loop. 8 required typed fields per §5 v6 §5.7.1: `run_id` (str UUID-4), `seat` (str matching router.yaml seat names), `timestamp` (str ISO 8601 UTC), `model_family_resolved` (str — provider-family canonical name from router.yaml taxonomy after fallback resolution: Anthropic / OpenAI / OpenAI-OSS / Alibaba / Meta / Moonshot / Google / Local-Ollama), `token_count_input` (int ≥ 0), `token_count_output` (int ≥ 0), `success_flag` (int ∈ {0, 1}), `latency_ms` (int — round-trip latency dispatch-to-response-complete in milliseconds). No optional fields in v0.1; the 8-field schema is the complete canonical surface. Future field additions require bumping `INVOCATION_RECORD_SCHEMA_VERSION` constant per §5.7.1.
- **Defined at:** `pipeline/blueprint/v0.1/section_05_v6_amendment.md` §5.7
- **Production implementation:** TO_BE_PINNED at v0.2 — `pipeline.observability.invocation_record` library module; v0.1 emits records to local session-log JSONL append-only file under `<run_dir>/invocation_records.jsonl`
- **Parent lock version:** §5 v6
- **Parent lock commit hash:** populated at commit time
- **Stability tier:** PARENT_UNLOCKED → STABLE at compound LOCK
- **Introduced in index version:** §0.5 v9 (cumulative; this companion file uses paired-commit pattern, not own-version-numbered)

## Row 2 — `str_derivation_and_aggregation` (mechanism)

- **Description:** Success-to-Token Ratio derivation at §5 v6 §5.8. Per-record STR = `success_flag / (token_count_input + token_count_output)` when token sum > 0; defined as 0 when token sum is 0 (zero-token-sum branch). Aggregated per-seat via rolling-window quantile distribution: k=5 sample size, W=30d window per A11 R.6 Telemetry Commons k-anonymity discipline. Distribution exported as quantiles only (q05/q25/q50/q75/q95), never per-invocation values.
- **Defined at:** `pipeline/blueprint/v0.1/section_05_v6_amendment.md` §5.8
- **Production implementation:** `pipeline.observability.str_window` (TO_BE_PINNED at v0.2; v0.1 may compute on-demand at run-close from invocation_records.jsonl)
- **Parent lock version:** §5 v6
- **Parent lock commit hash:** populated at commit time
- **Stability tier:** PARENT_UNLOCKED → STABLE at compound LOCK
- **Introduced in index version:** §0.5 v9 (cumulative)

# Parent_lock_commit_hash population

At compound LOCK time, both rows' `parent_lock_commit_hash` field is populated with the SHA-3-512 canonical-bytes hash of `section_05_v6_amendment.md` post-LOCKED-status edit.

# v7.0.1 carry-forward closure

This LOCK closes the final 3 v7.0.1 carry-forward items per the v7.0.1 amendment's "Predecessor blocker carry-forward exemption" list:

- `§5 telemetry-record hook` (per-seat invocation emits a record; ASPIRATIONAL-LOAD-BEARING) → CLOSED at this LOCK (Row 1 schema + production reference)
- `§5 per-invocation record schema` (8 fields; ASPIRATIONAL-LOAD-BEARING) → CLOSED at this LOCK (Row 1 schema definition)
- `STR derivation formula` (PROPOSED-NOT-EXISTS) → CLOSED at this LOCK (Row 2 mechanism definition)

After this LOCK lands, **all 8 v7.0.1 carry-forwards are CLOSED**. Recursion-closure milestone: GPP mechanism gates downstream amendments end-to-end with full carry-forward consumption.

# Non-goals for this amendment

- Does not modify any existing §0.5 row.
- Does not introduce a new primitive kind.
- Does not pin the `pipeline.observability` library implementation (v0.2 production wire-in).
- Does not add concurrent-access invariants for STRWindow (v0.1 single-session envelope; v0.2 deferred per §5 v6 §5.8.5 non-goal).
- Does not modify A11 R.6 ALLOWED-list (`str_distribution_allowlist_row` companion already LOCKed via v7.0.1 architecture E.P scope).

# Paired-commit reminder

This §0.5 companion amendment LOCKs atomically with `pipeline/blueprint/v0.1/section_05_v6_amendment.md`. F-INDEX-STALE PRE-gate fails-closed if both 2 rows are not in the index at the moment of compound commit.

# GPP three-tier expectations (2026-05-08 LOCK)

- **Tier 1 GPP-DET** — already PASS (`gpp_det_report_2026-05-08.md`); plan_sub_docs scope unchanged.
- **Tier 2 GPP-COUNCIL** — fresh live dispatch on §5 v6 + this §0.5 companion. This is the **fourth GPP-gated LOCK** in the same session 2026-05-08.
- **Tier 3 GPP-SYNTHESIS** — operator dispositions + signed manifest. Ephemeral keypair (B1 not yet LOCKed).

# Thesis round expectations (already cleared 2026-04-19)

§5 v6 cleared L-005 two-audit on 2026-04-19; this §0.5 companion is additive row-append against that cleared scope. No new Thesis round required — GPP three-tier substitutes per §0.5 paired-commit discipline.

# End of amendment
