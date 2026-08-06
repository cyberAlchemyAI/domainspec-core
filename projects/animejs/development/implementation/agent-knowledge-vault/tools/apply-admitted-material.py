#!/usr/bin/env python3
"""Apply one admitted Anime.js ontology material package and emit real closeout evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_digest(value: object) -> str:
    return sha256_bytes(
        json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode()
    )


def exact(root: Path, path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": sha256_bytes(data),
        "size_bytes": len(data),
    }


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"expected object: {path}")
    return value


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def assert_baseline(root: Path, baseline: dict[str, object]) -> None:
    target = root / str(baseline["path"])
    if baseline["state"] == "absent":
        if target.exists():
            raise ValueError(f"baseline changed from absent: {baseline['path']}")
        return
    if not target.is_file():
        raise ValueError(f"baseline changed from present: {baseline['path']}")
    data = target.read_bytes()
    if sha256_bytes(data) != baseline["sha256"] or len(data) != baseline["sizeBytes"]:
        raise ValueError(f"baseline identity changed: {baseline['path']}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--attempt-dir", required=True)
    parser.add_argument("--successor-unit")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    attempt = (root / args.attempt_dir).resolve()
    package_path = attempt / "producer/material-package.json"
    producer_receipt_path = attempt / "producer/material-package-receipt.json"
    admission_path = attempt / "MUTATION-ADMISSION-RECEIPT.json"
    request_path = attempt / "MUTATION-ADMISSION-REQUEST.template.json"
    selection_path = root / load(request_path)["planAdmission"]["selectionReceipt"]["path"]
    package = load(package_path)
    producer_receipt = load(producer_receipt_path)
    admission = load(admission_path)
    request = load(request_path)

    if producer_receipt.get("patchVerdict") != "pass" or producer_receipt.get("mutationHandoff") != "ready":
        raise ValueError("Invoke material package is not ready")
    if admission.get("admissionVerdict") != "admit" or admission.get("mutationReady") is not True:
        raise ValueError("Task Session mutation admission is not ready")
    if admission.get("materialPackageDigest") != canonical_digest(package):
        raise ValueError("admitted material package digest changed")
    if admission.get("attemptId") != package["plan_binding"]["attempt_id"]:
        raise ValueError("attempt identity mismatch")

    baselines = request["planAdmission"]["targetBaselines"]
    for baseline in baselines:
        assert_baseline(root, baseline)

    output_refs = []
    touched = []
    for change in package["changes"]:
        source = root / change["output_ref"]["path"]
        source_data = source.read_bytes()
        if sha256_bytes(source_data) != change["output_ref"]["sha256"] or len(source_data) != change["output_ref"]["size_bytes"]:
            raise ValueError(f"staged output changed: {change['output_ref']['path']}")
        target = root / change["target_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        touched.append(change["target_path"])
        output_refs.append(exact(root, target))

    validation_results = []
    result = "pass"
    for contract in package["plan_binding"]["validation_contracts"]:
        completed = subprocess.run(
            contract["argv"],
            cwd=root / contract["cwd"],
            check=False,
            capture_output=True,
            text=True,
            timeout=contract["timeout_seconds"],
        )
        stdout = completed.stdout.encode()[: contract["max_output_bytes"]]
        stderr = completed.stderr.encode()[: contract["max_output_bytes"]]
        command_result = "pass" if completed.returncode == 0 else "block"
        if command_result != "pass":
            result = "block"
        validation_results.append({
            **contract,
            "exit_code": completed.returncode,
            "result": command_result,
            "stdout": stdout.decode(errors="replace"),
            "stderr": stderr.decode(errors="replace"),
            "stdout_truncated": len(completed.stdout.encode()) > len(stdout),
            "stderr_truncated": len(completed.stderr.encode()) > len(stderr),
        })

    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    receipt = {
        "schema_version": "animejs.agent-knowledge-vault.task-session-receipt.v1",
        "attempt_id": admission["attemptId"],
        "task_id": admission["taskId"],
        "swu_id": admission["swuId"],
        "plan_epoch_id": admission["planEpochId"],
        "unit_contract_digest": admission["unitContractDigest"],
        "selection_receipt_ref": exact(root, selection_path),
        "material_package_ref": exact(root, package_path),
        "material_package_digest": canonical_digest(package),
        "material_receipt_ref": exact(root, producer_receipt_path),
        "mutation_admission_ref": exact(root, admission_path),
        "consumed_admission_token_sha256": sha256_bytes(str(admission["admissionToken"]).encode()),
        "single_use": True,
        "result": result,
        "touched_files": touched,
        "output_refs": output_refs,
        "validation_results": validation_results,
        "authority_effect": "none",
        "publication_class": "internal",
        "successor_unit": args.successor_unit,
        "successor_executed": False,
        "generated_at": generated_at,
        "residue": [] if result == "pass" else ["live validation failed after candidate-local apply"],
    }
    receipt_path = attempt / "TASK-SESSION-RECEIPT.json"
    write_json(receipt_path, receipt)

    refresh_receipt = {
        "schema_version": "animejs.agent-knowledge-vault.invoke-refresh-receipt.v1",
        "attempt_id": admission["attemptId"],
        "task_id": admission["taskId"],
        "swu_id": admission["swuId"],
        "source_receipt_ref": exact(root, receipt_path),
        "allowed_delta_class": "evidence_added",
        "status": "joined-pass" if result == "pass" else "joined-block",
        "plan_semantics_changed": False,
        "readiness_refresh_required": False,
        "authority_effect": "none",
        "next_owner": "task-session:selection" if result == "pass" and args.successor_unit else None,
        "successor_unit": args.successor_unit,
        "successor_executed": False,
        "generated_at": generated_at,
    }
    write_json(attempt / "INVOKE-REFRESH-RECEIPT.json", refresh_receipt)
    print(json.dumps({
        "result": result,
        "swu_id": admission["swuId"],
        "outputs": len(output_refs),
        "validations": len(validation_results),
        "receipt": receipt_path.relative_to(root).as_posix(),
    }, indent=2, sort_keys=True))
    return 0 if result == "pass" else 3


if __name__ == "__main__":
    raise SystemExit(main())
