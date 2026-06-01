"""pipeline.seats.scribe.seat — Round 3 subprocess entry.

Blueprint §7 v1.1.1 + §6 v1-r1 + §5 v6 + §4 v2.1 + §2 v7.1 LOCKED.
Spec card: ``pipeline/engineering/spec_cards/section_07_scribe_round_3_seat_entry_and_wiring.md``.

Disciplines (see spec §7):

- **E-017 injected-seam.** Every collaborator is a callable Protocol:
  ``ClockFn``, ``StdinReadCallable``, ``StdoutWriteCallable``,
  ``StderrWriteCallable``, ``AnthropicCallCallable``,
  ``ResponseParseCallable``, ``PreGateCallable``, ``PostGateCallable``.
  Production wires stdlib ``sys.stdin.buffer`` / ``sys.stdout.buffer`` /
  ``sys.stderr.buffer`` + real clock + real Anthropic HTTP client
  (already LOCKED at ``provider_anthropic.py``).
- **V1 inline-literal rebind-resistance.** Envelope and result version
  strings inline-literalled at dispatch (``"scribe-envelope.v1"`` /
  ``"scribe-result.v1"``). Exit-code mapping {0, 1, 2} also inline.
- **A-v1-13 minimal-env.** Keys never ride through ``os.environ``;
  BYOK retrieval happens via ``provider_anthropic.call_anthropic_scribe``
  on the injected ``KeyRetrieveCallable`` seam inside the subprocess.
- **§6.11 shell-hash persistence.** The compiled-prompt *shell* hash
  rides through the envelope and echoes in the result; the full prompt
  never crosses the persistence boundary (§J grant-content-never-flows).
- **No ``sys.exit`` inside run_seat.** ``run_seat`` returns an ``int``
  exit code; the ``__main__`` block below is the sole ``sys.exit`` caller.
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

from pipeline.seats.scribe.admin_risk_adapter import AdminRiskRegister
from pipeline.seats.scribe.provider_anthropic import (
    AnthropicBYOKMissing,
    AnthropicCallCallable,
    AnthropicPayloadCeiling,
    AnthropicProviderMalformed,
    AnthropicResponse,
    AnthropicSemanticFailure,
    AnthropicTransportFailure,
    F_SCRIBE_BYOK_MISSING,
    F_SCRIBE_PAYLOAD_CEILING,
    F_SCRIBE_PROVIDER_MALFORMED,
    F_SCRIBE_SEMANTIC_FAILURE,
    F_SCRIBE_TRANSPORT_FAILURE,
)
from pipeline.seats.scribe.section_draft import AdminRiskFlag, SectionDraft

# ---------------------------------------------------------------------------
# Envelope + result version literals (V1 rebind-resistance: inline-literalled
# in parse/emit; these constants are read-only for humans).
# ---------------------------------------------------------------------------

ENVELOPE_VERSION_V1: Final[str] = "scribe-envelope.v1"
RESULT_VERSION_V1: Final[str] = "scribe-result.v1"

# ---------------------------------------------------------------------------
# Exit codes (per §4.3 spec card).
# ---------------------------------------------------------------------------

EXIT_OK: Final[int] = 0
EXIT_INTERNAL_ERROR: Final[int] = 1
EXIT_GATE_FAIL: Final[int] = 2


# ---------------------------------------------------------------------------
# Failure codes extending §7.13 scope. Full string constants here so that
# logician_wiring + seat.py + admin_risk_adapter all reference them by-name.
# ---------------------------------------------------------------------------

F_SCRIBE_SCOPE_MISSING: Final[str] = "F-SCRIBE-SCOPE-MISSING"
F_SCRIBE_ORG_CROSS_REF: Final[str] = "F-SCRIBE-ORG-CROSS-REF"
F_SCRIBE_DIALECT_UNCLASSIFIED: Final[str] = "F-SCRIBE-DIALECT-UNCLASSIFIED"
F_SCRIBE_TEMPLATE_UNKNOWN: Final[str] = "F-SCRIBE-TEMPLATE-UNKNOWN"
F_SCRIBE_TEMPLATE_DRIFT: Final[str] = "F-SCRIBE-TEMPLATE-DRIFT"
F_SCRIBE_UNSOURCED_CLAIM: Final[str] = "F-SCRIBE-UNSOURCED-CLAIM"
F_SCRIBE_PARAPHRASED_NUMERIC: Final[str] = "F-SCRIBE-PARAPHRASED-NUMERIC"
F_SCRIBE_DIALECT_INDUCED_IDENTITY: Final[str] = "F-SCRIBE-DIALECT-INDUCED-IDENTITY"
F_SCRIBE_CONVERSATION_ANCHOR_INVALID: Final[str] = (
    "F-SCRIBE-CONVERSATION-ANCHOR-INVALID"
)
F_SCRIBE_DIALECT_DRIFT: Final[str] = "F-SCRIBE-DIALECT-DRIFT"
F_SCRIBE_SECTION_OVER_LIMIT_UNFLAGGED: Final[str] = (
    "F-SCRIBE-SECTION-OVER-LIMIT-UNFLAGGED"
)
F_SCRIBE_OVERLOOKED_EXPENSE_UNRESOLVED: Final[str] = (
    "F-SCRIBE-OVERLOOKED-EXPENSE-UNRESOLVED"
)
F_SCRIBE_SMART_INVENTED_METRIC: Final[str] = "F-SCRIBE-SMART-INVENTED-METRIC"
F_SCRIBE_EVALUATION_CRITERION_MISSING: Final[str] = (
    "F-SCRIBE-EVALUATION-CRITERION-MISSING"
)
F_SCRIBE_INELIGIBLE_ACTIVITY: Final[str] = "F-SCRIBE-INELIGIBLE-ACTIVITY"
F_SCRIBE_ENVELOPE_MALFORMED: Final[str] = "F-SCRIBE-ENVELOPE-MALFORMED"

# Valid funder-dialect enum (mirrors pipeline.seats.scribe.dialect.Dialect
# string values). Inline-literal frozenset at construction time.
_VALID_FUNDER_DIALECTS: Final[frozenset[str]] = frozenset(
    {"conservative", "centrist", "progressive", "soul_fire"}
)


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class ScribeGateFailed(RuntimeError):
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


class ScribeEnvelopeMalformed(RuntimeError):
    """Envelope parse / shape invariant violation."""


# ---------------------------------------------------------------------------
# Shapes: ScribeEnvelope + ScribeResult
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class ScribeEnvelope:
    """Subprocess stdin envelope — frozen, kw-only, slots (A-13).

    ``envelope_version`` MUST be the literal ``"scribe-envelope.v1"``.
    """

    envelope_version: str
    run_id: str
    org_slug: str
    iteration_number: int
    section_name: str
    section_order: int
    funder_dialect: str
    operator_override_dialect: str | None
    program_code: str
    admin_risk_register_snapshot_path: str
    admin_risk_snapshot_age_hours: float
    conversation_log_anchor: str | None
    compiled_prompt_shell_sha3_512: str
    compiled_prompt: str
    project_context: Mapping[str, Any]
    envelope_emitted_at_utc: datetime

    # §4 v2.x.5 CC-007 fields (LOCKED 2026-05-16 row 232) — production
    # wire-up reads these to construct the OutboundCallable wrapper around
    # provider_boundary.stdlib_urlopen_caller. Default to empty / Local-Only
    # so existing test fixtures that omit them still construct cleanly.
    classification_context_json: str = ""
    posture: Literal[
        "frontier_eligible", "split_context_hybrid", "local_only_sovereign"
    ] = "local_only_sovereign"

    def __post_init__(self) -> None:
        if self.envelope_version != "scribe-envelope.v1":
            raise ScribeEnvelopeMalformed(
                f"{F_SCRIBE_ENVELOPE_MALFORMED}: envelope_version must be "
                f"'scribe-envelope.v1'; got {self.envelope_version!r}"
            )
        if not self.run_id or not self.run_id.strip():
            raise ScribeEnvelopeMalformed(
                f"{F_SCRIBE_ENVELOPE_MALFORMED}: run_id must be non-empty"
            )
        if not self.org_slug or not self.org_slug.strip():
            raise ScribeEnvelopeMalformed(
                f"{F_SCRIBE_ENVELOPE_MALFORMED}: org_slug must be non-empty"
            )
        if self.iteration_number < 0:
            raise ScribeEnvelopeMalformed(
                f"{F_SCRIBE_ENVELOPE_MALFORMED}: iteration_number must be >= 0; "
                f"got {self.iteration_number!r}"
            )
        if not self.section_name or not self.section_name.strip():
            raise ScribeEnvelopeMalformed(
                f"{F_SCRIBE_ENVELOPE_MALFORMED}: section_name must be non-empty"
            )
        if self.section_order < 1:
            raise ScribeEnvelopeMalformed(
                f"{F_SCRIBE_ENVELOPE_MALFORMED}: section_order must be >= 1; "
                f"got {self.section_order!r}"
            )
        if self.funder_dialect not in _VALID_FUNDER_DIALECTS:
            raise ScribeEnvelopeMalformed(
                f"{F_SCRIBE_ENVELOPE_MALFORMED}: funder_dialect must be one of "
                f"{sorted(_VALID_FUNDER_DIALECTS)}; got {self.funder_dialect!r}"
            )
        if self.admin_risk_snapshot_age_hours < 0.0:
            raise ScribeEnvelopeMalformed(
                f"{F_SCRIBE_ENVELOPE_MALFORMED}: admin_risk_snapshot_age_hours "
                f"must be >= 0.0; got {self.admin_risk_snapshot_age_hours!r}"
            )
        if len(self.compiled_prompt_shell_sha3_512) != 128:
            raise ScribeEnvelopeMalformed(
                f"{F_SCRIBE_ENVELOPE_MALFORMED}: compiled_prompt_shell_sha3_512 "
                f"must be 128 hex chars; got {len(self.compiled_prompt_shell_sha3_512)!r}"
            )
        if self.compiled_prompt_shell_sha3_512 != self.compiled_prompt_shell_sha3_512.lower():
            raise ScribeEnvelopeMalformed(
                f"{F_SCRIBE_ENVELOPE_MALFORMED}: compiled_prompt_shell_sha3_512 "
                f"must be lowercase hex"
            )
        if self.envelope_emitted_at_utc.tzinfo is None:
            raise ScribeEnvelopeMalformed(
                f"{F_SCRIBE_ENVELOPE_MALFORMED}: envelope_emitted_at_utc must be "
                f"timezone-aware"
            )
        # Freeze project_context to MappingProxyType.
        if not isinstance(self.project_context, MappingProxyType):
            object.__setattr__(
                self,
                "project_context",
                MappingProxyType(dict(self.project_context)),
            )


@dataclass(frozen=True, kw_only=True, slots=True)
class ScribeResult:
    """Subprocess stdout payload — frozen, kw-only, slots (A-13)."""

    result_version: str
    run_id: str
    org_slug: str
    iteration_number: int
    section_drafts: tuple[SectionDraft, ...]
    compiled_prompt_shell_sha3_512: str
    provider_landed_family: str
    provider_landed_model_id: str
    admin_risk_flags: tuple[AdminRiskFlag, ...]
    seat_emitted_at_utc: datetime

    def __post_init__(self) -> None:
        if self.result_version != "scribe-result.v1":
            raise ValueError(
                f"ScribeResult.result_version must be 'scribe-result.v1'; got "
                f"{self.result_version!r}"
            )
        if self.iteration_number < 0:
            raise ValueError("iteration_number must be >= 0")
        if not self.section_drafts:
            raise ValueError(
                "ScribeResult.section_drafts must be non-empty — a seat that "
                "fails to draft emits exit 2, not an empty-tuple success"
            )
        if not self.provider_landed_family:
            raise ValueError("provider_landed_family must be non-empty")
        if not self.provider_landed_model_id:
            raise ValueError("provider_landed_model_id must be non-empty")
        if self.seat_emitted_at_utc.tzinfo is None:
            raise ValueError("seat_emitted_at_utc must be timezone-aware")
        if len(self.compiled_prompt_shell_sha3_512) != 128:
            raise ValueError("compiled_prompt_shell_sha3_512 must be 128-hex")


# ---------------------------------------------------------------------------
# E-017 Protocols
# ---------------------------------------------------------------------------


class ClockFn(Protocol):
    """Returns current UTC time; wall-clock seam for determinism tests."""

    def __call__(self) -> datetime: ...


class ResponseParseCallable(Protocol):
    """LLM text_body → (SectionDraft tuple, AdminRiskFlag tuple).

    Isolated from seat.py so the LLM-response schema evolves independently.
    """

    def __call__(
        self,
        *,
        response: AnthropicResponse,
        envelope: ScribeEnvelope,
    ) -> tuple[tuple[SectionDraft, ...], tuple[AdminRiskFlag, ...]]: ...


class PreGateCallable(Protocol):
    """Scribe PRE-gate assembler invocation. Raises ScribeGateFailed on trip."""

    def __call__(
        self,
        *,
        envelope: ScribeEnvelope,
        admin_risk_register: AdminRiskRegister,
    ) -> None: ...


class PostGateCallable(Protocol):
    """Scribe POST-gate assembler invocation. Raises ScribeGateFailed on trip."""

    def __call__(
        self,
        *,
        envelope: ScribeEnvelope,
        section_drafts: tuple[SectionDraft, ...],
        admin_risk_flags: tuple[AdminRiskFlag, ...],
        admin_risk_register: AdminRiskRegister,
    ) -> None: ...


class AdminRiskRegisterFetch(Protocol):
    """Envelope → AdminRiskRegister. Fetches via vault-primitive seam.

    Seated inside seat.py so the admin_risk_adapter module stays pure.
    """

    def __call__(self, *, envelope: ScribeEnvelope) -> AdminRiskRegister: ...


# ---------------------------------------------------------------------------
# Envelope decoder
# ---------------------------------------------------------------------------


def decode_envelope(*, raw_bytes: bytes) -> ScribeEnvelope:
    """Decode stdin bytes into a frozen ScribeEnvelope.

    Raises :class:`ScribeEnvelopeMalformed` on any parse / shape failure.
    """
    if not raw_bytes:
        raise ScribeEnvelopeMalformed(
            f"{F_SCRIBE_ENVELOPE_MALFORMED}: stdin empty"
        )
    try:
        decoded = json.loads(raw_bytes.decode("utf-8"))
    except UnicodeDecodeError as exc:
        raise ScribeEnvelopeMalformed(
            f"{F_SCRIBE_ENVELOPE_MALFORMED}: stdin not UTF-8: {exc}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise ScribeEnvelopeMalformed(
            f"{F_SCRIBE_ENVELOPE_MALFORMED}: stdin is not JSON: {exc}"
        ) from exc
    if not isinstance(decoded, dict):
        raise ScribeEnvelopeMalformed(
            f"{F_SCRIBE_ENVELOPE_MALFORMED}: stdin JSON top-level must be object; "
            f"got {type(decoded).__name__}"
        )
    # envelope_version pin is the first check — fail fast before touching anything.
    version = decoded.get("envelope_version")
    if version != "scribe-envelope.v1":
        raise ScribeEnvelopeMalformed(
            f"{F_SCRIBE_ENVELOPE_MALFORMED}: envelope_version must be "
            f"'scribe-envelope.v1'; got {version!r}"
        )
    # Required keys check.
    required_keys = (
        "envelope_version",
        "run_id",
        "org_slug",
        "iteration_number",
        "section_name",
        "section_order",
        "funder_dialect",
        "program_code",
        "admin_risk_register_snapshot_path",
        "admin_risk_snapshot_age_hours",
        "compiled_prompt_shell_sha3_512",
        "compiled_prompt",
        "project_context",
        "envelope_emitted_at_utc",
    )
    missing = [k for k in required_keys if k not in decoded]
    if missing:
        raise ScribeEnvelopeMalformed(
            f"{F_SCRIBE_ENVELOPE_MALFORMED}: envelope missing keys: {missing!r}"
        )
    # Parse envelope_emitted_at_utc (ISO-8601 offset-aware).
    emit_raw = decoded["envelope_emitted_at_utc"]
    if not isinstance(emit_raw, str):
        raise ScribeEnvelopeMalformed(
            f"{F_SCRIBE_ENVELOPE_MALFORMED}: envelope_emitted_at_utc must be "
            f"ISO-8601 string; got {type(emit_raw).__name__}"
        )
    try:
        emit_dt = datetime.fromisoformat(emit_raw)
    except ValueError as exc:
        raise ScribeEnvelopeMalformed(
            f"{F_SCRIBE_ENVELOPE_MALFORMED}: envelope_emitted_at_utc not ISO-8601: {exc}"
        ) from exc
    project_context = decoded["project_context"]
    if not isinstance(project_context, Mapping):
        raise ScribeEnvelopeMalformed(
            f"{F_SCRIBE_ENVELOPE_MALFORMED}: project_context must be mapping"
        )
    return ScribeEnvelope(
        envelope_version=version,
        run_id=str(decoded["run_id"]),
        org_slug=str(decoded["org_slug"]),
        iteration_number=int(decoded["iteration_number"]),
        section_name=str(decoded["section_name"]),
        section_order=int(decoded["section_order"]),
        funder_dialect=str(decoded["funder_dialect"]),
        operator_override_dialect=(
            str(decoded["operator_override_dialect"])
            if decoded.get("operator_override_dialect") is not None
            else None
        ),
        program_code=str(decoded["program_code"]),
        admin_risk_register_snapshot_path=str(
            decoded["admin_risk_register_snapshot_path"]
        ),
        admin_risk_snapshot_age_hours=float(
            decoded["admin_risk_snapshot_age_hours"]
        ),
        conversation_log_anchor=(
            str(decoded["conversation_log_anchor"])
            if decoded.get("conversation_log_anchor") is not None
            else None
        ),
        compiled_prompt_shell_sha3_512=str(
            decoded["compiled_prompt_shell_sha3_512"]
        ),
        compiled_prompt=str(decoded["compiled_prompt"]),
        project_context=dict(project_context),
        envelope_emitted_at_utc=emit_dt,
    )


# ---------------------------------------------------------------------------
# Result encoder
# ---------------------------------------------------------------------------


def encode_result(result: ScribeResult) -> bytes:
    """Encode a ScribeResult as canonical UTF-8 JSON bytes, trailing newline."""
    payload = {
        "result_version": result.result_version,
        "run_id": result.run_id,
        "org_slug": result.org_slug,
        "iteration_number": result.iteration_number,
        "compiled_prompt_shell_sha3_512": result.compiled_prompt_shell_sha3_512,
        "provider_landed_family": result.provider_landed_family,
        "provider_landed_model_id": result.provider_landed_model_id,
        "seat_emitted_at_utc": result.seat_emitted_at_utc.isoformat(),
        "section_drafts_count": len(result.section_drafts),
        "admin_risk_flags_count": len(result.admin_risk_flags),
        "section_drafts": [
            {
                "section_name": sd.section_name,
                "section_order": sd.section_order,
                "body_text": sd.body_text,
                "word_count": sd.word_count,
                "character_count": sd.character_count,
                "over_limit_flag": sd.over_limit_flag,
                "draft_dialect": sd.draft_dialect,
                "drafted_at_utc": sd.drafted_at_utc.isoformat(),
            }
            for sd in result.section_drafts
        ],
        "admin_risk_flags": [
            {
                "term": f.term,
                "severity": f.severity,
                "proposed_substitution": f.proposed_substitution,
                "applicant_approved": f.applicant_approved,
            }
            for f in result.admin_risk_flags
        ],
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
        "envelope_version": "scribe-envelope.v1",
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
    anthropic_call: AnthropicCallCallable,
    response_parse: ResponseParseCallable,
    pre_gate: PreGateCallable,
    post_gate: PostGateCallable,
    admin_risk_fetch: AdminRiskRegisterFetch,
    anthropic_binding: Any,
) -> int:
    """Subprocess entry. Returns 0/1/2 exit code; does NOT call sys.exit.

    Flow:
      1. Read stdin → decode envelope (version-literal pinned).
      2. Fetch admin-risk register via vault-primitive seam.
      3. Run PRE-gate assembly.
      4. Dispatch Anthropic call.
      5. Parse LLM text_body into SectionDraft tuple + AdminRiskFlag tuple.
      6. Run POST-gate assembly.
      7. Encode ScribeResult → stdout; exit 0.

    Fail-closed at any step → stderr JSON line + exit 2.
    Unexpected exception → stderr traceback + exit 1.
    """
    try:
        raw_bytes = stdin.read()
    except Exception as exc:  # pragma: no cover - stdin failure is a bug-class
        stderr.write(f"stdin read failed: {exc!r}\n".encode("utf-8"))
        return EXIT_INTERNAL_ERROR

    try:
        envelope = decode_envelope(raw_bytes=raw_bytes)
    except ScribeEnvelopeMalformed as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=F_SCRIBE_ENVELOPE_MALFORMED,
            trigger="envelope_decode_failed",
            evidence={"exception": str(exc)},
            clock=clock,
        )
        return EXIT_GATE_FAIL

    try:
        admin_risk_register = admin_risk_fetch(envelope=envelope)
    except ScribeGateFailed as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=exc.failure_code,
            trigger=exc.trigger,
            evidence=exc.evidence,
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except Exception as exc:
        # Defense-in-depth: a non-gate exception from the vault primitive
        # seam is bug-class. Sanitized stderr (class name only).
        stderr.write(
            f"admin_risk_fetch raised unhandled exception class={type(exc).__name__}\n".encode(
                "utf-8"
            )
        )
        return EXIT_INTERNAL_ERROR

    try:
        pre_gate(envelope=envelope, admin_risk_register=admin_risk_register)
    except ScribeGateFailed as exc:
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

    # Sanitize Anthropic-exception messages: pass exception class only into
    # the structured stderr `evidence` field (defense-in-depth against any
    # provider-level error message that might echo prompt text / org id /
    # filesystem paths).
    try:
        response = anthropic_call(
            binding=anthropic_binding,
            compiled_prompt=envelope.compiled_prompt,
            org_slug=envelope.org_slug,
        )
    except AnthropicBYOKMissing as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=F_SCRIBE_BYOK_MISSING,
            trigger="byok_missing",
            evidence={"exception_class": type(exc).__name__, "org_slug": envelope.org_slug},
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except AnthropicPayloadCeiling as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=F_SCRIBE_PAYLOAD_CEILING,
            trigger="payload_ceiling_exceeded",
            evidence={"exception_class": type(exc).__name__},
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except AnthropicTransportFailure as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=F_SCRIBE_TRANSPORT_FAILURE,
            trigger="transport_retry_exhausted",
            evidence={"exception_class": type(exc).__name__},
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except AnthropicSemanticFailure as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=F_SCRIBE_SEMANTIC_FAILURE,
            trigger="semantic_4xx",
            evidence={"exception_class": type(exc).__name__},
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except AnthropicProviderMalformed as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=F_SCRIBE_PROVIDER_MALFORMED,
            trigger="provider_non_json_or_missing_fields",
            evidence={"exception_class": type(exc).__name__},
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except Exception as exc:
        # Defense-in-depth catch for any Anthropic-class exception not
        # enumerated above (forward-compat: provider_anthropic may add new
        # exception subclasses without simultaneously updating seat.py).
        # Treat as bug-class (exit 1) — fail-closed but distinguishable from
        # gate-class trips. Surface only the exception class name (no
        # traceback / repr) — defense-in-depth against operator-environment
        # fingerprint leaks via filesystem paths in tb frames.
        stderr.write(
            f"anthropic_call raised unhandled exception class={type(exc).__name__}\n".encode(
                "utf-8"
            )
        )
        return EXIT_INTERNAL_ERROR

    try:
        section_drafts, admin_risk_flags = response_parse(
            response=response, envelope=envelope
        )
    except ScribeGateFailed as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=exc.failure_code,
            trigger=exc.trigger,
            evidence=exc.evidence,
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except Exception as exc:
        # Response-parse failure is a seat-bug class (exit 1), not gate-class.
        tb = traceback.format_exc()
        stderr.write(f"response_parse raised: {exc!r}\n{tb}\n".encode("utf-8"))
        return EXIT_INTERNAL_ERROR

    try:
        post_gate(
            envelope=envelope,
            section_drafts=section_drafts,
            admin_risk_flags=admin_risk_flags,
            admin_risk_register=admin_risk_register,
        )
    except ScribeGateFailed as exc:
        _emit_stderr_failure(
            stderr=stderr,
            failure_code=exc.failure_code,
            trigger=exc.trigger,
            evidence=exc.evidence,
            clock=clock,
        )
        return EXIT_GATE_FAIL
    except Exception as exc:
        # post_gate raising a non-gate exception is a seat-bug class.
        # Treat as exit 1 (bug-class) — distinct from gate-class fail-closed.
        # Class-name only (no traceback / repr) — same fingerprint-leak
        # discipline as the anthropic_call generic catch above.
        stderr.write(
            f"post_gate raised unhandled exception class={type(exc).__name__}\n".encode(
                "utf-8"
            )
        )
        return EXIT_INTERNAL_ERROR

    try:
        result = ScribeResult(
            result_version="scribe-result.v1",
            run_id=envelope.run_id,
            org_slug=envelope.org_slug,
            iteration_number=envelope.iteration_number,
            section_drafts=section_drafts,
            compiled_prompt_shell_sha3_512=envelope.compiled_prompt_shell_sha3_512,
            provider_landed_family="anthropic",
            provider_landed_model_id=response.landed_model_id,
            admin_risk_flags=admin_risk_flags,
            seat_emitted_at_utc=clock(),
        )
        stdout.write(encode_result(result))
    except Exception as exc:
        tb = traceback.format_exc()
        stderr.write(f"result emission failed: {exc!r}\n{tb}\n".encode("utf-8"))
        return EXIT_INTERNAL_ERROR

    return EXIT_OK


__all__ = [
    # Shapes
    "ScribeEnvelope",
    "ScribeResult",
    # Protocols
    "ClockFn",
    "ResponseParseCallable",
    "PreGateCallable",
    "PostGateCallable",
    "AdminRiskRegisterFetch",
    # Entry point
    "run_seat",
    # Envelope / result codec
    "decode_envelope",
    "encode_result",
    # Exceptions
    "ScribeGateFailed",
    "ScribeEnvelopeMalformed",
    # Constants
    "ENVELOPE_VERSION_V1",
    "RESULT_VERSION_V1",
    "EXIT_OK",
    "EXIT_INTERNAL_ERROR",
    "EXIT_GATE_FAIL",
    # Failure codes
    "F_SCRIBE_SCOPE_MISSING",
    "F_SCRIBE_ORG_CROSS_REF",
    "F_SCRIBE_DIALECT_UNCLASSIFIED",
    "F_SCRIBE_TEMPLATE_UNKNOWN",
    "F_SCRIBE_TEMPLATE_DRIFT",
    "F_SCRIBE_UNSOURCED_CLAIM",
    "F_SCRIBE_PARAPHRASED_NUMERIC",
    "F_SCRIBE_DIALECT_INDUCED_IDENTITY",
    "F_SCRIBE_CONVERSATION_ANCHOR_INVALID",
    "F_SCRIBE_DIALECT_DRIFT",
    "F_SCRIBE_SECTION_OVER_LIMIT_UNFLAGGED",
    "F_SCRIBE_OVERLOOKED_EXPENSE_UNRESOLVED",
    "F_SCRIBE_SMART_INVENTED_METRIC",
    "F_SCRIBE_EVALUATION_CRITERION_MISSING",
    "F_SCRIBE_INELIGIBLE_ACTIVITY",
    "F_SCRIBE_ENVELOPE_MALFORMED",
]
