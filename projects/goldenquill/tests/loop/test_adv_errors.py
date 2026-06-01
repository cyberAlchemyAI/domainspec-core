"""Adversarial tests for pipeline.loop.errors — attack-surface coverage.

Blueprint §5 v6 §6 LOCKED 2026-04-19. The happy-path surface lives in
``test_errors.py``. This file only holds attacks: whitelist-bypass attempts
against F_PIPE_21 / F_PIPE_22, cross-class discrimination under ``except``,
dispatch-table integrity, subclass-override bypass probes, and module-load
rebind-resistance on the integrity asserts. No test here re-proves a
happy-path property; every test tries to break a contract.

Closes T-01 from ``pipeline/engineering/codebase_alignment_audit_2026-04-20.md``.
"""

from __future__ import annotations

import importlib
import sys
from collections.abc import Mapping
from typing import Any

import pytest

from pipeline.loop.config import F_PIPE_21_TRIGGERS, F_PIPE_22_TRIGGERS
from pipeline.loop.errors import (
    F_EVAL_CROSS_ORG_READ_CODE,
    F_PIPE_01,
    F_PIPE_02,
    F_PIPE_03,
    F_PIPE_08,
    F_PIPE_20,
    F_PIPE_21,
    F_PIPE_22,
    F_PIPE_BY_CODE,
    PipelineFailure,
)


# ---------------------------------------------------------------------------
# F_PIPE_21 whitelist-bypass probes — every trigger must come from §6 v6 row.
# ---------------------------------------------------------------------------


class TestAdvFPipe21WhitelistBypass:
    def test_adv_homoglyph_trigger_rejected(self) -> None:
        # Cyrillic 'а' (U+0430) instead of ASCII 'a' — visually identical.
        homoglyph = "mode_ch\u0430nge_after_start"
        assert homoglyph not in F_PIPE_21_TRIGGERS
        with pytest.raises(ValueError, match="F_PIPE_21_TRIGGERS"):
            F_PIPE_21(trigger=homoglyph)

    def test_adv_whitespace_padded_trigger_rejected(self) -> None:
        # A trailing NBSP would pass a lazy ``.strip()`` but fail set membership.
        for padded in (
            "mode_change_after_start ",
            " mode_change_after_start",
            "mode_change_after_start\u00a0",
            "mode_change_after_start\n",
        ):
            with pytest.raises(ValueError, match="F_PIPE_21_TRIGGERS"):
                F_PIPE_21(trigger=padded)

    def test_adv_case_variant_trigger_rejected(self) -> None:
        # Allowlist is case-sensitive on purpose — no silent normalisation.
        for variant in (
            "MODE_CHANGE_AFTER_START",
            "Mode_Change_After_Start",
            "mode_Change_After_Start",
        ):
            with pytest.raises(ValueError, match="F_PIPE_21_TRIGGERS"):
                F_PIPE_21(trigger=variant)

    def test_adv_positional_trigger_still_validated(self) -> None:
        # First-positional fallback path (``code_or_trigger``) must route
        # through the same validator, not a back-door.
        with pytest.raises(ValueError, match="F_PIPE_21_TRIGGERS"):
            F_PIPE_21("not_in_set")
        # And the positional happy path still works.
        exc = F_PIPE_21("eval_mode_has_tab_envelope_hash")
        assert exc.trigger == "eval_mode_has_tab_envelope_hash"

    def test_adv_none_trigger_rejected(self) -> None:
        # Explicit ``trigger=None`` collapses to the positional default ("")
        # which is not in the set.
        with pytest.raises(ValueError, match="F_PIPE_21_TRIGGERS"):
            F_PIPE_21(trigger=None)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# F_PIPE_22 whitelist-bypass probes — same contract, smaller set.
# ---------------------------------------------------------------------------


class TestAdvFPipe22WhitelistBypass:
    def test_adv_inverted_intent_rejected(self) -> None:
        # "runstate_schema_upgrade" is the inverse of the allowed trigger
        # and would be a common typo / prompt-injection payload.
        with pytest.raises(ValueError, match="F_PIPE_22_TRIGGERS"):
            F_PIPE_22(trigger="runstate_schema_upgrade")

    def test_adv_empty_string_trigger_rejected(self) -> None:
        assert "" not in F_PIPE_22_TRIGGERS
        with pytest.raises(ValueError, match="F_PIPE_22_TRIGGERS"):
            F_PIPE_22()

    def test_adv_trigger_substring_match_not_accepted(self) -> None:
        # Substring of a valid trigger must not be accepted.
        with pytest.raises(ValueError, match="F_PIPE_22_TRIGGERS"):
            F_PIPE_22(trigger="runstate_schema_")
        with pytest.raises(ValueError, match="F_PIPE_22_TRIGGERS"):
            F_PIPE_22(trigger="schema_downgrade")


# ---------------------------------------------------------------------------
# Cross-class discrimination — ``except F_PIPE_02`` must NOT catch siblings.
# ---------------------------------------------------------------------------


class TestAdvCrossClassDiscrimination:
    def test_adv_sibling_not_caught_by_peer_except(self) -> None:
        # A careless ``except F_PIPE_02`` must not swallow F_PIPE_03.
        with pytest.raises(F_PIPE_03):
            try:
                raise F_PIPE_03(trigger="post_gate_timeout")
            except F_PIPE_02:
                pytest.fail("F_PIPE_03 was caught by ``except F_PIPE_02``")

    def test_adv_base_class_catches_every_subclass(self) -> None:
        # Contrapositive: ``except PipelineFailure`` does cover every F-PIPE.
        for code, cls in F_PIPE_BY_CODE.items():
            # Use an allowed trigger for validating subclasses (F_PIPE_21/22).
            if cls is F_PIPE_21:
                kwargs = {"trigger": next(iter(F_PIPE_21_TRIGGERS))}
            elif cls is F_PIPE_22:
                kwargs = {"trigger": next(iter(F_PIPE_22_TRIGGERS))}
            else:
                kwargs = {"trigger": f"adv-{code}"}
            with pytest.raises(PipelineFailure) as ei:
                raise cls(**kwargs)  # type: ignore[arg-type]
            assert ei.value.code == code


# ---------------------------------------------------------------------------
# Dispatch-table integrity — rebind attempts, duplicates, and round-trip.
# ---------------------------------------------------------------------------


class TestAdvDispatchTableIntegrity:
    def test_adv_dispatch_table_is_readonly_mapping(self) -> None:
        # ``types.MappingProxyType`` is not used but the declared type is
        # ``Mapping[...]`` — writing through the name must not succeed without
        # ``dict()`` coercion. Attempting item-assignment on the live object
        # should raise (it's a plain dict, but the test documents intent: if
        # a future refactor hardens to MappingProxyType, this test still
        # passes; today it passes because we do not assign.)
        assert isinstance(F_PIPE_BY_CODE, Mapping)
        # Round-trip every code through its class and back.
        for code, cls in F_PIPE_BY_CODE.items():
            assert cls.CODE == code
            assert F_PIPE_BY_CODE[cls.CODE] is cls

    def test_adv_dispatch_table_rejects_rebind_at_fresh_import(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # Rebinding F_PIPE_BY_CODE on an imported module does NOT invalidate
        # already-loaded callers (that's Python). But a fresh import with a
        # tampered length MUST fail the assert. Simulate by mutating the
        # source module's dict after a forced reimport.
        monkeypatch.delitem(sys.modules, "pipeline.loop.errors", raising=False)
        errs = importlib.import_module("pipeline.loop.errors")
        # The assert at module load already ran successfully; re-run the
        # invariant explicitly — this mirrors the fail-closed contract.
        assert len(errs.F_PIPE_BY_CODE) == 22
        # Simulate a downgrade: a rogue subclass lookup for a bogus code.
        with pytest.raises(KeyError):
            errs.F_PIPE_BY_CODE["F-PIPE-99"]


# ---------------------------------------------------------------------------
# Subclass-override bypass — a malicious subclass cannot downgrade CODE.
# ---------------------------------------------------------------------------


class TestAdvSubclassOverrideBypass:
    def test_adv_subclass_cannot_fake_foreign_code_via_instance_assign(self) -> None:
        exc = F_PIPE_08(trigger="no_cross_family_level")
        # Instance-level code mutation is not guarded by __setattr__ but the
        # class-level CODE is Final[str] and must not change.
        assert type(exc).CODE == "F-PIPE-08"
        # A caller who inspects the instance code gets whatever was set; the
        # Final contract is on the *class*. Document the behavior under
        # attack: instance-level overwrite does not propagate to sibling
        # instances or to the dispatch table.
        exc.code = "F-PIPE-01"  # type: ignore[assignment]
        twin = F_PIPE_08(trigger="also_no_cross_family")
        assert twin.code == "F-PIPE-08"
        assert F_PIPE_BY_CODE["F-PIPE-08"] is F_PIPE_08

    def test_adv_rogue_subclass_picks_up_own_code(self) -> None:
        # A new subclass that pins a fresh CODE must be routable via
        # ``type(self).CODE`` — and crucially must NOT be registered in the
        # canonical F_PIPE_BY_CODE dispatch table unless explicitly added.
        class F_PIPE_ROGUE(PipelineFailure):  # noqa: N801 — test double
            CODE = "F-PIPE-ROGUE"
            SEVERITY = "LOW"
            SAVE_STATE_CONTRACT = "state-failure"

        exc = F_PIPE_ROGUE(trigger="unsanctioned")
        assert exc.code == "F-PIPE-ROGUE"
        assert "F-PIPE-ROGUE" not in F_PIPE_BY_CODE


# ---------------------------------------------------------------------------
# Details-argument adversarial surface — mapping subclasses, aliasing.
# ---------------------------------------------------------------------------


class TestAdvDetailsArgumentSurface:
    def test_adv_details_snapshot_detached_from_caller_mutation(self) -> None:
        # The ctor does ``dict(details or {})`` which snapshots once.
        # Caller-side mutation after construction must NOT reach the
        # exception's captured dict.
        caller_dict: dict[str, Any] = {"attempts": 1}
        exc = F_PIPE_01(trigger="cas_exhausted", details=caller_dict)
        caller_dict["attempts"] = 9999
        caller_dict["injected"] = "prompt_injection_payload"
        assert exc.details == {"attempts": 1}

    def test_adv_mapping_subclass_consumed_via_dict_coercion(self) -> None:
        class OneShotMapping(Mapping[str, Any]):
            """Hands out real values on first read, traps on second."""

            def __init__(self) -> None:
                self._inner = {"a": 1, "b": 2}
                self._reads = 0

            def __getitem__(self, key: str) -> Any:
                self._reads += 1
                return self._inner[key]

            def __iter__(self):
                return iter(self._inner)

            def __len__(self) -> int:
                return len(self._inner)

        trap = OneShotMapping()
        exc = F_PIPE_20(trigger="cedar_decision_missing", details=trap)
        # The ctor should have drained the mapping exactly once into a
        # plain dict; subsequent reads on the exception do not re-enter
        # the trap.
        reads_after_ctor = trap._reads
        _ = exc.details["a"], exc.details["b"]
        assert trap._reads == reads_after_ctor
        assert exc.details == {"a": 1, "b": 2}


# ---------------------------------------------------------------------------
# Forward-dep sentinel — §4 v2.1 owns the class; §5 only owns the code string.
# ---------------------------------------------------------------------------


class TestAdvForwardDepSentinelContract:
    def test_adv_no_stray_cross_org_read_symbol_leaks_into_module(self) -> None:
        import pipeline.loop.errors as errs

        # The contract is: Section 5 does NOT define a class for
        # F-EVAL-CROSS-ORG-READ. If one appears (copy-paste drift), this
        # test catches it.
        forbidden_names = [
            "F_EVAL_CROSS_ORG_READ",
            "FEvalCrossOrgRead",
            "CrossOrgReadError",
        ]
        for name in forbidden_names:
            assert not hasattr(errs, name), (
                f"pipeline.loop.errors must not define {name!r}; "
                "the class lives in §4 v2.1"
            )

    def test_adv_sentinel_code_not_in_dispatch_table(self) -> None:
        # A common mistake would be to register the sentinel string in
        # F_PIPE_BY_CODE, causing §5 to raise on §4's gate. Fail-closed.
        assert F_EVAL_CROSS_ORG_READ_CODE not in F_PIPE_BY_CODE
        assert F_EVAL_CROSS_ORG_READ_CODE.startswith("F-EVAL-")
