"""pipeline.seats.editor.seat — §8 Editor Round 1 subprocess entry.

Matches :class:`pipeline.loop.seat_runner.invoke_editor` §4.4 contract
(same shape as Scribe R3 ``seat.py``): stdin JSON envelope → Logician
PRE-gate → adapter → Logician POST-gate → stdout JSON. Minimal-env
whitelist enforced upstream by ``seat_runner._build_minimal_env``; this
module trusts the env it receives.

Disciplines (per spec card §11 hardenings):

- **E-017 injected-seam pattern.** Every collaborator is a callable
  Protocol: :class:`ClockFn`, :class:`StdinReadCallable`,
  :class:`StdoutWriteCallable`, :class:`StderrWriteCallable`,
  :class:`PreGateCallable`, :class:`PostGateCallable`. Production wires
  stdlib stdin/stdout/stderr + real clock + real ``SkillLauncher``.
- **V1 inline-literal rebind-resistance.** Envelope and result version
  strings inline-literalled (``"editor-envelope.v1"`` /
  ``"editor-result.v1"``). Exit-code mapping {0, 1, 2} also inline.
- **A-v1-13 minimal-env.** Skills run via clawdis subprocess; key
  retrieval lives inside the launcher, not in :mod:`os.environ`.
- **No ``sys.exit`` inside run_seat.** ``run_seat`` returns an ``int``
  exit code; the ``__main__`` block below is the sole ``sys.exit`` caller.

Threat-model boundaries (per spec card §11 + adapter docstring):

- **Trusted-operator envelope (§3.11 v5).** Caller supplies
  ``editor-envelope.v1`` JSON; seat layer asserts envelope.org_slug
  matches the ambient ``TILTH_ORG_SLUG`` and refuses mismatched
  invocation (``F_PRE_CROSS_ORG_READ`` proxy).
- **Skill-subprocess trust boundary.** The skill itself is the LLM-call
  layer; seat.py only wraps the adapter to translate F-EDITOR-* into
  structured stderr JSON.
- **E-027 / E-028 N/A at adapter layer.** Adapter dispatches to skill
  subprocess (clawdis), not to a code-review committee; payload-size
  ceiling is between skill and provider, not between seat and reviewer.
- **Retry-with-clarification deferred to R2.** Seat raises on the
  adapter's first malformed-output, no in-loop retry.
"""

from __future__ import annotations

import json
import traceback
from dataclasses import dataclass
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Any, BinaryIO, Final, Mapping, Protocol

from pipeline.seats.editor.adapter import (
    EditorOutputShapeError,
    EditorRewroteInsteadOfFlaggedError,
    EditorSingleReplacementError,
    EditorSkillOutputMalformedJson,
    EditorSkillSubprocessFail,
    EditorSkillTimeout,
    SkillLauncher,
    invoke_editor_adapter,
)
from pipeline.seats.editor.types import (
    EditorInput,
    EditorOutput,
    _DIALECT_VALID,
)


# ---------------------------------------------------------------------------
# Envelope + result version literals (V1 rebind-resistance)
# ---------------------------------------------------------------------------

ENVELOPE_VERSION_V1: Final[str] = "editor-envelope.v1"
RESULT_VERSION_V1: Final[str] = "editor-result.v1"


# ---------------------------------------------------------------------------
# Exit codes (per Scribe R3 precedent)
# ---------------------------------------------------------------------------

EXIT_OK: Final[int] = 0
EXIT_INTERNAL_ERROR: Final[int] = 1
EXIT_GATE_FAIL: Final[int] = 2


# ---------------------------------------------------------------------------
# Failure-code constants (PRE-gate proxy + envelope-malformed)
# ---------------------------------------------------------------------------

F_EDITOR_ENVELOPE_MALFORMED: Final[str] = "F-EDITOR-ENVELOPE-MALFORMED"
F_EDITOR_ORG_CROSS_REF: Final[str] = "F-EDITOR-ORG-CROSS-REF"


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class EditorEnvelopeMalformed(RuntimeError):
    """Envelope parse / shape invariant violation."""


class EditorGateFailed(RuntimeError):
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


# ---------------------------------------------------------------------------
# EditorEnvelope + EditorSeatResult shapes
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class EditorEnvelope:
    """Subprocess stdin envelope — frozen, kw-only, slots (A-13).

    ``envelope_version`` MUST be the literal ``"editor-envelope.v1"``.
    """

    envelope_version: str
    run_id: str
    org_slug: str
    iteration_number: int
    section_drafts: tuple[Mapping[str, object], ...]
    rfa_excerpt: str
    dialect: str
    session_id: str
    envelope_emitted_at_utc: datetime

    def __post_init__(self) -> None:
        if self.envelope_version != "editor-envelope.v1":
            raise EditorEnvelopeMalformed(
                f"{F_EDITOR_ENVELOPE_MALFORMED}: envelope_version must be "
                f"'editor-envelope.v1'; got {self.envelope_version!r}"
            )
        if not self.run_id or not self.run_id.strip():
            raise EditorEnvelopeMalformed(
                f"{F_EDITOR_ENVELOPE_MALFORMED}: run_id must be non-empty"
            )
        if not self.org_slug or not self.org_slug.strip():
            raise EditorEnvelopeMalformed(
                f"{F_EDITOR_ENVELOPE_MALFORMED}: org_slug must be non-empty"
            )
        if self.iteration_number < 0:
            raise EditorEnvelopeMalformed(
                f"{F_EDITOR_ENVELOPE_MALFORMED}: iteration_number must be "
                f">= 0; got {self.iteration_number!r}"
            )
        if not isinstance(self.section_drafts, tuple) or len(self.section_drafts) < 1:
            raise EditorEnvelopeMalformed(
                f"{F_EDITOR_ENVELOPE_MALFORMED}: section_drafts must be a "
                f"non-empty tuple"
            )
        if self.dialect not in _DIALECT_VALID:
            raise EditorEnvelopeMalformed(
                f"{F_EDITOR_ENVELOPE_MALFORMED}: dialect must be one of "
                f"{sorted(_DIALECT_VALID)}; got {self.dialect!r}"
            )
        if not self.session_id or not self.session_id.strip():
            raise EditorEnvelopeMalformed(
                f"{F_EDITOR_ENVELOPE_MALFORMED}: session_id must be non-empty"
            )
        if self.envelope_emitted_at_utc.tzinfo is None:
            raise EditorEnvelopeMalformed(
                f"{F_EDITOR_ENVELOPE_MALFORMED}: envelope_emitted_at_utc must "
                f"be timezone-aware"
            )


@dataclass(frozen=True, kw_only=True, slots=True)
class EditorSeatResult:
    """Subprocess stdout payload — frozen, kw-only, slots (A-13)."""

    result_version: str
    run_id: str
    org_slug: str
    iteration_number: int
    editor_output: EditorOutput
    seat_emitted_at_utc: datetime

    def __post_init__(self) -> None:
        if self.result_version != "editor-result.v1":
            raise ValueError(
                f"EditorSeatResult.result_version must be 'editor-result.v1'; "
                f"got {self.result_version!r}"
            )
        if self.iteration_number < 0:
            raise ValueError("iteration_number must be >= 0")
        if self.seat_emitted_at_utc.tzinfo is None:
            raise ValueError("seat_emitted_at_utc must be timezone-aware")


# ---------------------------------------------------------------------------
# E-017 Protocols
# ---------------------------------------------------------------------------


class ClockFn(Protocol):
    """Returns current UTC time; wall-clock seam for determinism tests."""

    def __call__(self) -> datetime: ...


class PreGateCallable(Protocol):
    """Editor PRE-gate — caller-provided cross-org check (§4.2.1).

    Production wires a Cedar evaluator against the dossier; tests inject
    a deterministic stub. Raises :class:`EditorGateFailed` with
    :attr:`F_EDITOR_ORG_CROSS_REF` on mismatch.
    """

    def __call__(
        self,
        *,
        envelope: EditorEnvelope,
        ambient_org_slug: str,
    ) -> None: ...


class PostGateCallable(Protocol):
    """Editor POST-gate — wraps adapter validator output for §4.2.1.

    The adapter's ``validate_editor_output_shape`` raises specific
    :class:`F_EDITOR_*` exceptions inline; production wires this gate to
    a Logician adapter that re-runs the same checks (defense-in-depth)
    plus any future cross-seat invariants. Tests inject a no-op stub.
    """

    def __call__(
        self,
        *,
        envelope: EditorEnvelope,
        editor_output: EditorOutput,
    ) -> None: ...


# ---------------------------------------------------------------------------
# Envelope decoder
# ---------------------------------------------------------------------------


def decode_envelope(*, raw_bytes: bytes) -> EditorEnvelope:
    """Decode stdin bytes into a frozen EditorEnvelope.

    Raises :class:`EditorEnvelopeMalformed` on any parse / shape failure.
    """
    if not raw_bytes:
        raise EditorEnvelopeMalformed(
            f"{F_EDITOR_ENVELOPE_MALFORMED}: stdin empty"
        )
    try:
        decoded = json.loads(raw_bytes.decode("utf-8"))
    except UnicodeDecodeError as exc:
        raise EditorEnvelopeMalformed(
            f"{F_EDITOR_ENVELOPE_MALFORMED}: stdin not UTF-8: {exc}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise EditorEnvelopeMalformed(
            f"{F_EDITOR_ENVELOPE_MALFORMED}: stdin is not JSON: {exc}"
        ) from exc
    if not isinstance(decoded, dict):
        raise EditorEnvelopeMalformed(
            f"{F_EDITOR_ENVELOPE_MALFORMED}: stdin JSON top-level must be "
            f"object; got {type(decoded).__name__}"
        )
    version = decoded.get("envelope_version")
    if version != "editor-envelope.v1":
        raise EditorEnvelopeMalformed(
            f"{F_EDITOR_ENVELOPE_MALFORMED}: envelope_version must be "
            f"'editor-envelope.v1'; got {version!r}"
        )
    required_keys = (
        "envelope_version",
        "run_id",
        "org_slug",
        "iteration_number",
        "section_drafts",
        "rfa_excerpt",
        "dialect",
        "session_id",
        "envelope_emitted_at_utc",
    )
    missing = [k for k in required_keys if k not in decoded]
    if missing:
        raise EditorEnvelopeMalformed(
            f"{F_EDITOR_ENVELOPE_MALFORMED}: envelope missing keys: {missing!r}"
        )
    emit_raw = decoded["envelope_emitted_at_utc"]
    if not isinstance(emit_raw, str):
        raise EditorEnvelopeMalformed(
            f"{F_EDITOR_ENVELOPE_MALFORMED}: envelope_emitted_at_utc must be "
            f"ISO-8601 string; got {type(emit_raw).__name__}"
        )
    try:
        emit_dt = datetime.fromisoformat(emit_raw)
    except ValueError as exc:
        raise EditorEnvelopeMalformed(
            f"{F_EDITOR_ENVELOPE_MALFORMED}: envelope_emitted_at_utc not "
            f"ISO-8601: {exc}"
        ) from exc
    section_drafts_raw = decoded["section_drafts"]
    if not isinstance(section_drafts_raw, list):
        raise EditorEnvelopeMalformed(
            f"{F_EDITOR_ENVELOPE_MALFORMED}: section_drafts must be list; got "
            f"{type(section_drafts_raw).__name__}"
        )
    section_drafts: list[Mapping[str, object]] = []
    for i, sd in enumerate(section_drafts_raw):
        if not isinstance(sd, dict):
            raise EditorEnvelopeMalformed(
                f"{F_EDITOR_ENVELOPE_MALFORMED}: section_drafts[{i}] must be "
                f"object; got {type(sd).__name__}"
            )
        # Freeze each entry to MappingProxyType for immutability downstream.
        section_drafts.append(MappingProxyType(dict(sd)))
    return EditorEnvelope(
        envelope_version=version,
        run_id=str(decoded["run_id"]),
        org_slug=str(decoded["org_slug"]),
        iteration_number=int(decoded["iteration_number"]),
        section_drafts=tuple(section_drafts),
        rfa_excerpt=str(decoded["rfa_excerpt"]),
        dialect=str(decoded["dialect"]),
        session_id=str(decoded["session_id"]),
        envelope_emitted_at_utc=emit_dt,
    )


# ---------------------------------------------------------------------------
# Result encoder — emit canonical JSON bytes
# ---------------------------------------------------------------------------


def _replacement_to_dict(opt) -> dict:
    return {"label": opt.label, "text": opt.text, "note": opt.note}


def _flagged_term_to_dict(term) -> dict:
    return {
        "section_ref": term.section_ref,
        "issue_type": term.issue_type,
        "severity": term.severity,
        "excerpt": term.excerpt,
        "why_it_hurts": term.why_it_hurts,
        "rubric_connection": term.rubric_connection,
        "replacement_options": [
            _replacement_to_dict(o) for o in term.replacement_options
        ],
    }


def _miscategorization_to_dict(m) -> dict:
    return {
        "excerpt": m.excerpt,
        "stated_as": m.stated_as,
        "should_be": m.should_be,
        "why": m.why,
    }


def _taxonomy_to_dict(tx) -> dict:
    return {
        "goals_identified": list(tx.goals_identified),
        "outputs_identified": list(tx.outputs_identified),
        "outcomes_identified": list(tx.outcomes_identified),
        "objectives_identified": list(tx.objectives_identified),
        "miscategorizations": [
            _miscategorization_to_dict(m) for m in tx.miscategorizations
        ],
    }


def _readability_to_dict(r) -> dict:
    return {
        "score_10": r.score_10,
        "grade_level_estimate": r.grade_level_estimate,
        "verdict": r.verdict,
    }


def _tone_to_dict(t) -> dict:
    return {
        "overall_readability": _readability_to_dict(t.overall_readability),
        "key_message": t.key_message,
        "reviewer_fatigue_sections": list(t.reviewer_fatigue_sections),
    }


def _gap_to_dict(g) -> dict:
    return {
        "section_ref": g.section_ref,
        "issue": g.issue,
        "action_needed": g.action_needed,
    }


def _editor_output_to_dict(out: EditorOutput) -> dict:
    return {
        "flagged_terms": [_flagged_term_to_dict(t) for t in out.flagged_terms],
        "taxonomy_check": _taxonomy_to_dict(out.taxonomy_check),
        "tone_feedback": _tone_to_dict(out.tone_feedback),
        "quick_wins": list(out.quick_wins),
        "terms_to_verify": list(out.terms_to_verify),
        "gaps": [_gap_to_dict(g) for g in out.gaps],
    }


def encode_result(result: EditorSeatResult) -> bytes:
    """Encode an EditorSeatResult as canonical UTF-8 JSON, trailing newline."""
    payload = {
        "result_version": result.result_version,
        "run_id": result.run_id,
        "org_slug": result.org_slug,
        "iteration_number": result.iteration_number,
        "seat_emitted_at_utc": result.seat_emitted_at_utc.isoformat(),
        "editor_output": _editor_output_to_dict(result.editor_output),
    }
    data = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return data.encode("utf-8") + b"\n"


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
    except Exception:
        emitted_at = datetime.now(tz=timezone.utc).isoformat()
    payload = {
        "envelope_version": "editor-envelope.v1",
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
# Subprocess entry — run_seat
# ---------------------------------------------------------------------------


def run_seat(
    *,
    stdin: BinaryIO,
    stdout: BinaryIO,
    stderr: BinaryIO,
    clock: ClockFn,
    skill_launcher: SkillLauncher,
    pre_gate: PreGateCallable,
    post_gate: PostGateCallable,
    ambient_org_slug: str,
) -> int:
    """Subprocess entry. Returns 0/1/2 exit code; does NOT call sys.exit.

    Flow:
      1. Read stdin → decode envelope (version-literal pinned).
      2. Run PRE-gate (cross-org check via injected callable).
      3. Construct :class:`EditorInput` from envelope.
      4. Invoke adapter (skill dispatch + parse + validate).
      5. Run POST-gate (defense-in-depth re-validation).
      6. Encode :class:`EditorSeatResult` → stdout; exit 0.

    Fail-closed at any step → stderr JSON line + exit 2.
    Unexpected exception → stderr traceback + exit 1.
    """
    try:
        raw_bytes = stdin.read()
    except Exception as exc:  # pragma: no cover — bug-class
        stderr.write(f"stdin read failed: {exc!r}\n".encode("utf-8"))
        return EXIT_INTERNAL_ERROR

    try:
        envelope = decode_envelope(raw_bytes=raw_bytes)
    except EditorEnvelopeMalformed as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=F_EDITOR_ENVELOPE_MALFORMED,
            trigger="envelope_decode_failed",
            evidence={"exception": str(exc)},
            clock=clock,
        )
        return EXIT_GATE_FAIL

    try:
        pre_gate(envelope=envelope, ambient_org_slug=ambient_org_slug)
    except EditorGateFailed as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=exc.failure_code,
            trigger=exc.trigger,
            evidence=exc.evidence,
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except Exception as exc:
        # Defense-in-depth: pre_gate raising a non-gate exception is
        # bug-class. Sanitized stderr (class name only).
        stderr.write(
            f"pre_gate raised unhandled exception class={type(exc).__name__}\n".encode(
                "utf-8"
            )
        )
        return EXIT_INTERNAL_ERROR

    try:
        editor_input = EditorInput(
            section_drafts=envelope.section_drafts,
            rfa_excerpt=envelope.rfa_excerpt,
            dialect=envelope.dialect,  # type: ignore[arg-type]
            session_id=envelope.session_id,
            org_slug=envelope.org_slug,
        )
    except Exception as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=F_EDITOR_ENVELOPE_MALFORMED,
            trigger="editor_input_construction_failed",
            evidence={"exception_class": type(exc).__name__},
            clock=clock,
        )
        return EXIT_GATE_FAIL

    try:
        editor_output = invoke_editor_adapter(
            editor_input,
            skill_launcher=skill_launcher,
            clock=clock,
        )
    except EditorSkillTimeout as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=exc.failure_code,
            trigger="skill_subprocess_timeout",
            evidence={"exception_class": type(exc).__name__},
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except EditorSkillSubprocessFail as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=exc.failure_code,
            trigger="skill_subprocess_failed",
            evidence={"exception_class": type(exc).__name__},
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except EditorSkillOutputMalformedJson as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=exc.failure_code,
            trigger="skill_output_malformed_json",
            evidence={"exception_class": type(exc).__name__},
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except EditorOutputShapeError as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=exc.failure_code,
            trigger="output_shape_violation",
            evidence={"exception_class": type(exc).__name__},
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except EditorRewroteInsteadOfFlaggedError as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=exc.failure_code,
            trigger="rewrite_threshold_exceeded",
            evidence={"exception_class": type(exc).__name__},
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except EditorSingleReplacementError as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=exc.failure_code,
            trigger="replacement_count_violation",
            evidence={"exception_class": type(exc).__name__},
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except Exception as exc:
        # Defense-in-depth: any other exception from the adapter pipeline
        # is bug-class. Sanitized stderr (class name only) — same
        # fingerprint-leak discipline as Scribe R3 seat.
        stderr.write(
            f"invoke_editor_adapter raised unhandled exception "
            f"class={type(exc).__name__}\n".encode("utf-8")
        )
        return EXIT_INTERNAL_ERROR

    try:
        post_gate(envelope=envelope, editor_output=editor_output)
    except EditorGateFailed as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=exc.failure_code,
            trigger=exc.trigger,
            evidence=exc.evidence,
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except Exception as exc:
        # Same fingerprint-leak discipline as pre_gate above.
        stderr.write(
            f"post_gate raised unhandled exception class={type(exc).__name__}\n".encode(
                "utf-8"
            )
        )
        return EXIT_INTERNAL_ERROR

    try:
        result = EditorSeatResult(
            result_version="editor-result.v1",
            run_id=envelope.run_id,
            org_slug=envelope.org_slug,
            iteration_number=envelope.iteration_number,
            editor_output=editor_output,
            seat_emitted_at_utc=clock(),
        )
        stdout.write(encode_result(result))
    except Exception as exc:
        tb = traceback.format_exc()
        stderr.write(f"result emission failed: {exc!r}\n{tb}\n".encode("utf-8"))
        return EXIT_INTERNAL_ERROR

    return EXIT_OK


# ---------------------------------------------------------------------------
# Default PRE-gate — caller-supplied check (§4.2.1 caller-provided set)
# ---------------------------------------------------------------------------


def default_cross_org_pre_gate(
    *,
    envelope: EditorEnvelope,
    ambient_org_slug: str,
) -> None:
    """Default PRE-gate: assert envelope.org_slug == ambient_org_slug.

    Production may override with a Cedar evaluator; this default catches
    the common case (TILTH_ORG_SLUG mismatched against envelope) and
    raises :class:`EditorGateFailed` with :data:`F_EDITOR_ORG_CROSS_REF`.
    """
    if envelope.org_slug != ambient_org_slug:
        raise EditorGateFailed(
            failure_code=F_EDITOR_ORG_CROSS_REF,
            trigger="envelope_org_slug_mismatch",
            evidence={
                "envelope_org_slug": envelope.org_slug,
                "ambient_org_slug": ambient_org_slug,
            },
        )


def default_noop_post_gate(
    *,
    envelope: EditorEnvelope,
    editor_output: EditorOutput,
) -> None:
    """Default POST-gate: no-op. Adapter validator runs inline; production
    Logician POST-gate adapter wires here at integration time.
    """
    return None


__all__ = [
    # Constants
    "ENVELOPE_VERSION_V1",
    "RESULT_VERSION_V1",
    "EXIT_OK",
    "EXIT_INTERNAL_ERROR",
    "EXIT_GATE_FAIL",
    "F_EDITOR_ENVELOPE_MALFORMED",
    "F_EDITOR_ORG_CROSS_REF",
    # Shapes
    "EditorEnvelope",
    "EditorSeatResult",
    # Protocols
    "ClockFn",
    "PreGateCallable",
    "PostGateCallable",
    # Exceptions
    "EditorEnvelopeMalformed",
    "EditorGateFailed",
    # Codec
    "decode_envelope",
    "encode_result",
    # Entry
    "run_seat",
    "default_cross_org_pre_gate",
    "default_noop_post_gate",
]
