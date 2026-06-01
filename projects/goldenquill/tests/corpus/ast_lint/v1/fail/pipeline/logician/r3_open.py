"""Fail fixture R3 — logician opens a literal vault path."""

from __future__ import annotations


def leak() -> bytes:
    with open("orgs/fit_farms/vault/secret.json", "rb") as fh:
        return fh.read()
