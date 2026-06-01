"""Fail fixture R6 — loop accesses pipeline.logician internals via package alias."""

from __future__ import annotations

import pipeline.logician as L


def run():
    return L.cedar_eval.evaluate({})
