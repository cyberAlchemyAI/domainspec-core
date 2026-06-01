"""Happy-path tests for pipeline.loop.tab_delivery — §4.11 three-tab envelope.

Blueprint §5 v6 §4.11 LOCKED 2026-04-19 (inline-literal runtime check +
post-write verify + module-load integrity assert).

Coverage targets (spec card ``section_05_round_9_tab_delivery.md``):
- ``deliver_tab`` happy path: envelope construction, three hash_file calls
  in declaration order, canonical-bytes + sha256 round-trip, one
  vault_write (``write-if-absent`` / ``state-success``), one vault_read
  for post-write verify, returned :class:`TabSigningResult` shape.
- Re-export surface: ``from pipeline.loop import deliver_tab, ...``.
- Canonical-bytes determinism: same envelope → same bytes.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

import pytest

from pipeline.loop import (
    HashFileCallable,
    TabSigningResult,
    deliver_tab,
)
from pipeline.loop.tab_delivery import (
    _canonical_bytes,
    _canonical_bytes_without_self_hash,
    _parse_envelope,
)
from pipeline.loop.types import IterationState, RunState, TabEnvelope


# ---------------------------------------------------------------------------
# Fakes
# ---------------------------------------------------------------------------


@dataclass
class _FakeClock:
    iso_values: list[str] = field(
        default_factory=lambda: ["2026-04-21T12:00:00.000+00:00"]
    )
    ms_values: list[int] = field(default_factory=lambda: [1_714_000_000_000])
    _iso_i: int = 0
    _ms_i: int = 0

    def now_ms(self) -> int:
        if self._ms_i >= len(self.ms_values):
            return self.ms_values[-1] if self.ms_values else 0
        v = self.ms_values[self._ms_i]
        self._ms_i += 1
        return v

    def now_iso(self) -> str:
        if self._iso_i >= len(self.iso_values):
            return self.iso_values[-1] if self.iso_values else ""
        v = self.iso_values[self._iso_i]
        self._iso_i += 1
        return v


@dataclass
class _FakeVault:
    """In-process vault: supports write-if-absent + read-back."""

    store: dict[str, bytes] = field(default_factory=dict)
    read_calls: list[str] = field(default_factory=list)
    write_calls: list[dict[str, Any]] = field(default_factory=list)

    def read(self, *, path: str) -> bytes:
        self.read_calls.append(path)
        if path not in self.store:
            raise KeyError(path)
        return self.store[path]

    def write(
        self,
        *,
        path: str,
        payload: bytes,
        intent: str,
        write_mode: str,
        expected_current_file_hash: str | None,
    ) -> str:
        self.write_calls.append(
            {
                "path": path,
                "payload": payload,
                "intent": intent,
                "write_mode": write_mode,
                "expected_current_file_hash": expected_current_file_hash,
            }
        )
        if write_mode == "write-if-absent" and path in self.store:
            from pipeline.vault.error_codes import VaultWriteExists

            raise VaultWriteExists(
                f"write-if-absent collision at {path} (fake)"
            )
        self.store[path] = payload
        return hashlib.sha256(payload).hexdigest()


@dataclass
class _FakeHashFile:
    """Records the (ordered) sequence of payload paths requested."""

    hashes: dict[str, str]
    seen: list[str] = field(default_factory=list)

    def __call__(self, path: str) -> str:
        self.seen.append(path)
        if path not in self.hashes:
            raise FileNotFoundError(path)
        return self.hashes[path]


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------


def _mk_run_state(
    *,
    run_id: str = "01HG-RUN-A",
    mode: str = "submission",
    started_at_iso: str = "2026-04-21T10:00:00+00:00",
    iter_count: int = 2,
) -> RunState:
    iterations = [
        IterationState(iter_number=i) for i in range(1, iter_count + 1)
    ]
    return RunState(
        schema_version=2,
        run_id=run_id,
        mode=mode,
        rfa_hash="a" * 64 if mode == "submission" else None,
        project_context_hash="b" * 64 if mode == "submission" else None,
        golden_set_ref=None if mode == "submission" else "orgs/x/golden/item_01",
        org_slug="mycosymbiotics_coop",
        session_id="SESS-1",
        phase="report_signed",
        started_at_iso=started_at_iso,
        iterations=iterations,
    )


def _mk_hashes(run_id: str, run_id_date: str, final_n: int) -> dict[str, str]:
    return {
        f"vault/fund_radar/{run_id_date}/live_radar.json": "1" * 64,
        f"vault/deep_brief/{run_id}/brief.md": "2" * 64,
        f"vault/pipeline/{run_id}/iter_{final_n}/scribe_draft.md": "3" * 64,
    }


# ---------------------------------------------------------------------------
# Happy paths
# ---------------------------------------------------------------------------


class TestHappyPath:
    def test_deliver_tab_returns_tab_signing_result(self) -> None:
        rs = _mk_run_state()
        vault = _FakeVault()
        clock = _FakeClock()
        hf = _FakeHashFile(hashes=_mk_hashes("01HG-RUN-A", "2026-04-21", 2))

        result = deliver_tab(
            run_state=rs,
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            hash_file=hf,
        )
        assert isinstance(result, TabSigningResult)
        assert isinstance(result.envelope, TabEnvelope)
        assert result.stored_envelope_hash == result.envelope.envelope_sha256
        assert result.vault_path == "pipeline/01HG-RUN-A/tab_envelope.json"
        assert result.written_at_iso == "2026-04-21T12:00:00.000+00:00"

    def test_tab_ordering_pinned_to_final_constant(self) -> None:
        rs = _mk_run_state()
        vault = _FakeVault()
        hf = _FakeHashFile(hashes=_mk_hashes("01HG-RUN-A", "2026-04-21", 2))

        result = deliver_tab(
            run_state=rs,
            vault_read=vault.read,
            vault_write=vault.write,
            clock=_FakeClock(),
            hash_file=hf,
        )
        assert result.envelope.tab_ordering == (
            "live_radar",
            "deep_brief",
            "council_draft",
        )

    def test_envelope_sha256_matches_canonical_bytes_without_self(self) -> None:
        rs = _mk_run_state()
        vault = _FakeVault()
        hf = _FakeHashFile(hashes=_mk_hashes("01HG-RUN-A", "2026-04-21", 2))

        result = deliver_tab(
            run_state=rs,
            vault_read=vault.read,
            vault_write=vault.write,
            clock=_FakeClock(),
            hash_file=hf,
        )
        # Re-compute the canonical-bytes-without-self and verify sha256.
        expected = hashlib.sha256(
            _canonical_bytes_without_self_hash(result.envelope)
        ).hexdigest()
        assert result.envelope.envelope_sha256 == expected

    def test_post_write_verify_reads_back_identical_hash(self) -> None:
        rs = _mk_run_state()
        vault = _FakeVault()
        hf = _FakeHashFile(hashes=_mk_hashes("01HG-RUN-A", "2026-04-21", 2))

        result = deliver_tab(
            run_state=rs,
            vault_read=vault.read,
            vault_write=vault.write,
            clock=_FakeClock(),
            hash_file=hf,
        )
        # B-v1-09 closure — stored bytes must re-parse to an envelope with
        # the same envelope_sha256.
        raw = vault.store[result.vault_path]
        parsed = _parse_envelope(raw)
        assert parsed.envelope_sha256 == result.envelope.envelope_sha256

    def test_hash_file_called_exactly_three_times_in_order(self) -> None:
        rs = _mk_run_state()
        vault = _FakeVault()
        hf = _FakeHashFile(hashes=_mk_hashes("01HG-RUN-A", "2026-04-21", 2))

        deliver_tab(
            run_state=rs,
            vault_read=vault.read,
            vault_write=vault.write,
            clock=_FakeClock(),
            hash_file=hf,
        )
        assert hf.seen == [
            "vault/fund_radar/2026-04-21/live_radar.json",
            "vault/deep_brief/01HG-RUN-A/brief.md",
            "vault/pipeline/01HG-RUN-A/iter_2/scribe_draft.md",
        ]

    def test_vault_write_call_shape(self) -> None:
        rs = _mk_run_state()
        vault = _FakeVault()
        hf = _FakeHashFile(hashes=_mk_hashes("01HG-RUN-A", "2026-04-21", 2))

        deliver_tab(
            run_state=rs,
            vault_read=vault.read,
            vault_write=vault.write,
            clock=_FakeClock(),
            hash_file=hf,
        )
        assert len(vault.write_calls) == 1
        call = vault.write_calls[0]
        assert call["path"] == "pipeline/01HG-RUN-A/tab_envelope.json"
        assert call["intent"] == "state-success"
        assert call["write_mode"] == "write-if-absent"
        assert call["expected_current_file_hash"] is None

    def test_exactly_one_vault_read_for_post_write_verify(self) -> None:
        rs = _mk_run_state()
        vault = _FakeVault()
        hf = _FakeHashFile(hashes=_mk_hashes("01HG-RUN-A", "2026-04-21", 2))

        deliver_tab(
            run_state=rs,
            vault_read=vault.read,
            vault_write=vault.write,
            clock=_FakeClock(),
            hash_file=hf,
        )
        assert vault.read_calls == ["pipeline/01HG-RUN-A/tab_envelope.json"]

    def test_assembled_at_iso_stamped_from_clock(self) -> None:
        rs = _mk_run_state()
        vault = _FakeVault()
        hf = _FakeHashFile(hashes=_mk_hashes("01HG-RUN-A", "2026-04-21", 2))
        clock = _FakeClock(iso_values=["2099-12-31T23:59:59+00:00"])

        result = deliver_tab(
            run_state=rs,
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            hash_file=hf,
        )
        assert result.envelope.assembled_at_iso == "2099-12-31T23:59:59+00:00"
        assert result.written_at_iso == "2099-12-31T23:59:59+00:00"

    def test_final_n_derived_from_iteration_count(self) -> None:
        # iter_count = 3 → final_N = 3.
        rs = _mk_run_state(iter_count=3)
        vault = _FakeVault()
        hf = _FakeHashFile(hashes=_mk_hashes("01HG-RUN-A", "2026-04-21", 3))

        deliver_tab(
            run_state=rs,
            vault_read=vault.read,
            vault_write=vault.write,
            clock=_FakeClock(),
            hash_file=hf,
        )
        assert any(
            "iter_3/scribe_draft.md" in p for p in hf.seen
        ), hf.seen

    def test_canonical_bytes_deterministic(self) -> None:
        rs = _mk_run_state()
        vault = _FakeVault()
        hf = _FakeHashFile(hashes=_mk_hashes("01HG-RUN-A", "2026-04-21", 2))

        result = deliver_tab(
            run_state=rs,
            vault_read=vault.read,
            vault_write=vault.write,
            clock=_FakeClock(),
            hash_file=hf,
        )
        a = _canonical_bytes(result.envelope)
        b = _canonical_bytes(result.envelope)
        assert a == b
        # And: canonical bytes sort keys → ordering-independent dict.
        payload = json.loads(a.decode("utf-8"))
        assert list(payload.keys()) == sorted(payload.keys())

    def test_reexport_surface_resolves(self) -> None:
        # Re-export lives at pipeline.loop.__init__.
        from pipeline.loop import deliver_tab as dt, TabSigningResult as TSR
        from pipeline.loop import HashFileCallable as HFC

        assert dt is deliver_tab
        assert TSR is TabSigningResult
        assert HFC is HashFileCallable
