"""Fail fixture R7 — short-circuit ``or`` admits the fd_broker.request
under the emergency fallback path, bypassing the preflight sentinel."""

from __future__ import annotations

from typing import Final

import fd_broker  # type: ignore[import-not-found]

PREFLIGHT_OK: Final[bool] = True


def run(host: str, emergency: bool):
    if PREFLIGHT_OK or emergency:
        return fd_broker.request("https", host=host)
