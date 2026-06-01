---
title: §0.5 Blueprint Interface Index — §5 v8 Pipeline track-registry rows amendment (LOCKED 2026-05-10)
filed: 2026-05-10
operator: Josh
status: LOCKED 2026-05-10 — compound paired-commit with §5 v8 LOCK per §6.17 Option-B. L-005 strict two-cycle CLOSED with FULL cross-family rigor (Editor=Llama 3.3 70B/Groq + Judge=Gemini 2.5 Pro/Google + Red Team=GPT-OSS 120B/Groq across both cycles; audit trail at `pipeline/validation/v5_v8_thesis_2026-05-10/{audit_prompt_v1_*.md, audit_v1_{editor,judge,red_team}.{md,raw.json}, audit_v1_synthesis.md, cycle_1_fixes.md, audit_prompt_v2_*.md, audit_v2_{editor,judge,red_team}.{md,raw.json}, audit_v2_synthesis.md}`).
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md                                 # §0.5 v5 LOCKED 2026-04-19 — 101 master rows
  - pipeline/blueprint/v0.1/section_00_5_section_06_operating_envelope_amendment.md                # §0.5 v6 LOCKED 2026-04-21 — rows 102-117 (host of F-PIPELINE-TRACK-FROZEN dormant entry)
  - pipeline/blueprint/v0.1/section_00_5_section_07_scribe_amendment.md                            # §0.5 v7 LOCKED 2026-04-21 — rows 118-158
  - pipeline/blueprint/v0.1/section_00_5_section_10_red_team_amendment.md                          # §0.5 v8 LOCKED 2026-05-02 — rows 159-211
  - pipeline/blueprint/v0.1/section_00_5_section_12_uploader_amendment.md                          # §0.5 v9 LOCKED 2026-05-10 — rows 212-232
  - pipeline/blueprint/v0.1/section_00_5_section_11_intake_amendment.md                            # §0.5 v10 LOCKED 2026-05-10 — rows 233-256
  - pipeline/blueprint/v0.1/section_00_5_section_02_v7_2_operational_amendment.md                  # §0.5 v11 LOCKED 2026-05-10 — rows 257-278
  - pipeline/blueprint/v0.1/section_05_v8_amendment.md                                             # §5 v8 LOCKED 2026-05-10
companion_blueprint_amendment: pipeline/blueprint/v0.1/section_05_v8_amendment.md  # paired-commit at §5 v8 LOCK per §6.17 Option-B
compound_lock_with: section_05_v8_amendment.md
parent_wins_discipline: each row's parent_lock_version + parent_lock_commit_hash point at §5 v8; resolves to actual sha3-512 prefix at LOCK ceremony.
row_delta: prior runtime-live total at §0.5 v11 LOCK 2026-05-10 = 278 rows. **§5 v8 amendment claims rows 279-290 (12 rows).** New runtime-live total at this LOCK = 290.
kind_of_amendment: row-append. NO vocabulary extension — every row's `primitive_kind` resolves against the v5 + v6 16-value closed vocabulary (`marker / schema / interface-contract / failure-code / pre-gate-check / post-gate-check`). The 12 rows split as: 1 marker (section anchor) + 2 schema (Track + TrackRegistry dataclasses) + 6 interface-contract (TrackRegistryError + RegistrySchemaError + load_track_registry + load_track_registry_from_yaml_text + get_track + dispatch_track) + 3 failure-code (F-PIPE-TRACK-NOT-FOUND + F-PIPE-TRACK-NOT-SHIPPABLE + F-PIPE-TRACK-SHAPE-UNIMPLEMENTED).
dependency_order: §5 v8 LOCK + this §0.5 amendment land as a single compound paired-commit at the same `lock_timestamp_utc`.
f_index_stale_preflight: F-INDEX-STALE PRE-gate fires at commit time; all 12 new rows must be present in the index or the commit fails closed.
cross_family_posture: LIVE FULL CROSS-FAMILY (no Section E carve-out) — fourth substantive v0.1 round to LOCK at this rigor level (after WS-D v7.0.5 row 179 + WS-F §12 v1 rows 182-184 + WS-E §11 v1 row 185 + WS-H §2 v7.2 rows 186-187). Cycle 1: Editor + Judge READY_TO_LOCK; Red Team REQUIRES_FIXES (RT-01/02 HIGH; RT-03/04 MED; RT-05/06/07 LOW). Cycle-1 closures: 6 closed code + 4 amendment-text closures + 6 new tests (31 → 37 in `tests/loop/test_track_registry.py`). Cycle 2: unanimous READY_TO_LOCK (Editor clean; Judge 100/100; Red Team `blocking: false / verdict: PASS` with all Cycle-1 HIGH closures CLOSED + RT-04 REOPEN at MED + 5 NEW residuals NF-01..05 all MED/LOW non-blocking; deferred per §10 OQ-9).
f_pipeline_track_frozen_activation: this LOCK is the activation event for `architecture.r_pullforwards_enforcement` (§0.5 row 112) `dormant_activation_condition: "LOCK-time of Section 5 v6 spin (F-PIPELINE-TRACK-FROZEN)"`. F-PIPELINE-TRACK-FROZEN audit PASSED — registry exposes the v0.2 extension surface as R.PF1 demands; carve-out for grandfathered runners bounded by §7.19. The dormant entry on row 112 transitions DORMANT_UNTIL_SECTION_5_V6_LOCK → ACTIVE at this compound LOCK.
---

# Amendment intent

This amendment lands paired with §5 v8 LOCK per §6.17 Option-B compound-commit pattern. It registers §5 v8-owned primitives (one section-anchor marker + two dataclass schemas + six interface-contract rows + three failure-code rows) into the Index. R.PF1 (architecture-side dormant pull-forward, v7 LOCKED 2026-04-19) is the binding architectural commitment that §5 v8 lands; F-PIPELINE-TRACK-FROZEN is the dormant PRE-gate that wakes at this LOCK and audits the §5 v8 LOCKED text against R.PF1's "data-driven extension only" commitment. **The audit PASSED** at LOCK time — Cycle 1 Red Team and Judge both verified §4.16 + §7.19 jointly close the dodge-via-runner-internals escape hatch (RT-01) and §4.16 dispatcher contract clause 7 plus the runtime-rebind sentinel test close the closed-set monkey-patch attack (RT-02).

The §11 amendment (§0.5 v10 LOCKED 2026-05-10 with rows 233–256 across 24 rows) and the §2 v7.2 amendment (§0.5 v11 LOCKED 2026-05-10 with rows 257–278 across 22 rows) are the most recent compound-LOCK precedents. This amendment follows the same paired-commit pattern.

The master `section_00_5_interface_index_locked.md` remains LOCKED v5 on-disk; this amendment file is runtime-live at compound LOCK with §5 v8. Future master re-author folds all v6 / v7 / v8 / v9 / v10 / v11 / this amendment files into the master.

# Amendment §A — row append (rows 279–290)

All rows enter §0.5 at `stability_tier = "STABLE"` at compound v8 LOCK (no PARENT_UNLOCKED transit since §5 v8 LOCKs in the same compound transaction).

**Marker (row 279) — §5 v8 section anchor:**

| Row | primitive_id | defined_at | parent_lock_version | parent_lock_commit_hash | kind | stability_tier |
|---|---|---|---|---|---|---|
| 279 | `blueprint.section_anchor.s5_v8_track_registry.v1` | `pipeline/blueprint/v0.1/section_05_v8_amendment.md` | §5 v8 | `<resolved_at_commit>` | marker | STABLE |

**Schemas (rows 280–281) — track-registry dataclass canonical shapes:**

| Row | primitive_id | defined_at | kind | Parent / shape |
|---|---|---|---|---|
| 280 | `pipeline.loop.track_registry.Track.v1` | `pipeline/blueprint/v0.1/section_05_v8_amendment.md#§3.2.7` | schema | Track frozen kw_only slots dataclass; eleven fields (six §6.7 host-schema + five R.PF1 follow-on bindings); §7.20 enforces `{org_slug}` substring in `output_vault_subtree` |
| 281 | `pipeline.loop.track_registry.TrackRegistry.v1` | `pipeline/blueprint/v0.1/section_05_v8_amendment.md#§3.2.8` | schema | TrackRegistry frozen kw_only slots dataclass wrapping deterministic-order `tuple[tuple[str, Track], ...]`; declaration-order preserved across YAML → dataclass parse for byte-stable audit replay |

**Interface contracts (rows 282–287) — track-registry public surface:**

| Row | primitive_id | defined_at | kind | Parent / signature |
|---|---|---|---|---|
| 282 | `pipeline.loop.track_registry.TrackRegistryError.v1` | `pipeline/blueprint/v0.1/section_05_v8_amendment.md#§3.2.9` | interface-contract | Abstract base exception class; subclassed by `RegistrySchemaError` + `TrackNotFound` + `TrackNotShippable` + `TrackShapeUnimplemented`. Not a failure-code itself; the three runtime-failure subclasses carry F-PIPE-TRACK-* codes (registered as failure-code rows 288-290 below). |
| 283 | `pipeline.loop.track_registry.RegistrySchemaError.v1` | `pipeline/blueprint/v0.1/section_05_v8_amendment.md#§3.2.9` | interface-contract | Loader-side schema-malformation exception; raised by `load_track_registry` (missing keys, unknown keys, kind mismatch, cross_family_rigor mismatch, empty string fields, missing `{org_slug}` placeholder per §7.20) and by `load_track_registry_from_yaml_text` (duplicate mapping keys). NOT a runtime registry-lookup failure (no F-PIPE-TRACK-* code; trigger string `F-PIPE-TRACK-REGISTRY-DUPLICATE-KEY` documented at §4.16 YAML-text loader contract for the duplicate-key sub-case). |
| 284 | `pipeline.loop.track_registry.load_track_registry.v1` | `pipeline/blueprint/v0.1/section_05_v8_amendment.md#§4.16` | interface-contract | `load_track_registry(source: Mapping[str, Any]) -> TrackRegistry`. Loader contract clauses 1-8 per §4.16 (clauses 1-7 from initial draft; clause 8 added Cycle-1 RT-03 closure for `{org_slug}` placeholder validation). Returns frozen registry preserving declaration order. |
| 285 | `pipeline.loop.track_registry.load_track_registry_from_yaml_text.v1` | `pipeline/blueprint/v0.1/section_05_v8_amendment.md#§4.16` | interface-contract | `load_track_registry_from_yaml_text(yaml_text: str) -> TrackRegistry`. Cycle-1 RT-04 closure. Installs custom SafeLoader subclass with duplicate-detecting mapping constructor; raises `RegistrySchemaError` with trigger `F-PIPE-TRACK-REGISTRY-DUPLICATE-KEY` on any duplicate mapping key at any depth. The on-disk loader call-site MUST use this helper rather than `yaml.safe_load` directly (mechanical enforcement deferred per §10 OQ-9 RT-04 REOPEN tracking). |
| 286 | `pipeline.loop.track_registry.get_track.v1` | `pipeline/blueprint/v0.1/section_05_v8_amendment.md#§4.16` | interface-contract | `get_track(registry, name, *, current_version=TILTH_VERSION_FAMILY) -> Track`. Lookup with shippable_in lex-compare gate. Raises `TrackNotFound` on miss, `TrackNotShippable` if `track.shippable_in > current_version`. §7.21 documents lex-compare hazard for v0.10 / v1.0 future-version (out-of-scope at v0.1). |
| 287 | `pipeline.loop.track_registry.dispatch_track.v1` | `pipeline/blueprint/v0.1/section_05_v8_amendment.md#§4.16` | interface-contract | `dispatch_track(registry, name, *, current_version, submission_runner, eval_runner, submission_kwargs, eval_kwargs) -> Any`. Dispatcher contract clauses 1-7 per §4.16 (clauses 1-5 from initial draft; clauses 6-7 added Cycle-1 RT-07 + RT-02 closures: dispatch-by-shape; runtime-rebind sentinel via fall-through `TrackShapeUnimplemented` with "rebound at runtime" message). Future Judge DC-01 refactor (§10 OQ-8) MUST preserve the runtime-rebind sentinel. |

**Failure codes (rows 288–290) — three runtime registry-lookup failures (NOT the LOCK-time F-PIPELINE-TRACK-FROZEN audit gate, which is owned by §6.7):**

| Row | primitive_id | defined_at | kind | Parent / sub-tag |
|---|---|---|---|---|
| 288 | `pipeline.loop.track_registry.failure_code.F-PIPE-TRACK-NOT-FOUND.v1` | `pipeline/blueprint/v0.1/section_05_v8_amendment.md#§6` | failure-code | INFO (caller-error). Raised by `dispatch_track` / `get_track` when `name` is not in the registry. Distinct from architecture-side LOCK-time `F-PIPELINE-TRACK-FROZEN` (owned by §6.7, registered §0.5 row 112). |
| 289 | `pipeline.loop.track_registry.failure_code.F-PIPE-TRACK-NOT-SHIPPABLE.v1` | `pipeline/blueprint/v0.1/section_05_v8_amendment.md#§6` | failure-code | INFO (forward-compat-safety). Raised by `get_track` when `track.shippable_in > current_version` per lex-compare. The §6.7 forward-compatibility safety guarantee enforced runtime-side; complements the §7.21 lex-compare bound. |
| 290 | `pipeline.loop.track_registry.failure_code.F-PIPE-TRACK-SHAPE-UNIMPLEMENTED.v1` | `pipeline/blueprint/v0.1/section_05_v8_amendment.md#§6` | failure-code | CRIT (fail-closed). Raised by `dispatch_track` when (a) `track.pipeline_shape ∉ _V0_1_IMPLEMENTED_SHAPES`, OR (b) the matching runner argument is None, OR (c) the if/elif fall-through fires (runtime-rebind sentinel per §4.16 dispatcher contract clause 7). The (c) path is the Cycle-1 RT-02 closure runtime sentinel — distinct trigger message `"_V0_1_IMPLEMENTED_SHAPES has been rebound at runtime"`. |

# Parent_lock_commit_hash population

At compound LOCK time, all twelve rows' `parent_lock_commit_hash` field is populated with the SHA-3-512 canonical-bytes hash of `section_05_v8_amendment.md` post-LOCKED-status edit (per §4.11 hash-binding predicate; the §5 v8 amendment's compound-commit-interaction subsection cites this).

# F-PIPELINE-TRACK-FROZEN dormant-gate activation

§0.5 row 112 (`architecture.r_pullforwards_enforcement`) names two architectural pull-forward dormant entries — F-PIPELINE-TRACK-FROZEN (§5 side, R.PF1) and F-VAULT-ARTIFACT-ONLY (§2 side, R.PF2). Per §0.5 row 112's `dormant_activation_condition`: "LOCK-time of Section 5 v6 spin (F-PIPELINE-TRACK-FROZEN) or Section 2 v7.2 spin (F-VAULT-ARTIFACT-ONLY)". This LOCK is the F-PIPELINE-TRACK-FROZEN activation event (the §5 spin lands as v8, not v6, but is the spin that adopts the registry per the dispatch plan §WS-G; the §6.7 dormant-gate language at the architecture layer reads "§5 v6 spin or §5 v8 round" — see §6.7 line 270).

The F-VAULT-ARTIFACT-ONLY entry was activated at the §2 v7.2 LOCK earlier today (row 186); F-PIPELINE-TRACK-FROZEN activates at this LOCK. Both v0.1 architectural pull-forwards are now ACTIVE.

# Non-goals for this amendment

- Does not modify any existing §0.5 row.
- Does not introduce a new primitive_kind (vocabulary preservation per §11 + §12 + §2 v7.2 precedent — every row's `primitive_kind` resolves against the v5+v6 16-value closed vocabulary).
- Does not register §10 OQ-9 deferred residuals as §0.5 rows (RT-04 REOPEN + NF-01..05 are tracked in the §5 v8 amendment text only; mechanical-enforcement primitives that close them will land as new §0.5 rows in the future spin that owns them).
- Does not retire §5 v6 / §5 v7 invariants. §5 v8 is purely additive (per §5 v8 §1 Amendment intent — "v8 does not touch existing surface; it adds new surface").

# Paired-commit reminder

This §0.5 companion amendment LOCKs atomically with `pipeline/blueprint/v0.1/section_05_v8_amendment.md`. F-INDEX-STALE PRE-gate fails-closed if all 12 rows are not in the index at the moment of compound commit.

# Cross-family-rigor recap

Live cross-family bridge dispatch via `mcp__Control_your_Mac__osascript` → `openclaw infer model run --gateway` per AGENTS.md Cross-family review section. Three distinct non-Anthropic families (Editor=Meta/Llama, Judge=Google/Gemini, Red Team=OpenAI-OSS/GPT-OSS-120B) across both audit cycles. L-003 satisfied. Section E single-Claude carve-out NOT invoked (no dispatch failure logged). This is the **fourth** substantive v0.1 round to LOCK with FULL live cross-family rigor (after WS-D v7.0.5 row 179 architecture-class precedent + WS-F §12 v1 row 182 + WS-E §11 v1 row 185 + WS-H §2 v7.2 row 186 blueprint-class precedents).

# End of amendment
