from __future__ import annotations

import json
import selectors
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from poker_agent_arena.protocol.validation import parse_agent_output


@dataclass
class AgentResponse:
    status: str
    elapsed_ms: int
    envelope: dict[str, Any] | None = None
    event_code: str | None = None
    raw_stdout: str = ""
    stderr_tail: str = ""


class AgentProcess:
    def __init__(self, command: str, agent_id: str) -> None:
        self.command = command
        self.agent_id = agent_id
        self.proc: subprocess.Popen[str] | None = None

    def _argv(self) -> list[str]:
        path = Path(self.command)
        if path.suffix == ".py" or path.exists():
            return [sys.executable, str(path)]
        return self.command.split()

    def start(self) -> None:
        if self.proc is not None and self.proc.poll() is None:
            return
        self.proc = subprocess.Popen(
            self._argv(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

    def stop(self) -> None:
        if self.proc is None:
            return
        if self.proc.poll() is None:
            self.proc.kill()
        try:
            self.proc.communicate(timeout=0.2)
        except subprocess.TimeoutExpired:
            self.proc.kill()
        self.proc = None

    def request(self, decision_envelope: dict[str, Any], timeout_ms: int) -> AgentResponse:
        self.start()
        assert self.proc is not None
        assert self.proc.stdin is not None
        assert self.proc.stdout is not None
        started = time.monotonic()
        try:
            self.proc.stdin.write(json.dumps(decision_envelope, separators=(",", ":")) + "\n")
            self.proc.stdin.flush()
        except BrokenPipeError:
            return self._done("crash", started, event_code="crash")

        selector = selectors.DefaultSelector()
        selector.register(self.proc.stdout, selectors.EVENT_READ)
        line = ""
        try:
            while True:
                remaining = timeout_ms / 1000 - (time.monotonic() - started)
                if remaining <= 0:
                    self.stop()
                    return self._done("timeout", started, event_code="timeout")
                events = selector.select(remaining)
                if events:
                    line = self.proc.stdout.readline()
                    break
                if self.proc.poll() is not None:
                    line = self.proc.stdout.readline()
                    if not line:
                        code = "crash" if self.proc.returncode not in (0, None) else "eof"
                        return self._done(code, started, event_code=code)
            if not line:
                code = "crash" if self.proc.poll() not in (0, None) else "eof"
                return self._done(code, started, event_code=code)
            parsed = parse_agent_output(line)
            if parsed.status != "ok":
                return self._done("invalid", started, event_code=parsed.event_code, raw_stdout=parsed.raw_stdout)
            return self._done("ok", started, envelope=parsed.envelope, raw_stdout=parsed.raw_stdout)
        finally:
            try:
                selector.close()
            except Exception:
                pass

    def _done(
        self,
        status: str,
        started: float,
        envelope: dict[str, Any] | None = None,
        event_code: str | None = None,
        raw_stdout: str = "",
    ) -> AgentResponse:
        elapsed_ms = int((time.monotonic() - started) * 1000)
        return AgentResponse(status, elapsed_ms, envelope=envelope, event_code=event_code, raw_stdout=raw_stdout)
