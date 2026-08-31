#!/usr/bin/env python3
"""Validate the planned Minto L0 experiment over actual repository bytes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, NoReturn


SCRIPT = Path(__file__).resolve()
CASE_CHECK_IDS = [
    "case-schema-closed",
    "source-binding-exact",
    "positive-span-control",
    "declared-hierarchy-shape",
    "review-view-content-preserved",
    "boundary-inactive-untransformed",
    "claim-ceiling",
    "decision-contract-exact",
    "case-byte-binding",
]
JUDGMENT_IDS = [
    "factual-equivalence",
    "fair-representation",
    "executive-transport-fit",
    "hierarchy-plausibility",
    "named-decision-changed",
    "boundary-case-inactive",
]
ALLOWED_STATUSES = ["pass", "fail", "inconclusive"]
QUESTION_RECORDS = [
    {
        "question_id": "factual-equivalence",
        "prompt": "Do variants A and B preserve the same factual content without adding, omitting, or changing a claim?",
        "allowed_statuses": ALLOWED_STATUSES,
        "rationale_required": True,
    },
    {
        "question_id": "fair-representation",
        "prompt": "Given the supported concept and explicit source limits in review_context, does the declared hierarchy avoid claiming more than that context supports?",
        "allowed_statuses": ALLOWED_STATUSES,
        "rationale_required": True,
    },
    {
        "question_id": "executive-transport-fit",
        "prompt": "Given the stated audience, purpose, transport, and whole-document unit, is the declared hierarchy a plausible structural fit for this executive brief?",
        "allowed_statuses": ALLOWED_STATUSES,
        "rationale_required": True,
    },
    {
        "question_id": "hierarchy-plausibility",
        "prompt": "Does one variant plausibly present one governing point with the displayed support blocks associated beneath it?",
        "allowed_statuses": ALLOWED_STATUSES,
        "rationale_required": True,
    },
    {
        "question_id": "named-decision-changed",
        "prompt": "Does exactly one variant exhibit the declared-governing-point-support-hierarchy decision rather than the flat-evidence-led plan? Record A, B, or none.",
        "allowed_statuses": ALLOWED_STATUSES,
        "rationale_required": True,
        "exhibiting_variant_label_values": ["A", "B", "none"],
    },
    {
        "question_id": "boundary-case-inactive",
        "prompt": "Given the boundary intent in review_context, should the Minto candidate remain inactive and leave the discovery-led boundary view untransformed?",
        "allowed_statuses": ALLOWED_STATUSES,
        "rationale_required": True,
    },
]
REVIEWER_INSTRUCTIONS = [
    "Review only this packet before completing the response.",
    "Do not infer reader outcomes, preference, adoption, or integration authority.",
    "Use only pass, fail, or inconclusive and give a rationale for every judgment.",
    "For named-decision-changed, select A, B, or none as the view exhibiting the declared hierarchy.",
]
HEX_64 = re.compile(r"^[a-f0-9]{64}$")
NONCE = re.compile(r"^[a-f0-9]{32,128}$")


class ValidationFailure(ValueError):
    """One stable fail-closed validation failure."""

    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def repository_root() -> Path:
    for candidate in SCRIPT.parents:
        if (candidate / ".git").exists():
            return candidate
    raise ValidationFailure("REPOSITORY_ROOT_MISSING", str(SCRIPT))


ROOT = repository_root()


def fail(code: str, detail: str) -> NoReturn:
    raise ValidationFailure(code, detail)


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail("JSON_UNREADABLE", f"{path}: {error}")
    if not isinstance(value, dict):
        fail("OBJECT_REQUIRED", str(path))
    return value


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        fail("PATH_OUTSIDE_REPOSITORY", str(path))


def artifact_ref(path: Path) -> dict[str, Any]:
    try:
        payload = path.read_bytes()
    except OSError as error:
        fail("ARTIFACT_UNREADABLE", f"{path}: {error}")
    return {
        "path": rel(path),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "size_bytes": len(payload),
    }


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def exact_keys(value: Any, keys: set[str], location: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail("OBJECT_REQUIRED", location)
    actual = set(value)
    if actual != keys:
        fail(
            "CLOSED_SHAPE_MISMATCH",
            f"{location}: missing={sorted(keys - actual)} extra={sorted(actual - keys)}",
        )
    return value


def exact_ref(value: Any, path: Path, location: str) -> None:
    ref = exact_keys(value, {"path", "sha256", "size_bytes"}, location)
    expected = artifact_ref(path)
    if ref != expected:
        fail("ARTIFACT_REF_MISMATCH", f"{location}: expected={expected} actual={ref}")


def nonempty_string(value: Any, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail("NONEMPTY_STRING_REQUIRED", location)
    return value


def string_list(value: Any, location: str, *, nonempty: bool = True) -> list[str]:
    if not isinstance(value, list) or (nonempty and not value):
        fail("STRING_LIST_REQUIRED", location)
    if any(not isinstance(item, str) or not item.strip() for item in value):
        fail("STRING_LIST_REQUIRED", location)
    return value


def parse_time(value: Any, location: str) -> datetime:
    raw = nonempty_string(value, location)
    if not raw.endswith("Z"):
        fail("UTC_TIMESTAMP_REQUIRED", location)
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        fail("TIMESTAMP_INVALID", f"{location}: {raw}")


def span_map(spans: Any, location: str, prefix: str) -> dict[str, str]:
    if not isinstance(spans, list):
        fail("SPAN_LIST_REQUIRED", location)
    result: dict[str, str] = {}
    for index, raw in enumerate(spans):
        span = exact_keys(raw, {"span_id", "text"}, f"{location}/{index}")
        span_id = nonempty_string(span["span_id"], f"{location}/{index}/span_id")
        if not re.fullmatch(rf"{prefix}[0-9]{{2}}", span_id):
            fail("SPAN_ID_INVALID", span_id)
        if span_id in result:
            fail("SPAN_ID_DUPLICATE", span_id)
        result[span_id] = nonempty_string(span["text"], f"{location}/{index}/text")
    return result


def validate_view(
    raw: Any,
    location: str,
    expected_blocks: list[tuple[str, str | None, list[str]]],
    texts: dict[str, str],
    span_joiner: str,
    block_joiner: str,
) -> None:
    view = exact_keys(raw, {"blocks", "full_text"}, location)
    if not isinstance(view["blocks"], list) or len(view["blocks"]) != len(
        expected_blocks
    ):
        fail("REVIEW_BLOCK_COUNT_MISMATCH", location)
    rendered_blocks: list[str] = []
    for index, (role, group_id, span_ids) in enumerate(expected_blocks):
        keys = {"block_id", "role", "span_ids", "text"}
        if group_id is not None:
            keys.add("group_id")
        block = exact_keys(view["blocks"][index], keys, f"{location}/blocks/{index}")
        if block["block_id"] != f"BLOCK-{index + 1:02d}":
            fail("REVIEW_BLOCK_ID_MISMATCH", f"{location}/blocks/{index}")
        if block["role"] != role or block["span_ids"] != span_ids:
            fail("REVIEW_BLOCK_STRUCTURE_MISMATCH", f"{location}/blocks/{index}")
        if group_id is not None and block["group_id"] != group_id:
            fail("REVIEW_GROUP_ID_MISMATCH", f"{location}/blocks/{index}")
        try:
            rendered = span_joiner.join(texts[span_id] for span_id in span_ids)
        except KeyError as error:
            fail("REVIEW_SPAN_UNKNOWN", f"{location}: {error.args[0]}")
        if block["text"] != rendered:
            fail("REVIEW_TEXT_DRIFT", f"{location}/blocks/{index}")
        rendered_blocks.append(rendered)
    if view["full_text"] != block_joiner.join(rendered_blocks):
        fail("REVIEW_FULL_TEXT_DRIFT", location)


def validate_case(case: dict[str, Any]) -> dict[str, Any]:
    exact_keys(
        case,
        {
            "schema_version",
            "experiment_id",
            "candidate",
            "source_binding",
            "placement",
            "decision_contract",
            "positive_case",
            "boundary_case",
            "claim_boundary",
            "authority_effect",
        },
        "$case",
    )
    if case["schema_version"] != "whisper.minto-pyramid-experiment-case.v1":
        fail("CASE_SCHEMA_VERSION_INVALID", str(case["schema_version"]))
    if case["experiment_id"] != "minto-pyramid-experiment-001":
        fail("EXPERIMENT_ID_INVALID", str(case["experiment_id"]))
    if case["candidate"] != "minto-pyramid":
        fail("CANDIDATE_ID_INVALID", str(case["candidate"]))

    source = exact_keys(
        case["source_binding"],
        {
            "identity",
            "url",
            "version",
            "selectors",
            "supported_concept",
            "unsupported_inferences",
            "attribution_policy",
        },
        "$case/source_binding",
    )
    expected_source = {
        "identity": "Barbara Minto / Minto Books International",
        "url": "https://www.barbaraminto.com/",
        "version": "site-copyright-2007-2026; textbook-edition-1996",
        "selectors": ["Concept, lines 21-23", "Textbook, lines 35-37"],
        "supported_concept": "one-governing-point-with-supporting-ideas-organized-beneath-it",
        "unsupported_inferences": [
            "MECE",
            "complete-answer-first-method",
            "universal-applicability",
            "reader-efficacy",
        ],
        "attribution_policy": "paraphrase-only-original-examples",
    }
    if source != expected_source:
        fail("SOURCE_BINDING_MISMATCH", "$case/source_binding")

    placement = exact_keys(
        case["placement"],
        {"transport", "unit_level", "current_owner", "owner_context", "proof_status"},
        "$case/placement",
    )
    if placement != {
        "transport": "executive-brief",
        "unit_level": "whole-document",
        "current_owner": "composition_plan",
        "owner_context": "transport-side-of-transport_or_preset_profile",
        "proof_status": "unverified-experiment-candidate",
    }:
        fail("PLACEMENT_MISMATCH", "$case/placement")

    decision = exact_keys(
        case["decision_contract"],
        {"changed_decision", "prevented_failure", "controlled_delta"},
        "$case/decision_contract",
    )
    if decision != {
        "changed_decision": "declared-governing-point-support-hierarchy",
        "prevented_failure": "support-association-not-declared",
        "controlled_delta": ["composition_plan"],
    }:
        fail("DECISION_CONTRACT_MISMATCH", "$case/decision_contract")

    positive = exact_keys(
        case["positive_case"],
        {
            "audience",
            "purpose",
            "word_budget",
            "spans",
            "governing_point_id",
            "baseline",
            "candidate",
            "review_views",
        },
        "$case/positive_case",
    )
    if positive["audience"] != "senior-decision-maker":
        fail("AUDIENCE_MISMATCH", "$case/positive_case/audience")
    if positive["purpose"] != "approve-or-reject-a-reversible-pilot":
        fail("PURPOSE_MISMATCH", "$case/positive_case/purpose")
    if positive["word_budget"] != {"minimum": 300, "maximum": 450}:
        fail("WORD_BUDGET_MISMATCH", "$case/positive_case/word_budget")
    texts = span_map(positive["spans"], "$case/positive_case/spans", "S")
    if not 6 <= len(texts) <= 10:
        fail("POSITIVE_SPAN_COUNT_INVALID", str(len(texts)))
    word_count = sum(len(text.split()) for text in texts.values())
    if not 300 <= word_count <= 450:
        fail("POSITIVE_WORD_COUNT_INVALID", str(word_count))
    governing = positive["governing_point_id"]
    if governing not in texts:
        fail("GOVERNING_POINT_UNKNOWN", str(governing))

    baseline = exact_keys(
        positive["baseline"],
        {"composition_plan", "ordered_span_ids", "support_groups"},
        "$case/positive_case/baseline",
    )
    candidate = exact_keys(
        positive["candidate"],
        {"composition_plan", "ordered_span_ids", "support_groups"},
        "$case/positive_case/candidate",
    )
    ids = set(texts)
    for name, plan in (("baseline", baseline), ("candidate", candidate)):
        order = plan["ordered_span_ids"]
        if not isinstance(order, list) or len(order) != len(set(order)) or set(order) != ids:
            fail("POSITIVE_ORDER_NOT_EXACT", name)
    if baseline["composition_plan"] != "flat-evidence-led":
        fail("BASELINE_PLAN_INVALID", str(baseline["composition_plan"]))
    if baseline["support_groups"] != []:
        fail("BASELINE_GROUPS_FORBIDDEN", "$case/positive_case/baseline")
    if baseline["ordered_span_ids"].index(governing) == 0:
        fail("BASELINE_GOVERNING_POINT_NOT_DELAYED", governing)
    if candidate["composition_plan"] != "declared-governing-point-support-hierarchy":
        fail("CANDIDATE_PLAN_INVALID", str(candidate["composition_plan"]))
    if candidate["ordered_span_ids"][0] != governing:
        fail("CANDIDATE_GOVERNING_POINT_NOT_FIRST", governing)
    groups = candidate["support_groups"]
    if not isinstance(groups, list) or not 2 <= len(groups) <= 3:
        fail("SUPPORT_GROUP_COUNT_INVALID", str(groups))
    covered: list[str] = []
    group_tuples: list[tuple[str, str | None, list[str]]] = []
    seen_group_ids: set[str] = set()
    for index, raw in enumerate(groups):
        group = exact_keys(raw, {"group_id", "span_ids"}, f"$case/positive_case/candidate/support_groups/{index}")
        group_id = nonempty_string(group["group_id"], "group_id")
        if group_id in seen_group_ids:
            fail("SUPPORT_GROUP_ID_DUPLICATE", group_id)
        seen_group_ids.add(group_id)
        span_ids = group["span_ids"]
        if not isinstance(span_ids, list) or not span_ids:
            fail("SUPPORT_GROUP_EMPTY", group_id)
        covered.extend(span_ids)
        group_tuples.append(("support-group", group_id, span_ids))
    expected_support = [span_id for span_id in candidate["ordered_span_ids"] if span_id != governing]
    if covered != expected_support or len(covered) != len(set(covered)):
        fail("SUPPORT_GROUP_COVERAGE_INVALID", str(covered))

    views = exact_keys(
        positive["review_views"],
        {
            "span_joiner",
            "block_joiner",
            "preserve_span_text_exactly",
            "variant_specific_text_forbidden",
            "baseline",
            "candidate",
        },
        "$case/positive_case/review_views",
    )
    if views["span_joiner"] != " " or views["block_joiner"] != "\n\n":
        fail("RENDER_JOINER_INVALID", "$case/positive_case/review_views")
    if views["preserve_span_text_exactly"] is not True or views["variant_specific_text_forbidden"] is not True:
        fail("RENDER_CONTROL_DISABLED", "$case/positive_case/review_views")
    validate_view(
        views["baseline"],
        "$case/positive_case/review_views/baseline",
        [("flat", None, baseline["ordered_span_ids"])],
        texts,
        " ",
        "\n\n",
    )
    validate_view(
        views["candidate"],
        "$case/positive_case/review_views/candidate",
        [("governing-point", None, [governing]), *group_tuples],
        texts,
        " ",
        "\n\n",
    )

    boundary = exact_keys(
        case["boundary_case"],
        {
            "kind",
            "applicability",
            "candidate_activation",
            "intended_form",
            "failure_if_transformed",
            "spans",
            "ordered_span_ids",
            "review_view",
            "transformation",
        },
        "$case/boundary_case",
    )
    if boundary["kind"] != "discovery-led" or boundary["applicability"] is not False or boundary["candidate_activation"] is not False:
        fail("BOUNDARY_ACTIVATION_INVALID", "$case/boundary_case")
    nonempty_string(boundary["intended_form"], "$case/boundary_case/intended_form")
    nonempty_string(boundary["failure_if_transformed"], "$case/boundary_case/failure_if_transformed")
    if boundary["transformation"] is not None:
        fail("BOUNDARY_TRANSFORMATION_FORBIDDEN", "$case/boundary_case/transformation")
    boundary_texts = span_map(boundary["spans"], "$case/boundary_case/spans", "B")
    if not 3 <= len(boundary_texts) <= 6:
        fail("BOUNDARY_SPAN_COUNT_INVALID", str(len(boundary_texts)))
    boundary_order = boundary["ordered_span_ids"]
    if not isinstance(boundary_order, list) or len(boundary_order) != len(set(boundary_order)) or set(boundary_order) != set(boundary_texts):
        fail("BOUNDARY_ORDER_NOT_EXACT", str(boundary_order))
    validate_view(
        boundary["review_view"],
        "$case/boundary_case/review_view",
        [("flat", None, boundary_order)],
        boundary_texts,
        " ",
        "\n\n",
    )

    claims = exact_keys(
        case["claim_boundary"],
        {"reader_outcome_claims", "integration_authorized", "canonical_change_authorized"},
        "$case/claim_boundary",
    )
    if claims != {
        "reader_outcome_claims": False,
        "integration_authorized": False,
        "canonical_change_authorized": False,
    } or case["authority_effect"] != "none":
        fail("CLAIM_CEILING_INVALID", "$case")
    return {"positive_span_count": len(texts), "word_count": word_count}


def validate_mechanical(case_path: Path, mechanical_path: Path) -> dict[str, Any]:
    case = load(case_path)
    case_result = validate_case(case)
    receipt = load(mechanical_path)
    exact_keys(
        receipt,
        {
            "schema_version",
            "experiment_id",
            "case_ref",
            "checks",
            "failed_check_ids",
            "semantic_equivalence_evaluated",
            "reader_outcome_claims",
            "integration_authorized",
            "status",
            "authority_effect",
        },
        "$mechanical",
    )
    if receipt["schema_version"] != "whisper.minto-pyramid-mechanical-validation.v1" or receipt["experiment_id"] != "minto-pyramid-experiment-001":
        fail("MECHANICAL_IDENTITY_INVALID", "$mechanical")
    exact_ref(receipt["case_ref"], case_path, "$mechanical/case_ref")
    checks = receipt["checks"]
    if not isinstance(checks, list) or len(checks) != len(CASE_CHECK_IDS):
        fail("MECHANICAL_CHECK_COUNT_INVALID", str(checks))
    observed_ids: list[str] = []
    for index, raw in enumerate(checks):
        check = exact_keys(raw, {"check_id", "status", "detail"}, f"$mechanical/checks/{index}")
        observed_ids.append(check["check_id"])
        if check["status"] != "pass":
            fail("MECHANICAL_CHECK_NOT_PASS", str(check["check_id"]))
        nonempty_string(check["detail"], f"$mechanical/checks/{index}/detail")
    if observed_ids != CASE_CHECK_IDS:
        fail("MECHANICAL_CHECK_IDS_INVALID", str(observed_ids))
    if receipt["failed_check_ids"] != [] or receipt["status"] != "pass":
        fail("MECHANICAL_STATUS_INVALID", "$mechanical")
    if receipt["semantic_equivalence_evaluated"] is not False or receipt["reader_outcome_claims"] is not False or receipt["integration_authorized"] is not False or receipt["authority_effect"] != "none":
        fail("MECHANICAL_CLAIM_CEILING_INVALID", "$mechanical")
    return case_result


def packet_view_from_case(view: dict[str, Any]) -> dict[str, Any]:
    return {
        "blocks": [{"text": block["text"]} for block in view["blocks"]],
        "full_text": view["full_text"],
    }


def validate_review(
    case_path: Path,
    mechanical_path: Path,
    commitment_path: Path,
    packet_path: Path,
    response_path: Path,
    witness_path: Path,
) -> dict[str, Any]:
    case = load(case_path)
    validate_mechanical(case_path, mechanical_path)
    mechanical = load(mechanical_path)
    commitment = load(commitment_path)
    packet = load(packet_path)
    response = load(response_path)
    witness = load(witness_path)

    exact_keys(commitment, {"schema_version", "experiment_id", "algorithm", "commitment_input_schema", "commitment", "created_at", "authority_effect"}, "$commitment")
    if commitment["schema_version"] != "whisper.minto-pyramid-blinding-commitment.v1" or commitment["experiment_id"] != "minto-pyramid-experiment-001" or commitment["algorithm"] != "sha256-canonical-json" or commitment["commitment_input_schema"] != "mapping-A-B-to-baseline-candidate-plus-random-nonce" or not isinstance(commitment["commitment"], str) or not HEX_64.fullmatch(commitment["commitment"]) or commitment["authority_effect"] != "none":
        fail("BLINDING_COMMITMENT_INVALID", "$commitment")
    commitment_time = parse_time(commitment["created_at"], "$commitment/created_at")

    exact_keys(packet, {"schema_version", "experiment_id", "case_ref", "mechanical_ref", "commitment_ref", "created_at", "blinding_mode", "review_context", "reviewer_instructions", "variants", "boundary_view", "questions", "claim_boundary", "authority_effect"}, "$packet")
    if packet["schema_version"] != "whisper.minto-pyramid-blinded-review-packet.v1" or packet["experiment_id"] != "minto-pyramid-experiment-001" or packet["blinding_mode"] != "role-label-blind" or packet["authority_effect"] != "none":
        fail("REVIEW_PACKET_IDENTITY_INVALID", "$packet")
    exact_ref(packet["case_ref"], case_path, "$packet/case_ref")
    exact_ref(packet["mechanical_ref"], mechanical_path, "$packet/mechanical_ref")
    exact_ref(packet["commitment_ref"], commitment_path, "$packet/commitment_ref")
    packet_time = parse_time(packet["created_at"], "$packet/created_at")
    if commitment_time > packet_time:
        fail("BLINDING_CHRONOLOGY_INVALID", "commitment after packet")
    expected_review_context = {
        "audience": case["positive_case"]["audience"],
        "purpose": case["positive_case"]["purpose"],
        "transport": case["placement"]["transport"],
        "unit_level": case["placement"]["unit_level"],
        "supported_concept": case["source_binding"]["supported_concept"],
        "unsupported_inferences": case["source_binding"]["unsupported_inferences"],
        "changed_decision": case["decision_contract"]["changed_decision"],
        "prevented_failure": case["decision_contract"]["prevented_failure"],
        "boundary": {
            "kind": case["boundary_case"]["kind"],
            "intended_form": case["boundary_case"]["intended_form"],
            "candidate_activation": case["boundary_case"]["candidate_activation"],
            "failure_if_transformed": case["boundary_case"]["failure_if_transformed"],
        },
        "claim_limits": case["claim_boundary"],
    }
    if packet["review_context"] != expected_review_context:
        fail("REVIEW_CONTEXT_MISMATCH", "$packet/review_context")
    if packet["reviewer_instructions"] != REVIEWER_INSTRUCTIONS:
        fail("REVIEWER_INSTRUCTIONS_MISMATCH", "$packet/reviewer_instructions")
    variants = packet["variants"]
    if not isinstance(variants, list) or len(variants) != 2:
        fail("REVIEW_VARIANTS_INVALID", "$packet/variants")
    packet_views: dict[str, Any] = {}
    for index, raw in enumerate(variants):
        variant = exact_keys(raw, {"label", "view"}, f"$packet/variants/{index}")
        if variant["label"] not in {"A", "B"} or variant["label"] in packet_views:
            fail("REVIEW_VARIANT_LABEL_INVALID", str(variant["label"]))
        exact_keys(variant["view"], {"blocks", "full_text"}, f"$packet/variants/{index}/view")
        if not isinstance(variant["view"]["blocks"], list) or any(set(block) != {"text"} for block in variant["view"]["blocks"] if isinstance(block, dict)) or any(not isinstance(block, dict) for block in variant["view"]["blocks"]):
            fail("REVIEW_PACKET_VIEW_NOT_BLIND", str(variant["label"]))
        packet_views[variant["label"]] = variant["view"]
    exact_keys(packet["boundary_view"], {"blocks", "full_text"}, "$packet/boundary_view")
    if packet["questions"] != QUESTION_RECORDS:
        fail("REVIEW_QUESTIONS_INVALID", "$packet/questions")
    if packet["claim_boundary"] != {"reader_outcome_claims": False, "integration_authorized": False, "canonical_change_authorized": False}:
        fail("REVIEW_PACKET_CLAIM_CEILING_INVALID", "$packet")

    exact_keys(response, {"schema_version", "experiment_id", "packet_ref", "reviewer", "started_at", "completed_at", "mapping_known_before_completion", "judgments", "limitations", "authority_effect"}, "$response")
    if response["schema_version"] != "whisper.minto-pyramid-human-review-response.v1" or response["experiment_id"] != "minto-pyramid-experiment-001" or response["mapping_known_before_completion"] is not False or response["authority_effect"] != "none":
        fail("HUMAN_RESPONSE_IDENTITY_INVALID", "$response")
    exact_ref(response["packet_ref"], packet_path, "$response/packet_ref")
    reviewer = exact_keys(response["reviewer"], {"kind", "reviewer_id", "attestation"}, "$response/reviewer")
    if reviewer["kind"] != "human":
        fail("HUMAN_REVIEW_REQUIRED", "$response/reviewer/kind")
    nonempty_string(reviewer["reviewer_id"], "$response/reviewer/reviewer_id")
    nonempty_string(reviewer["attestation"], "$response/reviewer/attestation")
    started = parse_time(response["started_at"], "$response/started_at")
    completed = parse_time(response["completed_at"], "$response/completed_at")
    if packet_time > started or started > completed:
        fail("REVIEW_CHRONOLOGY_INVALID", "$response")
    if not isinstance(response["limitations"], list) or any(not isinstance(item, str) or not item.strip() for item in response["limitations"]):
        fail("REVIEW_LIMITATIONS_INVALID", "$response/limitations")
    judgments = response["judgments"]
    if not isinstance(judgments, list) or len(judgments) != len(JUDGMENT_IDS):
        fail("HUMAN_JUDGMENT_COUNT_INVALID", "$response/judgments")
    statuses: list[str] = []
    exhibiting_label: str | None = None
    for index, raw in enumerate(judgments):
        expected_id = JUDGMENT_IDS[index]
        keys = {"judgment_id", "status", "rationale"}
        if expected_id == "named-decision-changed":
            keys.add("exhibiting_variant_label")
        judgment = exact_keys(raw, keys, f"$response/judgments/{index}")
        if judgment["judgment_id"] != expected_id or judgment["status"] not in {"pass", "fail", "inconclusive"}:
            fail("HUMAN_JUDGMENT_INVALID", expected_id)
        nonempty_string(judgment["rationale"], f"$response/judgments/{index}/rationale")
        statuses.append(judgment["status"])
        if expected_id == "named-decision-changed":
            exhibiting_label = judgment["exhibiting_variant_label"]
            if exhibiting_label not in {"A", "B", "none"}:
                fail("EXHIBITING_LABEL_INVALID", str(exhibiting_label))

    exact_keys(witness, {"schema_version", "experiment_id", "case_ref", "mechanical_ref", "commitment_ref", "packet_ref", "response_ref", "blinding_reveal", "non_vacuity_verdict", "limitations", "reader_outcome_claims", "integration_authorized", "canonical_change_authorized", "authority_effect"}, "$witness")
    if witness["schema_version"] != "whisper.minto-pyramid-human-review-witness.v1" or witness["experiment_id"] != "minto-pyramid-experiment-001":
        fail("WITNESS_IDENTITY_INVALID", "$witness")
    exact_ref(witness["case_ref"], case_path, "$witness/case_ref")
    exact_ref(witness["mechanical_ref"], mechanical_path, "$witness/mechanical_ref")
    exact_ref(witness["commitment_ref"], commitment_path, "$witness/commitment_ref")
    exact_ref(witness["packet_ref"], packet_path, "$witness/packet_ref")
    exact_ref(witness["response_ref"], response_path, "$witness/response_ref")
    reveal = exact_keys(witness["blinding_reveal"], {"mapping", "nonce", "mapping_revealed_at", "commitment_matches"}, "$witness/blinding_reveal")
    mapping = exact_keys(reveal["mapping"], {"A", "B"}, "$witness/blinding_reveal/mapping")
    if set(mapping.values()) != {"baseline", "candidate"}:
        fail("BLINDING_MAPPING_INVALID", str(mapping))
    nonce = reveal["nonce"]
    if not isinstance(nonce, str) or not NONCE.fullmatch(nonce):
        fail("BLINDING_NONCE_INVALID", str(nonce))
    if canonical_digest({"mapping": mapping, "nonce": nonce}) != commitment["commitment"] or reveal["commitment_matches"] is not True:
        fail("BLINDING_COMMITMENT_MISMATCH", "$witness/blinding_reveal")
    revealed = parse_time(reveal["mapping_revealed_at"], "$witness/blinding_reveal/mapping_revealed_at")
    if completed >= revealed:
        fail("BLINDING_REVEALED_TOO_EARLY", "$witness/blinding_reveal")
    case_views = case["positive_case"]["review_views"]
    for label, role in mapping.items():
        if packet_views[label] != packet_view_from_case(case_views[role]):
            fail("BLINDED_VIEW_DRIFT", label)
    if packet["boundary_view"] != packet_view_from_case(case["boundary_case"]["review_view"]):
        fail("BOUNDARY_VIEW_DRIFT", "$packet/boundary_view")
    expected_verdict = (
        "pass"
        if all(status == "pass" for status in statuses)
        and exhibiting_label in {"A", "B"}
        and mapping[exhibiting_label] == "candidate"
        else "fail"
        if any(status == "fail" for status in statuses)
        else "inconclusive"
    )
    if witness["non_vacuity_verdict"] != expected_verdict:
        fail("WITNESS_VERDICT_MISMATCH", f"expected={expected_verdict}")
    if not isinstance(witness["limitations"], list) or any(not isinstance(item, str) or not item.strip() for item in witness["limitations"]):
        fail("WITNESS_LIMITATIONS_INVALID", "$witness/limitations")
    if witness["reader_outcome_claims"] is not False or witness["integration_authorized"] is not False or witness["canonical_change_authorized"] is not False or witness["authority_effect"] != "none":
        fail("WITNESS_CLAIM_CEILING_INVALID", "$witness")
    if mechanical["status"] != "pass":
        fail("MECHANICAL_PREDECESSOR_NOT_PASS", "$mechanical/status")
    return {"verdict": expected_verdict, "reviewer_kind": "human"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="mode", required=True)
    case_parser = subparsers.add_parser("case")
    case_parser.add_argument("--case", required=True, type=Path)
    mechanical_parser = subparsers.add_parser("mechanics")
    mechanical_parser.add_argument("--case", required=True, type=Path)
    mechanical_parser.add_argument("--mechanical", required=True, type=Path)
    review_parser = subparsers.add_parser("review")
    review_parser.add_argument("--case", required=True, type=Path)
    review_parser.add_argument("--mechanical", required=True, type=Path)
    review_parser.add_argument("--commitment", required=True, type=Path)
    review_parser.add_argument("--packet", required=True, type=Path)
    review_parser.add_argument("--response", required=True, type=Path)
    review_parser.add_argument("--witness", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.mode == "case":
            result = validate_case(load(args.case))
        elif args.mode == "mechanics":
            result = validate_mechanical(args.case, args.mechanical)
        else:
            result = validate_review(
                args.case,
                args.mechanical,
                args.commitment,
                args.packet,
                args.response,
                args.witness,
            )
    except ValidationFailure as error:
        print(str(error), file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "status": "pass",
                "mode": args.mode,
                "result": result,
                "configured_files_written": False,
                "semantic_equivalence_evaluated": False,
                "reader_outcome_claims": False,
                "authority_effect": "none",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
