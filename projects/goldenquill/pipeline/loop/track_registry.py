"""pipeline.loop.track_registry — §5 v8 track-registry adoption (R.PF1).

Blueprint §5 v8 amendment (DRAFT — pipeline/blueprint/v0.1/section_05_v8_amendment.md).
Architecture v7 LOCKED 2026-04-19 §R.PF1 (pull-forward; binding on §5 next-spin).
Operating envelope §6.7 (host of the registry schema; v1-r1 LOCKED 2026-04-21).

**What this module is.**

The track-registry is the data-driven binding §5 consumes to dispatch a
council round under one of N tracks (v0.1: ``submission`` + ``eval``;
forward-compat: ``report`` + ``content`` + ``tdsl_query``). Each registry
row binds a track name to:

  (a) Scribe prompt template
  (b) Judge rubric
  (c) Red Team probe template
  (d) Vault subtree for output
  (e) Output schema name

plus the §6.7 host schema fields (``pipeline_shape``, ``prompt_template_root``,
``failure_code_prefix``, ``cross_family_rigor``, ``shippable_in``).

The architectural commitment (R.PF1, F-PIPELINE-TRACK-FROZEN PRE-gate
dormant at v7 LOCK; activates against §5 LOCKED text at lock-time):
**adding a new track requires a new router.yaml registry row + new prompt
templates only — NOT a §5 re-architecture, NOT a new §3 module per track,
NOT a new §4.N mechanism per track.**

**What this module is NOT.**

This module does not parse the full router.yaml document. It parses the
``tracks:`` section out of an arbitrary YAML mapping. The submission and
eval pipeline-shape implementations live in
:mod:`pipeline.loop.run_pipeline` and :mod:`pipeline.loop.run_eval_pipeline`
respectively; this module is the registry + dispatcher that binds names
to those existing entry points.

**Public surface.**

- :class:`Track` — frozen dataclass, one per registry row
- :class:`TrackRegistry` — frozen dataclass wrapping a name → Track mapping
- :class:`TrackRegistryError` (and subclasses) — registry-side failures
- :func:`load_track_registry` — parse a YAML mapping into a TrackRegistry
- :func:`get_track` — name → Track lookup with shippable_in enforcement
- :func:`dispatch_track` — track-agnostic dispatcher that routes to the
  correct pipeline-shape implementation

**Forward-compat.**

The registry schema accommodates v0.2 tracks (``report``, ``content``,
``tdsl_query``) without code changes — only new rows + new
prompt templates. Tracks marked ``shippable_in: v0.2`` LOAD into the
registry but FAIL at :func:`dispatch_track` time with
:class:`TrackNotShippable`. This is the forward-compatibility safety
mandated by §6.7: an operator cannot accidentally start an unshipped
track even if the row is present.

Pipeline shapes that have no v0.1 implementation (e.g., the
report-vertical's ``rfa_to_council_to_signed_report`` shape, which is
NOT the same as the submission-vertical's
``rfa_to_council_to_signed_bundle`` shape) raise
:class:`TrackShapeUnimplemented` if they are dispatched at v0.1.

**Failure-code prefix.**

This module uses the ``F-PIPE-TRACK-*`` prefix for runtime failures.
The architecture-side ``F-PIPELINE-TRACK-FROZEN`` PRE-gate is a
LOCK-time lint over §5 LOCKED text (per §6.7), not a runtime exception.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Mapping

# Inline-literal version family for the shippable_in gate. v0.1 Tilth
# refuses to dispatch any track whose ``shippable_in`` is later than this
# (per §6.7: forward-compatibility safety — operator cannot accidentally
# opt into an unshipped track). At v0.2 LOCK this constant moves with the
# Tilth version; the registry schema is unchanged.
TILTH_VERSION_FAMILY: Final[str] = "v0.1"

# The closed set of v0.1 implementation-bound pipeline shapes. A registry
# row whose ``pipeline_shape`` is NOT in this set is loadable (forward-
# compat) but NOT dispatchable at v0.1 — :func:`dispatch_track` raises
# :class:`TrackShapeUnimplemented`. Adding a new v0.1 shape is itself a
# §5 spin (audited against R.PF1 at LOCK time); this set must NOT grow
# at v0.1 without that ceremony. Forward-compat shape names appear in
# the YAML rows for ``report`` / ``content`` / ``tdsl_query`` but stay
# out of this v0.1 implementation-bound set until their v0.2 spin lands.
_V0_1_IMPLEMENTED_SHAPES: Final[frozenset[str]] = frozenset(
    {
        "rfa_to_council_to_signed_bundle",
        "operator_harness_to_per_seat_calibration",
    }
)
assert len(_V0_1_IMPLEMENTED_SHAPES) == 2, (
    "_V0_1_IMPLEMENTED_SHAPES has been rebound at module load; "
    "refusing to load pipeline.loop.track_registry"
)

# The closed set of valid ``cross_family_rigor`` values (per §6.7).
_VALID_CROSS_FAMILY_RIGOR: Final[frozenset[str]] = frozenset(
    {"required", "not_required"}
)
assert len(_VALID_CROSS_FAMILY_RIGOR) == 2, (
    "_VALID_CROSS_FAMILY_RIGOR has been rebound at module load; "
    "refusing to load pipeline.loop.track_registry"
)

# Required keys per §6.7 + R.PF1 §5 follow-on. A registry row missing any
# of these fails :func:`load_track_registry` at parse time.
_REQUIRED_TRACK_KEYS: Final[frozenset[str]] = frozenset(
    {
        # §6.7 host schema (router.yaml-side):
        "kind",
        "pipeline_shape",
        "prompt_template_root",
        "failure_code_prefix",
        "cross_family_rigor",
        "shippable_in",
        # R.PF1 §5 follow-on bindings (architecture-side):
        "scribe_prompt_template",
        "judge_rubric_ref",
        "red_team_probe_template",
        "output_vault_subtree",
        "output_schema",
    }
)
assert len(_REQUIRED_TRACK_KEYS) == 11, (
    "_REQUIRED_TRACK_KEYS has been rebound at module load; "
    "refusing to load pipeline.loop.track_registry"
)


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class TrackRegistryError(Exception):
    """Base class for all track-registry runtime failures.

    Subclasses are emitted by :func:`load_track_registry` (schema
    failures) and :func:`dispatch_track` (lookup / shippable_in /
    shape-unimplemented).
    """


class RegistrySchemaError(TrackRegistryError):
    """A registry row is malformed or missing a required key."""


class TrackNotFound(TrackRegistryError):
    """``dispatch_track`` was asked for a name not present in the registry.

    Trigger code: ``F-PIPE-TRACK-NOT-FOUND``.
    """


class TrackNotShippable(TrackRegistryError):
    """The track's ``shippable_in`` is later than the current Tilth version.

    Trigger code: ``F-PIPE-TRACK-NOT-SHIPPABLE``. This is the forward-
    compatibility safety mandated by §6.7: a v0.2-shippable row can live
    in router.yaml at v0.1, but starting it raises this error.
    """


class TrackShapeUnimplemented(TrackRegistryError):
    """The track's ``pipeline_shape`` has no v0.1 dispatcher binding.

    Trigger code: ``F-PIPE-TRACK-SHAPE-UNIMPLEMENTED``. Distinct from
    :class:`TrackNotShippable`: a row may be marked ``shippable_in: v0.1``
    but reference a pipeline_shape outside :data:`_V0_1_IMPLEMENTED_SHAPES`
    (e.g., a maliciously-crafted router.yaml or a forward-port mistake).
    Fail-closed.
    """


# ---------------------------------------------------------------------------
# Public dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True, kw_only=True)
class Track:
    """One registry row.

    Field semantics per §6.7 + R.PF1:

    - ``name`` — the track key in the registry (e.g., ``"submission"``).
    - ``kind`` — always ``"track"`` per §6.7 schema.
    - ``pipeline_shape`` — descriptor of the pipeline shape this track
      runs (e.g., ``"rfa_to_council_to_signed_bundle"``). Used by
      :func:`dispatch_track` to select the implementation binding.
    - ``prompt_template_root`` — directory under which the per-seat
      prompt templates live (e.g., ``"pipeline/prompts/submission/"``).
    - ``failure_code_prefix`` — ``F-PIPE-<TRACK>-`` namespace this
      track's runtime failures use.
    - ``cross_family_rigor`` — ``"required"`` (Judge + Red Team must be
      cross-family-distinct from Scribe) or ``"not_required"``
      (single-seat calibration; eval-mode).
    - ``shippable_in`` — the earliest Tilth version that may dispatch
      this track. ``"v0.1"`` for tracks shipping today;
      ``"v0.2"`` for forward-compat rows.
    - ``scribe_prompt_template`` — vault-relative path to the Scribe
      prompt template specific to this track.
    - ``judge_rubric_ref`` — vault-relative path to the Judge rubric
      JSON specific to this track.
    - ``red_team_probe_template`` — vault-relative path to the Red Team
      probe template specific to this track.
    - ``output_vault_subtree`` — vault subtree (``{org_slug}`` /
      ``{run_id}`` placeholders permitted) where output artefacts land.
    - ``output_schema`` — name of the output-artefact dataclass /
      Pydantic schema (e.g., ``"SubmissionBundle"``,
      ``"CalibrationReport"``, ``"GrantReport"``).
    """

    name: str
    kind: str
    pipeline_shape: str
    prompt_template_root: str
    failure_code_prefix: str
    cross_family_rigor: str
    shippable_in: str
    scribe_prompt_template: str
    judge_rubric_ref: str
    red_team_probe_template: str
    output_vault_subtree: str
    output_schema: str


@dataclass(frozen=True, slots=True, kw_only=True)
class TrackRegistry:
    """Frozen mapping of track-name → :class:`Track`.

    Constructed by :func:`load_track_registry`. The :attr:`tracks` field
    is a tuple of (name, Track) pairs (deterministic order — the order
    in which rows appeared in the source YAML); :meth:`as_mapping` and
    :meth:`names` are the public lookup surfaces.
    """

    tracks: tuple[tuple[str, Track], ...]

    def as_mapping(self) -> Mapping[str, Track]:
        """Return a fresh dict view of the registry (defensive copy)."""

        return {name: track for name, track in self.tracks}

    def names(self) -> tuple[str, ...]:
        """Return the registered track names in declaration order."""

        return tuple(name for name, _ in self.tracks)


# ---------------------------------------------------------------------------
# Schema validation helpers
# ---------------------------------------------------------------------------


def _require_str(row: Mapping[str, Any], key: str, track_name: str) -> str:
    """Pull a required string field; raise :class:`RegistrySchemaError` on miss."""

    val = row.get(key)
    if val is None:
        raise RegistrySchemaError(
            f"track {track_name!r} is missing required key {key!r}"
        )
    if not isinstance(val, str):
        raise RegistrySchemaError(
            f"track {track_name!r} key {key!r} must be a string; got "
            f"{type(val).__name__}"
        )
    if not val:
        raise RegistrySchemaError(
            f"track {track_name!r} key {key!r} must be a non-empty string"
        )
    return val


def _validate_track_row(name: str, row: Any) -> Track:
    """Validate one registry row and return a :class:`Track`.

    Raises :class:`RegistrySchemaError` if the row is malformed.
    """

    if not isinstance(row, Mapping):
        raise RegistrySchemaError(
            f"track {name!r} must be a mapping; got {type(row).__name__}"
        )

    # Reject unknown keys (forward-compat extension requires a §5 spin
    # per R.PF1; silently swallowing unknown keys would defeat the
    # F-PIPELINE-TRACK-FROZEN audit pattern).
    extra = set(row.keys()) - _REQUIRED_TRACK_KEYS
    if extra:
        raise RegistrySchemaError(
            f"track {name!r} carries unknown keys {sorted(extra)!r}; "
            f"adding new fields requires a §5 spin per R.PF1"
        )

    missing = _REQUIRED_TRACK_KEYS - set(row.keys())
    if missing:
        raise RegistrySchemaError(
            f"track {name!r} is missing required keys {sorted(missing)!r}"
        )

    kind = _require_str(row, "kind", name)
    if kind != "track":
        raise RegistrySchemaError(
            f"track {name!r} kind must be 'track'; got {kind!r}"
        )

    cross_family_rigor = _require_str(row, "cross_family_rigor", name)
    if cross_family_rigor not in frozenset({"required", "not_required"}):
        raise RegistrySchemaError(
            f"track {name!r} cross_family_rigor must be 'required' or "
            f"'not_required'; got {cross_family_rigor!r}"
        )

    # §7.20 (Cycle-1 RT-03 closure): output_vault_subtree must contain
    # the "{org_slug}" placeholder so per-org Cedar isolation enforces at
    # the rendering site (Law 3 — Org Isolation). A row that omits the
    # placeholder would silently write to a workspace-shared path and
    # breach Law 3.
    output_vault_subtree = _require_str(row, "output_vault_subtree", name)
    if "{org_slug}" not in output_vault_subtree:
        raise RegistrySchemaError(
            f"track {name!r} output_vault_subtree must contain the "
            f"'{{org_slug}}' placeholder for Law-3 per-org isolation; "
            f"got {output_vault_subtree!r}"
        )

    return Track(
        name=name,
        kind=kind,
        pipeline_shape=_require_str(row, "pipeline_shape", name),
        prompt_template_root=_require_str(row, "prompt_template_root", name),
        failure_code_prefix=_require_str(row, "failure_code_prefix", name),
        cross_family_rigor=cross_family_rigor,
        shippable_in=_require_str(row, "shippable_in", name),
        scribe_prompt_template=_require_str(row, "scribe_prompt_template", name),
        judge_rubric_ref=_require_str(row, "judge_rubric_ref", name),
        red_team_probe_template=_require_str(
            row, "red_team_probe_template", name
        ),
        output_vault_subtree=output_vault_subtree,
        output_schema=_require_str(row, "output_schema", name),
    )


# ---------------------------------------------------------------------------
# Public API — load_track_registry
# ---------------------------------------------------------------------------


def load_track_registry(source: Mapping[str, Any]) -> TrackRegistry:
    """Parse a router.yaml-shaped mapping into a :class:`TrackRegistry`.

    ``source`` is a parsed YAML mapping containing a top-level
    ``tracks:`` key (per §6.7 schema). Either a router.yaml document
    (``yaml.safe_load(open("router.yaml"))``) or a synthetic
    test-fixture mapping is acceptable — this function only looks at
    the ``tracks`` subtree.

    Raises :class:`RegistrySchemaError` if the ``tracks`` key is absent,
    not a mapping, empty, or any row is malformed. Returns a frozen
    :class:`TrackRegistry` on success.

    The returned registry preserves declaration order (deterministic for
    audit + test-replay).
    """

    if not isinstance(source, Mapping):
        raise RegistrySchemaError(
            f"track-registry source must be a mapping; got "
            f"{type(source).__name__}"
        )

    tracks_section = source.get("tracks")
    if tracks_section is None:
        raise RegistrySchemaError(
            "track-registry source has no 'tracks:' key; per §6.7 the "
            "router.yaml must publish a tracks: mapping"
        )
    if not isinstance(tracks_section, Mapping):
        raise RegistrySchemaError(
            f"'tracks' must be a mapping; got {type(tracks_section).__name__}"
        )
    if not tracks_section:
        raise RegistrySchemaError(
            "'tracks' mapping is empty; v0.1 must register at least the "
            "'submission' and 'eval' rows"
        )

    rows: list[tuple[str, Track]] = []
    seen: set[str] = set()
    for raw_name, raw_row in tracks_section.items():
        if not isinstance(raw_name, str) or not raw_name:
            raise RegistrySchemaError(
                f"track key must be a non-empty string; got {raw_name!r}"
            )
        if raw_name in seen:
            raise RegistrySchemaError(
                f"duplicate track key {raw_name!r}"
            )
        seen.add(raw_name)
        rows.append((raw_name, _validate_track_row(raw_name, raw_row)))

    return TrackRegistry(tracks=tuple(rows))


# ---------------------------------------------------------------------------
# Public API — load_track_registry_from_yaml_text  (Cycle-1 RT-04 closure)
# ---------------------------------------------------------------------------


def load_track_registry_from_yaml_text(yaml_text: str) -> TrackRegistry:
    """Parse a router.yaml document text into a :class:`TrackRegistry`.

    This helper exists because PyYAML's default ``safe_load`` silently
    overwrites duplicate mapping keys at the parser level — so by the
    time :func:`load_track_registry` sees the parsed mapping, only the
    LAST occurrence of a duplicate ``submission:`` (or any other key)
    survives. The duplicate-detection in :func:`load_track_registry` is
    therefore dead code for the YAML-text input case.

    This loader installs a strict ``SafeLoader`` subclass that raises
    :class:`RegistrySchemaError` on any duplicate mapping key inside the
    YAML document — at the ``tracks:`` level OR at any nested mapping
    level (defence-in-depth: a duplicate row-internal key like
    ``shippable_in`` repeated would otherwise resolve to the last value).

    The on-disk loader call-site (e.g., loading workspace router.yaml at
    pipeline startup) MUST use this helper rather than calling
    ``yaml.safe_load`` directly.

    Closes RT-04 from §5 v8 Audit #1.
    """

    import yaml  # imported lazily — pure-mapping callers don't need pyyaml

    class _NoDuplicatesSafeLoader(yaml.SafeLoader):
        """A SafeLoader that raises on duplicate mapping keys."""

    def _construct_mapping_no_duplicates(
        loader: yaml.SafeLoader, node: yaml.MappingNode, deep: bool = False
    ) -> dict:
        mapping: dict = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in mapping:
                raise RegistrySchemaError(
                    f"duplicate YAML mapping key {key!r} at "
                    f"line {key_node.start_mark.line + 1} "
                    f"column {key_node.start_mark.column + 1}; "
                    f"track-registry YAML must not contain duplicate keys "
                    f"(F-PIPE-TRACK-REGISTRY-DUPLICATE-KEY)"
                )
            value = loader.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping

    _NoDuplicatesSafeLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        _construct_mapping_no_duplicates,
    )

    try:
        parsed = yaml.load(yaml_text, Loader=_NoDuplicatesSafeLoader)
    except RegistrySchemaError:
        raise
    except yaml.YAMLError as exc:
        raise RegistrySchemaError(
            f"router.yaml YAML parse error: {exc}"
        ) from exc

    if not isinstance(parsed, Mapping):
        raise RegistrySchemaError(
            f"router.yaml must parse to a mapping; got {type(parsed).__name__}"
        )

    return load_track_registry(parsed)


# ---------------------------------------------------------------------------
# Public API — get_track
# ---------------------------------------------------------------------------


def get_track(
    registry: TrackRegistry,
    name: str,
    *,
    current_version: str = TILTH_VERSION_FAMILY,
) -> Track:
    """Look up a track by name, enforcing :attr:`Track.shippable_in`.

    Returns the :class:`Track` if it exists AND its ``shippable_in`` is
    less-than-or-equal-to ``current_version``. Otherwise raises
    :class:`TrackNotFound` (no row) or :class:`TrackNotShippable`
    (row is forward-compat).

    ``current_version`` defaults to :data:`TILTH_VERSION_FAMILY`; tests
    may pass a synthetic value (e.g., ``"v0.2"``) to exercise the
    forward-compat path.

    Version comparison is lexicographic over ``"vM.N"`` strings — this
    is correct for ``v0.1 < v0.2 < ... < v0.9`` and for two-digit minors
    if we ever ship them. A future ``v1.0`` ordering swap is out of
    scope for v0.1.
    """

    mapping = registry.as_mapping()
    track = mapping.get(name)
    if track is None:
        raise TrackNotFound(
            f"track {name!r} not found in registry; known tracks: "
            f"{sorted(mapping)!r}"
        )
    if track.shippable_in > current_version:
        raise TrackNotShippable(
            f"track {name!r} is shippable_in={track.shippable_in!r}; "
            f"current Tilth version is {current_version!r} — refusing "
            f"to dispatch (F-PIPE-TRACK-NOT-SHIPPABLE)"
        )
    return track


# ---------------------------------------------------------------------------
# Public API — dispatch_track
# ---------------------------------------------------------------------------


def dispatch_track(
    registry: TrackRegistry,
    name: str,
    *,
    current_version: str = TILTH_VERSION_FAMILY,
    submission_runner: Any = None,
    eval_runner: Any = None,
    submission_kwargs: Mapping[str, Any] | None = None,
    eval_kwargs: Mapping[str, Any] | None = None,
) -> Any:
    """Track-agnostic dispatcher.

    Resolves ``name`` against ``registry``, enforces the shippable_in
    gate, and routes to the matching pipeline-shape implementation:

    - ``rfa_to_council_to_signed_bundle`` → ``submission_runner(**submission_kwargs)``
    - ``operator_harness_to_per_seat_calibration`` → ``eval_runner(**eval_kwargs)``
    - any other shape → :class:`TrackShapeUnimplemented`

    Both runners are injected as parameters (E-017 dependency-injection
    pattern) so tests can drive the dispatcher with stubs without
    importing the full submission / eval call stacks. Production callers
    pass :func:`pipeline.loop.run_pipeline.run_pipeline_5_seat` as
    ``submission_runner`` and
    :func:`pipeline.loop.run_eval_pipeline.run_eval_pipeline` as
    ``eval_runner``.

    Per R.PF1: adding a new pipeline_shape is a §5 spin (NOT a §3 module
    addition); until that spin lands, dispatching a forward-compat shape
    fails with :class:`TrackShapeUnimplemented`. This is the load-bearing
    invariant the F-PIPELINE-TRACK-FROZEN PRE-gate audits at LOCK time.

    Raises
    ------
    TrackNotFound
        ``name`` is not in ``registry``.
    TrackNotShippable
        Track is forward-compat (``shippable_in > current_version``).
    TrackShapeUnimplemented
        Track's ``pipeline_shape`` has no v0.1 implementation binding,
        OR the matching runner argument was not supplied.
    """

    track = get_track(registry, name, current_version=current_version)

    if track.pipeline_shape not in _V0_1_IMPLEMENTED_SHAPES:
        raise TrackShapeUnimplemented(
            f"track {name!r} declares pipeline_shape "
            f"{track.pipeline_shape!r} which has no v0.1 implementation "
            f"binding; v0.1 supports only "
            f"{sorted(_V0_1_IMPLEMENTED_SHAPES)!r} "
            f"(F-PIPE-TRACK-SHAPE-UNIMPLEMENTED)"
        )

    if track.pipeline_shape == "rfa_to_council_to_signed_bundle":
        if submission_runner is None:
            raise TrackShapeUnimplemented(
                f"track {name!r} maps to submission shape but no "
                f"submission_runner was supplied"
            )
        kwargs = dict(submission_kwargs or {})
        return submission_runner(**kwargs)

    if track.pipeline_shape == "operator_harness_to_per_seat_calibration":
        if eval_runner is None:
            raise TrackShapeUnimplemented(
                f"track {name!r} maps to eval shape but no eval_runner "
                f"was supplied"
            )
        kwargs = dict(eval_kwargs or {})
        return eval_runner(**kwargs)

    # Defensive — _V0_1_IMPLEMENTED_SHAPES gate above should have
    # excluded any other shape. Reaching here would mean the gate was
    # rebound at runtime; fail-closed.
    raise TrackShapeUnimplemented(  # pragma: no cover — gate above is exhaustive
        f"track {name!r} pipeline_shape {track.pipeline_shape!r} is in "
        f"the v0.1 implemented set but dispatch fell through; "
        f"_V0_1_IMPLEMENTED_SHAPES has been rebound at runtime"
    )


__all__ = [
    "TILTH_VERSION_FAMILY",
    "Track",
    "TrackNotFound",
    "TrackNotShippable",
    "TrackRegistry",
    "TrackRegistryError",
    "TrackShapeUnimplemented",
    "RegistrySchemaError",
    "dispatch_track",
    "get_track",
    "load_track_registry",
    "load_track_registry_from_yaml_text",
]
