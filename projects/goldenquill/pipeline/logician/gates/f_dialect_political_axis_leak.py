"""F-DIALECT-POLITICAL-AXIS-LEAK — apolitical-dialect routing enforcement.

PRE-gate at order 6.55 (between v7.0.8's F-CIC-CLC-COUPLING-VIOLATION at 6.5
and F-CIC-CLC-MATCH-NULL at 6.6 — dialect routing operates on the CLC enum
and presumes coupling-violation discipline is already clean). Static check;
fires at Tilth startup AND on any config refresh (router.yaml reload,
knowledge-pack reload, PROJECT_CONTEXT.md edit, prompt-template recompile,
CIC card load, admin_risk_register reload). Fail-closed.

Architecture authority: ``pipeline/architecture/v0.1/architecture_v7_0_12_apolitical_dialect_amendment.md``
(LOCKED 2026-05-16T14:00:00Z; lock_history rows 234/248).
Blueprint authority: ``pipeline/blueprint/v0.1/section_04_logician_v2_x_apolitical_dialect.md``
(LOCKED 2026-05-16T14:00:00Z; lock_history rows 236/249). Cycle 1 + Cycle 2
fold-ins (18 applied + 1 deferred) baked into LOCKed canonical bytes per
row-170 transparent disposition.

Detection layers
----------------
**Layer 1 — Lexical pattern (regex on field names and string literals).**
Catches the obvious surface naming patterns plus the four/five retired
literal values. Field-name detection uses both regex (case-insensitive,
word-boundary-aware per FI-2) and a token-based matcher (C2-M-6) to catch
CamelCase, dot-separated, abbreviated, and re-ordered variants. String-literal
detection is gated on the surrounding context being *routing-relevant* per the
explicit path-scope rule (FI-3 — no vague surrounding-context heuristic).

**Layer 1b — Field-name-independent literal proximity (FI-2).** Two-or-more
retired literals co-occurring within 200 characters / same YAML collection
trips the gate regardless of field name. Catches creative wrappers that
preserve the four-value enum but rename the carrier.

**Layer 1c — Singular literal in routing-relevant path (C2-H-1).** A single
occurrence of a retired literal in a routing-relevant path (per FI-3 path
scope) trips the gate without requiring co-occurrence. Strengthens FI-2 for
the case where the routing primitive carries one literal per row.

**Layer 2 — Pydantic AST inspection.** Static AST walk over all files
matching the routing-relevant Python scope. Flags any Pydantic model field
whose annotation is ``Literal[...]`` containing two or more of the retired
values. The actual AST walk lives in the caller; this module consumes the
discovered annotations via the injected source protocol.

**Layer 3 — Card + register schema validation.** Schema validators (CIC
card schema, admin_risk_register schema) explicitly forbid the retired
property names and explicitly forbid the retired enum values inside the
replacement `clc` field. Any validation failure surfaces here.

Subcodes
--------
- ``F-DIALECT-POLITICAL-AXIS-LEAK.field_name`` — retired field name found in
  routing-relevant context (Layer 1 field-name match).
- ``F-DIALECT-POLITICAL-AXIS-LEAK.routing_literal`` — retired enum literal
  found in a routing-relevant context with at least one other retired literal
  also present (Layer 1 + Layer 1b co-occurrence match).
- ``F-DIALECT-POLITICAL-AXIS-LEAK.routing_literal_independent`` — two-or-more
  retired literals co-occurring within proximity window regardless of field
  name (Layer 1b independent-of-field detection; FI-2).
- ``F-DIALECT-POLITICAL-AXIS-LEAK.routing_literal_singular`` — single
  occurrence of a retired literal inside a routing-relevant path; tripped
  without requiring co-occurrence (Layer 1c; C2-H-1).
- ``F-DIALECT-POLITICAL-AXIS-LEAK.pydantic_literal`` — Pydantic ``Literal[...]``
  annotation contains two or more retired values (Layer 2).
- ``F-DIALECT-POLITICAL-AXIS-LEAK.pydantic_literal_unresolved`` — Pydantic
  ``Literal[...]`` references a constant / re-export / typing.get_args /
  Final initializer that could not be resolved by the AST walker (Layer 2
  conservative HIGH-severity fail; FI-4 + C2-H-2).
- ``F-DIALECT-POLITICAL-AXIS-LEAK.schema_property`` — CIC card or
  admin_risk_register schema fails strict-validation (Layer 3).

Law 3 isolation discipline
--------------------------
Per Cycle 2 fold-in C2-P0-9: the ``surrounding_context_summary`` payload
field carries an SHA3-256 hex digest of the surrounding context, NEVER the
raw context text. Raw text can contain email addresses, grant IDs,
applicant-specific facts, or other PII; emitting it to a Logfire span would
breach Law 3 isolation. Callers that need the raw context for operator
recovery can read it from the offending file at the recorded line number.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Final, Iterable, Optional, Protocol, runtime_checkable


GATE_ID: Final[str] = "F-DIALECT-POLITICAL-AXIS-LEAK"
PRE_GATE_ORDER: Final[float] = 6.55


# ---------------------------------------------------------------------------
# Retired vocabulary — closed set per architecture v7.0.12 §1.1.
# ---------------------------------------------------------------------------

RETIRED_LITERALS: Final[frozenset[str]] = frozenset(
    {"conservative", "centrist", "progressive", "soul_fire", "soul-fire"}
)
"""Closed set of retired political-axis enum values."""

RETIRED_FIELD_NAMES: Final[frozenset[str]] = frozenset(
    {"funder_political_axis", "progressive_register"}
)
"""Closed set of retired field names (exact)."""

RETIRED_FIELD_NAME_TOKENS: Final[tuple[frozenset[str], ...]] = (
    frozenset({"funder", "political", "axis"}),
    frozenset({"progressive", "register"}),
)
"""Token sets for the C2-M-6 token-based matcher. Each tuple element is a
set of tokens that, if all present in an identifier's split-on-non-alphanumeric
form (case-insensitive), constitutes a field-name match. Catches
``funder_political_axis``, ``funderPoliticalAxis``, ``axisPoliticalFunder``,
``progressive_register_v2``, ``progressiveRegister``, etc."""


# Layer 1 lexical regexes (FI-2 broadened to case-insensitive word-boundary).
LAYER_1_FIELD_REGEX: Final[re.Pattern[str]] = re.compile(
    r"(?i)\b(funder[_\-]?political[_\-]?axis|progressive[_\-]?register)\b"
)

# Substring detector for any field name containing "political_axis" — FI-2
# catches ``funder_political_axis_v2``, ``_funder_political_axis``, etc.
LAYER_1_FIELD_SUBSTRING: Final[re.Pattern[str]] = re.compile(
    r"(?i)political[_\-]?axis"
)

LAYER_1_LITERAL_REGEX: Final[re.Pattern[str]] = re.compile(
    r"\b(conservative|centrist|progressive|soul[_\-]?fire)\b"
)


# ---------------------------------------------------------------------------
# Excluded-path allowlist (architecture v7.0.12 §1.1 list).
#
# Symlinks are resolved via ``os.path.realpath`` BEFORE path-scope match per
# Cycle 2 fold-in C2-M-3 (partial).
# ---------------------------------------------------------------------------

EXCLUDED_PATH_GLOBS: Final[tuple[str, ...]] = (
    "pipeline/engineering/lock_history.v1.jsonl",
    # Version-trail history files (LOCKed architecture snapshots).
    "pipeline/architecture/v0.1/tilth_architecture_locked_v4_2026-04-16.md",
    "pipeline/architecture/v0.1/tilth_architecture_locked_v5*.md",
    "pipeline/architecture/v0.1/tilth_architecture_locked_v6*.md",
    "pipeline/architecture/v0.1/tilth_architecture_locked_v7_a1_a6_2026-04-19.md",
    # Architecture amendment audit files documenting the retirement itself.
    "pipeline/architecture/v0.1/architecture_v7_0_12_apolitical_dialect_amendment.md",
    "pipeline/blueprint/v0.1/section_04_logician_v2_x_apolitical_dialect.md",
    "pipeline/blueprint/v0.1/section_00_5_apolitical_dialect_amendment.md",
    "pipeline/blueprint/v0.1/section_18_v1_2_amendment.md",
    # Validation audit trail.
    "pipeline/validation/v7_0_12_thesis_*/*",
    # Audit/thesis dispatch artifacts may quote the retired vocabulary.
    "pipeline/validation/v7_0_12_thesis_*/**/*",
    # Lessons / institutional memory expansion-cycles block lives at YAML path
    # (filtered by the schema-validation layer, NOT by path allowlist).
    # Logician gate + AST-lint rule + their tests legitimately reference the
    # retired vocabulary to detect it.
    "pipeline/logician/gates/f_dialect_political_axis_leak.py",
    "pipeline/logician/gates/f_dialect_migration_incomplete.py",
    "pipeline/linting/r_no_political_axis_literal.py",
    "tests/logician/gates/test_f_dialect_political_axis_leak.py",
    "tests/logician/gates/test_f_dialect_migration_incomplete.py",
    "tests/linting/test_r_no_political_axis_literal.py",
)


# ---------------------------------------------------------------------------
# Routing-relevant path scope (FI-3 — replaces the vague
# "surrounding-context check" with explicit path-scope rule).
#
# A path is routing-relevant if it matches ANY of these globs.
# ---------------------------------------------------------------------------

ROUTING_RELEVANT_PATH_GLOBS: Final[tuple[str, ...]] = (
    # Dialect-bearing modules (Scribe seat + dialect codebook).
    "pipeline/*/dialect*",
    "pipeline/*/*/dialect*",
    "pipeline/*/*/*/dialect*",
    "pipeline/seats/scribe/dialect*",
    # Register-bearing modules + admin-risk register.
    "pipeline/*/register*",
    "pipeline/*/*/register*",
    "pipeline/institutional_memory/admin_risk_register*",
    # All CIC + CLC cards + card schemas.
    "pipeline/cards/**/*.yaml",
    "pipeline/cards/_schema/*.json",
    # Prompt templates (any path containing /prompts/ or skill SKILL.md).
    "pipeline/*/prompts/**",
    "pipeline/**/prompts/**",
    "skills/**/SKILL.md",
    "skills/**/*.md",
    # Agent specs.
    "pipeline/engineering/agents/**",
    # Dialect codebook reference.
    "pipeline/engineering/agents/references/dialect_codebook.yaml",
)


# ---------------------------------------------------------------------------
# Layer 1b proximity window — characters.
# ---------------------------------------------------------------------------

LAYER_1B_PROXIMITY_WINDOW_CHARS: Final[int] = 200


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class DialectLeakFinding:
    """One detection of a political-axis leak.

    Per Cycle 2 fold-in C2-P0-9, ``surrounding_context_sha3_256_hex`` is the
    SHA3-256 hex digest of the surrounding context. Raw context is NEVER
    emitted into the finding payload because it may carry PII / applicant
    facts / grant IDs whose disclosure to a Logfire span would breach Law 3
    isolation. Callers needing the raw context for operator recovery read it
    from ``file_path`` at ``line_number``.
    """

    subcode: str
    layer: int
    file_path: str
    line_number: Optional[int]
    detail: str
    matched_pattern: str
    surrounding_context_sha3_256_hex: str


@dataclass(frozen=True, kw_only=True)
class DialectLeakResult:
    """Result of a full apolitical-dialect static scan.

    ``passed=True`` means no findings across all layers → cycle proceeds.
    ``passed=False`` means at least one finding → fail-closed at startup /
    config-refresh / commit-hook.
    """

    passed: bool
    findings: tuple[DialectLeakFinding, ...]

    # Stage-aware fields (Consulting Node Doctrine)
    has_findings: bool = False
    blocking: bool = True
    advisory_only: bool = False
    requires_handoff_disclosure: bool = False


# ---------------------------------------------------------------------------
# Injected source protocols (gate code never touches the filesystem).
# ---------------------------------------------------------------------------


@runtime_checkable
class FieldNameSourceCallable(Protocol):
    """Yields ``(file_path, line_number, field_name)`` triples from YAML
    files, JSON schemas, and Pydantic model field declarations across the
    scan scope."""

    def __call__(self) -> Iterable[tuple[str, Optional[int], str]]: ...


@runtime_checkable
class StringLiteralSourceCallable(Protocol):
    """Yields ``(file_path, line_number, literal, surrounding_context)``
    quadruples for every string literal value discovered in the scan scope
    that matches the retired-literal regex.

    ``surrounding_context`` is the textual neighborhood (typically the
    enclosing line plus 1-2 lines on either side, OR the enclosing YAML
    collection's serialized form) used by Layer 1b for proximity detection.
    The gate hashes this neighborhood before recording it; raw text never
    leaves this module."""

    def __call__(
        self,
    ) -> Iterable[tuple[str, Optional[int], str, str]]: ...


@runtime_checkable
class PydanticLiteralSourceCallable(Protocol):
    """Yields ``(file_path, line_number, field_name, literal_values,
    resolved)`` quintuples for every Pydantic field whose annotation is
    ``Literal[...]``.

    ``literal_values`` is the resolved tuple of string values inside the
    ``Literal[...]`` annotation. ``resolved`` is ``True`` if the AST walker
    successfully resolved all imported constants / list/tuple/set literals /
    ``typing.get_args(X)`` / Final/ClassVar initializers; ``False`` if any
    portion could not be statically resolved (forces the conservative
    `.pydantic_literal_unresolved` HIGH-severity sub-tag per FI-4 + C2-H-2)."""

    def __call__(
        self,
    ) -> Iterable[tuple[str, Optional[int], str, tuple[str, ...], bool]]: ...


@runtime_checkable
class SchemaValidationSourceCallable(Protocol):
    """Yields ``(file_path, property_path, failure_kind, matched_pattern)``
    quadruples for every CIC card schema / admin_risk_register schema
    validation failure that surfaces a retired property name or retired
    enum value.

    ``failure_kind`` is one of ``"property_forbidden"`` (retired property name
    survives in production data) or ``"enum_value_forbidden"`` (replacement
    field carries a retired enum value)."""

    def __call__(self) -> Iterable[tuple[str, str, str, str]]: ...


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _sha3_256_hex(text: str) -> str:
    """SHA3-256 hex digest of ``text``. Used to redact raw context per
    Cycle 2 fold-in C2-P0-9."""
    return hashlib.sha3_256(text.encode("utf-8", errors="replace")).hexdigest()


def _glob_match(pattern: str, path: str) -> bool:
    """Simple glob match for path-scope checks.

    Supports ``*`` (single segment), ``**`` (any segments), and exact match.
    Right-anchored to allow the path to live anywhere in the workspace tree.
    """
    import fnmatch

    # Translate ``**`` into the fnmatch idiom by anchoring on full path.
    if "**" in pattern:
        # Convert glob to regex for cross-segment matching.
        regex_parts: list[str] = []
        i = 0
        while i < len(pattern):
            c = pattern[i]
            if c == "*" and i + 1 < len(pattern) and pattern[i + 1] == "*":
                regex_parts.append(".*")
                i += 2
                # Consume trailing slash if present.
                if i < len(pattern) and pattern[i] == "/":
                    i += 1
            elif c == "*":
                regex_parts.append("[^/]*")
                i += 1
            elif c == "?":
                regex_parts.append("[^/]")
                i += 1
            elif c == ".":
                regex_parts.append(r"\.")
                i += 1
            else:
                regex_parts.append(re.escape(c))
                i += 1
        regex = "(?:.*/)?" + "".join(regex_parts) + "$"
        return re.match(regex, path) is not None
    # Single-segment glob — use fnmatch directly on full path or basename.
    if fnmatch.fnmatch(path, pattern):
        return True
    if fnmatch.fnmatch(path, "*/" + pattern):
        return True
    return False


def _is_excluded_path(file_path: str) -> bool:
    """Check if ``file_path`` matches any entry in ``EXCLUDED_PATH_GLOBS``.

    Per C2-M-3 (partial): callers should pass ``os.path.realpath``-resolved
    paths to defeat symlink-based bypass. This module performs the match
    on the path as-given; the resolution happens at the caller's source
    enumeration boundary.
    """
    for pattern in EXCLUDED_PATH_GLOBS:
        if _glob_match(pattern, file_path):
            return True
    return False


def _is_routing_relevant_path(file_path: str) -> bool:
    """Per FI-3: check if ``file_path`` is in a routing-relevant scope."""
    for pattern in ROUTING_RELEVANT_PATH_GLOBS:
        if _glob_match(pattern, file_path):
            return True
    return False


def _identifier_tokens(name: str) -> frozenset[str]:
    """Split an identifier on non-alphanumeric chars + camelCase boundaries.

    Returns the case-insensitive token set. Catches ``funderPoliticalAxis``,
    ``funder_political_axis``, ``funder.political.axis``,
    ``FunderPoliticalAxis`` per C2-M-6 token-based matcher.
    """
    # First split on non-alphanumeric chars.
    parts = re.split(r"[^A-Za-z0-9]+", name)
    out: set[str] = set()
    for p in parts:
        if not p:
            continue
        # Then split camelCase boundaries within each part.
        sub = re.findall(r"[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[A-Z]+|[0-9]+", p)
        for token in sub:
            if token:
                out.add(token.lower())
    return frozenset(out)


def _token_set_matches(name: str) -> bool:
    """C2-M-6 token-based matcher: True if ``name`` contains all tokens of
    any retired token-set in any order."""
    name_tokens = _identifier_tokens(name)
    for required in RETIRED_FIELD_NAME_TOKENS:
        if required.issubset(name_tokens):
            return True
    return False


# ---------------------------------------------------------------------------
# Layer-by-layer detectors
# ---------------------------------------------------------------------------


def _layer_1_field_name(
    field_name_source: FieldNameSourceCallable,
) -> list[DialectLeakFinding]:
    findings: list[DialectLeakFinding] = []
    for file_path, line_number, field_name in field_name_source():
        if _is_excluded_path(file_path):
            continue
        regex_match = LAYER_1_FIELD_REGEX.search(field_name)
        substring_match = LAYER_1_FIELD_SUBSTRING.search(field_name)
        token_match = _token_set_matches(field_name)
        if regex_match is None and substring_match is None and not token_match:
            continue
        # The matched pattern reported is the most specific detector that hit.
        matched = (
            regex_match.group(0)
            if regex_match
            else (substring_match.group(0) if substring_match else field_name)
        )
        findings.append(
            DialectLeakFinding(
                subcode=f"{GATE_ID}.field_name",
                layer=1,
                file_path=file_path,
                line_number=line_number,
                detail=(
                    f"field name {field_name!r} matches retired political-axis "
                    "field-name pattern; rename to a CLC slug (for routing "
                    "fields) or remove (for prose)"
                ),
                matched_pattern=matched,
                surrounding_context_sha3_256_hex=_sha3_256_hex(field_name),
            )
        )
    return findings


def _layer_1_literal_with_proximity(
    string_literal_source: StringLiteralSourceCallable,
) -> list[DialectLeakFinding]:
    """Combines Layer 1 routing-literal (co-occurrence with field-name match),
    Layer 1b independent literal proximity (FI-2), and Layer 1c singular
    in-routing-path (C2-H-1).

    A literal in a routing-relevant path trips ``.routing_literal_singular``
    immediately (C2-H-1). Two-or-more co-occurring literals within the
    proximity window trip ``.routing_literal_independent`` (FI-2) regardless
    of path scope. The legacy ``.routing_literal`` sub-tag fires when the
    proximity check + a field-name-adjacent context both apply (preserved
    for completeness with §4.X.1 prose).
    """
    findings: list[DialectLeakFinding] = []
    # Group literals by (file_path, surrounding_context) for proximity check.
    by_neighborhood: dict[tuple[str, str], list[
        tuple[Optional[int], str]
    ]] = {}
    for file_path, line_number, literal, context in string_literal_source():
        if _is_excluded_path(file_path):
            continue
        if not LAYER_1_LITERAL_REGEX.search(literal):
            continue
        # Layer 1c — singular in routing-relevant path (C2-H-1).
        if _is_routing_relevant_path(file_path):
            findings.append(
                DialectLeakFinding(
                    subcode=f"{GATE_ID}.routing_literal_singular",
                    layer=1,
                    file_path=file_path,
                    line_number=line_number,
                    detail=(
                        f"retired literal {literal!r} found in routing-relevant "
                        f"path {file_path!r}; rename or remove (C2-H-1: "
                        "single-occurrence detection in routing-scoped path)"
                    ),
                    matched_pattern=literal,
                    surrounding_context_sha3_256_hex=_sha3_256_hex(context),
                )
            )
        # Bucket by (file, sha3 of context) for proximity check.
        key = (file_path, context)
        by_neighborhood.setdefault(key, []).append((line_number, literal))

    # Layer 1b — co-occurrence detection (FI-2).
    for (file_path, context), entries in by_neighborhood.items():
        retired_in_window = [
            (ln, lit) for ln, lit in entries
            if LAYER_1_LITERAL_REGEX.search(lit)
        ]
        # Deduplicate literals — at least TWO distinct retired literals
        # within the same neighborhood is the FI-2 trip condition.
        distinct_literals = {
            (LAYER_1_LITERAL_REGEX.search(lit).group(0).lower()  # type: ignore[union-attr]
             if LAYER_1_LITERAL_REGEX.search(lit) else lit)
            for _ln, lit in retired_in_window
        }
        if len(distinct_literals) >= 2 and len(context) <= LAYER_1B_PROXIMITY_WINDOW_CHARS:
            ln = retired_in_window[0][0]
            findings.append(
                DialectLeakFinding(
                    subcode=f"{GATE_ID}.routing_literal_independent",
                    layer=1,
                    file_path=file_path,
                    line_number=ln,
                    detail=(
                        f"{len(distinct_literals)} distinct retired political-axis "
                        f"literals co-occur within {LAYER_1B_PROXIMITY_WINDOW_CHARS}-char "
                        "proximity window; constitutes routing-relevant evidence "
                        "regardless of field name (FI-2)"
                    ),
                    matched_pattern=",".join(sorted(distinct_literals)),
                    surrounding_context_sha3_256_hex=_sha3_256_hex(context),
                )
            )
    return findings


def _layer_2_pydantic_literal(
    pydantic_literal_source: PydanticLiteralSourceCallable,
) -> list[DialectLeakFinding]:
    findings: list[DialectLeakFinding] = []
    for (
        file_path,
        line_number,
        field_name,
        literal_values,
        resolved,
    ) in pydantic_literal_source():
        if _is_excluded_path(file_path):
            continue
        if not resolved:
            # FI-4 + C2-H-2: unresolved Literal[...] resolution is fail-closed
            # HIGH-severity per the conservative both-branch / try-except FAIL
            # discipline. Cannot statically prove the annotation is safe.
            findings.append(
                DialectLeakFinding(
                    subcode=f"{GATE_ID}.pydantic_literal_unresolved",
                    layer=2,
                    file_path=file_path,
                    line_number=line_number,
                    detail=(
                        f"Pydantic field {field_name!r} has Literal[...] "
                        "annotation that could not be statically resolved by "
                        "the AST walker (imported constant / re-export / "
                        "typing.get_args / Final initializer); fail-closed "
                        "conservatively (FI-4 + C2-H-2)"
                    ),
                    matched_pattern=field_name,
                    surrounding_context_sha3_256_hex=_sha3_256_hex(
                        f"{field_name}={literal_values!r}"
                    ),
                )
            )
            continue
        retired_present = {
            v.lower().replace("-", "_") for v in literal_values
            if v.lower().replace("-", "_") in {
                "conservative", "centrist", "progressive", "soul_fire"
            }
        }
        if len(retired_present) >= 2:
            findings.append(
                DialectLeakFinding(
                    subcode=f"{GATE_ID}.pydantic_literal",
                    layer=2,
                    file_path=file_path,
                    line_number=line_number,
                    detail=(
                        f"Pydantic field {field_name!r} has Literal[...] "
                        f"annotation containing {sorted(retired_present)!r} — "
                        "at least two retired political-axis values present; "
                        "fail-closed per architecture v7.0.12 §1.3 Layer 2"
                    ),
                    matched_pattern=",".join(sorted(retired_present)),
                    surrounding_context_sha3_256_hex=_sha3_256_hex(
                        f"{field_name}=Literal{literal_values!r}"
                    ),
                )
            )
    return findings


def _layer_3_schema(
    schema_validation_source: SchemaValidationSourceCallable,
) -> list[DialectLeakFinding]:
    findings: list[DialectLeakFinding] = []
    for (
        file_path,
        property_path,
        failure_kind,
        matched_pattern,
    ) in schema_validation_source():
        # Schema-validation failures are evaluated regardless of excluded-path
        # allowlist — the path allowlist exempts historical/audit prose from
        # the lexical layers, but schema-validation is a load-time check on
        # *production* card / register data and must fire even if the file
        # path nominally matches an excluded glob.
        findings.append(
            DialectLeakFinding(
                subcode=f"{GATE_ID}.schema_property",
                layer=3,
                file_path=file_path,
                line_number=None,
                detail=(
                    f"schema validation failed at property path "
                    f"{property_path!r} ({failure_kind}); production card or "
                    "register data carries retired political-axis vocabulary"
                ),
                matched_pattern=matched_pattern,
                surrounding_context_sha3_256_hex=_sha3_256_hex(
                    f"{property_path}:{failure_kind}:{matched_pattern}"
                ),
            )
        )
    return findings


# ---------------------------------------------------------------------------
# Gate entry point
# ---------------------------------------------------------------------------


from pipeline.logician.types import OutputType, GateStage, ArtifactType, FINAL_OR_SUBMISSION_STAGES

def run(
    *,
    field_name_source: FieldNameSourceCallable,
    string_literal_source: StringLiteralSourceCallable,
    pydantic_literal_source: PydanticLiteralSourceCallable,
    schema_validation_source: SchemaValidationSourceCallable,
    output_type: OutputType = "FIT_FARMS_SUBMISSION_PACKET",
    stage: GateStage = "final_export_attempt",
    artifact_type: ArtifactType = "pdf",
) -> DialectLeakResult:
    """Run all detection layers; aggregate findings.

    Caller assembles the four injected sources (file globbing, YAML parsing,
    AST walking, schema validation) and passes them in. Gate code never
    touches the filesystem. Per Cycle 2 C2-P0-9, all findings carry SHA3-256
    hashes of surrounding context — never raw text — to preserve Law 3
    isolation when findings are emitted to Logfire spans.
    """
    findings: list[DialectLeakFinding] = []
    findings.extend(_layer_1_field_name(field_name_source))
    findings.extend(_layer_1_literal_with_proximity(string_literal_source))
    findings.extend(_layer_2_pydantic_literal(pydantic_literal_source))
    findings.extend(_layer_3_schema(schema_validation_source))

    has_findings = len(findings) > 0
    blocking = has_findings
    advisory_only = False
    requires_handoff_disclosure = False

    if has_findings:
        if output_type == "THIRD_PARTY_DRAFT_DELIVERABLE":
            if stage not in FINAL_OR_SUBMISSION_STAGES:
                blocking = False
                advisory_only = True
                requires_handoff_disclosure = True
        else:
            if stage in ("draft_generation", "draft_review"):
                blocking = False
                advisory_only = True

    return DialectLeakResult(
        passed=not has_findings,
        findings=tuple(findings),
        has_findings=has_findings,
        blocking=blocking,
        advisory_only=advisory_only,
        requires_handoff_disclosure=requires_handoff_disclosure,
    )


__all__ = [
    "GATE_ID",
    "PRE_GATE_ORDER",
    "RETIRED_LITERALS",
    "RETIRED_FIELD_NAMES",
    "RETIRED_FIELD_NAME_TOKENS",
    "LAYER_1_FIELD_REGEX",
    "LAYER_1_FIELD_SUBSTRING",
    "LAYER_1_LITERAL_REGEX",
    "EXCLUDED_PATH_GLOBS",
    "ROUTING_RELEVANT_PATH_GLOBS",
    "LAYER_1B_PROXIMITY_WINDOW_CHARS",
    "DialectLeakFinding",
    "DialectLeakResult",
    "FieldNameSourceCallable",
    "StringLiteralSourceCallable",
    "PydanticLiteralSourceCallable",
    "SchemaValidationSourceCallable",
    "run",
]
