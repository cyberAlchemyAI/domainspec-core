"""Fail fixture R6 — indirect setattr('operator_decision') via aliased literal."""

from __future__ import annotations


def sneaky_accept(item) -> None:
    attr_name = "operator_decision"
    setattr(item, attr_name, "ACCEPT")
