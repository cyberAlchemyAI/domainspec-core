"""Unit tests for pipeline.vault.vault_write (§3.5 + §4.10 + §4.10.4 + §4.10.6 + §7.17.8).

Round P — SIMPLE-intent dispatcher across all three commit modes.

Covers:
* overwrite: first-write, replace-existing, hash on ack (``rails-report-write``).
* write-if-absent: success on fresh, F-VAULT-WRITE-EXISTS on collision
  (``claim-evidence-write``).
* append-cas: empty + nonempty head, hash match, mismatch raises
  F-VAULT-CAS-HEAD-MISMATCH (``admin-risk-append``).
* Cross-org rejection.
* Cedar-callback veto.
* Arg-type + write_mode validation.
* fcntl lock held during commit (best-effort by running under single thread).

v7.1 Batch 3 remediation — additional coverage:
* §4.10.4 post-gate allowlist: unknown intent → post_gate_unknown_intent;
  path-prefix mismatch → post_gate_path_mismatch; wrong mode for allowed
  intent → post_gate_mode_mismatch.
* §4.10.4 step 4.5 type-validation preamble: non-str intent / non-Path path
  / non-str write_mode all surface as :class:`CedarSection4WritePathDenied`
  with ``type_error=<T>`` on the exception (not as bare ``TypeError``).
* §4.10.6 kind-class hard-gate: SIMPLE intent + txn_token →
  ``F-VAULT-28.simple_intent_with_txn_token``; COMPOUND intent without
  txn_token → ``F-VAULT-28.compound_intent_without_txn_token``; COMPOUND
  intent + txn_token passes the gate (subsequent post-gate validation
  applies).
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

import pytest

from pipeline.vault.error_codes import (
    CedarSection4WritePathDenied,
    VaultCASHeadMismatch,
    VaultCompoundProtocolViolation,
    VaultCrossOrgAccess,
    VaultWriteDenied,
    VaultWriteExists,
)
from pipeline.vault.vault_write import (
    EMPTY_SHA3_512_HEX,
    POST_GATE_ALLOWLIST,
    PostGateAllowlistEntry,
    VaultWriteAck,
    WRITE_MODES,
    vault_write,
)


@pytest.fixture
def org(tmp_path: Path) -> dict[str, Path]:
    vault_root = tmp_path / "orgs" / "myco" / "vault"
    vault_root.mkdir(parents=True, exist_ok=True)
    return {
        "root": vault_root,
        "lock": vault_root / ".write.lock",
        # Per-subpath canonical targets. Each matches its intent's
        # §4.10.4 v7.1 allowlist suffix.
        "rails_target": vault_root / "rails_reports" / "r001.json",
        "claim_target": vault_root / "claim_evidence" / "claim001.json",
        "admin_target": vault_root / "admin_risk" / "ledger.jsonl",
        "convo_target": vault_root / "conversation_log" / "c001.log",
        "lessons_target": vault_root / "lessons_delta" / "l001.jsonl",
    }


def _call_rails(
    org: dict[str, Path],
    payload: bytes,
    *,
    target: Path | None = None,
    cedar_decide=None,
) -> VaultWriteAck:
    """Canonical overwrite-mode write (``rails-report-write``)."""
    return vault_write(
        target or org["rails_target"],
        payload,
        "rails-report-write",
        "sess-1",
        "myco",
        org_vault_root=org["root"],
        write_lock_path=org["lock"],
        write_mode="overwrite",
        cedar_decide=cedar_decide,
    )


def _call_claim(
    org: dict[str, Path],
    payload: bytes,
    *,
    target: Path | None = None,
) -> VaultWriteAck:
    """Canonical write-if-absent write (``claim-evidence-write``)."""
    return vault_write(
        target or org["claim_target"],
        payload,
        "claim-evidence-write",
        "sess-1",
        "myco",
        org_vault_root=org["root"],
        write_lock_path=org["lock"],
        write_mode="write-if-absent",
    )


def _call_admin(
    org: dict[str, Path],
    payload: bytes,
    *,
    expected: str,
    target: Path | None = None,
) -> VaultWriteAck:
    """Canonical append-cas write (``admin-risk-append``)."""
    return vault_write(
        target or org["admin_target"],
        payload,
        "admin-risk-append",
        "sess-1",
        "myco",
        org_vault_root=org["root"],
        write_lock_path=org["lock"],
        write_mode="append-cas",
        expected_current_file_hash=expected,
    )


# ---------------------------------------------------------------------------
# overwrite (rails-report-write)
# ---------------------------------------------------------------------------


class TestOverwrite:
    def test_first_write_creates_file(self, org) -> None:
        ack = _call_rails(org, b"hello")
        assert org["rails_target"].read_bytes() == b"hello"
        assert ack.committed is True
        assert ack.mode == "overwrite"
        assert ack.post_commit_hash == hashlib.sha3_512(b"hello").hexdigest()

    def test_second_write_replaces(self, org) -> None:
        _call_rails(org, b"one")
        _call_rails(org, b"two")
        assert org["rails_target"].read_bytes() == b"two"


# ---------------------------------------------------------------------------
# write-if-absent (claim-evidence-write)
# ---------------------------------------------------------------------------


class TestWriteIfAbsent:
    def test_success_on_fresh_target(self, org) -> None:
        ack = _call_claim(org, b"fresh")
        assert ack.committed is True
        assert ack.mode == "write-if-absent"
        assert org["claim_target"].read_bytes() == b"fresh"

    def test_collision_raises(self, org) -> None:
        _call_claim(org, b"first")
        with pytest.raises(VaultWriteExists):
            _call_claim(org, b"second")
        # Target must remain the first write.
        assert org["claim_target"].read_bytes() == b"first"


# ---------------------------------------------------------------------------
# append-cas (admin-risk-append)
# ---------------------------------------------------------------------------


class TestAppendCAS:
    def test_append_on_empty_matches_empty_hash(self, org) -> None:
        ack = _call_admin(org, b"entry1\n", expected=EMPTY_SHA3_512_HEX)
        assert ack.committed is True
        assert org["admin_target"].read_bytes() == b"entry1\n"

    def test_append_on_empty_accepts_empty_string_alias(self, org) -> None:
        # Blueprint says "" is normalized to the empty-hash constant.
        ack = _call_admin(org, b"entry1\n", expected="")
        assert ack.committed is True

    def test_append_matches_current_head(self, org) -> None:
        _call_admin(org, b"entry1\n", expected=EMPTY_SHA3_512_HEX)
        head = hashlib.sha3_512(b"entry1\n").hexdigest()
        ack = _call_admin(org, b"entry2\n", expected=head)
        assert org["admin_target"].read_bytes() == b"entry1\nentry2\n"
        assert ack.pre_append_hash == head

    def test_mismatched_head_raises(self, org) -> None:
        _call_admin(org, b"entry1\n", expected=EMPTY_SHA3_512_HEX)
        with pytest.raises(VaultCASHeadMismatch) as exc:
            _call_admin(org, b"entry2\n", expected="0" * 128)
        assert exc.value.expected_current_file_hash == "0" * 128
        actual = hashlib.sha3_512(b"entry1\n").hexdigest()
        assert exc.value.actual_current_file_hash == actual

    def test_case_insensitive_hash_match(self, org) -> None:
        ack = _call_admin(
            org,
            b"e\n",
            expected=EMPTY_SHA3_512_HEX.upper(),
        )
        assert ack.committed is True


# ---------------------------------------------------------------------------
# Cedar veto
# ---------------------------------------------------------------------------


class TestCedar:
    def test_veto_raises_write_denied(self, org) -> None:
        with pytest.raises(VaultWriteDenied):
            _call_rails(org, b"x", cedar_decide=lambda *_: False)

    def test_accept_proceeds(self, org) -> None:
        ack = _call_rails(org, b"x", cedar_decide=lambda *_: True)
        assert ack.committed is True


# ---------------------------------------------------------------------------
# Cross-org
# ---------------------------------------------------------------------------


class TestCrossOrg:
    def test_outside_org_root_raises(self, tmp_path: Path, org) -> None:
        other = tmp_path / "orgs" / "other_org" / "vault"
        other.mkdir(parents=True, exist_ok=True)
        with pytest.raises(VaultCrossOrgAccess):
            vault_write(
                other / "rails_reports" / "leak.json",
                b"x",
                "rails-report-write",
                "sess",
                "myco",
                org_vault_root=org["root"],
                write_lock_path=org["lock"],
                write_mode="overwrite",
            )


# ---------------------------------------------------------------------------
# Arg-type / mode validation
# ---------------------------------------------------------------------------


class TestArgTypes:
    def test_unknown_mode_rejected(self, org) -> None:
        with pytest.raises(ValueError):
            vault_write(
                org["rails_target"],
                b"x",
                "rails-report-write",
                "sess",
                "myco",
                org_vault_root=org["root"],
                write_lock_path=org["lock"],
                write_mode="bogus",
            )

    def test_append_cas_without_expected_rejected(self, org) -> None:
        with pytest.raises(ValueError):
            vault_write(
                org["admin_target"],
                b"x",
                "admin-risk-append",
                "sess",
                "myco",
                org_vault_root=org["root"],
                write_lock_path=org["lock"],
                write_mode="append-cas",
                expected_current_file_hash=None,
            )

    def test_expected_forbidden_in_overwrite(self, org) -> None:
        with pytest.raises(ValueError):
            vault_write(
                org["rails_target"],
                b"x",
                "rails-report-write",
                "sess",
                "myco",
                org_vault_root=org["root"],
                write_lock_path=org["lock"],
                write_mode="overwrite",
                expected_current_file_hash=EMPTY_SHA3_512_HEX,
            )

    def test_path_must_be_path(self, org) -> None:
        with pytest.raises(TypeError):
            vault_write(
                str(org["rails_target"]),  # type: ignore[arg-type]
                b"x",
                "rails-report-write",
                "s",
                "myco",
                org_vault_root=org["root"],
                write_lock_path=org["lock"],
            )

    def test_bytes_must_be_bytes(self, org) -> None:
        with pytest.raises(TypeError):
            vault_write(
                org["rails_target"],
                "not-bytes",  # type: ignore[arg-type]
                "rails-report-write",
                "s",
                "myco",
                org_vault_root=org["root"],
                write_lock_path=org["lock"],
            )


# ---------------------------------------------------------------------------
# WRITE_MODES contract
# ---------------------------------------------------------------------------


class TestWriteModes:
    def test_exact_set(self) -> None:
        assert WRITE_MODES == frozenset(
            {"overwrite", "write-if-absent", "append-cas"}
        )


# ---------------------------------------------------------------------------
# §4.10.4 v7.1 — post-gate path-allowlist (22-vector matrix per §7.17.8)
# ---------------------------------------------------------------------------


# The §7.17.8 v7 vector matrix: 5 SIMPLE intents × 4 off-by-one path
# permutations + 2 type-error vectors = 22 deny cases.
#
# Each row: (intent, permitted_mode, build_path_fn, expected_reason,
# expected_type_error_or_empty).
#
# ``build_path_fn(vault_root) -> Path`` produces a path that SHOULD fail the
# post-gate for the given intent.

def _swap_prefix(vault_root: Path, correct_suffix: str, wrong_suffix: str) -> Path:
    """Point at another SIMPLE-allowlisted directory under the same vault."""
    return vault_root / wrong_suffix / "x.bin"


_SIMPLE_INTENTS_AND_MODES: tuple[tuple[str, str, str], ...] = (
    ("claim-evidence-write", "write-if-absent", "claim_evidence/"),
    ("admin-risk-append", "append-cas", "admin_risk/"),
    ("conversation-log-append", "overwrite", "conversation_log/"),
    ("rails-report-write", "overwrite", "rails_reports/"),
    ("lessons-delta-append", "append-cas", "lessons_delta/"),
)


def _mismatch_path_permutations(
    vault_root: Path, intent: str, correct_suffix: str
) -> list[tuple[str, Path]]:
    """Four off-by-one permutations per intent, all expected to deny."""
    # Swap intent's allowlist dir with another intent's dir.
    other = {
        "claim-evidence-write": "admin_risk/",
        "admin-risk-append": "claim_evidence/",
        "conversation-log-append": "rails_reports/",
        "rails-report-write": "conversation_log/",
        "lessons-delta-append": "claim_evidence/",
    }[intent]
    return [
        (
            "wrong_subdir_but_same_vault",
            vault_root / other / "x.bin",
        ),
        (
            "partial_prefix_typo",
            vault_root / (correct_suffix.rstrip("/") + "_typo") / "x.bin",
        ),
        (
            "missing_subdir_writes_directly_under_vault",
            vault_root / "x.bin",
        ),
        (
            "deeper_wrong_subdir",
            vault_root / "nested" / correct_suffix / "x.bin",
        ),
    ]


class TestPostGateAllowlist:
    """§4.10.4 v7.1 22-vector matrix (§7.17.8)."""

    @pytest.mark.parametrize(
        ("intent", "permitted_mode", "correct_suffix"),
        _SIMPLE_INTENTS_AND_MODES,
    )
    @pytest.mark.parametrize("perm_idx", list(range(4)))
    def test_wrong_path_denied_with_post_gate_path_mismatch(
        self,
        org: dict[str, Path],
        intent: str,
        permitted_mode: str,
        correct_suffix: str,
        perm_idx: int,
    ) -> None:
        perms = _mismatch_path_permutations(
            org["root"], intent, correct_suffix
        )
        _label, wrong_path = perms[perm_idx]
        expected_hash = (
            EMPTY_SHA3_512_HEX if permitted_mode == "append-cas" else None
        )
        with pytest.raises(CedarSection4WritePathDenied) as exc:
            vault_write(
                wrong_path,
                b"x",
                intent,
                "sess",
                "myco",
                org_vault_root=org["root"],
                write_lock_path=org["lock"],
                write_mode=permitted_mode,
                expected_current_file_hash=expected_hash,
            )
        assert exc.value.reason == "post_gate_path_mismatch"
        assert exc.value.attempted_intent == intent

    def test_unknown_intent_denied(self, org: dict[str, Path]) -> None:
        with pytest.raises(CedarSection4WritePathDenied) as exc:
            vault_write(
                org["rails_target"],
                b"x",
                "never-heard-of-this-intent",
                "sess",
                "myco",
                org_vault_root=org["root"],
                write_lock_path=org["lock"],
                write_mode="overwrite",
            )
        assert exc.value.reason == "post_gate_unknown_intent"

    @pytest.mark.parametrize(
        ("intent", "permitted_mode", "correct_suffix"),
        _SIMPLE_INTENTS_AND_MODES,
    )
    def test_wrong_mode_denied(
        self,
        org: dict[str, Path],
        intent: str,
        permitted_mode: str,
        correct_suffix: str,
    ) -> None:
        # Pick a mode that is NOT in the entry's permitted_modes.
        entry = POST_GATE_ALLOWLIST[intent]
        wrong_mode = next(
            iter(WRITE_MODES - entry.permitted_modes), None
        )
        if wrong_mode is None:  # allowlist permits every mode — skip
            pytest.skip(f"{intent} permits every mode")
        target = org["root"] / correct_suffix / "x.bin"
        expected_hash = (
            EMPTY_SHA3_512_HEX if wrong_mode == "append-cas" else None
        )
        with pytest.raises(CedarSection4WritePathDenied) as exc:
            vault_write(
                target,
                b"x",
                intent,
                "sess",
                "myco",
                org_vault_root=org["root"],
                write_lock_path=org["lock"],
                write_mode=wrong_mode,
                expected_current_file_hash=expected_hash,
            )
        assert exc.value.reason == "post_gate_mode_mismatch"

    def test_type_error_intent_none(self, org: dict[str, Path]) -> None:
        """v7 type-error vector #1: intent=None → post_gate_unknown_intent."""
        with pytest.raises(TypeError) as exc:
            vault_write(
                org["rails_target"],
                b"x",
                None,  # type: ignore[arg-type]
                "sess",
                "myco",
                org_vault_root=org["root"],
                write_lock_path=org["lock"],
                write_mode="overwrite",
            )
        # ``_validate_args`` catches this at the pre-Cedar boundary as a
        # caller-facing ``TypeError``. The post-gate type-validation
        # preamble is the belt-and-suspenders second layer — exercised by
        # ``test_post_gate_catches_non_str_intent_when_pre_check_bypassed``
        # below.
        assert "intent" in str(exc.value)

    def test_post_gate_catches_non_str_intent_when_pre_check_bypassed(
        self, org: dict[str, Path], monkeypatch
    ) -> None:
        """Defense-in-depth: if ``_validate_args`` ever lets a non-str
        intent slip past, the §4.10.4 step 4.5 preamble still denies with
        ``CedarSection4WritePathDenied.type_error``. Exercised by
        monkeypatching the pre-check to a no-op."""
        from pipeline.vault import vault_write as _mod

        monkeypatch.setattr(_mod, "_validate_args", lambda **_k: None)
        with pytest.raises(CedarSection4WritePathDenied) as exc:
            vault_write(
                org["rails_target"],
                b"x",
                123,  # type: ignore[arg-type]
                "sess",
                "myco",
                org_vault_root=org["root"],
                write_lock_path=org["lock"],
                write_mode="overwrite",
            )
        assert exc.value.reason == "post_gate_unknown_intent"
        assert exc.value.type_error == "int"

    def test_post_gate_catches_non_path_path_when_pre_check_bypassed(
        self, org: dict[str, Path], monkeypatch
    ) -> None:
        """v7 type-error vector #2: ``path=b"..."`` — post-gate catches with
        ``post_gate_path_mismatch, type_error=bytes`` rather than propagating
        a bare ``TypeError`` from ``str(path).startswith``."""
        from pipeline.vault import vault_write as _mod

        monkeypatch.setattr(_mod, "_validate_args", lambda **_k: None)
        monkeypatch.setattr(_mod, "_within_org_root", lambda *_a: True)
        with pytest.raises(CedarSection4WritePathDenied) as exc:
            vault_write(
                b"orgs/myco/vault/rails_reports/leak.json",  # type: ignore[arg-type]
                b"x",
                "rails-report-write",
                "sess",
                "myco",
                org_vault_root=org["root"],
                write_lock_path=org["lock"],
                write_mode="overwrite",
            )
        assert exc.value.reason == "post_gate_path_mismatch"
        assert exc.value.type_error == "bytes"


# ---------------------------------------------------------------------------
# §4.10.6 v7.1 — dispatcher kind-class hard-gate
# ---------------------------------------------------------------------------


class TestKindClassHardGate:
    def test_simple_with_txn_token_rejected(self, org: dict[str, Path]) -> None:
        with pytest.raises(VaultCompoundProtocolViolation) as exc:
            vault_write(
                org["rails_target"],
                b"x",
                "rails-report-write",
                "sess",
                "myco",
                org_vault_root=org["root"],
                write_lock_path=org["lock"],
                write_mode="overwrite",
                txn_token="fake-token-abc123",
            )
        assert exc.value.sub_reason == "simple_intent_with_txn_token"

    def test_compound_without_txn_token_rejected(
        self, org: dict[str, Path]
    ) -> None:
        # Use the index-amendment-audit-append COMPOUND row since its
        # vault-relative path is exactly reachable in the test vault.
        target = org["root"] / "admin_risk" / "ledger.jsonl"
        with pytest.raises(VaultCompoundProtocolViolation) as exc:
            vault_write(
                target,
                b"stamp\n",
                "index-amendment-audit-append",
                "sess",
                "myco",
                org_vault_root=org["root"],
                write_lock_path=org["lock"],
                write_mode="append-cas",
                expected_current_file_hash=EMPTY_SHA3_512_HEX,
                txn_token=None,
            )
        assert exc.value.sub_reason == "compound_intent_without_txn_token"

    def test_compound_with_txn_token_passes_gate(
        self, org: dict[str, Path]
    ) -> None:
        """With a txn_token, a COMPOUND write proceeds to persist — in v0.1
        the vault_write dispatcher itself honours the persist primitives;
        higher-level orchestration (compound_txn.commit.persist_hook) wires
        the lifecycle."""
        target = org["root"] / "admin_risk" / "ledger.jsonl"
        ack = vault_write(
            target,
            b"stamp\n",
            "index-amendment-audit-append",
            "sess",
            "myco",
            org_vault_root=org["root"],
            write_lock_path=org["lock"],
            write_mode="append-cas",
            expected_current_file_hash=EMPTY_SHA3_512_HEX,
            txn_token="v0.1-compound-txn-token-00000000000000",
        )
        assert ack.committed is True
        assert ack.mode == "append-cas"


# ---------------------------------------------------------------------------
# Allowlist shape contract
# ---------------------------------------------------------------------------


class TestAllowlistShape:
    def test_allowlist_has_fourteen_entries(self) -> None:
        # v7.1 LOCKED: 5 SIMPLE + 2 COMPOUND = 7 entries.
        # v7.2 DRAFT: adds 7 SIMPLE operational sub-kind rows → 14.
        # §17 v1 LOCK 2026-05-11: adds cycle_receipt SIMPLE row → total 15
        # (13 SIMPLE + 2 COMPOUND).
        assert len(POST_GATE_ALLOWLIST) == 15

    def test_allowlist_entry_types(self) -> None:
        for intent, entry in POST_GATE_ALLOWLIST.items():
            assert isinstance(entry, PostGateAllowlistEntry)
            assert entry.kind_class in {"SIMPLE", "COMPOUND"}
            assert entry.permitted_modes.issubset(WRITE_MODES)
            # Exactly one of the two path-shape fields is set.
            has_prefix = entry.vault_relative_prefix is not None
            has_regex = entry.repo_relative_regex_str is not None
            assert has_prefix ^ has_regex, (
                f"{intent}: exactly one of vault_relative_prefix / "
                f"repo_relative_regex_str must be set"
            )

    def test_compound_entries_carry_required_intents(self) -> None:
        compound = {
            k: v
            for k, v in POST_GATE_ALLOWLIST.items()
            if v.kind_class == "COMPOUND"
        }
        assert set(compound.keys()) == {
            "index-update",
            "index-amendment-audit-append",
        }
        for entry in compound.values():
            assert entry.required_intents == (
                "index-update",
                "index-amendment-audit-append",
            )

    def test_simple_entries_have_no_required_intents(self) -> None:
        simple = [
            v for v in POST_GATE_ALLOWLIST.values() if v.kind_class == "SIMPLE"
        ]
        # v7.1 = 5; v7.2 §2.13 adds 7 operational rows → 12.
        # §17 v1 LOCK adds cycle_receipt → 13.
        assert len(simple) == 13
        for entry in simple:
            assert entry.required_intents is None


class TestBlueprintDepsPin:
    def test_blueprint_deps_pin(self) -> None:
        from pipeline.vault import vault_write as _mod

        deps = _mod.BLUEPRINT_DEPS
        assert "section_02_vault_topology.md" in deps
        section = deps["section_02_vault_topology.md"]
        assert section["version"] == "v7.1"
        assert section["hash_sha3_512_prefix16"] == "83a898275a4cf0a1"
        sections = section["sections_implemented"]
        # v7.1 additions must appear.
        assert any("§4.10.4" in s for s in sections)
        assert any("§4.10.6" in s for s in sections)
