"""Fail fixture R7 — fd_broker.request without preflight-sentinel dominator."""

from __future__ import annotations

import fd_broker  # type: ignore[import-not-found]


def run(host: str):
    return fd_broker.request("https", host=host)
