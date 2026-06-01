"""``cycle_receipt`` sub-kind — WPFA cycle-close telemetry artifact. [§17 v1]

Schema + canonical-bytes codec + record-id derivation for the
CycleReceipt Pydantic shape emitted by the Cycle Accountant at every
cycle close.

Severity defaults YELLOW; elevates to RED when ``signed_by_operator_ed25519``
is non-None (buyer-attested receipts need admin-risk attention before
ship).

A12 Decimal mandate is **extended to energy quantities** per §17.3.5 —
``watt_hours_total_micro`` is ``int`` micro-watt-hours (10^-6 Wh), never
float. Float arithmetic on energy fields is an R-WPFA-DECIMAL-MANDATE-
ENERGY AST-lint violation.

Blueprint authority:
    - section_17_watts_per_funding_action.md §17.3 (schema)
    - section_17_watts_per_funding_action.md §17.3.3 (sub-kind registry row)
    - section_04_v2_x_z_wpfa_amendment.md §5.1.WPFA.11 (F-WPFA-SCHEMA-INVALID)
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
    "section_17_watts_per_funding_action.md": {
        "version": "v1-LOCKED-2026-05-11",
        "sections_implemented": [
            "§17.3.1 CycleReceipt schema",
            "§17.3.2 nested shapes",
            "§17.3.3 SUB_KIND_REGISTRY row",
            "§17.3.4 invariants",
        ],
    },
}

INTENT: Final[str] = "operational-cycle-receipt-write"
SUB_KIND: Final[str] = "cycle_receipt"
VAULT_SUBTREE: Final[str] = "operational/cycle_receipts/"
ADMIN_RISK_SEVERITY_DEFAULT: Final[str] = "YELLOW"

_SEMVER_RE: Final[re.Pattern[str]] = re.compile(r"^\d+\.\d+\.\d+$")
_SHA3_512_HEX_RE: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{128}$")
# Cycle 2 RT-C2-05 FIX-IN-PLACE: strict cycle_id grammar prevents path-traversal
# via crafted values (`../evil`, `..\\foo`, leading slash, etc.). cycle_id is
# the filename for the on-disk receipt; only A-Za-z0-9 plus hyphen/underscore
# are admitted. Length floor 1, ceiling 128 to bound filesystem path lengths.
_CYCLE_ID_RE: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z0-9_-]{1,128}$")
_QUARTER_RE: Final[re.Pattern[str]] = re.compile(r"^Q[1-4]-\d{4}$")
_UTC_ISO_RE: Final[re.Pattern[str]] = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$"
)
_ALLOWED_DIMENSIONS: Final[frozenset[str]] = frozenset(
    {"dollars", "energy", "water", "co2"}
)
_V0_1_DIMENSIONS: Final[tuple[str, ...]] = ("dollars", "energy")
_ED25519_HEX_LEN: Final[int] = 128  # 64 bytes hex-encoded


def _ensure_non_neg_int(value: object, field_name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(
            f"{field_name} must be int (A12 mandate — int minor units / "
            f"micro-units, never float; bool excluded), got "
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


# ---------------------------------------------------------------------------
# Nested shapes
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class CycleReceiptDimensionTotals:
    """Per-dimension totals: actual or counterfactual."""

    dollars_total_minor_units: int
    currency: str
    watt_hours_total_micro: int
    water_liters_micro: int | None = None  # v0.2 forward-compat
    co2_grams_micro: int | None = None  # v0.2 forward-compat

    def __post_init__(self) -> None:
        _ensure_non_neg_int(self.dollars_total_minor_units, "dollars_total_minor_units")
        if (
            not isinstance(self.currency, str)
            or len(self.currency) != 3
            or not self.currency.isalpha()
            or self.currency != self.currency.upper()
        ):
            raise ValueError(
                "currency must be a 3-letter uppercase ISO-4217 code"
            )
        _ensure_non_neg_int(self.watt_hours_total_micro, "watt_hours_total_micro")
        for opt_field, opt_value in (
            ("water_liters_micro", self.water_liters_micro),
            ("co2_grams_micro", self.co2_grams_micro),
        ):
            if opt_value is not None:
                _ensure_non_neg_int(opt_value, opt_field)


@dataclass(frozen=True, kw_only=True)
class PerModelCall:
    """One aggregated row per distinct model_id in the cycle's span tree."""

    model_id: str
    is_local: bool
    hardware_sku: str | None
    input_tokens: int
    output_tokens: int
    dollars_minor_units: int
    watt_hours_micro: int
    span_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.model_id, str) or not self.model_id:
            raise ValueError("model_id must be a non-empty string")
        if not isinstance(self.is_local, bool):
            raise ValueError("is_local must be bool")
        if self.is_local:
            if not isinstance(self.hardware_sku, str) or not self.hardware_sku:
                raise ValueError(
                    "is_local=True requires non-empty hardware_sku"
                )
        else:
            if self.hardware_sku is not None:
                raise ValueError(
                    "is_local=False requires hardware_sku=None"
                )
        for fname, fval in (
            ("input_tokens", self.input_tokens),
            ("output_tokens", self.output_tokens),
            ("dollars_minor_units", self.dollars_minor_units),
            ("watt_hours_micro", self.watt_hours_micro),
        ):
            _ensure_non_neg_int(fval, fname)
        if not isinstance(self.span_ids, tuple) or not self.span_ids:
            raise ValueError("span_ids must be a non-empty tuple of str")
        for sid in self.span_ids:
            if not isinstance(sid, str) or not sid:
                raise ValueError("each span_id must be a non-empty string")


@dataclass(frozen=True, kw_only=True)
class CycleReceiptDelta:
    """Regenerative-savings delta = counterfactual - actual."""

    dollars_saved_minor_units: int
    watt_hours_saved_micro: int
    percent_dollars_saved: int  # basis points; ROUND_HALF_EVEN
    percent_watt_hours_saved: int
    water_liters_saved_micro: int | None = None  # v0.2
    co2_grams_saved_micro: int | None = None  # v0.2

    def __post_init__(self) -> None:
        # delta values MAY be negative (anti-pattern: cloud actually saved
        # energy over local). We range-check only the percent fields.
        _ensure_int(self.dollars_saved_minor_units, "dollars_saved_minor_units")
        _ensure_int(self.watt_hours_saved_micro, "watt_hours_saved_micro")
        _ensure_int(self.percent_dollars_saved, "percent_dollars_saved")
        _ensure_int(self.percent_watt_hours_saved, "percent_watt_hours_saved")
        for opt_field, opt_value in (
            ("water_liters_saved_micro", self.water_liters_saved_micro),
            ("co2_grams_saved_micro", self.co2_grams_saved_micro),
        ):
            if opt_value is not None:
                _ensure_int(opt_value, opt_field)


@dataclass(frozen=True, kw_only=True)
class SpanProvenance:
    """Per-claim Logfire span_id mapping + cycle-close marker pointer."""

    trace_ids: tuple[str, ...]
    logfire_export_uri: str | None
    cycle_close_marker_span_id: str
    per_claim_span_ids: Mapping[str, tuple[str, ...]]

    def __post_init__(self) -> None:
        if not isinstance(self.trace_ids, tuple) or not self.trace_ids:
            raise ValueError("trace_ids must be a non-empty tuple of str")
        for tid in self.trace_ids:
            if not isinstance(tid, str) or not tid:
                raise ValueError("each trace_id must be a non-empty string")
        if self.logfire_export_uri is not None and (
            not isinstance(self.logfire_export_uri, str)
            or not self.logfire_export_uri
        ):
            raise ValueError(
                "logfire_export_uri must be None or non-empty string"
            )
        if (
            not isinstance(self.cycle_close_marker_span_id, str)
            or not self.cycle_close_marker_span_id
        ):
            raise ValueError(
                "cycle_close_marker_span_id must be a non-empty string"
            )
        if not isinstance(self.per_claim_span_ids, Mapping):
            raise ValueError("per_claim_span_ids must be a Mapping")
        if not self.per_claim_span_ids:
            raise ValueError(
                "per_claim_span_ids must be non-empty — F-WPFA-SPAN-"
                "PROVENANCE-MISSING.claim_key_unmapped guard"
            )
        for claim_key, sids in self.per_claim_span_ids.items():
            if not isinstance(claim_key, str) or not claim_key:
                raise ValueError("claim_key must be a non-empty string")
            if not isinstance(sids, tuple) or not sids:
                raise ValueError(
                    f"per_claim_span_ids[{claim_key!r}] must be a non-empty "
                    "tuple of span_ids — F-WPFA-SPAN-PROVENANCE-"
                    "MISSING.no_trace_id guard"
                )
            for s in sids:
                if not isinstance(s, str) or not s:
                    raise ValueError(
                        f"per_claim_span_ids[{claim_key!r}] entry must be "
                        "non-empty string"
                    )


# ---------------------------------------------------------------------------
# Top-level CycleReceipt
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class CycleReceipt:
    """Cycle-close telemetry artifact per §17 v1."""

    # Identity + provenance
    cycle_id: str
    org_slug: str
    schema_version: str
    classification_register_version: str

    # Emission context
    emitted_at: str
    baseline_model_id: str
    baseline_quarter: str
    coefficients_registry_version: str
    coefficients_registry_signature_ed25519: str

    # Active dimensions
    dimensions_active: tuple[str, ...]

    # Actual consumption
    actual: CycleReceiptDimensionTotals
    actual_per_model: tuple[PerModelCall, ...]

    # Counterfactual
    counterfactual: CycleReceiptDimensionTotals

    # Delta
    delta: CycleReceiptDelta

    # Provenance
    span_provenance: SpanProvenance

    # Operator attestation
    signed_by_operator_ed25519: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.cycle_id, str) or not self.cycle_id:
            raise ValueError("cycle_id must be a non-empty string")
        if not _CYCLE_ID_RE.match(self.cycle_id):
            # Cycle 2 RT-C2-05 FIX-IN-PLACE: strict cycle_id grammar prevents
            # path-traversal via crafted values. cycle_id MUST match
            # ^[A-Za-z0-9_-]{1,128}$. Path separators, dots, leading slashes,
            # and any other special chars fail-close.
            raise ValueError(
                "cycle_id must match ^[A-Za-z0-9_-]{1,128}$ "
                "(F-WPFA-SCHEMA-INVALID guard; RT-C2-05 path-traversal defense)"
            )
        if not isinstance(self.org_slug, str) or not self.org_slug:
            raise ValueError("org_slug must be a non-empty string")
        if not _SEMVER_RE.match(self.schema_version):
            raise ValueError(
                "schema_version must match semver ^\\d+\\.\\d+\\.\\d+$"
            )
        if not _SHA3_512_HEX_RE.match(self.classification_register_version):
            raise ValueError(
                "classification_register_version must be 128-hex-char SHA3-512"
            )
        if not _UTC_ISO_RE.match(self.emitted_at):
            raise ValueError(
                "emitted_at must be UTC ISO-8601 ending in 'Z'"
            )
        if not isinstance(self.baseline_model_id, str) or not self.baseline_model_id:
            raise ValueError("baseline_model_id must be non-empty string")
        if not _QUARTER_RE.match(self.baseline_quarter):
            raise ValueError("baseline_quarter must match ^Q[1-4]-\\d{4}$")
        if not _SHA3_512_HEX_RE.match(self.coefficients_registry_version):
            raise ValueError(
                "coefficients_registry_version must be 128-hex-char SHA3-512"
            )
        if (
            not isinstance(self.coefficients_registry_signature_ed25519, str)
            or len(self.coefficients_registry_signature_ed25519) != _ED25519_HEX_LEN
            or not all(
                c in "0123456789abcdef"
                for c in self.coefficients_registry_signature_ed25519.lower()
            )
        ):
            raise ValueError(
                "coefficients_registry_signature_ed25519 must be "
                f"{_ED25519_HEX_LEN}-char lowercase hex"
            )
        if not isinstance(self.dimensions_active, tuple) or not self.dimensions_active:
            raise ValueError(
                "dimensions_active must be a non-empty tuple of str"
            )
        for d in self.dimensions_active:
            if d not in _ALLOWED_DIMENSIONS:
                raise ValueError(
                    f"dimensions_active entry {d!r} not in "
                    f"{sorted(_ALLOWED_DIMENSIONS)}"
                )
        # Currency identity
        if self.actual.currency != self.counterfactual.currency:
            raise ValueError(
                "actual.currency must equal counterfactual.currency "
                "(no mixed-currency receipts)"
            )
        # Delta arithmetic invariant
        expected_d_dollars = (
            self.counterfactual.dollars_total_minor_units
            - self.actual.dollars_total_minor_units
        )
        if self.delta.dollars_saved_minor_units != expected_d_dollars:
            raise ValueError(
                "delta.dollars_saved_minor_units != counterfactual - actual "
                "(F-WPFA-SCHEMA-INVALID.delta_arithmetic_mismatch)"
            )
        expected_d_energy = (
            self.counterfactual.watt_hours_total_micro
            - self.actual.watt_hours_total_micro
        )
        if self.delta.watt_hours_saved_micro != expected_d_energy:
            raise ValueError(
                "delta.watt_hours_saved_micro != counterfactual - actual "
                "(F-WPFA-SCHEMA-INVALID.delta_arithmetic_mismatch)"
            )
        # Per-model aggregate identity
        if not isinstance(self.actual_per_model, tuple):
            raise ValueError("actual_per_model must be a tuple")
        dollars_sum = sum(
            row.dollars_minor_units for row in self.actual_per_model
        )
        if dollars_sum != self.actual.dollars_total_minor_units:
            raise ValueError(
                "sum(actual_per_model[*].dollars_minor_units) != "
                "actual.dollars_total_minor_units "
                "(F-WPFA-SCHEMA-INVALID.per_model_aggregate_mismatch)"
            )
        energy_sum = sum(row.watt_hours_micro for row in self.actual_per_model)
        if energy_sum != self.actual.watt_hours_total_micro:
            raise ValueError(
                "sum(actual_per_model[*].watt_hours_micro) != "
                "actual.watt_hours_total_micro "
                "(F-WPFA-SCHEMA-INVALID.per_model_aggregate_mismatch)"
            )
        # Operator signature shape (if non-None)
        if self.signed_by_operator_ed25519 is not None:
            sig = self.signed_by_operator_ed25519
            if (
                not isinstance(sig, str)
                or len(sig) != _ED25519_HEX_LEN
                or not all(c in "0123456789abcdef" for c in sig.lower())
            ):
                raise ValueError(
                    "signed_by_operator_ed25519 must be None or "
                    f"{_ED25519_HEX_LEN}-char lowercase hex"
                )

    @property
    def is_buyer_attested(self) -> bool:
        """True iff this receipt carries an operator attestation."""
        return self.signed_by_operator_ed25519 is not None


# ---------------------------------------------------------------------------
# Canonical codec
# ---------------------------------------------------------------------------


def to_canonical_bytes(record: CycleReceipt) -> bytes:
    if not isinstance(record, CycleReceipt):
        raise TypeError(
            f"record must be CycleReceipt, got {type(record).__name__}"
        )
    return to_canonical_json_bytes(record)


def from_canonical_bytes(payload: bytes) -> CycleReceipt:
    parsed = from_canonical_json_bytes(payload)
    # Decode nested structures explicitly to enforce int re-validation
    # (catches tampered float fields per F-WPFA-SCHEMA-INVALID.numeric_field_float)
    actual_raw = parsed["actual"]
    actual = CycleReceiptDimensionTotals(
        dollars_total_minor_units=_decode_int(
            actual_raw["dollars_total_minor_units"], "actual.dollars_total_minor_units"
        ),
        currency=str(actual_raw["currency"]),
        watt_hours_total_micro=_decode_int(
            actual_raw["watt_hours_total_micro"], "actual.watt_hours_total_micro"
        ),
        water_liters_micro=_decode_opt_int(
            actual_raw.get("water_liters_micro"), "actual.water_liters_micro"
        ),
        co2_grams_micro=_decode_opt_int(
            actual_raw.get("co2_grams_micro"), "actual.co2_grams_micro"
        ),
    )
    counterfactual_raw = parsed["counterfactual"]
    counterfactual = CycleReceiptDimensionTotals(
        dollars_total_minor_units=_decode_int(
            counterfactual_raw["dollars_total_minor_units"],
            "counterfactual.dollars_total_minor_units",
        ),
        currency=str(counterfactual_raw["currency"]),
        watt_hours_total_micro=_decode_int(
            counterfactual_raw["watt_hours_total_micro"],
            "counterfactual.watt_hours_total_micro",
        ),
        water_liters_micro=_decode_opt_int(
            counterfactual_raw.get("water_liters_micro"),
            "counterfactual.water_liters_micro",
        ),
        co2_grams_micro=_decode_opt_int(
            counterfactual_raw.get("co2_grams_micro"),
            "counterfactual.co2_grams_micro",
        ),
    )
    delta_raw = parsed["delta"]
    delta = CycleReceiptDelta(
        dollars_saved_minor_units=_decode_int_signed(
            delta_raw["dollars_saved_minor_units"], "delta.dollars_saved_minor_units"
        ),
        watt_hours_saved_micro=_decode_int_signed(
            delta_raw["watt_hours_saved_micro"], "delta.watt_hours_saved_micro"
        ),
        percent_dollars_saved=_decode_int_signed(
            delta_raw["percent_dollars_saved"], "delta.percent_dollars_saved"
        ),
        percent_watt_hours_saved=_decode_int_signed(
            delta_raw["percent_watt_hours_saved"], "delta.percent_watt_hours_saved"
        ),
        water_liters_saved_micro=_decode_opt_int_signed(
            delta_raw.get("water_liters_saved_micro"),
            "delta.water_liters_saved_micro",
        ),
        co2_grams_saved_micro=_decode_opt_int_signed(
            delta_raw.get("co2_grams_saved_micro"), "delta.co2_grams_saved_micro"
        ),
    )
    per_model = tuple(
        PerModelCall(
            model_id=str(r["model_id"]),
            is_local=bool(r["is_local"]),
            hardware_sku=(
                None if r.get("hardware_sku") is None else str(r["hardware_sku"])
            ),
            input_tokens=_decode_int(r["input_tokens"], "per_model.input_tokens"),
            output_tokens=_decode_int(r["output_tokens"], "per_model.output_tokens"),
            dollars_minor_units=_decode_int(
                r["dollars_minor_units"], "per_model.dollars_minor_units"
            ),
            watt_hours_micro=_decode_int(
                r["watt_hours_micro"], "per_model.watt_hours_micro"
            ),
            span_ids=tuple(str(s) for s in r["span_ids"]),
        )
        for r in parsed["actual_per_model"]
    )
    sp_raw = parsed["span_provenance"]
    span_provenance = SpanProvenance(
        trace_ids=tuple(str(t) for t in sp_raw["trace_ids"]),
        logfire_export_uri=(
            None
            if sp_raw.get("logfire_export_uri") is None
            else str(sp_raw["logfire_export_uri"])
        ),
        cycle_close_marker_span_id=str(sp_raw["cycle_close_marker_span_id"]),
        per_claim_span_ids={
            str(k): tuple(str(s) for s in v)
            for k, v in sp_raw["per_claim_span_ids"].items()
        },
    )
    return CycleReceipt(
        cycle_id=str(parsed["cycle_id"]),
        org_slug=str(parsed["org_slug"]),
        schema_version=str(parsed["schema_version"]),
        classification_register_version=str(
            parsed["classification_register_version"]
        ),
        emitted_at=str(parsed["emitted_at"]),
        baseline_model_id=str(parsed["baseline_model_id"]),
        baseline_quarter=str(parsed["baseline_quarter"]),
        coefficients_registry_version=str(parsed["coefficients_registry_version"]),
        coefficients_registry_signature_ed25519=str(
            parsed["coefficients_registry_signature_ed25519"]
        ),
        dimensions_active=tuple(str(d) for d in parsed["dimensions_active"]),
        actual=actual,
        actual_per_model=per_model,
        counterfactual=counterfactual,
        delta=delta,
        span_provenance=span_provenance,
        signed_by_operator_ed25519=(
            None
            if parsed.get("signed_by_operator_ed25519") is None
            else str(parsed["signed_by_operator_ed25519"])
        ),
    )


def _decode_int(value: object, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(
            f"{field_name} must decode as int (A12 mandate; F-WPFA-SCHEMA-"
            f"INVALID.numeric_field_float), got {type(value).__name__}"
        )
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0, got {value!r}")
    return value


def _decode_int_signed(value: object, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(
            f"{field_name} must decode as int (A12 mandate; F-WPFA-SCHEMA-"
            f"INVALID.numeric_field_float), got {type(value).__name__}"
        )
    return value


def _decode_opt_int(value: object, field_name: str) -> int | None:
    if value is None:
        return None
    return _decode_int(value, field_name)


def _decode_opt_int_signed(value: object, field_name: str) -> int | None:
    if value is None:
        return None
    return _decode_int_signed(value, field_name)


def record_id_for(record: CycleReceipt) -> str:
    return record.cycle_id


__all__ = [
    "CycleReceipt",
    "CycleReceiptDimensionTotals",
    "PerModelCall",
    "CycleReceiptDelta",
    "SpanProvenance",
    "INTENT",
    "SUB_KIND",
    "VAULT_SUBTREE",
    "ADMIN_RISK_SEVERITY_DEFAULT",
    "to_canonical_bytes",
    "from_canonical_bytes",
    "record_id_for",
]
