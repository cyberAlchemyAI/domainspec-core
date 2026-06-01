"""Unit tests for logician.gates.topology_gate.

These tests build isolated tmp trees and set QUILL_WORKSPACE + HOME so the
gate's module-level constants resolve against the sandbox. Since the gate
reads WORKSPACE and HOME at import time, each test reloads the module with
importlib.reload() after setting env vars / monkeypatching Path.home.

Run from workspace root:
    python3 -m pytest logician/tests/test_topology_gate.py -v

or directly:
    python3 logician/tests/test_topology_gate.py
"""
from __future__ import annotations

import importlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))


class TopologyGateTestBase(unittest.TestCase):
    """Builds a tmp workspace + tmp openclaw runtime root, reloads the gate
    against them, and provides helpers for making the tree look the way a
    specific scenario requires."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="tg_test_"))
        self.workspace = self.tmp / "GoldenQuill"
        self.home = self.tmp / "home"
        self.workspace.mkdir()
        self.home.mkdir()
        (self.home / ".openclaw").mkdir()
        # Minimal required identity set so the IDENTITY file scan has something
        # to check; individual tests overwrite these.
        for name in ("SOUL.md", "USER.md", "AGENTS.md", "CLAUDE.md",
                     "router.yaml", "lessons.md", "MEMORY.md"):
            (self.workspace / name).write_text("x")
        self._orig_env = dict(os.environ)
        os.environ["QUILL_WORKSPACE"] = str(self.workspace)
        os.environ["HOME"] = str(self.home)
        # Import fresh each time
        if "logician.gates.topology_gate" in sys.modules:
            del sys.modules["logician.gates.topology_gate"]
        # Also clear any cached parent packages that reference Path.home()
        import logician.gates.topology_gate as tg  # noqa: E402
        importlib.reload(tg)
        # Patch module-level HOME (Path.home() may cache on some platforms)
        tg.HOME = self.home
        tg.WORKSPACE = self.workspace
        tg.ZONES["RUNTIME"]["root"] = self.home / ".openclaw"
        tg.ZONES["MCP"]["root"] = self.home / ".mempalace"
        self.tg = tg

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self._orig_env)
        shutil.rmtree(self.tmp, ignore_errors=True)

    # -- helpers -----------------------------------------------------------

    def touch(self, relpath: str, content: str = "x") -> Path:
        p = self.workspace / relpath
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        return p

    def mkdir_ws(self, relpath: str) -> Path:
        p = self.workspace / relpath
        p.mkdir(parents=True, exist_ok=True)
        return p

    def mkdir_runtime(self, relpath: str) -> Path:
        p = self.home / ".openclaw" / relpath
        p.mkdir(parents=True, exist_ok=True)
        return p


class TestCleanWorkspace(TopologyGateTestBase):
    """A clean workspace with all harvested identity files in the allow-list
    should produce OK severity."""

    def test_clean_bedrock_workspace_is_ok(self):
        # Add all harvested identity files
        for name in ("IDENTITY.md", "HEARTBEAT.md", "TOOLS.md",
                     "SKELETON.md", "FOUNDATION_README.md"):
            self.touch(name)
        for d in ("daily_logs", "orgs", "pipeline", "logician", "skills",
                  "tools", "state", "sessions", "_private",
                  "HeartbeatQAfiles", "Sovereign_Node_Handoff"):
            self.mkdir_ws(d)
        result = self.tg.run()
        self.assertEqual(result.severity, "OK",
                         msg=f"unexpected violations: {[(v.severity, v.rule, v.path) for v in result.violations]}")
        self.assertEqual(result.violations, [])


class TestUnknownTopLevel(TopologyGateTestBase):
    """A rogue top-level file should WARN."""

    def test_rogue_top_level_warns(self):
        self.touch("rogue_notes.md")
        result = self.tg.run()
        warns = [v for v in result.violations if v.rule == "unknown_top_level"]
        self.assertEqual(len(warns), 1)
        self.assertIn("rogue_notes.md", warns[0].detail)
        self.assertEqual(warns[0].severity, "WARN")


class TestIdentityMissing(TopologyGateTestBase):
    """Removing a required identity file (MEMORY.md) escalates to ERROR."""

    def test_missing_identity_file_errors(self):
        (self.workspace / "MEMORY.md").unlink()
        result = self.tg.run()
        self.assertEqual(result.severity, "ERROR")
        errs = [v for v in result.violations if v.rule == "identity_file_missing"]
        self.assertTrue(any("MEMORY.md" in v.detail for v in errs))


class TestForbiddenRuntimeDir(TopologyGateTestBase):
    """`~/.openclaw/workspace/` is forbidden; `~/.openclaw/agents/` is OK
    unless it contains workspace-shaped drift."""

    def test_workspace_dir_under_openclaw_errors(self):
        self.mkdir_runtime("workspace")
        result = self.tg.run()
        errs = [v for v in result.violations if v.rule == "forbidden_runtime_dir"]
        self.assertEqual(len(errs), 1)
        self.assertIn("workspace", errs[0].path)
        self.assertEqual(result.severity, "ERROR")

    def test_agents_dir_alone_is_ok(self):
        self.mkdir_runtime("agents")
        result = self.tg.run()
        # agents/ alone: no forbidden_runtime_dir, no drift sub-errors.
        self.assertNotIn("forbidden_runtime_dir", [v.rule for v in result.violations])
        self.assertNotIn("workspace_drift_in_agents",
                         [v.rule for v in result.violations])

    def test_agents_with_workspace_suffix_subdir_errors(self):
        self.mkdir_runtime("agents/tilth-workspace")
        result = self.tg.run()
        drift = [v for v in result.violations
                 if v.rule == "workspace_drift_in_agents"]
        self.assertEqual(len(drift), 1)
        self.assertIn("tilth-workspace", drift[0].path)
        self.assertEqual(drift[0].severity, "ERROR")

    def test_agents_with_identity_leak_errors(self):
        d = self.mkdir_runtime("agents/stealth")
        (d / "IDENTITY.md").write_text("leaked")
        result = self.tg.run()
        drift = [v for v in result.violations
                 if v.rule == "workspace_drift_in_agents"]
        self.assertEqual(len(drift), 1)
        self.assertIn("IDENTITY.md", drift[0].detail)

    def test_agents_with_normal_subagent_is_ok(self):
        d = self.mkdir_runtime("agents/tilth")
        (d / "agent").mkdir()
        (d / "agent" / "config.json").write_text("{}")
        result = self.tg.run()
        self.assertNotIn("workspace_drift_in_agents",
                         [v.rule for v in result.violations])


class TestSymlinkSafety(TopologyGateTestBase):
    """Symlinks inside ~/.openclaw/ must not be followed and must not trigger
    false forbidden-dir ERRORs."""

    def test_workspace_symlink_does_not_escape_or_error(self):
        runtime = self.home / ".openclaw"
        # Create a symlink NAMED `workspace` pointing at /tmp — if the scan
        # followed it, it would either false-ERROR (if is_dir() followed) or
        # escape. Neither must happen.
        link = runtime / "workspace"
        link.symlink_to(self.tmp)  # /tmp-ish target
        result = self.tg.run()
        # forbidden_runtime_dir must NOT fire on a symlink
        fr = [v for v in result.violations if v.rule == "forbidden_runtime_dir"]
        self.assertEqual(fr, [])
        # A WARN about the symlink itself is expected
        sym_warn = [v for v in result.violations
                    if v.rule == "runtime_symlink_present"]
        self.assertEqual(len(sym_warn), 1)


class TestMarkdownEscape(TopologyGateTestBase):
    """Filenames with markdown control chars must be escaped in the daily log."""

    def test_md_escape_blocks_injection(self):
        out = self.tg._md_escape("*sneaky* `backtick` [link](x) |pipe|")
        # Every control char should be backslashed
        for ch in ("*", "`", "[", "]", "|"):
            self.assertIn("\\" + ch, out)


class TestCLIExitCodes(TopologyGateTestBase):
    """Running as a script exits non-zero on ERROR, zero on OK."""

    def test_cli_exits_zero_on_clean(self):
        for name in ("IDENTITY.md", "HEARTBEAT.md", "TOOLS.md",
                     "SKELETON.md", "FOUNDATION_README.md"):
            self.touch(name)
        env = dict(os.environ)
        env["QUILL_WORKSPACE"] = str(self.workspace)
        env["HOME"] = str(self.home)
        r = subprocess.run(
            [sys.executable, "-m", "logician.gates.topology_gate", "--json-only"],
            cwd=str(REPO_ROOT), env=env, capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, msg=r.stderr + r.stdout)
        payload = json.loads(r.stdout)
        self.assertIn(payload["severity"], ("OK", "INFO", "WARN"))

    def test_cli_exits_nonzero_on_error(self):
        self.mkdir_runtime("workspace")
        env = dict(os.environ)
        env["QUILL_WORKSPACE"] = str(self.workspace)
        env["HOME"] = str(self.home)
        r = subprocess.run(
            [sys.executable, "-m", "logician.gates.topology_gate", "--json-only"],
            cwd=str(REPO_ROOT), env=env, capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 1)
        payload = json.loads(r.stdout)
        self.assertEqual(payload["severity"], "ERROR")


if __name__ == "__main__":
    unittest.main(verbosity=2)
