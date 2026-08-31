#!/usr/bin/env python3
"""Emit one exact custom owner request for the frozen Invoke bootstrap repair."""

from __future__ import annotations

import argparse
import hashlib
import json
import stat
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def exact_ref(path: Path, root: Path) -> dict[str, Any]:
    content = path.read_bytes()
    return {
        "path": path.resolve().relative_to(root.resolve()).as_posix(),
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def mode_string(path: Path) -> str:
    return f"{stat.S_IMODE(path.stat().st_mode):04o}"


def verify_exact_ref(reference: dict[str, Any], root: Path, label: str) -> None:
    path = root / reference["path"]
    if not path.is_file():
        raise ValueError(f"missing {label}: {reference['path']}")
    content = path.read_bytes()
    if hashlib.sha256(content).hexdigest() != reference["sha256"]:
        raise ValueError(f"{label} digest drift: {reference['path']}")
    if len(content) != reference["size_bytes"]:
        raise ValueError(f"{label} size drift: {reference['path']}")


def verify_freeze(
    root: Path,
    freeze: dict[str, Any],
    material: dict[str, Any],
    material_receipt: dict[str, Any],
    review: dict[str, Any],
) -> None:
    freeze_projection = dict(freeze)
    claimed_freeze_digest = freeze_projection.pop("freeze_digest", None)
    if claimed_freeze_digest != canonical_digest(freeze_projection):
        raise ValueError("freeze digest mismatch")

    targets = freeze["targets"]
    target_paths = [item["target_path"] for item in targets]
    if len(target_paths) != 68 or len(set(target_paths)) != 68:
        raise ValueError("freeze target count or uniqueness mismatch")
    if freeze["canonical_target_count"] != 32:
        raise ValueError("canonical target count mismatch")
    if freeze["generated_target_count"] != 36:
        raise ValueError("generated target count mismatch")
    if freeze["delete_target_count"] != 0:
        raise ValueError("delete target present")

    computed_baseline_digest = canonical_digest(
        [
            {"target_path": item["target_path"], **item["baseline"]}
            for item in targets
        ]
    )
    if computed_baseline_digest != freeze["baseline_digest"]:
        raise ValueError("baseline digest mismatch")
    computed_postimage_digest = canonical_digest(
        [
            {
                "target_path": item["target_path"],
                "operation": item["operation"],
                "postimage_ref": item["postimage_ref"],
                "postimage_mode": item["postimage_mode"],
            }
            for item in targets
        ]
    )
    if computed_postimage_digest != freeze["postimage_digest"]:
        raise ValueError("postimage digest mismatch")

    for item in targets:
        target_path = item["target_path"]
        verify_exact_ref(item["postimage_ref"], root, "frozen postimage")
        postimage_path = root / item["postimage_ref"]["path"]
        if mode_string(postimage_path) != item["postimage_mode"]:
            raise ValueError(f"postimage mode drift: {target_path}")

        live_path = root / target_path
        baseline = item["baseline"]
        if baseline["state"] == "absent":
            if live_path.exists():
                raise ValueError(f"absent live baseline now exists: {target_path}")
            if item["operation"] != "create":
                raise ValueError(f"absent baseline is not create: {target_path}")
        else:
            if not live_path.is_file():
                raise ValueError(f"present live baseline is missing: {target_path}")
            content = live_path.read_bytes()
            if hashlib.sha256(content).hexdigest() != baseline["sha256"]:
                raise ValueError(f"live baseline digest drift: {target_path}")
            if len(content) != baseline["size_bytes"]:
                raise ValueError(f"live baseline size drift: {target_path}")
            if mode_string(live_path) != baseline["mode"]:
                raise ValueError(f"live baseline mode drift: {target_path}")
            if item["operation"] != "update":
                raise ValueError(f"present baseline is not update: {target_path}")

    material_paths = [item["target_path"] for item in material["changes"]]
    if material_paths != target_paths:
        raise ValueError("material package target order or inventory mismatch")
    if material_receipt.get("patchVerdict") != "candidate-pass":
        raise ValueError("material package is not candidate-pass")
    if material_receipt.get("mutationHandoff") != "gated":
        raise ValueError("material handoff is not gated")
    if material_receipt.get("validatedPaths") != sorted(target_paths):
        raise ValueError("material receipt validated-path inventory mismatch")
    if material_receipt.get("packageDigest") != canonical_digest(material):
        raise ValueError("material package digest mismatch")

    if review.get("result") != "pass":
        raise ValueError("independent review did not pass")
    if review.get("reviewed_freeze_digest") != freeze["freeze_digest"]:
        raise ValueError("review freeze binding mismatch")
    if review.get("reviewed_baseline_digest") != freeze["baseline_digest"]:
        raise ValueError("review baseline binding mismatch")
    if review.get("reviewed_postimage_digest") != freeze["postimage_digest"]:
        raise ValueError("review postimage binding mismatch")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    run_dir = args.run_dir.resolve()
    request_path = run_dir / "REPAIR-EFFECT-AUTHORIZATION-REQUEST.json"
    if request_path.exists():
        existing = load_json(request_path)
        projection = dict(existing)
        claimed = projection.pop("request_digest", None)
        if claimed != canonical_digest(projection):
            raise ValueError("existing request digest mismatch")
        print(json.dumps({"result": "idempotent-existing", "request_digest": claimed}))
        return 0

    freeze_path = run_dir / "CANDIDATE-FREEZE.json"
    material_path = run_dir / "MATERIAL-PACKAGE.json"
    material_receipt_path = run_dir / "MATERIAL-PACKAGE-RECEIPT.json"
    validation_path = run_dir / "VALIDATION-RECEIPT.json"
    review_path = run_dir / "INDEPENDENT-REVIEW.json"
    selection_path = run_dir / "CANDIDATE-SELECTION-RECEIPT.json"
    unit_contract_path = run_dir / "UNIT-CONTRACT.json"
    reconciliation_path = run_dir / "LIVE-DRIFT-RECONCILIATION.json"
    for path in (
        freeze_path,
        material_path,
        material_receipt_path,
        validation_path,
        review_path,
        selection_path,
        unit_contract_path,
        reconciliation_path,
    ):
        if not path.is_file():
            raise ValueError(f"missing request prerequisite: {path}")

    freeze = load_json(freeze_path)
    material = load_json(material_path)
    material_receipt = load_json(material_receipt_path)
    review = load_json(review_path)
    verify_freeze(root, freeze, material, material_receipt, review)

    target_paths = [item["target_path"] for item in freeze["targets"]]
    run_id = freeze["run_id"]
    target_count = freeze["target_count"]
    canonical_target_count = freeze["canonical_target_count"]
    generated_target_count = freeze["generated_target_count"]
    request: dict[str, Any] = {
        "schema_version": "invoke.governance-repair-effect-authorization-request.v1",
        "request_id": f"invoke-governance-repair-{run_id}",
        "status": "pending-owner-decision",
        "request_class": "custom-bootstrap-exact-owner-decision",
        "canonical_v3_request_claimed": False,
        "issued_at": datetime.now(timezone.utc).isoformat(),
        "lifecycle_owner": "spellcraft",
        "evidence": {
            "freeze_ref": exact_ref(freeze_path, root),
            "freeze_digest": freeze["freeze_digest"],
            "baseline_digest": freeze["baseline_digest"],
            "postimage_digest": freeze["postimage_digest"],
            "material_package_ref": exact_ref(material_path, root),
            "material_package_receipt_ref": exact_ref(material_receipt_path, root),
            "validation_receipt_ref": exact_ref(validation_path, root),
            "independent_review_ref": exact_ref(review_path, root),
            "selection_receipt_ref": exact_ref(selection_path, root),
            "unit_contract_ref": exact_ref(unit_contract_path, root),
            "live_drift_reconciliation_ref": exact_ref(reconciliation_path, root),
        },
        "requested_effect": {
            "effect_id": f"install-invoke-preacceptance-governance-repair-{run_id}",
            "target_count": target_count,
            "canonical_target_count": canonical_target_count,
            "generated_target_count": generated_target_count,
            "delete_target_count": 0,
            "target_paths": target_paths,
            "baseline_digest": freeze["baseline_digest"],
            "postimage_digest": freeze["postimage_digest"],
            "allowed_effects": [
                "revalidate every accepted live baseline before the first write",
                f"apply only the {canonical_target_count} accepted canonical postimages and their accepted modes",
                "run the selective Invoke generated-package sync for repo-codex and claude profiles",
                f"require the resulting {generated_target_count} generated targets to equal the accepted postimages and modes",
                "run the accepted canonical, generated, Task Session, and hygiene validations",
                "write a local repair execution receipt",
            ],
            "forbidden_effects": [
                f"modify any path outside the accepted {target_count}-target inventory",
                "modify Task Session runtime, schema, script, or generated package targets",
                "modify Task Session Until Blocker runtime, schema, script, or generated package targets",
                "treat the preserved accepted-stream candidate as selected, admitted, accepted, or runtime-ready",
                "copy the whole isolated candidate or its run reports",
                "mutate Body War product bytes",
                "submit to Strava or use credentials",
                "deploy, publish, commit, push, or create external effects",
                "execute a successor after any baseline or validation failure",
            ],
            "apply_protocol": [
                f"verify the accepted envelope and all {target_count} live baselines again",
                f"apply exact canonical postimages from {run_id}",
                "sync only the Invoke generated skill package into the two declared profiles",
                f"verify all {target_count} post-apply bytes and modes against {run_id}",
                "run all accepted validation commands and stop on the first effectful failure",
            ],
            "failure_policy": (
                "Any pre-write drift invalidates this request. Any effectful failure stops "
                "the chain before Body War continuation and preserves failure evidence."
            ),
        },
        "post_apply_no_effect_continuation": (
            "After a passing repair receipt, generate a fresh proposal-only Body War "
            "continuation route. This request does not authorize Body War product mutation, "
            "Strava submission, deployment, geometry, scoring, or privacy-owner decisions."
        ),
        "acceptance_protocol": {
            "response_prefix": "confirmed ",
            "binds_field": "request_digest",
            "exact_match_required": True,
            "identical_confirmation_is_idempotent": True,
            "any_envelope_or_baseline_change_requires_new_request": True,
        },
        "authority_effect": "none-until-exact-owner-confirmation",
        "claim_ceiling": (
            "This custom request proves a reviewed bootstrap repair candidate only. It is "
            "not canonical owner-acceptance-request output and does not itself apply, "
            "publish, deploy, execute Body War, admit accepted-stream work, establish "
            "accepted-stream runtime readiness, or create external effects."
        ),
        "superseded_attempts": [
            "20260826T212341Z-spellcraft-candidate-freeze-001",
            "20260826T214819Z-spellcraft-candidate-freeze-002",
            "20260826T223042Z-spellcraft-candidate-freeze-003",
            "20260827T004549Z-spellcraft-candidate-freeze-004",
            "20260827T005054Z-spellcraft-candidate-freeze-005",
        ],
    }
    request["request_digest"] = canonical_digest(request)
    request_path.write_text(
        json.dumps(request, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    if file_digest(request_path) == "":
        raise AssertionError("unreachable empty request digest")
    print(
        json.dumps(
            {
                "result": "emitted",
                "request_path": str(request_path),
                "request_digest": request["request_digest"],
                "target_count": target_count,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
