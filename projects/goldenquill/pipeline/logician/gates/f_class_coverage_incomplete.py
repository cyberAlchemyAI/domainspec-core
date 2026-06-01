"""F-CLASS-COVERAGE-INCOMPLETE — META PRE-cycle gate (Beta-shipping precondition).

Per architecture v7.0.7 §5.1 (LOCKED 2026-05-10 row 180) — the dormant
PRE-cycle gate that prevents Beta deployment shipping with un-realized
F-CLASS-* enforcement.

This is a META gate: its enforcement check is "every v7.0.7 §5.1 code
has a corresponding live module + test in pipeline/logician/gates/".
At Slice 3 LANDED + §4 v2.x amendment LOCK ceremony, the gate
ACTIVATES — every Beta cycle thereafter runs the COVERAGE check at
cycle start and fail-closes if any of the eleven other F-CLASS-*
codes lacks a live module + test.

Per L-006 dormant-binding pattern, the gate is on-disk evidence at v7
LOCK; the realization at WS-L Slice 3 fires the binding. Operator-
visible: the Classification Review stage at white-glove cannot
complete its step-4 test cycle without this coverage. After §4 v2.x
LOCKs, the gate ALWAYS fires green (every code has its module + test);
re-running it on every cycle start protects against tampering with the
pipeline tree post-deployment.

Bypass: NO M13 — this gate is the architectural commitment binding.
Beta deployment cannot ship without classification-driven routing
realization; bypassing the binding bypasses the structural sovereignty
claim.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final, Optional, Sequence

from pipeline.logician.gates._protocols import FileExistsCallable


F_CLASS_COVERAGE_INCOMPLETE: Final[str] = "F-CLASS-COVERAGE-INCOMPLETE"

# Canonical F-CLASS-* codes with v7.0.10 voice-STT coverage folded in.
# The total excludes F-CLASS-COVERAGE-INCOMPLETE itself; the
# coverage gate excludes itself from the verification target (it's the
# auditor, not the auditee).
REQUIRED_F_CLASS_CODES: Final[tuple[str, ...]] = (
    "F-CLASS-REGISTER-MISSING",
    "F-CLASS-REGISTER-UNSIGNED",
    "F-CLASS-REGISTER-SIGNATURE-INVALID",
    "F-CLASS-REGISTER-HASH-MISMATCH",
    "F-CLASS-NEW-FACT-UNCLASSIFIED",
    "F-CLASS-ROUTING-INDETERMINATE",
    "F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL",
    "F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED",
    "F-CLASS-SLOT-ID-NON-OPAQUE",
    "F-CLASS-PER-GRANT-OVERRIDE-UNSIGNED",
    "F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID",
    "F-CLASS-HIGH-STAKES-FLAG-LEAK",
    "F-CLASS-VOICE-CONFIDENTIAL-CLOUD-STT",
)


@dataclass(frozen=True, kw_only=True)
class CoverageEntry:
    """Per-code coverage assertion — one module path + one test path.

    Each F-CLASS-* code (other than F-CLASS-COVERAGE-INCOMPLETE itself)
    must have both a module file AND a test file on disk for the META
    gate to PASS.
    """

    code: str
    module_path: str
    test_path: str


@dataclass(frozen=True, kw_only=True)
class CoverageIncompleteResult:
    """Result of F-CLASS-COVERAGE-INCOMPLETE check."""

    success: bool
    failure_code: Optional[str]
    detail: str
    missing_codes: tuple[str, ...] = field(default_factory=tuple)
    missing_modules: tuple[str, ...] = field(default_factory=tuple)
    missing_tests: tuple[str, ...] = field(default_factory=tuple)


def check_class_coverage_incomplete(
    *,
    coverage_entries: Sequence[CoverageEntry],
    file_exists: FileExistsCallable,
) -> CoverageIncompleteResult:
    """META PRE-cycle gate: every required F-CLASS-* code has live module + test.

    Verifies that every code in :data:`REQUIRED_F_CLASS_CODES` is
    represented in ``coverage_entries`` AND that both files exist on
    disk according to ``file_exists``.

    Parameters
    ----------
    coverage_entries
        One per F-CLASS-* code (excluding F-CLASS-COVERAGE-INCOMPLETE
        itself). The orchestrator constructs this sequence from a
        registry; the gate verifies on-disk presence via the injected
        callable.
    file_exists
        Injected :class:`FileExistsCallable`. Gate never reads the
        filesystem directly per AST-lint R3.

    Returns
    -------
    CoverageIncompleteResult. PASS only when every required code has
    a live module + test on disk. FAIL with itemized
    missing_codes / missing_modules / missing_tests on any gap.
    """
    by_code = {entry.code: entry for entry in coverage_entries}

    missing_codes: list[str] = []
    missing_modules: list[str] = []
    missing_tests: list[str] = []

    for required_code in REQUIRED_F_CLASS_CODES:
        entry = by_code.get(required_code)
        if entry is None:
            missing_codes.append(required_code)
            continue

        module_path = entry.module_path
        test_path = entry.test_path
        try:
            module_present = file_exists(module_path)
        except Exception as exc:  # noqa: BLE001 — fail-closed
            return CoverageIncompleteResult(
                success=False,
                failure_code=F_CLASS_COVERAGE_INCOMPLETE,
                detail=(
                    f"file_exists raised {type(exc).__name__}: {exc} on "
                    f"module_path={module_path!r} for code={required_code!r}"
                ),
            )
        try:
            test_present = file_exists(test_path)
        except Exception as exc:  # noqa: BLE001 — fail-closed
            return CoverageIncompleteResult(
                success=False,
                failure_code=F_CLASS_COVERAGE_INCOMPLETE,
                detail=(
                    f"file_exists raised {type(exc).__name__}: {exc} on "
                    f"test_path={test_path!r} for code={required_code!r}"
                ),
            )

        if module_present is not True:
            missing_modules.append(f"{required_code}={module_path}")
        if test_present is not True:
            missing_tests.append(f"{required_code}={test_path}")

    if missing_codes or missing_modules or missing_tests:
        gaps: list[str] = []
        if missing_codes:
            gaps.append(
                "missing coverage entries for codes: "
                + ", ".join(missing_codes[:5])
            )
        if missing_modules:
            gaps.append(
                "module files missing on disk: "
                + ", ".join(missing_modules[:5])
            )
        if missing_tests:
            gaps.append(
                "test files missing on disk: "
                + ", ".join(missing_tests[:5])
            )
        return CoverageIncompleteResult(
            success=False,
            failure_code=F_CLASS_COVERAGE_INCOMPLETE,
            detail=(
                "F-CLASS-* coverage incomplete — Beta deployment cannot ship "
                "until §4 v2.x WS-L Slice 3 closes every gap: "
                + " | ".join(gaps)
                + " (no M13 bypass — architectural commitment binding)"
            ),
            missing_codes=tuple(missing_codes[:5]),
            missing_modules=tuple(missing_modules[:5]),
            missing_tests=tuple(missing_tests[:5]),
        )

    return CoverageIncompleteResult(
        success=True,
        failure_code=None,
        detail=(
            f"F-CLASS-* coverage complete — all "
            f"{len(REQUIRED_F_CLASS_CODES)} required codes have live "
            "module + test files on disk; Beta cycle may proceed"
        ),
    )


__all__ = [
    "CoverageEntry",
    "CoverageIncompleteResult",
    "F_CLASS_COVERAGE_INCOMPLETE",
    "REQUIRED_F_CLASS_CODES",
    "check_class_coverage_incomplete",
]
