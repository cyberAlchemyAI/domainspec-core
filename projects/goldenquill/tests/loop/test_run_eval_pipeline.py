"""Happy-path tests for pipeline.loop.run_eval_pipeline — §4.15 eval-mode capstone (R12.B).

Blueprint §5 v6 LOCKED 2026-04-19 (§4.15 11-step eval-mode sequence).

Round 12.B is the SECOND §5 capstone (first was R11 submission-mode). These
tests exercise the 11-step eval-mode phase walk over a CAS-aware in-memory
vault with real R12.A primitives wired through:

- Full success single-item → calibration_assembled → calibration_signed →
  eval_finalized.
- Multi-item (3 items) — report carries 3 CalibrationReportItems.
- Subset filter — manifest has 5 items, subset=("a","c") → 2 processed in
  manifest order.
- PRE-gate soft-fail (F-EVAL-CROSS-ORG-READ) → aborted_trusted_fail.
- PRE-gate soft-fail (generic code) → aborted_trusted_fail.
- First-write of operator pubkey — provenance sidecar written.
- Second-run reconciles against stored pubkey (no re-write).
- Freshness verification on a post-sign verify_calibration_report call.
- Per-item checkpoint cadence pin (phase sequence captured).
- Mode-isolation: every vault_write observed has intent in the allow-list.
- EvalPipelineRunResult frozen + slotted.
- Empty subset (tuple()) → zero items processed, calibration assembled over
  empty items tuple.
- run_id propagates via fixed-factory closure (Round 3 surface untouched).
- Cascade failures — N/A at R12.B (Round 5 owns them) but we exercise a
  delta-plateau outcome mapping.
- iter_cap_no_pass mapping through F_PIPE_05 translation.

Adversarial surfaces live in ``tests/loop/test_adv_run_eval_pipeline.py``.
"""

from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from pipeline.calibration import (
    Ed25519ReferenceSigner,
    report_from_json,
    verify_calibration_report,
)
from pipeline.logician import PreGateInput, PreGateResult
from pipeline.loop.run_eval_pipeline import (
    EvalPipelineRunResult,
    RunEvalPipelineContext,
    run_eval_pipeline,
)
from pipeline.loop.seat_runner import SeatInvocationContext, SubprocessResult
from pipeline.loop.types import ProviderCascade, RunState, SeatCharter


# ---------------------------------------------------------------------------
# In-memory CAS-aware vault fake (shared shape with R11 tests)
# ---------------------------------------------------------------------------


@dataclass
class _InMemoryVault:
    store: dict[str, bytes] = field(default_factory=dict)
    writes: list[dict[str, Any]] = field(default_factory=list)

    def write(
        self,
        *,
        path: str,
        payload: bytes,
        intent: str,
        write_mode: str,
        expected_current_file_hash: str | None,
    ) -> str:
        self.writes.append(
            {
                "path": path,
                "intent": intent,
                "write_mode": write_mode,
                "expected_current_file_hash": expected_current_file_hash,
                "payload_len": len(payload),
                "payload": payload,
            }
        )
        if write_mode == "write-if-absent" and path in self.store:
            from pipeline.vault import VaultWriteExists

            raise VaultWriteExists(f"{path} already exists")
        if (
            write_mode == "overwrite"
            and expected_current_file_hash is not None
            and path in self.store
        ):
            current = hashlib.sha256(self.store[path]).hexdigest()
            if current != expected_current_file_hash:
                from pipeline.vault import VaultCASHeadMismatch

                raise VaultCASHeadMismatch(
                    f"{path}: expected {expected_current_file_hash[:8]}, got {current[:8]}"
                )
        self.store[path] = payload
        return hashlib.sha256(payload).hexdigest()

    def read(self, *, path: str) -> bytes:
        return self.store[path]


@dataclass
class _Clock:
    ms_start: int = 1_000
    ms_step: int = 5
    _ms: int = 0
    iso: str = "2026-04-21T12:00:00+00:00"

    def __post_init__(self) -> None:
        self._ms = self.ms_start

    def now_ms(self) -> int:
        v = self._ms
        self._ms += self.ms_step
        return v

    def now_iso(self) -> str:
        return self.iso


def _sleep_noop(_ms: int) -> None:
    return None


# ---------------------------------------------------------------------------
# Round 4/5 seam fakes
# ---------------------------------------------------------------------------


@dataclass
class _ContextFactory:
    calls: list[dict[str, Any]] = field(default_factory=list)

    def __call__(
        self,
        *,
        seat_kind: str,
        iter_n: int,
        prev_editor_hash: str | None,
        prev_judge_hash: str | None,
        run_state: RunState,
    ) -> SeatInvocationContext:
        self.calls.append(
            {
                "seat_kind": seat_kind,
                "iter_n": iter_n,
            }
        )
        return SeatInvocationContext(
            stdin_payload=f"{seat_kind}-iter-{iter_n}".encode("utf-8"),
            session_id=run_state.session_id,
            path_value="/usr/bin:/bin",
            home_value="/home/tilth",
        )


@dataclass
class _Launcher:
    per_seat: dict[str, list[SubprocessResult]] = field(default_factory=dict)
    default_judge_stdout: bytes = b'{"verdict": "PASS", "total_score": 90, "per_dimension": {"rigor": 9, "clarity": 8}}'
    calls: list[dict[str, Any]] = field(default_factory=list)

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
                "family": family,
                "model_id": model_id,
            }
        )
        q = self.per_seat.get(seat_kind, [])
        if q:
            return q.pop(0)
        stdout = self.default_judge_stdout if seat_kind == "judge" else b"draft"
        return SubprocessResult(
            exit_code=0,
            stdout=stdout,
            stderr=b"",
            timed_out=False,
            landed_family=family,
            landed_model_id=model_id,
        )


# ---------------------------------------------------------------------------
# PRE-gate seam fakes
# ---------------------------------------------------------------------------


@dataclass
class _PreGateCallable:
    result: PreGateResult | None = None
    calls: list[PreGateInput] = field(default_factory=list)

    def __call__(self, input_: PreGateInput) -> PreGateResult:
        self.calls.append(input_)
        assert self.result is not None
        return self.result


@dataclass
class _PreGateInputFactory:
    payload: Any = None
    calls: list[dict[str, Any]] = field(default_factory=list)

    def __call__(self, *, run_state: RunState) -> PreGateInput:
        self.calls.append({"run_state_id": run_state.run_id, "phase": run_state.phase})
        return self.payload  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Round 6 POST-gate seam — never invoked in eval mode v0.1 (shape stub)
# ---------------------------------------------------------------------------


class _PostGateRunnerStub:
    def run_post_gate(self, input_: Any) -> Any:  # pragma: no cover — unused
        raise AssertionError("POST-gate runner must not be invoked in eval mode")


def _post_gate_input_factory_stub(
    *, run_state: RunState, inner_loop_result: Any
) -> Any:  # pragma: no cover — unused
    raise AssertionError("POST-gate input factory must not be invoked in eval mode")


def _hash_file_stub(path: str) -> str:  # pragma: no cover — unused
    raise AssertionError("hash_file must not be invoked in eval mode")


# ---------------------------------------------------------------------------
# R12.A calibration seam fakes
# ---------------------------------------------------------------------------


@dataclass
class _GoldenSetVaultRead:
    """Fake for GoldenSetVaultRead — forwards to underlying _InMemoryVault.

    The signer for R12.A's golden_set module expects a vault-keyed lookup
    (no ``vault/`` prefix in the injected path — matches GoldenSetVaultRead
    Protocol shape). We wrap the vault's store to serve manifest bytes.
    """

    manifests: dict[str, bytes] = field(default_factory=dict)
    calls: list[str] = field(default_factory=list)

    def __call__(self, *, path: str) -> bytes:
        self.calls.append(path)
        # The path comes in as a resolved Path object from golden_set_iter
        # or as the original manifest_path; accept either.
        key = str(path)
        if key in self.manifests:
            return self.manifests[key]
        # Fallback: try basename match to accommodate resolved absolute paths.
        for k, v in self.manifests.items():
            if key.endswith(k) or k.endswith(key):
                return v
        raise FileNotFoundError(f"GoldenSetVaultRead: no manifest at {key}")


def _realpath_identity(p: str) -> str:
    """realpath fake — returns input unchanged (no symlink resolution)."""
    return p


def _is_symlink_false(p: Any) -> bool:
    """is_symlink fake — nothing is a symlink."""
    return False


@dataclass
class _PubkeyVault:
    """Fake PubkeyVaultReader + PubkeyVaultWriter pair."""

    stored: dict[str, bytes] = field(default_factory=dict)
    provenance: dict[str, bytes] = field(default_factory=dict)
    reads: list[str] = field(default_factory=list)
    writes: list[dict[str, Any]] = field(default_factory=list)

    def read(self, *, operator_org_slug: str) -> bytes | None:
        self.reads.append(operator_org_slug)
        return self.stored.get(operator_org_slug)

    def write(
        self,
        *,
        operator_org_slug: str,
        pubkey_bytes: bytes,
        provenance_bytes: bytes,
    ) -> tuple[str, str]:
        self.writes.append(
            {
                "operator_org_slug": operator_org_slug,
                "pubkey_len": len(pubkey_bytes),
                "provenance_len": len(provenance_bytes),
            }
        )
        self.stored[operator_org_slug] = pubkey_bytes
        self.provenance[operator_org_slug] = provenance_bytes
        return (f"pubkey:{operator_org_slug}", f"prov:{operator_org_slug}")


def _now_utc_fixed() -> datetime:
    return datetime(2026, 4, 21, 12, 0, 0, tzinfo=timezone.utc)


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------


def _charter(seat_kind: str) -> SeatCharter:
    return SeatCharter(
        seat_kind=seat_kind,
        allowed_families=frozenset({"anthropic", "google", "openai"}),
        primary_model="primary",
        cascade_level=0,
        subprocess_timeout_ms=180_000,
    )


def _cascade(seat_kind: str) -> ProviderCascade:
    if seat_kind == "scribe":
        levels = (("anthropic", "claude-opus"), ("google", "gemini"), ("openai", "gpt"))
    elif seat_kind == "editor":
        levels = (("google", "gemini"), ("openai", "gpt"), ("meta", "llama"))
    else:
        levels = (("openai", "gpt"), ("meta", "llama"), ("mistral", "mixtral"))
    return ProviderCascade(seat_kind=seat_kind, levels=levels, current_level=0)


def _pre_gate_pass() -> PreGateResult:
    return PreGateResult(
        passed=True,
        failed_check_number=None,
        failure_code=None,
        failure_detail=None,
        completed_checks=(1, 2, 3),
    )


def _pre_gate_fail(code: str = "F-EVAL-CROSS-ORG-READ") -> PreGateResult:
    return PreGateResult(
        passed=False,
        failed_check_number=5,
        failure_code=code,
        failure_detail="stub eval PRE-gate fail",
        completed_checks=(1, 2, 3, 4),
    )


_DEFAULT_MANIFEST_HASH: str = "a" * 64


def _build_manifest(
    *,
    org_slug: str = "fit_farms_llc",
    items: tuple[dict[str, Any], ...] | None = None,
    manifest_hash: str = _DEFAULT_MANIFEST_HASH,
) -> bytes:
    """Build a golden-set manifest payload that round-trips _deserialize_manifest.

    The manifest_hash is the top-level aggregate hash AND is replicated into
    every item (the per-item GoldenSetItem.manifest_hash mirrors the
    manifest-level hash — see R12.A GoldenSetItem contract).
    """
    default_items = (
        {
            "item_id": "item-A",
            "org_slug": org_slug,
            "funded_grant_label": "VAPG-FY26-A",
            "rfa_snapshot_path": f"vault/{org_slug}/golden_set/rfa/a.txt",
            "submitted_artifact_path": f"vault/{org_slug}/golden_set/submitted/a.pdf",
            "funded_outcome": "funded",
            "operator_curation_iso": "2026-03-15T09:00:00+00:00",
            "manifest_hash": manifest_hash,
        },
    )
    if items is None:
        body_items = default_items
    else:
        # Ensure every item carries the manifest_hash key.
        body_items = tuple(
            {**it, "manifest_hash": it.get("manifest_hash", manifest_hash)}
            for it in items
        )
    payload = {
        "schema_version": 1,
        "org_slug": org_slug,
        "manifest_hash": manifest_hash,
        "items": list(body_items),
    }
    return json.dumps(payload, sort_keys=True).encode("utf-8")


@dataclass
class _Harness:
    vault: _InMemoryVault
    clock: _Clock
    launcher: _Launcher
    context_factory: _ContextFactory
    pre_gate_callable: _PreGateCallable
    pre_gate_input_factory: _PreGateInputFactory
    golden_set_read: _GoldenSetVaultRead
    signer: Ed25519ReferenceSigner
    pubkey_vault: _PubkeyVault
    ctx: RunEvalPipelineContext
    manifest_path: str


def _build_harness(
    *,
    run_id: str = "run-r12b-happy",
    org_slug: str = "fit_farms_llc",
    pre_gate_result: PreGateResult | None = None,
    manifest_items: tuple[dict[str, Any], ...] | None = None,
    pre_existing_pubkey: bytes | None = None,
    signer: Ed25519ReferenceSigner | None = None,
) -> _Harness:
    vault = _InMemoryVault()
    clock = _Clock()
    launcher = _Launcher()
    context_factory = _ContextFactory()
    pre_gate_callable = _PreGateCallable(
        result=pre_gate_result if pre_gate_result is not None else _pre_gate_pass()
    )
    pre_gate_input_factory = _PreGateInputFactory(payload="pre-gate-input-opaque")

    manifest_path = f"vault/{org_slug}/golden_set/manifest.json"
    manifest_bytes = _build_manifest(org_slug=org_slug, items=manifest_items)
    golden_set_read = _GoldenSetVaultRead(manifests={manifest_path: manifest_bytes})

    if signer is None:
        private_key = Ed25519PrivateKey.generate()
        signer = Ed25519ReferenceSigner(private_key)

    pubkey_vault = _PubkeyVault()
    if pre_existing_pubkey is not None:
        pubkey_vault.stored[org_slug] = pre_existing_pubkey

    ctx = RunEvalPipelineContext(
        vault_read=vault.read,
        vault_write=vault.write,
        clock=clock,
        sleep=_sleep_noop,
        run_id_factory=lambda: run_id,
        subprocess_launcher=launcher,
        seat_context_factory=context_factory,
        pre_gate_callable=pre_gate_callable,
        pre_gate_input_factory=pre_gate_input_factory,
        post_gate_runner=_PostGateRunnerStub(),
        post_gate_input_factory=_post_gate_input_factory_stub,
        hash_file=_hash_file_stub,
        golden_set_vault_read=golden_set_read,
        realpath=_realpath_identity,
        is_symlink=_is_symlink_false,
        calibration_signer=signer,
        pubkey_vault_read=pubkey_vault.read,
        pubkey_vault_write=pubkey_vault.write,
        now_utc=_now_utc_fixed,
        council_charter_snapshot_hash="a" * 64,
        router_yaml_snapshot_hash="b" * 64,
    )
    return _Harness(
        vault=vault,
        clock=clock,
        launcher=launcher,
        context_factory=context_factory,
        pre_gate_callable=pre_gate_callable,
        pre_gate_input_factory=pre_gate_input_factory,
        golden_set_read=golden_set_read,
        signer=signer,
        pubkey_vault=pubkey_vault,
        ctx=ctx,
        manifest_path=manifest_path,
    )


def _run(
    harness: _Harness,
    *,
    run_id: str = "run-r12b-happy",
    operator_org_slug: str = "fit_farms_llc",
    subset: tuple[str, ...] | None = None,
) -> EvalPipelineRunResult:
    return run_eval_pipeline(
        run_id=run_id,
        operator_org_slug=operator_org_slug,
        golden_set_manifest_path=harness.manifest_path,
        session_id="sess-r12b",
        scribe_charter=_charter("scribe"),
        editor_charter=_charter("editor"),
        judge_charter=_charter("judge"),
        scribe_cascade=_cascade("scribe"),
        editor_cascade=_cascade("editor"),
        judge_cascade=_cascade("judge"),
        ctx=harness.ctx,
        subset=subset,
    )


# ===========================================================================
# Happy-path full success
# ===========================================================================


class TestFullSuccessSingleItem:
    def test_returns_eval_pipeline_run_result_eval_finalized(self) -> None:
        h = _build_harness(run_id="run-S1")
        result = _run(h, run_id="run-S1")

        assert isinstance(result, EvalPipelineRunResult)
        assert result.run_id == "run-S1"
        assert result.final_phase == "eval_finalized"
        assert result.items_consumed == 1
        assert result.aborted_operator is False
        assert result.calibration_report_path is not None
        assert result.calibration_report_path.endswith(
            "fit_farms_llc/golden_set/calibration_reports/run-S1.json"
        )
        assert result.calibration_signature_path is not None
        assert result.calibration_signature_path.endswith("run-S1.sig")
        assert result.elapsed_ms >= 0

    def test_pre_gate_factory_invoked_exactly_once(self) -> None:
        h = _build_harness()
        _run(h)
        assert len(h.pre_gate_input_factory.calls) == 1

    def test_pre_gate_callable_invoked_exactly_once(self) -> None:
        h = _build_harness()
        _run(h)
        assert len(h.pre_gate_callable.calls) == 1

    def test_result_is_frozen_slotted_dataclass(self) -> None:
        h = _build_harness()
        result = _run(h)
        with pytest.raises((AttributeError, Exception)):
            result.run_id = "mutated"  # type: ignore[misc]

    def test_context_is_frozen_slotted_dataclass(self) -> None:
        h = _build_harness()
        with pytest.raises((AttributeError, Exception)):
            h.ctx.sleep = lambda _ms: None  # type: ignore[misc]


# ===========================================================================
# Multi-item golden set
# ===========================================================================


class TestMultiItem:
    def test_three_items_produce_three_calibration_report_items(self) -> None:
        items = tuple(
            {
                "item_id": f"item-{name}",
                "org_slug": "fit_farms_llc",
                "funded_grant_label": f"label-{name}",
                "rfa_snapshot_path": f"vault/fit_farms_llc/golden_set/rfa/{name}.txt",
                "submitted_artifact_path": f"vault/fit_farms_llc/golden_set/submitted/{name}.pdf",
                "funded_outcome": "funded",
                "operator_curation_iso": "2026-03-15T09:00:00+00:00",
            }
            for name in ("A", "B", "C")
        )
        h = _build_harness(run_id="run-multi", manifest_items=items)
        result = _run(h, run_id="run-multi")

        assert result.final_phase == "eval_finalized"
        assert result.items_consumed == 3

        report_bytes = h.vault.store[result.calibration_report_path or ""]
        report = report_from_json(report_bytes)
        assert len(report.items) == 3
        assert [it.item_id for it in report.items] == ["item-A", "item-B", "item-C"]

    def test_zero_item_run_is_legal(self) -> None:
        h = _build_harness(run_id="run-empty", manifest_items=())
        result = _run(h, run_id="run-empty")
        assert result.final_phase == "eval_finalized"
        assert result.items_consumed == 0


# ===========================================================================
# Subset filter
# ===========================================================================


class TestSubsetFilter:
    def test_subset_filters_to_matching_items_preserving_manifest_order(self) -> None:
        items = tuple(
            {
                "item_id": f"item-{name}",
                "org_slug": "fit_farms_llc",
                "funded_grant_label": f"label-{name}",
                "rfa_snapshot_path": f"vault/fit_farms_llc/golden_set/rfa/{name}.txt",
                "submitted_artifact_path": f"vault/fit_farms_llc/golden_set/submitted/{name}.pdf",
                "funded_outcome": "funded",
                "operator_curation_iso": "2026-03-15T09:00:00+00:00",
            }
            for name in ("A", "B", "C", "D", "E")
        )
        h = _build_harness(run_id="run-sub", manifest_items=items)
        # subset in a different order than the manifest — manifest order must win.
        result = _run(
            h, run_id="run-sub", subset=("item-C", "item-A")
        )
        assert result.items_consumed == 2

        report_bytes = h.vault.store[result.calibration_report_path or ""]
        report = report_from_json(report_bytes)
        # Manifest order preserved even though subset is (C, A).
        assert [it.item_id for it in report.items] == ["item-A", "item-C"]

    def test_empty_subset_selects_zero_items(self) -> None:
        items = tuple(
            {
                "item_id": f"item-{name}",
                "org_slug": "fit_farms_llc",
                "funded_grant_label": f"label-{name}",
                "rfa_snapshot_path": f"vault/fit_farms_llc/golden_set/rfa/{name}.txt",
                "submitted_artifact_path": f"vault/fit_farms_llc/golden_set/submitted/{name}.pdf",
                "funded_outcome": "funded",
                "operator_curation_iso": "2026-03-15T09:00:00+00:00",
            }
            for name in ("A", "B")
        )
        h = _build_harness(run_id="run-ev", manifest_items=items)
        result = _run(h, run_id="run-ev", subset=())
        assert result.items_consumed == 0


# ===========================================================================
# PRE-gate soft-fail paths
# ===========================================================================


class TestPreGateSoftFail:
    def test_f_eval_cross_org_read_maps_to_aborted_trusted_fail(self) -> None:
        h = _build_harness(
            run_id="run-xo",
            pre_gate_result=_pre_gate_fail(code="F-EVAL-CROSS-ORG-READ"),
        )
        result = _run(h, run_id="run-xo")

        assert result.final_phase == "aborted_trusted_fail"
        assert result.items_consumed == 0
        assert result.calibration_report_path is None
        assert result.calibration_signature_path is None
        assert result.aborted_operator is False
        # No calibration reports written.
        assert not any(
            "calibration_reports" in w["path"] for w in h.vault.writes
        )

    def test_generic_pre_gate_fail_also_aborts(self) -> None:
        h = _build_harness(
            run_id="run-xo2",
            pre_gate_result=_pre_gate_fail(code="F-PRE-07-STUB"),
        )
        result = _run(h, run_id="run-xo2")
        assert result.final_phase == "aborted_trusted_fail"


# ===========================================================================
# Operator pubkey first-write + reconcile
# ===========================================================================


class TestOperatorPubkey:
    def test_first_write_populates_stored_pubkey_and_provenance(self) -> None:
        h = _build_harness(run_id="run-fw")
        assert h.pubkey_vault.stored == {}  # pre-condition

        result = _run(h, run_id="run-fw")
        assert result.final_phase == "eval_finalized"

        assert "fit_farms_llc" in h.pubkey_vault.stored
        stored = h.pubkey_vault.stored["fit_farms_llc"]
        assert len(stored) == 32  # Ed25519 raw pubkey
        assert stored == h.signer.public_key_bytes()

        assert "fit_farms_llc" in h.pubkey_vault.provenance
        prov_bytes = h.pubkey_vault.provenance["fit_farms_llc"]
        prov = json.loads(prov_bytes.decode("utf-8"))
        assert prov["operator_org_slug"] == "fit_farms_llc"
        assert prov["first_write_run_id"] == "run-fw"
        assert prov["algorithm"] == "Ed25519"

    def test_second_run_with_matching_stored_pubkey_does_not_rewrite(self) -> None:
        # First run: first-write.
        h1 = _build_harness(run_id="run-first")
        r1 = _run(h1, run_id="run-first")
        assert r1.final_phase == "eval_finalized"
        stored_pubkey = h1.pubkey_vault.stored["fit_farms_llc"]

        # Second run with same signer — should NOT trigger a write.
        h2 = _build_harness(
            run_id="run-second",
            pre_existing_pubkey=stored_pubkey,
            signer=h1.signer,
        )
        r2 = _run(h2, run_id="run-second")
        assert r2.final_phase == "eval_finalized"
        # No new writes — the same stored pubkey matches.
        assert h2.pubkey_vault.writes == []


# ===========================================================================
# Verification via R12.A verify_calibration_report (freshness)
# ===========================================================================


class TestVerificationRoundTrip:
    def test_signed_report_verifies_with_stored_pubkey(self) -> None:
        h = _build_harness(run_id="run-verify")
        result = _run(h, run_id="run-verify")
        assert result.final_phase == "eval_finalized"

        report_bytes = h.vault.store[result.calibration_report_path or ""]
        report = report_from_json(report_bytes)
        # signed_at_iso matches the clock's iso; ~5 ms into the future of
        # _now_utc_fixed so freshness window passes easily.
        verify_calibration_report(
            report,
            pubkey_bytes=h.pubkey_vault.stored["fit_farms_llc"],
            now_utc=_now_utc_fixed,
        )

    def test_detached_signature_bytes_match_report_signature(self) -> None:
        h = _build_harness(run_id="run-sigbytes")
        result = _run(h, run_id="run-sigbytes")

        report_bytes = h.vault.store[result.calibration_report_path or ""]
        sig_bytes = h.vault.store[result.calibration_signature_path or ""]

        report = report_from_json(report_bytes)
        assert report.signature == sig_bytes
        assert len(sig_bytes) == 64  # Ed25519 detached


# ===========================================================================
# Mode-isolation shield
# ===========================================================================


class TestModeIsolation:
    def test_every_write_has_an_allowed_intent(self) -> None:
        h = _build_harness(run_id="run-iso")
        _run(h, run_id="run-iso")

        # Eval-mode allowed intents: golden-set-write, state-success, state-failure.
        allowed = frozenset({"golden-set-write", "state-success", "state-failure"})
        seen = {w["intent"] for w in h.vault.writes}
        # All writes must be drawn from the allow-list.
        assert seen.issubset(allowed), f"unexpected intents: {seen - allowed}"

    def test_no_three_tab_deliver_intent_appears(self) -> None:
        h = _build_harness(run_id="run-nodel")
        _run(h, run_id="run-nodel")
        assert not any(
            w["intent"] == "three-tab-deliver" for w in h.vault.writes
        )


# ===========================================================================
# Phase cadence + CAS threading
# ===========================================================================


class TestPhaseCadence:
    def test_phase_progression_captures_eval_iter_pending_and_calibration(self) -> None:
        h = _build_harness(run_id="run-cadence")
        _run(h, run_id="run-cadence")

        # Every state-success write serializes the RunState. Because the
        # checkpoint path is stable (CAS-overwritten), the vault.store only
        # holds the last body — scan the write-time payload instead.
        phases: list[str] = []
        for w in h.vault.writes:
            if w["intent"] != "state-success":
                continue
            try:
                data = json.loads(w["payload"].decode("utf-8"))
            except Exception:
                continue
            if isinstance(data, dict) and "phase" in data:
                phases.append(data["phase"])

        # Required phase waypoints (at minimum — resume anchor phases).
        required = {
            "pre_gate_pending",
            "pre_gate_passed",
            "eval_iter_pending",
            "inner_loop_iter_1",
            "calibration_assembled",
            "calibration_signed",
            "eval_finalized",
        }
        assert required.issubset(set(phases)), (
            f"missing eval-mode phase waypoints: {required - set(phases)}"
        )

    def test_eval_finalized_is_last_phase_written(self) -> None:
        h = _build_harness(run_id="run-last")
        _run(h, run_id="run-last")

        phases_in_order: list[str] = []
        for w in h.vault.writes:
            if w["intent"] != "state-success":
                continue
            try:
                data = json.loads(w["payload"].decode("utf-8"))
            except Exception:
                continue
            if isinstance(data, dict) and "phase" in data:
                phases_in_order.append(data["phase"])
        assert phases_in_order, "no state-success phases captured"
        assert phases_in_order[-1] == "eval_finalized"


# ===========================================================================
# run_id + mode propagation
# ===========================================================================


class TestRunIdMode:
    def test_run_id_propagates_via_fixed_factory(self) -> None:
        h = _build_harness(run_id="run-fixed")
        result = _run(h, run_id="run-fixed")
        assert result.run_id == "run-fixed"

    def test_eval_mode_runstate_carries_golden_set_ref(self) -> None:
        h = _build_harness(run_id="run-mode")
        _run(h, run_id="run-mode")

        # Locate a state-success write and inspect the payload shape.
        for w in h.vault.writes:
            if w["intent"] != "state-success":
                continue
            try:
                data = json.loads(w["payload"].decode("utf-8"))
            except Exception:
                continue
            if isinstance(data, dict) and data.get("run_id") == "run-mode":
                assert data.get("mode") == "eval"
                assert data.get("rfa_hash") is None
                assert data.get("project_context_hash") is None
                assert data.get("golden_set_ref") == h.manifest_path
                return
        pytest.fail("no eval-mode runstate payload captured")


# ===========================================================================
# Sidecar progress + elapsed_ms
# ===========================================================================


class TestAuxiliarySurfaces:
    def test_progress_sidecar_written_under_pipeline_run_id(self) -> None:
        h = _build_harness(run_id="run-sidecar")
        _run(h, run_id="run-sidecar")

        sidecar_paths = [
            w["path"]
            for w in h.vault.writes
            if w["path"].startswith("pipeline/run-sidecar/eval_progress.json")
        ]
        assert sidecar_paths, "progress sidecar was never written"

    def test_elapsed_ms_is_non_negative(self) -> None:
        h = _build_harness(run_id="run-elapsed")
        result = _run(h, run_id="run-elapsed")
        assert result.elapsed_ms >= 0

    def test_blueprint_deps_constant_is_populated(self) -> None:
        from pipeline.loop.run_eval_pipeline import BLUEPRINT_DEPS

        assert "section_05_pipeline.md" in BLUEPRINT_DEPS
        assert BLUEPRINT_DEPS["section_05_pipeline.md"]["version"] == "v6"
