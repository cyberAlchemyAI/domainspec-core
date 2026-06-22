"""Tests for sentinel_monitor module."""
from __future__ import annotations
from unittest.mock import patch, MagicMock
import requests
import pytest
from zrig.sentinel_monitor import SentinelConfig, SentinelCheck, SentinelResult, SentinelMonitor


@pytest.fixture
def config():
    return SentinelConfig(
        health_url="http://localhost:5001/health",
        check_routes=["/", "/admin/login"],
        poll_interval_s=0.01,
        duration_s=0.05,
        response_time_threshold_ms=5000.0,
        max_consecutive_failures=3,
    )


@pytest.fixture
def config_short():
    return SentinelConfig(
        health_url="http://localhost:5001/health",
        poll_interval_s=0.01,
        duration_s=0.03,
        max_consecutive_failures=3,
    )


class TestSentinelConfig:
    def test_from_dict(self):
        c = SentinelConfig.from_dict({"health_url": "http://x/health", "duration_s": 60})
        assert c.health_url == "http://x/health"
        assert c.duration_s == 60.0
        assert c.poll_interval_s == 10.0

    def test_from_dict_defaults(self):
        c = SentinelConfig.from_dict({"health_url": "http://x"})
        assert c.max_consecutive_failures == 3
        assert c.verify_ssl is True


class TestSentinelResult:
    def test_to_gate_output_healthy(self):
        r = SentinelResult(total_checks=10, passed_checks=10)
        out = r.to_gate_output()
        assert out["sentinel_status"] == "HEALTHY"
        assert out["findings"] == []
        assert out["pass_rate"] == 1.0

    def test_to_gate_output_degraded(self):
        r = SentinelResult(
            total_checks=10, passed_checks=7, failed_checks=3,
            degradation_detected=True, degradation_reason="3 failures"
        )
        out = r.to_gate_output()
        assert out["sentinel_status"] == "DEGRADED"
        assert len(out["findings"]) == 1
        assert out["findings"][0]["severity"] == "CRITICAL"

    def test_to_gate_output_zero_checks(self):
        r = SentinelResult()
        out = r.to_gate_output()
        assert out["pass_rate"] == 0


class TestSentinelMonitor:
    def test_check_endpoint_healthy_200(self, config_short):
        monitor = SentinelMonitor(config_short)
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        with patch.object(monitor.session, "get", return_value=mock_resp):
            check = monitor.check_endpoint("http://localhost/health")
        assert check.passed is True
        assert check.status_code == 200
        assert check.response_time_ms >= 0

    def test_check_endpoint_server_error_500(self, config_short):
        monitor = SentinelMonitor(config_short)
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        with patch.object(monitor.session, "get", return_value=mock_resp):
            check = monitor.check_endpoint("http://localhost/health")
        assert check.passed is False
        assert check.status_code == 500

    def test_check_endpoint_timeout(self, config_short):
        monitor = SentinelMonitor(config_short)
        with patch.object(monitor.session, "get", side_effect=requests.exceptions.Timeout("timeout")):
            check = monitor.check_endpoint("http://localhost/health")
        assert check.passed is False
        assert check.status_code is None
        assert "Timeout" in check.error

    def test_check_endpoint_connection_error(self, config_short):
        monitor = SentinelMonitor(config_short)
        with patch.object(monitor.session, "get", side_effect=requests.exceptions.ConnectionError("refused")):
            check = monitor.check_endpoint("http://localhost/health")
        assert check.passed is False
        assert "ConnectionError" in check.error

    def test_run_all_healthy(self, config_short):
        monitor = SentinelMonitor(config_short)
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        with patch.object(monitor.session, "get", return_value=mock_resp):
            result = monitor.run()
        assert result.total_checks > 0
        assert result.passed_checks == result.total_checks
        assert result.degradation_detected is False

    def test_run_detects_consecutive_failures(self):
        cfg = SentinelConfig(
            health_url="http://localhost/health",
            poll_interval_s=0.001,
            duration_s=1.0,
            max_consecutive_failures=2,
        )
        monitor = SentinelMonitor(cfg)
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        with patch.object(monitor.session, "get", return_value=mock_resp):
            result = monitor.run()
        assert result.degradation_detected is True
        assert "consecutive failures" in result.degradation_reason.lower()

    def test_run_detects_slow_response_time(self):
        cfg = SentinelConfig(
            health_url="http://localhost/health",
            poll_interval_s=0.001,
            duration_s=0.02,
            response_time_threshold_ms=0.001,  # impossibly low
            max_consecutive_failures=100,
        )
        monitor = SentinelMonitor(cfg)
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        with patch.object(monitor.session, "get", return_value=mock_resp):
            result = monitor.run()
        assert result.degradation_detected is True
        assert "response time" in result.degradation_reason.lower()

    def test_run_checks_additional_routes(self, config):
        monitor = SentinelMonitor(config)
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        urls_checked = []
        def track_get(url, **kw):
            urls_checked.append(url)
            return mock_resp
        with patch.object(monitor.session, "get", side_effect=track_get):
            monitor.run()
        assert any("/admin/login" in u for u in urls_checked)

    def test_run_stops_early_on_degradation(self):
        cfg = SentinelConfig(
            health_url="http://localhost/health",
            poll_interval_s=0.001,
            duration_s=10.0,  # long duration
            max_consecutive_failures=2,
        )
        monitor = SentinelMonitor(cfg)
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        with patch.object(monitor.session, "get", return_value=mock_resp):
            result = monitor.run()
        assert result.degradation_detected is True
        assert result.duration_s < 5.0  # stopped well before 10s
