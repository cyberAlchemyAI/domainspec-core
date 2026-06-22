"""Z-Rig deployment adapter — SSH-based staging deployment."""
from __future__ import annotations

import json
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import requests


@dataclass
class DeployConfig:
    """Deployment target configuration."""

    host: str  # SSH host (IP or hostname)
    user: str = "root"  # SSH user
    app_path: str = ""  # Remote app directory
    service_name: str = ""  # systemd service name
    venv_path: str = ""  # Remote virtualenv path
    health_url: str = ""  # URL to check after deploy
    health_timeout_s: int = 30  # Health check timeout
    git_branch: str = "main"  # Git branch to deploy
    pre_deploy_commands: list[str] = field(default_factory=list)
    post_deploy_commands: list[str] = field(default_factory=list)

    @classmethod
    def from_file(cls, path: str | Path) -> DeployConfig:
        """Load configuration from a JSON file.

        Args:
            path: Path to the JSON configuration file.

        Returns:
            A DeployConfig instance populated from the file.

        Raises:
            FileNotFoundError: If the config file does not exist.
            json.JSONDecodeError: If the file contains invalid JSON.
        """
        raw = Path(path).read_text(encoding="utf-8")
        data = json.loads(raw)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> DeployConfig:
        """Create a DeployConfig from a plain dictionary.

        Only keys that match DeployConfig fields are used; unknown keys
        are silently ignored so config files can carry extra metadata.

        Args:
            d: Dictionary with config values.

        Returns:
            A DeployConfig instance.
        """
        known_fields = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        filtered = {k: v for k, v in d.items() if k in known_fields}
        return cls(**filtered)


@dataclass
class DeployResult:
    """Result of a deployment operation."""

    success: bool
    steps_completed: list[str] = field(default_factory=list)
    steps_failed: list[str] = field(default_factory=list)
    health_check_passed: bool = False
    rollback_commit: str | None = None  # commit SHA before deploy (for rollback)
    duration_s: float = 0.0
    error: str | None = None
    logs: list[str] = field(default_factory=list)


class DeployAdapter:
    """SSH-based deployment adapter.

    Connects to a remote host over SSH (key-based auth) and executes
    a deterministic deployment sequence:

        1. Record current commit (for rollback)
        2. Run pre-deploy commands
        3. ``git pull origin <branch>``
        4. ``pip install -r requirements.txt`` (inside venv)
        5. ``systemctl restart <service>``
        6. Wait for health check
        7. Run post-deploy commands
    """

    SSH_CONNECT_TIMEOUT = 10  # seconds

    def __init__(self, config: DeployConfig) -> None:
        self.config = config

    # ------------------------------------------------------------------
    # SSH primitive
    # ------------------------------------------------------------------

    def _ssh(self, command: str, timeout: int = 60) -> tuple[int, str, str]:
        """Execute a single command on the remote host via SSH.

        Args:
            command: Shell command to run remotely.
            timeout: Maximum seconds to wait for the command.

        Returns:
            Tuple of ``(returncode, stdout, stderr)``.
        """
        ssh_cmd = [
            "ssh",
            "-o", "BatchMode=yes",
            "-o", "StrictHostKeyChecking=accept-new",
            "-o", f"ConnectTimeout={self.SSH_CONNECT_TIMEOUT}",
            f"{self.config.user}@{self.config.host}",
            command,
        ]
        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def get_current_commit(self) -> str:
        """Get current git commit SHA on the remote server.

        Returns:
            The 40-character SHA of HEAD, or ``"unknown"`` on failure.
        """
        rc, stdout, _ = self._ssh(f"cd {self.config.app_path} && git rev-parse HEAD")
        if rc == 0 and stdout:
            return stdout.split("\n")[0].strip()
        return "unknown"

    def health_check(self) -> tuple[bool, float]:
        """Check the health URL after deployment.

        Returns:
            Tuple of ``(passed, response_time_ms)``.  If no health URL is
            configured the check is considered passed with 0 ms latency.
        """
        if not self.config.health_url:
            return True, 0.0

        deadline = time.monotonic() + self.config.health_timeout_s
        last_time_ms = 0.0

        while time.monotonic() < deadline:
            try:
                start = time.monotonic()
                resp = requests.get(self.config.health_url, timeout=5)
                last_time_ms = (time.monotonic() - start) * 1000
                if resp.status_code == 200:
                    return True, last_time_ms
            except requests.RequestException:
                pass
            time.sleep(1)

        return False, last_time_ms

    # ------------------------------------------------------------------
    # Deploy / Rollback
    # ------------------------------------------------------------------

    def _run_step(
        self,
        label: str,
        command: str,
        result: DeployResult,
        timeout: int = 120,
    ) -> bool:
        """Run a single deployment step and update *result* in-place.

        Returns:
            ``True`` if the step succeeded, ``False`` otherwise.
        """
        result.logs.append(f"[step] {label}: {command}")
        rc, stdout, stderr = self._ssh(command, timeout=timeout)
        if stdout:
            result.logs.append(f"[stdout] {stdout}")
        if stderr:
            result.logs.append(f"[stderr] {stderr}")

        if rc != 0:
            result.steps_failed.append(label)
            result.error = f"Step '{label}' failed (rc={rc}): {stderr or stdout}"
            result.logs.append(f"[FAIL] {label} rc={rc}")
            return False

        result.steps_completed.append(label)
        return True

    def deploy(self) -> DeployResult:
        """Execute the full deployment sequence.

        Steps:
            1. Record current commit (for rollback).
            2. Run pre-deploy commands.
            3. ``git pull origin <branch>``.
            4. ``pip install -r requirements.txt`` (in venv).
            5. ``systemctl restart <service>``.
            6. Health check.
            7. Run post-deploy commands.

        Returns:
            A :class:`DeployResult` summarising the deployment.
        """
        t0 = time.monotonic()
        result = DeployResult(success=False)

        # 1. Record current commit
        result.rollback_commit = self.get_current_commit()
        result.logs.append(f"[info] rollback commit: {result.rollback_commit}")

        # 2. Pre-deploy commands
        for idx, cmd in enumerate(self.config.pre_deploy_commands):
            label = f"pre-deploy-{idx}"
            if not self._run_step(label, cmd, result):
                result.duration_s = time.monotonic() - t0
                return result

        # 3. Git pull
        git_cmd = f"cd {self.config.app_path} && git pull origin {self.config.git_branch}"
        if not self._run_step("git-pull", git_cmd, result):
            result.duration_s = time.monotonic() - t0
            return result

        # 4. pip install
        if self.config.venv_path:
            pip_bin = f"{self.config.venv_path}/bin/pip"
        else:
            pip_bin = "pip"
        pip_cmd = f"cd {self.config.app_path} && {pip_bin} install -r requirements.txt"
        if not self._run_step("pip-install", pip_cmd, result):
            result.duration_s = time.monotonic() - t0
            return result

        # 5. Restart service
        if self.config.service_name:
            restart_cmd = f"systemctl restart {self.config.service_name}"
            if not self._run_step("service-restart", restart_cmd, result):
                result.duration_s = time.monotonic() - t0
                return result

        # 6. Health check
        passed, latency_ms = self.health_check()
        result.health_check_passed = passed
        result.logs.append(f"[health] passed={passed} latency={latency_ms:.1f}ms")
        if not passed:
            result.steps_failed.append("health-check")
            result.error = f"Health check failed after {self.config.health_timeout_s}s"
            result.duration_s = time.monotonic() - t0
            return result
        result.steps_completed.append("health-check")

        # 7. Post-deploy commands
        for idx, cmd in enumerate(self.config.post_deploy_commands):
            label = f"post-deploy-{idx}"
            if not self._run_step(label, cmd, result):
                result.duration_s = time.monotonic() - t0
                return result

        result.success = True
        result.duration_s = time.monotonic() - t0
        return result

    def rollback(self, commit_sha: str) -> DeployResult:
        """Rollback the remote application to a specific commit.

        Performs ``git checkout <sha>``, re-installs dependencies, and
        restarts the service.

        Args:
            commit_sha: The git commit SHA to roll back to.

        Returns:
            A :class:`DeployResult` summarising the rollback.
        """
        t0 = time.monotonic()
        result = DeployResult(success=False)
        result.rollback_commit = commit_sha
        result.logs.append(f"[info] rolling back to {commit_sha}")

        # 1. Git checkout
        checkout_cmd = f"cd {self.config.app_path} && git checkout {commit_sha}"
        if not self._run_step("git-checkout", checkout_cmd, result):
            result.duration_s = time.monotonic() - t0
            return result

        # 2. Reinstall deps
        if self.config.venv_path:
            pip_bin = f"{self.config.venv_path}/bin/pip"
        else:
            pip_bin = "pip"
        pip_cmd = f"cd {self.config.app_path} && {pip_bin} install -r requirements.txt"
        if not self._run_step("pip-install", pip_cmd, result):
            result.duration_s = time.monotonic() - t0
            return result

        # 3. Restart service
        if self.config.service_name:
            restart_cmd = f"systemctl restart {self.config.service_name}"
            if not self._run_step("service-restart", restart_cmd, result):
                result.duration_s = time.monotonic() - t0
                return result

        # 4. Health check
        passed, latency_ms = self.health_check()
        result.health_check_passed = passed
        result.logs.append(f"[health] passed={passed} latency={latency_ms:.1f}ms")
        if not passed:
            result.steps_failed.append("health-check")
            result.error = f"Health check failed after rollback to {commit_sha}"
            result.duration_s = time.monotonic() - t0
            return result
        result.steps_completed.append("health-check")

        result.success = True
        result.duration_s = time.monotonic() - t0
        return result
