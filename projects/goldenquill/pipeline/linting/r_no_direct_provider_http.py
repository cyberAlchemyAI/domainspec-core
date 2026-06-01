"""R-NO-DIRECT-PROVIDER-HTTP — forbid direct HTTP egress outside the wrapper.

Companion code for §4 v2.x.5 amendment (LOCKED 2026-05-16 row 232).
Extended by §4 v2.x.6 amendment (LOCKED 2026-05-16T16:30:00Z row 234) with
the ``.direct_provider_call_without_wrapper`` sub-tag per §11.1.

Closes the CC-007 sovereignty bypass at the AST-lint layer. Mirrors the
§4 v2.x.1 row 198 sub-tag-extension precedent (R-ARCHIVIST-NO-CANONICAL-MUTATE)
— enumerated forbidden primitives + MappingProxyType-wrapped table +
ALLOWLISTED_FILES closed set + named drift tests per sub-tag.

Sub-tags (5 + 2 fold-ins)
-------------------------

==========================================================  =================================
Primitive (concrete Call.func shape)                        Sub-tag
==========================================================  =================================
``urllib.request.urlopen(...)``                             ``no_direct_provider_http.urlopen``
``urllib.request.Request(...)`` followed by ``urlopen``     ``no_direct_provider_http.urlopen``
``requests.{post,get,put,delete,...}`` / ``Session.*``      ``no_direct_provider_http.requests_lib``
``httpx.{post,get,...}`` / ``Client.*`` / ``AsyncClient.*`` ``no_direct_provider_http.httpx_lib``
``aiohttp.ClientSession.*`` / ``aiohttp.request``           ``no_direct_provider_http.aiohttp``
``socket.socket().connect()`` + HTTP-style sendall          ``no_direct_provider_http.raw_socket``
``http.client.HTTPConnection`` / ``HTTPSConnection``        ``no_direct_provider_http.raw_socket``
Unknown HTTP-class library import (RT-14 fold-in)           ``no_direct_provider_http.unknown_http_library_import``
``_call_anthropic`` / ``_call_openai_style`` without        ``no_direct_provider_http.``
``http_post=`` kwarg (§4 v2.x.6 §11.1 — RT-06 static layer)  ``direct_provider_call_without_wrapper``
==========================================================  =================================

ALLOWLISTED_FILES (closed set)
------------------------------

Only ``pipeline/orchestrator/provider_boundary.py`` is permitted to call
``urllib.request.urlopen``. Per §11.6 DC-01 + RT-16 fold-in the router-side
allowlist entry collapses once ``router._http_post_outbound_shape`` delegates
to ``stdlib_urlopen_caller``; this module's allowlist matches the LOCKed §11.6
shape — single permitted call site.

OD-4 grandfathered glob exclusion
---------------------------------

``pipeline/validation/**`` and ``pipeline/engineering/_scratch/**`` are
Thesis-pipeline / dispatch / scratch helpers — out of sovereignty scope. The
AST visitor early-returns on path match.

Threat-model bounding
---------------------

Bounded under v7 LOCKED A1 (single-client) + A4 (operator-trusted preflight).
Static-analysis evasion shapes (``getattr(urllib.request, 'urlopen')``,
``__dict__['urlopen']``, local-name reassignment, ``importlib.import_module``)
are out-of-scope; the runtime identity pin in ``provider_boundary.py``
catches these at invocation time (§12.4 RT-C2-02 + §12.11 RT-14 PARTIAL).
Multi-tenant promotion to MED severity lands at Section O.5 v2 hardening +
Stage-5 Sovereign Node commons amendment.

CC-003 carry-forward
--------------------

Per §4 v2.x.5 §11.6 the CC-003 quarantine logic (deprecated-module-import
ban) is preserved inside this rule body. The seat-local provider files
(``provider_anthropic.py``, ``provider_google.py``, ``provider_groq.py``)
are no longer allowlisted — after CC-007 refactor they contain no direct
HTTP primitives, so they fall off the allowlist naturally.
"""

from __future__ import annotations

import ast
from pathlib import Path
from types import MappingProxyType
from typing import Final, Iterator, Mapping

from pipeline.linting._rule_types import Rule, Violation


# ---------------------------------------------------------------------------
# Target glob — every Python module under pipeline/, minus OD-4 grandfathered
# subdirs. The Rule.target_glob fires once per file matching the pattern; the
# visitor's path-check skips OD-4 dirs unconditionally.
# ---------------------------------------------------------------------------

_TARGET_GLOB: Final[str] = "pipeline/**/*.py"

# Failure-code attribution — carried in Violation.message body so the
# F-CLASS-* attribution travels with the diagnostic regardless of how the
# reason_tag is read downstream.
_FAILURE_CODE: Final[str] = "R-NO-DIRECT-PROVIDER-HTTP"


# ---------------------------------------------------------------------------
# Closed-set allowlist of files permitted to invoke forbidden primitives.
# Per §3.1 + §11.6 (DC-01 + RT-16 fold-in collapse).
# ---------------------------------------------------------------------------

_ALLOWLISTED_FILE_SUFFIXES: Final[frozenset[str]] = frozenset({
    # Sole permitted urllib.request.urlopen call site.
    "pipeline/orchestrator/provider_boundary.py",
})

ALLOWLISTED_FILES: Final[Mapping[str, str]] = MappingProxyType({
    "pipeline/orchestrator/provider_boundary.py": (
        "Sole permitted urllib.request.urlopen call site; defines "
        "stdlib_urlopen_caller wrapped by enforce_outbound_boundary."
    ),
})

# OD-4 grandfathered glob exclusions. Path-substring match; visitor early-
# returns on hit. ``pipeline/deprecated/`` is a quarantined operator-glue
# tree (pre-§4 v2.x.5 CC-003 carry-forward) — modules there may still hold
# legacy urllib paths but are not imported from runtime per the deprecated-
# import ban below.
_GRANDFATHER_PATH_MARKERS: Final[tuple[str, ...]] = (
    "/pipeline/validation/",
    "/pipeline/engineering/_scratch/",
    "/pipeline/deprecated/",
)


# ---------------------------------------------------------------------------
# Forbidden-primitive table (5 sub-tags + RT-14 fold-in).
# (module_dotted_path, attribute_name) → sub-tag (without the leading dot —
# the dot is added at emit time so the disposition-packet acceptance form
# ``".urlopen" in result.sub_tags`` matches the wire representation).
# ---------------------------------------------------------------------------

_FORBIDDEN_PRIMITIVES_INTERNAL: dict[tuple[str, str], str] = {
    # urllib family — .urlopen sub-tag.
    ("urllib.request", "urlopen"): "urlopen",
    ("urllib.request", "Request"): "urlopen",

    # requests library — .requests_lib sub-tag.
    ("requests", "post"): "requests_lib",
    ("requests", "get"): "requests_lib",
    ("requests", "put"): "requests_lib",
    ("requests", "delete"): "requests_lib",
    ("requests", "patch"): "requests_lib",
    ("requests", "head"): "requests_lib",
    ("requests", "request"): "requests_lib",
    ("requests", "Session"): "requests_lib",
    ("requests.sessions", "Session"): "requests_lib",

    # httpx library — .httpx_lib sub-tag.
    ("httpx", "post"): "httpx_lib",
    ("httpx", "get"): "httpx_lib",
    ("httpx", "put"): "httpx_lib",
    ("httpx", "delete"): "httpx_lib",
    ("httpx", "patch"): "httpx_lib",
    ("httpx", "head"): "httpx_lib",
    ("httpx", "request"): "httpx_lib",
    ("httpx", "Client"): "httpx_lib",
    ("httpx", "AsyncClient"): "httpx_lib",

    # aiohttp — .aiohttp sub-tag.
    ("aiohttp", "ClientSession"): "aiohttp",
    ("aiohttp", "request"): "aiohttp",

    # raw socket / http.client — .raw_socket sub-tag.
    ("http.client", "HTTPConnection"): "raw_socket",
    ("http.client", "HTTPSConnection"): "raw_socket",
}

#: MappingProxyType-wrapped immutable view (RT-14 closure precedent — same
#: shape as R-ARCHIVIST-NO-CANONICAL-MUTATE.FORBIDDEN_PRIMITIVES).
#: Downstream consumers cannot silence the rule by reassignment.
FORBIDDEN_PRIMITIVES: Mapping[tuple[str, str], str] = MappingProxyType(
    _FORBIDDEN_PRIMITIVES_INTERNAL
)


# ---------------------------------------------------------------------------
# Allowed HTTP libraries (RT-14 fold-in).
# Imports of any HTTP-class library NOT in this set fire the
# .unknown_http_library_import sub-tag at module-load AST visit time.
# Closed set regenerated via scripts/regenerate_allowed_http_libs.py per
# Cycle-2 §12.8 RT-C2-06.
# ---------------------------------------------------------------------------

ALLOWED_HTTP_LIBS: Final[frozenset[str]] = frozenset({
    "urllib",
    "urllib.request",
    "urllib.parse",
    "urllib.error",
    "urllib.response",
})

# HTTP-class library prefixes that must appear in ALLOWED_HTTP_LIBS if
# imported. Anything matching one of these patterns AND not in the allowlist
# fires the .unknown_http_library_import sub-tag.
_KNOWN_HTTP_LIB_PREFIXES: Final[tuple[str, ...]] = (
    "http",
    "httpx",
    "requests",
    "aiohttp",
    "urllib3",
    "httpcore",
    "pycurl",
)


# ---------------------------------------------------------------------------
# Legacy CC-003 hook — pipeline.deprecated.* import ban.
# Preserved from the pre-§4-v2.x.5 rule so the §4 v2.x.5 LOCK does not
# regress that quarantine.
# ---------------------------------------------------------------------------

_DEPRECATED_IMPORT_PREFIX: Final[str] = "pipeline.deprecated"


# ---------------------------------------------------------------------------
# AST helpers.
# ---------------------------------------------------------------------------


def _path_is_allowlisted(path: Path) -> bool:
    """True iff ``path`` ends with one of the closed-set allowlisted suffixes."""
    posix = path.as_posix()
    return any(posix.endswith(suffix) for suffix in _ALLOWLISTED_FILE_SUFFIXES)


def _path_is_grandfathered(path: Path) -> bool:
    """True iff ``path`` is under an OD-4 grandfathered glob exclusion."""
    posix = "/" + path.as_posix()
    return any(marker in posix for marker in _GRANDFATHER_PATH_MARKERS)


def _collect_imports(tree: ast.AST) -> dict[str, str]:
    """Map every local name to its canonical module identity.

    Mirrors the R-ARCHIVIST-NO-CANONICAL-MUTATE._collect_imports shape:
    walks the whole tree (function-scoped imports too); one-way mapping
    local_name → canonical dotted path.
    """
    out: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                local = alias.asname or alias.name.split(".")[0]
                if alias.asname:
                    out[local] = alias.name
                else:
                    out[local] = local
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for alias in node.names:
                local = alias.asname or alias.name
                if mod:
                    out[local] = f"{mod}.{alias.name}"
                else:
                    out[local] = alias.name
    return out


def _resolve_callable_to_module_attr(
    func: ast.AST, imports: dict[str, str]
) -> tuple[str, str] | None:
    """Resolve a Call.func to a (module, attr) pair if possible.

    Two shapes handled:

    1. ``Attribute(Name)`` — ``module.func(...)``.
    2. ``Attribute(Attribute(Name))`` — ``module.sub.func(...)`` — common
       for ``urllib.request.urlopen``.
    3. Bare ``Name`` — handled via from-import rebind in imports table.
    """
    # Shape 1+2: Attribute chain rooted on a Name.
    if isinstance(func, ast.Attribute):
        # Walk the Attribute chain to its root Name.
        parts: list[str] = [func.attr]
        cur: ast.AST = func.value
        while isinstance(cur, ast.Attribute):
            parts.append(cur.attr)
            cur = cur.value
        if isinstance(cur, ast.Name):
            local = cur.id
            canonical_root = imports.get(local)
            if canonical_root is None:
                return None
            # Build the full dotted path; the rightmost element is the attr.
            # parts is [attr, ..., outermost_dot]; reverse to chain order.
            parts.reverse()
            attr = parts[-1]
            if len(parts) == 1:
                # `urllib.urlopen` — local was imported as urllib, attr=urlopen.
                mod = canonical_root
            else:
                # `urllib.request.urlopen` — chain through `request`.
                mod = ".".join([canonical_root, *parts[:-1]])
            return (mod, attr)
    # Shape 3: bare Name via from-import.
    if isinstance(func, ast.Name):
        canonical_full = imports.get(func.id)
        if canonical_full is None or "." not in canonical_full:
            return None
        mod, _, attr = canonical_full.rpartition(".")
        return (mod, attr)
    return None


def _is_http_class_lib(name: str) -> bool:
    """True iff `name` matches a known HTTP-class library prefix.

    Matches root or dotted-prefix: ``http`` or ``http.client`` or
    ``requests.sessions``. ``http.server`` does NOT match (server-side; not
    HTTP egress).
    """
    head = name.split(".")[0]
    if head == "http":
        # http.client is HTTP egress; http.server is not.
        return name == "http.client" or name.startswith("http.client.")
    return head in _KNOWN_HTTP_LIB_PREFIXES


def _check_forbidden_calls(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    """Emit a Violation for every Call to a forbidden HTTP primitive."""
    imports = _collect_imports(tree)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        resolved = _resolve_callable_to_module_attr(node.func, imports)
        if resolved is None:
            continue
        sub_tag = _FORBIDDEN_PRIMITIVES_INTERNAL.get(resolved)
        if sub_tag is None:
            continue
        mod, attr = resolved
        yield Violation(
            rule_name="R-NO-DIRECT-PROVIDER-HTTP",
            reason_tag=f"no_direct_provider_http.{sub_tag}",
            file=path,
            line=node.lineno,
            col=node.col_offset,
            message=(
                f"{_FAILURE_CODE}: {mod}.{attr}(...) is a forbidden HTTP "
                "primitive in seat-local / pipeline code. Use "
                "pipeline.orchestrator.provider_boundary.enforce_outbound_"
                "boundary(stdlib_urlopen_caller, ...) at subprocess wire-up "
                "instead. Per §4 v2.x.5 LOCKED 2026-05-16."
            ),
        )


def _check_unknown_http_library_imports(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    """RT-14 fold-in: flag any HTTP-class library import not in ALLOWED_HTTP_LIBS."""
    for node in ast.walk(tree):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names = [node.module]
        for name in names:
            if not _is_http_class_lib(name):
                continue
            # Accept ALLOWED_HTTP_LIBS exact-match or as a prefix
            # ("urllib.request" matches when "urllib.request" is allowed).
            if name in ALLOWED_HTTP_LIBS:
                continue
            if any(
                name == prefix or name.startswith(prefix + ".")
                for prefix in ALLOWED_HTTP_LIBS
            ):
                continue
            yield Violation(
                rule_name="R-NO-DIRECT-PROVIDER-HTTP",
                reason_tag="no_direct_provider_http.unknown_http_library_import",
                file=path,
                line=getattr(node, "lineno", 1),
                col=getattr(node, "col_offset", 0),
                message=(
                    f"{_FAILURE_CODE}: import of HTTP-class library {name!r} "
                    "outside ALLOWED_HTTP_LIBS closed set. Per §11.2 RT-14 "
                    "fold-in (Cycle 1) + §12.8 RT-C2-06 (Cycle 2) only the "
                    "stdlib urllib family is permitted; add to "
                    "ALLOWED_HTTP_LIBS via scripts/regenerate_allowed_http_libs.py "
                    "and operator approval."
                ),
            )


def _check_deprecated_imports(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    """CC-003 carry-forward — pipeline.deprecated.* import ban."""
    for node in ast.walk(tree):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names = [node.module]
        for name in names:
            if name == _DEPRECATED_IMPORT_PREFIX or name.startswith(
                _DEPRECATED_IMPORT_PREFIX + "."
            ):
                yield Violation(
                    rule_name="R-NO-DIRECT-PROVIDER-HTTP",
                    reason_tag="pipeline_deprecated_imported_from_runtime",
                    file=path,
                    line=getattr(node, "lineno", 1),
                    col=getattr(node, "col_offset", 0),
                    message=(
                        f"{_FAILURE_CODE}: Production modules must not import "
                        f"quarantined operator glue {name!r}. Move shared "
                        "behavior out of pipeline.deprecated."
                    ),
                )


# ---------------------------------------------------------------------------
# §4 v2.x.6 §11.1 — direct_provider_call_without_wrapper sub-tag.
# Fires on calls to `_call_anthropic` / `_call_openai_style` inside
# `pipeline/orchestrator/router.py` that omit the `http_post=` keyword
# argument. Static defense layer; the runtime assertion in router.py catches
# dynamic-call shapes the AST cannot see (getattr / importlib / re-export).
# ---------------------------------------------------------------------------

_WRAPPER_REQUIRED_FUNCTIONS: Final[frozenset[str]] = frozenset({
    "_call_anthropic",
    "_call_openai_style",
})

#: Sole production-code file in scope for the .direct_provider_call_without_wrapper
#: sub-tag. Test code is grandfathered via _GRANDFATHER_PATH_MARKERS / file scope.
_DIRECT_PROVIDER_CALL_SCOPE_SUFFIX: Final[str] = (
    "pipeline/orchestrator/router.py"
)


def _path_is_router(path: Path) -> bool:
    """True iff ``path`` is the production router module."""
    return path.as_posix().endswith(_DIRECT_PROVIDER_CALL_SCOPE_SUFFIX)


def _call_has_http_post_kwarg(node: ast.Call) -> bool:
    """True iff the Call node passes an `http_post=` keyword argument.

    Also accepts **kwargs unpacking (`**caller_kwargs`) as a permissive shape
    — defense-in-depth lives at the runtime assertion inside the called
    functions per §3 RT-06 fold-in.
    """
    for kw in node.keywords:
        if kw.arg == "http_post":
            return True
        if kw.arg is None:  # **kwargs unpacking
            return True
    return False


def _check_direct_provider_call_without_wrapper(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    """§4 v2.x.6 §11.1 — fires on _call_anthropic / _call_openai_style sans http_post=.

    Static-layer guard. Production scope is `pipeline/orchestrator/router.py`
    only; the runtime assertion at the body entry of these functions covers
    dynamic-call shapes that AST inspection cannot reach.
    """
    if not _path_is_router(path):
        return
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name):
            target = func.id
        elif isinstance(func, ast.Attribute):
            target = func.attr
        else:
            continue
        if target not in _WRAPPER_REQUIRED_FUNCTIONS:
            continue
        if _call_has_http_post_kwarg(node):
            continue
        yield Violation(
            rule_name="R-NO-DIRECT-PROVIDER-HTTP",
            reason_tag="no_direct_provider_http.direct_provider_call_without_wrapper",
            file=path,
            line=node.lineno,
            col=node.col_offset,
            message=(
                f"{_FAILURE_CODE}: call to {target}(...) at module scope must "
                "pass http_post=<OutboundCallable> (the F-CLASS wrapper). Bare "
                "calls bypass the outbound boundary; the runtime assertion in "
                "the function body fail-closes on http_post=None. Per §4 v2.x.6 "
                "LOCKED 2026-05-16T16:30:00Z §11.1 — OD-3 ratified."
            ),
        )


def _check_no_direct_provider_http(tree: ast.AST, path: Path) -> Iterator[Violation]:
    """Compose: allowlist/grandfather → forbidden calls + unknown libs + deprecated imports."""
    if _path_is_grandfathered(path):
        return
    # Allowlisted files may use forbidden primitives, but they STILL must not
    # import unknown HTTP libs (the closed-set discipline is universal).
    allowlisted = _path_is_allowlisted(path)
    if not allowlisted:
        yield from _check_forbidden_calls(tree, path)
    yield from _check_unknown_http_library_imports(tree, path)
    yield from _check_deprecated_imports(tree, path)
    yield from _check_direct_provider_call_without_wrapper(tree, path)


NO_DIRECT_PROVIDER_HTTP: Rule = Rule(
    name="R-NO-DIRECT-PROVIDER-HTTP",
    reason_tag="no_direct_provider_http",
    target_glob=_TARGET_GLOB,
    check=_check_no_direct_provider_http,
    description=(
        "Forbid direct HTTP primitive calls under pipeline/ outside the "
        "single allowlisted call site (pipeline/orchestrator/"
        "provider_boundary.py). Five sub-tags: .urlopen, .requests_lib, "
        ".httpx_lib, .aiohttp, .raw_socket — plus .unknown_http_library_"
        "import (RT-14 fold-in), .direct_provider_call_without_wrapper "
        "(§4 v2.x.6 §11.1 — RT-06 static layer on _call_anthropic / "
        "_call_openai_style sans http_post= kwarg), and a CC-003 carry-"
        "forward pipeline_deprecated_imported_from_runtime reason-tag for the "
        "pipeline.deprecated.* import ban. Lands at §4 v2.x.5 LOCKED "
        "2026-05-16; extended at §4 v2.x.6 LOCKED 2026-05-16T16:30:00Z; "
        "closes CC-007 sovereignty bypass at the AST-lint layer; "
        "ALLOWLISTED_FILES is a MappingProxyType frozen view per RT-14 "
        "closure precedent on R-ARCHIVIST-NO-CANONICAL-MUTATE."
    ),
)


__all__ = [
    "NO_DIRECT_PROVIDER_HTTP",
    "FORBIDDEN_PRIMITIVES",
    "ALLOWLISTED_FILES",
    "ALLOWED_HTTP_LIBS",
]
