"""Pure deterministic ChapterRun state-core identity surface."""

from .canonical import (
    CanonicalIdentity,
    canonical_bytes,
    canonical_identity,
    canonical_sha256,
)
from .model import (
    DERIVATIVE_PROFILE_ORDER,
    DERIVATIVE_STATES,
    EFFECT_STATES,
    MANUSCRIPT_STATES,
    RUN_PHASES,
    SUPPORTED_SCHEMA_ID,
    SUPPORTED_SCHEMA_VERSION,
    TERMINAL_OUTCOMES,
    ChapterRun,
    ChapterRunValidationError,
    Diagnostic,
    DiagnosticCode,
    ValidationResult,
    validate_chapter_run,
)

__all__ = [
    "DERIVATIVE_PROFILE_ORDER",
    "DERIVATIVE_STATES",
    "EFFECT_STATES",
    "MANUSCRIPT_STATES",
    "RUN_PHASES",
    "SUPPORTED_SCHEMA_ID",
    "SUPPORTED_SCHEMA_VERSION",
    "TERMINAL_OUTCOMES",
    "CanonicalIdentity",
    "ChapterRun",
    "ChapterRunValidationError",
    "Diagnostic",
    "DiagnosticCode",
    "ValidationResult",
    "canonical_bytes",
    "canonical_identity",
    "canonical_sha256",
    "validate_chapter_run",
]
