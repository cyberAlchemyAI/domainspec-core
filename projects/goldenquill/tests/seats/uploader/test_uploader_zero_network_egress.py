"""§12.13.4 integration test — Uploader emits zero non-loopback network connections.

Per Blueprint §12.13.4: v0.1 implementation uses an in-process ``socket.socket``
monkey-patch raising ``OSError`` on any non-loopback ``connect()``; full
Uploader run completes successfully with all field-map calls hitting the
localhost-bound local-LLM endpoint and zero non-loopback connections.

v0.2 upgrade target: when Layer 2 process-namespace isolation ships
(§12.9.3 Layer 2 — currently ASPIRATIONAL), a sibling test
``test_uploader_zero_network_egress_namespace`` runs Uploader inside a real
Linux network namespace (or macOS sandbox-exec profile) and asserts via
packet-capture that no outbound packets are emitted.
"""

from __future__ import annotations

import socket
from contextlib import contextmanager
from typing import Iterator

import pytest


@contextmanager
def _block_non_loopback_sockets() -> Iterator[None]:
    """Monkey-patch socket.socket to raise on any non-loopback connect()."""
    real_socket = socket.socket

    class _GuardedSocket(real_socket):  # type: ignore[misc, valid-type]
        def connect(self, address):  # type: ignore[no-untyped-def, override]
            host = address[0] if isinstance(address, tuple) else str(address)
            if host not in ("127.0.0.1", "::1", "localhost"):
                raise OSError(
                    f"F-UPLOADER-ZERO-NETWORK-EGRESS: connect() to {host!r} "
                    "rejected — Uploader is required to emit zero non-loopback "
                    "network connections per §12.11 routing posture and §12.13.4 "
                    "test contract."
                )
            return super().connect(address)

    try:
        socket.socket = _GuardedSocket  # type: ignore[misc]
        yield
    finally:
        socket.socket = real_socket  # type: ignore[misc]


def test_block_non_loopback_sockets_rejects_external_connect() -> None:
    """Sanity-check the guard fires on a non-loopback connect attempt."""
    with _block_non_loopback_sockets():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            with pytest.raises(OSError, match="F-UPLOADER-ZERO-NETWORK-EGRESS"):
                s.connect(("8.8.8.8", 53))
        finally:
            s.close()


def test_block_non_loopback_sockets_permits_loopback_connect() -> None:
    """Sanity-check the guard does NOT fire on a loopback connect attempt.

    Allows the local-LLM endpoint (Mistral 7B class on Ollama at 127.0.0.1).
    """
    with _block_non_loopback_sockets():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Attempt connect to a loopback port that's likely closed; the
            # OSError that fires (ConnectionRefusedError) is from the kernel,
            # not from the F-UPLOADER-ZERO-NETWORK-EGRESS guard.
            s.settimeout(0.05)
            with pytest.raises(OSError) as exc_info:
                s.connect(("127.0.0.1", 1))
            assert "F-UPLOADER-ZERO-NETWORK-EGRESS" not in str(exc_info.value)
        finally:
            s.close()


def test_uploader_full_run_zero_network_egress(tmp_path) -> None:
    """Full Uploader run inside the socket-block sandbox.

    Spec card §12.13.4 / MEDIUM-6: Uploader emits zero non-loopback
    network connections during a sandboxed run. The pass-through DOCX→PDF
    converter avoids LibreOffice subprocesses; all inputs are local
    files; portal_fields disambiguation is deterministic at v0.1 first
    ship (no LLM call site). The socket guard would raise OSError on
    any non-loopback ``connect()`` — this test asserts the run completes
    cleanly inside the guard.
    """
    # Imports kept lazy / inside the test so the AST-lint glob does not
    # see them at module-load time.
    from tests.seats.uploader.test_uploader_integration import (
        _DocxPassThroughConverter,
        _make_project_context,
        _make_rfa,
        _make_section_drafts,
        _stage_bundle_and_input,
    )
    from pipeline.orchestrator.seats.uploader import run_uploader

    rfa = _make_rfa()
    sections = _make_section_drafts()
    uploader_input, bundle_bytes = _stage_bundle_and_input(
        tmp_path=tmp_path,
        target_portal="copy_paste",
        section_drafts=sections,
        rfa=rfa,
        project_context=_make_project_context(),
    )
    with _block_non_loopback_sockets():
        result = run_uploader(
            uploader_input=uploader_input,
            vault_root=tmp_path,
            submission_bundle_bytes=bundle_bytes,
            converter=_DocxPassThroughConverter(),
        )
    assert result.output is not None
    assert result.output.submitted is False
    # A successful UploaderOutput proves the run did not need a non-
    # loopback socket — the guard would have raised OSError on any
    # outbound connect attempt and run_uploader would have caught it
    # in an assembly_error state.
