"""Tests for integration_runner module."""
from __future__ import annotations
from unittest.mock import patch, MagicMock, PropertyMock
import pytest
from zrig.integration_runner import IntegrationConfig, IntegrationResult, IntegrationRunner


@pytest.fixture
def config():
    return IntegrationConfig(base_url="http://localhost:5001", db_url="postgresql://test@localhost/test", admin_password="secret")


@pytest.fixture
def config_no_db():
    return IntegrationConfig(base_url="http://localhost:5001")


class TestIntegrationConfig:
    def test_from_dict(self):
        c = IntegrationConfig.from_dict({"base_url": "http://x", "db_url": "pg://y", "admin_password": "pw"})
        assert c.base_url == "http://x"
        assert c.db_url == "pg://y"
        assert c.admin_password == "pw"

    def test_from_dict_defaults(self):
        c = IntegrationConfig.from_dict({"base_url": "http://x"})
        assert c.db_url == ""
        assert c.timeout_s == 10
        assert c.verify_ssl is True


class TestIntegrationResult:
    def test_all_passed_true(self):
        r = IntegrationResult(passed=3, failed=0)
        assert r.all_passed is True

    def test_all_passed_false(self):
        r = IntegrationResult(passed=2, failed=1)
        assert r.all_passed is False

    def test_to_gate_output_no_failures(self):
        r = IntegrationResult(passed=2, tests=[
            {"name": "t1", "passed": True, "duration_ms": 10, "error": None},
            {"name": "t2", "passed": True, "duration_ms": 20, "error": None},
        ])
        out = r.to_gate_output()
        assert out["findings"] == []
        assert out["verification_confidence"] == 1.0

    def test_to_gate_output_with_failures(self):
        r = IntegrationResult(passed=1, failed=1, tests=[
            {"name": "t1", "passed": True, "duration_ms": 10, "error": None},
            {"name": "t2", "passed": False, "duration_ms": 20, "error": "broke"},
        ])
        out = r.to_gate_output()
        assert len(out["findings"]) == 1
        assert out["findings"][0]["id"] == "t2"
        assert out["findings"][0]["severity"] == "CRITICAL"


class TestIntegrationRunner:
    @patch("zrig.integration_runner.requests.Session")
    def test_landing_page_200_passes(self, MockSession, config_no_db):
        mock_session = MockSession.return_value
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = "x" * 200
        mock_session.get.return_value = mock_resp
        runner = IntegrationRunner(config_no_db)
        runner.session = mock_session
        runner._test_landing_page()
        assert runner.results.passed == 1

    @patch("zrig.integration_runner.requests.Session")
    def test_landing_page_500_fails(self, MockSession, config_no_db):
        mock_session = MockSession.return_value
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_resp.text = "error"
        mock_session.get.return_value = mock_resp
        runner = IntegrationRunner(config_no_db)
        runner.session = mock_session
        runner._test_landing_page()
        assert runner.results.failed == 1

    @patch("zrig.integration_runner.requests.Session")
    def test_csrf_token_extraction(self, MockSession, config_no_db):
        mock_session = MockSession.return_value
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = '<input name="csrf_token" value="abc123">'
        mock_session.get.return_value = mock_resp
        runner = IntegrationRunner(config_no_db)
        runner.session = mock_session
        runner._test_admin_login_form_has_csrf()
        assert runner.results.passed == 1

    @patch("zrig.integration_runner.requests.Session")
    def test_admin_login_flow_success(self, MockSession, config):
        mock_session = MockSession.return_value
        get_resp = MagicMock()
        get_resp.status_code = 200
        get_resp.text = '<input name="csrf_token" value="tok123">'
        post_resp = MagicMock()
        post_resp.status_code = 200
        post_resp.url = "http://localhost:5001/admin/"
        post_resp.text = "dashboard"
        mock_session.get.return_value = get_resp
        mock_session.post.return_value = post_resp
        runner = IntegrationRunner(config)
        runner.session = mock_session
        runner._test_admin_login_flow()
        assert runner.results.passed == 1

    @patch("zrig.integration_runner.requests.Session")
    def test_reports_redirect_without_auth(self, MockSession, config_no_db):
        mock_session = MockSession.return_value
        mock_resp = MagicMock()
        mock_resp.status_code = 302
        runner = IntegrationRunner(config_no_db)
        # Use a fresh session for this test
        with patch("zrig.integration_runner.requests.Session") as fresh:
            fresh.return_value.get.return_value = mock_resp
            runner._test_reports_requires_auth()
        assert runner.results.passed == 1

    @patch("zrig.integration_runner.psycopg2.connect")
    def test_database_tables_exist(self, mock_connect, config):
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_cur.fetchall.return_value = [("leads",), ("stores",), ("representatives",), ("qr_codes",), ("other",)]
        mock_conn.cursor.return_value = mock_cur
        mock_connect.return_value = mock_conn
        runner = IntegrationRunner(config)
        runner._test_database_tables_exist()
        assert runner.results.passed == 1

    @patch("zrig.integration_runner.psycopg2.connect")
    def test_database_connection_failure(self, mock_connect, config):
        mock_connect.side_effect = Exception("Connection refused")
        runner = IntegrationRunner(config)
        runner._test_database_tables_exist()
        assert runner.results.failed == 1
        assert "Connection refused" in runner.results.tests[0]["error"]

    @patch("zrig.integration_runner.requests.Session")
    def test_run_all_aggregates(self, MockSession, config_no_db):
        mock_session = MockSession.return_value
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = "x" * 200
        mock_resp.url = "http://localhost:5001/admin/"
        mock_session.get.return_value = mock_resp
        mock_session.post.return_value = mock_resp
        with patch("zrig.integration_runner.requests.Session") as fresh:
            fresh.return_value.get.return_value = MagicMock(status_code=302)
            runner = IntegrationRunner(config_no_db)
            runner.session = mock_session
            result = runner.run_all()
        assert result.total_duration_s > 0
        assert len(result.tests) == 6  # no DB tests
