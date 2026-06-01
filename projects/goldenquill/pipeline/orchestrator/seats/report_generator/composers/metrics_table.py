"""§14.6.2 metrics_table sub-section composer.

Reads: operational-data ``metrics`` sub-kind + KFR canonical (cross-
validation) + ``proposal_commitments`` ``evaluation_criteria``
(target + tolerance per metric).

Scribe assembles the table row-by-row with
``metric_name | target | actual | variance | variance_explanation``
columns. KGIE preflight extended: every numeric value MUST have an
operational-data metrics OR KFR source in ``claim_evidence_map``.

ALL numeric arithmetic per the v7.0.4-M1 Decimal mandate — ANY float
comparison path is a defect. The composer's variance computation goes
through :func:`pipeline.logician.gates.f_report_numeric_drift.variance_pct`
which enforces the Decimal contract.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Mapping, Optional, Sequence

from .._schemas import ClaimEntry, SourceRef
from ._base import (
    ClockCallable,
    ComposerError,
    HashBytesCallable,
    ScribeFieldSpec,
    ScribeProtocol,
    VaultReadIntentCallable,
    compute_claim_id,
)


_SUB_SECTION: str = "metrics_table"


@dataclass(frozen=True, kw_only=True)
class MetricRow:
    """Pre-parsed view of one operational-data ``metrics`` row.

    Composer-level invariant: ``actual`` MUST be a :class:`decimal.Decimal`
    (Decimal mandate per v7.0.4-M1). The composer raises
    :class:`ComposerError` at coerce time if the parsed row contains a
    float.
    """

    metric_id: str
    source_path: str
    metric_name: str
    actual: Decimal
    unit: Optional[str]
    content_sha3_512: str
    related_commitment_id: Optional[str] = None
    related_evaluation_field: Optional[str] = None


@dataclass(frozen=True, kw_only=True)
class KfrMetricRow:
    """Pre-parsed view of one KFR canonical metric row (cross-validation).

    Same Decimal mandate as :class:`MetricRow`.
    """

    metric_name: str
    kfr_value: Decimal
    kfr_unit: Optional[str]
    source_path: str
    source_row_id: str
    source_content_sha3_512: str
    atomic_snapshot_id: str


@dataclass(frozen=True, kw_only=True)
class CommitmentMetricTarget:
    """Per-commitment numeric evaluation target derived from
    ``proposal_commitments.yaml`` ``evaluation_criteria`` rows.

    Composer matches by ``field`` name against the operational-data
    metric_name (case-sensitive); tolerance is a :class:`Decimal`
    (Decimal mandate).
    """

    commitment_id: str
    field_name: str
    target: Decimal
    tolerance: Decimal
    scope_tags_at_commitment: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, kw_only=True)
class MetricsTableDeps:
    read_metrics: VaultReadIntentCallable
    read_kfr_metrics: VaultReadIntentCallable
    read_commitment_targets: VaultReadIntentCallable
    read_template_field_specs: VaultReadIntentCallable
    scribe: ScribeProtocol
    clock: ClockCallable
    hash_bytes: HashBytesCallable


@dataclass(frozen=True, kw_only=True)
class MetricsTableResult:
    markdown_fragment: str
    claims: tuple[ClaimEntry, ...]
    rows_authored: int


def compose_metrics_table(
    *,
    deps: MetricsTableDeps,
    org_slug: str,
    grant_id: str,
    period_n: int,
    operational_data_root: str,
    proposal_commitments_path: str,
    reporting_template_path: str,
    kfr_register_path: str,
) -> MetricsTableResult:
    """Compose ``metrics_table`` per §14.6.2.

    Returns (markdown_fragment, claims). Composer-level invariants:

    1. Every metric ``actual`` is :class:`Decimal` (Decimal mandate).
    2. Every claim ``sub_section == "metrics_table"``.
    3. Every claim has at least one operational_data OR kfr source.
    4. ``claim_id`` is :func:`compute_claim_id`-derivable.
    """
    if period_n < 1:
        raise ComposerError(f"period_n must be >= 1; got {period_n!r}")

    field_specs_raw = deps.read_template_field_specs(
        kind="reporting_template",
        path=reporting_template_path,
        sub_section=_SUB_SECTION,
    )
    field_specs = _coerce_field_specs(field_specs_raw)
    metrics = _coerce_metrics(
        deps.read_metrics(
            kind="operational_data",
            sub_kind="metrics",
            path=f"{operational_data_root.rstrip('/')}/metrics",
            period_n=period_n,
        )
    )
    if not metrics:
        raise ComposerError(
            "metrics_table composer: zero operational-data metric rows for "
            f"period_n={period_n}"
        )

    kfr_metrics = _coerce_kfr_metrics(
        deps.read_kfr_metrics(
            kind="kfr",
            path=kfr_register_path,
            period_n=period_n,
        )
    )
    kfr_index: dict[str, KfrMetricRow] = {k.metric_name: k for k in kfr_metrics}

    commitment_targets = _coerce_commitment_targets(
        deps.read_commitment_targets(
            kind="proposal_commitments",
            path=proposal_commitments_path,
            sub_section=_SUB_SECTION,
        )
    )
    target_index: dict[str, CommitmentMetricTarget] = {
        t.field_name: t for t in commitment_targets
    }

    claims: list[ClaimEntry] = []
    rendered_rows: list[str] = []
    rendered_rows.append("| metric_name | target | actual | variance | variance_explanation |")
    rendered_rows.append("|---|---|---|---|---|")

    for m_idx, metric in enumerate(metrics):
        target_row = target_index.get(metric.metric_name)
        target_text = (
            str(target_row.target) if target_row is not None else ""
        )
        actual_text = str(metric.actual)
        variance_text = ""
        explanation_text = ""
        if target_row is not None and target_row.target != Decimal("0"):
            variance = _variance_pct_safe(
                actual=metric.actual, budgeted=target_row.target
            )
            variance_text = str(variance)
            spec = _find_spec(field_specs, metric.metric_name) or _default_table_spec()
            sources_for_scribe = _scribe_sources_for_metric(
                metric=metric,
                kfr_row=kfr_index.get(metric.metric_name),
                target_row=target_row,
            )
            explanation_text = deps.scribe(
                spec=spec, sources=sources_for_scribe
            )
            if not isinstance(explanation_text, str):
                raise ComposerError(
                    f"Scribe returned non-string for variance explanation: "
                    f"{type(explanation_text).__name__}"
                )

        rendered_rows.append(
            f"| {metric.metric_name} | {target_text} | {actual_text} | "
            f"{variance_text} | {explanation_text} |"
        )

        # One claim per metric row — the actual value is the claim.
        claim_id = compute_claim_id(
            sub_section=_SUB_SECTION,
            paragraph_index=0,
            sentence_index=m_idx,
            claim_text=f"{metric.metric_name}={metric.actual}",
        )
        refs = _source_refs_for_metric(
            metric=metric, kfr_row=kfr_index.get(metric.metric_name)
        )
        if not refs:
            raise ComposerError(
                f"metrics_table composer: metric {metric.metric_name!r} has no "
                f"operational-data OR KFR source (composer-level check)"
            )
        claims.append(
            ClaimEntry(
                claim_id=claim_id,
                sub_section=_SUB_SECTION,
                claim_text=f"{metric.metric_name}={metric.actual}",
                claim_kind="numeric",
                sources=refs,
            )
        )

    _validate_composer_invariants(claims=tuple(claims))

    return MetricsTableResult(
        markdown_fragment="\n".join(rendered_rows),
        claims=tuple(claims),
        rows_authored=len(metrics),
    )


# ---------------------------------------------------------------------------
# Decimal-mandate-safe variance computation
# ---------------------------------------------------------------------------


def _variance_pct_safe(*, actual: Decimal, budgeted: Decimal) -> Decimal:
    """Wrapper around ``f_report_numeric_drift.variance_pct``.

    Re-imports the gate's helper lazily to avoid module-load cycles.
    Defensive type-assertions mirror the gate-side Decimal mandate.
    """
    if not isinstance(actual, Decimal):
        raise ComposerError(
            f"variance computation requires Decimal actual; got "
            f"{type(actual).__name__} — Decimal mandate violation"
        )
    if not isinstance(budgeted, Decimal):
        raise ComposerError(
            f"variance computation requires Decimal budgeted; got "
            f"{type(budgeted).__name__} — Decimal mandate violation"
        )
    from pipeline.logician.gates.f_report_numeric_drift import variance_pct

    return variance_pct(actual=actual, budgeted=budgeted)


# ---------------------------------------------------------------------------
# Coercion helpers — guarded against float intrusion
# ---------------------------------------------------------------------------


def _to_decimal_strict(value: object, field_name: str) -> Decimal:
    """Coerce a value to Decimal, rejecting float outright."""
    if isinstance(value, Decimal):
        return value
    if isinstance(value, bool):
        raise ComposerError(
            f"{field_name}={value!r} is bool; must be Decimal/int/str"
        )
    if isinstance(value, float):
        raise ComposerError(
            f"{field_name}={value!r} is float; Decimal mandate violation "
            f"(per v7.0.4-M1)"
        )
    if isinstance(value, (int, str)):
        try:
            return Decimal(value)
        except (InvalidOperation, ValueError) as exc:
            raise ComposerError(
                f"{field_name}={value!r} not convertible to Decimal: {exc}"
            ) from exc
    raise ComposerError(
        f"{field_name}={value!r} type {type(value).__name__} not coercible to Decimal"
    )


def _coerce_metrics(raw: object) -> tuple[MetricRow, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, (list, tuple)):
        raise ComposerError(
            f"metrics rows must be list/tuple; got {type(raw).__name__}"
        )
    rows: list[MetricRow] = []
    for idx, r in enumerate(raw):
        if isinstance(r, MetricRow):
            rows.append(r)
            continue
        if not isinstance(r, Mapping):
            raise ComposerError(f"metrics[{idx}] not Mapping")
        try:
            rows.append(
                MetricRow(
                    metric_id=str(r["metric_id"]),
                    source_path=str(r["source_path"]),
                    metric_name=str(r["metric_name"]),
                    actual=_to_decimal_strict(r["actual"], f"metrics[{idx}].actual"),
                    unit=str(r["unit"]) if r.get("unit") is not None else None,
                    content_sha3_512=str(r["content_sha3_512"]),
                    related_commitment_id=(
                        str(r["related_commitment_id"])
                        if r.get("related_commitment_id") is not None
                        else None
                    ),
                    related_evaluation_field=(
                        str(r["related_evaluation_field"])
                        if r.get("related_evaluation_field") is not None
                        else None
                    ),
                )
            )
        except KeyError as exc:
            raise ComposerError(f"metrics[{idx}] missing key {exc!s}") from exc
    return tuple(rows)


def _coerce_kfr_metrics(raw: object) -> tuple[KfrMetricRow, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, (list, tuple)):
        raise ComposerError(
            f"kfr metrics must be list/tuple; got {type(raw).__name__}"
        )
    rows: list[KfrMetricRow] = []
    for idx, r in enumerate(raw):
        if isinstance(r, KfrMetricRow):
            rows.append(r)
            continue
        if not isinstance(r, Mapping):
            raise ComposerError(f"kfr_metrics[{idx}] not Mapping")
        try:
            rows.append(
                KfrMetricRow(
                    metric_name=str(r["metric_name"]),
                    kfr_value=_to_decimal_strict(
                        r["kfr_value"], f"kfr_metrics[{idx}].kfr_value"
                    ),
                    kfr_unit=str(r["kfr_unit"]) if r.get("kfr_unit") is not None else None,
                    source_path=str(r["source_path"]),
                    source_row_id=str(r["source_row_id"]),
                    source_content_sha3_512=str(r["source_content_sha3_512"]),
                    atomic_snapshot_id=str(r["atomic_snapshot_id"]),
                )
            )
        except KeyError as exc:
            raise ComposerError(f"kfr_metrics[{idx}] missing key {exc!s}") from exc
    return tuple(rows)


def _coerce_commitment_targets(raw: object) -> tuple[CommitmentMetricTarget, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, (list, tuple)):
        raise ComposerError(
            f"commitment targets must be list/tuple; got {type(raw).__name__}"
        )
    rows: list[CommitmentMetricTarget] = []
    for idx, r in enumerate(raw):
        if isinstance(r, CommitmentMetricTarget):
            rows.append(r)
            continue
        if not isinstance(r, Mapping):
            raise ComposerError(f"commitment_targets[{idx}] not Mapping")
        try:
            rows.append(
                CommitmentMetricTarget(
                    commitment_id=str(r["commitment_id"]),
                    field_name=str(r["field_name"]),
                    target=_to_decimal_strict(
                        r["target"], f"commitment_targets[{idx}].target"
                    ),
                    tolerance=_to_decimal_strict(
                        r.get("tolerance", 0),
                        f"commitment_targets[{idx}].tolerance",
                    ),
                    scope_tags_at_commitment=tuple(
                        str(s) for s in r.get("scope_tags_at_commitment", ())
                    ),
                )
            )
        except KeyError as exc:
            raise ComposerError(
                f"commitment_targets[{idx}] missing key {exc!s}"
            ) from exc
    return tuple(rows)


def _coerce_field_specs(raw: object) -> tuple[ScribeFieldSpec, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, (list, tuple)):
        return ()
    specs: list[ScribeFieldSpec] = []
    for row in raw:
        if isinstance(row, ScribeFieldSpec):
            specs.append(row)
        elif isinstance(row, Mapping):
            field_name = row.get("field") or row.get("field_name") or "variance_explanation"
            specs.append(
                ScribeFieldSpec(
                    sub_section=_SUB_SECTION,
                    field_name=str(field_name),
                    kind="structured_table",
                    column_specs=tuple(row.get("column_specs", ())),
                )
            )
    return tuple(specs)


def _default_table_spec() -> ScribeFieldSpec:
    return ScribeFieldSpec(
        sub_section=_SUB_SECTION,
        field_name="variance_explanation",
        kind="structured_table",
    )


def _find_spec(
    specs: Sequence[ScribeFieldSpec], metric_name: str
) -> Optional[ScribeFieldSpec]:
    for s in specs:
        if s.field_name == metric_name:
            return s
    return None


def _scribe_sources_for_metric(
    *,
    metric: MetricRow,
    kfr_row: Optional[KfrMetricRow],
    target_row: CommitmentMetricTarget,
) -> tuple[Mapping[str, object], ...]:
    """Source dicts for Scribe's variance-explanation drafting."""
    sources: list[Mapping[str, object]] = []
    sources.append(
        {
            "kind": "operational_data",
            "sub_kind": "metrics",
            "metric_id": metric.metric_id,
            "source_path": metric.source_path,
            "metric_name": metric.metric_name,
            "actual": str(metric.actual),
            "unit": metric.unit,
        }
    )
    if kfr_row is not None:
        sources.append(
            {
                "kind": "kfr",
                "source_path": kfr_row.source_path,
                "source_row_id": kfr_row.source_row_id,
                "metric_name": kfr_row.metric_name,
                "kfr_value": str(kfr_row.kfr_value),
                "kfr_unit": kfr_row.kfr_unit,
            }
        )
    sources.append(
        {
            "kind": "proposal_commitments",
            "commitment_id": target_row.commitment_id,
            "field_name": target_row.field_name,
            "target": str(target_row.target),
            "tolerance": str(target_row.tolerance),
        }
    )
    return tuple(sources)


def _source_refs_for_metric(
    *,
    metric: MetricRow,
    kfr_row: Optional[KfrMetricRow],
) -> tuple[SourceRef, ...]:
    refs: list[SourceRef] = [
        SourceRef(
            kind="operational_data",
            sub_kind="metrics",
            source_path=metric.source_path,
            source_row_id=metric.metric_id,
            source_content_sha3_512=metric.content_sha3_512,
            source_value=metric.actual,
        )
    ]
    if kfr_row is not None:
        refs.append(
            SourceRef(
                kind="kfr",
                source_path=kfr_row.source_path,
                source_row_id=kfr_row.source_row_id,
                source_content_sha3_512=kfr_row.source_content_sha3_512,
                source_value=kfr_row.kfr_value,
                kfr_atomic_snapshot_id=kfr_row.atomic_snapshot_id,
            )
        )
    return tuple(refs)


def _validate_composer_invariants(*, claims: tuple[ClaimEntry, ...]) -> None:
    if not claims:
        raise ComposerError("metrics_table composer produced zero claims")
    for c in claims:
        if c.sub_section != _SUB_SECTION:
            raise ComposerError(
                f"metrics_table claim {c.claim_id!r} sub_section={c.sub_section!r}"
            )
        if c.claim_kind != "numeric":
            raise ComposerError(
                f"metrics_table claim {c.claim_id!r} claim_kind={c.claim_kind!r}; "
                f"expected 'numeric'"
            )
        if not c.sources:
            raise ComposerError(
                f"metrics_table claim {c.claim_id!r} has no sources"
            )


__all__ = [
    "CommitmentMetricTarget",
    "KfrMetricRow",
    "MetricRow",
    "MetricsTableDeps",
    "MetricsTableResult",
    "compose_metrics_table",
]
