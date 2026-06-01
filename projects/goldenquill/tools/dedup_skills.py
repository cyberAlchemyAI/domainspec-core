"""dedup_skills — merge two skill trees (workspace/skills + tilth-workspace/skills)
into one canonical /GoldenQuill/skills/ with per-skill operator approval.

No default-to-newer. No default-to-either. Every drift decision is explicit.

Workflow
--------
1. Walk both source trees, hash each skill directory by its sorted file
   manifest (path + content sha256).
2. For skills present in only one tree → land under /GoldenQuill/skills/.
3. For skills present in both with identical hashes → land one copy.
4. For skills present in both with different hashes → DRIFT.
   - Write a side-by-side diff to tools/skill_drift_<name>.diff
   - Append (don't overwrite!) any new drift entries to tools/skill_decisions.yaml
   - DO NOT land anything. Operator must edit skill_decisions.yaml with
     {keep: workspace|tilth|both|custom, rationale: "..."} per drift entry,
     then re-run with --apply.

Rationale for requiring operator approval
-----------------------------------------
Skills are prompt assets. A newer version is not automatically a better
version — it could be a regression. A bug-fix in the "older" tree could be
silently lost. Only the operator can judge.

Usage
-----
    # Pass 1: detect and report drift
    python tools/dedup_skills.py --scan

    # Operator edits tools/skill_decisions.yaml to resolve drift
    # Pass 2: apply landed + per-decision resolutions
    python tools/dedup_skills.py --apply

Board-review fixes (2026-04-14, cross-family code review)
---------------------------------------------------------
- SECURITY: target skill names validated against strict whitelist regex to
  block path-traversal (e.g. "../../etc").
- SECURITY: DRIFT_DIR must resolve to a real sub-path of WORKSPACE (no
  symlink escape).
- BUG: all file I/O uses encoding="utf-8".
- RATIONALIZATION: --scan now MERGES new drift into the decisions file
  instead of overwriting the operator's completed entries.
- (rev-3) SECURITY: _assert_within now refuses if `root` itself is a
  symlink (otherwise both root and child resolve under attacker target,
  passing the relative_to check while actually escaping the workspace).
- (rev-3) RACE: PID-scoped staging name in _copy_skill (.<name>.<pid>.new)
  prevents concurrent --apply runs from clobbering each other's staging.
- (rev-3) GAP: case-insensitive duplicate detection in _scan_sources —
  macOS APFS collapses "SkillA" / "skilla" to one dir; operator now sees
  a warning instead of a silent overwrite at apply time.
- (rev-3) BUG: _load_decisions parser now handles escaped quotes (`\"`,
  `\\`, `\n`, `\t`) inside quoted values; previously truncated rationale
  text at the first internal quote.

- BUG: _load_decisions now uses a proper (bounded) YAML parser that handles
  quoted values containing colons.
- GAP: permission errors during scan are reported, not raised.
- ORDERING: "keep=both" aborts if the rename target already exists.
- RATIONALIZATION: --apply now precheckes that every drifted skill has a
  resolved `keep` decision; otherwise returns non-zero without copying.
- SECURITY: shutil.copytree(symlinks=False) — symlinks inside a skill are
  NOT preserved as links (prevents skill-tree from carrying link bombs).
- AMBIGUOUS: status messages to stderr; stdout is reserved for summary JSON.
"""
from __future__ import annotations

import argparse
import dataclasses
import difflib
import hashlib
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Optional

HOME = Path.home()
# Portable: derive workspace root from this file's location.
# tools/dedup_skills.py → workspace root is one parent up.
# Override via QUILL_WORKSPACE env var if needed.
import os as _os
WORKSPACE = Path(_os.environ.get("QUILL_WORKSPACE") or Path(__file__).resolve().parent.parent)

SRC_WORKSPACE = HOME / ".openclaw" / "workspace" / "skills"
SRC_TILTH = HOME / ".openclaw" / "agents" / "tilth-workspace" / "skills"
DEST = WORKSPACE / "skills"

DRIFT_DIR = WORKSPACE / "tools"
DECISIONS_FILE = DRIFT_DIR / "skill_decisions.yaml"

# Allowed skill-directory name characters. Prevents "../../x" and similar.
SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def _safe_name(name: str) -> bool:
    return bool(SAFE_NAME.match(name))


def _assert_within(root: Path, p: Path, label: str) -> None:
    """Raise if p does not resolve to a sub-path of root (blocks symlink escape).

    rev-3 hardening: also reject if `root` itself is a symlink. A malicious
    symlinked root would resolve to an external path, and the relative_to
    check would then succeed against the wrong directory — letting DRIFT_DIR
    or DEST land outside the workspace.
    """
    if root.is_symlink():
        raise RuntimeError(f"{label}: root {root} is a symlink; refuse to use")
    try:
        root_r = root.resolve()
        p_r = p.resolve()
    except OSError as e:
        raise RuntimeError(f"{label}: cannot resolve path: {e}")
    try:
        p_r.relative_to(root_r)
    except ValueError:
        raise RuntimeError(f"{label}: {p_r} escapes {root_r} (symlink or traversal)")


# --- Hash + manifest -------------------------------------------------------

def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _skill_manifest(skill_dir: Path) -> dict[str, str]:
    """Return {relative_path: sha256} for every file under skill_dir.
    Permission errors on individual files are recorded as '<perror>' sentinel."""
    manifest: dict[str, str] = {}
    for p in sorted(skill_dir.rglob("*")):
        try:
            if not p.is_file():
                continue
            rel = str(p.relative_to(skill_dir))
            manifest[rel] = _sha256_file(p)
        except PermissionError:
            rel = str(p.relative_to(skill_dir)) if skill_dir in p.parents else p.name
            manifest[rel] = "<perror>"
        except OSError:
            continue
    return manifest


def _skill_hash(manifest: dict[str, str]) -> str:
    h = hashlib.sha256()
    for rel in sorted(manifest):
        h.update(rel.encode("utf-8", errors="replace"))
        h.update(b":")
        h.update(manifest[rel].encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


# --- Classification --------------------------------------------------------

@dataclasses.dataclass
class SkillRecord:
    name: str
    in_workspace: bool
    in_tilth: bool
    ws_hash: Optional[str]
    tilth_hash: Optional[str]

    @property
    def status(self) -> str:
        if self.in_workspace and not self.in_tilth:
            return "workspace_only"
        if self.in_tilth and not self.in_workspace:
            return "tilth_only"
        if self.ws_hash == self.tilth_hash:
            return "identical"
        return "drift"


def _list_skill_dirs(root: Path) -> tuple[set[str], list[str]]:
    """Return (set of skill names, list of warnings)."""
    names: set[str] = set()
    warnings: list[str] = []
    if not root.exists():
        return names, warnings
    try:
        entries = list(root.iterdir())
    except PermissionError as e:
        warnings.append(f"cannot list {root}: {e}")
        return names, warnings
    for d in entries:
        try:
            if not d.is_dir():
                continue
        except OSError:
            continue
        if not _safe_name(d.name):
            warnings.append(f"skipping unsafe skill name {d.name!r} under {root}")
            continue
        names.add(d.name)
    return names, warnings


def _scan_sources() -> tuple[dict[str, SkillRecord], list[str]]:
    records: dict[str, SkillRecord] = {}
    ws_skills, w1 = _list_skill_dirs(SRC_WORKSPACE)
    tilth_skills, w2 = _list_skill_dirs(SRC_TILTH)
    warnings = w1 + w2

    # Case-insensitive duplicate detection. macOS APFS is case-insensitive
    # by default; "SkillA" and "skilla" are the same dir on disk but
    # different in our set. If two source roots disagree on case, the
    # operator needs to know — left silent, _apply would copy both into
    # DEST and produce two entries on a case-sensitive FS or a mysterious
    # overwrite on a case-insensitive one.
    by_lower: dict[str, list[str]] = {}
    for name in (ws_skills | tilth_skills):
        by_lower.setdefault(name.lower(), []).append(name)
    for low, variants in by_lower.items():
        if len(set(variants)) > 1:
            warnings.append(
                f"case-collision skill names: {sorted(set(variants))!r} "
                f"all collapse to {low!r} — pick one canonical spelling "
                "before --apply"
            )

    for name in sorted(ws_skills | tilth_skills):
        ws_hash = None
        tilth_hash = None
        if name in ws_skills:
            ws_hash = _skill_hash(_skill_manifest(SRC_WORKSPACE / name))
        if name in tilth_skills:
            tilth_hash = _skill_hash(_skill_manifest(SRC_TILTH / name))
        records[name] = SkillRecord(
            name=name,
            in_workspace=name in ws_skills,
            in_tilth=name in tilth_skills,
            ws_hash=ws_hash,
            tilth_hash=tilth_hash,
        )
    return records, warnings


# --- Drift diff ------------------------------------------------------------

def _write_drift_diff(rec: SkillRecord) -> Path:
    ws_dir = SRC_WORKSPACE / rec.name
    tilth_dir = SRC_TILTH / rec.name

    ws_manifest = _skill_manifest(ws_dir)
    tilth_manifest = _skill_manifest(tilth_dir)

    all_files = sorted(set(ws_manifest) | set(tilth_manifest))
    lines: list[str] = [
        f"# DRIFT for skill: {rec.name}",
        f"# workspace_hash: {rec.ws_hash}",
        f"# tilth_hash:     {rec.tilth_hash}",
        "",
    ]
    for rel in all_files:
        ws_file = ws_dir / rel
        tilth_file = tilth_dir / rel
        if not ws_file.exists():
            lines.append(f"### {rel} — present in TILTH only")
            continue
        if not tilth_file.exists():
            lines.append(f"### {rel} — present in WORKSPACE only")
            continue
        if ws_manifest.get(rel) == tilth_manifest.get(rel):
            continue
        try:
            a = ws_file.read_text(encoding="utf-8").splitlines()
            b = tilth_file.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            lines.append(f"### {rel} — binary drift (hashes differ, not text-diffable)")
            continue
        diff = difflib.unified_diff(
            a, b, fromfile=f"workspace/{rel}", tofile=f"tilth/{rel}", lineterm=""
        )
        lines.append(f"### {rel}")
        lines.extend(diff)
        lines.append("")

    out = DRIFT_DIR / f"skill_drift_{rec.name}.diff"
    DRIFT_DIR.mkdir(parents=True, exist_ok=True)
    _assert_within(WORKSPACE, DRIFT_DIR, "DRIFT_DIR")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


# --- Decisions file --------------------------------------------------------

def _write_decisions_template(drifted: list[SkillRecord]) -> Path:
    """MERGE new drift entries into skill_decisions.yaml. Never overwrite
    the operator's resolved entries."""
    DRIFT_DIR.mkdir(parents=True, exist_ok=True)
    existing = _load_decisions() if DECISIONS_FILE.exists() else {}

    header = [
        "# Skill drift decisions — REQUIRED operator input.",
        "# For each drifted skill, set 'keep' to one of: workspace | tilth | both | custom",
        "# - workspace: use the workspace/skills/ copy",
        "# - tilth:     use the tilth-workspace/skills/ copy",
        "# - both:      land both as <name>_workspace and <name>_tilth (rare)",
        "# - custom:    you'll manually merge; script will skip this skill",
        "# Add a rationale line for future auditability.",
        "",
    ]
    lines: list[str] = list(header)

    # Preserve existing entries first (in original order was not tracked; sort
    # alphabetically for reproducibility).
    for name in sorted(existing):
        e = existing[name]
        lines.extend([
            f"{name}:",
            f"  keep: {e.get('keep','CHOOSE')}  # workspace | tilth | both | custom",
            f"  rationale: \"{e.get('rationale','')}\"",
            f"  ws_hash: {e.get('ws_hash','')}",
            f"  tilth_hash: {e.get('tilth_hash','')}",
            "",
        ])

    # Append any new drift entries that aren't already recorded.
    new_names = [r.name for r in drifted if r.name not in existing]
    if new_names:
        lines.append("# --- new drift below (added by --scan) ---")
        lines.append("")
        for rec in drifted:
            if rec.name in existing:
                continue
            lines.extend([
                f"{rec.name}:",
                f"  keep: CHOOSE  # workspace | tilth | both | custom",
                f"  rationale: \"\"",
                f"  ws_hash: {rec.ws_hash}",
                f"  tilth_hash: {rec.tilth_hash}",
                "",
            ])

    DECISIONS_FILE.write_text("\n".join(lines), encoding="utf-8")
    return DECISIONS_FILE


def _strip_quotes(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
        return v[1:-1]
    return v


def _load_decisions() -> dict[str, dict]:
    """Parse the decisions YAML. Supports keys with quoted values containing
    colons (e.g. rationale: \"foo: bar\"). No yaml-lib dependency."""
    if not DECISIONS_FILE.exists():
        return {}
    decisions: dict[str, dict] = {}
    current: Optional[str] = None
    for raw in DECISIONS_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith((" ", "\t")):
            # top-level: must end with ':'
            stripped = line.strip()
            if stripped.endswith(":"):
                name = stripped[:-1].strip()
                if _safe_name(name):
                    current = name
                    decisions[current] = {}
                else:
                    current = None
            else:
                current = None
            continue
        if current is None:
            continue
        # indented key: value — split on FIRST ':' only, and strip comments
        # from outside quoted strings.
        body = line.strip()
        if ":" not in body:
            continue
        k, _, rest = body.partition(":")
        key = k.strip()
        v = rest.lstrip()
        if v.startswith(('"', "'")):
            # Quote-scanning loop: walks chars one by one so that an
            # escaped quote (`\"` or `\'`) does NOT terminate the value.
            # Prior parser used str.find which truncated rationale strings
            # at the first internal quote. Operators losing part of their
            # rationale text was a real risk on dense decisions files.
            q = v[0]
            buf = []
            i = 1
            terminated = False
            while i < len(v):
                ch = v[i]
                if ch == "\\" and i + 1 < len(v):
                    nxt = v[i + 1]
                    # Recognise common escapes: \" \' \\ \n \t
                    if nxt == q or nxt in ("\\",):
                        buf.append(nxt)
                        i += 2
                        continue
                    if nxt == "n":
                        buf.append("\n"); i += 2; continue
                    if nxt == "t":
                        buf.append("\t"); i += 2; continue
                    # Unknown escape — keep both chars verbatim.
                    buf.append(ch); buf.append(nxt); i += 2; continue
                if ch == q:
                    terminated = True
                    i += 1
                    break
                buf.append(ch)
                i += 1
            if not terminated:
                # Unterminated quote: take what we got but record the
                # condition so the operator gets a hint at apply time.
                decisions[current].setdefault("_warnings", []).append(
                    f"key {key!r}: unterminated quote in value"
                )
            decisions[current][key] = "".join(buf)
            continue
        # Unquoted value: trim trailing comment, then strip quotes.
        if "#" in v:
            v = v.split("#", 1)[0]
        decisions[current][key] = _strip_quotes(v.strip())
    return decisions


# --- Apply -----------------------------------------------------------------

def _copy_skill(src: Path, name: str, rename: Optional[str] = None) -> None:
    """Stage → atomic-swap → remove. Closes Risk 1 (mid-op crash between
    rmtree(dest) and copytree(src, dest) leaving DEST/<name> missing).

    Sequence:
      1. Copy src into a hidden staging dir: DEST/.<name>.new
      2. If DEST/<name> already exists, rename it to DEST/.<name>.old
         (atomic os.rename on same filesystem)
      3. Rename staging to DEST/<name> (atomic os.rename)
      4. Remove DEST/.<name>.old

    Worst-case crash windows:
      - Between step 1 and step 2: staging exists, original intact. Retry safe.
      - Between step 2 and step 3: original is now .old, canonical absent for
        O(ms) — a readonly reader may see it missing, but won't see partial.
        Retry safe.
      - Between step 3 and step 4: canonical present, .old leftover. Cleanup
        on next invocation (step 1 clears stale staging/.old first).
    """
    target_name = rename or name
    if not _safe_name(target_name):
        raise RuntimeError(f"unsafe target name refused: {target_name!r}")
    DEST.mkdir(parents=True, exist_ok=True)
    dest = DEST / target_name
    _assert_within(DEST, dest.parent, "DEST parent")

    # PID-scoped staging/old names prevent two concurrent `--apply` runs
    # (or a crashed-then-restarted run overlapping with its own zombie)
    # from clobbering each other's intermediate directories. Cleanup below
    # only touches names that include THIS pid, so stale artefacts from
    # other pids are left alone.
    pid = os.getpid()
    staging = DEST / f".{target_name}.{pid}.new"
    old = DEST / f".{target_name}.{pid}.old"

    # Clean up any leftover staging/.old from a previous aborted run.
    for stale in (staging, old):
        if stale.is_symlink():
            stale.unlink()
        elif stale.is_dir():
            shutil.rmtree(stale)
        elif stale.exists():
            stale.unlink()

    # 1. Stage: copy into .<name>.new. symlinks=False prevents link bombs.
    shutil.copytree(src, staging, symlinks=False)

    # 2. Move existing dest out of the way (atomic rename on same fs).
    moved_old = False
    if dest.is_symlink():
        dest.unlink()
    elif dest.is_dir():
        os.rename(dest, old)
        moved_old = True
    elif dest.exists():
        dest.unlink()

    # 3. Promote staging to canonical (atomic rename on same fs).
    os.rename(staging, dest)

    # 4. Remove old now-superseded copy.
    if moved_old and old.is_dir():
        shutil.rmtree(old)


def _apply(records: dict[str, SkillRecord]) -> tuple[int, int, list[str]]:
    """Returns (landed_count, skipped_count, warnings)."""
    DEST.mkdir(parents=True, exist_ok=True)
    decisions = _load_decisions()
    warnings: list[str] = []

    # PRECHECK: every drift must have a resolved keep before we copy anything.
    drifted = [r for r in records.values() if r.status == "drift"]
    unresolved = []
    for rec in drifted:
        d = decisions.get(rec.name, {})
        keep = (d.get("keep") or "").strip().lower()
        if keep not in {"workspace", "tilth", "both", "custom"}:
            unresolved.append(rec.name)
    if unresolved:
        warnings.append(
            f"PRECHECK FAIL: {len(unresolved)} drifted skills lack a valid 'keep' decision: "
            f"{', '.join(unresolved)}. Edit {DECISIONS_FILE} and re-run."
        )
        # Return 0 landed so caller can detect and refuse to proceed.
        return 0, len(unresolved), warnings

    # PRECHECK: block any 'both' decision that would collide with existing
    # rename-target that already exists (prevents silent overwrite).
    for rec in drifted:
        d = decisions.get(rec.name, {})
        if (d.get("keep") or "").strip().lower() == "both":
            for suffix in ("_workspace", "_tilth"):
                target = DEST / f"{rec.name}{suffix}"
                if target.exists():
                    warnings.append(
                        f"PRECHECK FAIL: {rec.name} keep=both but {target} already exists. "
                        "Remove it manually or change decision."
                    )
    if any(w.startswith("PRECHECK FAIL:") for w in warnings):
        return 0, len(unresolved) + 1, warnings

    landed = 0
    skipped = 0
    for rec in records.values():
        try:
            if rec.status == "workspace_only":
                _copy_skill(SRC_WORKSPACE / rec.name, rec.name); landed += 1
            elif rec.status == "tilth_only":
                _copy_skill(SRC_TILTH / rec.name, rec.name); landed += 1
            elif rec.status == "identical":
                _copy_skill(SRC_WORKSPACE / rec.name, rec.name); landed += 1
            elif rec.status == "drift":
                d = decisions[rec.name]
                keep = d.get("keep", "").strip().lower()
                rationale = d.get("rationale", "").strip()
                if keep in {"workspace", "tilth"} and not rationale:
                    warnings.append(f"{rec.name}: decision={keep} but no rationale")
                if keep == "workspace":
                    _copy_skill(SRC_WORKSPACE / rec.name, rec.name); landed += 1
                elif keep == "tilth":
                    _copy_skill(SRC_TILTH / rec.name, rec.name); landed += 1
                elif keep == "both":
                    _copy_skill(SRC_WORKSPACE / rec.name, rec.name, rename=f"{rec.name}_workspace")
                    _copy_skill(SRC_TILTH / rec.name, rec.name, rename=f"{rec.name}_tilth")
                    landed += 2
                elif keep == "custom":
                    warnings.append(f"{rec.name}: decision=custom, manual merge required")
                    skipped += 1
        except Exception as e:
            warnings.append(f"{rec.name}: copy failed — {type(e).__name__}: {e}")
            skipped += 1
    return landed, skipped, warnings


# --- CLI -------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Dedupe skills with per-skill operator approval")
    ap.add_argument("--scan", action="store_true",
                    help="report-only; write drift diffs and merge new drift into decisions template")
    ap.add_argument("--apply", action="store_true",
                    help="land skills; drift requires resolved decisions")
    ap.add_argument("--json", action="store_true",
                    help="emit JSON summary to stdout (status text still to stderr)")
    args = ap.parse_args()

    if not args.scan and not args.apply:
        ap.print_help()
        return 2

    if not SRC_WORKSPACE.exists() and not SRC_TILTH.exists():
        print(f"ERROR: neither {SRC_WORKSPACE} nor {SRC_TILTH} exists", file=sys.stderr)
        return 2

    t_scan0 = time.time()
    records, scan_warnings = _scan_sources()
    t_scan = time.time() - t_scan0
    by_status: dict[str, list[SkillRecord]] = {}
    for rec in records.values():
        by_status.setdefault(rec.status, []).append(rec)

    # Wall-time abort guard (Risk 7): if the scan blows past expectations on
    # this 8GB host, surface it so operator doesn't mistake a hang for work.
    SCAN_BUDGET_SEC = 60
    if t_scan > SCAN_BUDGET_SEC:
        print(f"[dedup_skills] WARN: scan took {t_scan:.1f}s "
              f"(> {SCAN_BUDGET_SEC}s budget)", file=sys.stderr)

    print(f"[dedup_skills] scanned {len(records)} skills in {t_scan:.2f}s",
          file=sys.stderr)
    for status, recs in sorted(by_status.items()):
        print(f"  {status}: {len(recs)}", file=sys.stderr)
    for w in scan_warnings:
        print(f"  SCAN-WARN: {w}", file=sys.stderr)

    if args.scan:
        drifted = by_status.get("drift", [])
        for rec in drifted:
            out = _write_drift_diff(rec)
            print(f"  drift: {rec.name} → {out.name}", file=sys.stderr)
        _write_decisions_template(drifted)
        summary = {
            "scanned": len(records),
            "by_status": {k: len(v) for k, v in by_status.items()},
            "decisions_file": str(DECISIONS_FILE),
        }
        if args.json:
            sys.stdout.write(json.dumps(summary, indent=2) + "\n")
        if drifted:
            print(f"\nDecisions required: edit {DECISIONS_FILE}", file=sys.stderr)
            print("Then re-run: python tools/dedup_skills.py --apply", file=sys.stderr)
        return 0

    # --apply
    landed, skipped, warnings = _apply(records)
    print(f"\n[dedup_skills] landed {landed}, skipped {skipped}", file=sys.stderr)
    for w in warnings:
        print(f"  WARN: {w}", file=sys.stderr)
    summary = {"landed": landed, "skipped": skipped, "warnings": warnings}
    if args.json:
        sys.stdout.write(json.dumps(summary, indent=2) + "\n")
    precheck_failed = any(w.startswith("PRECHECK FAIL:") for w in warnings)
    if precheck_failed:
        return 2
    return 0 if skipped == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
