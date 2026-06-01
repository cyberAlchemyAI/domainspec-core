# Spec card — pipeline.sovereignty.audit

**STATUS:** LOCKED

**Blueprint anchor:** `pipeline/blueprint/v0.1/section_1_sovereignty_envelope.md` §1 inventory row 4 (v6); §5.6 BT8; §5.3 BT3; §7.3 unit tests; §6.5 Ledger-related failures; §8 constants
**Blueprint hash-at-card:** `<to-populate-at-LOCK>`
**Spec-card version:** v1
**Round:** B (2026-04-19)
**Futureproofing scope:** §4.1 public API / §4.2 schema versioning / §4.3 regression corpus / §4.4 crypto-agile types (reuses Round-A HashDigest) / §4.6 BLUEPRINT_DEPS / §4.9 regression discipline / §4.10 type hints / §4.11 docstrings / E-001 enforce-by-default / E-002 case-normalized identifiers

## Scope

`audit.py` is the GENERIC hash-chain primitive layer. Callers (admin_risk.py Round F, degradation_log.py Round F, sovereignty init marker helpers Round C) consume these primitives with THEIR keystore-derived keys. audit.py itself is keystore-agnostic — it takes raw HMAC key bytes as arguments. This keeps Round B self-contained (no keys.py dependency).

## Public API (goes in `__all__`)

- `LedgerTrailer` frozen dataclass — per-ledger HMAC trailer payload.
- `WatermarksTrailer` frozen dataclass — watermarks-file HMAC trailer.
- `LedgerWatermark` frozen dataclass — one watermark entry per ledger.
- `append_to_ledger(ledger_path, entry_fields, *, ledger_name, hmac_key, lock_path, trailer_path, watermarks_path, watermarks_hmac_key, watermarks_hmac_path, watermarks_lock_path)` — atomic append + trailer update + watermark update under single fcntl lock. Returns the new `LedgerTrailer`. (Amended 2026-04-19 post-committee: (a) `entry_fields: dict` replaces earlier `entry_bytes: bytes` draft — audit.py canonicalizes + adds chain metadata, spares caller serialization concerns; (b) `ledger_name` required for trailer + watermark keying per §5.6; (c) `watermarks_hmac_path` + `watermarks_lock_path` required because `update_watermark` is called inside the same critical section. D-11 of `drift_log_2026-04-19.md` records the amendment.)
- `verify_ledger(ledger_path, trailer_path, *, hmac_key)` — verify hash-chain + trailer HMAC + trailer-over-trailer HMAC. Returns parsed `LedgerTrailer` on success. (Amended 2026-04-19: `hmac_key` unified — blueprint §5.6 keys trailer-over-trailer with the same per-ledger key `tilth.ledger.{name}.hmac.v1` that signs the ledger body. Earlier draft's separate `trailer_hmac_key` was redundant in v0.1.)
- `verify_watermarks(watermarks_path, hmac_path, *, watermarks_hmac_key)` — verify watermarks body against its sibling HMAC file. Returns `dict[str, LedgerWatermark]`.
- `verify_ledger_freshness(ledger_path, trailer_path, watermarks, *, hmac_key)` — combined ledger-integrity + rollback-detection. Used at boot. (Amended 2026-04-19: single `hmac_key` — same reasoning as `verify_ledger`.)
- `update_watermark(ledger_name, trailer, watermarks_path, hmac_path, *, watermarks_hmac_key, lock_path)` — single-held-lock body + HMAC-trailer write.
- `LedgerHMACTrailerMismatch`, `LedgerWatermarkRegression`, `WatermarkHmacMissing`, `WatermarkHmacMismatch`, `LedgerUnreadable`, `LedgerChainBroken` exceptions.
- `LEDGER_ROTATION_SIZE_LIMIT_BYTES: int = 104_857_600` — 100 MiB per §8 constant.
- `canonical_json_bytes(obj: dict) -> bytes` — deterministic JSON serialization (sort_keys=True, separators=(",",":"), ensure_ascii=False, utf-8). Used for HMAC inputs and schema hashing.
- `rotate_ledger_if_needed(ledger_path, *, trailer_path) -> Path | None` — rotate if ≥ 100 MiB; returns the new segment path if rotated, None otherwise.

## Data structures

```python
@dataclass(frozen=True, kw_only=True)
class LedgerTrailer:
    schema_version: str = "v2"         # §4.2 schema versioning
    ledger_name: str
    last_seq_id: int
    last_entry_hash: str                # 128 hex chars SHA-3-512 of last ledger line
    ledger_hmac: str                    # 128 hex chars HMAC over full ledger file
    trailer_version: int = 2            # blueprint §5.6 v2 trailer-version constant

@dataclass(frozen=True, kw_only=True)
class WatermarksTrailer:
    schema_version: str = "v1"
    watermarks_version: int = 1
    watermarks_hmac: str                # HMAC over watermarks body
    wall_at_write_utc: str              # ISO-8601 Z
    trailer_hmac: str                   # HMAC over the trailer object itself (tamper-evident)

@dataclass(frozen=True, kw_only=True)
class LedgerWatermark:
    schema_version: str = "v1"
    ledger_name: str
    last_seq_id: int
    last_trailer_hmac_hex: str
    wall_at_write_utc: str
```

## Algorithms

### Hash-chain append (the BT8 / BT3 primitive)

Per blueprint §5.6 append path:

1. Acquire fcntl.LOCK_EX on `lock_path`. Hold for the entire sequence.
2. Read current ledger file (if exists) → prev_tail_hash (last line's `entry_hash` or zero if empty).
3. Build new entry JSON: `{seq_id: prev+1, timestamp_utc: ..., issued_monotonic_ns: ..., prev_hash: prev_tail_hash, entry_hash: sha3_512_hex(canonical_entry || prev_hash)}` — but entry_bytes is ALREADY pre-formatted by caller; audit.py wraps with the chain prefix.
4. Append entry line (with newline) to ledger via `tmp → fsync → rename → fsync parent`.
5. Rotate if ledger size ≥ `LEDGER_ROTATION_SIZE_LIMIT_BYTES`.
6. Recompute full-file ledger HMAC using `hmac_key` → `new_ledger_hmac`.
7. Build new `LedgerTrailer`; serialize via `canonical_json_bytes`; compute trailer-over-trailer HMAC; write trailer file via atomic rename.
8. Call `update_watermark(...)` under same lock for ledger monotonicity tracking.
9. Release lock.
10. Return the new trailer.

### Boot verification

Per blueprint §5.6 (v4 verification order):

1. `verify_watermarks` — watermarks body + HMAC pair consistency.
2. `verify_ledger_freshness` per ledger — trailer HMAC verifies, ledger HMAC verifies, last_seq_id does NOT regress, trailer HMAC matches watermark's last_trailer_hmac_hex if seq_id equals.
3. Return dict of parsed trailers.

### Rotation

At 100 MiB: rename current `.jsonl` to `.jsonl.segment_NNN` (monotonic counter), start fresh. Trailer tracks ACROSS rotation via `last_seq_id`.

### Canonical JSON

```python
def canonical_json_bytes(obj: dict) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",",":"),
                      ensure_ascii=False).encode("utf-8")
```

Matches the pattern used across Section 0.5 Interface Index + Option-B canonical-bytes pinning.

## Failure codes

Per blueprint §6.5 (Ledger-related):

- `LedgerHMACTrailerMismatch` — trailer HMAC does not verify over ledger file bytes.
- `LedgerChainBroken` — hash-chain gap (line N's `prev_hash` doesn't equal line N-1's `entry_hash`).
- `LedgerWatermarkRegression` — seq_id regressed OR trailer HMAC mismatch at same seq_id.
- `WatermarkHmacMissing` — watermarks body exists but `.hmac` does not.
- `WatermarkHmacMismatch` — watermarks HMAC does not verify over watermarks body bytes.
- `LedgerUnreadable` — file corrupted / missing / permission-denied.
- `TypeError` at public-surface entry for wrong arg types.

Round-A E-001 lesson: every primitive accepts a `min_key_bytes: int = 32` default kwarg for HMAC operations. Callers with legitimate shorter-key use cases override explicitly.

## Test surface

Target ≥ 35 tests.

### Property tests
- Monotonic seq_id: appends always produce strictly increasing seq_id.
- Hash-chain integrity: flipping any byte of any line triggers `LedgerChainBroken` at that line.
- Deterministic trailer: same input ledger + same key → byte-identical trailer file.
- Watermark monotonicity: watermark's last_seq_id matches ledger's last seq_id after every append.
- `canonical_json_bytes` is deterministic and whitespace-insensitive.

### Failure-code tests
- Single test per failure code; red-first.
- Concurrency test: two threads racing `append_to_ledger` on the same ledger — fcntl.LOCK_EX serializes; no interleaved writes; both succeed.
- Rotation test: ledger at 99.9 MiB; append 200 KiB entry; `rotate_ledger_if_needed` triggers; trailer tracks across rotation.
- Rollback attack simulation: replace ledger+trailer+watermark with older consistent snapshot; watermarks HMAC fails (per §5.6 v4 closure of RT-v3 HIGH-1).

### Corpus tests
- `tests/corpus/audit/v1/` — preserved input ledgers + expected trailers for regression.
- Ledger with exactly 0 entries, 1 entry, 1000 entries.
- Pre-rotated ledgers with segment files.

### Blueprint §7.3 regression tests (MUST pass)
- `test_bt3_fail_closed_on_unreadable_ledger`
- `test_bt8_chain_verification_detects_tamper`
- `test_bt8_chain_verification_detects_replay`

## Futureproofing commitments

- Public API via `__all__`; downstream imports from `pipeline.sovereignty` only.
- `BLUEPRINT_DEPS` at module top.
- `schema_version` on every dataclass; migration placeholder (even if v0.1 has only v1/v2).
- `canonical_json_bytes` helper reused across every on-disk serialization in this module AND exposed for future callers (admin_risk, degradation_log).
- Fully typed.
- Docstring citations.
- E-001 enforce-by-default: `min_key_bytes=32` on every HMAC call by default.
- E-002: no uppercase / lowercase drift in algorithm identifiers.
- Lock discipline: always `fcntl.LOCK_EX`; always via context manager; never released between body write and trailer write per §5.6 invariant.

## Dependencies

- `pipeline.sovereignty.crypto_primitives.hmac_sha3_512` — Round A, already locked.
- `pipeline.sovereignty.crypto_primitives.sha3_512_hex` — Round A.
- `pipeline.sovereignty.crypto_primitives.constant_time_equal` — Round A.
- `fcntl`, `hashlib`, `json`, `time`, `pathlib` — stdlib.

No cross-section imports. No keystore dependency (callers pass keys).

## Done definition

- ≥ 35 pytest tests covering every public function, every failure mode, every blueprint §7.3 regression vector.
- `pytest tests/` cumulative green (Round A + Round B).
- Lines-of-code target ~900 per blueprint §1 row 4 (retroactively amended 2026-04-19 post-committee E3 synthesis — original ~430 estimate did not account for the four-sub-system scope: §5.6 BT8 HMAC trailer + §5.6 v4 watermark integrity + §5.6 rotation + §5.3 BT3 append, plus the frozen-dataclass serialization helpers + per-field canonical dict builders + trailer-loader shape validation each sub-system requires); accept ±25% (675-1125 acceptable). Drift D-14 records the retroactive estimate adjustment.
- All public symbols in `pipeline/sovereignty/__init__.py` `__all__`.
- Concurrency correctness property test passes on M1 8GB dev node.
- Rollback-attack simulation test passes.

## Out of scope (Round B — stubbed or deferred)

- `write_sovereignty_init_marker_first_boot` / `verify_sovereignty_init_marker` (§3.11b) — those helpers use audit.py primitives but live at the caller layer; deferred to Round C or E.
- BT3 rate-limiting logic — lives in `admin_risk.py` Round F, consumes audit.py primitives.
- BT8 degraded-run flag semantics — lives in `degradation_log.py` Round F, consumes audit.py primitives.
- Boot-integration tests — Round I (boot.py) integration round.
