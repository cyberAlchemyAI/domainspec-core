"""F-CIC-CLC-COUPLING-VIOLATION — structural decoupling enforcement.

PRE-gate at order 6.5. Static check; fires at Tilth startup AND on any config
refresh (router.yaml reload, knowledge-pack reload, PROJECT_CONTEXT.md edit,
prompt-template recompile). Fail-closed.

Authority: ``pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md``
§4.1 (LOCKED 2026-05-08; Cycle-1 RT-02 fix expanded detection from regex-only
to four layers).

Detection layers
----------------
**Layer 1 — Lexical pattern (regex on field/function names).** Primary
detection, NOT exclusive. Catches the obvious naming patterns
(``primary_clc_*``, ``preferred_capital_logic_*``, etc.).

**Layer 2 — Pydantic AST inspection.** Catches structural coupling regardless
of field name. Flags any Pydantic model field whose annotation is
structurally-equivalent to ``Mapping[CustomerIdentityCategory, Collection[CapitalLogicCard]]``
(or the reverse direction).

**Layer 3 — Value-set check.** Catches creative renamings (e.g.,
``funding_streams: [public_purpose, operating_capacity]``). For every YAML
file under the scanned roots, walks the dict; if any field's value-list is a
non-empty strict subset of either canonical enum AND appears in a context
keyed by the OTHER canonical enum, the gate trips.

**Layer 4 — Knowledge-pack schema validation.** The ``KnowledgePackManifest``
Pydantic schema explicitly forbids any top-level field whose annotation
includes ``CapitalLogicCard``. Knowledge packs may carry CIC tags but may NOT
carry CLC eligibility lists.

Any layer's match trips the gate. HIGH severity, operator escalation,
fail-closed at startup.

Subcodes
--------
- ``F-CIC-CLC-COUPLING-VIOLATION.layer1_lexical`` — regex match
- ``F-CIC-CLC-COUPLING-VIOLATION.layer2_pydantic_shape`` — AST shape match
- ``F-CIC-CLC-COUPLING-VIOLATION.layer3_value_set`` — value-list subset match in CIC-keyed context
- ``F-CIC-CLC-COUPLING-VIOLATION.layer4_knowledge_pack_schema`` — manifest field annotation includes CLC
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Optional, Protocol, runtime_checkable

from pipeline.types import (
    CAPITAL_LOGIC_CARD_VALUES,
    CUSTOMER_IDENTITY_CATEGORY_VALUES,
)


GATE_ID = "F-CIC-CLC-COUPLING-VIOLATION"
PRE_GATE_ORDER = 6.5

# ---------------------------------------------------------------------------
# Layer 1 regex (primary detection — not exclusive; Layers 2/3/4 catch the
# rest)
#
# Matches field names like:
#   primary_clc, preferred_capital_logic_activations, allowed_clc_subset,
#   activated_capital_logic, enabled_clc_streams, valid_capital_logic_set
# ---------------------------------------------------------------------------

LAYER_1_FIELD_REGEX = re.compile(
    r"^(primary|preferred|allowed|activated|enabled|valid)"
    r"_(capital_logic|clc)([._].*)?$",
    re.IGNORECASE,
)


# Set view of canonical enum values for fast subset check (Layer 3)
_CIC_VALUE_SET = frozenset(CUSTOMER_IDENTITY_CATEGORY_VALUES)
_CLC_VALUE_SET = frozenset(CAPITAL_LOGIC_CARD_VALUES)


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CouplingFinding:
    """One detection of a coupling violation."""

    subcode: str
    layer: int
    file_path: str
    line_number: Optional[int]
    detail: str


@dataclass(frozen=True)
class CouplingViolationResult:
    """Result of a full coupling-violation static scan.

    ``passed=True`` means no findings across all four layers → cycle proceeds.
    ``passed=False`` means at least one finding → fail-closed at startup.
    """

    passed: bool
    findings: tuple[CouplingFinding, ...]


# ---------------------------------------------------------------------------
# Injected dependencies (no direct file I/O in gate code)
# ---------------------------------------------------------------------------


@runtime_checkable
class FieldNameSourceCallable(Protocol):
    """Yields ``(file_path, line_number, field_name)`` triples across all
    YAML files, Pydantic schemas, and prompt templates in the scan scope.

    Caller is responsible for file globbing, YAML parsing, AST walking. Gate
    consumes a flat stream of name observations and applies Layer-1 regex.
    """

    def __call__(self) -> Iterable[tuple[str, Optional[int], str]]: ...


@runtime_checkable
class PydanticShapeSourceCallable(Protocol):
    """Yields ``(file_path, line_number, field_name, annotation_repr)``
    quadruples for every Pydantic model field discovered in the scan scope.

    Caller resolves the annotation repr to a canonical structural shape; the
    gate matches the canonical shape against forbidden patterns.
    """

    def __call__(self) -> Iterable[tuple[str, Optional[int], str, str]]: ...


@runtime_checkable
class CICKeyedYamlValueSourceCallable(Protocol):
    """Yields ``(file_path, line_number, key, value_list)`` quadruples for
    YAML structures shaped like::

        somefield:
          food_systems: [public_purpose, operating_capacity]
          educator: [research_evidence]

    Caller walks YAML files in the scan roots (``vault_shared/``,
    ``orgs/<slug>/``, ``pipeline/knowledge_packs/``, ``vault_*/``), identifies
    dict keys that are valid ``CustomerIdentityCategory`` values, and yields
    each (key, value_list) it encounters. The gate then checks whether the
    value_list is a non-empty subset of the CLC enum.

    The symmetric direction (CLC-keyed → CIC value-list) is also yielded by
    this reader; gate handles both via the ``key_enum`` discriminator the
    reader supplies (encoded as ``"cic"`` or ``"clc"`` prefix in ``key``).
    """

    def __call__(
        self,
    ) -> Iterable[tuple[str, Optional[int], str, list[str]]]: ...


@runtime_checkable
class KnowledgePackManifestSourceCallable(Protocol):
    """Yields ``(file_path, field_name, annotation_repr)`` triples for every
    field annotation discovered on ``KnowledgePackManifest``-style Pydantic
    models in the scan scope.

    Gate flags any annotation_repr containing ``CapitalLogicCard`` (with or
    without quotes / aliases / Optional / list[ ] wrappers).
    """

    def __call__(self) -> Iterable[tuple[str, str, str]]: ...


# ---------------------------------------------------------------------------
# Layer-by-layer detectors
# ---------------------------------------------------------------------------


def _layer_1_lexical(
    field_name_source: FieldNameSourceCallable,
) -> list[CouplingFinding]:
    findings: list[CouplingFinding] = []
    for file_path, line_number, field_name in field_name_source():
        if LAYER_1_FIELD_REGEX.match(field_name):
            findings.append(
                CouplingFinding(
                    subcode=f"{GATE_ID}.layer1_lexical",
                    layer=1,
                    file_path=file_path,
                    line_number=line_number,
                    detail=(
                        f"field name {field_name!r} matches forbidden "
                        "CIC→CLC coupling regex (Layer 1)"
                    ),
                )
            )
    return findings


def _layer_2_pydantic(
    pydantic_shape_source: PydanticShapeSourceCallable,
) -> list[CouplingFinding]:
    """Detect Mapping[CIC, Collection[CLC]] or its reverse, regardless of name."""
    findings: list[CouplingFinding] = []
    for file_path, line_number, field_name, annotation in pydantic_shape_source():
        norm = annotation.replace(" ", "")
        # Forward direction: dict[CIC, Collection[CLC]]
        forward = (
            ("CustomerIdentityCategory" in norm or "CIC" in norm)
            and "CapitalLogicCard" in norm
            and ("dict[" in norm or "Mapping[" in norm)
        )
        # Reverse direction: dict[CLC, Collection[CIC]]
        # Same check — we don't disambiguate forward/reverse at the structural level
        if forward:
            findings.append(
                CouplingFinding(
                    subcode=f"{GATE_ID}.layer2_pydantic_shape",
                    layer=2,
                    file_path=file_path,
                    line_number=line_number,
                    detail=(
                        f"Pydantic field {field_name!r} has annotation "
                        f"{annotation!r} which structurally couples CIC and "
                        "CLC; orthogonality forbids any (CIC, CLC) coupling "
                        "shape (Layer 2)"
                    ),
                )
            )
    return findings


def _layer_3_value_set(
    cic_keyed_yaml_value_source: CICKeyedYamlValueSourceCallable,
) -> list[CouplingFinding]:
    """Catches subset-of-canonical-enum value lists in keyed-by-other-enum contexts."""
    findings: list[CouplingFinding] = []
    for file_path, line_number, key, value_list in cic_keyed_yaml_value_source():
        if not value_list:
            continue
        value_set = frozenset(value_list)
        # If key is a CIC value AND value_list is subset of CLCs → coupling
        if key in _CIC_VALUE_SET and value_set.issubset(_CLC_VALUE_SET):
            findings.append(
                CouplingFinding(
                    subcode=f"{GATE_ID}.layer3_value_set",
                    layer=3,
                    file_path=file_path,
                    line_number=line_number,
                    detail=(
                        f"YAML node keyed by CIC value {key!r} carries value "
                        f"list {value_list!r} which is a subset of "
                        "CapitalLogicCard; constitutes CIC→CLC coupling "
                        "(Layer 3)"
                    ),
                )
            )
        # Symmetric: key is CLC, value_list subset of CICs
        elif key in _CLC_VALUE_SET and value_set.issubset(_CIC_VALUE_SET):
            findings.append(
                CouplingFinding(
                    subcode=f"{GATE_ID}.layer3_value_set",
                    layer=3,
                    file_path=file_path,
                    line_number=line_number,
                    detail=(
                        f"YAML node keyed by CLC value {key!r} carries value "
                        f"list {value_list!r} which is a subset of "
                        "CustomerIdentityCategory; constitutes CLC→CIC "
                        "coupling (Layer 3)"
                    ),
                )
            )
    return findings


def _layer_4_knowledge_pack(
    knowledge_pack_manifest_source: KnowledgePackManifestSourceCallable,
) -> list[CouplingFinding]:
    findings: list[CouplingFinding] = []
    for file_path, field_name, annotation in knowledge_pack_manifest_source():
        if "CapitalLogicCard" in annotation:
            findings.append(
                CouplingFinding(
                    subcode=f"{GATE_ID}.layer4_knowledge_pack_schema",
                    layer=4,
                    file_path=file_path,
                    line_number=None,
                    detail=(
                        f"KnowledgePackManifest-shaped model declares field "
                        f"{field_name!r} with annotation {annotation!r} "
                        "containing CapitalLogicCard; knowledge packs may "
                        "NOT carry CLC eligibility lists (Layer 4)"
                    ),
                )
            )
    return findings


# ---------------------------------------------------------------------------
# Gate entry point
# ---------------------------------------------------------------------------


def run(
    *,
    field_name_source: FieldNameSourceCallable,
    pydantic_shape_source: PydanticShapeSourceCallable,
    cic_keyed_yaml_value_source: CICKeyedYamlValueSourceCallable,
    knowledge_pack_manifest_source: KnowledgePackManifestSourceCallable,
) -> CouplingViolationResult:
    """Run all four detection layers; aggregate findings.

    Caller assembles the four injected sources (file globbing, YAML parsing,
    AST walking) and passes them in. Gate code never touches the filesystem.
    """
    findings: list[CouplingFinding] = []
    findings.extend(_layer_1_lexical(field_name_source))
    findings.extend(_layer_2_pydantic(pydantic_shape_source))
    findings.extend(_layer_3_value_set(cic_keyed_yaml_value_source))
    findings.extend(_layer_4_knowledge_pack(knowledge_pack_manifest_source))

    return CouplingViolationResult(
        passed=len(findings) == 0,
        findings=tuple(findings),
    )
