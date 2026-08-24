#!/usr/bin/env python3
"""Apply the selected OAVA-002 material package and emit one terminal receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected object: {path}")
    return value


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def exact(root: Path, path: Path) -> dict:
    data = path.read_bytes()
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": sha256(data),
        "size_bytes": len(data),
    }


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


parser = argparse.ArgumentParser()
parser.add_argument("--repo-root", required=True)
parser.add_argument("--run-dir", required=True)
parser.add_argument("--material-package", required=True)
args = parser.parse_args()

root = Path(args.repo_root).resolve()
run_dir = (root / args.run_dir).resolve()
ticket_path = run_dir / "execution-ticket.json"
ticket = load(ticket_path)
package = load((root / args.material_package).resolve())

declared = ticket["declared_outputs"]
changes = package["changes"]
if [item["target_path"] for item in changes] != declared:
    raise SystemExit("material package target order differs from execution ticket")

baseline_by_path = {item["path"]: item for item in ticket["baseline_inventory"]}
prepared: list[tuple[Path, bytes]] = []
for change in changes:
    target_path = change["target_path"]
    target = (root / target_path).resolve()
    baseline = baseline_by_path[target_path]
    if baseline != {"path": target_path, "state": "absent", "sha256": None, "size_bytes": None}:
        raise SystemExit(f"OAVA-002 expected an absent baseline: {target_path}")
    if target.exists():
        raise SystemExit(f"target appeared after admission: {target_path}")
    output_ref = change["output_ref"]
    staged = (root / output_ref["path"]).resolve()
    data = staged.read_bytes()
    if sha256(data) != output_ref["sha256"] or len(data) != output_ref["size_bytes"]:
        raise SystemExit(f"staged output identity mismatch: {target_path}")
    prepared.append((target, data))

for target, data in prepared:
    atomic_write(target, data)

validation_results = []
captured_stdout = 0
captured_stderr = 0
validation_passed = True
for contract in ticket["validation_contracts"]:
    completed = subprocess.run(
        contract["argv"],
        cwd=(root / contract["cwd"]).resolve(),
        shell=False,
        capture_output=True,
        timeout=contract["timeout_seconds"],
        check=False,
    )
    captured_stdout += len(completed.stdout)
    captured_stderr += len(completed.stderr)
    passed = completed.returncode == 0
    validation_passed = validation_passed and passed
    validation_results.append(
        {
            **contract,
            "exit_code": completed.returncode,
            "result": "pass" if passed else "block",
        }
    )

if not validation_passed:
    for target, _ in reversed(prepared):
        if target.is_file():
            target.unlink()

receipt_path = (root / ticket["executor_contract"]["expected_receipt_path"]).resolve()
outputs = [exact(root, target) for target, _ in prepared] if validation_passed else []
receipt = {
    "schema_version": "task-session.executor-receipt.v1",
    "receipt_id": "executor-receipt-oava002-v1.0.0",
    "run_id": ticket["run_id"],
    "task_id": ticket["task_id"],
    "swu_id": ticket["swu_id"],
    "ticket_ref": exact(root, ticket_path),
    "owner_identity": ticket["executor_contract"]["owner_identity"],
    "idempotency_key": ticket["idempotency_key"],
    "result": "pass" if validation_passed else "block",
    "touched_files": declared if validation_passed else [],
    "outputs": outputs,
    "validation_results": validation_results,
    "bounded_capture": {
        "max_output_bytes": ticket["executor_contract"]["max_output_bytes"],
        "stdout_bytes": captured_stdout,
        "stderr_bytes": captured_stderr,
        "stdout_truncated": captured_stdout > ticket["executor_contract"]["max_output_bytes"],
        "stderr_truncated": captured_stderr > ticket["executor_contract"]["max_output_bytes"],
    },
    "terminal_sequence": {
        "sequence_number": 2,
        "receipt_path": receipt_path.relative_to(root).as_posix(),
        "final_executor_write": True,
    },
    "residue": [] if validation_passed else ["Acceptance-critical validation failed; newly created material targets were removed."],
}
atomic_write(receipt_path, (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode())
raise SystemExit(0 if validation_passed else 1)
