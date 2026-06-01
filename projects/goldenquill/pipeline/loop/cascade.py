"""pipeline.loop.cascade — §4.9 v2 provider-cascade level selection (Round 8).

Blueprint §5 v6 LOCKED 2026-04-19:
- §4.9 v2 ``select_cascade_level`` (lines 625-647) — live landed-family
  consulted, first-eligible-with-capacity returned, F_PIPE_08 on tail
  exhaustion.
- §3.2.1 ``RunState.run_iteration_families_so_far`` (Round 1 typed as
  ``dict[str, tuple[str, str]]`` — per-seat (family, endpoint) recording).
- §4.8 ``rate_limiter.can_reserve`` (Round 7, read-only capacity probe).
- §6 F-PIPE-08 ``cross_family_violation``.
- §4.5 cross-family-rigor guard: editor excludes scribe's family; judge
  excludes scribe + editor families; scribe excludes nothing.

**Design decisions (confirmed at Round 8 ORIENT — 2026-04-21)**

1. *CascadeLevel shape owned by Round 8.* Round 1 ``ProviderCascade.levels``
   is typed as ``tuple[tuple[str, str], ...]`` — ``(family, model_id)`` pairs
   WITHOUT ``provider_endpoint`` or ``estimated_tokens_budget``. The blueprint
   §4.9 pseudo-code accesses ``level.family``, ``level.provider_endpoint``,
   and ``level.estimated_tokens_budget``. Round 8 defines a new
   :class:`CascadeLevel` frozen-slotted dataclass here rather than mutating
   the LOCKed Round 1 shape. A future cleanup round (§5 Round 11+ capstone
   wiring) reconciles the Round 1 shape with this richer form — Round 8
   accepts enriched levels + start-index as separate kwargs so the caller
   (capstone wiring) performs the reshape.

2. *Signature takes ``levels`` + ``current_level_index`` directly.* The
   spec card proposed ``cascade: ProviderCascade`` but the Round 1 shape
   does not carry the required per-level endpoint + budget. Taking the
   richer tuple explicitly keeps Round 1 LOCKed and makes the shape
   requirement explicit at the call-site.

3. *Read-only by construction.* No ``vault_write``, no mutation of
   ``run_state``, no ``sleep``, no ``randint``. The function's only side
   effect is the injected ``vault_read`` calls forwarded to
   :func:`pipeline.loop.rate_limiter.can_reserve`.

4. *Family-exclusion seat-kind strings are inline literals (V1
   discipline).* ``"editor"``, ``"judge"``, ``"scribe"`` appear as inline
   string literals at every comparison site. Rebinding
   :data:`pipeline.loop.types.SeatKind` (a TypeAlias) cannot alter dispatch.

5. *F_PIPE_08 trigger taxonomy.* On tail exhaustion the raised
   :class:`F_PIPE_08` carries
   ``trigger = f"cross_family_exhausted:{seat_kind}:{run_id}"`` and a
   ``details`` dict with ``excluded_families``, ``skipped_for_capacity``,
   ``probe_count``, ``cascade_length``. Format mirrors
   :func:`pipeline.loop.rate_limiter.reserve`'s
   ``cas_retry_exhausted:{endpoint}:{max_attempts}`` idiom (§5 R7 precedent).

6. *``run_iteration_families_so_far`` is consulted by ``in``-check.*
   Per blueprint §4.9 line 633 the presence check is ``if "scribe" in
   landed_so_far``. Missing seat keys yield no exclusion (no
   ``KeyError``). The tuple value's ``[0]`` element is the family name
   (Round 1 docstring pins this as ``(family, endpoint)``).

7. *Early-exit on first match.* The probe loop breaks on the first level
   that both survives family-exclusion AND has rate-limiter capacity.
   ``probe_count`` reflects only the levels actually inspected — the loop
   does not over-probe after a hit.

**Threat model (§3.11 v5 trusted-operator envelope; E-023 closure)**

Round 8 is a pure selector — no network, no subprocess, no §4 Logician
consumption, no vault_write. The following residuals are OUT-OF-SCOPE for
v0.1 and documented by explicit ``test_adv_*`` tests rather than defended
at this layer:

- **``vault_read`` raising ``KeyError``** when a probed endpoint's
  rate-limiter state file is missing (first-run boot). Round 8 lets it
  propagate unwrapped — operators must ensure per-endpoint state files
  exist as part of ``start_run`` boot.

- **Malformed rate-limiter state at a probed endpoint.** ``json.JSONDecodeError``
  / ``ValueError`` from ``rate_limiter._deserialize_rate_limiter_state``
  propagates unwrapped (Round 7 residual).

- **Endpoint absent from ``state.buckets``.** ``KeyError`` from
  ``rate_limiter.can_reserve``'s bucket lookup propagates unwrapped.

- **Stale probe between cascade-selection and subsequent ``reserve``.**
  The capacity observed by ``can_reserve`` is a point-in-time projection;
  a concurrent ``reserve`` can drain the bucket before the caller commits.
  This is a benign race — the subsequent ``reserve`` returns
  ``InsufficientTokens`` and the caller re-enters cascade selection. Not
  defended at this layer.

- **Review-seat exhaustion.** Blueprint §4.9 line 649 defers review-seat
  exhaustion to ``graceful_degradation.request_bypass_authorization``
  (§4.12). Round 8 does NOT special-case review — review-seat invocation
  does not flow through :func:`select_cascade_level`.

Spec card: ``pipeline/engineering/spec_cards/section_05_round_8_cascade.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from pipeline.loop.errors import F_PIPE_08
from pipeline.loop.rate_limiter import can_reserve
from pipeline.loop.run_lifecycle import VaultReadCallable
from pipeline.loop.state_checkpoint import ClockProtocol
from pipeline.loop.types import RunState

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_05_pipeline.md": {
        "version": "v6",
        "hash_sha3_512_prefix16": "feb5928491e4dc40",
        "sections_implemented": [
            "§4.9 v2 select_cascade_level (live landed-family + can_reserve)",
            "§3.2.1 RunState.run_iteration_families_so_far consumption",
            "§4.5 cross-family rigor guard (editor/judge exclusion)",
            "§6 F-PIPE-08 cross_family_exhausted",
        ],
    },
}

# ---------------------------------------------------------------------------
# Inline-literal module-load integrity asserts (V1 discipline)
# ---------------------------------------------------------------------------

# F_PIPE_08's CODE is pinned at :data:`pipeline.loop.errors.F_PIPE_08.CODE`
# as a ``Final[str]``. A rebind at import-time is caught here.
assert F_PIPE_08.CODE == "F-PIPE-08", (
    "pipeline.loop.errors.F_PIPE_08.CODE has been rebound before "
    "pipeline.loop.cascade import; refusing to load"
)


# ---------------------------------------------------------------------------
# Public dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class CascadeLevel:
    """§4.9 cascade level — enriched per-level record consumed by the selector.

    Owned by Round 8 (Round 1's :class:`pipeline.loop.types.ProviderCascade`
    carries ``(family, model_id)`` tuples without ``provider_endpoint`` or
    ``estimated_tokens_budget``; the capstone (Rounds 10+) reshapes Round 1
    cascades into tuples of this type at the call-site).

    Attributes
    ----------
    family
        Provider-family name (router.yaml taxonomy — e.g. ``"anthropic"``,
        ``"google"``, ``"meta"``, ``"openai"``, ``"alibaba"``, ``"moonshot"``,
        ``"openai-oss"``). Used for §4.5 cross-family-rigor exclusion.
    provider_endpoint
        Per-endpoint key used to look up rate-limiter state at
        ``pipeline/rate_limiter/{provider_endpoint}.json`` (§4.8 line 573).
    estimated_tokens_budget
        Token budget for the upcoming seat invocation at this level.
        Passed to :func:`pipeline.loop.rate_limiter.can_reserve` as the
        capacity threshold. Must be non-negative.
    model_id
        The concrete model identifier (e.g. ``"claude-sonnet-4-6"``,
        ``"gemini-2.5-pro"``). Informational; not consulted by
        :func:`select_cascade_level`. Callers thread it through to the
        seat-invocation layer.
    """

    family: str
    provider_endpoint: str
    estimated_tokens_budget: int
    model_id: str

    def __post_init__(self) -> None:
        if not self.family:
            raise ValueError("CascadeLevel.family must be non-empty")
        if not self.provider_endpoint:
            raise ValueError(
                "CascadeLevel.provider_endpoint must be non-empty"
            )
        if not self.model_id:
            raise ValueError("CascadeLevel.model_id must be non-empty")
        if self.estimated_tokens_budget < 0:
            raise ValueError(
                f"CascadeLevel.estimated_tokens_budget must be >= 0; "
                f"got {self.estimated_tokens_budget}"
            )


@dataclass(frozen=True, kw_only=True, slots=True)
class CascadeSelection:
    """Result of a successful :func:`select_cascade_level` call.

    Attributes
    ----------
    selected_level
        The first :class:`CascadeLevel` in the cascade tail that (a)
        survived family-exclusion and (b) had rate-limiter capacity.
    excluded_families
        The frozenset of provider families excluded by §4.5 rigor rules
        for this ``seat_kind`` at this moment of inspection. Empty for
        ``seat_kind == "scribe"``; up to one element for
        ``seat_kind == "editor"`` (scribe's family if scribe landed); up
        to two elements for ``seat_kind == "judge"`` (scribe's and
        editor's families if they landed).
    skipped_for_capacity
        Tuple of ``provider_endpoint`` strings, in probe order, whose
        :func:`pipeline.loop.rate_limiter.can_reserve` probe returned
        ``False``. Informational for callers that want to surface
        capacity pressure; never includes levels skipped for
        family-exclusion.
    probe_count
        Number of levels actually inspected end-to-end. Upper bound:
        ``len(levels) - current_level_index``. Matches the expected value
        for early-exit on first hit (no over-probe).
    """

    selected_level: CascadeLevel
    excluded_families: frozenset[str]
    skipped_for_capacity: tuple[str, ...]
    probe_count: int


# ---------------------------------------------------------------------------
# Internal helper — family-exclusion derivation
# ---------------------------------------------------------------------------


def _derive_excluded_families(
    *,
    seat_kind: str,
    landed_so_far: dict[str, tuple[str, str]],
) -> frozenset[str]:
    """§4.5 cross-family rigor — derive the family-exclusion set.

    Blueprint §4.9 lines 632-638:

    - ``seat_kind == "scribe"`` → no exclusion (empty set).
    - ``seat_kind == "editor"`` → exclude scribe's family if scribe landed.
    - ``seat_kind == "judge"`` → exclude scribe's + editor's families if
      they landed.

    Missing seat keys are treated as "not yet landed" — no exclusion.
    Seat-kind strings are inline literals at every comparison site
    (V1 discipline: rebinding :data:`pipeline.loop.types.SeatKind` cannot
    alter dispatch).
    """
    excluded: set[str] = set()
    # Inline-literal RHS — editor excludes scribe.
    if seat_kind == "editor":
        if "scribe" in landed_so_far:
            excluded.add(landed_so_far["scribe"][0])
    # Inline-literal RHS — judge excludes scribe + editor.
    elif seat_kind == "judge":
        if "scribe" in landed_so_far:
            excluded.add(landed_so_far["scribe"][0])
        if "editor" in landed_so_far:
            excluded.add(landed_so_far["editor"][0])
    # scribe (or any unrecognised seat_kind) → no exclusion.
    return frozenset(excluded)


# ---------------------------------------------------------------------------
# Public API — select_cascade_level
# ---------------------------------------------------------------------------


def select_cascade_level(
    *,
    seat_kind: str,
    levels: tuple[CascadeLevel, ...],
    current_level_index: int,
    run_state: RunState,
    vault_read: VaultReadCallable,
    clock: ClockProtocol,
) -> CascadeSelection:
    """§4.9 v2 deterministic cascade selector.

    Iterates ``levels[current_level_index:]`` and returns the first level
    whose family is not excluded by §4.5 rigor AND whose endpoint has
    rate-limiter capacity (via :func:`pipeline.loop.rate_limiter.can_reserve`).
    Pure selection: no mutation of ``run_state``, no ``vault_write``, no
    sleeps, no retries.

    Parameters
    ----------
    seat_kind
        One of ``"scribe"``, ``"editor"``, ``"judge"``. Inline-literal
        comparison at every dispatch site. An unrecognised seat_kind is
        treated as "no family exclusion" (matches blueprint §4.9 lines
        632-638 default branch) — the function does not enforce the
        :data:`pipeline.loop.types.SeatKind` literal here because Round 1
        already validates it at RunState construction.
    levels
        The full per-seat cascade as a tuple of :class:`CascadeLevel`.
        Must be non-empty; ``current_level_index`` must be in
        ``[0, len(levels))``.
    current_level_index
        Zero-based start index into ``levels``. The selector inspects
        ``levels[current_level_index:]`` in order. A value equal to
        ``len(levels)`` means "cascade pre-exhausted"; Round 8 raises
        :class:`F_PIPE_08` immediately.
    run_state
        Live :class:`RunState`. Only ``run_iteration_families_so_far``
        and ``run_id`` are read; no mutation.
    vault_read, clock
        Injected Protocols (forwarded to
        :func:`pipeline.loop.rate_limiter.can_reserve`).

    Returns
    -------
    CascadeSelection
        Describes the first-eligible-with-capacity level plus the
        excluded-family set, the endpoints skipped for capacity, and
        the probe count.

    Raises
    ------
    F_PIPE_08
        No level in the cascade tail both survived family-exclusion AND
        had rate-limiter capacity. Trigger string:
        ``cross_family_exhausted:{seat_kind}:{run_id}``. Details dict:
        ``excluded_families`` (list), ``skipped_for_capacity`` (list),
        ``probe_count`` (int), ``cascade_length`` (int),
        ``current_level_index`` (int).
    ValueError
        ``levels`` is empty or ``current_level_index`` is out of
        ``[0, len(levels)]``. Programmer/data contract violation.
    KeyError
        Propagated unwrapped from
        :func:`pipeline.loop.rate_limiter.can_reserve` when a probed
        endpoint's rate-limiter state file is missing, or when the
        endpoint is absent from ``state.buckets``.
    """
    if not levels:
        raise ValueError(
            "select_cascade_level: levels must be non-empty"
        )
    if not (0 <= current_level_index <= len(levels)):
        raise ValueError(
            f"select_cascade_level: current_level_index out of range "
            f"[0, {len(levels)}]; got {current_level_index}"
        )

    excluded_families = _derive_excluded_families(
        seat_kind=seat_kind,
        landed_so_far=run_state.run_iteration_families_so_far,
    )

    skipped_for_capacity: list[str] = []
    probe_count = 0

    # Iterate the cascade tail. ``current_level_index == len(levels)`` is
    # a valid zero-length tail — we fall through to the F_PIPE_08 raise.
    for level in levels[current_level_index:]:
        probe_count += 1
        if level.family in excluded_families:
            continue
        # can_reserve is the read-only Round 7 probe. KeyError / ValueError
        # / JSONDecodeError from malformed state propagate unwrapped.
        has_capacity = can_reserve(
            endpoint=level.provider_endpoint,
            estimated_tokens=level.estimated_tokens_budget,
            vault_read=vault_read,
            clock=clock,
        )
        if has_capacity:
            return CascadeSelection(
                selected_level=level,
                excluded_families=excluded_families,
                skipped_for_capacity=tuple(skipped_for_capacity),
                probe_count=probe_count,
            )
        skipped_for_capacity.append(level.provider_endpoint)

    raise F_PIPE_08(
        trigger=f"cross_family_exhausted:{seat_kind}:{run_state.run_id}",
        details={
            "seat_kind": seat_kind,
            "run_id": run_state.run_id,
            "excluded_families": sorted(excluded_families),
            "skipped_for_capacity": list(skipped_for_capacity),
            "probe_count": probe_count,
            "cascade_length": len(levels),
            "current_level_index": current_level_index,
        },
    )


__all__ = [
    "BLUEPRINT_DEPS",
    "CascadeLevel",
    "CascadeSelection",
    "select_cascade_level",
]
