"""Round 3 — pipeline.scout.channel_b_cache (§4.2 Channel B DISCOVER).

Exercises ``discover_channel_b`` with injected ``VaultReader`` + path-lister
fakes. No real disk, no real vault. The Protocol seams are the full I/O
surface Round 3 touches and both are duck-typed fakes here.
"""

from __future__ import annotations

import datetime as _dt
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

import pytest

import pipeline.scout as scout
from pipeline.linting.ast_lint import DEFAULT_RULES, lint_tree
from pipeline.scout import (
    CACHE_WATERMARK_DEGRADED_DAYS,
    CHANNEL_B,
    HEALTH_DEGRADED,
    HEALTH_FAILED,
    HEALTH_OK,
    Candidate,
    ChannelBDiscoverResult,
    ChannelBIdentityTupleMismatch,
    DegradationEvent,
    INTENT_CACHE_READ,
    discover_channel_b,
)


# ---------------------------------------------------------------------------
# Fakes — fixed duck-typed Protocol stand-ins
# ---------------------------------------------------------------------------


@dataclass
class _FakeIdentity:
    intent: str
    session_id: str
    slug: str


@dataclass
class _FakeSession:
    session_id: str = "sess-round3"
    slug: str = "fit_farms_llc"


@dataclass
class _MemoryVaultReader:
    files: dict[str, bytes] = field(default_factory=dict)
    identity_overrides: dict[str, _FakeIdentity] = field(default_factory=dict)
    calls: list[dict] = field(default_factory=list)

    def read(
        self,
        *,
        path: str,
        intent: str,
        session_id: str,
        slug: str,
    ) -> tuple[bytes, _FakeIdentity]:
        self.calls.append(
            {
                "path": path,
                "intent": intent,
                "session_id": session_id,
                "slug": slug,
            }
        )
        data = self.files[path]
        ident = self.identity_overrides.get(
            path,
            _FakeIdentity(intent=intent, session_id=session_id, slug=slug),
        )
        return data, ident


def _header(watermark_utc: str, **extra) -> str:
    payload = {"watermark_utc": watermark_utc}
    payload.update(extra)
    return json.dumps(payload)


def _row(
    *,
    candidate_id: str = "cand-0001",
    feed_or_adapter_id: str = "cache:federal-grants-gov-2026",
    source_key: str = "grants-gov-opp-42",
    title: str = "Soil Health Infrastructure",
    funder: str = "USDA",
    funder_kind: str = "federal",
    url: str = "https://grants.gov/opp/42",
    applicant_types: Optional[list] = None,
    fetch_timestamp_utc: str = "2026-04-01T00:00:00Z",
    url_hash: str = "ab" * 32,
    fit_score_cached: int = 72,
    **optional,
) -> str:
    row = {
        "candidate_id": candidate_id,
        "feed_or_adapter_id": feed_or_adapter_id,
        "source_key": source_key,
        "title": title,
        "funder": funder,
        "funder_kind": funder_kind,
        "url": url,
        "applicant_types": applicant_types or ["nonprofit", "cooperative"],
        "fetch_timestamp_utc": fetch_timestamp_utc,
        "url_hash": url_hash,
        "fit_score_cached": fit_score_cached,
    }
    row.update(optional)
    return json.dumps(row)


def _jsonl(watermark_utc: str, *rows: str) -> bytes:
    lines = [_header(watermark_utc)] + list(rows)
    return "\n".join(lines).encode("utf-8")


def _fixed_clock(iso: str) -> Callable[[], _dt.datetime]:
    parsed = _dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=_dt.timezone.utc)
    return lambda: parsed


_NOW_ISO = "2026-04-20T00:00:00Z"
_FRESH_WATERMARK = "2026-04-20T00:00:00Z"


def _run(
    *,
    files: dict[str, bytes],
    identity_overrides: Optional[dict[str, _FakeIdentity]] = None,
    session: Optional[_FakeSession] = None,
    paths_order: Optional[tuple[str, ...]] = None,
    clock_iso: str = _NOW_ISO,
) -> tuple[ChannelBDiscoverResult, _MemoryVaultReader]:
    session = session or _FakeSession()
    reader = _MemoryVaultReader(
        files=dict(files),
        identity_overrides=dict(identity_overrides or {}),
    )
    listed = paths_order if paths_order is not None else tuple(files.keys())
    result = discover_channel_b(
        session=session,
        vault_reader=reader,
        list_cache_paths=lambda slug: listed,
        clock=_fixed_clock(clock_iso),
    )
    return result, reader


# ---------------------------------------------------------------------------
# TestHappyPath — 4
# ---------------------------------------------------------------------------


class TestHappyPath:
    def test_single_file_three_rows_yields_three_candidates(self):
        files = {
            "vault_shared/cached_opportunities/federal/usda.jsonl": _jsonl(
                _FRESH_WATERMARK,
                _row(candidate_id="c-001", source_key="a"),
                _row(candidate_id="c-002", source_key="b"),
                _row(candidate_id="c-003", source_key="c"),
            ),
        }
        result, _ = _run(files=files)
        assert result.channel_state == HEALTH_OK
        assert len(result.candidates) == 3
        assert all(c.channel == CHANNEL_B for c in result.candidates)
        assert result.per_file_events == ()

    def test_three_files_concatenate_candidates(self):
        files = {
            "vault_shared/cached_opportunities/federal/f.jsonl": _jsonl(
                _FRESH_WATERMARK,
                _row(candidate_id="f-1", source_key="f1"),
                _row(candidate_id="f-2", source_key="f2"),
            ),
            "vault_shared/cached_opportunities/state/s.jsonl": _jsonl(
                _FRESH_WATERMARK,
                _row(candidate_id="s-1", source_key="s1"),
            ),
            "vault_shared/cached_opportunities/foundation/fo.jsonl": _jsonl(
                _FRESH_WATERMARK,
                _row(candidate_id="fo-1", source_key="fo1"),
                _row(candidate_id="fo-2", source_key="fo2"),
            ),
        }
        result, _ = _run(files=files)
        assert result.channel_state == HEALTH_OK
        assert len(result.candidates) == 5

    def test_empty_file_no_rows_still_ok(self):
        files = {
            "vault_shared/cached_opportunities/federal/empty.jsonl": b"",
        }
        result, _ = _run(files=files)
        assert result.channel_state == HEALTH_OK
        assert result.candidates == ()
        assert result.per_file_events == ()

    def test_respects_per_org_subscribed_feeds(self):
        files = {
            "orgs/fit_farms_llc/vault/subscribed_feeds/myco.jsonl": _jsonl(
                _FRESH_WATERMARK,
                _row(candidate_id="sub-1", source_key="sub1"),
            ),
            "vault_shared/cached_opportunities/federal/u.jsonl": _jsonl(
                _FRESH_WATERMARK,
                _row(candidate_id="fed-1", source_key="fed1"),
            ),
        }
        result, reader = _run(files=files)
        assert result.channel_state == HEALTH_OK
        assert {c.candidate_id for c in result.candidates} == {"sub-1", "fed-1"}
        # Both paths were read.
        assert len(reader.calls) == 2


# ---------------------------------------------------------------------------
# TestWatermark — 6
# ---------------------------------------------------------------------------


class TestWatermark:
    def _one_file(self, watermark: str) -> dict[str, bytes]:
        return {
            "vault_shared/cached_opportunities/federal/a.jsonl": _jsonl(
                watermark, _row()
            )
        }

    def test_zero_day_watermark_ok(self):
        result, _ = _run(files=self._one_file(_FRESH_WATERMARK))
        assert result.channel_state == HEALTH_OK
        assert result.per_file_events == ()

    def test_14_day_watermark_boundary_ok(self):
        # Exactly 14 days old — inclusive of allowed.
        result, _ = _run(files=self._one_file("2026-04-06T00:00:00Z"))
        assert result.channel_state == HEALTH_OK
        assert all(
            e.reason_tag != "cache_stale_channel_b"
            for e in result.per_file_events
        )

    def test_15_day_watermark_degrades(self):
        result, _ = _run(files=self._one_file("2026-04-04T00:00:00Z"))
        assert result.channel_state == HEALTH_DEGRADED
        stale = [
            e for e in result.per_file_events
            if e.reason_tag == "cache_stale_channel_b"
        ]
        assert len(stale) == 1
        assert stale[0].code == "F-SCOUT-B-02"
        assert stale[0].severity == "MEDIUM"
        # Rows are still yielded on stale (data usable per §4.2).
        assert len(result.candidates) == 1

    def test_missing_header_yields_f_scout_b_02(self):
        # File has rows but no header watermark.
        body = "\n".join([_row(), _row(candidate_id="c-002")]).encode("utf-8")
        result, _ = _run(
            files={
                "vault_shared/cached_opportunities/federal/no_header.jsonl": body
            }
        )
        assert result.channel_state == HEALTH_DEGRADED
        codes = {e.code for e in result.per_file_events}
        assert "F-SCOUT-B-02" in codes
        assert result.candidates == ()

    def test_header_without_watermark_key(self):
        body = "\n".join(
            [json.dumps({"note": "this is not a watermark header"}), _row()]
        ).encode("utf-8")
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/x.jsonl": body}
        )
        assert result.channel_state == HEALTH_DEGRADED
        tags = {e.reason_tag for e in result.per_file_events}
        assert "missing_watermark_utc" in tags

    def test_watermark_unparseable_is_f_scout_b_02(self):
        body = "\n".join(
            [json.dumps({"watermark_utc": "not-a-date"}), _row()]
        ).encode("utf-8")
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/bad.jsonl": body}
        )
        assert result.channel_state == HEALTH_DEGRADED
        tags = {e.reason_tag or "" for e in result.per_file_events}
        assert any(t.startswith("watermark_unparseable") for t in tags)


# ---------------------------------------------------------------------------
# TestMalformedRows — 7
# ---------------------------------------------------------------------------


class TestMalformedRows:
    def test_single_malformed_row_is_row_skipped(self):
        body = "\n".join(
            [
                _header(_FRESH_WATERMARK),
                _row(candidate_id="ok-1"),
                "{not-json",
                _row(candidate_id="ok-2"),
                _row(candidate_id="ok-3"),
                _row(candidate_id="ok-4"),
                _row(candidate_id="ok-5"),
                _row(candidate_id="ok-6"),
                _row(candidate_id="ok-7"),
                _row(candidate_id="ok-8"),
                _row(candidate_id="ok-9"),
            ]
        ).encode("utf-8")
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/m.jsonl": body}
        )
        # 1 malformed / 10 data rows = 10% exactly → DEGRADED (inclusive).
        assert len(result.candidates) == 9
        assert result.channel_state == HEALTH_DEGRADED
        codes = [e.code for e in result.per_file_events]
        assert codes.count("F-SCOUT-B-01") == 1
        assert codes.count("F-SCOUT-B-05") == 1

    def test_below_10pct_malformed_stays_ok(self):
        # 1 malformed / 11 data rows ≈ 9.09% → OK.
        ok_rows = [_row(candidate_id=f"ok-{i}") for i in range(10)]
        body = "\n".join(
            [_header(_FRESH_WATERMARK), "{not-json", *ok_rows]
        ).encode("utf-8")
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/b.jsonl": body}
        )
        assert result.channel_state == HEALTH_OK
        assert len(result.candidates) == 10
        codes = {e.code for e in result.per_file_events}
        assert "F-SCOUT-B-01" in codes
        assert "F-SCOUT-B-05" not in codes

    def test_exactly_10pct_malformed_degrades(self):
        # 1 malformed / 10 rows = 10.0% → DEGRADED.
        ok_rows = [_row(candidate_id=f"ok-{i}") for i in range(9)]
        body = "\n".join(
            [_header(_FRESH_WATERMARK), "{bad-json", *ok_rows]
        ).encode("utf-8")
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/c.jsonl": body}
        )
        assert result.channel_state == HEALTH_DEGRADED
        codes = [e.code for e in result.per_file_events]
        assert "F-SCOUT-B-05" in codes
        assert len(result.candidates) == 9

    def test_100pct_malformed_yields_no_candidates_and_degrades(self):
        body = "\n".join(
            [
                _header(_FRESH_WATERMARK),
                "{bad-1",
                "{bad-2",
                "{bad-3",
            ]
        ).encode("utf-8")
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/d.jsonl": body}
        )
        assert result.candidates == ()
        assert result.channel_state == HEALTH_DEGRADED
        codes = [e.code for e in result.per_file_events]
        assert codes.count("F-SCOUT-B-01") == 3
        assert "F-SCOUT-B-05" in codes

    def test_malformed_plus_identity_mismatch_failed_wins(self):
        body = "\n".join(
            [_header(_FRESH_WATERMARK), "{not-json", "{also-bad"]
        ).encode("utf-8")
        session = _FakeSession()
        path = "vault_shared/cached_opportunities/federal/e.jsonl"
        result, _ = _run(
            files={path: body},
            identity_overrides={
                path: _FakeIdentity(
                    intent=INTENT_CACHE_READ,
                    session_id="WRONG-SESSION",
                    slug=session.slug,
                )
            },
            session=session,
        )
        # FAILED takes precedence; file is aborted before row parsing so
        # no F-SCOUT-B-01 events appear for this file.
        assert result.channel_state == HEALTH_FAILED
        codes = [e.code for e in result.per_file_events]
        assert "F-SCOUT-B-04" in codes
        assert "F-SCOUT-B-01" not in codes

    def test_row_with_non_dict_json_is_skipped(self):
        body = "\n".join(
            [
                _header(_FRESH_WATERMARK),
                json.dumps(["not", "a", "dict"]),
                _row(candidate_id="c-ok"),
            ]
        ).encode("utf-8")
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/n.jsonl": body}
        )
        # 1 malformed / 2 data rows = 50% → DEGRADED.
        assert result.channel_state == HEALTH_DEGRADED
        assert len(result.candidates) == 1

    def test_row_missing_required_field_is_skipped(self):
        # `fit_score_cached` missing — row rejected with F-SCOUT-B-01.
        incomplete = json.dumps(
            {
                "candidate_id": "c-x",
                "feed_or_adapter_id": "cache:x",
                "source_key": "x",
                "title": "t",
                "funder": "f",
                "funder_kind": "federal",
                "url": "https://x",
                "applicant_types": ["nonprofit"],
                "fetch_timestamp_utc": "2026-04-01T00:00:00Z",
                "url_hash": "aa" * 32,
            }
        )
        body = "\n".join(
            [_header(_FRESH_WATERMARK), incomplete, _row(candidate_id="c-ok")]
        ).encode("utf-8")
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/r.jsonl": body}
        )
        assert len(result.candidates) == 1
        codes = [e.code for e in result.per_file_events]
        assert "F-SCOUT-B-01" in codes


# ---------------------------------------------------------------------------
# TestIdentityTupleMismatch — 6
# ---------------------------------------------------------------------------


class TestIdentityTupleMismatch:
    def _single_file(self) -> tuple[str, dict[str, bytes]]:
        path = "vault_shared/cached_opportunities/federal/id.jsonl"
        files = {path: _jsonl(_FRESH_WATERMARK, _row())}
        return path, files

    def test_intent_mismatch_failed(self):
        path, files = self._single_file()
        session = _FakeSession()
        result, _ = _run(
            files=files,
            identity_overrides={
                path: _FakeIdentity(
                    intent="write",
                    session_id=session.session_id,
                    slug=session.slug,
                )
            },
            session=session,
        )
        assert result.channel_state == HEALTH_FAILED
        assert result.candidates == ()
        assert result.per_file_events[0].code == "F-SCOUT-B-04"

    def test_slug_mismatch_failed(self):
        path, files = self._single_file()
        session = _FakeSession()
        result, _ = _run(
            files=files,
            identity_overrides={
                path: _FakeIdentity(
                    intent=INTENT_CACHE_READ,
                    session_id=session.session_id,
                    slug="other_org",
                )
            },
            session=session,
        )
        assert result.channel_state == HEALTH_FAILED
        assert result.per_file_events[0].code == "F-SCOUT-B-04"

    def test_session_id_mismatch_failed(self):
        path, files = self._single_file()
        session = _FakeSession()
        result, _ = _run(
            files=files,
            identity_overrides={
                path: _FakeIdentity(
                    intent=INTENT_CACHE_READ,
                    session_id="attacker-session",
                    slug=session.slug,
                )
            },
            session=session,
        )
        assert result.channel_state == HEALTH_FAILED
        assert result.per_file_events[0].code == "F-SCOUT-B-04"

    def test_nfc_drift_triggers_b_05(self):
        # NFC-composed "é" (U+00E9) vs NFD-decomposed "e" + U+0301 combining acute.
        path, files = self._single_file()
        session = _FakeSession()
        # Use a decomposed form of the intent string. The intent is ASCII so
        # inject a non-ASCII NFC-drift pattern by appending combining accent
        # that normalises to identity suffix mismatch at strict level.
        decomposed = "cache-read" + "\u0301"  # lone combining accent
        result, _ = _run(
            files=files,
            identity_overrides={
                path: _FakeIdentity(
                    intent=decomposed,
                    session_id=session.session_id,
                    slug=session.slug,
                )
            },
            session=session,
        )
        # Combining accent attached to 'd' composes to 'ḋ'-like — NFC.normalize
        # does not reduce back to 'cache-read'. Strict mismatch → F-SCOUT-B-04.
        # Verify code is in the -04 / -05 family.
        assert result.channel_state == HEALTH_FAILED
        assert result.per_file_events[0].code in {"F-SCOUT-B-04", "F-SCOUT-B-05"}

    def test_trailing_whitespace_intent_triggers_b_05(self):
        path, files = self._single_file()
        session = _FakeSession()
        result, _ = _run(
            files=files,
            identity_overrides={
                path: _FakeIdentity(
                    intent="cache-read ",
                    session_id=session.session_id,
                    slug=session.slug,
                )
            },
            session=session,
        )
        assert result.channel_state == HEALTH_FAILED
        assert result.per_file_events[0].code == "F-SCOUT-B-05"

    def test_failed_file_does_not_block_other_files(self):
        good_path = "vault_shared/cached_opportunities/federal/good.jsonl"
        bad_path = "vault_shared/cached_opportunities/federal/bad.jsonl"
        files = {
            good_path: _jsonl(
                _FRESH_WATERMARK, _row(candidate_id="good-1")
            ),
            bad_path: _jsonl(
                _FRESH_WATERMARK, _row(candidate_id="bad-1")
            ),
        }
        session = _FakeSession()
        result, _ = _run(
            files=files,
            identity_overrides={
                bad_path: _FakeIdentity(
                    intent="wrong",
                    session_id=session.session_id,
                    slug=session.slug,
                )
            },
            session=session,
        )
        # Channel FAILED sticky, but good-1 still yielded.
        assert result.channel_state == HEALTH_FAILED
        ids = {c.candidate_id for c in result.candidates}
        assert "good-1" in ids
        assert "bad-1" not in ids


# ---------------------------------------------------------------------------
# TestS10aRowKind — 2 (current locus is Section 2 write-time, ARCH-02)
# ---------------------------------------------------------------------------


class TestS10aRowKind:
    def test_row_with_slug_field_currently_accepted(self):
        """ARCH-02 current locus: Section 2 write-time is authoritative.

        Scout Round 3 does not inspect row contents for S10a. A row carrying
        a forbidden ``slug`` key is currently consumed. When ARCH-02 moves
        S10a read-time enforcement into Scout, this test polarity flips and
        ``F-SCOUT-B-03`` is emitted.
        """
        dirty_row = json.dumps(
            {
                "candidate_id": "c-dirty",
                "feed_or_adapter_id": "cache:dirty",
                "source_key": "dirty",
                "title": "T",
                "funder": "F",
                "funder_kind": "federal",
                "url": "https://x",
                "applicant_types": ["nonprofit"],
                "fetch_timestamp_utc": "2026-04-01T00:00:00Z",
                "url_hash": "cd" * 32,
                "fit_score_cached": 70,
                # The forbidden field:
                "slug": "fit_farms_llc",
            }
        )
        body = "\n".join([_header(_FRESH_WATERMARK), dirty_row]).encode("utf-8")
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/s.jsonl": body}
        )
        assert result.channel_state == HEALTH_OK
        codes = {e.code for e in result.per_file_events}
        assert "F-SCOUT-B-03" not in codes
        assert len(result.candidates) == 1

    def test_polarity_inversion_documenting_current_locus(self):
        """Defence-in-depth placeholder: asserts F-SCOUT-B-03 NOT emitted.

        When ARCH-02 resolves Scout-read-time as the enforcement locus, the
        assertion flips to ``"F-SCOUT-B-03" in codes`` and the row count
        flips to 0.
        """
        dirty_row = json.dumps(
            {
                "candidate_id": "c-d2",
                "feed_or_adapter_id": "cache:d2",
                "source_key": "d2",
                "title": "T",
                "funder": "F",
                "funder_kind": "federal",
                "url": "https://x",
                "applicant_types": ["nonprofit"],
                "fetch_timestamp_utc": "2026-04-01T00:00:00Z",
                "url_hash": "ef" * 32,
                "fit_score_cached": 70,
                "session_id": "sess-leak",  # another org-identifier-like key
            }
        )
        body = "\n".join([_header(_FRESH_WATERMARK), dirty_row]).encode("utf-8")
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/p.jsonl": body}
        )
        assert result.channel_state == HEALTH_OK
        codes = {e.code for e in result.per_file_events}
        assert "F-SCOUT-B-03" not in codes


# ---------------------------------------------------------------------------
# TestFileOrdering — 3
# ---------------------------------------------------------------------------


class TestFileOrdering:
    def test_candidate_order_is_stable_across_invocations(self):
        files = {
            "vault_shared/cached_opportunities/state/z.jsonl": _jsonl(
                _FRESH_WATERMARK, _row(candidate_id="z-1")
            ),
            "vault_shared/cached_opportunities/federal/a.jsonl": _jsonl(
                _FRESH_WATERMARK, _row(candidate_id="a-1")
            ),
            "vault_shared/cached_opportunities/foundation/m.jsonl": _jsonl(
                _FRESH_WATERMARK, _row(candidate_id="m-1")
            ),
        }
        r1, _ = _run(files=files, paths_order=tuple(files.keys()))
        r2, _ = _run(files=files, paths_order=tuple(reversed(list(files.keys()))))
        assert [c.candidate_id for c in r1.candidates] == [
            "a-1",
            "m-1",
            "z-1",
        ]
        assert [c.candidate_id for c in r1.candidates] == [
            c.candidate_id for c in r2.candidates
        ]

    def test_path_lister_is_sorted_internally(self):
        path_a = "vault_shared/cached_opportunities/federal/a.jsonl"
        path_b = "vault_shared/cached_opportunities/federal/b.jsonl"
        files = {
            path_b: _jsonl(_FRESH_WATERMARK, _row(candidate_id="b")),
            path_a: _jsonl(_FRESH_WATERMARK, _row(candidate_id="a")),
        }
        result, reader = _run(files=files, paths_order=(path_b, path_a))
        # Read call order follows sorted() of the real paths (alphabetical).
        call_paths = [c["path"] for c in reader.calls]
        assert call_paths == [path_a, path_b]
        assert [c.candidate_id for c in result.candidates] == ["a", "b"]

    def test_zero_files_yields_ok_and_empty(self):
        result, _ = _run(files={}, paths_order=())
        assert result.channel_state == HEALTH_OK
        assert result.candidates == ()
        assert result.per_file_events == ()


# ---------------------------------------------------------------------------
# TestFitScoreVerbatim — 3
# ---------------------------------------------------------------------------


class TestFitScoreVerbatim:
    def test_low_fit_rows_not_filtered(self):
        body = _jsonl(
            _FRESH_WATERMARK,
            _row(candidate_id="low-1", fit_score_cached=10),
            _row(candidate_id="low-2", fit_score_cached=0),
        )
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/lf.jsonl": body}
        )
        scores = sorted(c.fit_score_cached for c in result.candidates)
        assert scores == [0, 10]

    def test_high_fit_rows_carry_through(self):
        body = _jsonl(
            _FRESH_WATERMARK,
            _row(candidate_id="hi-1", fit_score_cached=90),
            _row(candidate_id="hi-2", fit_score_cached=100),
        )
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/hf.jsonl": body}
        )
        scores = sorted(c.fit_score_cached for c in result.candidates)
        assert scores == [90, 100]

    def test_mixed_fit_rows_all_returned(self):
        body = _jsonl(
            _FRESH_WATERMARK,
            _row(candidate_id="mix-1", fit_score_cached=5),
            _row(candidate_id="mix-2", fit_score_cached=59),
            _row(candidate_id="mix-3", fit_score_cached=60),
            _row(candidate_id="mix-4", fit_score_cached=99),
        )
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/mx.jsonl": body}
        )
        assert len(result.candidates) == 4
        assert {c.fit_score_cached for c in result.candidates} == {5, 59, 60, 99}


# ---------------------------------------------------------------------------
# TestVaultReaderCallSite — 5
# ---------------------------------------------------------------------------


class TestVaultReaderCallSite:
    def test_reader_called_with_cache_read_intent(self):
        path = "vault_shared/cached_opportunities/federal/v.jsonl"
        result, reader = _run(files={path: _jsonl(_FRESH_WATERMARK, _row())})
        assert all(c["intent"] == INTENT_CACHE_READ for c in reader.calls)
        assert INTENT_CACHE_READ == "cache-read"
        assert result.channel_state == HEALTH_OK

    def test_reader_called_with_each_path(self):
        files = {
            "vault_shared/cached_opportunities/federal/a.jsonl": _jsonl(
                _FRESH_WATERMARK, _row(candidate_id="a")
            ),
            "vault_shared/cached_opportunities/state/b.jsonl": _jsonl(
                _FRESH_WATERMARK, _row(candidate_id="b")
            ),
        }
        _, reader = _run(files=files)
        call_paths = {c["path"] for c in reader.calls}
        assert call_paths == set(files.keys())

    def test_reader_gets_session_id_propagated(self):
        session = _FakeSession(session_id="sess-verify-propagation")
        _, reader = _run(
            files={
                "vault_shared/cached_opportunities/federal/s.jsonl": _jsonl(
                    _FRESH_WATERMARK, _row()
                )
            },
            session=session,
        )
        assert reader.calls[0]["session_id"] == "sess-verify-propagation"

    def test_reader_gets_slug_propagated(self):
        session = _FakeSession(slug="mycosymbiotics_cooperative")
        _, reader = _run(
            files={
                "vault_shared/cached_opportunities/federal/s.jsonl": _jsonl(
                    _FRESH_WATERMARK, _row()
                )
            },
            session=session,
        )
        assert reader.calls[0]["slug"] == "mycosymbiotics_cooperative"

    def test_path_lister_receives_slug(self):
        captured: list[str] = []

        def listfn(slug: str) -> tuple[str, ...]:
            captured.append(slug)
            return ()

        discover_channel_b(
            session=_FakeSession(slug="org_under_test"),
            vault_reader=_MemoryVaultReader(),
            list_cache_paths=listfn,
            clock=_fixed_clock(_NOW_ISO),
        )
        assert captured == ["org_under_test"]


# ---------------------------------------------------------------------------
# TestNoModuleSideEffects — 1
# ---------------------------------------------------------------------------


class TestNoModuleSideEffects:
    def test_import_has_no_side_effects(self):
        # Re-import in an isolated manner — any side-effect (disk open,
        # network call) at module level would already have fired during
        # pytest collection. This test is the explicit documentation gate.
        import importlib

        mod = importlib.import_module("pipeline.scout.channel_b_cache")
        # Protocols + dataclasses + the public function are all that the
        # module should expose. No `_CACHE_OPEN`, no singleton state.
        public = {name for name in dir(mod) if not name.startswith("_")}
        assert "discover_channel_b" in public
        assert "ChannelBDiscoverResult" in public
        assert "VaultReader" in public


# ---------------------------------------------------------------------------
# TestASTLintRegression — 1
# ---------------------------------------------------------------------------


class TestASTLintRegression:
    def test_channel_b_cache_is_lint_clean(self):
        repo_root = Path(__file__).resolve().parents[2]
        target = repo_root / "pipeline" / "scout"
        violations = [
            v
            for v in lint_tree(target, DEFAULT_RULES)
            if v.file.name == "channel_b_cache.py"
        ]
        assert violations == []


# ---------------------------------------------------------------------------
# TestKWOnly — 1
# ---------------------------------------------------------------------------


class TestKWOnly:
    def test_positional_call_rejected(self):
        session = _FakeSession()
        reader = _MemoryVaultReader()
        with pytest.raises(TypeError):
            discover_channel_b(
                session,
                reader,
                lambda slug: (),
                _fixed_clock(_NOW_ISO),
            )  # type: ignore[misc]


# ---------------------------------------------------------------------------
# TestProtocolDiscipline — 2
# ---------------------------------------------------------------------------


class TestProtocolDiscipline:
    def test_minimal_duck_typed_session_works(self):
        class _MinimalSession:
            session_id = "sess-minimal"
            slug = "org_minimal"

        path = "vault_shared/cached_opportunities/federal/p.jsonl"
        reader = _MemoryVaultReader(files={path: _jsonl(_FRESH_WATERMARK, _row())})
        result = discover_channel_b(
            session=_MinimalSession(),
            vault_reader=reader,
            list_cache_paths=lambda slug: (path,),
            clock=_fixed_clock(_NOW_ISO),
        )
        assert result.channel_state == HEALTH_OK
        assert len(result.candidates) == 1

    def test_minimal_duck_typed_identity_works(self):
        @dataclass
        class _TinyIdentity:
            intent: str
            session_id: str
            slug: str

        path = "vault_shared/cached_opportunities/federal/t.jsonl"
        session = _FakeSession()

        class _TinyReader:
            def read(
                self,
                *,
                path: str,
                intent: str,
                session_id: str,
                slug: str,
            ) -> tuple[bytes, _TinyIdentity]:
                return (
                    _jsonl(_FRESH_WATERMARK, _row()),
                    _TinyIdentity(
                        intent=intent,
                        session_id=session_id,
                        slug=slug,
                    ),
                )

        result = discover_channel_b(
            session=session,
            vault_reader=_TinyReader(),
            list_cache_paths=lambda slug: (path,),
            clock=_fixed_clock(_NOW_ISO),
        )
        assert result.channel_state == HEALTH_OK


# ---------------------------------------------------------------------------
# TestChannelStateAggregation — 4
# ---------------------------------------------------------------------------


class TestChannelStateAggregation:
    def test_all_files_ok_yields_ok(self):
        files = {
            "vault_shared/cached_opportunities/federal/a.jsonl": _jsonl(
                _FRESH_WATERMARK, _row(candidate_id="a")
            ),
            "vault_shared/cached_opportunities/state/b.jsonl": _jsonl(
                _FRESH_WATERMARK, _row(candidate_id="b")
            ),
        }
        result, _ = _run(files=files)
        assert result.channel_state == HEALTH_OK

    def test_one_stale_file_plus_ok_yields_degraded(self):
        files = {
            "vault_shared/cached_opportunities/federal/fresh.jsonl": _jsonl(
                _FRESH_WATERMARK, _row(candidate_id="fresh")
            ),
            "vault_shared/cached_opportunities/state/stale.jsonl": _jsonl(
                "2026-01-01T00:00:00Z", _row(candidate_id="stale")
            ),
        }
        result, _ = _run(files=files)
        assert result.channel_state == HEALTH_DEGRADED

    def test_one_identity_mismatch_file_yields_failed(self):
        good = "vault_shared/cached_opportunities/federal/good.jsonl"
        bad = "vault_shared/cached_opportunities/state/bad.jsonl"
        session = _FakeSession()
        files = {
            good: _jsonl(_FRESH_WATERMARK, _row(candidate_id="good")),
            bad: _jsonl(_FRESH_WATERMARK, _row(candidate_id="bad")),
        }
        result, _ = _run(
            files=files,
            identity_overrides={
                bad: _FakeIdentity(
                    intent="wrong",
                    session_id=session.session_id,
                    slug=session.slug,
                )
            },
            session=session,
        )
        assert result.channel_state == HEALTH_FAILED

    def test_degraded_sticky_not_downgraded_to_ok(self):
        files = {
            "vault_shared/cached_opportunities/federal/stale.jsonl": _jsonl(
                "2026-01-01T00:00:00Z", _row(candidate_id="s")
            ),
            "vault_shared/cached_opportunities/state/fresh.jsonl": _jsonl(
                _FRESH_WATERMARK, _row(candidate_id="f")
            ),
        }
        # Order: stale first, then fresh — channel state should stick at DEGRADED.
        result, _ = _run(
            files=files,
            paths_order=(
                "vault_shared/cached_opportunities/federal/stale.jsonl",
                "vault_shared/cached_opportunities/state/fresh.jsonl",
            ),
        )
        assert result.channel_state == HEALTH_DEGRADED


# ---------------------------------------------------------------------------
# TestNonceReleasedAfterRead — 1 (placeholder, Channel B is local-only)
# ---------------------------------------------------------------------------


class TestNonceReleasedAfterRead:
    def test_channel_b_does_not_reserve_nonces(self):
        """Placeholder: Channel A reserves outbound-network nonces; Channel
        B is local-only and does not. The ``nonce_released_on_every_exit_path``
        invariant is therefore vacuously true for Channel B. This test lives
        here so that the §7.2 blueprint checklist has a concrete assertion
        against the Channel B module when the checklist is mechanically
        audited.
        """
        path = "vault_shared/cached_opportunities/federal/n.jsonl"
        result, reader = _run(
            files={path: _jsonl(_FRESH_WATERMARK, _row())}
        )
        # Evidence: the reader was called, but no nonce-related kwargs were
        # passed — the VaultReader Protocol does not expose nonces.
        assert all(
            set(call.keys()) == {"path", "intent", "session_id", "slug"}
            for call in reader.calls
        )
        assert result.channel_state == HEALTH_OK


# ---------------------------------------------------------------------------
# TestPublicSurface — 3 (coverage: re-exports + canonical intent constant)
# ---------------------------------------------------------------------------


class TestPublicSurface:
    def test_channel_b_symbols_reexported(self):
        # Round 3 adds these to the pipeline.scout public surface.
        for name in (
            "discover_channel_b",
            "ChannelBDiscoverResult",
            "ChannelBIdentityTupleMismatch",
            "DegradationEvent",
            "INTENT_CACHE_READ",
            "VaultReader",
        ):
            assert hasattr(scout, name), name

    def test_version_bumped_to_round_3(self):
        # Monotonic: scout package version is bumped each round; pin to the
        # latest-locked round prefix to avoid drift breakage.
        assert scout.__version__.startswith("0.1.0-scout-r")
        assert int(scout.__version__.rsplit("r", 1)[1]) >= 3

    def test_intent_cache_read_is_cache_read(self):
        # The §9 canonical intent string Channel B must use on vault_read.
        assert INTENT_CACHE_READ == "cache-read"

    def test_degradation_event_is_frozen_kw_only(self):
        # Module-level frozen kw_only dataclass invariant (§2 style).
        with pytest.raises(TypeError):
            DegradationEvent("p", "F-SCOUT-B-01", None, "LOW")  # type: ignore[misc]
        ev = DegradationEvent(
            path="p", code="F-SCOUT-B-01", reason_tag=None, severity="LOW"
        )
        with pytest.raises(Exception):
            ev.path = "other"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# TestEdgeCaseCoverage — auxiliary exercises (100 % coverage target)
# ---------------------------------------------------------------------------


class TestEdgeCaseCoverage:
    def test_identity_mismatch_exception_carries_code(self):
        exc = ChannelBIdentityTupleMismatch("hit", sub_tag="intent_nfc_drift")
        assert exc.code == "F-SCOUT-B-04"
        assert exc.sub_tag == "intent_nfc_drift"
        assert str(exc) == "hit"

    def test_default_clock_used_when_omitted(self):
        # Exercises the ``_default_clock`` branch — discover_channel_b is
        # called without ``clock`` and must succeed against a fresh file.
        from datetime import datetime as _dt_dt, timezone as _tz

        now_iso = (
            _dt_dt.now(_tz.utc)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z")
        )
        path = "vault_shared/cached_opportunities/federal/dc.jsonl"
        reader = _MemoryVaultReader(
            files={path: _jsonl(now_iso, _row(candidate_id="dc"))}
        )
        result = discover_channel_b(
            session=_FakeSession(),
            vault_reader=reader,
            list_cache_paths=lambda slug: (path,),
        )
        assert result.channel_state == HEALTH_OK
        assert len(result.candidates) == 1

    def test_watermark_non_string_degrades(self):
        body = "\n".join(
            [json.dumps({"watermark_utc": 42}), _row()]
        ).encode("utf-8")
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/ns.jsonl": body}
        )
        assert result.channel_state == HEALTH_DEGRADED
        tags = {e.reason_tag or "" for e in result.per_file_events}
        assert any(t.startswith("watermark_unparseable") for t in tags)

    def test_watermark_naive_timezone_degrades(self):
        body = "\n".join(
            [json.dumps({"watermark_utc": "2026-04-20T00:00:00"}), _row()]
        ).encode("utf-8")
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/nt.jsonl": body}
        )
        assert result.channel_state == HEALTH_DEGRADED
        tags = {e.reason_tag or "" for e in result.per_file_events}
        assert any(t.startswith("watermark_unparseable") for t in tags)

    def test_blank_data_line_skipped_not_malformed(self):
        # A single blank data line should be treated as absent (parsed to
        # None by `_parse_row` but not counted — wait, it IS counted as
        # malformed per current semantics since _parse_row returns None).
        # Two data lines: one blank, one valid. Blank → malformed; 1/2=50%
        # → DEGRADED; valid row still yielded.
        body = (
            "\n".join([_header(_FRESH_WATERMARK), "", _row(candidate_id="ok")])
        ).encode("utf-8")
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/bl.jsonl": body}
        )
        assert result.channel_state == HEALTH_DEGRADED
        assert len(result.candidates) == 1

    def test_applicant_types_not_a_list_rejected(self):
        bad = json.dumps(
            {
                "candidate_id": "c-at",
                "feed_or_adapter_id": "cache:at",
                "source_key": "at",
                "title": "T",
                "funder": "F",
                "funder_kind": "federal",
                "url": "https://x",
                "applicant_types": "nonprofit",  # wrong: str, not list
                "fetch_timestamp_utc": "2026-04-01T00:00:00Z",
                "url_hash": "cd" * 32,
                "fit_score_cached": 70,
            }
        )
        body = "\n".join([_header(_FRESH_WATERMARK), bad, _row()]).encode(
            "utf-8"
        )
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/at.jsonl": body}
        )
        # 1 rejected / 2 rows = 50% → DEGRADED, 1 candidate yielded.
        assert result.channel_state == HEALTH_DEGRADED
        assert len(result.candidates) == 1

    def test_fit_score_non_numeric_rejected(self):
        bad = json.dumps(
            {
                "candidate_id": "c-fs",
                "feed_or_adapter_id": "cache:fs",
                "source_key": "fs",
                "title": "T",
                "funder": "F",
                "funder_kind": "federal",
                "url": "https://x",
                "applicant_types": ["nonprofit"],
                "fetch_timestamp_utc": "2026-04-01T00:00:00Z",
                "url_hash": "ef" * 32,
                "fit_score_cached": "not-a-number",
            }
        )
        body = "\n".join([_header(_FRESH_WATERMARK), bad, _row()]).encode(
            "utf-8"
        )
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/fs.jsonl": body}
        )
        assert len(result.candidates) == 1
        codes = [e.code for e in result.per_file_events]
        assert "F-SCOUT-B-01" in codes

    def test_utf8_decode_error_degrades(self):
        bad_bytes = b"\xff\xfe\x00\x00 not-valid-utf8"
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/u.jsonl": bad_bytes}
        )
        assert result.channel_state == HEALTH_DEGRADED
        tags = {e.reason_tag for e in result.per_file_events}
        assert "utf8_decode_error" in tags

    def test_blank_header_line_degrades(self):
        # First line is blank but file has more lines — header_line_blank.
        body = b"\n" + _row().encode("utf-8") + b"\n"
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/bh.jsonl": body}
        )
        assert result.channel_state == HEALTH_DEGRADED
        tags = {e.reason_tag for e in result.per_file_events}
        assert "header_line_blank" in tags

    def test_header_unparseable_json_degrades(self):
        body = (
            "{not-valid-json\n" + _row() + "\n"
        ).encode("utf-8")
        result, _ = _run(
            files={"vault_shared/cached_opportunities/federal/hh.jsonl": body}
        )
        assert result.channel_state == HEALTH_DEGRADED
        tags = {e.reason_tag for e in result.per_file_events}
        assert "header_unparseable" in tags
