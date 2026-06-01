"""F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND — consolidated PRE/POST/PRE-write gate.

Per §13 Data Collector v1 LOCKED 2026-05-10 §13.9.4 with Cycle-1 + Cycle-2
sub-tag expansions per RT-08, RT-09, RT-10, RT-11, RT-12, RT-14, RT-21,
RT-23, RT-26, RT-C2-01, RT-C2-03, RT-C2-05, RT-C2-06, RT-C2-12.

This is the broad-strokes "any code path that could expose data outside the
per-org consent-bounded recipient set" envelope. It exposes one branch
function per sub-tag plus a consolidated convenience runner.

Sub-tags shipped at v1 LOCK:

* ``.semantic_slot_in_outbound``
* ``.path_cross_org`` / ``.symlink_escape``
* ``.mtproto_cross_org`` / ``.cross_org_chat_id_collision``
* ``.mtproto_session_path_unbound``
* ``.telegram_group_chat_rejected``
* ``.sms_size_overflow``
* ``.whatsapp_template_unapproved``
* ``.state_card_signature_invalid``
* ``.batch_hash_mismatch`` / ``.per_recipient_signature_invalid`` /
  ``.per_recipient_signature_grant_or_org_mismatch`` /
  ``.batch_recipient_order_swap``
* ``.token_invalid_inbound`` / ``.aead_tag_invalid`` /
  ``.revoked_token_replay`` / ``.channel_binding_mismatch`` /
  ``.token_id_collision_detected``
* ``.cedar_engine_unready``
* ``.env_var_auto_confirm_set``
* ``.send_lock_hold_timeout``
* ``.orgscoped_bot_subclassing_forbidden``
* ``.config_signature_invalid``

Each branch is a small pure function — predicates take dataclass /
Mapping / bytes inputs and return ``PiiLeakResult`` instances. The seat
module composes branches at the relevant lifecycle points; the gate
package neither reads files nor performs crypto directly.
"""

from __future__ import annotations

import hmac
import re
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Final, Mapping, Optional, Sequence

F_DATACOLLECTOR_PII_LEAK_IN_OUTBOUND: Final[str] = (
    "F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND"
)

PERMITTED_CHANNELS: Final[frozenset[str]] = frozenset({
    "email",
    "sms",
    "voice",
    "telegram",
    "whatsapp",
})

# Sub-tag inventory (canonical at v1 LOCK).
SUB_TAG_SEMANTIC_SLOT_IN_OUTBOUND: Final[str] = ".semantic_slot_in_outbound"
SUB_TAG_PATH_CROSS_ORG: Final[str] = ".path_cross_org"
SUB_TAG_SYMLINK_ESCAPE: Final[str] = ".symlink_escape"
SUB_TAG_MTPROTO_CROSS_ORG: Final[str] = ".mtproto_cross_org"
SUB_TAG_CROSS_ORG_CHAT_ID_COLLISION: Final[str] = ".cross_org_chat_id_collision"
SUB_TAG_MTPROTO_SESSION_PATH_UNBOUND: Final[str] = ".mtproto_session_path_unbound"
SUB_TAG_TELEGRAM_GROUP_CHAT_REJECTED: Final[str] = ".telegram_group_chat_rejected"
SUB_TAG_SMS_SIZE_OVERFLOW: Final[str] = ".sms_size_overflow"
SUB_TAG_WHATSAPP_TEMPLATE_UNAPPROVED: Final[str] = ".whatsapp_template_unapproved"
SUB_TAG_STATE_CARD_SIGNATURE_INVALID: Final[str] = (
    ".state_card_signature_invalid"
)
SUB_TAG_BATCH_HASH_MISMATCH: Final[str] = ".batch_hash_mismatch"
SUB_TAG_PER_RECIPIENT_SIGNATURE_INVALID: Final[str] = (
    ".per_recipient_signature_invalid"
)
SUB_TAG_PER_RECIPIENT_SIGNATURE_GRANT_OR_ORG_MISMATCH: Final[str] = (
    ".per_recipient_signature_grant_or_org_mismatch"
)
SUB_TAG_BATCH_RECIPIENT_ORDER_SWAP: Final[str] = ".batch_recipient_order_swap"
SUB_TAG_TOKEN_INVALID_INBOUND: Final[str] = ".token_invalid_inbound"
SUB_TAG_AEAD_TAG_INVALID: Final[str] = ".aead_tag_invalid"
SUB_TAG_REVOKED_TOKEN_REPLAY: Final[str] = ".revoked_token_replay"
SUB_TAG_CHANNEL_BINDING_MISMATCH: Final[str] = ".channel_binding_mismatch"
SUB_TAG_TOKEN_ID_COLLISION_DETECTED: Final[str] = ".token_id_collision_detected"
SUB_TAG_CEDAR_ENGINE_UNREADY: Final[str] = ".cedar_engine_unready"
SUB_TAG_ENV_VAR_AUTO_CONFIRM_SET: Final[str] = ".env_var_auto_confirm_set"
SUB_TAG_SEND_LOCK_HOLD_TIMEOUT: Final[str] = ".send_lock_hold_timeout"
SUB_TAG_ORGSCOPED_BOT_SUBCLASSING_FORBIDDEN: Final[str] = (
    ".orgscoped_bot_subclassing_forbidden"
)
SUB_TAG_CONFIG_SIGNATURE_INVALID: Final[str] = ".config_signature_invalid"

# Semantic-slot regex per F-CLASS-SLOT-ID-NON-OPAQUE mirror.
# Numeric IDs accepted: ``[SLOT_001]``. Anything else rejected.
SEMANTIC_SLOT_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"\[SLOT_([A-Z_]+)\]",
    re.ASCII,
)
NUMERIC_SLOT_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"\[SLOT_\d+\]",
    re.ASCII,
)

SMS_MAX_BODY_BYTES: Final[int] = 1600

PROHIBITED_ENV_VAR_KEYS: Final[frozenset[str]] = frozenset({
    "DATACOLLECTOR_AUTO_CONFIRM",
    "DATACOLLECTOR_YES",
    "DATACOLLECTOR_FORCE",
    "DC_AUTO",
    "DC_YES",
    "DC_FORCE",
})


@dataclass(frozen=True, kw_only=True)
class PiiLeakResult:
    """Result of an F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND sub-check."""

    success: bool
    failure_code: Optional[str]
    sub_tag: Optional[str]
    detail: str
    branch: str = ""


def _fail(branch: str, sub_tag: str, detail: str) -> PiiLeakResult:
    return PiiLeakResult(
        success=False,
        failure_code=F_DATACOLLECTOR_PII_LEAK_IN_OUTBOUND,
        sub_tag=sub_tag,
        detail=detail,
        branch=branch,
    )


def _ok(branch: str, detail: str) -> PiiLeakResult:
    return PiiLeakResult(
        success=True,
        failure_code=None,
        sub_tag=None,
        detail=detail,
        branch=branch,
    )


# ---------------------------------------------------------------------------
# Branch — semantic-slot detection in rendered outbound bytes
# ---------------------------------------------------------------------------


def check_semantic_slot_in_outbound(*, rendered_bytes: bytes) -> PiiLeakResult:
    """Mirror of F-CLASS-SLOT-ID-NON-OPAQUE for outbound message bytes.

    ``[SLOT_<NAME>]`` where NAME contains uppercase letters/underscores fails
    closed (semantic name leakage). ``[SLOT_001]`` (numeric) is permitted.
    """
    branch = "semantic_slot_in_outbound"
    try:
        text = rendered_bytes.decode("utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001
        return _fail(
            branch,
            SUB_TAG_SEMANTIC_SLOT_IN_OUTBOUND,
            f"rendered_bytes decode failed: {type(exc).__name__}: {exc}",
        )
    matches = SEMANTIC_SLOT_PATTERN.findall(text)
    if matches:
        return _fail(
            branch,
            SUB_TAG_SEMANTIC_SLOT_IN_OUTBOUND,
            f"semantic-named slot(s) in outbound: {matches[:5]}",
        )
    return _ok(branch, "no semantic-named slots in rendered outbound bytes")


# ---------------------------------------------------------------------------
# Branch — cross-org path leak / symlink escape
# ---------------------------------------------------------------------------


def check_path_cross_org(
    *,
    candidate_path: str,
    org_slug: str,
    is_symlink: bool = False,
    workspace_shared_prefix: str = "vault_shared/",
) -> PiiLeakResult:
    """All vault paths must resolve under ``orgs/<org_slug>/`` or workspace-shared."""
    branch = "path_cross_org"
    if is_symlink:
        return _fail(
            branch,
            SUB_TAG_SYMLINK_ESCAPE,
            f"candidate_path {candidate_path!r} resolves through a symlink",
        )
    parts = PurePosixPath(candidate_path).parts
    org_prefix = ("orgs", org_slug)
    if parts[: len(org_prefix)] == org_prefix:
        return _ok(branch, f"path resolves under orgs/{org_slug}/")
    if candidate_path.startswith(workspace_shared_prefix):
        return _ok(branch, f"path resolves under {workspace_shared_prefix}")
    return _fail(
        branch,
        SUB_TAG_PATH_CROSS_ORG,
        (
            f"candidate_path {candidate_path!r} does not resolve under "
            f"orgs/{org_slug}/ or {workspace_shared_prefix}"
        ),
    )


# ---------------------------------------------------------------------------
# Branch — MTProto cross-org isolation + chat_id collision + session path
# ---------------------------------------------------------------------------


def check_mtproto_cross_org(
    *,
    chat_id: object,
    expected_org_slug: str,
    resolved_org_slug: Optional[str],
) -> PiiLeakResult:
    """RT-26: chat_id resolution must land in the invocation's org."""
    branch = "mtproto_cross_org"
    if resolved_org_slug is None:
        return _fail(
            branch,
            SUB_TAG_MTPROTO_CROSS_ORG,
            f"chat_id={chat_id!r} did not resolve to any org_slug",
        )
    if resolved_org_slug != expected_org_slug:
        return _fail(
            branch,
            SUB_TAG_MTPROTO_CROSS_ORG,
            (
                f"chat_id={chat_id!r} resolved to org={resolved_org_slug!r} "
                f"but invocation expects org={expected_org_slug!r}"
            ),
        )
    return _ok(branch, "chat_id resolves to invocation's org_slug")


def check_cross_org_chat_id_collision(
    *,
    chat_id: object,
    matching_org_slugs: Sequence[str],
) -> PiiLeakResult:
    """RT-08: a single chat_id must NOT match multiple org consent ledgers."""
    branch = "cross_org_chat_id_collision"
    if len(matching_org_slugs) > 1:
        return _fail(
            branch,
            SUB_TAG_CROSS_ORG_CHAT_ID_COLLISION,
            (
                f"chat_id={chat_id!r} matches multiple org consent ledgers: "
                f"{list(matching_org_slugs)}"
            ),
        )
    return _ok(branch, f"chat_id={chat_id!r} bound to at most one org")


def check_mtproto_session_path_bound(
    *,
    session_path: str,
    org_slug: str,
) -> PiiLeakResult:
    """RT-26: session path must contain the org_slug substring."""
    branch = "mtproto_session_path_unbound"
    if not session_path or org_slug not in session_path:
        return _fail(
            branch,
            SUB_TAG_MTPROTO_SESSION_PATH_UNBOUND,
            (
                f"MTProto session_path={session_path!r} does not contain "
                f"org_slug={org_slug!r}"
            ),
        )
    return _ok(branch, "MTProto session_path bound to org_slug")


def check_telegram_chat_type(*, chat_type: str) -> PiiLeakResult:
    """RT-09: group / supergroup chat_ids are rejected."""
    branch = "telegram_group_chat_rejected"
    if chat_type in {"group", "supergroup", "channel"}:
        return _fail(
            branch,
            SUB_TAG_TELEGRAM_GROUP_CHAT_REJECTED,
            f"telegram chat_type={chat_type!r} not permitted; only 'private'",
        )
    return _ok(branch, f"telegram chat_type={chat_type!r} permitted")


# ---------------------------------------------------------------------------
# Branch — SMS size + WhatsApp template + state card signature
# ---------------------------------------------------------------------------


def check_sms_size_overflow(*, rendered_body_bytes: bytes) -> PiiLeakResult:
    branch = "sms_size_overflow"
    if len(rendered_body_bytes) > SMS_MAX_BODY_BYTES:
        return _fail(
            branch,
            SUB_TAG_SMS_SIZE_OVERFLOW,
            (
                f"rendered SMS body {len(rendered_body_bytes)} bytes "
                f"exceeds {SMS_MAX_BODY_BYTES}-byte cap"
            ),
        )
    return _ok(branch, f"rendered SMS body {len(rendered_body_bytes)} bytes")


def check_whatsapp_template_approved(
    *,
    inside_24h_window: bool,
    template_id: Optional[str],
    approved_template_ids: frozenset[str],
) -> PiiLeakResult:
    branch = "whatsapp_template_unapproved"
    if inside_24h_window:
        return _ok(branch, "inside 24h conversation window — free-form permitted")
    if template_id is None:
        return _fail(
            branch,
            SUB_TAG_WHATSAPP_TEMPLATE_UNAPPROVED,
            "outside 24h window and template_id is None",
        )
    if template_id not in approved_template_ids:
        return _fail(
            branch,
            SUB_TAG_WHATSAPP_TEMPLATE_UNAPPROVED,
            (
                f"outside 24h window; template_id={template_id!r} not in "
                f"approved register"
            ),
        )
    return _ok(branch, f"template_id={template_id!r} approved + outside-24h ok")


def check_state_card_signature(
    *,
    state_code: str,
    signature_valid: bool,
) -> PiiLeakResult:
    branch = "state_card_signature_invalid"
    if not signature_valid:
        return _fail(
            branch,
            SUB_TAG_STATE_CARD_SIGNATURE_INVALID,
            (
                f"state card for {state_code!r} Ed25519 signature "
                "verification failed against SN-LLC pinned public key"
            ),
        )
    return _ok(branch, f"state card for {state_code!r} signature verified")


# ---------------------------------------------------------------------------
# Branch — batch hash + per-recipient signature + recipient order
# ---------------------------------------------------------------------------


def check_batch_hash(
    *,
    batch_content_sha3_512_signed: bytes,
    batch_content_sha3_512_recomputed: bytes,
) -> PiiLeakResult:
    branch = "batch_hash_mismatch"
    if not isinstance(batch_content_sha3_512_signed, (bytes, bytearray)) or not isinstance(
        batch_content_sha3_512_recomputed, (bytes, bytearray)
    ):
        return _fail(
            branch,
            SUB_TAG_BATCH_HASH_MISMATCH,
            "batch_content_sha3_512 inputs are not bytes",
        )
    if not hmac.compare_digest(
        bytes(batch_content_sha3_512_signed),
        bytes(batch_content_sha3_512_recomputed),
    ):
        return _fail(
            branch,
            SUB_TAG_BATCH_HASH_MISMATCH,
            "signed batch_content_sha3_512 differs from recomputed digest",
        )
    return _ok(branch, "batch_content_sha3_512 matches signed digest")


def check_per_recipient_signature_valid(
    *,
    signature_valid: bool,
    recipient_id: str,
) -> PiiLeakResult:
    branch = "per_recipient_signature_invalid"
    if not signature_valid:
        return _fail(
            branch,
            SUB_TAG_PER_RECIPIENT_SIGNATURE_INVALID,
            (
                f"per-recipient Ed25519 signature invalid for "
                f"recipient_id={recipient_id!r}"
            ),
        )
    return _ok(
        branch,
        f"per-recipient signature verified for recipient_id={recipient_id!r}",
    )


def check_per_recipient_signature_grant_or_org(
    *,
    signed_grant_id: str,
    invocation_grant_id: str,
    signed_org_slug: str,
    invocation_org_slug: str,
    recipient_id: str,
) -> PiiLeakResult:
    """RT-C2-01: signed envelope must bind grant_id + org_slug."""
    branch = "per_recipient_signature_grant_or_org_mismatch"
    if signed_grant_id != invocation_grant_id:
        return _fail(
            branch,
            SUB_TAG_PER_RECIPIENT_SIGNATURE_GRANT_OR_ORG_MISMATCH,
            (
                f"signed grant_id={signed_grant_id!r} != invocation "
                f"grant_id={invocation_grant_id!r} for recipient={recipient_id!r}"
            ),
        )
    if signed_org_slug != invocation_org_slug:
        return _fail(
            branch,
            SUB_TAG_PER_RECIPIENT_SIGNATURE_GRANT_OR_ORG_MISMATCH,
            (
                f"signed org_slug={signed_org_slug!r} != invocation "
                f"org_slug={invocation_org_slug!r} for recipient={recipient_id!r}"
            ),
        )
    return _ok(branch, "signed grant_id + org_slug match invocation")


def check_batch_recipient_order(
    *,
    signed_recipient_order: Sequence[str],
    dispatch_recipient_order: Sequence[str],
) -> PiiLeakResult:
    """RT-C2-12: dispatch order must match the signed approved order."""
    branch = "batch_recipient_order_swap"
    if list(signed_recipient_order) != list(dispatch_recipient_order):
        return _fail(
            branch,
            SUB_TAG_BATCH_RECIPIENT_ORDER_SWAP,
            (
                "dispatch order differs from signed approved_recipient_order; "
                f"first divergence index: "
                f"{_first_divergence(signed_recipient_order, dispatch_recipient_order)}"
            ),
        )
    return _ok(branch, "dispatch order matches signed approved_recipient_order")


def _first_divergence(a: Sequence[str], b: Sequence[str]) -> int:
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i
    return min(len(a), len(b))


# ---------------------------------------------------------------------------
# Branch — token validation (inbound + AEAD + revoked + binding + uuid)
# ---------------------------------------------------------------------------


def check_token_inbound_valid(
    *,
    inbound_token_value: bytes,
    register_token_value: bytes,
    rotates_at_utc_in_future: bool,
) -> PiiLeakResult:
    """Token decoded + matches register + rotation date in future."""
    branch = "token_invalid_inbound"
    if not isinstance(inbound_token_value, (bytes, bytearray)) or not isinstance(
        register_token_value, (bytes, bytearray)
    ):
        return _fail(
            branch,
            SUB_TAG_TOKEN_INVALID_INBOUND,
            "token bytes inputs are not bytes",
        )
    if not hmac.compare_digest(
        bytes(inbound_token_value),
        bytes(register_token_value),
    ):
        return _fail(
            branch,
            SUB_TAG_TOKEN_INVALID_INBOUND,
            "inbound token bytes do not match register",
        )
    if not rotates_at_utc_in_future:
        return _fail(
            branch,
            SUB_TAG_TOKEN_INVALID_INBOUND,
            "token past rotates_at_utc — stale",
        )
    return _ok(branch, "inbound token matches register and not stale")


def check_aead_tag_valid(*, aead_verified: bool) -> PiiLeakResult:
    branch = "aead_tag_invalid"
    if not aead_verified:
        return _fail(
            branch,
            SUB_TAG_AEAD_TAG_INVALID,
            "AEAD authentication tag verification failed — suspected tamper",
        )
    return _ok(branch, "AEAD tag verified")


def check_token_revoked(*, token_revoked: bool) -> PiiLeakResult:
    branch = "revoked_token_replay"
    if token_revoked:
        return _fail(
            branch,
            SUB_TAG_REVOKED_TOKEN_REPLAY,
            "token marked revoked=True (rotated); reject regardless of rotates_at_utc",
        )
    return _ok(branch, "token not revoked")


def check_channel_binding(
    *,
    inbound_channel: str,
    token_channel_binding: str,
) -> PiiLeakResult:
    """RT-10: token channel binding must match inbound channel."""
    branch = "channel_binding_mismatch"
    if inbound_channel != token_channel_binding:
        return _fail(
            branch,
            SUB_TAG_CHANNEL_BINDING_MISMATCH,
            (
                f"inbound_channel={inbound_channel!r} differs from token "
                f"channel_binding={token_channel_binding!r}"
            ),
        )
    return _ok(branch, "inbound channel matches token channel_binding")


def check_token_id_uniqueness(
    *,
    new_token_id: str,
    existing_token_ids: frozenset[str],
) -> PiiLeakResult:
    """RT-C2-06: token_id collision detection at issue time."""
    branch = "token_id_collision_detected"
    if new_token_id in existing_token_ids:
        return _fail(
            branch,
            SUB_TAG_TOKEN_ID_COLLISION_DETECTED,
            f"new_token_id={new_token_id!r} collides with existing token",
        )
    return _ok(branch, f"new_token_id={new_token_id!r} unique")


# ---------------------------------------------------------------------------
# Branch — Cedar engine readiness
# ---------------------------------------------------------------------------


def check_cedar_engine_ready(*, cedar_engine_ready: bool) -> PiiLeakResult:
    branch = "cedar_engine_unready"
    # Identity-strict per v7.0.7 §4.3.4 — truthy non-True fail-closes.
    if cedar_engine_ready is not True:
        return _fail(
            branch,
            SUB_TAG_CEDAR_ENGINE_UNREADY,
            f"cedar_engine_ready is not True (got {cedar_engine_ready!r})",
        )
    return _ok(branch, "Cedar engine ready (identity-strict True)")


# ---------------------------------------------------------------------------
# Branch — env-var bypass (RT-23 + RT-C2-13)
# ---------------------------------------------------------------------------


def check_env_var_auto_confirm_set(*, env: Mapping[str, str]) -> PiiLeakResult:
    branch = "env_var_auto_confirm_set"
    set_keys = sorted(k for k in PROHIBITED_ENV_VAR_KEYS if k in env)
    if set_keys:
        return _fail(
            branch,
            SUB_TAG_ENV_VAR_AUTO_CONFIRM_SET,
            f"prohibited env-var keys present: {set_keys}",
        )
    return _ok(branch, "no prohibited env-var keys present")


# ---------------------------------------------------------------------------
# Branch — send-lock-hold timeout (RT-C2-05)
# ---------------------------------------------------------------------------


def check_send_lock_hold_timeout(
    *,
    elapsed_seconds: float,
    timeout_seconds: float = 30.0,
) -> PiiLeakResult:
    branch = "send_lock_hold_timeout"
    if elapsed_seconds > timeout_seconds:
        return _fail(
            branch,
            SUB_TAG_SEND_LOCK_HOLD_TIMEOUT,
            (
                f"send-lock held {elapsed_seconds:.3f}s exceeds "
                f"{timeout_seconds:.3f}s timeout — abort recipient"
            ),
        )
    return _ok(branch, f"send-lock hold {elapsed_seconds:.3f}s within timeout")


# ---------------------------------------------------------------------------
# Branch — OrgScopedBot subclassing (RT-C2-03)
# ---------------------------------------------------------------------------


def check_orgscoped_bot_class(*, candidate_class_name: str) -> PiiLeakResult:
    branch = "orgscoped_bot_subclassing_forbidden"
    if candidate_class_name != "OrgScopedBot":
        return _fail(
            branch,
            SUB_TAG_ORGSCOPED_BOT_SUBCLASSING_FORBIDDEN,
            (
                f"OrgScopedBot is final; subclassing {candidate_class_name!r} "
                "not permitted"
            ),
        )
    return _ok(branch, "OrgScopedBot used directly (no subclass)")


__all__ = [
    "F_DATACOLLECTOR_PII_LEAK_IN_OUTBOUND",
    "NUMERIC_SLOT_PATTERN",
    "PERMITTED_CHANNELS",
    "PROHIBITED_ENV_VAR_KEYS",
    "PiiLeakResult",
    "SEMANTIC_SLOT_PATTERN",
    "SMS_MAX_BODY_BYTES",
    "SUB_TAG_AEAD_TAG_INVALID",
    "SUB_TAG_BATCH_HASH_MISMATCH",
    "SUB_TAG_BATCH_RECIPIENT_ORDER_SWAP",
    "SUB_TAG_CEDAR_ENGINE_UNREADY",
    "SUB_TAG_CHANNEL_BINDING_MISMATCH",
    "SUB_TAG_CONFIG_SIGNATURE_INVALID",
    "SUB_TAG_CROSS_ORG_CHAT_ID_COLLISION",
    "SUB_TAG_ENV_VAR_AUTO_CONFIRM_SET",
    "SUB_TAG_MTPROTO_CROSS_ORG",
    "SUB_TAG_MTPROTO_SESSION_PATH_UNBOUND",
    "SUB_TAG_ORGSCOPED_BOT_SUBCLASSING_FORBIDDEN",
    "SUB_TAG_PATH_CROSS_ORG",
    "SUB_TAG_PER_RECIPIENT_SIGNATURE_GRANT_OR_ORG_MISMATCH",
    "SUB_TAG_PER_RECIPIENT_SIGNATURE_INVALID",
    "SUB_TAG_REVOKED_TOKEN_REPLAY",
    "SUB_TAG_SEMANTIC_SLOT_IN_OUTBOUND",
    "SUB_TAG_SEND_LOCK_HOLD_TIMEOUT",
    "SUB_TAG_SMS_SIZE_OVERFLOW",
    "SUB_TAG_STATE_CARD_SIGNATURE_INVALID",
    "SUB_TAG_SYMLINK_ESCAPE",
    "SUB_TAG_TELEGRAM_GROUP_CHAT_REJECTED",
    "SUB_TAG_TOKEN_ID_COLLISION_DETECTED",
    "SUB_TAG_TOKEN_INVALID_INBOUND",
    "SUB_TAG_WHATSAPP_TEMPLATE_UNAPPROVED",
    "check_aead_tag_valid",
    "check_batch_hash",
    "check_batch_recipient_order",
    "check_cedar_engine_ready",
    "check_channel_binding",
    "check_cross_org_chat_id_collision",
    "check_env_var_auto_confirm_set",
    "check_mtproto_cross_org",
    "check_mtproto_session_path_bound",
    "check_orgscoped_bot_class",
    "check_path_cross_org",
    "check_per_recipient_signature_grant_or_org",
    "check_per_recipient_signature_valid",
    "check_semantic_slot_in_outbound",
    "check_send_lock_hold_timeout",
    "check_sms_size_overflow",
    "check_state_card_signature",
    "check_telegram_chat_type",
    "check_token_id_uniqueness",
    "check_token_inbound_valid",
    "check_token_revoked",
    "check_whatsapp_template_approved",
]
