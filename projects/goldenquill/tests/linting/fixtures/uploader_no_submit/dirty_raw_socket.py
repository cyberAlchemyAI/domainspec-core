"""R-UPLOADER-NO-SUBMIT — raw socket call (must fire)."""

from __future__ import annotations

import socket


def submit(host: str, port: int, payload: bytes) -> None:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(payload)
    s.close()
