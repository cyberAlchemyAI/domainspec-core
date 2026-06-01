"""R-UPLOADER-NO-SUBMIT — urllib3 PoolManager call (must fire)."""

from __future__ import annotations

import urllib3


def submit(url: str, payload: bytes) -> None:
    pool = urllib3.PoolManager()
    pool.request("POST", url, body=payload)
