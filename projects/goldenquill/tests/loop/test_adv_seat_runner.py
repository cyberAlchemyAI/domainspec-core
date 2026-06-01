"""Adversarial tests for pipeline.loop.seat_runner (Round 4).

Blueprint §5 v6 LOCKED 2026-04-19.

These tests harden Round 4's contract against subtle tampering / leakage
/ rebind attacks that the happy-path suite does not exercise by design:

1. **Rebind resistance.** :data:`pipeline.loop.config.SCRIBE/EDITOR/JUDGE
   _SUBPROCESS_TIMEOUT_MS` rebinds do NOT change invocation timeouts —
   the dispatch site uses inline literals.
2. **Minimal-env integrity.** :data:`pipeline.loop.seat_runner
   .MINIMAL_ENV_ALLOWED_KEYS` rebind cannot widen the actual env emitted
   to the launcher — :func:`_build_minimal_env` uses an inline-literal
   RHS in its set-equality check.
3. **Protocol-inputs-not-invoked pin (Round 4).** ``vault_write`` /
   ``clock`` / ``sleep`` arguments are reserved for Rounds 5 / 7;
   Round 4 MUST NOT invoke them. Test injects exploding doubles.
4. **Parser failure mode taxonomy.** Non-dict JSON, null, primitives,
   mutable exception types all wrap as :class:`F_PIPE_09` with
   ``judge_parse_failed``.
5. **Cause preservation (PEP-3134).** ``F_PIPE_09`` carries the parser's
   original exception as ``__cause__``.
6. **Cascade resumes from fresh current_level** across sequential calls.
7. **Scribe ignores run_iteration_families_so_far**: iter_2 Scribe
   collides with prior iter_1 scribe? NO — scribe never cross-checks.
8. **Thin wrappers are call-for-call equivalent to dispatcher.**
9. **Blueprint-hash pin.** BLUEPRINT_DEPS carries the v6 LOCKED hash
   prefix.

E-023 scope-authority documentation at the bottom lists out-of-scope
surfaces that are DELIBERATELY not defended at this layer.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

import pytest

from pipeline.loop import config as config_module
from pipeline.loop import seat_runner as seat_runner_module
from pipeline.loop.errors import F_PIPE_06, F_PIPE_09
from pipeline.loop.seat_runner import (
    BLUEPRINT_DEPS,
    MINIMAL_ENV_ALLOWED_KEYS,
    SeatInvocationContext,
    SubprocessResult,
    _build_minimal_env,
    default_judge_parse,
    invoke_editor,
    invoke_judge,
    invoke_scribe,
    invoke_seat,
)
from pipeline.loop.types import ProviderCascade, RunState, SeatCharter


# ---------------------------------------------------------------------------
# Shared helpers (mirror test_seat_runner.py; kept local for isolation)
# ---------------------------------------------------------------------------


@dataclass
class _FakeLauncher:
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


def _rs(
    *,
    families: dict[str, tuple[str, str]] | None = None,
) -> RunState:
    rs = RunState(
        schema_version=2,
        run_id="run-adv",
        mode="submission",
        rfa_hash="r1",
        project_context_hash="pc1",
        golden_set_ref=None,
        org_slug="org-adv",
        session_id="sess-adv",
        phase="inner_loop_iter_1",
    )
    if families:
        rs.run_iteration_families_so_far.update(families)
    return rs


def _ch(seat_kind: str) -> SeatCharter:
    return SeatCharter(
        seat_kind=seat_kind,
        allowed_families=frozenset({"anthropic", "google", "openai"}),
        primary_model="pri",
        cascade_level=0,
        subprocess_timeout_ms=180_000,
    )


def _cs(
    seat_kind: str,
    *,
    levels: tuple[tuple[str, str], ...] = (
        ("anthropic", "m0"),
        ("google", "m1"),
    ),
    current_level: int = 0,
) -> ProviderCascade:
    return ProviderCascade(
        seat_kind=seat_kind,
        levels=levels,
        current_level=current_level,
    )


def _ctx() -> SeatInvocationContext:
    return SeatInvocationContext(
        stdin_payload=b"{}",
        session_id="sess-adv",
        path_value="/p",
        home_value="/h",
    )


# ---------------------------------------------------------------------------
# 1. Timeout-constant rebind resistance
# ---------------------------------------------------------------------------


class TestAdvTimeoutRebindResistance:
    def test_rebind_scribe_timeout_does_not_affect_dispatch(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            config_module, "SCRIBE_SUBPROCESS_TIMEOUT_MS", 1, raising=True
        )
        launcher = _FakeLauncher()
        invoke_scribe(
            run_state=_rs(),
            iteration_number=1,
            charter=_ch("scribe"),
            cascade=_cs("scribe"),
            context=_ctx(),
            subprocess_launcher=launcher,
        )
        assert launcher.calls[0]["timeout_ms"] == 300_000

    def test_rebind_editor_timeout_does_not_affect_dispatch(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            config_module, "EDITOR_SUBPROCESS_TIMEOUT_MS", 9_999_999, raising=True
        )
        launcher = _FakeLauncher()
        invoke_editor(
            run_state=_rs(),
            iteration_number=1,
            charter=_ch("editor"),
            cascade=_cs("editor"),
            context=_ctx(),
            subprocess_launcher=launcher,
        )
        assert launcher.calls[0]["timeout_ms"] == 180_000

    def test_rebind_judge_timeout_does_not_affect_dispatch(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            config_module, "JUDGE_SUBPROCESS_TIMEOUT_MS", 1, raising=True
        )
        launcher = _FakeLauncher(default_stdout=b'{"ok": 1}')
        invoke_judge(
            run_state=_rs(
                families={
                    "scribe": ("anthropic", "a1"),
                    "editor": ("google", "g1"),
                }
            ),
            iteration_number=1,
            charter=_ch("judge"),
            cascade=_cs("judge", levels=(("openai", "gpt-5"),)),
            context=_ctx(),
            subprocess_launcher=launcher,
        )
        assert launcher.calls[0]["timeout_ms"] == 180_000


# ---------------------------------------------------------------------------
# 2. MINIMAL_ENV_ALLOWED_KEYS rebind resistance
# ---------------------------------------------------------------------------


class TestAdvMinimalEnvRebind:
    def test_rebind_minimal_env_allowed_keys_does_not_widen_runtime_env(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # Adversary widens the module attribute post-import.
        monkeypatch.setattr(
            seat_runner_module,
            "MINIMAL_ENV_ALLOWED_KEYS",
            frozenset(
                {
                    "PATH",
                    "HOME",
                    "TILTH_SESSION_ID",
                    "TILTH_RUN_ID",
                    "TILTH_ORG_SLUG",
                    "TILTH_SEAT_KIND",
                    "ANTHROPIC_API_KEY",
                    "GROQ_API_KEY",
                }
            ),
            raising=True,
        )
        launcher = _FakeLauncher()
        invoke_scribe(
            run_state=_rs(),
            iteration_number=1,
            charter=_ch("scribe"),
            cascade=_cs("scribe"),
            context=_ctx(),
            subprocess_launcher=launcher,
        )
        # Actual env still exactly the 6 whitelisted keys.
        assert set(launcher.calls[0]["env"].keys()) == {
            "PATH",
            "HOME",
            "TILTH_SESSION_ID",
            "TILTH_RUN_ID",
            "TILTH_ORG_SLUG",
            "TILTH_SEAT_KIND",
        }

    def test_build_minimal_env_smoke(self) -> None:
        env = _build_minimal_env(
            session_id="s",
            run_id="r",
            org_slug="o",
            seat_kind="scribe",
            path_value="/p",
            home_value="/h",
        )
        assert frozenset(env.keys()) == MINIMAL_ENV_ALLOWED_KEYS


# ---------------------------------------------------------------------------
# 3. Round-4-reserved Protocol inputs NOT invoked
# ---------------------------------------------------------------------------


class _ExplodingVaultWrite:
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        raise AssertionError("vault_write must NOT be invoked by Round 4")


class _ExplodingClock:
    def now(self) -> Any:
        raise AssertionError("clock.now must NOT be invoked by Round 4")

    def iso_now(self) -> Any:
        raise AssertionError("clock.iso_now must NOT be invoked by Round 4")


def _exploding_sleep(seconds: float) -> None:
    raise AssertionError("sleep must NOT be invoked by Round 4")


class TestAdvProtocolInputsNotInvoked:
    def test_vault_write_clock_sleep_not_called(self) -> None:
        rs = _rs()
        launcher = _FakeLauncher()
        result = invoke_scribe(
            run_state=rs,
            iteration_number=1,
            charter=_ch("scribe"),
            cascade=_cs("scribe"),
            context=_ctx(),
            subprocess_launcher=launcher,
            vault_write=_ExplodingVaultWrite(),  # type: ignore[arg-type]
            clock=_ExplodingClock(),  # type: ignore[arg-type]
            sleep=_exploding_sleep,
        )
        assert result.landed_family == "anthropic"

    def test_vault_write_clock_sleep_default_none(self) -> None:
        launcher = _FakeLauncher()
        invoke_scribe(
            run_state=_rs(),
            iteration_number=1,
            charter=_ch("scribe"),
            cascade=_cs("scribe"),
            context=_ctx(),
            subprocess_launcher=launcher,
        )
        assert len(launcher.calls) == 1


# ---------------------------------------------------------------------------
# 4. Judge parser failure-mode taxonomy
# ---------------------------------------------------------------------------


class TestAdvJudgeParseTaxonomy:
    @pytest.mark.parametrize(
        "stdout",
        [
            b"null",
            b"true",
            b"42",
            b"\"just a string\"",
            b"[1, 2]",
            b"{}",
            b"",
            b"{bogus",
            b"\x80\x81\x82",
        ],
    )
    def test_default_parser_rejects_non_object_outputs(self, stdout: bytes) -> None:
        with pytest.raises((ValueError, UnicodeDecodeError, json.JSONDecodeError)):
            default_judge_parse(stdout)

    def test_parser_exception_wrapped_as_f_pipe_09_with_cause(self) -> None:
        class _Boom(RuntimeError):
            pass

        def boom(_: bytes) -> dict[str, Any]:
            raise _Boom("parser internal failure")

        launcher = _FakeLauncher(default_stdout=b'{"x": 1}')
        with pytest.raises(F_PIPE_09) as exc_info:
            invoke_judge(
                run_state=_rs(
                    families={
                        "scribe": ("anthropic", "a1"),
                        "editor": ("google", "g1"),
                    }
                ),
                iteration_number=1,
                charter=_ch("judge"),
                cascade=_cs("judge", levels=(("openai", "gpt-5"),)),
                context=_ctx(),
                subprocess_launcher=launcher,
                judge_parse=boom,
            )
        assert exc_info.value.trigger == "judge_parse_failed"
        assert isinstance(exc_info.value.__cause__, _Boom)
        assert exc_info.value.details["parser_error"] == "_Boom"


# ---------------------------------------------------------------------------
# 5. Cascade current_level semantics under repeated invocation
# ---------------------------------------------------------------------------


class TestAdvCascadeStateful:
    def test_cascade_after_used_as_next_input_advances_further(self) -> None:
        rs = _rs()
        levels = (
            ("anthropic", "a"),
            ("google", "g"),
            ("openai", "o"),
        )
        launcher1 = _FakeLauncher(
            queue=[
                SubprocessResult(
                    exit_code=137,
                    stdout=b"",
                    stderr=b"",
                    timed_out=True,
                    landed_family="anthropic",
                    landed_model_id="a",
                ),
            ],
        )
        result1 = invoke_scribe(
            run_state=rs,
            iteration_number=1,
            charter=_ch("scribe"),
            cascade=_cs("scribe", levels=levels, current_level=0),
            context=_ctx(),
            subprocess_launcher=launcher1,
        )
        assert result1.cascade_after.current_level == 1

        # Second invocation using cascade_after as starting point.
        launcher2 = _FakeLauncher(
            queue=[
                SubprocessResult(
                    exit_code=137,
                    stdout=b"",
                    stderr=b"",
                    timed_out=True,
                    landed_family="google",
                    landed_model_id="g",
                ),
            ],
        )
        result2 = invoke_scribe(
            run_state=rs,
            iteration_number=1,
            charter=_ch("scribe"),
            cascade=result1.cascade_after,
            context=_ctx(),
            subprocess_launcher=launcher2,
        )
        assert result2.cascade_after.current_level == 2
        assert result2.landed_family == "openai"


# ---------------------------------------------------------------------------
# 6. Scribe ignores run_iteration_families_so_far
# ---------------------------------------------------------------------------


class TestAdvScribeNoCrossFamily:
    def test_scribe_iter2_with_populated_families_still_dispatches_level_0(
        self,
    ) -> None:
        rs = _rs(
            families={
                "scribe": ("anthropic", "iter1-scribe"),
                "editor": ("google", "iter1-editor"),
                "judge": ("openai", "iter1-judge"),
            }
        )
        launcher = _FakeLauncher()
        result = invoke_scribe(
            run_state=rs,
            iteration_number=2,
            charter=_ch("scribe"),
            cascade=_cs("scribe", levels=(("anthropic", "iter2"),)),
            context=_ctx(),
            subprocess_launcher=launcher,
        )
        assert result.landed_family == "anthropic"
        assert result.level_advances == 0


# ---------------------------------------------------------------------------
# 7. Thin wrapper equivalence
# ---------------------------------------------------------------------------


class TestAdvThinWrapperEquivalence:
    def test_invoke_scribe_matches_invoke_seat_scribe(self) -> None:
        kwargs = dict(
            run_state=_rs(),
            iteration_number=1,
            charter=_ch("scribe"),
            cascade=_cs("scribe"),
            context=_ctx(),
        )
        la = _FakeLauncher()
        lb = _FakeLauncher()
        ra = invoke_scribe(subprocess_launcher=la, **kwargs)  # type: ignore[arg-type]
        rb = invoke_seat(
            seat_kind="scribe", subprocess_launcher=lb, **kwargs
        )  # type: ignore[arg-type]
        assert ra.output_hash == rb.output_hash
        assert ra.landed_family == rb.landed_family
        assert la.calls[0]["timeout_ms"] == lb.calls[0]["timeout_ms"]
        assert la.calls[0]["seat_kind"] == lb.calls[0]["seat_kind"] == "scribe"

    def test_invoke_editor_matches_invoke_seat_editor(self) -> None:
        kwargs = dict(
            run_state=_rs(),
            iteration_number=1,
            charter=_ch("editor"),
            cascade=_cs("editor"),
            context=_ctx(),
        )
        la = _FakeLauncher()
        lb = _FakeLauncher()
        invoke_editor(subprocess_launcher=la, **kwargs)  # type: ignore[arg-type]
        invoke_seat(
            seat_kind="editor", subprocess_launcher=lb, **kwargs
        )  # type: ignore[arg-type]
        assert la.calls[0]["timeout_ms"] == lb.calls[0]["timeout_ms"] == 180_000

    def test_invoke_judge_matches_invoke_seat_judge(self) -> None:
        rs = _rs(
            families={
                "scribe": ("anthropic", "a1"),
                "editor": ("google", "g1"),
            }
        )
        kwargs = dict(
            run_state=rs,
            iteration_number=1,
            charter=_ch("judge"),
            cascade=_cs("judge", levels=(("openai", "gpt-5"),)),
            context=_ctx(),
        )
        la = _FakeLauncher(default_stdout=b'{"v": 1}')
        lb = _FakeLauncher(default_stdout=b'{"v": 1}')
        ra = invoke_judge(subprocess_launcher=la, **kwargs)  # type: ignore[arg-type]
        rb = invoke_seat(
            seat_kind="judge", subprocess_launcher=lb, **kwargs
        )  # type: ignore[arg-type]
        assert ra.judge_verdict == rb.judge_verdict == {"v": 1}


# ---------------------------------------------------------------------------
# 8. Mixed timeout/collision exhaustion details
# ---------------------------------------------------------------------------


class TestAdvMixedExhaustionDetails:
    def test_f_pipe_06_details_include_cascade_levels(self) -> None:
        rs = _rs()
        levels = (("anthropic", "a"), ("google", "g"))
        launcher = _FakeLauncher(
            queue=[
                SubprocessResult(
                    exit_code=137,
                    stdout=b"",
                    stderr=b"",
                    timed_out=True,
                    landed_family=f,
                    landed_model_id=m,
                )
                for f, m in levels
            ],
        )
        with pytest.raises(F_PIPE_06) as exc_info:
            invoke_scribe(
                run_state=rs,
                iteration_number=1,
                charter=_ch("scribe"),
                cascade=_cs("scribe", levels=levels),
                context=_ctx(),
                subprocess_launcher=launcher,
            )
        assert exc_info.value.details["cascade_levels"] == [
            ["anthropic", "a"],
            ["google", "g"],
        ]
        assert exc_info.value.details["start_level"] == 0


# ---------------------------------------------------------------------------
# 9. Blueprint hash pin
# ---------------------------------------------------------------------------


class TestAdvBlueprintPin:
    def test_blueprint_deps_carries_v6_locked_hash(self) -> None:
        assert (
            BLUEPRINT_DEPS["section_05_pipeline.md"]["hash_sha3_512_prefix16"]
            == "feb5928491e4dc40"
        )
        assert BLUEPRINT_DEPS["section_05_pipeline.md"]["version"] == "v6"

    def test_blueprint_deps_v6_amendment_entry_present(self) -> None:
        assert "section_05_v6_amendment.md" in BLUEPRINT_DEPS
        assert (
            BLUEPRINT_DEPS["section_05_v6_amendment.md"]["hash_sha3_512_prefix16"]
            == "52ae6b3b97b159b5"
        )


# ---------------------------------------------------------------------------
# E-023 scope-authority documentation
# ---------------------------------------------------------------------------
#
# Out-of-scope surfaces deliberately NOT tested here (per §3.11 v5 trusted-
# operator envelope and Round 4 spec card):
#
#  1. Production subprocess spawning (fork/exec). §2 Vault's seat_launch
#     contract owns this; Round 4 only consumes a Protocol.
#  2. Launcher merging os.environ into env. The launcher's bug, not
#     Round 4's. Round 4's guarantee is the env dict it PASSES, not what
#     the launcher does with it.
#  3. Subprocess exit-code semantics for non-Judge seats. Round 5
#     revision_loop inspects the result; Round 4 only branches on
#     ``timed_out``.
#  4. Cross-iteration cross-family enforcement (iter_2 Scribe ==
#     iter_1 Editor family? allowed). ``run_iteration_families_so_far``
#     is a single-iteration snapshot per blueprint §4.6.
#  5. SeatCharter.allowed_families vs cascade families. Round 1 validates
#     this at charter construction; Round 4 trusts the validated input.
#  6. Judge semantic validation (score ranges, rubric dimensions). §4
#     Logician POST-gate + Round 5 revision_loop own that layer.
#  7. vault_write / clock / sleep behaviour under Round 5+7 wiring. Round
#     4 only pins "Round 4 does not invoke them." Semantics will be
#     validated at Round 5 / Round 7 LOCK time.
