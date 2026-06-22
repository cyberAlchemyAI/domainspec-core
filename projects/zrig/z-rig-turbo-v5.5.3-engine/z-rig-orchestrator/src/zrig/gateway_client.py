#!/usr/bin/env python3
"""
HRR-005 Builder 3 — gateway_client.py

HTTP client for standalone CLI mode.
Talks directly to the OpenClaw Gateway API (http://localhost:18789 by default).

Endpoints implemented:
  - POST /sessions/spawn          → spawn a subagent session
  - GET  /sessions/{id}/status    → poll session status
  - GET  /sessions/{id}/result    → retrieve final result

Auth: reads gateway token from openclaw.json (or env OPENCLAW_GATEWAY_TOKEN).
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import httpx


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_GATEWAY_URL = "http://localhost:18789"
DEFAULT_TIMEOUT_S = 3600.0
POLL_INTERVAL_S = 3.0


@dataclass
class GatewayConfig:
    base_url: str = DEFAULT_GATEWAY_URL
    token: Optional[str] = None
    timeout_s: float = DEFAULT_TIMEOUT_S


def load_gateway_config(config_path: Optional[Path] = None) -> GatewayConfig:
    """
    Load gateway URL + token.

    Priority:
      1. OPENCLAW_GATEWAY_URL / OPENCLAW_GATEWAY_TOKEN env vars
      2. ~/.openclaw/openclaw.json
      3. defaults
    """
    base_url = os.environ.get("OPENCLAW_GATEWAY_URL", DEFAULT_GATEWAY_URL)
    token = os.environ.get("OPENCLAW_GATEWAY_TOKEN")

    if token is None and config_path is None:
        config_path = Path.home() / ".openclaw" / "openclaw.json"

    if token is None and config_path and config_path.exists():
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
            token = data.get("gateway_token") or data.get("token")
            if "gateway_url" in data:
                base_url = data["gateway_url"]
        except Exception:
            pass

    return GatewayConfig(base_url=base_url, token=token)


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

class OpenClawGatewayClient:
    """
    Minimal HTTP client for the OpenClaw Gateway.

    Usage (standalone mode):
        client = OpenClawGatewayClient()
        session_id = client.spawn_session(model="grok-4", task="...")
        status = client.wait_for_completion(session_id)
        result = client.get_result(session_id)
    """

    def __init__(self, config: Optional[GatewayConfig] = None):
        self.config = config or load_gateway_config()
        self._client = httpx.Client(
            base_url=self.config.base_url,
            timeout=30.0,
            headers=self._auth_headers(),
        )

    def _auth_headers(self) -> Dict[str, str]:
        if self.config.token:
            return {"Authorization": f"Bearer {self.config.token}"}
        return {}

    # ------------------------------------------------------------------ #
    # Core session operations                                            #
    # ------------------------------------------------------------------ #

    def spawn_session(
        self,
        model: str,
        task: str,
        timeout_ms: Optional[int] = None,
        workspace: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        POST /sessions/spawn
        Returns the new session_id.
        """
        payload = {
            "model": model,
            "task": task,
            "timeout_ms": timeout_ms,
            "workspace": workspace,
            "metadata": metadata or {},
        }
        r = self._client.post("/sessions/spawn", json=payload)
        r.raise_for_status()
        data = r.json()
        return data["session_id"]

    def get_status(self, session_id: str) -> str:
        """
        GET /sessions/{id}/status
        Returns one of: PENDING | RUNNING | COMPLETED | FAILED | TIMEOUT
        """
        r = self._client.get(f"/sessions/{session_id}/status")
        r.raise_for_status()
        return r.json().get("status", "UNKNOWN")

    def get_result(self, session_id: str) -> Dict[str, Any]:
        """
        GET /sessions/{id}/result
        Returns the final agent output envelope (or error payload).
        """
        r = self._client.get(f"/sessions/{session_id}/result")
        r.raise_for_status()
        return r.json()

    # ------------------------------------------------------------------ #
    # Convenience: wait + fetch                                          #
    # ------------------------------------------------------------------ #

    def wait_for_completion(
        self,
        session_id: str,
        poll_interval_s: float = POLL_INTERVAL_S,
        max_wait_s: Optional[float] = None,
    ) -> str:
        """
        Poll until status is terminal (COMPLETED / FAILED / TIMEOUT).
        Returns the final status.
        """
        deadline = time.time() + (max_wait_s or self.config.timeout_s)
        while time.time() < deadline:
            status = self.get_status(session_id)
            if status in ("COMPLETED", "FAILED", "TIMEOUT"):
                return status
            time.sleep(poll_interval_s)
        return "TIMEOUT"

    def spawn_and_wait(
        self,
        model: str,
        task: str,
        timeout_ms: Optional[int] = None,
        workspace: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        High-level helper: spawn → wait → fetch result.
        """
        sid = self.spawn_session(model, task, timeout_ms, workspace)
        final = self.wait_for_completion(sid)
        if final != "COMPLETED":
            raise RuntimeError(f"Session {sid} ended with status {final}")
        return self.get_result(sid)

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
