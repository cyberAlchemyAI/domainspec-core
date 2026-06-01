"""Fail fixture R6 — indirect LLM-client load via importlib.import_module."""

from __future__ import annotations

import importlib


def load_provider():
    return importlib.import_module("anthropic")
