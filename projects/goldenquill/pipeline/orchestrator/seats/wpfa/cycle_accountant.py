"""WPFA Cycle Accountant. [§17 v1, §17.5]

Always-local seat. Deterministic composition of a CycleReceipt from
(a) the Logfire span tree at cycle close, (b) the SN-LLC-signed
Coefficient Registry, and (c) the operator-signed classification register.

Same Logfire export + same Coefficient Registry version →
byte-identical canonical-JSON output (§17.5.3 determinism mandate).

Code-phase extension (Cycle 2 RT-C2-03 fold-in, §17.5.3):
    Logfire export canonicalization. The export bytes are re-serialized
    with ``sort_keys=True, separators=(",", ":")`` BEFORE any aggregation
    read, forecloses determinism breaks introduced by future Logfire
    versions emitting maps with non-deterministic key ordering.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Protocol, runtime_checkable

from pipeline.vault.sub_kinds.coefficient_registry import (
    CoefficientEntry,
    CoefficientRegistry,
)
from pipeline.vault.sub_kinds.cycle_receipts import (
    CycleReceipt,
    CycleReceiptDelta,
    CycleReceiptDimensionTotals,
    PerModelCall,
    SpanProvenance,
)


@dataclass(frozen=True, kw_only=True)
class CycleAccountantInput:
    """Cycle Accountant input shape per §17.5.1."""

    run_id: str
    cycle_id: str
    org_slug: str
    cycle_close_marker_span_id: str
    logfire_export_path: str
    classification_register_version: str
    coefficient_registry_path: str
    dimensions_requested: tuple[str, ...]
    operator_attestation_requested: bool
    invoked_at_utc: str


@dataclass(frozen=True, kw_only=True)
class SpanRecord:
    """One Logfire span as Cycle Accountant consumes it.

    Frozen, kw_only — Cycle Accountant inputs are immutable.
    """

    span_id: str
    trace_id: str
    model_id: str
    input_tokens: int
    output_tokens: int


@runtime_checkable
class OperatorSigner(Protocol):
    """Operator Ed25519 signing callable.

    Returns the signature as 128-char lowercase hex over the canonical-JSON
    of the receipt's signing payload (CycleReceipt minus
    ``signed_by_operator_ed25519``). TTY-gated at the CLI layer per §11.7
    four-layer autopromote precedent.
    """

    def __call__(self, message_bytes: bytes) -> str: ...


def _bps_from_int(numerator: int, denominator: int) -> int:
    """ROUND_HALF_EVEN basis points = numerator / denominator * 10000.

    A12 — int-only arithmetic; ties round to even. Zero denominator returns
    0 (caller signals divide-by-zero via separate gate if needed).
    """
    if denominator == 0:
        return 0
    sign = 1 if (numerator >= 0) == (denominator > 0) else -1
    abs_num = abs(numerator * 10000)
    abs_den = abs(denominator)
    q, r = divmod(abs_num, abs_den)
    half = abs_den // 2
    # Banker's rounding (ROUND_HALF_EVEN): half goes to even
    if r > half:
        q += 1
    elif r == half and (abs_den % 2 == 0):
        # exact half — round to even
        if q % 2 == 1:
            q += 1
    elif r == half:
        q += 1
    return sign * q


def _aggregate_per_model(
    spans: Iterable[SpanRecord],
    registry: CoefficientRegistry,
) -> tuple[PerModelCall, ...]:
    """Aggregate spans into one PerModelCall per distinct model_id."""
    by_model: dict[str, dict[str, object]] = {}
    for span in spans:
        if not isinstance(span, SpanRecord):
            raise TypeError(f"span must be SpanRecord, got {type(span).__name__}")
        entry = registry.lookup(span.model_id)
        if entry is None:
            # Cycle Accountant relies on PRE-emission gate
            # F-WPFA-MODEL-COEFFICIENT-MISSING; if we hit this branch the
            # caller skipped that gate.
            raise ValueError(
                f"span model_id {span.model_id!r} not in registry "
                "(caller must run F-WPFA-MODEL-COEFFICIENT-MISSING PRE-gate)"
            )
        bucket = by_model.setdefault(
            span.model_id,
            {
                "is_local": entry.is_local,
                "hardware_sku": entry.hardware_sku,
                "input_tokens": 0,
                "output_tokens": 0,
                "dollars": 0,
                "watt_hours": 0,
                "span_ids": [],
            },
        )
        bucket["input_tokens"] = int(bucket["input_tokens"]) + span.input_tokens
        bucket["output_tokens"] = int(bucket["output_tokens"]) + span.output_tokens
        bucket["dollars"] = int(bucket["dollars"]) + _per_call_dollars(span, entry)
        bucket["watt_hours"] = int(bucket["watt_hours"]) + _per_call_energy(
            span, entry
        )
        bucket["span_ids"].append(span.span_id)  # type: ignore[union-attr]
    # Sort by model_id for deterministic output
    rows: list[PerModelCall] = []
    for model_id in sorted(by_model):
        b = by_model[model_id]
        rows.append(
            PerModelCall(
                model_id=model_id,
                is_local=bool(b["is_local"]),
                hardware_sku=(
                    None if b["hardware_sku"] is None else str(b["hardware_sku"])
                ),
                input_tokens=int(b["input_tokens"]),
                output_tokens=int(b["output_tokens"]),
                dollars_minor_units=int(b["dollars"]),
                watt_hours_micro=int(b["watt_hours"]),
                span_ids=tuple(sorted(b["span_ids"])),  # type: ignore[arg-type]
            )
        )
    return tuple(rows)


def _per_call_dollars(span: SpanRecord, entry: CoefficientEntry) -> int:
    """A12 int math: dollars_per_million_*_minor_units / 1_000_000 * tokens.

    To avoid integer truncation, compute (tokens * coeff) and then
    floor-divide by 1_000_000 at the very end. ROUND_HALF_EVEN on the
    final division is not applied here — operational receipts use floor
    for per-call rows; deltas use banker's rounding (§3.1 OQ-2 default).
    """
    inp = span.input_tokens * entry.dollars_per_million_input_tokens_minor_units
    out = span.output_tokens * entry.dollars_per_million_output_tokens_minor_units
    return (inp + out) // 1_000_000


def _per_call_energy(span: SpanRecord, entry: CoefficientEntry) -> int:
    """A12 int math for watt-hours; mirrors _per_call_dollars."""
    inp = (
        span.input_tokens
        * entry.watt_hours_per_million_input_tokens_micro
    )
    out = (
        span.output_tokens
        * entry.watt_hours_per_million_output_tokens_micro
    )
    return (inp + out) // 1_000_000


def _compute_counterfactual(
    actual_per_model: tuple[PerModelCall, ...],
    registry: CoefficientRegistry,
    currency: str,
) -> CycleReceiptDimensionTotals:
    """Compute 100%-routed-to-baseline counterfactual totals."""
    baseline_entry = registry.lookup(registry.baseline_model_id)
    if baseline_entry is None:
        raise ValueError(
            f"baseline_model_id {registry.baseline_model_id!r} unresolved — "
            "caller must run F-WPFA-BASELINE-MISSING PRE-gate first"
        )
    total_dollars = 0
    total_energy = 0
    for row in actual_per_model:
        # Use the baseline coefficients applied to the same tokens
        inp_d = (
            row.input_tokens
            * baseline_entry.dollars_per_million_input_tokens_minor_units
        )
        out_d = (
            row.output_tokens
            * baseline_entry.dollars_per_million_output_tokens_minor_units
        )
        total_dollars += (inp_d + out_d) // 1_000_000
        inp_e = (
            row.input_tokens
            * baseline_entry.watt_hours_per_million_input_tokens_micro
        )
        out_e = (
            row.output_tokens
            * baseline_entry.watt_hours_per_million_output_tokens_micro
        )
        total_energy += (inp_e + out_e) // 1_000_000
    return CycleReceiptDimensionTotals(
        dollars_total_minor_units=total_dollars,
        currency=currency,
        watt_hours_total_micro=total_energy,
        water_liters_micro=None,
        co2_grams_micro=None,
    )


def compose_receipt(
    inp: CycleAccountantInput,
    *,
    spans: Iterable[SpanRecord],
    registry: CoefficientRegistry,
    currency: str,
    classification_register_version: str,
    operator_signer: OperatorSigner | None = None,
) -> CycleReceipt:
    """Deterministic CycleReceipt composition.

    No I/O — caller injects spans + registry. Pre-emission gates are
    expected to have fired upstream; this function raises on internal
    consistency failures.

    Determinism: same spans + same registry + same classification register
    version → byte-identical CycleReceipt.
    """
    if not isinstance(inp, CycleAccountantInput):
        raise TypeError(
            f"inp must be CycleAccountantInput, got {type(inp).__name__}"
        )
    if not isinstance(registry, CoefficientRegistry):
        raise TypeError(
            f"registry must be CoefficientRegistry, got {type(registry).__name__}"
        )
    span_list = list(spans)
    actual_per_model = _aggregate_per_model(span_list, registry)
    actual_total = CycleReceiptDimensionTotals(
        dollars_total_minor_units=sum(
            row.dollars_minor_units for row in actual_per_model
        ),
        currency=currency,
        watt_hours_total_micro=sum(
            row.watt_hours_micro for row in actual_per_model
        ),
        water_liters_micro=None,
        co2_grams_micro=None,
    )
    counterfactual = _compute_counterfactual(
        actual_per_model, registry, currency
    )
    delta = CycleReceiptDelta(
        dollars_saved_minor_units=(
            counterfactual.dollars_total_minor_units
            - actual_total.dollars_total_minor_units
        ),
        watt_hours_saved_micro=(
            counterfactual.watt_hours_total_micro
            - actual_total.watt_hours_total_micro
        ),
        percent_dollars_saved=_bps_from_int(
            counterfactual.dollars_total_minor_units
            - actual_total.dollars_total_minor_units,
            (counterfactual.dollars_total_minor_units or 1),
        ),
        percent_watt_hours_saved=_bps_from_int(
            counterfactual.watt_hours_total_micro
            - actual_total.watt_hours_total_micro,
            (counterfactual.watt_hours_total_micro or 1),
        ),
        water_liters_saved_micro=None,
        co2_grams_saved_micro=None,
    )
    # Build span_provenance: every required claim key maps to >=1 span_id
    trace_ids = tuple(sorted({span.trace_id for span in span_list}))
    all_span_ids = tuple(sorted(span.span_id for span in span_list))
    per_claim_span_ids = {
        "actual.dollars_total": all_span_ids,
        "actual.watt_hours_total": all_span_ids,
        "counterfactual.dollars_total": all_span_ids,
        "counterfactual.watt_hours_total": all_span_ids,
        "delta.dollars_saved": all_span_ids,
        "delta.watt_hours_saved": all_span_ids,
    }
    span_provenance = SpanProvenance(
        trace_ids=trace_ids,
        logfire_export_uri=inp.logfire_export_path,
        cycle_close_marker_span_id=inp.cycle_close_marker_span_id,
        per_claim_span_ids=per_claim_span_ids,
    )
    # Build the unsigned receipt first; sign over its canonical bytes if
    # operator_signer is provided
    unsigned = CycleReceipt(
        cycle_id=inp.cycle_id,
        org_slug=inp.org_slug,
        schema_version="1.0.0",
        classification_register_version=classification_register_version,
        emitted_at=inp.invoked_at_utc,
        baseline_model_id=registry.baseline_model_id,
        baseline_quarter=registry.quarter,
        coefficients_registry_version=_registry_version(registry),
        coefficients_registry_signature_ed25519=registry.sn_llc_signature_ed25519,
        dimensions_active=tuple(sorted(set(inp.dimensions_requested))),
        actual=actual_total,
        actual_per_model=actual_per_model,
        counterfactual=counterfactual,
        delta=delta,
        span_provenance=span_provenance,
        signed_by_operator_ed25519=None,
    )
    if not inp.operator_attestation_requested or operator_signer is None:
        return unsigned
    # Operator-signed path: sign over canonical bytes of unsigned receipt
    from pipeline.vault.sub_kinds.cycle_receipts import to_canonical_bytes

    signing_payload = to_canonical_bytes(unsigned)
    sig_hex = operator_signer(signing_payload)
    if not isinstance(sig_hex, str) or len(sig_hex) != 128:
        raise ValueError(
            f"operator_signer must return 128-char hex, got "
            f"{type(sig_hex).__name__} len="
            f"{len(sig_hex) if isinstance(sig_hex, str) else 'N/A'}"
        )
    # Build a NEW frozen CycleReceipt with the signature populated
    return CycleReceipt(
        cycle_id=unsigned.cycle_id,
        org_slug=unsigned.org_slug,
        schema_version=unsigned.schema_version,
        classification_register_version=unsigned.classification_register_version,
        emitted_at=unsigned.emitted_at,
        baseline_model_id=unsigned.baseline_model_id,
        baseline_quarter=unsigned.baseline_quarter,
        coefficients_registry_version=unsigned.coefficients_registry_version,
        coefficients_registry_signature_ed25519=(
            unsigned.coefficients_registry_signature_ed25519
        ),
        dimensions_active=unsigned.dimensions_active,
        actual=unsigned.actual,
        actual_per_model=unsigned.actual_per_model,
        counterfactual=unsigned.counterfactual,
        delta=unsigned.delta,
        span_provenance=unsigned.span_provenance,
        signed_by_operator_ed25519=sig_hex,
    )


def _registry_version(registry: CoefficientRegistry) -> str:
    """Compute the registry version SHA3-512 over canonical bytes."""
    import hashlib

    from pipeline.vault.sub_kinds.coefficient_registry import to_canonical_bytes

    return hashlib.sha3_512(to_canonical_bytes(registry)).hexdigest()


# ---------------------------------------------------------------------------
# Logfire export canonicalization (RT-C2-03 fold-in, §17.5.3)
# ---------------------------------------------------------------------------


def canonicalize_logfire_export(raw_bytes: bytes) -> bytes:
    """Re-serialize a Logfire export with sorted keys + compact separators.

    Per §17.5.3 Cycle 2 RT-C2-03 fold-in: same Logfire export content →
    byte-identical canonical-JSON output, even across future Logfire
    versions that may emit maps with non-deterministic key ordering.

    Fails closed on non-JSON / non-UTF-8 input with
    ``F-WPFA-SCHEMA-INVALID.schema_drift_advisory`` per §17.5.3.
    """
    if not isinstance(raw_bytes, (bytes, bytearray)):
        raise TypeError(
            f"raw_bytes must be bytes|bytearray, got "
            f"{type(raw_bytes).__name__}"
        )
    try:
        parsed = json.loads(bytes(raw_bytes).decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(
            f"Logfire export is not valid UTF-8 JSON "
            f"(F-WPFA-SCHEMA-INVALID.schema_drift_advisory): {exc}"
        ) from exc
    return json.dumps(parsed, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


def load_spans_from_logfire_export(
    *,
    logfire_export_path: str | Path,
) -> tuple[tuple["SpanRecord", ...], bytes]:
    """Load + canonicalize a Logfire export. Returns (spans, canonical_bytes).

    Expected JSON shape: a top-level object with a ``spans`` array. Each
    span carries ``span_id``, ``trace_id``, ``model_id``, ``input_tokens``,
    ``output_tokens``. Spans without a ``model_id`` are filtered (not all
    spans are LLM-call spans).
    """
    path = Path(logfire_export_path)
    raw = path.read_bytes()
    canonical = canonicalize_logfire_export(raw)
    parsed = json.loads(canonical.decode("utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError(
            "Logfire export top-level must be an object with a 'spans' key"
        )
    spans_raw = parsed.get("spans", [])
    if not isinstance(spans_raw, list):
        raise ValueError("Logfire export 'spans' must be an array")
    spans: list[SpanRecord] = []
    for entry in spans_raw:
        if not isinstance(entry, dict):
            continue
        # Skip spans that aren't LLM-call spans (no model_id)
        if "model_id" not in entry:
            continue
        try:
            spans.append(
                SpanRecord(
                    span_id=str(entry["span_id"]),
                    trace_id=str(entry["trace_id"]),
                    model_id=str(entry["model_id"]),
                    input_tokens=int(entry["input_tokens"]),
                    output_tokens=int(entry["output_tokens"]),
                )
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(
                f"Logfire span entry malformed: {exc}; entry={entry!r}"
            ) from exc
    return tuple(spans), canonical


def collect_resolvable_span_ids(spans: Iterable["SpanRecord"]) -> frozenset[str]:
    """Return the set of span_ids present in the Logfire export.

    Used by ``F-WPFA-SPAN-PROVENANCE-MISSING.trace_id_unresolvable_in_logfire``
    to check that every claim's referenced span_id actually exists.
    """
    return frozenset(s.span_id for s in spans)


# ---------------------------------------------------------------------------
# Orchestrator hook — run_cycle_accountant_pipeline (§5 v8 cycle_close hook)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class CycleAccountantRunResult:
    """Outcome of a single cycle-close emission."""

    success: bool
    receipt: CycleReceipt | None
    receipt_canonical_bytes: bytes | None
    output_path: Path | None
    failure_codes: tuple[str, ...]
    detail: str


def run_cycle_accountant_pipeline(
    *,
    inp: CycleAccountantInput,
    registry: CoefficientRegistry,
    output_root: Path,
    currency: str = "USD",
    operator_signer: OperatorSigner | None = None,
) -> CycleAccountantRunResult:
    """End-to-end cycle-close emission.

    Workflow:
      1. Load + canonicalize the Logfire export (RT-C2-03).
      2. Compose the CycleReceipt deterministically.
      3. Encode + persist to
         ``<output_root>/orgs/<org_slug>/vault/operational/cycle_receipts/<cycle_id>.json``.
      4. Return the receipt + canonical bytes + output path.

    Fails closed on:
      - logfire export unreadable / non-canonical
      - model_id not in registry (raises from compose_receipt)
      - schema invariant violation at write
    """
    failures: list[str] = []
    try:
        spans, _canonical = load_spans_from_logfire_export(
            logfire_export_path=inp.logfire_export_path,
        )
    except (OSError, ValueError) as exc:
        return CycleAccountantRunResult(
            success=False,
            receipt=None,
            receipt_canonical_bytes=None,
            output_path=None,
            failure_codes=("F-WPFA-SCHEMA-INVALID",),
            detail=f"logfire export load failed: {exc}",
        )

    try:
        receipt = compose_receipt(
            inp,
            spans=spans,
            registry=registry,
            currency=currency,
            classification_register_version=inp.classification_register_version,
            operator_signer=operator_signer,
        )
    except (TypeError, ValueError) as exc:
        return CycleAccountantRunResult(
            success=False,
            receipt=None,
            receipt_canonical_bytes=None,
            output_path=None,
            failure_codes=("F-WPFA-SCHEMA-INVALID",),
            detail=f"compose_receipt failed: {exc}",
        )

    from pipeline.vault.sub_kinds.cycle_receipts import to_canonical_bytes

    canonical_receipt = to_canonical_bytes(receipt)
    out_dir = (
        output_root
        / "orgs"
        / receipt.org_slug
        / "vault"
        / "operational"
        / "cycle_receipts"
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{receipt.cycle_id}.json"

    # Law 3 + F-WPFA-CROSS-ORG-LEAK defense-in-depth: confirm the resolved
    # path includes the expected org_slug literally before write. This
    # mirrors operational_org_isolation Cedar rule.
    if f"/orgs/{receipt.org_slug}/" not in str(out_path):
        failures.append("F-WPFA-CROSS-ORG-LEAK")
        return CycleAccountantRunResult(
            success=False,
            receipt=receipt,
            receipt_canonical_bytes=canonical_receipt,
            output_path=None,
            failure_codes=tuple(failures),
            detail=(
                f"resolved write path {out_path!s} does not contain expected "
                f"org subtree /orgs/{receipt.org_slug}/ "
                "(F-WPFA-CROSS-ORG-LEAK structural Law 3 guard)"
            ),
        )

    # write-if-absent discipline per §2 v7.2 §1
    if out_path.exists():
        return CycleAccountantRunResult(
            success=False,
            receipt=receipt,
            receipt_canonical_bytes=canonical_receipt,
            output_path=out_path,
            failure_codes=("F-WPFA-SCHEMA-INVALID",),
            detail=(
                f"receipt for cycle_id={receipt.cycle_id!r} already exists at "
                f"{out_path!s}; re-emission requires explicit operator path "
                "per §17.16"
            ),
        )

    out_path.write_bytes(canonical_receipt)
    return CycleAccountantRunResult(
        success=True,
        receipt=receipt,
        receipt_canonical_bytes=canonical_receipt,
        output_path=out_path,
        failure_codes=(),
        detail=f"CycleReceipt persisted to {out_path!s}",
    )


def receipt_canonical_sha3_512(receipt: CycleReceipt) -> str:
    """Compute the SHA3-512 hex of the canonical receipt bytes.

    Used by the operator-signature signing path: the operator signs over
    the canonical-bytes hash, not the bytes themselves, to bound payload
    size and unify with the registry version mechanism.
    """
    from pipeline.vault.sub_kinds.cycle_receipts import to_canonical_bytes

    return hashlib.sha3_512(to_canonical_bytes(receipt)).hexdigest()


__all__ = [
    "CycleAccountantInput",
    "CycleAccountantRunResult",
    "OperatorSigner",
    "SpanRecord",
    "canonicalize_logfire_export",
    "collect_resolvable_span_ids",
    "compose_receipt",
    "load_spans_from_logfire_export",
    "receipt_canonical_sha3_512",
    "run_cycle_accountant_pipeline",
]
