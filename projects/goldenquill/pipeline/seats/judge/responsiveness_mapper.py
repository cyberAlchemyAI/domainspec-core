"""pipeline.seats.judge.responsiveness_mapper — §9 R2 responsiveness factor mapper.

Extracts "responsiveness factors" — categorical claims about applicant
identity, project category, or beneficiary group — from a rubric's
**raw JSON** and bundles them into a frozen
:class:`pipeline.seats.judge.types.ResponsivenessMap` keyed by
criterion id + factor name.

Why a separate raw-JSON path: the
:class:`pipeline.seats.judge.types.Rubric` shape only preserves the
six fields the dimension scorer needs (``id`` / ``name`` /
``max_points`` / ``scorer`` / ``subcriteria`` / ``must_address`` /
``tiers``). The "responsiveness" data — VAPG ``f.i.qualifying_categories``,
``f.ii.qualifying_applicants`` / ``must_benefit``, ``g.categories[*].name``
— lives elsewhere in the JSON. R2 ships
:func:`extract_responsiveness_factors_from_rubric_json` to walk the raw
JSON and pull these fields, plus :func:`build_responsiveness_map` to
assemble the final :class:`ResponsivenessMap` (the latter is callable
from non-VAPG rubrics with arbitrary criterion-extras input).

Closed-set discipline: only a known set of factor keys is recognized
(see :data:`KNOWN_RESPONSIVENESS_FACTOR_KEYS`). Unknown keys are
silently skipped — the rubric loader is the authoritative shape gate
for non-responsiveness keys; the mapper does not police rubric schema
beyond its own factor extraction.

Pure-deterministic: stdlib + intra-package imports only; zero LLM, zero
network, zero subprocess, no I/O.

Threat model (R2):

- **In scope.** Empty / missing factor key → factor not emitted.
  Duplicate ``(criterion_id, factor_name)`` keys in input → rejected at
  :class:`ResponsivenessMap` construction (caller-side malformed input).
  Non-string factor value → rejected by :class:`ResponsivenessEntry`
  ``__post_init__``. ``categories`` factor with malformed entries
  (non-mapping, missing ``name`` field, empty / non-string ``name``) →
  ``ValueError``.
- **Out of scope, deferred.** Cross-rubric responsiveness reconciliation
  (e.g., REAP's ``rural_area_certified`` factor vs. VAPG's
  ``qualifying_applicants`` overlap); responsiveness-driven score
  adjustment (the mapper produces metadata; scoring stays criterion-
  bound through :func:`pipeline.seats.judge.dimension_scorer.score_dimension`).
"""

from __future__ import annotations

from typing import Any, Final, Mapping, Sequence

from pipeline.seats.judge.types import (
    ResponsivenessEntry,
    ResponsivenessMap,
    Rubric,
)


# ---------------------------------------------------------------------------
# Closed-set factor keys — V1 inline literal rebind-resistance
# ---------------------------------------------------------------------------

KNOWN_RESPONSIVENESS_FACTOR_KEYS: Final[frozenset[str]] = frozenset(
    {
        "qualifying_categories",
        "qualifying_applicants",
        "must_benefit",
        "categories",
    }
)

# Subset whose value is a JSON list of strings (flat list).
_LIST_OF_STR_FACTOR_KEYS: Final[frozenset[str]] = frozenset(
    {
        "qualifying_categories",
        "qualifying_applicants",
        "must_benefit",
    }
)

# Subset whose value is a JSON list of objects each carrying a "name"
# field (we flatten the names into factor_values).
_LIST_OF_OBJECT_NAME_FACTOR_KEYS: Final[frozenset[str]] = frozenset(
    {
        "categories",
    }
)


# ---------------------------------------------------------------------------
# Internal extraction helpers
# ---------------------------------------------------------------------------


def _coerce_str_list(
    value: Any, *, where: str
) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(
            f"responsiveness_mapper: {where} must be a JSON array of "
            f"strings; got {type(value).__name__}."
        )
    out: list[str] = []
    for i, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise ValueError(
                f"responsiveness_mapper: {where}[{i}] must be a "
                f"non-empty string; got {item!r}."
            )
        out.append(item)
    return tuple(out)


def _coerce_object_name_list(
    value: Any, *, where: str
) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(
            f"responsiveness_mapper: {where} must be a JSON array of "
            f"objects; got {type(value).__name__}."
        )
    out: list[str] = []
    for i, entry in enumerate(value):
        if not isinstance(entry, Mapping):
            raise ValueError(
                f"responsiveness_mapper: {where}[{i}] must be a JSON "
                f"object; got {type(entry).__name__}."
            )
        name = entry.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(
                f"responsiveness_mapper: {where}[{i}].name must be a "
                f"non-empty string; got {name!r}."
            )
        out.append(name)
    return tuple(out)


def _walk_node_for_factors(
    node: Mapping[str, Any], *, criterion_id: str, where: str
) -> dict[str, tuple[str, ...]]:
    """Pull recognized factor keys out of a single criterion or
    subcriterion mapping.

    Returns a fresh ``dict`` keyed by factor_name. Unknown keys are
    silently skipped. Empty / missing factor keys are also skipped
    (no entry emitted) — only present-and-non-empty factor values
    produce entries.
    """
    extracted: dict[str, tuple[str, ...]] = {}
    for key in KNOWN_RESPONSIVENESS_FACTOR_KEYS:
        if key not in node:
            continue
        raw = node[key]
        if raw is None:
            continue
        if key in _LIST_OF_STR_FACTOR_KEYS:
            values = _coerce_str_list(raw, where=f"{where}.{key}")
        elif key in _LIST_OF_OBJECT_NAME_FACTOR_KEYS:
            values = _coerce_object_name_list(raw, where=f"{where}.{key}")
        else:  # pragma: no cover — KNOWN set is exhaustively partitioned
            continue
        if not values:
            # Empty list — skip (would fail ResponsivenessEntry invariant).
            continue
        if key in extracted:
            # Same key appearing twice in one node would be a malformed
            # JSON object; Python dict load would have collapsed it,
            # but defending against a custom Mapping is cheap.
            raise ValueError(
                f"responsiveness_mapper: criterion {criterion_id!r} "
                f"node has duplicate factor key {key!r}."
            )
        extracted[key] = values
    return extracted


# ---------------------------------------------------------------------------
# Public extraction — RUBRIC JSON → criterion-extras mapping
# ---------------------------------------------------------------------------


def extract_responsiveness_factors_from_rubric_json(
    rubric_json: Mapping[str, Any],
) -> dict[str, dict[str, tuple[str, ...]]]:
    """Walk a raw rubric JSON dict and pull recognized responsiveness
    factor keys into a ``{criterion_id: {factor_name: factor_values}}``
    nested mapping.

    Walks every criterion under ``scoring_criteria`` and, when present,
    every subcriterion under ``criterion.subcriteria``. Both
    criterion-level and subcriterion-level factors are emitted under
    the criterion-or-subcriterion id (so VAPG ``f.i.qualifying_categories``
    surfaces under id ``"f.i"``, not ``"f"``).

    Raises:
        ValueError: ``rubric_json`` is not a mapping or
            ``scoring_criteria`` is not a list, or any extracted factor
            list is malformed.

    The function tolerates missing meta — it only iterates
    ``scoring_criteria``. A rubric_json with no responsiveness factors
    returns ``{}``.
    """
    if not isinstance(rubric_json, Mapping):
        raise ValueError(
            f"extract_responsiveness_factors_from_rubric_json: rubric_json "
            f"must be a JSON object; got {type(rubric_json).__name__}."
        )
    scoring = rubric_json.get("scoring_criteria")
    if scoring is None:
        return {}
    if not isinstance(scoring, list):
        raise ValueError(
            f"extract_responsiveness_factors_from_rubric_json: "
            f"scoring_criteria must be a JSON array; got "
            f"{type(scoring).__name__}."
        )
    out: dict[str, dict[str, tuple[str, ...]]] = {}
    for i, crit in enumerate(scoring):
        if not isinstance(crit, Mapping):
            raise ValueError(
                f"extract_responsiveness_factors_from_rubric_json: "
                f"scoring_criteria[{i}] must be a JSON object; got "
                f"{type(crit).__name__}."
            )
        crit_id = crit.get("id")
        if not isinstance(crit_id, str) or not crit_id.strip():
            raise ValueError(
                f"extract_responsiveness_factors_from_rubric_json: "
                f"scoring_criteria[{i}].id must be a non-empty string."
            )
        crit_factors = _walk_node_for_factors(
            crit, criterion_id=crit_id, where=f"scoring_criteria[{i}]"
        )
        if crit_factors:
            out[crit_id] = crit_factors
        sub_raw = crit.get("subcriteria")
        if sub_raw is None:
            continue
        if not isinstance(sub_raw, list):
            raise ValueError(
                f"extract_responsiveness_factors_from_rubric_json: "
                f"scoring_criteria[{i}].subcriteria must be a JSON array."
            )
        for j, sub in enumerate(sub_raw):
            if not isinstance(sub, Mapping):
                raise ValueError(
                    f"extract_responsiveness_factors_from_rubric_json: "
                    f"scoring_criteria[{i}].subcriteria[{j}] must be a "
                    f"JSON object."
                )
            sub_id = sub.get("id")
            if not isinstance(sub_id, str) or not sub_id.strip():
                raise ValueError(
                    f"extract_responsiveness_factors_from_rubric_json: "
                    f"scoring_criteria[{i}].subcriteria[{j}].id must be a "
                    f"non-empty string."
                )
            sub_factors = _walk_node_for_factors(
                sub,
                criterion_id=sub_id,
                where=f"scoring_criteria[{i}].subcriteria[{j}]",
            )
            if sub_factors:
                out[sub_id] = sub_factors
    return out


# ---------------------------------------------------------------------------
# Public assembly — criterion-extras mapping → ResponsivenessMap
# ---------------------------------------------------------------------------


def build_responsiveness_map(
    rubric: Rubric,
    *,
    criterion_extras: Mapping[str, Mapping[str, Sequence[str]]],
) -> ResponsivenessMap:
    """Assemble a :class:`ResponsivenessMap` from a rubric + raw
    criterion-extras mapping.

    ``criterion_extras`` is keyed by either a criterion id or a
    subcriterion id (matching what
    :func:`extract_responsiveness_factors_from_rubric_json` returns).
    Entries whose key is not present in the rubric (neither as a
    top-level criterion id nor as any criterion's subcriterion id) →
    ``ValueError`` (the input is referencing a criterion the rubric
    doesn't carry).

    Within each criterion, factor names are emitted in sorted order to
    keep the output deterministic across input dict orderings; criterion
    ids are emitted in the rubric's criterion / subcriterion declaration
    order so the map mirrors the dispatcher's :func:`dispatch_score_units`
    iteration. Empty ``criterion_extras`` → empty map (legitimate; not
    every rubric carries responsiveness data).

    Raises:
        ValueError: ``criterion_extras`` references a criterion / sub
            id absent from the rubric; any factor list is empty;
            duplicate ``(criterion_id, factor_name)`` would be produced
            (the :class:`ResponsivenessMap` ``__post_init__`` raises).
    """
    # Build the rubric's id → declaration-order index.
    declared_order: list[str] = []
    valid_ids: set[str] = set()
    for crit in rubric.criteria:
        valid_ids.add(crit.id)
        if not crit.subcriteria:
            declared_order.append(crit.id)
            continue
        # Even subcriteria-bearing criteria can carry top-level
        # responsiveness factors (e.g., a future rubric variant);
        # include the parent first, then each subcriterion in order.
        declared_order.append(crit.id)
        for sub in crit.subcriteria:
            valid_ids.add(sub.id)
            declared_order.append(sub.id)

    for cid in criterion_extras:
        if cid not in valid_ids:
            raise ValueError(
                f"build_responsiveness_map: criterion_extras key {cid!r} "
                f"is not a criterion or subcriterion id in rubric "
                f"{rubric.program_code!r}."
            )

    entries: list[ResponsivenessEntry] = []
    for cid in declared_order:
        cfg = criterion_extras.get(cid)
        if not cfg:
            continue
        for fname in sorted(cfg.keys()):
            raw_values = cfg[fname]
            values_tuple = tuple(raw_values)
            entries.append(
                ResponsivenessEntry(
                    criterion_id=cid,
                    factor_name=fname,
                    factor_values=values_tuple,
                )
            )
    return ResponsivenessMap(entries=tuple(entries))


__all__ = [
    "KNOWN_RESPONSIVENESS_FACTOR_KEYS",
    "build_responsiveness_map",
    "extract_responsiveness_factors_from_rubric_json",
]
