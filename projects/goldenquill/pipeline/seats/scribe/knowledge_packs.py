"""pipeline.seats.scribe.knowledge_packs — sector-scoped terminology pack loader.

Pattern source
--------------
Adapted from MIT-licensed `linkedin_ssi_booster`
(github.com/samjd-zz/linkedin_ssi_booster, ``services/avatar_intelligence/
_loaders.py:218-337``). Their ``_load_domain_knowledge`` + auto-merge of
``domain_knowledge_*.json`` siblings is the cleanest prior art we found
for plug-in terminology packs. We preserve the schema shape (so packs are
portable across both projects) and replace the per-pack name pattern with
a sector-directory layout that fits Tilth's six-sector scope.

Why this exists
---------------
Scribe currently writes from RFA + ``orgs/<slug>/PROJECT_CONTEXT.md`` —
correct for Law 1 (RFA verbatim) and Law 5 (applicant substance). But
Scribe has no per-sector terminology surface: when drafting for the urban-
ag sector, Scribe doesn't know that "soilless" / "controlled environment
agriculture" / "CEA" are the canonical funder dialects, vs. "regenerative"
/ "soil health" / "covered soil" for field-scale ag. This module provides
the surface — a loader for sector-scoped terminology packs that Scribe
can consult at PRE-gate context assembly.

This module ships **the abstraction only**. Wiring into ``Scribe.seat`` is
a separate Round bundle. Loader is callable today; nothing in the locked
v0.1 hot path depends on it.

Six-sector scope (CLAUDE.md ``§ Six-sector scope``)
---------------------------------------------------
Sector enum is closed. Adding a 7th requires updating
:data:`SECTOR_VALID` (deliberate friction — sector taxonomy is a
governance choice, not a free-form string).

- ``workforce_future``      — workforce of the future
- ``education_future``      — future-proof education
- ``regenerative_ag``       — regenerative agriculture
- ``urban_ag``              — urban / soilless ag
- ``land_community``        — land and community development
- ``eco_art``               — eco-art

Layout convention
-----------------
::

    pipeline/knowledge_packs/
      regenerative_ag/
        usda_terminology.json
        cover_crops.json
        livestock_integration.json
      urban_ag.json                  # single-file form also accepted

A sector may be a directory (``glob('*.json')`` auto-merge, sorted) OR a
single JSON file. Missing sectors load to an empty pack — the consuming
gate decides whether that's an error.

Pack JSON schema (v1.0)
-----------------------
::

    {
      "schemaVersion": "1.0",
      "description": "<human-readable>",
      "domains": [
        {"id": "soil-health", "name": "...", "description": "..."}
      ],
      "facts": [
        {
          "id": "fct-001",
          "domainId": "soil-health",
          "statement": "...",
          "tags": ["cover-crops", "no-till"],
          "confidence": "high",      // {high, medium, low}
          "scope": "federal"         // {general, federal, state, regional}
        }
      ],
      "relationships": [
        {
          "id": "rel-001",
          "fromFactId": "fct-001",
          "toFactId": "fct-002",
          "relationType": "supports",
          "description": "..."
        }
      ]
    }

Fail-closed posture
-------------------
- JSON parse errors → :class:`KnowledgePackSchemaError`
- Missing/wrong-typed required fields → :class:`KnowledgePackSchemaError`
- Duplicate fact / domain / relationship IDs across merged files →
  :class:`KnowledgePackDuplicateIdError`. Ambiguity is not silently
  resolved; the operator must rename the duplicate.
- Missing sector directory or file → empty :class:`KnowledgePack` with
  ``is_loaded=False``. **Not** an error — caller decides.

Sovereignty / dependency posture
--------------------------------
Pure stdlib (``json``, ``pathlib``). No spaCy, no NetworkX, no Pydantic.
Adheres to ``pyproject.toml`` § ``[project]`` locked deps.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final, Literal, Mapping

# --------------------------------------------------------------------------
# Sector enum — closed set per CLAUDE.md § Six-sector scope
# --------------------------------------------------------------------------

Sector = Literal[
    "workforce_future",
    "education_future",
    "regenerative_ag",
    "urban_ag",
    "land_community",
    "eco_art",
]

SECTOR_VALID: Final[frozenset[str]] = frozenset({
    "workforce_future",
    "education_future",
    "regenerative_ag",
    "urban_ag",
    "land_community",
    "eco_art",
})

ConfidenceTier = Literal["high", "medium", "low"]
_CONFIDENCE_VALID: Final[frozenset[str]] = frozenset({"high", "medium", "low"})

# Scope is advisory metadata — packs use it to scope facts to a jurisdiction.
# Not enforced as a closed set so packs can carry e.g. "region:northeast" or
# "state:PA" without schema changes.

# --------------------------------------------------------------------------
# Exceptions
# --------------------------------------------------------------------------

class KnowledgePackError(Exception):
    """Base class for knowledge-pack load errors."""


class KnowledgePackSchemaError(KnowledgePackError):
    """JSON parse failure or schema-shape violation in a pack file."""


class KnowledgePackDuplicateIdError(KnowledgePackError):
    """Duplicate fact / domain / relationship ID across merged pack files.

    Raised fail-closed: ambiguous ID would corrupt downstream lookups. The
    operator must rename one of the colliding entries.
    """


class KnowledgePackInvalidSectorError(KnowledgePackError):
    """Caller passed a sector name not in :data:`SECTOR_VALID`."""


# --------------------------------------------------------------------------
# Dataclasses (frozen / kw_only / slots — §7 R1 convention)
# --------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True, slots=True)
class PackDomain:
    """A grouping of related facts within a pack."""

    id: str
    name: str
    description: str = ""

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise KnowledgePackSchemaError("PackDomain.id must be non-empty")
        if not self.name.strip():
            raise KnowledgePackSchemaError("PackDomain.name must be non-empty")


@dataclass(frozen=True, kw_only=True, slots=True)
class PackFact:
    """A single sector-scoped terminology / context statement."""

    id: str
    domain_id: str
    statement: str
    tags: tuple[str, ...] = ()
    confidence: ConfidenceTier = "medium"
    scope: str = "general"

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise KnowledgePackSchemaError("PackFact.id must be non-empty")
        if not self.domain_id.strip():
            raise KnowledgePackSchemaError(
                f"PackFact[{self.id}].domain_id must be non-empty"
            )
        if not self.statement.strip():
            raise KnowledgePackSchemaError(
                f"PackFact[{self.id}].statement must be non-empty"
            )
        if self.confidence not in _CONFIDENCE_VALID:
            raise KnowledgePackSchemaError(
                f"PackFact[{self.id}].confidence={self.confidence!r} "
                f"not in {sorted(_CONFIDENCE_VALID)}"
            )


@dataclass(frozen=True, kw_only=True, slots=True)
class PackRelationship:
    """A typed edge between two facts within (or across) a pack."""

    id: str
    from_fact_id: str
    to_fact_id: str
    relation_type: str
    description: str = ""

    def __post_init__(self) -> None:
        for attr in ("id", "from_fact_id", "to_fact_id", "relation_type"):
            if not getattr(self, attr).strip():
                raise KnowledgePackSchemaError(
                    f"PackRelationship.{attr} must be non-empty"
                )


@dataclass(frozen=True, kw_only=True, slots=True)
class KnowledgePack:
    """Merged pack for a single sector.

    ``is_loaded`` is False when the sector has no pack files on disk —
    that's not an error, just an empty terminology surface.
    ``source_files`` lists the absolute paths that were merged, in the
    order they were applied (sorted glob).
    """

    sector: str
    schema_version: str
    domains: tuple[PackDomain, ...]
    facts: tuple[PackFact, ...]
    relationships: tuple[PackRelationship, ...]
    source_files: tuple[Path, ...] = field(default_factory=tuple)
    is_loaded: bool = False

    def __post_init__(self) -> None:
        if self.sector not in SECTOR_VALID:
            raise KnowledgePackInvalidSectorError(
                f"sector={self.sector!r} not in {sorted(SECTOR_VALID)}"
            )

    def fact_by_id(self, fact_id: str) -> PackFact | None:
        """Return the fact with matching id, or None."""
        for fact in self.facts:
            if fact.id == fact_id:
                return fact
        return None

    def facts_in_domain(self, domain_id: str) -> tuple[PackFact, ...]:
        """Return all facts whose ``domain_id`` matches."""
        return tuple(f for f in self.facts if f.domain_id == domain_id)


# --------------------------------------------------------------------------
# Schema validation helpers
# --------------------------------------------------------------------------

def _validate_top_level(data: object, source: Path) -> dict:
    """Confirm a pack JSON parses to an object with the required keys."""
    if not isinstance(data, dict):
        raise KnowledgePackSchemaError(
            f"{source}: top-level must be a JSON object, got {type(data).__name__}"
        )
    if not isinstance(data.get("schemaVersion"), str):
        raise KnowledgePackSchemaError(
            f"{source}: missing or non-string 'schemaVersion'"
        )
    for key in ("domains", "facts", "relationships"):
        if not isinstance(data.get(key), list):
            raise KnowledgePackSchemaError(
                f"{source}: missing or non-list '{key}'"
            )
    return data


def _parse_domain(raw: object, source: Path) -> PackDomain:
    if not isinstance(raw, dict):
        raise KnowledgePackSchemaError(
            f"{source}: domain entries must be objects, got {type(raw).__name__}"
        )
    return PackDomain(
        id=str(raw.get("id", "")),
        name=str(raw.get("name", "")),
        description=str(raw.get("description", "")),
    )


def _parse_fact(raw: object, source: Path) -> PackFact:
    if not isinstance(raw, dict):
        raise KnowledgePackSchemaError(
            f"{source}: fact entries must be objects, got {type(raw).__name__}"
        )
    tags_raw = raw.get("tags", [])
    if not isinstance(tags_raw, list) or not all(isinstance(t, str) for t in tags_raw):
        raise KnowledgePackSchemaError(
            f"{source}: fact.tags must be a list of strings"
        )
    confidence = raw.get("confidence", "medium")
    if not isinstance(confidence, str):
        raise KnowledgePackSchemaError(
            f"{source}: fact.confidence must be a string"
        )
    return PackFact(
        id=str(raw.get("id", "")),
        domain_id=str(raw.get("domainId", "")),
        statement=str(raw.get("statement", "")),
        tags=tuple(tags_raw),
        confidence=confidence,  # type: ignore[arg-type]  # validated in __post_init__
        scope=str(raw.get("scope", "general")),
    )


def _parse_relationship(raw: object, source: Path) -> PackRelationship:
    if not isinstance(raw, dict):
        raise KnowledgePackSchemaError(
            f"{source}: relationship entries must be objects, got "
            f"{type(raw).__name__}"
        )
    return PackRelationship(
        id=str(raw.get("id", "")),
        from_fact_id=str(raw.get("fromFactId", "")),
        to_fact_id=str(raw.get("toFactId", "")),
        relation_type=str(raw.get("relationType", "")),
        description=str(raw.get("description", "")),
    )


# --------------------------------------------------------------------------
# Single-file load
# --------------------------------------------------------------------------

def _load_pack_file(path: Path) -> tuple[
    str,
    list[PackDomain],
    list[PackFact],
    list[PackRelationship],
]:
    """Load and validate one pack JSON file.

    Returns (schemaVersion, domains, facts, relationships). Raises
    :class:`KnowledgePackSchemaError` on parse / shape failure.
    """
    try:
        raw_text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise KnowledgePackSchemaError(f"{path}: read failed: {exc}") from exc

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise KnowledgePackSchemaError(f"{path}: JSON parse error: {exc}") from exc

    parsed = _validate_top_level(data, path)
    schema_version = parsed["schemaVersion"]

    domains = [_parse_domain(d, path) for d in parsed["domains"]]
    facts = [_parse_fact(f, path) for f in parsed["facts"]]
    relationships = [_parse_relationship(r, path) for r in parsed["relationships"]]

    return schema_version, domains, facts, relationships


# --------------------------------------------------------------------------
# Merge logic
# --------------------------------------------------------------------------

def _merge_check_unique(
    items: list[PackDomain] | list[PackFact] | list[PackRelationship],
    label: str,
    source: Path,
) -> None:
    """Raise if any id appears twice within or across merged files."""
    seen: dict[str, Path] = {}
    for item in items:
        if item.id in seen:
            raise KnowledgePackDuplicateIdError(
                f"{label} id={item.id!r} duplicated: "
                f"first seen in {seen[item.id]}, repeated in {source}. "
                f"Rename one of the colliding entries."
            )
        seen[item.id] = source


# --------------------------------------------------------------------------
# Public entry point
# --------------------------------------------------------------------------

DEFAULT_BASE_DIR: Final[Path] = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "pipeline" / "knowledge_packs"
)


def _resolve_pack_paths(sector: str, base_dir: Path) -> list[Path]:
    """Return sorted list of JSON files to merge for *sector*.

    - ``base_dir/<sector>/`` directory: glob ``*.json``, sorted.
    - ``base_dir/<sector>.json`` single file: list of one.
    - Neither: empty list (caller treats as "no pack on disk").
    """
    sector_dir = base_dir / sector
    if sector_dir.is_dir():
        return sorted(sector_dir.glob("*.json"))

    sector_file = base_dir / f"{sector}.json"
    if sector_file.is_file():
        return [sector_file]

    return []


def load_sector_pack(
    sector: str,
    base_dir: Path | None = None,
) -> KnowledgePack:
    """Load and merge all knowledge-pack files for *sector*.

    Args:
        sector: Must be in :data:`SECTOR_VALID`.
        base_dir: Override base directory (defaults to
            ``pipeline/knowledge_packs/`` relative to the project root).

    Returns:
        :class:`KnowledgePack` with merged domains/facts/relationships.
        ``is_loaded`` is True iff at least one pack file was found and
        parsed successfully.

    Raises:
        :class:`KnowledgePackInvalidSectorError`: sector not in enum.
        :class:`KnowledgePackSchemaError`: any pack file fails parse/shape.
        :class:`KnowledgePackDuplicateIdError`: duplicate id across merge.
    """
    if sector not in SECTOR_VALID:
        raise KnowledgePackInvalidSectorError(
            f"sector={sector!r} not in {sorted(SECTOR_VALID)}"
        )

    resolved_base = base_dir if base_dir is not None else DEFAULT_BASE_DIR
    paths = _resolve_pack_paths(sector, resolved_base)

    if not paths:
        return KnowledgePack(
            sector=sector,
            schema_version="1.0",
            domains=(),
            facts=(),
            relationships=(),
            source_files=(),
            is_loaded=False,
        )

    merged_domains: list[PackDomain] = []
    merged_facts: list[PackFact] = []
    merged_relationships: list[PackRelationship] = []
    schema_version: str | None = None
    loaded_files: list[Path] = []

    for path in paths:
        sv, doms, facts, rels = _load_pack_file(path)
        if schema_version is None:
            schema_version = sv
        merged_domains.extend(doms)
        merged_facts.extend(facts)
        merged_relationships.extend(rels)
        loaded_files.append(path)

        # Per-file uniqueness already enforced by accumulation against `seen`
        # in the dedicated check below — but cheap to surface a clear error
        # message tied to the offending file.
        _merge_check_unique(merged_domains, "PackDomain", path)
        _merge_check_unique(merged_facts, "PackFact", path)
        _merge_check_unique(merged_relationships, "PackRelationship", path)

    assert schema_version is not None  # paths non-empty implies one load

    return KnowledgePack(
        sector=sector,
        schema_version=schema_version,
        domains=tuple(merged_domains),
        facts=tuple(merged_facts),
        relationships=tuple(merged_relationships),
        source_files=tuple(loaded_files),
        is_loaded=True,
    )


# --------------------------------------------------------------------------
# Integration helpers — for orchestrator / envelope-builder wire-in
#
# The Scribe seat receives a `ScribeEnvelope` whose `compiled_prompt` is
# already assembled and `project_context` is already populated. The
# upstream envelope-builder calls these helpers to fold sector-pack
# terminology into either surface before constructing the envelope.
#
# Two integration shapes (caller picks):
#
#   A) Splice into compiled_prompt:
#        block = render_sector_context_block(pack)
#        compiled_prompt = f"{rfa_block}\n\n{block}\n\n{project_context_block}"
#
#   B) Inject into project_context map:
#        ctx = merge_pack_into_project_context(project_context, pack)
#        envelope = ScribeEnvelope(..., project_context=ctx)
#
# Shape (A) gives Scribe the sector vocabulary directly in its prompt
# context. Shape (B) makes the pack inspectable by Logician PRE-gate
# (e.g., a future `F-SCRIBE-SECTOR-PACK-MISSING` gate could read the
# 'sector_knowledge' key on the project_context mapping).
# --------------------------------------------------------------------------

# Reasonable default cap on facts surfaced into a prompt — keeps token
# budget bounded even when an operator over-populates a pack. Operators can
# raise via the explicit `max_facts` arg if needed.
_DEFAULT_PROMPT_FACT_CAP: Final[int] = 24

# Project-context key used by `merge_pack_into_project_context`. Documented
# here so downstream Logician gates have a stable read site.
PROJECT_CONTEXT_PACK_KEY: Final[str] = "sector_knowledge"


def render_sector_context_block(
    pack: KnowledgePack,
    *,
    max_facts: int | None = None,
) -> str:
    """Render a pack as a prompt-ready Markdown context block.

    Returns a non-empty string when ``pack.is_loaded`` is True; returns an
    empty string otherwise (so callers can unconditionally splice the
    result with ``f"{...}\\n\\n{block}\\n\\n{...}"`` and rely on a
    no-pack-loaded sector producing no extra noise).

    Output shape (one section per domain, facts grouped by ``domain_id``):

    ::

        ## Sector context: <sector>

        ### <Domain Name>
        - [<confidence>] <statement>
        - [<confidence>] <statement>
        ...

    Args:
        pack: Loaded :class:`KnowledgePack`.
        max_facts: Optional cap on total facts in the rendered block. When
            ``None`` (default), uses :data:`_DEFAULT_PROMPT_FACT_CAP`.
            Pass ``0`` to render headers only (no facts) — useful for
            audit-trail tests.
    """
    if not pack.is_loaded or not pack.facts:
        return ""

    cap = _DEFAULT_PROMPT_FACT_CAP if max_facts is None else max(0, int(max_facts))

    lines: list[str] = [f"## Sector context: {pack.sector}", ""]

    domains_by_id: dict[str, PackDomain] = {d.id: d for d in pack.domains}
    facts_emitted = 0

    # Render in declaration order (pack.domains order); ungrouped facts at end.
    seen_domain_ids: set[str] = set()
    for domain in pack.domains:
        domain_facts = pack.facts_in_domain(domain.id)
        if not domain_facts:
            continue

        lines.append(f"### {domain.name}")
        if domain.description:
            lines.append(f"_{domain.description}_")
        for fact in domain_facts:
            if facts_emitted >= cap:
                break
            lines.append(f"- [{fact.confidence}] {fact.statement}")
            facts_emitted += 1
        lines.append("")
        seen_domain_ids.add(domain.id)
        if facts_emitted >= cap:
            break

    # Catch facts whose domain_id wasn't declared — surface under a fallback
    # header rather than dropping silently.
    orphans = tuple(
        f for f in pack.facts
        if f.domain_id not in domains_by_id
    )
    if orphans and facts_emitted < cap:
        lines.append("### Other context")
        for fact in orphans:
            if facts_emitted >= cap:
                break
            lines.append(f"- [{fact.confidence}] {fact.statement}")
            facts_emitted += 1
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def merge_pack_into_project_context(
    project_context: Mapping[str, Any],
    pack: KnowledgePack,
) -> dict[str, Any]:
    """Return a copy of *project_context* with a sector-knowledge entry added.

    The new key (:data:`PROJECT_CONTEXT_PACK_KEY`, defaults to
    ``"sector_knowledge"``) maps to a structured dict containing the
    pack's sector, source-file paths, fact tuple, and rendered prompt
    block. Downstream Logician gates can inspect either the structured
    facts or the rendered text.

    A no-pack-loaded sector (``pack.is_loaded == False``) still injects
    the key with ``loaded=False`` so consumers can detect the
    sector-was-attempted vs sector-not-set distinction.

    Never mutates the input mapping. Returns a new dict.
    """
    out: dict[str, Any] = dict(project_context)
    out[PROJECT_CONTEXT_PACK_KEY] = {
        "sector": pack.sector,
        "loaded": pack.is_loaded,
        "schema_version": pack.schema_version,
        "fact_count": len(pack.facts),
        "domain_count": len(pack.domains),
        "source_files": tuple(str(p) for p in pack.source_files),
        "rendered_block": render_sector_context_block(pack),
    }
    return out


__all__ = [
    "Sector",
    "SECTOR_VALID",
    "ConfidenceTier",
    "KnowledgePack",
    "PackDomain",
    "PackFact",
    "PackRelationship",
    "KnowledgePackError",
    "KnowledgePackSchemaError",
    "KnowledgePackDuplicateIdError",
    "KnowledgePackInvalidSectorError",
    "load_sector_pack",
    "render_sector_context_block",
    "merge_pack_into_project_context",
    "PROJECT_CONTEXT_PACK_KEY",
    "DEFAULT_BASE_DIR",
]
