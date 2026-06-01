"""Fail fixture R4 — operator_decision written outside review_stage.py."""

from __future__ import annotations


def sneaky(item) -> None:
    setattr(item, "operator_decision", "ACCEPT")
