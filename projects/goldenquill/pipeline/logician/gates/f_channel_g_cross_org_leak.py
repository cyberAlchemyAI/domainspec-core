"""F-CHANNEL-G-CROSS-ORG-LEAK — POST-extract gate (Law 3 isolation, P0).

Per architecture v7.0.5 §3 + §5.3 + companion `section_04_v7_0_5_companion.md`.
Funder Intelligence Database docs may carry `match_id` references whose
target org slug differs from the session-bound slug (e.g., a foundation
strategic plan published with anonymized prior-funded examples that
include match_id metadata). After Channel G extracts text, this gate
scans for any cross-org match_id pattern remaining and rejects the
extraction.

Encoding-evasion guard (v7.0.5 Cycle 2 Probe B closure): the gate runs
a deterministic decode-then-rescan cascade for known encodings (base-64,
hex, URL-encoding) BEFORE the regex pass. Any decoded payload that
surfaces a canonical match_id pattern triggers fail-closed identical to
raw matches.

Bypass: M13 (audited operator override; HIGH severity admin-risk entry).
"""

from __future__ import annotations

import base64
import binascii
import re
from dataclasses import dataclass
from typing import Final, Optional, Sequence
from urllib.parse import unquote


F_CHANNEL_G_CROSS_ORG_LEAK: Final[str] = "F-CHANNEL-G-CROSS-ORG-LEAK"

# Match DB ID pattern: literal "match_" + 32 hex chars. Case-insensitive.
_MATCH_ID_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"match_[a-f0-9]{32}", re.IGNORECASE
)

# Org slug reference pattern: `orgs/<slug>/match_database/...`. Captures the
# slug so the gate can compare against the session-bound slug.
_ORG_REF_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"orgs/([a-z0-9_]+)/match_database/", re.IGNORECASE
)


@dataclass(frozen=True, kw_only=True)
class ChannelGLeakResult:
    """Result of F-CHANNEL-G-CROSS-ORG-LEAK check."""

    success: bool
    failure_code: Optional[str]
    detail: str
    leaked_match_ids: tuple[str, ...] = ()
    leaked_org_slugs: tuple[str, ...] = ()


def _try_base64_decode(token: str) -> Optional[str]:
    """Best-effort base64 decode; returns decoded UTF-8 text or None."""
    if len(token) < 4 or len(token) % 4 != 0:
        return None
    try:
        decoded = base64.b64decode(token, validate=True)
        return decoded.decode("utf-8", errors="replace")
    except (binascii.Error, ValueError, UnicodeDecodeError):
        return None


def _try_hex_decode(token: str) -> Optional[str]:
    """Best-effort hex decode; returns decoded UTF-8 text or None."""
    if len(token) < 2 or len(token) % 2 != 0:
        return None
    try:
        decoded = bytes.fromhex(token)
        return decoded.decode("utf-8", errors="replace")
    except (ValueError, UnicodeDecodeError):
        return None


def _decode_rescan_cascade(text: str) -> str:
    """Run base-64 / hex / URL-encoding decoders and append to text.

    Returns the original text concatenated with any decoded payloads. The
    final regex pass scans the combined string. Decoders are best-effort
    and silently skip non-decodable tokens — this is a defense-in-depth
    cascade, not a parser.
    """
    chunks = [text]
    # URL-decode pass (idempotent on non-encoded chars)
    chunks.append(unquote(text))
    # Tokenize on whitespace + punctuation for per-token decode attempts
    tokens = re.findall(r"[A-Za-z0-9+/=]{8,}", text)
    for token in tokens:
        b64 = _try_base64_decode(token)
        if b64:
            chunks.append(b64)
        hex_decoded = _try_hex_decode(token)
        if hex_decoded:
            chunks.append(hex_decoded)
    return "\n".join(chunks)


def check_channel_g_cross_org_leak(
    *,
    extracted_text: str,
    session_slug: str,
) -> ChannelGLeakResult:
    """POST-extract gate: extracted text must not leak cross-org references.

    Parameters
    ----------
    extracted_text
        Text Channel G extracted from a Funder Intel doc, after the
        sanitization pre-pass per v7.0.5 §3.
    session_slug
        Org slug parsed from active PROJECT_CONTEXT.md at session start.

    Returns
    -------
    ChannelGLeakResult. Fails if any `match_*` ID OR any `orgs/<other>/match_database/`
    reference survives the decode-rescan cascade. Passes only when the
    combined raw + decoded text contains zero match-ID patterns AND zero
    cross-org references.
    """
    if not session_slug:
        return ChannelGLeakResult(
            success=False,
            failure_code=F_CHANNEL_G_CROSS_ORG_LEAK,
            detail="empty session_slug — cannot enforce Law 3",
        )

    combined = _decode_rescan_cascade(extracted_text)
    leaked_ids = tuple(sorted(set(_MATCH_ID_PATTERN.findall(combined))))
    org_refs = _ORG_REF_PATTERN.findall(combined)
    cross_org_slugs = tuple(
        sorted({slug for slug in org_refs if slug.lower() != session_slug.lower()})
    )

    if leaked_ids or cross_org_slugs:
        return ChannelGLeakResult(
            success=False,
            failure_code=F_CHANNEL_G_CROSS_ORG_LEAK,
            detail=(
                f"channel-G extract contains {len(leaked_ids)} match_id(s) "
                f"and {len(cross_org_slugs)} cross-org slug ref(s); "
                f"sanitization pre-pass failed to redact"
            ),
            leaked_match_ids=leaked_ids,
            leaked_org_slugs=cross_org_slugs,
        )
    return ChannelGLeakResult(
        success=True,
        failure_code=None,
        detail="no match_id or cross-org references in extracted text",
    )
