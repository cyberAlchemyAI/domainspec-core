"""Z-Rig integration test runner — tests against live staging."""
from __future__ import annotations

import re
import time
import requests
import psycopg2
from dataclasses import dataclass, field
from typing import Any


@dataclass
class IntegrationConfig:
    """Configuration for integration test run."""
    base_url: str
    db_url: str = ""
    admin_password: str = ""
    timeout_s: int = 10
    verify_ssl: bool = True

    @classmethod
    def from_dict(cls, d: dict) -> IntegrationConfig:
        return cls(
            base_url=d["base_url"],
            db_url=d.get("db_url", ""),
            admin_password=d.get("admin_password", ""),
            timeout_s=d.get("timeout_s", 10),
            verify_ssl=d.get("verify_ssl", True),
        )


@dataclass
class IntegrationResult:
    """Result of integration test suite."""
    passed: int = 0
    failed: int = 0
    errors: int = 0
    tests: list[dict] = field(default_factory=list)
    total_duration_s: float = 0.0

    @property
    def all_passed(self) -> bool:
        return self.failed == 0 and self.errors == 0

    def to_gate_output(self) -> dict:
        """Format for W4 gate compatibility."""
        findings = []
        for t in self.tests:
            if not t["passed"]:
                findings.append({
                    "id": t["name"],
                    "severity": "CRITICAL",
                    "description": t.get("error", "Test failed"),
                    "location": "integration",
                })
        total = max(self.passed + self.failed, 1)
        return {
            "findings": findings,
            "verification_confidence": self.passed / total,
            "trace_matrix": {t["name"]: "pass" if t["passed"] else "fail" for t in self.tests},
        }


class IntegrationRunner:
    """Runs integration tests against a live staging server."""

    def __init__(self, config: IntegrationConfig):
        self.config = config
        self.session = requests.Session()
        self.results = IntegrationResult()

    def run_all(self) -> IntegrationResult:
        """Run all integration tests."""
        t0 = time.time()
        self._test_landing_page()
        self._test_health_endpoint()
        self._test_admin_login_form_has_csrf()
        self._test_admin_login_flow()
        self._test_address_checker()
        self._test_reports_requires_auth()
        if self.config.db_url:
            self._test_database_tables_exist()
            self._test_database_has_data()
        self.results.total_duration_s = time.time() - t0
        return self.results

    def _record(self, name: str, passed: bool, duration_ms: float, error: str | None = None):
        """Record a test result."""
        self.results.tests.append({
            "name": name,
            "passed": passed,
            "duration_ms": duration_ms,
            "error": error,
        })
        if passed:
            self.results.passed += 1
        else:
            self.results.failed += 1

    def _test_landing_page(self):
        """Test that the landing page returns 200 with content."""
        t0 = time.time()
        try:
            resp = self.session.get(
                self.config.base_url,
                timeout=self.config.timeout_s,
                verify=self.config.verify_ssl,
            )
            passed = resp.status_code == 200 and len(resp.text) > 100
            self._record("landing_page", passed, (time.time() - t0) * 1000,
                         None if passed else f"Status {resp.status_code}")
        except Exception as e:
            self._record("landing_page", False, (time.time() - t0) * 1000, str(e))

    def _test_health_endpoint(self):
        """Test the /health endpoint."""
        t0 = time.time()
        try:
            url = f"{self.config.base_url.rstrip('/')}/health"
            resp = self.session.get(url, timeout=self.config.timeout_s, verify=self.config.verify_ssl)
            passed = resp.status_code in (200, 204)
            self._record("health_endpoint", passed, (time.time() - t0) * 1000,
                         None if passed else f"Status {resp.status_code}")
        except Exception as e:
            self._record("health_endpoint", False, (time.time() - t0) * 1000, str(e))

    def _test_admin_login_form_has_csrf(self):
        """Test that admin login form contains a CSRF token."""
        t0 = time.time()
        try:
            url = f"{self.config.base_url.rstrip('/')}/admin/login"
            resp = self.session.get(url, timeout=self.config.timeout_s, verify=self.config.verify_ssl)
            if resp.status_code != 200:
                self._record("admin_login_form_has_csrf", False, (time.time() - t0) * 1000,
                             f"Status {resp.status_code}")
                return
            match = re.search(r'name=["\']csrf_token["\'][^>]*value=["\']([^"\']+)["\']', resp.text)
            if not match:
                match = re.search(r'value=["\']([^"\']+)["\'][^>]*name=["\']csrf_token["\']', resp.text)
            passed = match is not None
            self._record("admin_login_form_has_csrf", passed, (time.time() - t0) * 1000,
                         None if passed else "CSRF token not found in form")
        except Exception as e:
            self._record("admin_login_form_has_csrf", False, (time.time() - t0) * 1000, str(e))

    def _test_admin_login_flow(self):
        """Test full CSRF login flow: GET form → extract token → POST login."""
        t0 = time.time()
        try:
            base = self.config.base_url.rstrip('/')
            login_url = f"{base}/admin/login"
            resp = self.session.get(login_url, timeout=self.config.timeout_s, verify=self.config.verify_ssl)
            if resp.status_code != 200:
                self._record("admin_login_flow", False, (time.time() - t0) * 1000,
                             "Login page not reachable")
                return
            match = re.search(r'name=["\']csrf_token["\'][^>]*value=["\']([^"\']+)["\']', resp.text)
            if not match:
                match = re.search(r'value=["\']([^"\']+)["\'][^>]*name=["\']csrf_token["\']', resp.text)
            if not match:
                self._record("admin_login_flow", False, (time.time() - t0) * 1000,
                             "No CSRF token found")
                return
            csrf = match.group(1)
            data = {"csrf_token": csrf, "password": self.config.admin_password or "test"}
            post_resp = self.session.post(login_url, data=data, timeout=self.config.timeout_s,
                                          verify=self.config.verify_ssl, allow_redirects=True)
            passed = post_resp.status_code == 200 and (
                "/admin/" in post_resp.url or "dashboard" in post_resp.text.lower()
            )
            self._record("admin_login_flow", passed, (time.time() - t0) * 1000,
                         None if passed else f"Login failed: status {post_resp.status_code}")
        except Exception as e:
            self._record("admin_login_flow", False, (time.time() - t0) * 1000, str(e))

    def _test_address_checker(self):
        """Test the address coverage checker endpoint."""
        t0 = time.time()
        try:
            url = f"{self.config.base_url.rstrip('/')}/check-address"
            resp = self.session.get(url, params={"address": "123 Main St"},
                                    timeout=self.config.timeout_s, verify=self.config.verify_ssl)
            passed = resp.status_code == 200
            self._record("address_checker", passed, (time.time() - t0) * 1000,
                         None if passed else f"Status {resp.status_code}")
        except Exception as e:
            self._record("address_checker", False, (time.time() - t0) * 1000, str(e))

    def _test_reports_requires_auth(self):
        """Test that /reports/ redirects when not authenticated."""
        t0 = time.time()
        try:
            fresh_session = requests.Session()
            url = f"{self.config.base_url.rstrip('/')}/reports/"
            resp = fresh_session.get(url, timeout=self.config.timeout_s,
                                      verify=self.config.verify_ssl, allow_redirects=False)
            passed = resp.status_code in (302, 401, 403)
            self._record("reports_requires_auth", passed, (time.time() - t0) * 1000,
                         None if passed else f"Status {resp.status_code} (expected redirect)")
        except Exception as e:
            self._record("reports_requires_auth", False, (time.time() - t0) * 1000, str(e))

    def _test_database_tables_exist(self):
        """Test that expected tables exist in the database."""
        t0 = time.time()
        try:
            conn = psycopg2.connect(self.config.db_url, connect_timeout=self.config.timeout_s)
            cur = conn.cursor()
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            tables = {r[0] for r in cur.fetchall()}
            cur.close()
            conn.close()
            expected = {"leads", "stores", "representatives", "qr_codes"}
            missing = expected - tables
            passed = len(missing) == 0
            self._record("database_tables_exist", passed, (time.time() - t0) * 1000,
                         None if passed else f"Missing tables: {missing}")
        except Exception as e:
            self._record("database_tables_exist", False, (time.time() - t0) * 1000, str(e))

    def _test_database_has_data(self):
        """Test that at least one table has rows."""
        t0 = time.time()
        try:
            conn = psycopg2.connect(self.config.db_url, connect_timeout=self.config.timeout_s)
            cur = conn.cursor()
            has_data = False
            for table in ["leads", "stores", "representatives"]:
                try:
                    cur.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cur.fetchone()[0]
                    if count > 0:
                        has_data = True
                        break
                except Exception:
                    continue
            cur.close()
            conn.close()
            self._record("database_has_data", has_data, (time.time() - t0) * 1000,
                         None if has_data else "No data found in leads/stores/representatives")
        except Exception as e:
            self._record("database_has_data", False, (time.time() - t0) * 1000, str(e))
