"""Z-Rig sentinel monitor — post-deployment health monitoring."""
from __future__ import annotations

import time
import requests
import logging
from dataclasses import dataclass, field
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("zrig.sentinel")


@dataclass
class SentinelConfig:
    """Configuration for sentinel monitoring."""
    health_url: str
    check_routes: list[str] = field(default_factory=list)
    poll_interval_s: float = 10.0
    duration_s: float = 120.0
    response_time_threshold_ms: float = 5000.0
    max_consecutive_failures: int = 3
    verify_ssl: bool = True

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> SentinelConfig:
        """Creates a SentinelConfig from a dictionary."""
        return cls(
            health_url=d["health_url"],
            check_routes=d.get("check_routes", []),
            poll_interval_s=float(d.get("poll_interval_s", 10.0)),
            duration_s=float(d.get("duration_s", 120.0)),
            response_time_threshold_ms=float(d.get("response_time_threshold_ms", 5000.0)),
            max_consecutive_failures=int(d.get("max_consecutive_failures", 3)),
            verify_ssl=bool(d.get("verify_ssl", True)),
        )


@dataclass
class SentinelCheck:
    """Result of a single health check."""
    url: str
    status_code: int | None
    response_time_ms: float
    passed: bool
    timestamp: str
    error: str | None = None


@dataclass
class SentinelResult:
    """Result of a sentinel monitoring session."""
    total_checks: int = 0
    passed_checks: int = 0
    failed_checks: int = 0
    avg_response_time_ms: float = 0.0
    max_response_time_ms: float = 0.0
    min_response_time_ms: float = float("inf")
    degradation_detected: bool = False
    degradation_reason: str | None = None
    regression_detected: bool = False
    checks: list[SentinelCheck] = field(default_factory=list)
    duration_s: float = 0.0

    def to_gate_output(self) -> dict[str, Any]:
        """Format for W11 gate compatibility."""
        pass_rate = (self.passed_checks / self.total_checks) if self.total_checks > 0 else 0
        return {
            "sentinel_status": "DEGRADED" if self.degradation_detected else "HEALTHY",
            "findings": [{
                "id": "SENTINEL-DEGRADATION",
                "severity": "CRITICAL",
                "description": self.degradation_reason,
            }] if self.degradation_detected else [],
            "regression_detected": self.regression_detected,
            "avg_response_time_ms": self.avg_response_time_ms,
            "max_response_time_ms": self.max_response_time_ms,
            "total_checks": self.total_checks,
            "pass_rate": pass_rate,
        }


class SentinelMonitor:
    """Post-deployment health monitor."""

    def __init__(self, config: SentinelConfig):
        """Initializes the sentinel monitor."""
        self.config = config
        self.session = requests.Session()

    def check_endpoint(self, url: str) -> SentinelCheck:
        """Check a single endpoint. Returns SentinelCheck."""
        start_time = time.monotonic()
        try:
            response = self.session.get(
                url,
                timeout=self.config.poll_interval_s,
                verify=self.config.verify_ssl,
            )
            response_time_ms = (time.monotonic() - start_time) * 1000
            passed = response.status_code == 200
            return SentinelCheck(
                url=url,
                status_code=response.status_code,
                response_time_ms=response_time_ms,
                passed=passed,
                timestamp=datetime.now(timezone.utc).isoformat(),
                error=None if passed else f"Received status code {response.status_code}",
            )
        except requests.exceptions.RequestException as e:
            response_time_ms = (time.monotonic() - start_time) * 1000
            return SentinelCheck(
                url=url,
                status_code=None,
                response_time_ms=response_time_ms,
                passed=False,
                timestamp=datetime.now(timezone.utc).isoformat(),
                error=f"{type(e).__name__}: {e}",
            )

    def run(self) -> SentinelResult:
        """Run sentinel monitoring for the configured duration."""
        result = SentinelResult()
        start_time = time.monotonic()
        consecutive_failures = 0
        all_response_times: list[float] = []

        urls_to_check = [self.config.health_url]
        base_url = self.config.health_url.rsplit('/', 1)[0]
        for route in self.config.check_routes:
            if route.startswith(('http://', 'https://')):
                urls_to_check.append(route)
            else:
                urls_to_check.append(f"{base_url.rstrip('/')}/{route.lstrip('/')}")

        while time.monotonic() - start_time < self.config.duration_s:
            for url in urls_to_check:
                check = self.check_endpoint(url)
                result.checks.append(check)
                result.total_checks += 1

                if check.passed:
                    result.passed_checks += 1
                    consecutive_failures = 0
                    all_response_times.append(check.response_time_ms)
                else:
                    result.failed_checks += 1
                    consecutive_failures += 1

                if consecutive_failures >= self.config.max_consecutive_failures:
                    result.degradation_detected = True
                    result.degradation_reason = (
                        f"Detected {consecutive_failures} consecutive failures, "
                        f"exceeding threshold of {self.config.max_consecutive_failures}. "
                        f"Last error: {check.error}"
                    )
                    break

            if result.degradation_detected:
                break

            time.sleep(self.config.poll_interval_s)

        result.duration_s = time.monotonic() - start_time

        if all_response_times:
            result.avg_response_time_ms = sum(all_response_times) / len(all_response_times)
            result.max_response_time_ms = max(all_response_times)
            result.min_response_time_ms = min(all_response_times)

            if not result.degradation_detected and result.avg_response_time_ms > self.config.response_time_threshold_ms:
                result.degradation_detected = True
                result.degradation_reason = (
                    f"Average response time {result.avg_response_time_ms:.2f}ms "
                    f"exceeded threshold of {self.config.response_time_threshold_ms:.2f}ms."
                )

        return result
