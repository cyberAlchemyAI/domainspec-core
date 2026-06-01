# Spec card — pipeline.scout Round 3 (Channel B — curated cached datasets)

**STATUS:** LOCKED-backfilled

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_03_scout.md`
  - §4.2 Channel B full spec (lines 473–491) — implementation target
  - §2.1 `Candidate` schema (Round 1 `_types.py`) — DISCOVER row shape
  - §4.6 `_assert_intent_matches` post-read intent equality check (line 584) — defence-in-depth primitive Round 3 consumes
  - §6.2 F-SCOUT-B-01..04 failure codes
  - §7.2 test surface for `channel_b_cache` (lines 1248–1256)
  - §8 `CACHE_WATERMARK_DEGRADED_DAYS = 14` (Round 1 `_constants.py`)
  - §9 Cache reads use intent `"cache-read"` (NOT the Scout-specific `INTENT_READ` — distinct cache-path intent, see §4.2 line 491)
- Section 2 consumed surface: `vault_read(path, intent, session_id, slug) -> (bytes, IdentityTuple)` — LOCKED; `_assert_intent_matches` primitive (Section 1) — LOCKED.

**Blueprint hash-at-card:** `0a82d955f95b0fca` (sha3_512(section_03_scout.md)[:16]) — identical to Rounds 1 + 2.

**Spec-card version:** v1
**Round:** Scout R3 of 11. Consumes Round 1 schema + constants only. Does NOT consume Round 2 (M7 sits downstream of per-channel discovery).

---

## Summary

Land `pipeline/scout/channel_b_cache.py` — the Channel B DISCOVER adapter. Read-only, zero network. Produces `list[Candidate]` from `vault_read`-backed JSONL cache files and a per-channel `str` health state for M7 consumption.

Public surface:

```python
def discover_channel_b(
    *,
    session: SessionLike,
    vault_reader: VaultReader,
    clock: ClockFn = _default_clock,
) -> ChannelBDiscoverResult: ...
```

Where `ChannelBDiscoverResult` is a frozen kw_only dataclass: `candidates: tuple[Candidate, ...]`, `channel_state: str` (∈ `{OK, DEGRADED, FAILED}`), `per_file_events: tuple[DegradationEvent, ...]`.

## Design decisions (operator-disposed 2026-04-20, reversible)

1. **`VaultReader` Protocol seam.** Same pattern Round 2 used for `VaultWriter`. Production binding adapts `pipeline.vault` read path; tests inject an in-memory reader. Reader returns `(bytes, IdentityTuple)`.
2. **`_assert_intent_matches` is a pure helper.** Round 3 defines a local module-level check (strict equality after NFC + strip) that mirrors §4.6's contract. Cross-ref in docstring; deduped into `pipeline.sovereignty` only if Channels C–F reuse it identically.
3. **Per-row failure is row-skip; per-file failure is hard-fail.** `F-SCOUT-B-01` (malformed JSON) skips the row. `F-SCOUT-B-04` (IdentityTuple mismatch) aborts the file and flips Channel B → FAILED.
4. **10% malformed-row threshold is inclusive.** Per A-07 closure: a file with exactly 10% malformed rows degrades.
5. **Watermark check reads the header row only.** First line of every JSONL is a header with `watermark_utc`. Missing header = F-SCOUT-B-02. Stale header (> 14 days) records DEGRADED + `cache_stale_channel_b`.
6. **Per-row fit-score threshold is NOT enforced by Round 3.** `fit_score_cached` is stored verbatim; Pipeline's VERIFY stage does the `>= 60` filter. Round 3 must NOT short-circuit low-fit rows.
7. **S10a invariant read-time check is scoped per ARCH-02 decision.** Round 3 accepts rows with or without org-identifier fields; a test documents the current Section-2-write-time locus (test_s10a_defence_in_depth_row_currently_accepted). Polarity flips when ARCH-02 resolves.
8. **File ordering.** `sorted(...)` over federal/state/foundation + the per-org subscribed_feeds path. Deterministic.
9. **No module-level side effects on import.** All state lives in `discover_channel_b`.

## Public surface

```python
# pipeline/scout/channel_b_cache.py
from typing import Protocol

from pipeline.scout import Candidate, HEALTH_OK, HEALTH_DEGRADED, HEALTH_FAILED

class VaultReader(Protocol):
    def read(self, *, path: str, intent: str, session_id: str, slug: str
             ) -> tuple[bytes, "IdentityTupleLike"]: ...

class IdentityTupleLike(Protocol):
    intent: str
    session_id: str
    slug: str

class SessionLike(Protocol):
    session_id: str
    slug: str

@dataclass(frozen=True, kw_only=True)
class DegradationEvent:
    path: str
    code: str
    reason_tag: str | None
    severity: str  # "LOW" | "MEDIUM" | "HIGH"

@dataclass(frozen=True, kw_only=True)
class ChannelBDiscoverResult:
    candidates: tuple[Candidate, ...]
    channel_state: str
    per_file_events: tuple[DegradationEvent, ...]

class ChannelBIdentityTupleMismatch(RuntimeError):
    code: str  # "F-SCOUT-B-04"

def discover_channel_b(
    *, session: SessionLike, vault_reader: VaultReader,
    clock: ClockFn = _default_clock,
) -> ChannelBDiscoverResult: ...
```

Re-export `discover_channel_b`, `ChannelBDiscoverResult`, `DegradationEvent`, `ChannelBIdentityTupleMismatch`, `VaultReader` from `pipeline.scout.__init__`. Bump `__version__` to `"0.1.0-scout-r3"`.

## Failure-code taxonomy

| Code | Raised when | State effect |
|------|-------------|--------------|
| `F-SCOUT-B-01` | JSONL row is malformed JSON | row skipped; ≥10% of rows → DEGRADED |
| `F-SCOUT-B-02` | header row missing or missing `watermark_utc` | file skipped; event recorded |
| `F-SCOUT-B-03` | row carries forbidden org-identifier field (S10a) | row skipped (current ARCH-02 locus — Section 2 write-time) |
| `F-SCOUT-B-04` | IdentityTuple intent/slug/session mismatch post-read | file aborted; Channel B → FAILED |
| `F-SCOUT-B-05` (new) | `_assert_intent_matches` detects NFC/whitespace drift | raised; file aborted; same handling as -04 |

## Test surface (target ~50 tests)

Per §7.2 plus coverage additions. Lives at `tests/scout/test_round_3_channel_b_cache.py`.

- `TestHappyPath` (4) — single file with 3 valid rows; three-file concat; empty file (no rows, still OK); respects per-org subscribed_feeds.
- `TestWatermark` (4) — 0-day = OK; 14-day = OK (boundary inclusive of allowed); 15-day = DEGRADED + `cache_stale_channel_b`; missing = F-SCOUT-B-02.
- `TestMalformedRows` (5) — single malformed = row skip; 9.99% malformed = OK; 10% malformed = DEGRADED (inclusive); 100% malformed = file skip; malformed + IdentityTuple mismatch = FAILED takes precedence.
- `TestIdentityTupleMismatch` (5) — intent mismatch → F-SCOUT-B-04 + Channel FAILED; slug mismatch → same; session_id mismatch → same; NFC drift on intent → F-SCOUT-B-05; trailing whitespace on intent → F-SCOUT-B-05.
- `TestS10aRowKind` (2) — row with `slug` field → F-SCOUT-B-03 row skip; polarity-inverted defence-in-depth test documenting ARCH-02 current locus.
- `TestFileOrdering` (2) — output `Candidate` order is stable under `sorted` file ordering across invocations.
- `TestFitScoreVerbatim` (2) — low-fit rows (fit_score_cached < 60) are NOT filtered here; high-fit rows carry through.
- `TestVaultReaderCallSite` (4) — reader called with `intent="cache-read"`, per-file `path`, propagates `session_id` + `slug`.
- `TestNoModuleSideEffects` (1) — import does not open FDs or call reader.
- `TestASTLintRegression` (1) — `lint_tree` clean on `channel_b_cache.py`.
- `TestKWOnly` (1) — positional call rejected.
- `TestProtocolDiscipline` (2) — VaultReader + SessionLike + IdentityTupleLike minimal duck-typed fakes work.
- `TestChannelStateAggregation` (3) — all files OK → OK; one stale + rest OK → DEGRADED; one F-SCOUT-B-04 file → FAILED.
- `TestNonceReleasedAfterRead` (1) — placeholder test documenting that Channel B is local-only and does NOT reserve nonces (unlike Channel A); the `nonce_released_on_every_exit_path` invariant is asserted vacuously here, live for Channel A Round 4.

Total ≈ 50. Coverage target 100% on `channel_b_cache.py`.

## pyproject.toml / dep changes

None. Stdlib only.

## Committee dispatch

Single-cycle self-LOCK eligible IF: all tests green in one RED→GREEN, 100% coverage, AST-lint clean, no regressions in the full suite. Otherwise dispatch 5-family Code Thesis Committee per `router.yaml`.

## Done-definition

1. `pipeline/scout/channel_b_cache.py` written per surface above.
2. `pipeline/scout/__init__.py` re-exports + `__version__ = "0.1.0-scout-r3"`.
3. `tests/scout/test_round_3_channel_b_cache.py` — ≥50 tests across classes above.
4. `scripts/run_tests.sh tests/scout/` green.
5. `scripts/run_tests.sh` full suite green.
6. `scripts/run_lint.sh` clean.
7. Coverage on `pipeline.scout.channel_b_cache` = 100%.
8. LOCK entry `project_impl_scout_round_3_locked.md` + MEMORY.md pointer.
9. Round 4 spec card pre-staged (`scout_round_4_channel_a_federal_apis.md`).

## Dependencies and timing

- **Unblocks:** Scout R11 orchestrator + any test that wants a real Channel B state to feed into Round 2's M7 signing.
- **Blocked by:** Round 1 LOCK (done). Round 2 LOCK (done). No external blockers.
- **Risk surface:** Section 2 `vault_read` signature stability (LOCKED Rounds P..U); Section 1 NFC normalisation helper stability.

## Pre-flight checklist

- [x] Blueprint hash pinned (`0a82d955f95b0fca`).
- [x] Round 1 + Round 2 LOCKs verified.
- [x] Section 2 `vault_read` surface consumed as Protocol (E-017 reused).
- [ ] RED→GREEN cycle executed.
- [ ] Committee dispatch OR self-LOCK gate reached.
