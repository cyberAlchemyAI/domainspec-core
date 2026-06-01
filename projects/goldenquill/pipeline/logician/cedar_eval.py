"""Cedar entity shapes + minimal pure-Python evaluator. [§2.6 + §4.4 + §4.5]

Section 4 evaluates Cedar policy at PRE-gate (vault access gating, M14/M15)
and at cite-time (dossier verification, cross-org reference policy). At v0.1
the evaluator is a deterministic pure-Python dispatcher over the four entity
shapes from §2.6 — no third-party ``cedar`` engine dependency. The three
policies wired here are:

* ``org_isolation`` — Law 3 / M14: Session may only access VaultPaths whose
  org_slug_hint matches Session.org_slug, or VaultPaths flagged ``is_shared``.
* ``byok_key_scope`` — Law 3 / M9: OperatorKeyringKey.bound_org_slug must
  match Session.org_slug.
* ``cross_org_dossier_reference`` — Law 3 / BT11: Claim.cross_org_dossier may
  be True only with an explicit operator confirmation flag.

Round 6 capstone wires these into ``pre_gate.py`` (#4 + #17) and into
``gate_runner.py`` (POST-gate step 5). The evaluator is fail-closed: any
unknown policy name, any malformed entity, any policy-compile failure
returns ``CedarDecision(allow=False, ...)``.

Real Cedar engine integration is deferred to a future round; the entity
shapes are stable per §2.6 and will not change.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# Cedar grammar comment-strip pattern: `// line comment` and `/* block comment */`.
# Used by compile_cedar_policy to prevent the substring effect-keyword check
# (`permit` / `forbid`) from being bypassed by comments containing those words.
# Closes finding (e) of §4 Logician Group 7 Batch A committee dispatch
# (gpt_oss F-1 MEDIUM; L-005 narrow-fix landed 2026-04-29). Real Cedar parsing
# is deferred to a future round.
_CEDAR_COMMENT_PATTERN = re.compile(r"//[^\n]*|/\*.*?\*/", re.DOTALL)


# ---------------------------------------------------------------------------
# Failure-code constants (§6.1 + §6.10)
#
# F-CEDAR-01..04 are module-internal Cedar denial codes consumed by §7 Scribe
# / §8 Editor / §9 Judge / §10 Red Team seat wiring (LOCKED rounds) and by
# §4.4.1 step 5 dossier verify. §4 v2.1 §6.13 currently catalogs only
# F-CEDAR-COMPOUND-DENIED (the §4.11 compound-commit predicate code); the
# 01..04 family is a v0.2 candidate for §6.10 catalog promotion. Scope:
# referenced by spec cards section_07_scribe_round_3, section_08_editor_*,
# section_09_judge_round_3 — all LOCKED — under the canonical
# `pipeline.logician.cedar_eval.evaluate*` public surface.
# ---------------------------------------------------------------------------


F_PRE_04_CEDAR_UNSIGNED: str = "F-PRE-04.cedar_policy_unsigned"
F_PRE_04_LEDGER_MISMATCH: str = "F-PRE-04.cedar_policy_ledger_mismatch"
F_PRE_17_CEDAR_COMPILE_ERROR: str = "F-PRE-17.cedar_policy_compile_error"

F_CEDAR_ORG_ISOLATION_DENY: str = "F-CEDAR-01.org_isolation_deny"
F_CEDAR_BYOK_KEY_SCOPE_DENY: str = "F-CEDAR-02.byok_key_scope_deny"
F_CEDAR_CROSS_ORG_DENY: str = "F-CEDAR-03.cross_org_dossier_deny"
F_CEDAR_UNKNOWN_POLICY: str = "F-CEDAR-04.unknown_policy"

KNOWN_POLICY_NAMES: frozenset[str] = frozenset(
    {"org_isolation", "byok_key_scope", "cross_org_dossier_reference"}
)

VALID_TAGS: frozenset[str] = frozenset({"DOC_SOURCED", "USER_DATA", "UNSOURCED"})


# ---------------------------------------------------------------------------
# Cedar entity dataclasses (§2.6 verbatim)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class SessionEntity:
    """`entity Session` per §2.6."""

    session_id: str
    org_slug: str
    org_root_hash: str
    byok_key_id: str
    started_at_utc: str


@dataclass(frozen=True, kw_only=True)
class VaultPathEntity:
    """`entity VaultPath` per §2.6.

    ``org_slug_hint`` is extracted from the path; the authoritative check is
    ``canonical_path`` vs ``org_root`` (caller's responsibility). The
    evaluator uses ``org_slug_hint`` for fast-path policy decisions and
    relies on the caller to have already canonicalised the path.
    """

    canonical_path: str
    inode: int
    volume_uuid: str
    org_slug_hint: str
    is_shared: bool


@dataclass(frozen=True, kw_only=True)
class ClaimEntity:
    """`entity Claim` per §2.6."""

    claim_id: str
    tag: str
    source_kind: str
    cross_org_dossier: bool


@dataclass(frozen=True, kw_only=True)
class OperatorKeyringKeyEntity:
    """`entity OperatorKeyringKey` per §2.6."""

    key_id: str
    bound_org_slug: str


# ---------------------------------------------------------------------------
# Cedar policy + decision wrappers
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class CedarPolicy:
    """A signed + M15-committed Cedar policy."""

    name: str
    text: str
    operator_signature: bytes
    signed_at_utc: str
    m15_ledger_head: str


@dataclass(frozen=True, kw_only=True)
class CedarDecision:
    """Outcome of evaluating one policy against one entity context."""

    allow: bool
    policy_name: str
    failure_code: Optional[str]
    reason: str


# ---------------------------------------------------------------------------
# Policy compile (minimal grammar check)
# ---------------------------------------------------------------------------


def compile_cedar_policy(policy: CedarPolicy) -> tuple[bool, str]:
    """Minimal Cedar policy grammar check.

    At v0.1 we delegate full Cedar parsing to a future round. For PRE-gate
    check #17 (`F-PRE-17.cedar_policy_compile_error`), this function
    enforces:

    * Policy name is in :data:`KNOWN_POLICY_NAMES`.
    * Policy text is non-empty after strip.
    * Policy text contains at least one of the Cedar effect keywords
      ``permit`` or ``forbid``.

    Returns ``(ok, detail)``. On ok=False, detail names the violation.
    """

    if not isinstance(policy, CedarPolicy):
        return (
            False,
            f"policy must be CedarPolicy, got {type(policy).__name__}",
        )
    if policy.name not in KNOWN_POLICY_NAMES:
        return (
            False,
            f"unknown policy name {policy.name!r}; expected one of "
            f"{sorted(KNOWN_POLICY_NAMES)}",
        )
    text = policy.text.strip()
    if not text:
        return (False, "policy text is empty")
    # Strip Cedar comments before the effect-keyword check so a policy whose
    # only `permit` / `forbid` token lives inside a comment fails compile.
    # Closes finding (e) — gpt_oss F-1 MEDIUM, §4 Group 7 Batch A 2026-04-29.
    text_no_comments = _CEDAR_COMMENT_PATTERN.sub("", text)
    if "permit" not in text_no_comments and "forbid" not in text_no_comments:
        return (
            False,
            "policy text contains neither 'permit' nor 'forbid' effect "
            "(comments stripped before check per §4.7 grammar floor)",
        )
    return (True, "")


def verify_cedar_policy_signed(
    policy: CedarPolicy,
    *,
    expected_ledger_head: str,
    signature_verifier,  # callable: (CedarPolicy) -> bool — REQUIRED; None forbidden (fail-closed per §4.2.1 row 4)
) -> Optional[str]:
    """Returns failure code if signature/ledger check fails; None on PASS.

    Used at PRE-gate check #4. ``signature_verifier`` is supplied by the
    caller (Section 1 keyring) and is REQUIRED — passing ``None`` raises
    ``TypeError`` because the §4.2.1 row 4 fail-closed mandate forbids
    accepting a non-empty ``operator_signature`` byte string as proof of
    signature without cryptographic verification. Closes finding (a) of
    §4 Logician Group 7 Batch A committee dispatch (gpt_oss F-1 HIGH;
    L-005 narrow-fix landed 2026-04-29).
    """

    if not isinstance(policy, CedarPolicy):
        raise TypeError("policy must be CedarPolicy")
    if signature_verifier is None:
        raise TypeError(
            "signature_verifier is required (None forbidden per §4.2.1 row 4 "
            "fail-closed mandate; pass a callable that cryptographically "
            "verifies policy.operator_signature against the operator keyring)"
        )
    if not callable(signature_verifier):
        raise TypeError("signature_verifier must be callable")
    if not policy.operator_signature:
        return F_PRE_04_CEDAR_UNSIGNED
    if not signature_verifier(policy):
        return F_PRE_04_CEDAR_UNSIGNED
    if policy.m15_ledger_head != expected_ledger_head:
        return F_PRE_04_LEDGER_MISMATCH
    return None


# ---------------------------------------------------------------------------
# Per-policy evaluators
# ---------------------------------------------------------------------------


def evaluate_org_isolation(
    *,
    session: SessionEntity,
    vault_path: VaultPathEntity,
) -> CedarDecision:
    """Law 3 / M14 — session may only access its own org's vault subtree."""

    if not isinstance(session, SessionEntity):
        raise TypeError("session must be SessionEntity")
    if not isinstance(vault_path, VaultPathEntity):
        raise TypeError("vault_path must be VaultPathEntity")
    if vault_path.is_shared:
        return CedarDecision(
            allow=True,
            policy_name="org_isolation",
            failure_code=None,
            reason="vault_path is shared (vault_shared/)",
        )
    if vault_path.org_slug_hint == session.org_slug:
        return CedarDecision(
            allow=True,
            policy_name="org_isolation",
            failure_code=None,
            reason="org_slug match",
        )
    return CedarDecision(
        allow=False,
        policy_name="org_isolation",
        failure_code=F_CEDAR_ORG_ISOLATION_DENY,
        reason=(
            f"session.org_slug={session.org_slug!r} != "
            f"vault_path.org_slug_hint={vault_path.org_slug_hint!r}"
        ),
    )


def evaluate_byok_key_scope(
    *,
    session: SessionEntity,
    key: OperatorKeyringKeyEntity,
) -> CedarDecision:
    """Law 3 / M9 — BYOK key must be scoped to session org."""

    if not isinstance(session, SessionEntity):
        raise TypeError("session must be SessionEntity")
    if not isinstance(key, OperatorKeyringKeyEntity):
        raise TypeError("key must be OperatorKeyringKeyEntity")
    if key.bound_org_slug == session.org_slug:
        return CedarDecision(
            allow=True,
            policy_name="byok_key_scope",
            failure_code=None,
            reason="key bound to session org",
        )
    return CedarDecision(
        allow=False,
        policy_name="byok_key_scope",
        failure_code=F_CEDAR_BYOK_KEY_SCOPE_DENY,
        reason=(
            f"key.bound_org_slug={key.bound_org_slug!r} != "
            f"session.org_slug={session.org_slug!r}"
        ),
    )


def evaluate_cross_org_dossier(
    *,
    session: SessionEntity,
    claim: ClaimEntity,
    operator_confirmation_present: bool,
) -> CedarDecision:
    """Law 3 / BT11 — cross-org dossier reference requires operator OK."""

    if not isinstance(session, SessionEntity):
        raise TypeError("session must be SessionEntity")
    if not isinstance(claim, ClaimEntity):
        raise TypeError("claim must be ClaimEntity")
    if claim.tag not in VALID_TAGS:
        raise ValueError(f"claim.tag {claim.tag!r} not in {sorted(VALID_TAGS)}")
    if not claim.cross_org_dossier:
        return CedarDecision(
            allow=True,
            policy_name="cross_org_dossier_reference",
            failure_code=None,
            reason="claim does not cite a cross-org dossier",
        )
    if operator_confirmation_present:
        return CedarDecision(
            allow=True,
            policy_name="cross_org_dossier_reference",
            failure_code=None,
            reason="operator confirmation present at draft time",
        )
    return CedarDecision(
        allow=False,
        policy_name="cross_org_dossier_reference",
        failure_code=F_CEDAR_CROSS_ORG_DENY,
        reason="cross-org dossier cited without operator confirmation",
    )


# ---------------------------------------------------------------------------
# Top-level dispatcher
# ---------------------------------------------------------------------------


def evaluate(
    *,
    policy_name: str,
    session: SessionEntity,
    vault_path: Optional[VaultPathEntity] = None,
    claim: Optional[ClaimEntity] = None,
    key: Optional[OperatorKeyringKeyEntity] = None,
    operator_confirmation_present: bool = False,
) -> CedarDecision:
    """Dispatch to a per-policy evaluator. Unknown policy → fail-closed DENY.

    The dispatcher does NOT compile or verify the policy text; callers must
    have already passed :func:`compile_cedar_policy` and (at PRE-gate)
    :func:`verify_cedar_policy_signed`. This function evaluates entity
    context only.
    """

    if not isinstance(policy_name, str):
        raise TypeError("policy_name must be str")

    if policy_name == "org_isolation":
        if vault_path is None:
            raise ValueError("org_isolation requires vault_path")
        return evaluate_org_isolation(session=session, vault_path=vault_path)
    if policy_name == "byok_key_scope":
        if key is None:
            raise ValueError("byok_key_scope requires key")
        return evaluate_byok_key_scope(session=session, key=key)
    if policy_name == "cross_org_dossier_reference":
        if claim is None:
            raise ValueError("cross_org_dossier_reference requires claim")
        return evaluate_cross_org_dossier(
            session=session,
            claim=claim,
            operator_confirmation_present=operator_confirmation_present,
        )

    return CedarDecision(
        allow=False,
        policy_name=policy_name,
        failure_code=F_CEDAR_UNKNOWN_POLICY,
        reason=f"unknown policy {policy_name!r}",
    )


# ---------------------------------------------------------------------------
# Bundled-policy engine — WS-I §13 Data Collector Slice 3 (2026-05-11)
#
# Distinct from the §4.4.1 operator-signed runtime policy registry above.
# Bundled policies ship with the appliance, frozen at Golden Image build,
# and are loaded at module-import time by per-seat ``_bootstrap_cedar_engine``
# hooks. The contract for bundled policies is intentionally simpler than the
# operator-signed flow:
#
#   * No M15 ledger commitment (policies are frozen at Golden Image build).
#   * No operator Ed25519 signature (the appliance's Golden Image build is
#     itself the trust root; image integrity is checked separately).
#   * Same minimal Cedar grammar floor — non-empty after stripping comments
#     AND at least one ``permit``/``forbid`` effect keyword present.
#
# The engine is fail-closed: any file that fails the grammar floor, any
# directory that has no .cedar files, any IO error raises
# ``CedarEngineLoadError``. The caller wraps the import in its own
# fail-closed BaseException-subclass (per the §13.16.2 RT-C2-04 closure
# pattern); see ``pipeline/orchestrator/seats/data_collector/__init__.py``.
# ---------------------------------------------------------------------------


class CedarEngineLoadError(Exception):
    """Raised when a bundled Cedar policy file fails to load or compile.

    Subclass of ``Exception`` (not ``BaseException``) so it composes with
    the seat-side ``CriticalPolicyError(BaseException)`` discipline — the
    seat's ``_bootstrap_cedar_engine`` catches ``BaseException`` and
    re-raises through ``CriticalPolicyError`` so upstream
    ``try/except Exception`` cannot swallow.
    """


@dataclass(frozen=True, kw_only=True)
class BundledCedarPolicy:
    """A Cedar policy file shipped with the appliance.

    No operator signature; no M15 ledger head. Trust root is the Golden
    Image build itself. The ``text`` field is the raw .cedar source.
    """

    name: str
    path: Path
    text: str


def _bundled_grammar_floor(text: str) -> tuple[bool, str]:
    """Apply the minimal grammar floor used for bundled policies.

    Mirrors ``compile_cedar_policy`` but is name-agnostic (the bundled
    policies belong to their owning seats and are not enumerated in
    ``KNOWN_POLICY_NAMES``).
    """
    stripped = text.strip()
    if not stripped:
        return (False, "policy text is empty")
    text_no_comments = _CEDAR_COMMENT_PATTERN.sub("", stripped)
    if "permit" not in text_no_comments and "forbid" not in text_no_comments:
        return (
            False,
            "policy text contains neither 'permit' nor 'forbid' effect "
            "(comments stripped before check per §4.7 grammar floor)",
        )
    return (True, "")


@dataclass
class CedarEngine:
    """Bundled Cedar policy engine.

    Construction: ``CedarEngine(policy_dir=Path("…/cedar_policies"))``.
    Load: ``engine.load_all()`` walks ``policy_dir`` for ``*.cedar`` files,
    applies the bundled grammar floor to each, and stores the parsed
    policies in ``engine._policies``. Failure → ``CedarEngineLoadError``;
    no partial-load state survives the exception (engine returns to its
    pre-load state). Readiness: ``engine.is_ready()`` returns ``True``
    iff ``load_all()`` completed successfully and ``policy_dir`` contained
    at least one ``.cedar`` file. The caller MUST check
    ``engine.is_ready() is True`` (identity-strict per v7.0.7 §4.3.4
    pattern + §13.16.2 RT-C2-04 closure).
    """

    policy_dir: Path
    _policies: dict[str, BundledCedarPolicy] = field(default_factory=dict)
    _ready: bool = False

    def load_all(self) -> None:
        """Walk ``policy_dir`` and load every ``*.cedar`` file.

        Raises ``CedarEngineLoadError`` on:
          * ``policy_dir`` missing or not a directory.
          * Any ``*.cedar`` file fails the grammar floor.
          * Any IO error reading a ``*.cedar`` file.
          * Zero ``*.cedar`` files found.

        On success, ``self._policies`` is populated and ``self._ready``
        flips to ``True``.
        """
        # Reset state — partial-load failures must not leave stale entries.
        self._policies = {}
        self._ready = False

        directory = Path(self.policy_dir)
        if not directory.is_dir():
            raise CedarEngineLoadError(
                f"policy_dir is not a directory: {directory!r}"
            )

        # Deterministic order — sorted by filename — so test fixtures and
        # diagnostics are stable across operating systems.
        cedar_files = sorted(directory.glob("*.cedar"))
        if not cedar_files:
            raise CedarEngineLoadError(
                f"policy_dir {directory!r} contains no *.cedar files"
            )

        for path in cedar_files:
            try:
                text = path.read_text(encoding="utf-8")
            except OSError as exc:
                raise CedarEngineLoadError(
                    f"failed to read Cedar policy {path!r}: {exc}"
                ) from exc
            ok, detail = _bundled_grammar_floor(text)
            if not ok:
                raise CedarEngineLoadError(
                    f"Cedar policy {path!r} failed grammar floor: {detail}"
                )
            name = path.stem
            if name in self._policies:
                # Two files with the same stem — non-deterministic resolution
                # would be a foot-gun; fail closed.
                raise CedarEngineLoadError(
                    f"duplicate Cedar policy name {name!r} (first at "
                    f"{self._policies[name].path!r}, second at {path!r})"
                )
            self._policies[name] = BundledCedarPolicy(
                name=name, path=path, text=text
            )

        self._ready = True

    def is_ready(self) -> bool:
        """Return True iff ``load_all`` has completed successfully.

        Callers MUST use ``engine.is_ready() is True`` (identity-strict).
        """
        return self._ready

    def loaded_policy_names(self) -> tuple[str, ...]:
        """Return the sorted tuple of loaded policy stems (for diagnostics)."""
        return tuple(sorted(self._policies))

    def policy_text(self, name: str) -> str:
        """Return the raw text of the named policy.

        Raises ``KeyError`` if the policy has not been loaded.
        """
        return self._policies[name].text


__all__ = [
    "F_PRE_04_CEDAR_UNSIGNED",
    "F_PRE_04_LEDGER_MISMATCH",
    "F_PRE_17_CEDAR_COMPILE_ERROR",
    "F_CEDAR_ORG_ISOLATION_DENY",
    "F_CEDAR_BYOK_KEY_SCOPE_DENY",
    "F_CEDAR_CROSS_ORG_DENY",
    "F_CEDAR_UNKNOWN_POLICY",
    "KNOWN_POLICY_NAMES",
    "VALID_TAGS",
    "SessionEntity",
    "VaultPathEntity",
    "ClaimEntity",
    "OperatorKeyringKeyEntity",
    "CedarPolicy",
    "CedarDecision",
    "BundledCedarPolicy",
    "CedarEngine",
    "CedarEngineLoadError",
    "compile_cedar_policy",
    "verify_cedar_policy_signed",
    "evaluate_org_isolation",
    "evaluate_byok_key_scope",
    "evaluate_cross_org_dossier",
    "evaluate",
]
