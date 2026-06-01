"""§4 Logician Round L capstone — fixture library.

Round L promotes §4 from LOCKED-per-module (9 non-gate modules + 12 v2.2
amendment-enforcement gates + 3 v2.x cross-cutting amendments) to
LOCKED-as-a-whole-section. This file ships the shared builders used by:

* ``test_section_4_integration.py`` — L.1 PRE → silent-loop → POST integration
  (8 orchestrator-phase classes).
* ``test_section_4_bt_properties.py`` — L.2 §4-owned BT/M-family invariants
  (BT7 + BT9 + BT10 + BT11 + BT13 + M8 + M11/S11c).
* ``test_section_4_lifecycle_property.py`` — L.3 N ∈ {2, 8, 16, 32} parametric
  fuzz harness across (org_slug, session_id, claim_set) triples.

Per spec card ``pipeline/engineering/spec_cards/section_4_round_l_capstone.md``
§ "L.4 §7 test suite packaging". Mirrors the §5 R13 fixture-library shape
verbatim (regular helper module, NOT a pytest-discovered ``conftest.py``);
test files import builders directly. Per § "L.4" bullet 1: clean Logician
instance with all 21+ modules wired, sample PreGateInput + PostGateInput,
sample Cedar policy bundle, sample ConversationLogEntry chain, sample
admin-risk register, mock vault_write capturing intent + canonical bytes,
mock Section 1 keyring with BT6 rotation-aware lookup.

No pytest fixtures here — every helper is a plain factory so test classes
can compose inputs in-line. Pure-Python; zero filesystem coupling beyond
what individual builders explicitly own.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass, field
from typing import Callable, Optional

from pipeline.logician.cedar_eval import (
    CedarPolicy,
    ClaimEntity,
    OperatorKeyringKeyEntity,
    SessionEntity,
    VaultPathEntity,
)
from pipeline.logician.claim_evidence import (
    ClaimEntry,
    SourceRef,
    compute_claim_id,
)
from pipeline.logician.conversation_log import (
    ConversationLogEntry,
    SessionKeyVerifier,
    build_appended_entry,
    compute_content_hash,
)
from pipeline.logician.dossier_verify import (
    DossierLiveState,
    DossierSignoffSnapshot,
)
from pipeline.logician.gate_runner import (
    POST_GATE_STEP_NAMES,
    LogicianGateRunner,
    PostGateInput,
    PostGateStepOutcome,
)
from pipeline.logician.pre_gate import (
    PRE_GATE_CHECK_NAMES,
    CheckOutcome,
    PreGateInput,
)


# ---------------------------------------------------------------------------
# Canonical constants (BT6-style HMAC keys; all-zero bytes for determinism)
# ---------------------------------------------------------------------------


# 64-byte session HMAC key (rotation-active). Used for BT9 conversation log
# session-key signing AND BT13 rails-report signing under the per-session
# HMAC discipline.
SESSION_HMAC_KEY_ACTIVE: bytes = b"\x10" * 64
SESSION_HMAC_KEY_RETIRED: bytes = b"\x20" * 64
SESSION_HMAC_KEY_WRONG: bytes = b"\xff" * 64

# Canonical 128-hex SHA3 placeholders used for hash-shape fields where
# the value is irrelevant to the test (the test exercises the structural
# invariant, not the hash semantics).
DRAFT_HASH_FIXTURE: str = "d" * 128
RFA_HASH_FIXTURE: str = "r" * 128
RFA_URL_HASH_FIXTURE: str = "u" * 128
LEDGER_HEAD_FIXTURE: str = "h" * 128
DOSSIER_HASH_FIXTURE: str = "c" * 128


# ---------------------------------------------------------------------------
# CheckOutcome / PostGateStepOutcome convenience builders
# ---------------------------------------------------------------------------


def make_pre_check_pass(check_number: int) -> CheckOutcome:
    return CheckOutcome(
        check_number=check_number,
        check_name=PRE_GATE_CHECK_NAMES[check_number],
        passed=True,
        failure_code=None,
        failure_detail="",
    )


def make_pre_check_fail(
    check_number: int, code: str, detail: str = "fail"
) -> CheckOutcome:
    return CheckOutcome(
        check_number=check_number,
        check_name=PRE_GATE_CHECK_NAMES[check_number],
        passed=False,
        failure_code=code,
        failure_detail=detail,
    )


def default_caller_pre_outcomes() -> dict[int, CheckOutcome]:
    """All 13 caller-provided PRE checks → PASS."""

    return {
        n: make_pre_check_pass(n)
        for n in (1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 16, 18)
    }


def make_post_step_pass(step_number: int) -> PostGateStepOutcome:
    return PostGateStepOutcome(
        step_number=step_number,
        step_name=POST_GATE_STEP_NAMES[step_number],
        passed=True,
        failure_code=None,
        failure_detail="",
    )


def make_post_step_fail(
    step_number: int, code: str, detail: str = "fail"
) -> PostGateStepOutcome:
    return PostGateStepOutcome(
        step_number=step_number,
        step_name=POST_GATE_STEP_NAMES[step_number],
        passed=False,
        failure_code=code,
        failure_detail=detail,
    )


def default_caller_post_outcomes() -> dict[int, PostGateStepOutcome]:
    """All 9 caller-provided POST steps → PASS."""

    return {n: make_post_step_pass(n) for n in (1, 2, 3, 7, 8, 10, 11, 12, 13)}


# ---------------------------------------------------------------------------
# Cedar policy + signature verifiers
# ---------------------------------------------------------------------------


def make_signed_cedar_policy(
    *,
    name: str = "org_isolation",
    text: str = "permit(principal, action, resource);",
    operator_signature: bytes = b"\x01\x02\x03\x04",
    signed_at_utc: str = "2026-04-22T00:00:00Z",
    m15_ledger_head: str = LEDGER_HEAD_FIXTURE,
) -> CedarPolicy:
    return CedarPolicy(
        name=name,
        text=text,
        operator_signature=operator_signature,
        signed_at_utc=signed_at_utc,
        m15_ledger_head=m15_ledger_head,
    )


def cedar_signature_verifier_pass(_policy: CedarPolicy) -> bool:
    return True


def cedar_signature_verifier_fail(_policy: CedarPolicy) -> bool:
    return False


# ---------------------------------------------------------------------------
# PreGateInput / PostGateInput defaults
# ---------------------------------------------------------------------------


def default_pre_input(**overrides) -> PreGateInput:
    base: dict = dict(
        caller_outcomes=default_caller_pre_outcomes(),
        cedar_policy=make_signed_cedar_policy(),
        cedar_expected_ledger_head=LEDGER_HEAD_FIXTURE,
        cedar_signature_verifier=cedar_signature_verifier_pass,
        admin_risk_ok=True,
        admin_risk_sub_failure_code=None,
        admin_risk_failure_detail="",
        dossier_signoff_states=(("entity_a", True),),
        project_context_text="EIN: 12-3456789\nUEI: ABCD1234EFGH\n",
    )
    base.update(overrides)
    return PreGateInput(**base)


def default_post_input(**overrides) -> PostGateInput:
    base: dict = dict(
        caller_step_outcomes=default_caller_post_outcomes(),
        draft_hash=DRAFT_HASH_FIXTURE,
        rfa_hash=RFA_HASH_FIXTURE,
        session_id="sess-capstone-l",
        org_slug="mycosymbiotics_cooperative",
        rfa_url_hash=RFA_URL_HASH_FIXTURE,
        claims=(make_doc_sourced_claim(),),
        generated_at_utc="2026-04-22T12:00:00Z",
        dossier_verify_failure_codes=(),
        admin_risk_hard_block_count=0,
        rigor_breach_active=False,
    )
    base.update(overrides)
    return PostGateInput(**base)


# ---------------------------------------------------------------------------
# ClaimEntry convenience builders
# ---------------------------------------------------------------------------


def make_doc_sourced_claim(
    *,
    draft_hash: str = DRAFT_HASH_FIXTURE,
    offset: int = 0,
    text: str = "Mycelial networks process matter into structured tilth.",
    canonical_path: str = "/rfa/abc.md",
    inode: int = 42,
    content_hash: str = DOSSIER_HASH_FIXTURE,
    window_size: int = 2,
    rigor_breach: bool = False,
) -> ClaimEntry:
    cid = compute_claim_id(
        draft_hash=draft_hash, draft_offset=offset, claim_text=text
    )
    return ClaimEntry(
        claim_id=cid,
        draft_offset=offset,
        claim_text=text,
        tag="DOC_SOURCED",
        source_ref=SourceRef(
            source_kind="RFA",
            canonical_path=canonical_path,
            inode=inode,
            content_hash=content_hash,
            grep_string=text,
            window_size_sentences=window_size,
        ),
        verify_method="grep_windowed_pm2",
        verify_result="PASS",
        verify_detail="ok",
        rigor_breach_flag=rigor_breach,
    )


def make_unsourced_claim(
    *,
    draft_hash: str = DRAFT_HASH_FIXTURE,
    offset: int = 1,
    text: str = "An unsupported assertion lacking any source.",
) -> ClaimEntry:
    cid = compute_claim_id(
        draft_hash=draft_hash, draft_offset=offset, claim_text=text
    )
    return ClaimEntry(
        claim_id=cid,
        draft_offset=offset,
        claim_text=text,
        tag="UNSOURCED",
        source_ref=None,
        verify_method="unresolved",
        verify_result="UNSOURCED",
        verify_detail="no source",
        rigor_breach_flag=False,
    )


def make_user_data_claim(
    *,
    draft_hash: str = DRAFT_HASH_FIXTURE,
    offset: int = 2,
    text: str = "The operator confirmed in turn 17 that 4 cohorts ran in 2025.",
    matched_seq_id: int = 17,
) -> ClaimEntry:
    cid = compute_claim_id(
        draft_hash=draft_hash, draft_offset=offset, claim_text=text
    )
    return ClaimEntry(
        claim_id=cid,
        draft_offset=offset,
        claim_text=text,
        tag="USER_DATA",
        source_ref=SourceRef(
            source_kind="CONVERSATION_LOG",
            canonical_path=f"/orgs/x/vault/conversations/sess-{matched_seq_id}.jsonl",
            inode=100 + matched_seq_id,
            content_hash="b" * 128,
            grep_string=None,
            window_size_sentences=None,
        ),
        verify_method="conversation_anchor",
        verify_result="PASS",
        verify_detail=f"anchored at seq_id={matched_seq_id}",
        rigor_breach_flag=False,
    )


# ---------------------------------------------------------------------------
# Conversation-log chain builder + rotation-aware key verifier
# ---------------------------------------------------------------------------


def hmac_signer(key: bytes) -> Callable[[bytes], bytes]:
    """Return a deterministic HMAC-SHA3-512 signer keyed off ``key``."""

    def _sign(payload: bytes) -> bytes:
        return hmac.new(key, payload, hashlib.sha3_512).digest()

    return _sign


def build_genesis_chain(
    n: int,
    *,
    session_id: str = "sess-l",
    org_slug: str = "mycosymbiotics_cooperative",
    key: bytes = SESSION_HMAC_KEY_ACTIVE,
    speakers: Optional[tuple[str, ...]] = None,
    contents: Optional[tuple[str, ...]] = None,
    base_timestamp: str = "2026-04-22T08:00:00Z",
) -> tuple[ConversationLogEntry, ...]:
    """Construct a genesis-rooted conversation-log chain of ``n`` entries.

    Speakers default to ``operator`` / ``scribe`` alternating; contents are
    auto-generated unless overridden. Signer is deterministic HMAC over the
    canonical signing payload — matches the §4.6.4 verifier expectations.
    """

    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be non-negative int")
    if speakers is None:
        speakers = tuple(
            "operator" if i % 2 == 0 else "scribe" for i in range(n)
        )
    if contents is None:
        contents = tuple(f"utterance #{i + 1} bound to {session_id}" for i in range(n))
    if len(speakers) != n or len(contents) != n:
        raise ValueError("speakers + contents must each be of length n")

    signer = hmac_signer(key)
    entries: list[ConversationLogEntry] = []
    for i in range(n):
        ts = f"2026-04-22T08:{i:02d}:00Z" if i < 60 else base_timestamp
        entry = build_appended_entry(
            prior_entries=tuple(entries),
            utc_timestamp=ts,
            session_id=session_id,
            org_slug=org_slug,
            speaker=speakers[i],
            content=contents[i],
            signer=signer,
        )
        entries.append(entry)
    return tuple(entries)


@dataclass(frozen=True)
class RotationAwareSessionKeyVerifier:
    """BT6-aware :class:`SessionKeyVerifier` for cross-module integration tests.

    Active keys verify ``ACTIVE``; retired keys verify ``RETIRED`` (anchor
    PASS, F-BT9-02 INFO); other keys verify ``WRONG_KEY``. ``invalid_keys``
    cause signature math to fail and return ``INVALID``.
    """

    active_keys: tuple[bytes, ...] = (SESSION_HMAC_KEY_ACTIVE,)
    retired_keys: tuple[bytes, ...] = ()
    invalid_keys: tuple[bytes, ...] = ()

    def verify_entry(self, entry: ConversationLogEntry) -> str:
        # Recompute signature under each candidate key; first that matches the
        # entry's stored signature wins. Mirrors a real BT6 catalog walk.
        from pipeline.logician.conversation_log import signing_payload

        payload = signing_payload(entry)
        if entry.session_key_signature in (b"",):
            return "INVALID"
        for k in self.invalid_keys:
            if hmac.new(k, payload, hashlib.sha3_512).digest() == entry.session_key_signature:
                return "INVALID"
        for k in self.active_keys:
            if hmac.new(k, payload, hashlib.sha3_512).digest() == entry.session_key_signature:
                return "ACTIVE"
        for k in self.retired_keys:
            if hmac.new(k, payload, hashlib.sha3_512).digest() == entry.session_key_signature:
                return "RETIRED"
        return "WRONG_KEY"


# ---------------------------------------------------------------------------
# Dossier verify — signoff snapshot + live state builders
# ---------------------------------------------------------------------------


def make_dossier_signoff(
    *,
    canonical_path: str = "/orgs/mycosymbiotics_cooperative/dossier/entities/alpha.md",
    inode: int = 4242,
    content_hash: str = DOSSIER_HASH_FIXTURE,
    operator_id: str = "op-1",
    signed_at_utc: str = "2026-04-22T07:00:00Z",
    expires_at_utc: str = "2026-12-31T23:59:59Z",
    operator_signature: bytes = b"\xa0" * 64,
) -> DossierSignoffSnapshot:
    return DossierSignoffSnapshot(
        signed_at_utc=signed_at_utc,
        operator_id=operator_id,
        signed_canonical_path=canonical_path,
        signed_inode=inode,
        signed_content_hash=content_hash,
        operator_signature=operator_signature,
        expires_at_utc=expires_at_utc,
    )


def make_dossier_live(
    *,
    canonical_path: str = "/orgs/mycosymbiotics_cooperative/dossier/entities/alpha.md",
    inode: int = 4242,
    content_hash: str = DOSSIER_HASH_FIXTURE,
) -> DossierLiveState:
    return DossierLiveState(
        canonical_path=canonical_path,
        inode=inode,
        content_hash=content_hash,
    )


# ---------------------------------------------------------------------------
# Cedar entity convenience builders
# ---------------------------------------------------------------------------


def make_session_entity(
    *,
    session_id: str = "sess-l",
    org_slug: str = "mycosymbiotics_cooperative",
    org_root_hash: str = "o" * 128,
    byok_key_id: str = "key-myco-1",
    started_at_utc: str = "2026-04-22T08:00:00Z",
) -> SessionEntity:
    return SessionEntity(
        session_id=session_id,
        org_slug=org_slug,
        org_root_hash=org_root_hash,
        byok_key_id=byok_key_id,
        started_at_utc=started_at_utc,
    )


def make_vault_path_entity(
    *,
    canonical_path: str = "/orgs/mycosymbiotics_cooperative/vault/x.md",
    inode: int = 12345,
    volume_uuid: str = "vol-uuid-abcd",
    org_slug_hint: str = "mycosymbiotics_cooperative",
    is_shared: bool = False,
) -> VaultPathEntity:
    return VaultPathEntity(
        canonical_path=canonical_path,
        inode=inode,
        volume_uuid=volume_uuid,
        org_slug_hint=org_slug_hint,
        is_shared=is_shared,
    )


def make_keyring_key(
    *, key_id: str = "key-myco-1", bound_org_slug: str = "mycosymbiotics_cooperative"
) -> OperatorKeyringKeyEntity:
    return OperatorKeyringKeyEntity(
        key_id=key_id,
        bound_org_slug=bound_org_slug,
    )


def make_claim_entity(
    *,
    claim_id: str = "claim-1",
    tag: str = "DOC_SOURCED",
    source_kind: str = "RFA",
    cross_org_dossier: bool = False,
) -> ClaimEntity:
    return ClaimEntity(
        claim_id=claim_id,
        tag=tag,
        source_kind=source_kind,
        cross_org_dossier=cross_org_dossier,
    )


# ---------------------------------------------------------------------------
# Capturing vault_write — captures intent + canonical bytes per call
# ---------------------------------------------------------------------------


@dataclass
class CapturingVaultWrite:
    """Mock §2 vault_write capturing the canonical-bytes contract.

    Every recorded call carries ``intent`` + ``canonical_bytes`` + ``path``;
    test assertions walk this list to verify §4.4.1 step 12 atomic-write
    semantics WITHOUT touching disk.
    """

    calls: list[dict] = field(default_factory=list)

    def write(
        self,
        *,
        intent: str,
        path: str,
        canonical_bytes: bytes,
        org_slug: str = "",
        session_id: str = "",
    ) -> dict:
        record = {
            "intent": intent,
            "path": path,
            "canonical_bytes": canonical_bytes,
            "org_slug": org_slug,
            "session_id": session_id,
            "sha3_512_hex": hashlib.sha3_512(canonical_bytes).hexdigest(),
        }
        self.calls.append(record)
        return record


# ---------------------------------------------------------------------------
# Rails report HMAC sign / verify — BT13 modeling
# ---------------------------------------------------------------------------


def sign_rails_report(body: bytes, key: bytes = SESSION_HMAC_KEY_ACTIVE) -> bytes:
    """HMAC-SHA3-512(body, per-session key)."""

    return hmac.new(key, body, hashlib.sha3_512).digest()


def verify_rails_report(body: bytes, signature: bytes, key: bytes) -> bool:
    """Constant-time HMAC verify (mirrors BT6 active-key compare)."""

    expected = hmac.new(key, body, hashlib.sha3_512).digest()
    return hmac.compare_digest(expected, signature)


def canonical_rails_report_bytes(report: dict) -> bytes:
    """Canonical-JSON bytes recipe (sorted, compact, UTF-8)."""

    return json.dumps(
        report, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


# ---------------------------------------------------------------------------
# Admin-risk monotonicity helper
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class AdminRiskCounters:
    """In-memory admin-risk register monotonicity tracker.

    Logician's M8 contract: cumulative_low / cumulative_medium / cumulative_high
    never decrease across appends. Round 1 verifies on disk; here we model the
    invariant in memory so the property tests can exercise monotonicity
    directly without spinning up a real ledger.
    """

    cumulative_low: int = 0
    cumulative_medium: int = 0
    cumulative_high: int = 0

    def append(self, severity: str) -> "AdminRiskCounters":
        if severity == "GREEN":
            return AdminRiskCounters(
                cumulative_low=self.cumulative_low + 1,
                cumulative_medium=self.cumulative_medium,
                cumulative_high=self.cumulative_high,
            )
        if severity == "YELLOW":
            return AdminRiskCounters(
                cumulative_low=self.cumulative_low,
                cumulative_medium=self.cumulative_medium + 1,
                cumulative_high=self.cumulative_high,
            )
        if severity == "RED":
            return AdminRiskCounters(
                cumulative_low=self.cumulative_low,
                cumulative_medium=self.cumulative_medium,
                cumulative_high=self.cumulative_high + 1,
            )
        raise ValueError(f"unknown severity {severity!r}")

    def dominates(self, prior: "AdminRiskCounters") -> bool:
        """True iff every counter has not decreased relative to ``prior``."""

        return (
            self.cumulative_low >= prior.cumulative_low
            and self.cumulative_medium >= prior.cumulative_medium
            and self.cumulative_high >= prior.cumulative_high
        )


# ---------------------------------------------------------------------------
# Clean LogicianGateRunner factory
# ---------------------------------------------------------------------------


def fresh_runner() -> LogicianGateRunner:
    """A fresh runner in PRE state, no PRE/POST results yet."""

    return LogicianGateRunner()


__all__ = [
    "SESSION_HMAC_KEY_ACTIVE",
    "SESSION_HMAC_KEY_RETIRED",
    "SESSION_HMAC_KEY_WRONG",
    "DRAFT_HASH_FIXTURE",
    "RFA_HASH_FIXTURE",
    "RFA_URL_HASH_FIXTURE",
    "LEDGER_HEAD_FIXTURE",
    "DOSSIER_HASH_FIXTURE",
    "AdminRiskCounters",
    "CapturingVaultWrite",
    "RotationAwareSessionKeyVerifier",
    "build_genesis_chain",
    "canonical_rails_report_bytes",
    "cedar_signature_verifier_fail",
    "cedar_signature_verifier_pass",
    "default_caller_post_outcomes",
    "default_caller_pre_outcomes",
    "default_post_input",
    "default_pre_input",
    "fresh_runner",
    "hmac_signer",
    "make_claim_entity",
    "make_doc_sourced_claim",
    "make_dossier_live",
    "make_dossier_signoff",
    "make_keyring_key",
    "make_post_step_fail",
    "make_post_step_pass",
    "make_pre_check_fail",
    "make_pre_check_pass",
    "make_session_entity",
    "make_signed_cedar_policy",
    "make_unsourced_claim",
    "make_user_data_claim",
    "make_vault_path_entity",
    "sign_rails_report",
    "verify_rails_report",
]
