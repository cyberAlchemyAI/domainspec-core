"""Topology Gate — filesystem zone enforcement for GoldenQuill + OpenClaw runtime.

Zones are deterministic. Unknown paths inside tracked roots are violations.
Violations log to /GoldenQuill/daily_logs/<today>.md and fail-closed block
the caller (agent startup, daily cron).

Design principles
-----------------
- Zones are path-prefix rules, not ACL rules. We do not enforce write perms;
  we report drift.
- "Unknown" ≠ "new". New files under CODE/ are normal dev flow; new files
  under IDENTITY/ or RUNTIME/ root are drift.
- Fail-closed: any ERROR-severity violation returns exit != 0 and a structured
  result. Callers decide whether to halt.
- Idempotent: running the scan twice produces the same report on a clean tree.
- Robust: broken symlinks, non-dir paths, non-UTF-8 filenames, and concurrent
  log writes do NOT crash the gate. A crashing gate is a worse fail mode than
  a clean ERROR-severity report.

Usage
-----
    result = topology_gate.run()
    if result.severity == "ERROR":
        sys.exit(1)

    # Daily cron:
    python -m pipeline.logician.gates.topology_gate --cron

Integration
-----------
Registered in Logician's gate list. Called at OpenClaw agent startup (via
agent hook) and nightly via `openclaw cron`. Results append to daily_logs.

Board-review fixes (2026-04-14, cross-family code review)
---------------------------------------------------------
- ORDERING: .git/.gitignore/.DS_Store whitelist now runs before the
  hidden-entry WARN block (previously `.git` flagged as drift).
- BUG: broken symlink no longer crashes _scan_identity_files (try/except).
- BUG: ~/.openclaw/ as a regular file no longer crashes _scan_runtime.
- BUG: log file now opened with encoding="utf-8".
- SECURITY: violation detail is escaped before being written into markdown
  daily logs (backticks/pipes in paths can't forge markdown or inject).
- CONCURRENCY: log append is protected by fcntl.flock on POSIX; best-effort
  (no-op if fcntl unavailable).
- CLI: argparse replaces the ad-hoc `--cron in sys.argv` check.

Board-review rev 3 fixes (2026-04-14, 3-seat rerun, board HEALTHY)
------------------------------------------------------------------
- SECURITY (Editor): _md_escape now also escapes `*` and `_` so a
  filename like `*important*` can't forge bold/italic and visually hide
  the real path in the daily log.
- BUG (Editor/Red Team): _scan_runtime used is_dir() which follows
  symlinks — a symlink inside ~/.openclaw/ named `workspace` pointing
  at /etc could trigger the forbidden-dir check AND allow escape.
  Now: is_dir(follow_symlinks=False); symlinks reported separately.
- MICRO (Red Team): `import stat` moved to module level (was re-imported
  per identity file in the scan loop).

Bedrock-fix pass (2026-04-15, post-council-audit)
-------------------------------------------------
- Allow-list (WORKSPACE_ROOT_OK) expanded to include the harvested
  identity files (IDENTITY.md, HEARTBEAT.md, TOOLS.md, SKELETON.md,
  FOUNDATION_README.md) and the operational dirs (state/, sessions/,
  _private/) that were introduced by the bedrock consolidation.
- RUNTIME rule refined: `agents/` is no longer a blanket forbidden dir
  (OpenClaw requires it for agent registry). Instead, we scan the
  contents of `agents/` for workspace-shaped drift (a subdir whose name
  ends `-workspace`/`_workspace`, or a subdir containing IDENTITY.md).
  This is the correct intent of the original rule: no *workspace
  content* under the runtime tree. `workspace/` at runtime root remains
  forbidden.
- Workspace drift under agents/ is reported via the new
  `workspace_drift_in_agents` rule at ERROR severity.
"""
from __future__ import annotations

import argparse
import dataclasses
import datetime
import json
import stat as _stat
import sys
from pathlib import Path

try:
    import fcntl  # POSIX-only; None on Windows
    _HAS_FCNTL = True
except ImportError:  # pragma: no cover
    _HAS_FCNTL = False

# --- Canonical zones -------------------------------------------------------

HOME = Path.home()
# Portable: derive workspace root from this file's location.
# pipeline/logician/gates/topology_gate.py → workspace root is three parents up.
# Override via QUILL_WORKSPACE env var if needed.
import os as _os
WORKSPACE = Path(_os.environ.get("QUILL_WORKSPACE") or Path(__file__).resolve().parents[3])

ZONES = {
    "IDENTITY": {
        "root": WORKSPACE,
        "files": {
            "SOUL.md", "USER.md", "AGENTS.md", "CLAUDE.md",
            "router.yaml", "lessons.md", "MEMORY.md",
        },
        "description": "Workspace-wide identity + routing files. Writes require audited decision.",
    },
    "WORKSPACE_DATA": {
        "root": WORKSPACE,
        "dirs": {"daily_logs", "orgs"},
        "description": "Append-mostly data; edits to existing entries are logged.",
    },
    "CODE": {
        "root": WORKSPACE,
        "dirs": {"pipeline", "logician", "skills", "tools"},
        "description": "Code tree. Writes are normal dev flow.",
    },
    "RUNTIME": {
        "root": HOME / ".openclaw",
        # OpenClaw itself seeds `agents/` — the directory is required for
        # agent registry (openclaw.json -> agents.list[].agentDir lives under
        # it). The topology rule is that no *workspace content* lives under
        # ~/.openclaw/. So we forbid:
        #   - a top-level `workspace/` dir (OpenClaw's default workspace slot
        #     — we don't use it; Tilth's workspace is at GoldenQuill/)
        #   - any subdir of `agents/` whose name looks like a workspace
        #     (suffix `-workspace` or contains an IDENTITY.md at its top).
        "forbidden_dirs": {"workspace"},
        "workspace_drift_under": "agents",
        "description": (
            "OpenClaw runtime churn. `agents/` is permitted (OpenClaw needs "
            "it for agent registry) but no workspace content may live inside "
            "it. `workspace/` at runtime root is forbidden — Tilth workspace "
            "is at GoldenQuill/."
        ),
    },
    "MCP": {
        "root": HOME / ".mempalace",
        "dirs": None,
        "description": "MemPalace MCP; Tilth does not write here directly.",
    },
    "ARCHIVE": {
        "root": WORKSPACE,
        "dir_prefix": "_archive_",
        "description": "Migration archive directories; frozen, never modified after creation.",
    },
}

# Always-OK entries at workspace root.
# Post-bedrock 2026-04-15: harvested identity files (IDENTITY/HEARTBEAT/TOOLS/
# SKELETON/FOUNDATION_README) and operational dirs (state/sessions/_private)
# added after the bedrock consolidation pass re-seated them at canonical root.
WORKSPACE_ROOT_OK = {
    # Identity docs
    "SOUL.md", "USER.md", "AGENTS.md", "CLAUDE.md",
    "IDENTITY.md", "HEARTBEAT.md", "TOOLS.md", "SKELETON.md",
    "FOUNDATION_README.md",
    # Routing / memory / lessons
    "router.yaml", "lessons.md", "MEMORY.md",
    # Operational dirs
    "daily_logs", "orgs", "pipeline", "logician", "skills", "tools",
    "state", "sessions", "_private",
    # Client / companion workspaces
    "HeartbeatQAfiles", "Sovereign_Node_Handoff", "mycosymbioticsandbeyond",
    "site_images",
    # Migration-era artifacts (frozen, pre-bedrock)
    "MIGRATION_PLAN_FINAL_2026-04-14.md",
    "MIGRATION_PLAN_2026-04-14.md",
    "THESIS_DEFENSE_REVIEW_2026-04-14.md",
    "REDTEAM_REVIEW_2026-04-14.md",
    "SN-QA-REPORT-2026-04-14-MIGRATION.md",
    "CODE_REVIEW_2026-04-14.md",
    "CODE_REVIEW_BOARD_HEALTH_2026-04-14.json",
    # Hidden always-OK
    ".DS_Store", ".gitignore", ".git",
}

# Hidden files always allowed (not just at root — matches .git, .gitignore, etc.)
_HIDDEN_ALWAYS_OK = {".DS_Store", ".gitignore", ".git"}


# --- Result types ----------------------------------------------------------

@dataclasses.dataclass
class Violation:
    zone: str
    severity: str          # "ERROR" | "WARN" | "INFO"
    path: str
    rule: str
    detail: str


@dataclasses.dataclass
class ScanResult:
    timestamp: str
    severity: str          # "ERROR" | "WARN" | "INFO" | "OK"
    violations: list[Violation]
    scanned_paths: int

    def to_json(self) -> str:
        return json.dumps({
            "timestamp": self.timestamp,
            "severity": self.severity,
            "violations": [dataclasses.asdict(v) for v in self.violations],
            "scanned_paths": self.scanned_paths,
        }, indent=2)


# --- Helpers ---------------------------------------------------------------

def _md_escape(s: str) -> str:
    """Escape markdown control chars so violation details can't forge log
    formatting. Escapes backticks, pipes, brackets, angle-brackets,
    backslashes, asterisks, and underscores — the last two prevent a
    filename like `*important*` from rendering bold/italic and visually
    hiding the real violating path."""
    if not s:
        return ""
    out = s.replace("\\", "\\\\")
    for ch in ("`", "|", "<", ">", "[", "]", "*", "_"):
        out = out.replace(ch, "\\" + ch)
    # Collapse newlines so one violation is one line.
    return out.replace("\r", " ").replace("\n", " ")


# --- Scan logic ------------------------------------------------------------

def _scan_workspace_root(violations: list[Violation]) -> int:
    """Check GoldenQuill root for unexpected top-level entries."""
    if not WORKSPACE.exists():
        violations.append(Violation(
            zone="IDENTITY", severity="ERROR",
            path=str(WORKSPACE), rule="workspace_exists",
            detail="GoldenQuill workspace root missing entirely",
        ))
        return 0
    if not WORKSPACE.is_dir():
        violations.append(Violation(
            zone="IDENTITY", severity="ERROR",
            path=str(WORKSPACE), rule="workspace_not_dir",
            detail="GoldenQuill path exists but is not a directory",
        ))
        return 0

    count = 0
    try:
        entries = list(WORKSPACE.iterdir())
    except (PermissionError, OSError) as e:
        violations.append(Violation(
            zone="IDENTITY", severity="ERROR",
            path=str(WORKSPACE), rule="workspace_read_failed",
            detail=f"cannot list workspace root: {type(e).__name__}: {e}",
        ))
        return 0

    for entry in entries:
        count += 1
        name = entry.name
        # Whitelist check FIRST — otherwise .git / .gitignore get misflagged
        # as "unknown hidden" because they start with a dot.
        if name in WORKSPACE_ROOT_OK:
            continue
        if name.startswith("_archive_"):
            continue  # ARCHIVE zone
        if name.startswith("."):
            # Hidden and not in whitelist → WARN (not ERROR; hidden scratch
            # from editors/tools is common).
            violations.append(Violation(
                zone="IDENTITY", severity="WARN",
                path=str(entry), rule="unknown_hidden",
                detail=f"unexpected hidden entry at workspace root: {name}",
            ))
            continue
        violations.append(Violation(
            zone="IDENTITY", severity="WARN",
            path=str(entry), rule="unknown_top_level",
            detail=f"entry at workspace root not in WORKSPACE_ROOT_OK: {name}",
        ))
    return count


def _scan_runtime(violations: list[Violation]) -> int:
    """Check ~/.openclaw/ for forbidden workspace/ or agents/ presence."""
    runtime = HOME / ".openclaw"
    if not runtime.exists():
        violations.append(Violation(
            zone="RUNTIME", severity="INFO",
            path=str(runtime), rule="runtime_absent",
            detail="~/.openclaw/ not present (pre-install state)",
        ))
        return 0
    if not runtime.is_dir():
        violations.append(Violation(
            zone="RUNTIME", severity="ERROR",
            path=str(runtime), rule="runtime_not_dir",
            detail="~/.openclaw exists but is not a directory",
        ))
        return 0

    try:
        entries = list(runtime.iterdir())
    except (PermissionError, OSError) as e:
        violations.append(Violation(
            zone="RUNTIME", severity="ERROR",
            path=str(runtime), rule="runtime_read_failed",
            detail=f"cannot list ~/.openclaw/: {type(e).__name__}: {e}",
        ))
        return 0

    forbidden = ZONES["RUNTIME"]["forbidden_dirs"]
    drift_parent = ZONES["RUNTIME"].get("workspace_drift_under")
    count = 0
    for entry in entries:
        count += 1
        # Use is_dir(follow_symlinks=False) so a malicious symlink named
        # `workspace` pointing at /etc doesn't (a) trigger a false
        # forbidden-dir ERROR, or (b) let the scan follow it out of
        # ~/.openclaw/. Symlinks inside runtime root are their own concern
        # and are reported separately.
        try:
            lst = entry.lstat()
        except OSError:
            continue
        is_symlink = _stat.S_ISLNK(lst.st_mode)
        is_real_dir = _stat.S_ISDIR(lst.st_mode)
        if is_symlink:
            violations.append(Violation(
                zone="RUNTIME", severity="WARN",
                path=str(entry), rule="runtime_symlink_present",
                detail=(
                    f"symlink {entry.name} inside ~/.openclaw/ — not "
                    "followed by scan; review manually if unexpected."
                ),
            ))
            continue
        if entry.name in forbidden and is_real_dir:
            violations.append(Violation(
                zone="RUNTIME", severity="ERROR",
                path=str(entry), rule="forbidden_runtime_dir",
                detail=(
                    f"{entry.name}/ under ~/.openclaw/ — post-migration "
                    "topology forbids this. Workspace lives at GoldenQuill."
                ),
            ))
        # Scan inside the permitted `agents/` (or configured drift_parent)
        # for workspace-shaped drift: a subdir named *-workspace* OR a subdir
        # containing an IDENTITY.md at its top is workspace content that
        # doesn't belong in the runtime tree.
        if drift_parent and entry.name == drift_parent and is_real_dir:
            count += _scan_runtime_for_drift(entry, violations)
    return count


def _scan_runtime_for_drift(agents_dir: Path, violations: list[Violation]) -> int:
    """Scan ~/.openclaw/agents/ for workspace-shaped drift.

    Workspace drift = a subdirectory of agents/ that is either:
      - named with a `-workspace` or `_workspace` suffix, OR
      - contains an IDENTITY.md file at its top level.

    Neither is allowed: agents/ holds agent registry entries (each slot is
    an agent config, not a workspace). Workspace content belongs at
    GoldenQuill/.
    """
    try:
        subs = list(agents_dir.iterdir())
    except OSError as e:
        violations.append(Violation(
            zone="RUNTIME", severity="WARN",
            path=str(agents_dir), rule="runtime_agents_unreadable",
            detail=f"cannot list {agents_dir}: {type(e).__name__}: {e}",
        ))
        return 0
    count = 0
    for sub in subs:
        count += 1
        name = sub.name
        try:
            lst = sub.lstat()
        except OSError:
            continue
        if not _stat.S_ISDIR(lst.st_mode):
            continue
        if _stat.S_ISLNK(lst.st_mode):
            continue
        suffix_drift = name.endswith("-workspace") or name.endswith("_workspace")
        identity_leak = (sub / "IDENTITY.md").exists()
        if suffix_drift or identity_leak:
            reason = []
            if suffix_drift:
                reason.append("name suffix suggests a workspace directory")
            if identity_leak:
                reason.append("contains IDENTITY.md (workspace content)")
            violations.append(Violation(
                zone="RUNTIME", severity="ERROR",
                path=str(sub), rule="workspace_drift_in_agents",
                detail=(
                    f"{name}/ under ~/.openclaw/agents/ looks like workspace "
                    f"content ({'; '.join(reason)}). Move to _archive_ under "
                    f"~/.openclaw/ or to GoldenQuill/."
                ),
            ))
    return count


def _scan_identity_files(violations: list[Violation]) -> int:
    """Check that canonical IDENTITY files exist, are regular files, and are
    non-empty. Broken symlinks are reported, not raised."""
    count = 0
    for name in ZONES["IDENTITY"]["files"]:
        p = WORKSPACE / name
        count += 1
        # lstat check catches broken symlinks without raising.
        try:
            lst = p.lstat()
        except FileNotFoundError:
            violations.append(Violation(
                zone="IDENTITY", severity="ERROR",
                path=str(p), rule="identity_file_missing",
                detail=f"canonical identity file missing: {name}",
            ))
            continue
        except OSError as e:
            violations.append(Violation(
                zone="IDENTITY", severity="ERROR",
                path=str(p), rule="identity_file_stat_failed",
                detail=f"cannot stat {name}: {type(e).__name__}: {e}",
            ))
            continue

        # Symlink? Check target resolves. (_stat imported at module level.)
        if _stat.S_ISLNK(lst.st_mode):
            try:
                st = p.stat()  # follows symlink
            except (FileNotFoundError, OSError) as e:
                violations.append(Violation(
                    zone="IDENTITY", severity="ERROR",
                    path=str(p), rule="identity_file_broken_symlink",
                    detail=f"{name} is a symlink to a missing target: {e}",
                ))
                continue
        else:
            st = lst

        if st.st_size == 0:
            violations.append(Violation(
                zone="IDENTITY", severity="ERROR",
                path=str(p), rule="identity_file_empty",
                detail=f"canonical identity file is empty: {name}",
            ))
    return count


def run() -> ScanResult:
    """Execute all zone scans. Return structured result."""
    violations: list[Violation] = []
    scanned = 0
    scanned += _scan_workspace_root(violations)
    scanned += _scan_runtime(violations)
    scanned += _scan_identity_files(violations)

    order = {"OK": 0, "INFO": 1, "WARN": 2, "ERROR": 3}
    worst = "OK"
    for v in violations:
        if order.get(v.severity, 0) > order.get(worst, 0):
            worst = v.severity

    return ScanResult(
        timestamp=datetime.datetime.now().isoformat(timespec="seconds"),
        severity=worst,
        violations=violations,
        scanned_paths=scanned,
    )


def log_to_daily(result: ScanResult) -> None:
    """Append a scan result summary to today's daily log, safely."""
    today = datetime.date.today().isoformat()
    log_dir = WORKSPACE / "daily_logs"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"[topology_gate] WARN: cannot create log dir: {e}", file=sys.stderr)
        return
    log_path = log_dir / f"{today}.md"
    block_lines = [
        "",
        f"### Topology Gate scan — {result.timestamp}",
        f"- severity: {result.severity}",
        f"- paths scanned: {result.scanned_paths}",
        f"- violations: {len(result.violations)}",
    ]
    for v in result.violations:
        block_lines.append(
            f"  - [{v.severity}] {v.zone} / {v.rule}: "
            f"{_md_escape(v.detail)} — `{_md_escape(v.path)}`"
        )
    block_lines.append("")
    block = "\n".join(block_lines)
    try:
        with log_path.open("a", encoding="utf-8") as f:
            if _HAS_FCNTL:
                try:
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                except OSError:
                    pass  # best-effort; continue unlocked
            f.write(block)
            if _HAS_FCNTL:
                try:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                except OSError:
                    pass
    except OSError as e:
        print(f"[topology_gate] WARN: cannot write daily log: {e}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Topology Gate — filesystem zone enforcement"
    )
    ap.add_argument("--cron", action="store_true",
                    help="append scan result to today's daily log regardless of severity")
    ap.add_argument("--json-only", action="store_true",
                    help="emit only the scan JSON to stdout (for pipes)")
    args = ap.parse_args(argv)

    result = run()
    if args.json_only:
        # stdout: JSON only; nothing else.
        sys.stdout.write(result.to_json() + "\n")
    else:
        # stdout is still machine-parseable JSON; human context goes to stderr.
        sys.stdout.write(result.to_json() + "\n")
    if args.cron or result.severity == "ERROR":
        log_to_daily(result)
    return 1 if result.severity == "ERROR" else 0


if __name__ == "__main__":
    sys.exit(main())
