#!/usr/bin/env python3
"""Prove downstream consumer closure before an epoch acceptance artifact exists.

The validator is deliberately no-authority.  It initializes Implementation
Readiness without deciding an action, binds the WPRA documents through Task
Session Until Blocker's public binder, and validates terminal/closeout shape.
It never selects a unit, admits mutation, or executes configured unit commands.

The ``guard`` operation is the only writer intended for a downstream acceptance
artifact.  It refuses presence-only, failing, stale-input, stale-consumer, or
authority-bearing closure receipts and uses exclusive creation for its output.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import runpy
import sys
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator


INPUT_NAMES = (
    "execution_contracts",
    "audit_config",
    "audit_report",
    "semantic_manifest",
    "selection_handoff",
)

REQUIRED_CHECK_IDS = (
    "no-authority-input-ceiling",
    "canonical-stop-taxonomy",
    "implementation-readiness-initialize",
    "frontier-derived-route-coverage",
    "receipt-closeout-terminal-contracts",
    "task-session-until-blocker-wpra-binding",
    "terminal-schema-and-successor-semantics",
)

CONSUMER_PATHS = {
    "implementation_readiness_initializer": (
        "arcanum/spells/implementation-readiness/scripts/readiness_execution.py"
    ),
    "implementation_readiness_contracts": (
        "arcanum/spells/implementation-readiness/scripts/execution_contracts.py"
    ),
    "implementation_readiness_runner": (
        "arcanum/spells/implementation-readiness/scripts/run_execution_loop.py"
    ),
    "implementation_readiness_policy_schema": (
        "arcanum/spells/implementation-readiness/schemas/execution-policy.schema.json"
    ),
    "task_session_until_blocker_runner": (
        "arcanum/spells/task-session-until-blocker/scripts/run_chain.py"
    ),
    "task_session_until_blocker_chain_schema": (
        "arcanum/spells/task-session-until-blocker/schemas/chain-config.schema.json"
    ),
    "wpra_audit_config_schema": (
        "arcanum/spells/work-pack-readiness-audit/schemas/audit-config-v2.schema.json"
    ),
}

RECEIPT_SCHEMA = (
    Path(__file__).resolve().parents[1]
    / "schemas"
    / "consumer-closure-receipt.schema.json"
)


class ConsumerClosureError(ValueError):
    """Stable fail-closed diagnostic for validation or guarded emission."""

    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def closure_implementation_sha256() -> dict[str, str]:
    return {
        "validator": file_sha256(Path(__file__).resolve()),
        "receipt_schema": file_sha256(RECEIPT_SCHEMA),
    }


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ConsumerClosureError("DOCUMENT_NOT_OBJECT", str(path))
    return value


def _inside(root: Path, path: Path) -> Path:
    root = root.resolve()
    path = path.resolve()
    try:
        path.relative_to(root)
    except ValueError as error:
        raise ConsumerClosureError("PATH_OUTSIDE_REPOSITORY", str(path)) from error
    if not path.is_file():
        raise ConsumerClosureError("INPUT_NOT_FILE", str(path))
    return path


def exact_ref(root: Path, path: Path) -> dict[str, Any]:
    path = _inside(root, path)
    content = path.read_bytes()
    return {
        "path": path.relative_to(root.resolve()).as_posix(),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def verify_exact_ref(root: Path, reference: dict[str, Any]) -> Path:
    if set(reference) != {"path", "sha256", "size_bytes"}:
        raise ConsumerClosureError("EXACT_REF_INVALID", repr(reference))
    path = _inside(root, root / reference["path"])
    observed = exact_ref(root, path)
    if observed != reference:
        raise ConsumerClosureError("EXACT_REF_STALE", reference["path"])
    return path


def schema_errors(document: Any, schema: dict[str, Any]) -> list[str]:
    Draft202012Validator.check_schema(schema)
    return [
        f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(document),
            key=lambda item: list(item.absolute_path),
        )
    ]


def consumer_refs(root: Path) -> dict[str, dict[str, Any]]:
    return {
        name: exact_ref(root, root / relative)
        for name, relative in sorted(CONSUMER_PATHS.items())
    }


def resolve_input_paths(
    root: Path, input_paths: dict[str, Path]
) -> dict[str, Path]:
    root = root.resolve()
    return {
        name: path if path.is_absolute() else root / path
        for name, path in input_paths.items()
    }


def _load_readiness(root: Path) -> Any:
    scripts = root / "arcanum/spells/implementation-readiness/scripts"
    path = scripts / "readiness_execution.py"
    specification = importlib.util.spec_from_file_location(
        "wpra_preacceptance_readiness_execution", path
    )
    if specification is None or specification.loader is None:
        raise ConsumerClosureError("CONSUMER_IMPORT_FAILED", str(path))
    module = importlib.util.module_from_spec(specification)
    sys.path.insert(0, str(scripts))
    try:
        specification.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


def _load_chain(root: Path) -> dict[str, Any]:
    path = root / CONSUMER_PATHS["task_session_until_blocker_runner"]
    return runpy.run_path(
        str(path), run_name="wpra_preacceptance_task_session_until_blocker"
    )


def _record(
    checks: list[dict[str, Any]],
    failures: list[dict[str, str]],
    check_id: str,
    details: dict[str, Any],
    problems: list[tuple[str, str]],
) -> None:
    ordered = sorted(problems, key=lambda item: (item[0], item[1]))
    checks.append(
        {
            "check_id": check_id,
            "status": "block" if ordered else "pass",
            "details": details,
            "failure_codes": sorted({code for code, _ in ordered}),
        }
    )
    failures.extend({"code": code, "detail": detail} for code, detail in ordered)


def _not_run(
    checks: list[dict[str, Any]], check_id: str, reason: str
) -> None:
    checks.append(
        {
            "check_id": check_id,
            "status": "not-run",
            "details": {"reason": reason},
            "failure_codes": [],
        }
    )


def _route_maps(
    manifest: dict[str, Any], frontier: list[str]
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    list[tuple[str, str]],
]:
    task_routes: dict[str, dict[str, Any]] = {}
    closeout_routes: dict[str, dict[str, Any]] = {}
    problems: list[tuple[str, str]] = []
    frontier_set = set(frontier)
    for route in manifest.get("allowed_routes", []):
        if not isinstance(route, dict):
            problems.append(("ROUTE_NOT_OBJECT", repr(route)))
            continue
        unit_id = route.get("frontier_swu")
        if unit_id not in frontier_set:
            problems.append(("ROUTE_OUTSIDE_FRONTIER", str(unit_id)))
            continue
        capability = route.get("capability")
        target = task_routes if capability == "task-session" else (
            closeout_routes if capability == "invoke" else None
        )
        if target is None:
            problems.append(("ROUTE_CAPABILITY_UNSUPPORTED", str(capability)))
        elif unit_id in target:
            problems.append(
                ("ROUTE_PER_UNIT_NON_UNIQUE", f"{capability}:{unit_id}")
            )
        else:
            target[unit_id] = route
    missing_task = sorted(frontier_set - set(task_routes))
    missing_closeout = sorted(frontier_set - set(closeout_routes))
    if missing_task:
        problems.append(
            ("TASK_ROUTE_COVERAGE_MISMATCH", ",".join(missing_task))
        )
    if missing_closeout:
        problems.append(
            ("CLOSEOUT_ROUTE_COVERAGE_MISMATCH", ",".join(missing_closeout))
        )
    return task_routes, closeout_routes, problems


def _static_contract_problems(
    contracts: dict[str, Any], frontier: list[str]
) -> list[tuple[str, str]]:
    problems: list[tuple[str, str]] = []
    units = contracts.get("units")
    if not isinstance(units, list):
        return [("UNIT_CONTRACTS_NOT_ARRAY", "units")]
    by_unit = {
        item.get("unit_id"): item for item in units if isinstance(item, dict)
    }
    if set(by_unit) != set(frontier) or len(units) != len(frontier):
        problems.append(
            (
                "UNIT_CONTRACT_COVERAGE_MISMATCH",
                f"frontier={len(frontier)},units={len(units)},unique={len(by_unit)}",
            )
        )
        return problems
    required = {
        "receipt_contract",
        "closeout_contract",
        "terminal_modes",
        "terminal_write_policy",
        "gate_contract",
        "execution_outputs",
        "allowed_writes",
    }
    missing: dict[str, list[str]] = {}
    separation: list[str] = []
    for index, unit_id in enumerate(frontier):
        unit = by_unit[unit_id]
        absent = sorted(name for name in required if name not in unit)
        if absent:
            missing[unit_id] = absent
            continue
        receipt = unit["receipt_contract"].get("path")
        closeout = unit["closeout_contract"].get("expected_owner_receipt")
        if not receipt or not closeout or receipt == closeout:
            separation.append(unit_id)
        if closeout in unit["execution_outputs"]:
            separation.append(unit_id)
        expected_successor = (
            by_unit[frontier[index + 1]].get("swu_id")
            if index + 1 < len(frontier)
            else None
        )
        if unit.get("canonical_successor") != expected_successor:
            problems.append(
                (
                    "TERMINAL_SUCCESSOR_SEMANTICS_INVALID",
                    f"{unit_id}:expected={expected_successor!r},observed={unit.get('canonical_successor')!r}",
                )
            )
    if missing:
        rendered = ";".join(
            f"{unit}:{','.join(fields)}" for unit, fields in sorted(missing.items())
        )
        problems.append(("UNIT_TERMINAL_CLOSEOUT_CONTRACT_INCOMPLETE", rendered))
    if separation:
        problems.append(
            ("RECEIPT_CLOSEOUT_SEPARATION_INVALID", ",".join(sorted(set(separation))))
        )
    return problems


def _schema_constant(schema: dict[str, Any], field: str, fallback: Any) -> Any:
    value = schema.get("properties", {}).get(field, {})
    if "const" in value:
        return value["const"]
    values = value.get("enum")
    if isinstance(values, list) and values:
        return values[0]
    return fallback


def _synthetic_terminal(
    schema: dict[str, Any],
    binding: dict[str, Any],
    successor: dict[str, Any] | None,
    normalized: dict[str, Any],
    contracts_ref: dict[str, Any],
) -> dict[str, Any]:
    by_unit = {
        item["unit_id"]: item for item in normalized["execution_bindings"]
    }
    dispositions = []
    for dependency in binding.get("dependencies", []):
        bound = by_unit[dependency]
        dispositions.append(
            {
                "dependency_id": bound["swu_id"],
                "receipt_ref": {
                    "path": bound["receipt_contract"]["path"],
                    "sha256": "0" * 64,
                    "size_bytes": 0,
                },
            }
        )
    return {
        "schema_version": _schema_constant(
            schema, "schema_version", "wpra.consumer-closure.synthetic/1.0.0"
        ),
        "receipt_id": f"consumer-closure-{binding['unit_id']}",
        "work_pack_id": _schema_constant(
            schema,
            "work_pack_id",
            binding.get("closeout_route", {}).get("target"),
        ),
        "unit_id": binding["unit_id"],
        "swu_id": binding["swu_id"],
        "task_id": binding["task_id"],
        "result": _schema_constant(schema, "result", "pass"),
        "terminal_mode": binding["terminal_modes"][0],
        "validation": {
            "status": "pass",
            "command_results": [
                {
                    "command_id": item["command_id"],
                    "status": "pass",
                    "evidence_ref": contracts_ref,
                }
                for item in binding["validation_contracts"]
            ],
        },
        "evidence_refs": [contracts_ref],
        "dependency_dispositions": dispositions,
        "blockers": [],
        "successor": {
            "unit_id": successor["swu_id"] if successor else None,
            "execution_started": False,
        },
        "authority_effect": "none",
        "mutation_ready": False,
    }


def validate_consumer_closure(
    root: Path, input_paths: dict[str, Path]
) -> dict[str, Any]:
    """Return one deterministic pass/block receipt without runtime authority."""

    root = root.resolve()
    input_paths = resolve_input_paths(root, input_paths)
    documents = {name: load_object(input_paths[name]) for name in INPUT_NAMES}
    contracts = documents["execution_contracts"]
    audit_config = documents["audit_config"]
    report = documents["audit_report"]
    manifest = documents["semantic_manifest"]
    handoff = documents["selection_handoff"]
    refs = {name: exact_ref(root, input_paths[name]) for name in INPUT_NAMES}
    consumers = consumer_refs(root)
    checks: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    metrics: dict[str, Any] = {}

    authority_problems: list[tuple[str, str]] = []
    expected_markers = (
        ("audit_report.authority_effect", report.get("authority_effect"), "none"),
        ("audit_report.selected_unit", report.get("selected_unit"), None),
        ("audit_report.mutation_ready", report.get("mutation_ready"), False),
        (
            "audit_report.configured_commands_executed",
            report.get("configured_commands_executed"),
            False,
        ),
        ("semantic_manifest.authority_effect", manifest.get("authority_effect"), "none"),
        ("semantic_manifest.selected_unit", manifest.get("selected_unit"), None),
        ("semantic_manifest.mutation_ready", manifest.get("mutation_ready"), False),
        ("selection_handoff.authority_effect", handoff.get("authority_effect"), "none"),
        ("selection_handoff.mutation_ready", handoff.get("mutation_ready"), False),
    )
    for label, observed, expected in expected_markers:
        if observed != expected:
            authority_problems.append(
                ("NO_AUTHORITY_MARKER_INVALID", f"{label}={observed!r}")
            )
    _record(
        checks,
        failures,
        "no-authority-input-ceiling",
        {"marker_count": len(expected_markers)},
        authority_problems,
    )

    policy_schema = load_object(
        root / CONSUMER_PATHS["implementation_readiness_policy_schema"]
    )
    canonical_stops = set(
        policy_schema["properties"]["stop_decisions"]["items"]["enum"]
    )
    configured_stops = audit_config.get("execution_policy", {}).get(
        "stop_decisions", []
    )
    invalid_stops = sorted(set(configured_stops) - canonical_stops)
    taxonomy_problems = [
        ("STOP_DECISION_TAXONOMY_MISMATCH", value) for value in invalid_stops
    ]
    _record(
        checks,
        failures,
        "canonical-stop-taxonomy",
        {
            "configured_count": len(configured_stops),
            "canonical_count": len(canonical_stops),
            "invalid": invalid_stops,
        },
        taxonomy_problems,
    )

    readiness_problems: list[tuple[str, str]] = []
    policy: dict[str, Any] | None = None
    state: dict[str, Any] | None = None
    try:
        readiness = _load_readiness(root)
        policy, state = readiness.initialize_from_readiness(
            audit_config,
            report,
            source_invocation_id="wpra-preacceptance-consumer-closure",
            created_at="1970-01-01T00:00:00Z",
            execution_mode="until-real-blocker",
            step_budget=len(manifest.get("ready_frontier", [])),
        )
        entry = state.get("current_entry", {})
        if entry.get("entry_state") != "selection-ready":
            readiness_problems.append(
                ("READINESS_ENTRY_NOT_SELECTION_READY", repr(entry.get("entry_state")))
            )
        if entry.get("selected_unit") is not None:
            readiness_problems.append(
                ("READINESS_INITIALIZE_SELECTED_UNIT", repr(entry["selected_unit"]))
            )
        if policy.get("authority_effect") != "none" or state.get(
            "authority_effect"
        ) != "none":
            readiness_problems.append(
                ("READINESS_INITIALIZE_AUTHORITY_EFFECT", "non-none")
            )
    except Exception as error:  # canonical consumers use typed ValueError subclasses
        readiness_problems.append(
            ("IMPLEMENTATION_READINESS_INITIALIZE_REJECTED", str(error))
        )
    _record(
        checks,
        failures,
        "implementation-readiness-initialize",
        {
            "policy_schema_version": policy.get("schema_version") if policy else None,
            "compiled_route_count": len(policy.get("allowed_routes", [])) if policy else 0,
            "compiled_stop_decision_count": len(policy.get("stop_decisions", [])) if policy else 0,
            "selected_unit": (
                state.get("current_entry", {}).get("selected_unit") if state else None
            ),
        },
        readiness_problems,
    )

    frontier = manifest.get("ready_frontier")
    if not isinstance(frontier, list):
        frontier = []
    metrics["frontier_count"] = len(frontier)
    task_routes, closeout_routes, route_problems = _route_maps(manifest, frontier)
    metrics["task_route_count"] = len(task_routes)
    metrics["closeout_route_count"] = len(closeout_routes)
    _record(
        checks,
        failures,
        "frontier-derived-route-coverage",
        {
            "frontier_count": len(frontier),
            "task_route_count": len(task_routes),
            "closeout_route_count": len(closeout_routes),
        },
        route_problems,
    )

    static_problems = _static_contract_problems(contracts, frontier)
    _record(
        checks,
        failures,
        "receipt-closeout-terminal-contracts",
        {"unit_count": len(contracts.get("units", []))},
        static_problems,
    )

    chain = _load_chain(root)
    normalized: dict[str, Any] | None = None
    chain_problems: list[tuple[str, str]] = []
    chain_config = {
        "audit_verdict": report.get("verdict"),
        "audit_flags": report.get("flags", []),
        "approved_epoch": {
            "audit_projection_digest": report.get("audit_projection_digest"),
            "canonical_semantic_digest": report.get("canonical_semantic_digest"),
            "source_snapshot_digest": report.get("source_snapshot", {}).get("digest"),
        },
        "wpra_v2": {"execution_contracts_ref": refs["execution_contracts"]},
    }
    try:
        normalized = chain["normalize_plan_semantic_manifest"](
            manifest,
            chain_config,
            report,
            {
                "audit_config": audit_config,
                "execution_contracts": contracts,
                "selection_handoff": handoff,
            },
        )
        if normalized.get("wpra_v2_bound") is not True:
            chain_problems.append(("CHAIN_WPRA_BINDING_ABSENT", "wpra_v2_bound"))
        if len(normalized.get("execution_bindings", [])) != len(frontier):
            chain_problems.append(
                (
                    "CHAIN_UNIT_COVERAGE_MISMATCH",
                    f"frontier={len(frontier)},bound={len(normalized.get('execution_bindings', []))}",
                )
            )
    except Exception as error:
        chain_problems.append(("TASK_SESSION_CHAIN_BIND_REJECTED", str(error)))
    _record(
        checks,
        failures,
        "task-session-until-blocker-wpra-binding",
        {
            "wpra_v2_bound": bool(normalized and normalized.get("wpra_v2_bound")),
            "normalized_unit_count": (
                len(normalized.get("execution_bindings", [])) if normalized else 0
            ),
        },
        chain_problems,
    )

    if normalized is None or normalized.get("wpra_v2_bound") is not True:
        _not_run(
            checks,
            "terminal-schema-and-successor-semantics",
            "current WPRA v2 chain binding blocked",
        )
    else:
        terminal_problems: list[tuple[str, str]] = []
        try:
            schema_binding = audit_config["receipt_bindings"]["terminal_schema_ref"]
            schema_ref = schema_binding["artifact_ref"]
            schema_path = verify_exact_ref(root, schema_ref)
            terminal_schema = load_object(schema_path)
            bindings = normalized["execution_bindings"]
            probes = [
                ("nonterminal", bindings[0], bindings[1] if len(bindings) > 1 else None),
                ("terminal", bindings[-1], None),
            ]
            terminal_receipt_errors: Callable[..., list[str]] = chain[
                "terminal_receipt_errors"
            ]
            for label, current, successor in probes:
                synthetic = _synthetic_terminal(
                    terminal_schema, current, successor, normalized, refs["execution_contracts"]
                )
                for error in schema_errors(synthetic, terminal_schema):
                    terminal_problems.append(
                        ("TERMINAL_SCHEMA_REJECTED", f"{label}:{error}")
                    )
                if label == "terminal" and current.get("dependencies"):
                    # Future dependency receipts do not exist before acceptance.
                    # Replace only exact-byte resolution; the canonical function
                    # still checks their IDs, paths, shape, and successor semantics.
                    globals_ = terminal_receipt_errors.__globals__
                    original = globals_["verify_exact_ref"]
                    globals_["verify_exact_ref"] = lambda _root, ref: _root / ref["path"]
                    try:
                        semantic = terminal_receipt_errors(
                            root,
                            synthetic,
                            refs["execution_contracts"],
                            current,
                            successor,
                            normalized,
                        )
                    finally:
                        globals_["verify_exact_ref"] = original
                else:
                    semantic = terminal_receipt_errors(
                        root,
                        synthetic,
                        refs["execution_contracts"],
                        current,
                        successor,
                        normalized,
                    )
                for error in semantic:
                    terminal_problems.append(
                        ("TERMINAL_SUCCESSOR_SEMANTICS_INVALID", f"{label}:{error}")
                    )
        except Exception as error:
            terminal_problems.append(("TERMINAL_CONSUMER_PROBE_FAILED", str(error)))
        _record(
            checks,
            failures,
            "terminal-schema-and-successor-semantics",
            {
                "probe_classes": ["nonterminal", "terminal"],
                "future_dependency_byte_resolution": "shape-only",
            },
            terminal_problems,
        )

    failures = sorted(failures, key=lambda item: (item["code"], item["detail"]))
    payload = {
        "schema_version": "arcanum.wpra.consumer-closure-receipt/1.0.0",
        "status": "block" if failures else "pass",
        "check_results": checks,
        "failures": failures,
        "metrics": metrics,
        "exact_inputs": refs,
        "canonical_consumers": consumers,
        "closure_implementation_sha256": closure_implementation_sha256(),
        "authority_effect": "none",
        "selection_performed": False,
        "mutation_performed": False,
        "configured_unit_commands_executed": False,
        "claim_ceiling": (
            "Exact-byte downstream contract compatibility only; no approval, "
            "selection, admission, mutation, configured unit command execution, "
            "promotion, publication, deployment, release, or production proof."
        ),
    }
    receipt = {**payload, "receipt_digest": canonical_digest(payload)}
    errors = schema_errors(receipt, load_object(RECEIPT_SCHEMA))
    if errors:
        raise ConsumerClosureError("RECEIPT_SCHEMA_INVALID", "; ".join(errors))
    return receipt


def write_receipt(receipt: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as handle:
        json.dump(receipt, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def require_passing_receipt(
    root: Path, receipt_path: Path, input_paths: dict[str, Path]
) -> dict[str, Any]:
    """Revalidate a closure receipt immediately before acceptance emission."""

    root = root.resolve()
    input_paths = resolve_input_paths(root, input_paths)
    receipt = load_object(receipt_path)
    errors = schema_errors(receipt, load_object(RECEIPT_SCHEMA))
    if errors:
        raise ConsumerClosureError("CLOSURE_RECEIPT_SCHEMA_INVALID", "; ".join(errors))
    payload = {key: value for key, value in receipt.items() if key != "receipt_digest"}
    if receipt["receipt_digest"] != canonical_digest(payload):
        raise ConsumerClosureError("CLOSURE_RECEIPT_DIGEST_STALE", str(receipt_path))
    if receipt["status"] != "pass" or receipt["failures"]:
        raise ConsumerClosureError("CLOSURE_RECEIPT_NOT_PASSING", receipt["status"])
    checks = receipt.get("check_results", [])
    observed_check_ids = [item.get("check_id") for item in checks]
    if (
        len(checks) != len(REQUIRED_CHECK_IDS)
        or set(observed_check_ids) != set(REQUIRED_CHECK_IDS)
        or len(observed_check_ids) != len(set(observed_check_ids))
    ):
        raise ConsumerClosureError(
            "CLOSURE_RECEIPT_CHECK_COVERAGE_INVALID",
            ",".join(str(item) for item in observed_check_ids),
        )
    nonpassing = sorted(
        item["check_id"] for item in checks if item.get("status") != "pass"
    )
    if nonpassing:
        raise ConsumerClosureError(
            "CLOSURE_RECEIPT_CHECK_NOT_PASSING", ",".join(nonpassing)
        )
    failure_bearing = sorted(
        item["check_id"] for item in checks if item.get("failure_codes")
    )
    if failure_bearing:
        raise ConsumerClosureError(
            "CLOSURE_RECEIPT_CHECK_FAILURE_CODES_PRESENT",
            ",".join(failure_bearing),
        )
    expected_ceiling = {
        "authority_effect": "none",
        "selection_performed": False,
        "mutation_performed": False,
        "configured_unit_commands_executed": False,
    }
    for field, expected in expected_ceiling.items():
        if receipt.get(field) != expected:
            raise ConsumerClosureError(
                "CLOSURE_RECEIPT_AUTHORITY_INVALID", f"{field}={receipt.get(field)!r}"
            )
    expected_inputs = {
        name: exact_ref(root, input_paths[name]) for name in INPUT_NAMES
    }
    if receipt["exact_inputs"] != expected_inputs:
        raise ConsumerClosureError("CLOSURE_RECEIPT_INPUT_STALE", "exact_inputs")
    if receipt["canonical_consumers"] != consumer_refs(root):
        raise ConsumerClosureError(
            "CLOSURE_RECEIPT_CONSUMER_STALE", "canonical_consumers"
        )
    if receipt["closure_implementation_sha256"] != closure_implementation_sha256():
        raise ConsumerClosureError(
            "CLOSURE_RECEIPT_VALIDATOR_STALE", "closure_implementation_sha256"
        )
    return receipt


def guarded_draft_binding(
    root: Path, receipt_path: Path, input_paths: dict[str, Path]
) -> dict[str, Any]:
    """Return the closed identity tuple every guarded draft must carry."""

    root = root.resolve()
    input_paths = resolve_input_paths(root, input_paths)
    receipt_path = receipt_path if receipt_path.is_absolute() else root / receipt_path
    audit_config = load_object(input_paths["audit_config"])
    report = load_object(input_paths["audit_report"])
    manifest = load_object(input_paths["semantic_manifest"])
    work_pack_id = manifest.get("work_pack_id")
    if audit_config.get("execution_policy", {}).get("work_pack_id") != work_pack_id:
        raise ConsumerClosureError(
            "GUARDED_DRAFT_SOURCE_TUPLE_INVALID", "work_pack_id"
        )
    return {
        "work_pack_id": work_pack_id,
        "plan_epoch_id": manifest.get("plan_epoch_id"),
        "manifest_id": manifest.get("manifest_id"),
        "audit_id": report.get("audit_id"),
        "audit_verdict": report.get("verdict"),
        "terminal_code": report.get("terminal_code"),
        "consumer_closure_receipt_ref": exact_ref(root, receipt_path),
    }


def write_guarded_artifact(
    root: Path,
    receipt_path: Path,
    input_paths: dict[str, Path],
    draft_path: Path,
    output_path: Path,
) -> None:
    """Copy one JSON draft only after closure passes, using exclusive create."""

    root = root.resolve()
    input_paths = resolve_input_paths(root, input_paths)
    receipt_path = receipt_path if receipt_path.is_absolute() else root / receipt_path
    require_passing_receipt(root, receipt_path, input_paths)
    draft = load_object(draft_path)
    expected_binding = guarded_draft_binding(root, receipt_path, input_paths)
    missing = sorted(name for name in expected_binding if name not in draft)
    if missing:
        raise ConsumerClosureError(
            "GUARDED_DRAFT_BINDING_MISSING", ",".join(missing)
        )
    stale = sorted(
        name for name, expected in expected_binding.items() if draft.get(name) != expected
    )
    if stale:
        raise ConsumerClosureError(
            "GUARDED_DRAFT_BINDING_STALE", ",".join(stale)
        )
    rendered = draft_path.read_bytes()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("xb") as handle:
        handle.write(rendered)


def _input_paths(args: argparse.Namespace) -> dict[str, Path]:
    return {name: getattr(args, name.replace("-", "_")) for name in INPUT_NAMES}


def _add_inputs(parser: argparse.ArgumentParser) -> None:
    for name in INPUT_NAMES:
        parser.add_argument(f"--{name.replace('_', '-')}", required=True, type=Path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="operation", required=True)

    validate = subparsers.add_parser("validate")
    validate.add_argument("--repository-root", type=Path, default=Path("."))
    _add_inputs(validate)
    validate.add_argument("--output", required=True, type=Path)

    guard = subparsers.add_parser("guard")
    guard.add_argument("--repository-root", type=Path, default=Path("."))
    _add_inputs(guard)
    guard.add_argument("--receipt", required=True, type=Path)
    guard.add_argument("--draft", required=True, type=Path)
    guard.add_argument("--output", required=True, type=Path)

    args = parser.parse_args()
    try:
        if args.operation == "validate":
            receipt = validate_consumer_closure(
                args.repository_root, _input_paths(args)
            )
            write_receipt(receipt, args.output)
            print(
                json.dumps(
                    {
                        "status": receipt["status"],
                        "failure_codes": sorted(
                            {item["code"] for item in receipt["failures"]}
                        ),
                        "authority_effect": "none",
                        "selection_performed": False,
                        "mutation_performed": False,
                        "configured_unit_commands_executed": False,
                        "output": str(args.output),
                    },
                    sort_keys=True,
                )
            )
            return 0 if receipt["status"] == "pass" else 2
        write_guarded_artifact(
            args.repository_root,
            args.receipt,
            _input_paths(args),
            args.draft,
            args.output,
        )
        print(
            json.dumps(
                {
                    "status": "pass",
                    "guarded_output": str(args.output),
                    "authority_effect": "none",
                },
                sort_keys=True,
            )
        )
        return 0
    except (ConsumerClosureError, OSError, ValueError, KeyError, TypeError) as error:
        code = getattr(error, "code", "CONSUMER_CLOSURE_ERROR")
        print(
            json.dumps(
                {"status": "block", "code": code, "detail": str(error)},
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
