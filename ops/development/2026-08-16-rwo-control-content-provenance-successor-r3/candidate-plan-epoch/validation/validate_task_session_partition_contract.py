#!/usr/bin/env python3
"""Validate the three-unit R3 successor against fast-entry partition semantics."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path


SOURCE_BINDINGS = {
    "arcanum/arcana/task-session/scripts/task-session-governance-runner.py": "fdaf210967aa2be5f5c94c32c7be22344ff23737d6213b31826ba9ba0d24fa1c",
    "arcanum/arcana/task-session/schemas/governance-run-request.schema.json": "865e58ec48a4e2ebf009282fa7411220c265949ae7c52a9e9c638e96a103ed07",
    "arcanum/arcana/task-session/schemas/fast-execution-entry-receipt.schema.json": "9763c941f969bfe4ad00409ff84b79f864f090432231e738fef0f39ca72d2ec9",
    "arcanum/arcana/task-session/schemas/mutation-admission-request.schema.json": "e9017a5efa7a00870ffbe6db1f3671f23700d9a8390dba6058a14ba2fc1379a4",
    "arcanum/arcana/task-session/schemas/mutation-admission-receipt.schema.json": "1eb07937cf40e5487af790f65be6b6be844f705e091d63bc4079d4fcc67ecfb6",
    "arcanum/arcana/task-session/development/test_plan_once_governance.py": "71bc3bc2dad1476f8be77bc9d391c02665ef43316ee13fd55272cad3b4930f4f",
    "arcanum/arcana/task-session/development/validate-governance-runner.py": "b34406298f57f8d89be7ff5c7ff30b6b88db8e76fa6791888c99622a363eeea4",
    "arcanum/arcana/task-session/development/test_plan_once_admission.py": "cd5ecc7dfa3fd25b46a59cef4a6aee2afbe20afc422c4c6bfc5e1a3b91658d18",
}


class ContractError(RuntimeError):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def embedded_task(path: Path) -> dict:
    match = re.search(r"```json\n(.*?)\n```", path.read_text(encoding="utf-8"), re.S)
    if match is None:
        raise ContractError("TASK_CONTRACT_MISSING", path.as_posix())
    return json.loads(match.group(1))


def expand_groups(groups: list[dict]) -> list[str]:
    result: list[str] = []
    for group in groups:
        prefix = group["prefix"].rstrip("/")
        for member in group["members"]:
            result.append(f"{prefix}/{member}" if prefix else member)
    return result


def material_paths(task: dict) -> list[str]:
    if "material_write_groups" in task:
        return expand_groups(task["material_write_groups"])
    return list(task.get("material_writes", []))


def mutation_outputs(task: dict) -> list[str]:
    return expand_groups(task["execution_output_groups"])


def require_unique(values: list[str], label: str) -> None:
    if len(values) != len(set(values)):
        raise ContractError("DUPLICATE_PARTITION_PATH", label)


def check_partition(task: dict, *, injected_negative: bool = False) -> dict:
    partition = task["task_session_partition_contract"]
    route_receipt = partition["route_expected_receipt"]
    pre_execution = list(partition["pre_execution_controls"])
    validation = list(partition["validation_outputs"])
    lifecycle = list(partition["lifecycle_outputs"])
    baselines = list(partition["target_baseline_paths"])
    material = material_paths(task)
    outputs = mutation_outputs(task)
    allowed = sorted(set(material + outputs))

    for values, label in (
        (pre_execution, "pre-execution controls"),
        (validation, "validation outputs"),
        (lifecycle, "lifecycle outputs"),
        (baselines, "target baselines"),
        (material, "material writes"),
        (outputs, "execution outputs"),
    ):
        require_unique(values, label)

    topology = task["receipt_topology"]
    if route_receipt != topology["E"]:
        raise ContractError("ROUTE_RECEIPT_NOT_E", task["task_id"])
    if validation != [topology["V"]]:
        raise ContractError("VALIDATION_PARTITION_INVALID", task["task_id"])
    if lifecycle != [topology[key] for key in ("O", "P", "C", "B", "T")]:
        raise ContractError("LIFECYCLE_PARTITION_INVALID", task["task_id"])
    if set(pre_execution) & ({route_receipt} | set(validation) | set(lifecycle)):
        raise ContractError("PRE_EXECUTION_PARTITION_COLLISION", task["task_id"])

    if task["write_profile"] == "execution-output-only":
        if injected_negative:
            outputs = sorted(set(outputs + [route_receipt]))
            allowed = sorted(set(allowed + [route_receipt]))
            baselines = sorted(set(baselines + [route_receipt]))
        if route_receipt in outputs or route_receipt in allowed or route_receipt in baselines:
            raise ContractError("OUTPUT_ONLY_ROUTE_RECEIPT_COLLISION", task["task_id"])
        if material:
            raise ContractError("OUTPUT_ONLY_MATERIAL_WRITE", task["task_id"])
        if sorted(baselines) != sorted(outputs):
            raise ContractError("OUTPUT_ONLY_BASELINE_MISMATCH", task["task_id"])
        requested = outputs
    elif task["write_profile"] == "material-bound":
        if outputs != [route_receipt]:
            raise ContractError("MATERIAL_TERMINAL_OUTPUT_MISMATCH", task["task_id"])
        if route_receipt in material or route_receipt in baselines:
            raise ContractError("MATERIAL_ROUTE_RECEIPT_COLLISION", task["task_id"])
        if sorted(baselines) != sorted(material):
            raise ContractError("MATERIAL_BASELINE_MISMATCH", task["task_id"])
        requested = material
    else:
        raise ContractError("UNKNOWN_WRITE_PROFILE", task["task_id"])

    route_scope = sorted(set(requested + [route_receipt]))
    if sorted(partition["route_write_scope"]) != route_scope:
        raise ContractError("ROUTE_SCOPE_PARTITION_MISMATCH", task["task_id"])
    if sorted(partition["admission_material_writes"]) != sorted(material):
        raise ContractError("ADMISSION_MATERIAL_PARTITION_MISMATCH", task["task_id"])
    if sorted(partition["admission_execution_outputs"]) != sorted(outputs):
        raise ContractError("ADMISSION_OUTPUT_PARTITION_MISMATCH", task["task_id"])
    if sorted(partition["admission_allowed_writes"]) != allowed:
        raise ContractError("ADMISSION_ALLOWED_PARTITION_MISMATCH", task["task_id"])
    return {
        "task_id": task["task_id"],
        "write_profile": task["write_profile"],
        "requested_write_count": len(requested),
        "route_scope_count": len(route_scope),
        "route_expected_receipt": route_receipt,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-root", type=Path, required=True)
    parser.add_argument("--repository-root", type=Path, default=Path("."))
    args = parser.parse_args()
    candidate = args.candidate_root.resolve()
    repository = args.repository_root.resolve()

    for relative, expected in SOURCE_BINDINGS.items():
        actual = sha256(repository / relative)
        if actual != expected:
            raise ContractError("TASK_SESSION_SOURCE_DRIFT", relative)

    entry = json.loads((candidate / "EXECUTION-ENTRY.json").read_text(encoding="utf-8"))
    audit = json.loads(
        (candidate / "readiness/AUDIT-CONFIG-v2.json").read_text(encoding="utf-8")
    )
    routes = {
        route["frontier_swu"]: route for route in entry["execution_policy"]["allowed_routes"]
    }
    bindings = {binding["swu_id"]: binding for binding in audit["execution_bindings"]}
    task_paths = sorted((candidate / "work-pack/tasks").glob("TASK-*.md"))
    if len(task_paths) != 3:
        raise ContractError("TASK_COUNT_INVALID", str(len(task_paths)))

    positives = []
    negative_count = 0
    for path in task_paths:
        task = embedded_task(path)
        positive = check_partition(task)
        positives.append(positive)
        route = routes[task["swu_id"]]
        partition = task["task_session_partition_contract"]
        if route["expected_receipt"] != partition["route_expected_receipt"]:
            raise ContractError("ENTRY_ROUTE_RECEIPT_MISMATCH", task["task_id"])
        if sorted(route["write_scope"]) != sorted(partition["route_write_scope"]):
            raise ContractError("ENTRY_ROUTE_SCOPE_MISMATCH", task["task_id"])
        binding = bindings[task["swu_id"]]
        if sorted(binding["material_writes"]) != sorted(partition["admission_material_writes"]):
            raise ContractError("AUDIT_MATERIAL_PARTITION_MISMATCH", task["task_id"])
        if sorted(binding["execution_outputs"]) != sorted(partition["admission_execution_outputs"]):
            raise ContractError("AUDIT_OUTPUT_PARTITION_MISMATCH", task["task_id"])
        if sorted(binding["allowed_writes"]) != sorted(partition["admission_allowed_writes"]):
            raise ContractError("AUDIT_ALLOWED_PARTITION_MISMATCH", task["task_id"])
        baseline_paths = sorted(item["path"] for item in binding["byte_baselines"])
        if partition["route_expected_receipt"] in baseline_paths:
            raise ContractError("ROUTE_RECEIPT_BASELINE_COLLISION", task["task_id"])
        if task["write_profile"] == "execution-output-only":
            mutated = copy.deepcopy(task)
            try:
                check_partition(mutated, injected_negative=True)
            except ContractError as error:
                if error.code != "OUTPUT_ONLY_ROUTE_RECEIPT_COLLISION":
                    raise
                negative_count += 1
            else:
                raise ContractError("NEGATIVE_FIXTURE_ACCEPTED", task["task_id"])

    if negative_count != 1:
        raise ContractError("NEGATIVE_FIXTURE_COUNT_INVALID", str(negative_count))
    print(
        json.dumps(
            {
                "code": "PARTITION_CONTRACT_PASS",
                "positive_unit_count": len(positives),
                "negative_collision_count": negative_count,
                "source_binding_count": len(SOURCE_BINDINGS),
                "units": positives,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
