"""Tests for Z-Rig deploy_adapter and deploy_config_schema."""
from __future__ import annotations

import json
import subprocess
import textwrap
import time
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest

from src.zrig.deploy_adapter import DeployAdapter, DeployConfig, DeployResult
from src.zrig.deploy_config_schema import load_project_configs, validate_deploy_config


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_config(**overrides: object) -> DeployConfig:
    """Return a DeployConfig with sensible defaults, overridden as needed."""
    defaults = dict(
        host="5.161.249.196",
        user="root",
        app_path="/opt/lux-wireless-staging",
        service_name="lux-wireless-staging.service",
        venv_path="/opt/lux-wireless-staging/venv",
        health_url="http://127.0.0.1:5001/health",
        health_timeout_s=5,
        git_branch="main",
        pre_deploy_commands=[],
        post_deploy_commands=[],
    )
    defaults.update(overrides)
    return DeployConfig(**defaults)  # type: ignore[arg-type]


def _mock_ssh_success(stdout: str = "", stderr: str = "") -> MagicMock:
    """Return a mock subprocess.run result for a successful SSH call."""
    m = MagicMock()
    m.returncode = 0
    m.stdout = stdout
    m.stderr = stderr
    return m


def _mock_ssh_failure(stdout: str = "", stderr: str = "error") -> MagicMock:
    m = MagicMock()
    m.returncode = 1
    m.stdout = stdout
    m.stderr = stderr
    return m


# ---------------------------------------------------------------------------
# 1. test_ssh_command_execution
# ---------------------------------------------------------------------------


@patch("src.zrig.deploy_adapter.subprocess.run")
def test_ssh_command_execution(mock_run: MagicMock) -> None:
    """_ssh() should invoke subprocess.run with correct SSH arguments."""
    mock_run.return_value = _mock_ssh_success(stdout="hello")
    adapter = DeployAdapter(_make_config())

    rc, out, err = adapter._ssh("echo hello", timeout=30)

    mock_run.assert_called_once()
    args = mock_run.call_args
    cmd_list: list[str] = args[0][0]
    assert "ssh" == cmd_list[0]
    assert "root@5.161.249.196" in cmd_list
    assert "echo hello" in cmd_list
    assert args[1]["timeout"] == 30
    assert rc == 0
    assert out == "hello"


# ---------------------------------------------------------------------------
# 2. test_deploy_sequence_all_steps_pass
# ---------------------------------------------------------------------------


@patch("src.zrig.deploy_adapter.requests.get")
@patch("src.zrig.deploy_adapter.subprocess.run")
def test_deploy_sequence_all_steps_pass(
    mock_run: MagicMock, mock_get: MagicMock
) -> None:
    """Full deploy with all steps passing should return success=True."""
    # Every SSH call succeeds; first call is get_current_commit
    mock_run.return_value = _mock_ssh_success(stdout="abc123")
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_get.return_value = mock_resp

    config = _make_config(
        pre_deploy_commands=["echo pre"],
        post_deploy_commands=["echo post"],
    )
    adapter = DeployAdapter(config)
    result = adapter.deploy()

    assert result.success is True
    assert result.health_check_passed is True
    assert result.rollback_commit == "abc123"
    assert "git-pull" in result.steps_completed
    assert "pip-install" in result.steps_completed
    assert "service-restart" in result.steps_completed
    assert "health-check" in result.steps_completed
    assert "pre-deploy-0" in result.steps_completed
    assert "post-deploy-0" in result.steps_completed
    assert result.duration_s >= 0


# ---------------------------------------------------------------------------
# 3. test_deploy_git_pull_failure_stops_deploy
# ---------------------------------------------------------------------------


@patch("src.zrig.deploy_adapter.subprocess.run")
def test_deploy_git_pull_failure_stops_deploy(mock_run: MagicMock) -> None:
    """If git pull fails the deploy should abort without continuing."""
    # First call: get_current_commit -> ok
    # Second call: git pull -> fail
    mock_run.side_effect = [
        _mock_ssh_success(stdout="abc123"),  # get_current_commit
        _mock_ssh_failure(stderr="merge conflict"),  # git pull
    ]

    adapter = DeployAdapter(_make_config())
    result = adapter.deploy()

    assert result.success is False
    assert "git-pull" in result.steps_failed
    assert "pip-install" not in result.steps_completed
    assert "merge conflict" in (result.error or "")


# ---------------------------------------------------------------------------
# 4. test_deploy_health_check_failure
# ---------------------------------------------------------------------------


@patch("src.zrig.deploy_adapter.time.sleep")
@patch("src.zrig.deploy_adapter.requests.get")
@patch("src.zrig.deploy_adapter.subprocess.run")
def test_deploy_health_check_failure(
    mock_run: MagicMock, mock_get: MagicMock, mock_sleep: MagicMock
) -> None:
    """Deploy should fail when the health check never returns 200."""
    mock_run.return_value = _mock_ssh_success(stdout="abc123")

    # Health check always 500
    mock_resp = MagicMock()
    mock_resp.status_code = 500
    mock_get.return_value = mock_resp

    config = _make_config(health_timeout_s=1)
    adapter = DeployAdapter(config)
    result = adapter.deploy()

    assert result.success is False
    assert result.health_check_passed is False
    assert "health-check" in result.steps_failed


# ---------------------------------------------------------------------------
# 5. test_deploy_records_rollback_commit
# ---------------------------------------------------------------------------


@patch("src.zrig.deploy_adapter.requests.get")
@patch("src.zrig.deploy_adapter.subprocess.run")
def test_deploy_records_rollback_commit(
    mock_run: MagicMock, mock_get: MagicMock
) -> None:
    """Deploy should record the pre-deploy commit for potential rollback."""
    sha = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
    mock_run.return_value = _mock_ssh_success(stdout=sha)
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_get.return_value = mock_resp

    adapter = DeployAdapter(_make_config())
    result = adapter.deploy()

    assert result.rollback_commit == sha


# ---------------------------------------------------------------------------
# 6. test_rollback_executes_git_checkout
# ---------------------------------------------------------------------------


@patch("src.zrig.deploy_adapter.requests.get")
@patch("src.zrig.deploy_adapter.subprocess.run")
def test_rollback_executes_git_checkout(
    mock_run: MagicMock, mock_get: MagicMock
) -> None:
    """Rollback should execute git checkout with the given SHA."""
    sha = "abc123"
    mock_run.return_value = _mock_ssh_success()
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_get.return_value = mock_resp

    adapter = DeployAdapter(_make_config())
    result = adapter.rollback(sha)

    assert result.success is True
    # Verify git checkout was called (first SSH call)
    first_ssh_call = mock_run.call_args_list[0]
    cmd_str = first_ssh_call[0][0][-1]  # last element is the remote command
    assert f"git checkout {sha}" in cmd_str


# ---------------------------------------------------------------------------
# 7. test_health_check_passes_on_200
# ---------------------------------------------------------------------------


@patch("src.zrig.deploy_adapter.requests.get")
def test_health_check_passes_on_200(mock_get: MagicMock) -> None:
    """Health check should pass when the endpoint returns 200."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_get.return_value = mock_resp

    adapter = DeployAdapter(_make_config())
    passed, latency = adapter.health_check()

    assert passed is True
    assert latency >= 0


# ---------------------------------------------------------------------------
# 8. test_health_check_fails_on_500
# ---------------------------------------------------------------------------


@patch("src.zrig.deploy_adapter.time.sleep")
@patch("src.zrig.deploy_adapter.requests.get")
def test_health_check_fails_on_500(
    mock_get: MagicMock, mock_sleep: MagicMock
) -> None:
    """Health check should fail when the endpoint always returns 500."""
    mock_resp = MagicMock()
    mock_resp.status_code = 500
    mock_get.return_value = mock_resp

    config = _make_config(health_timeout_s=1)
    adapter = DeployAdapter(config)
    passed, _ = adapter.health_check()

    assert passed is False


# ---------------------------------------------------------------------------
# 9. test_health_check_timeout
# ---------------------------------------------------------------------------


@patch("src.zrig.deploy_adapter.time.sleep")
@patch("src.zrig.deploy_adapter.requests.get")
def test_health_check_timeout(
    mock_get: MagicMock, mock_sleep: MagicMock
) -> None:
    """Health check should fail when requests raise a timeout exception."""
    import requests as _req

    mock_get.side_effect = _req.Timeout("timed out")

    config = _make_config(health_timeout_s=1)
    adapter = DeployAdapter(config)
    passed, latency = adapter.health_check()

    assert passed is False


# ---------------------------------------------------------------------------
# 10. test_deploy_config_from_file
# ---------------------------------------------------------------------------


def test_deploy_config_from_file(tmp_path: Path) -> None:
    """DeployConfig.from_file should correctly load a JSON config."""
    cfg = {
        "host": "10.0.0.1",
        "user": "deploy",
        "app_path": "/srv/app",
        "service_name": "myapp.service",
        "venv_path": "/srv/app/venv",
        "git_branch": "staging",
        "health_url": "http://localhost:8080/health",
        "health_timeout_s": 15,
    }
    f = tmp_path / "deploy_config.json"
    f.write_text(json.dumps(cfg))

    loaded = DeployConfig.from_file(f)

    assert loaded.host == "10.0.0.1"
    assert loaded.user == "deploy"
    assert loaded.app_path == "/srv/app"
    assert loaded.service_name == "myapp.service"
    assert loaded.git_branch == "staging"
    assert loaded.health_timeout_s == 15


# ---------------------------------------------------------------------------
# 11. test_deploy_config_from_dict
# ---------------------------------------------------------------------------


def test_deploy_config_from_dict() -> None:
    """DeployConfig.from_dict should ignore unknown keys."""
    d = {
        "host": "1.2.3.4",
        "app_path": "/app",
        "service_name": "svc",
        "unknown_key": "should be ignored",
    }
    cfg = DeployConfig.from_dict(d)

    assert cfg.host == "1.2.3.4"
    assert cfg.app_path == "/app"
    assert cfg.user == "root"  # default
    assert not hasattr(cfg, "unknown_key")


# ---------------------------------------------------------------------------
# 12. test_validate_deploy_config_valid
# ---------------------------------------------------------------------------


def test_validate_deploy_config_valid() -> None:
    """A fully valid config should produce no errors."""
    cfg = {
        "host": "5.161.249.196",
        "app_path": "/opt/lux-wireless-staging",
        "service_name": "lux-wireless-staging.service",
        "user": "root",
        "venv_path": "/opt/lux-wireless-staging/venv",
        "health_url": "http://127.0.0.1:5001/health",
        "health_timeout_s": 30,
        "git_branch": "main",
        "pre_deploy_commands": ["echo pre"],
        "post_deploy_commands": ["echo post"],
    }
    valid, errors = validate_deploy_config(cfg)

    assert valid is True
    assert errors == []


# ---------------------------------------------------------------------------
# 13. test_validate_deploy_config_missing_host
# ---------------------------------------------------------------------------


def test_validate_deploy_config_missing_host() -> None:
    """Validation should fail when 'host' is missing."""
    cfg = {
        "app_path": "/opt/app",
        "service_name": "app.service",
    }
    valid, errors = validate_deploy_config(cfg)

    assert valid is False
    assert any("host" in e for e in errors)


# ---------------------------------------------------------------------------
# 14. test_deploy_result_dataclass
# ---------------------------------------------------------------------------


def test_deploy_result_dataclass() -> None:
    """DeployResult should initialise with correct defaults."""
    r = DeployResult(success=True)

    assert r.success is True
    assert r.steps_completed == []
    assert r.steps_failed == []
    assert r.health_check_passed is False
    assert r.rollback_commit is None
    assert r.duration_s == 0.0
    assert r.error is None
    assert r.logs == []


# ---------------------------------------------------------------------------
# 15. test_pre_post_deploy_commands_executed
# ---------------------------------------------------------------------------


@patch("src.zrig.deploy_adapter.requests.get")
@patch("src.zrig.deploy_adapter.subprocess.run")
def test_pre_post_deploy_commands_executed(
    mock_run: MagicMock, mock_get: MagicMock
) -> None:
    """Pre- and post-deploy commands should each be executed as SSH calls."""
    mock_run.return_value = _mock_ssh_success(stdout="abc123")
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_get.return_value = mock_resp

    config = _make_config(
        pre_deploy_commands=["echo warming-up", "echo ready"],
        post_deploy_commands=["echo cleanup"],
    )
    adapter = DeployAdapter(config)
    result = adapter.deploy()

    assert result.success is True
    assert "pre-deploy-0" in result.steps_completed
    assert "pre-deploy-1" in result.steps_completed
    assert "post-deploy-0" in result.steps_completed

    # Verify the actual commands were sent over SSH
    ssh_commands = [c[0][0][-1] for c in mock_run.call_args_list]
    assert "echo warming-up" in ssh_commands
    assert "echo ready" in ssh_commands
    assert "echo cleanup" in ssh_commands


# ---------------------------------------------------------------------------
# 16. test_validate_deploy_config_wrong_types
# ---------------------------------------------------------------------------


def test_validate_deploy_config_wrong_types() -> None:
    """Validation should catch type mismatches."""
    cfg = {
        "host": "1.2.3.4",
        "app_path": "/app",
        "service_name": "svc",
        "health_timeout_s": "not-an-int",
        "pre_deploy_commands": "not-a-list",
    }
    valid, errors = validate_deploy_config(cfg)

    assert valid is False
    assert any("health_timeout_s" in e for e in errors)
    assert any("pre_deploy_commands" in e for e in errors)


# ---------------------------------------------------------------------------
# 17. test_validate_deploy_config_empty_host
# ---------------------------------------------------------------------------


def test_validate_deploy_config_empty_host() -> None:
    """Validation should reject a blank host."""
    cfg = {
        "host": "   ",
        "app_path": "/app",
        "service_name": "svc",
    }
    valid, errors = validate_deploy_config(cfg)

    assert valid is False
    assert any("host" in e for e in errors)


# ---------------------------------------------------------------------------
# 18. test_validate_deploy_config_negative_timeout
# ---------------------------------------------------------------------------


def test_validate_deploy_config_negative_timeout() -> None:
    """Validation should reject non-positive health_timeout_s."""
    cfg = {
        "host": "1.2.3.4",
        "app_path": "/app",
        "service_name": "svc",
        "health_timeout_s": -5,
    }
    valid, errors = validate_deploy_config(cfg)

    assert valid is False
    assert any("health_timeout_s" in e for e in errors)


# ---------------------------------------------------------------------------
# 19. test_validate_deploy_config_list_items_must_be_strings
# ---------------------------------------------------------------------------


def test_validate_deploy_config_list_items_must_be_strings() -> None:
    """pre/post_deploy_commands list items must all be strings."""
    cfg = {
        "host": "1.2.3.4",
        "app_path": "/app",
        "service_name": "svc",
        "pre_deploy_commands": ["echo ok", 42],
    }
    valid, errors = validate_deploy_config(cfg)

    assert valid is False
    assert any("pre_deploy_commands[1]" in e for e in errors)


# ---------------------------------------------------------------------------
# 20. test_load_project_configs (integration-style with tmp_path)
# ---------------------------------------------------------------------------


def test_load_project_configs(tmp_path: Path) -> None:
    """load_project_configs should load valid configs and skip invalid ones."""
    # Valid config
    valid = {
        "host": "1.2.3.4",
        "app_path": "/app",
        "service_name": "app.service",
    }
    (tmp_path / "staging.json").write_text(json.dumps(valid))

    # Invalid config (missing host)
    invalid = {"app_path": "/app"}
    (tmp_path / "broken.json").write_text(json.dumps(invalid))

    # Non-JSON file (should be skipped)
    (tmp_path / "notes.txt").write_text("not json")

    configs = load_project_configs(tmp_path)

    assert "staging" in configs
    assert configs["staging"].host == "1.2.3.4"
    assert "broken" not in configs


# ---------------------------------------------------------------------------
# 21. test_health_check_no_url_configured
# ---------------------------------------------------------------------------


def test_health_check_no_url_configured() -> None:
    """Health check should auto-pass when no URL is configured."""
    config = _make_config(health_url="")
    adapter = DeployAdapter(config)
    passed, latency = adapter.health_check()

    assert passed is True
    assert latency == 0.0


# ---------------------------------------------------------------------------
# 22. test_deploy_no_service_name_skips_restart
# ---------------------------------------------------------------------------


@patch("src.zrig.deploy_adapter.requests.get")
@patch("src.zrig.deploy_adapter.subprocess.run")
def test_deploy_no_service_name_skips_restart(
    mock_run: MagicMock, mock_get: MagicMock
) -> None:
    """Deploy with no service_name should skip the restart step."""
    mock_run.return_value = _mock_ssh_success(stdout="abc123")
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_get.return_value = mock_resp

    config = _make_config(service_name="")
    adapter = DeployAdapter(config)
    result = adapter.deploy()

    assert result.success is True
    assert "service-restart" not in result.steps_completed

    # Verify no systemctl restart was called
    ssh_commands = [c[0][0][-1] for c in mock_run.call_args_list]
    assert not any("systemctl restart" in cmd for cmd in ssh_commands)


# ---------------------------------------------------------------------------
# 23. test_get_current_commit_failure_returns_unknown
# ---------------------------------------------------------------------------


@patch("src.zrig.deploy_adapter.subprocess.run")
def test_get_current_commit_failure_returns_unknown(mock_run: MagicMock) -> None:
    """get_current_commit should return 'unknown' when SSH fails."""
    mock_run.return_value = _mock_ssh_failure()

    adapter = DeployAdapter(_make_config())
    commit = adapter.get_current_commit()

    assert commit == "unknown"


# ---------------------------------------------------------------------------
# 24. test_validate_deploy_config_not_a_dict
# ---------------------------------------------------------------------------


def test_validate_deploy_config_not_a_dict() -> None:
    """validate_deploy_config should reject non-dict input."""
    valid, errors = validate_deploy_config("not a dict")  # type: ignore[arg-type]

    assert valid is False
    assert any("dict" in e for e in errors)


# ---------------------------------------------------------------------------
# 25. test_rollback_failure_on_pip_install
# ---------------------------------------------------------------------------


@patch("src.zrig.deploy_adapter.subprocess.run")
def test_rollback_failure_on_pip_install(mock_run: MagicMock) -> None:
    """Rollback should fail if pip install fails after checkout."""
    mock_run.side_effect = [
        _mock_ssh_success(),  # git checkout ok
        _mock_ssh_failure(stderr="pip broken"),  # pip install fails
    ]

    adapter = DeployAdapter(_make_config())
    result = adapter.rollback("abc123")

    assert result.success is False
    assert "pip-install" in result.steps_failed
    assert "pip broken" in (result.error or "")
