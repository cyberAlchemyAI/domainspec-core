"""Routing Consistency Gate — ensures router.yaml and routing.yaml agree.

Why this exists
---------------
Two files describe the seat→model mapping:

  /router.yaml                         — workspace-root identity doc. Humans
                                         read this first when they want to
                                         know what powers what.
  /pipeline/orchestrator/routing.yaml — operative config loaded by
                                         pipeline/orchestrator/router.py at
                                         dispatch time.

If they drift (e.g. router.yaml says `groq/qwen-3-32b` while routing.yaml
says `groq/qwen/qwen3-32b`, or a seat exists in only one file), the system
looks consistent to `router.py --check` — which reads only routing.yaml —
while human readers of router.yaml believe something different. This is the
structural version of the "5 Claudes arguing without a tie-break" failure
class: two configs, both apparently authoritative, no arbitration.

Rule
----
For every LLM-backed seat (any seat whose active-tier `provider` is not
`none` and which doesn't declare `implementation: python_deterministic`):

  1. Seat must appear in both files.
  2. The `primary:` line in router.yaml must equal
     "{provider}/{model}" from the active tier of routing.yaml.

Deterministic-only seats (logician) need appear only marked in both files;
the presence check is cosmetic.

Usage
-----
    result = routing_consistency_gate.run()
    if result.severity == "ERROR":
        sys.exit(1)

Design
------
Fail-closed on disagreement. No LLM. Zero cost. Safe to run pre-commit and
at daemon startup.
"""
from __future__ import annotations

import argparse
import dataclasses
import datetime
import json
import os
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # PyYAML
except ImportError:  # pragma: no cover - yaml is a hard dep
    yaml = None  # type: ignore[assignment]


WORKSPACE = Path(
    os.environ.get("QUILL_WORKSPACE")
    or Path(__file__).resolve().parents[2]
)
ROUTER_YAML = WORKSPACE / "router.yaml"
ROUTING_YAML = WORKSPACE / "pipeline" / "orchestrator" / "routing.yaml"


@dataclasses.dataclass
class Finding:
    severity: str      # "ERROR" | "WARN" | "INFO"
    rule: str
    detail: str


@dataclasses.dataclass
class Result:
    timestamp: str
    severity: str
    findings: list[Finding]
    seats_checked: list[str]

    def to_json(self) -> str:
        return json.dumps(
            {
                "timestamp": self.timestamp,
                "severity": self.severity,
                "findings": [dataclasses.asdict(f) for f in self.findings],
                "seats_checked": self.seats_checked,
            },
            indent=2,
        )


def _load_yaml(p: Path) -> dict[str, Any] | None:
    if not p.exists():
        return None
    if yaml is None:
        raise RuntimeError(
            "PyYAML is required for routing_consistency_gate. "
            "Install with: pip install pyyaml --break-system-packages"
        )
    return yaml.safe_load(p.read_text())


def _router_primary_for(router: dict, seat: str) -> str | None:
    tilth = router.get("tilth", {})
    entry = tilth.get(seat)
    if not isinstance(entry, dict):
        return None
    return entry.get("primary")


def _routing_active_for(routing: dict, seat: str) -> tuple[str | None, str | None, bool]:
    """Return (provider, model, is_deterministic) for a seat in routing.yaml."""
    seats = routing.get("seats", {})
    seat_cfg = seats.get(seat)
    if not isinstance(seat_cfg, dict):
        return None, None, False
    if seat_cfg.get("implementation") == "python_deterministic":
        return None, None, True
    active_tier = routing.get("active_tier", "tier_8gb")
    tier_cfg = seat_cfg.get(active_tier)
    if not isinstance(tier_cfg, dict):
        return None, None, False
    return tier_cfg.get("provider"), tier_cfg.get("model"), False


def _all_seats(router: dict, routing: dict) -> list[str]:
    r1 = set((router.get("tilth") or {}).keys())
    r2 = set((routing.get("seats") or {}).keys())
    return sorted(r1 | r2)


def run() -> Result:
    findings: list[Finding] = []
    seats_checked: list[str] = []
    router = _load_yaml(ROUTER_YAML)
    routing = _load_yaml(ROUTING_YAML)
    if router is None:
        findings.append(Finding("ERROR", "router_yaml_missing",
                                f"{ROUTER_YAML} is missing"))
    if routing is None:
        findings.append(Finding("ERROR", "routing_yaml_missing",
                                f"{ROUTING_YAML} is missing"))
    if router is None or routing is None:
        return _finalize(findings, seats_checked)

    for seat in _all_seats(router, routing):
        seats_checked.append(seat)
        in_router = seat in (router.get("tilth") or {})
        in_routing = seat in (routing.get("seats") or {})
        if not in_router:
            findings.append(Finding(
                "ERROR", "seat_missing_in_router_yaml",
                f"seat '{seat}' is in routing.yaml but not router.yaml — "
                "identity doc is blind to a seat that the operative router "
                "will actually load.",
            ))
            continue
        if not in_routing:
            findings.append(Finding(
                "ERROR", "seat_missing_in_routing_yaml",
                f"seat '{seat}' is in router.yaml but not routing.yaml — "
                "router.py cannot load this seat even though identity doc "
                "claims it exists.",
            ))
            continue
        provider, model, is_det = _routing_active_for(routing, seat)
        if is_det:
            # Deterministic seat: no model string to compare. Just confirm
            # it's marked present in router.yaml.
            continue
        if provider is None or model is None:
            findings.append(Finding(
                "WARN", "routing_tier_missing",
                f"seat '{seat}' has no active-tier entry in routing.yaml",
            ))
            continue
        expected = f"{provider}/{model}"
        actual = _router_primary_for(router, seat)
        if actual is None:
            findings.append(Finding(
                "ERROR", "router_primary_missing",
                f"seat '{seat}' has no `primary:` in router.yaml",
            ))
            continue
        if actual != expected:
            findings.append(Finding(
                "ERROR", "model_string_mismatch",
                f"seat '{seat}': router.yaml primary={actual!r}, "
                f"routing.yaml active_tier={expected!r}",
            ))
    return _finalize(findings, seats_checked)


def _finalize(findings: list[Finding], seats_checked: list[str]) -> Result:
    order = {"OK": 0, "INFO": 1, "WARN": 2, "ERROR": 3}
    worst = "OK"
    for f in findings:
        if order.get(f.severity, 0) > order.get(worst, 0):
            worst = f.severity
    return Result(
        timestamp=datetime.datetime.now().isoformat(timespec="seconds"),
        severity=worst,
        findings=findings,
        seats_checked=seats_checked,
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json-only", action="store_true")
    args = ap.parse_args(argv)
    result = run()
    sys.stdout.write(result.to_json() + "\n")
    return 1 if result.severity == "ERROR" else 0


if __name__ == "__main__":
    sys.exit(main())
