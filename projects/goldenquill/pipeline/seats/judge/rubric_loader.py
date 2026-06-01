"""pipeline.seats.judge.rubric_loader — §9 R1 deterministic rubric loader.

Reads a rubric JSON file, validates its schema against the VAPG FY26
shape (the canonical R1 fixture), computes a canonical-bytes SHA-256
hash, and returns a frozen :class:`pipeline.seats.judge.types.Rubric`.

Pure-deterministic at R1: stdlib-only (``json``, ``hashlib``, ``pathlib``,
``datetime``); zero LLM calls; zero subprocess; zero network. The
``clock`` callable is the only injected seam — production binds
``datetime.datetime.now(tz=UTC)``; tests inject a fixed clock for
deterministic ``loaded_at_utc`` snapshots.

Threat model (R1):

- **In scope.** JSON parse error → ``ValueError`` tagged
  ``F-JUDGE-RUBRIC-MALFORMED``; missing required keys (``meta``,
  ``meta.program``, ``meta.funder``, ``meta.nofo_number``,
  ``meta.min_score``, ``meta.max_score``, ``scoring_criteria``,
  per-criterion ``id``/``name``/``max_points``/``scorer``) →
  ``ValueError`` tagged ``F-JUDGE-RUBRIC-MALFORMED``; duplicate criterion
  id → ``ValueError`` tagged ``F-JUDGE-RUBRIC-MALFORMED``; UTF-8 BOM at
  start of file → ``ValueError`` (canonical-bytes discipline rejects
  BOM); ``min_score > max_score`` → ``ValueError``;
  ``max_score < sum(criterion.max_points)`` → ``ValueError``.
- **Out of scope, deferred to R3.** Translation of these residual
  ``ValueError`` raises into Logician PRE-gate codes; runtime rubric-hash
  drift detection (``F-JUDGE-RUBRIC-HASH-DRIFT`` re-hashes on every Judge
  invocation and compares to the persisted ``rubric_sha256``).

Canonicalization discipline: the rubric_sha256 is computed over
``json.dumps(payload, sort_keys=True, separators=(",", ":"),
ensure_ascii=False).encode("utf-8")`` — pinned as inline literals here
(V1 rebind-resistance per §7 design decision 9). The hash is
dict-order-independent so re-saving the JSON in a different order does
not change the hash.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping

from pipeline.seats.judge.types import (
    F_JUDGE_RUBRIC_MALFORMED,
    Rubric,
    RubricCriterion,
    RubricScorerRole,
    RubricSubCriterion,
)


ClockFn = Callable[[], datetime]


def _default_utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


# ---------------------------------------------------------------------------
# Public hash primitive
# ---------------------------------------------------------------------------


def compute_rubric_sha256(rubric_bytes: bytes) -> str:
    """Canonical-bytes SHA-256 of an already-canonicalized rubric payload.

    Returns 64-hex lowercase. Caller is responsible for serializing the
    rubric dict via ``json.dumps(..., sort_keys=True,
    separators=(",", ":"), ensure_ascii=False).encode("utf-8")`` before
    invoking — this function does not re-canonicalize.

    Used at:
    - load time (over the serialized parsed dict — see :func:`load_rubric`)
    - audit time (re-hash on-disk rubric JSON, compare against the
      ``rubric_sha256`` pinned in the persisted JudgeOutput)
    - R3 PRE-gate firing (re-hash before every Judge invocation, compare
      against the ``rubric_sha256`` carried in the in-memory Rubric).
    """
    return hashlib.sha256(rubric_bytes).hexdigest()


# ---------------------------------------------------------------------------
# Internal canonicalization (V1 inline literals)
# ---------------------------------------------------------------------------


def _canonicalize(payload: Mapping[str, Any]) -> bytes:
    """Serialize a parsed rubric dict to canonical bytes for hashing.

    Pinned as inline literals to satisfy V1 rebind-resistance discipline:

    - ``sort_keys=True`` — dict-order-independent.
    - ``separators=(",", ":")`` — no incidental whitespace.
    - ``ensure_ascii=False`` — preserves UTF-8 source bytes; paired with
      ``encode("utf-8")`` to produce a deterministic byte stream.
    """
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


# ---------------------------------------------------------------------------
# Internal schema validators
# ---------------------------------------------------------------------------


def _require_mapping(value: Any, *, where: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(
            f"{F_JUDGE_RUBRIC_MALFORMED}: {where} must be a JSON object; "
            f"got {type(value).__name__}."
        )
    return value


def _require_str(value: Any, *, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            f"{F_JUDGE_RUBRIC_MALFORMED}: {where} must be a non-empty "
            f"string; got {value!r}."
        )
    return value


def _require_int(value: Any, *, where: str) -> int:
    # Reject bool explicitly: in Python `True` is an int subclass.
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(
            f"{F_JUDGE_RUBRIC_MALFORMED}: {where} must be an int; got "
            f"{type(value).__name__} ({value!r})."
        )
    return value


def _coerce_tier_tuple(value: Any, *, where: str) -> tuple[Mapping[str, Any], ...]:
    """A tier list is a JSON array of objects (each with ``points`` +
    ``description``). Empty / missing → empty tuple.
    """
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValueError(
            f"{F_JUDGE_RUBRIC_MALFORMED}: {where} must be a JSON array; "
            f"got {type(value).__name__}."
        )
    out: list[Mapping[str, Any]] = []
    for i, tier in enumerate(value):
        if not isinstance(tier, Mapping):
            raise ValueError(
                f"{F_JUDGE_RUBRIC_MALFORMED}: {where}[{i}] must be a JSON "
                f"object; got {type(tier).__name__}."
            )
        # Frozen dict copy — defensive against caller-mutation post-load.
        out.append({str(k): tier[k] for k in tier})
    return tuple(out)


def _coerce_str_tuple(value: Any, *, where: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValueError(
            f"{F_JUDGE_RUBRIC_MALFORMED}: {where} must be a JSON array; "
            f"got {type(value).__name__}."
        )
    out: list[str] = []
    for i, item in enumerate(value):
        if not isinstance(item, str):
            raise ValueError(
                f"{F_JUDGE_RUBRIC_MALFORMED}: {where}[{i}] must be a "
                f"string; got {type(item).__name__}."
            )
        out.append(item)
    return tuple(out)


def _build_subcriterion(
    raw: Mapping[str, Any], *, parent_id: str
) -> RubricSubCriterion:
    sub_id = _require_str(raw.get("id"), where=f"subcriterion under {parent_id!r}: id")
    sub_name = _require_str(
        raw.get("name"), where=f"subcriterion {sub_id!r}: name"
    )
    sub_max = _require_int(
        raw.get("max_points"),
        where=f"subcriterion {sub_id!r}: max_points",
    )
    if sub_max < 0:
        raise ValueError(
            f"{F_JUDGE_RUBRIC_MALFORMED}: subcriterion {sub_id!r}.max_points "
            f"must be >= 0; got {sub_max!r}."
        )
    must_address = _coerce_str_tuple(
        raw.get("must_address"),
        where=f"subcriterion {sub_id!r}: must_address",
    )
    tiers = _coerce_tier_tuple(
        raw.get("tiers"), where=f"subcriterion {sub_id!r}: tiers"
    )
    return RubricSubCriterion(
        id=sub_id,
        name=sub_name,
        max_points=sub_max,
        must_address=must_address,
        tiers=tiers,
    )


def _build_criterion(raw: Mapping[str, Any]) -> RubricCriterion:
    crit_id = _require_str(raw.get("id"), where="scoring_criteria[*].id")
    crit_name = _require_str(
        raw.get("name"), where=f"criterion {crit_id!r}: name"
    )
    crit_max = _require_int(
        raw.get("max_points"),
        where=f"criterion {crit_id!r}: max_points",
    )
    if crit_max < 0:
        raise ValueError(
            f"{F_JUDGE_RUBRIC_MALFORMED}: criterion {crit_id!r}.max_points "
            f"must be >= 0; got {crit_max!r}."
        )
    scorer_raw = raw.get("scorer")
    if scorer_raw not in ("review_panel", "state_office", "administrator"):
        raise ValueError(
            f"{F_JUDGE_RUBRIC_MALFORMED}: criterion {crit_id!r}.scorer must "
            f"be one of review_panel/state_office/administrator; got "
            f"{scorer_raw!r}."
        )
    scorer: RubricScorerRole = scorer_raw  # type: ignore[assignment]

    sub_raw = raw.get("subcriteria")
    if sub_raw is None:
        subcriteria: tuple[RubricSubCriterion, ...] = ()
    elif isinstance(sub_raw, list):
        sub_list: list[RubricSubCriterion] = []
        for entry in sub_raw:
            if not isinstance(entry, Mapping):
                raise ValueError(
                    f"{F_JUDGE_RUBRIC_MALFORMED}: criterion {crit_id!r} "
                    f"subcriteria entry must be a JSON object."
                )
            sub_list.append(_build_subcriterion(entry, parent_id=crit_id))
        subcriteria = tuple(sub_list)
    else:
        raise ValueError(
            f"{F_JUDGE_RUBRIC_MALFORMED}: criterion {crit_id!r}.subcriteria "
            f"must be a JSON array; got {type(sub_raw).__name__}."
        )

    must_address = _coerce_str_tuple(
        raw.get("must_address"),
        where=f"criterion {crit_id!r}: must_address",
    )
    tiers = _coerce_tier_tuple(
        raw.get("tiers"), where=f"criterion {crit_id!r}: tiers"
    )
    return RubricCriterion(
        id=crit_id,
        name=crit_name,
        max_points=crit_max,
        scorer=scorer,
        subcriteria=subcriteria,
        must_address=must_address,
        tiers=tiers,
    )


# ---------------------------------------------------------------------------
# Public loader
# ---------------------------------------------------------------------------


def load_rubric(
    rubric_path: Path,
    *,
    clock: ClockFn = _default_utc_now,
) -> Rubric:
    """Load a rubric JSON file and return a frozen :class:`Rubric`.

    Raises:
        FileNotFoundError: when ``rubric_path`` does not exist.
        ValueError: tagged ``F-JUDGE-RUBRIC-MALFORMED`` for any schema
            violation: malformed JSON, missing meta/scoring_criteria,
            missing per-criterion id/name/max_points/scorer, duplicate
            criterion id, UTF-8 BOM at start of file,
            ``min_score > max_score``,
            ``max_score < sum(criterion.max_points)``.

    Pure deterministic under a fixed ``clock``. The injected clock
    populates ``Rubric.loaded_at_utc`` so tests can pin the field for
    snapshot comparison; production wires
    ``datetime.datetime.now(tz=UTC)``.
    """
    raw_bytes = rubric_path.read_bytes()
    # Reject UTF-8 BOM — canonicalization assumes pure UTF-8 source bytes;
    # a leading BOM produces a different SHA-256 than the BOM-stripped
    # version, and silently stripping it would let a BOM/no-BOM pair drift
    # past a hash comparison.
    if raw_bytes.startswith(b"\xef\xbb\xbf"):
        raise ValueError(
            f"{F_JUDGE_RUBRIC_MALFORMED}: rubric file at {str(rubric_path)!r} "
            f"starts with a UTF-8 BOM; canonical-bytes discipline rejects "
            f"BOM-prefixed files."
        )
    try:
        raw_text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            f"{F_JUDGE_RUBRIC_MALFORMED}: rubric file at "
            f"{str(rubric_path)!r} is not valid UTF-8: {exc}"
        ) from exc

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"{F_JUDGE_RUBRIC_MALFORMED}: rubric file at "
            f"{str(rubric_path)!r} is not valid JSON: {exc}"
        ) from exc

    if not isinstance(parsed, Mapping):
        raise ValueError(
            f"{F_JUDGE_RUBRIC_MALFORMED}: rubric top-level must be a JSON "
            f"object; got {type(parsed).__name__}."
        )

    meta = _require_mapping(parsed.get("meta"), where="meta")
    program_code = _require_str(meta.get("program"), where="meta.program")
    funder = _require_str(meta.get("funder"), where="meta.funder")
    nofo_number = _require_str(
        meta.get("nofo_number"), where="meta.nofo_number"
    )
    min_score = _require_int(meta.get("min_score"), where="meta.min_score")
    max_score = _require_int(meta.get("max_score"), where="meta.max_score")

    if min_score < 0 or max_score < 0:
        raise ValueError(
            f"{F_JUDGE_RUBRIC_MALFORMED}: meta.min_score / meta.max_score "
            f"must be >= 0; got min={min_score!r}, max={max_score!r}."
        )
    if min_score > max_score:
        raise ValueError(
            f"{F_JUDGE_RUBRIC_MALFORMED}: meta.min_score ({min_score}) > "
            f"meta.max_score ({max_score})."
        )

    scoring_raw = parsed.get("scoring_criteria")
    if not isinstance(scoring_raw, list) or not scoring_raw:
        raise ValueError(
            f"{F_JUDGE_RUBRIC_MALFORMED}: scoring_criteria must be a "
            f"non-empty JSON array; got {type(scoring_raw).__name__}."
        )

    criteria_list: list[RubricCriterion] = []
    seen_ids: set[str] = set()
    for entry in scoring_raw:
        if not isinstance(entry, Mapping):
            raise ValueError(
                f"{F_JUDGE_RUBRIC_MALFORMED}: scoring_criteria entry must "
                f"be a JSON object; got {type(entry).__name__}."
            )
        crit = _build_criterion(entry)
        if crit.id in seen_ids:
            raise ValueError(
                f"{F_JUDGE_RUBRIC_MALFORMED}: duplicate criterion id "
                f"{crit.id!r}."
            )
        seen_ids.add(crit.id)
        criteria_list.append(crit)
    criteria = tuple(criteria_list)

    sum_max = sum(c.max_points for c in criteria)
    if max_score < sum_max:
        raise ValueError(
            f"{F_JUDGE_RUBRIC_MALFORMED}: meta.max_score ({max_score}) < "
            f"sum of criterion max_points ({sum_max})."
        )

    canonical = _canonicalize(parsed)
    rubric_sha256 = compute_rubric_sha256(canonical)

    return Rubric(
        program_code=program_code,
        funder=funder,
        nofo_number=nofo_number,
        max_score=max_score,
        min_score=min_score,
        criteria=criteria,
        rubric_sha256=rubric_sha256,
        loaded_at_utc=clock(),
    )


__all__ = [
    "ClockFn",
    "compute_rubric_sha256",
    "load_rubric",
]
