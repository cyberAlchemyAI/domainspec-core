"""R-UPLOADER-NO-SUBMIT — direct httpx.post call (must fire)."""

from __future__ import annotations

import httpx


def submit(url: str, payload: bytes) -> None:
    httpx.post(url, content=payload)
