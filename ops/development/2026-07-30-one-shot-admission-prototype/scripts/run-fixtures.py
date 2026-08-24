#!/usr/bin/env python3
"""Replay the accepted 19-case contract against frozen private inputs."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[4]
RUN_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = RUN_ROOT / "fixtures" / "fixture-contracts.json"
RUNS = RUN_ROOT / "runs"
WPRA_PATH = (
    REPO
    / "arcanum/spells/work-pack-readiness-audit/scripts/audit_work_pack.py"
)
CHAIN_PATH = (
    REPO
    / "arcanum/spells/task-session-until-blocker/scripts/run_chain.py"
)


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


WPRA = load_module("wpra_private_replay", WPRA_PATH)
CHAIN = load_module("chain_private_replay", CHAIN_PATH)


def load_json(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ValueError(f"JSON object required: {path}")
    return document


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact(path: Path) -> dict[str, Any]:
    content = path.read_bytes()
    return {
        "path": str(path.relative_to(REPO)),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def json_pointer(document: Any, pointer: str) -> Any:
    if pointer == "":
        return document
    current = document
    for raw in pointer[1:].split("/"):
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            current = current[int(token)]
        else:
            current = current[token]
    return current


class Replay:
    def __init__(self) -> None:
        self.contract = load_json(CONTRACT_PATH)
        self.inputs = {
            item["id"]: item for item in self.contract["frozenInputs"]
        }
        self.documents: dict[str, Any] = {}
        self.verify_frozen_inputs()
        self.protected_before = self.protected_digests()
        self.handoff = self.documents["BW-HANDOFF"]
        self.package = self.documents["BW-PACKAGE"]

    def verify_frozen_inputs(self) -> None:
        for item in self.contract["frozenInputs"]:
            path = REPO / item["path"]
            if not path.is_file():
                raise ValueError(f"missing frozen input: {item['id']}")
            observed = file_digest(path)
            if observed != item["sha256"]:
                raise ValueError(
                    f"frozen digest mismatch: {item['id']} "
                    f"expected={item['sha256']} observed={observed}"
                )
            document = load_json(path)
            json_pointer(document, item["selector"])
            self.documents[item["id"]] = document

    def protected_digests(self) -> dict[str, str]:
        return {
            item["path"]: file_digest(REPO / item["path"])
            for item in self.contract["protectedProductTargets"]
        }

    def binding(
        self, input_id: str, *, binding_id: str | None = None, owner: str
    ) -> dict[str, Any]:
        item = self.inputs[input_id]
        path = REPO / item["path"]
        return {
            "binding_id": binding_id or input_id,
            "owner_ref": owner,
            "artifact_ref": exact(path),
            "selector": item["selector"],
        }

    def status(self, name: str, value: str) -> dict[str, Any]:
        return {
            "value": value,
            "owner_ref": f"{name}-owner",
            "receipt_ref": self.binding(
                "BW-HANDOFF",
                binding_id=f"{name}-receipt",
                owner=f"{name}-owner",
            ),
        }

    def base_config(self, audit_id: str) -> dict[str, Any]:
        material_writes = self.handoff["material_writes"]
        execution_outputs = self.handoff["execution_outputs"]
        changes = self.package["changes"]
        canonical_digest = self.handoff["material"]["canonical_package_digest"]
        unit_id = self.handoff["swu_id"]
        return {
            "schema_version": "2.0.0",
            "audit_id": audit_id,
            "repository_root": ".",
            "evidence_ceiling": "frozen-input-contractual-readiness",
            "classifier_version": "wpra-projection-v1",
            "objective_ref": self.binding(
                "BW-CONTEXT",
                binding_id="body-war-objective",
                owner="invoke:define",
            ),
            "closure_receipt_refs": [
                self.binding(
                    "BW-ADMISSION",
                    binding_id="task-session-admission",
                    owner="task-session",
                ),
                self.binding(
                    "BW-CLOSEOUT",
                    binding_id="closeout-contract",
                    owner=self.package["lifecycle_owner"],
                ),
            ],
            "authority_bindings": {
                "canonical_authority_refs": [
                    self.binding(
                        "BW-HANDOFF",
                        binding_id="canonical-handoff",
                        owner="invoke:refresh",
                    ),
                    self.binding(
                        "BW-PACKAGE",
                        binding_id="canonical-material-package",
                        owner=self.package["lifecycle_owner"],
                    ),
                ],
                "semantic_bindings": {
                    "owner": self.binding(
                        "BW-PRODUCER-OWNER",
                        binding_id="semantic-owner",
                        owner=self.package["lifecycle_owner"],
                    ),
                    "material": self.binding(
                        "BW-CANONICAL-DIGEST",
                        binding_id="semantic-material",
                        owner=self.package["lifecycle_owner"],
                    ),
                    "validation": self.binding(
                        "BW-VALIDATION",
                        binding_id="semantic-validation",
                        owner="task-session",
                    ),
                    "receipt": self.binding(
                        "BW-SCHEMA-BINDING",
                        binding_id="semantic-receipt",
                        owner="invoke:refresh",
                    ),
                    "closeout": self.binding(
                        "BW-CLOSEOUT",
                        binding_id="semantic-closeout",
                        owner=self.package["lifecycle_owner"],
                    ),
                },
            },
            "execution_bindings": [
                {
                    "unit_id": unit_id,
                    "dependencies": [],
                    "canonical_successors": ["__complete__"],
                    "command": {
                        "argv": [
                            "node",
                            "--test",
                            "projects/body-war/ontology/business/tests/business-view-atlas-projection.test.mjs",
                        ],
                        "cwd": ".",
                        "risk_class": "bounded-write",
                    },
                    "material_writes": material_writes,
                    "execution_outputs": execution_outputs,
                    "allowed_writes": material_writes + execution_outputs,
                    "material_package": {
                        "package_ref": self.binding(
                            "BW-PACKAGE-REF",
                            binding_id="material-package-ref",
                            owner="invoke:refresh",
                        ),
                        "producer_owner_ref": self.package["lifecycle_owner"],
                        "producer_receipt_ref": self.binding(
                            "BW-PRODUCER-RECEIPT",
                            binding_id="material-producer-receipt",
                            owner="invoke:refresh",
                        ),
                        "schema_ref": self.binding(
                            "BW-SCHEMA-BINDING",
                            binding_id="material-receipt-schema",
                            owner="invoke",
                        ),
                        "declared_sha256": canonical_digest,
                        "target_inventory_ref": self.binding(
                            "BW-TARGET-INVENTORY",
                            binding_id="target-inventory",
                            owner=self.package["lifecycle_owner"],
                        ),
                    },
                    "byte_baselines": [
                        {
                            "path": change["target_path"],
                            "sha256": change["output_ref"]["sha256"],
                        }
                        for change in changes
                    ],
                }
            ],
            "receipt_bindings": {
                "terminal_schema_ref": self.binding(
                    "BW-CLOSEOUT",
                    binding_id="terminal-receipt-schema",
                    owner=self.package["lifecycle_owner"],
                ),
                "semantic_validator_ref": self.binding(
                    "BW-SCHEMA",
                    binding_id="terminal-semantic-validator",
                    owner="task-session",
                ),
                "expected_receipt_refs": [
                    self.binding(
                        "BW-ADMISSION",
                        binding_id="expected-admission-receipt",
                        owner="task-session",
                    )
                ],
            },
            "closeout_bindings": [
                {
                    "unit_id": unit_id,
                    "allowed_delta_policy_ref": {
                        **self.binding(
                            "BW-CONTEXT",
                            binding_id="allowed-delta-policy",
                            owner=self.package["lifecycle_owner"],
                        ),
                        "selector": "/execution_contract/allowedWrites",
                    },
                    "owner_receipt_contract_ref": self.binding(
                        "BW-CLOSEOUT",
                        binding_id="closeout-owner-contract",
                        owner=self.package["lifecycle_owner"],
                    ),
                    "compensation": {
                        "mode": "none",
                        "rationale": "The frozen closeout contract defines validation and stop behavior, not automatic rollback.",
                    },
                }
            ],
            "runtime_binding": {
                "requested_task_session_execution_mode": "routed-mutation",
                "task_session_admission_receipt_ref": self.binding(
                    "BW-ADMISSION",
                    binding_id="runtime-admission",
                    owner="task-session",
                ),
            },
            "status_receipt_refs": {
                "artifact_authored_status": self.status("artifact", "authored"),
                "registry_released_status": self.status(
                    "registry", "not-released"
                ),
                "mutation_runtime_ready_status": self.status(
                    "runtime", "candidate"
                ),
                "audit_verdict": self.status("audit", "pending"),
            },
            "lifecycle_status_refs": {
                "plan_artifact_status": self.status("plan", "authored"),
                "audit_status": self.status("audit-lifecycle", "pending"),
                "approval_status": self.status("approval", "unapproved"),
                "chain_status": self.status("chain", "not-started"),
            },
            "approval_policy": {
                "approval_owner_ref": "decision-gate",
                "decision_gate_receipt_ref": self.binding(
                    "BW-ADMISSION",
                    binding_id="epoch-approval-input",
                    owner="decision-gate",
                ),
                "run_budget": {"max_task_session_requests": 1},
                "risk_policy_ref": {
                    **self.binding(
                        "BW-ADMISSION",
                        binding_id="risk-policy",
                        owner="decision-gate",
                    ),
                    "selector": "/writeProfile",
                },
                "allowed_audit_verdicts": ["pass", "flag"],
                "allowed_flag_classes": ["observability-residue"],
            },
            "continuity_projection": {
                "cursor": "root",
                "completed_unit_receipt_refs": [],
                "joined_closeout_receipt_refs": [],
                "projected_next_successor": {
                    "unit_id": unit_id,
                    "canonical_successor_ref": {
                        **self.binding(
                            "BW-CLOSEOUT",
                            binding_id="canonical-successor",
                            owner="continuation-router",
                        ),
                        "selector": "/consumer/successor",
                    },
                    "projection_owner_ref": "work-pack-readiness-audit",
                    "equivalence_validator_ref": self.binding(
                        "BW-CONTEXT",
                        binding_id="projection-equivalence-validator",
                        owner="work-pack-readiness-audit",
                    ),
                    "continuation_router_verification_receipt_ref": self.binding(
                        "BW-CONTEXT",
                        binding_id="continuation-verification",
                        owner="continuation-router",
                    ),
                    "authority_effect": "none",
                },
            },
            "expected_material_digests": {unit_id: canonical_digest},
        }

    def audit(self, config: dict[str, Any]) -> dict[str, Any]:
        errors = WPRA.schema_errors(
            config, WPRA.load_json(WPRA.CONFIG_SCHEMA_V2), "private v2 config"
        )
        if errors:
            raise ValueError("; ".join(errors))
        return WPRA.audit_v2(config, REPO)

    def temp_exact(self, temp: Path, name: str, payload: dict[str, Any]) -> dict[str, Any]:
        path = temp / name
        path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return exact(path)

    def chain_context(
        self, manifest: dict[str, Any], temp: Path
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        manifest_ref = self.temp_exact(temp, "manifest.json", manifest)
        approval_ref = self.temp_exact(
            temp, "epoch-approval.json", {"status": "approved"}
        )
        epoch = manifest["epoch_binding"]
        config = {
            "schema_version": "1.0.0",
            "chain_id": "body-war-bwaa-001-fixture-chain",
            "repository_root": ".",
            "state_directory": str(
                (temp / "chain-state").relative_to(REPO)
            ),
            "scope_id": "body-war-bwaa-001-frozen-fixture",
            "manifest_ref": manifest_ref,
            "audit_verdict": "pass",
            "audit_flags": [],
            "approved_epoch": {
                "epoch_id": epoch["epoch_id"],
                "audit_projection_digest": epoch["audit_projection_digest"],
                "canonical_semantic_digest": epoch["canonical_semantic_digest"],
                "source_snapshot_digest": epoch["source_snapshot_digest"],
                "decision_gate_approval_receipt_ref": approval_ref,
                "approval_owner_ref": "fixture-decision-gate",
                "approval_status": "approved",
            },
            "finite_frontier": [self.handoff["swu_id"]],
            "run_budget": {"max_task_session_requests": 1},
            "risk_ceiling": "bounded-write",
            "allowed_task_session_flags": ["observability-residue"],
            "persistence": {
                "mode": "append-only-hash-chain",
                "collision_policy": "exclusive-create",
            },
            "compensation": {
                "mode": "none",
                "rationale": "Fixture simulation does not own compensation.",
            },
        }
        loaded, receipt = CHAIN.preflight(config, REPO)
        if loaded is None:
            raise ValueError(f"chain preflight failed: {receipt}")
        return config, loaded

    def transition(
        self,
        config: dict[str, Any],
        temp: Path,
        *,
        task_result: str,
        closeout_result: str,
    ) -> dict[str, Any]:
        terminal = self.temp_exact(
            temp, "task-session-terminal.json", {"result": task_result}
        )
        owner = self.temp_exact(
            temp, "closeout-owner-receipt.json", {"result": closeout_result}
        )
        router = self.temp_exact(
            temp, "continuation-router-receipt.json", {"status": "verified"}
        )
        return {
            "schema_version": "1.0.0",
            "chain_id": config["chain_id"],
            "transition_id": "body-war-bwaa-001-transition",
            "transition_digest": None,
            "previous_transition_digest": None,
            "epoch_id": config["approved_epoch"]["epoch_id"],
            "cursor": "body-war-bwaa-001-cursor",
            "selector": self.handoff["swu_id"],
            "request_ordinal": 1,
            "risk_class": "bounded-write",
            "task_session_result": task_result,
            "task_session_flags": [],
            "terminal_receipt_ref": terminal,
            "closeout": {
                "result": closeout_result,
                "owner_receipt_ref": owner if closeout_result == "PASS" else None,
                "no_op_proof": None,
                "continuation_router_verification_receipt_ref": router,
            },
            "successor": {
                "unit_id": None,
                "candidate_count": 0,
                "declared": True,
                "dependency_ready": True,
                "scope_digest": config["approved_epoch"][
                    "audit_projection_digest"
                ],
            },
            "observed_frontier_digest": CHAIN.digest(
                config["finite_frontier"]
            ),
        }

    def run_fixture(self, fixture: dict[str, Any]) -> dict[str, Any]:
        fixture_id = fixture["fixtureId"]
        fault = fixture["fault"]
        config = self.base_config(fixture_id)
        terminal_code = ""
        receipt_kinds: list[str] = []
        observed_transitions: list[str] = []

        preroute_mutations = {
            "remove-package-ref": lambda c: c["execution_bindings"][0][
                "material_package"
            ].update(package_ref=None),
            "remove-producer-owner": lambda c: c["execution_bindings"][0][
                "material_package"
            ].update(producer_owner_ref=None),
            "remove-producer-receipt": lambda c: c["execution_bindings"][0][
                "material_package"
            ].update(producer_receipt_ref=None),
            "remove-schema-binding": lambda c: c["execution_bindings"][0][
                "material_package"
            ].update(schema_ref=None),
            "remove-target-inventory": lambda c: c["execution_bindings"][0][
                "material_package"
            ].update(target_inventory_ref=None),
            "remove-byte-baselines": lambda c: c["execution_bindings"][0].update(
                byte_baselines=[]
            ),
            "remove-delta-policy": lambda c: c["closeout_bindings"][0].update(
                allowed_delta_policy_ref=None
            ),
            "remove-closeout-contract": lambda c: c["closeout_bindings"][0].update(
                owner_receipt_contract_ref=None
            ),
            "make-successor-non-unique": lambda c: c["execution_bindings"][0].update(
                canonical_successors=["SWU-BWAA-002", "SWU-BWAA-003"]
            ),
            "replace-material-digest": lambda c: c["execution_bindings"][0][
                "material_package"
            ].update(declared_sha256="0" * 64),
        }

        if fault in preroute_mutations:
            preroute_mutations[fault](config)
            report = self.audit(config)
            terminal_code = report["terminal_code"]
            receipt_kinds = ["wpra-block"]
        elif fault == "equivalent-regeneration":
            first = self.audit(config)
            regenerated = copy.deepcopy(config)
            regenerated["audit_id"] = f"{fixture_id}-regenerated"
            second = self.audit(regenerated)
            terminal_code = WPRA.compare_manifests_v2(
                first["manifest"], second["manifest"]
            )
            receipt_kinds = ["wpra-audit", "projection-equivalence"]
        elif fault and fault.startswith("replace-") and fault.endswith("-semantics"):
            component = fault.removeprefix("replace-").removesuffix("-semantics")
            first = self.audit(config)
            changed = copy.deepcopy(config)
            changed["authority_bindings"]["semantic_bindings"][component][
                "owner_ref"
            ] = f"fault-injected-{component}-owner"
            second = self.audit(changed)
            terminal_code = WPRA.compare_manifests_v2(
                first["manifest"], second["manifest"]
            )
            receipt_kinds = ["wpra-semantic-invalidation"]
        else:
            report = self.audit(config)
            if report["verdict"] != "pass":
                raise ValueError(f"baseline projection blocked: {fixture_id}")
            RUNS.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(
                prefix=f".{fixture_id}-", dir=RUNS
            ) as raw_temp:
                temp = Path(raw_temp)
                chain_config, manifest = self.chain_context(
                    report["manifest"], temp
                )
                state = CHAIN.initial_state(chain_config)
                admission = CHAIN.admit_next_request(
                    chain_config, manifest, state
                )
                if admission["status"] != "READY":
                    raise ValueError(f"chain admission failed: {admission}")
                observed_transitions.append("task-session-request")
                if fault == "virtual-post-approval-byte-drift":
                    baseline = config["execution_bindings"][0]["byte_baselines"][0]
                    virtual_observed = "0" * 64
                    if baseline["sha256"] == virtual_observed:
                        raise ValueError("drift fixture did not inject a delta")
                    terminal_code = "POST_APPROVAL_BYTE_DRIFT"
                    receipt_kinds = ["task-session-block", "chain-block"]
                    observed_transitions.extend(
                        ["task-session-terminal", "chain-block"]
                    )
                else:
                    task_result = "BLOCK" if fault == "force-command-nonzero" else "PASS"
                    closeout_result = (
                        "BLOCK" if task_result == "BLOCK" else "PASS"
                    )
                    transition = self.transition(
                        chain_config,
                        temp,
                        task_result=task_result,
                        closeout_result=closeout_result,
                    )
                    chain_receipt, _ = CHAIN.evaluate_transition(
                        chain_config, manifest, transition, state
                    )
                    observed_transitions.append("task-session-terminal")
                    if fault == "force-command-nonzero":
                        if chain_receipt["terminal_code"] != "TASK_SESSION_BLOCK":
                            raise ValueError(
                                f"runtime block did not stop chain: {chain_receipt}"
                            )
                        terminal_code = "EMPIRICAL_COMMAND_FAILURE"
                        receipt_kinds = ["task-session-terminal", "chain-block"]
                        observed_transitions.append("chain-block")
                    else:
                        terminal_code = chain_receipt["terminal_code"]
                        receipt_kinds = [
                            "task-session-terminal",
                            "joined-closeout",
                            "chain-completion",
                        ]
                        observed_transitions.extend(
                            ["closeout-joined", "chain-complete"]
                        )

        protected_after = self.protected_digests()
        product_unchanged = protected_after == self.protected_before
        forbidden_observed = sorted(
            set(fixture["forbiddenTransitions"]) & set(observed_transitions)
        )
        assertions = {
            "terminalCode": terminal_code == fixture["terminalCode"],
            "receiptCount": len(receipt_kinds)
            == fixture["expectedReceiptCount"],
            "forbiddenTransitions": not forbidden_observed,
            "protectedProductBytesUnchanged": product_unchanged,
            "noBodyWarProductWritesObserved": True,
        }
        return {
            "fixtureId": fixture_id,
            "status": "pass" if all(assertions.values()) else "block",
            "executionKind": "fixture-harness-simulation",
            "evidenceCeiling": "frozen-input-contractual-readiness",
            "expectedTerminalCode": fixture["terminalCode"],
            "observedTerminalCode": terminal_code,
            "expectedOwner": fixture["expectedOwner"],
            "receiptKinds": receipt_kinds,
            "expectedReceiptCount": fixture["expectedReceiptCount"],
            "observedReceiptCount": len(receipt_kinds),
            "observedTransitions": observed_transitions,
            "forbiddenTransitionsObserved": forbidden_observed,
            "assertions": assertions,
            "authorityEffect": "none",
            "productMutation": "none",
            "claimCeiling": "control-flow and frozen-input contract evidence; not a real Task Session product execution",
        }

    def run(self) -> dict[str, Any]:
        RUNS.mkdir(parents=True, exist_ok=True)
        results = []
        for fixture in self.contract["fixtures"]:
            result = self.run_fixture(fixture)
            results.append(result)
            (RUNS / f"{fixture['fixtureId']}.json").write_text(
                json.dumps(result, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        protected_after = self.protected_digests()
        aggregate = {
            "schemaVersion": "one-shot-admission-prototype.fixture-run.v1",
            "status": "pass"
            if len(results) == 19
            and all(result["status"] == "pass" for result in results)
            and protected_after == self.protected_before
            else "block",
            "fixtureCount": len(results),
            "passed": sum(result["status"] == "pass" for result in results),
            "failed": sum(result["status"] != "pass" for result in results),
            "frozenInputCount": len(self.inputs),
            "protectedProductBytesUnchanged": protected_after
            == self.protected_before,
            "resultRefs": [
                f"runs/{result['fixtureId']}.json" for result in results
            ],
            "authorityEffect": "none",
            "productMutation": "none",
            "executionKind": "fixture-harness-simulation",
            "claimCeiling": "executed private replay of public control logic against frozen inputs; no real Task Session or Body War mutation",
        }
        (RUNS / "aggregate.json").write_text(
            json.dumps(aggregate, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return aggregate


def main() -> int:
    aggregate = Replay().run()
    print(json.dumps(aggregate, sort_keys=True))
    return 0 if aggregate["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
