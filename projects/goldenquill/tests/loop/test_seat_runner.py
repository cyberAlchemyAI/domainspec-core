"""Tests for pipeline.loop.seat_runner — §4.3/§4.4/§4.5 invoke_seat (Round 4).

Blueprint §5 v6 LOCKED 2026-04-19.

Covers the spec card's test surface:

- invoke_scribe / invoke_editor / invoke_judge happy paths (level 0).
- Timeout → cascade advance; multi-timeout exhaustion raises F_PIPE_06.
- Cross-family collision at start level → skip + advance.
- Pure cross-family exhaustion → F_PIPE_08 (never observed a timeout).
- Judge three-way cross-family (scribe-family and editor-family forbidden).
- Judge parse failure → F_PIPE_09 with ``judge_parse_failed`` trigger.
- Minimal-env contract (A-v1-13): exactly the 6 whitelisted keys.
- Timeout constants pinned as inline literals at dispatch.
- ProviderCascade returned fresh (``cascade is not cascade_after``).
- Family recording: landed_family from subprocess, not charter.primary.
- Thin wrappers (``invoke_scribe`` / ``invoke_editor`` / ``invoke_judge``)
  pin ``seat_kind`` correctly.
- ValueError surface for mismatched seat_kind / charter / cascade /
  iteration_number.

Adversarial and out-of-scope surfaces live in ``test_adv_seat_runner.py``.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

import pytest

from pipeline.loop.errors import F_PIPE_06, F_PIPE_08, F_PIPE_09
from pipeline.loop.seat_runner import (
    MINIMAL_ENV_ALLOWED_KEYS,
    JudgeParseCallable,
    SeatInvocationContext,
    SeatInvocationResult,
    SubprocessLauncher,
    SubprocessResult,
    default_judge_parse,
    invoke_editor,
    invoke_judge,
    invoke_scribe,
    invoke_seat,
)
from pipeline.loop.types import ProviderCascade, RunState, SeatCharter


# ---------------------------------------------------------------------------
# Fakes
# ---------------------------------------------------------------------------


@dataclass
class _FakeLauncher:
    """Injectable :class:`SubprocessLauncher` double.

    ``queue`` is popped left-to-right, one result per call. If empty a
    default success is returned. All calls are recorded in ``calls`` for
    assertion.
    """

    queue: list[SubprocessResult] = field(default_factory=list)
    calls: list[dict[str, Any]] = field(default_factory=list)
    default_stdout: bytes = b'{"ok": true}'

    def __call__(
        self,
        *,
        seat_kind: str,
        env: dict[str, str],
        stdin_payload: bytes,
        timeout_ms: int,
        family: str,
        model_id: str,
    ) -> SubprocessResult:
        self.calls.append(
            {
                "seat_kind": seat_kind,
                "env": dict(env),
                "stdin_payload": stdin_payload,
                "timeout_ms": timeout_ms,
                "family": family,
                "model_id": model_id,
            }
        )
        if self.queue:
            return self.queue.pop(0)
        return SubprocessResult(
            exit_code=0,
            stdout=self.default_stdout,
            stderr=b"",
            timed_out=False,
            landed_family=family,
            landed_model_id=model_id,
        )


# ---------------------------------------------------------------------------
# Fixture builders
# ---------------------------------------------------------------------------


def _run_state(
    *,
    run_id: str = "run-abc",
    session_id: str = "sess-xyz",
    org_slug: str = "org-fitfarms",
    phase: str = "inner_loop_iter_1",
    families: dict[str, tuple[str, str]] | None = None,
) -> RunState:
    rs = RunState(
        schema_version=2,
        run_id=run_id,
        mode="submission",
        rfa_hash="rfa-hash-01",
        project_context_hash="pc-hash-01",
        golden_set_ref=None,
        org_slug=org_slug,
        session_id=session_id,
        phase=phase,
    )
    if families:
        rs.run_iteration_families_so_far.update(families)
    return rs


def _charter(
    seat_kind: str,
    *,
    allowed: frozenset[str] = frozenset({"anthropic", "google", "openai"}),
    primary_model: str = "primary-model",
) -> SeatCharter:
    return SeatCharter(
        seat_kind=seat_kind,
        allowed_families=allowed,
        primary_model=primary_model,
        cascade_level=0,
        subprocess_timeout_ms=180_000,
    )


def _cascade(
    seat_kind: str,
    *,
    levels: tuple[tuple[str, str], ...] = (
        ("anthropic", "claude-opus-4-7"),
        ("google", "gemini-2.5-pro"),
        ("openai", "gpt-5"),
    ),
    current_level: int = 0,
) -> ProviderCascade:
    return ProviderCascade(
        seat_kind=seat_kind,
        levels=levels,
        current_level=current_level,
    )


def _context(
    *,
    stdin_payload: bytes = b"{}",
    session_id: str = "sess-xyz",
    path_value: str = "/usr/bin:/bin",
    home_value: str = "/home/tilth",
) -> SeatInvocationContext:
    return SeatInvocationContext(
        stdin_payload=stdin_payload,
        session_id=session_id,
        path_value=path_value,
        home_value=home_value,
    )


# ---------------------------------------------------------------------------
# Happy paths
# ---------------------------------------------------------------------------


class TestHappyPaths:
    def test_scribe_level_0_success(self) -> None:
        rs = _run_state()
        launcher = _FakeLauncher()
        result = invoke_scribe(
            run_state=rs,
            iteration_number=1,
            charter=_charter("scribe"),
            cascade=_cascade("scribe"),
            context=_context(),
            subprocess_launcher=launcher,
        )
        assert isinstance(result, SeatInvocationResult)
        assert result.landed_family == "anthropic"
        assert result.landed_model_id == "claude-opus-4-7"
        assert result.level_advances == 0
        assert result.cascade_after.current_level == 0
        assert result.judge_verdict is None
        assert len(launcher.calls) == 1
        assert launcher.calls[0]["seat_kind"] == "scribe"

    def test_editor_level_0_success_cross_family_clear(self) -> None:
        rs = _run_state(
            families={"scribe": ("anthropic", "claude-opus-4-7")},
        )
        cascade = _cascade(
            "editor",
            levels=(
                ("google", "gemini-2.5-pro"),
                ("openai", "gpt-5"),
            ),
        )
        launcher = _FakeLauncher()
        result = invoke_editor(
            run_state=rs,
            iteration_number=1,
            charter=_charter("editor"),
            cascade=cascade,
            context=_context(),
            subprocess_launcher=launcher,
        )
        assert result.landed_family == "google"
        assert result.level_advances == 0
        assert launcher.calls[0]["seat_kind"] == "editor"

    def test_judge_level_0_success_with_default_parse(self) -> None:
        rs = _run_state(
            families={
                "scribe": ("anthropic", "claude-opus-4-7"),
                "editor": ("google", "gemini-2.5-pro"),
            },
        )
        cascade = _cascade(
            "judge",
            levels=(
                ("openai", "gpt-5"),
                ("meta", "llama-3.1-405b"),
            ),
        )
        payload = {"score": 87.0, "notes": "solid"}
        stdout = json.dumps(payload).encode("utf-8")
        launcher = _FakeLauncher(default_stdout=stdout)
        result = invoke_judge(
            run_state=rs,
            iteration_number=1,
            charter=_charter("judge"),
            cascade=cascade,
            context=_context(),
            subprocess_launcher=launcher,
        )
        assert result.landed_family == "openai"
        assert result.judge_verdict == payload
        assert result.output_hash == hashlib.sha256(stdout).hexdigest()

    def test_output_hash_is_sha256_of_stdout(self) -> None:
        rs = _run_state()
        stdout = b"\x00\x01deterministic\x02\x03"
        launcher = _FakeLauncher(default_stdout=stdout)
        result = invoke_scribe(
            run_state=rs,
            iteration_number=1,
            charter=_charter("scribe"),
            cascade=_cascade("scribe"),
            context=_context(),
            subprocess_launcher=launcher,
        )
        assert result.output_hash == hashlib.sha256(stdout).hexdigest()

    def test_raw_stdout_carries_subprocess_bytes_verbatim(self) -> None:
        """R4 micro-amend: Round 5 needs raw bytes for vault draft persistence."""
        rs = _run_state()
        stdout = b"scribe draft bytes \xe2\x98\x83 with non-ascii"
        launcher = _FakeLauncher(default_stdout=stdout)
        result = invoke_scribe(
            run_state=rs,
            iteration_number=1,
            charter=_charter("scribe"),
            cascade=_cascade("scribe"),
            context=_context(),
            subprocess_launcher=launcher,
        )
        assert result.raw_stdout == stdout
        assert result.output_hash == hashlib.sha256(result.raw_stdout).hexdigest()


# ---------------------------------------------------------------------------
# Cascade advance & exhaustion
# ---------------------------------------------------------------------------


def _timeout_result(*, family: str, model_id: str) -> SubprocessResult:
    return SubprocessResult(
        exit_code=137,
        stdout=b"",
        stderr=b"SIGKILL",
        timed_out=True,
        landed_family=family,
        landed_model_id=model_id,
    )


class TestCascadeAdvance:
    def test_level_0_timeout_level_1_success(self) -> None:
        rs = _run_state()
        cascade = _cascade(
            "scribe",
            levels=(
                ("anthropic", "claude-opus-4-7"),
                ("google", "gemini-2.5-pro"),
                ("openai", "gpt-5"),
            ),
        )
        launcher = _FakeLauncher(
            queue=[_timeout_result(family="anthropic", model_id="claude-opus-4-7")],
        )
        result = invoke_scribe(
            run_state=rs,
            iteration_number=1,
            charter=_charter("scribe"),
            cascade=cascade,
            context=_context(),
            subprocess_launcher=launcher,
        )
        assert result.level_advances == 1
        assert result.cascade_after.current_level == 1
        assert result.landed_family == "google"
        assert len(launcher.calls) == 2

    def test_all_levels_timeout_raises_f_pipe_06(self) -> None:
        rs = _run_state()
        levels = (
            ("anthropic", "claude-opus-4-7"),
            ("google", "gemini-2.5-pro"),
            ("openai", "gpt-5"),
        )
        launcher = _FakeLauncher(
            queue=[_timeout_result(family=f, model_id=m) for f, m in levels],
        )
        with pytest.raises(F_PIPE_06) as exc_info:
            invoke_scribe(
                run_state=rs,
                iteration_number=1,
                charter=_charter("scribe"),
                cascade=_cascade("scribe", levels=levels),
                context=_context(),
                subprocess_launcher=launcher,
            )
        assert exc_info.value.trigger == "cascade_exhausted"
        assert exc_info.value.details["seat_kind"] == "scribe"
        assert exc_info.value.details["exhausted_at_level"] == len(levels)
        assert len(launcher.calls) == len(levels)

    def test_cascade_starts_from_current_level(self) -> None:
        rs = _run_state()
        cascade = _cascade(
            "scribe",
            levels=(
                ("anthropic", "m0"),
                ("google", "m1"),
                ("openai", "m2"),
            ),
            current_level=2,
        )
        launcher = _FakeLauncher()
        result = invoke_scribe(
            run_state=rs,
            iteration_number=1,
            charter=_charter("scribe"),
            cascade=cascade,
            context=_context(),
            subprocess_launcher=launcher,
        )
        assert len(launcher.calls) == 1
        assert launcher.calls[0]["family"] == "openai"
        assert result.cascade_after.current_level == 2
        assert result.level_advances == 0

    def test_cascade_after_is_fresh_instance_on_advance(self) -> None:
        rs = _run_state()
        cascade = _cascade("scribe")
        launcher = _FakeLauncher(
            queue=[_timeout_result(family="anthropic", model_id="claude-opus-4-7")],
        )
        result = invoke_scribe(
            run_state=rs,
            iteration_number=1,
            charter=_charter("scribe"),
            cascade=cascade,
            context=_context(),
            subprocess_launcher=launcher,
        )
        assert result.cascade_after is not cascade
        assert cascade.current_level == 0
        assert result.cascade_after.current_level == 1


# ---------------------------------------------------------------------------
# Cross-family collision paths
# ---------------------------------------------------------------------------


class TestCrossFamily:
    def test_editor_level_0_collides_with_scribe_skips_to_level_1(self) -> None:
        rs = _run_state(
            families={"scribe": ("anthropic", "claude-opus-4-7")},
        )
        cascade = _cascade(
            "editor",
            levels=(
                ("anthropic", "sonnet-4-6"),
                ("google", "gemini-2.5-pro"),
            ),
        )
        launcher = _FakeLauncher()
        result = invoke_editor(
            run_state=rs,
            iteration_number=1,
            charter=_charter("editor"),
            cascade=cascade,
            context=_context(),
            subprocess_launcher=launcher,
        )
        assert result.landed_family == "google"
        assert result.level_advances == 1
        assert [c["family"] for c in launcher.calls] == ["google"]

    def test_editor_pure_collision_exhaustion_raises_f_pipe_08(self) -> None:
        rs = _run_state(
            families={"scribe": ("anthropic", "claude-opus-4-7")},
        )
        cascade = _cascade(
            "editor",
            levels=(
                ("anthropic", "sonnet-4-6"),
                ("anthropic", "haiku-4-5"),
            ),
        )
        launcher = _FakeLauncher()
        with pytest.raises(F_PIPE_08) as exc_info:
            invoke_editor(
                run_state=rs,
                iteration_number=1,
                charter=_charter("editor"),
                cascade=cascade,
                context=_context(),
                subprocess_launcher=launcher,
            )
        assert exc_info.value.trigger == "same_family_as_scribe"
        assert exc_info.value.details["scribe_family"] == "anthropic"
        assert launcher.calls == []

    def test_judge_three_way_collision_exhaustion(self) -> None:
        rs = _run_state(
            families={
                "scribe": ("anthropic", "claude-opus-4-7"),
                "editor": ("google", "gemini-2.5-pro"),
            },
        )
        cascade = _cascade(
            "judge",
            levels=(
                ("anthropic", "sonnet-4-6"),
                ("google", "gemini-flash-3"),
            ),
        )
        launcher = _FakeLauncher()
        with pytest.raises(F_PIPE_08) as exc_info:
            invoke_judge(
                run_state=rs,
                iteration_number=1,
                charter=_charter("judge"),
                cascade=cascade,
                context=_context(),
                subprocess_launcher=launcher,
            )
        assert exc_info.value.trigger == "same_family_as_scribe_or_editor"
        assert launcher.calls == []

    def test_judge_skips_past_scribe_and_editor_families(self) -> None:
        rs = _run_state(
            families={
                "scribe": ("anthropic", "claude-opus-4-7"),
                "editor": ("google", "gemini-2.5-pro"),
            },
        )
        cascade = _cascade(
            "judge",
            levels=(
                ("anthropic", "sonnet-4-6"),
                ("google", "flash"),
                ("openai", "gpt-5"),
            ),
        )
        launcher = _FakeLauncher(default_stdout=b'{"score": 90.0}')
        result = invoke_judge(
            run_state=rs,
            iteration_number=1,
            charter=_charter("judge"),
            cascade=cascade,
            context=_context(),
            subprocess_launcher=launcher,
        )
        assert result.landed_family == "openai"
        assert result.level_advances == 2
        assert [c["family"] for c in launcher.calls] == ["openai"]

    def test_scribe_never_collides_even_if_families_populated(self) -> None:
        rs = _run_state(
            families={"scribe": ("anthropic", "prev")},
        )
        launcher = _FakeLauncher()
        result = invoke_scribe(
            run_state=rs,
            iteration_number=2,
            charter=_charter("scribe"),
            cascade=_cascade("scribe"),
            context=_context(),
            subprocess_launcher=launcher,
        )
        assert result.level_advances == 0
        assert launcher.calls[0]["family"] == "anthropic"


# ---------------------------------------------------------------------------
# Mixed timeout + collision classification
# ---------------------------------------------------------------------------


class TestMixedExhaustion:
    def test_timeout_then_collision_still_advances_to_success(self) -> None:
        rs = _run_state(
            families={"scribe": ("google", "g1")},
        )
        cascade = _cascade(
            "editor",
            levels=(
                ("anthropic", "a1"),
                ("google", "g2"),
                ("openai", "o1"),
            ),
        )
        launcher = _FakeLauncher(
            queue=[_timeout_result(family="anthropic", model_id="a1")],
        )
        result = invoke_editor(
            run_state=rs,
            iteration_number=1,
            charter=_charter("editor"),
            cascade=cascade,
            context=_context(),
            subprocess_launcher=launcher,
        )
        assert result.landed_family == "openai"
        assert result.level_advances == 2
        assert [c["family"] for c in launcher.calls] == ["anthropic", "openai"]

    def test_timeout_then_collision_exhaustion_raises_f_pipe_06(self) -> None:
        rs = _run_state(
            families={"scribe": ("google", "g1")},
        )
        cascade = _cascade(
            "editor",
            levels=(
                ("anthropic", "a1"),
                ("google", "g2"),
            ),
        )
        launcher = _FakeLauncher(
            queue=[_timeout_result(family="anthropic", model_id="a1")],
        )
        with pytest.raises(F_PIPE_06) as exc_info:
            invoke_editor(
                run_state=rs,
                iteration_number=1,
                charter=_charter("editor"),
                cascade=cascade,
                context=_context(),
                subprocess_launcher=launcher,
            )
        assert exc_info.value.trigger == "cascade_exhausted"


# ---------------------------------------------------------------------------
# Judge parse
# ---------------------------------------------------------------------------


class TestJudgeParse:
    def test_default_parser_accepts_non_empty_object(self) -> None:
        assert default_judge_parse(b'{"x": 1}') == {"x": 1}

    def test_default_parser_rejects_list(self) -> None:
        with pytest.raises(ValueError):
            default_judge_parse(b"[1, 2, 3]")

    def test_default_parser_rejects_empty_object(self) -> None:
        with pytest.raises(ValueError):
            default_judge_parse(b"{}")

    def test_default_parser_rejects_malformed_json(self) -> None:
        with pytest.raises(ValueError):
            default_judge_parse(b"not json at all")

    def test_judge_parse_failure_raises_f_pipe_09(self) -> None:
        rs = _run_state(
            families={
                "scribe": ("anthropic", "a1"),
                "editor": ("google", "g1"),
            },
        )
        launcher = _FakeLauncher(default_stdout=b"definitely not json")
        with pytest.raises(F_PIPE_09) as exc_info:
            invoke_judge(
                run_state=rs,
                iteration_number=1,
                charter=_charter("judge"),
                cascade=_cascade("judge", levels=(("openai", "gpt-5"),)),
                context=_context(),
                subprocess_launcher=launcher,
            )
        assert exc_info.value.trigger == "judge_parse_failed"
        assert exc_info.value.details["landed_family"] == "openai"
        assert "parser_error" in exc_info.value.details

    def test_judge_custom_parser_injected(self) -> None:
        rs = _run_state(
            families={
                "scribe": ("anthropic", "a1"),
                "editor": ("google", "g1"),
            },
        )
        captured: list[bytes] = []

        def custom_parser(stdout: bytes) -> dict[str, Any]:
            captured.append(stdout)
            return {"verdict": "custom"}

        launcher = _FakeLauncher(default_stdout=b"arbitrary bytes")
        result = invoke_judge(
            run_state=rs,
            iteration_number=1,
            charter=_charter("judge"),
            cascade=_cascade("judge", levels=(("openai", "gpt-5"),)),
            context=_context(),
            subprocess_launcher=launcher,
            judge_parse=custom_parser,
        )
        assert captured == [b"arbitrary bytes"]
        assert result.judge_verdict == {"verdict": "custom"}

    def test_scribe_and_editor_do_not_invoke_parser(self) -> None:
        rs = _run_state()

        def explode(_: bytes) -> dict[str, Any]:
            raise AssertionError("parser must not be called for non-judge seats")

        launcher = _FakeLauncher()
        result = invoke_scribe(
            run_state=rs,
            iteration_number=1,
            charter=_charter("scribe"),
            cascade=_cascade("scribe"),
            context=_context(),
            subprocess_launcher=launcher,
            judge_parse=explode,
        )
        assert result.judge_verdict is None


# ---------------------------------------------------------------------------
# Minimal-env contract (A-v1-13)
# ---------------------------------------------------------------------------


class TestMinimalEnv:
    def test_env_passed_to_launcher_has_exactly_six_keys(self) -> None:
        rs = _run_state(
            run_id="RUN-001", session_id="SES-002", org_slug="org-fitfarms"
        )
        launcher = _FakeLauncher()
        invoke_scribe(
            run_state=rs,
            iteration_number=1,
            charter=_charter("scribe"),
            cascade=_cascade("scribe"),
            context=_context(
                session_id="SES-002", path_value="/P", home_value="/H"
            ),
            subprocess_launcher=launcher,
        )
        env = launcher.calls[0]["env"]
        assert set(env.keys()) == MINIMAL_ENV_ALLOWED_KEYS
        assert env == {
            "PATH": "/P",
            "HOME": "/H",
            "TILTH_SESSION_ID": "SES-002",
            "TILTH_RUN_ID": "RUN-001",
            "TILTH_ORG_SLUG": "org-fitfarms",
            "TILTH_SEAT_KIND": "scribe",
        }

    def test_env_has_no_host_secrets(self) -> None:
        rs = _run_state()
        launcher = _FakeLauncher()
        invoke_editor(
            run_state=rs,
            iteration_number=1,
            charter=_charter("editor"),
            cascade=_cascade("editor"),
            context=_context(),
            subprocess_launcher=launcher,
        )
        env = launcher.calls[0]["env"]
        forbidden_prefixes = ("ANTHROPIC_", "OPENAI_", "GOOGLE_", "GROQ_")
        for key in env:
            assert not key.startswith(forbidden_prefixes)

    def test_minimal_env_allowed_keys_is_frozen_set_of_six(self) -> None:
        assert isinstance(MINIMAL_ENV_ALLOWED_KEYS, frozenset)
        assert len(MINIMAL_ENV_ALLOWED_KEYS) == 6


# ---------------------------------------------------------------------------
# Timeout constants pinned at dispatch
# ---------------------------------------------------------------------------


class TestTimeoutConstants:
    def test_scribe_timeout_is_300_000_ms(self) -> None:
        rs = _run_state()
        launcher = _FakeLauncher()
        invoke_scribe(
            run_state=rs,
            iteration_number=1,
            charter=_charter("scribe"),
            cascade=_cascade("scribe"),
            context=_context(),
            subprocess_launcher=launcher,
        )
        assert launcher.calls[0]["timeout_ms"] == 300_000

    def test_editor_timeout_is_180_000_ms(self) -> None:
        rs = _run_state()
        launcher = _FakeLauncher()
        invoke_editor(
            run_state=rs,
            iteration_number=1,
            charter=_charter("editor"),
            cascade=_cascade("editor"),
            context=_context(),
            subprocess_launcher=launcher,
        )
        assert launcher.calls[0]["timeout_ms"] == 180_000

    def test_judge_timeout_is_180_000_ms(self) -> None:
        rs = _run_state(
            families={
                "scribe": ("anthropic", "a1"),
                "editor": ("google", "g1"),
            },
        )
        launcher = _FakeLauncher(default_stdout=b'{"v": 1}')
        invoke_judge(
            run_state=rs,
            iteration_number=1,
            charter=_charter("judge"),
            cascade=_cascade("judge", levels=(("openai", "gpt-5"),)),
            context=_context(),
            subprocess_launcher=launcher,
        )
        assert launcher.calls[0]["timeout_ms"] == 180_000


# ---------------------------------------------------------------------------
# Family recording (A-v1-02: subprocess is source of truth)
# ---------------------------------------------------------------------------


class TestFamilyRecording:
    def test_landed_family_comes_from_subprocess_result(self) -> None:
        rs = _run_state()
        launcher = _FakeLauncher(
            queue=[
                SubprocessResult(
                    exit_code=0,
                    stdout=b'{"ok": true}',
                    stderr=b"",
                    timed_out=False,
                    landed_family="meta",
                    landed_model_id="llama-3.1-405b",
                )
            ],
        )
        result = invoke_scribe(
            run_state=rs,
            iteration_number=1,
            charter=_charter("scribe"),
            cascade=_cascade("scribe"),
            context=_context(),
            subprocess_launcher=launcher,
        )
        assert result.landed_family == "meta"
        assert result.landed_model_id == "llama-3.1-405b"


# ---------------------------------------------------------------------------
# Thin wrappers
# ---------------------------------------------------------------------------


class TestThinWrappers:
    def test_invoke_scribe_pins_seat_kind(self) -> None:
        rs = _run_state()
        launcher = _FakeLauncher()
        invoke_scribe(
            run_state=rs,
            iteration_number=1,
            charter=_charter("scribe"),
            cascade=_cascade("scribe"),
            context=_context(),
            subprocess_launcher=launcher,
        )
        assert launcher.calls[0]["seat_kind"] == "scribe"

    def test_invoke_editor_pins_seat_kind(self) -> None:
        rs = _run_state()
        launcher = _FakeLauncher()
        invoke_editor(
            run_state=rs,
            iteration_number=1,
            charter=_charter("editor"),
            cascade=_cascade("editor"),
            context=_context(),
            subprocess_launcher=launcher,
        )
        assert launcher.calls[0]["seat_kind"] == "editor"

    def test_invoke_judge_pins_seat_kind(self) -> None:
        rs = _run_state(
            families={
                "scribe": ("anthropic", "a1"),
                "editor": ("google", "g1"),
            },
        )
        launcher = _FakeLauncher(default_stdout=b'{"x": 1}')
        invoke_judge(
            run_state=rs,
            iteration_number=1,
            charter=_charter("judge"),
            cascade=_cascade("judge", levels=(("openai", "gpt-5"),)),
            context=_context(),
            subprocess_launcher=launcher,
        )
        assert launcher.calls[0]["seat_kind"] == "judge"


# ---------------------------------------------------------------------------
# Validation surface
# ---------------------------------------------------------------------------


class TestValidation:
    def test_unknown_seat_kind_raises_value_error(self) -> None:
        rs = _run_state()
        with pytest.raises(ValueError, match="seat_kind"):
            invoke_seat(
                seat_kind="poet",  # type: ignore[arg-type]
                run_state=rs,
                iteration_number=1,
                charter=_charter("scribe"),
                cascade=_cascade("scribe"),
                context=_context(),
                subprocess_launcher=_FakeLauncher(),
            )

    def test_charter_seat_kind_mismatch_raises_value_error(self) -> None:
        rs = _run_state()
        with pytest.raises(ValueError, match="charter.seat_kind"):
            invoke_seat(
                seat_kind="scribe",
                run_state=rs,
                iteration_number=1,
                charter=_charter("editor"),
                cascade=_cascade("scribe"),
                context=_context(),
                subprocess_launcher=_FakeLauncher(),
            )

    def test_cascade_seat_kind_mismatch_raises_value_error(self) -> None:
        rs = _run_state()
        with pytest.raises(ValueError, match="cascade.seat_kind"):
            invoke_seat(
                seat_kind="scribe",
                run_state=rs,
                iteration_number=1,
                charter=_charter("scribe"),
                cascade=_cascade("editor"),
                context=_context(),
                subprocess_launcher=_FakeLauncher(),
            )

    def test_iteration_number_zero_raises_value_error(self) -> None:
        rs = _run_state()
        with pytest.raises(ValueError, match="iteration_number"):
            invoke_scribe(
                run_state=rs,
                iteration_number=0,
                charter=_charter("scribe"),
                cascade=_cascade("scribe"),
                context=_context(),
                subprocess_launcher=_FakeLauncher(),
            )


# ---------------------------------------------------------------------------
# Structural sanity
# ---------------------------------------------------------------------------


class TestStructural:
    def test_subprocess_launcher_is_runtime_checkable_protocol(self) -> None:
        launcher = _FakeLauncher()
        assert isinstance(launcher, SubprocessLauncher)

    def test_judge_parse_callable_is_runtime_checkable(self) -> None:
        def parse(stdout: bytes) -> dict[str, Any]:
            return {}

        assert isinstance(parse, JudgeParseCallable)

    def test_seat_invocation_context_is_frozen(self) -> None:
        ctx = _context()
        with pytest.raises(Exception):
            ctx.session_id = "mutated"  # type: ignore[misc]

    def test_seat_invocation_result_is_frozen(self) -> None:
        rs = _run_state()
        launcher = _FakeLauncher()
        result = invoke_scribe(
            run_state=rs,
            iteration_number=1,
            charter=_charter("scribe"),
            cascade=_cascade("scribe"),
            context=_context(),
            subprocess_launcher=launcher,
        )
        with pytest.raises(Exception):
            result.output_hash = "mutated"  # type: ignore[misc]
