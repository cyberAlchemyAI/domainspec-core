"""Local, deterministic chapter-factory workflow.

The factory binds exact repository sources, imports or prepares one manuscript,
runs mechanical checks, and emits an author-review packet.  It never accepts
prose, calls a model/provider, resolves secrets, or publishes an artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .canonical import canonical_identity


CONFIG_SCHEMA = "lucifers-lights.chapter-factory-config/1.0.0"
RECEIPT_SCHEMA = "lucifers-lights.chapter-factory-receipt/1.0.0"
AUTHOR_DECISION_SCHEMA = "lucifers-lights.author-decision/1.0.0"
MANAGED_OUTPUTS = (
    "context-manifest.json",
    "chapter-run.json",
    "chapter-brief.md",
    "deterministic-review.json",
    "editorial-review.md",
    "factory-status.json",
    "decision-request.md",
    "chapter-review.html",
)
VOICE_HANDOFF_OUTPUT = "voice-handoff.json"
FORBIDDEN_SOURCE_COMPONENTS = frozenset(
    {".env", ".secrets", "secrets", "credential", "credentials"}
)


class FactoryError(ValueError):
    """Stable failure raised before unsafe or ambiguous factory work."""


@dataclass(frozen=True, slots=True)
class SourceBinding:
    source_id: str
    role: str
    path: str
    sha256: str
    size_bytes: int

    def to_document(self) -> dict[str, object]:
        return {
            "id": self.source_id,
            "path": self.path,
            "role": self.role,
            "sha256": self.sha256,
            "size_bytes": self.size_bytes,
        }


@dataclass(frozen=True, slots=True)
class AuthorDecision:
    source: SourceBinding
    decision_id: str
    selected_option_id: str
    decided_at: str
    revision_number: int
    prior_digest: str


@dataclass(frozen=True, slots=True)
class CheckResult:
    check_id: str
    status: str
    evidence: str

    def to_document(self) -> dict[str, str]:
        return {
            "check_id": self.check_id,
            "evidence": self.evidence,
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class Paragraph:
    text: str
    source_line: int


def _canonical_json(document: object) -> str:
    return json.dumps(
        document,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        allow_nan=False,
    ) + "\n"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _closed_mapping(
    value: object,
    label: str,
    required: Iterable[str],
    optional: Iterable[str] = (),
) -> dict[str, object]:
    if not isinstance(value, dict):
        raise FactoryError(f"{label} must be an object")
    required_set = set(required)
    allowed = required_set | set(optional)
    missing = sorted(required_set - set(value))
    unknown = sorted(set(value) - allowed)
    if missing:
        raise FactoryError(f"{label} missing fields: {', '.join(missing)}")
    if unknown:
        raise FactoryError(f"{label} has unknown fields: {', '.join(unknown)}")
    return value


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value or value.strip() != value:
        raise FactoryError(f"{label} must be a non-empty trimmed string")
    return value


def _string_list(value: object, label: str) -> list[str]:
    if not isinstance(value, list):
        raise FactoryError(f"{label} must be an array")
    result = [_text(item, f"{label}[{index}]") for index, item in enumerate(value)]
    if len(result) != len(set(result)):
        raise FactoryError(f"{label} contains duplicate values")
    return result


def _integer(value: object, label: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise FactoryError(f"{label} must be an integer >= {minimum}")
    return value


def _repo_path(repo_root: Path, raw: object, label: str) -> tuple[str, Path]:
    relative = Path(_text(raw, label))
    if relative.is_absolute():
        raise FactoryError(f"{label} must be repository-relative")
    if any(part.lower() in FORBIDDEN_SOURCE_COMPONENTS for part in relative.parts):
        raise FactoryError(f"{label} targets a forbidden secret/credential surface")
    resolved = (repo_root / relative).resolve()
    try:
        normalized = resolved.relative_to(repo_root).as_posix()
    except ValueError as error:
        raise FactoryError(f"{label} escapes the repository root") from error
    return normalized, resolved


def load_config(config_path: Path) -> dict[str, object]:
    try:
        document = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise FactoryError(f"cannot read factory config: {error}") from error
    root = _closed_mapping(
        document,
        "config",
        (
            "schema_version",
            "project_id",
            "chapter",
            "run",
            "sources",
            "brief",
            "review",
            "review_template",
        ),
        ("author_decision", "voice"),
    )
    if root["schema_version"] != CONFIG_SCHEMA:
        raise FactoryError(f"unsupported config schema: {root['schema_version']!r}")
    _text(root["project_id"], "config.project_id")
    _validate_chapter(root["chapter"])
    _validate_run(root["run"])
    _validate_sources(root["sources"])
    _validate_brief(root["brief"])
    _validate_review(root["review"])
    _text(root["review_template"], "config.review_template")
    if "author_decision" in root:
        _validate_author_decision(root["author_decision"], root["sources"])
    if "voice" in root:
        _validate_voice(root["voice"], root["sources"])
        voice = root["voice"]
        assert isinstance(voice, dict)
        if (
            voice["derivative_status"] == "local-compile-ready"
            and "author_decision" not in root
        ):
            raise FactoryError(
                "config.voice cannot be local-compile-ready without an author decision"
            )
    return root


def _validate_chapter(value: object) -> None:
    chapter = _closed_mapping(
        value,
        "config.chapter",
        ("id", "number", "slug", "title", "manuscript_source_id", "expected_sha256"),
    )
    _text(chapter["id"], "config.chapter.id")
    _integer(chapter["number"], "config.chapter.number", minimum=1)
    _text(chapter["slug"], "config.chapter.slug")
    _text(chapter["title"], "config.chapter.title")
    _text(chapter["manuscript_source_id"], "config.chapter.manuscript_source_id")
    expected = _text(chapter["expected_sha256"], "config.chapter.expected_sha256")
    if not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise FactoryError("config.chapter.expected_sha256 must be lowercase SHA-256")


def _validate_run(value: object) -> None:
    run = _closed_mapping(value, "config.run", ("id", "mode"))
    _text(run["id"], "config.run.id")
    if run["mode"] not in {"review_existing", "draft_candidate"}:
        raise FactoryError(f"unsupported factory mode: {run['mode']!r}")


def _validate_sources(value: object) -> None:
    if not isinstance(value, list) or not value:
        raise FactoryError("config.sources must be a non-empty array")
    ids: list[str] = []
    paths: list[str] = []
    for index, candidate in enumerate(value):
        source = _closed_mapping(
            candidate,
            f"config.sources[{index}]",
            ("id", "role", "path"),
        )
        ids.append(_text(source["id"], f"config.sources[{index}].id"))
        _text(source["role"], f"config.sources[{index}].role")
        paths.append(_text(source["path"], f"config.sources[{index}].path"))
    if len(ids) != len(set(ids)):
        raise FactoryError("config.sources contains duplicate ids")
    if len(paths) != len(set(paths)):
        raise FactoryError("config.sources contains duplicate paths")


def _validate_author_decision(value: object, sources_value: object) -> None:
    decision = _closed_mapping(
        value,
        "config.author_decision",
        ("source_id",),
    )
    source_id = _text(
        decision["source_id"], "config.author_decision.source_id"
    )
    assert isinstance(sources_value, list)
    matching = [
        item
        for item in sources_value
        if isinstance(item, dict) and item.get("id") == source_id
    ]
    if not matching:
        raise FactoryError(
            f"config.author_decision references undeclared source id: {source_id}"
        )
    if matching[0].get("role") != "author-decision-receipt":
        raise FactoryError(
            "config.author_decision source role must be author-decision-receipt"
        )


def _validate_voice(value: object, sources_value: object) -> None:
    voice = _closed_mapping(
        value,
        "config.voice",
        (
            "source_id",
            "compiler_config_source_id",
            "sync_disposition_source_id",
            "derivative_profile",
            "derivative_status",
        ),
    )
    source_id = _text(voice["source_id"], "config.voice.source_id")
    config_id = _text(
        voice["compiler_config_source_id"],
        "config.voice.compiler_config_source_id",
    )
    sync_id = _text(
        voice["sync_disposition_source_id"],
        "config.voice.sync_disposition_source_id",
    )
    if len({source_id, config_id, sync_id}) != 3:
        raise FactoryError("config.voice source ids must be distinct")
    if voice["derivative_profile"] != "motion-comic-voiceover":
        raise FactoryError("unsupported config.voice derivative profile")
    if voice["derivative_status"] not in {
        "needs-post-revision-sync",
        "local-compile-ready",
    }:
        raise FactoryError("unsupported config.voice derivative status")
    assert isinstance(sources_value, list)
    declared_ids = {
        str(item["id"])
        for item in sources_value
        if isinstance(item, dict) and "id" in item
    }
    missing = sorted({source_id, config_id, sync_id} - declared_ids)
    if missing:
        raise FactoryError(
            f"config.voice references undeclared source ids: {', '.join(missing)}"
        )


def _validate_brief(value: object) -> None:
    brief = _closed_mapping(
        value,
        "config.brief",
        ("objective", "candidate_id", "scene_engine", "preserve", "open_questions"),
    )
    _text(brief["objective"], "config.brief.objective")
    _text(brief["candidate_id"], "config.brief.candidate_id")
    for field in ("scene_engine", "preserve", "open_questions"):
        _string_list(brief[field], f"config.brief.{field}")


def _validate_review(value: object) -> None:
    review = _closed_mapping(
        value,
        "config.review",
        (
            "word_count",
            "required_markers",
            "forbidden_markers",
            "clock",
            "manual_gates",
            "part_boundaries",
            "editorial_notes",
        ),
    )
    word_count = _closed_mapping(
        review["word_count"],
        "config.review.word_count",
        ("minimum", "maximum"),
    )
    minimum = _integer(word_count["minimum"], "config.review.word_count.minimum")
    maximum = _integer(word_count["maximum"], "config.review.word_count.maximum")
    if maximum < minimum:
        raise FactoryError("config.review.word_count maximum is below minimum")
    for field in ("required_markers", "forbidden_markers", "manual_gates"):
        _string_list(review[field], f"config.review.{field}")
    _validate_clock(review["clock"])
    _validate_part_boundaries(review["part_boundaries"])
    notes = _closed_mapping(
        review["editorial_notes"],
        "config.review.editorial_notes",
        ("status", "strengths", "watch_items", "recommendation"),
    )
    if notes["status"] not in {"ready_for_author_review", "revision_recommended"}:
        raise FactoryError("unsupported editorial note status")
    _string_list(notes["strengths"], "config.review.editorial_notes.strengths")
    _string_list(notes["watch_items"], "config.review.editorial_notes.watch_items")
    _text(notes["recommendation"], "config.review.editorial_notes.recommendation")


def _validate_clock(value: object) -> None:
    clock = _closed_mapping(value, "config.review.clock", ("deadline", "events"))
    _clock_minutes(_text(clock["deadline"], "config.review.clock.deadline"))
    events = clock["events"]
    if not isinstance(events, list) or not events:
        raise FactoryError("config.review.clock.events must be a non-empty array")
    ids: list[str] = []
    for index, candidate in enumerate(events):
        event = _closed_mapping(
            candidate,
            f"config.review.clock.events[{index}]",
            ("id", "time", "expected_remaining_minutes", "time_marker", "remaining_marker"),
        )
        ids.append(_text(event["id"], f"config.review.clock.events[{index}].id"))
        _clock_minutes(_text(event["time"], f"config.review.clock.events[{index}].time"))
        _integer(
            event["expected_remaining_minutes"],
            f"config.review.clock.events[{index}].expected_remaining_minutes",
        )
        _text(event["time_marker"], f"config.review.clock.events[{index}].time_marker")
        _text(
            event["remaining_marker"],
            f"config.review.clock.events[{index}].remaining_marker",
        )
    if len(ids) != len(set(ids)):
        raise FactoryError("config.review.clock.events contains duplicate ids")


def _validate_part_boundaries(value: object) -> None:
    if not isinstance(value, list) or not value:
        raise FactoryError("config.review.part_boundaries must be a non-empty array")
    ids: list[str] = []
    for index, candidate in enumerate(value):
        boundary = _closed_mapping(
            candidate,
            f"config.review.part_boundaries[{index}]",
            ("part_id", "start_text"),
        )
        ids.append(
            _text(boundary["part_id"], f"config.review.part_boundaries[{index}].part_id")
        )
        _text(boundary["start_text"], f"config.review.part_boundaries[{index}].start_text")
    if len(ids) != len(set(ids)):
        raise FactoryError("config.review.part_boundaries contains duplicate part ids")


def _clock_minutes(value: str) -> int:
    match = re.fullmatch(r"([0-1][0-9]|2[0-3]):([0-5][0-9])", value)
    if match is None:
        raise FactoryError(f"invalid 24-hour clock value: {value!r}")
    return int(match.group(1)) * 60 + int(match.group(2))


def bind_sources(config: dict[str, object], repo_root: Path) -> list[SourceBinding]:
    bindings: list[SourceBinding] = []
    for index, source_value in enumerate(config["sources"]):
        assert isinstance(source_value, dict)
        relative, path = _repo_path(
            repo_root,
            source_value["path"],
            f"config.sources[{index}].path",
        )
        if not path.is_file():
            raise FactoryError(f"required source is not a file: {relative}")
        bindings.append(
            SourceBinding(
                source_id=str(source_value["id"]),
                role=str(source_value["role"]),
                path=relative,
                sha256=_sha256(path),
                size_bytes=path.stat().st_size,
            )
        )
    chapter = config["chapter"]
    assert isinstance(chapter, dict)
    manuscript_id = str(chapter["manuscript_source_id"])
    manuscript = next((item for item in bindings if item.source_id == manuscript_id), None)
    if manuscript is None:
        raise FactoryError(f"manuscript source id is not declared: {manuscript_id}")
    if manuscript.sha256 != chapter["expected_sha256"]:
        raise FactoryError(
            "manuscript digest drift: "
            f"expected {chapter['expected_sha256']}, observed {manuscript.sha256}"
        )
    return bindings


def _sha256_text(value: object, label: str) -> str:
    digest = _text(value, label)
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise FactoryError(f"{label} must be lowercase SHA-256")
    return digest


def _validate_evidence_binding(
    value: object,
    label: str,
    repo_root: Path,
) -> tuple[str, Path]:
    binding = _closed_mapping(value, label, ("path", "sha256"))
    relative, path = _repo_path(repo_root, binding["path"], f"{label}.path")
    if not path.is_file():
        raise FactoryError(f"{label} is not a file: {relative}")
    expected = _sha256_text(binding["sha256"], f"{label}.sha256")
    observed = _sha256(path)
    if observed != expected:
        raise FactoryError(
            f"{label} digest drift: expected {expected}, observed {observed}"
        )
    return relative, path


def load_author_decision(
    config: dict[str, object],
    bindings: list[SourceBinding],
    repo_root: Path,
    manuscript: SourceBinding,
) -> AuthorDecision | None:
    decision_config = config.get("author_decision")
    if decision_config is None:
        return None
    assert isinstance(decision_config, dict)
    source_id = str(decision_config["source_id"])
    source = next((item for item in bindings if item.source_id == source_id), None)
    if source is None:
        raise FactoryError(f"author decision source binding is missing: {source_id}")
    if source.role != "author-decision-receipt":
        raise FactoryError("author decision source role must be author-decision-receipt")

    try:
        document = json.loads((repo_root / source.path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise FactoryError(f"cannot read author decision receipt: {error}") from error
    root = _closed_mapping(
        document,
        "author decision receipt",
        (
            "schema_version",
            "decision_id",
            "selected_option_id",
            "decision_state",
            "decided_at",
            "project_id",
            "chapter_id",
            "run_id",
            "manuscript",
            "revision",
            "authority",
            "decision_record",
            "admissibility_receipt",
        ),
    )
    if root["schema_version"] != AUTHOR_DECISION_SCHEMA:
        raise FactoryError("unsupported author decision receipt schema")
    decision_id = _text(root["decision_id"], "author decision receipt.decision_id")
    selected_option_id = _text(
        root["selected_option_id"],
        "author decision receipt.selected_option_id",
    )
    if root["decision_state"] != "accepted":
        raise FactoryError("author decision receipt state must be accepted")
    decided_at = _text(root["decided_at"], "author decision receipt.decided_at")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", decided_at) is None:
        raise FactoryError("author decision receipt.decided_at must be UTC seconds")

    chapter = config["chapter"]
    run = config["run"]
    assert isinstance(chapter, dict)
    assert isinstance(run, dict)
    expected_identity = {
        "project_id": config["project_id"],
        "chapter_id": chapter["id"],
        "run_id": run["id"],
    }
    for field, expected in expected_identity.items():
        observed = _text(root[field], f"author decision receipt.{field}")
        if observed != expected:
            raise FactoryError(
                f"author decision receipt {field} does not match factory config"
            )

    manuscript_value = _closed_mapping(
        root["manuscript"],
        "author decision receipt.manuscript",
        ("path", "sha256"),
    )
    if manuscript_value["path"] != manuscript.path:
        raise FactoryError("author decision manuscript path does not match binding")
    if manuscript_value["sha256"] != manuscript.sha256:
        raise FactoryError("author decision manuscript digest does not match binding")

    revision = _closed_mapping(
        root["revision"],
        "author decision receipt.revision",
        ("number", "prior_digest"),
    )
    revision_number = _integer(
        revision["number"], "author decision receipt.revision.number", minimum=1
    )
    prior_digest = _sha256_text(
        revision["prior_digest"], "author decision receipt.revision.prior_digest"
    )
    if prior_digest == manuscript.sha256:
        raise FactoryError("author decision prior digest must differ from accepted digest")

    authority = _closed_mapping(
        root["authority"],
        "author decision receipt.authority",
        ("owner", "scope", "external_effects_authorized"),
    )
    if authority["owner"] != "author":
        raise FactoryError("author decision owner must be author")
    if authority["scope"] != "exact-manuscript-baseline":
        raise FactoryError("author decision scope must be exact-manuscript-baseline")
    if authority["external_effects_authorized"] is not False:
        raise FactoryError("author decision cannot authorize external effects")

    _, record_path = _validate_evidence_binding(
        root["decision_record"], "author decision receipt.decision_record", repo_root
    )
    _, admissibility_path = _validate_evidence_binding(
        root["admissibility_receipt"],
        "author decision receipt.admissibility_receipt",
        repo_root,
    )
    record_text = record_path.read_text(encoding="utf-8")
    for marker in (
        f"Decision ID: `{decision_id}`",
        "Status: `PASS`",
        f"Selected option: `{selected_option_id}`",
        f"Candidate SHA-256: `{manuscript.sha256}`",
    ):
        if marker not in record_text:
            raise FactoryError(
                f"author decision record is missing required marker: {marker}"
            )
    try:
        admissibility = json.loads(admissibility_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise FactoryError(f"cannot read option admissibility receipt: {error}") from error
    if not isinstance(admissibility, dict):
        raise FactoryError("option admissibility receipt must be an object")
    if admissibility.get("decisionId") != decision_id:
        raise FactoryError("option admissibility decision id does not match")
    if admissibility.get("routeOutcome") != "gate":
        raise FactoryError("option admissibility route must be gate")
    option_ids = admissibility.get("admissibleOptionIds")
    if not isinstance(option_ids, list) or selected_option_id not in option_ids:
        raise FactoryError("selected author option was not admissible")

    return AuthorDecision(
        source=source,
        decision_id=decision_id,
        selected_option_id=selected_option_id,
        decided_at=decided_at,
        revision_number=revision_number,
        prior_digest=prior_digest,
    )


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", text, flags=re.UNICODE))


def evaluate_manuscript(
    manuscript_text: str,
    manuscript_digest: str,
    config: dict[str, object],
) -> tuple[list[CheckResult], dict[str, int]]:
    chapter = config["chapter"]
    review = config["review"]
    assert isinstance(chapter, dict)
    assert isinstance(review, dict)
    results: list[CheckResult] = []

    lines = manuscript_text.splitlines()
    words = _word_count(manuscript_text)
    expected_title = f"# {chapter['title']}"
    actual_title = lines[0] if lines else ""
    results.append(
        CheckResult(
            "title",
            "pass" if actual_title == expected_title else "fail",
            f"expected {expected_title!r}; observed {actual_title!r}",
        )
    )
    results.append(
        CheckResult(
            "manuscript_digest",
            "pass" if manuscript_digest == chapter["expected_sha256"] else "fail",
            manuscript_digest,
        )
    )

    word_rule = review["word_count"]
    assert isinstance(word_rule, dict)
    minimum = int(word_rule["minimum"])
    maximum = int(word_rule["maximum"])
    results.append(
        CheckResult(
            "word_count",
            "pass" if minimum <= words <= maximum else "fail",
            f"observed {words}; allowed {minimum}..{maximum}",
        )
    )

    for index, marker in enumerate(review["required_markers"]):
        marker = str(marker)
        results.append(
            CheckResult(
                f"required_marker_{index + 1:02d}",
                "pass" if marker in manuscript_text else "fail",
                f"required marker {'present' if marker in manuscript_text else 'missing'}: {marker}",
            )
        )
    for index, marker in enumerate(review["forbidden_markers"]):
        marker = str(marker)
        present = marker.casefold() in manuscript_text.casefold()
        results.append(
            CheckResult(
                f"forbidden_marker_{index + 1:02d}",
                "fail" if present else "pass",
                f"forbidden authoring marker {'present' if present else 'absent'}: {marker}",
            )
        )

    clock = review["clock"]
    assert isinstance(clock, dict)
    deadline = _clock_minutes(str(clock["deadline"]))
    for event_value in clock["events"]:
        assert isinstance(event_value, dict)
        event_time = _clock_minutes(str(event_value["time"]))
        remaining = deadline - event_time
        if remaining < 0:
            remaining += 24 * 60
        expected = int(event_value["expected_remaining_minutes"])
        time_marker = str(event_value["time_marker"])
        remaining_marker = str(event_value["remaining_marker"])
        marker_pass = time_marker in manuscript_text and remaining_marker in manuscript_text
        arithmetic_pass = remaining == expected
        results.append(
            CheckResult(
                f"clock_{event_value['id']}",
                "pass" if marker_pass and arithmetic_pass else "fail",
                (
                    f"{event_value['time']} -> {clock['deadline']} = {remaining} minutes; "
                    f"expected {expected}; markers {'present' if marker_pass else 'missing'}"
                ),
            )
        )

    return results, {"line_count": len(lines), "word_count": words}


def build_chapter_run(
    config: dict[str, object],
    bindings: list[SourceBinding],
    manuscript: SourceBinding,
    metrics: dict[str, int],
    decision: AuthorDecision | None,
) -> dict[str, object]:
    chapter = config["chapter"]
    run = config["run"]
    assert isinstance(chapter, dict)
    assert isinstance(run, dict)
    accepted = decision is not None
    tags = [
        "author-accepted" if accepted else "author-gate-pending",
        "factory-pilot",
        "production-unbound",
    ]
    voice = config.get("voice")
    derivative_profiles: list[str] = []
    derivatives: dict[str, object] = {}
    if isinstance(voice, dict):
        derivative_profiles.append("motion_comic")
        voice_source = next(
            item
            for item in bindings
            if item.source_id == str(voice["source_id"])
        )
        derivative_state = (
            "eligible"
            if accepted and voice["derivative_status"] == "local-compile-ready"
            else "stale"
        )
        derivative_inputs = [str(chapter["manuscript_source_id"])]
        if decision is not None:
            derivative_inputs.append(decision.source.source_id)
        derivative_inputs.append(str(voice["sync_disposition_source_id"]))
        derivative_inputs.sort()
        derivatives["motion-comic-voiceover"] = {
            "id": "motion-comic-voiceover",
            "kind": "performance-script",
            "inputs": derivative_inputs,
            "state": derivative_state,
            "binding": {
                "source_id": voice_source.source_id,
                "source_digest": voice_source.sha256,
            },
            "adaptation_ref": str(voice["compiler_config_source_id"]),
        }
    return {
        "schema": {"id": "lucifers-lights.chapter-run", "version": "1.0.0"},
        "identity": {
            "project_id": config["project_id"],
            "chapter_id": chapter["id"],
            "run_id": run["id"],
        },
        "revision": {
            "number": decision.revision_number if decision is not None else 0,
            "prior_digest": decision.prior_digest if decision is not None else None,
        },
        "run_phase": "baseline_ready" if accepted else "author_review",
        "context_snapshot": {
            "source": {
                "kind": "repository",
                "locator": manuscript.path,
                "sha256": manuscript.sha256,
                "size_bytes": manuscript.size_bytes,
                "owner": "author",
                "status": "accepted" if accepted else "review_pending",
            },
            "production": {
                "production_id": "production-unbound",
                "status": "unbound",
            },
            "counts": {
                "line_count": metrics["line_count"],
                "speaker_count": 0,
                "tag_count": len(tags),
            },
            "speakers": [],
            "tags": tags,
        },
        "manuscript": {
            "locator": manuscript.path,
            "sha256": manuscript.sha256,
            "decision_state": "accepted" if accepted else "review_pending",
            "decision_receipt_ref": (
                decision.source.path if decision is not None else None
            ),
        },
        "derivative_profiles": derivative_profiles,
        "derivatives": derivatives,
        "effects": {},
        "receipts": (
            [
                {
                    "id": decision.decision_id,
                    "sha256": decision.source.sha256,
                }
            ]
            if decision is not None
            else []
        ),
        "residue_ref": None,
        "terminal_outcome": None,
    }


def _markdown_list(items: Iterable[object]) -> str:
    return "\n".join(f"- {item}" for item in items)


def build_brief(
    config: dict[str, object],
    bindings: list[SourceBinding],
    decision: AuthorDecision | None,
) -> str:
    chapter = config["chapter"]
    brief = config["brief"]
    assert isinstance(chapter, dict)
    assert isinstance(brief, dict)
    source_rows = "\n".join(
        f"| `{item.source_id}` | `{item.role}` | `{item.path}` | `{item.sha256}` |"
        for item in bindings
    )
    status = "accepted-pilot-baseline" if decision is not None else "review-pending-pilot"
    boundary = (
        "The manuscript acceptance is author-owned and bound to the exact decision "
        "receipt listed above. This packet projects that decision but cannot extend "
        "it into provider calls, media generation, publication, commit, or push."
        if decision is not None
        else (
            "The manuscript remains author-owned. This packet may prepare, review, "
            "and propose corrections, but it cannot accept prose, promote canon, "
            "authorize derivatives, resolve secrets, call providers, publish, "
            "commit, or push."
        )
    )
    return f"""# Chapter Factory Brief — {chapter['title']}

Status: `{status}`

## Objective

{brief['objective']}

## Chapter engine

{_markdown_list(brief['scene_engine'])}

## Preserve

{_markdown_list(brief['preserve'])}

## Open questions

{_markdown_list(brief['open_questions'])}

## Exact sources

| ID | Role | Path | SHA-256 |
|---|---|---|---|
{source_rows}

## Factory boundary

{boundary}
"""


def build_editorial_review(
    config: dict[str, object],
    results: list[CheckResult],
    metrics: dict[str, int],
    manuscript: SourceBinding,
    decision: AuthorDecision | None,
) -> str:
    chapter = config["chapter"]
    review = config["review"]
    assert isinstance(chapter, dict)
    assert isinstance(review, dict)
    notes = review["editorial_notes"]
    assert isinstance(notes, dict)
    check_rows = "\n".join(
        f"| `{item.check_id}` | `{item.status}` | {item.evidence} |" for item in results
    )
    human_gate = "approved" if decision is not None else "pending"
    closing = (
        "The exact manuscript digest above is author-accepted through the bound "
        "decision receipt. This review does not authorize external effects."
        if decision is not None
        else (
            "This review is preparation evidence only. It does not accept Chapter 1 "
            "or mutate the canonical manuscript."
        )
    )
    return f"""# Factory Editorial Review — {chapter['title']}

- Status: `{notes['status']}`
- Human gate: `{human_gate}`
- Manuscript: `{manuscript.path}`
- SHA-256: `{manuscript.sha256}`
- Size: `{manuscript.size_bytes}` bytes; {metrics['line_count']} lines; {metrics['word_count']} words

## Outcome

{notes['recommendation']}

## Strengths preserved

{_markdown_list(notes['strengths'])}

## Watch during the author read

{_markdown_list(notes['watch_items'])}

## Deterministic checks

| Check | Status | Evidence |
|---|---|---|
{check_rows}

## Manual gates

{_markdown_list(review['manual_gates'])}

{closing}
"""


def build_decision_request(
    config: dict[str, object],
    manuscript: SourceBinding,
    review_status: str,
    decision: AuthorDecision | None,
) -> str:
    chapter = config["chapter"]
    assert isinstance(chapter, dict)
    if decision is not None:
        return f"""# Chapter 1 Author Decision

Factory review status: `{review_status}`

The author accepted the exact manuscript baseline:

- SHA-256: `{manuscript.sha256}`
- Size: `{manuscript.size_bytes}` bytes
- Decision ID: `{decision.decision_id}`
- Selected option: `{decision.selected_option_id}`
- Decided at: `{decision.decided_at}`
- Receipt: `{decision.source.path}`

This decision applies only to the exact manuscript digest above. It does not
authorize voice-provider calls, media generation, publication, deployment,
commit, or push.
"""
    return f"""# Chapter 1 Author Decision Request

Factory review status: `{review_status}`

Please read the exact manuscript at `{manuscript.path}` bound to:

- SHA-256: `{manuscript.sha256}`
- Size: `{manuscript.size_bytes}` bytes

Choose one:

1. **Accept exact candidate** — accept only the digest above as the Chapter 1
   manuscript baseline.
2. **Request corrections** — identify paragraph block IDs/comments in
   `chapter-review.html`; a new revision candidate will be created separately.

No response is inferred. Silence, a successful test, or an empty comment payload
does not count as acceptance.
"""


def _parse_markdown(path: Path) -> tuple[str, list[Paragraph]]:
    title = path.stem
    paragraphs: list[Paragraph] = []
    current: list[str] = []
    start_line = 1
    in_code = False

    def flush() -> None:
        nonlocal current
        if current:
            paragraphs.append(Paragraph(" ".join(current).strip(), start_line))
            current = []

    for line_number, raw in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw.strip()
        if line.startswith("```"):
            flush()
            in_code = not in_code
            continue
        if in_code:
            continue
        if not line:
            flush()
            continue
        if line.startswith("# "):
            flush()
            title = line[2:].strip()
            continue
        if line.startswith("#"):
            flush()
            continue
        if not current:
            start_line = line_number
        current.append(line)
    flush()
    return title, paragraphs


def _inline_markdown(value: str) -> str:
    escaped = html.escape(value)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    return escaped


def _review_blocks(
    paragraphs: list[Paragraph], boundaries: object
) -> tuple[str, list[dict[str, object]]]:
    assert isinstance(boundaries, list)
    normalized = [(str(item["part_id"]), str(item["start_text"])) for item in boundaries]
    current_part = normalized[0][0]
    article: list[str] = []
    blocks: list[dict[str, object]] = []
    for index, paragraph in enumerate(paragraphs, start=1):
        for part_id, start_text in normalized:
            if paragraph.text.startswith(start_text):
                current_part = part_id
        block_id = f"p{index:03d}"
        blocks.append(
            {
                "block_id": block_id,
                "paragraph_index": index,
                "part_id": current_part,
                "role": "novel_scene",
                "source_line": paragraph.source_line,
                "text": paragraph.text,
            }
        )
        article.append(
            "\n".join(
                (
                    f'<section class="review-block" data-review-block data-block-id="{block_id}" '
                    f'data-part-id="{html.escape(current_part)}" tabindex="0">',
                    '  <div class="block-meta">',
                    f'    <span class="block-id">{block_id}</span>',
                    f'    <span class="part-id">{html.escape(current_part)}</span>',
                    f"    <span>line {paragraph.source_line}</span>",
                    "  </div>",
                    '  <div class="block-body">',
                    f"    <p>{_inline_markdown(paragraph.text)}</p>",
                    '    <div class="block-actions">',
                    '      <button type="button" data-add-comment>Comment</button>',
                    f'      <span class="comment-count" data-comment-count="{block_id}">0</span>',
                    "    </div>",
                    "  </div>",
                    "</section>",
                )
            )
        )
    return "\n".join(article), blocks


def build_review_html(
    config: dict[str, object],
    repo_root: Path,
    manuscript_path: Path,
    manuscript: SourceBinding,
    status: dict[str, object],
) -> str:
    template_relative, template_path = _repo_path(
        repo_root, config["review_template"], "config.review_template"
    )
    if not template_path.is_file():
        raise FactoryError(f"review template is not a file: {template_relative}")
    title, paragraphs = _parse_markdown(manuscript_path)
    review = config["review"]
    brief = config["brief"]
    chapter = config["chapter"]
    assert isinstance(review, dict)
    assert isinstance(brief, dict)
    assert isinstance(chapter, dict)
    article_html, blocks = _review_blocks(paragraphs, review["part_boundaries"])
    review_data = {
        "review_id": f"{chapter['slug']}-{manuscript.sha256[:12]}",
        "transport": "novel_chapter",
        "draft": {
            "id": chapter["slug"],
            "path": manuscript.path,
            "sha256": manuscript.sha256,
            "sha256_12": manuscript.sha256[:12],
            "title": title,
        },
        "schema": {
            "path": "projects/lucifers-lights/ontology/WHISPER-INTENT.md",
            "substrate_version": "project-local-candidate",
        },
        "pareto": {
            "hard_gates": ["author_acceptance", "canonical_manuscript_unchanged"],
            "objectives": ["resonance", "relevance", "trajectory"],
            "selected_candidate": brief["candidate_id"],
            "tiering": "project-local",
        },
        "factory": status,
        "blocks": blocks,
    }
    data_json = json.dumps(review_data, ensure_ascii=True, indent=2).replace("</", "<\\/")
    template = template_path.read_text(encoding="utf-8")
    rendered = template.replace("__WHISPER_REVIEW_DATA_JSON__", data_json).replace(
        "__WHISPER_REVIEW_ARTICLE_HTML__", f"<h1>{_inline_markdown(title)}</h1>\n{article_html}"
    )
    rendered = rendered.replace(
        "</title>",
        '</title>\n  <link rel="icon" href="data:,">',
        1,
    )
    stage_items = "\n".join(
        (
            '<li class="factory-stage">'
            f'<span>{html.escape(str(item["label"]))}</span>'
            f'<strong data-stage-status="{html.escape(str(item["status"]))}">'
            f'{html.escape(str(item["status"]))}</strong></li>'
        )
        for item in status["stages"]
    )
    chapter_label = f"Chapter {chapter['number']}"
    if status["result"] == "accepted":
        boundary = (
            f"{chapter_label} is author-accepted. Local derivative compilation is "
            "eligible; provider synthesis remains unauthorized."
        )
    elif status["result"] == "blocked":
        boundary = (
            f"{chapter_label} is mechanically blocked. No editorial, derivative, "
            "or export action is eligible."
        )
    else:
        boundary = (
            f"{chapter_label} is review-pending. Tests and comments cannot accept it."
        )

    def factory_card(variant: str, aria_label: str) -> str:
        return f"""
      <section class="factory-card factory-card--{variant}" aria-label="{aria_label}">
        <p class="kicker">Chapter Factory Pilot</p>
        <h2 class="panel-title">{html.escape(str(status['current_stage']))}</h2>
        <p class="factory-boundary">{html.escape(boundary)}</p>
        <ol class="factory-stages">{stage_items}</ol>
      </section>
"""

    sidecard = factory_card("sidebar", "Chapter Factory status")
    mobile_card = factory_card("mobile", "Chapter Factory status for narrow screens")
    css = """
    .factory-card { margin: 0 0 24px; padding: 14px; border: 1px solid var(--accent); border-radius: var(--radius); background: #151412; }
    .factory-card--mobile { display: none; }
    .factory-boundary { color: var(--muted); font-size: .86rem; line-height: 1.45; }
    .factory-stages { list-style: none; padding: 0; margin: 14px 0 0; display: grid; gap: 7px; }
    .factory-stage { display: flex; justify-content: space-between; gap: 12px; color: var(--muted); font-size: .82rem; }
    .factory-stage strong { color: var(--accent-2); font-weight: 700; text-transform: uppercase; }
    .factory-stage strong[data-stage-status="pending"], .factory-stage strong[data-stage-status="withheld"] { color: var(--accent); }
    @media (max-width: 980px) {
      .factory-card--mobile { display: block; }
      .factory-card--sidebar { display: none; }
    }
"""
    rendered = rendered.replace("  </style>", css + "\n  </style>", 1)
    rendered = rendered.replace(
        '      <article class="article" id="draft-article">',
        mobile_card + '\n      <article class="article" id="draft-article">',
        1,
    )
    rendered = rendered.replace(
        '    <aside class="side-pane">',
        '    <aside class="side-pane">\n' + sidecard,
        1,
    )
    return rendered


def _managed_outputs(config: dict[str, object]) -> tuple[str, ...]:
    if "voice" in config:
        return (*MANAGED_OUTPUTS, VOICE_HANDOFF_OUTPUT)
    return MANAGED_OUTPUTS


def _binding_by_id(
    bindings: list[SourceBinding], source_id: str, label: str
) -> SourceBinding:
    binding = next((item for item in bindings if item.source_id == source_id), None)
    if binding is None:
        raise FactoryError(f"{label} source binding is missing: {source_id}")
    return binding


def _validate_voice_sync_disposition(
    config: dict[str, object],
    binding: SourceBinding,
    repo_root: Path,
    compiler_root: dict[str, object],
) -> None:
    if binding.role != "derivative-sync-decision":
        raise FactoryError(
            "voice sync disposition source role must be derivative-sync-decision"
        )
    try:
        document = json.loads(
            (repo_root / binding.path).read_text(encoding="utf-8")
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise FactoryError(f"cannot read voice sync disposition: {error}") from error
    root = _closed_mapping(
        document,
        "voice sync disposition",
        (
            "schema_version",
            "project_id",
            "chapter_id",
            "manuscript_sha256",
            "transport",
            "authorization",
            "structural_contract",
            "dispositions",
        ),
    )
    if root["schema_version"] != "lucifers-lights.voice-sync-disposition/1.0.0":
        raise FactoryError("unsupported voice sync disposition schema")
    chapter = config["chapter"]
    assert isinstance(chapter, dict)
    if root["project_id"] != config["project_id"]:
        raise FactoryError("voice sync disposition project id does not match")
    if root["chapter_id"] != chapter["id"]:
        raise FactoryError("voice sync disposition chapter id does not match")
    if root["manuscript_sha256"] != chapter["expected_sha256"]:
        raise FactoryError("voice sync disposition manuscript digest does not match")
    if root["transport"] != "motion-comic-voiceover":
        raise FactoryError("unsupported voice sync disposition transport")

    authorization = _closed_mapping(
        root["authorization"],
        "voice sync disposition.authorization",
        ("instruction", "recorded_at", "scope", "external_effects_authorized"),
    )
    _text(authorization["instruction"], "voice sync disposition.authorization.instruction")
    _text(authorization["recorded_at"], "voice sync disposition.authorization.recorded_at")
    if authorization["scope"] != "accepted-manuscript-to-local-performance-script":
        raise FactoryError("voice sync authorization scope does not match")
    if authorization["external_effects_authorized"] is not False:
        raise FactoryError("voice sync disposition cannot authorize external effects")

    contract = _closed_mapping(
        root["structural_contract"],
        "voice sync disposition.structural_contract",
        (
            "expected_segment_count",
            "expected_performance_tag_count",
            "preserve_speaker_sequence",
            "preserve_performance_tag_positions",
        ),
    )
    segment_count = _integer(
        contract["expected_segment_count"],
        "voice sync disposition.structural_contract.expected_segment_count",
        minimum=1,
    )
    tag_count = _integer(
        contract["expected_performance_tag_count"],
        "voice sync disposition.structural_contract.expected_performance_tag_count",
    )
    for field in ("preserve_speaker_sequence", "preserve_performance_tag_positions"):
        if contract[field] is not True:
            raise FactoryError(f"voice sync disposition must require {field}")

    acceptance = _closed_mapping(
        compiler_root["acceptance"],
        "voice compiler config acceptance",
        (
            "allowed_speakers",
            "expected_segment_count",
            "performance_tags",
            "transformations_require_approval",
        ),
    )
    if acceptance["expected_segment_count"] != segment_count:
        raise FactoryError("voice sync segment count does not match compiler config")
    performance_tags = _closed_mapping(
        acceptance["performance_tags"],
        "voice compiler config performance tags",
        ("expected_count", "profile"),
    )
    if performance_tags["expected_count"] != tag_count:
        raise FactoryError("voice sync tag count does not match compiler config")
    if acceptance["transformations_require_approval"] is not True:
        raise FactoryError("voice compiler config must require transformation approval")

    dispositions = root["dispositions"]
    if not isinstance(dispositions, list) or not dispositions:
        raise FactoryError("voice sync dispositions must be a non-empty array")
    observed_blocks: list[str] = []
    for index, value in enumerate(dispositions):
        item = _closed_mapping(
            value,
            f"voice sync disposition.dispositions[{index}]",
            ("review_block_ids", "action", "target_segment_ordinals", "rationale"),
        )
        block_ids = _string_list(
            item["review_block_ids"],
            f"voice sync disposition.dispositions[{index}].review_block_ids",
        )
        observed_blocks.extend(block_ids)
        action = item["action"]
        if action not in {"include", "omit"}:
            raise FactoryError("voice sync disposition action must be include or omit")
        targets = item["target_segment_ordinals"]
        if not isinstance(targets, list) or any(
            isinstance(value, bool)
            or not isinstance(value, int)
            or value < 1
            or value > segment_count
            for value in targets
        ):
            raise FactoryError("voice sync target ordinals are invalid")
        if len(targets) != len(set(targets)):
            raise FactoryError("voice sync target ordinals contain duplicates")
        if action == "include" and not targets:
            raise FactoryError("included voice sync disposition requires a target")
        if action == "omit" and targets:
            raise FactoryError("omitted voice sync disposition cannot have a target")
        _text(
            item["rationale"],
            f"voice sync disposition.dispositions[{index}].rationale",
        )
    if len(observed_blocks) != len(set(observed_blocks)):
        raise FactoryError("voice sync disposition repeats review block ids")


def build_voice_handoff(
    config: dict[str, object],
    bindings: list[SourceBinding],
    repo_root: Path,
    chapter_run_digest: str,
    decision: AuthorDecision | None,
) -> dict[str, object]:
    """Build a local-only handoff with an explicit manuscript and effect ceiling."""

    voice = config.get("voice")
    if not isinstance(voice, dict):
        raise FactoryError("voice handoff requested without config.voice")
    chapter = config["chapter"]
    run = config["run"]
    assert isinstance(chapter, dict)
    assert isinstance(run, dict)

    source = _binding_by_id(
        bindings,
        str(voice["source_id"]),
        "voice derivative",
    )
    compiler_config = _binding_by_id(
        bindings,
        str(voice["compiler_config_source_id"]),
        "voice compiler config",
    )
    sync_disposition = _binding_by_id(
        bindings,
        str(voice["sync_disposition_source_id"]),
        "voice sync disposition",
    )
    if source.role != "audio-script-derivative":
        raise FactoryError("voice source role must be audio-script-derivative")
    if compiler_config.role != "voice-compiler-config":
        raise FactoryError("voice compiler config role must be voice-compiler-config")

    try:
        compiler_document = json.loads(
            (repo_root / compiler_config.path).read_text(encoding="utf-8")
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise FactoryError(f"cannot read voice compiler config: {error}") from error
    compiler_root = _closed_mapping(
        compiler_document,
        "voice compiler config",
        (
            "schema_version",
            "production_id",
            "source",
            "selection",
            "acceptance",
            "output_policy",
        ),
    )
    if compiler_root["schema_version"] != "voice-production.compiler-config/v1":
        raise FactoryError("unsupported voice compiler config schema")
    compiler_source = _closed_mapping(
        compiler_root["source"],
        "voice compiler config source",
        ("expected_sha256", "locator", "media_type", "profile", "header"),
    )
    if compiler_source["expected_sha256"] != source.sha256:
        raise FactoryError("voice compiler config source digest does not match binding")
    if compiler_source["locator"] != source.path:
        raise FactoryError("voice compiler config source locator does not match binding")
    _validate_voice_sync_disposition(
        config, sync_disposition, repo_root, compiler_root
    )

    local_compile_ready = (
        decision is not None
        and voice["derivative_status"] == "local-compile-ready"
    )

    return {
        "schema_version": "lucifers-lights.voice-compiler-handoff/1.0.0",
        "identity": {
            "project_id": config["project_id"],
            "chapter_id": chapter["id"],
            "run_id": run["id"],
        },
        "chapter_run_digest": chapter_run_digest,
        "manuscript_gate": {
            "expected_sha256": chapter["expected_sha256"],
            "decision_state": "accepted" if decision is not None else "review_pending",
            "decision_receipt_ref": (
                decision.source.path if decision is not None else None
            ),
        },
        "voice_source": source.to_document(),
        "compiler_config": {
            **compiler_config.to_document(),
            "schema_version": compiler_root["schema_version"],
            "production_id": compiler_root["production_id"],
        },
        "sync_disposition": sync_disposition.to_document(),
        "derivative": {
            "profile": voice["derivative_profile"],
            "status": voice["derivative_status"],
        },
        "admission": {
            "state": "eligible" if local_compile_ready else "withheld",
            "scope": "local-compile-only",
            "reason": (
                "accepted_manuscript_and_synchronized_script"
                if local_compile_ready
                else (
                    "derivative_sync_pending"
                    if decision is not None
                    else "author_acceptance_pending"
                )
            ),
        },
        "transport": "local-repository-data-only",
        "authority_effect": "none",
        "external_effects": {
            "network": False,
            "provider": False,
            "secret_access": False,
            "media_generation": False,
            "publication": False,
        },
    }


def _output_status(
    config: dict[str, object],
    deterministic_status: str,
    run_digest: str,
    decision: AuthorDecision | None,
) -> dict[str, object]:
    chapter = config["chapter"]
    run = config["run"]
    assert isinstance(chapter, dict)
    assert isinstance(run, dict)
    accepted = decision is not None
    validation_passed = deterministic_status == "pass"
    review_stage = (
        "pass" if accepted and validation_passed else (
            "pending" if validation_passed else "withheld"
        )
    )
    local_compile_ready = (
        accepted
        and validation_passed
        and isinstance(config.get("voice"), dict)
        and config["voice"]["derivative_status"] == "local-compile-ready"
    )
    stages = [
        {"id": "sources", "label": "Source binding", "status": "pass"},
        {"id": "brief", "label": "Chapter brief", "status": "pass"},
        {"id": "manuscript", "label": "Draft/import", "status": "pass"},
        {
            "id": "deterministic_review",
            "label": "Mechanical checks",
            "status": deterministic_status,
        },
        {"id": "editorial_review", "label": "Editorial review", "status": review_stage},
        {
            "id": "revision",
            "label": "Revision candidate",
            "status": "pass" if accepted and validation_passed else "withheld",
        },
        {
            "id": "author_decision",
            "label": "Author decision",
            "status": "pass" if accepted else "pending",
        },
    ]
    if "voice" in config:
        stages.append(
            {
                "id": "voice_handoff",
                "label": "Voice handoff",
                "status": "eligible" if local_compile_ready else "withheld",
            }
        )
    stages.extend(
        [
            {
                "id": "export",
                "label": "Accepted export",
                "status": "eligible" if accepted and validation_passed else "withheld",
            },
            {
                "id": "next_chapter",
                "label": "Next chapter",
                "status": "eligible" if accepted and validation_passed else "withheld",
            },
        ]
    )
    return {
        "schema_version": "lucifers-lights.chapter-factory-status/1.0.0",
        "project_id": config["project_id"],
        "chapter_id": chapter["id"],
        "run_id": run["id"],
        "chapter_run_digest": run_digest,
        "current_stage": (
            "local voice compile"
            if local_compile_ready
            else (
                "accepted baseline"
                if accepted and validation_passed
                else (
                    "author review"
                    if validation_passed
                    else "deterministic review blocked"
                )
            )
        ),
        "result": (
            "blocked"
            if not validation_passed
            else ("accepted" if accepted else "review_pending")
        ),
        "stages": stages,
        "authority_effect": "none",
        "external_effects": {
            "network": False,
            "provider": False,
            "secret_access": False,
            "media_generation": False,
            "publication": False,
        },
    }


def run_pilot(
    config_path: Path,
    output_dir: Path,
    repo_root: Path,
    *,
    replace: bool = False,
) -> dict[str, object]:
    repo_root = repo_root.resolve()
    config_path = config_path.resolve()
    try:
        config_path.relative_to(repo_root)
    except ValueError as error:
        raise FactoryError("config path is outside the repository") from error
    output_dir = output_dir.resolve()
    try:
        output_dir.relative_to(repo_root)
    except ValueError as error:
        raise FactoryError("output directory is outside the repository") from error
    if output_dir.exists() and any(output_dir.iterdir()) and not replace:
        raise FactoryError(f"output directory is not empty: {output_dir}")

    config = load_config(config_path)
    bindings = bind_sources(config, repo_root)
    chapter = config["chapter"]
    assert isinstance(chapter, dict)
    manuscript = next(
        item for item in bindings if item.source_id == chapter["manuscript_source_id"]
    )
    decision = load_author_decision(config, bindings, repo_root, manuscript)
    manuscript_path = repo_root / manuscript.path
    manuscript_text = manuscript_path.read_text(encoding="utf-8")
    checks, metrics = evaluate_manuscript(manuscript_text, manuscript.sha256, config)
    deterministic_status = "pass" if all(item.status == "pass" for item in checks) else "fail"

    chapter_run = build_chapter_run(config, bindings, manuscript, metrics, decision)
    identity = canonical_identity(chapter_run)
    status = _output_status(config, deterministic_status, identity.sha256, decision)
    human_gate = "approved" if decision is not None else "pending"
    context_manifest = {
        "schema_version": "lucifers-lights.chapter-factory-context/1.0.0",
        "config_path": config_path.relative_to(repo_root).as_posix(),
        "project_id": config["project_id"],
        "run_id": config["run"]["id"],
        "sources": [item.to_document() for item in bindings],
        "source_count": len(bindings),
        "contains_manuscript_prose": False,
        "authority_effect": "none",
    }
    review_report = {
        "schema_version": "lucifers-lights.chapter-factory-review/1.0.0",
        "run_id": config["run"]["id"],
        "manuscript": manuscript.to_document(),
        "metrics": metrics,
        "checks": [item.to_document() for item in checks],
        "deterministic_status": deterministic_status,
        "human_gate": human_gate,
        "result": (
            "block"
            if deterministic_status != "pass"
            else ("pass" if decision is not None else "flag")
        ),
        "authority_effect": "none",
    }

    documents: dict[str, str] = {
        "context-manifest.json": _canonical_json(context_manifest),
        "chapter-run.json": _canonical_json(chapter_run),
        "chapter-brief.md": build_brief(config, bindings, decision),
        "deterministic-review.json": _canonical_json(review_report),
        "editorial-review.md": build_editorial_review(
            config, checks, metrics, manuscript, decision
        ),
        "factory-status.json": _canonical_json(status),
        "decision-request.md": build_decision_request(
            config,
            manuscript,
            (
                "accepted"
                if decision is not None and deterministic_status == "pass"
                else (
                    "ready_for_author_review"
                    if deterministic_status == "pass"
                    else "blocked"
                )
            ),
            decision,
        ),
        "chapter-review.html": build_review_html(
            config, repo_root, manuscript_path, manuscript, status
        ),
    }
    if "voice" in config:
        documents[VOICE_HANDOFF_OUTPUT] = _canonical_json(
            build_voice_handoff(
                config, bindings, repo_root, identity.sha256, decision
            )
        )
    managed_outputs = _managed_outputs(config)
    output_dir.mkdir(parents=True, exist_ok=True)
    for name in managed_outputs:
        (output_dir / name).write_text(documents[name], encoding="utf-8")

    output_inventory = []
    for name in managed_outputs:
        path = output_dir / name
        output_inventory.append(
            {"path": name, "sha256": _sha256(path), "size_bytes": path.stat().st_size}
        )
    receipt = {
        "schema_version": RECEIPT_SCHEMA,
        "run_id": config["run"]["id"],
        "result": status["result"],
        "deterministic_validation": deterministic_status,
        "human_gate": human_gate,
        "chapter_run_digest": identity.sha256,
        "outputs": output_inventory,
        "canonical_manuscript_changed": False,
        "authority_effect": "none",
        "external_effects": status["external_effects"],
    }
    receipt_path = output_dir / "factory-receipt.json"
    receipt_path.write_text(_canonical_json(receipt), encoding="utf-8")
    return {
        "result": receipt["result"],
        "output_dir": str(output_dir),
        "receipt": str(receipt_path),
        "chapter_run_digest": identity.sha256,
        "manuscript_sha256": manuscript.sha256,
        "deterministic_validation": deterministic_status,
        "human_gate": human_gate,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    pilot = subparsers.add_parser("pilot", help="build one local review-pending run")
    pilot.add_argument("--repo-root", type=Path, default=Path.cwd())
    pilot.add_argument("--config", type=Path, required=True)
    pilot.add_argument("--output", type=Path, required=True)
    pilot.add_argument("--replace", action="store_true")
    status = subparsers.add_parser("status", help="print one factory status document")
    status.add_argument("--run", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "status":
            path = args.run / "factory-status.json"
            print(path.read_text(encoding="utf-8"), end="")
            return 0
        result = run_pilot(
            args.config,
            args.output,
            args.repo_root,
            replace=args.replace,
        )
    except (FactoryError, OSError, UnicodeError) as error:
        print(f"BLOCK: {error}")
        return 2
    print(_canonical_json(result), end="")
    return 0 if result["deterministic_validation"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "CONFIG_SCHEMA",
    "FactoryError",
    "SourceBinding",
    "bind_sources",
    "build_chapter_run",
    "build_voice_handoff",
    "evaluate_manuscript",
    "load_config",
    "run_pilot",
]
