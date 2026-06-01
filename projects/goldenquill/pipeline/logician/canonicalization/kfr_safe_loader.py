"""KFR YAML SafeLoader — refuses anchors / aliases / merge-keys / custom tags.

Architecture v7.0.4-M1 §2.2.2 (CF-RT-01 closure leg 2). The loader is a
``yaml.SafeLoader`` subclass that fails-closed at construction time on
any YAML construct that could decouple raw-byte representation from
parsed-object representation:

* ``&anchor`` declarations.
* ``*alias`` references.
* Mapping keys equal to the literal string ``<<`` (PyYAML's merge-key
  surface) — checked BEFORE PyYAML's merge-key resolution runs.
* The ``tag:yaml.org,2002:merge`` tag explicitly.
* Any custom tag (``!!python/``, ``!!set``, ``!!omap``, etc.).
* Any tag prefix outside the YAML 1.2 core scalar/mapping/sequence
  set.

On rejection the loader raises :class:`KfrConstructError`. The
:func:`load_kfr_safe` and :func:`load_kfr_safe_bytes` helpers translate
``yaml.YAMLError`` into ``KfrConstructError`` with the offending
construct named so the caller can map to ``F-KFR-YAML-CONSTRUCT-FORBIDDEN``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Final

import yaml
from yaml.constructor import ConstructorError


# YAML 1.2 core mapping/sequence/scalar tags. Anything outside this set
# (and not a plain unrecognized scalar tag) is forbidden.
_ALLOWED_CORE_TAGS: Final[frozenset[str]] = frozenset({
    "tag:yaml.org,2002:map",
    "tag:yaml.org,2002:seq",
    "tag:yaml.org,2002:str",
    "tag:yaml.org,2002:int",
    "tag:yaml.org,2002:float",
    "tag:yaml.org,2002:bool",
    "tag:yaml.org,2002:null",
})

# Forbidden tags surfaced by name in error detail. The merge-key tag is
# the single highest-priority closure (RT-01 verbatim path).
KFR_FORBIDDEN_TAGS: Final[frozenset[str]] = frozenset({
    "tag:yaml.org,2002:merge",
    "tag:yaml.org,2002:python",
    "tag:yaml.org,2002:python/none",
    "tag:yaml.org,2002:python/bool",
    "tag:yaml.org,2002:python/str",
    "tag:yaml.org,2002:python/unicode",
    "tag:yaml.org,2002:python/int",
    "tag:yaml.org,2002:python/long",
    "tag:yaml.org,2002:python/float",
    "tag:yaml.org,2002:python/complex",
    "tag:yaml.org,2002:python/tuple",
    "tag:yaml.org,2002:python/list",
    "tag:yaml.org,2002:python/dict",
    "tag:yaml.org,2002:python/object",
    "tag:yaml.org,2002:python/object/apply",
    "tag:yaml.org,2002:python/object/new",
    "tag:yaml.org,2002:python/module",
    "tag:yaml.org,2002:python/name",
    "tag:yaml.org,2002:set",
    "tag:yaml.org,2002:omap",
    "tag:yaml.org,2002:pairs",
    "tag:yaml.org,2002:timestamp",
    "tag:yaml.org,2002:binary",
})


class KfrConstructError(ValueError):
    """Raised when the SafeLoader refuses a YAML construct.

    Carries an ``offending_construct`` attribute summarizing what
    failed: ``"anchor"``, ``"alias"``, ``"merge_key"``, ``"custom_tag"``,
    ``"forbidden_tag"``.
    """

    def __init__(self, message: str, *, offending_construct: str) -> None:
        super().__init__(message)
        self.offending_construct = offending_construct


class KfrSafeLoader(yaml.SafeLoader):
    """SafeLoader subclass enforcing §2.2.2 anchor / alias / merge-key ban."""

    # Class-level toggles set by yaml.YAMLObject metaclass machinery.
    yaml_constructors = dict(yaml.SafeLoader.yaml_constructors)
    yaml_multi_constructors = dict(yaml.SafeLoader.yaml_multi_constructors)

    def construct_mapping(self, node, deep=False):  # type: ignore[override]
        # Pre-resolve check: refuse mappings containing the literal
        # string key ``<<`` BEFORE PyYAML's merge-key resolution can
        # fire.  This is the verbatim RT-01 closure path — the check
        # happens regardless of whether the value side is an alias,
        # an inline mapping, or a sequence of mappings.
        if isinstance(node, yaml.MappingNode):
            for key_node, _value_node in node.value:
                key_resolved_tag = key_node.tag
                if key_resolved_tag == "tag:yaml.org,2002:merge":
                    raise KfrConstructError(
                        f"YAML merge-key tag found at "
                        f"{key_node.start_mark} — KFR forbids "
                        "merge-keys (architecture v7.0.4-M1 §2.2.2 RT-01 "
                        "closure leg 2)",
                        offending_construct="merge_key",
                    )
                if (
                    isinstance(key_node, yaml.ScalarNode)
                    and isinstance(key_node.value, str)
                    and key_node.value == "<<"
                ):
                    raise KfrConstructError(
                        f"mapping key '<<' found at "
                        f"{key_node.start_mark} — KFR forbids the "
                        "merge-key surface even when the literal "
                        "appears without ``*alias`` "
                        "(architecture v7.0.4-M1 §2.2.2)",
                        offending_construct="merge_key",
                    )
        return super().construct_mapping(node, deep=deep)


def _check_node_recursive(node: yaml.Node) -> None:
    """Walk a parsed YAML node tree; refuse forbidden tags / anchors."""
    if node is None:
        return
    anchor = getattr(node, "anchor", None)
    if anchor is not None:
        raise KfrConstructError(
            f"YAML anchor '&{anchor}' found at {node.start_mark} — "
            "KFR forbids anchor declarations "
            "(architecture v7.0.4-M1 §2.2.2)",
            offending_construct="anchor",
        )
    tag = node.tag
    if isinstance(tag, str):
        if tag in KFR_FORBIDDEN_TAGS:
            raise KfrConstructError(
                f"forbidden YAML tag {tag!r} found at "
                f"{node.start_mark} — KFR refuses fail-closed "
                "(architecture v7.0.4-M1 §2.2.2)",
                offending_construct="forbidden_tag",
            )
        if tag.startswith("tag:yaml.org,2002:python"):
            raise KfrConstructError(
                f"forbidden Python custom tag {tag!r} found at "
                f"{node.start_mark} — KFR refuses fail-closed "
                "(architecture v7.0.4-M1 §2.2.2)",
                offending_construct="custom_tag",
            )
        if tag.startswith("!"):
            raise KfrConstructError(
                f"forbidden custom tag {tag!r} found at "
                f"{node.start_mark} — KFR admits only YAML 1.2 core "
                "tags (architecture v7.0.4-M1 §2.2.2)",
                offending_construct="custom_tag",
            )
        if tag.startswith("tag:yaml.org,2002:") and tag not in _ALLOWED_CORE_TAGS:
            raise KfrConstructError(
                f"forbidden core-namespace tag {tag!r} found at "
                f"{node.start_mark} — KFR admits only YAML 1.2 core "
                "scalar/mapping/sequence tags",
                offending_construct="forbidden_tag",
            )
    if isinstance(node, yaml.SequenceNode):
        for child in node.value:
            _check_node_recursive(child)
    if isinstance(node, yaml.MappingNode):
        for key_node, value_node in node.value:
            _check_node_recursive(key_node)
            _check_node_recursive(value_node)


def _scan_alias_events(text: str) -> None:
    """Pre-parse pass that refuses alias references.

    PyYAML's parser walks events once during loading; the
    :class:`KfrSafeLoader` already refuses aliases via the
    ``construct_yaml_str`` constructor refusal indirectly, but to make
    the failure mode explicit we also pre-scan the event stream.
    """
    for event in yaml.parse(text, Loader=yaml.SafeLoader):
        if isinstance(event, yaml.AliasEvent):
            raise KfrConstructError(
                f"YAML alias '*{event.anchor}' found at "
                f"{event.start_mark} — KFR forbids alias references "
                "(architecture v7.0.4-M1 §2.2.2)",
                offending_construct="alias",
            )
        if isinstance(event, (yaml.ScalarEvent, yaml.MappingStartEvent, yaml.SequenceStartEvent)):
            anchor = getattr(event, "anchor", None)
            if anchor is not None:
                raise KfrConstructError(
                    f"YAML anchor '&{anchor}' declaration found at "
                    f"{event.start_mark} — KFR forbids anchor "
                    "declarations (architecture v7.0.4-M1 §2.2.2)",
                    offending_construct="anchor",
                )


def load_kfr_safe_bytes(data: bytes) -> Any:
    """Parse ``data`` (UTF-8 bytes) under :class:`KfrSafeLoader`.

    Raises :class:`KfrConstructError` on any forbidden construct.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise KfrConstructError(
            f"load_kfr_safe_bytes expects bytes, got "
            f"{type(data).__name__}",
            offending_construct="invalid_input",
        )
    try:
        text = bytes(data).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise KfrConstructError(
            f"KFR file is not valid UTF-8: {exc}",
            offending_construct="invalid_encoding",
        ) from exc

    # Phase 1: pre-scan event stream to refuse aliases / anchor decls.
    _scan_alias_events(text)
    # Phase 2: full compose to capture node tree for tag checks.
    try:
        node = yaml.compose(text, Loader=KfrSafeLoader)
    except ConstructorError as exc:
        raise KfrConstructError(
            f"KFR YAML construction refused: {exc}",
            offending_construct="custom_tag",
        ) from exc
    except yaml.YAMLError as exc:
        raise KfrConstructError(
            f"KFR YAML parse error: {exc}",
            offending_construct="parse_error",
        ) from exc
    _check_node_recursive(node)
    # Phase 3: load via SafeLoader (post-merge-key check).
    try:
        result = yaml.load(text, Loader=KfrSafeLoader)
    except KfrConstructError:
        raise
    except yaml.YAMLError as exc:
        raise KfrConstructError(
            f"KFR YAML load error: {exc}",
            offending_construct="parse_error",
        ) from exc
    return result


def load_kfr_safe(path: Path | str) -> Any:
    """Read ``path`` and parse under :class:`KfrSafeLoader`.

    Raises :class:`KfrConstructError` on any forbidden construct or I/O
    error encountered while reading.  Path is resolved as-is (no
    symlink-rejection here — that lives in the atomic-read discipline
    of §4.2.2; this loader is a pure-bytes parser).
    """
    path_obj = Path(path)
    try:
        data = path_obj.read_bytes()
    except OSError as exc:
        raise KfrConstructError(
            f"KFR file at {path_obj!s} unreadable: {exc}",
            offending_construct="io_error",
        ) from exc
    return load_kfr_safe_bytes(data)


__all__ = [
    "KFR_FORBIDDEN_TAGS",
    "KfrConstructError",
    "KfrSafeLoader",
    "load_kfr_safe",
    "load_kfr_safe_bytes",
]
