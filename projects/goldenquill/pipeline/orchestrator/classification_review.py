"""Classification Review operator UX wrapper — v0.1 Beta.

Authority
---------
Architecture v7.0.7 §3 + §3.6 + §3.7 LOCKED 2026-05-10 (row 180).
Architecture v7.0.10 §1.4 LOCKED 2026-05-11 (row 215) — Classification Review
step 3 + step 4 amended to add deployment-posture selection alongside per-field
classification. The per-field 4-class enum (public/shareable/confidential/
operator_flagged) is unchanged at v7.0.10; the v7.0.10 addition is a separate
deployment-scope 3-posture enum (frontier_eligible / split_context_hybrid /
local_only_sovereign). The signed register at v7.0.10 attests to BOTH per-field
classifications AND the selected posture; F-CLASS-REGISTER-* gates carry sub-tag
extensions for the posture-signature trail (`.posture_unsigned` / `.posture_invalid`
/ `.posture_hash_mismatch`).

White-glove playbook §2 (`docs/white_glove_v0_1_beta.md`).

What this module is
-------------------
The operator-facing workflow that consumes Intake-proposed classifications
for a single document, walks the operator through per-field confirm /
override decisions, persists per-document evidence, and commits the final
classifications into the per-org classification register at the canonical
path the F-CLASS-REGISTER-* gates check.

Sequence
--------
1. ``load_proposed_classifications`` — read the Intake-produced proposal
   artifact at ``orgs/<slug>/classification_review/proposals/<doc-hash>.proposed.yaml``.
2. ``apply_operator_decisions`` — apply per-field operator decisions
   (confirm / override). Pure transformation; no I/O.
3. ``write_audit_entries`` — append one JSONL line per override to
   ``orgs/<slug>/classification_review/audit_log.jsonl``.
4. ``write_signed_review_artifact`` — per-document
   ``classification_review_<doc-hash>.yaml`` under ``signed/`` carries the
   field decisions, attestation_string, and Ed25519 signature.
5. ``commit_to_register`` — upsert per-field classifications into
   ``orgs/<slug>/vault/classification/register.yaml`` (creates if absent).
6. ``sign_register`` — append the
   ``operator_signature_at_white_glove_completion`` block per §3.7.
7. ``verify_register_against_class_gates`` — wires the orchestrator output
   through the existing F-CLASS-REGISTER-MISSING / -UNSIGNED /
   -SIGNATURE-INVALID / -HASH-MISMATCH gates so the F-CLASS-COVERAGE-
   INCOMPLETE PRE-cycle precondition is satisfied for the per-org artifact.

Path conventions
----------------
Per v7.0.7 §3.7 + white-glove playbook §2.4:

* Per-org persistent register (gate-checked):
  ``orgs/<slug>/vault/classification/register.yaml``
* Per-document operator review evidence:
  ``orgs/<slug>/classification_review/proposals/<doc-hash>.proposed.yaml``
  ``orgs/<slug>/classification_review/signed/classification_review_<doc-hash>.yaml``
* Per-org override audit log (override = operator flipped Card-default):
  ``orgs/<slug>/classification_review/audit_log.jsonl``

Crypto discipline
-----------------
The orchestrator is a *caller layer* — direct use of
``cryptography.hazmat.primitives.asymmetric.ed25519`` and ``hashlib.sha3_512``
is permitted (the AST-lint R3 LOGICIAN_OPEN_BAN applies to gate modules
under ``pipeline/logician/gates/``, not to orchestrators / CLIs which are
the sanctioned I/O layer). Tests inject pre-built keypairs via
``signing_key_bytes`` / ``verifying_key_bytes`` to avoid touching the
operator's real keystore.

Determinism
-----------
* No wall clocks at module scope; ``now_utc_iso8601`` is injected.
* No random keypair generation inside this module — caller supplies
  Ed25519 ``signing_key_bytes`` (32 bytes raw) + ``verifying_key_bytes``
  (32 bytes raw).
* Canonicalization for hash inputs is JSON with ``sort_keys=True,
  separators=(",", ":")``; the same canonicalization is applied at sign
  time and at gate verify time.
"""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Final, Mapping, Optional, Sequence

import yaml
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

from pipeline.logician.gates.f_class_register import (
    F_CLASS_REGISTER_HASH_MISMATCH,
    F_CLASS_REGISTER_MISSING,
    F_CLASS_REGISTER_SIGNATURE_INVALID,
    F_CLASS_REGISTER_UNSIGNED,
    SIGN_OFF_HASH_CLASS_KEY,
    SIGN_OFF_HASH_FIELDS_KEY,
    SIGN_OFF_KEY,
    ClassRegisterResult,
    check_class_register_hash_mismatch,
    check_class_register_missing,
    check_class_register_signature_invalid,
    check_class_register_unsigned,
)


# ---------------------------------------------------------------------------
# Public constants
# ---------------------------------------------------------------------------


CLASS_PUBLIC: Final[str] = "public"
CLASS_SHAREABLE: Final[str] = "shareable"
CLASS_CONFIDENTIAL: Final[str] = "confidential"
CLASS_OPERATOR_FLAGGED: Final[str] = "operator_flagged"

PERMITTED_CLASSES: Final[frozenset[str]] = frozenset(
    {CLASS_PUBLIC, CLASS_SHAREABLE, CLASS_CONFIDENTIAL, CLASS_OPERATOR_FLAGGED}
)

# Deployment posture vocabulary per architecture v7.0.10 LOCKED 2026-05-11 §1.1.
# Operator-selected at Classification Review step 3 + Ed25519-signed at step 4.
# Customer-facing names from v7.0.10 §1.1 (operator-facing wording).
POSTURE_FRONTIER_ELIGIBLE: Final[str] = "frontier_eligible"
POSTURE_SPLIT_CONTEXT_HYBRID: Final[str] = "split_context_hybrid"
POSTURE_LOCAL_ONLY_SOVEREIGN: Final[str] = "local_only_sovereign"

PERMITTED_POSTURES: Final[frozenset[str]] = frozenset(
    {
        POSTURE_FRONTIER_ELIGIBLE,
        POSTURE_SPLIT_CONTEXT_HYBRID,
        POSTURE_LOCAL_ONLY_SOVEREIGN,
    }
)

# Customer-facing display labels (CLI step-3 routing-simulation surface).
POSTURE_DISPLAY_LABELS: Final[dict[str, str]] = {
    POSTURE_FRONTIER_ELIGIBLE: "Frontier-Eligible",
    POSTURE_SPLIT_CONTEXT_HYBRID: "Split-Context Hybrid",
    POSTURE_LOCAL_ONLY_SOVEREIGN: "Local-Only / Sovereign",
}

# One-paragraph operator-facing descriptions (v7.0.10 §1.1 wording).
POSTURE_DESCRIPTIONS: Final[dict[str, str]] = {
    POSTURE_FRONTIER_ELIGIBLE: (
        "Customer permits selected project data to route to external/frontier "
        "models. Tilth assigns the strongest available model to each role per "
        "benchmark fit, prior results, task type, and cost/performance. "
        "Confidential + operator-flagged fields remain local even under this "
        "posture; the posture authorizes cloud routing for non-Confidential "
        "content only."
    ),
    POSTURE_SPLIT_CONTEXT_HYBRID: (
        "Frontier models help with structure, section strategy, prompts, "
        "funder-language framing, and generic draft scaffolds — operating only "
        "on the operator-signed Split-Context allow-list (RFA text + funder "
        "agency name + funder rubric + program template name + section structure "
        "+ KGIE keywords + dialect classification). Confidential local data stays "
        "on the node. A local model inserts restricted facts, evidence, metrics, "
        "names, and applicant-specific substance. No opaque-slot rendering "
        "round-trip."
    ),
    POSTURE_LOCAL_ONLY_SOVEREIGN: (
        "All drafting, review, routing, and evidence use remain local. Maximum-"
        "custody posture, but marked as performance-dependent / under validation "
        "until proven against real grant workloads. Heavy-Judge swap to 200B-class "
        "local model fires under same operator-flag discipline."
    ),
}

# v7.0.10 deprecation footnote — "Sanitized" / opaque-slot-token posture was
# deprecated at v7.0.10 LOCK 2026-05-11. The two enforcement gates remain live
# as defense-in-depth (firing = bug or attack). The CLI never offers Sanitized
# as a selectable option; this constant exists so callers can detect attempts
# to set the field to the deprecated value and surface an explicit error.
DEPRECATED_POSTURE_SANITIZED: Final[str] = "sanitized"

ACTION_CONFIRMED: Final[str] = "confirmed"
ACTION_OVERRIDDEN: Final[str] = "overridden"

PERMITTED_ACTIONS: Final[frozenset[str]] = frozenset(
    {ACTION_CONFIRMED, ACTION_OVERRIDDEN}
)

# Schema versions
PROPOSAL_SCHEMA_VERSION: Final[str] = "classification_review.proposal.v1"
SIGNED_REVIEW_SCHEMA_VERSION: Final[str] = "classification_review.signed.v1"
REGISTER_SCHEMA_VERSION: Final[str] = "classification_register.v1"

# Path templates (relative to repo_root)
PROPOSAL_PATH_TEMPLATE: Final[str] = (
    "orgs/{org_slug}/classification_review/proposals/{doc_hash}.proposed.yaml"
)
SIGNED_REVIEW_PATH_TEMPLATE: Final[str] = (
    "orgs/{org_slug}/classification_review/signed/"
    "classification_review_{doc_hash}.yaml"
)
AUDIT_LOG_PATH_TEMPLATE: Final[str] = (
    "orgs/{org_slug}/classification_review/audit_log.jsonl"
)
REGISTER_PATH_TEMPLATE: Final[str] = (
    "orgs/{org_slug}/vault/classification/register.yaml"
)


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class ClassificationReviewError(RuntimeError):
    """Common parent for orchestrator failures."""

    code: str = "F-CLASSIFICATION-REVIEW"


class ProposalNotFound(ClassificationReviewError):
    """Proposal artifact does not exist at the expected path."""

    code = "F-CLASSIFICATION-REVIEW-PROPOSAL-MISSING"


class ProposalSchemaError(ClassificationReviewError):
    """Proposal artifact present but schema does not match expectations."""

    code = "F-CLASSIFICATION-REVIEW-PROPOSAL-SCHEMA-INVALID"


class DecisionCoverageGap(ClassificationReviewError):
    """Operator decisions do not cover every proposed field."""

    code = "F-CLASSIFICATION-REVIEW-DECISION-COVERAGE-GAP"


class InvalidClassValue(ClassificationReviewError):
    """A decision specifies a class outside the permitted four-value set."""

    code = "F-CLASSIFICATION-REVIEW-INVALID-CLASS"


class InvalidPostureValue(ClassificationReviewError):
    """A posture selection is outside the permitted three-value set.

    Per architecture v7.0.10 LOCKED 2026-05-11 §1.1, the only admissible
    posture values are :data:`POSTURE_FRONTIER_ELIGIBLE`,
    :data:`POSTURE_SPLIT_CONTEXT_HYBRID`, and
    :data:`POSTURE_LOCAL_ONLY_SOVEREIGN`. The pre-v7.0.10 fourth posture
    ("Sanitized" / opaque-slot-token) is deprecated; passing
    :data:`DEPRECATED_POSTURE_SANITIZED` raises this exception with a
    pointed error message so operators get an immediate signal.
    """

    code = "F-CLASSIFICATION-REVIEW-INVALID-POSTURE"


class GateVerificationFailed(ClassificationReviewError):
    """One or more F-CLASS-REGISTER-* gates rejected the orchestrator output.

    Carries the per-gate :class:`ClassRegisterResult` list so callers can
    surface the underlying ``failure_code`` to the operator.
    """

    code = "F-CLASSIFICATION-REVIEW-GATE-VERIFICATION-FAILED"

    def __init__(
        self, message: str, *, gate_results: Sequence[ClassRegisterResult]
    ) -> None:
        super().__init__(message)
        self.gate_results = tuple(gate_results)


# ---------------------------------------------------------------------------
# Frozen dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ProposedField:
    """One Intake-proposed classification for a single field path."""

    field_path: str
    extracted_value: str
    proposed_class: str
    confidence: float
    rationale: str

    def __post_init__(self) -> None:
        if self.proposed_class not in PERMITTED_CLASSES:
            raise InvalidClassValue(
                f"proposed_class={self.proposed_class!r} for "
                f"field_path={self.field_path!r} not in {sorted(PERMITTED_CLASSES)}"
            )
        if not isinstance(self.confidence, (int, float)) or not (
            0.0 <= float(self.confidence) <= 1.0
        ):
            raise ProposalSchemaError(
                f"confidence must be 0.0..1.0, got {self.confidence!r} for "
                f"field_path={self.field_path!r}"
            )


@dataclass(frozen=True, kw_only=True)
class Proposal:
    """Intake-produced proposal artifact for a single document."""

    schema_version: str
    doc_hash: str
    doc_path: str
    proposed_at_iso8601: str
    proposed_by: str
    card_default_card_id: str
    fields: tuple[ProposedField, ...]


@dataclass(frozen=True, kw_only=True)
class OperatorDecision:
    """Operator's decision on one field (confirm or override)."""

    field_path: str
    final_class: str
    operator_action: str  # ACTION_CONFIRMED | ACTION_OVERRIDDEN
    operator_reason: Optional[str] = None  # required when operator_action == OVERRIDDEN

    def __post_init__(self) -> None:
        if self.final_class not in PERMITTED_CLASSES:
            raise InvalidClassValue(
                f"final_class={self.final_class!r} for "
                f"field_path={self.field_path!r} not in {sorted(PERMITTED_CLASSES)}"
            )
        if self.operator_action not in PERMITTED_ACTIONS:
            raise ClassificationReviewError(
                f"operator_action={self.operator_action!r} for "
                f"field_path={self.field_path!r} not in {sorted(PERMITTED_ACTIONS)}"
            )
        if self.operator_action == ACTION_OVERRIDDEN and not (
            isinstance(self.operator_reason, str)
            and self.operator_reason.strip()
        ):
            raise ClassificationReviewError(
                f"operator_action={ACTION_OVERRIDDEN} requires non-empty "
                f"operator_reason on field_path={self.field_path!r}"
            )


@dataclass(frozen=True, kw_only=True)
class FieldDecision:
    """Resolved per-field decision (proposed × operator)."""

    field_path: str
    extracted_value: str
    proposed_class: str
    final_class: str
    operator_action: str
    operator_reason: Optional[str]
    audit_entry_id: Optional[str]


@dataclass(frozen=True, kw_only=True)
class AuditEntry:
    """One per-override audit-log row."""

    audit_entry_id: str
    timestamp_iso8601: str
    doc_hash: str
    field_path: str
    proposed_class: str
    final_class: str
    operator_reason: str

    def to_jsonl(self) -> str:
        return _canonical_json(
            {
                "audit_entry_id": self.audit_entry_id,
                "timestamp_iso8601": self.timestamp_iso8601,
                "doc_hash": self.doc_hash,
                "field_path": self.field_path,
                "proposed_class": self.proposed_class,
                "final_class": self.final_class,
                "operator_reason": self.operator_reason,
            }
        )


@dataclass(frozen=True, kw_only=True)
class ReviewResult:
    """Aggregate result of a single document classification review session."""

    doc_hash: str
    org_slug: str
    field_decisions: tuple[FieldDecision, ...]
    audit_entries: tuple[AuditEntry, ...]
    signed_review_path: str
    register_path: str
    register_signed_at_iso8601: str
    register_signing_key_id: str
    gate_verification: tuple[ClassRegisterResult, ...]
    selected_posture: Optional[str] = None  # v7.0.10 §1.4: one of PERMITTED_POSTURES; None for legacy callers


def validate_posture(posture: Optional[str]) -> Optional[str]:
    """Normalize + validate a posture selection.

    ``None`` is permitted (legacy call sites that pre-date v7.0.10's
    posture-selection step); a string outside :data:`PERMITTED_POSTURES`
    raises :class:`InvalidPostureValue`. The deprecated v7.0.7-era
    ``"sanitized"`` posture surfaces a pointed error message naming the
    v7.0.10 LOCK so operators get an immediate signal.
    """
    if posture is None:
        return None
    if not isinstance(posture, str):
        raise InvalidPostureValue(
            f"selected_posture must be a string or None, got {type(posture).__name__}"
        )
    normalized = posture.strip().lower()
    if normalized == DEPRECATED_POSTURE_SANITIZED:
        raise InvalidPostureValue(
            "selected_posture='sanitized' is DEPRECATED. The opaque-slot-token / "
            "'Sanitized' posture was retired at architecture v7.0.10 LOCK "
            "2026-05-11 (row 215). Select one of: "
            f"{sorted(PERMITTED_POSTURES)}. See "
            "pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md."
        )
    if normalized not in PERMITTED_POSTURES:
        raise InvalidPostureValue(
            f"selected_posture={posture!r} not in {sorted(PERMITTED_POSTURES)}. "
            f"Permitted values are the three v7.0.10 customer-facing postures."
        )
    return normalized


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _canonical_json(data: Any) -> str:
    """Canonical JSON for hash + signature inputs.

    Sorted keys, no whitespace, ASCII-safe. Identical at sign time and at
    gate verify time so the hash check is deterministic.
    """
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha3_512_hex16(data: bytes) -> str:
    """SHA3-512 prefix per v7.0.7 §3.7 schema (lowercase, 16 hex chars)."""
    return hashlib.sha3_512(data).hexdigest()[:16]


def _now_utc_iso8601(clock: Optional[Callable[[], datetime]] = None) -> str:
    if clock is None:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return clock().strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _atomic_write(path: Path, data: str) -> None:
    """Write text atomically: tmp + fsync + rename."""
    _ensure_parent(path)
    tmp = path.with_suffix(path.suffix + f".tmp.{os.getpid()}")
    fd = os.open(str(tmp), os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600)
    try:
        os.write(fd, data.encode("utf-8"))
        os.fsync(fd)
    finally:
        os.close(fd)
    os.rename(str(tmp), str(path))


def _load_yaml(path: Path) -> Mapping[str, Any]:
    """Read YAML safely. Raises ProposalNotFound / ProposalSchemaError."""
    if not path.is_file():
        raise ProposalNotFound(f"proposal artifact not found at {path}")
    try:
        with open(path, "rb") as fh:
            data = yaml.safe_load(fh)
    except (OSError, yaml.YAMLError) as exc:
        raise ProposalSchemaError(
            f"could not parse YAML at {path}: {type(exc).__name__}: {exc}"
        ) from exc
    if not isinstance(data, Mapping):
        raise ProposalSchemaError(
            f"YAML root at {path} is not a mapping (got {type(data).__name__})"
        )
    return data


def _proposal_from_dict(raw: Mapping[str, Any], *, source_path: Path) -> Proposal:
    schema_version = raw.get("schema_version")
    if schema_version != PROPOSAL_SCHEMA_VERSION:
        raise ProposalSchemaError(
            f"schema_version mismatch at {source_path}: expected "
            f"{PROPOSAL_SCHEMA_VERSION!r}, got {schema_version!r}"
        )
    fields_raw = raw.get("fields")
    if not isinstance(fields_raw, list) or not fields_raw:
        raise ProposalSchemaError(
            f"fields list missing or empty at {source_path}"
        )
    parsed_fields: list[ProposedField] = []
    for idx, field_raw in enumerate(fields_raw):
        if not isinstance(field_raw, Mapping):
            raise ProposalSchemaError(
                f"fields[{idx}] is not a mapping at {source_path}"
            )
        try:
            parsed_fields.append(
                ProposedField(
                    field_path=str(field_raw["field_path"]),
                    extracted_value=str(field_raw["extracted_value"]),
                    proposed_class=str(field_raw["proposed_class"]),
                    confidence=float(field_raw.get("confidence", 0.0)),
                    rationale=str(field_raw.get("rationale", "")),
                )
            )
        except KeyError as exc:
            raise ProposalSchemaError(
                f"fields[{idx}] missing required key {exc!s} at {source_path}"
            ) from exc
    return Proposal(
        schema_version=schema_version,
        doc_hash=str(raw.get("doc_hash", "")),
        doc_path=str(raw.get("doc_path", "")),
        proposed_at_iso8601=str(raw.get("proposed_at_iso8601", "")),
        proposed_by=str(raw.get("proposed_by", "")),
        card_default_card_id=str(raw.get("card_default_card_id", "")),
        fields=tuple(parsed_fields),
    )


# ---------------------------------------------------------------------------
# Step 1 — load proposal
# ---------------------------------------------------------------------------


def load_proposed_classifications(
    *, repo_root: Path, org_slug: str, doc_hash: str
) -> Proposal:
    """Read the Intake-produced proposal artifact for one document.

    Raises :class:`ProposalNotFound` if the file is absent (Intake has not
    run BULK_INGEST against the document yet) or
    :class:`ProposalSchemaError` if the schema does not match v1.
    """
    path = repo_root / PROPOSAL_PATH_TEMPLATE.format(
        org_slug=org_slug, doc_hash=doc_hash
    )
    raw = _load_yaml(path)
    return _proposal_from_dict(raw, source_path=path)


# ---------------------------------------------------------------------------
# Step 2 — apply operator decisions (pure)
# ---------------------------------------------------------------------------


def apply_operator_decisions(
    *, proposal: Proposal, decisions: Sequence[OperatorDecision]
) -> tuple[FieldDecision, ...]:
    """Resolve per-field FieldDecision tuples from proposal × operator decisions.

    Pure transformation: no I/O, no UUID generation. Audit-entry IDs are
    populated downstream in :func:`build_audit_entries` because the ID
    itself is bound to the timestamp + UUID4 generated at write time.

    Raises :class:`DecisionCoverageGap` if any proposed field lacks a
    decision OR if any decision references a field not in the proposal.
    """
    decisions_by_path = {d.field_path: d for d in decisions}
    proposed_paths = {f.field_path for f in proposal.fields}
    decision_paths = set(decisions_by_path)

    missing_decisions = proposed_paths - decision_paths
    extra_decisions = decision_paths - proposed_paths
    if missing_decisions or extra_decisions:
        raise DecisionCoverageGap(
            f"decision coverage gap on doc_hash={proposal.doc_hash!r}: "
            f"missing={sorted(missing_decisions)!s}, "
            f"extra={sorted(extra_decisions)!s}"
        )

    resolved: list[FieldDecision] = []
    for proposed in proposal.fields:
        decision = decisions_by_path[proposed.field_path]
        if decision.operator_action == ACTION_OVERRIDDEN:
            if decision.final_class == proposed.proposed_class:
                # Operator marked OVERRIDDEN but final == proposed; treat as
                # confirmation to keep the audit log clean. This is a
                # defensive collapse (not a hard fail) because it is a
                # plausible operator-UX edge case.
                operator_action = ACTION_CONFIRMED
                operator_reason = None
            else:
                operator_action = ACTION_OVERRIDDEN
                operator_reason = decision.operator_reason
        else:
            if decision.final_class != proposed.proposed_class:
                # If operator_action == CONFIRMED but final differs, that is
                # an operator UX bug — confirm-but-different is incoherent.
                raise ClassificationReviewError(
                    f"operator_action={ACTION_CONFIRMED} but "
                    f"final_class={decision.final_class!r} != "
                    f"proposed_class={proposed.proposed_class!r} on "
                    f"field_path={decision.field_path!r}"
                )
            operator_action = ACTION_CONFIRMED
            operator_reason = None
        resolved.append(
            FieldDecision(
                field_path=proposed.field_path,
                extracted_value=proposed.extracted_value,
                proposed_class=proposed.proposed_class,
                final_class=decision.final_class,
                operator_action=operator_action,
                operator_reason=operator_reason,
                audit_entry_id=None,  # filled in by build_audit_entries
            )
        )
    return tuple(resolved)


# ---------------------------------------------------------------------------
# Step 3 — build + write audit entries
# ---------------------------------------------------------------------------


def build_audit_entries(
    *,
    field_decisions: Sequence[FieldDecision],
    doc_hash: str,
    timestamp_iso8601: str,
    uuid_generator: Optional[Callable[[], str]] = None,
) -> tuple[tuple[FieldDecision, ...], tuple[AuditEntry, ...]]:
    """Generate audit entries for OVERRIDDEN decisions only.

    Returns the field_decisions tuple with ``audit_entry_id`` populated on
    overridden rows, plus the parallel AuditEntry tuple.

    ``uuid_generator`` is injected for deterministic tests; defaults to
    ``uuid.uuid4().hex``.
    """
    gen = uuid_generator if uuid_generator is not None else (lambda: uuid.uuid4().hex)
    new_decisions: list[FieldDecision] = []
    audit_entries: list[AuditEntry] = []
    for decision in field_decisions:
        if decision.operator_action == ACTION_OVERRIDDEN:
            entry_id = gen()
            audit_entries.append(
                AuditEntry(
                    audit_entry_id=entry_id,
                    timestamp_iso8601=timestamp_iso8601,
                    doc_hash=doc_hash,
                    field_path=decision.field_path,
                    proposed_class=decision.proposed_class,
                    final_class=decision.final_class,
                    operator_reason=decision.operator_reason or "",
                )
            )
            new_decisions.append(
                FieldDecision(
                    field_path=decision.field_path,
                    extracted_value=decision.extracted_value,
                    proposed_class=decision.proposed_class,
                    final_class=decision.final_class,
                    operator_action=decision.operator_action,
                    operator_reason=decision.operator_reason,
                    audit_entry_id=entry_id,
                )
            )
        else:
            new_decisions.append(decision)
    return tuple(new_decisions), tuple(audit_entries)


def write_audit_entries(
    *, repo_root: Path, org_slug: str, audit_entries: Sequence[AuditEntry]
) -> Path:
    """Append audit entries to the per-org JSONL audit log (atomic per line)."""
    path = repo_root / AUDIT_LOG_PATH_TEMPLATE.format(org_slug=org_slug)
    _ensure_parent(path)
    if not audit_entries:
        # Empty review session (no overrides) — no log lines emitted, but the
        # file is touched so downstream readers see a real path.
        if not path.exists():
            with open(path, "ab") as fh:
                pass
        return path
    # Sequential append under a per-file lock would be ideal at multi-tenant
    # scale; v0.1 single-operator A1 makes a plain append safe.
    with open(path, "ab") as fh:
        for entry in audit_entries:
            fh.write(entry.to_jsonl().encode("utf-8") + b"\n")
            fh.flush()
            os.fsync(fh.fileno())
    return path


# ---------------------------------------------------------------------------
# Step 4 — write per-document signed review artifact
# ---------------------------------------------------------------------------


def _build_signed_review_payload(
    *,
    proposal: Proposal,
    field_decisions: Sequence[FieldDecision],
    operator_signed_at_iso8601: str,
    operator_key_id: str,
    attestation_string: str,
) -> dict[str, Any]:
    return {
        "schema_version": SIGNED_REVIEW_SCHEMA_VERSION,
        "doc_hash": proposal.doc_hash,
        "doc_path": proposal.doc_path,
        "proposal_artifact_path": PROPOSAL_PATH_TEMPLATE.format(
            org_slug="<org_slug>", doc_hash=proposal.doc_hash
        ),
        "operator_signed_at_iso8601": operator_signed_at_iso8601,
        "operator_key_id": operator_key_id,
        "card_default_card_id": proposal.card_default_card_id,
        "field_decisions": [
            {
                "field_path": d.field_path,
                "proposed_class": d.proposed_class,
                "final_class": d.final_class,
                "operator_action": d.operator_action,
                "audit_entry_id": d.audit_entry_id,
                "operator_reason": d.operator_reason,
            }
            for d in field_decisions
        ],
        "attestation_string": attestation_string,
    }


def write_signed_review_artifact(
    *,
    repo_root: Path,
    org_slug: str,
    proposal: Proposal,
    field_decisions: Sequence[FieldDecision],
    operator_signed_at_iso8601: str,
    operator_key_id: str,
    attestation_string: str,
    signing_key_bytes: bytes,
) -> tuple[Path, bytes]:
    """Write the per-document classification_review_<doc-hash>.yaml artifact.

    Returns the on-disk path AND the raw Ed25519 signature bytes (so the
    caller can chain the same signature into the persistent register's
    sign-off block).
    """
    payload = _build_signed_review_payload(
        proposal=proposal,
        field_decisions=field_decisions,
        operator_signed_at_iso8601=operator_signed_at_iso8601,
        operator_key_id=operator_key_id,
        attestation_string=attestation_string,
    )
    signed_message_bytes = _canonical_json(payload).encode("utf-8")
    signing_key = ed25519.Ed25519PrivateKey.from_private_bytes(signing_key_bytes)
    signature = signing_key.sign(signed_message_bytes)

    document = dict(payload)
    document["signature_base64"] = _bytes_to_b64(signature)

    path = repo_root / SIGNED_REVIEW_PATH_TEMPLATE.format(
        org_slug=org_slug, doc_hash=proposal.doc_hash
    )
    _atomic_write(path, yaml.safe_dump(document, sort_keys=False))
    return path, signature


def _bytes_to_b64(data: bytes) -> str:
    import base64

    return base64.b64encode(data).decode("ascii")


def _b64_to_bytes(s: str) -> bytes:
    import base64

    return base64.b64decode(s.encode("ascii"))


# ---------------------------------------------------------------------------
# Step 5 — commit field classifications into per-org register
# ---------------------------------------------------------------------------


def _default_class_definitions() -> dict[str, Any]:
    """Per v7.0.7 §2 schema — class_definitions block with all four classes."""
    return {
        CLASS_PUBLIC: {
            "definition": (
                "On the org's website, in funder-facing prior grants, "
                "in regulatory filings."
            ),
            "routing": (
                "Cloud-routable when ALL input is public + shareable; "
                "otherwise local."
            ),
            "examples": [
                "Org name, EIN (SAM.gov-public), street address visible on website",
                "Mission statement printed on annual report",
                "Federal RFA text + agency-published rubric",
            ],
        },
        CLASS_SHAREABLE: {
            "definition": (
                "Not public but operator-comfortable to share with cloud "
                "frontier models."
            ),
            "routing": (
                "Cloud-routable when ALL input is public + shareable; "
                "otherwise local."
            ),
            "examples": [
                "Project narrative paragraphs the operator has previously "
                "sent to other funders",
                "Aggregated, non-identifying outcome statistics",
                "Acres in production / production volume rounded to nearest "
                "order of magnitude",
            ],
        },
        CLASS_CONFIDENTIAL: {
            "definition": (
                "Stays local. Slot-filled into post-fill drafts only after "
                "cloud agents return."
            ),
            "routing": (
                "Always local. Cloud routing structurally prevented at "
                "outbound boundary (§5)."
            ),
            "examples": [
                "Audited annual revenue figures",
                "Specific partnership names not publicly disclosed",
                "Internal capacity assessments",
                "EIN of clients served by an intermediary applicant",
            ],
        },
        CLASS_OPERATOR_FLAGGED: {
            "definition": (
                "Operator marked sensitive in onboarding regardless of "
                "default class. Routes identically to confidential."
            ),
            "routing": (
                "Always local. Treated as confidential by §1 routing rule."
            ),
            "examples": [
                "A field the operator wants tighter posture on for "
                "reasons specific to a grant cycle",
                "Custom organizational data the Card archetype defaults "
                "did not anticipate",
            ],
        },
    }


def commit_to_register(
    *,
    repo_root: Path,
    org_slug: str,
    proposal: Proposal,
    field_decisions: Sequence[FieldDecision],
    populated_at_iso8601: str,
    populated_by: str,
) -> tuple[Path, dict[str, Any]]:
    """Upsert per-field classifications into the per-org register.

    Creates ``orgs/<slug>/vault/classification/register.yaml`` if absent;
    otherwise loads the existing register and merges new field decisions
    by ``field_path`` (last-write-wins).

    Returns the on-disk path AND the in-memory register dict (the caller
    chains this into :func:`sign_register`).
    """
    register_path = repo_root / REGISTER_PATH_TEMPLATE.format(org_slug=org_slug)
    register: dict[str, Any]
    if register_path.exists():
        loaded = _load_yaml(register_path)
        register = dict(loaded)
    else:
        register = {
            "schema_version": REGISTER_SCHEMA_VERSION,
            "populated_at": populated_at_iso8601,
            "populated_by": populated_by,
            "populated_via": "white_glove_onboarding",
            "org_slug": org_slug,
            "classification_defaults": {
                "source": "card_archetype",
                "card_id": proposal.card_default_card_id,
            },
            "field_classifications": [],
            "class_definitions": _default_class_definitions(),
            "grant_overrides": [],
            "audit_chain": [],
        }

    # Ensure shape — defensive against partial registers from prior tooling.
    register.setdefault("schema_version", REGISTER_SCHEMA_VERSION)
    register.setdefault("org_slug", org_slug)
    register.setdefault("class_definitions", _default_class_definitions())
    register.setdefault("field_classifications", [])
    register.setdefault("grant_overrides", [])
    register.setdefault("audit_chain", [])
    register["populated_at"] = populated_at_iso8601
    register["populated_by"] = populated_by
    register.setdefault("populated_via", "white_glove_onboarding")
    register.setdefault(
        "classification_defaults",
        {"source": "card_archetype", "card_id": proposal.card_default_card_id},
    )

    existing_by_path: dict[str, dict[str, Any]] = {}
    for entry in register.get("field_classifications", []):
        if isinstance(entry, Mapping) and "field_path" in entry:
            existing_by_path[str(entry["field_path"])] = dict(entry)

    for decision in field_decisions:
        existing_by_path[decision.field_path] = {
            "field_path": decision.field_path,
            "class": decision.final_class,
            "locked_by": (
                "operator_override"
                if decision.operator_action == ACTION_OVERRIDDEN
                else "card_default"
            ),
            "operator_override": decision.operator_action == ACTION_OVERRIDDEN,
            "override_reason": decision.operator_reason,
            "last_updated_doc_hash": proposal.doc_hash,
        }

    # Stable ordering by field_path for canonical hashing.
    register["field_classifications"] = [
        existing_by_path[k] for k in sorted(existing_by_path)
    ]

    _atomic_write(register_path, yaml.safe_dump(register, sort_keys=False))
    return register_path, register


# ---------------------------------------------------------------------------
# Step 6 — sign register (append §3.7 sign-off block)
# ---------------------------------------------------------------------------


def _canonical_block_bytes(block: Any) -> bytes:
    return _canonical_json(block).encode("utf-8")


def sign_register(
    *,
    register: Mapping[str, Any],
    register_path: Path,
    operator_signed_at_iso8601: str,
    operator_key_id: str,
    signed_routing_simulation_artifact_path: str,
    signed_test_cycle_artifact_path: str,
    attestation_string: str,
    signing_key_bytes: bytes,
    selected_posture: Optional[str] = None,
) -> dict[str, Any]:
    """Append the §3.7 ``operator_signature_at_white_glove_completion`` block.

    Per v7.0.10 §1.4 the signed register attests to BOTH per-field classifications
    AND the operator-selected deployment posture. When ``selected_posture`` is
    supplied (non-None), the register's top-level ``selected_posture`` field is
    set and the operator Ed25519 signature covers the extended payload
    (including the posture field). Sub-tag extensions on the F-CLASS-REGISTER-*
    gates (`.posture_unsigned` / `.posture_invalid` / `.posture_hash_mismatch`)
    verify the trail per §4 v2.x amendment §4.3.7.

    Returns the updated register dict (also writes it to disk).
    """
    normalized_posture = validate_posture(selected_posture)
    field_canonical_bytes = _canonical_block_bytes(
        register.get("field_classifications", [])
    )
    class_canonical_bytes = _canonical_block_bytes(
        register.get("class_definitions", {})
    )
    fields_hash = _sha3_512_hex16(field_canonical_bytes)
    class_hash = _sha3_512_hex16(class_canonical_bytes)

    sign_off_payload = {
        "signed_at_iso8601": operator_signed_at_iso8601,
        "signing_key_id": operator_key_id,
        SIGN_OFF_HASH_FIELDS_KEY: fields_hash,
        SIGN_OFF_HASH_CLASS_KEY: class_hash,
        "signed_card_default_card_id": (
            register.get("classification_defaults", {}).get("card_id", "")
        ),
        "signed_routing_simulation_artifact_path": (
            signed_routing_simulation_artifact_path
        ),
        "signed_test_cycle_artifact_path": signed_test_cycle_artifact_path,
        "attestation_string": attestation_string,
    }
    if normalized_posture is not None:
        # v7.0.10 §1.4: posture covered by the same Ed25519 signature as the
        # per-field classifications. Sub-tag `.posture_unsigned` fires if
        # this key is absent on a v7.0.10+ register.
        sign_off_payload["selected_posture"] = normalized_posture
    signed_message_bytes = _canonical_block_bytes(sign_off_payload)
    signing_key = ed25519.Ed25519PrivateKey.from_private_bytes(signing_key_bytes)
    signature = signing_key.sign(signed_message_bytes)

    sign_off_block = dict(sign_off_payload)
    sign_off_block["signature_base64"] = _bytes_to_b64(signature)

    new_register = dict(register)
    new_register[SIGN_OFF_KEY] = sign_off_block
    if normalized_posture is not None:
        # Top-level mirror — the gate-checked path expects the
        # selected_posture field on the register's top-level dict, not only
        # inside the sign-off block.
        new_register["selected_posture"] = normalized_posture

    audit_chain_entry = {
        "kind": "operator_signature_at_white_glove_completion",
        "signed_at_iso8601": operator_signed_at_iso8601,
        "key_id": operator_key_id,
        "signed_field_classifications_hash": fields_hash,
        "signed_class_definitions_hash": class_hash,
    }
    if normalized_posture is not None:
        audit_chain_entry["signed_posture"] = normalized_posture
    audit_chain = list(new_register.get("audit_chain", []))
    audit_chain.append(audit_chain_entry)
    new_register["audit_chain"] = audit_chain

    _atomic_write(register_path, yaml.safe_dump(new_register, sort_keys=False))
    return new_register


# ---------------------------------------------------------------------------
# Step 7 — verify against F-CLASS-REGISTER-* gates
# ---------------------------------------------------------------------------


def _file_exists_callable(path_str: str) -> bool:
    return Path(path_str).is_file()


def _hash_bytes_callable(data: bytes) -> str:
    return hashlib.sha3_512(data).hexdigest()


def _signature_verify_callable(
    message_bytes: bytes, signature: bytes, public_key: bytes
) -> bool:
    try:
        ed25519.Ed25519PublicKey.from_public_bytes(public_key).verify(
            signature, message_bytes
        )
    except (InvalidSignature, ValueError):
        return False
    return True


def verify_register_against_class_gates(
    *,
    register_path: Path,
    register: Mapping[str, Any],
    verifying_key_bytes: bytes,
) -> tuple[ClassRegisterResult, ...]:
    """Run all four F-CLASS-REGISTER-* gates against the register on disk.

    The register dict passed in MUST mirror the on-disk contents. The gate
    expects ``signature`` as bytes in the sign-off block; we decode the
    base64 wire format here so the gate sees raw bytes.
    """
    sign_off = dict(register.get(SIGN_OFF_KEY, {}) or {})
    if "signature_base64" in sign_off and "signature" not in sign_off:
        sign_off = dict(sign_off)
        sign_off["signature"] = _b64_to_bytes(sign_off["signature_base64"])
    register_for_gates = dict(register)
    register_for_gates[SIGN_OFF_KEY] = sign_off

    results: list[ClassRegisterResult] = []

    missing = check_class_register_missing(
        register_path=str(register_path),
        file_exists=_file_exists_callable,
    )
    results.append(missing)
    if not missing.success:
        return tuple(results)

    unsigned = check_class_register_unsigned(
        register=register_for_gates,
        register_path=str(register_path),
    )
    results.append(unsigned)
    if not unsigned.success:
        return tuple(results)

    # Reconstruct the canonical signed-message bytes the gate must verify
    # against — same canonicalization as :func:`sign_register`.
    sign_off_payload_for_verify = {
        k: v
        for k, v in sign_off.items()
        if k not in ("signature", "signature_base64")
    }
    signed_message_bytes = _canonical_block_bytes(sign_off_payload_for_verify)

    signature_invalid = check_class_register_signature_invalid(
        register=register_for_gates,
        signed_message_bytes=signed_message_bytes,
        signing_public_key=verifying_key_bytes,
        signature_verify=_signature_verify_callable,
        register_path=str(register_path),
    )
    results.append(signature_invalid)
    if not signature_invalid.success:
        return tuple(results)

    field_canonical_bytes = _canonical_block_bytes(
        register.get("field_classifications", [])
    )
    class_canonical_bytes = _canonical_block_bytes(
        register.get("class_definitions", {})
    )
    hash_mismatch = check_class_register_hash_mismatch(
        register=register_for_gates,
        field_classifications_canonical_bytes=field_canonical_bytes,
        class_definitions_canonical_bytes=class_canonical_bytes,
        hash_bytes=_hash_bytes_callable,
        register_path=str(register_path),
    )
    results.append(hash_mismatch)
    return tuple(results)


# ---------------------------------------------------------------------------
# End-to-end orchestrator entry point
# ---------------------------------------------------------------------------


def run_classification_review(
    *,
    repo_root: Path,
    org_slug: str,
    doc_hash: str,
    decisions: Sequence[OperatorDecision],
    operator_key_id: str,
    signing_key_bytes: bytes,
    verifying_key_bytes: bytes,
    attestation_string: Optional[str] = None,
    clock: Optional[Callable[[], datetime]] = None,
    uuid_generator: Optional[Callable[[], str]] = None,
    selected_posture: Optional[str] = None,
) -> ReviewResult:
    """Top-level orchestrator entry — runs steps 1 → 7 in sequence.

    Raises:
        ProposalNotFound, ProposalSchemaError: step 1 issues.
        DecisionCoverageGap, InvalidClassValue, ClassificationReviewError:
            step 2 / 3 issues.
        GateVerificationFailed: step 7 (F-CLASS-REGISTER-* gate rejected
            the orchestrator output — fail-closed; orchestrator does not
            mark the workflow successful).
    """
    # v7.0.10 §1.4 — validate posture early so a deprecated 'sanitized' string
    # surfaces an error before any file I/O.
    normalized_posture = validate_posture(selected_posture)

    proposal = load_proposed_classifications(
        repo_root=repo_root, org_slug=org_slug, doc_hash=doc_hash
    )
    if proposal.doc_hash != doc_hash:
        raise ProposalSchemaError(
            f"proposal artifact doc_hash={proposal.doc_hash!r} does not match "
            f"requested doc_hash={doc_hash!r}"
        )

    initial_decisions = apply_operator_decisions(
        proposal=proposal, decisions=decisions
    )

    timestamp = _now_utc_iso8601(clock=clock)
    field_decisions, audit_entries = build_audit_entries(
        field_decisions=initial_decisions,
        doc_hash=proposal.doc_hash,
        timestamp_iso8601=timestamp,
        uuid_generator=uuid_generator,
    )

    write_audit_entries(
        repo_root=repo_root, org_slug=org_slug, audit_entries=audit_entries
    )

    n_confirmed = sum(
        1 for d in field_decisions if d.operator_action == ACTION_CONFIRMED
    )
    n_overridden = sum(
        1 for d in field_decisions if d.operator_action == ACTION_OVERRIDDEN
    )
    final_attestation = (
        attestation_string
        or (
            f"I, operator {operator_key_id}, have reviewed the classification "
            f"proposal for document {proposal.doc_hash} at field-level, "
            f"confirmed {n_confirmed} fields, overridden {n_overridden} fields, "
            f"and authorize the resulting classification register update as of "
            f"{timestamp}."
        )
    )

    signed_review_path, _signed_review_signature = write_signed_review_artifact(
        repo_root=repo_root,
        org_slug=org_slug,
        proposal=proposal,
        field_decisions=field_decisions,
        operator_signed_at_iso8601=timestamp,
        operator_key_id=operator_key_id,
        attestation_string=final_attestation,
        signing_key_bytes=signing_key_bytes,
    )

    register_path, register = commit_to_register(
        repo_root=repo_root,
        org_slug=org_slug,
        proposal=proposal,
        field_decisions=field_decisions,
        populated_at_iso8601=timestamp,
        populated_by=operator_key_id,
    )

    signed_register = sign_register(
        register=register,
        register_path=register_path,
        operator_signed_at_iso8601=timestamp,
        operator_key_id=operator_key_id,
        signed_routing_simulation_artifact_path=str(
            signed_review_path.relative_to(repo_root)
        ),
        signed_test_cycle_artifact_path="",
        attestation_string=final_attestation,
        signing_key_bytes=signing_key_bytes,
        selected_posture=normalized_posture,
    )

    gate_results = verify_register_against_class_gates(
        register_path=register_path,
        register=signed_register,
        verifying_key_bytes=verifying_key_bytes,
    )
    failures = [r for r in gate_results if not r.success]
    if failures:
        codes = [r.failure_code for r in failures]
        raise GateVerificationFailed(
            f"F-CLASS-REGISTER-* gate(s) rejected orchestrator output: "
            f"{codes!r}",
            gate_results=gate_results,
        )

    return ReviewResult(
        doc_hash=proposal.doc_hash,
        org_slug=org_slug,
        field_decisions=field_decisions,
        audit_entries=audit_entries,
        signed_review_path=str(signed_review_path),
        register_path=str(register_path),
        register_signed_at_iso8601=timestamp,
        register_signing_key_id=operator_key_id,
        gate_verification=gate_results,
        selected_posture=normalized_posture,
    )


__all__ = [
    "ACTION_CONFIRMED",
    "ACTION_OVERRIDDEN",
    "AUDIT_LOG_PATH_TEMPLATE",
    "AuditEntry",
    "CLASS_CONFIDENTIAL",
    "CLASS_OPERATOR_FLAGGED",
    "CLASS_PUBLIC",
    "CLASS_SHAREABLE",
    "ClassificationReviewError",
    "DecisionCoverageGap",
    "DEPRECATED_POSTURE_SANITIZED",
    "F_CLASS_REGISTER_HASH_MISMATCH",
    "F_CLASS_REGISTER_MISSING",
    "F_CLASS_REGISTER_SIGNATURE_INVALID",
    "F_CLASS_REGISTER_UNSIGNED",
    "FieldDecision",
    "GateVerificationFailed",
    "InvalidClassValue",
    "InvalidPostureValue",
    "OperatorDecision",
    "POSTURE_DESCRIPTIONS",
    "POSTURE_DISPLAY_LABELS",
    "POSTURE_FRONTIER_ELIGIBLE",
    "POSTURE_LOCAL_ONLY_SOVEREIGN",
    "POSTURE_SPLIT_CONTEXT_HYBRID",
    "PROPOSAL_PATH_TEMPLATE",
    "PROPOSAL_SCHEMA_VERSION",
    "PERMITTED_ACTIONS",
    "PERMITTED_CLASSES",
    "PERMITTED_POSTURES",
    "Proposal",
    "ProposalNotFound",
    "ProposalSchemaError",
    "ProposedField",
    "REGISTER_PATH_TEMPLATE",
    "REGISTER_SCHEMA_VERSION",
    "ReviewResult",
    "SIGNED_REVIEW_PATH_TEMPLATE",
    "SIGNED_REVIEW_SCHEMA_VERSION",
    "apply_operator_decisions",
    "build_audit_entries",
    "commit_to_register",
    "load_proposed_classifications",
    "run_classification_review",
    "sign_register",
    "validate_posture",
    "verify_register_against_class_gates",
    "write_audit_entries",
    "write_signed_review_artifact",
]
