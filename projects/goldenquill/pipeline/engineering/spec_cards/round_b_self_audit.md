# Round B — Spec-Card Self-Audit (Rule 2 Magic Step)

**STATUS:** LOCKED

**Author:** Claude Code CLI window (2026-04-19 evening)
**Round:** B (topology.py + audit.py)
**Status:** LOCKED 2026-04-19 via E3 operator synthesis. Committee-confirmed post-lock; see `pipeline/validation/code_reviews/round_b_2026-04-19/final_synthesis.md`. LOC targets since retroactively amended per D-14; self-audit "DEVIATION" rows below are historical — the targets now match the 271 / 966 LOC reality.

This file is the Phase-4 "every row check" per engineering_process_v0.1.md §1. Each row from the two spec cards is re-stated and marked implemented or deviated.

Cumulative pytest result (before committee dispatch): **199/199 green** on Python 3.14.4 + pytest 9.0.3. Round A 103 + Round B topology 48 + Round B audit 48.

---

## Module 1 — `pipeline/sovereignty/topology.py`

### Spec card: `round_b_topology.md` row-by-row

| Row (spec card) | Status | Evidence |
|---|---|---|
| `is_doc_sourced_path(path, *, bound_slug, repo_root) -> bool` | ✓ | topology.py L217-274 |
| `DocSourcedRoot` frozen dataclass | ✓ | topology.py L105-125 |
| `DOC_SOURCED_ROOTS: tuple[DocSourcedRoot, ...]` 5-tuple | ✓ | topology.py L129-156 |
| `canonicalize_vault_path(path, *, repo_root) -> Path` | ✓ | topology.py L277-321; **note: signature adds `repo_root` kwarg** — spec card shape was `canonicalize_vault_path(path: Path) -> Path` without repo_root; actual API takes `repo_root` because the symlink-escape walk needs it as an anchor. Deviation surfaced in self-audit; reviewer may flag. |
| `PathEscapedRoot` exception | ✓ | topology.py L62-75 |
| `SymlinkRejected` exception | ✓ | topology.py L78-92 |
| DocSourcedRoot entries (5 rows: rfa, org, dossier, rubrics, institutional_memory) | ✓ | topology.py L131-156; matches spec card exactly |
| `is_doc_sourced_path` algorithm steps 1-4 | ✓ | topology.py L251-274 (type gate L251, repo_root resolve L253-257, per-root loop L262-272, False return L274) |
| `canonicalize_vault_path` algorithm steps 1-4 | ✓ | topology.py L295-321 (type gate L295-303, repo_root resolve L305-309, strict=True path resolve L311, relative_to check L314-317, symlink walk L320, return L321) |
| `InvalidSlug` propagation (via `canonical_slug`) | ✓ | topology.py L178 (calls `canonical_slug(bound_slug)`); propagates InvalidSlug/ReservedSlug. Tested at test_topology.py `TestSlugEntryGate`. |
| `tests/corpus/topology/v1/doc_sourced_vectors.json` | ✓ | created with 6 accept + 6 reject vectors |
| Blueprint §7.5 regression tests | ✓ | `test_topology_doc_sourced_whitelist_rejects_cache_path` (test_topology.py `TestRejectsNonDocSourced::test_cache_path_rejected`), `test_topology_doc_sourced_whitelist_accepts_five_roots` (test_topology.py `TestAcceptsFiveRoots` — 5 parametric tests) |
| Property tests (5 listed) | ✓ | `TestAcceptsFiveRoots::*` (reflexive accept), `TestRejectsNonDocSourced::*` (outside-universe), `TestCanonicalizeVaultPath::test_idempotent`, `TestProperties::test_dossier_is_strict_subset_of_org` |
| Failure-code tests (type errors, slug mismatch, symlink escapes) | ✓ | `TestTypeSafety`, `TestSlugEntryGate`, `TestSymlinkEscape` |
| `__all__` public export | ✓ | __init__.py updated with topology symbols |
| No import from `topology.py` in tests except public API | ✓ | test_topology.py imports via `pipeline.sovereignty` only |
| §4.1 Public API | ✓ | `__all__` declared |
| §4.6 BLUEPRINT_DEPS | ✓ | topology.py L53-59 |
| §4.10 full type hints | ✓ | Path, str, tuple[DocSourcedRoot,...], Iterator |
| §4.11 blueprint-citing docstrings | ✓ | Every public function cites [§1 row 7], [§7.5], [§3.11d], [§6.7] |
| E-001 enforce by default | ✓ | `_validate_entry_args` runs type checks + slug canonicality BEFORE semantic path work |
| E-002 case-normalized identifiers | ✓ | DocSourcedRoot labels all lowercase ascii; asserted in `TestDocSourcedRoot::test_labels_are_lowercase_ascii` |
| LOC target ~180 ±25% (135-225) | ✗ **DEVIATION — 397 lines** | +115% over target. Driver: defensive `_walk_for_symlink_escape` helper (~60 LOC) + `_validate_entry_args` (~40 LOC) + extensive docstrings citing blueprint. Author recommends keeping the code as-is — the over-run is all defensive checks + blueprint-citation comments, not accidental bloat. Reviewer may flag; narrow-edit would require trimming docstrings. |

**Deviations self-flagged for reviewer attention:**
1. `canonicalize_vault_path` takes `repo_root` kwarg not listed in spec card signature (needed for symlink-escape walk anchor).
2. LOC over target by ~75%. Driven by defensive code + blueprint-citation docstrings.
3. Added `_walk_for_symlink_escape` helper + `_validate_entry_args` helper — not in spec-card Data Structures but natural decomposition.

---

## Module 2 — `pipeline/sovereignty/audit.py`

### Spec card: `round_b_audit.md` row-by-row

| Row (spec card) | Status | Evidence |
|---|---|---|
| `LedgerTrailer` frozen dataclass | ✓ | audit.py L197-225 — schema_version, ledger_name, last_seq_id, last_entry_hash, ledger_hmac, trailer_version, trailer_hmac |
| `WatermarksTrailer` frozen dataclass | ✓ | audit.py L228-244 |
| `LedgerWatermark` frozen dataclass | ✓ | audit.py L247-257 |
| `append_to_ledger(ledger_path, entry_bytes, *, hmac_key, lock_path, trailer_path, watermarks_path, watermarks_hmac_key)` | ✓ **with signature expansion** | audit.py L830-935; takes `entry_fields: dict` instead of `entry_bytes: bytes` (cleaner — caller passes domain fields, audit adds chain metadata per §5.6). Also adds `ledger_name`, `watermarks_hmac_path`, `watermarks_lock_path` as required kwargs (needed to resolve §5.6 watermark + lock paths). |
| `verify_ledger(ledger_path, trailer_path, *, hmac_key, trailer_hmac_key)` | ✓ **unified key** | audit.py L672-725 — unified to single `hmac_key` because blueprint §5.6 uses one key id per ledger (`tilth.ledger.{name}.hmac.v1`) for both ledger-body HMAC and trailer-over-trailer HMAC. Spec card's separate `trailer_hmac_key` was redundant in v0.1. |
| `verify_watermarks(watermarks_path, hmac_path, *, watermarks_hmac_key)` | ✓ | audit.py L591-669 |
| `verify_ledger_freshness(ledger_path, trailer_path, watermarks, *, hmac_key, trailer_hmac_key)` | ✓ **unified key** | audit.py L728-764 — same single-key reduction |
| `update_watermark(...)` single-held-lock body+HMAC | ✓ | audit.py L789-826 (lock L808, body write L814, HMAC compute L816, HMAC write L827, all under same lock) |
| Exceptions (LedgerHMACTrailerMismatch, LedgerWatermarkRegression, WatermarkHmacMissing, WatermarkHmacMismatch, LedgerUnreadable, LedgerChainBroken) | ✓ | audit.py L163-194 — all 6 exceptions with §6.5 codes in docstrings |
| `LEDGER_ROTATION_SIZE_LIMIT_BYTES: int = 100 MiB` | ✓ | audit.py L114 |
| `canonical_json_bytes(obj)` | ✓ | audit.py L259-283 — sort_keys, separators, ensure_ascii=False, utf-8 |
| `rotate_ledger_if_needed(ledger_path, *, trailer_path) -> Path \| None` | ✓ | audit.py L768-802 |
| `CHAIN_VERIFY_FAST_TAIL_ENTRIES: int = 100` | ✓ | audit.py L115 (per §8 constant) |
| §5.6 BT8 append protocol (steps 1-10) | ✓ | audit.py L852-935 matches blueprint §5.6 step list |
| §5.6 BT8 boot verification order (v4) | ✓ | `verify_watermarks` → `verify_ledger_freshness` matches §5.6 v4 sequence |
| Rotation at 100 MiB | ✓ | audit.py `rotate_ledger_if_needed` + `TestRotation::test_rotation_moves_ledger_and_creates_empty` |
| `canonical_json_bytes` as shared helper | ✓ | audit.py L259-283, exported for reuse |
| E-001 `min_key_bytes=32` default on HMAC | ✓ inherited from Round A's `hmac_sha3_512` default; audit.py does not override. Tested at `TestHMACKeyDiscipline::test_append_rejects_short_key`. |
| E-002 lowercase identifiers | ✓ | all schema_version strings lowercase, ledger_name case-preserved as caller supplies |
| Lock discipline — single `fcntl.LOCK_EX` across mutations | ✓ | `_acquire_exclusive_lock` context manager; `append_to_ledger` uses it across read-tail, rotation, append, trailer, watermark-update |
| §4.1 public API | ✓ | `__all__` declared |
| §4.2 schema versioning | ✓ | every dataclass has `schema_version` field |
| §4.3 backwards-compat corpus | ⚠ PARTIAL | `tests/corpus/audit/v1/` directory created, no vectors yet. Blueprint §7.3 regression tests work via dynamic creation inside the test suite. Author's call: audit ledger corpus is always dynamically-generated (appending to an empty ledger) — preserving "input ledgers + expected trailers" is moot because the trailer is a function of the input + key, and the HMAC key is not kept in the corpus. Reviewer may flag. |
| §4.6 BLUEPRINT_DEPS | ✓ | audit.py L82-96 |
| §4.9 regression-discipline on tests | ✓ | 48 tests cover all failure codes + properties + regression triplet |
| §4.10 full type hints | ✓ | Path, bytes, int, str, dict, tuple, Iterator |
| §4.11 docstring anchors | ✓ | every public function cites [§5.3], [§5.6], [§6.5], [§7.3], [§8] |
| Blueprint §7.3 regression triplet | ✓ | `test_bt3_fail_closed_on_unreadable_ledger`, `test_bt8_chain_verification_detects_tamper`, `test_bt8_chain_verification_detects_replay` — all present in `TestBT3BT8Regression` |
| Concurrency test (fcntl serialization) | ✓ | `TestConcurrency::test_two_threads_serialize_via_fcntl` — 8 threads, monotonic seq verified |
| Rollback-attack simulation | ✓ | `TestLedgerFreshness::test_rollback_attack_detected` + `test_same_seq_different_hmac_detected` |
| LOC target ~430 ±25% (322-537) | ✗ **DEVIATION — 1125 lines** | +162% over target. Driver breakdown: module docstring 55 LOC, 6 exception classes 70 LOC, 3 frozen dataclasses with docstrings 70 LOC, canonical helpers 60 LOC, constants + type declarations 80 LOC, lock + atomic-write helpers 60 LOC, trailer serialization / load 200 LOC, watermarks body helpers 70 LOC, verify_watermarks 90 LOC, chain verification helpers 110 LOC, verify_ledger 70 LOC, verify_ledger_freshness 50 LOC, rotation 50 LOC, update_watermark 55 LOC, append_to_ledger 120 LOC, misc helpers 30 LOC. Author recommendation: accept the LOC overage. Trimming would require removing defensive checks / blueprint-citation docstrings that actually pull weight. Reviewer may disagree. |

**Deviations self-flagged for reviewer attention:**
1. `append_to_ledger` takes `entry_fields: dict` not `entry_bytes: bytes` — cleaner API, still matches §5.6 semantics.
2. Added `ledger_name`, `watermarks_hmac_path`, `watermarks_lock_path` kwargs (needed for full §5.6 semantics).
3. `verify_ledger` + `verify_ledger_freshness` unified `trailer_hmac_key` into `hmac_key` — v0.1 uses one key per ledger per blueprint.
4. LOC over target by ~160%. Driven by defensive code + dataclass serialization helpers.
5. `§4.3 backwards-compat corpus` — `tests/corpus/audit/v1/` directory exists but empty; regression via dynamic ledger construction in test code. Reviewer may want a seeded corpus.

---

## Round-A-lesson pre-checks (E-001..E-004)

- **E-001** enforce-by-default HMAC ≥32-byte default — ✓ inherited from Round-A `hmac_sha3_512`; audit.py never overrides. Short-key rejection tested in `TestHMACKeyDiscipline`.
- **E-002** case discipline — ✓ schema_version strings all lowercase, ledger_name preserved as supplied (per-caller convention).
- **E-003** Unicode NFC strict rule — N/A for Round B (no Unicode-canonicalization surfaces; topology accepts str `bound_slug` which is already canonicalized by Round A).
- **E-004** committee fallback — ✓ process-level; this round substitutes Gemini 2.5 Pro for Kimi K2 upfront per router.yaml fallback (drift note D-08 from Round A still applies).

---

## Drift notes (file-based state per handoff §5a)

Will be appended to `pipeline/handoffs/drift_log_2026-04-19.md` on LOCK. Preview:

- **D-10 (pending)** — topology.py `canonicalize_vault_path` signature accepts `repo_root` kwarg not listed in Round-B spec-card row. Author-side judgment: anchoring the symlink-escape walk requires it. Reviewers asked to confirm acceptable or surface as spec-card amendment.
- **D-11 (pending)** — audit.py `append_to_ledger` signature deviates from spec-card in arg name (entry_fields vs entry_bytes) and additional path kwargs. Judged as blueprint-fidelity-preserving improvement over the spec-card shape.

No drift is a LOCK blocker. All drift is deliberate; committee confirms or overrides.

---

End of self-audit.
