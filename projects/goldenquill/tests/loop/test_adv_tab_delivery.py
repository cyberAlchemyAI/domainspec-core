"""Adversarial tests for pipeline.loop.tab_delivery — §4.11 v3 closure pins.

Blueprint §5 v6 §4.11 LOCKED 2026-04-19 + §4.15 eval-mode shield + §6
F-PIPE-01 / F-PIPE-16 / F-PIPE-21 raise-site taxonomy.

Closure-pin coverage (spec card ``section_05_round_9_tab_delivery.md``):
- V1 rebind-resistance — TAB_ORDERING + "submission" sentinel.
- A-v1-06 — AST-grep banned-pattern regression (no inline tab_ordering tuple).
- B-v1-09 — post-write hash-mismatch path.
- B-v1-17 — module-load integrity assert inherited from config.py.
- §4.15 — eval-mode shield; F-PIPE-21 with taxonomy trigger.
- §3.5 — TabEnvelope __post_init__ inline-literal runtime check.
- E-023 residuals — malformed bytes, missing file, duplicate dispatch,
  non-monotonic clock, empty run_id, empty payload hash, empty canonical
  bytes stability under field-order change, cross-family non-dependency,
  threat-model docstring, signature hygiene.
"""

from __future__ import annotations

import hashlib
import importlib
import inspect
import json
import sys
from dataclasses import asdict, dataclass, field, replace
from typing import Any

import pytest

from pipeline.loop import tab_delivery as tab_delivery_module
from pipeline.loop.errors import F_PIPE_01, F_PIPE_16, F_PIPE_21, PipelineFailure
from pipeline.loop.tab_delivery import (
    HashFileCallable,
    TabSigningResult,
    _canonical_bytes,
    _canonical_bytes_without_self_hash,
    _canonical_default,
    _parse_envelope,
    deliver_tab,
)
from pipeline.loop.types import IterationState, RunState, TabEnvelope
from pipeline.vault.error_codes import VaultWriteExists


# ---------------------------------------------------------------------------
# Fakes (mirror happy-path module; repeated locally to keep this file
# self-describing under E-024 adversarial-LOC multiplier)
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
    store: dict[str, bytes] = field(default_factory=dict)
    read_calls: list[str] = field(default_factory=list)
    write_calls: list[dict[str, Any]] = field(default_factory=list)
    # Test hook: when set, vault.read() returns these bytes for the next
    # read regardless of what was written. Lets us simulate post-write
    # corruption without touching the store.
    read_override: dict[str, bytes] = field(default_factory=dict)

    def read(self, *, path: str) -> bytes:
        self.read_calls.append(path)
        if path in self.read_override:
            return self.read_override[path]
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
            raise VaultWriteExists(
                f"write-if-absent collision at {path} (fake)"
            )
        self.store[path] = payload
        return hashlib.sha256(payload).hexdigest()


@dataclass
class _FakeHashFile:
    hashes: dict[str, str]
    seen: list[str] = field(default_factory=list)

    def __call__(self, path: str) -> str:
        self.seen.append(path)
        if path not in self.hashes:
            raise FileNotFoundError(path)
        return self.hashes[path]


def _mk_run_state(
    *,
    run_id: str = "01HG-RUN-ADV",
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
        golden_set_ref=None if mode == "submission" else "orgs/x/golden/item",
        org_slug="mycosymbiotics_coop",
        session_id="SESS-ADV",
        phase="report_signed",
        started_at_iso=started_at_iso,
        iterations=iterations,
    )


def _mk_hashes(run_id: str, date: str, final_n: int) -> dict[str, str]:
    return {
        f"vault/fund_radar/{date}/live_radar.json": "1" * 64,
        f"vault/deep_brief/{run_id}/brief.md": "2" * 64,
        f"vault/pipeline/{run_id}/iter_{final_n}/scribe_draft.md": "3" * 64,
    }


# ---------------------------------------------------------------------------
# V1 rebind-resistance — TAB_ORDERING
# ---------------------------------------------------------------------------


class TestV1RebindResistance:
    def test_config_tab_ordering_late_rebind_has_no_effect(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Rebinding ``pipeline.loop.config.TAB_ORDERING`` AFTER tab_delivery
        import has no effect on tab_delivery's runtime behaviour.

        tab_delivery captures ``TAB_ORDERING`` at module import via
        ``from pipeline.loop.config import TAB_ORDERING`` — the local
        binding in ``pipeline.loop.tab_delivery`` is frozen at import.
        A late config-module rebind cannot reach inside. The module-load
        assert is what catches rebind-BEFORE-load; a runtime rebind of
        the config-module attribute is impotent.

        This test is the inverse pin of the next test
        (``test_tab_delivery_module_tab_ordering_rebind_fails_step7_check``),
        which patches the tab_delivery-module binding directly and
        confirms Round 1's ``__post_init__`` fires.
        """
        from pipeline.loop import config as config_module

        monkeypatch.setattr(
            config_module,
            "TAB_ORDERING",
            ("council_draft", "deep_brief", "live_radar"),
        )
        rs = _mk_run_state()
        vault = _FakeVault()
        hf = _FakeHashFile(hashes=_mk_hashes("01HG-RUN-ADV", "2026-04-21", 2))

        # No raise — tab_delivery's captured TAB_ORDERING is unchanged.
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

    def test_tab_delivery_module_tab_ordering_rebind_fails_step7_check(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Rebind ``pipeline.loop.tab_delivery.TAB_ORDERING`` in the
        tab_delivery module namespace.

        Round 1's ``TabEnvelope.__post_init__`` still has its OWN inline
        literal and raises F_PIPE_16 at envelope construction — so the
        mutation visible inside tab_delivery doesn't help.
        """
        monkeypatch.setattr(
            tab_delivery_module,
            "TAB_ORDERING",
            ("bogus", "tuple", "here"),
        )
        rs = _mk_run_state()
        vault = _FakeVault()
        hf = _FakeHashFile(hashes=_mk_hashes("01HG-RUN-ADV", "2026-04-21", 2))

        with pytest.raises(F_PIPE_16) as exc_info:
            deliver_tab(
                run_state=rs,
                vault_read=vault.read,
                vault_write=vault.write,
                clock=_FakeClock(),
                hash_file=hf,
            )
        assert exc_info.value.trigger == "tab_envelope_ordering_violation"
        assert vault.write_calls == []

    def test_submission_sentinel_is_inline_literal(self) -> None:
        """Source-level pin: the entry-gate comparison uses inline literal.

        We grep the function source for the pattern
        ``run_state.mode != "submission"`` to confirm there is no
        module-attribute reference. A future refactor that introduces
        ``SUBMISSION_MODE = "submission"`` and compares against that
        name would regress V1 rebind-resistance.
        """
        src = inspect.getsource(deliver_tab)
        assert 'run_state.mode != "submission"' in src


# ---------------------------------------------------------------------------
# F-PIPE-16 taxonomy pin
# ---------------------------------------------------------------------------


class TestFPipe16Taxonomy:
    def test_mid_order_swap_raises_f_pipe_16_at_construction(self) -> None:
        """Direct TabEnvelope construction with swapped ordering raises
        F_PIPE_16 via :meth:`TabEnvelope.__post_init__`."""
        with pytest.raises(F_PIPE_16) as exc_info:
            TabEnvelope(
                run_id="RID",
                tab_ordering=("deep_brief", "live_radar", "council_draft"),
                live_radar_payload_hash="1" * 64,
                deep_brief_payload_hash="2" * 64,
                council_draft_payload_hash="3" * 64,
                assembled_at_iso="2026-04-21T12:00:00+00:00",
                envelope_sha256="",
            )
        assert exc_info.value.CODE == "F-PIPE-16"
        assert exc_info.value.trigger == "tab_envelope_ordering_violation"
        assert exc_info.value.details["observed"] == (
            "deep_brief",
            "live_radar",
            "council_draft",
        )


# ---------------------------------------------------------------------------
# F-PIPE-21 eval-mode shield
# ---------------------------------------------------------------------------


class TestFPipe21EvalShield:
    def test_eval_mode_raises_f_pipe_21_before_any_io(self) -> None:
        rs = _mk_run_state(mode="eval")
        vault = _FakeVault()
        hf = _FakeHashFile(hashes={})  # empty — would raise FileNotFoundError

        with pytest.raises(F_PIPE_21) as exc_info:
            deliver_tab(
                run_state=rs,
                vault_read=vault.read,
                vault_write=vault.write,
                clock=_FakeClock(),
                hash_file=hf,
            )
        assert exc_info.value.CODE == "F-PIPE-21"
        assert exc_info.value.trigger == "eval_run_reached_tab_delivery"
        # No hash_file, no vault_read, no vault_write.
        assert hf.seen == []
        assert vault.read_calls == []
        assert vault.write_calls == []

    def test_f_pipe_21_trigger_is_enumerated(self) -> None:
        """The eval-mode trigger MUST be a declared F_PIPE_21 sub-trigger."""
        from pipeline.loop.config import F_PIPE_21_TRIGGERS

        assert "eval_run_reached_tab_delivery" in F_PIPE_21_TRIGGERS


# ---------------------------------------------------------------------------
# B-v1-09 post-write hash-mismatch path
# ---------------------------------------------------------------------------


class TestBv109PostWriteVerify:
    def test_hash_mismatch_raises_f_pipe_01(self) -> None:
        rs = _mk_run_state()
        vault = _FakeVault()
        hf = _FakeHashFile(hashes=_mk_hashes("01HG-RUN-ADV", "2026-04-21", 2))

        # Pre-arrange: the read_override returns a DIFFERENT envelope's
        # canonical bytes. We fabricate one by constructing a fresh
        # TabEnvelope with a bogus envelope_sha256 value and serialising.
        bogus_envelope = TabEnvelope(
            run_id="01HG-RUN-ADV",
            tab_ordering=("live_radar", "deep_brief", "council_draft"),
            live_radar_payload_hash="1" * 64,
            deep_brief_payload_hash="2" * 64,
            council_draft_payload_hash="3" * 64,
            assembled_at_iso="2026-04-21T12:00:00.000+00:00",
            envelope_sha256="f" * 64,
        )
        vault.read_override[
            "pipeline/01HG-RUN-ADV/tab_envelope.json"
        ] = _canonical_bytes(bogus_envelope)

        with pytest.raises(F_PIPE_01) as exc_info:
            deliver_tab(
                run_state=rs,
                vault_read=vault.read,
                vault_write=vault.write,
                clock=_FakeClock(),
                hash_file=hf,
            )
        assert exc_info.value.CODE == "F-PIPE-01"
        assert exc_info.value.trigger == "tab_envelope_hash_mismatch"
        details = exc_info.value.details
        assert details["observed"] == "f" * 64
        assert details["expected"] != "f" * 64
        assert details["vault_path"] == "pipeline/01HG-RUN-ADV/tab_envelope.json"


# ---------------------------------------------------------------------------
# E-023 residuals — malformed bytes, missing file, duplicate dispatch
# ---------------------------------------------------------------------------


class TestE023Residuals:
    def test_malformed_bytes_at_read_back_propagates_json_error(self) -> None:
        rs = _mk_run_state()
        vault = _FakeVault()
        hf = _FakeHashFile(hashes=_mk_hashes("01HG-RUN-ADV", "2026-04-21", 2))
        vault.read_override[
            "pipeline/01HG-RUN-ADV/tab_envelope.json"
        ] = b"not valid json{{{"

        with pytest.raises(json.JSONDecodeError):
            deliver_tab(
                run_state=rs,
                vault_read=vault.read,
                vault_write=vault.write,
                clock=_FakeClock(),
                hash_file=hf,
            )

    def test_missing_live_radar_payload_propagates_filenotfound(self) -> None:
        rs = _mk_run_state()
        vault = _FakeVault()
        # Omit the live_radar hash — hash_file raises FileNotFoundError.
        hashes = _mk_hashes("01HG-RUN-ADV", "2026-04-21", 2)
        hashes.pop("vault/fund_radar/2026-04-21/live_radar.json")
        hf = _FakeHashFile(hashes=hashes)

        with pytest.raises(FileNotFoundError):
            deliver_tab(
                run_state=rs,
                vault_read=vault.read,
                vault_write=vault.write,
                clock=_FakeClock(),
                hash_file=hf,
            )
        # No vault_write on this branch.
        assert vault.write_calls == []

    def test_missing_deep_brief_payload_propagates_filenotfound(self) -> None:
        rs = _mk_run_state()
        vault = _FakeVault()
        hashes = _mk_hashes("01HG-RUN-ADV", "2026-04-21", 2)
        hashes.pop("vault/deep_brief/01HG-RUN-ADV/brief.md")
        hf = _FakeHashFile(hashes=hashes)

        with pytest.raises(FileNotFoundError):
            deliver_tab(
                run_state=rs,
                vault_read=vault.read,
                vault_write=vault.write,
                clock=_FakeClock(),
                hash_file=hf,
            )
        assert vault.write_calls == []

    def test_missing_council_draft_payload_propagates_filenotfound(self) -> None:
        rs = _mk_run_state()
        vault = _FakeVault()
        hashes = _mk_hashes("01HG-RUN-ADV", "2026-04-21", 2)
        hashes.pop("vault/pipeline/01HG-RUN-ADV/iter_2/scribe_draft.md")
        hf = _FakeHashFile(hashes=hashes)

        with pytest.raises(FileNotFoundError):
            deliver_tab(
                run_state=rs,
                vault_read=vault.read,
                vault_write=vault.write,
                clock=_FakeClock(),
                hash_file=hf,
            )
        assert vault.write_calls == []

    def test_empty_payload_hash_rejected_before_envelope(self) -> None:
        """Programmer contract — empty hash_file return is a ValueError."""
        rs = _mk_run_state()
        vault = _FakeVault()
        hashes = _mk_hashes("01HG-RUN-ADV", "2026-04-21", 2)
        hashes["vault/deep_brief/01HG-RUN-ADV/brief.md"] = ""  # empty!
        hf = _FakeHashFile(hashes=hashes)

        with pytest.raises(ValueError, match="empty payload hash"):
            deliver_tab(
                run_state=rs,
                vault_read=vault.read,
                vault_write=vault.write,
                clock=_FakeClock(),
                hash_file=hf,
            )
        assert vault.write_calls == []

    def test_duplicate_dispatch_raises_vault_write_exists(self) -> None:
        """Second deliver_tab for same run_id → write-if-absent fires."""
        rs = _mk_run_state()
        vault = _FakeVault()
        hf1 = _FakeHashFile(hashes=_mk_hashes("01HG-RUN-ADV", "2026-04-21", 2))
        hf2 = _FakeHashFile(hashes=_mk_hashes("01HG-RUN-ADV", "2026-04-21", 2))

        # First call succeeds.
        deliver_tab(
            run_state=rs,
            vault_read=vault.read,
            vault_write=vault.write,
            clock=_FakeClock(),
            hash_file=hf1,
        )
        # Second call — write-if-absent collision.
        with pytest.raises(VaultWriteExists):
            deliver_tab(
                run_state=rs,
                vault_read=vault.read,
                vault_write=vault.write,
                clock=_FakeClock(),
                hash_file=hf2,
            )

    def test_non_monotonic_clock_preserves_hash_stability(self) -> None:
        """Decreasing clock → unusual assembled_at_iso but valid envelope."""
        rs = _mk_run_state()
        vault = _FakeVault()
        hf = _FakeHashFile(hashes=_mk_hashes("01HG-RUN-ADV", "2026-04-21", 2))
        clock = _FakeClock(iso_values=["1999-01-01T00:00:00+00:00"])

        result = deliver_tab(
            run_state=rs,
            vault_read=vault.read,
            vault_write=vault.write,
            clock=clock,
            hash_file=hf,
        )
        assert result.envelope.assembled_at_iso == "1999-01-01T00:00:00+00:00"
        # Post-write verify still passes (hash is over canonical bytes).
        assert result.stored_envelope_hash == result.envelope.envelope_sha256


# ---------------------------------------------------------------------------
# A-v1-06 — banned-pattern regression (AST-grep equivalent)
# ---------------------------------------------------------------------------


class TestAv106BannedPattern:
    def test_no_inline_tuple_tab_ordering_in_source(self) -> None:
        """Grep the module source: every TabEnvelope(...) construction must
        reference TAB_ORDERING (or a replace() of an existing envelope).
        No call with an inline tuple/list as ``tab_ordering=`` arg."""
        import ast

        src = inspect.getsource(tab_delivery_module)
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            # Match TabEnvelope(...) calls.
            name = ""
            if isinstance(func, ast.Name):
                name = func.id
            elif isinstance(func, ast.Attribute):
                name = func.attr
            if name != "TabEnvelope":
                continue
            for kw in node.keywords:
                if kw.arg != "tab_ordering":
                    continue
                # The value MUST be an ast.Name (reference a constant),
                # NOT an inline ast.Tuple or ast.List literal.
                assert not isinstance(
                    kw.value, (ast.Tuple, ast.List)
                ), (
                    f"A-v1-06 regression: TabEnvelope(tab_ordering=<inline "
                    f"tuple>) at line {kw.value.lineno}"
                )


# ---------------------------------------------------------------------------
# Canonical-bytes stability under field-order changes
# ---------------------------------------------------------------------------


class TestCanonicalBytesStability:
    def test_sort_keys_gives_field_order_independence(self) -> None:
        rs = _mk_run_state()
        vault = _FakeVault()
        hf = _FakeHashFile(hashes=_mk_hashes("01HG-RUN-ADV", "2026-04-21", 2))

        result = deliver_tab(
            run_state=rs,
            vault_read=vault.read,
            vault_write=vault.write,
            clock=_FakeClock(),
            hash_file=hf,
        )

        # Re-serialise with deliberately scrambled insertion order.
        original = _canonical_bytes(result.envelope)
        scrambled_dict = dict(
            reversed(list(json.loads(original.decode("utf-8")).items()))
        )
        re_serialised = json.dumps(
            scrambled_dict, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        assert re_serialised == original

    def test_canonical_bytes_without_self_excludes_envelope_sha256(self) -> None:
        env = TabEnvelope(
            run_id="X",
            tab_ordering=("live_radar", "deep_brief", "council_draft"),
            live_radar_payload_hash="1" * 64,
            deep_brief_payload_hash="2" * 64,
            council_draft_payload_hash="3" * 64,
            assembled_at_iso="iso",
            envelope_sha256="deadbeef",
        )
        body = _canonical_bytes_without_self_hash(env).decode("utf-8")
        assert "envelope_sha256" not in body
        # And the full canonical bytes DO include it.
        full = _canonical_bytes(env).decode("utf-8")
        assert "envelope_sha256" in full


# ---------------------------------------------------------------------------
# Threat-model docstring + cross-family non-dependency pins
# ---------------------------------------------------------------------------


class TestDocstringAndImports:
    def test_threat_model_docstring_enumerates_four_residuals(self) -> None:
        doc = tab_delivery_module.__doc__ or ""
        assert "Malformed envelope bytes at read-back" in doc
        assert "Missing signature file" in doc
        assert "Half-signed tab" in doc
        assert "Zero-tab delivery" in doc

    def test_no_rate_limiter_or_cascade_import(self) -> None:
        """Parallel-dispatch regression pin — R9 MUST NOT import R7/R8."""
        src = inspect.getsource(tab_delivery_module)
        assert "rate_limiter" not in src
        assert "from pipeline.loop.cascade" not in src

    def test_deliver_tab_signature_is_keyword_only(self) -> None:
        sig = inspect.signature(deliver_tab)
        for name, param in sig.parameters.items():
            assert param.kind == inspect.Parameter.KEYWORD_ONLY, (
                f"{name} is not keyword-only"
            )

    def test_module_load_integrity_assert_present(self) -> None:
        """Re-import the module cleanly → module-load assert passes.

        A rebind of TAB_ORDERING BEFORE the module loads would trip the
        ``assert`` at import time. We confirm the assert line exists in
        source as a structural pin.
        """
        src = inspect.getsource(tab_delivery_module)
        assert 'assert TAB_ORDERING == ("live_radar"' in src

    def test_reimport_round_trips_clean(self) -> None:
        """Remove + re-import → module loads without integrity failure."""
        mod_name = tab_delivery_module.__name__
        saved = sys.modules.pop(mod_name)
        try:
            reloaded = importlib.import_module(mod_name)
            assert reloaded.TAB_ORDERING == (
                "live_radar",
                "deep_brief",
                "council_draft",
            )
        finally:
            sys.modules[mod_name] = saved


# ---------------------------------------------------------------------------
# Malformed RunState
# ---------------------------------------------------------------------------


class TestMalformedRunState:
    def test_empty_started_at_iso_uses_empty_date_prefix(self) -> None:
        """RunState with empty started_at_iso → run_id_date == "".

        The three payload paths still resolve (the hash_file sees an
        empty-date path segment). This is a documented E-023 residual —
        the caller is responsible for stamping started_at_iso at
        start_run.
        """
        rs = _mk_run_state(started_at_iso="")
        vault = _FakeVault()
        hashes = {
            "vault/fund_radar//live_radar.json": "1" * 64,
            "vault/deep_brief/01HG-RUN-ADV/brief.md": "2" * 64,
            "vault/pipeline/01HG-RUN-ADV/iter_2/scribe_draft.md": "3" * 64,
        }
        hf = _FakeHashFile(hashes=hashes)

        result = deliver_tab(
            run_state=rs,
            vault_read=vault.read,
            vault_write=vault.write,
            clock=_FakeClock(),
            hash_file=hf,
        )
        assert "vault/fund_radar//live_radar.json" in hf.seen
        assert result.vault_path == "pipeline/01HG-RUN-ADV/tab_envelope.json"

    def test_zero_iterations_final_n_is_zero(self) -> None:
        """Empty iterations → iter_0 path."""
        rs = _mk_run_state(iter_count=0)
        # iter_count=0 means len(iterations) == 0 → final_n = 0.
        rs.iterations = []
        vault = _FakeVault()
        hashes = {
            "vault/fund_radar/2026-04-21/live_radar.json": "1" * 64,
            "vault/deep_brief/01HG-RUN-ADV/brief.md": "2" * 64,
            "vault/pipeline/01HG-RUN-ADV/iter_0/scribe_draft.md": "3" * 64,
        }
        hf = _FakeHashFile(hashes=hashes)

        result = deliver_tab(
            run_state=rs,
            vault_read=vault.read,
            vault_write=vault.write,
            clock=_FakeClock(),
            hash_file=hf,
        )
        assert any("iter_0" in p for p in hf.seen)
        assert result.envelope.run_id == "01HG-RUN-ADV"


# ---------------------------------------------------------------------------
# PipelineFailure inheritance pin
# ---------------------------------------------------------------------------


class TestCanonicalDefaultBranches:
    """Direct unit coverage for ``_canonical_default`` non-mainline branches.

    ``asdict`` normalises nested dataclasses, tuples, and most types before
    ``json.dumps`` invokes ``default=``. The branch arms exist to harden
    canonicalisation against any future non-trivial field type (e.g. a
    ``frozenset`` or nested dataclass leaf) — they're exercised here by
    direct invocation so Round 9 ships at 100% coverage.
    """

    def test_dataclass_leaf_returns_asdict(self) -> None:
        @dataclass
        class _Leaf:
            x: int = 7
            y: str = "z"

        result = _canonical_default(_Leaf())
        assert result == {"x": 7, "y": "z"}

    def test_frozenset_returns_sorted_list(self) -> None:
        assert _canonical_default(frozenset({"b", "a", "c"})) == ["a", "b", "c"]

    def test_set_returns_sorted_list(self) -> None:
        assert _canonical_default({"b", "a", "c"}) == ["a", "b", "c"]

    def test_tuple_returns_list(self) -> None:
        assert _canonical_default(("x", "y")) == ["x", "y"]

    def test_dataclass_type_is_not_unpacked(self) -> None:
        """Guards against passing a class object (vs. instance)."""

        @dataclass
        class _Shape:
            a: int = 1

        result = _canonical_default(_Shape)
        # _Shape class falls through to the repr branch.
        assert "__repr__" in result

    def test_unknown_type_falls_back_to_repr(self) -> None:
        class _Thing:
            def __repr__(self) -> str:
                return "<thing>"

        result = _canonical_default(_Thing())
        assert result == {"__repr__": "<thing>"}


class TestExceptionHierarchy:
    def test_f_pipe_16_inherits_from_pipeline_failure(self) -> None:
        assert issubclass(F_PIPE_16, PipelineFailure)

    def test_f_pipe_01_inherits_from_pipeline_failure(self) -> None:
        assert issubclass(F_PIPE_01, PipelineFailure)

    def test_f_pipe_21_inherits_from_pipeline_failure(self) -> None:
        assert issubclass(F_PIPE_21, PipelineFailure)
