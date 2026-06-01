"""R-UPLOADER-NO-SUBMIT — requests.request call (must fire)."""

from __future__ import annotations

import requests


def submit(url: str, payload: bytes) -> None:
    requests.request("POST", url, data=payload)
