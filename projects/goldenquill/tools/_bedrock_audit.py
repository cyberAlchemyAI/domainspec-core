#!/usr/bin/env python3
"""
Bedrock Audit — deterministic sweep of the canonical workspace after the
2026-04-14/15 consolidation. Runs every Logician gate we can legitimately
point at the workspace state itself (not at an in-flight grant), plus
structural checks that the bedrock work exposed as needed.

Outputs a single JSON at pipeline/validation/bedrock_audit_2026-04-15/
suitable as input to the Scribe→Editor→Judge→Red-Team council pass.

Rules:
- Everything here is deterministic. No LLM call. This is thesis-team work.
- Fail-closed: if a check can't be performed, it reports "INDETERMINATE",
  not "PASS".
- Idempotent: running twice on the same state produces the same report.
"""
from __future__ import annotations
import json
import os
import re
import sys
import subprocess
import hashlib
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path(os.environ.get("QUILL_WORKSPACE") or "/Users/goldenquill/Downloads/GoldenQuill")
AUDIT_DIR = WORKSPACE / "pipeline" / "validation" / "bedrock_audit_2026-04-15"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

# --- sanity: workspace must exist -----------------------------------------
assert WORKSPACE.exists(), f"workspace missing: {WORKSPACE}"

REPORT: dict = {
    "audit_id": "bedrock_audit_2026-04-15",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "workspace": str(WORKSPACE),
    "checks": {},
    "summary": {},
}


# =========================================================================
# Check 1 — Topology gate (shells out to the real gate; captures its JSON)
# =========================================================================
def check_topology() -> dict:
    try:
        p = subprocess.run(
            ["python3", "-m", "logician.gates.topology_gate", "--cron"],
            cwd=str(WORKSPACE),
            capture_output=True, text=True, timeout=60,
        )
        try:
            data = json.loads(p.stdout)
        except json.JSONDecodeError:
            return {"status": "INDETERMINATE", "error": "gate output not JSON",
                    "stdout": p.stdout[:2000], "stderr": p.stderr[:2000]}
        return {
            "status": "OK" if data.get("severity") == "OK"
                     else ("ERROR" if data.get("severity") == "ERROR" else "WARN"),
            "gate_severity": data.get("severity"),
            "violation_count": len(data.get("violations", [])),
            "error_count": sum(1 for v in data.get("violations", []) if v.get("severity") == "ERROR"),
            "warn_count":  sum(1 for v in data.get("violations", []) if v.get("severity") == "WARN"),
            "violations": data.get("violations", []),
            "scanned_paths": data.get("scanned_paths"),
            "gate_exit_code": p.returncode,
        }
    except Exception as e:
        return {"status": "INDETERMINATE", "error": f"{type(e).__name__}: {e}"}


# =========================================================================
# Check 2 — Admin-risk term scan over identity surface
# =========================================================================
def check_admin_risk() -> dict:
    register_path = WORKSPACE / "logician" / "registers" / "admin_risk_register.json"
    if not register_path.exists():
        return {"status": "INDETERMINATE", "error": "admin-risk register missing"}
    try:
        register = json.loads(register_path.read_text())
    except Exception as e:
        return {"status": "INDETERMINATE", "error": f"register unparseable: {e}"}

    identity_targets = [
        "SOUL.md", "USER.md", "AGENTS.md", "CLAUDE.md",
        "IDENTITY.md", "SKELETON.md", "MEMORY.md",
        "router.yaml", "lessons.md", "FOUNDATION_README.md",
    ]
    # Register entries may be a list of dicts or a dict of term→entry.
    terms = []
    if isinstance(register, list):
        for e in register:
            t = e.get("term") or e.get("phrase")
            if t:
                terms.append((t, e))
    elif isinstance(register, dict):
        # Flatten common top-level containers (e.g., {"entries":[...]}).
        entries = register.get("entries", register.get("register", []))
        if isinstance(entries, list):
            for e in entries:
                t = e.get("term") or e.get("phrase")
                if t:
                    terms.append((t, e))

    hits = []
    for fname in identity_targets:
        fp = WORKSPACE / fname
        if not fp.exists():
            continue
        text = fp.read_text(errors="replace")
        for term, entry in terms:
            # word-boundary insensitive match
            pattern = re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)
            for m in pattern.finditer(text):
                # capture some context
                start = max(0, m.start() - 40)
                end = min(len(text), m.end() + 40)
                hits.append({
                    "file": fname,
                    "term": term,
                    "severity": entry.get("severity") or entry.get("tier"),
                    "reason":   entry.get("reason") or entry.get("note") or "",
                    "suggestion": entry.get("suggestion") or entry.get("substitute") or "",
                    "context": text[start:end].replace("\n", " "),
                    "offset": m.start(),
                })

    return {
        "status": "OK" if not hits else "WARN",
        "terms_in_register": len(terms),
        "files_scanned": [f for f in identity_targets if (WORKSPACE / f).exists()],
        "hit_count": len(hits),
        "hits": hits[:100],  # cap
    }


# =========================================================================
# Check 3 — Hardcoded absolute paths in tools (Sovereignty smell)
# =========================================================================
def check_hardcoded_paths() -> dict:
    tools_dir = WORKSPACE / "tools"
    if not tools_dir.exists():
        return {"status": "INDETERMINATE", "error": "no tools/ dir"}
    patt = re.compile(r"/Users/goldenquill/")
    findings = []
    for p in tools_dir.rglob("*"):
        if p.is_file() and p.suffix in {".sh", ".py"}:
            try:
                text = p.read_text(errors="replace")
            except Exception:
                continue
            for i, line in enumerate(text.splitlines(), 1):
                if patt.search(line):
                    findings.append({
                        "file": str(p.relative_to(WORKSPACE)),
                        "line": i,
                        "text": line.strip()[:180],
                    })
    return {
        "status": "OK" if not findings else "WARN",
        "finding_count": len(findings),
        "findings": findings[:100],
        "note": "Hardcoded /Users/goldenquill/ is a topology smell — scripts won't move with the workspace.",
    }


# =========================================================================
# Check 4 — Routing consistency: router.yaml ↔ pipeline/orchestrator/routing.yaml
# =========================================================================
def _parse_simple_yaml(text: str) -> dict:
    # Minimal YAML parser for comparison purposes; dont want PyYAML dep here.
    # Best-effort; returns nested dict. Catches inline {k:v} maps.
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text) or {}
    except Exception:
        pass
    return {}

def check_routing_consistency() -> dict:
    identity = WORKSPACE / "router.yaml"
    operative = WORKSPACE / "pipeline" / "orchestrator" / "routing.yaml"
    if not identity.exists() or not operative.exists():
        return {"status": "INDETERMINATE",
                "error": f"missing: {identity.exists()=} {operative.exists()=}"}
    id_doc = _parse_simple_yaml(identity.read_text())
    op_doc = _parse_simple_yaml(operative.read_text())
    if not id_doc or not op_doc:
        return {"status": "INDETERMINATE", "error": "yaml parse failed (PyYAML not installed?)"}

    # Build canonical seat→primary map from each.
    id_seats = {}
    for seat_name, spec in (id_doc.get("tilth") or {}).items():
        if isinstance(spec, dict) and "primary" in spec:
            id_seats[seat_name] = spec.get("primary")

    active_tier = op_doc.get("active_tier", "tier_8gb")
    op_seats = {}
    for seat_name, spec in (op_doc.get("seats") or {}).items():
        if isinstance(spec, dict) and active_tier in spec:
            t = spec.get(active_tier) or {}
            if isinstance(t, dict):
                prov = t.get("provider")
                model = t.get("model")
                if prov and model:
                    op_seats[seat_name] = f"{prov}/{model}"

    mismatches = []
    shared = set(id_seats) & set(op_seats)
    for s in sorted(shared):
        if id_seats[s] != op_seats[s]:
            mismatches.append({
                "seat": s,
                "router.yaml(identity)": id_seats[s],
                "routing.yaml(operative)": op_seats[s],
            })
    only_id = sorted(set(id_seats) - set(op_seats))
    only_op = sorted(set(op_seats) - set(id_seats))

    return {
        "status": "OK" if not (mismatches or only_id or only_op) else "WARN",
        "active_tier": active_tier,
        "identity_seats": id_seats,
        "operative_seats": op_seats,
        "mismatches": mismatches,
        "only_in_router_yaml": only_id,
        "only_in_routing_yaml": only_op,
    }


# =========================================================================
# Check 5 — OpenClaw pointer alignment
# =========================================================================
def check_openclaw_pointer() -> dict:
    oc = Path.home() / ".openclaw" / "openclaw.json"
    if not oc.exists():
        return {"status": "INDETERMINATE", "error": "openclaw.json missing"}
    try:
        data = json.loads(oc.read_text())
    except Exception as e:
        return {"status": "INDETERMINATE", "error": f"unparseable: {e}"}
    tilth = None
    for a in (data.get("agents", {}).get("list") or []):
        if a.get("id") == "tilth":
            tilth = a
            break
    if not tilth:
        return {"status": "ERROR", "error": "no tilth agent in openclaw.json"}
    workspace = tilth.get("workspace", "")
    agent_dir = tilth.get("agentDir", "")
    canonical = str(WORKSPACE)
    workspace_ok = (workspace == canonical)
    # agentDir is runtime; expected to live under ~/.openclaw/. That's by design.
    return {
        "status": "OK" if workspace_ok else "ERROR",
        "tilth.workspace": workspace,
        "tilth.agentDir": agent_dir,
        "canonical_expected": canonical,
        "workspace_aligned": workspace_ok,
        "agentDir_is_runtime": agent_dir.startswith(str(Path.home() / ".openclaw")),
    }


# =========================================================================
# Check 6 — Run-log sanity: does run_log.json point at canonical paths?
# =========================================================================
def check_run_log_paths() -> dict:
    rl = WORKSPACE / "pipeline" / "orchestrator" / "run_log.json"
    if not rl.exists():
        return {"status": "INDETERMINATE", "error": "run_log.json missing"}
    try:
        data = json.loads(rl.read_text())
    except Exception as e:
        return {"status": "INDETERMINATE", "error": f"unparseable: {e}"}

    old_path = "/Users/goldenquill/.openclaw/agents/tilth-workspace"
    canonical = str(WORKSPACE)

    entries = data.get("runs", data if isinstance(data, list) else [])
    if isinstance(entries, dict):
        entries = entries.get("runs", [])

    stale = 0
    fresh = 0
    sample_stale = []
    for e in entries or []:
        if not isinstance(e, dict):
            continue
        out = e.get("output", "") or ""
        if old_path in out:
            stale += 1
            if len(sample_stale) < 5:
                sample_stale.append({"run_id": e.get("run_id"), "output": out})
        elif canonical in out:
            fresh += 1

    return {
        "status": "OK" if stale == 0 else "WARN",
        "total_runs": len(entries) if entries else 0,
        "stale_path_runs": stale,
        "canonical_path_runs": fresh,
        "sample_stale": sample_stale,
        "note": "Stale paths are historical — the files referenced may no longer exist. Not a live bug, but a forensics hazard.",
    }


# =========================================================================
# Check 7 — IDENTITY.md vs SOUL.md seat-count coherence
# =========================================================================
def check_seat_count_coherence() -> dict:
    targets = ["SOUL.md", "USER.md", "AGENTS.md", "CLAUDE.md",
               "IDENTITY.md", "SKELETON.md", "MEMORY.md"]
    results = {}
    for t in targets:
        fp = WORKSPACE / t
        if not fp.exists():
            results[t] = {"present": False}
            continue
        text = fp.read_text(errors="replace")
        four_hits = len(re.findall(r"four[- ]seat", text, re.IGNORECASE))
        five_hits = len(re.findall(r"five[- ]seat", text, re.IGNORECASE))
        editor_hits = len(re.findall(r"\bEditor\b", text))
        results[t] = {
            "present": True,
            "four_seat_mentions": four_hits,
            "five_seat_mentions": five_hits,
            "editor_mentions": editor_hits,
        }
    # Flag: any file with four-seat claim still present
    bad = [f for f, r in results.items() if r.get("four_seat_mentions", 0) > 0]
    return {
        "status": "OK" if not bad else "WARN",
        "files_still_claiming_four_seats": bad,
        "per_file": results,
    }


# =========================================================================
# Check 8 — What I touched today (fingerprint)
# =========================================================================
def check_recent_touches() -> dict:
    today = datetime.now().strftime("%Y-%m-%d")
    yday = "2026-04-14"  # the bedrock window
    # Find files modified in the last 48h under canonical
    import time
    cutoff = time.time() - (48 * 3600)
    touched = []
    for p in WORKSPACE.rglob("*"):
        if p.is_file():
            try:
                m = p.stat().st_mtime
                if m >= cutoff:
                    # skip dotdirs we don't control
                    rel = str(p.relative_to(WORKSPACE))
                    if rel.startswith(".git/") or "__pycache__" in rel:
                        continue
                    touched.append({
                        "path": rel,
                        "mtime": datetime.fromtimestamp(m, tz=timezone.utc).isoformat(),
                        "bytes": p.stat().st_size,
                    })
            except Exception:
                continue
    touched.sort(key=lambda x: x["mtime"], reverse=True)
    return {
        "status": "INFO",
        "window_hours": 48,
        "touched_count": len(touched),
        "touched": touched[:200],
    }


# =========================================================================
# Orchestrate
# =========================================================================
CHECKS = [
    ("topology_gate", check_topology),
    ("admin_risk_identity_scan", check_admin_risk),
    ("hardcoded_paths_in_tools", check_hardcoded_paths),
    ("routing_consistency", check_routing_consistency),
    ("openclaw_pointer_alignment", check_openclaw_pointer),
    ("run_log_path_hygiene", check_run_log_paths),
    ("seat_count_doc_coherence", check_seat_count_coherence),
    ("recent_touches_fingerprint", check_recent_touches),
]

for name, fn in CHECKS:
    print(f"=== {name} ===", file=sys.stderr)
    try:
        REPORT["checks"][name] = fn()
    except Exception as e:
        REPORT["checks"][name] = {"status": "INDETERMINATE",
                                  "error": f"{type(e).__name__}: {e}"}
    print(f"    status: {REPORT['checks'][name].get('status')}", file=sys.stderr)

# Summary roll-up
statuses = [c.get("status") for c in REPORT["checks"].values()]
REPORT["summary"] = {
    "ok":            sum(1 for s in statuses if s == "OK"),
    "warn":          sum(1 for s in statuses if s == "WARN"),
    "error":         sum(1 for s in statuses if s == "ERROR"),
    "indeterminate": sum(1 for s in statuses if s == "INDETERMINATE"),
    "info":          sum(1 for s in statuses if s == "INFO"),
    "overall": ("ERROR" if "ERROR" in statuses
                else "WARN" if "WARN" in statuses
                else "INDETERMINATE" if "INDETERMINATE" in statuses
                else "OK"),
}

out = AUDIT_DIR / "02_logician_audit.json"
out.write_text(json.dumps(REPORT, indent=2, default=str))
print(f"\nWrote: {out}", file=sys.stderr)
print(f"Overall: {REPORT['summary']['overall']}", file=sys.stderr)
print(json.dumps(REPORT["summary"], indent=2))
