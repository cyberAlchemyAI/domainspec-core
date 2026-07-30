#!/usr/bin/env python3
"""Materialize the exact Invoke Refresh target inventory into staging."""

from __future__ import annotations

import hashlib
import json
import textwrap
from collections import defaultdict
from pathlib import Path
from typing import Any


REFRESH_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = REFRESH_ROOT.parents[6]
RUN_ROOT = Path(
    "projects/body-war/development/invoke-runs/"
    "20260730T050022Z-ontology-focus-scene-pivot"
)
STAGING_ROOT = REFRESH_ROOT / "material/staged"
WORKBENCH = "cyberAlchemy-v2/implementation/ontology-evidence-workbench"

TARGETS = [
    RUN_ROOT / "WORK-PACK.md",
    RUN_ROOT / "TASK-SESSION-RECEIPT.schema.json",
    RUN_ROOT / "work-pack/shared/CONTEXT.md",
    RUN_ROOT / "work-pack/shared/CLOSEOUT-CONTRACT.md",
    RUN_ROOT / "work-pack/shared/COMMAND-MATRIX.json",
    RUN_ROOT / "work-pack/shared/validate-task-session-receipt.py",
    RUN_ROOT / "work-pack/shared/test-task-session-receipt.py",
    RUN_ROOT / "work-pack/tasks/TASK-CLOSURE.md",
    RUN_ROOT / "work-pack/tasks/TASK-FOUNDATION.md",
    RUN_ROOT / "work-pack/tasks/TASK-PACKAGE.md",
]


def read(path: Path) -> str:
    return (REPOSITORY_ROOT / path).read_text(encoding="utf-8")


def replace_once(value: str, old: str, new: str, label: str) -> str:
    count = value.count(old)
    if count != 1:
        raise ValueError(f"{label}: expected one match, found {count}")
    return value.replace(old, new)


def stage(path: Path, content: str) -> None:
    target = STAGING_ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def exact_ref(path: Path) -> dict[str, Any]:
    content = (REPOSITORY_ROOT / path).read_bytes()
    return {
        "path": path.as_posix(),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def command(
    argv: list[str],
    *,
    cwd: str = WORKBENCH,
    risk: str = "read-only",
    timeout: int = 300,
) -> dict[str, Any]:
    return {
        "cwd": cwd,
        "argv": argv,
        "expected_exit_code": 0,
        "timeout_seconds": timeout,
        "environment": {},
        "runtime_identity": {
            "executable": argv[0],
            "version_policy": (
                "exact Node v22.12.0 or Python 3 runtime captured at "
                "Task Session preflight"
            ),
            "hash_policy": (
                "resolve executable and bind SHA-256 in the terminal receipt"
            ),
        },
        "risk_class": risk,
    }


def attempt(
    unit_id: str, required: bool, *, browser: bool = False
) -> dict[str, Any]:
    if not required:
        return {
            "required": False,
            "id_algorithm": "",
            "collision_policy": "fail-if-exists",
            "retention_policy": "retain-receipt-only",
            "teardown_on_success": [],
            "teardown_on_failure": [],
        }
    script = (
        "scripts/validate-body-war-focus-scene.mjs"
        if browser
        else "scripts/materialize-focus-scene-build.mjs"
    )
    action = "teardown" if browser else "cleanup"
    teardown = command(
        [
            "node",
            script,
            action,
            "--attempt-dir",
            f"generated/runs/{unit_id}/{{attempt_id}}",
            "--verify-clean",
        ],
        risk="bounded-write",
    )
    return {
        "required": True,
        "id_algorithm": (
            "UTC YYYYMMDDTHHMMSSZ + '-' + first12(sha256(unit_id + "
            "canonical input-lock digests)); fail if directory exists"
        ),
        "collision_policy": "fail-if-exists",
        "retention_policy": "retain-all",
        "teardown_on_success": [teardown],
        "teardown_on_failure": [teardown],
    }


def unit_commands(unit_id: str) -> list[dict[str, Any]]:
    number = unit_id.rsplit("-", 1)[-1] if unit_id.startswith("SWU-") else ""
    simple_tests = {
        "001": "test/focus-scene-fixture.test.mjs",
        "002": "test/focus-scene-overlay.test.mjs",
        "003": "test/focus-scene-materializer.test.mjs",
        "004": "test/focus-scene-build-verifier.test.mjs",
        "015": "test/body-war-focus-scene-browser.test.mjs",
    }
    if number in simple_tests:
        return [command(["node", "--test", simple_tests[number]])]
    if number in {
        "005",
        "006",
        "007",
        "008",
        "009",
        "010",
        "011",
        "012",
        "013",
        "017",
        "018",
        "019",
        "020",
        "021",
        "024",
        "025",
    }:
        return [
            command(
                [
                    "node",
                    "scripts/materialize-focus-scene-build.mjs",
                    "validate-unit",
                    "--lock",
                    "upstream/FOCUS-SCENE-BUILD.lock.json",
                    "--unit",
                    unit_id,
                ],
                risk="bounded-write",
                timeout=900,
            )
        ]
    if number in {"014", "022"}:
        layer = "L0" if number == "014" else "L1"
        attempt_dir = f"generated/runs/{unit_id}/{{attempt_id}}"
        return [
            command(
                [
                    "node",
                    "scripts/materialize-focus-scene-build.mjs",
                    "build",
                    "--lock",
                    "upstream/FOCUS-SCENE-BUILD.lock.json",
                    "--layer",
                    layer,
                    "--attempt-dir",
                    attempt_dir,
                ],
                risk="bounded-write",
                timeout=1800,
            ),
            command(
                [
                    "node",
                    "scripts/verify-focus-scene-build.mjs",
                    "verify",
                    "--lock",
                    "upstream/FOCUS-SCENE-BUILD.lock.json",
                    "--handle",
                    f"{attempt_dir}/build-handle.json",
                    "--output",
                    f"{attempt_dir}/build-verification.json",
                ],
                risk="bounded-write",
            ),
        ]
    if number in {"016", "023"}:
        layer = "L0" if number == "016" else "L1"
        attempt_dir = f"generated/runs/{unit_id}/{{attempt_id}}"
        return [
            command(
                [
                    "node",
                    "scripts/validate-body-war-focus-scene.mjs",
                    "run",
                    "--layer",
                    layer,
                    "--build-handle",
                    (
                        f"generated/runs/SWU-OFSP-"
                        f"{'014' if number == '016' else '022'}/"
                        "{dependency_attempt_id}/build-handle.json"
                    ),
                    "--graph",
                    "generated/runs/BODY-WAR-ONTOLOGY-001/presentation-graph.json",
                    "--attempt-dir",
                    attempt_dir,
                ],
                risk="browser",
                timeout=900,
            ),
            command(
                [
                    "node",
                    "scripts/validate-body-war-focus-scene.mjs",
                    "verify",
                    "--receipt",
                    f"{attempt_dir}/browser-receipt.json",
                ]
            ),
        ]
    if number == "026":
        attempt_dir = f"generated/runs/{unit_id}/{{attempt_id}}"
        return [
            command(
                [
                    "node",
                    "scripts/materialize-focus-scene-build.mjs",
                    "reproduce",
                    "--manifest",
                    "contracts/focus-scene-prototype-manifest.json",
                    "--attempt-dir",
                    attempt_dir,
                ],
                risk="bounded-write",
                timeout=1800,
            )
        ]
    if unit_id.startswith("TASK-"):
        return [
            command(
                [
                    "python3",
                    "work-pack/shared/validate-task-session-receipt.py",
                    "--closure-task",
                    unit_id,
                    "--output",
                    f"work-pack/closeout/{unit_id}.receipt.json",
                ],
                cwd=RUN_ROOT.as_posix(),
                risk="bounded-write",
            )
        ]
    raise ValueError(f"missing command contract: {unit_id}")


def load_pre_units() -> list[dict[str, Any]]:
    path = (
        REPOSITORY_ROOT
        / RUN_ROOT
        / "readiness-runs/pre-refresh/AUDIT-CONFIG.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))["units"]


def command_matrix() -> dict[str, Any]:
    units = load_pre_units()
    order = [unit["unit_id"] for unit in units]
    run_prefix = RUN_ROOT.as_posix() + "/"
    for unit in units:
        unit_id = unit["unit_id"]
        if unit_id.startswith("TASK-"):
            receipt = run_prefix + f"work-pack/closeout/{unit_id}.receipt.json"
            unit["execution_outputs"] = [receipt]
            unit["allowed_writes"] = [receipt]
        if unit_id == "SWU-OFSP-026":
            fixed = []
            for path in unit["execution_outputs"]:
                path = path.replace("/<attempt>/{attempt_id}", "/{attempt_id}")
                fixed.append(path)
            unit["execution_outputs"] = fixed
            unit["allowed_writes"] = unit["material_writes"] + fixed
        unit["validation_commands"] = unit_commands(unit_id)
        browser = unit_id in {"SWU-OFSP-016", "SWU-OFSP-023"}
        unit["attempt"] = attempt(
            unit_id, bool(unit["execution_outputs"]) and not unit_id.startswith("TASK-"),
            browser=browser,
        )
        unit.pop("contract_ref", None)
        unit.pop("contract_kind", None)
        unit.pop("dependency_receipts", None)
        unit.pop("material_package", None)

    writers: dict[str, list[str]] = defaultdict(list)
    for unit in units:
        for path in unit["allowed_writes"]:
            writers[path].append(unit["unit_id"])
    shared = []
    for path, participants in sorted(writers.items()):
        unique = [unit for unit in order if unit in set(participants)]
        if len(unique) > 1:
            shared.append(
                {
                    "path": path,
                    "owner": "ontology-evidence-workbench successor-overlay lifecycle",
                    "ordered_units": unique,
                }
            )
    return {
        "schema_version": "1.0.0",
        "work_pack_id": "body-war-ontology-focus-scene-pivot-20260730",
        "claim_ceiling": "plan contracts only; no command executed by this matrix",
        "runtime_contract": {
            "node": "v22.12.0",
            "pnpm": "10.6.2 via existing L1 toolchain lock and materializer",
            "playwright": "1.59.1 global shared runtime",
            "chromium_revision": "1217",
        },
        "units": units,
        "shared_write_owners": shared,
    }


def hardened_receipt_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "body-war.invoke.task-session-terminal-receipt.v2",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version",
            "run_id",
            "session_id",
            "dispatch_id",
            "step_id",
            "capability_ref",
            "terminal_receipt_kind",
            "status",
            "unit_id",
            "work_pack_sha256",
            "successor",
            "execution_class",
            "files_touched",
            "artifacts",
            "validation",
            "validation_result",
            "blockers",
            "residue",
            "attempt_id",
            "teardown_result",
            "expected_closeout_receipt",
            "authority_effect",
            "claim_ceiling",
            "handoff_note",
        ],
        "properties": {
            "schema_version": {
                "const": "body-war.invoke.task-session-terminal-receipt.v2"
            },
            "run_id": {"type": "string", "minLength": 1},
            "session_id": {"type": "string", "minLength": 1},
            "dispatch_id": {
                "const": "body-war-ontology-focus-scene-pivot-20260730"
            },
            "step_id": {"enum": ["s1", "s2", "s3", "s4", "s5", "s6"]},
            "capability_ref": {"const": "task-session"},
            "terminal_receipt_kind": {"const": "task-session-terminal"},
            "status": {"enum": ["pass", "flag", "block", "interrupted"]},
            "unit_id": {
                "type": "string",
                "pattern": (
                    "^(SWU-OFSP-[0-9]{3}|TASK-VERIFY|"
                    "TASK-AUDIT-ALIGNMENT|TASK-AUDIT-LAYERING)$"
                ),
            },
            "work_pack_sha256": {
                "type": "string",
                "pattern": "^[a-f0-9]{64}$",
            },
            "successor": {"type": ["string", "null"], "minLength": 1},
            "execution_class": {
                "enum": [
                    "material-mutation",
                    "output-only",
                    "audit-only",
                    "read-only-validation",
                ]
            },
            "files_touched": {
                "type": "array",
                "uniqueItems": True,
                "items": {"type": "string", "minLength": 1},
            },
            "artifacts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["path", "sha256", "size_bytes"],
                    "properties": {
                        "path": {"type": "string", "minLength": 1},
                        "sha256": {
                            "type": "string",
                            "pattern": "^[a-f0-9]{64}$",
                        },
                        "size_bytes": {"type": "integer", "minimum": 0},
                    },
                },
            },
            "validation": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["cwd", "argv", "exit_code"],
                    "properties": {
                        "cwd": {"type": "string", "minLength": 1},
                        "argv": {
                            "type": "array",
                            "minItems": 1,
                            "items": {"type": "string", "minLength": 1},
                        },
                        "exit_code": {"type": "integer"},
                    },
                },
            },
            "validation_result": {
                "enum": ["pass", "flag", "block", "not-run"]
            },
            "blockers": {
                "type": "array",
                "items": {"type": "string", "minLength": 1},
            },
            "residue": {
                "type": "array",
                "items": {"type": "string", "minLength": 1},
            },
            "attempt_id": {"type": ["string", "null"], "minLength": 1},
            "teardown_result": {"enum": ["pass", "block", "not-applicable"]},
            "expected_closeout_receipt": {
                "type": "string",
                "minLength": 1,
            },
            "authority_effect": {"const": "none"},
            "claim_ceiling": {"type": "string", "minLength": 1},
            "handoff_note": {"type": "string", "minLength": 1},
        },
        "allOf": [
            {
                "if": {
                    "properties": {"status": {"const": "pass"}},
                    "required": ["status"],
                },
                "then": {
                    "properties": {
                        "validation_result": {"const": "pass"},
                        "blockers": {"maxItems": 0},
                        "artifacts": {"minItems": 1},
                        "validation": {"minItems": 1},
                        "teardown_result": {
                            "enum": ["pass", "not-applicable"]
                        },
                    }
                },
            },
            {
                "if": {
                    "properties": {"status": {"const": "block"}},
                    "required": ["status"],
                },
                "then": {
                    "properties": {
                        "validation_result": {"enum": ["block", "not-run"]},
                        "blockers": {"minItems": 1},
                    }
                },
            },
            {
                "if": {
                    "properties": {"status": {"const": "interrupted"}},
                    "required": ["status"],
                },
                "then": {
                    "properties": {
                        "validation_result": {"const": "not-run"},
                        "blockers": {"minItems": 1},
                    }
                },
            },
        ],
    }


def closure_contract() -> str:
    return textwrap.dedent(
        """\
        # TASK-CLOSURE — Terminal Verification And Audit Receipts

        These are output-only/audit-only contracts. They do not repair source
        findings and must never declare placeholder material writes.

        ## TASK-VERIFY

        - Primary behavior: verify every required SWU terminal receipt, digest,
          command result, artifact, teardown result, and successor boundary.
        - Dependencies: `SWU-OFSP-025`.
        - Material writes: none.
        - Execution output:
          `work-pack/closeout/TASK-VERIFY.receipt.json`.
        - Validation argv: see
          `../shared/COMMAND-MATRIX.json#TASK-VERIFY`.
        - Acceptance: output validates against the terminal schema and semantic
          validator; findings block and are never repaired here.
        - Successor: `TASK-AUDIT-ALIGNMENT`.

        ## TASK-AUDIT-ALIGNMENT

        - Primary behavior: audit exact spec/design/work-pack/terminal-evidence
          alignment without changing any source.
        - Dependencies: `TASK-VERIFY`.
        - Material writes: none.
        - Execution output:
          `work-pack/closeout/TASK-AUDIT-ALIGNMENT.receipt.json`.
        - Validation argv: see
          `../shared/COMMAND-MATRIX.json#TASK-AUDIT-ALIGNMENT`.
        - Acceptance: every claim maps to exact current evidence; ambiguity
          blocks and no plan or implementation file is repaired.
        - Successor: `TASK-AUDIT-LAYERING`.

        ## TASK-AUDIT-LAYERING

        - Primary behavior: audit owner, layer, authority, publication, and
          candidate-local claim ceilings without changing any source.
        - Dependencies: `TASK-AUDIT-ALIGNMENT`.
        - Material writes: none.
        - Execution output:
          `work-pack/closeout/TASK-AUDIT-LAYERING.receipt.json`.
        - Validation argv: see
          `../shared/COMMAND-MATRIX.json#TASK-AUDIT-LAYERING`.
        - Acceptance: every boundary passes; findings block and remain owned by
          their lifecycle owner.
        - Successor: `SWU-OFSP-026`.

        ## Runtime Admission Gap

        The live Task Session `routed-mutation` request requires at least one
        material write. These tasks truthfully have none. They remain
        runtime-blocked until the Task Session lifecycle owner admits a bounded
        output-only/audit-only mode. This plan does not fabricate a material
        path to bypass that gate.
        """
    )


def semantic_validator() -> str:
    return textwrap.dedent(
        '''\
        #!/usr/bin/env python3
        """Validate Body War OFSP terminal receipt semantics against an audit config."""

        from __future__ import annotations

        import argparse
        import json
        from pathlib import Path
        from typing import Any

        from jsonschema import Draft202012Validator


        def load(path: Path) -> dict[str, Any]:
            value = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(value, dict):
                raise ValueError(f"JSON object required: {path}")
            return value


        def validate(receipt: dict[str, Any], config: dict[str, Any], schema: dict[str, Any]) -> list[str]:
            errors = [
                f"schema:{'/'.join(map(str, error.absolute_path)) or '<root>'}:{error.message}"
                for error in Draft202012Validator(schema).iter_errors(receipt)
            ]
            by_id = {unit["unit_id"]: unit for unit in config["units"]}
            unit = by_id.get(receipt.get("unit_id"))
            if unit is None:
                errors.append("unit is outside captured audit frontier")
                return sorted(errors)
            expected = {
                "step_id": unit["dispatch_step"],
                "work_pack_sha256": config["work_pack"]["sha256"],
                "successor": unit["successor"],
                "execution_class": unit["task_class"],
                "expected_closeout_receipt": unit["closeout_receipt"],
            }
            for key, value in expected.items():
                if receipt.get(key) != value:
                    errors.append(f"{key} mismatch")
            touched = set(receipt.get("files_touched", []))
            allowed = set(unit["allowed_writes"])
            if not touched <= allowed:
                errors.append("files_touched escapes allowed writes")
            artifact_paths = {
                item.get("path")
                for item in receipt.get("artifacts", [])
                if isinstance(item, dict)
            }
            if not artifact_paths <= allowed:
                errors.append("artifact path escapes allowed writes")
            required_attempt = unit["attempt"]["required"]
            if required_attempt and not receipt.get("attempt_id"):
                errors.append("attempt_id required for attempt-producing unit")
            if not required_attempt and receipt.get("attempt_id") is not None:
                errors.append("attempt_id forbidden for non-attempt unit")
            if receipt.get("status") == "pass" and receipt.get("teardown_result") == "block":
                errors.append("pass receipt cannot carry blocked teardown")
            return sorted(set(errors))


        def main() -> int:
            parser = argparse.ArgumentParser()
            parser.add_argument("--receipt", type=Path)
            parser.add_argument("--audit-config", type=Path)
            parser.add_argument("--schema", type=Path)
            parser.add_argument("--closure-task")
            parser.add_argument("--output", type=Path)
            args = parser.parse_args()
            if args.closure_task:
                raise SystemExit(
                    "closure execution is not implemented by the semantic validator; "
                    "Task Session output-only admission remains blocked"
                )
            if not (args.receipt and args.audit_config and args.schema):
                raise SystemExit("--receipt, --audit-config, and --schema are required")
            errors = validate(load(args.receipt), load(args.audit_config), load(args.schema))
            result = {"verdict": "pass" if not errors else "block", "errors": errors}
            if args.output:
                args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\\n")
            else:
                print(json.dumps(result, indent=2, sort_keys=True))
            return 0 if not errors else 1


        if __name__ == "__main__":
            raise SystemExit(main())
        '''
    )


def semantic_tests() -> str:
    return textwrap.dedent(
        '''\
        #!/usr/bin/env python3
        """Adversarial tests for the OFSP terminal receipt schema."""

        from __future__ import annotations

        import copy
        import importlib.util
        import json
        import unittest
        from pathlib import Path

        from jsonschema import Draft202012Validator


        ROOT = Path(__file__).resolve().parent
        SCHEMA = json.loads((ROOT.parent.parent / "TASK-SESSION-RECEIPT.schema.json").read_text())
        SPEC = importlib.util.spec_from_file_location("semantic", ROOT / "validate-task-session-receipt.py")
        assert SPEC and SPEC.loader
        SEMANTIC = importlib.util.module_from_spec(SPEC)
        SPEC.loader.exec_module(SEMANTIC)


        def base() -> dict:
            return {
                "schema_version": "body-war.invoke.task-session-terminal-receipt.v2",
                "run_id": "run",
                "session_id": "session",
                "dispatch_id": "body-war-ontology-focus-scene-pivot-20260730",
                "step_id": "s1",
                "capability_ref": "task-session",
                "terminal_receipt_kind": "task-session-terminal",
                "status": "pass",
                "unit_id": "SWU-OFSP-001",
                "work_pack_sha256": "a" * 64,
                "successor": "SWU-OFSP-002",
                "execution_class": "material-mutation",
                "files_touched": ["target"],
                "artifacts": [{"path": "target", "sha256": "b" * 64, "size_bytes": 1}],
                "validation": [{"cwd": ".", "argv": ["node", "--test"], "exit_code": 0}],
                "validation_result": "pass",
                "blockers": [],
                "residue": [],
                "attempt_id": None,
                "teardown_result": "not-applicable",
                "expected_closeout_receipt": "closeout.json",
                "authority_effect": "none",
                "claim_ceiling": "bounded",
                "handoff_note": "next",
            }


        class ReceiptAdversaries(unittest.TestCase):
            def reject(self, mutate) -> None:
                value = base()
                mutate(value)
                self.assertTrue(list(Draft202012Validator(SCHEMA).iter_errors(value)))

            def test_pass_not_run(self): self.reject(lambda x: x.update(validation_result="not-run"))
            def test_pass_with_blocker(self): self.reject(lambda x: x["blockers"].append("x"))
            def test_pass_without_artifacts(self): self.reject(lambda x: x.update(artifacts=[]))
            def test_pass_without_validation(self): self.reject(lambda x: x.update(validation=[]))
            def test_block_with_pass_validation(self):
                self.reject(lambda x: x.update(status="block", blockers=["x"], validation_result="pass"))
            def test_numeric_hash(self): self.reject(lambda x: x["artifacts"][0].update(sha256=7))
            def test_nested_extra_field(self): self.reject(lambda x: x["artifacts"][0].update(extra=True))
            def test_numeric_unit_id(self): self.reject(lambda x: x.update(unit_id=1))


        if __name__ == "__main__":
            unittest.main()
        '''
    )


def patch_existing_targets(matrix: dict[str, Any]) -> None:
    work_pack = read(RUN_ROOT / "WORK-PACK.md")
    work_pack = replace_once(
        work_pack, "status: pass-for-explicit-selection", "status: blocked-runtime-admission", "work pack frontmatter"
    )
    work_pack = replace_once(
        work_pack, "| `workPackGateStatus` | `pass` |", "| `workPackGateStatus` | `block-runtime-admission` |", "gate table"
    )
    work_pack = replace_once(
        work_pack, "| `closeoutSyncStatus` | `pass` |", "| `closeoutSyncStatus` | `pass-plan-contract` |", "closeout table"
    )
    work_pack = replace_once(
        work_pack,
        "| `first_selectable_swu` | `SWU-OFSP-001` |",
        "| `first_selectable_swu` | `none` |\n| `first_planned_swu` | `SWU-OFSP-001` |",
        "first selectable",
    )
    work_pack = replace_once(
        work_pack,
        "`workPackGateStatus: pass` means the plan is authored and internally complete.\nDistill recheck passed. No SWU may execute until the user explicitly selects\none unit.",
        "`workPackGateStatus: block-runtime-admission` means the refreshed plan\ncontract is complete, but no SWU may be selected or executed. Material SWUs\nlack current material-package admission, and output-only/audit-only units have\nno truthful live Task Session mutation mode.",
        "gate explanation",
    )
    work_pack = replace_once(
        work_pack,
        "Task-shaped count after repair: `0 of 26`.",
        "Atomicity-only result: `0 of 26` task-shaped. This does not imply\ncommand, receipt, closeout, or runtime readiness.",
        "atomicity ceiling",
    )
    work_pack = replace_once(
        work_pack,
        "- [closeout chain](work-pack/shared/CLOSEOUT-CONTRACT.md);\n- `TASK-SESSION-RECEIPT.schema.json`.",
        "- [closeout chain](work-pack/shared/CLOSEOUT-CONTRACT.md);\n- [closure task contracts](work-pack/tasks/TASK-CLOSURE.md);\n- [exact command matrix](work-pack/shared/COMMAND-MATRIX.json);\n- hardened `TASK-SESSION-RECEIPT.schema.json` plus semantic validator\n  `work-pack/shared/validate-task-session-receipt.py`.",
        "handoff refs",
    )
    work_pack = replace_once(
        work_pack,
        "## Blockers And Deferrals\n\n- Blocking planning: none after repaired Distill recheck.\n- Native feature source blocked until 002–004 pass.",
        "## Blockers And Deferrals\n\n- Plan-contract gaps found by the readiness audit are repaired and must be\n  rechecked by the post-refresh audit.\n- Runtime admission remains blocked for all 29 units: material SWUs need current\n  exact material packages, while output-only and audit-only tasks need a\n  truthful Task Session execution mode owned by the Task Session lifecycle.\n- Native feature source remains blocked until 002–004 pass.",
        "blockers",
    )
    work_pack = replace_once(
        work_pack,
        "Independent recheck passed with `0 of 26` task-shaped units and no\nacceptance-critical residue.",
        "Distill atomicity recheck passed with `0 of 26` task-shaped units. The\nlater full-frontier readiness audit correctly blocked selection and supersedes\nany broader readiness inference.",
        "recheck ceiling",
    )
    work_pack = replace_once(
        work_pack,
        "- plan authored/repaired: pass\n- plan evidence: pending\n- selected SWU: none\n- implementation authority: not granted\n- next route: explicit selection of 001",
        "- plan authored/repaired: pass pending post-refresh audit\n- plan evidence: pending\n- runtime admission: block\n- selected SWU: none\n- implementation authority: not granted\n- next route: rerun `work-pack-readiness-audit`; then route Task Session\n  task-class admission to `sigil-development` and build a material package for\n  the first explicitly selected material SWU",
        "gate result",
    )
    stage(RUN_ROOT / "WORK-PACK.md", work_pack)

    context = read(RUN_ROOT / "work-pack/shared/CONTEXT.md")
    context = replace_once(
        context,
        "- accepted review `findings.md` and `synthesis.md`",
        "- accepted review\n  `projects/body-war/development/reviews/20260730-ontology-ui-black-box/findings.md`\n  and\n  `projects/body-war/development/reviews/20260730-ontology-ui-black-box/synthesis.md`",
        "review selectors",
    )
    context += textwrap.dedent(
        """

        ## Readiness And Runtime Reuse

        - `COMMAND-MATRIX.json` is the exact per-unit argv/cwd/write/attempt/
          teardown contract.
        - SWU 003 generalizes the retained
          `scripts/materialize-l1-workroot.mjs` lifecycle instead of creating a
          second extraction/install/cleanup owner.
        - SWU 004 extends its independent-verification pattern.
        - A successor `FOCUS-SCENE-BUILD.lock.json` may import only verified
          upstream/toolchain/execution substrate from `L1-BUILD.lock.json`; it
          must not import the historical `?oew=1` feature overlay.
        - The closeout directory is created atomically by the first admitted
          closeout owner; an absent directory is not execution evidence.
        """
    )
    stage(RUN_ROOT / "work-pack/shared/CONTEXT.md", context)

    closeout = read(RUN_ROOT / "work-pack/shared/CLOSEOUT-CONTRACT.md")
    closeout = replace_once(
        closeout,
        "Every SWU terminal receipt validates against\n`TASK-SESSION-RECEIPT.schema.json`. Invoke Refresh may update only:",
        "Every SWU terminal receipt validates structurally against\n`TASK-SESSION-RECEIPT.schema.json` and semantically against\n`validate-task-session-receipt.py`. A Task Session terminal receipt is not an\nInvoke Refresh owner receipt; each keeps its own identity and owner.\n\nInvoke Refresh may update only:",
        "receipt boundary",
    )
    closeout = replace_once(
        closeout,
        "Closure tasks use the same normalized receipt schema with their exact task ID\nin `unit_id`. They have no source write scope and cannot repair findings.",
        "Full closure task contracts live at\n`../tasks/TASK-CLOSURE.md`. They use the same terminal schema with their exact\nID in `unit_id`, have no source/material write scope, and cannot repair\nfindings. Their only write is the declared closeout receipt.\n\n`work-pack/closeout/` may be absent before execution. The first admitted\ncloseout owner creates it atomically, fails if a non-directory occupies the\npath, never overwrites an existing receipt, and records creation or reuse in\nits terminal receipt.",
        "closure contract",
    )
    stage(RUN_ROOT / "work-pack/shared/CLOSEOUT-CONTRACT.md", closeout)

    foundation = read(RUN_ROOT / "work-pack/tasks/TASK-FOUNDATION.md")
    foundation = replace_once(
        foundation,
        "- Primary behavior: author a materializer that can create an outside-repository,",
        "- Primary behavior: generalize the retained\n  `scripts/materialize-l1-workroot.mjs` lifecycle into a successor materializer\n  that can create an outside-repository,",
        "materializer reuse",
    )
    foundation = replace_once(
        foundation,
        "- Primary behavior: author independent validation of a materializer handle",
        "- Primary behavior: extend the retained independent-verification pattern\n  to validate a successor materializer handle",
        "verifier reuse",
    )
    foundation = replace_once(
        foundation,
        "SWU-OFSP-014 produces and verifies the first immutable handle.",
        "SWU-OFSP-014 produces and verifies the first immutable handle. The\nsuccessor `FOCUS-SCENE-BUILD.lock.json` imports only verified upstream,\ntoolchain, and execution substrate; the historical `?oew=1` feature inputs stay\nexcluded.",
        "successor lock",
    )
    stage(RUN_ROOT / "work-pack/tasks/TASK-FOUNDATION.md", foundation)

    package = read(RUN_ROOT / "work-pack/tasks/TASK-PACKAGE.md")
    package = replace_once(
        package,
        "`cyberAlchemy-v2/implementation/ontology-evidence-workbench/generated/runs/SWU-OFSP-026/<attempt>/`",
        "`cyberAlchemy-v2/implementation/ontology-evidence-workbench/generated/runs/SWU-OFSP-026/{attempt_id}/`",
        "package attempt path",
    )
    package = replace_once(
        package,
        "- Validation: manifest schema/digest verification and one clean local\n  reproduction.",
        "- Validation: exact argv, runtime, attempt ID, collision, and teardown\n  contracts are owned by `../shared/COMMAND-MATRIX.json#SWU-OFSP-026`.",
        "package command",
    )
    stage(RUN_ROOT / "work-pack/tasks/TASK-PACKAGE.md", package)

    stage(
        RUN_ROOT / "TASK-SESSION-RECEIPT.schema.json",
        json.dumps(hardened_receipt_schema(), indent=2, sort_keys=True) + "\n",
    )
    stage(
        RUN_ROOT / "work-pack/shared/COMMAND-MATRIX.json",
        json.dumps(matrix, indent=2, sort_keys=True) + "\n",
    )
    stage(RUN_ROOT / "work-pack/tasks/TASK-CLOSURE.md", closure_contract())
    stage(
        RUN_ROOT / "work-pack/shared/validate-task-session-receipt.py",
        semantic_validator(),
    )
    stage(
        RUN_ROOT / "work-pack/shared/test-task-session-receipt.py",
        semantic_tests(),
    )


def main() -> int:
    matrix = command_matrix()
    patch_existing_targets(matrix)
    inventory = []
    for target in TARGETS:
        staged = STAGING_ROOT / target
        content = staged.read_bytes()
        inventory.append(
            {
                "target_path": target.as_posix(),
                "operation": "update"
                if (REPOSITORY_ROOT / target).exists()
                else "create",
                "sha256": hashlib.sha256(content).hexdigest(),
                "size_bytes": len(content),
            }
        )
    (REFRESH_ROOT / "STAGED-TARGET-INVENTORY.json").write_text(
        json.dumps(inventory, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"targets": len(inventory), "staging_root": str(STAGING_ROOT)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
