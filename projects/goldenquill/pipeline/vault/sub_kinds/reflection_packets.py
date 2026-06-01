"""``reflection_packet`` sub-kind — Reflection Packet artifact (v0.1 hook DORMANT).

Schema + canonical-bytes codec for the ReflectionPacket Pydantic shape
emitted by ``archivist.reflection_submode`` at every grant cycle close
(emit + backfill discipline per §16.3).

**v0.1 Beta hook scope per OQ-2 (a):** schema module authored; canonical-
codec helpers + dataclass mechanics + length/grammar/type/closed-set
invariants are LIVE for testability. Semantic invariants that depend on
runtime substrates (Logfire span resolution, KFR ledger, classification
register cross-check) stay under F-PACKET-* predicate-body NotImplementedError
at v0.1 hook; bodies land at v0.2 first wave compound LOCK.

**SUB_KIND_REGISTRY entry is DEFERRED to v0.2 first wave.** This module is
authored but NOT registered. Vault read/write dispatch will not find a
"reflection_packet" sub-kind at v0.1 hook — by design.

Blueprint authority:
    - section_16_reflection_packet.md §16.2 (schema)
    - section_16_reflection_packet.md §16.2.3 (21 invariants)
    - section_16_reflection_packet.md §16.2.4 (canonical-bytes codec)
    - section_16_reflection_packet.md §16.3 (producer contract emit + backfill)
    - section_16_reflection_packet.md §16.5 (signing regime)
    - section_04_v2_x_y_packet_amendment.md (F-PACKET-* family)
    - section_00_5_section_16_packet_amendment.md (§0.5 v21 rows 471-505)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Final, Mapping

from pipeline.vault.sub_kinds._canonical import (
    from_canonical_json_bytes,
    to_canonical_json_bytes,
)

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_16_reflection_packet.md": {
        "version": "v1-LOCKED-2026-05-15",
        "sections_implemented": [
            "§16.2.1 ReflectionPacket schema",
            "§16.2.2 nested shapes (6 sub-shapes)",
            "§16.2.3 invariants (21 invariants)",
            "§16.2.4 canonical-bytes codec",
        ],
    },
    "section_04_v2_x_y_packet_amendment.md": {
        "version": "v2.x.y-LOCKED-2026-05-15",
        "predicate_signatures_registered": 19,
        "live_bodies_at_v0_1_hook": 1,
    },
}

INTENT: Final[str] = "operational-reflection-packet-write"
SUB_KIND: Final[str] = "reflection_packet"
VAULT_SUBTREE: Final[str] = "operational/reflection_packets/"
ADMIN_RISK_SEVERITY_DEFAULT: Final[str] = "YELLOW"

# v0.1 hook DORMANT — SUB_KIND_REGISTRY entry not registered.
# Registers at v0.2 first wave compound LOCK per §16 v1 §16.9.
SUB_KIND_REGISTRY_REGISTERED_AT_V0_1: Final[bool] = False

# Closed CIC + CLC sets per Tilth-internal taxonomy
_VALID_CIC: Final[frozenset[str]] = frozenset(
    {
        "food_systems",
        "educator",
        "public_agency",
        "arts_culture",
        "cooperative",
        "ecosystem_intermediary",
    }
)
_VALID_CLC: Final[frozenset[str]] = frozenset(
    {
        "public_purpose_and_works",
        "catalytic_change",
        "operating_capacity",
        "research_and_evidence",
        "market_access",
        "credit_and_underwriting",
        "sponsorship_and_corporate_support",
        "shared_assets",
    }
)
_VALID_SEVERITY: Final[frozenset[str]] = frozenset({"LOW", "MEDIUM", "HIGH"})
_VALID_OUTCOME_STATUS: Final[frozenset[str]] = frozenset(
    {"PENDING", "AWARDED", "DECLINED", "NO_DECISION"}
)
_VALID_EDITOR_VERDICT: Final[frozenset[str]] = frozenset(
    {"READY", "NEEDS_FIXES", "NOT_READY"}
)
_VALID_GROUNDING_SIGNAL_CLASSES: Final[frozenset[str]] = frozenset(
    {
        "external_funder_outcome",
        "operator_approval",
        "logician_gate_outcome",
        "kfr_drift_event",
        "admin_risk_event",
        "match_db_outcome",
        # LLM-eval-only classes admissible but cannot be the ONLY grounding:
        "council_split_event",
        "judge_score",
        "red_team_score",
        "editor_verdict",
    }
)
_LLM_EVAL_ONLY_CLASSES: Final[frozenset[str]] = frozenset(
    {"council_split_event", "judge_score", "red_team_score", "editor_verdict"}
)

# v0.1 producer registry closed set per §16 v1 §16.3
_PRODUCER_REGISTRY_V0_1: Final[frozenset[str]] = frozenset(
    {"archivist.reflection_submode"}
)

# Regex grammars (mirror §17 cycle_id grammar; closes path-traversal class)
_PACKET_ID_RE: Final[re.Pattern[str]] = re.compile(
    r"^[A-Za-z0-9_-]{1,128}$"
)
_CYCLE_ID_RE: Final[re.Pattern[str]] = re.compile(
    r"^[A-Za-z0-9_-]{1,128}$"
)
_ORG_SLUG_RE: Final[re.Pattern[str]] = re.compile(
    r"^[a-z][a-z0-9_]{0,63}$"
)
_SEMVER_RE: Final[re.Pattern[str]] = re.compile(r"^\d+\.\d+\.\d+$")
_SHA3_512_HEX_RE: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{128}$")
_ED25519_SIG_HEX_RE: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{128}$")
_UTC_ISO_RE: Final[re.Pattern[str]] = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$"
)
_SPAN_ID_RE: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z0-9_-]{1,128}$")
_CURRENCY_RE: Final[re.Pattern[str]] = re.compile(r"^[A-Z]{3}$")

# Pattern-summary + rule length bounds
_PATTERN_SUMMARY_MAX_LEN: Final[int] = 4096
_PROPOSED_RULE_MAX_LEN: Final[int] = 4096


def _ensure_non_neg_int(value: object, field_name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(
            f"{field_name} must be int (A12 Decimal mandate — int minor "
            f"units, never float; bool excluded), got "
            f"{type(value).__name__}"
        )
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0, got {value!r}")


def _ensure_int(value: object, field_name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(
            f"{field_name} must be int (A12 mandate; bool excluded), got "
            f"{type(value).__name__}"
        )


def _ensure_in_range(
    value: int, lo: int, hi: int, field_name: str
) -> None:
    if not (lo <= value <= hi):
        raise ValueError(
            f"{field_name} must be in [{lo}, {hi}], got {value!r}"
        )


# ---------------------------------------------------------------------------
# Nested shapes
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class PatternObservation:
    """Pattern-LEVEL observation. Instance-level text refused per
    F-PACKET-INSTANCE-LEAK (predicate body lands v0.2 first wave)."""

    pattern_summary: str
    cic: str
    clc: str
    frequency: int
    severity: str
    first_observed_cycle_id: str
    supporting_span_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.pattern_summary, str) or not self.pattern_summary:
            raise ValueError("pattern_summary must be a non-empty str")
        if len(self.pattern_summary) > _PATTERN_SUMMARY_MAX_LEN:
            raise ValueError(
                f"pattern_summary length {len(self.pattern_summary)} "
                f"exceeds bound {_PATTERN_SUMMARY_MAX_LEN}"
            )
        if self.cic not in _VALID_CIC:
            raise ValueError(
                f"cic {self.cic!r} not in closed CIC set {sorted(_VALID_CIC)!r}"
            )
        if self.clc not in _VALID_CLC:
            raise ValueError(
                f"clc {self.clc!r} not in closed CLC set {sorted(_VALID_CLC)!r}"
            )
        _ensure_int(self.frequency, "frequency")
        if self.frequency < 1:
            raise ValueError(f"frequency must be >= 1, got {self.frequency}")
        if self.severity not in _VALID_SEVERITY:
            raise ValueError(
                f"severity {self.severity!r} not in {sorted(_VALID_SEVERITY)!r}"
            )
        if not _CYCLE_ID_RE.match(self.first_observed_cycle_id):
            raise ValueError(
                f"first_observed_cycle_id {self.first_observed_cycle_id!r} "
                f"does not match grammar {_CYCLE_ID_RE.pattern}"
            )
        if not isinstance(self.supporting_span_ids, tuple):
            raise ValueError("supporting_span_ids must be tuple")
        if not self.supporting_span_ids:
            raise ValueError("supporting_span_ids must be non-empty")
        for i, sid in enumerate(self.supporting_span_ids):
            if not isinstance(sid, str) or not _SPAN_ID_RE.match(sid):
                raise ValueError(
                    f"supporting_span_ids[{i}] {sid!r} fails grammar "
                    f"{_SPAN_ID_RE.pattern}"
                )


@dataclass(frozen=True, kw_only=True)
class ProposedLesson:
    """Pattern-rolled lesson; frequency >= 2 OR severity == 'HIGH' per
    F-PACKET-PREMATURE-GENERALIZATION."""

    lesson_id: str
    pattern_summary: str
    proposed_rule: str
    frequency: int
    severity: str
    supporting_pattern_observation_ids: tuple[str, ...]
    supporting_cycle_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.lesson_id, str) or not _PACKET_ID_RE.match(
            self.lesson_id
        ):
            raise ValueError(
                f"lesson_id {self.lesson_id!r} fails grammar "
                f"{_PACKET_ID_RE.pattern}"
            )
        if not isinstance(self.pattern_summary, str) or not self.pattern_summary:
            raise ValueError("pattern_summary must be non-empty str")
        if len(self.pattern_summary) > _PATTERN_SUMMARY_MAX_LEN:
            raise ValueError("pattern_summary exceeds length bound")
        if not isinstance(self.proposed_rule, str) or not self.proposed_rule:
            raise ValueError("proposed_rule must be non-empty str")
        if len(self.proposed_rule) > _PROPOSED_RULE_MAX_LEN:
            raise ValueError("proposed_rule exceeds length bound")
        _ensure_int(self.frequency, "frequency")
        if self.frequency < 1:
            raise ValueError(f"frequency must be >= 1, got {self.frequency}")
        if self.severity not in _VALID_SEVERITY:
            raise ValueError(
                f"severity {self.severity!r} not in {sorted(_VALID_SEVERITY)!r}"
            )
        # Invariant 10 — frequency==1 requires severity=='HIGH'
        if self.frequency == 1 and self.severity != "HIGH":
            raise ValueError(
                "ProposedLesson with frequency==1 must have severity=='HIGH' "
                "(F-PACKET-PREMATURE-GENERALIZATION invariant)"
            )
        if not isinstance(self.supporting_pattern_observation_ids, tuple):
            raise ValueError(
                "supporting_pattern_observation_ids must be tuple"
            )
        if not isinstance(self.supporting_cycle_ids, tuple):
            raise ValueError("supporting_cycle_ids must be tuple")
        if len(self.supporting_cycle_ids) < self.frequency:
            raise ValueError(
                f"len(supporting_cycle_ids) ({len(self.supporting_cycle_ids)})"
                f" must be >= frequency ({self.frequency})"
            )
        for i, cid in enumerate(self.supporting_cycle_ids):
            if not isinstance(cid, str) or not _CYCLE_ID_RE.match(cid):
                raise ValueError(
                    f"supporting_cycle_ids[{i}] {cid!r} fails grammar"
                )


@dataclass(frozen=True, kw_only=True)
class GatePassCounts:
    """Per-family gate-pass / gate-fail counts observed across the cycle."""

    f_class_pass: int
    f_class_fail: int
    f_archivist_pass: int
    f_archivist_fail: int
    f_reflection_pass: int
    f_reflection_fail: int
    f_packet_pass: int
    f_packet_fail: int
    f_logician_total_pass: int
    f_logician_total_fail: int

    def __post_init__(self) -> None:
        for fname in (
            "f_class_pass",
            "f_class_fail",
            "f_archivist_pass",
            "f_archivist_fail",
            "f_reflection_pass",
            "f_reflection_fail",
            "f_packet_pass",
            "f_packet_fail",
            "f_logician_total_pass",
            "f_logician_total_fail",
        ):
            _ensure_non_neg_int(getattr(self, fname), fname)


@dataclass(frozen=True, kw_only=True)
class ScoreSignals:
    """Judge / Red Team / Editor signals; deterministic fields only."""

    judge_score: int | None
    red_team_score: int | None
    editor_verdict: str | None
    judge_red_team_divergence: int | None
    council_split_fired: bool
    cross_family_satisfied: bool

    def __post_init__(self) -> None:
        if self.judge_score is not None:
            _ensure_non_neg_int(self.judge_score, "judge_score")
            _ensure_in_range(self.judge_score, 0, 100, "judge_score")
        if self.red_team_score is not None:
            _ensure_non_neg_int(self.red_team_score, "red_team_score")
            _ensure_in_range(self.red_team_score, 0, 100, "red_team_score")
        if (
            self.editor_verdict is not None
            and self.editor_verdict not in _VALID_EDITOR_VERDICT
        ):
            raise ValueError(
                f"editor_verdict {self.editor_verdict!r} not in "
                f"{sorted(_VALID_EDITOR_VERDICT)!r}"
            )
        if self.judge_red_team_divergence is not None:
            _ensure_non_neg_int(
                self.judge_red_team_divergence, "judge_red_team_divergence"
            )
        if not isinstance(self.council_split_fired, bool):
            raise ValueError("council_split_fired must be bool")
        if not isinstance(self.cross_family_satisfied, bool):
            raise ValueError("cross_family_satisfied must be bool")


@dataclass(frozen=True, kw_only=True)
class CycleOutcome:
    """Outcome status + amount; emit + backfill discipline per §16.3."""

    status: str
    funder_id: str | None
    award_amount_minor_units: int | None
    award_currency: str | None
    decision_observed_at: str | None
    outcome_evidence_span_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.status not in _VALID_OUTCOME_STATUS:
            raise ValueError(
                f"status {self.status!r} not in {sorted(_VALID_OUTCOME_STATUS)!r}"
            )
        if self.award_amount_minor_units is not None:
            _ensure_non_neg_int(
                self.award_amount_minor_units, "award_amount_minor_units"
            )
        if self.award_currency is not None:
            if not isinstance(
                self.award_currency, str
            ) or not _CURRENCY_RE.match(self.award_currency):
                raise ValueError(
                    f"award_currency {self.award_currency!r} must match "
                    f"ISO-4217 alpha-3 {_CURRENCY_RE.pattern}"
                )
        if self.decision_observed_at is not None:
            if not _UTC_ISO_RE.match(self.decision_observed_at):
                raise ValueError(
                    f"decision_observed_at {self.decision_observed_at!r} "
                    f"must match UTC ISO-8601 'Z' grammar"
                )
        if not isinstance(self.outcome_evidence_span_ids, tuple):
            raise ValueError("outcome_evidence_span_ids must be tuple")
        for i, sid in enumerate(self.outcome_evidence_span_ids):
            if not isinstance(sid, str) or not _SPAN_ID_RE.match(sid):
                raise ValueError(
                    f"outcome_evidence_span_ids[{i}] {sid!r} fails grammar"
                )
        # AWARDED requires amount + currency
        if self.status == "AWARDED":
            if (
                self.award_amount_minor_units is None
                or self.award_currency is None
            ):
                raise ValueError(
                    "outcome.status='AWARDED' requires both "
                    "award_amount_minor_units and award_currency"
                )
        # non-AWARDED forbids amount / currency
        else:
            if self.award_amount_minor_units is not None:
                raise ValueError(
                    f"outcome.status={self.status!r} forbids "
                    f"award_amount_minor_units"
                )
            if self.award_currency is not None:
                raise ValueError(
                    f"outcome.status={self.status!r} forbids award_currency"
                )
        # non-PENDING requires decision_observed_at + outcome_evidence
        if self.status != "PENDING":
            if self.decision_observed_at is None:
                raise ValueError(
                    f"outcome.status={self.status!r} requires "
                    f"decision_observed_at"
                )
            if not self.outcome_evidence_span_ids:
                raise ValueError(
                    f"outcome.status={self.status!r} requires non-empty "
                    f"outcome_evidence_span_ids"
                )
        # PENDING forbids decision_observed_at + evidence
        else:
            if self.decision_observed_at is not None:
                raise ValueError(
                    "outcome.status='PENDING' forbids decision_observed_at"
                )
            if self.outcome_evidence_span_ids:
                raise ValueError(
                    "outcome.status='PENDING' forbids outcome_evidence_span_ids"
                )


@dataclass(frozen=True, kw_only=True)
class PacketSpanProvenance:
    """Logfire trace + per-claim span_id mapping."""

    trace_ids: tuple[str, ...]
    logfire_export_uri: str | None
    per_claim_span_ids: Mapping[str, tuple[str, ...]]

    def __post_init__(self) -> None:
        if not isinstance(self.trace_ids, tuple) or not self.trace_ids:
            raise ValueError("trace_ids must be non-empty tuple")
        for i, tid in enumerate(self.trace_ids):
            if not isinstance(tid, str) or not _SPAN_ID_RE.match(tid):
                raise ValueError(
                    f"trace_ids[{i}] {tid!r} fails grammar"
                )
        if self.logfire_export_uri is not None and not isinstance(
            self.logfire_export_uri, str
        ):
            raise ValueError("logfire_export_uri must be str when present")
        if not isinstance(self.per_claim_span_ids, Mapping):
            raise ValueError("per_claim_span_ids must be Mapping")
        for ck, sids in self.per_claim_span_ids.items():
            if not isinstance(ck, str) or not ck:
                raise ValueError(
                    f"per_claim_span_ids key {ck!r} must be non-empty str"
                )
            if not isinstance(sids, tuple) or not sids:
                raise ValueError(
                    f"per_claim_span_ids[{ck!r}] must map to non-empty tuple"
                )
            for i, sid in enumerate(sids):
                if not isinstance(sid, str) or not _SPAN_ID_RE.match(sid):
                    raise ValueError(
                        f"per_claim_span_ids[{ck!r}][{i}] {sid!r} fails grammar"
                    )


# ---------------------------------------------------------------------------
# Top-level ReflectionPacket
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ReflectionPacket:
    """Top-level Reflection Packet artifact per §16 v1 §16.2.1.

    v0.1 hook DORMANT — sub-kind registry entry deferred to v0.2 first wave.
    Schema + canonical-codec + 21 length/grammar/type invariants are LIVE
    for testability; semantic invariants (Logfire span resolution, etc.)
    are under F-PACKET-* predicate-body NotImplementedError at v0.1 hook.
    """

    # Identity + provenance
    packet_id: str
    cycle_id: str
    org_slug: str
    schema_version: str
    classification_register_version: str

    # Emission context
    emitted_at: str
    emitted_by_seat: str
    cycle_close_marker_span_id: str

    # Pattern-level observations
    pattern_observations: tuple[PatternObservation, ...]
    lessons_proposed: tuple[ProposedLesson, ...]

    # Quantitative signals
    gate_pass_counts: GatePassCounts
    score_signals: ScoreSignals
    outcome: CycleOutcome

    # Grounding signal class declarations
    grounding_signal_classes: frozenset[str]

    # Provenance
    span_provenance: PacketSpanProvenance

    # Signing regime
    canonical_bytes_hash: str
    producer_signature_ed25519: str
    operator_signature_ed25519: str | None

    def __post_init__(self) -> None:
        # Invariant 2 — packet_id grammar
        if not isinstance(self.packet_id, str) or not _PACKET_ID_RE.match(
            self.packet_id
        ):
            raise ValueError(
                f"packet_id {self.packet_id!r} fails grammar "
                f"{_PACKET_ID_RE.pattern}"
            )
        # Invariant 1 — cycle_id grammar (path-traversal defense)
        if not isinstance(self.cycle_id, str) or not _CYCLE_ID_RE.match(
            self.cycle_id
        ):
            raise ValueError(
                f"cycle_id {self.cycle_id!r} fails grammar "
                f"{_CYCLE_ID_RE.pattern}"
            )
        # Invariant 3 — org_slug grammar
        if not isinstance(self.org_slug, str) or not _ORG_SLUG_RE.match(
            self.org_slug
        ):
            raise ValueError(
                f"org_slug {self.org_slug!r} fails grammar "
                f"{_ORG_SLUG_RE.pattern}"
            )
        # Invariant 4 — semver
        if not _SEMVER_RE.match(self.schema_version):
            raise ValueError(
                f"schema_version {self.schema_version!r} fails semver"
            )
        # Invariant 5 — classification register SHA3-512 hex
        if not _SHA3_512_HEX_RE.match(self.classification_register_version):
            raise ValueError(
                "classification_register_version must be 128-hex SHA3-512"
            )
        # Invariant 6 — UTC ISO-8601 'Z' on emitted_at
        if not _UTC_ISO_RE.match(self.emitted_at):
            raise ValueError(
                f"emitted_at {self.emitted_at!r} must be UTC ISO-8601 'Z'"
            )
        # Invariant 7 — emitted_by_seat closed set
        if self.emitted_by_seat not in _PRODUCER_REGISTRY_V0_1:
            raise ValueError(
                f"emitted_by_seat {self.emitted_by_seat!r} not in "
                f"v0.1 producer registry {sorted(_PRODUCER_REGISTRY_V0_1)!r}"
            )
        # cycle_close_marker_span_id grammar
        if not _SPAN_ID_RE.match(self.cycle_close_marker_span_id):
            raise ValueError(
                f"cycle_close_marker_span_id {self.cycle_close_marker_span_id!r}"
                f" fails grammar"
            )
        # pattern_observations / lessons_proposed tuple type
        if not isinstance(self.pattern_observations, tuple):
            raise ValueError("pattern_observations must be tuple")
        if not isinstance(self.lessons_proposed, tuple):
            raise ValueError("lessons_proposed must be tuple")
        # Invariant 11 — grounding signal class set rules
        if not isinstance(self.grounding_signal_classes, frozenset):
            raise ValueError(
                "grounding_signal_classes must be frozenset[str]"
            )
        if not self.grounding_signal_classes:
            raise ValueError("grounding_signal_classes must be non-empty")
        if not self.grounding_signal_classes <= _VALID_GROUNDING_SIGNAL_CLASSES:
            raise ValueError(
                "grounding_signal_classes contains unknown class(es): "
                f"{sorted(self.grounding_signal_classes - _VALID_GROUNDING_SIGNAL_CLASSES)!r}"
            )
        # MUST NOT be a subset of LLM-eval-only classes
        if self.grounding_signal_classes <= _LLM_EVAL_ONLY_CLASSES:
            raise ValueError(
                "grounding_signal_classes is a subset of LLM-eval-only "
                "classes — F-PACKET-EVAL-ONLY-GROUNDED invariant violated; "
                "at least one non-LLM-eval-only class required"
            )
        # Invariant 16 — outcome.status non-PENDING requires operator sig + evidence
        if self.outcome.status != "PENDING":
            if self.operator_signature_ed25519 is None:
                raise ValueError(
                    f"outcome.status={self.outcome.status!r} requires "
                    f"operator_signature_ed25519 non-None "
                    f"(F-PACKET-OPERATOR-SIGNATURE-MISSING invariant)"
                )
        else:
            # Cycle 2 RT-C2-02 fold-in — PENDING forbids operator signature
            if self.operator_signature_ed25519 is not None:
                raise ValueError(
                    "outcome.status='PENDING' forbids non-None "
                    "operator_signature_ed25519 (F-PACKET-OPERATOR-SIGNATURE-"
                    "MISSING sub-tag .signature_present_for_pending)"
                )
        # Invariant 18 — canonical-bytes-hash SHA3-512 hex
        if not _SHA3_512_HEX_RE.match(self.canonical_bytes_hash):
            raise ValueError(
                "canonical_bytes_hash must be 128-hex SHA3-512"
            )
        # Invariant 19 — producer signature hex
        if not _ED25519_SIG_HEX_RE.match(self.producer_signature_ed25519):
            raise ValueError(
                "producer_signature_ed25519 must be 128-hex Ed25519 signature"
            )
        # Invariant 20 — operator signature hex when present
        if (
            self.operator_signature_ed25519 is not None
            and not _ED25519_SIG_HEX_RE.match(self.operator_signature_ed25519)
        ):
            raise ValueError(
                "operator_signature_ed25519 must be 128-hex when present"
            )


# ---------------------------------------------------------------------------
# Canonical-bytes codec — mirrors v7.0.4-M1 KFR byte-for-byte
# ---------------------------------------------------------------------------

_SIGNATURE_FIELDS_EXCLUDED: Final[frozenset[str]] = frozenset(
    {
        "canonical_bytes_hash",
        "producer_signature_ed25519",
        "operator_signature_ed25519",
    }
)


def to_canonical_bytes(packet: ReflectionPacket) -> bytes:
    """Serialize ReflectionPacket to canonical-JSON bytes with signature
    fields excluded.

    SHA3-512 of this output produces ``canonical_bytes_hash``. Ed25519
    signing of this output produces ``producer_signature_ed25519`` and
    ``operator_signature_ed25519``.

    Mirrors v7.0.4-M1 §2 KFR canonicalization regime byte-for-byte.
    """
    from dataclasses import asdict

    payload = asdict(packet)
    # Convert frozenset to sorted list for canonical encoding (frozensets
    # are not JSON-serializable; sorted list ensures stable bytes)
    if "grounding_signal_classes" in payload:
        gcs = payload["grounding_signal_classes"]
        if isinstance(gcs, (frozenset, set)):
            payload["grounding_signal_classes"] = sorted(gcs)
    # Exclude signature fields
    for fname in _SIGNATURE_FIELDS_EXCLUDED:
        payload.pop(fname, None)
    import json

    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


def from_canonical_bytes(payload: bytes) -> dict:
    """Decode canonical bytes back to a dict (NOT to ReflectionPacket —
    signature fields are absent in canonical form, so re-constructing the
    record requires re-attaching the signature fields)."""
    return from_canonical_json_bytes(payload)


__all__ = [
    "BLUEPRINT_DEPS",
    "INTENT",
    "SUB_KIND",
    "VAULT_SUBTREE",
    "ADMIN_RISK_SEVERITY_DEFAULT",
    "SUB_KIND_REGISTRY_REGISTERED_AT_V0_1",
    "ReflectionPacket",
    "PatternObservation",
    "ProposedLesson",
    "GatePassCounts",
    "ScoreSignals",
    "CycleOutcome",
    "PacketSpanProvenance",
    "to_canonical_bytes",
    "from_canonical_bytes",
]
