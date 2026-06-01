"""Fail fixture R5 — scout calls eval()."""

from __future__ import annotations


def run(expr: str):
    return eval(expr)
