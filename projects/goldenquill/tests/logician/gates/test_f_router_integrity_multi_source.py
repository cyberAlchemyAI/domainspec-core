"""Unit tests for F-ROUTER-INTEGRITY-MULTI-SOURCE (F-AMDT-10)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from typing import Optional

import pytest

from pipeline.logician.gates.f_router_integrity_multi_source import (
    F_AMDT_10,
    F_AMDT_10_CHAIN_BREAK,
    F_AMDT_10_EXTERNAL,
    F_AMDT_10_PAIR,
    F_AMDT_10_READER_FAIL,
    F_AMDT_10_SIGNATURE,
    RouterIntegrityDetail,
    RouterIntegrityResult,
    check_router_integrity_multi_source,
)


# ---------------------------------------------------------------------------
# Fakes
# ---------------------------------------------------------------------------


class _HashFn:
    """Deterministic fake hash — returns canonical-hex-like string."""

    def __init__(self, mapping: Optional[dict] = None):
        self._map = mapping or {}

    def __call__(self, data: bytes) -> str:
        if data in self._map:
            return self._map[data]
        # Stable fake — hex of a rolling sum per byte.
        return "".join(f"{b:02x}" for b in data)[:128] or "emptyhash"


class _StaticVerifier:
    def __init__(self, *, result: object = True, raises: Optional[BaseException] = None):
        self._result = result
        self._raises = raises
        self.calls: list[tuple[bytes, bytes, bytes]] = []

    def __call__(self, payload: bytes, signature: bytes, public_key: bytes) -> bool:
        self.calls.append((payload, signature, public_key))
        if self._raises is not None:
            raise self._raises
        return self._result  # type: ignore[return-value]


def _make_manifest(
    *,
    chain_head_hash: str,
    prior_chain_head_hash: str,
    signature: bytes = b"sig",
    signed_payload_bytes: bytes = b"payload",
    extra: Optional[dict] = None,
) -> dict:
    d: dict = {
        "chain_head_hash": chain_head_hash,
        "prior_chain_head_hash": prior_chain_head_hash,
        "signature": signature,
        "signed_payload_bytes": signed_payload_bytes,
    }
    if extra:
        d.update(extra)
    return d


def _router_reader(data: bytes):
    def _r() -> bytes:
        return data
    return _r


def _pinned_reader(hash_value: str, *, override: Optional[dict] = None):
    def _r() -> dict:
        return override if override is not None else {"router_yaml_sha3_512": hash_value}
    return _r


def _manifest_reader(manifest: dict):
    def _r() -> dict:
        return manifest
    return _r


def _prior_reader(value: Optional[str]):
    def _r() -> Optional[str]:
        return value
    return _r


# ---------------------------------------------------------------------------
# Happy paths
# ---------------------------------------------------------------------------


def test_all_three_sources_agree_with_valid_sig_and_prior_link_passes():
    yaml = b"router: yaml: here"
    live = "".join(f"{b:02x}" for b in yaml)[:128]
    manifest = _make_manifest(chain_head_hash=live, prior_chain_head_hash="priorhash")
    verifier = _StaticVerifier(result=True)
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(yaml),
        pinned_hash_reader=_pinned_reader(live),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_prior_reader("priorhash"),
        signature_verify=verifier,
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is True
    assert r.failure_code is None
    assert r.detail is not None
    assert r.detail.reason_tag == "ok"
    assert r.detail.check_failed == ""
    assert r.detail.live_hash == live
    assert r.detail.pinned_hash == live
    assert r.detail.manifest_chain_head == live
    assert r.detail.reader_error is None
    assert len(verifier.calls) == 1
    assert verifier.calls[0] == (b"payload", b"sig", b"pk")


def test_bootstrap_row_prior_empty_string_and_prior_reader_none_passes():
    yaml = b"bootstrap router"
    live = "".join(f"{b:02x}" for b in yaml)[:128]
    manifest = _make_manifest(chain_head_hash=live, prior_chain_head_hash="")
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(yaml),
        pinned_hash_reader=_pinned_reader(live),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is True


def test_happy_path_ignores_extra_manifest_fields():
    yaml = b"abc"
    live = "".join(f"{b:02x}" for b in yaml)[:128]
    manifest = _make_manifest(
        chain_head_hash=live,
        prior_chain_head_hash="p",
        extra={"author": "ops", "timestamp": "2026-04-21"},
    )
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(yaml),
        pinned_hash_reader=_pinned_reader(live),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_prior_reader("p"),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# Pair mismatch (Check 1)
# ---------------------------------------------------------------------------


def test_live_hash_mismatches_pinned_denies_pair():
    yaml = b"hello"
    manifest = _make_manifest(chain_head_hash="ignored", prior_chain_head_hash="")
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(yaml),
        pinned_hash_reader=_pinned_reader("totally-different-hash"),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_10_PAIR
    assert r.detail.check_failed == "pair"
    assert r.detail.reason_tag == "live_hash_mismatches_pinned"


# ---------------------------------------------------------------------------
# External mismatch (Check 2)
# ---------------------------------------------------------------------------


def test_manifest_chain_head_mismatches_live_denies_external():
    yaml = b"router"
    live = "".join(f"{b:02x}" for b in yaml)[:128]
    manifest = _make_manifest(chain_head_hash="different-head", prior_chain_head_hash="")
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(yaml),
        pinned_hash_reader=_pinned_reader(live),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_10_EXTERNAL
    assert r.detail.check_failed == "external"
    assert r.detail.reason_tag == "manifest_chain_head_mismatches_live"


# ---------------------------------------------------------------------------
# Signature failures (Check 3)
# ---------------------------------------------------------------------------


def test_signature_verify_returns_false_denies_signature():
    yaml = b"r"
    live = "".join(f"{b:02x}" for b in yaml)[:128]
    manifest = _make_manifest(chain_head_hash=live, prior_chain_head_hash="")
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(yaml),
        pinned_hash_reader=_pinned_reader(live),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=False),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_10_SIGNATURE
    assert r.detail.check_failed == "signature"


@pytest.mark.parametrize("truthy", [1, "True", [1], (1,), object()])
def test_signature_verify_truthy_not_True_denies_signature(truthy):
    yaml = b"r"
    live = "".join(f"{b:02x}" for b in yaml)[:128]
    manifest = _make_manifest(chain_head_hash=live, prior_chain_head_hash="")
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(yaml),
        pinned_hash_reader=_pinned_reader(live),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=truthy),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_10_SIGNATURE


def test_signature_verify_raises_fail_closed():
    yaml = b"r"
    live = "".join(f"{b:02x}" for b in yaml)[:128]
    manifest = _make_manifest(chain_head_hash=live, prior_chain_head_hash="")
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(yaml),
        pinned_hash_reader=_pinned_reader(live),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(raises=RuntimeError("crypto engine offline")),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_10_READER_FAIL
    assert r.detail.check_failed == "reader_fail"
    assert r.detail.reason_tag == "signature_verify_raised"
    assert r.detail.reader_error is not None
    assert "signature_verify:" in r.detail.reader_error
    assert "RuntimeError" in r.detail.reader_error


# ---------------------------------------------------------------------------
# Chain-break failures (Check 4)
# ---------------------------------------------------------------------------


def test_bootstrap_with_nonempty_prior_denies_chain_break():
    yaml = b"boot"
    live = "".join(f"{b:02x}" for b in yaml)[:128]
    manifest = _make_manifest(chain_head_hash=live, prior_chain_head_hash="somehash")
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(yaml),
        pinned_hash_reader=_pinned_reader(live),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_10_CHAIN_BREAK
    assert r.detail.check_failed == "chain_break"
    assert r.detail.reason_tag == "bootstrap_prior_chain_head_hash_nonempty"


def test_prior_hash_mismatches_reader_denies_chain_break():
    yaml = b"r"
    live = "".join(f"{b:02x}" for b in yaml)[:128]
    manifest = _make_manifest(chain_head_hash=live, prior_chain_head_hash="claimed-prior")
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(yaml),
        pinned_hash_reader=_pinned_reader(live),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_prior_reader("actual-prior"),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_10_CHAIN_BREAK
    assert r.detail.reason_tag == "prior_chain_head_hash_mismatches_prior_reader"


# ---------------------------------------------------------------------------
# Reader-raise fail-closed (parametrized)
# ---------------------------------------------------------------------------


class _Raiser:
    def __init__(self, exc: BaseException):
        self._exc = exc

    def __call__(self, *args, **kwargs):
        raise self._exc


@pytest.mark.parametrize("exc", [
    ValueError("v"),
    RuntimeError("r"),
    OSError("o"),
    KeyError("k"),
    TypeError("t"),
    IndexError("i"),
])
def test_router_yaml_reader_raises_fail_closed(exc):
    r = check_router_integrity_multi_source(
        router_yaml_reader=_Raiser(exc),
        pinned_hash_reader=_pinned_reader("x"),
        external_manifest_reader=_manifest_reader(_make_manifest(chain_head_hash="x", prior_chain_head_hash="")),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_10_READER_FAIL
    assert r.detail.reason_tag == "router_yaml_reader_raised"
    assert r.detail.reader_error is not None
    assert "router_yaml_reader:" in r.detail.reader_error


@pytest.mark.parametrize("exc", [ValueError("v"), RuntimeError("r")])
def test_hash_bytes_raises_fail_closed(exc):
    class H:
        def __call__(self, data: bytes) -> str:
            raise exc
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(b"x"),
        pinned_hash_reader=_pinned_reader("x"),
        external_manifest_reader=_manifest_reader(_make_manifest(chain_head_hash="x", prior_chain_head_hash="")),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=H(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_10_READER_FAIL
    assert r.detail.reason_tag == "hash_bytes_raised"


@pytest.mark.parametrize("exc", [ValueError("v"), RuntimeError("r"), OSError("o")])
def test_pinned_hash_reader_raises_fail_closed(exc):
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(b"x"),
        pinned_hash_reader=_Raiser(exc),
        external_manifest_reader=_manifest_reader(_make_manifest(chain_head_hash="x", prior_chain_head_hash="")),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_10_READER_FAIL
    assert r.detail.reason_tag == "pinned_hash_reader_raised"


@pytest.mark.parametrize("exc", [ValueError("v"), RuntimeError("r"), OSError("o")])
def test_external_manifest_reader_raises_fail_closed(exc):
    yaml = b"x"
    live = "".join(f"{b:02x}" for b in yaml)[:128]
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(yaml),
        pinned_hash_reader=_pinned_reader(live),
        external_manifest_reader=_Raiser(exc),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_10_READER_FAIL
    assert r.detail.reason_tag == "external_manifest_reader_raised"


@pytest.mark.parametrize("exc", [ValueError("v"), RuntimeError("r")])
def test_prior_chain_head_reader_raises_fail_closed(exc):
    yaml = b"x"
    live = "".join(f"{b:02x}" for b in yaml)[:128]
    manifest = _make_manifest(chain_head_hash=live, prior_chain_head_hash="p")
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(yaml),
        pinned_hash_reader=_pinned_reader(live),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_Raiser(exc),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_10_READER_FAIL
    assert r.detail.reason_tag == "prior_chain_head_reader_raised"


# ---------------------------------------------------------------------------
# Structural input validation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("bad_pk", [None, "str", 123, [1]])
def test_public_key_not_bytes_denies_reader_fail(bad_pk):
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(b"x"),
        pinned_hash_reader=_pinned_reader("x"),
        external_manifest_reader=_manifest_reader(_make_manifest(chain_head_hash="x", prior_chain_head_hash="")),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=bad_pk,  # type: ignore[arg-type]
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_10_READER_FAIL
    assert r.detail.reason_tag == "public_key_not_bytes"


@pytest.mark.parametrize("bad_yaml", ["str", 1, None, [1]])
def test_router_yaml_not_bytes_denies(bad_yaml):
    def reader():
        return bad_yaml
    r = check_router_integrity_multi_source(
        router_yaml_reader=reader,
        pinned_hash_reader=_pinned_reader("x"),
        external_manifest_reader=_manifest_reader(_make_manifest(chain_head_hash="x", prior_chain_head_hash="")),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.detail.reason_tag == "router_yaml_not_bytes"


@pytest.mark.parametrize("bad_hash_return", [None, 123, b"bytes", [1]])
def test_hash_bytes_non_str_denies(bad_hash_return):
    class H:
        def __call__(self, data: bytes):
            return bad_hash_return
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(b"x"),
        pinned_hash_reader=_pinned_reader("x"),
        external_manifest_reader=_manifest_reader(_make_manifest(chain_head_hash="x", prior_chain_head_hash="")),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=H(),  # type: ignore[arg-type]
        public_key=b"pk",
    )
    assert r.success is False
    assert r.detail.reason_tag == "live_hash_not_str"


def test_hash_bytes_empty_string_denies():
    class H:
        def __call__(self, data: bytes) -> str:
            return ""
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(b"x"),
        pinned_hash_reader=_pinned_reader("x"),
        external_manifest_reader=_manifest_reader(_make_manifest(chain_head_hash="x", prior_chain_head_hash="")),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=H(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.detail.reason_tag == "live_hash_empty"


@pytest.mark.parametrize("bad_pinned", ["str", 1, None, [1]])
def test_pinned_not_dict_denies(bad_pinned):
    def reader():
        return bad_pinned
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(b"x"),
        pinned_hash_reader=reader,
        external_manifest_reader=_manifest_reader(_make_manifest(chain_head_hash="x", prior_chain_head_hash="")),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.detail.reason_tag == "pinned_hash_not_dict"


@pytest.mark.parametrize("override", [
    {},
    {"other_field": "x"},
    {"router_yaml_sha3_512": ""},
    {"router_yaml_sha3_512": None},
    {"router_yaml_sha3_512": 123},
    {"router_yaml_sha3_512": b"bytes"},
])
def test_pinned_field_missing_or_bad_denies(override):
    def reader():
        return override
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(b"x"),
        pinned_hash_reader=reader,
        external_manifest_reader=_manifest_reader(_make_manifest(chain_head_hash="x", prior_chain_head_hash="")),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.detail.reason_tag == "pinned_router_yaml_sha3_512_missing_or_empty"


@pytest.mark.parametrize("bad_manifest", ["str", 1, None, [1]])
def test_manifest_not_dict_denies(bad_manifest):
    def reader():
        return bad_manifest
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(b"x"),
        pinned_hash_reader=_pinned_reader("x"),
        external_manifest_reader=reader,
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.detail.reason_tag == "external_manifest_not_dict"


@pytest.mark.parametrize("head", [None, "", 123, b"bytes", [1]])
def test_manifest_chain_head_missing_denies(head):
    manifest = {
        "chain_head_hash": head,
        "prior_chain_head_hash": "",
        "signature": b"sig",
        "signed_payload_bytes": b"p",
    }
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(b"x"),
        pinned_hash_reader=_pinned_reader("x"),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.detail.reason_tag == "manifest_chain_head_hash_missing_or_empty"


@pytest.mark.parametrize("sig", [None, "str", 123, [1]])
def test_manifest_signature_not_bytes_denies(sig):
    manifest = {
        "chain_head_hash": "x",
        "prior_chain_head_hash": "",
        "signature": sig,
        "signed_payload_bytes": b"p",
    }
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(b"x"),
        pinned_hash_reader=_pinned_reader("x"),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.detail.reason_tag == "manifest_signature_not_bytes"


@pytest.mark.parametrize("payload", [None, "str", 123, [1]])
def test_manifest_payload_not_bytes_denies(payload):
    manifest = {
        "chain_head_hash": "x",
        "prior_chain_head_hash": "",
        "signature": b"sig",
        "signed_payload_bytes": payload,
    }
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(b"x"),
        pinned_hash_reader=_pinned_reader("x"),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.detail.reason_tag == "manifest_signed_payload_bytes_not_bytes"


@pytest.mark.parametrize("prior", [None, 123, b"bytes", [1]])
def test_manifest_prior_not_str_denies(prior):
    manifest = {
        "chain_head_hash": "x",
        "prior_chain_head_hash": prior,
        "signature": b"sig",
        "signed_payload_bytes": b"p",
    }
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(b"x"),
        pinned_hash_reader=_pinned_reader("x"),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.detail.reason_tag == "manifest_prior_chain_head_hash_not_str"


@pytest.mark.parametrize("bad_prior", [123, b"bytes", [1], {"x": 1}])
def test_prior_reader_return_not_str_or_none_denies(bad_prior):
    def reader():
        return bad_prior
    yaml = b"x"
    live = "".join(f"{b:02x}" for b in yaml)[:128]
    manifest = _make_manifest(chain_head_hash=live, prior_chain_head_hash="p")
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(yaml),
        pinned_hash_reader=_pinned_reader(live),
        external_manifest_reader=_manifest_reader(manifest),
        prior_chain_head_reader=reader,  # type: ignore[arg-type]
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    assert r.success is False
    assert r.detail.reason_tag == "prior_chain_head_return_invalid"


# ---------------------------------------------------------------------------
# Frozen dataclasses
# ---------------------------------------------------------------------------


def test_result_and_detail_are_frozen():
    r = check_router_integrity_multi_source(
        router_yaml_reader=_router_reader(b"x"),
        pinned_hash_reader=_pinned_reader("".join(f"{b:02x}" for b in b"x")[:128]),
        external_manifest_reader=_manifest_reader(
            _make_manifest(chain_head_hash="".join(f"{b:02x}" for b in b"x")[:128], prior_chain_head_hash="")
        ),
        prior_chain_head_reader=_prior_reader(None),
        signature_verify=_StaticVerifier(result=True),
        hash_bytes=_HashFn(),
        public_key=b"pk",
    )
    with pytest.raises(FrozenInstanceError):
        r.success = False  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        r.detail.reason_tag = "x"  # type: ignore[misc]


def test_failure_code_constants():
    assert F_AMDT_10 == "F-AMDT-10"
    assert F_AMDT_10_PAIR == "F-AMDT-10-PAIR"
    assert F_AMDT_10_EXTERNAL == "F-AMDT-10-EXTERNAL"
    assert F_AMDT_10_SIGNATURE == "F-AMDT-10-SIGNATURE"
    assert F_AMDT_10_CHAIN_BREAK == "F-AMDT-10-CHAIN-BREAK"
    assert F_AMDT_10_READER_FAIL == "F-AMDT-10-READER-FAIL"
