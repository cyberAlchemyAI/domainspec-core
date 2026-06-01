"""Fail fixture R6 — indirect vault read via ``builtins.open`` attribute form."""

from __future__ import annotations

import builtins


def leak() -> bytes:
    return builtins.open("orgs/fit_farms/vault/secret.json", "rb").read()
