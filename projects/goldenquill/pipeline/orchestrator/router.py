#!/usr/bin/env python3
"""
Golden Quill / Tilth — Seat Router
----------------------------------
Single call_seat(seat_name, messages, system=None, classification_context=...)
interface over Anthropic / Groq / Ollama / any OpenAI-compatible endpoint.

Hardware tier is read from routing.yaml active_tier field.
No provider-specific logic leaks into seat scripts.

Usage (CLI):
    python3 router.py <seat_name> "your prompt"
    python3 router.py --check                    # ping every active seat
    python3 router.py --list                     # show active-tier routing

Usage (Python):
    from router import call_seat
    r = call_seat(
        "judge",
        [{"role":"user","content":"..."}],
        system="...",
        classification_context={
            "inputs": [{"field_path": "prompt", "class_name": "public"}],
        },
    )
    print(r["content"])
"""

from __future__ import annotations
import json
import os
import sys
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

try:
    from pipeline.logician.gates.f_class_outbound_boundary import (
        CLASS_CONFIDENTIAL,
        CLASS_OPERATOR_FLAGGED,
        CLASS_PUBLIC,
        CLASS_SHAREABLE,
        ClassifiedValue,
        F_CLASS_CLOUD_RECEIVED_CONFIDENTIAL,
        F_CLASS_CLOUD_RECEIVED_OPAQUE_SLOT_FILLED,
        F_CLASS_HIGH_STAKES_FLAG_LEAK,
        F_CLASS_SLOT_ID_NON_OPAQUE,
        SlotPosition,
        check_class_cloud_received_confidential,
        check_class_cloud_received_opaque_slot_filled,
        check_class_high_stakes_flag_leak,
        check_class_slot_id_non_opaque,
    )
    from pipeline.logician.gates.f_class_routing_indeterminate import (
        CallInput,
        F_CLASS_ROUTING_INDETERMINATE,
        check_class_routing_indeterminate,
    )
    from pipeline.logician.gates.f_class_register import (
        F_CLASS_REGISTER_SIGNATURE_INVALID,
    )
    from pipeline.orchestrator import deployment_posture, provider_boundary
    from pipeline.orchestrator.deployment_posture import (
        Posture,
        get_current_posture,
    )
    from pipeline.orchestrator.provider_boundary import (
        OutboundBoundaryRefusedError,
        OutboundCallable,
        enforce_outbound_boundary,
    )
    from pipeline.vault.classification.signed_register_loader import (
        load_signed_register,
    )
except ModuleNotFoundError:
    # Script execution from pipeline/orchestrator still needs absolute project imports.
    _repo_root = Path(__file__).resolve().parents[2]
    if str(_repo_root) not in sys.path:
        sys.path.insert(0, str(_repo_root))
    from pipeline.logician.gates.f_class_outbound_boundary import (
        CLASS_CONFIDENTIAL,
        CLASS_OPERATOR_FLAGGED,
        CLASS_PUBLIC,
        CLASS_SHAREABLE,
        ClassifiedValue,
        F_CLASS_CLOUD_RECEIVED_CONFIDENTIAL,
        F_CLASS_CLOUD_RECEIVED_OPAQUE_SLOT_FILLED,
        F_CLASS_HIGH_STAKES_FLAG_LEAK,
        F_CLASS_SLOT_ID_NON_OPAQUE,
        SlotPosition,
        check_class_cloud_received_confidential,
        check_class_cloud_received_opaque_slot_filled,
        check_class_high_stakes_flag_leak,
        check_class_slot_id_non_opaque,
    )
    from pipeline.logician.gates.f_class_routing_indeterminate import (
        CallInput,
        F_CLASS_ROUTING_INDETERMINATE,
        check_class_routing_indeterminate,
    )
    from pipeline.logician.gates.f_class_register import (
        F_CLASS_REGISTER_SIGNATURE_INVALID,
    )
    from pipeline.orchestrator import deployment_posture, provider_boundary
    from pipeline.orchestrator.deployment_posture import (
        Posture,
        get_current_posture,
    )
    from pipeline.orchestrator.provider_boundary import (
        OutboundBoundaryRefusedError,
        OutboundCallable,
        enforce_outbound_boundary,
    )
    from pipeline.vault.classification.signed_register_loader import (
        load_signed_register,
    )

ROUTING_PATH = Path(__file__).parent / "routing.yaml"
ENV_FILE = Path.home() / ".openclaw" / ".env"


# --------------------------------------------------------------------- YAML
# Avoid PyYAML dependency — minimal YAML subset parser for our config shape.
# Supports: dict nesting by indent, inline {k: v, ...} maps, strings/bools/ints/null/lists.
def _parse_yaml(text: str) -> dict:
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text)
    except ImportError:
        pass
    # Fallback: shell out to python3 -c using the json helper if available.
    # Last resort — use a tiny hand parser limited to our config.
    return _mini_yaml(text)


def _mini_yaml(text: str) -> Any:
    """Tiny YAML subset sufficient for routing.yaml. Raises if unsupported."""
    # Strip comments and blank lines first.
    lines = []
    for raw in text.splitlines():
        s = raw.rstrip()
        if not s.strip() or s.strip().startswith("#"):
            continue
        # strip inline comments only if not inside a string
        if "#" in s:
            in_str = False
            q = None
            cut = -1
            for i, c in enumerate(s):
                if c in ("'", '"'):
                    if not in_str:
                        in_str = True; q = c
                    elif q == c:
                        in_str = False; q = None
                elif c == "#" and not in_str:
                    cut = i; break
            if cut >= 0:
                s = s[:cut].rstrip()
        if s:
            lines.append(s)

    def indent(line: str) -> int:
        return len(line) - len(line.lstrip(" "))

    def scalar(v: str) -> Any:
        v = v.strip()
        if v.startswith('"') and v.endswith('"'):
            return v[1:-1]
        if v.startswith("'") and v.endswith("'"):
            return v[1:-1]
        if v.lower() in ("null", "~", ""):
            return None
        if v.lower() == "true":
            return True
        if v.lower() == "false":
            return False
        try:
            if "." in v:
                return float(v)
            return int(v)
        except ValueError:
            return v

    def parse_inline_map(s: str) -> dict:
        # {k: v, k2: v2}
        assert s.startswith("{") and s.endswith("}")
        body = s[1:-1].strip()
        if not body:
            return {}
        out = {}
        depth = 0
        buf = ""
        parts = []
        in_str = False; q = None
        for c in body:
            if c in ("'", '"'):
                if not in_str:
                    in_str = True; q = c
                elif q == c:
                    in_str = False; q = None
                buf += c
            elif c == "{" and not in_str:
                depth += 1; buf += c
            elif c == "}" and not in_str:
                depth -= 1; buf += c
            elif c == "," and depth == 0 and not in_str:
                parts.append(buf); buf = ""
            else:
                buf += c
        if buf.strip():
            parts.append(buf)
        for p in parts:
            if ":" not in p:
                continue
            k, v = p.split(":", 1)
            out[k.strip()] = scalar(v.strip())
        return out

    def parse_block(idx: int, parent_indent: int) -> tuple[Any, int]:
        if idx >= len(lines):
            return None, idx
        first = lines[idx]
        first_indent = indent(first)
        stripped = first.lstrip()
        # list?
        if stripped.startswith("- "):
            lst = []
            while idx < len(lines) and indent(lines[idx]) == first_indent and lines[idx].lstrip().startswith("- "):
                item_line = lines[idx].lstrip()[2:]
                if item_line.strip().startswith("{"):
                    lst.append(parse_inline_map(item_line.strip()))
                    idx += 1
                elif ":" in item_line:
                    # inline key in list element
                    # Re-insert the key as a dict at this indent + 2
                    # Build child dict from this and continuing lines
                    synthetic = " " * (first_indent + 2) + item_line
                    old = lines[idx]
                    lines[idx] = synthetic
                    val, idx = parse_block(idx, first_indent)
                    lines[idx-1] = old  # restore (not strictly needed)
                    lst.append(val)
                else:
                    lst.append(scalar(item_line))
                    idx += 1
            return lst, idx
        # dict
        result: dict[str, Any] = {}
        while idx < len(lines):
            line = lines[idx]
            cur_indent = indent(line)
            if cur_indent < first_indent:
                break
            if cur_indent > first_indent:
                # shouldn't happen if called correctly
                idx += 1
                continue
            content = line.lstrip()
            if ":" not in content:
                break
            key, _, rest = content.partition(":")
            key = key.strip()
            rest = rest.strip()
            if rest == "":
                # nested block follows at greater indent
                idx += 1
                if idx < len(lines) and indent(lines[idx]) > first_indent:
                    val, idx = parse_block(idx, first_indent)
                    result[key] = val
                else:
                    result[key] = None
            elif rest.startswith("{") and rest.endswith("}"):
                result[key] = parse_inline_map(rest)
                idx += 1
            elif rest.startswith("[") and rest.endswith("]"):
                body = rest[1:-1]
                result[key] = [scalar(x) for x in body.split(",")] if body.strip() else []
                idx += 1
            else:
                result[key] = scalar(rest)
                idx += 1
        return result, idx

    root, _ = parse_block(0, -1)
    return root


# --------------------------------------------------------------------- config
def load_config() -> dict:
    return _parse_yaml(ROUTING_PATH.read_text())


def get_seat_config(seat_name: str, tier: str | None = None) -> dict:
    cfg = load_config()
    tier = tier or cfg["active_tier"]
    if seat_name not in cfg["seats"]:
        raise KeyError(f"seat '{seat_name}' not in routing.yaml")
    seat = cfg["seats"][seat_name]
    tier_cfg = seat.get(tier)
    if not tier_cfg:
        raise KeyError(f"seat '{seat_name}' has no config for tier '{tier}'")
    return {
        "provider": tier_cfg["provider"],
        "model": tier_cfg["model"],
        "family": tier_cfg["family"],
        "via_openclaw": tier_cfg.get("via_openclaw", False),
        "temperature": seat.get("temperature", 0.3),
        "max_tokens": seat.get("max_tokens", 4000),
        "fallback": seat.get("fallback"),
        "role": seat.get("role"),
    }


# --------------------------------------------------------------------- keys
# BYOK key lifecycle is owned by `keyring_loader` (SYN-4 fix, 2026-04-15):
#   1. OS keyring (macOS Keychain / Secret Service) — preferred
#   2. Legacy ~/.openclaw/.env — deprecated, logs a warning on read
#   3. os.environ — only for explicitly allowlisted names
# Keys are loaded per call. Never cached in this process.
def load_api_key(env_name: str | None) -> str | None:
    if not env_name:
        return None
    # Allow providers that declare `api_key_env: null` (e.g. local ollama)
    # to pass through as no-op.
    if env_name.lower() in ("null", "none", ""):
        return None
    # Lazy import keeps the router importable even if keyring_loader moves.
    _here = Path(__file__).parent
    if str(_here) not in sys.path:
        sys.path.insert(0, str(_here))
    try:
        from keyring_loader import get_key  # type: ignore
    except ImportError as e:
        raise RuntimeError(
            f"keyring_loader unavailable ({e}); cannot load {env_name}"
        ) from e
    try:
        return get_key(env_name)
    except KeyError as e:
        raise RuntimeError(str(e)) from e


# --------------------------------------------------------------------- call
class SeatCallError(RuntimeError):
    def __init__(self, provider: str, status: int | None, body: str):
        self.provider = provider
        self.status = status
        self.body = body
        super().__init__(f"{provider} error {status}: {body[:200]}")


USER_AGENT = "TilthCouncil/0.1 (Golden Quill; +https://yourgoldenquill.com)"


class ClassificationBoundaryError(RuntimeError):
    """Raised when a model call would violate v7.0.7 classification routing."""

    def __init__(self, failure_code: str, detail: str):
        self.failure_code = failure_code
        self.detail = detail
        super().__init__(f"{failure_code}: {detail}")


@dataclass(frozen=True, kw_only=True)
class ClassificationContext:
    """Per-call proof that cloud routing is allowed for the exact payload."""

    inputs: tuple[CallInput, ...]
    classified_values: tuple[ClassifiedValue, ...] = field(default_factory=tuple)
    slot_positions: tuple[SlotPosition, ...] = field(default_factory=tuple)
    high_stakes_flag_values: tuple[str, ...] = field(default_factory=tuple)
    post_fill_draft: bool = False


_CLOUD_PROVIDERS = frozenset({"anthropic", "groq", "openai", "google"})
_LOCAL_PROVIDERS = frozenset({"ollama"})
_BLOCKING_CLASSES = frozenset({CLASS_CONFIDENTIAL, CLASS_OPERATOR_FLAGGED})


def public_classification_context(field_path: str = "prompt") -> ClassificationContext:
    """Convenience for explicitly public/shareable cloud-safe calls."""
    return ClassificationContext(
        inputs=(CallInput(field_path=field_path, class_name=CLASS_PUBLIC),)
    )


def _coerce_call_inputs(raw_inputs: Sequence[Any]) -> tuple[CallInput, ...]:
    out: list[CallInput] = []
    for item in raw_inputs:
        if isinstance(item, CallInput):
            out.append(item)
        elif isinstance(item, Mapping):
            out.append(
                CallInput(
                    field_path=str(item.get("field_path", "")),
                    class_name=str(item.get("class_name", "")),
                    locked_by=str(item.get("locked_by", "")),
                )
            )
        else:
            raise TypeError(f"unsupported classification input: {type(item).__name__}")
    return tuple(out)


def _coerce_classified_values(raw_values: Sequence[Any]) -> tuple[ClassifiedValue, ...]:
    out: list[ClassifiedValue] = []
    for item in raw_values:
        if isinstance(item, ClassifiedValue):
            out.append(item)
        elif isinstance(item, Mapping):
            out.append(
                ClassifiedValue(
                    value=str(item.get("value", "")),
                    class_name=str(item.get("class_name", "")),
                    field_path=str(item.get("field_path", "")),
                )
            )
        else:
            raise TypeError(f"unsupported classified value: {type(item).__name__}")
    return tuple(out)


def _coerce_slot_positions(raw_slots: Sequence[Any]) -> tuple[SlotPosition, ...]:
    out: list[SlotPosition] = []
    for item in raw_slots:
        if isinstance(item, SlotPosition):
            out.append(item)
        elif isinstance(item, Mapping):
            out.append(
                SlotPosition(
                    slot_id=str(item.get("slot_id", "")),
                    pre_marker=str(item.get("pre_marker", "")),
                    post_marker=str(item.get("post_marker", "")),
                )
            )
        else:
            raise TypeError(f"unsupported slot position: {type(item).__name__}")
    return tuple(out)


def _coerce_classification_context(
    classification_context: ClassificationContext | Mapping[str, Any] | None,
) -> ClassificationContext | None:
    if classification_context is None:
        return None
    if isinstance(classification_context, ClassificationContext):
        return classification_context
    if not isinstance(classification_context, Mapping):
        raise TypeError(
            "classification_context must be ClassificationContext, mapping, or None"
        )
    return ClassificationContext(
        inputs=_coerce_call_inputs(classification_context.get("inputs", ())),
        classified_values=_coerce_classified_values(
            classification_context.get("classified_values", ())
        ),
        slot_positions=_coerce_slot_positions(
            classification_context.get("slot_positions", ())
        ),
        high_stakes_flag_values=tuple(
            str(v) for v in classification_context.get("high_stakes_flag_values", ())
        ),
        post_fill_draft=bool(classification_context.get("post_fill_draft", False)),
    )


def _message_text(messages: list[dict], system: str | None) -> str:
    parts: list[str] = []
    if system:
        parts.append(system)
    for msg in messages:
        content = msg.get("content")
        if isinstance(content, str):
            parts.append(content)
        else:
            parts.append(json.dumps(content, ensure_ascii=False, sort_keys=True))
    return "\n".join(parts)


def _is_cloud_provider(provider_name: str, provider_cfg: dict) -> bool:
    if provider_name in _CLOUD_PROVIDERS:
        return True
    if provider_name in _LOCAL_PROVIDERS:
        return False
    endpoint = str(provider_cfg.get("endpoint", ""))
    return endpoint.startswith("https://") and "localhost" not in endpoint


def _raise_if_failed(result: Any) -> None:
    if not result.success:
        raise ClassificationBoundaryError(result.failure_code or "F-CLASS", result.detail)


# §4 v2.x.6 OD-5 full router dedup (LOCKED 2026-05-16T16:30:00Z row 234).
# Single-source-of-truth router-layer adapter constructs `enforce_outbound_boundary`
# per dispatch. The wrapper is the SOLE site where F-CLASS PRE/POST gates fire
# on the router-level cloud dispatch path (closes RT-17 from §4 v2.x.5 Cycle 1).


def _coerce_to_provider_boundary_context(
    rc: ClassificationContext,
) -> provider_boundary.ClassificationContext:
    """Map router's ClassificationContext to the wrapper's ClassificationContext.

    OD-1 ratified: keep two ClassificationContext types decoupled. Both share
    the underlying CallInput / ClassifiedValue / SlotPosition types (re-exported
    from f_class_*), so fields pass straight through. The wrapper's extra
    `cycle_id` and `payload_sha3_512_commitment` fields default to empty
    strings — the wrapper skips its sha3 commitment check on empty input.
    """
    return provider_boundary.ClassificationContext(
        inputs=tuple(rc.inputs),
        classified_values=tuple(rc.classified_values),
        slot_positions=tuple(rc.slot_positions),
        high_stakes_flag_values=tuple(rc.high_stakes_flag_values),
        post_fill_draft=rc.post_fill_draft,
    )


def _load_router_posture_and_register() -> tuple[Posture, Mapping[str, Any] | None]:
    """Load deployment posture + Ed25519-verified signed register.

    Per §6 + §13.3 (RT-04 + RT-C2-03 fold-ins):

    - Under `local_only_sovereign` (the default; cloud egress is structurally
      absent), skip the register load entirely. The wrapper refuses cloud
      egress before any register-dependent check fires, so an absent register
      under this posture is correct and expected in test/dev environments.
    - Under `frontier_eligible` or `split_context_hybrid`, the signed register
      is required: loader success returns (posture, register); any loader
      exception (file missing, parse failure, signature invalid, …) collapses
      to fail-closed `ClassificationBoundaryError(F_CLASS_REGISTER_SIGNATURE_INVALID)`.
    """
    posture = get_current_posture()
    if posture == "local_only_sovereign":
        return posture, None
    try:
        register = load_signed_register()
    except Exception as exc:
        raise ClassificationBoundaryError(
            F_CLASS_REGISTER_SIGNATURE_INVALID,
            f"signed classification register load failed under posture={posture}: "
            f"{type(exc).__name__}: {str(exc)[:200]}. Fail-closed per RT-04 + RT-C2-03.",
        ) from exc
    if register is None:
        raise ClassificationBoundaryError(
            F_CLASS_REGISTER_SIGNATURE_INVALID,
            f"signed classification register absent under posture={posture}; "
            f"non-test deployments require an operator-signed register loaded "
            f"at process startup. Fail-closed per RT-04.",
        )
    return posture, register


def _local_provider_caller(
    *,
    url: str,
    headers: Mapping[str, str],
    body: bytes,
    timeout_seconds: float,
) -> tuple[int, bytes]:
    """Local-provider HTTP shim — no F-CLASS gates.

    Local providers (ollama, vLLM) are explicitly out of scope for cloud-
    egress F-CLASS gates per v7.0.10 §1. The wrapper would refuse them under
    `local_only_sovereign` posture. This shim delegates to the canonical
    `stdlib_urlopen_caller` (sole permitted urlopen site under
    R-NO-DIRECT-PROVIDER-HTTP allowlist) with the `_INSIDE_WRAPPER` flag set
    so the direct-call guard does not fire.
    """
    provider_boundary._INSIDE_WRAPPER.active = True
    try:
        return provider_boundary._CANONICAL_STDLIB_URLOPEN_CALLER(
            url=url,
            headers=headers,
            body=body,
            timeout_seconds=timeout_seconds,
        )
    finally:
        provider_boundary._INSIDE_WRAPPER.active = False


def _dispatch_with_classification_boundary(
    *,
    provider_name: str,
    provider_cfg: dict,
    seat_cfg: dict,
    messages: list[dict],
    system: str | None,
    classification_context: ClassificationContext | None,
) -> dict:
    """Per §2 v2.x.6 canonical body.

    Constructs the OutboundCallable wrapper once per dispatch and threads it
    down to `_call_anthropic` / `_call_openai_style` via `http_post`. The
    wrapper composes the F-CLASS PRE chain (routing-indeterminate, slot-id,
    confidential-input, high-stakes-flag-leak, raw-bytes register scan) and
    POST chain (confidential drift, opaque-slot drift, high-stakes flag leak
    in response). Translates `OutboundBoundaryRefusedError` ↔
    `ClassificationBoundaryError` per §4 so the existing public exception
    contract is preserved.
    """
    if not _is_cloud_provider(provider_name, provider_cfg):
        # Local providers do not need the wrapper; the canonical stdlib shim
        # handles the direct-call thread-local flag. F-CLASS gates are
        # out-of-scope for local egress per v7.0.10 §1.
        return _dispatch(provider_cfg, seat_cfg, messages, system, http_post=_local_provider_caller)

    if classification_context is None:
        # Cloud provider + no classification_context → fail-closed per v7.0.7
        # §4 (same predicate as F-CLASS-ROUTING-INDETERMINATE). The wrapper
        # would also raise here; raising at the router layer keeps the
        # existing public-surface exception contract identical to
        # pre-amendment behavior.
        raise ClassificationBoundaryError(
            F_CLASS_ROUTING_INDETERMINATE,
            "cloud provider requested without classification_context; fail-closed "
            "LOCAL per v7.0.7",
        )

    # v7.0.7 post-fill-draft sovereignty rule. The wrapper PRE chain does not
    # currently inspect post_fill_draft (provider_boundary.py is LOCKed at §4
    # v2.x.5); preserving the check at the router layer closes the gap until
    # a future v2.x.y amendment lifts post_fill_draft enforcement into the
    # wrapper. The fail-closed return shape matches the legacy router behavior.
    if classification_context.post_fill_draft:
        raise ClassificationBoundaryError(
            F_CLASS_CLOUD_RECEIVED_CONFIDENTIAL,
            "post-fill draft requested a cloud provider; v7.0.7 requires all "
            "downstream seats reading post-fill drafts to route local-only",
        )

    posture, signed_register = _load_router_posture_and_register()
    register_posture = (
        deployment_posture.load_posture_from_signed_register(
            signed_register=dict(signed_register)
        )
        if signed_register is not None
        else None
    )
    pb_classification_context = _coerce_to_provider_boundary_context(
        classification_context
    )
    wrapped_caller = enforce_outbound_boundary(
        provider_boundary._CANONICAL_STDLIB_URLOPEN_CALLER,
        classification_context=pb_classification_context,
        posture=posture,
        operator_signed_register=signed_register,
        register_posture=register_posture,
    )

    try:
        return _dispatch(provider_cfg, seat_cfg, messages, system, http_post=wrapped_caller)
    except OutboundBoundaryRefusedError as exc:
        # Narrow translation per Cycle-1 RT-02 fold-in. Other wrapper-origin
        # exceptions (transport / timeout / runtime integrity) are NOT
        # translated to ClassificationBoundaryError — they propagate as-is and
        # are caught by call_seat's generic `except Exception as primary_err`
        # handler below. Semantic two-bucket dichotomy preserved:
        # ClassificationBoundaryError = fail-closed-by-policy (audited,
        # fallback eligible); transport/timeout = transient failure.
        raise ClassificationBoundaryError(exc.failure_code, exc.detail) from exc


def _call_openai_style(
    provider_cfg: dict,
    seat_cfg: dict,
    messages: list,
    system: str | None,
    *,
    http_post: OutboundCallable,
) -> dict:
    # RT-06 fold-in — runtime defense against dynamic-call bypass. Static
    # AST-lint catches the `_call_openai_style(...)` shape; this guard catches
    # `getattr(router, '_call_openai_style')(...)` /
    # `importlib.import_module(...).module._call_openai_style(...)` shapes
    # that the lint rule cannot detect statically.
    if http_post is None:
        raise ClassificationBoundaryError(
            F_CLASS_CLOUD_RECEIVED_CONFIDENTIAL,
            "_call_openai_style invoked without http_post wrapper (direct-call "
            "bypass detected at runtime); fail-closed per OD-3 + RT-06.",
        )
    url = provider_cfg["endpoint"]
    payload: dict[str, Any] = {
        "model": seat_cfg["model"],
        "messages": ([{"role": "system", "content": system}] if system else []) + messages,
        "temperature": seat_cfg.get("temperature", 0.3),
        "max_tokens": seat_cfg.get("max_tokens", 4000),
    }
    headers: dict[str, str] = {"Content-Type": "application/json", "User-Agent": USER_AGENT}
    if provider_cfg.get("api_key_env"):
        key = load_api_key(provider_cfg["api_key_env"])
        if provider_cfg.get("auth_header_style") == "bearer":
            headers["Authorization"] = f"Bearer {key}"
        else:
            headers[provider_cfg.get("auth_header_name", "Authorization")] = key
    # RT-07 fold-in — pin canonical JSON encoder settings so the wrapper PRE-scan
    # operates on byte-equivalent input to what gets POST'd.
    body_bytes = json.dumps(
        payload, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    status, response_bytes = http_post(
        url=url,
        headers=headers,
        body=body_bytes,
        timeout_seconds=120.0,
    )
    response_text = response_bytes.decode("utf-8", errors="replace")
    if status >= 400:
        raise SeatCallError(url, status, response_text)
    data = json.loads(response_text)
    content = data["choices"][0]["message"]["content"]
    return {
        "content": content,
        "model": seat_cfg["model"],
        "family": seat_cfg["family"],
        "usage": data.get("usage"),
        "raw": data,
    }


def _call_anthropic(
    provider_cfg: dict,
    seat_cfg: dict,
    messages: list,
    system: str | None,
    *,
    http_post: OutboundCallable,
) -> dict:
    if http_post is None:
        raise ClassificationBoundaryError(
            F_CLASS_CLOUD_RECEIVED_CONFIDENTIAL,
            "_call_anthropic invoked without http_post wrapper (direct-call "
            "bypass detected at runtime); fail-closed per OD-3 + RT-06.",
        )
    key = load_api_key(provider_cfg["api_key_env"])
    url = provider_cfg["endpoint"]
    payload: dict[str, Any] = {
        "model": seat_cfg["model"],
        "messages": messages,
        "temperature": seat_cfg.get("temperature", 0.3),
        "max_tokens": seat_cfg.get("max_tokens", 4000),
    }
    if system:
        payload["system"] = system
    headers: dict[str, str] = {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
    }
    body_bytes = json.dumps(
        payload, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    status, response_bytes = http_post(
        url=url,
        headers=headers,
        body=body_bytes,
        timeout_seconds=120.0,
    )
    response_text = response_bytes.decode("utf-8", errors="replace")
    if status >= 400:
        raise SeatCallError(url, status, response_text)
    data = json.loads(response_text)
    parts = data.get("content", [])
    text = "".join(p.get("text", "") for p in parts if p.get("type") == "text")
    return {
        "content": text,
        "model": seat_cfg["model"],
        "family": seat_cfg["family"],
        "usage": data.get("usage"),
        "raw": data,
    }


def _dispatch(
    provider_cfg: dict,
    seat_cfg: dict,
    messages: list,
    system: str | None,
    *,
    http_post: OutboundCallable,
) -> dict:
    """Wire-style dispatch. `http_post` is required per §13.2 (RT-C2-02 fold-in)
    — the caller (`_dispatch_with_classification_boundary`) constructs either
    the F-CLASS-wrapped caller for cloud providers or a local-provider shim.
    """
    style = provider_cfg.get("wire_style")
    if style == "openai_chat":
        return _call_openai_style(
            provider_cfg, seat_cfg, messages, system, http_post=http_post
        )
    if style == "anthropic_messages":
        return _call_anthropic(
            provider_cfg, seat_cfg, messages, system, http_post=http_post
        )
    raise ValueError(f"unknown wire_style: {style}")


def call_seat(
    seat_name: str,
    messages: list[dict],
    system: str | None = None,
    tier: str | None = None,
    classification_context: ClassificationContext | Mapping[str, Any] | None = None,
) -> dict:
    """
    Call a seat. Returns dict with keys: content, model, family, usage, raw.
    Cloud providers require classification_context. Missing, indeterminate,
    confidential/operator_flagged, post-fill, semantic slot, or high-stakes
    leakage fails closed before network dispatch.
    """
    cfg = load_config()
    sc = get_seat_config(seat_name, tier=tier)
    class_ctx = _coerce_classification_context(classification_context)
    if sc["via_openclaw"]:
        raise RuntimeError(
            f"seat '{seat_name}' is marked via_openclaw=true — call through OpenClaw, not router."
        )
    provider_cfg = cfg["providers"][sc["provider"]]
    try:
        return _dispatch_with_classification_boundary(
            provider_name=sc["provider"],
            provider_cfg=provider_cfg,
            seat_cfg=sc,
            messages=messages,
            system=system,
            classification_context=class_ctx,
        )
    except ClassificationBoundaryError:
        fb = sc.get("fallback")
        if not fb:
            raise
        fb_provider_cfg = cfg["providers"][fb["provider"]]
        if _is_cloud_provider(fb["provider"], fb_provider_cfg):
            raise
        sys.stderr.write(
            f"[router] {seat_name} primary blocked by classification boundary; "
            "trying local fallback\n"
        )
        fb_sc = {
            **sc,
            "provider": fb["provider"],
            "model": fb["model"],
            "family": fb["family"],
        }
        return _dispatch_with_classification_boundary(
            provider_name=fb["provider"],
            provider_cfg=fb_provider_cfg,
            seat_cfg=fb_sc,
            messages=messages,
            system=system,
            classification_context=class_ctx,
        )
    except Exception as primary_err:
        fb = sc.get("fallback")
        if not fb:
            raise
        sys.stderr.write(f"[router] {seat_name} primary failed ({primary_err}); trying fallback\n")
        fb_provider = cfg["providers"][fb["provider"]]
        fb_sc = {
            **sc,
            "provider": fb["provider"],
            "model": fb["model"],
            "family": fb["family"],
        }
        return _dispatch_with_classification_boundary(
            provider_name=fb["provider"],
            provider_cfg=fb_provider,
            seat_cfg=fb_sc,
            messages=messages,
            system=system,
            classification_context=class_ctx,
        )


# --------------------------------------------------------------------- CLI
def _cli_list() -> None:
    cfg = load_config()
    tier = cfg["active_tier"]
    print(f"Active tier: {tier}\n")
    print(f"{'seat':<12} {'provider':<10} {'family':<12} model")
    print("-" * 70)
    for seat, spec in cfg["seats"].items():
        if "implementation" in spec:
            print(f"{seat:<12} {'(python)':<10} {'-':<12} {spec.get('path','deterministic')}")
            continue
        t = spec.get(tier) or {}
        print(f"{seat:<12} {t.get('provider',''):<10} {t.get('family',''):<12} {t.get('model','')}")


def _cli_check() -> None:
    cfg = load_config()
    tier = cfg["active_tier"]
    print(f"Pinging all seats on tier {tier}...\n")
    for seat_name, spec in cfg["seats"].items():
        if "implementation" in spec:
            print(f"  {seat_name:<12} [python deterministic] OK")
            continue
        if spec.get(tier, {}).get("via_openclaw"):
            print(f"  {seat_name:<12} [via OpenClaw — skip direct ping]")
            continue
        t0 = time.time()
        try:
            r = call_seat(
                seat_name,
                [{"role": "user", "content": "Reply with just: pong"}],
                classification_context=public_classification_context("router.check"),
            )
            dt = time.time() - t0
            reply = (r["content"] or "").strip()[:40]
            print(f"  {seat_name:<12} [{r['family']}/{r['model']}] {dt:.1f}s → {reply!r}")
        except Exception as e:
            print(f"  {seat_name:<12} FAILED: {e}")


def _cli_main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "--list":
        _cli_list()
        return 0
    if argv[0] == "--check":
        _cli_check()
        return 0
    seat = argv[0]
    prompt = " ".join(argv[1:]) or "ping"
    r = call_seat(
        seat,
        [{"role": "user", "content": prompt}],
        classification_context=public_classification_context("router.cli_prompt"),
    )
    print(f"[{r['family']}/{r['model']}]")
    print(r["content"])
    return 0


if __name__ == "__main__":
    sys.exit(_cli_main(sys.argv[1:]))
