"""conftest_section_5 — §5 Round 13 capstone fixture library.

Blueprint §5 v6 LOCKED 2026-04-19 — this file provides shared fixtures for
R13 capstone tests that promote §5 from LOCKED-per-module (R1-R12.B) to
LOCKED-as-a-whole-section.

This module is a SIBLING of (not a replacement for) any existing conftest
in ``tests/loop/``. At R13 write time, ``tests/loop/conftest.py`` does not
exist — R13 adds ``conftest_section_5.py`` with the section-5-specific
fixtures. Fixtures are exported via pytest's ``conftest_section_5``
autouse module mechanism: R13 tests that need them import the helper
factories directly (not via pytest fixture injection) to keep the
capstone test surface uniform with R11 + R12.B harness patterns.

The harness helpers here mirror the ``_InMemoryVault`` / ``_Clock`` /
``_Launcher`` / ``_ContextFactory`` shapes from R11's
``test_run_pipeline.py`` + R12.B's ``test_run_eval_pipeline.py`` verbatim,
so R13 tests exercise the exact public surface shape used in the
per-round LOCK evidence.

ORIENT OQ resolutions (spec card §"Open questions"):
1. *Separate conftest.* R13 ships this file as a sibling, not merged into
   an existing ``tests/loop/conftest.py`` (which does not exist at write
   time — smaller blast radius; rollback is file-delete).
2. *Threading + in-memory vault for BT5 fork-race.* The
   ``_SharedVault`` below is safe for ``threading`` (uses ``threading.Lock``
   around CAS mutations); see ``test_section_5_bt5_rate_limit.py``.
3. *100 paired firings for J.5 fuzz* — builders below accept per-call
   run_id / org_slug so the fuzz harness can parameterize 100 pairs.
4. *§7.16 canonical-bytes exhaustiveness re-asserted in R13* via a
   dataclass-field walker in ``test_section_5_invariants.py``.
5. *Explicit J.5 first-write-pubkey assertion* — harness captures every
   ``pubkey_vault.writes`` entry; the fuzz test asserts
   ``len(writes) == org_slug_count`` (one first-write per slug, zero
   second-writes).
6. *Sequential fuzz in one pytest session* — single harness module, no
   CI split.
7. *AST-lint R7 domain check* — test files live outside ``pipeline.loop.*``
   namespace; R7 walker is unaffected. Verified at R13 ORIENT.
"""

from __future__ import annotations

import hashlib
import json
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from pipeline.calibration import Ed25519ReferenceSigner
from pipeline.logician import PreGateInput, PreGateResult
from pipeline.loop.post_gate_runner import GateRunnerPostResult
from pipeline.loop.revision_loop import InnerLoopResult
from pipeline.loop.run_eval_pipeline import RunEvalPipelineContext
from pipeline.loop.run_pipeline import RunPipelineContext
from pipeline.loop.seat_runner import SeatInvocationContext, SubprocessResult
from pipeline.loop.types import ProviderCascade, RunState, SeatCharter


# ---------------------------------------------------------------------------
# CAS-aware in-memory vault — shared shape with R11 + R12.B test harnesses
# ---------------------------------------------------------------------------


@dataclass
class InMemoryVault:
    """Single-threaded CAS-aware vault fake (R11/R12.B shape)."""

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
                    f"{path}: expected {expected_current_file_hash[:8]}, "
                    f"got {current[:8]}"
                )
        self.store[path] = payload
        return hashlib.sha256(payload).hexdigest()

    def read(self, *, path: str) -> bytes:
        return self.store[path]


@dataclass
class SharedVault:
    """Thread-safe CAS-aware vault fake for BT5 fork-race harness (J.4)."""

    store: dict[str, bytes] = field(default_factory=dict)
    writes: list[dict[str, Any]] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def write(
        self,
        *,
        path: str,
        payload: bytes,
        intent: str,
        write_mode: str,
        expected_current_file_hash: str | None,
    ) -> str:
        with self._lock:
            self.writes.append(
                {
                    "path": path,
                    "intent": intent,
                    "write_mode": write_mode,
                    "expected_current_file_hash": expected_current_file_hash,
                    "payload_len": len(payload),
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
                        f"{path}: expected {expected_current_file_hash[:8]}, "
                        f"got {current[:8]}"
                    )
            self.store[path] = payload
            return hashlib.sha256(payload).hexdigest()

    def read(self, *, path: str) -> bytes:
        with self._lock:
            return self.store[path]


# ---------------------------------------------------------------------------
# Clock + sleep fakes
# ---------------------------------------------------------------------------


@dataclass
class Clock:
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


def sleep_noop(_ms: int) -> None:
    return None


def now_utc_fixed() -> datetime:
    return datetime(2026, 4, 21, 12, 0, 0, tzinfo=timezone.utc)


# ---------------------------------------------------------------------------
# Seat fakes
# ---------------------------------------------------------------------------


@dataclass
class ContextFactory:
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
                "prev_editor_hash": prev_editor_hash,
                "prev_judge_hash": prev_judge_hash,
            }
        )
        return SeatInvocationContext(
            stdin_payload=f"{seat_kind}-iter-{iter_n}".encode("utf-8"),
            session_id=run_state.session_id,
            path_value="/usr/bin:/bin",
            home_value="/home/tilth",
        )


@dataclass
class Launcher:
    per_seat: dict[str, list[SubprocessResult]] = field(default_factory=dict)
    default_judge_stdout: bytes = (
        b'{"verdict": "PASS", "total_score": 90, '
        b'"per_dimension": {"rigor": 9, "clarity": 8}}'
    )
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
            {"seat_kind": seat_kind, "family": family, "model_id": model_id}
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
# PRE-gate + POST-gate fakes
# ---------------------------------------------------------------------------


@dataclass
class PreGateCallable:
    result: PreGateResult | None = None
    raise_exc: BaseException | None = None
    calls: list[PreGateInput] = field(default_factory=list)

    def __call__(self, input_: PreGateInput) -> PreGateResult:
        self.calls.append(input_)
        if self.raise_exc is not None:
            raise self.raise_exc
        assert self.result is not None
        return self.result


@dataclass
class PreGateInputFactory:
    payload: Any = None
    calls: list[dict[str, Any]] = field(default_factory=list)

    def __call__(self, *, run_state: RunState) -> PreGateInput:
        self.calls.append(
            {"run_state_id": run_state.run_id, "phase": run_state.phase}
        )
        return self.payload  # type: ignore[return-value]


@dataclass
class PostGateRunner:
    result: GateRunnerPostResult | None = None
    calls: list[Any] = field(default_factory=list)

    def run_post_gate(self, input_: Any) -> GateRunnerPostResult:
        self.calls.append(input_)
        assert self.result is not None
        return self.result


@dataclass
class PostGateInputFactory:
    payload: Any = None
    calls: list[dict[str, Any]] = field(default_factory=list)

    def __call__(
        self, *, run_state: RunState, inner_loop_result: InnerLoopResult
    ) -> Any:
        self.calls.append(
            {
                "run_state_id": run_state.run_id,
                "iterations_run": inner_loop_result.iterations_run,
            }
        )
        return self.payload


@dataclass
class HashFile:
    data: dict[str, str] = field(default_factory=dict)
    calls: list[str] = field(default_factory=list)

    def __call__(self, path: str) -> str:
        self.calls.append(path)
        return self.data.get(path, "a" * 64)


# ---------------------------------------------------------------------------
# Eval-mode seam fakes
# ---------------------------------------------------------------------------


@dataclass
class GoldenSetVaultRead:
    manifests: dict[str, bytes] = field(default_factory=dict)
    calls: list[str] = field(default_factory=list)

    def __call__(self, *, path: str) -> bytes:
        self.calls.append(path)
        key = str(path)
        if key in self.manifests:
            return self.manifests[key]
        for k, v in self.manifests.items():
            if key.endswith(k) or k.endswith(key):
                return v
        raise FileNotFoundError(f"GoldenSetVaultRead: no manifest at {key}")


def realpath_identity(p: str) -> str:
    return p


def is_symlink_false(p: Any) -> bool:
    return False


@dataclass
class PubkeyVault:
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


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------


def make_charter(seat_kind: str) -> SeatCharter:
    return SeatCharter(
        seat_kind=seat_kind,
        allowed_families=frozenset({"anthropic", "google", "openai"}),
        primary_model="primary",
        cascade_level=0,
        subprocess_timeout_ms=180_000,
    )


def make_cascade(seat_kind: str) -> ProviderCascade:
    if seat_kind == "scribe":
        levels = (
            ("anthropic", "claude-opus"),
            ("google", "gemini"),
            ("openai", "gpt"),
        )
    elif seat_kind == "editor":
        levels = (
            ("google", "gemini"),
            ("openai", "gpt"),
            ("meta", "llama"),
        )
    else:
        levels = (
            ("openai", "gpt"),
            ("meta", "llama"),
            ("mistral", "mixtral"),
        )
    return ProviderCascade(
        seat_kind=seat_kind, levels=levels, current_level=0
    )


def pre_gate_pass() -> PreGateResult:
    return PreGateResult(
        passed=True,
        failed_check_number=None,
        failure_code=None,
        failure_detail=None,
        completed_checks=(1, 2, 3),
    )


def pre_gate_fail(code: str = "F-PRE-05-STUB") -> PreGateResult:
    return PreGateResult(
        passed=False,
        failed_check_number=5,
        failure_code=code,
        failure_detail="stub PRE-gate fail",
        completed_checks=(1, 2, 3, 4),
    )


def post_gate_pass() -> GateRunnerPostResult:
    return GateRunnerPostResult(
        passed=True,
        failed_step_number=None,
        failure_code=None,
        failure_detail="",
        failure_codes=(),
        completed_steps=(),
        claim_evidence_map=None,
        underlying_post_gate_result=None,
    )


def post_gate_fail(code: str = "F-POST-12-STUB") -> GateRunnerPostResult:
    return GateRunnerPostResult(
        passed=False,
        failed_step_number=12,
        failure_code=code,
        failure_detail="stub POST-gate fail",
        failure_codes=(code,),
        completed_steps=(),
        claim_evidence_map=None,
        underlying_post_gate_result=None,
    )


DEFAULT_MANIFEST_HASH: str = "a" * 64


def build_manifest(
    *,
    org_slug: str = "fit_farms_llc",
    items: tuple[dict[str, Any], ...] | None = None,
    manifest_hash: str = DEFAULT_MANIFEST_HASH,
) -> bytes:
    """Produce a golden-set manifest JSON bytes payload."""

    default_items = (
        {
            "item_id": "item-A",
            "org_slug": org_slug,
            "funded_grant_label": "VAPG-FY26-A",
            "rfa_snapshot_path": f"vault/{org_slug}/golden_set/rfa/a.txt",
            "submitted_artifact_path": (
                f"vault/{org_slug}/golden_set/submitted/a.pdf"
            ),
            "funded_outcome": "funded",
            "operator_curation_iso": "2026-03-15T09:00:00+00:00",
            "manifest_hash": manifest_hash,
        },
    )
    if items is None:
        body_items = default_items
    else:
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
class SubmissionHarness:
    vault: InMemoryVault
    clock: Clock
    launcher: Launcher
    context_factory: ContextFactory
    pre_gate_callable: PreGateCallable
    pre_gate_input_factory: PreGateInputFactory
    post_gate_runner: PostGateRunner
    post_gate_input_factory: PostGateInputFactory
    hash_file: HashFile
    context: RunPipelineContext


def build_submission_harness(
    *,
    run_id: str = "run-R13",
    pre_gate_result: PreGateResult | None = None,
    post_gate_result: GateRunnerPostResult | None = None,
    vault: InMemoryVault | None = None,
) -> SubmissionHarness:
    vault_obj = vault if vault is not None else InMemoryVault()
    clock = Clock()
    launcher = Launcher()
    context_factory = ContextFactory()
    pre_gate_callable = PreGateCallable(
        result=pre_gate_result if pre_gate_result is not None else pre_gate_pass()
    )
    pre_gate_input_factory = PreGateInputFactory(payload="pre-gate-input-opaque")
    post_gate_runner = PostGateRunner(
        result=post_gate_result
        if post_gate_result is not None
        else post_gate_pass()
    )
    post_gate_input_factory = PostGateInputFactory(payload="post-gate-input-opaque")
    hash_file = HashFile()
    context = RunPipelineContext(
        vault_read=vault_obj.read,
        vault_write=vault_obj.write,
        clock=clock,
        sleep=sleep_noop,
        run_id_factory=lambda: run_id,
        subprocess_launcher=launcher,
        seat_context_factory=context_factory,
        pre_gate_callable=pre_gate_callable,
        post_gate_runner=post_gate_runner,
        post_gate_input_factory=post_gate_input_factory,
        hash_file=hash_file,
    )
    return SubmissionHarness(
        vault=vault_obj,
        clock=clock,
        launcher=launcher,
        context_factory=context_factory,
        pre_gate_callable=pre_gate_callable,
        pre_gate_input_factory=pre_gate_input_factory,
        post_gate_runner=post_gate_runner,
        post_gate_input_factory=post_gate_input_factory,
        hash_file=hash_file,
        context=context,
    )


@dataclass
class EvalHarness:
    vault: InMemoryVault
    clock: Clock
    launcher: Launcher
    context_factory: ContextFactory
    pre_gate_callable: PreGateCallable
    pre_gate_input_factory: PreGateInputFactory
    golden_set_read: GoldenSetVaultRead
    signer: Ed25519ReferenceSigner
    pubkey_vault: PubkeyVault
    ctx: RunEvalPipelineContext
    manifest_path: str


def _post_gate_input_factory_unused(
    *, run_state: RunState, inner_loop_result: Any
) -> Any:  # pragma: no cover — eval mode never invokes POST-gate factory.
    raise AssertionError("POST-gate input factory must not fire in eval mode")


class _PostGateRunnerUnused:
    def run_post_gate(self, input_: Any) -> Any:  # pragma: no cover — ditto.
        raise AssertionError("POST-gate runner must not fire in eval mode")


def _hash_file_unused(
    path: str,
) -> str:  # pragma: no cover — eval mode never runs tab_delivery.
    raise AssertionError("hash_file must not be invoked in eval mode")


def build_eval_harness(
    *,
    run_id: str = "run-R13-eval",
    org_slug: str = "fit_farms_llc",
    pre_gate_result: PreGateResult | None = None,
    manifest_items: tuple[dict[str, Any], ...] | None = None,
    pre_existing_pubkey: bytes | None = None,
    signer: Ed25519ReferenceSigner | None = None,
    vault: InMemoryVault | None = None,
    pubkey_vault: PubkeyVault | None = None,
) -> EvalHarness:
    vault_obj = vault if vault is not None else InMemoryVault()
    clock = Clock()
    launcher = Launcher()
    context_factory = ContextFactory()
    pre_gate_callable = PreGateCallable(
        result=pre_gate_result if pre_gate_result is not None else pre_gate_pass()
    )
    pre_gate_input_factory = PreGateInputFactory(payload="pre-gate-input-opaque")

    manifest_path = f"vault/{org_slug}/golden_set/manifest.json"
    manifest_bytes = build_manifest(org_slug=org_slug, items=manifest_items)
    golden_set_read = GoldenSetVaultRead(manifests={manifest_path: manifest_bytes})

    if signer is None:
        private_key = Ed25519PrivateKey.generate()
        signer = Ed25519ReferenceSigner(private_key)

    pv = pubkey_vault if pubkey_vault is not None else PubkeyVault()
    if pre_existing_pubkey is not None:
        pv.stored[org_slug] = pre_existing_pubkey

    ctx = RunEvalPipelineContext(
        vault_read=vault_obj.read,
        vault_write=vault_obj.write,
        clock=clock,
        sleep=sleep_noop,
        run_id_factory=lambda: run_id,
        subprocess_launcher=launcher,
        seat_context_factory=context_factory,
        pre_gate_callable=pre_gate_callable,
        pre_gate_input_factory=pre_gate_input_factory,
        post_gate_runner=_PostGateRunnerUnused(),
        post_gate_input_factory=_post_gate_input_factory_unused,
        hash_file=_hash_file_unused,
        golden_set_vault_read=golden_set_read,
        realpath=realpath_identity,
        is_symlink=is_symlink_false,
        calibration_signer=signer,
        pubkey_vault_read=pv.read,
        pubkey_vault_write=pv.write,
        now_utc=now_utc_fixed,
        council_charter_snapshot_hash="a" * 64,
        router_yaml_snapshot_hash="b" * 64,
    )
    return EvalHarness(
        vault=vault_obj,
        clock=clock,
        launcher=launcher,
        context_factory=context_factory,
        pre_gate_callable=pre_gate_callable,
        pre_gate_input_factory=pre_gate_input_factory,
        golden_set_read=golden_set_read,
        signer=signer,
        pubkey_vault=pv,
        ctx=ctx,
        manifest_path=manifest_path,
    )


# ---------------------------------------------------------------------------
# Sample static RFA + PROJECT_CONTEXT bytes for R11 + R12.B integration
# ---------------------------------------------------------------------------


SAMPLE_RFA_BYTES: bytes = (
    b"# VAPG FY26 RFA (stub)\n"
    b"\n"
    b"Purpose: value-added producer grant program announcement.\n"
)


SAMPLE_PROJECT_CONTEXT_BYTES: bytes = (
    b"# PROJECT_CONTEXT (stub)\n"
    b"\n"
    b"Org: FIT Farms\n"
    b"Mission: regenerative grant intelligence\n"
)


def sample_rfa_hash() -> str:
    return hashlib.sha256(SAMPLE_RFA_BYTES).hexdigest()


def sample_project_context_hash() -> str:
    return hashlib.sha256(SAMPLE_PROJECT_CONTEXT_BYTES).hexdigest()


# ---------------------------------------------------------------------------
# Deterministic randint for BT5 (returns centre of range)
# ---------------------------------------------------------------------------


def deterministic_randint(a: int, b: int) -> int:
    """Midpoint-of-range randint — deterministic fake for BT5 jitter tests."""

    return (a + b) // 2


@dataclass
class RecordingRandInt:
    """Randint fake that records invocations for invariant assertions."""

    calls: list[tuple[int, int]] = field(default_factory=list)
    constant: int = 150

    def __call__(self, a: int, b: int) -> int:
        self.calls.append((a, b))
        # Clamp to range to satisfy Protocol contract.
        if self.constant < a:
            return a
        if self.constant > b:
            return b
        return self.constant


__all__ = [
    # Vault fakes
    "InMemoryVault",
    "SharedVault",
    # Time / sleep
    "Clock",
    "sleep_noop",
    "now_utc_fixed",
    # Seats
    "ContextFactory",
    "Launcher",
    # Gates
    "PreGateCallable",
    "PreGateInputFactory",
    "PostGateRunner",
    "PostGateInputFactory",
    "HashFile",
    # Eval-only seams
    "GoldenSetVaultRead",
    "realpath_identity",
    "is_symlink_false",
    "PubkeyVault",
    # Builders
    "make_charter",
    "make_cascade",
    "pre_gate_pass",
    "pre_gate_fail",
    "post_gate_pass",
    "post_gate_fail",
    "build_manifest",
    "DEFAULT_MANIFEST_HASH",
    "SubmissionHarness",
    "build_submission_harness",
    "EvalHarness",
    "build_eval_harness",
    # Static bytes
    "SAMPLE_RFA_BYTES",
    "SAMPLE_PROJECT_CONTEXT_BYTES",
    "sample_rfa_hash",
    "sample_project_context_hash",
    # BT5 helpers
    "deterministic_randint",
    "RecordingRandInt",
]
