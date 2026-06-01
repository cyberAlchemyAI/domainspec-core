"""Tests for R-NO-DIRECT-PROVIDER-HTTP — §4 v2.x.5 LOCKED 2026-05-16.

Companion test for the §4 v2.x.5 amendment: 5 sub-tags + RT-14 fold-in
``.unknown_http_library_import``; ALLOWLISTED_FILES collapsed per §11.6
DC-01 + RT-16 to ``{provider_boundary.py}``; CC-003 deprecated-import
carry-forward preserved.
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent
from types import MappingProxyType

from pipeline.linting.ast_lint import DEFAULT_RULES, lint_tree
from pipeline.linting.r_no_direct_provider_http import (
    ALLOWED_HTTP_LIBS,
    ALLOWLISTED_FILES,
    FORBIDDEN_PRIMITIVES,
    NO_DIRECT_PROVIDER_HTTP,
)


def _write(path: Path, source: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(source).lstrip("\n"), encoding="utf-8")
    return path


def test_rule_is_registered_in_default_rules() -> None:
    assert NO_DIRECT_PROVIDER_HTTP in DEFAULT_RULES


def test_forbidden_primitives_table_is_immutable() -> None:
    """RT-14 closure: MappingProxyType wrap prevents downstream mutation."""
    assert isinstance(FORBIDDEN_PRIMITIVES, MappingProxyType)
    try:
        FORBIDDEN_PRIMITIVES[("evil", "module")] = "evil_tag"  # type: ignore[index]
    except TypeError:
        return
    raise AssertionError("FORBIDDEN_PRIMITIVES allowed mutation (RT-14 closure breach)")


def test_allowlisted_files_is_collapsed_to_provider_boundary_only() -> None:
    """§11.6 DC-01 + RT-16 closure: ALLOWLISTED_FILES = {provider_boundary.py}."""
    keys = set(ALLOWLISTED_FILES.keys())
    assert keys == {"pipeline/orchestrator/provider_boundary.py"}


# ---------------------------------------------------------------------------
# Sub-tag matrix (5 + 1 RT-14 fold-in).
# ---------------------------------------------------------------------------


def test_urlopen_sub_tag_fires(tmp_path: Path) -> None:
    """.urlopen sub-tag: direct urllib.request.urlopen call."""
    _write(
        tmp_path / "pipeline" / "scout" / "bad_urlopen.py",
        """
        import urllib.request

        def fetch(url):
            with urllib.request.urlopen(url, timeout=10) as r:
                return r.read()
        """,
    )
    vs = lint_tree(tmp_path, [NO_DIRECT_PROVIDER_HTTP])
    sub_tags = {v.reason_tag for v in vs}
    assert "no_direct_provider_http.urlopen" in sub_tags


def test_requests_lib_sub_tag_fires(tmp_path: Path) -> None:
    """.requests_lib sub-tag: requests.post call."""
    _write(
        tmp_path / "pipeline" / "scout" / "bad_requests.py",
        """
        import requests

        def fetch(url, data):
            return requests.post(url, json=data)
        """,
    )
    vs = lint_tree(tmp_path, [NO_DIRECT_PROVIDER_HTTP])
    sub_tags = {v.reason_tag for v in vs}
    # requests.post fires .requests_lib; the import itself fires .unknown_http_library_import.
    assert "no_direct_provider_http.requests_lib" in sub_tags


def test_httpx_lib_sub_tag_fires(tmp_path: Path) -> None:
    """.httpx_lib sub-tag: httpx.post call."""
    _write(
        tmp_path / "pipeline" / "scout" / "bad_httpx.py",
        """
        import httpx

        def fetch(url, data):
            return httpx.post(url, json=data)
        """,
    )
    vs = lint_tree(tmp_path, [NO_DIRECT_PROVIDER_HTTP])
    sub_tags = {v.reason_tag for v in vs}
    assert "no_direct_provider_http.httpx_lib" in sub_tags


def test_aiohttp_sub_tag_fires(tmp_path: Path) -> None:
    """.aiohttp sub-tag: aiohttp.ClientSession call."""
    _write(
        tmp_path / "pipeline" / "scout" / "bad_aiohttp.py",
        """
        import aiohttp

        async def fetch(url):
            async with aiohttp.ClientSession() as s:
                return await s.get(url)
        """,
    )
    vs = lint_tree(tmp_path, [NO_DIRECT_PROVIDER_HTTP])
    sub_tags = {v.reason_tag for v in vs}
    assert "no_direct_provider_http.aiohttp" in sub_tags


def test_raw_socket_sub_tag_fires(tmp_path: Path) -> None:
    """.raw_socket sub-tag: http.client.HTTPSConnection call."""
    _write(
        tmp_path / "pipeline" / "scout" / "bad_http_client.py",
        """
        import http.client

        def fetch(host):
            conn = http.client.HTTPSConnection(host)
            conn.request("GET", "/")
            return conn.getresponse()
        """,
    )
    vs = lint_tree(tmp_path, [NO_DIRECT_PROVIDER_HTTP])
    sub_tags = {v.reason_tag for v in vs}
    assert "no_direct_provider_http.raw_socket" in sub_tags


def test_unknown_http_library_import_sub_tag_fires(tmp_path: Path) -> None:
    """RT-14 fold-in: bare `import httpx` fires .unknown_http_library_import."""
    _write(
        tmp_path / "pipeline" / "scout" / "imports_only.py",
        """
        import httpx
        # No call — just the import.
        """,
    )
    vs = lint_tree(tmp_path, [NO_DIRECT_PROVIDER_HTTP])
    sub_tags = {v.reason_tag for v in vs}
    assert "no_direct_provider_http.unknown_http_library_import" in sub_tags


# ---------------------------------------------------------------------------
# Allowlist + grandfather.
# ---------------------------------------------------------------------------


def test_provider_boundary_is_allowlisted(tmp_path: Path) -> None:
    """Forbidden-call inside provider_boundary.py is permitted."""
    _write(
        tmp_path / "pipeline" / "orchestrator" / "provider_boundary.py",
        """
        import urllib.request

        def caller(url):
            return urllib.request.urlopen(url, timeout=10)
        """,
    )
    vs = lint_tree(tmp_path, [NO_DIRECT_PROVIDER_HTTP])
    # Only allowlisted file → no Call-related violations should fire. The
    # ALLOWED_HTTP_LIBS check still runs but urllib.request is allowed.
    sub_tags = {v.reason_tag for v in vs}
    assert "no_direct_provider_http.urlopen" not in sub_tags


def test_validation_dispatcher_is_grandfathered(tmp_path: Path) -> None:
    """OD-4: pipeline/validation/** scripts are grandfathered out of scope."""
    _write(
        tmp_path / "pipeline" / "validation" / "old_round" / "dispatch.py",
        """
        import requests

        def fetch():
            return requests.post("https://api.groq.com/v1/chat", json={})
        """,
    )
    vs = lint_tree(tmp_path, [NO_DIRECT_PROVIDER_HTTP])
    assert vs == []


def test_engineering_scratch_is_grandfathered(tmp_path: Path) -> None:
    """OD-4: pipeline/engineering/_scratch/** is grandfathered."""
    _write(
        tmp_path / "pipeline" / "engineering" / "_scratch" / "probe.py",
        """
        import urllib.request

        def hit(url):
            return urllib.request.urlopen(url)
        """,
    )
    vs = lint_tree(tmp_path, [NO_DIRECT_PROVIDER_HTTP])
    assert vs == []


# ---------------------------------------------------------------------------
# CC-003 deprecated-import carry-forward.
# ---------------------------------------------------------------------------


def test_pipeline_deprecated_import_fires(tmp_path: Path) -> None:
    """CC-003 carry-forward — pipeline.deprecated.* imports remain banned."""
    _write(
        tmp_path / "pipeline" / "scout" / "uses_deprecated.py",
        """
        from pipeline.deprecated.operator_glue import scan_golden_quill
        """,
    )
    vs = lint_tree(tmp_path, [NO_DIRECT_PROVIDER_HTTP])
    sub_tags = {v.reason_tag for v in vs}
    assert "pipeline_deprecated_imported_from_runtime" in sub_tags


# ---------------------------------------------------------------------------
# Clean modules.
# ---------------------------------------------------------------------------


def test_clean_module_no_violations(tmp_path: Path) -> None:
    """A module with no forbidden primitives + only allowed imports passes."""
    _write(
        tmp_path / "pipeline" / "scout" / "clean.py",
        """
        import json
        import os
        from urllib.parse import urlencode

        def utility():
            return urlencode({"key": "value"})
        """,
    )
    assert lint_tree(tmp_path, [NO_DIRECT_PROVIDER_HTTP]) == []


def test_provider_domain_literal_alone_does_not_fire(tmp_path: Path) -> None:
    """String literal of a provider domain (no HTTP import or call) passes."""
    _write(
        tmp_path / "pipeline" / "docs_only.py",
        """
        ENDPOINT_DOC = "https://api.openai.com/v1/responses"
        """,
    )
    assert lint_tree(tmp_path, [NO_DIRECT_PROVIDER_HTTP]) == []


def test_allowed_http_libs_contains_only_stdlib_urllib_family() -> None:
    """v2.x.5 hard-codes urllib family only; third-party libs forbidden."""
    assert ALLOWED_HTTP_LIBS == frozenset({
        "urllib",
        "urllib.request",
        "urllib.parse",
        "urllib.error",
        "urllib.response",
    })


# ---------------------------------------------------------------------------
# §4 v2.x.6 §11.1 — direct_provider_call_without_wrapper sub-tag.
# Fires inside pipeline/orchestrator/router.py only; bare calls to
# _call_anthropic / _call_openai_style without an http_post= keyword arg
# are forbidden.
# ---------------------------------------------------------------------------


def test_direct_provider_call_without_wrapper_fires_in_router(tmp_path: Path) -> None:
    """Bare _call_anthropic(...) in router.py without http_post= keyword fires."""
    _write(
        tmp_path / "pipeline" / "orchestrator" / "router.py",
        """
        def offending():
            return _call_anthropic({}, {}, [], None)
        """,
    )
    vs = lint_tree(tmp_path, [NO_DIRECT_PROVIDER_HTTP])
    sub_tags = {v.reason_tag for v in vs}
    assert "no_direct_provider_http.direct_provider_call_without_wrapper" in sub_tags


def test_direct_provider_call_with_http_post_kwarg_passes(tmp_path: Path) -> None:
    """_call_anthropic(..., http_post=wrapper) in router.py is permitted."""
    _write(
        tmp_path / "pipeline" / "orchestrator" / "router.py",
        """
        def compliant(wrapper):
            return _call_anthropic({}, {}, [], None, http_post=wrapper)
        """,
    )
    vs = lint_tree(tmp_path, [NO_DIRECT_PROVIDER_HTTP])
    sub_tags = {v.reason_tag for v in vs}
    assert (
        "no_direct_provider_http.direct_provider_call_without_wrapper" not in sub_tags
    )


def test_direct_provider_call_outside_router_is_grandfathered(tmp_path: Path) -> None:
    """The sub-tag only fires in pipeline/orchestrator/router.py.

    Bare _call_anthropic(...) inside a test fixture or scratch script under
    other paths must NOT fire the new sub-tag (the runtime assertion in the
    router covers dynamic shapes; the static layer is narrow on purpose).
    """
    _write(
        tmp_path / "pipeline" / "scout" / "some_unrelated.py",
        """
        def thing():
            return _call_anthropic({}, {}, [], None)
        """,
    )
    vs = lint_tree(tmp_path, [NO_DIRECT_PROVIDER_HTTP])
    sub_tags = {v.reason_tag for v in vs}
    assert (
        "no_direct_provider_http.direct_provider_call_without_wrapper" not in sub_tags
    )


def test_direct_provider_call_with_kwargs_unpacking_passes(tmp_path: Path) -> None:
    """**kwargs unpacking is permissive — runtime guard catches None at body entry."""
    _write(
        tmp_path / "pipeline" / "orchestrator" / "router.py",
        """
        def forwarding(**caller_kwargs):
            return _call_openai_style({}, {}, [], None, **caller_kwargs)
        """,
    )
    vs = lint_tree(tmp_path, [NO_DIRECT_PROVIDER_HTTP])
    sub_tags = {v.reason_tag for v in vs}
    assert (
        "no_direct_provider_http.direct_provider_call_without_wrapper" not in sub_tags
    )
