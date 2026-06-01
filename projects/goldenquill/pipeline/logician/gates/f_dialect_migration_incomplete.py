"""F-DIALECT-MIGRATION-INCOMPLETE — admin_risk_register migration completeness.

PRE-gate at order 6.56 (between F-DIALECT-POLITICAL-AXIS-LEAK at 6.55 which
verifies schema shape, and F-CIC-CLC-MATCH-NULL at 6.6 — structural correctness
before content correctness, per Cycle 2 fold-in JD-C2-LOW-1). Fires at LOCK
ceremony pre-flight AND on admin_risk_register reload. Fail-closed.

Authority: ``pipeline/blueprint/v0.1/section_04_logician_v2_x_apolitical_dialect.md``
§4.X.6 (Cycle 1 fold-in FI-7b new failure code; LOCKED 2026-05-16T14:00:00Z;
lock_history rows 236/249). Per Cycle 2 fold-ins C2-H-4 + C2-NEW-MED-2 +
C2-NEW-HIGH-3 + C2-NEW-MED-4.

Rationale
---------
Architecture v7.0.12 §1.2 retires ``progressive_register`` on every
admin_risk_register entry and replaces it with ``per_clc_register`` (a map of
CLC slug → AVOID|OK|EXPECTED|PREFERRED, defaulting to AVOID-everywhere).
Per FI-7 REVISED, **no inherited heuristic mapping** from the prior
``progressive_register`` value is applied — every existing term must be
re-audited by the operator (~75 terms × 8 CLCs = ~75 decisions × 3-5 min each =
4-6 hours operator work). The audit decisions live in
``pipeline/institutional_memory/admin_risk_register_audit_decisions.md`` (one
row per term, with a per-term Ed25519 signature pair from the operator).

This gate refuses LOCK ceremony or admin_risk_register reload unless every
term in the register either (a) has a non-empty ``per_clc_register`` map, OR
(b) has a signed audit-decision row in ``admin_risk_register_audit_decisions.md``
explicitly recording ``audit_status: confirmed_avoid_all`` (per C2-NEW-MED-2)
and bearing a per-term Ed25519 signature (per C2-H-4).

Subcodes
--------
- ``F-DIALECT-MIGRATION-INCOMPLETE.unaudited_term`` — admin_risk_register
  term has empty ``per_clc_register`` AND no signed audit decision row.
- ``F-DIALECT-MIGRATION-INCOMPLETE.audit_decisions_missing`` —
  ``admin_risk_register_audit_decisions.md`` file absent at gate trigger
  (C2-NEW-MED-4: try/except wraps file-read so missing file surfaces as a
  clean FAIL with this sub-tag instead of an uncaught traceback).
- ``F-DIALECT-MIGRATION-INCOMPLETE.per_term_signature_missing`` — term has
  audit row but per-term Ed25519 signature absent (C2-H-4: single-file-
  signature shortcut closed — rubber-stamp bypass not possible).
- ``F-DIALECT-MIGRATION-INCOMPLETE.predicate_body_not_deployed`` — pre-LOCK
  module-check failed; ``f_dialect_migration_incomplete.py`` either
  un-importable OR raises ``NotImplementedError`` (C2-NEW-HIGH-3: pre-LOCK
  predicate-deployment check).
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Final, Iterable, Mapping, Optional, Protocol, runtime_checkable


GATE_ID: Final[str] = "F-DIALECT-MIGRATION-INCOMPLETE"
PRE_GATE_ORDER: Final[float] = 6.56


# ---------------------------------------------------------------------------
# Audit-decision status enum
# ---------------------------------------------------------------------------

AUDIT_STATUS_CONFIRMED_AVOID_ALL: Final[str] = "confirmed_avoid_all"
"""C2-NEW-MED-2: distinguishes operator-audited AVOID-everywhere from
unaudited default. Only this exact value satisfies the audited-AVOID gate
arm; any other status (or missing status) is treated as unaudited."""

AUDIT_STATUS_CONFIRMED_PER_CLC: Final[str] = "confirmed_per_clc"
"""Operator audited the term and supplied per-CLC registers."""


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class MigrationIncompleteFinding:
    """One detection of an unmigrated / under-audited admin_risk_register term.

    ``term_hash`` is a SHA3-256 hex digest of the term + its severity
    (per the audit-decisions discipline) and serves as the unambiguous
    identifier. The raw term value is preserved in ``term`` because the
    register is operator-curated and not PII-bearing; if the term itself
    is sensitive (e.g., a flagged phrase containing applicant context), the
    operator marks it for hash-only emission via the audit decision row.
    """

    subcode: str
    term: str
    term_hash: str
    detail: str


@dataclass(frozen=True, kw_only=True)
class MigrationIncompleteResult:
    """Result of a full migration-completeness check.

    ``passed=True`` means every term either has a non-empty per_clc_register
    OR a signed audit-decision row with status confirmed_avoid_all. Cycle /
    LOCK proceeds.

    ``passed=False`` means at least one term is unaudited / under-signed /
    the audit file is missing. Refuses LOCK ceremony OR admin_risk_register
    reload at runtime.
    """

    passed: bool
    findings: tuple[MigrationIncompleteFinding, ...]

    # Stage-aware fields (Consulting Node Doctrine)
    has_findings: bool = False
    blocking: bool = True
    advisory_only: bool = False
    requires_handoff_disclosure: bool = False


# ---------------------------------------------------------------------------
# Injected dependencies
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class AdminRiskRegisterEntry:
    """One entry from the admin_risk_register canonical YAML."""

    term: str
    severity: str  # RED | YELLOW | GREEN
    per_clc_register: Mapping[str, str]  # CLC slug → AVOID|OK|EXPECTED|PREFERRED


@dataclass(frozen=True, kw_only=True)
class AuditDecisionRow:
    """One row from admin_risk_register_audit_decisions.md.

    The decisions file is operator-authored markdown with a structured table;
    the caller parses each table row into one of these dataclasses before
    handing the gate the parsed view.
    """

    term: str
    term_hash: str
    audit_status: str  # confirmed_avoid_all | confirmed_per_clc
    operator_ed25519_signature_hex: Optional[str]
    operator_pubkey_ed25519_hex: Optional[str]


@runtime_checkable
class AdminRiskRegisterReaderCallable(Protocol):
    """Returns the parsed admin_risk_register entry list."""

    def __call__(self) -> Iterable[AdminRiskRegisterEntry]: ...


@runtime_checkable
class AuditDecisionsReaderCallable(Protocol):
    """Returns the parsed audit-decisions row list, OR raises
    ``FileNotFoundError`` if the audit-decisions file does not exist (the
    gate catches this and emits ``.audit_decisions_missing`` per
    C2-NEW-MED-4)."""

    def __call__(self) -> Iterable[AuditDecisionRow]: ...


@runtime_checkable
class SignatureVerifierCallable(Protocol):
    """Verifies that ``signature_hex`` is a valid Ed25519 signature on
    the canonical bytes of ``(term, term_hash, audit_status)`` under
    ``pubkey_hex``. Returns True / False."""

    def __call__(
        self,
        *,
        term: str,
        term_hash: str,
        audit_status: str,
        signature_hex: str,
        pubkey_hex: str,
    ) -> bool: ...


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _term_hash(term: str, severity: str) -> str:
    """SHA3-256 hex digest of ``term||\\0||severity``. Stable identifier
    used to match register entries against audit-decision rows."""
    import hashlib

    return hashlib.sha3_256(
        f"{term}\x00{severity}".encode("utf-8")
    ).hexdigest()


# ---------------------------------------------------------------------------
# C2-NEW-HIGH-3 — pre-LOCK predicate deployment check
# ---------------------------------------------------------------------------


def check_predicate_body_deployed(
    *,
    module_dotted_path: str = (
        "pipeline.logician.gates.f_dialect_migration_incomplete"
    ),
) -> Optional[MigrationIncompleteFinding]:
    """C2-NEW-HIGH-3: verify the gate module is importable AND its ``run``
    function does not raise ``NotImplementedError`` on a smoke probe.

    Returns ``None`` if the predicate body is deployed and live; returns a
    finding (with subcode ``.predicate_body_not_deployed``) otherwise. The
    LOCK ceremony driver calls this before executing the gate proper —
    catches the case where someone landed the §0.5 row registration but the
    predicate body is still a ``NotImplementedError`` stub.
    """
    try:
        mod = importlib.import_module(module_dotted_path)
    except ImportError as exc:
        return MigrationIncompleteFinding(
            subcode=f"{GATE_ID}.predicate_body_not_deployed",
            term="<predicate_module>",
            term_hash=_term_hash(module_dotted_path, "<module>"),
            detail=(
                f"predicate module {module_dotted_path!r} is not importable: "
                f"{exc!r}; C2-NEW-HIGH-3 fail-closed"
            ),
        )
    run_fn = getattr(mod, "run", None)
    if run_fn is None:
        return MigrationIncompleteFinding(
            subcode=f"{GATE_ID}.predicate_body_not_deployed",
            term="<predicate_module>",
            term_hash=_term_hash(module_dotted_path, "<module>"),
            detail=(
                f"predicate module {module_dotted_path!r} has no `run` "
                "callable; C2-NEW-HIGH-3 fail-closed"
            ),
        )
    # Smoke probe: empty sources should not raise.
    try:
        _ = run_fn(
            admin_risk_register_reader=lambda: iter([]),
            audit_decisions_reader=lambda: iter([]),
            signature_verifier=lambda **_k: True,
        )
    except NotImplementedError as exc:
        return MigrationIncompleteFinding(
            subcode=f"{GATE_ID}.predicate_body_not_deployed",
            term="<predicate_module>",
            term_hash=_term_hash(module_dotted_path, "<module>"),
            detail=(
                f"predicate body raises NotImplementedError on smoke probe: "
                f"{exc!r}; C2-NEW-HIGH-3 fail-closed"
            ),
        )
    except Exception:
        # Any other exception on the empty-source smoke probe is itself a
        # bug — but it is NOT a "not deployed" sub-tag situation. Surface
        # it via the standard exception ladder rather than swallowing.
        raise
    return None


# ---------------------------------------------------------------------------
# Gate entry point
# ---------------------------------------------------------------------------


from pipeline.logician.types import OutputType, GateStage, ArtifactType, FINAL_OR_SUBMISSION_STAGES

def run(
    *,
    admin_risk_register_reader: AdminRiskRegisterReaderCallable,
    audit_decisions_reader: AuditDecisionsReaderCallable,
    signature_verifier: SignatureVerifierCallable,
    output_type: OutputType = "FIT_FARMS_SUBMISSION_PACKET",
    stage: GateStage = "final_export_attempt",
    artifact_type: ArtifactType = "pdf",
) -> MigrationIncompleteResult:
    """Run the migration-completeness check on the admin_risk_register.

    Algorithm:

    1. Read the register entries.
    2. Attempt to read the audit-decisions file; if missing, emit
       ``.audit_decisions_missing`` for the first unaudited term and
       short-circuit (no point checking signatures against an absent file).
    3. For each register entry whose ``per_clc_register`` is non-empty,
       skip (already migrated).
    4. For each entry whose ``per_clc_register`` is empty:
       a. Look up the matching audit-decision row by ``term_hash``.
       b. If no matching row exists → ``.unaudited_term``.
       c. If the row exists but ``audit_status != confirmed_avoid_all`` →
          ``.unaudited_term`` (the only audit status that authorizes empty
          per_clc_register is ``confirmed_avoid_all``; ``confirmed_per_clc``
          requires the per_clc_register to actually be populated).
       d. If the row exists with the correct status but
          ``operator_ed25519_signature_hex`` is missing → ``.per_term_signature_missing``.
       e. If the signature is present but verification fails →
          ``.per_term_signature_missing``.

    All findings aggregated; ``passed = len(findings) == 0``.
    """
    findings: list[MigrationIncompleteFinding] = []

    # Read the audit decisions, catching missing-file with a clean sub-tag
    # per C2-NEW-MED-4.
    try:
        audit_rows = list(audit_decisions_reader())
        audit_decisions_present = True
    except FileNotFoundError as exc:
        audit_rows = []
        audit_decisions_present = False
        # The detail mentions the original exception so operator can trace
        # the missing-file location.
        findings.append(
            MigrationIncompleteFinding(
                subcode=f"{GATE_ID}.audit_decisions_missing",
                term="<audit_decisions_file>",
                term_hash=_term_hash(
                    "admin_risk_register_audit_decisions.md", "<file>"
                ),
                detail=(
                    "admin_risk_register_audit_decisions.md absent at gate "
                    f"trigger ({exc!r}); cards-ceremony must produce this "
                    "file with one signed row per term before LOCK or "
                    "register-reload proceeds (C2-NEW-MED-4)"
                ),
            )
        )

    # Build lookup: term_hash → list[AuditDecisionRow].
    by_hash: dict[str, list[AuditDecisionRow]] = {}
    for row in audit_rows:
        by_hash.setdefault(row.term_hash, []).append(row)

    for entry in admin_risk_register_reader():
        # If per_clc_register is non-empty, this term is already migrated.
        if len(entry.per_clc_register) > 0:
            continue
        # Empty per_clc_register → need a signed audit-decision row.
        if not audit_decisions_present:
            # The .audit_decisions_missing finding already covers the case.
            # Add a per-term .unaudited_term to surface the specific terms
            # the operator must address.
            findings.append(
                MigrationIncompleteFinding(
                    subcode=f"{GATE_ID}.unaudited_term",
                    term=entry.term,
                    term_hash=_term_hash(entry.term, entry.severity),
                    detail=(
                        f"term {entry.term!r} (severity {entry.severity!r}) "
                        "has empty per_clc_register and no audit-decisions "
                        "file present"
                    ),
                )
            )
            continue
        term_hash = _term_hash(entry.term, entry.severity)
        matching = by_hash.get(term_hash, [])
        if not matching:
            findings.append(
                MigrationIncompleteFinding(
                    subcode=f"{GATE_ID}.unaudited_term",
                    term=entry.term,
                    term_hash=term_hash,
                    detail=(
                        f"term {entry.term!r} (severity {entry.severity!r}) "
                        "has empty per_clc_register and no matching audit-"
                        "decision row; operator must audit this term per "
                        "FI-7 REVISED"
                    ),
                )
            )
            continue
        # We have at least one matching audit row.
        eligible_rows = [
            r for r in matching
            if r.audit_status == AUDIT_STATUS_CONFIRMED_AVOID_ALL
        ]
        if not eligible_rows:
            findings.append(
                MigrationIncompleteFinding(
                    subcode=f"{GATE_ID}.unaudited_term",
                    term=entry.term,
                    term_hash=term_hash,
                    detail=(
                        f"term {entry.term!r} audit-decision row exists but "
                        f"audit_status != {AUDIT_STATUS_CONFIRMED_AVOID_ALL!r}; "
                        "empty per_clc_register requires explicit "
                        "confirmed_avoid_all decision (C2-NEW-MED-2)"
                    ),
                )
            )
            continue
        # Signature check (C2-H-4 per-term Ed25519).
        signed = False
        for row in eligible_rows:
            if not row.operator_ed25519_signature_hex or not row.operator_pubkey_ed25519_hex:
                continue
            try:
                ok = signature_verifier(
                    term=row.term,
                    term_hash=row.term_hash,
                    audit_status=row.audit_status,
                    signature_hex=row.operator_ed25519_signature_hex,
                    pubkey_hex=row.operator_pubkey_ed25519_hex,
                )
            except Exception:
                ok = False
            if ok:
                signed = True
                break
        if not signed:
            findings.append(
                MigrationIncompleteFinding(
                    subcode=f"{GATE_ID}.per_term_signature_missing",
                    term=entry.term,
                    term_hash=term_hash,
                    detail=(
                        f"term {entry.term!r} has eligible audit-decision row "
                        "but per-term Ed25519 signature is missing or "
                        "verification failed; per-term sig required to close "
                        "single-file-signature shortcut (C2-H-4)"
                    ),
                )
            )

    has_findings = len(findings) > 0
    blocking = has_findings
    advisory_only = False
    requires_handoff_disclosure = False

    if has_findings:
        if output_type == "THIRD_PARTY_DRAFT_DELIVERABLE":
            if stage not in FINAL_OR_SUBMISSION_STAGES:
                blocking = False
                advisory_only = True
                requires_handoff_disclosure = True
        else:
            if stage in ("draft_generation", "draft_review"):
                blocking = False
                advisory_only = True

    return MigrationIncompleteResult(
        passed=not has_findings,
        findings=tuple(findings),
        has_findings=has_findings,
        blocking=blocking,
        advisory_only=advisory_only,
        requires_handoff_disclosure=requires_handoff_disclosure,
    )


__all__ = [
    "GATE_ID",
    "PRE_GATE_ORDER",
    "AUDIT_STATUS_CONFIRMED_AVOID_ALL",
    "AUDIT_STATUS_CONFIRMED_PER_CLC",
    "AdminRiskRegisterEntry",
    "AdminRiskRegisterReaderCallable",
    "AuditDecisionRow",
    "AuditDecisionsReaderCallable",
    "MigrationIncompleteFinding",
    "MigrationIncompleteResult",
    "SignatureVerifierCallable",
    "check_predicate_body_deployed",
    "run",
]
