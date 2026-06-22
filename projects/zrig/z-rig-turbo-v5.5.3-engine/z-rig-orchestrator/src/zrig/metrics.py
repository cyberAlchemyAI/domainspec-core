#!/usr/bin/env python3
"""
HRR-004 Builder 3 — metrics.py
Pipeline Self-Metrics (A.11) + MECH-038 threshold triggers.
Gate first-pass rate, FATAL-per-run, rework frequency, time-to-completion.
"""

from __future__ import annotations
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


@dataclass
class RunMetrics:
    run_id: str
    gate_first_pass_rate: float
    fatal_count: int
    rework_count: int
    time_to_completion_s: float
    waves_completed: int
    timestamp: str


class MetricsStore:
    """metrics_store.jsonl persistence + threshold triggers (MECH-038)."""

    def __init__(self, store_path: Path = Path("metrics_store.jsonl")):
        self.store_path = store_path
        self.runs: List[RunMetrics] = []

    def record_run(self, metrics: RunMetrics) -> RunMetrics:
        self.runs.append(metrics)
        self._append(metrics)
        return metrics

    def _append(self, m: RunMetrics):
        with open(self.store_path, "a") as f:
            f.write(json.dumps(asdict(m)) + "\n")

    def evaluate_triggers(self, current: RunMetrics) -> List[str]:
        """MECH-038 SELF_IMPROVEMENT_TRIGGER_EVAL."""
        triggers = []
        if current.gate_first_pass_rate < 0.70:
            triggers.append("AUTO_ESCALATE_LOW_FIRST_PASS")
        if current.fatal_count >= 3:
            triggers.append("DEMOTE_MODELS_HIGH_FATAL")
        if current.rework_count > 5:
            triggers.append("FLAG_MECHANISM_REWORK_SPIKE")
        if current.time_to_completion_s > 14400:  # 4h
            triggers.append("AUTO_ESCALATE_SLOW_RUN")
        return triggers

    def load_history(self) -> List[RunMetrics]:
        if not self.store_path.exists():
            return []
        history = []
        with open(self.store_path) as f:
            for line in f:
                try:
                    history.append(RunMetrics(**json.loads(line)))
                except Exception:
                    continue
        return history
