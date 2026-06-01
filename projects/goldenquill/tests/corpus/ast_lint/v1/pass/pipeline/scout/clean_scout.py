"""Pass fixture — a scout module that obeys R4 + R5."""

from __future__ import annotations


def evaluate(candidate):
    candidate.score = 0.9  # attribute other than operator_decision — allowed
    return candidate
