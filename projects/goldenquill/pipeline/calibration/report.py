"""pipeline.calibration.report — §5.6 CalibrationReport + canonical bytes.

Blueprint §5 v6 LOCKED 2026-04-19:
- §5.6 CalibrationReport dataclass (15 fields; blueprint-authoritative shape)
- §5.6 CalibrationReportItem dataclass (7 fields)
- §5.6.4 canonical-bytes enumeration (exhaustive field-level table)
- §7.16 canonical-bytes exhaustiveness invariant
- §4.15 step 7 assemble_from_run

**Relationship to pipeline.loop.types.** The loop-types module ships simpler
7-field ``CalibrationReport`` / 7-field ``CalibrationReportItem`` dataclasses
that were LOCKED at Round 1. This module ships the blueprint-§5.6 15-field /
7-field shapes that §4.15 actually drives. The two shapes coexist — callers
import from the module whose surface matches the data they hold. R12.A
signing + assembly operate exclusively against the blueprint shapes here.

**Canonical bytes (§5.6.4 exhaustive table):**

Every field on ``CalibrationReport``, ``CalibrationReportItem``, and the
referenced ``GoldenSetItem`` (imported from ``pipeline.calibration.golden_set``)
is EITHER serialized by ``canonical_bytes()`` OR explicitly listed in the
exclusion table below. The invariant (§7.16) is that the signed payload is a
total function of the dataclass field set.

Exclusions (the ONLY two):
- ``CalibrationReport.signature`` — the signature cannot cover itself.
- ``CalibrationReport.canonical_sha256`` — this field stores the hash OF the
  canonical bytes; the receiver recomputes and compares, so including it
  would be circular.

Everything else is canonical-INCLUDED. Adding a new field to any of the
dataclasses MUST either fall through ``canonical_bytes()`` automatically (via
``dataclasses.asdict`` + sort_keys) OR add an explicit exclusion entry with
paired rationale and paired §9.9.30 AST-grep test update.

**V1 discipline:** inline-literal RHS comparisons; canonical serialization
uses ``json.dumps(..., sort_keys=True, separators=(", ", ": "), ensure_ascii=False)``
after NFC normalization on every string leaf.

Spec card: ``pipeline/engineering/spec_cards/section_05_round_12_run_eval_pipeline.md``
(R12.A split).
"""

from __future__ import annotations

import hashlib
import json
import statistics
import unicodedata
from dataclasses import asdict, dataclass, field, fields
from typing import Any, Final, Literal

from pipeline.loop.config import CALIBRATION_REPORT_SCHEMA_VERSION
from pipeline.loop.errors import F_PIPE_22

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_05_pipeline.md": {
        "version": "v6",
        "hash_sha3_512_prefix16": "feb5928491e4dc40",
        "sections_implemented": [
            "§5.6 CalibrationReport (blueprint-authoritative 15-field shape)",
            "§5.6 CalibrationReportItem (7-field shape)",
            "§5.6.4 canonical-bytes enumeration (exhaustive)",
            "§7.16 canonical-bytes exhaustiveness invariant",
            "§4.15 step 7 assemble_from_run",
        ],
    },
}

# ---------------------------------------------------------------------------
# Module-load integrity asserts (V1 discipline)
# ---------------------------------------------------------------------------

# The imported constant must still equal the inline-literal value. A rebind of
# ``pipeline.loop.config.CALIBRATION_REPORT_SCHEMA_VERSION`` would have been
# caught at that module's own load assert; this second assert is defence-in-
# depth for import-order anomalies.
assert CALIBRATION_REPORT_SCHEMA_VERSION == 1, (
    "pipeline.loop.config.CALIBRATION_REPORT_SCHEMA_VERSION has been rebound "
    "before pipeline.calibration.report import; refusing to load"
)

# Exhaustive exclusion table — sourced directly from blueprint §5.6.4. The
# exclusion rationale is embedded so the exhaustiveness AST-grep test can
# assert both membership AND rationale coverage.
_CANONICAL_BYTES_EXCLUSIONS: Final[dict[str, str]] = {
    "signature": "the signature cannot cover itself",
    "canonical_sha256": "field stores the hash OF canonical bytes; "
    "receiver recomputes and compares",
}
assert len(_CANONICAL_BYTES_EXCLUSIONS) == 2, (
    "_CANONICAL_BYTES_EXCLUSIONS has been rebound at module load; "
    "refusing to load pipeline.calibration.report"
)


# ---------------------------------------------------------------------------
# §5.6 CalibrationReportItem (7 fields, blueprint-authoritative)
# ---------------------------------------------------------------------------


_REVISION_LOOP_OUTCOMES: Final[frozenset[str]] = frozenset(
    {
        "pass_iter1",
        "pass_iter2",
        "pass_iter3",
        "iter_cap_no_pass",
        "plateau_no_pass",
    }
)
assert len(_REVISION_LOOP_OUTCOMES) == 5, (
    "_REVISION_LOOP_OUTCOMES has been rebound at module load; "
    "refusing to load pipeline.calibration.report"
)


@dataclass(frozen=True, slots=True, kw_only=True)
class CalibrationReportItem:
    """§5.6 — one golden-set item's per-run calibration outcome."""

    item_id: str
    judge_total_score: int
    judge_per_dimension: dict[str, int]
    editor_critique_summary: str
    iterations_used: int
    revision_loop_outcome: Literal[
        "pass_iter1",
        "pass_iter2",
        "pass_iter3",
        "iter_cap_no_pass",
        "plateau_no_pass",
    ]
    item_run_id: str

    def __post_init__(self) -> None:
        if not self.item_id:
            raise ValueError("CalibrationReportItem.item_id must be non-empty")
        if not (0 <= self.judge_total_score <= 100):
            raise ValueError(
                f"CalibrationReportItem.judge_total_score must be in [0, 100]; "
                f"got {self.judge_total_score}"
            )
        if not (1 <= self.iterations_used <= 3):
            raise ValueError(
                f"CalibrationReportItem.iterations_used must be in [1, 3]; "
                f"got {self.iterations_used}"
            )
        # Inline-literal frozenset (V1 discipline).
        if self.revision_loop_outcome not in frozenset(
            {
                "pass_iter1",
                "pass_iter2",
                "pass_iter3",
                "iter_cap_no_pass",
                "plateau_no_pass",
            }
        ):
            raise ValueError(
                f"CalibrationReportItem.revision_loop_outcome invalid; "
                f"got {self.revision_loop_outcome!r}"
            )
        if not isinstance(self.judge_per_dimension, dict):
            raise TypeError(
                f"CalibrationReportItem.judge_per_dimension must be dict; "
                f"got {type(self.judge_per_dimension).__name__}"
            )
        for dim_name, dim_score in self.judge_per_dimension.items():
            if not isinstance(dim_name, str) or not dim_name:
                raise ValueError(
                    "CalibrationReportItem.judge_per_dimension key must be "
                    "non-empty str"
                )
            if not isinstance(dim_score, int) or not (0 <= dim_score <= 10):
                raise ValueError(
                    f"CalibrationReportItem.judge_per_dimension[{dim_name!r}] "
                    f"must be int in [0, 10]; got {dim_score!r}"
                )
        if not self.item_run_id:
            raise ValueError("CalibrationReportItem.item_run_id must be non-empty")


# ---------------------------------------------------------------------------
# §5.6 CalibrationReport (15 fields, blueprint-authoritative)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True, kw_only=True)
class CalibrationReport:
    """§5.6 — signed aggregate calibration report for one eval_mode run.

    15 fields. Canonical bytes include all EXCEPT ``signature`` and
    ``canonical_sha256`` (see module docstring for rationale).

    ``signature`` is ``None`` before §4.15 step 10 (``sign_report``); it is
    populated with the Ed25519 detached signature after. ``signed_at_iso``
    is similarly ``None`` before signing. Both become non-None together at
    the sign step.

    ``canonical_sha256`` is the SHA-256 of ``canonical_bytes(...)``; it is
    computed at assembly time (``assemble_from_run``) and re-verified at
    ``verify_calibration_report`` time.
    """

    schema_version: int
    run_id: str
    operator_org_slug: str
    golden_set_manifest_path: str
    golden_set_manifest_hash: str
    items: tuple[CalibrationReportItem, ...]
    summary_judge_mean: float
    summary_judge_stddev: float
    summary_per_dimension_mean: dict[str, float]
    council_charter_snapshot_hash: str
    router_yaml_snapshot_hash: str
    assembled_at_iso: str
    canonical_sha256: str
    signature: bytes | None = None
    signed_at_iso: str | None = None

    def __post_init__(self) -> None:
        # schema_version — inline-literal RHS.
        if self.schema_version != 1:
            raise F_PIPE_22(
                trigger="calibration_report_schema_mismatch",
                details={
                    "shape": "CalibrationReport",
                    "observed": self.schema_version,
                    "expected": 1,
                },
            )
        if not self.run_id:
            raise ValueError("CalibrationReport.run_id must be non-empty")
        if not self.operator_org_slug:
            raise ValueError(
                "CalibrationReport.operator_org_slug must be non-empty"
            )
        if not self.golden_set_manifest_path:
            raise ValueError(
                "CalibrationReport.golden_set_manifest_path must be non-empty"
            )
        if not self.golden_set_manifest_hash:
            raise ValueError(
                "CalibrationReport.golden_set_manifest_hash must be non-empty"
            )
        if not isinstance(self.items, tuple):
            raise TypeError(
                f"CalibrationReport.items must be tuple; "
                f"got {type(self.items).__name__}"
            )
        for idx, it in enumerate(self.items):
            if not isinstance(it, CalibrationReportItem):
                raise TypeError(
                    f"CalibrationReport.items[{idx}] must be "
                    f"CalibrationReportItem; got {type(it).__name__}"
                )
        if not isinstance(self.summary_per_dimension_mean, dict):
            raise TypeError(
                "CalibrationReport.summary_per_dimension_mean must be dict"
            )
        if not self.council_charter_snapshot_hash:
            raise ValueError(
                "CalibrationReport.council_charter_snapshot_hash must be non-empty"
            )
        if not self.router_yaml_snapshot_hash:
            raise ValueError(
                "CalibrationReport.router_yaml_snapshot_hash must be non-empty"
            )
        if not self.assembled_at_iso:
            raise ValueError(
                "CalibrationReport.assembled_at_iso must be non-empty"
            )
        # ``canonical_sha256`` may be "" pre-assembly (see assemble_from_run
        # which recomputes). Accept empty at construction; signing asserts
        # non-empty at its own gate.
        if not isinstance(self.canonical_sha256, str):
            raise TypeError(
                "CalibrationReport.canonical_sha256 must be str"
            )
        # signature/signed_at_iso must be both-None or both-non-None.
        sig_none = self.signature is None
        ts_none = self.signed_at_iso is None
        if sig_none != ts_none:
            raise ValueError(
                f"CalibrationReport.signature and signed_at_iso must be "
                f"both None or both non-None; got "
                f"signature={'None' if sig_none else 'bytes'}, "
                f"signed_at_iso={self.signed_at_iso!r}"
            )
        if self.signature is not None and not isinstance(self.signature, bytes):
            raise TypeError(
                f"CalibrationReport.signature must be bytes or None; "
                f"got {type(self.signature).__name__}"
            )


# ---------------------------------------------------------------------------
# Canonical bytes — §5.6.4 exhaustive enumeration
# ---------------------------------------------------------------------------


def _nfc_normalize_leaves(obj: Any) -> Any:  # noqa: ANN401 — recursive JSON shape
    """Apply Unicode NFC normalization to every string leaf.

    Mirrors the TabEnvelope canonical-bytes discipline (blueprint §5.6.4
    prose: "sorted keys, UTF-8, NFC-normalized text, separator `, `, no
    trailing whitespace"). Recursively descends dict / list / tuple / str
    leaves; other scalars pass through.
    """
    if isinstance(obj, str):
        return unicodedata.normalize("NFC", obj)
    if isinstance(obj, dict):
        return {k: _nfc_normalize_leaves(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_nfc_normalize_leaves(v) for v in obj]
    if isinstance(obj, tuple):
        return [_nfc_normalize_leaves(v) for v in obj]
    return obj


def canonical_bytes(report: CalibrationReport) -> bytes:
    """Compute canonical signing bytes per §5.6.4.

    Rules:
    1. Start from ``dataclasses.asdict(report)`` — recursively flattens
       nested dataclasses (items + CalibrationReportItem fields).
    2. Pop the two excluded keys (``signature``, ``canonical_sha256``) —
       inline-literal frozenset RHS (V1 discipline).
    3. NFC-normalize every string leaf recursively.
    4. ``json.dumps(..., sort_keys=True, separators=(", ", ": "),
       ensure_ascii=False)`` — deterministic across Python dict insertion
       order, NFC-stable, human-readable separator per blueprint prose.
    5. Encode as UTF-8.

    The ``bytes`` return is the exact input to the Ed25519 signing operation.
    """
    # Step 1.
    payload = asdict(report)

    # Step 2 — inline-literal exclusion set (V1 discipline; rebind-resistant).
    for excluded in frozenset({"signature", "canonical_sha256"}):
        payload.pop(excluded, None)

    # Step 3.
    normalized = _nfc_normalize_leaves(payload)

    # Step 4+5.
    return json.dumps(
        normalized,
        sort_keys=True,
        separators=(", ", ": "),
        ensure_ascii=False,
    ).encode("utf-8")


def compute_canonical_sha256(report: CalibrationReport) -> str:
    """SHA-256 hex-digest of ``canonical_bytes(report)``."""
    return hashlib.sha256(canonical_bytes(report)).hexdigest()


def canonical_bytes_exclusions() -> dict[str, str]:
    """Return a fresh copy of the §5.6.4 exclusion table.

    Exposed for §9.9.30 AST-grep test consumption. Returns a copy so
    callers cannot mutate the module-level table.
    """
    return dict(_CANONICAL_BYTES_EXCLUSIONS)


def calibration_report_field_set() -> frozenset[str]:
    """Return the set of declared ``CalibrationReport`` field names.

    Used by the §9.9.30 exhaustiveness test: every declared field must be
    either serialised by ``canonical_bytes()`` OR in the exclusion table.
    """
    return frozenset(f.name for f in fields(CalibrationReport))


def calibration_report_item_field_set() -> frozenset[str]:
    """Return the set of declared ``CalibrationReportItem`` field names."""
    return frozenset(f.name for f in fields(CalibrationReportItem))


# ---------------------------------------------------------------------------
# §4.15 step 7 — assemble_from_run
# ---------------------------------------------------------------------------


def _mean(xs: list[float]) -> float:
    """Arithmetic mean; 0.0 on empty list (empty golden-set edge case)."""
    if not xs:
        return 0.0
    return statistics.fmean(xs)


def _stddev(xs: list[float]) -> float:
    """Population stddev; 0.0 on lists of length 0 or 1."""
    if len(xs) < 2:
        return 0.0
    return statistics.pstdev(xs)


def _per_dimension_means(
    per_item_dims: list[dict[str, int]],
) -> dict[str, float]:
    """Compute per-dimension arithmetic means across items.

    The dimension-key universe is the UNION of every item's keys (items may
    have different dimension sets if the rubric drifted mid-run, though in
    v0.1 that is prevented by the per-item charter lock). A dimension present
    in only a subset of items is averaged over only those items where it
    appears.
    """
    agg: dict[str, list[int]] = {}
    for dims in per_item_dims:
        for k, v in dims.items():
            agg.setdefault(k, []).append(v)
    return {k: _mean([float(x) for x in vs]) for k, vs in agg.items()}


@dataclass(frozen=True, slots=True, kw_only=True)
class AssembleInputs:
    """Caller-supplied inputs for ``assemble_from_run``.

    Packaged as a dataclass so the call site's kwargs stay flat and the
    function signature is stable across v0.2 additions (e.g., per-seat
    observability snapshots).
    """

    run_id: str
    operator_org_slug: str
    golden_set_manifest_path: str
    golden_set_manifest_hash: str
    per_item_results: tuple[CalibrationReportItem, ...]
    council_charter_snapshot_hash: str
    router_yaml_snapshot_hash: str
    assembled_at_iso: str


def assemble_from_run(inputs: AssembleInputs) -> CalibrationReport:
    """§4.15 step 7 — build an unsigned ``CalibrationReport`` from per-item results.

    The returned report has:
    - ``schema_version = 1`` (inline-literal; rebind-resistant).
    - ``items`` in the order supplied by the caller (manifest order; §4.15
      step 6a-6e preserves this).
    - ``summary_judge_mean`` / ``summary_judge_stddev`` / ``summary_per_dimension_mean``
      computed from the items.
    - ``canonical_sha256`` set to the hash of the canonical bytes of the
      fully-populated-but-unsigned report (computed via a throwaway
      construction with ``canonical_sha256=""`` to break circularity;
      blueprint §5.6.4 table: ``canonical_sha256`` is N/A to canonical bytes).
    - ``signature = None``, ``signed_at_iso = None`` (signing lands at
      ``pipeline.calibration.signing.sign_report``).

    :raises F_PIPE_22: if any ``CalibrationReportItem`` carries a schema
        mismatch (propagated from its own ``__post_init__``).
    """
    if not inputs.run_id:
        raise ValueError("AssembleInputs.run_id must be non-empty")
    if not inputs.operator_org_slug:
        raise ValueError("AssembleInputs.operator_org_slug must be non-empty")
    if not inputs.per_item_results:
        # Empty golden set: still legal (operator may curate an empty
        # manifest pre-population); assembles with mean=0, stddev=0, empty
        # per-dimension dict. Edge-case tested by R12.A adversarial test.
        pass

    totals = [float(it.judge_total_score) for it in inputs.per_item_results]
    per_dim_dicts = [dict(it.judge_per_dimension) for it in inputs.per_item_results]

    summary_mean = _mean(totals)
    summary_stddev = _stddev(totals)
    per_dim_mean = _per_dimension_means(per_dim_dicts)

    # Build unsigned report with canonical_sha256="" first, then recompute.
    unsigned_skeleton = CalibrationReport(
        schema_version=1,
        run_id=inputs.run_id,
        operator_org_slug=inputs.operator_org_slug,
        golden_set_manifest_path=inputs.golden_set_manifest_path,
        golden_set_manifest_hash=inputs.golden_set_manifest_hash,
        items=tuple(inputs.per_item_results),
        summary_judge_mean=summary_mean,
        summary_judge_stddev=summary_stddev,
        summary_per_dimension_mean=per_dim_mean,
        council_charter_snapshot_hash=inputs.council_charter_snapshot_hash,
        router_yaml_snapshot_hash=inputs.router_yaml_snapshot_hash,
        assembled_at_iso=inputs.assembled_at_iso,
        canonical_sha256="",
        signature=None,
        signed_at_iso=None,
    )
    digest = compute_canonical_sha256(unsigned_skeleton)

    # Re-materialize with the computed digest.
    return CalibrationReport(
        schema_version=1,
        run_id=inputs.run_id,
        operator_org_slug=inputs.operator_org_slug,
        golden_set_manifest_path=inputs.golden_set_manifest_path,
        golden_set_manifest_hash=inputs.golden_set_manifest_hash,
        items=tuple(inputs.per_item_results),
        summary_judge_mean=summary_mean,
        summary_judge_stddev=summary_stddev,
        summary_per_dimension_mean=per_dim_mean,
        council_charter_snapshot_hash=inputs.council_charter_snapshot_hash,
        router_yaml_snapshot_hash=inputs.router_yaml_snapshot_hash,
        assembled_at_iso=inputs.assembled_at_iso,
        canonical_sha256=digest,
        signature=None,
        signed_at_iso=None,
    )


# ---------------------------------------------------------------------------
# JSON round-trip (on-disk persistence — step 8 write + step 10 verify read)
# ---------------------------------------------------------------------------


def report_to_json(report: CalibrationReport) -> bytes:
    """Serialize a CalibrationReport to JSON bytes for vault persistence.

    The signature (if present) is base64-encoded to survive JSON.
    Deserialization via ``report_from_json`` round-trips identity.
    """
    import base64

    payload = asdict(report)
    # Tuple-of-dataclasses ``items`` was already flattened by asdict to list.
    # Convert base64-safe signature representation.
    if payload.get("signature") is not None:
        payload["signature"] = base64.b64encode(report.signature or b"").decode(
            "ascii"
        )
    return json.dumps(
        payload, sort_keys=True, separators=(", ", ": "), ensure_ascii=False
    ).encode("utf-8")


def report_from_json(payload: bytes) -> CalibrationReport:
    """Inverse of ``report_to_json``.

    :raises F_PIPE_22: on ``calibration_report_schema_mismatch``.
    :raises json.JSONDecodeError: on malformed payload.
    :raises KeyError: on missing required field.
    """
    import base64

    data = json.loads(payload.decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError("CalibrationReport payload is not a JSON object")

    observed_schema = data.get("schema_version")
    # Inline-literal RHS.
    if observed_schema != 1:
        raise F_PIPE_22(
            trigger="calibration_report_schema_mismatch",
            details={
                "shape": "CalibrationReport",
                "observed": observed_schema,
                "expected": 1,
            },
        )

    items_raw = data.get("items", [])
    items = tuple(
        CalibrationReportItem(
            item_id=str(it["item_id"]),
            judge_total_score=int(it["judge_total_score"]),
            judge_per_dimension={
                str(k): int(v) for k, v in it["judge_per_dimension"].items()
            },
            editor_critique_summary=str(it.get("editor_critique_summary", "")),
            iterations_used=int(it["iterations_used"]),
            revision_loop_outcome=it["revision_loop_outcome"],
            item_run_id=str(it["item_run_id"]),
        )
        for it in items_raw
    )

    sig_encoded = data.get("signature")
    signature: bytes | None = (
        base64.b64decode(sig_encoded.encode("ascii"))
        if isinstance(sig_encoded, str) and sig_encoded
        else None
    )

    return CalibrationReport(
        schema_version=1,
        run_id=str(data["run_id"]),
        operator_org_slug=str(data["operator_org_slug"]),
        golden_set_manifest_path=str(data["golden_set_manifest_path"]),
        golden_set_manifest_hash=str(data["golden_set_manifest_hash"]),
        items=items,
        summary_judge_mean=float(data["summary_judge_mean"]),
        summary_judge_stddev=float(data["summary_judge_stddev"]),
        summary_per_dimension_mean={
            str(k): float(v) for k, v in data["summary_per_dimension_mean"].items()
        },
        council_charter_snapshot_hash=str(data["council_charter_snapshot_hash"]),
        router_yaml_snapshot_hash=str(data["router_yaml_snapshot_hash"]),
        assembled_at_iso=str(data["assembled_at_iso"]),
        canonical_sha256=str(data["canonical_sha256"]),
        signature=signature,
        signed_at_iso=data.get("signed_at_iso"),
    )


__all__ = [
    "BLUEPRINT_DEPS",
    "AssembleInputs",
    "CalibrationReport",
    "CalibrationReportItem",
    "assemble_from_run",
    "calibration_report_field_set",
    "calibration_report_item_field_set",
    "canonical_bytes",
    "canonical_bytes_exclusions",
    "compute_canonical_sha256",
    "report_from_json",
    "report_to_json",
]
