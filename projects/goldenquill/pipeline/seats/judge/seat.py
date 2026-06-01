"""pipeline.seats.judge.seat — §9 Judge Round 3 subprocess entry.

Spec card: ``pipeline/engineering/spec_cards/section_09_judge_round_3_seat_entry_and_sfr.md``

Disciplines (mirrors Scribe R3):

- **E-017 injected-seam.** Every collaborator is a callable Protocol:
  :class:`ClockFn`, :class:`GoogleCallCallable`, :class:`PreGateCallable`,
  :class:`PostGateCallable`, :class:`RubricLoaderCallable`,
  :class:`ScoreOrchestrator`. Production wires stdlib stdin/stdout/stderr
  + real clock + real Google HTTP client (LOCKED at ``provider_google.py``).
- **V1 inline-literal rebind-resistance.** Envelope and result version
  strings inline-literalled at dispatch (``"judge-envelope.v1"`` /
  ``"judge-result.v1"``). Exit-code mapping {0, 1, 2} also inline.
- **A-v1-13 minimal-env.** Keys never ride through ``os.environ``;
  BYOK retrieval happens via ``provider_google.call_google_judge``
  on the injected ``KeyRetrieveCallable`` seam inside the subprocess.
- **§F.1 SFR emission.** Judge is **NOT** SFR-exempt. Successful runs
  emit a three-block SFR text alongside the JudgeVerdict in the result.
- **F_PIPE_08 cross-family enforcement.** The envelope carries the
  Scribe-landed family. seat.py refuses (PRE-gate
  ``F-JUDGE-CROSS-FAMILY-COLLISION``) when Scribe's family equals
  ``"google"`` — Judge's production binding family.
- **No ``sys.exit`` inside run_seat.** ``run_seat`` returns an ``int``
  exit code; the ``__main__`` block (deferred to the production launcher)
  is the sole ``sys.exit`` caller.
"""

from __future__ import annotations

import json
import traceback
from dataclasses import dataclass
from datetime import datetime, timezone
from types import MappingProxyType
from typing import (
    Any,
    BinaryIO,
    Final,
    Literal,
    Mapping,
    Protocol,
)

from pipeline.seats.judge.provider_google import (
    F_JUDGE_BYOK_MISSING,
    F_JUDGE_PAYLOAD_CEILING,
    F_JUDGE_PROVIDER_MALFORMED,
    F_JUDGE_SEMANTIC_FAILURE,
    F_JUDGE_TRANSPORT_FAILURE,
    GoogleBYOKMissing,
    GoogleCallCallable,
    GooglePayloadCeiling,
    GoogleProviderMalformed,
    GoogleResponse,
    GoogleSemanticFailure,
    GoogleTransportFailure,
)
from pipeline.seats.judge.sfr_emitter import SfrReport
from pipeline.seats.judge.types import (
    JudgeVerdict,
    Rubric,
    SectionDraftLike,
)


# ---------------------------------------------------------------------------
# Envelope + result version literals
# ---------------------------------------------------------------------------

ENVELOPE_VERSION_V1: Final[str] = "judge-envelope.v1"
RESULT_VERSION_V1: Final[str] = "judge-result.v1"

EXIT_OK: Final[int] = 0
EXIT_INTERNAL_ERROR: Final[int] = 1
EXIT_GATE_FAIL: Final[int] = 2


# ---------------------------------------------------------------------------
# R3 failure-code constants (extending R1's six F-JUDGE-* codes)
# ---------------------------------------------------------------------------

F_JUDGE_ENVELOPE_MALFORMED: Final[str] = "F-JUDGE-ENVELOPE-MALFORMED"
F_JUDGE_CROSS_FAMILY_COLLISION: Final[str] = "F-JUDGE-CROSS-FAMILY-COLLISION"
F_JUDGE_ORG_CROSS_REF: Final[str] = "F-JUDGE-ORG-CROSS-REF"
F_JUDGE_RUBRIC_LOAD_FAIL: Final[str] = "F-JUDGE-RUBRIC-LOAD-FAIL"
F_JUDGE_SCORE_ORCHESTRATION_FAIL: Final[str] = (
    "F-JUDGE-SCORE-ORCHESTRATION-FAIL"
)


# Provider-family closed set for the cross-family collision check.
_JUDGE_OWN_FAMILY: Final[str] = "google"


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class JudgeGateFailed(RuntimeError):
    """Fail-closed PRE/POST-gate outcome; stderr JSON emitted; exit 2."""

    def __init__(
        self,
        *,
        failure_code: str,
        trigger: str,
        evidence: Mapping[str, Any],
    ) -> None:
        super().__init__(f"{failure_code}: {trigger}")
        self.failure_code = failure_code
        self.trigger = trigger
        self.evidence = dict(evidence)


class JudgeEnvelopeMalformed(RuntimeError):
    """Envelope parse / shape invariant violation."""


# ---------------------------------------------------------------------------
# Shapes: JudgeEnvelope + JudgeResult
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class JudgeEnvelope:
    """Subprocess stdin envelope — frozen, kw-only, slots (A-13).

    ``envelope_version`` MUST be the literal ``"judge-envelope.v1"``.
    ``scribe_provider_family`` is the family the prior Scribe step landed
    on; the seat refuses when it equals ``"google"`` (cross-family
    discipline).
    """

    envelope_version: str
    run_id: str
    org_slug: str
    iteration_number: int
    program_code: str
    rubric_path: str
    rfa_content_sha3_512: str
    rfa_scope_summary: str
    scribe_provider_family: str
    section_drafts_blob: tuple[Mapping[str, Any], ...]
    compiled_prompt_shell_sha3_512: str
    project_context: Mapping[str, Any]
    envelope_emitted_at_utc: datetime

    # §4 v2.x.5 CC-007 fields (LOCKED 2026-05-16 row 232) — production
    # wire-up reads these to construct the OutboundCallable wrapper around
    # provider_boundary.stdlib_urlopen_caller.
    classification_context_json: str = ""
    posture: Literal[
        "frontier_eligible", "split_context_hybrid", "local_only_sovereign"
    ] = "local_only_sovereign"

    def __post_init__(self) -> None:
        if self.envelope_version != "judge-envelope.v1":
            raise JudgeEnvelopeMalformed(
                f"{F_JUDGE_ENVELOPE_MALFORMED}: envelope_version must be "
                f"'judge-envelope.v1'; got {self.envelope_version!r}"
            )
        if not self.run_id or not self.run_id.strip():
            raise JudgeEnvelopeMalformed(
                f"{F_JUDGE_ENVELOPE_MALFORMED}: run_id must be non-empty"
            )
        if not self.org_slug or not self.org_slug.strip():
            raise JudgeEnvelopeMalformed(
                f"{F_JUDGE_ENVELOPE_MALFORMED}: org_slug must be non-empty"
            )
        if self.iteration_number < 0:
            raise JudgeEnvelopeMalformed(
                f"{F_JUDGE_ENVELOPE_MALFORMED}: iteration_number must be >= 0"
            )
        if not self.program_code.strip():
            raise JudgeEnvelopeMalformed(
                f"{F_JUDGE_ENVELOPE_MALFORMED}: program_code must be non-empty"
            )
        if not self.rubric_path.strip():
            raise JudgeEnvelopeMalformed(
                f"{F_JUDGE_ENVELOPE_MALFORMED}: rubric_path must be non-empty"
            )
        if len(self.rfa_content_sha3_512) != 128:
            raise JudgeEnvelopeMalformed(
                f"{F_JUDGE_ENVELOPE_MALFORMED}: rfa_content_sha3_512 must be "
                f"128 hex chars; got {len(self.rfa_content_sha3_512)}"
            )
        if self.rfa_content_sha3_512 != self.rfa_content_sha3_512.lower():
            raise JudgeEnvelopeMalformed(
                f"{F_JUDGE_ENVELOPE_MALFORMED}: rfa_content_sha3_512 must be "
                f"lowercase hex"
            )
        if not self.rfa_scope_summary.strip():
            raise JudgeEnvelopeMalformed(
                f"{F_JUDGE_ENVELOPE_MALFORMED}: rfa_scope_summary must be "
                f"non-empty"
            )
        if not self.scribe_provider_family.strip():
            raise JudgeEnvelopeMalformed(
                f"{F_JUDGE_ENVELOPE_MALFORMED}: scribe_provider_family must "
                f"be non-empty"
            )
        if not self.section_drafts_blob:
            raise JudgeEnvelopeMalformed(
                f"{F_JUDGE_ENVELOPE_MALFORMED}: section_drafts_blob must be "
                f"non-empty"
            )
        if len(self.compiled_prompt_shell_sha3_512) != 128:
            raise JudgeEnvelopeMalformed(
                f"{F_JUDGE_ENVELOPE_MALFORMED}: compiled_prompt_shell_sha3_512 "
                f"must be 128 hex chars"
            )
        if (
            self.compiled_prompt_shell_sha3_512
            != self.compiled_prompt_shell_sha3_512.lower()
        ):
            raise JudgeEnvelopeMalformed(
                f"{F_JUDGE_ENVELOPE_MALFORMED}: compiled_prompt_shell_sha3_512 "
                f"must be lowercase hex"
            )
        if self.envelope_emitted_at_utc.tzinfo is None:
            raise JudgeEnvelopeMalformed(
                f"{F_JUDGE_ENVELOPE_MALFORMED}: envelope_emitted_at_utc must "
                f"be timezone-aware"
            )
        if not isinstance(self.project_context, MappingProxyType):
            object.__setattr__(
                self,
                "project_context",
                MappingProxyType(dict(self.project_context)),
            )


@dataclass(frozen=True, kw_only=True, slots=True)
class JudgeResult:
    """Subprocess stdout payload — frozen, kw-only, slots (A-13)."""

    result_version: str
    run_id: str
    org_slug: str
    iteration_number: int
    judge_verdict: JudgeVerdict
    sfr_report: SfrReport
    sfr_text: str
    compiled_prompt_shell_sha3_512: str
    provider_landed_family: str
    provider_landed_model_id: str
    seat_emitted_at_utc: datetime

    def __post_init__(self) -> None:
        if self.result_version != "judge-result.v1":
            raise ValueError(
                f"JudgeResult.result_version must be 'judge-result.v1'; "
                f"got {self.result_version!r}"
            )
        if self.iteration_number < 0:
            raise ValueError("iteration_number must be >= 0")
        if not self.provider_landed_family:
            raise ValueError("provider_landed_family must be non-empty")
        if not self.provider_landed_model_id:
            raise ValueError("provider_landed_model_id must be non-empty")
        if self.seat_emitted_at_utc.tzinfo is None:
            raise ValueError("seat_emitted_at_utc must be timezone-aware")
        if len(self.compiled_prompt_shell_sha3_512) != 128:
            raise ValueError("compiled_prompt_shell_sha3_512 must be 128-hex")
        if not self.sfr_text.strip():
            raise ValueError("JudgeResult.sfr_text must be non-empty (§F.1)")


# ---------------------------------------------------------------------------
# E-017 Protocols
# ---------------------------------------------------------------------------


class ClockFn(Protocol):
    """Returns current UTC time; wall-clock seam for determinism tests."""

    def __call__(self) -> datetime: ...


class RubricLoaderCallable(Protocol):
    """Load a rubric from disk → :class:`Rubric`. Production wires
    :func:`pipeline.seats.judge.rubric_loader.load_rubric`."""

    def __call__(self, *, rubric_path: str) -> Rubric: ...


class ScoreOrchestrator(Protocol):
    """Drive R1 + R2 primitives: dispatch_score_units → score_dimension per
    unit → assemble_verdict. Production composes
    :func:`pipeline.seats.judge.cross_rubric_dispatch.dispatch_score_units` +
    :func:`pipeline.seats.judge.dimension_scorer.score_dimension` +
    :func:`pipeline.seats.judge.verdict_assembler.assemble_verdict`.

    Returns the assembled :class:`JudgeVerdict` plus the provider-reported
    ``landed_model_id`` and ``landed_family`` (for the result envelope).
    """

    def __call__(
        self,
        *,
        envelope: "JudgeEnvelope",
        rubric: Rubric,
        section_drafts: tuple[SectionDraftLike, ...],
        google_call: GoogleCallCallable,
    ) -> tuple[JudgeVerdict, str, str]: ...


class PreGateCallable(Protocol):
    """Judge PRE-gate assembler invocation. Raises JudgeGateFailed on trip."""

    def __call__(self, *, envelope: "JudgeEnvelope") -> None: ...


class PostGateCallable(Protocol):
    """Judge POST-gate assembler invocation. Raises JudgeGateFailed on trip."""

    def __call__(
        self,
        *,
        envelope: "JudgeEnvelope",
        judge_verdict: JudgeVerdict,
        rubric: Rubric,
        section_drafts: tuple[SectionDraftLike, ...],
    ) -> None: ...


class SectionDraftDecoder(Protocol):
    """Decode envelope section_drafts_blob → tuple of SectionDraftLike.

    Production wires the Scribe SectionDraft re-hydrator; tests inject a
    stub that returns lightweight dataclass instances satisfying the
    SectionDraftLike Protocol.
    """

    def __call__(
        self, *, blob: tuple[Mapping[str, Any], ...]
    ) -> tuple[SectionDraftLike, ...]: ...


# ---------------------------------------------------------------------------
# Envelope decoder
# ---------------------------------------------------------------------------


def decode_envelope(*, raw_bytes: bytes) -> JudgeEnvelope:
    """Decode stdin bytes into a frozen JudgeEnvelope.

    Raises :class:`JudgeEnvelopeMalformed` on any parse / shape failure.
    """
    if not raw_bytes:
        raise JudgeEnvelopeMalformed(
            f"{F_JUDGE_ENVELOPE_MALFORMED}: stdin empty"
        )
    try:
        decoded = json.loads(raw_bytes.decode("utf-8"))
    except UnicodeDecodeError as exc:
        raise JudgeEnvelopeMalformed(
            f"{F_JUDGE_ENVELOPE_MALFORMED}: stdin not UTF-8: {exc}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise JudgeEnvelopeMalformed(
            f"{F_JUDGE_ENVELOPE_MALFORMED}: stdin is not JSON: {exc}"
        ) from exc
    if not isinstance(decoded, dict):
        raise JudgeEnvelopeMalformed(
            f"{F_JUDGE_ENVELOPE_MALFORMED}: stdin JSON top-level must be "
            f"object; got {type(decoded).__name__}"
        )
    version = decoded.get("envelope_version")
    if version != "judge-envelope.v1":
        raise JudgeEnvelopeMalformed(
            f"{F_JUDGE_ENVELOPE_MALFORMED}: envelope_version must be "
            f"'judge-envelope.v1'; got {version!r}"
        )
    required_keys = (
        "envelope_version",
        "run_id",
        "org_slug",
        "iteration_number",
        "program_code",
        "rubric_path",
        "rfa_content_sha3_512",
        "rfa_scope_summary",
        "scribe_provider_family",
        "section_drafts_blob",
        "compiled_prompt_shell_sha3_512",
        "project_context",
        "envelope_emitted_at_utc",
    )
    missing = [k for k in required_keys if k not in decoded]
    if missing:
        raise JudgeEnvelopeMalformed(
            f"{F_JUDGE_ENVELOPE_MALFORMED}: envelope missing keys: "
            f"{missing!r}"
        )
    emit_raw = decoded["envelope_emitted_at_utc"]
    if not isinstance(emit_raw, str):
        raise JudgeEnvelopeMalformed(
            f"{F_JUDGE_ENVELOPE_MALFORMED}: envelope_emitted_at_utc must be "
            f"ISO-8601 string; got {type(emit_raw).__name__}"
        )
    try:
        emit_dt = datetime.fromisoformat(emit_raw)
    except ValueError as exc:
        raise JudgeEnvelopeMalformed(
            f"{F_JUDGE_ENVELOPE_MALFORMED}: envelope_emitted_at_utc not "
            f"ISO-8601: {exc}"
        ) from exc
    project_context = decoded["project_context"]
    if not isinstance(project_context, Mapping):
        raise JudgeEnvelopeMalformed(
            f"{F_JUDGE_ENVELOPE_MALFORMED}: project_context must be mapping"
        )
    blob_raw = decoded["section_drafts_blob"]
    if not isinstance(blob_raw, list):
        raise JudgeEnvelopeMalformed(
            f"{F_JUDGE_ENVELOPE_MALFORMED}: section_drafts_blob must be array"
        )
    blob_tuple = tuple(
        e for e in blob_raw if isinstance(e, Mapping)
    )
    if len(blob_tuple) != len(blob_raw):
        raise JudgeEnvelopeMalformed(
            f"{F_JUDGE_ENVELOPE_MALFORMED}: section_drafts_blob entries must "
            f"all be objects"
        )
    return JudgeEnvelope(
        envelope_version=version,
        run_id=str(decoded["run_id"]),
        org_slug=str(decoded["org_slug"]),
        iteration_number=int(decoded["iteration_number"]),
        program_code=str(decoded["program_code"]),
        rubric_path=str(decoded["rubric_path"]),
        rfa_content_sha3_512=str(decoded["rfa_content_sha3_512"]),
        rfa_scope_summary=str(decoded["rfa_scope_summary"]),
        scribe_provider_family=str(decoded["scribe_provider_family"]),
        section_drafts_blob=blob_tuple,
        compiled_prompt_shell_sha3_512=str(
            decoded["compiled_prompt_shell_sha3_512"]
        ),
        project_context=dict(project_context),
        envelope_emitted_at_utc=emit_dt,
    )


# ---------------------------------------------------------------------------
# Result encoder
# ---------------------------------------------------------------------------


def encode_result(result: JudgeResult) -> bytes:
    """Encode a JudgeResult as canonical UTF-8 JSON bytes, trailing newline."""
    payload = {
        "result_version": result.result_version,
        "run_id": result.run_id,
        "org_slug": result.org_slug,
        "iteration_number": result.iteration_number,
        "compiled_prompt_shell_sha3_512": result.compiled_prompt_shell_sha3_512,
        "provider_landed_family": result.provider_landed_family,
        "provider_landed_model_id": result.provider_landed_model_id,
        "seat_emitted_at_utc": result.seat_emitted_at_utc.isoformat(),
        "judge_verdict": _serialize_verdict(result.judge_verdict),
        "sfr_report": _serialize_sfr(result.sfr_report),
        "sfr_text": result.sfr_text,
    }
    data = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return data.encode("utf-8") + b"\n"


def _serialize_verdict(verdict: JudgeVerdict) -> Mapping[str, Any]:
    jo = verdict.judge_output
    return {
        "rubric_program_code": verdict.rubric_program_code,
        "assembled_at_utc": verdict.assembled_at_utc.isoformat(),
        "responsiveness_entries": [
            {
                "criterion_id": e.criterion_id,
                "factor_name": e.factor_name,
                "factor_values": list(e.factor_values),
            }
            for e in verdict.responsiveness_map.entries
        ],
        "judge_output": {
            "total_score": jo.total_score,
            "max_total": jo.max_total,
            "rubric_sha256": jo.rubric_sha256,
            "rfa_content_sha3_512": jo.rfa_content_sha3_512,
            "scored_at_utc": jo.scored_at_utc.isoformat(),
            "criterion_scores": [
                {
                    "criterion_id": cs.criterion_id,
                    "score": cs.score,
                    "evidence_quote": cs.evidence_quote,
                    "confidence": cs.confidence,
                    "rationale": cs.rationale,
                }
                for cs in jo.criterion_scores
            ],
        },
    }


def _serialize_sfr(report: SfrReport) -> Mapping[str, Any]:
    return {
        "program_code": report.program_code,
        "funder": report.funder,
        "nofo_number": report.nofo_number,
        "rubric_sha256": report.rubric_sha256,
        "rfa_scope_summary": report.rfa_scope_summary,
        "total_score": report.total_score,
        "max_total": report.max_total,
        "percent_score": report.percent_score,
        "pass_threshold": report.pass_threshold,
        "passed": report.passed,
        "mean_confidence": report.mean_confidence,
        "line_items": [
            {
                "criterion_id": li.criterion_id,
                "score": li.score,
                "max_points": li.max_points,
                "confidence": li.confidence,
                "evidence_quote": li.evidence_quote,
                "rationale": li.rationale,
            }
            for li in report.line_items
        ],
    }


# ---------------------------------------------------------------------------
# Stderr JSON-line emitter
# ---------------------------------------------------------------------------


def _emit_stderr_failure(
    *,
    stderr: BinaryIO,
    failure_code: str,
    trigger: str,
    evidence: Mapping[str, Any],
    clock: ClockFn,
) -> None:
    """Write a single-line structured failure JSON to stderr."""
    try:
        emitted_at = clock().isoformat()
    except Exception:  # pragma: no cover — clock-fn defensive fallback
        emitted_at = datetime.now(tz=timezone.utc).isoformat()
    payload = {
        "envelope_version": "judge-envelope.v1",
        "failure_code": failure_code,
        "trigger": trigger,
        "evidence": dict(evidence),
        "emitted_at_utc": emitted_at,
    }
    line = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    stderr.write(line.encode("utf-8") + b"\n")


# ---------------------------------------------------------------------------
# The subprocess entry
# ---------------------------------------------------------------------------


def run_seat(
    *,
    stdin: BinaryIO,
    stdout: BinaryIO,
    stderr: BinaryIO,
    clock: ClockFn,
    google_call: GoogleCallCallable,
    rubric_loader: RubricLoaderCallable,
    section_draft_decoder: SectionDraftDecoder,
    score_orchestrator: ScoreOrchestrator,
    sfr_emitter: "SfrEmitterCallable",
    pre_gate: PreGateCallable,
    post_gate: PostGateCallable,
) -> int:
    """Subprocess entry. Returns 0/1/2 exit code; does NOT call sys.exit.

    Flow:
      1. Read stdin → decode envelope (version-literal pinned).
      2. Run PRE-gate assembly (cross-family + Cedar org-isolation +
         rubric-hash drift).
      3. Load rubric via injected ``rubric_loader``.
      4. Decode section_drafts_blob → tuple of SectionDraftLike.
      5. Run ``score_orchestrator`` (drives R1+R2 primitives + Google call).
      6. Emit SFR via injected ``sfr_emitter``.
      7. Run POST-gate assembly (evidence-in-draft + score bounds).
      8. Encode JudgeResult → stdout; exit 0.

    Fail-closed at any step → stderr JSON line + exit 2.
    Unexpected exception → stderr traceback + exit 1.
    """
    try:
        raw_bytes = stdin.read()
    except Exception as exc:  # pragma: no cover - stdin failure is bug-class
        stderr.write(f"stdin read failed: {exc!r}\n".encode("utf-8"))
        return EXIT_INTERNAL_ERROR

    try:
        envelope = decode_envelope(raw_bytes=raw_bytes)
    except JudgeEnvelopeMalformed as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=F_JUDGE_ENVELOPE_MALFORMED,
            trigger="envelope_decode_failed",
            evidence={"exception": str(exc)},
            clock=clock,
        )
        return EXIT_GATE_FAIL

    try:
        pre_gate(envelope=envelope)
    except JudgeGateFailed as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=exc.failure_code,
            trigger=exc.trigger,
            evidence=exc.evidence,
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except Exception as exc:
        stderr.write(
            f"pre_gate raised unhandled exception class={type(exc).__name__}\n".encode(
                "utf-8"
            )
        )
        return EXIT_INTERNAL_ERROR

    try:
        rubric = rubric_loader(rubric_path=envelope.rubric_path)
    except JudgeGateFailed as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=exc.failure_code,
            trigger=exc.trigger,
            evidence=exc.evidence,
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except Exception as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=F_JUDGE_RUBRIC_LOAD_FAIL,
            trigger="rubric_loader_raised",
            evidence={"exception_class": type(exc).__name__},
            clock=clock,
        )
        return EXIT_GATE_FAIL

    try:
        section_drafts = section_draft_decoder(blob=envelope.section_drafts_blob)
    except JudgeGateFailed as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=exc.failure_code,
            trigger=exc.trigger,
            evidence=exc.evidence,
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except Exception as exc:
        stderr.write(
            f"section_draft_decoder raised unhandled exception "
            f"class={type(exc).__name__}\n".encode("utf-8")
        )
        return EXIT_INTERNAL_ERROR

    # Sanitize Google-exception messages.
    try:
        judge_verdict, landed_family, landed_model_id = score_orchestrator(
            envelope=envelope,
            rubric=rubric,
            section_drafts=section_drafts,
            google_call=google_call,
        )
    except GoogleBYOKMissing as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=F_JUDGE_BYOK_MISSING,
            trigger="byok_missing",
            evidence={"exception_class": type(exc).__name__, "org_slug": envelope.org_slug},
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except GooglePayloadCeiling as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=F_JUDGE_PAYLOAD_CEILING,
            trigger="payload_ceiling_exceeded",
            evidence={"exception_class": type(exc).__name__},
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except GoogleTransportFailure as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=F_JUDGE_TRANSPORT_FAILURE,
            trigger="transport_retry_exhausted",
            evidence={"exception_class": type(exc).__name__},
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except GoogleSemanticFailure as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=F_JUDGE_SEMANTIC_FAILURE,
            trigger="semantic_4xx",
            evidence={"exception_class": type(exc).__name__},
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except GoogleProviderMalformed as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=F_JUDGE_PROVIDER_MALFORMED,
            trigger="provider_non_json_or_missing_fields",
            evidence={"exception_class": type(exc).__name__},
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except JudgeGateFailed as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=exc.failure_code,
            trigger=exc.trigger,
            evidence=exc.evidence,
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except Exception as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=F_JUDGE_SCORE_ORCHESTRATION_FAIL,
            trigger="score_orchestrator_raised",
            evidence={"exception_class": type(exc).__name__},
            clock=clock,
        )
        return EXIT_GATE_FAIL

    try:
        sfr_report = sfr_emitter(
            envelope=envelope,
            judge_verdict=judge_verdict,
            rubric=rubric,
            section_drafts=section_drafts,
        )
    except JudgeGateFailed as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=exc.failure_code,
            trigger=exc.trigger,
            evidence=exc.evidence,
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except Exception as exc:
        tb = traceback.format_exc()
        stderr.write(f"sfr_emitter raised: {exc!r}\n{tb}\n".encode("utf-8"))
        return EXIT_INTERNAL_ERROR

    try:
        post_gate(
            envelope=envelope,
            judge_verdict=judge_verdict,
            rubric=rubric,
            section_drafts=section_drafts,
        )
    except JudgeGateFailed as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=exc.failure_code,
            trigger=exc.trigger,
            evidence=exc.evidence,
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except Exception as exc:
        stderr.write(
            f"post_gate raised unhandled exception class={type(exc).__name__}\n".encode(
                "utf-8"
            )
        )
        return EXIT_INTERNAL_ERROR

    try:
        from pipeline.seats.judge.sfr_emitter import render_sfr_text

        sfr_text = render_sfr_text(sfr_report)
        result = JudgeResult(
            result_version="judge-result.v1",
            run_id=envelope.run_id,
            org_slug=envelope.org_slug,
            iteration_number=envelope.iteration_number,
            judge_verdict=judge_verdict,
            sfr_report=sfr_report,
            sfr_text=sfr_text,
            compiled_prompt_shell_sha3_512=envelope.compiled_prompt_shell_sha3_512,
            provider_landed_family=landed_family,
            provider_landed_model_id=landed_model_id,
            seat_emitted_at_utc=clock(),
        )
        stdout.write(encode_result(result))
    except Exception as exc:  # pragma: no cover — defensive: upstream invariants make this unreachable
        tb = traceback.format_exc()
        stderr.write(f"result emission failed: {exc!r}\n{tb}\n".encode("utf-8"))
        return EXIT_INTERNAL_ERROR

    return EXIT_OK


# ---------------------------------------------------------------------------
# SfrEmitter Protocol — defined here to keep run_seat's signature dense
# ---------------------------------------------------------------------------


class SfrEmitterCallable(Protocol):
    def __call__(
        self,
        *,
        envelope: JudgeEnvelope,
        judge_verdict: JudgeVerdict,
        rubric: Rubric,
        section_drafts: tuple[SectionDraftLike, ...],
    ) -> SfrReport: ...


__all__ = [
    # Shapes
    "JudgeEnvelope",
    "JudgeResult",
    # Protocols
    "ClockFn",
    "RubricLoaderCallable",
    "ScoreOrchestrator",
    "PreGateCallable",
    "PostGateCallable",
    "SectionDraftDecoder",
    "SfrEmitterCallable",
    # Entry point
    "run_seat",
    # Codec
    "decode_envelope",
    "encode_result",
    # Exceptions
    "JudgeGateFailed",
    "JudgeEnvelopeMalformed",
    # Constants
    "ENVELOPE_VERSION_V1",
    "RESULT_VERSION_V1",
    "EXIT_OK",
    "EXIT_INTERNAL_ERROR",
    "EXIT_GATE_FAIL",
    # Failure-code constants
    "F_JUDGE_ENVELOPE_MALFORMED",
    "F_JUDGE_CROSS_FAMILY_COLLISION",
    "F_JUDGE_ORG_CROSS_REF",
    "F_JUDGE_RUBRIC_LOAD_FAIL",
    "F_JUDGE_SCORE_ORCHESTRATION_FAIL",
]
