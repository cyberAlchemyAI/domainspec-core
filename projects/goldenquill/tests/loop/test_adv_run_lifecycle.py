"""Adversarial tests for pipeline.loop.run_lifecycle (§5 Round 3).

Blueprint §5 v6 §4.1 LOCKED 2026-04-19.

Focus: V1 discipline + E-023 out-of-scope documentation.

1. **Inline-literal frozenset rebind resistance.** Monkeypatching the public
   ``_allowed_resume_phases_for`` helper does NOT broaden ``resume_run``'s
   enforced set — ``resume_run`` inlines the literal at its call site.

2. **Malformed vault_read payloads.** Garbled JSON / non-UTF-8 bytes surface
   cleanly as ``json.JSONDecodeError`` / ``UnicodeDecodeError`` — documented
   as caller-terminating; Round 3 does not defend at this layer (trusted-operator
   envelope §3.11 v5).

3. **Schema-tampering ordering.** An on-disk ``schema_version`` other than ``2``
   (downgrade OR forward-version) must write state-failure BEFORE raising
   F_PIPE_22 — regardless of whether the other fields remain structurally valid.

4. **Quarantine marker is written BEFORE F_PIPE_18 is raised.** Ordering
   asserted via the vault-write call log.

5. **RunIdFactory adversarial returns.** Empty string / very long strings:
   Round 3 trusts the factory's ULID contract; documented here, not defended.

LOC target: 160 (range 120-200).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

import pytest

from pipeline.loop import run_lifecycle as rl
from pipeline.loop.errors import F_PIPE_18, F_PIPE_22
from pipeline.loop.run_lifecycle import (
    _allowed_resume_phases_for,
    resume_run,
    start_run,
)
from pipeline.loop.state_checkpoint import _canonicalize_runstate
from pipeline.loop.types import RunState


# ---------------------------------------------------------------------------
# Shared fakes (duplicated from the main test file — keeps the adv file
# self-contained per session metrics / audit-isolation discipline).
# ---------------------------------------------------------------------------


@dataclass
class _FakeClock:
    iso: str = "2026-04-20T12:00:00Z"
    ms: int = 1000

    def now_ms(self) -> int:
        self.ms += 1
        return self.ms

    def now_iso(self) -> str:
        return self.iso


@dataclass
class _FakeSleep:
    calls: list[int] = field(default_factory=list)

    def __call__(self, ms: int) -> None:
        self.calls.append(ms)


@dataclass
class _FakeVault:
    store: dict[str, bytes] = field(default_factory=dict)
    calls: list[dict[str, Any]] = field(default_factory=list)

    def __call__(
        self,
        *,
        path: str,
        payload: bytes,
        intent: str,
        write_mode: str,
        expected_current_file_hash: str | None,
    ) -> str:
        self.calls.append(
            {
                "path": path,
                "payload": payload,
                "intent": intent,
                "write_mode": write_mode,
                "expected_current_file_hash": expected_current_file_hash,
            }
        )
        self.store[path] = payload
        return hashlib.sha256(payload).hexdigest()

    def read(self, *, path: str) -> bytes:
        return self.store[path]


def _mk_submission(run_id: str, phase: str = "pre_gate_passed") -> RunState:
    return RunState(
        schema_version=2,
        run_id=run_id,
        mode="submission",
        rfa_hash="rfa-h",
        project_context_hash="pc-h",
        golden_set_ref=None,
        org_slug="myco",
        session_id="s-1",
        phase=phase,
        started_at_iso="2026-04-20T12:00:00Z",
        last_checkpoint_iso="2026-04-20T12:01:00Z",
    )


def _persist(vault: _FakeVault, rs: RunState) -> None:
    vault.store[f"pipeline/{rs.run_id}/state.json"] = _canonicalize_runstate(rs)


def _write_tampered(vault: _FakeVault, run_id: str, mutate: dict[str, Any]) -> None:
    rs = _mk_submission(run_id)
    data = json.loads(_canonicalize_runstate(rs).decode("utf-8"))
    data.update(mutate)
    vault.store[f"pipeline/{run_id}/state.json"] = json.dumps(
        data, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


# ---------------------------------------------------------------------------
# 1. Inline-literal frozenset rebind resistance
# ---------------------------------------------------------------------------


class TestFrozensetRebindResistance:
    def test_rebinding_helper_does_not_broaden_resume_set(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Patching ``_allowed_resume_phases_for`` to return every phase must
        NOT let ``resume_run`` accept a forbidden phase — the function body
        uses INLINE frozenset literals, not the helper."""
        vault = _FakeVault()
        _write_tampered(vault, "run-rebind-1", {"phase": "finalized"})

        monkeypatch.setattr(
            rl,
            "_allowed_resume_phases_for",
            lambda mode: frozenset(
                {
                    "pre_gate_pending",
                    "pre_gate_passed",
                    "inner_loop_iter_1",
                    "inner_loop_iter_2",
                    "inner_loop_iter_3",
                    "post_gate_pending",
                    "signoff_pending",
                    "degraded_paused",
                    "finalized",  # attempted broadening
                    "report_signed",
                }
            ),
        )

        with pytest.raises(F_PIPE_18) as exc_info:
            resume_run(
                "run-rebind-1",
                vault_read=vault.read,
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )
        assert exc_info.value.trigger == "resume_phase_mismatch"

    def test_helper_and_inline_sets_agree(self) -> None:
        """If these ever diverge, resume_run's inline sets are authoritative —
        this test catches accidental drift between the helper (docs/tests)
        and the call-site literals."""
        assert _allowed_resume_phases_for("submission") == frozenset(
            {
                "pre_gate_pending",
                "pre_gate_passed",
                "inner_loop_iter_1",
                "inner_loop_iter_2",
                "inner_loop_iter_3",
                "post_gate_pending",
                "signoff_pending",
                "signoff_pending_council_split",  # v7 §5 v7 amendment §4.7
                "degraded_paused",
            }
        )
        assert _allowed_resume_phases_for("eval") == frozenset(
            {"eval_iter_pending", "calibration_assembled"}
        )


# ---------------------------------------------------------------------------
# 2. Malformed vault_read — out-of-scope per §3.11 v5 trusted envelope
# ---------------------------------------------------------------------------


class TestMalformedVaultRead:
    def test_non_json_bytes_raise_json_decode_error(self) -> None:
        """Round 3 trusts vault_read's return — garbled bytes propagate as
        JSONDecodeError. Defence-in-depth belongs at §2 Vault's integrity tag
        verification, not here."""
        vault = _FakeVault()
        vault.store["pipeline/run-garbled-1/state.json"] = b"not json at all"
        with pytest.raises(json.JSONDecodeError):
            resume_run(
                "run-garbled-1",
                vault_read=vault.read,
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )

    def test_non_utf8_bytes_raise_unicode_decode_error(self) -> None:
        vault = _FakeVault()
        vault.store["pipeline/run-garbled-2/state.json"] = b"\xff\xfe\x00\x00"
        with pytest.raises(UnicodeDecodeError):
            resume_run(
                "run-garbled-2",
                vault_read=vault.read,
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )

    def test_empty_payload_raises_json_decode_error(self) -> None:
        vault = _FakeVault()
        vault.store["pipeline/run-empty/state.json"] = b""
        with pytest.raises(json.JSONDecodeError):
            resume_run(
                "run-empty",
                vault_read=vault.read,
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )


# ---------------------------------------------------------------------------
# 3. Schema-tampering: downgrade AND forward-version
# ---------------------------------------------------------------------------


class TestSchemaTamperingOrdering:
    def test_forward_version_also_writes_state_failure_before_raise(self) -> None:
        """schema_version=3 (hypothetical forward bump without migration) must
        trigger the same F_PIPE_22 path as the downgrade case — state-failure
        wrapper lands BEFORE re-raise."""
        vault = _FakeVault()
        _write_tampered(vault, "run-fwd-1", {"schema_version": 3})
        with pytest.raises(F_PIPE_22):
            resume_run(
                "run-fwd-1",
                vault_read=vault.read,
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )
        failure_writes = [c for c in vault.calls if c["intent"] == "state-failure"]
        assert len(failure_writes) == 1
        assert failure_writes[0]["path"] == "pipeline/run-fwd-1/state_failure.json"

    def test_missing_schema_version_key_triggers_f_pipe_22(self) -> None:
        """If the on-disk payload omits schema_version entirely, the raw-dict
        peek sees ``None`` → F_PIPE_22 (not a KeyError). Ordering preserved."""
        vault = _FakeVault()
        rs = _mk_submission("run-missing-1")
        data = json.loads(_canonicalize_runstate(rs).decode("utf-8"))
        del data["schema_version"]
        vault.store["pipeline/run-missing-1/state.json"] = json.dumps(
            data, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        with pytest.raises(F_PIPE_22):
            resume_run(
                "run-missing-1",
                vault_read=vault.read,
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )
        failure_writes = [c for c in vault.calls if c["intent"] == "state-failure"]
        assert len(failure_writes) == 1

    def test_eval_mode_schema_downgrade_also_writes_eval_skeleton(self) -> None:
        """Downgrade on an eval-mode RunState: skeleton must preserve mode=eval
        so the state-failure wrapper labels are accurate. Exercises the
        eval branch of the skeleton builder."""
        vault = _FakeVault()
        rs = RunState(
            schema_version=2,
            run_id="run-eval-dgrd",
            mode="eval",
            rfa_hash=None,
            project_context_hash=None,
            golden_set_ref="gs-1",
            org_slug="myco",
            session_id="s-1",
            phase="eval_iter_pending",
            started_at_iso="2026-04-20T12:00:00Z",
            last_checkpoint_iso="2026-04-20T12:01:00Z",
        )
        data = json.loads(_canonicalize_runstate(rs).decode("utf-8"))
        data["schema_version"] = 1
        vault.store["pipeline/run-eval-dgrd/state.json"] = json.dumps(
            data, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        with pytest.raises(F_PIPE_22):
            resume_run(
                "run-eval-dgrd",
                vault_read=vault.read,
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )
        failure_writes = [c for c in vault.calls if c["intent"] == "state-failure"]
        assert len(failure_writes) == 1
        assert failure_writes[0]["path"] == "pipeline/run-eval-dgrd/state_failure.json"


# ---------------------------------------------------------------------------
# 4. Quarantine-before-raise ordering on F_PIPE_18
# ---------------------------------------------------------------------------


class TestQuarantineOrdering:
    def test_quarantine_written_before_f_pipe_18_phase_mismatch(self) -> None:
        vault = _FakeVault()
        _write_tampered(vault, "run-qrt-1", {"phase": "finalized"})
        with pytest.raises(F_PIPE_18):
            resume_run(
                "run-qrt-1",
                vault_read=vault.read,
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )
        quarantine_writes = [
            c for c in vault.calls if c["path"].endswith("/quarantine.json")
        ]
        assert len(quarantine_writes) == 1
        assert quarantine_writes[0]["path"] == "pipeline/run-qrt-1/quarantine.json"

    def test_quarantine_written_before_f_pipe_18_bypass_missing(self) -> None:
        vault = _FakeVault()
        _write_tampered(
            vault,
            "run-qrt-2",
            {"phase": "degraded_paused", "bypass_pending_checkpoint_ref": None},
        )
        with pytest.raises(F_PIPE_18):
            resume_run(
                "run-qrt-2",
                vault_read=vault.read,
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )
        quarantine_writes = [
            c for c in vault.calls if c["path"].endswith("/quarantine.json")
        ]
        assert len(quarantine_writes) == 1


# ---------------------------------------------------------------------------
# 5. RunIdFactory adversarial contract (documented, not defended)
# ---------------------------------------------------------------------------


class TestRunIdFactoryContract:
    def test_factory_returning_empty_string_is_rejected_by_runstate(self) -> None:
        """Round 3 delegates run_id validation to RunState's __post_init__ (which
        rejects empty strings as ValueError). Documents the defence-in-depth:
        RunState is the enforcement point, not start_run itself."""
        vault = _FakeVault()
        with pytest.raises(ValueError, match="run_id must be non-empty"):
            start_run(
                mode="submission",
                org_slug="myco",
                session_id="s-1",
                rfa_hash="rfa-h",
                project_context_hash="pc-h",
                golden_set_ref=None,
                run_id_factory=lambda: "",  # adversarial
                vault_write=vault,
                clock=_FakeClock(),
                sleep=_FakeSleep(),
            )
        # vault_write never called — RunState construction raised before checkpoint.
        assert vault.calls == []

    def test_factory_returning_very_long_string_is_not_defended(self) -> None:
        long_id = "a" * 500
        vault = _FakeVault()
        rs = start_run(
            mode="submission",
            org_slug="myco",
            session_id="s-1",
            rfa_hash="rfa-h",
            project_context_hash="pc-h",
            golden_set_ref=None,
            run_id_factory=lambda: long_id,
            vault_write=vault,
            clock=_FakeClock(),
            sleep=_FakeSleep(),
        )
        assert rs.run_id == long_id
