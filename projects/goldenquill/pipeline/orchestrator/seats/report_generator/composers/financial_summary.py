"""§14.6.3 financial_summary sub-section composer.

Reads: operational-data ``financials`` sub-kind +
``proposal_commitments`` ``evaluation_criteria`` (budget line targets +
tolerance).

ALL monetary values are :class:`decimal.Decimal` per v7.0.4-M1 mandate.
Any float in the arithmetic path is a defect; coercion fails closed.
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


_SUB_SECTION: str = "financial_summary"


@dataclass(frozen=True, kw_only=True)
class FinancialActualRow:
    """Pre-parsed view of one operational-data ``financials`` row.

    All monetary values are :class:`Decimal`. Float coercion fails closed.
    """

    line_id: str
    source_path: str
    budget_line: str
    actuals: Decimal
    content_sha3_512: str
    related_commitment_id: Optional[str] = None


@dataclass(frozen=True, kw_only=True)
class CommitmentBudgetTarget:
    """Per-commitment budget-line target derived from
    ``proposal_commitments.yaml`` ``evaluation_criteria``."""

    commitment_id: str
    budget_line: str
    budgeted: Decimal
    tolerance_pct: Decimal
    scope_tags_at_commitment: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, kw_only=True)
class FinancialSummaryDeps:
    read_financials: VaultReadIntentCallable
    read_commitment_budgets: VaultReadIntentCallable
    read_template_field_specs: VaultReadIntentCallable
    scribe: ScribeProtocol
    clock: ClockCallable
    hash_bytes: HashBytesCallable


@dataclass(frozen=True, kw_only=True)
class FinancialSummaryResult:
    markdown_fragment: str
    claims: tuple[ClaimEntry, ...]
    lines_authored: int


def compose_financial_summary(
    *,
    deps: FinancialSummaryDeps,
    org_slug: str,
    grant_id: str,
    period_n: int,
    operational_data_root: str,
    proposal_commitments_path: str,
    reporting_template_path: str,
) -> FinancialSummaryResult:
    """Compose ``financial_summary`` per §14.6.3.

    Composer-level invariants:

    1. Every monetary value is :class:`Decimal` (Decimal mandate).
    2. Every claim ``sub_section == "financial_summary"`` and
       ``claim_kind == "financial"``.
    3. Every claim has at least one operational_data source.
    """
    if period_n < 1:
        raise ComposerError(f"period_n must be >= 1; got {period_n!r}")

    field_specs = _coerce_field_specs(
        deps.read_template_field_specs(
            kind="reporting_template",
            path=reporting_template_path,
            sub_section=_SUB_SECTION,
        )
    )
    financials = _coerce_financials(
        deps.read_financials(
            kind="operational_data",
            sub_kind="financials",
            path=f"{operational_data_root.rstrip('/')}/financials",
            period_n=period_n,
        )
    )
    if not financials:
        raise ComposerError(
            "financial_summary composer: zero operational-data financial rows "
            f"for period_n={period_n}"
        )

    budgets = _coerce_commitment_budgets(
        deps.read_commitment_budgets(
            kind="proposal_commitments",
            path=proposal_commitments_path,
            sub_section=_SUB_SECTION,
        )
    )
    budget_index: dict[str, CommitmentBudgetTarget] = {
        b.budget_line: b for b in budgets
    }

    rendered_rows: list[str] = []
    rendered_rows.append("| budget_line | budgeted | actuals | variance | variance_explanation |")
    rendered_rows.append("|---|---|---|---|---|")

    claims: list[ClaimEntry] = []
    for idx, actual_row in enumerate(financials):
        budget = budget_index.get(actual_row.budget_line)
        if budget is None:
            budgeted_text = ""
            variance_text = ""
            explanation_text = ""
        else:
            budgeted_text = str(budget.budgeted)
            variance = _signed_variance(
                budgeted=budget.budgeted, actuals=actual_row.actuals
            )
            variance_text = str(variance)
            spec = _find_spec(field_specs, actual_row.budget_line) or _default_spec()
            sources_for_scribe = _scribe_sources_for_line(
                actual_row=actual_row, budget=budget
            )
            explanation_text = deps.scribe(
                spec=spec, sources=sources_for_scribe
            )
            if not isinstance(explanation_text, str):
                raise ComposerError(
                    f"Scribe returned non-string for financial variance: "
                    f"{type(explanation_text).__name__}"
                )

        rendered_rows.append(
            f"| {actual_row.budget_line} | {budgeted_text} | "
            f"{str(actual_row.actuals)} | {variance_text} | {explanation_text} |"
        )

        claim_id = compute_claim_id(
            sub_section=_SUB_SECTION,
            paragraph_index=0,
            sentence_index=idx,
            claim_text=f"{actual_row.budget_line}={actual_row.actuals}",
        )
        refs = (
            SourceRef(
                kind="operational_data",
                sub_kind="financials",
                source_path=actual_row.source_path,
                source_row_id=actual_row.line_id,
                source_content_sha3_512=actual_row.content_sha3_512,
                source_value=actual_row.actuals,
            ),
        )
        if budget is not None:
            refs = refs + (
                SourceRef(
                    kind="proposal_commitments",
                    commitment_id=budget.commitment_id,
                    commitment_status="PROMOTED",
                    scope_tags_at_commitment=budget.scope_tags_at_commitment,
                ),
            )
        claims.append(
            ClaimEntry(
                claim_id=claim_id,
                sub_section=_SUB_SECTION,
                claim_text=f"{actual_row.budget_line}={actual_row.actuals}",
                claim_kind="financial",
                sources=refs,
            )
        )

    _validate_composer_invariants(claims=tuple(claims))

    return FinancialSummaryResult(
        markdown_fragment="\n".join(rendered_rows),
        claims=tuple(claims),
        lines_authored=len(financials),
    )


# ---------------------------------------------------------------------------
# Decimal arithmetic (signed variance)
# ---------------------------------------------------------------------------


def _signed_variance(*, budgeted: Decimal, actuals: Decimal) -> Decimal:
    """``actuals - budgeted`` — Decimal subtraction (no float)."""
    if not isinstance(budgeted, Decimal) or not isinstance(actuals, Decimal):
        raise ComposerError(
            "_signed_variance requires Decimal inputs; Decimal mandate "
            "violation (per v7.0.4-M1)"
        )
    return actuals - budgeted


# ---------------------------------------------------------------------------
# Coercion helpers
# ---------------------------------------------------------------------------


def _to_decimal_strict(value: object, field_name: str) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, bool):
        raise ComposerError(f"{field_name}={value!r} is bool")
    if isinstance(value, float):
        raise ComposerError(
            f"{field_name}={value!r} is float; Decimal mandate violation"
        )
    if isinstance(value, (int, str)):
        try:
            return Decimal(value)
        except (InvalidOperation, ValueError) as exc:
            raise ComposerError(
                f"{field_name}={value!r} not convertible to Decimal: {exc}"
            ) from exc
    raise ComposerError(
        f"{field_name}={value!r} type {type(value).__name__} not coercible"
    )


def _coerce_financials(raw: object) -> tuple[FinancialActualRow, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, (list, tuple)):
        raise ComposerError(
            f"financials rows must be list/tuple; got {type(raw).__name__}"
        )
    rows: list[FinancialActualRow] = []
    for idx, r in enumerate(raw):
        if isinstance(r, FinancialActualRow):
            rows.append(r)
            continue
        if not isinstance(r, Mapping):
            raise ComposerError(f"financials[{idx}] not Mapping")
        try:
            rows.append(
                FinancialActualRow(
                    line_id=str(r["line_id"]),
                    source_path=str(r["source_path"]),
                    budget_line=str(r["budget_line"]),
                    actuals=_to_decimal_strict(
                        r["actuals"], f"financials[{idx}].actuals"
                    ),
                    content_sha3_512=str(r["content_sha3_512"]),
                    related_commitment_id=(
                        str(r["related_commitment_id"])
                        if r.get("related_commitment_id") is not None
                        else None
                    ),
                )
            )
        except KeyError as exc:
            raise ComposerError(f"financials[{idx}] missing key {exc!s}") from exc
    return tuple(rows)


def _coerce_commitment_budgets(raw: object) -> tuple[CommitmentBudgetTarget, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, (list, tuple)):
        raise ComposerError(
            f"commitment_budgets must be list/tuple; got {type(raw).__name__}"
        )
    rows: list[CommitmentBudgetTarget] = []
    for idx, r in enumerate(raw):
        if isinstance(r, CommitmentBudgetTarget):
            rows.append(r)
            continue
        if not isinstance(r, Mapping):
            raise ComposerError(f"commitment_budgets[{idx}] not Mapping")
        try:
            rows.append(
                CommitmentBudgetTarget(
                    commitment_id=str(r["commitment_id"]),
                    budget_line=str(r["budget_line"]),
                    budgeted=_to_decimal_strict(
                        r["budgeted"], f"commitment_budgets[{idx}].budgeted"
                    ),
                    tolerance_pct=_to_decimal_strict(
                        r.get("tolerance_pct", 0),
                        f"commitment_budgets[{idx}].tolerance_pct",
                    ),
                    scope_tags_at_commitment=tuple(
                        str(s) for s in r.get("scope_tags_at_commitment", ())
                    ),
                )
            )
        except KeyError as exc:
            raise ComposerError(
                f"commitment_budgets[{idx}] missing key {exc!s}"
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


def _default_spec() -> ScribeFieldSpec:
    return ScribeFieldSpec(
        sub_section=_SUB_SECTION,
        field_name="variance_explanation",
        kind="structured_table",
    )


def _find_spec(
    specs: Sequence[ScribeFieldSpec], budget_line: str
) -> Optional[ScribeFieldSpec]:
    for s in specs:
        if s.field_name == budget_line:
            return s
    return None


def _scribe_sources_for_line(
    *,
    actual_row: FinancialActualRow,
    budget: CommitmentBudgetTarget,
) -> tuple[Mapping[str, object], ...]:
    return (
        {
            "kind": "operational_data",
            "sub_kind": "financials",
            "line_id": actual_row.line_id,
            "source_path": actual_row.source_path,
            "budget_line": actual_row.budget_line,
            "actuals": str(actual_row.actuals),
        },
        {
            "kind": "proposal_commitments",
            "commitment_id": budget.commitment_id,
            "budget_line": budget.budget_line,
            "budgeted": str(budget.budgeted),
            "tolerance_pct": str(budget.tolerance_pct),
        },
    )


def _validate_composer_invariants(*, claims: tuple[ClaimEntry, ...]) -> None:
    if not claims:
        raise ComposerError("financial_summary composer produced zero claims")
    for c in claims:
        if c.sub_section != _SUB_SECTION:
            raise ComposerError(
                f"financial_summary claim {c.claim_id!r} sub_section={c.sub_section!r}"
            )
        if c.claim_kind != "financial":
            raise ComposerError(
                f"financial_summary claim {c.claim_id!r} claim_kind="
                f"{c.claim_kind!r}; expected 'financial'"
            )
        if not c.sources:
            raise ComposerError(
                f"financial_summary claim {c.claim_id!r} has no sources"
            )


__all__ = [
    "CommitmentBudgetTarget",
    "FinancialActualRow",
    "FinancialSummaryDeps",
    "FinancialSummaryResult",
    "compose_financial_summary",
]
