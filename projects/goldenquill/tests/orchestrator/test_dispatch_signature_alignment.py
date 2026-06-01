"""§4 v2.x.6 §13.2 — RT-C2-02 fold-in. `_dispatch` signature contract.

Asserts that ``router._dispatch`` exposes ``http_post`` as a REQUIRED
keyword-only parameter. The runtime contract per the OD-3 ratified amendment:
no legacy direct-call branch, no ``Optional[None]`` default; every call site
inside ``pipeline/orchestrator/router.py`` must pass an ``http_post`` argument
constructed by ``_dispatch_with_classification_boundary`` (wrapper for cloud
providers, local-shim caller for local providers).
"""

from __future__ import annotations

import inspect

from pipeline.orchestrator.provider_boundary import OutboundCallable
from pipeline.orchestrator.router import _call_anthropic, _call_openai_style, _dispatch


def test_dispatch_has_keyword_only_required_http_post_parameter() -> None:
    """`_dispatch` must accept ``*, http_post`` as a keyword-only required arg."""
    sig = inspect.signature(_dispatch)
    params = sig.parameters
    assert "http_post" in params, (
        "_dispatch is missing the http_post parameter (RT-C2-02 contract)."
    )
    http_post = params["http_post"]
    assert http_post.kind is inspect.Parameter.KEYWORD_ONLY, (
        f"_dispatch.http_post must be keyword-only; got kind={http_post.kind}."
    )
    assert http_post.default is inspect.Parameter.empty, (
        "_dispatch.http_post must have no default (OD-3 ratified — required parameter)."
    )


def test_call_anthropic_has_keyword_only_required_http_post_parameter() -> None:
    """`_call_anthropic` must accept ``*, http_post`` as a keyword-only required arg."""
    sig = inspect.signature(_call_anthropic)
    http_post = sig.parameters.get("http_post")
    assert http_post is not None, "_call_anthropic missing http_post parameter."
    assert http_post.kind is inspect.Parameter.KEYWORD_ONLY
    assert http_post.default is inspect.Parameter.empty


def test_call_openai_style_has_keyword_only_required_http_post_parameter() -> None:
    """`_call_openai_style` must accept ``*, http_post`` as a keyword-only required arg."""
    sig = inspect.signature(_call_openai_style)
    http_post = sig.parameters.get("http_post")
    assert http_post is not None, "_call_openai_style missing http_post parameter."
    assert http_post.kind is inspect.Parameter.KEYWORD_ONLY
    assert http_post.default is inspect.Parameter.empty


def test_dispatch_http_post_annotation_is_outbound_callable() -> None:
    """`_dispatch.http_post` type annotation must be the OutboundCallable Protocol."""
    sig = inspect.signature(_dispatch)
    annotation = sig.parameters["http_post"].annotation
    # The annotation may be the OutboundCallable class itself (when imported
    # directly) or its qualified-name string (under `from __future__ import
    # annotations`). Accept either shape.
    assert annotation is OutboundCallable or annotation == "OutboundCallable", (
        f"_dispatch.http_post annotation should be OutboundCallable; got {annotation!r}."
    )
