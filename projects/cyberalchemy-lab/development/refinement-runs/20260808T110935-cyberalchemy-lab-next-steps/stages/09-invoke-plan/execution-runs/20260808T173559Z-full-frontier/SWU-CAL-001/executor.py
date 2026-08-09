#!/usr/bin/env python3
"""Apply the admitted SWU-CAL-001 material and emit one bounded executor receipt."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


REPO_ROOT = Path.cwd().resolve()
SWU_ROOT = REPO_ROOT / "projects/cyberalchemy-lab/development/refinement-runs/20260808T110935-cyberalchemy-lab-next-steps/stages/09-invoke-plan/execution-runs/20260808T173559Z-full-frontier/SWU-CAL-001"
RUN_DIR = SWU_ROOT / "governance-run"
MATERIAL_PACKAGE = SWU_ROOT / "material-package.json"
MATERIAL_RECEIPT = SWU_ROOT / "material-package-receipt.json"
TARGET_ROOT = REPO_ROOT / "projects/cyberalchemy-lab/research/tower-evidence-navigator"
RECEIPT_PATH = RUN_DIR / "terminal-executor-receipt.json"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def canonical_digest(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def exact_ref(path: Path) -> dict:
    content = path.read_bytes()
    return {
        "path": path.relative_to(REPO_ROOT).as_posix(),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def atomic_json(path: Path, value: dict) -> None:
    data = (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
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


def fail_receipt(ticket: dict, validation: list[dict], stdout: bytes, stderr: bytes, residue: str) -> None:
    receipt = {
        "schema_version": "task-session.executor-receipt.v1",
        "receipt_id": f"executor:{ticket['run_id']}:block",
        "run_id": ticket["run_id"],
        "task_id": ticket["task_id"],
        "swu_id": ticket["swu_id"],
        "ticket_ref": exact_ref(RUN_DIR / "execution-ticket.json"),
        "owner_identity": ticket["executor_contract"]["owner_identity"],
        "idempotency_key": ticket["idempotency_key"],
        "result": "block",
        "touched_files": [],
        "outputs": [],
        "validation_results": validation,
        "bounded_capture": {
            "max_output_bytes": ticket["executor_contract"]["max_output_bytes"],
            "stdout_bytes": len(stdout),
            "stderr_bytes": len(stderr),
            "stdout_truncated": False,
            "stderr_truncated": False,
        },
        "terminal_sequence": {
            "sequence_number": 1,
            "receipt_path": RECEIPT_PATH.relative_to(REPO_ROOT).as_posix(),
            "final_executor_write": True,
        },
        "residue": [residue],
    }
    atomic_json(RECEIPT_PATH, receipt)


def main() -> int:
    ticket = load(RUN_DIR / "execution-ticket.json")
    package = load(MATERIAL_PACKAGE)
    material_receipt = load(MATERIAL_RECEIPT)
    plan = ticket["plan_admission"]
    ledger = REPO_ROOT / plan["consumption_ledger_path"]
    if not ledger.is_file():
        raise RuntimeError("single-use admission was not consumed before executor launch")
    if material_receipt["packageDigest"] != canonical_digest(package):
        raise RuntimeError("material package receipt is stale")

    by_target = {item["target_path"]: item for item in package["changes"]}
    if list(by_target) != ticket["allowed_writes"]:
        raise RuntimeError("ticket write order differs from material package")
    if ticket["declared_outputs"] != ticket["allowed_writes"]:
        raise RuntimeError("executor output inventory differs from allowed writes")
    if TARGET_ROOT.exists():
        raise RuntimeError("SWU-CAL-001 target root baseline is no longer absent")

    TARGET_ROOT.parent.mkdir(parents=True, exist_ok=True)
    temporary_root = Path(
        tempfile.mkdtemp(prefix=".tower-evidence-navigator-swu001-", dir=TARGET_ROOT.parent)
    )
    applied = False
    try:
        for target_path in ticket["allowed_writes"]:
            change = by_target[target_path]
            source = REPO_ROOT / change["output_ref"]["path"]
            content = source.read_bytes()
            if hashlib.sha256(content).hexdigest() != change["output_ref"]["sha256"]:
                raise RuntimeError(f"staged output digest mismatch: {target_path}")
            if len(content) != change["output_ref"]["size_bytes"]:
                raise RuntimeError(f"staged output size mismatch: {target_path}")
            relative = (REPO_ROOT / target_path).relative_to(TARGET_ROOT)
            destination = temporary_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
        os.replace(temporary_root, TARGET_ROOT)
        applied = True

        validations = []
        stdout = b""
        stderr = b""
        for contract in ticket["validation_contracts"]:
            completed = subprocess.run(
                contract["argv"],
                cwd=REPO_ROOT if contract["cwd"] == "." else REPO_ROOT / contract["cwd"],
                shell=False,
                capture_output=True,
                timeout=contract["timeout_seconds"],
                check=False,
            )
            stdout += completed.stdout
            stderr += completed.stderr
            result = "pass" if completed.returncode == 0 else "block"
            validations.append({**contract, "exit_code": completed.returncode, "result": result})
            if completed.returncode != 0:
                shutil.rmtree(TARGET_ROOT)
                applied = False
                fail_receipt(
                    ticket,
                    validations,
                    stdout,
                    stderr,
                    f"acceptance-critical validation failed: {contract['command_id']}",
                )
                return 2

        output_refs = [exact_ref(REPO_ROOT / path) for path in ticket["declared_outputs"]]
        receipt = {
            "schema_version": "task-session.executor-receipt.v1",
            "receipt_id": f"executor:{ticket['run_id']}:pass",
            "run_id": ticket["run_id"],
            "task_id": ticket["task_id"],
            "swu_id": ticket["swu_id"],
            "ticket_ref": exact_ref(RUN_DIR / "execution-ticket.json"),
            "owner_identity": ticket["executor_contract"]["owner_identity"],
            "idempotency_key": ticket["idempotency_key"],
            "result": "pass",
            "touched_files": ticket["declared_outputs"],
            "outputs": output_refs,
            "validation_results": validations,
            "bounded_capture": {
                "max_output_bytes": ticket["executor_contract"]["max_output_bytes"],
                "stdout_bytes": len(stdout),
                "stderr_bytes": len(stderr),
                "stdout_truncated": False,
                "stderr_truncated": False,
            },
            "terminal_sequence": {
                "sequence_number": 1,
                "receipt_path": RECEIPT_PATH.relative_to(REPO_ROOT).as_posix(),
                "final_executor_write": True,
            },
            "residue": [],
        }
        atomic_json(RECEIPT_PATH, receipt)
        return 0
    finally:
        if temporary_root.exists():
            shutil.rmtree(temporary_root)
        if applied and not RECEIPT_PATH.is_file():
            shutil.rmtree(TARGET_ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
