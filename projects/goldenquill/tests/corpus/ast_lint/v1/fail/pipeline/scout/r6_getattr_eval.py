"""Fail fixture R6 — indirect eval via ``getattr(__builtins__, "eval")``."""

from __future__ import annotations


def run_dynamic(source: str):
    return getattr(__builtins__, "eval")(source)
