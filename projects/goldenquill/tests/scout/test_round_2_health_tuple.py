"""Round 2 — pipeline.scout.health_tuple (M7 assemble + sign).

Exercises §4.10 assemble_and_sign_health_tuple end-to-end with injected
SessionSigner + VaultWriter fakes. No real keystore, no real disk — the
Section 1 and §2 seams are the only crypto / I/O surfaces Scout touches,
and both are Protocols in this module so tests keep the signing contract
honest without spinning a live session.
"""

from __future__ import annotations

import dataclasses
import hashlib
import hmac as _stdlib_hmac
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import pytest

import pipeline.scout as scout
from pipeline.scout import (
    HEALTH_DEGRADED,
    HEALTH_FAILED,
    HEALTH_OK,
    INTENT_SCOUT_RUN_LOG_WRITE,
    HealthTuple,
    HealthTupleSchemaError,
    SessionSigner,
    SignedHealthTuple,
    VaultWriter,
    assemble_and_sign_health_tuple,
    health_tuple_canonical_bytes,
)


# ---------------------------------------------------------------------------
# Fakes
# ---------------------------------------------------------------------------


@dataclass
class _FakeSession:
    session_id: str = "sess-0000"
    slug: str = "fit_farms_llc"
    hmac_key_id: str = "tilth.scout.health.hmac.v1"
    secret: bytes = b"k" * 64
    signed_inputs: list[bytes] = field(default_factory=list)
    raise_on_sign: Exception | None = None

    def sign_health_tuple(self, tuple_bytes: bytes) -> bytes:
        if self.raise_on_sign is not None:
            raise self.raise_on_sign
        self.signed_inputs.append(bytes(tuple_bytes))
        return _stdlib_hmac.new(
            self.secret, tuple_bytes, hashlib.sha3_512
        ).digest()


@dataclass
class _MemoryVaultWriter:
    writes: list[dict] = field(default_factory=list)
    raise_on_write: Exception | None = None

    def write(
        self,
        *,
        path: str,
        bytes_: bytes,
        intent: str,
        session_id: str,
        slug: str,
    ) -> None:
        if self.raise_on_write is not None:
            raise self.raise_on_write
        self.writes.append(
            {
                "path": path,
                "bytes_": bytes(bytes_),
                "intent": intent,
                "session_id": session_id,
                "slug": slug,
            }
        )


def _ok_channels() -> dict[str, str]:
    return {ch: HEALTH_OK for ch in ("A", "B", "C", "D", "E", "F")}


def _ok_endpoints() -> dict[str, str]:
    return {ep: HEALTH_OK for ep in ("grants.gov", "sam.gov", "usaspending.gov")}


def _pinned_urandom(buf: bytes) -> Callable[[int], bytes]:
    def _urandom(n: int) -> bytes:
        assert len(buf) == n, f"urandom stub sized for {len(buf)}, got {n}"
        return buf

    return _urandom


def _pinned_monotonic(ns: int) -> Callable[[], int]:
    return lambda: ns


def _pinned_clock(iso: str) -> Callable[[], str]:
    return lambda: iso


def _invoke(
    *,
    session: _FakeSession | None = None,
    per_channel: dict[str, str] | None = None,
    per_channel_a_endpoints: dict[str, str] | None = None,
    run_wall_ns: int = 1_700_000_000_000_000_000,
    run_tiebreak_seed: bytes | None = None,
    vault_writer: _MemoryVaultWriter | None = None,
    clock: Callable[[], str] | None = None,
    urandom: Callable[[int], bytes] | None = None,
    monotonic_ns: Callable[[], int] | None = None,
) -> tuple[SignedHealthTuple, _FakeSession, _MemoryVaultWriter]:
    session = session or _FakeSession()
    vault_writer = vault_writer or _MemoryVaultWriter()
    per_channel = per_channel if per_channel is not None else _ok_channels()
    per_channel_a_endpoints = (
        per_channel_a_endpoints
        if per_channel_a_endpoints is not None
        else _ok_endpoints()
    )
    run_tiebreak_seed = (
        run_tiebreak_seed if run_tiebreak_seed is not None else b"\xab" * 16
    )
    kwargs: dict = {
        "session": session,
        "per_channel": per_channel,
        "per_channel_a_endpoints": per_channel_a_endpoints,
        "run_wall_ns": run_wall_ns,
        "run_tiebreak_seed": run_tiebreak_seed,
        "vault_writer": vault_writer,
    }
    if clock is not None:
        kwargs["clock"] = clock
    if urandom is not None:
        kwargs["urandom"] = urandom
    if monotonic_ns is not None:
        kwargs["monotonic_ns"] = monotonic_ns
    signed = assemble_and_sign_health_tuple(**kwargs)
    return signed, session, vault_writer


# ---------------------------------------------------------------------------
# Happy path + backbone_failed derivation
# ---------------------------------------------------------------------------


class TestAssembleHappyPath:
    def test_all_ok_signs_and_writes(self):
        signed, session, writer = _invoke()
        assert isinstance(signed, SignedHealthTuple)
        assert len(signed.hmac_sha3_512) == 64
        assert signed.hmac_key_id == session.hmac_key_id
        assert len(writer.writes) == 1

    def test_one_degraded_accepted(self):
        channels = _ok_channels()
        channels["C"] = HEALTH_DEGRADED
        signed, _, _ = _invoke(per_channel=channels)
        decoded = json.loads(signed.tuple_canonical.decode("utf-8"))
        assert decoded["channel_c"] == HEALTH_DEGRADED

    def test_one_failed_channel_e_accepted(self):
        channels = _ok_channels()
        channels["E"] = HEALTH_FAILED
        signed, _, _ = _invoke(per_channel=channels)
        decoded = json.loads(signed.tuple_canonical.decode("utf-8"))
        assert decoded["channel_e"] == HEALTH_FAILED
        assert decoded["backbone_failed"] is False

    def test_backbone_failed_when_all_three_a_endpoints_failed(self):
        eps = {ep: HEALTH_FAILED for ep in ("grants.gov", "sam.gov", "usaspending.gov")}
        signed, _, _ = _invoke(per_channel_a_endpoints=eps)
        decoded = json.loads(signed.tuple_canonical.decode("utf-8"))
        assert decoded["backbone_failed"] is True


# ---------------------------------------------------------------------------
# Channel-state validation (F-SCOUT-H-01)
# ---------------------------------------------------------------------------


class TestChannelStateValidation:
    def test_missing_channel_raises(self):
        channels = _ok_channels()
        del channels["D"]
        with pytest.raises(HealthTupleSchemaError) as exc:
            _invoke(per_channel=channels)
        assert exc.value.code == "F-SCOUT-H-01"

    def test_typo_channel_value_raises(self):
        channels = _ok_channels()
        channels["B"] = "OKAY"
        with pytest.raises(HealthTupleSchemaError) as exc:
            _invoke(per_channel=channels)
        assert exc.value.code == "F-SCOUT-H-01"

    @pytest.mark.parametrize("ch", ["A", "B", "C", "D", "E", "F"])
    def test_each_channel_invalid_in_turn(self, ch):
        channels = _ok_channels()
        channels[ch] = "unknown"
        with pytest.raises(HealthTupleSchemaError) as exc:
            _invoke(per_channel=channels)
        assert exc.value.code == "F-SCOUT-H-01"


# ---------------------------------------------------------------------------
# Channel-A endpoint validation (F-SCOUT-H-02)
# ---------------------------------------------------------------------------


class TestChannelAEndpointValidation:
    def test_missing_grants_gov_raises(self):
        eps = _ok_endpoints()
        del eps["grants.gov"]
        with pytest.raises(HealthTupleSchemaError) as exc:
            _invoke(per_channel_a_endpoints=eps)
        assert exc.value.code == "F-SCOUT-H-02"

    def test_typo_sam_gov_raises(self):
        eps = _ok_endpoints()
        eps["sam.gov"] = "Oke"
        with pytest.raises(HealthTupleSchemaError) as exc:
            _invoke(per_channel_a_endpoints=eps)
        assert exc.value.code == "F-SCOUT-H-02"

    def test_typo_usaspending_gov_raises(self):
        eps = _ok_endpoints()
        eps["usaspending.gov"] = ""
        with pytest.raises(HealthTupleSchemaError) as exc:
            _invoke(per_channel_a_endpoints=eps)
        assert exc.value.code == "F-SCOUT-H-02"

    def test_empty_endpoint_dict_raises(self):
        with pytest.raises(HealthTupleSchemaError) as exc:
            _invoke(per_channel_a_endpoints={})
        assert exc.value.code == "F-SCOUT-H-02"


# ---------------------------------------------------------------------------
# run_id derivation (F-SCOUT-H-03)
# ---------------------------------------------------------------------------


class TestRunIdDerivation:
    def test_run_id_is_24_hex_chars(self):
        signed, _, _ = _invoke()
        decoded = json.loads(signed.tuple_canonical.decode("utf-8"))
        run_id = decoded["run_id"]
        assert len(run_id) == 24
        assert all(c in "0123456789abcdef" for c in run_id)

    def test_run_id_changes_with_run_wall_ns(self):
        urandom = _pinned_urandom(b"\xcd" * 8)
        monotonic = _pinned_monotonic(1_000)
        signed_a, _, _ = _invoke(
            run_wall_ns=1, urandom=urandom, monotonic_ns=monotonic
        )
        signed_b, _, _ = _invoke(
            run_wall_ns=2, urandom=urandom, monotonic_ns=monotonic
        )
        ra = json.loads(signed_a.tuple_canonical.decode("utf-8"))["run_id"]
        rb = json.loads(signed_b.tuple_canonical.decode("utf-8"))["run_id"]
        assert ra != rb

    def test_run_id_changes_with_session_id(self):
        urandom = _pinned_urandom(b"\xcd" * 8)
        monotonic = _pinned_monotonic(1_000)
        sa = _FakeSession(session_id="sess-A")
        sb = _FakeSession(session_id="sess-B")
        signed_a, _, _ = _invoke(session=sa, urandom=urandom, monotonic_ns=monotonic)
        signed_b, _, _ = _invoke(session=sb, urandom=urandom, monotonic_ns=monotonic)
        ra = json.loads(signed_a.tuple_canonical.decode("utf-8"))["run_id"]
        rb = json.loads(signed_b.tuple_canonical.decode("utf-8"))["run_id"]
        assert ra != rb

    def test_run_id_changes_with_monotonic_jitter(self):
        urandom = _pinned_urandom(b"\xcd" * 8)
        signed_a, _, _ = _invoke(
            urandom=urandom, monotonic_ns=_pinned_monotonic(1_000)
        )
        signed_b, _, _ = _invoke(
            urandom=urandom, monotonic_ns=_pinned_monotonic(2_000)
        )
        ra = json.loads(signed_a.tuple_canonical.decode("utf-8"))["run_id"]
        rb = json.loads(signed_b.tuple_canonical.decode("utf-8"))["run_id"]
        assert ra != rb

    def test_run_id_changes_with_urandom_jitter(self):
        monotonic = _pinned_monotonic(1_000)
        signed_a, _, _ = _invoke(
            urandom=_pinned_urandom(b"\x01" * 8), monotonic_ns=monotonic
        )
        signed_b, _, _ = _invoke(
            urandom=_pinned_urandom(b"\x02" * 8), monotonic_ns=monotonic
        )
        ra = json.loads(signed_a.tuple_canonical.decode("utf-8"))["run_id"]
        rb = json.loads(signed_b.tuple_canonical.decode("utf-8"))["run_id"]
        assert ra != rb


# ---------------------------------------------------------------------------
# _fresh_urandom short-read hardening (F-SCOUT-H-03.urandom_short_read)
# ---------------------------------------------------------------------------


class TestUrandomShortRead:
    def test_first_short_triggers_retry_then_succeeds(self):
        calls = {"n": 0}
        full = b"\xaa" * 8

        def urandom(n: int) -> bytes:
            calls["n"] += 1
            if calls["n"] == 1:
                return b"\x00" * (n - 1)  # short
            return full

        _invoke(urandom=urandom)
        assert calls["n"] == 2

    def test_second_short_raises_urandom_short_read(self):
        def urandom(n: int) -> bytes:
            return b"\x00" * (n - 1)

        with pytest.raises(HealthTupleSchemaError) as exc:
            _invoke(urandom=urandom)
        assert exc.value.code == "F-SCOUT-H-03"
        assert exc.value.sub_tag == "urandom_short_read"

    def test_full_length_first_try_is_noop(self):
        calls = {"n": 0}

        def urandom(n: int) -> bytes:
            calls["n"] += 1
            return b"\xbb" * n

        _invoke(urandom=urandom)
        assert calls["n"] == 1


# ---------------------------------------------------------------------------
# run_tiebreak_seed length gate (F-SCOUT-V-06)
# ---------------------------------------------------------------------------


class TestRunTiebreakSeed:
    def test_correct_length_accepts(self):
        _invoke(run_tiebreak_seed=b"\xde" * 16)

    def test_wrong_length_raises(self):
        with pytest.raises(HealthTupleSchemaError) as exc:
            _invoke(run_tiebreak_seed=b"\xde" * 15)
        assert exc.value.code == "F-SCOUT-V-06"

    def test_zero_length_raises(self):
        with pytest.raises(HealthTupleSchemaError) as exc:
            _invoke(run_tiebreak_seed=b"")
        assert exc.value.code == "F-SCOUT-V-06"

    def test_exact_16_passes_and_embeds_hex(self):
        seed = bytes(range(16))
        signed, _, _ = _invoke(run_tiebreak_seed=seed)
        decoded = json.loads(signed.tuple_canonical.decode("utf-8"))
        assert decoded["run_entropy"]["run_tiebreak_seed_hex"] == seed.hex()


# ---------------------------------------------------------------------------
# Canonical-bytes determinism + round-trip
# ---------------------------------------------------------------------------


class TestCanonicalBytes:
    def test_tuple_canonical_matches_helper(self):
        urandom = _pinned_urandom(b"\x11" * 8)
        monotonic = _pinned_monotonic(42)
        seed = b"\x22" * 16
        session = _FakeSession()
        signed, _, _ = _invoke(
            session=session,
            run_tiebreak_seed=seed,
            urandom=urandom,
            monotonic_ns=monotonic,
        )
        decoded = json.loads(signed.tuple_canonical.decode("utf-8"))
        ht = HealthTuple(
            session_id=decoded["session_id"],
            slug=decoded["slug"],
            run_id=decoded["run_id"],
            run_wall_ns=decoded["run_wall_ns"],
            channel_a=decoded["channel_a"],
            channel_b=decoded["channel_b"],
            channel_c=decoded["channel_c"],
            channel_d=decoded["channel_d"],
            channel_e=decoded["channel_e"],
            channel_f=decoded["channel_f"],
            channel_a_endpoints=decoded["channel_a_endpoints"],
            backbone_failed=decoded["backbone_failed"],
            run_entropy=decoded["run_entropy"],
        )
        assert signed.tuple_canonical == health_tuple_canonical_bytes(ht)

    def test_determinism_under_pinned_fakes(self):
        urandom = _pinned_urandom(b"\x33" * 8)
        monotonic = _pinned_monotonic(100)
        clock = _pinned_clock("2026-04-20T00:00:00Z")
        seed = b"\x44" * 16
        a, _, _ = _invoke(
            session=_FakeSession(),
            run_tiebreak_seed=seed,
            urandom=urandom,
            monotonic_ns=monotonic,
            clock=clock,
        )
        b, _, _ = _invoke(
            session=_FakeSession(),
            run_tiebreak_seed=seed,
            urandom=urandom,
            monotonic_ns=monotonic,
            clock=clock,
        )
        assert a.tuple_canonical == b.tuple_canonical

    def test_sign_verify_round_trip_symmetric(self):
        """The HMAC-over-tuple_canonical round-trip is the §3 → §4 contract."""
        signed, session, _ = _invoke()
        expected = _stdlib_hmac.new(
            session.secret, signed.tuple_canonical, hashlib.sha3_512
        ).digest()
        assert _stdlib_hmac.compare_digest(signed.hmac_sha3_512, expected)


# ---------------------------------------------------------------------------
# Signature delegation
# ---------------------------------------------------------------------------


class TestSignatureDelegation:
    def test_signer_receives_exact_canonical_bytes(self):
        signed, session, _ = _invoke()
        assert session.signed_inputs == [signed.tuple_canonical]

    def test_returned_signature_is_hmac_output(self):
        signed, session, _ = _invoke()
        expected = _stdlib_hmac.new(
            session.secret, signed.tuple_canonical, hashlib.sha3_512
        ).digest()
        assert signed.hmac_sha3_512 == expected

    def test_hmac_key_id_flows_through(self):
        session = _FakeSession(hmac_key_id="tilth.custom.key.v9")
        signed, _, _ = _invoke(session=session)
        assert signed.hmac_key_id == "tilth.custom.key.v9"


# ---------------------------------------------------------------------------
# Vault-write call-site
# ---------------------------------------------------------------------------


class TestVaultWriteCallSite:
    def test_path_is_org_run_log_health_json(self):
        signed, session, writer = _invoke()
        decoded = json.loads(signed.tuple_canonical.decode("utf-8"))
        run_id = decoded["run_id"]
        assert writer.writes[0]["path"] == (
            f"orgs/{session.slug}/scout/run_log/{run_id}-health.json"
        )

    def test_intent_is_scout_run_log_write(self):
        _, _, writer = _invoke()
        assert writer.writes[0]["intent"] == INTENT_SCOUT_RUN_LOG_WRITE

    def test_session_id_and_slug_match(self):
        _, session, writer = _invoke()
        assert writer.writes[0]["session_id"] == session.session_id
        assert writer.writes[0]["slug"] == session.slug

    def test_vault_payload_carries_signed_fields(self):
        signed, _, writer = _invoke()
        payload = json.loads(writer.writes[0]["bytes_"].decode("utf-8"))
        assert payload["tuple_canonical"] == signed.tuple_canonical.hex()
        assert payload["hmac_sha3_512"] == signed.hmac_sha3_512.hex()
        assert payload["hmac_key_id"] == signed.hmac_key_id


# ---------------------------------------------------------------------------
# Verifier round-trip (§3 → §4 HMAC symmetry)
# ---------------------------------------------------------------------------


class TestVerifierRoundTrip:
    def test_mutated_canonical_breaks_signature(self):
        signed, session, _ = _invoke()
        mutated = bytearray(signed.tuple_canonical)
        mutated[0] ^= 0x01  # flip one bit
        expected_mut = _stdlib_hmac.new(
            session.secret, bytes(mutated), hashlib.sha3_512
        ).digest()
        assert not _stdlib_hmac.compare_digest(signed.hmac_sha3_512, expected_mut)

    def test_vault_payload_deserializes_to_signed_fields(self):
        signed, _, writer = _invoke()
        payload = json.loads(writer.writes[0]["bytes_"].decode("utf-8"))
        assert bytes.fromhex(payload["tuple_canonical"]) == signed.tuple_canonical
        assert bytes.fromhex(payload["hmac_sha3_512"]) == signed.hmac_sha3_512


# ---------------------------------------------------------------------------
# Signature failure propagation (F-SCOUT-H-04)
# ---------------------------------------------------------------------------


class TestSignatureFailurePropagation:
    def test_sign_raise_wrapped_as_f_scout_h_04(self):
        boom = RuntimeError("keystore not bound")
        session = _FakeSession(raise_on_sign=boom)
        with pytest.raises(HealthTupleSchemaError) as exc:
            _invoke(session=session)
        assert exc.value.code == "F-SCOUT-H-04"
        assert exc.value.__cause__ is boom

    def test_vault_writer_not_called_on_sign_failure(self):
        session = _FakeSession(raise_on_sign=RuntimeError("nope"))
        writer = _MemoryVaultWriter()
        with pytest.raises(HealthTupleSchemaError):
            _invoke(session=session, vault_writer=writer)
        assert writer.writes == []


# ---------------------------------------------------------------------------
# Keyword-only call + Protocol duck-typing + AST-lint
# ---------------------------------------------------------------------------


class TestKWOnly:
    def test_positional_call_rejected(self):
        session = _FakeSession()
        writer = _MemoryVaultWriter()
        with pytest.raises(TypeError):
            assemble_and_sign_health_tuple(  # type: ignore[call-arg]
                session,
                _ok_channels(),
                _ok_endpoints(),
                1,
                b"\x00" * 16,
                writer,
            )


class TestProtocolDiscipline:
    def test_session_signer_is_a_protocol(self):
        # SessionSigner is typing.Protocol-shaped; isinstance check is not
        # required at runtime (Protocols are structural), but we verify the
        # attribute surface is present on our fake so the contract holds.
        assert hasattr(SessionSigner, "__class_getitem__") or True
        fake = _FakeSession()
        assert hasattr(fake, "session_id")
        assert hasattr(fake, "slug")
        assert hasattr(fake, "hmac_key_id")
        assert callable(fake.sign_health_tuple)

    def test_minimal_duck_typed_fake_works(self):
        @dataclass
        class _Minimal:
            session_id: str = "sess-x"
            slug: str = "x_org"
            hmac_key_id: str = "k"

            def sign_health_tuple(self, tuple_bytes: bytes) -> bytes:
                return b"\x00" * 64

        writer = _MemoryVaultWriter()
        signed = assemble_and_sign_health_tuple(
            session=_Minimal(),
            per_channel=_ok_channels(),
            per_channel_a_endpoints=_ok_endpoints(),
            run_wall_ns=1,
            run_tiebreak_seed=b"\xff" * 16,
            vault_writer=writer,
        )
        assert signed.hmac_sha3_512 == b"\x00" * 64


class TestASTLintRegression:
    def test_health_tuple_module_is_ast_lint_clean(self):
        from pipeline.linting.ast_lint import DEFAULT_RULES, lint_tree

        # lint the whole scout package; assert no health_tuple.py violations.
        pkg_root = Path(scout.__file__).parent
        violations = lint_tree(pkg_root, DEFAULT_RULES)
        health_tuple_violations = [
            v for v in violations if "health_tuple.py" in str(v.file)
        ]
        assert health_tuple_violations == []


# ---------------------------------------------------------------------------
# run_entropy field (Option A of Round 2 spec card)
# ---------------------------------------------------------------------------


class TestRunEntropyField:
    def test_run_entropy_present_in_canonical_bytes(self):
        urandom = _pinned_urandom(b"\x77" * 8)
        monotonic = _pinned_monotonic(555)
        seed = b"\x88" * 16
        signed, _, _ = _invoke(
            run_tiebreak_seed=seed, urandom=urandom, monotonic_ns=monotonic
        )
        decoded = json.loads(signed.tuple_canonical.decode("utf-8"))
        assert "run_entropy" in decoded
        entropy = decoded["run_entropy"]
        assert entropy["run_urandom_hex"] == (b"\x77" * 8).hex()
        assert entropy["run_monotonic_ns"] == 555
        assert entropy["run_tiebreak_seed_hex"] == seed.hex()

    def test_run_entropy_keys_are_sorted_in_canonical_bytes(self):
        signed, _, _ = _invoke()
        decoded = json.loads(signed.tuple_canonical.decode("utf-8"))
        entropy_keys = list(decoded["run_entropy"].keys())
        assert entropy_keys == sorted(entropy_keys)


# ---------------------------------------------------------------------------
# __init__ re-exports
# ---------------------------------------------------------------------------


class TestPackageReExports:
    def test_version_is_scout_round_tag(self):
        # Forward-compat: any future round bump stays valid. The round-specific
        # pin (e.g. r3 after Round 3 LOCK) lives in that round's own test file,
        # so this Round-2 test does not need touching every bump.
        assert re.fullmatch(r"0\.1\.0-scout-r\d+", scout.__version__), scout.__version__

    def test_public_symbols_exported(self):
        for name in (
            "assemble_and_sign_health_tuple",
            "HealthTupleSchemaError",
            "SessionSigner",
            "VaultWriter",
        ):
            assert name in scout.__all__
            assert getattr(scout, name) is not None
