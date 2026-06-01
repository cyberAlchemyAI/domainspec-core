"""Fail fixture R7 — ``Final[bool]`` sentinel has a non-literal initializer
(Call sub-tree). B-v5-01 rejects the guard; the fd_broker.request sink fires."""

from __future__ import annotations

import os
from typing import Final

import fd_broker  # type: ignore[import-not-found]

PREFLIGHT_OK: Final[bool] = bool(os.environ.get("READY"))


def run(host: str):
    if PREFLIGHT_OK:
        return fd_broker.request("https", host=host)
