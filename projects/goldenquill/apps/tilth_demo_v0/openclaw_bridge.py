"""
OpenClaw dispatch bridge.

The Tilth demo UI dispatches LLM work through the OpenClaw `tilth` agent.
We shell out to the `openclaw` CLI rather than calling the HTTP API directly —
the dashboard at 127.0.0.1:18789 serves an SPA, and the /v1/* paths returned
200 only because the SPA catches them as routes (not real REST endpoints).
The CLI is the actual programmatic surface.

PATH discipline: openclaw lives in ~/.npm-global/bin and depends on node at
/opt/homebrew/bin/node (Homebrew install). Both must be on PATH for the
subprocess to succeed.
"""

from __future__ import annotations

import asyncio
import os
import shlex
import uuid
from pathlib import Path
from typing import AsyncIterator

OPENCLAW_PATH_PREFIX = "/opt/homebrew/bin:" + os.path.expanduser("~/.npm-global/bin")
DEFAULT_AGENT = "tilth"
DEFAULT_TIMEOUT_SEC = 600


def new_session_id() -> str:
    """Generate a fresh openclaw session id so each dispatch is stateless.

    The default `agent:tilth:main` session accumulates conversation history
    and quickly overflows model context. For per-action UI dispatch (Scout,
    Read-Pass, Scribe), we mint a new session per call.
    """
    return f"tilth-demo-{uuid.uuid4().hex[:12]}"


def _env() -> dict[str, str]:
    """Build the environment for openclaw subprocess calls."""
    env = os.environ.copy()
    env["PATH"] = f"{OPENCLAW_PATH_PREFIX}:{env.get('PATH', '')}"
    return env


async def health_check() -> dict:
    """Return OpenClaw gateway health snapshot, or {'ok': False, 'error': ...}."""
    import httpx
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            r = await client.get("http://127.0.0.1:18789/health")
            return r.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}


async def dispatch_agent_turn(
    prompt: str,
    *,
    agent: str = DEFAULT_AGENT,
    session_id: str | None = None,
    timeout: int = DEFAULT_TIMEOUT_SEC,
) -> AsyncIterator[dict]:
    """
    Run one agent turn through the openclaw Gateway, streaming structured events.

    Correct CLI shape (verified 2026-05-11):
      openclaw agent --agent {agent} --session-id {sid} -m {prompt} --json

    Each dispatch mints a fresh session id by default — the persistent
    `agent:tilth:main` session accumulates history and overflows context.

    Yields dicts of shape:
      {"kind": "session", "session_id": ...}
      {"kind": "stdout", "text": "..."}      (raw line, mostly final JSON)
      {"kind": "result", "data": {...}}      (parsed final JSON if recognizable)
      {"kind": "exit",   "code": int}
      {"kind": "error",  "text": "..."}
    """
    sid = session_id or new_session_id()
    cmd = [
        "openclaw",
        "agent",
        "--agent", agent,
        "--session-id", sid,
        "-m", prompt,
        "--json",
    ]
    yield {"kind": "session", "session_id": sid, "cmd": " ".join(shlex.quote(c) for c in cmd)}

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=_env(),
    )
    stdout_chunks: list[str] = []
    try:
        assert proc.stdout is not None
        while True:
            try:
                line_bytes = await asyncio.wait_for(proc.stdout.readline(), timeout=timeout)
            except asyncio.TimeoutError:
                proc.kill()
                yield {"kind": "error", "text": f"[timeout after {timeout}s]"}
                return
            if not line_bytes:
                break
            line = line_bytes.decode("utf-8", errors="replace")
            stdout_chunks.append(line)
            yield {"kind": "stdout", "text": line}
    finally:
        if proc.returncode is None:
            try:
                await proc.wait()
            except Exception:
                proc.kill()

    # Try to parse the final stdout as JSON and surface the result payload.
    import json
    full_stdout = "".join(stdout_chunks).strip()
    if full_stdout:
        try:
            parsed = json.loads(full_stdout)
            yield {"kind": "result", "data": parsed}
        except json.JSONDecodeError:
            # Not valid JSON — caller saw the raw stream via stdout events.
            pass

    yield {"kind": "exit", "code": proc.returncode if proc.returncode is not None else -1}


async def dispatch_infer(
    prompt: str,
    *,
    model: str,
    timeout: int = DEFAULT_TIMEOUT_SEC,
) -> str:
    """
    Direct model inference via openclaw infer model run --gateway.

    Returns the JSON response as a string. Used for one-shot seat runs
    (Editor, Judge, Red Team) that don't need session memory.
    """
    cmd = [
        "openclaw",
        "infer",
        "model",
        "run",
        "--gateway",
        "--model", model,
        "--prompt", prompt,
        "--json",
    ]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=_env(),
    )
    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except asyncio.TimeoutError:
        proc.kill()
        return f'{{"error": "timeout after {timeout}s"}}'
    if proc.returncode != 0:
        err = (stderr or b"").decode("utf-8", errors="replace")
        return f'{{"error": "openclaw exit {proc.returncode}", "stderr": {err!r}}}'
    return (stdout or b"").decode("utf-8", errors="replace")


def workspace_root() -> Path:
    """Resolve the GoldenQuill workspace root from this file's location."""
    return Path(__file__).resolve().parent.parent.parent
