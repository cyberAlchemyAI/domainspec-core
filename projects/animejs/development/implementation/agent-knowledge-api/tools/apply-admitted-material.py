#!/usr/bin/env python3
"""Apply one admitted WP-AKVE-001 package and emit canonical Task Session evidence."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from types import ModuleType
from typing import Any


PHASES = [
    "resolved",
    "governed",
    "admitted",
    "ticketed",
    "execution-received",
    "reconciled",
    "closeout-joined",
    "observed",
]
SCHEMAS = {
    "governance-run-request": "governance-run-request.schema.json",
    "execution-ticket": "execution-ticket.schema.json",
    "governance-phase-receipt": "governance-phase-receipt.schema.json",
    "executor-receipt": "executor-receipt.schema.json",
    "governance-terminal-receipt": "governance-terminal-receipt.schema.json",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_digest(value: object) -> str:
    return sha(
        json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode()
    )


def exact(root: Path, path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": sha(data),
        "size_bytes": len(data),
    }


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected object: {path}")
    return value


def write(path: Path, value: object) -> None:
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
    if sha(data) != baseline["sha256"] or len(data) != baseline["sizeBytes"]:
        raise ValueError(f"baseline identity changed: {baseline['path']}")


def owner(capability: str, subject: str) -> dict[str, str]:
    return {"capability": capability, "subject": subject}


def load_canonical_validator(root: Path) -> ModuleType:
    path = (
        root
        / "arcanum/arcana/task-session/development/validate-governance-run-contracts.py"
    )
    spec = importlib.util.spec_from_file_location("task_session_contracts", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load canonical validator: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_governance_documents(
    root: Path,
    request: dict[str, Any],
    ticket: dict[str, Any],
    phase_documents: list[dict[str, Any]],
    executor: dict[str, Any],
    terminal: dict[str, Any],
) -> None:
    canonical = load_canonical_validator(root)
    schema_dir = root / ".agents/skills/task-session/schemas"
    documents = {
        "governance-run-request": request,
        "execution-ticket": ticket,
        "executor-receipt": executor,
        "governance-terminal-receipt": terminal,
    }
    errors: list[str] = []
    for name, document in documents.items():
        schema = load(schema_dir / SCHEMAS[name])
        errors.extend(f"{name}: {issue}" for issue in canonical.schema_errors(document, schema))
    phase_schema = load(schema_dir / SCHEMAS["governance-phase-receipt"])
    for phase in phase_documents:
        errors.extend(
            f"phase-{phase['phase']}: {issue}"
            for issue in canonical.schema_errors(phase, phase_schema)
        )
    semantic_family = {
        **documents,
        "governance-phase-receipt": phase_documents[-1],
    }
    errors.extend(f"semantic: {issue}" for issue in canonical.semantic_errors(semantic_family))
    if errors:
        raise ValueError("canonical governance validation failed:\n" + "\n".join(errors))


def phase_document(
    *,
    run_id: str,
    task_id: str,
    swu_id: str,
    phase: str,
    phase_index: int,
    predecessor_phase: str,
    predecessor_ref: dict[str, object],
    input_refs: list[dict[str, object]],
    output_refs: list[dict[str, object]],
    result: str,
) -> dict[str, object]:
    return {
        "schema_version": "task-session.governance-phase-receipt.v1",
        "run_id": run_id,
        "task_id": task_id,
        "swu_id": swu_id,
        "phase": phase,
        "phase_index": phase_index,
        "predecessor": {
            "phase": predecessor_phase,
            "receipt_ref": predecessor_ref,
        },
        "input_refs": input_refs,
        "result": result,
        "output_refs": output_refs,
        "owner_identity": owner("task-session", "animejs-agent-knowledge-runner"),
        "idempotency_key": f"{run_id}:{phase}",
        "diagnostics": [],
    }


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
    mutation_request_path = attempt / "MUTATION-ADMISSION-REQUEST.template.json"
    package, producer, admission, mutation_request = map(
        load,
        [package_path, producer_receipt_path, admission_path, mutation_request_path],
    )
    selection_path = root / mutation_request["planAdmission"]["selectionReceipt"]["path"]
    context_path = attempt / "CONTEXT-PACK.json"
    work_pack_path = root / "projects/animejs/development/implementation/agent-knowledge-api/WORK-PACK.json"
    task_path = next(
        root / item["path"]
        for item in mutation_request["controlArtifacts"]
        if item["role"] == "task-contract"
    )
    if producer.get("patchVerdict") != "pass" or producer.get("mutationHandoff") != "ready":
        raise ValueError("Invoke material package is not ready")
    if admission.get("admissionVerdict") != "admit" or admission.get("mutationReady") is not True:
        raise ValueError("Task Session mutation admission is not ready")
    if admission.get("materialPackageDigest") != canonical_digest(package):
        raise ValueError("admitted material package digest changed")
    for baseline in mutation_request["planAdmission"]["targetBaselines"]:
        assert_baseline(root, baseline)

    touched: list[str] = []
    for change in package["changes"]:
        source = root / change["output_ref"]["path"]
        data = source.read_bytes()
        if sha(data) != change["output_ref"]["sha256"] or len(data) != change["output_ref"]["size_bytes"]:
            raise ValueError(f"staged output changed: {change['output_ref']['path']}")
        target = root / change["target_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        touched.append(change["target_path"])

    validation_results: list[dict[str, object]] = []
    result = "pass"
    stdout_bytes = 0
    stderr_bytes = 0
    stdout_truncated = False
    stderr_truncated = False
    validation_contracts = package["plan_binding"]["validation_contracts"]
    for contract in validation_contracts:
        completed = subprocess.run(
            contract["argv"],
            cwd=root / contract["cwd"],
            check=False,
            capture_output=True,
            timeout=contract["timeout_seconds"],
        )
        command_result = "pass" if completed.returncode == 0 else "block"
        if command_result == "block":
            result = "block"
        stdout_bytes += len(completed.stdout)
        stderr_bytes += len(completed.stderr)
        stdout_truncated = stdout_truncated or len(completed.stdout) > contract["max_output_bytes"]
        stderr_truncated = stderr_truncated or len(completed.stderr) > contract["max_output_bytes"]
        validation_results.append(
            {
                **contract,
                "exit_code": completed.returncode,
                "result": command_result,
            }
        )

    outputs = [exact(root, root / path) for path in touched]
    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    run_id = str(admission["attemptId"])
    task_id = str(admission["taskId"])
    swu_id = str(admission["swuId"])
    terminal_path = attempt / "TASK-SESSION-RECEIPT.json"
    executor_path = attempt / "EXECUTOR-RECEIPT.json"
    request_path = attempt / "GOVERNANCE-RUN-REQUEST.json"
    ticket_path = attempt / "EXECUTION-TICKET.json"
    consumption_path = attempt / "ADMISSION-CONSUMPTION.json"
    phases_dir = attempt / "phases"
    max_timeout = max(int(item["timeout_seconds"]) for item in validation_contracts)
    max_output = max(int(item["max_output_bytes"]) for item in validation_contracts)
    closeout_contract = {
        "required_owner_capabilities": [
            "invoke:refresh:apply-approved",
            "continuation-router:one-hop",
        ],
        "continuation_policy": "emit-cursor-never-execute-successor",
        "terminal_receipt_path": terminal_path.relative_to(root).as_posix(),
    }
    target_baselines = [
        {
            "path": item["path"],
            "state": item["state"],
            "sha256": item["sha256"],
            "size_bytes": item["sizeBytes"],
        }
        for item in mutation_request["planAdmission"]["targetBaselines"]
    ]
    plan_admission_request = {
        "plan_epoch_id": admission["planEpochId"],
        "unit_contract_digest": admission["unitContractDigest"],
        "attempt_id": run_id,
        "selection_receipt_ref": exact(root, selection_path),
        "mutation_admission_receipt_ref": exact(root, admission_path),
        "admission_token": admission["admissionToken"],
        "target_baseline_digest": admission["targetBaselineDigest"],
        "validation_contract_digest": admission["validationContractDigest"],
        "consumption_ledger_path": consumption_path.relative_to(root).as_posix(),
    }
    request = {
        "schema_version": "task-session.governance-run-request.v1",
        "admission_profile": "plan-once-selected-unit",
        "plan_admission": plan_admission_request,
        "request_id": f"request-{run_id}",
        "run_id": run_id,
        "work_pack_ref": exact(root, work_pack_path),
        "swu_ref": exact(root, task_path),
        "task_id": task_id,
        "swu_id": swu_id,
        "control_refs": [exact(root, context_path), exact(root, selection_path), exact(root, admission_path)],
        "execution_contract": {
            "allowed_writes": touched,
            "declared_outputs": touched,
            "validation_commands": validation_contracts,
            "timeout_seconds": max_timeout,
            "max_output_bytes": max_output,
        },
        "owner_identity": owner("task-session", "animejs-agent-knowledge-runner"),
        "idempotency_key": f"{run_id}:request",
        "closeout_contract": closeout_contract,
    }
    write(request_path, request)

    phase_documents: list[dict[str, Any]] = []
    phase_paths: list[Path] = []

    def emit_phase(
        phase: str,
        predecessor_phase: str,
        predecessor_ref: dict[str, object],
        input_refs: list[dict[str, object]],
        output_refs: list[dict[str, object]],
    ) -> None:
        index = len(phase_documents) + 1
        document = phase_document(
            run_id=run_id,
            task_id=task_id,
            swu_id=swu_id,
            phase=phase,
            phase_index=index,
            predecessor_phase=predecessor_phase,
            predecessor_ref=predecessor_ref,
            input_refs=input_refs,
            output_refs=output_refs,
            result=result,
        )
        path = phases_dir / f"{index:02d}-{phase}.json"
        write(path, document)
        phase_documents.append(document)
        phase_paths.append(path)

    request_ref = exact(root, request_path)
    emit_phase("resolved", "request", request_ref, [request_ref], [exact(root, context_path)])
    emit_phase("governed", "resolved", exact(root, phase_paths[-1]), [exact(root, phase_paths[-1])], [exact(root, work_pack_path)])
    emit_phase("admitted", "governed", exact(root, phase_paths[-1]), [exact(root, phase_paths[-1])], [exact(root, admission_path)])

    ticket_plan_admission = {
        **plan_admission_request,
        "target_baselines": target_baselines,
    }
    ticket = {
        "schema_version": "task-session.execution-ticket.v1",
        "admission_profile": "plan-once-selected-unit",
        "plan_admission": ticket_plan_admission,
        "ticket_id": f"ticket-{run_id}",
        "run_id": run_id,
        "task_id": task_id,
        "swu_id": swu_id,
        "request_ref": request_ref,
        "predecessor_ref": {"phase": "admitted", "receipt_ref": exact(root, phase_paths[-1])},
        "control_refs": request["control_refs"],
        "baseline_inventory": target_baselines,
        "allowed_writes": touched,
        "declared_outputs": touched,
        "validation_contracts": validation_contracts,
        "executor_contract": {
            "owner_identity": owner("implementation-executor", "animejs-agent-knowledge-executor"),
            "argv": [
                "python3",
                "projects/animejs/development/implementation/agent-knowledge-api/tools/apply-admitted-material.py",
                "--repo-root",
                ".",
                "--attempt-dir",
                attempt.relative_to(root).as_posix(),
            ],
            "cwd": ".",
            "environment_names": ["PATH"],
            "timeout_seconds": max_timeout,
            "max_output_bytes": max_output,
            "expected_receipt_path": executor_path.relative_to(root).as_posix(),
            "expected_receipt_schema_ref": exact(root, root / ".agents/skills/task-session/schemas/executor-receipt.schema.json"),
        },
        "owner_identity": owner("task-session", "animejs-agent-knowledge-runner"),
        "idempotency_key": f"{run_id}:ticket",
        "closeout_contract": closeout_contract,
    }
    write(ticket_path, ticket)
    ticket_ref = exact(root, ticket_path)
    emit_phase("ticketed", "admitted", exact(root, phase_paths[-1]), [exact(root, phase_paths[-1])], [ticket_ref])

    executor = {
        "schema_version": "task-session.executor-receipt.v1",
        "receipt_id": f"executor-receipt-{run_id}",
        "run_id": run_id,
        "task_id": task_id,
        "swu_id": swu_id,
        "ticket_ref": ticket_ref,
        "owner_identity": owner("implementation-executor", "animejs-agent-knowledge-executor"),
        "idempotency_key": f"{run_id}:executor",
        "result": result,
        "touched_files": touched,
        "outputs": outputs,
        "validation_results": validation_results,
        "bounded_capture": {
            "max_output_bytes": max_output,
            "stdout_bytes": stdout_bytes,
            "stderr_bytes": stderr_bytes,
            "stdout_truncated": stdout_truncated,
            "stderr_truncated": stderr_truncated,
        },
        "terminal_sequence": {
            "sequence_number": 1,
            "receipt_path": executor_path.relative_to(root).as_posix(),
            "final_executor_write": True,
        },
        "residue": [] if result == "pass" else ["live validation failed after candidate-local apply"],
    }
    write(executor_path, executor)
    executor_ref = exact(root, executor_path)
    emit_phase("execution-received", "ticketed", exact(root, phase_paths[-1]), [exact(root, phase_paths[-1])], [executor_ref])

    consumption = {
        "schema_version": "animejs.agent-knowledge-api.admission-consumption.v1",
        "run_id": run_id,
        "attempt_id": run_id,
        "admission_token": admission["admissionToken"],
        "mutation_admission_receipt_ref": exact(root, admission_path),
        "executor_receipt_ref": executor_ref,
        "single_use": True,
        "result": result,
        "recorded_at": generated_at,
    }
    write(consumption_path, consumption)
    reconciliation_path = attempt / "RECONCILIATION-RECEIPT.json"
    write(reconciliation_path, {
        "schema_version": "animejs.agent-knowledge-api.reconciliation-receipt.v1",
        "run_id": run_id,
        "executor_receipt_ref": executor_ref,
        "admission_consumption_ref": exact(root, consumption_path),
        "allowed_writes_equal_touched_files": sorted(ticket["allowed_writes"]) == sorted(executor["touched_files"]),
        "declared_outputs_equal_outputs": sorted(ticket["declared_outputs"]) == sorted(item["path"] for item in outputs),
        "result": result,
        "authority_effect": "none",
        "recorded_at": generated_at,
    })
    reconciliation_ref = exact(root, reconciliation_path)
    emit_phase("reconciled", "execution-received", exact(root, phase_paths[-1]), [exact(root, phase_paths[-1])], [reconciliation_ref])

    refresh_path = attempt / "INVOKE-REFRESH-RECEIPT.json"
    refresh = {
        "schema_version": "animejs.agent-knowledge-api.invoke-refresh-receipt.v1",
        "attempt_id": run_id,
        "task_id": task_id,
        "swu_id": swu_id,
        "source_receipt_ref": executor_ref,
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
    write(refresh_path, refresh)
    continuation_path = attempt / "CONTINUATION-ROUTER-RECEIPT.json"
    continuation = {
        "schema_version": "animejs.agent-knowledge-api.continuation-receipt.v1",
        "attempt_id": run_id,
        "source_receipt_ref": executor_ref,
        "verified_result": result,
        "next_unit": args.successor_unit if result == "pass" else None,
        "successor_executed": False,
        "authority_effect": "none",
        "generated_at": generated_at,
    }
    write(continuation_path, continuation)
    cursor_path = attempt / "CONTINUITY-CURSOR.json"
    cursor = {
        "schema_version": "animejs.agent-knowledge-api.continuity-cursor.v1",
        "run_id": run_id,
        "completed_unit": swu_id,
        "next_unit": args.successor_unit if result == "pass" else None,
        "source_receipts": [exact(root, refresh_path), exact(root, continuation_path)],
        "successor_executed": False,
        "authority_effect": "none",
        "generated_at": generated_at,
    }
    write(cursor_path, cursor)
    closeout_refs = [exact(root, refresh_path), exact(root, continuation_path), exact(root, cursor_path)]
    emit_phase("closeout-joined", "reconciled", exact(root, phase_paths[-1]), [exact(root, phase_paths[-1])], closeout_refs)

    observation_path = attempt / "OBSERVATION-RECEIPT.json"
    observation = {
        "schema_version": "animejs.agent-knowledge-api.observation-receipt.v1",
        "run_id": run_id,
        "task_id": task_id,
        "swu_id": swu_id,
        "closeout_phase_ref": exact(root, phase_paths[-1]),
        "result": result,
        "successor_executed": False,
        "authority_effect": "none",
        "observed_at": generated_at,
    }
    write(observation_path, observation)
    observation_ref = exact(root, observation_path)
    emit_phase("observed", "closeout-joined", exact(root, phase_paths[-1]), [exact(root, phase_paths[-1])], [observation_ref])

    terminal = {
        "schema_version": "task-session.governance-terminal-receipt.v1",
        "admission_profile": "plan-once-selected-unit",
        "consumed_admission": {
            "receipt_ref": exact(root, admission_path),
            "admission_token": admission["admissionToken"],
            "attempt_id": run_id,
            "consumption_ledger_ref": exact(root, consumption_path),
        },
        "receipt_id": f"terminal-receipt-{run_id}",
        "run_id": run_id,
        "task_id": task_id,
        "swu_id": swu_id,
        "request_ref": request_ref,
        "ticket_ref": ticket_ref,
        "predecessor_ref": {"phase": "observed", "receipt_ref": exact(root, phase_paths[-1])},
        "phase_receipts": [
            {"phase": phase, "receipt_ref": exact(root, path)}
            for phase, path in zip(PHASES, phase_paths, strict=True)
        ],
        "executor_receipt_ref": executor_ref,
        "closeout_join": {
            "required_owner_capabilities": closeout_contract["required_owner_capabilities"],
            "joined_owner_receipts": [
                {
                    "owner_capability": "invoke:refresh:apply-approved",
                    "receipt_ref": exact(root, refresh_path),
                    "result": "pass" if result == "pass" else "no-op",
                },
                {
                    "owner_capability": "continuation-router:one-hop",
                    "receipt_ref": exact(root, continuation_path),
                    "result": "pass" if result == "pass" else "no-op",
                },
            ],
            "continuation": {
                "policy": "emit-cursor-never-execute-successor",
                "cursor_ref": exact(root, cursor_path),
                "successor_executed": False,
            },
        },
        "observation_ref": observation_ref,
        "owner_identity": owner("task-session", "animejs-agent-knowledge-runner"),
        "idempotency_key": f"{run_id}:terminal",
        "result": result,
        "output_refs": outputs,
        "residue": executor["residue"],
    }
    validate_governance_documents(root, request, ticket, phase_documents, executor, terminal)
    write(terminal_path, terminal)
    print(json.dumps({
        "result": result,
        "swu_id": swu_id,
        "outputs": len(outputs),
        "validations": len(validation_results),
        "governance_documents": 13,
        "receipt": terminal_path.relative_to(root).as_posix(),
    }, indent=2, sort_keys=True))
    return 0 if result == "pass" else 3


if __name__ == "__main__":
    raise SystemExit(main())
