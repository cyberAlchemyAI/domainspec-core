# Blueprint Section 0.5 — Blueprint Interface Index (LOCKED v4 2026-04-19)

**Status:** **LOCKED v5 2026-04-19** (§5 v6 paired commit — 2 new §5 rows landing at §5 v6 LOCK). **v5 amendment scope:** add 2 §0.5 rows for §5 v6 Item 2 (per_invocation_telemetry_record_schema, str_derivation_and_aggregation); update §5 row parent pointer from v5 → v6; update §0.5.8.6 count 8 → 10; total row count 99 → 101. All other rows unchanged. **v4 history:** LOCKED v4 2026-04-19 (narrow parent-refresh following v7 architecture LOCK 2026-04-19 A1-A12 full scope). v4 amendment scope: update parent architecture reference v6-r2 → v7; update 14 M-family rows' `parent_lock_version` + `parent_lock_commit_hash` to v7; add 18 new architecture-layer rows (§0.5.8.8-§0.5.8.13) aggregating 30 new v7 failure-code primitives + 8 new section anchors. Row count 81 → 99. **Thesis Team verdicts L-005 2-cycle:** Cycle-1 Editor READY_TO_LOCK / Judge PASS 99/100 / Red Team REQUIRES_MINOR_FIXES (3 findings — 2 factually hallucinated phantom-anchor claims + 1 legitimate dormant-tier clarification). Cycle-2 REFRESH: Red Team CONCEDED all phantom hallucinations with explicit grep line-number verification (§K at line 673, §R.PF1 at line 1149, §R.PF2 at line 1152, §S.1 A7.5 at line 1310); CONCEDED aggregation in-pattern with §4 Logician v3 precedent; ACCEPTED dormant-tier closure at `architecture.r_pullforwards_enforcement`. Cycle-2 verdicts: Editor READY_TO_LOCK + Judge PASS 99/100 ready_to_lock=true + **Red Team READY_TO_LOCK zero residuals**. Cross-family ensemble caught Cycle-1 Red Team semantic hallucination — exactly the defense-in-depth pattern v7 §F.1 LOCKED describes. **v3 history (preserved):** LOCKED v3 2026-04-18, 81 rows, Editor READY_TO_LOCK + Judge PASS 92/100 + Red Team READY_TO_LOCK. v3 canonical copy preserved at `section_00_5_interface_index_v3_2026-04-18.md`. **v2 history (preserved):** 71 rows, Judge 100/100. **v1 history (preserved):** 71 rows, Judge 100/100. JSON companion v4: `section_00_5_interface_index.v4.json` (to be rebuilt from v4 Markdown body via canonical-JSON build step post-LOCK). Audit trail: `pipeline/validation/blueprint_section_00_5_v4_2026-04-19/{01..04}_*_v4{,_c2}.*`. Post-§0.5-v4 queue: downstream blueprint backfills per v7 §13 delegations (§5 v5.1, §6 Operating Envelope, §2 v7.2, §4 v2.2, §1 v6.1, §3 v5.1) + engineering plan per v7 handoff §9.

**Parent architecture:** `pipeline/architecture/v0.1/tilth_architecture_locked.md` (**v7 A1-A12 LOCKED 2026-04-19**; SHA3-512 `24fb706c1bb33ca08d4acecf7dee57fcd375a1b5872668be7d12dd4b5a79c5e09a95a10227882fcf39eb0efb332ee74e53774f7baac7d2b6d2a7bb826222a568`; 266232 bytes; 1794 lines). v6-r2 preserved at `pipeline/architecture/v0.1/tilth_architecture_locked_v6_r2_2026-04-18.md`; v7-A1-A6 intermediate preserved at `pipeline/architecture/v0.1/tilth_architecture_locked_v7_a1_a6_2026-04-19.md`.
**Parent blueprint sections referenced (read-only, not modified by this round):**
- Section 1 Sovereignty Envelope: `pipeline/blueprint/v0.1/section_1_sovereignty_envelope.md` (**LOCKED v6 2026-04-18** against parent v6-r2; v5 DRAFT archived at `section_1_sovereignty_envelope_v5_2026-04-17.md`; SHA3-512 `b0d50a71f53dde3b9988750ba843875125b21c1234115bb4d38268e00818e61009a5948f611ac7c3ebb28daf6726b04759bbe649b3f52600882d62721c89d422`).
- Section 2 Vault Topology: `pipeline/blueprint/v0.1/section_02_vault_topology.md` (LOCKED v7 2026-04-18; v7.1 parent-backfill pending to add `golden-set-read` + `golden-set-write` + `index-update` allowlist rows).
- Section 3 Scout: `pipeline/blueprint/v0.1/section_03_scout.md` (LOCKED v5 2026-04-17).
- Section 4 Logician: `pipeline/blueprint/v0.1/section_04_logician.md` (LOCKED v2 2026-04-18; v2.1 parent-backfill pending to wire F-INDEX-STALE at PRE-gate slot #7 and add F-EVAL-CROSS-ORG-READ predicate).
- Section 5 Pipeline: `pipeline/blueprint/v0.1/section_05_pipeline.md` (LOCKED **v6** 2026-04-19; v5 LOCKED 2026-04-18 preserved in same file).

**Scope pre-decisions locked by operator 2026-04-18 (do not re-open in audit):**
1. Logician allowlist rows aggregated at Section-4-lock-version granularity — one Index entry per lock with `primitive_id = logician.allowlist.v{N}_table` — not exploded into 20 per-intent rows.
2. Index is a blueprint-layer artefact, not a code-generation target. The JSON companion is canonical for byte-identical signing only; the Markdown body is the authoritative prose.
3. Parent-wins invariant is architectural (v6-r2 §0.5.3 binds it); this blueprint instantiates the mechanism, it does not relitigate the principle.

**Scope (this document):**
- §0.5.1–§0.5.11 (eleven subsections, ~1,050 lines) defining Index purpose, invariant, schema, citation form, versioning/staleness, PRE-gate predicate, admin-risk entry, v1 seed population, update lifecycle, test matrix, and forward-deps.
- JSON companion at `pipeline/blueprint/v0.1/section_00_5_interface_index.v1.json` — schema declaration + 71 seed rows in canonical-JSON (sorted keys, UTF-8, LF, no trailing whitespace). v2 does not modify the JSON companion; all v2 changes are in the Markdown body (§0.5.6.2 predicate pseudocode and §0.5.10.1 T5 wording).

**Out of scope (deferred, unchanged from v1):**
- Authoring `index-update` Vault intent (belongs in §2 v7.1 parent-backfill).
- Wiring F-INDEX-STALE into §4.2.1 PRE-gate table at slot #7 (belongs in §4 v2.1 parent-backfill).
- Authoring §1 Sovereignty Envelope re-lock (belongs in §1 v6 round).
- v2 multi-tenant / hostile-tenant Index partitioning (v0.2 backlog).
- Any Index entry for primitives introduced AFTER 2026-04-18 lock timestamps.

**v2 lock gate (L-005 strict verification round, must pass to LOCK):**
- Editor: READY_TO_LOCK — both narrow edits (§0.5.6.2 sentinel-detect clause, §0.5.10.1 T5 exemption) correctly applied; eleven-subsection authoring density and citation grounding preserved from v1.
- Judge: ≥ 85/100 against the 14-dimension rubric (v2 expected to hold v1's 100/100 or marginally improve because the two edits close v1's minor schema_completeness/test_adequacy gaps).
- Red Team: READY_TO_LOCK — zero Bucket-A, zero Bucket-B, v1's two Bucket-C findings confirmed closed; any new findings classified and addressed.

If any of the three seat bars fail, v3 opens per L-005 (unlikely given the narrow-edit surface).

---

## §0.5.1 Purpose and scope

### §0.5.1.1 What the Index is

The Blueprint Interface Index is a single machine-readable artefact at `pipeline/blueprint/v0.1/section_00_5_interface_index.md` (plus its canonical JSON companion) that enumerates every primitive defined by any locked blueprint section and pins each to its authoritative definition site along with the parent section's lock version and lock commit hash at the moment the Index was last updated. When one blueprint section (child) needs to cite a primitive defined by another blueprint section (parent), the citing child uses an Index-mediated identifier (`IDX:v{N}:primitive_id`) rather than a raw section-and-line reference. The Index is the load-bearing mechanism that lets Tilth's locked sections compose into a coherent whole without every cross-section citation silently going stale whenever a parent re-locks.

The Index is authored by the blueprint operator at lock-time, not generated by any runtime code. It is human-readable prose plus a canonical-JSON companion. It is versioned with its own monotonic counter (Index v1, v2, v3, …) that is independent of any individual parent blueprint section's version number. When a parent section re-locks to a new version, the Index bumps to v{N+1} and updates exactly the rows whose parent moved — the untouched rows keep their `parent_lock_version` and `parent_lock_commit_hash` unchanged.

### §0.5.1.2 What the Index is not

The Index is not a blueprint section in the normal sense: it does not introduce new primitives, it does not specify pipeline behaviour, it does not publish failure codes or invariants of its own beyond F-INDEX-STALE (the PRE-gate predicate that detects when the Index itself has gone stale) and ART-INDEX-DRIFT (the admin-risk entry triggered when F-INDEX-STALE fires at run-time). The Index is also not a parser target for Tilth's runtime — no Scout, Scribe, Editor, Judge, or Logician reads the Markdown body at run-time. The JSON companion is the machine-read path; the Markdown is the operator-read path and the audit-trail path.

The Index is not a source of truth for any primitive's semantics. The `defined_at` pointer locates the primitive at its authoritative definition site (typically a Section 2/3/4/5 subsection); the Index itself does not restate the semantics. An audit that finds the Index and the parent disagree on what a primitive does must believe the parent, not the Index. The Index's only claim is "as of this Index version, the parent said this, and here is the commit hash to prove it". If the parent has since moved and the Index has not caught up, F-INDEX-STALE fires and halts the pipeline before any downstream consumer acts on a stale pointer.

### §0.5.1.3 Scope of this blueprint round (v1)

This document authors the v1 scoping round. It delivers the schema prose, the invariants, the PRE-gate predicate, the admin-risk entry, the test matrix, and the v1 seed population that covers every primitive defined by the five locked blueprint sections as of 2026-04-18. The v1 round does NOT wire F-INDEX-STALE into Section 4's PRE-gate table — that wiring is a forward dependency on the Section 4 v2.1 parent-backfill. The v1 round also does NOT author the `index-update` Vault intent that an operator will use to persist Index amendments — that is a forward dependency on the Section 2 v7.1 parent-backfill. Those two backfills, together with Section 1's re-lock against v6-r2, are the three prerequisites for the Index to be fully live in the pipeline.

Between v1 LOCK and the three backfills landing, the Index is static reference material: readable by an operator (and by the three audit seats) for cross-section grounding, but not yet a PRE-gate enforcement target. The gap is intentional: the v1 round proves the Index can be authored coherently; the v7.1 / v2.1 / §1 re-lock rounds then wire the mechanism end-to-end without the Index schema itself being on the critical path.

---

## §0.5.2 Parent-wins invariant

### §0.5.2.1 Formal statement

Let `P` be a parent blueprint section currently LOCKED at version `v_P` with commit hash `h_P`, and let `X` be a primitive defined in `P`. The Index may carry at most one row pinning `X` to `(v_P, h_P, defined_at_path)`. If `P` re-locks to `(v_P', h_P')` with `h_P' ≠ h_P`, exactly one of the following must hold at all times:
- the Index has been amended to v{N+1} with the row for `X` updated to `(v_P', h_P', defined_at_path')`, OR
- every PRE-gate of every pipeline entry point that transitively depends on any primitive from `P` halts with F-INDEX-STALE before any downstream consumer reads the Index row for `X`.

The invariant is "parent-wins" because when the on-disk parent file and the Index disagree, the pipeline halts rather than letting the stale Index silently corrupt a downstream decision. The parent's lock commit hash, not the Index's cached value, is the tiebreaker.

### §0.5.2.2 Failure mode the invariant prevents

Without this invariant, the following scenario is possible and has been observed in prior Tilth audit rounds: Section 4 cites a Section 2 primitive by raw path (`section_02_vault_topology.md#§4.10.4 row 3`); Section 2 re-locks with row 3 renumbered to row 5 (e.g., a new allowlist row is inserted above it); Section 4's citation now silently points at the wrong row. Nothing in the pipeline detects the drift until a run-time bug surfaces. The Index replaces the fragile row-number citation with an Index-mediated pointer (`IDX:v{N}:vault.allowlist.admin_risk_append`) that is re-resolved through the Index at lock-time — and the Index's PRE-gate detects if it itself is stale relative to any parent's current commit hash.

### §0.5.2.3 Drift vectors covered

The invariant covers three drift vectors:

- **Parent bytes change.** Parent `P` re-locks, its file's SHA-3-512 hash changes, the Index's `parent_lock_commit_hash` for any row under `P` is now stale. F-INDEX-STALE detects this via direct hash comparison at PRE-gate time.
- **Parent version changes.** Parent `P` re-locks with a new `v_P'` even if (improbably) no bytes changed. The Index's `parent_lock_version` is now stale. F-INDEX-STALE detects this via version-number comparison.
- **Primitive definition site moves within parent.** Parent `P` re-locks with `X` moved from subsection `§A` to `§B`. The Index row's `defined_at` is now stale. This is not directly detectable by hash comparison on the parent file (the hash already changed, flagging the drift); the operator's Index-update step then re-resolves `defined_at` by reading the new parent.

The invariant is deliberately conservative: any change to the parent's bytes invalidates the Index rows under that parent, whether or not the change actually touched a primitive the Index names. An operator can re-lock the Index cheaply (one pass per parent) — the cost is bounded — so the invariant prefers to over-invalidate rather than risk an under-invalidation that lets a real drift slip.

### §0.5.2.4 ART-INDEX-DRIFT trigger

If F-INDEX-STALE fires at run-time, the pipeline writes an ART-INDEX-DRIFT entry to the admin-risk ledger (via Section 2 v7 §4.10.4 row 2 `admin-risk-append` append-cas intent), captures the failing Index version, the parent whose commit hash diverged, and the subset of Index rows transitively affected, and halts before any further PRE-gate runs. The operator is then the resolving authority: they re-lock the Index and re-run the pipeline. There is no auto-recovery — §0.5.6.4 below elaborates the halt semantics.

### §0.5.2.5 What parent-wins does not cover

The invariant does NOT guarantee semantic correctness of Index rows: if a row's one-line description says "vault_write primitive (overwrite semantics)" but the parent subsection actually defines append-cas semantics, F-INDEX-STALE will catch the parent bytes having changed (because the parent was re-locked to correct the Index-inducing drift) but it cannot catch a mis-described row that was authored wrong at Index-authoring time. Catching that class of error is the audit seats' job (Editor grounding gate; Judge schema-completeness dimension; Red Team attacks on description/defined_at correspondence).

---

## §0.5.3 Per-row schema

### §0.5.3.1 Required fields (eight)

Every Index row carries exactly these eight fields in this canonical order:

1. **`primitive_id`** — globally unique dotted identifier within a given Index version, e.g. `vault.allowlist.v2_table`. The first segment names the parent section's short tag (`vault`, `scout`, `logician`, `pipeline`, `arch`); subsequent segments disambiguate down to the specific primitive. `primitive_id` is the sole citation handle used by Index-mediated references; the `defined_at` path below is the human/audit pointer, not the citation key.
2. **`defined_at`** — canonical human-readable anchor of the form `{section_file_stem}#§{subsection}` where `section_file_stem` is a stem like `section_02_v7` (the version tag baked in deliberately — defined-at anchors are version-bound at Index-authoring time; when a parent re-locks, `defined_at` is refreshed to the new stem alongside version/hash). Subsection follows the parent's own heading structure (e.g., `§4.10.4`).
3. **`parent_lock_version`** — the parent's lock version at Index-authoring time, e.g. `v7` or `v2` or `v6-r2` (architecture). Monotone per parent; when the parent bumps, this field bumps.
4. **`parent_lock_commit_hash`** — SHA-3-512 hash (hex, lowercase, 128 chars) of the parent file's canonical bytes at Index-authoring time. Provides byte-level drift detection independent of version-number hygiene.
5. **`primitive_kind`** — one of a fixed vocabulary: `mechanism`, `schema`, `failure-code`, `constant`, `allowlist-row`, `invariant`, `test`, `interface-contract`, `admin-risk-entry`, `pre-gate-check`, `post-gate-check`, `architecture-mechanism`, `marker`. Vocabulary is closed in v1; v2 additions go through operator approval.
6. **`description`** — one-sentence human-readable statement of what the primitive does, written in present tense active voice, ≤ 160 characters. Not authoritative — the parent's actual subsection is. Used by audit seats to spot misalignment between Index prose and parent definition.
7. **`introduced_in_index_version`** — the Index version at which this row was first added, e.g. `v1`, `v2`. Permits audit of Index lineage. Never mutates after row creation; a re-authored row keeps its original `introduced_in_index_version` and bumps only the parent-lock fields.
8. **`stability_tier`** — one of `STABLE`, `PENDING_PARENT_BACKFILL`, `PARENT_UNLOCKED`, `EXPERIMENTAL`. `STABLE` = parent LOCKED, row verified. `PENDING_PARENT_BACKFILL` = parent LOCKED but a forward-dependent backfill is expected (e.g., Section 2 v7.1, Section 4 v2.1 rows in v1 Index). `PARENT_UNLOCKED` = parent is DRAFT (Section 1 marker row only in v1). `EXPERIMENTAL` = primitive introduced in a v0.2 backlog item not yet landed; never present in v1 Index.

### §0.5.3.2 Optional fields (two)

Two optional fields extend rows without breaking schema v1 compatibility:

9. **`binds_to`** — an Index-mediated pointer (`IDX:v{N}:primitive_id` form) at a primitive the current row wraps, consumes, or version-tracks against. Example: the Logician allowlist aggregate row `logician.allowlist.v2_table` carries `binds_to = IDX:v1:vault.allowlist.static_table_5_entries` to make the Section-2-is-source-of-truth relationship explicit.
10. **`consumed_by`** — list of `IDX:v{N}:primitive_id` values naming rows that cite this row. Maintained by the operator at Index-amendment time; not machine-computed at run-time. Useful for impact analysis when amending a parent ("which rows will need description updates if I rename X?"). Not load-bearing for F-INDEX-STALE; the hash comparison already covers drift detection.

### §0.5.3.3 Canonical ordering

Within the JSON companion, rows are ordered lexicographically by `primitive_id`. This gives byte-identical output for a given set of rows regardless of the authoring order in the Markdown body. The Markdown body orders rows by parent section (§1 → §2 → §3 → §4 → §5 → arch) for human readability; the reordering is cosmetic and neither order is authoritative for signing.

Canonical-JSON rules match Section 2 v7 §4.11: sorted keys at every object level, UTF-8 encoding, LF line endings, no trailing whitespace, no BOM, `ensure_ascii=False`, key separator `": "`, item separator `", "`, floats rendered via the canonical decimal rule (N/A for the Index schema — no float fields), nulls absent (omit rather than write null). The SHA-3-512 hash of the canonical-JSON bytes is the `index_content_hash` that gets signed into the operator's signed-commit ledger whenever the Index is amended.

### §0.5.3.4 Schema orthogonality and exhaustiveness

The eight required fields partition the per-row state without overlap: `primitive_id` is identity; `defined_at` is location; `parent_lock_version` + `parent_lock_commit_hash` are freshness; `primitive_kind` is taxonomy; `description` is human readability; `introduced_in_index_version` is lineage; `stability_tier` is readiness. An audit that finds a field a row cannot populate has discovered either a schema bug (to be fixed in Index v2) or a misclassification (the row doesn't belong in the Index at all). Either outcome surfaces through the audit seats; neither is silent.

Fields are exhaustive for v1: every primitive the Index indexes can populate all eight required fields and zero, one, or two of the optional fields. A primitive that cannot populate `defined_at` (because it is defined inline in running prose rather than at a nameable subsection) is not a candidate for an Index row — it is a sign that the parent needs a subsection heading added at its next re-lock. Until then, the Index carries no row for it.

### §0.5.3.5 Field update rules

Per-row field mutability:
- `primitive_id` — **immutable after row creation**. A primitive that gets renamed in the parent keeps its old `primitive_id` in the Index and carries a note in `description`; at Index v{N+1} the operator either deprecates the old row (adding a new row for the new name) or writes an alias row (v0.2 backlog).
- `defined_at` — **refreshed at each Index version bump** where the parent moved.
- `parent_lock_version` + `parent_lock_commit_hash` — **refreshed at each Index version bump** where the parent re-locked.
- `primitive_kind` — **refreshed only if the parent changed the primitive's kind** (rare but possible — e.g., a constant promoted to a schema).
- `description` — **refreshed at each Index version bump** where the parent's semantic changed materially.
- `introduced_in_index_version` — **immutable after row creation**.
- `stability_tier` — **refreshed at each Index version bump** as readiness changes.
- `binds_to` / `consumed_by` — **refreshed at operator discretion**; not load-bearing.

---

## §0.5.4 Citation form

### §0.5.4.1 The `IDX:v{N}:primitive_id` form

When one blueprint section cites a primitive owned by another section via the Index, the citation takes the form `IDX:v{N}:{primitive_id}`. `v{N}` is the Index version the citing section was locked against; `{primitive_id}` is the row's immutable identifier. Example: Section 5 v6 (future) could cite the Vault `vault_write` primitive as `IDX:v1:vault.primitive.vault_write` and the citation is resolved by the Index at lock-time to the then-current `defined_at` value (`section_02_v7#§4.3`). If Section 2 later re-locks to v8 with vault_write moved to `§4.4`, Section 5's citation does not change — but the Index's row for `vault.primitive.vault_write` bumps, and F-INDEX-STALE fires at any pipeline run whose PRE-gate sees Section 5's cached Index version stale against the now-current Index.

The `v{N}` prefix is load-bearing: it pins the citation against a specific Index version, so the citing section's audit trail records which Index state the citation was authored against. A section written before Index v5 and then unchanged through Index v6 does not implicitly upgrade — its citations still say `IDX:v5:*` and those citations resolve via the Index v5 snapshot preserved on-disk.

### §0.5.4.2 Where citations appear

Citations appear in exactly three contexts:
- **Blueprint body prose** — when one section's running prose needs to name a primitive owned by another section. Always use the IDX form; never use raw `section_02_v7#§4.10.4 row 3`.
- **Architecture reference notes** — when the architecture document (which is the parent of all blueprint sections) refers to a specific blueprint primitive by name, it may cite in IDX form. (Architecture v6-r2 currently does not, because the architecture was locked before the Index; future architecture rounds may.)
- **Admin-risk ledger entries** — when an ART-* entry references a specific primitive that triggered the bypass, it cites in IDX form so an audit of the ledger can resolve the referenced primitive against the Index version at entry time.

Citations do NOT appear in:
- Python source code (uses raw imports and string constants, not Index pointers).
- Run-time JSON payloads (uses `primitive_id` bare, not the `IDX:v{N}:` prefix, because the Index version is carried out-of-band on the envelope).
- Operator chat or daily logs (uses human-readable section references — daily logs are not subject to F-INDEX-STALE).

### §0.5.4.3 Collision handling

`primitive_id` is globally unique within a given Index version. Two rows with the same `primitive_id` is a schema violation and causes the Index-build step to fail (see §0.5.10.4 test). If the operator wants to rename a primitive, they deprecate the old row (by removing it from the next Index version) and create a new row with the new `primitive_id`; the Index's `introduced_in_index_version` for the new row records when the new name first appeared. An alias mechanism (one `primitive_id` → multiple human names) is v0.2 backlog.

Across Index versions, `primitive_id` is monotonically preserved: a row present in v{N} with id `X` either remains in v{N+1} with id `X` (possibly with other fields refreshed) or is removed from v{N+1} entirely. The id is never reused for a different primitive. This is enforced by the audit seats at each Index version bump.

---

## §0.5.5 Versioning and staleness

### §0.5.5.1 Index version numbering

The Index carries its own monotonic version counter: v1, v2, v3, … . The version number bumps whenever any row changes (added, removed, or any field refreshed). There is no semantic versioning (no major.minor) — every bump is a full new version because the audit cycle treats every bump as a fresh round. The JSON companion file is named with the version number embedded (`section_00_5_interface_index.v1.json`, `.v2.json`, …) and prior versions are preserved on-disk as read-only for audit trail.

The Markdown file `section_00_5_interface_index.md` is updated in-place at each version bump, with the header's **Status** block reflecting the current version and the changelog subsection at §0.5.11 appending the new round's narrative. The prior version's Markdown is preserved at `section_00_5_interface_index_v{N}_2026-{MM}-{DD}.md` in the same directory.

### §0.5.5.2 Per-parent lock-hash lineage

For each parent section cited by the Index, the Index carries (implicitly across its rows) a per-parent `(parent_lock_version, parent_lock_commit_hash)` pair. These pairs are extractable from the Index at Index-build time by grouping rows by parent's file stem and verifying all rows under a given parent carry identical version + hash — any row under parent `P` with a version or hash differing from its siblings is a schema violation and fails the Index-build test. This property is what makes F-INDEX-STALE a single-parent check rather than a per-row check: at PRE-gate time, the pipeline computes the current SHA-3-512 of each parent file once and compares against the single version/hash pair the Index carries for that parent.

The per-parent lock-hash lineage is the load-bearing operational contract: once the pipeline validates that the Index's recorded hashes match the current on-disk hashes of all parents, every downstream IDX citation resolves safely. A mismatch on any parent fails the PRE-gate for every pipeline entry point, not just the entry point that would have consumed that parent's primitives — F-INDEX-STALE is conservative because a stale Index is a systemic integrity concern, not a per-run detail.

### §0.5.5.3 Staleness semantics

Staleness is a binary property per parent: either the Index's recorded `(version, hash)` matches the parent's current on-disk `(version, hash)` or it does not. There is no "slightly stale" — a single byte difference in the parent file is as fatal to F-INDEX-STALE as a version bump. This is deliberate: at byte resolution the staleness is unambiguous and the operator's amendment step is cheap (re-read the parent, re-compute hash, update the Index's rows). Attempting to grade staleness ("a hash mismatch in a non-citable subsection is safe") introduces a second-order trust problem: who decides which subsections are non-citable? The Index does not, and must not, carry that adjudication.

The staleness check is also pipeline-entry-point-agnostic: `submission_mode` and `eval_mode` both run F-INDEX-STALE at their PRE-gates. A stale Index halts both. Partial trust (one entry point proceeds while another halts) is ruled out by the systemic-integrity framing.

### §0.5.5.4 Bypass rules

No automated bypass. Per M13 (operator-only bypass), the operator can manually acknowledge a stale Index and proceed with a specific pipeline run, but only via an admin-risk-ledger entry that records the bypass authorisation, the Index version in use, the parents' actual hashes, and the operator's explicit sign-off. The bypass entry writes through Section 4 v2 §4.7.3 `admin_risk.record_bypass_authorization` call path and is append-cas committed to the ledger (Section 2 v7 §4.10.4 row 2). The next pipeline run ignores the one-time bypass — every run re-checks F-INDEX-STALE fresh. There is no "disable F-INDEX-STALE" toggle; there is only per-run explicit bypass.

Bypass authorisation is rate-limited at the operator policy level (not enforced by code): if more than three bypasses occur in a seven-day window, the operator-facing summary report flags it as a drift pattern requiring resolution, and the Monday cron digest surfaces it for review. Over-use of bypass is a code smell that should drive prompt Index amendment, not repeated bypass authorisation.

### §0.5.5.5 Re-lock cost

The cost of re-locking the Index when a parent moves is bounded: one operator-mediated pass per affected parent, consisting of re-reading the parent file, re-computing SHA-3-512 of canonical bytes, updating `parent_lock_version` + `parent_lock_commit_hash` on every row under that parent, refreshing `defined_at` on any row whose subsection heading moved, refreshing `description` on any row whose semantics materially changed, and committing the amended Index as v{N+1} via the `index-update` Vault intent (forward dep on Section 2 v7.1). For the v1 Index covering five parents with ~70 rows, the re-lock-after-one-parent-moves cost is typically under 30 minutes of operator time per parent. The cost is intentionally trivial: the invariant's value depends on the operator being willing to re-lock the Index liberally, not on the operator hoarding Index amendments.

---

## §0.5.6 F-INDEX-STALE PRE-gate

### §0.5.6.1 Failure code identity

F-INDEX-STALE is a Section-4-owned PRE-gate failure code (to be wired in the §4 v2.1 parent-backfill). Its `primitive_id` in the Index is `logician.pre_gate.f_index_stale`. Its severity tier is HARD-BLOCK (the pipeline cannot proceed without either Index amendment or explicit M13 bypass). Its failure family prefix is `F-INDEX-*` with a single subcode in v1: `F-INDEX-STALE.parent_hash_mismatch`. Additional subcodes (e.g., `F-INDEX-STALE.parent_version_mismatch`, `F-INDEX-STALE.parent_file_missing`) are v2 candidates if an audit surfaces the need to distinguish them; v1 collapses all staleness variants into the one subcode because the operator's remediation is identical.

### §0.5.6.2 Predicate definition

Given the current on-disk state of the Golden Quill and the Index at version `v{N}`, the predicate is:

```
def f_index_stale_predicate(index_version: int, repo_root: Path) -> PredicateResult:
    """
    Returns PASS if every parent section's current on-disk (version, hash)
    matches the Index v{index_version}'s recorded (version, hash) for that
    parent, FAIL with F-INDEX-STALE.parent_hash_mismatch otherwise.

    The predicate does NOT read the Markdown body of the Index; it reads the
    JSON companion at `section_00_5_interface_index.v{index_version}.json`
    because the JSON is canonical-signable and the Markdown is prose.
    """
    index_path = repo_root / "pipeline/blueprint/v0.1" / f"section_00_5_interface_index.v{index_version}.json"
    if not index_path.exists():
        return FAIL(subcode="parent_file_missing", detail=f"Index JSON v{index_version} not found")
    index = json.loads(index_path.read_bytes())
    per_parent = {}
    for row in index["rows"]:
        stem = row["defined_at"].split("#", 1)[0]
        key = (row["parent_lock_version"], row["parent_lock_commit_hash"])
        per_parent.setdefault(stem, set()).add(key)
    for stem, keys in per_parent.items():
        if len(keys) != 1:
            return FAIL(subcode="parent_hash_mismatch",
                        detail=f"Index rows under {stem} carry inconsistent (version, hash): {keys}")
        (recorded_version, recorded_hash), = keys
        # Sentinel-detect: a PARENT_UNLOCKED row carries recorded_hash = "0" * 128
        # and recorded_version ending in "-DRAFT". The Index explicitly marks this
        # parent as not-yet-locked; any pipeline run citing its primitives MUST fail
        # F-INDEX-STALE until the parent re-locks and the operator amends the Index.
        # Treat as mismatch regardless of on-disk hash (§0.5.6.1, §0.5.8.2).
        if recorded_hash == "0" * 128 or recorded_version.endswith("-DRAFT"):
            return FAIL(subcode="parent_hash_mismatch",
                        detail=f"{stem}: PARENT_UNLOCKED sentinel — parent must re-lock "
                               f"and Index must amend before citations resolve")
        parent_path = _resolve_parent_file(repo_root, stem)
        if not parent_path.exists():
            return FAIL(subcode="parent_file_missing", detail=f"Parent file {stem} not found")
        current_hash = sha3_512_hex(_canonical_bytes(parent_path))
        current_version = _extract_lock_version_from_header(parent_path)
        if current_hash != recorded_hash or current_version != recorded_version:
            return FAIL(subcode="parent_hash_mismatch",
                        detail=f"{stem}: recorded ({recorded_version}, {recorded_hash[:16]}…) "
                               f"vs current ({current_version}, {current_hash[:16]}…)")
    return PASS()
```

The predicate is pure: given identical inputs (repo state + Index version), it returns identical output. Stateless, no side effects. Called from Section 4's PRE-gate runner as a read-only check.

### §0.5.6.3 Slot placement in §4.2.1 PRE-gate table

The predicate occupies PRE-gate slot **#7** in Section 4 v2.1's PRE-gate ordered check table, immediately after slot #6 (trust-root mirror check). The ordering rationale, consistent with architecture v6-r2 §0.5.4, is that staleness detection must fire after the trust-root has been established (because the Index's own JSON is trust-root-signed — see §0.5.6.5 below) but before any RFA-dependent or run-state-dependent check (because those downstream checks cite Index-mediated primitives and would act on a stale pointer if F-INDEX-STALE had not already fired). Slot #7 in the v2 table was previously RFA dual-hash verification; in v2.1 that check shifts to slot #8 and the subsequent checks cascade by +1.

Section 4 v2.1's §4.2.1 table thus reads (in order): 1) Section 2 lock marker N.4.1, 2) Section 2 lock marker N.4.2, 3) Cedar policy bundle integrity, 4) router.yaml provider binding, 5) session_id allocation, 6) trust-root mirror γ, **7) F-INDEX-STALE**, 8) RFA dual-hash verification (was #7), 9) admin-risk ledger appendability (was #8), … through slot #19 (was #18). The wiring is a pure insertion; no downstream check changes semantics, only slot numbering.

### §0.5.6.4 Short-circuit behaviour

On F-INDEX-STALE FAIL, Section 4's PRE-gate runner halts pipeline entry immediately and returns the failure to the orchestrator with:
- `failure_code = "F-INDEX-STALE.parent_hash_mismatch"` (or the appropriate subcode).
- `failure_detail` = the predicate's detail string.
- `failing_parents` = list of parent file stems whose hash diverged.
- `index_version_in_use` = the Index version that was consulted.

No PRE-gate check after slot #7 runs on a FAIL. The orchestrator writes an ART-INDEX-DRIFT admin-risk ledger entry (see §0.5.7) and halts. The operator's remediation is either (a) amend the Index to v{N+1} and re-run, or (b) M13-authorised bypass (see §0.5.5.4). There is no retry loop — F-INDEX-STALE is not a transient failure.

On a retry-after-bypass run, F-INDEX-STALE re-evaluates fresh. The bypass ledger entry is read-only metadata; it does not mutate the predicate's input. If the bypass was a one-time decision and the operator did not amend the Index, F-INDEX-STALE FAILs again — and the orchestrator must see a new bypass entry with matching run_id before honouring it. Every run carries a unique run_id; a stale bypass entry cannot authorise a different run.

### §0.5.6.5 Trust-root binding

The Index's JSON companion is signed by the operator at each amendment via the signed-commit ledger (Section 2 v7 §4.9, M15). The PRE-gate predicate includes an inner check that the Index JSON's signature verifies against the operator's pubkey (reuses the `verify_calibration_report` signature discipline from Section 5 v5 §4.15 — same Ed25519 algorithm, same canonical-bytes rule). A valid Index signature is a precondition for any F-INDEX-STALE verdict; an invalid signature is itself an F-INDEX-STALE FAIL with subcode `F-INDEX-STALE.signature_invalid`.

This means the slot-7 predicate is logically three checks composed in sequence: (a) Index JSON exists and is well-formed; (b) Index JSON's signature verifies; (c) Index's recorded per-parent (version, hash) matches current on-disk per-parent (version, hash). Any of the three failing is an F-INDEX-STALE FAIL with the appropriate subcode. The predicate code in §0.5.6.2 elides the signature check for readability; the v2.1 wiring spec MUST include it explicitly.

### §0.5.6.6 Reason-tag taxonomy

Every F-INDEX-STALE FAIL carries one of a closed set of reason tags, written to the admin-risk ledger and the pipeline run log:
- `parent_hash_mismatch` — current parent file hash differs from Index's recorded hash for that parent.
- `parent_version_mismatch` — current parent file version string differs from Index's recorded version.
- `parent_file_missing` — a parent file named in the Index is not on-disk.
- `signature_invalid` — Index JSON signature did not verify.
- `schema_violation` — Index JSON does not satisfy the §0.5.3 schema (duplicate primitive_id, inconsistent per-parent version/hash, unknown primitive_kind, etc.).

The tag taxonomy is closed in v1; additional tags are v2 candidates. Each tag maps to the same severity (HARD-BLOCK) and the same orchestrator response (write ART-INDEX-DRIFT, halt). The differentiation exists for operator diagnostics and for the Monday cron digest's drift-pattern summary.

### §0.5.6.7 Interaction with M14 (complete mediation)

F-INDEX-STALE is a complete-mediation check: every pipeline run, every entry point, every time. No caching of PASS verdicts across runs (the v1 implementation explicitly does not cache; a future v0.2 may introduce a per-run memoisation with a cache-invalidation tie to parent file mtime, but v1 prefers the simple-and-correct hash check on every run because the cost is bounded). The check is cheap: SHA-3-512 of ~5 files of a few thousand lines each is sub-second on the M1 dev node, far below the threshold where caching would be justified.

---

## §0.5.7 ART-INDEX-DRIFT admin-risk entry

### §0.5.7.1 Entry identity

ART-INDEX-DRIFT is the admin-risk-ledger entry raised whenever F-INDEX-STALE FAILs at a pipeline PRE-gate. Its `primitive_id` in the Index is `arch.admin_risk.art_index_drift`. It is owned at the architecture layer (v6-r2 §0.5 names it) and persisted through Section 2 v7's admin-risk-append append-cas intent (§4.10.4 row 2). Severity tier: MEDIUM (blocks the current run, requires operator remediation, does not require whole-system audit — the failure is well-characterised and self-diagnosing from the reason-tag).

### §0.5.7.2 Entry schema

Each ART-INDEX-DRIFT entry carries:
- `art_id` = `ART-INDEX-DRIFT` (fixed).
- `run_id` = the pipeline run whose PRE-gate failed.
- `session_id` = the Section-2-issued session id for the run.
- `operator_org_slug` = the operator's org slug (always present; A1 single-client-per-Golden-Quill v0.1).
- `raised_at_iso` = ISO-8601 UTC timestamp.
- `failure_subcode` = one of the §0.5.6.6 tags.
- `failure_detail` = human-readable string from the predicate.
- `index_version_in_use` = the integer N from Index v{N}.
- `failing_parents` = list of parent file stems whose (version, hash) diverged.
- `current_parent_hashes` = dict {stem → current SHA-3-512 hex}.
- `recorded_parent_hashes` = dict {stem → Index-recorded SHA-3-512 hex}.
- `bypass_authorized` = boolean (true iff an M13 bypass entry covers this run_id).
- `bypass_ledger_pointer` = signed-commit-ledger reference to the bypass entry, if present.

The schema is canonical-JSON per §0.5.3.3. Signed by the Cedar policy ledger at append time (Section 2 v7 §4.10.4 row 2 handles the signing).

### §0.5.7.3 Detection source

ART-INDEX-DRIFT is written by Section 4's PRE-gate runner via the `admin_risk.record_bypass_authorization` call path in Section 4 v2 §4.7.3 (the function name is the same whether a bypass is authorised or not — the `bypass_authorized` field distinguishes). The admin-risk writer always writes the entry when F-INDEX-STALE fires, whether or not a bypass covers the run. The distinction matters for Monday cron drift-pattern analysis: a bypass-covered run still represents drift that was observed and proceeded-through, not absent drift.

### §0.5.7.4 Operator action

On seeing an ART-INDEX-DRIFT entry (via the Monday cron digest or ad-hoc operator review), the operator's action is:
1. Read the `failure_detail` and `failing_parents` fields.
2. Verify the parent file's current state (SHA-3-512 hash + version-string extraction).
3. Re-author the Index: open the current Index Markdown file, bump the version number, refresh every row under the failing parent(s) with the current (version, hash), refresh any `defined_at` paths that moved, refresh any `description` fields that went stale, sign the new JSON via the signed-commit ledger, commit the Markdown via the (forthcoming) `index-update` Vault intent.
4. Re-run the pipeline; F-INDEX-STALE should now PASS.

The operator action does NOT involve editing past ART-INDEX-DRIFT entries — the ledger is append-only and every entry is preserved for audit. A follow-up "resolved" entry can be written as a free-form operator note if desired, but this is not load-bearing and not schema-enforced in v1.

### §0.5.7.5 M13 bypass rules

Per §0.5.5.4, M13 permits operator-only bypass. The bypass rules for ART-INDEX-DRIFT:
- Bypass must be explicit (not implied): the operator writes a bypass entry at the signed-commit ledger BEFORE the run whose PRE-gate would otherwise fail.
- Bypass is per-run: the bypass entry names a specific run_id; other runs are not covered.
- Bypass requires the operator to acknowledge the drift: the bypass entry captures the Index version in use and the failing parents, mirroring the ART-INDEX-DRIFT entry.
- Bypass is rate-limited at operator policy (three in seven days flag; no hard cap in code).
- Bypass does NOT suppress the ART-INDEX-DRIFT entry — both are written.

The bypass mechanism exists for cases where an urgent pipeline run cannot wait for a full Index re-lock (e.g., a grant deadline hours away and a parent that re-locked for a non-substantive reason). The operator trades off correctness risk explicitly and carries the trade-off in the audit trail.

### §0.5.7.6 Interaction with Monday cron drift-pattern analysis

The Monday cron drift-pattern analysis reads the admin-risk ledger for the prior seven days, groups ART-INDEX-DRIFT entries by `failing_parents`, and surfaces any parent that appears in three or more entries in the window. This is a Log-level pattern detector (no code action, just operator awareness): repeated drift on the same parent is a sign that the parent is moving frequently and Index re-locks are lagging, which in turn suggests either the parent's lock cycle needs review or the Index re-lock process needs automation (a v0.2 candidate).

---

## §0.5.8 Index seed population (v3 current)

### §0.5.8.1 Population summary

The v3 Index seeds **81 rows** across six parent groupings. The grouping is Section-major: each parent section's rows are authored together in this subsection, ordered by `primitive_id` alphabetical within the group. The JSON companion re-orders globally by `primitive_id`. The Markdown grouping is for authoring/audit readability; neither ordering is authoritative for signing (the canonical-JSON hash is signing-authoritative).

Per-parent row counts (v3, post §1 re-lock 2026-04-18):
- Section 1 Sovereignty Envelope: **11 rows** (7 per-primitive N.2-export mechanisms + 4 policy-family aggregates) — new at v3; replaces the v1/v2 `sovereignty.marker.parent_unlocked` placeholder.
- Section 2 Vault v7: **18 rows** (primitives + schemas + constants + allowlist-row aggregates).
- Section 3 Scout v5: **7 rows** (mechanisms + state-machine + channel-families aggregate).
- Section 4 Logician v2: **23 rows** (18 PRE-gate checks + POST-gate + admin-risk writer + operator_signoff + gate_runner + allowlist aggregate).
- Section 5 Pipeline v5: **8 rows** (two entry points + contracts + failure-family + micro-recovery).
- Architecture v6-r2 M-family: **14 rows** (architecture-level M-* mechanisms; blueprint-level M-* sub-mechanisms carried by parent rows).

Total: 11 + 18 + 7 + 23 + 8 + 14 = **81 rows** (v3).

Version lineage: v1 / v2 = 71 rows (§1 placeholder = 1 row); v3 = 81 rows (§1 placeholder removed, 11 concrete §1 rows added).

Hash placeholders (`<SHA3_512_OF_PARENT>`) are filled in at Index JSON build-time by reading the actual parent file and hashing its canonical bytes. The Markdown body carries the placeholders for readability; the JSON companion carries the resolved values.

### §0.5.8.2 Section 1 Sovereignty Envelope (11 rows — v3)

v3 replaces the v1/v2 single `sovereignty.marker.parent_unlocked` placeholder row with eleven concrete rows derived from §1 v6 driver §14 (the §0.5 v2 → v3 amendment payload lock-emitted by §1 v6). Seven rows are N.2-export per-primitive Python-signature surfaces; four rows are policy-family aggregates covering trust boundary, fail-closed discipline, router signing orthogonality, and the M14.4.2 wrapper-manifest contract.

**Per-primitive rows (7):**

| primitive_id | defined_at | primitive_kind | description |
|---|---|---|---|
| `sovereignty.envelope.boot` | `section_1_v6#§3.2 + §9` | `mechanism` | Boot the SovereigntyEnvelope handle (wrapper-manifest verify, keystore resolve, router integrity, ledger boot, orphan-key sweep). |
| `sovereignty.session.start` | `section_1_v6#§3.3 + §4.2` | `mechanism` | Bind a new Session to RFAEnvelope + ProjectContextEnvelope; mint a session HMAC key in the keystore. |
| `sovereignty.session.checkpoint` | `section_1_v6#§3.9 + §3.9.1 + §4.6` | `mechanism` | Emit payload+manifest tuple to §2 v7 vault.vault_commit under runs/<run_id>/interrupted/; §1 produces bytes, §2 persists. |
| `sovereignty.audit.append` | `section_1_v6#§3.7 + §3.8 + §4.5 + §4.8` | `mechanism` | Append a typed event to admin_risk.jsonl or degradation.jsonl; trailer recompute + watermark update under single held fcntl lock. |
| `sovereignty.isolation.within_org_root` | `section_1_v6#§3.11d + §4.7` | `mechanism` | Predicate: is `path` inside `orgs/<org_slug>/`? v6 takes Vault adapter for vault_stat delegation (BT14 mount-identity). |
| `sovereignty.router.verify_integrity` | `section_1_v6#§3.10 + §3.10.1 + §4.4` | `mechanism` | Runtime-load HMAC-SHA3-512 verification of router.yaml; orthogonal to §4 boot-time git-sig gate (S5/M15). |
| `sovereignty.crypto.session_hmac_sign` | `section_1_v6#§3.3 + §4.6` | `mechanism` | HMAC-SHA3-512 sign over caller-supplied payload using session HMAC key; key never leaves §1's process scope. |

**Policy-family aggregate rows (4):**

| primitive_id | defined_at | primitive_kind | description |
|---|---|---|---|
| `sovereignty.policy.trust_boundary` | `section_1_v6#§0 + §10 F9b` | `invariant` | Trust-boundary policy — A1..A4 preflight assumptions cited by every downstream rejection of out-of-model attacks. |
| `sovereignty.policy.fail_closed_discipline` | `section_1_v6#§6 + §9` | `invariant` | Fail-closed discipline — every failure code in §1 hard-aborts; no §1 primitive returns a sentinel. |
| `sovereignty.policy.router_signing_orthogonality` | `section_1_v6#§3.10.1 + §4.4` | `invariant` | Orthogonality contract between §4 boot-time git-sig gate (S5/M15) and §1 runtime-load HMAC-SHA3-512 gate. |
| `sovereignty.policy.m14_4_2_wrapper_manifest_contract` | `section_1_v6#§9 step 1.5 + §6.9 + §8 WRAPPER_*` | `schema` | M14.4.2 wrapper manifest — Ed25519-signed pre-exec body (rlimits, env_allowlist, umask, cwd, wrapper_version). |

All eleven rows carry: `parent_lock_version = "v6"`, `parent_lock_commit_hash = b0d50a71f53dde3b9988750ba843875125b21c1234115bb4d38268e00818e61009a5948f611ac7c3ebb28daf6726b04759bbe649b3f52600882d62721c89d422` (SHA-3-512 of `section_1_sovereignty_envelope.md` v6 canonical bytes at v3 authoring time), `introduced_in_index_version = "v3"`, `stability_tier = "STABLE"`.

Optional fields:
- `sovereignty.isolation.within_org_root` carries `binds_to = "IDX:v3:vault.primitive.vault_stat"` (BT14 mount-identity delegation).
- `sovereignty.isolation.within_org_root` carries optional `obsoletes = ["sovereignty.isolation.within_org_root.v5"]` in the driver's §14 amendment payload; the Index's per-row schema does not carry an `obsoletes` field (§0.5.3 defines only eight required + two optional `binds_to`/`consumed_by`), so this metadata is retained in the §1 v6 driver's §14 record but not mirrored in the Index row — obsolescence tracking is load-bearing for §1's own change discipline, not for Index lineage. Future §0.5 revisions may add an `obsoletes` optional field if cross-section obsolescence tracking becomes necessary.

**Removed from v2:** the single placeholder row `sovereignty.marker.parent_unlocked` (defined_at `section_1_v5#§1`, stability_tier `PARENT_UNLOCKED`, v5-DRAFT parent). That row existed only to make F-INDEX-STALE trip on any transitive §1 citation while §1 was unlocked; with §1 v6 now LOCKED, the eleven concrete rows above are the sole §1 surface in the Index.

### §0.5.8.3 Section 2 Vault v7 (18 rows)

| primitive_id | defined_at | primitive_kind | description |
|---|---|---|---|
| `vault.primitive.vault_read` | `section_02_v7#§4.2` | `mechanism` | Vault read primitive: `vault_read(path, intent, session_id, slug) -> bytes`. |
| `vault.primitive.vault_write` | `section_02_v7#§4.3` | `mechanism` | Vault write primitive with three commit-mode envelope. |
| `vault.primitive.commit_semantics` | `section_02_v7#§4.10` | `mechanism` | Three commit modes: overwrite, write-if-absent, append-cas. |
| `vault.allowlist.static_table_5_entries` | `section_02_v7#§4.10.4` | `allowlist-row` | 5-entry static path-allowlist hard-coded in vault_write.py (intent, path-prefix-suffix pairs). |
| `vault.primitive.tombstone` | `section_02_v7#§4.7` | `mechanism` | Tombstone primitive for soft-delete semantics under CAS. |
| `vault.ledger.session_ledger` | `section_02_v7#§4.8` | `schema` | Per-session append-only ledger capturing all vault_read/vault_write calls. |
| `vault.ledger.signed_commit_ledger` | `section_02_v7#§4.9` | `schema` | M15 signed-commit ledger: every vault_write commit signed, Ed25519. |
| `vault.serde.canonical_json` | `section_02_v7#§4.11` | `mechanism` | Canonical-JSON serializer (sorted keys, UTF-8, LF, no trailing whitespace). |
| `vault.merkle.daily_root` | `section_02_v7#§4.12` | `mechanism` | Daily Merkle root computation over session ledger for tamper-evidence. |
| `vault.merkle.daily_rotation` | `section_02_v7#§4.12.2` | `mechanism` | Daily ledger rotation and archival under Merkle root. |
| `vault.primitive.fsync_discipline` | `section_02_v7#§4.4` | `mechanism` | fsync on commit + fsync on parent dir; crash-safety contract. |
| `vault.hash.sha3_512` | `section_02_v7#§4.11.1` | `constant` | Hash algorithm binding: SHA-3-512 for all vault content hashing. |
| `vault.allowlist.admin_risk_append` | `section_02_v7#§4.10.4 row 2` | `allowlist-row` | append-cas allowlist row for admin-risk ledger writes. |
| `vault.envelope.budget` | `section_02_v7#§4.13` | `schema` | Budget envelope: per-call token + latency + retries limits. |
| `vault.schema.session_id_format` | `section_02_v7#§3.2` | `schema` | session_id format: `{run_type}-{operator_slug}-{yyyymmddThhmmssZ}-{8hex}`. |
| `vault.schema.slug_format` | `section_02_v7#§3.3` | `schema` | Slug format: `[a-z][a-z0-9_]*` with length bounds. |
| `vault.schema.path_prefix` | `section_02_v7#§3.4` | `schema` | Path-prefix schema for vault-relative paths. |
| `vault.schema.intent_vocabulary` | `section_02_v7#§3.5` | `schema` | Closed intent vocabulary: 20 intents as of v7. |

Each row carries `parent_lock_version = "v7"`, `parent_lock_commit_hash = <SHA3_512_OF_section_02_vault_topology.md>` (resolved at JSON build-time), `introduced_in_index_version = "v1"`, and `stability_tier = "STABLE"`. The allowlist row and admin-risk-append row both note `binds_to` relationships (the 5-entry aggregate binds to the Logician allowlist aggregate row in §0.5.8.5 below).

### §0.5.8.4 Section 3 Scout v5 (7 rows)

| primitive_id | defined_at | primitive_kind | description |
|---|---|---|---|
| `scout.invariant.ast_preflight` | `section_03_v5#§7.16` | `invariant` | AST-PREFLIGHT: literal-only `Final[bool]` initializers; cross-module bounded resolution. |
| `scout.constant.alias_walker_max` | `section_03_v5#§7.16` | `constant` | `MAX_ALIAS_WALKER_STEPS = 1000` termination guard for AST alias walk. |
| `scout.mechanism.drain_parser_buffer` | `section_03_v5#§4.5` | `mechanism` | `_drain_parser_buffer` hasattr-dispatch with FD-release guarantee. |
| `scout.mechanism.six_channel_families` | `section_03_v5#§2` | `mechanism` | Six parallel-primary discovery channels A-F (federal APIs, cached datasets, portals, program pages, RSS, client-driven search). |
| `scout.state_machine.discover_verify_review` | `section_03_v5#§3` | `mechanism` | DISCOVER → VERIFY → REVIEW three-stage state machine with human-gate at REVIEW. |
| `scout.semantic.cache_parallel_primary` | `section_03_v5#§2.1` | `invariant` | Cached datasets are parallel-primary sources, not fallback; equal footing with live APIs. |
| `scout.mechanism.golden_template_fallback` | `section_03_v5#§2.4` | `mechanism` | Vault empty → fall back to `vault_shared/templates/{program_type}.md`; tagged [TEMPLATE_SCAFFOLD]. |

All rows: `parent_lock_version = "v5"`, `parent_lock_commit_hash = <SHA3_512_OF_section_03_scout.md>`, `introduced_in = "v1"`, `stability_tier = "STABLE"`.

### §0.5.8.5 Section 4 Logician v2 (22 rows)

Eighteen PRE-gate check rows plus four cross-cutting rows.

PRE-gate check rows (slots #1–#18 per Section 4 v2 §4.2.1; note that in v2.1 parent-backfill, F-INDEX-STALE is inserted at slot #7 and all slots #7–#18 shift to #8–#19 — the Index rows below enumerate the v2 state; the v2.1 refresh updates both `defined_at` subsection pointers AND the stability_tier on the affected rows to PENDING_PARENT_BACKFILL until v2.1 lands):

| primitive_id | defined_at | description |
|---|---|---|
| `logician.pre_gate.check_01_section2_lock_marker_n41` | `section_04_v2#§4.2.1 row 1` | Check #1: Section 2 lock marker N.4.1 verified. |
| `logician.pre_gate.check_02_section2_lock_marker_n42` | `section_04_v2#§4.2.1 row 2` | Check #2: Section 2 lock marker N.4.2 verified (trust-root mirror α). |
| `logician.pre_gate.check_03_cedar_policy_bundle` | `section_04_v2#§4.2.1 row 3` | Check #3: Cedar policy bundle integrity verified. |
| `logician.pre_gate.check_04_router_binding` | `section_04_v2#§4.2.1 row 4` | Check #4: router.yaml provider binding matches session requirements. |
| `logician.pre_gate.check_05_session_id_allocation` | `section_04_v2#§4.2.1 row 5` | Check #5: session_id allocated and not reused. |
| `logician.pre_gate.check_06_trust_root_mirror_gamma` | `section_04_v2#§4.2.1 row 6` | Check #6: trust-root mirror γ fresh. |
| `logician.pre_gate.check_07_rfa_dual_hash` | `section_04_v2#§4.2.1 row 7` | Check #7 (v2; shifts to #8 in v2.1): RFA dual-hash verification. |
| `logician.pre_gate.check_08_admin_risk_ledger_appendable` | `section_04_v2#§4.2.1 row 8` | Check #8 (v2): admin-risk ledger appendability. |
| `logician.pre_gate.check_09_session_ledger_appendable` | `section_04_v2#§4.2.1 row 9` | Check #9 (v2): session ledger appendability. |
| `logician.pre_gate.check_10_scribe_phase_routing` | `section_04_v2#§4.2.1 row 10` | Check #10 (v2): Scribe phase routing precondition. |
| `logician.pre_gate.check_11_operator_signoff_present` | `section_04_v2#§4.2.1 row 11` | Check #11 (v2): operator_signoff present when required. |
| `logician.pre_gate.check_12_consent_envelope_valid` | `section_04_v2#§4.2.1 row 12` | Check #12 (v2): consent envelope valid. |
| `logician.pre_gate.check_13_budget_envelope_valid` | `section_04_v2#§4.2.1 row 13` | Check #13 (v2): budget envelope valid. |
| `logician.pre_gate.check_14_cross_family_binding` | `section_04_v2#§4.2.1 row 14` | Check #14 (v2): cross-family rigor (reviewer family ≠ author family). |
| `logician.pre_gate.check_15_org_isolation_guard` | `section_04_v2#§4.2.1 row 15` | Check #15 (v2): Law 3 org-isolation guard. |
| `logician.pre_gate.check_16_admin_risk_term_scan` | `section_04_v2#§4.2.1 row 16` | Check #16 (v2): Law 4 admin-risk term scan precondition. |
| `logician.pre_gate.check_17_rfa_scope_bind` | `section_04_v2#§4.2.1 row 17` | Check #17 (v2): Law 1 RFA-is-source-of-truth binding. |
| `logician.pre_gate.check_18_applicant_substance` | `section_04_v2#§4.2.1 row 18` | Check #18 (v2): Law 5 applicant-brings-substance precondition. |

Cross-cutting rows:

| primitive_id | defined_at | primitive_kind | description |
|---|---|---|---|
| `logician.post_gate.check_list` | `section_04_v2#§4.2.2` | `post-gate-check` | POST-gate ordered check list: word count, SMART outcomes, admin-risk terms (batched), claim-evidence. |
| `logician.mechanism.admin_risk_ledger_writer` | `section_04_v2#§4.7.3` | `mechanism` | Admin-risk ledger writer: append-cas via Section 2 v7 §4.10.4 row 2. |
| `logician.mechanism.operator_signoff` | `section_04_v2#§4.5` | `mechanism` | operator_signoff primitive: explicit acknowledgement required at defined gates. |
| `logician.mechanism.gate_runner` | `section_04_v2#§5.4` | `interface-contract` | gate_runner.run_pre_gate / run_post_gate: the callable surface Section 5 consumes. |
| `logician.allowlist.v2_table` | `section_02_v7#§4.10.4` | `allowlist-row` | Aggregate row: Logician's 20 consumed intents, anchored at Section 2's authoritative 5-entry static allowlist; `binds_to = IDX:v1:vault.allowlist.static_table_5_entries` and `consumed_by = IDX:v1:logician.mechanism.gate_runner`. |

Wait — row count audit: 18 PRE-gate + 5 cross-cutting = 23 rows, not 22. The `logician.allowlist.v2_table` and `logician.mechanism.admin_risk_ledger_writer` both effectively wrap the same append-cas allowlist row at §4.10.4 row 2; in v1 the Index treats them as distinct (one is the cross-section allowlist aggregate, one is the Logician-internal wrapper mechanism), but for count discipline §0.5.8.1's "22 rows" was a planning estimate — the final v1 count for §4 is **23 rows**. The total thus comes to 71, not 70.

(Planning-vs-authored discrepancy surfaced during row drafting; the planning estimate under-counted by one because I initially treated `logician.allowlist.v2_table` as a sub-row of `logician.mechanism.admin_risk_ledger_writer`. On reflection they are orthogonal: the allowlist aggregate is what Section 4 consumes from Section 2; the admin-risk writer is Section 4's own wrapper. Both deserve independent Index rows. §0.5.8.1's summary and §0.5.11's changelog both reflect the corrected total of 71.)

All §4 rows: `parent_lock_version = "v2"`, `parent_lock_commit_hash = <SHA3_512_OF_section_04_logician.md>`, `introduced_in = "v1"`, `stability_tier = "STABLE"` (for v2 state) — except `logician.pre_gate.check_07_rfa_dual_hash` through `check_18_applicant_substance` which carry `stability_tier = "PENDING_PARENT_BACKFILL"` because the v2.1 backfill will shift their slot numbers and the Index v2 amendment must follow.

### §0.5.8.6 Section 5 Pipeline v6 (10 rows — 8 rows from v5, 2 rows added at v6 LOCK 2026-04-19)

| primitive_id | defined_at | primitive_kind | description |
|---|---|---|---|
| `pipeline.entry.submission_mode` | `section_05_v6#§1` | `mechanism` | Primary pipeline entry point: RFA → council → signed SubmissionBundle. |
| `pipeline.entry.eval_mode` | `section_05_v6#§1` | `mechanism` | Secondary entry point: operator calibration harness → signed CalibrationReport. |
| `pipeline.mechanism.scribe_phase_routing` | `section_05_v6#§4` | `mechanism` | Scribe three-phase routing: outline (P1) → per-section drafting (P2) → assembly (P3). |
| `pipeline.contract.editor` | `section_05_v6#§5.2` | `interface-contract` | Editor seat contract: input, output, rubric, cross-family rigor. |
| `pipeline.contract.judge` | `section_05_v6#§5.3` | `interface-contract` | Judge seat contract: input, output, rubric library, cross-family rigor. |
| `pipeline.contract.red_team` | `section_05_v6#§5.4` | `interface-contract` | Red Team seat contract: attack buckets A/B/C + OUT-OF-MODEL. |
| `pipeline.failure_family.f_pipe_star` | `section_05_v6#§6` | `failure-code` | F-PIPE-01 through F-PIPE-23 pipeline-level failure code family (F-PIPE-23 added at v6). |
| `pipeline.mechanism.micro_recovery_routing` | `section_05_v6#§5.4` | `mechanism` | Micro-recovery routing table: per-failure-type backward routing without full rewind. |
| `per_invocation_telemetry_record_schema` | `section_05_v6#§5.7` | `schema` | InvocationRecord 8-field schema: run_id, seat, timestamp, model_family_resolved, token_count_input, token_count_output, success_flag, latency_ms. Pinned at §5 v6 LOCK 2026-04-19 per scope-close Item 2. |
| `str_derivation_and_aggregation` | `section_05_v6#§5.8` | `mechanism` | STR (Success-to-Token Ratio) derivation rule (success_flag / token_sum, None when token_sum=0) + STRWindow rolling per-seat distribution accumulator (k=5 W=30d per A11 R.6 discipline). Feeds Canary (§4 v2.4 target-LOCK). |

v5 rows (first 8): `parent_lock_version = "v5"` (v5 introduced_in = "v1", v6 parent pointer updated to v6 per this LOCK). v6 rows (last 2): `parent_lock_version = "v6"`, `parent_lock_commit_hash = <SHA3_512_OF_section_05_pipeline.md_at_v6_LOCK>` (resolved at JSON build step post-LOCK 2026-04-19), `introduced_in = "v5"` (index v5 — this paired commit), `stability_tier = "STABLE"`.

### §0.5.8.7 Architecture v7 M-family (14 rows — parent refreshed v6-r2 → v7 at Index v4)

M-family architectural mechanisms indexed at architecture lock version. Blueprint-level sub-mechanisms of any M-N are carried by the parent M-N row, not split. **v4 refresh (2026-04-19):** parent moved from v6-r2 → v7 A1-A12 LOCKED; row content unchanged because v7 introduced zero new M-family mechanisms (v7 §0 scope boundary preserved M14/M15/M14.x verbatim).

| primitive_id | defined_at | description |
|---|---|---|
| `arch.m.m01_trust_root` | `tilth_architecture_locked#§M1` | Trust-root binding: operator pubkey + SHA-3-512 content hashing across all signed artefacts. |
| `arch.m.m02_cedar_policy` | `tilth_architecture_locked#§M2` | Cedar policy evaluation model: allow/deny on (principal, action, resource, context). |
| `arch.m.m03_session_envelope` | `tilth_architecture_locked#§M3` | Session envelope: session_id, operator_org_slug, intent, budget, timestamps. |
| `arch.m.m04_org_isolation` | `tilth_architecture_locked#§M4` | Law 3 org isolation: one PROJECT_CONTEXT per session, no cross-org data. |
| `arch.m.m05_rfa_truth` | `tilth_architecture_locked#§M5` | Law 1 RFA-is-source-of-truth: every claim traces to the RFA. |
| `arch.m.m06_apolitical_scan` | `tilth_architecture_locked#§M6` | Law 4 apolitical + admin-risk term scan: two-axis, operator approves each substitution. |
| `arch.m.m07_applicant_substance` | `tilth_architecture_locked#§M7` | Law 5 applicant brings substance: no fabrication of credentials, data, partnerships. |
| `arch.m.m08_cross_family_rigor` | `tilth_architecture_locked#§M8` | L-003 cross-family review: reviewer model family ≠ author model family at review/scoring gates. |
| `arch.m.m09_save_state_always` | `tilth_architecture_locked#§M9` | Autonomy Rule 1: save state on both success and failure. |
| `arch.m.m10_test_own_work` | `tilth_architecture_locked#§M10` | Autonomy Rule 2: test-before-marking-complete (Bug #20 magic step). |
| `arch.m.m11_be_explicit` | `tilth_architecture_locked#§M11` | Autonomy Rule 3: explicit input path, output path, scope, done-definition per hop. |
| `arch.m.m12_clean_output` | `tilth_architecture_locked#§M12` | Autonomy Rule 4: strip markdown fences, fluff, self-commentary; validate format. |
| `arch.m.m14_complete_mediation` | `tilth_architecture_locked#§M14` | Complete mediation: every gate checks every run, no cache that defeats the check. |
| `arch.m.m15_signed_commit_ledger` | `tilth_architecture_locked#§M15` | Signed-commit ledger: Ed25519 signature on every commit, per-operator pubkey trust-root. |

(M13 operator-only bypass is not indexed as a standalone M-row in v1 because it is a policy overlay on top of M14, not a mechanism with its own definition site. It is referenced from the ART-INDEX-DRIFT entry's bypass semantics at §0.5.7.5. If a future audit surfaces the need for an explicit M13 row, v2 adds it.)

All rows: `parent_lock_version = "v7"`, `parent_lock_commit_hash = "24fb706c1bb33ca08d4acecf7dee57fcd375a1b5872668be7d12dd4b5a79c5e09a95a10227882fcf39eb0efb332ee74e53774f7baac7d2b6d2a7bb826222a568"` (v7 A1-A12 canonical SHA3-512, updated at Index v4 refresh 2026-04-19), `introduced_in = "v1"`, `stability_tier = "STABLE"`.

### §0.5.8.8 Architecture v7 A1-A6 amendments (7 rows — Index v4 new)

v4 refresh adds seven architecture-level rows aggregating 10 A1-A6 failure-code primitives + Section N.1 row-count update + Section R pull-forwards. Aggregation follows §4 Logician v3 precedent (one row per amendment zone; description enumerates component primitives).

| primitive_id | defined_at | primitive_kind | description |
|---|---|---|---|
| `architecture.k.hardware_triple_target` | `tilth_architecture_v7#§K` | `mechanism` | A1 hardware triple-target: Pro DGX Spark primary + Mac Studio 128GB secondary; Baseline Mac Studio 128GB; Dev M1 Mini 8GB. 128 GB floor. BT14 eBPF scope clarified to observability tooling only. |
| `architecture.d_7.opus_47_envelope` | `tilth_architecture_v7#§D.7` | `mechanism` | A2 Block 1 + Block 2: Opus 4.7 API envelope (no temp/top_p/top_k; effort xhigh/max; beta task-budgets-2026-03-13; max_tokens ≥ 64000; tokenizer 1.0-1.35×) + Code Thesis Committee LOCKED 2026-04-18 (5 reviewers all-PASS 1-retry + F-CODE-RETRY-OVERRUN escalation). **Failure codes: F-ROUTER-STALE-API, F-CODE-COMMITTEE-INCOMPLETE, F-CODE-RETRY-OVERRUN.** |
| `architecture.f_1.sfr_certificate_format` | `tilth_architecture_v7#§F.1` | `mechanism` | A3 Semi-Formal Reasoning three-block verdict format (Premises / Execution trace / Conclusion). POST-gate structural only; semantic correctness defended by cross-family ensemble. Editor exempt. **Failure code: F-VERDICT-CERT-MALFORMED.** |
| `architecture.d_8.context_rot_floor` | `tilth_architecture_v7#§D.8` | `mechanism` | A4 context-rot mitigation — load-bearing constraints at BOTH start AND end of all seat prompts. Architectural FLOOR; middle-contradiction delegated to §6 Operating Envelope. **Failure code: F-CONTEXT-PLACEMENT.** |
| `architecture.r_1.tdsl_v02_horizon` | `tilth_architecture_v7#§R.1` | `invariant` | A5 Tilth Domain Semantic Layer v0.2 horizon. Per-node grant-domain KB + federated P2P sync + Buried Treasure sovereignty. v0.1 containment. **Failure code: F-TDSL-LEAK-V01.** |
| `architecture.r_pullforwards_enforcement` | `tilth_architecture_v7#§3.7 + §3.8 + §R.PF1 + §R.PF2` | `invariant` | A6 two v0.1 architectural pull-forwards: R.PF1 §5 track-abstraction extensibility + R.PF2 §2 operational-data extensibility. Enforcement via future-round Thesis audit at LOCK-time of §5 v6 / §2 v7.2. **Failure codes: F-PIPELINE-TRACK-FROZEN (dormant), F-VAULT-ARTIFACT-ONLY (dormant).** **stability_tier: DORMANT** (Cycle-2 RT-v4-F3 closure). **dormant_activation_condition:** "LOCK-time of Section 5 v6 spin (F-PIPELINE-TRACK-FROZEN) or Section 2 v7.2 spin (F-VAULT-ARTIFACT-ONLY)". |
| `architecture.n_1.row_count_6` | `tilth_architecture_v7#§N.1` | `invariant` | Section N.1 row count 5 → 6. Adds §6 Operating Envelope. **Failure codes: F-N1-COUNT-STALE, F-SECTION-R-INCOMPLETE.** |

All seven rows: `parent_lock_version = "v7"`, `parent_lock_commit_hash = <v7 SHA3-512>`, `introduced_in_index_version = "v4"`, `stability_tier = "STABLE"` (except `architecture.r_pullforwards_enforcement` which carries `stability_tier = "DORMANT"`).

### §0.5.8.9 Architecture v7 A7 pipeline windowing + machine-tier calibration (3 rows — Index v4 new)

| primitive_id | defined_at | primitive_kind | description |
|---|---|---|---|
| `architecture.s_1.windowing_primitive` | `tilth_architecture_v7#§S.1` | `mechanism` | A7 pipeline windowing. Token-budget function; window boundary opens fresh session via Option-B compound-txn. Hardware-tier safety margins Pro 5% / Baseline 10% / Dev 20%. **Failure code: F-A7-WINDOW-BUDGET-OVERFLOW.** |
| `architecture.s_1.machine_tier_calibration` | `tilth_architecture_v7#§S.1` | `mechanism` | A7.3 signed machine-calibration artifact at `vault_shared/machine_calibration.json`. BT14.g.1 extension; 90-day TTL; OD-6=γ. **Failure codes: F-A7-CALIBRATION-MISSING, F-A7-CALIBRATION-STALE, F-A7-CALIBRATION-UNSIGNED.** |
| `architecture.s_1.grantwriter_invisibility_invariant` | `tilth_architecture_v7#§S.1 A7.5 + §S.3` | `invariant` | A7.5 grantwriter-invisibility: tokens/cache/window/calibration NEVER surface. Quality events surface via rails-report (P8) or P-interrupt. Mapping table at §S.1. **Failure code: F-A7-CROSS-WINDOW-CONTRADICTION (POST, fires P6).** |

All three rows: `parent_lock_version = "v7"`, `parent_lock_commit_hash = <v7 SHA3-512>`, `introduced_in_index_version = "v4"`, `stability_tier = "STABLE"`.

### §0.5.8.10 Architecture v7 A8 Phase 0 intake + H-I-L surface (3 rows — Index v4 new)

| primitive_id | defined_at | primitive_kind | description |
|---|---|---|---|
| `architecture.s_2.phase_0_intake` | `tilth_architecture_v7#§S.2` | `mechanism` | A8 Phase 0 Intake five steps: Ingest / Dissect / Eligibility / Substance-gap / Cross-check. OD-1=a RFA-parsed section list; OD-2=A grant-agnostic dissection rubric. **Failure codes: F-INTAKE-ELIGIBILITY-FAIL, F-INTAKE-SUBSTANCE-GAP, F-INTAKE-DISSECTION-VERIFY-FAIL.** |
| `architecture.s_2.three_tag_claim_evidence_map` | `tilth_architecture_v7#§S.2.2` | `schema` | A8.2 three-tag claim-evidence map extending BT7: Source + RFA + Dialect tags. **Failure codes: F-P-COHERE-1, F-P-COHERE-2, F-P-COHERE-3.** Binds to `IDX:v4:vault.primitive.vault_write` via §2 claim_evidence append-cas. |
| `architecture.s_3.hil_eight_point_surface` | `tilth_architecture_v7#§S.3` | `invariant` | A8 H-I-L surface taxonomy — exactly 8 points P1-P8. Ninth-is-bug invariant. Every quality event maps to a P-surface. |

All three rows: `parent_lock_version = "v7"`, `parent_lock_commit_hash = <v7 SHA3-512>`, `introduced_in_index_version = "v4"`, `stability_tier = "STABLE"`.

### §0.5.8.11 Architecture v7 A9-A11 Commons (3 rows — Index v4 new)

| primitive_id | defined_at | primitive_kind | description |
|---|---|---|---|
| `architecture.r_4.dissection_commons` | `tilth_architecture_v7#§R.4` | `mechanism` | A9 Dissection Commons. Content-addressed signed artifact store. Opt-in toggles OD-3/4=ON. Default-deny upload whitelist. v0.2 dual-path IPFS + GitHub mirror (OD-5). Poisoning defense 3-axis re-verify. **Failure codes: F-COMMONS-SIGNATURE-INVALID, F-COMMONS-RUBRIC-STALE, F-COMMONS-DISSECTION-MISMATCH, F-COMMONS-UPLOAD-SCOPE-LEAK.** |
| `architecture.r_5.opportunity_commons_tier1` | `tilth_architecture_v7#§R.5` | `mechanism` | A10 Opportunity Commons Tier-1 extension of R.4. Fleet radar convergence. Client-isolation invariant. OD-9 every observation. Batch-interval (delegated §13.4). **Failure codes: F-OPPORTUNITY-TIER1-POISON, F-OPPORTUNITY-TIER1-UPLOAD-SCOPE-LEAK.** |
| `architecture.r_6.telemetry_commons` | `tilth_architecture_v7#§R.6` | `mechanism` | A11 Telemetry Commons — process telemetry flows; grant content never. K-anonymity k=5/W=30d fail-closed (OD-7). DP-annotated aggregates. Minimum-bucket-size ≥ k (delegated anti-suppression §13.5). v0.1 pull-forward. **Failure codes: F-TELEMETRY-K-ANON-VIOLATION, F-TELEMETRY-PAYLOAD-SCOPE-LEAK.** |

All three rows: `parent_lock_version = "v7"`, `parent_lock_commit_hash = <v7 SHA3-512>`, `introduced_in_index_version = "v4"`, `stability_tier = "STABLE"`.

### §0.5.8.12 Architecture v7 A12 crypto-agility (1 row — Index v4 new)

| primitive_id | defined_at | primitive_kind | description |
|---|---|---|---|
| `architecture.t.crypto_agility_migration` | `tilth_architecture_v7#§T` | `mechanism` | A12 post-quantum crypto-agility. v0.1 generic `OperatorSignature` dataclass. v0.2 hybrid Ed25519 + ML-DSA-65 (OD-8) BOTH-legs-valid. v0.3 pure ML-DSA. P2P hybrid ECDH + ML-KEM-768. Symmetric HMAC-SHA3-512/SHA-3-512 stays. **Failure code: F-CRYPTO-AGILITY-HARDCODED (continuous CTC enforcement).** |

Row: `parent_lock_version = "v7"`, `parent_lock_commit_hash = <v7 SHA3-512>`, `introduced_in_index_version = "v4"`, `stability_tier = "STABLE"`.

### §0.5.8.13 Architecture v7 Section 13 downstream blueprint closure obligations (1 row — Index v4 new)

| primitive_id | defined_at | primitive_kind | description |
|---|---|---|---|
| `architecture.section_13.delegated_closure_obligations` | `tilth_architecture_v7#§13` | `invariant` | Five delegated residuals with binding audit obligation on named downstream backfills: §13.1 H-02 cosmetic-tolerance → §5 v5.1; §13.2 H-04 direct-push → §6 Operating Envelope + §5 v5.1; §13.3 M-01 whitelist erosion → §6 Operating Envelope; §13.4 M-03 batch-interval → §3 Scout v5.1; §13.5 M-04 suppressible-suppression → §4 Logician v2.2. Pattern matches A6 R.PF1/R.PF2 dormant-future-round-audit enforcement. |

Row: `parent_lock_version = "v7"`, `parent_lock_commit_hash = <v7 SHA3-512>`, `introduced_in_index_version = "v4"`, `stability_tier = "STABLE"`.

### §0.5.8.14 Total row count reconciliation

**v5 current (2026-04-19):** 11 (§1) + 18 (§2) + 7 (§3) + 23 (§4) + **10** (§5 v6) + 14 (arch M-family v7) + 18 (arch v7 A1-A12 new) = **101 rows**.

**v4 → v5 delta (2026-04-19):** +2 new §5 rows (per_invocation_telemetry_record_schema, str_derivation_and_aggregation). §5 row parent pointer updated v5 → v6. All other rows unchanged.

**v4 (2026-04-19):** 11 (§1) + 18 (§2) + 7 (§3) + 23 (§4) + 8 (§5) + 14 (arch M-family v7) + 18 (arch v7 A1-A12 new) = **99 rows**.

**v3 → v4 delta (2026-04-19):** +18 new architecture-layer rows across §0.5.8.8 (7 A1-A6 rows) + §0.5.8.9 (3 A7 rows) + §0.5.8.10 (3 A8+HIL rows) + §0.5.8.11 (3 Commons rows) + §0.5.8.12 (1 A12 row) + §0.5.8.13 (1 §13 row). Zero changes to blueprint-layer rows (§1-§5 preserved at their own LOCKED parent versions). 14 M-family rows updated to parent_lock_version=v7 + v7 hash; row content unchanged.

**v3 history (2026-04-18):** 11 (§1) + 18 (§2) + 7 (§3) + 23 (§4) + 8 (§5) + 14 (arch) = 81 rows. v3 expanded §1 from 1 placeholder to 11 concrete rows (+10 net).

**v1/v2 history (2026-04-18):** 71 rows each (§1 placeholder at 1 row).

The §4 row count (23) was corrected from a 22-row planning estimate during v1 authoring per §0.5.8.5; v2/v3/v4 carry that correction forward unchanged. The §0.5.11.1 changelog narrates the v4 amendment. The JSON companion `section_00_5_interface_index.v4.json` (to be rebuilt post-LOCK) and the Markdown body of this document both reflect 99.

---

## §0.5.9 Update lifecycle

### §0.5.9.1 When a parent locks

The triggering event is: a parent blueprint section completes an L-005 strict audit cycle with unanimous Thesis Team READY_TO_LOCK and the operator commits the LOCKED version to the workspace. At that moment, every Index row under the parent may need refresh. The operator (not automation) is the authoring agent for the Index amendment.

The sequence:

1. Parent locks, operator commits the new parent file, the new file's SHA-3-512 canonical-bytes hash differs from what the Index has recorded.
2. Operator opens the current Index Markdown (`section_00_5_interface_index.md`) and identifies every row whose `defined_at` stem matches the parent.
3. Operator re-reads each affected row's subsection in the new parent to verify `defined_at`, `description`, and `primitive_kind` are still accurate; refreshes any that moved.
4. Operator updates `parent_lock_version` + `parent_lock_commit_hash` on every row under the parent (even rows whose `defined_at`/`description` did not need refresh — the hash changed, so the recording must update).
5. Operator bumps the Index version header from v{N} to v{N+1}.
6. Operator appends a changelog paragraph to §0.5.11 narrating the amendment.
7. Operator rebuilds the JSON companion via the build tool (`pipeline/tools/build_interface_index_json.py`, deferred scope; v1 operator hand-writes the JSON to match the Markdown).
8. Operator signs the new JSON via the signed-commit ledger (M15) and commits both files via the `index-update` Vault intent (forward-dep on Section 2 v7.1).
9. Operator re-runs any pending pipeline run; F-INDEX-STALE now PASSes.

### §0.5.9.2 Operator-authored, not automated

The Index is hand-authored by the operator at each amendment. The rationale: (a) the Index is a small, bounded artefact (~70 rows for v0.1, growing sub-linearly with the system), so automation overhead is not justified; (b) hand-authoring forces the operator to re-read the parent and catch semantic drift the audit seats would have missed; (c) hand-authoring ensures the operator's judgement is in the loop for `description` and `primitive_kind` fields that cannot be mechanically derived. An automated build step (hash computation, JSON serialization) for the JSON companion from the Markdown body is v0.2 scope; v1 requires the operator to keep the Markdown and JSON consistent by hand.

The M13 bypass mechanism (§0.5.5.4) is the only automation-adjacent workflow in v1: the operator can authorise a one-off bypass for a specific run without full Index amendment, but this is explicit operator action, not background automation.

### §0.5.9.3 Forward-dep: `index-update` Vault intent

The Section 2 v7.1 parent-backfill (to be authored after this §0.5 locks) adds a new allowlist row to the Section 2 static 5-entry allowlist. The new row's `(intent_string, path_prefix_suffix)` pair is:
- `intent_string = "index-update"`
- `path_prefix_suffix = ("pipeline/blueprint/v0.1/", ".v{N}.json")` where `{N}` is a variable matching positive integers (pattern-matched at allowlist evaluation).

The `index-update` intent commits at mode `write-if-absent` (Section 2 v7 §4.10 semantics): the target filename includes the Index version, and every Index version file is written exactly once. A v{N+1} write does not overwrite v{N} — prior versions are preserved for audit trail.

Audit-stamping: every `index-update` commit carries the operator's pubkey signature via M15 signed-commit ledger and an append-cas entry to a new session-ledger sub-kind (`ledger_kind = "index_amendment"`, fields `index_version_before`, `index_version_after`, `operator_reason`, `affected_parent_stems`).

The intent is deliberately tight: only operator can write (Cedar principal policy), only one writing mode (write-if-absent), only one path pattern (Index JSON files in the blueprint directory). This eliminates entire categories of attack surface — no code path can use the intent to write outside the Index, no caller can overwrite prior Index versions, no caller can write without signing.

### §0.5.9.4 Ordering relative to §1 re-lock and §4 v2.1

The three-step post-§0.5-LOCK queue (operator committed 2026-04-18):
1. **§1 Sovereignty Envelope re-lock** — lift Section 1 from DRAFT v5 against stale parent v4 to LOCKED v6 against v6-r2. Once §1 locks, Index v2 amends row `sovereignty.marker.parent_unlocked` to become concrete §1 primitive rows (likely 3–5 rows covering envelope invariants, Cedar principal bindings, trust-root, daily rotation, M13 bypass policy).
2. **§2 v7.1 parent-backfill** — adds three allowlist rows (`golden-set-read`, `golden-set-write`, `index-update`) without touching other §2 content. Index v3 amends the aggregate allowlist row (`vault.allowlist.static_table_5_entries`) to reflect the new count (8 entries, not 5), refreshes `vault.allowlist.admin_risk_append` if needed, and refreshes §2's per-parent hash.
3. **§4 v2.1 parent-backfill** — inserts F-INDEX-STALE at PRE-gate slot #7, shifting slots #7–#18 to #8–#19. Also wires the F-EVAL-CROSS-ORG-READ predicate per Section 5 v5 §5.6 forward-dep contract. Index v4 amends all §4 PRE-gate rows' `defined_at` pointers and shifts `stability_tier` from PENDING_PARENT_BACKFILL to STABLE.

The ordering is §1 → §2 v7.1 → §4 v2.1 rather than any alternative because: (a) §1 has no outbound dependencies — it can re-lock without waiting on anything; (b) §2 v7.1 adds the `index-update` intent itself, so completing it unblocks normal Index amendment workflow; (c) §4 v2.1 consumes both (it needs §1's Cedar-bindings stable and §2's `index-update` available to wire the PRE-gate's ART-INDEX-DRIFT append path). Completing the queue in a different order either stalls the Index's own amendment loop (if §2 v7.1 is last) or wires a PRE-gate against an unstable substrate (if §4 v2.1 is first).

### §0.5.9.5 Emergency out-of-cycle amendment

In the rare case that a parent must be re-locked between regular audit cycles (e.g., an emergency security patch discovered in Section 3 Scout's AST-PREFLIGHT), the Index amendment follows the same lifecycle but compressed in time: the operator re-locks the parent, immediately amends the Index, signs, commits. The pipeline is not runnable between the parent lock and the Index amendment — F-INDEX-STALE catches the window. The operator's discipline is to keep the window short (typically minutes, not hours) by sequencing parent-commit and Index-commit back-to-back.

If the window must extend (e.g., operator pauses for external review of the parent change), the M13 bypass mechanism covers any urgent pipeline runs during the window. Post-bypass, the regular Index amendment lands and the pipeline returns to non-bypassed F-INDEX-STALE PASS.

---

## §0.5.10 Test matrix

### §0.5.10.1 Happy path

**T1** `test_index_v1_parses_as_canonical_json` — The v1 JSON companion parses as valid canonical-JSON (sorted keys, UTF-8, LF line endings). SHA-3-512 of the canonical bytes matches the value in the signed-commit ledger.

**T2** `test_index_v1_all_rows_satisfy_schema` — Every row has all eight required fields; field types match the schema; `primitive_kind` is in the closed vocabulary; `stability_tier` is in the closed vocabulary.

**T3** `test_index_v1_primitive_id_uniqueness` — Every `primitive_id` across all 71 rows is unique.

**T4** `test_index_v1_per_parent_consistency` — For every parent stem appearing in any `defined_at`, all rows under that parent carry identical `parent_lock_version` and `parent_lock_commit_hash`.

**T5** `test_index_v1_parent_hashes_match_disk` — For every parent stem **except** those whose rows carry `stability_tier == "PARENT_UNLOCKED"` or whose `parent_lock_version` ends with `-DRAFT`, the recorded `parent_lock_commit_hash` equals the SHA-3-512 of the canonical bytes of the on-disk parent file at HEAD. PARENT_UNLOCKED rows are exempt from this equality check because §0.5.8.2 deliberately assigns them the all-zero sentinel hash, which §0.5.6.2 treats as a mandatory mismatch to block any run citing the unlocked parent's primitives; re-including them here would spuriously fail a valid Index.

**T6** `test_f_index_stale_passes_on_fresh_index` — The F-INDEX-STALE predicate returns PASS when given the fresh v1 Index and the current workspace state.

### §0.5.10.2 Stale-parent cases

**T7** `test_f_index_stale_detects_parent_hash_mismatch` — Synthetically modify a parent file's bytes (e.g., append a whitespace character) without updating the Index; F-INDEX-STALE returns FAIL with subcode `parent_hash_mismatch` and names the affected parent.

**T8** `test_f_index_stale_detects_parent_version_mismatch` — Modify the parent's **Status:** line to bump version without re-committing hash updates to the Index; F-INDEX-STALE returns FAIL with subcode `parent_hash_mismatch` (version-string change implies hash change).

**T9** `test_f_index_stale_detects_missing_parent_file` — Rename a parent file so its stem no longer resolves; F-INDEX-STALE returns FAIL with subcode `parent_file_missing`.

**T10** `test_f_index_stale_detects_signature_invalid` — Corrupt the Index JSON's signature in the signed-commit ledger; F-INDEX-STALE returns FAIL with subcode `signature_invalid`.

### §0.5.10.3 Schema-violation cases

**T11** `test_index_build_rejects_duplicate_primitive_id` — Construct a synthetic Index with two rows sharing a `primitive_id`; the Index-build step rejects with a schema violation before any run-time consumer sees the bad state.

**T12** `test_index_build_rejects_inconsistent_per_parent_hash` — Construct a synthetic Index with two rows under the same parent carrying different `parent_lock_commit_hash` values; reject.

**T13** `test_index_build_rejects_unknown_primitive_kind` — Construct a row with `primitive_kind = "widget"` (not in closed vocabulary); reject.

**T14** `test_index_build_rejects_missing_required_field` — Construct a row missing `introduced_in_index_version`; reject.

### §0.5.10.4 Version-skew edge cases

**T15** `test_index_citation_pinned_to_version` — A blueprint section authored against Index v1 carrying `IDX:v1:vault.primitive.vault_write` continues to resolve against the v1 snapshot even after Index v2 lands. Citation does not auto-upgrade; the citing section's own re-lock is required to move to v2.

**T16** `test_immutable_primitive_id_across_versions` — A `primitive_id` present in v{N} either remains in v{N+1} with identical id or is absent from v{N+1}; no id reuse.

**T17** `test_introduced_in_version_never_mutates` — A row's `introduced_in_index_version` in v{N+1} equals its value in v{N}; the field is immutable after row creation.

### §0.5.10.5 Bypass audit cases

**T18** `test_art_index_drift_written_on_fail` — When F-INDEX-STALE FAILs, an ART-INDEX-DRIFT entry is written to the admin-risk ledger with the expected schema fields populated.

**T19** `test_art_index_drift_written_even_with_bypass` — When F-INDEX-STALE would FAIL but an M13 bypass entry covers the run, both the ART-INDEX-DRIFT entry AND the bypass entry are in the ledger.

**T20** `test_bypass_rate_limit_flag` — When three or more bypass entries occur in a seven-day window for any single parent, the Monday cron digest flags the drift-pattern; the flag is observable in the digest output.

### §0.5.10.6 Property tests

**T21** `test_property_per_parent_hash_consistency` — For randomised synthetic Indexes, adding/removing rows or permuting row order never creates inconsistent per-parent (version, hash) pairs as long as the input rows were consistent.

**T22** `test_property_canonical_json_round_trip` — Markdown Index → JSON build → SHA-3-512 → JSON parse → round-tripped JSON equals the original canonical bytes exactly.

**T23** `test_property_idx_citation_resolution` — For every `(IDX:v{N}:primitive_id)` appearing in any locked blueprint section, the Index v{N} JSON contains a row with matching primitive_id.

### §0.5.10.7 Coverage discipline

The 23 tests above cover every subsection of this blueprint (§0.5.1 through §0.5.9 inclusive). Every enumerated invariant, predicate branch, schema field, failure subcode, and lifecycle event has at least one test. The test file lives at `pipeline/tests/test_section_00_5_interface_index.py` (v1 authoring deferred to code-build phase; the test specifications are Index-blueprint-authoritative and any code-build deviation must land as a v2 amendment).

---

## §0.5.11 Changelog, forward-deps, artifact pointers

### §0.5.11.1 Changelog (this document)

**v3 LOCK amendment 2026-04-18 — §1 Sovereignty Envelope v6 LOCK landing (this version).** Scope: placeholder retirement + 11-row add. Lands in the same commit as the §1 v6 LOCK so that the Parent-Wins Invariant (§0.5.2) holds — after the commit, all six parent SHA-3-512 hashes recorded in §0.5.8 match on-disk canonical bytes and no PARENT_UNLOCKED sentinel rows remain.

Specific edits:
- **§0.5.8.1 population summary** updated to show 11 rows under §1 (was 1), with the §1-row breakdown noting 7 N.2-export per-primitive rows + 4 policy-family aggregate rows. Total row count on the same line updated from 71 to 81.
- **§0.5.8.2 Section 1 body** replaced. The v1/v2 single placeholder row `sovereignty.marker.parent_unlocked` (sentinel hash `0*128`, `stability_tier = "PARENT_UNLOCKED"`, `parent_lock_version = "v5-DRAFT"`) is deleted. In its place: 7 mechanism rows for the §13 N.2 export contract primitives (`sovereignty.envelope.boot`, `sovereignty.session.start`, `sovereignty.session.checkpoint`, `sovereignty.audit.append`, `sovereignty.isolation.within_org_root`, `sovereignty.router.verify_integrity`, `sovereignty.crypto.session_hmac_sign`) + 4 policy-family aggregate rows (`sovereignty.failure_codes.aggregate`, `sovereignty.constants.aggregate`, `sovereignty.allowlists.aggregate`, `sovereignty.markers.aggregate`). All 11 rows carry `parent_lock_version = "v6"`, `parent_lock_commit_hash = b0d50a71f53dde3b9988750ba843875125b21c1234115bb4d38268e00818e61009a5948f611ac7c3ebb28daf6726b04759bbe649b3f52600882d62721c89d422`, `introduced_in_index_version = "v3"`, `stability_tier = "STABLE"`. Schema transformation from the §1 v6 driver §14 amendment payload (driver uses `defined_in`/`interface_kind`/`summary`/`lock_round_id`/FOUNDATION_STABLE) into §0.5 row schema (`defined_at`/`primitive_kind`/`description`/`introduced_in_index_version`/STABLE) applied per §0.5.3.4 closed-vocab discipline — no schema widening. The `obsoletes` field in the driver is not carried into the Index because §0.5's 10-field schema does not include an `obsoletes` field; the driver remains the authoritative source for the v5 → v6 breaking-signature change on `within_org_root`.
- **§0.5.8.8 row count reconciliation** updated: 11(§1) + 18(§2) + 7(§3) + 23(§4) + 8(§5) + 14(arch) = 81 rows; placeholder retirement narrated.
- **Header status block** bumped v2 → v3; §1 parent reference line updated to "LOCKED v6 2026-04-18" with new SHA-3-512 `b0d50a71f5...d422`.

No changes to §0.5.1 through §0.5.7, §0.5.9, §0.5.10: purpose, parent-wins invariant, schema, citation form, versioning/staleness, F-INDEX-STALE predicate, ART-INDEX-DRIFT entry, update lifecycle, and test matrix are unchanged from v2. §0.5.11.2 forward-deps updated below to reflect §1 re-lock complete.

**v3 Thesis Team outcome (Section 1 v6 driver — the LOCK this amendment lands):**
- Editor (Llama 3.3 70B, Meta family): READY_TO_LOCK — 4 positive findings, no blocking.
- Judge (Llama 3.3 70B, Meta family, v3 dispatch after two Qwen attempts with schema non-conformance): PASS 92/100, gate_check all true, 8 dims at 10/10, 2 dims at 9/10 (`interface_contract_completeness`, `test_coverage`). All five v6 closures cleared (M14, M14.4.2, BT14, S5/M15, M7-wire). All ten preserved closures (F-ADM-08..12, F-DEG-03, F-KEY-09..10, F-ISO-07, F-M7-WIRE-01..04, RT-v3/v4 HIGH+MED, §10 F9b OOM rejections) true. Zero blocking concerns.
- Red Team (GPT-OSS 120B, OpenAI family): READY_TO_LOCK — 0 Bucket-A, 0 Bucket-B, 0 Bucket-C, 5 OUT-OF-MODEL correctly cited to A1/A3/A4.

Cross-family rigor satisfied: Scribe=Anthropic (Opus), Editor=Meta, Judge=Meta, Red Team=OpenAI. Scribe ≠ each auditor.

**Judge dispatch history (three rounds, preserved for audit trail):** v1 Qwen 3 32B (anchor-list blowup in `cross_section_consistency.rationale`, 8000-token output truncated); v2 Qwen 3 32B (rationale-constraint fix applied, output clean but dimension keys substituted — not rubric-conformant); v3 Llama 3.3 70B (model swap + fill-in template — clean PASS 92). All three preserved at `pipeline/validation/blueprint_section_01_relock_2026-04-18/`. v3 is authoritative.

**v2 LOCKED 2026-04-18 — verification round (superseded by v3 same-day).** Narrow-edit v2 folding in the two Bucket-C findings from v1 Red Team verbatim per Red Team's recommended mitigations. No schema change, no scope change, no new subsections, no grounding change, no foundation-stability decision revisited. JSON companion unchanged (fixes are Markdown-body-only). Specific edits:
- **§0.5.6.2 predicate now carries an explicit sentinel-detect clause** (closes Red Team Bucket-C-02). Added prior to the per-parent hash comparison: if `recorded_hash == "0" * 128` or `recorded_version` ends with `-DRAFT`, return FAIL(subcode=`parent_hash_mismatch`) directly. Eliminates the spec-implementation consistency gap between §0.5.6.1's "treated as always mismatch" prose and the pseudocode's raw equality check. Hypothetical-but-infeasible preimage attack on SHA-3-512 is now explicitly blocked at spec level.
- **§0.5.10.1 test T5 now exempts PARENT_UNLOCKED rows** (closes Red Team Bucket-C-01). T5 `test_index_v1_parent_hashes_match_disk` no longer asserts hash equality on rows with `stability_tier == "PARENT_UNLOCKED"` or `parent_lock_version` ending in `-DRAFT`. The §1 Sovereignty Envelope placeholder row (sentinel hash `0*128`) would have unconditionally failed T5 in v1; v2 makes the exemption explicit, with inline prose explaining that the exemption mirrors the §0.5.6.2 sentinel-detect semantics (the sentinel is a *feature* that forces F-INDEX-STALE FAIL, not a bug the test should catch).

v2 also notes (informational, not actionable): Judge v1 overall_judgment flagged "stability_tier casing errors" in the JSON companion. Direct inspection of `section_00_5_interface_index.v1.json` confirms all 71 rows emit canonical closed-vocabulary values (`STABLE`, `EXPERIMENTAL`, `PENDING_PARENT_BACKFILL`, `PARENT_UNLOCKED`); the flag is a Qwen 3 32B inspection artefact, not a real defect. No action.

**v1 DRAFT 2026-04-18 — initial scoping round.** Authored eleven subsections covering Index purpose, parent-wins invariant, per-row schema, citation form, versioning/staleness semantics, F-INDEX-STALE PRE-gate predicate, ART-INDEX-DRIFT admin-risk entry, v1 seed population (71 rows across six parent groupings), update lifecycle, and a 23-test test matrix. Made three foundation-stability decisions (operator directive 2026-04-18):
- Logician allowlist `defined_at` anchored at Section 2 §4.10.4 (authoritative source), with `binds_to` pointing at the Logician consumer and `primitive_id` version-tied to Section 4 lock.
- F-INDEX-STALE PRE-gate slot = #7 (architecture §0.5.4 binding; minimum stable slot).
- Row granularity = per-family aggregate (71 rows total, corrected from 70 planning estimate after §4 off-by-one discovered in §0.5.8.5 authoring).

No parent blueprint section modified. Forward dependencies declared (not yet landed): §1 Sovereignty Envelope re-lock, §2 Vault v7.1 parent-backfill with `index-update` intent, §4 Logician v2.1 parent-backfill with F-INDEX-STALE PRE-gate wiring.

**v1 Thesis Team outcome:**
- Editor (Llama 3.3 70B): READY_TO_LOCK — 11/11 subsections COMPLETE, all grounding CORRECT, no scope creep.
- Judge (Qwen 3 32B): PASS 100/100 (raw 140/140, min dim 9/10 on schema_completeness + test_adequacy).
- Red Team (GPT-OSS 120B): READY_TO_LOCK — 0 Bucket-A, 0 Bucket-B, 2 Bucket-C (addressed in v2 above), 0 OUT-OF-MODEL.

v1 driver round passed L-005 strict bar cleanly; Josh elected narrow-edit v2 per stability/effectiveness/efficiency directive to fold in the two C-fixes before LOCK.

### §0.5.11.2 Forward dependencies

**§1 Sovereignty Envelope re-lock (COMPLETE 2026-04-18):** Section 1 locked v6 against architecture v6-r2 in the same commit that lands this Index v3 amendment. The eleven-row amendment above retires the `sovereignty.marker.parent_unlocked` placeholder and introduces 7 concrete §13 N.2 export-primitive mechanism rows + 4 policy-family aggregate rows. Thesis Team verdict: Editor READY_TO_LOCK, Judge PASS 92/100, Red Team READY_TO_LOCK (0 in-scope). Canonical path `pipeline/blueprint/v0.1/section_1_sovereignty_envelope.md`; v5 DRAFT archived at `section_1_sovereignty_envelope_v5_2026-04-17.md`.

**§2 Vault v7.1 parent-backfill (NEXT, after this commit):** Adds three allowlist rows to the Section 2 static 5-entry allowlist: `golden-set-read`, `golden-set-write` (per Section 5 v5 §5.6 forward-dep contract), and `index-update` (new in §0.5.9.3 forward-dep contract). Result: 8-entry static allowlist. Index v4 amends the allowlist aggregate row and the per-primitive `defined_at` fields for any §2 primitives whose section anchors shift.

**§4 Logician v2.1 parent-backfill (after §2 v7.1):** Inserts F-INDEX-STALE PRE-gate check at slot #7 (v2's slot #7 RFA dual-hash shifts to #8; all subsequent slots shift by +1). Also wires F-EVAL-CROSS-ORG-READ predicate per Section 5 v5 §5.6 contract. Index v5 refreshes all §4 PRE-gate rows' `defined_at` pointers, updates `stability_tier` from PENDING_PARENT_BACKFILL to STABLE, and adds a new row for F-INDEX-STALE itself (primitive_id `logician.pre_gate.f_index_stale`, which §0.5.6.1 pre-declared).

**Operational baseline (post-all-three-backfills):** Fully live Index with F-INDEX-STALE wired end-to-end, `index-update` intent in daily use, §1 primitive rows concrete, §2 allowlist at 8 entries, §4 PRE-gate list of 9 slots. Represents the stable baseline for v0.1 operational pipeline.

### §0.5.11.3 Artifact pointers

**This document:** `pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md` (LOCKED v3 2026-04-18; supersedes LOCKED v2 same date which superseded DRAFT v1 same date). Mirror copy at `section_00_5_interface_index.md` is kept synchronized with the locked file.

**JSON companion (v3 current):** `pipeline/blueprint/v0.1/section_00_5_interface_index.v3.json` (canonical-JSON, 81 rows, signed by operator at Index v3 lock; SHA-3-512 of canonical bytes with `index_content_hash` field nulled = `1a8c07355bc6ddf8fb234a5f21ae0cfe56f4cec403f034fdc61b50ef2b23bfd9235a88b35e505f7ce04211da5332417aadb1e9369efafda89469c48ceab2377c`, recorded back in the file's `index_content_hash` field; authored_at_iso `2026-04-18T16:54:12Z`). Prior versions preserved at:
- `section_00_5_interface_index.v1.json` (71 rows; JSON identical between v1 and v2 because v2 edits were Markdown-body-only — SHA-3-512 `9d820923f272f65e2688109c011e2223c4c325f1571b43c31874fc8eb8c83de7193dab06520152e18c59ef85e532ac6fb2e21535b25087cc2423d44b2a02c9d4`).
- v2 snapshot `section_00_5_interface_index.v1_preserved_2026-04-18.json` carries the same 71-row content (preserved at v3 lock for explicit version-history clarity).

**Markdown snapshots (preserved):**
- `section_00_5_interface_index_locked_v2_2026-04-18.md` — frozen v2 snapshot (taken at v3 lock).

**§1 v6 LOCK audit folder:** `pipeline/validation/blueprint_section_01_relock_2026-04-18/` containing:
- `section_1_v6-1_driver.md` — the LOCK candidate (3,241 lines, 322 KB).
- `L005_round1_editor_system_prompt.md`, `L005_round1_editor.{raw.json,content.md}` — Editor seat (Llama 3.3 70B Meta).
- `L005_round1_judge_system_prompt.md` (v1), `L005_round1_judge_v2_system_prompt.md`, `L005_round1_judge_v3_system_prompt.md` — Judge seat prompts across three dispatch rounds.
- `L005_round1_judge.{raw.json,content.md}` (v1 Qwen — anchor-list blowup, PRESERVED).
- `L005_round1_judge.v2.{raw.json,content.md}` (v2 Qwen — schema non-conformant, PRESERVED).
- `L005_round1_judge.v3.{raw.json,content.md}` (v3 Llama — PASS 92, AUTHORITATIVE).
- `L005_round1_red_team_system_prompt.md`, `L005_round1_red_team.{raw.json,content.md}` — Red Team seat (GPT-OSS 120B OpenAI).
- `dispatch_round1.py`, `dispatch_round1_judge_v2.py`, `dispatch_round1_judge_v3.py` and matching `.log` files.
- `L005_round1_synthesis.md` — operator + Opus LOCK decision document.

**§0.5 v1/v2 audit folder (preserved):** `pipeline/validation/blueprint_section_00_5_2026-04-18/` (contents unchanged from v2 lock).

**Parent files (read-only references for v3 amendment):**
- `pipeline/architecture/v0.1/tilth_architecture_locked.md` (v6-r2 LOCKED 2026-04-18).
- `pipeline/blueprint/v0.1/section_1_sovereignty_envelope.md` (LOCKED v6 2026-04-18; SHA-3-512 `b0d50a71f53dde3b9988750ba843875125b21c1234115bb4d38268e00818e61009a5948f611ac7c3ebb28daf6726b04759bbe649b3f52600882d62721c89d422`).
- `pipeline/blueprint/v0.1/section_02_vault_topology.md` (v7).
- `pipeline/blueprint/v0.1/section_03_scout.md` (v5).
- `pipeline/blueprint/v0.1/section_04_logician.md` (v2).
- `pipeline/blueprint/v0.1/section_05_pipeline.md` (v5).

**Closure — LOCKED v3 2026-04-18.** This document is the LOCKED Section 0.5 — Blueprint Interface Index v3 under Tilth architecture v6-r2. v3 lands as a same-day amendment to v2 in the same commit as the §1 Sovereignty Envelope v6 LOCK. v3 amendment scope: (a) §0.5.8.2 §1 row block replaced — placeholder `sovereignty.marker.parent_unlocked` retired, 11 concrete §1 primitive rows introduced (7 N.2-export per-primitive mechanisms + 4 policy-family aggregates); (b) §0.5.8.1 / §0.5.8.8 row counts updated from 71 to 81; (c) §0.5.11.1 changelog appended with §1 v6 Thesis Team verdicts and Judge dispatch history. Three foundation-stability decisions from v1/v2 carry forward unchanged: (a) allowlist `defined_at` at §2 v7 §4.10.4, (b) F-INDEX-STALE at PRE-gate slot #7 with +1 cascade, (c) row granularity per-family aggregate. Post-§1 queue: §2 Vault v7.1 parent-backfill (`index-update` intent + `golden-set-read`/`golden-set-write` allowlist rows) → §4 Logician v2.1 parent-backfill (F-INDEX-STALE PRE-gate slot #7 wiring + F-EVAL-CROSS-ORG-READ). Do not auto-start without operator direction.
