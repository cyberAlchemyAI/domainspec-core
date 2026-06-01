"""Fail fixture R2 — loop reaches into a logician internal module."""

from __future__ import annotations

from pipeline.logician.cedar_eval import evaluate  # noqa: F401
