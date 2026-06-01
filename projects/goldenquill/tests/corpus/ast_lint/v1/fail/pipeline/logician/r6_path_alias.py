"""Fail fixture R6 — indirect vault read via Path alias chain."""

from __future__ import annotations

from pathlib import Path


def leak() -> bytes:
    return Path("orgs/fit_farms/vault/secret.json").open("rb").read()
