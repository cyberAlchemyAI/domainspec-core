"""Tests for the 13 R-DATACOLLECTOR-* AST-lint extensions (Slice 3).

Per §13 v1 LOCKED 2026-05-10 §13.16.6.4 final AST-lint roster + WS-I Code
phase Slice 3 handoff (2026-05-10 evening).

Each rule has at least one positive (forbidden pattern fires) and one
negative (admissible pattern passes) test. Most rules have multiple
positive cases covering the closure dispositions enumerated in
§13.16.1 / §13.16.6.

All rule fixtures live under tmp_path / "pipeline" / "orchestrator" /
"seats" / "data_collector" / so the rule glob matches. The
``_dc_path(tmp_path, name)`` helper produces the canonical fixture
location.
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest

from pipeline.linting.ast_lint import DEFAULT_RULES, lint_tree
from pipeline.linting.r_datacollector_slice_3 import (
    ALL_RULES,
    DATACOLLECTOR_TARGET_GLOB,
    OUTBOUND_BATCH_FILENAME,
    PROHIBITED_ENV_VAR_NAMES,
    BENEFICIARY_CONSENT_TIER_LITERALS,
    R_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER_ENUM,
    R_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER_REQUIRED,
    R_DATACOLLECTOR_CARD_MANDATORY_SIG_VERIFY,
    R_DATACOLLECTOR_CARD_SAFE_LOAD,
    R_DATACOLLECTOR_CEDAR_NO_CATCH,
    R_DATACOLLECTOR_CIC_CLC_ORTHOGONALITY,
    R_DATACOLLECTOR_ENV_VAR_PROHIBIT_BYPASS,
    R_DATACOLLECTOR_NO_AUTOSEND,
    R_DATACOLLECTOR_NO_CULTIVATOR_LEDGER_IMPORT,
    R_DATACOLLECTOR_NO_RAW_TELEGRAM_BOT_IMPORT,
    R_DATACOLLECTOR_ORGSCOPEDBOT_FINAL,
    R_DATACOLLECTOR_TOKEN_NONCE_UNIQUE,
    R_DATACOLLECTOR_VAULT_INTENT_REQUIRED,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------


def _write(path: Path, source: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(source).lstrip("\n"), encoding="utf-8")
    return path


def _dc_path(tmp_path: Path, name: str) -> Path:
    """Return the canonical Data Collector fixture path for `name`."""
    return (
        tmp_path
        / "pipeline"
        / "orchestrator"
        / "seats"
        / "data_collector"
        / name
    )


def _dc_root(tmp_path: Path) -> Path:
    return tmp_path / "pipeline" / "orchestrator" / "seats" / "data_collector"


# ---------------------------------------------------------------------------
# Sanity: 13 rules registered + present in DEFAULT_RULES
# ---------------------------------------------------------------------------


def test_all_rules_thirteen():
    assert len(ALL_RULES) == 13


def test_all_rules_registered_in_default_rules():
    names_in_default = {r.name for r in DEFAULT_RULES}
    for rule in ALL_RULES:
        assert rule.name in names_in_default, (
            f"{rule.name!r} missing from DEFAULT_RULES"
        )


def test_all_rules_target_data_collector_glob():
    for rule in ALL_RULES:
        assert rule.target_glob == DATACOLLECTOR_TARGET_GLOB


# ===========================================================================
# 1. R-DATACOLLECTOR-NO-AUTOSEND
# ===========================================================================


@pytest.mark.parametrize(
    "channel",
    ["email", "sms", "voice", "telegram", "whatsapp"],
)
def test_no_autosend_fires_on_channel_send_outside_dispatcher(
    tmp_path: Path, channel: str
):
    """``<channel>_channel.send(...)`` outside outbound_batch.py fires."""
    src = f"""
    import {channel}_channel

    def smuggler():
        return {channel}_channel.send(message=None, operator_batch_signature=None)
    """
    _write(_dc_path(tmp_path, "smuggler.py"), src)
    violations = lint_tree(_dc_root(tmp_path), [R_DATACOLLECTOR_NO_AUTOSEND])
    assert len(violations) == 1
    v = violations[0]
    assert v.rule_name == "R-DATACOLLECTOR-NO-AUTOSEND"
    assert v.reason_tag == "datacollector_autosend_attempted"
    assert f"{channel}_channel.send" in v.message


def test_no_autosend_skips_outbound_batch_file(tmp_path: Path):
    """outbound_batch.py is the canonical dispatcher; calls there pass."""
    src = """
    import email_channel

    def dispatch_after_operator_approval():
        return email_channel.send(message=None, operator_batch_signature=None)
    """
    _write(_dc_path(tmp_path, OUTBOUND_BATCH_FILENAME), src)
    violations = lint_tree(_dc_root(tmp_path), [R_DATACOLLECTOR_NO_AUTOSEND])
    assert violations == []


def test_no_autosend_clean_module_passes(tmp_path: Path):
    """A module that doesn't call any channel send passes."""
    _write(_dc_path(tmp_path, "clean.py"), "def f(): return 1\n")
    violations = lint_tree(_dc_root(tmp_path), [R_DATACOLLECTOR_NO_AUTOSEND])
    assert violations == []


# ===========================================================================
# 2. R-DATACOLLECTOR-VAULT-INTENT-REQUIRED
# ===========================================================================


def test_vault_intent_required_fires_on_raw_vault_open(tmp_path: Path):
    src = """
    def smuggler():
        with open('orgs/clientA/vault/operational/grants/G/period_1/beneficiary_records/x.yaml', 'rb') as fp:
            return fp.read()
    """
    _write(_dc_path(tmp_path, "vault_open.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_VAULT_INTENT_REQUIRED]
    )
    assert len(violations) == 1
    assert violations[0].rule_name == "R-DATACOLLECTOR-VAULT-INTENT-REQUIRED"
    assert violations[0].reason_tag == "datacollector_raw_open_against_vault_path"


def test_vault_intent_required_passes_non_vault_paths(tmp_path: Path):
    """orgs/<slug>/data_collector/... is NOT a vault path (just DC state)."""
    src = """
    def reader():
        with open('orgs/clientA/data_collector/consent_ledger/r__email.yaml', 'rb') as fp:
            return fp.read()
    """
    _write(_dc_path(tmp_path, "ledger_read.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_VAULT_INTENT_REQUIRED]
    )
    assert violations == []


def test_vault_intent_required_passes_vault_shared_paths(tmp_path: Path):
    """vault_shared/ is workspace-public; not gated by this rule."""
    src = """
    def card_reader():
        with open('vault_shared/state_rules_card/PA.yaml', 'rb') as fp:
            return fp.read()
    """
    _write(_dc_path(tmp_path, "card_open.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_VAULT_INTENT_REQUIRED]
    )
    assert violations == []


# ===========================================================================
# 3. R-DATACOLLECTOR-NO-CULTIVATOR-LEDGER-IMPORT
# ===========================================================================


@pytest.mark.parametrize(
    "import_stmt",
    [
        "import cultivator.consent_ledger",
        "from cultivator.consent_ledger import ConsentEntry",
        "from cultivator import consent_ledger",
        "import cultivator",
    ],
)
def test_no_cultivator_ledger_import_fires(tmp_path: Path, import_stmt: str):
    src = f"""
    {import_stmt}

    def f():
        pass
    """
    _write(_dc_path(tmp_path, "imports.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_NO_CULTIVATOR_LEDGER_IMPORT]
    )
    assert len(violations) == 1
    assert violations[0].rule_name == "R-DATACOLLECTOR-NO-CULTIVATOR-LEDGER-IMPORT"


def test_no_cultivator_ledger_import_passes_clean(tmp_path: Path):
    src = """
    from pipeline.orchestrator.seats.data_collector import ConsentLedgerEntry

    def f():
        return ConsentLedgerEntry
    """
    _write(_dc_path(tmp_path, "clean_import.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_NO_CULTIVATOR_LEDGER_IMPORT]
    )
    assert violations == []


# ===========================================================================
# 4. R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-REQUIRED
# ===========================================================================


def test_beneficiary_consent_tier_required_fires_on_missing_kwarg(
    tmp_path: Path,
):
    src = """
    def writer():
        return BeneficiaryRecord(name="alice", grant_id="G", org_slug="O")
    """
    _write(_dc_path(tmp_path, "writer.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path),
        [R_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER_REQUIRED],
    )
    assert len(violations) == 1
    assert (
        violations[0].rule_name
        == "R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-REQUIRED"
    )


def test_beneficiary_consent_tier_required_passes_with_kwarg(
    tmp_path: Path,
):
    src = """
    def writer():
        return BeneficiaryRecord(
            name="alice",
            grant_id="G",
            org_slug="O",
            consent_tier="my_eyes_only",
        )
    """
    _write(_dc_path(tmp_path, "writer.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path),
        [R_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER_REQUIRED],
    )
    assert violations == []


def test_beneficiary_consent_tier_required_fires_on_write_helper(
    tmp_path: Path,
):
    src = """
    def writer(vault):
        return vault.write_beneficiary_record(record={"name": "alice"})
    """
    _write(_dc_path(tmp_path, "writer2.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path),
        [R_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER_REQUIRED],
    )
    assert len(violations) == 1


# ===========================================================================
# 5. R-DATACOLLECTOR-CIC-CLC-ORTHOGONALITY
# ===========================================================================


@pytest.mark.parametrize(
    "token",
    [
        "FOOD_SYSTEMS",
        "EDUCATOR",
        "PUBLIC_AGENCY",
        "ARTS_CULTURE",
        "COOPERATIVE",
        "ECOSYSTEM_INTERMEDIARY",
        "CIC_FOOD_SYSTEMS",
        "INTERNAL_FOOD_SYSTEMS",
    ],
)
def test_cic_clc_orthogonality_fires_on_each_token(
    tmp_path: Path, token: str
):
    src = f"""
    {token} = "x"

    def f():
        return {token}
    """
    _write(_dc_path(tmp_path, "cic_leak.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_CIC_CLC_ORTHOGONALITY]
    )
    assert len(violations) >= 1
    assert all(
        v.rule_name == "R-DATACOLLECTOR-CIC-CLC-ORTHOGONALITY"
        for v in violations
    )


def test_cic_clc_orthogonality_fires_on_string_literal(tmp_path: Path):
    src = """
    CONFIG = {"archetype": "FOOD_SYSTEMS"}
    """
    _write(_dc_path(tmp_path, "cic_literal.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_CIC_CLC_ORTHOGONALITY]
    )
    assert len(violations) >= 1


def test_cic_clc_orthogonality_passes_clean(tmp_path: Path):
    src = """
    CONFIG = {"channel": "email"}

    def f():
        return CONFIG
    """
    _write(_dc_path(tmp_path, "clean.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_CIC_CLC_ORTHOGONALITY]
    )
    assert violations == []


def test_cic_clc_orthogonality_passes_when_token_in_python_comment(
    tmp_path: Path,
):
    """The lexical scanner strips ``#`` comments — references in comments
    do NOT fire."""
    src = """
    # FOOD_SYSTEMS is one of six CICs; this comment must NOT fire.
    def f():
        return "ok"
    """
    _write(_dc_path(tmp_path, "comment_only.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_CIC_CLC_ORTHOGONALITY]
    )
    assert violations == []


# ===========================================================================
# 6. R-DATACOLLECTOR-NO-RAW-TELEGRAM-BOT-IMPORT
# ===========================================================================


@pytest.mark.parametrize(
    "import_stmt",
    [
        "from telegram import Bot",
        "from telegram.ext import Application",
        "import telegram",
        "import pyrogram",
        "from pyrogram import Client",
        "import telethon",
        "from telethon import TelegramClient",
    ],
)
def test_no_raw_telegram_bot_import_fires(tmp_path: Path, import_stmt: str):
    src = f"""
    {import_stmt}
    """
    _write(_dc_path(tmp_path, "tg_smuggler.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path),
        [R_DATACOLLECTOR_NO_RAW_TELEGRAM_BOT_IMPORT],
    )
    assert len(violations) == 1
    assert (
        violations[0].rule_name
        == "R-DATACOLLECTOR-NO-RAW-TELEGRAM-BOT-IMPORT"
    )


def test_no_raw_telegram_bot_import_passes_for_orgscoped_bot(
    tmp_path: Path,
):
    """OrgScopedBot import (from the DC seat package) is fine — only raw
    telegram library imports are rejected."""
    src = """
    from pipeline.orchestrator.seats.data_collector.telegram_channel import OrgScopedBot
    """
    _write(_dc_path(tmp_path, "uses_orgscoped.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path),
        [R_DATACOLLECTOR_NO_RAW_TELEGRAM_BOT_IMPORT],
    )
    assert violations == []


# ===========================================================================
# 7. R-DATACOLLECTOR-CARD-MANDATORY-SIG-VERIFY
# ===========================================================================


def test_card_mandatory_sig_verify_fires_on_raw_card_open(
    tmp_path: Path,
):
    src = """
    def smuggler():
        with open('vault_shared/state_rules_card/PA.yaml', 'rb') as fp:
            return fp.read()
    """
    _write(_dc_path(tmp_path, "raw_card.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path),
        [R_DATACOLLECTOR_CARD_MANDATORY_SIG_VERIFY],
    )
    assert len(violations) == 1
    assert (
        violations[0].rule_name
        == "R-DATACOLLECTOR-CARD-MANDATORY-SIG-VERIFY"
    )


def test_card_mandatory_sig_verify_passes_state_rules_card_file(
    tmp_path: Path,
):
    """The canonical state_rules_card.py loader is allowed to open."""
    src = """
    def load_state_card(card_dir, state_code):
        path = card_dir / f"{state_code}.yaml"
        with open('vault_shared/state_rules_card/PA.yaml', 'rb') as fp:
            return fp.read()
    """
    _write(_dc_path(tmp_path, "state_rules_card.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path),
        [R_DATACOLLECTOR_CARD_MANDATORY_SIG_VERIFY],
    )
    assert violations == []


# ===========================================================================
# 8. R-DATACOLLECTOR-CARD-SAFE-LOAD
# ===========================================================================


def test_card_safe_load_fires_on_yaml_load(tmp_path: Path):
    src = """
    import yaml

    def smuggler(fp):
        return yaml.load(fp)
    """
    _write(_dc_path(tmp_path, "unsafe.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_CARD_SAFE_LOAD]
    )
    assert len(violations) == 1
    assert violations[0].rule_name == "R-DATACOLLECTOR-CARD-SAFE-LOAD"


def test_card_safe_load_passes_for_yaml_safe_load(tmp_path: Path):
    src = """
    import yaml

    def reader(fp):
        return yaml.safe_load(fp)
    """
    _write(_dc_path(tmp_path, "safe.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_CARD_SAFE_LOAD]
    )
    assert violations == []


# ===========================================================================
# 9. R-DATACOLLECTOR-ORGSCOPEDBOT-FINAL
# ===========================================================================


def test_orgscopedbot_final_fires_on_subclass(tmp_path: Path):
    src = """
    class MyBot(OrgScopedBot):
        pass
    """
    _write(_dc_path(tmp_path, "subclass.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_ORGSCOPEDBOT_FINAL]
    )
    assert len(violations) == 1
    assert violations[0].rule_name == "R-DATACOLLECTOR-ORGSCOPEDBOT-FINAL"


def test_orgscopedbot_final_fires_on_attribute_base_subclass(tmp_path: Path):
    """``class X(tg.OrgScopedBot)`` — qualified base name still fires."""
    src = """
    import telegram_channel as tg

    class MyBot(tg.OrgScopedBot):
        pass
    """
    _write(_dc_path(tmp_path, "subclass_attr.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_ORGSCOPEDBOT_FINAL]
    )
    assert len(violations) == 1


def test_orgscopedbot_final_passes_for_class_definition_itself(
    tmp_path: Path,
):
    """Defining ``class OrgScopedBot`` is fine — only subclasses are
    rejected."""
    src = """
    from typing import final

    @final
    class OrgScopedBot:
        pass
    """
    _write(_dc_path(tmp_path, "telegram_channel.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_ORGSCOPEDBOT_FINAL]
    )
    assert violations == []


# ===========================================================================
# 10. R-DATACOLLECTOR-CEDAR-NO-CATCH
# ===========================================================================


def test_cedar_no_catch_fires_on_baseexception_around_dc_import(
    tmp_path: Path,
):
    src = """
    try:
        from pipeline.orchestrator.seats.data_collector import REGISTERED_GATES
    except BaseException:
        REGISTERED_GATES = {}
    """
    _write(_dc_path(tmp_path, "swallow.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_CEDAR_NO_CATCH]
    )
    assert len(violations) == 1
    assert violations[0].rule_name == "R-DATACOLLECTOR-CEDAR-NO-CATCH"


def test_cedar_no_catch_fires_on_bare_except_around_dc_import(
    tmp_path: Path,
):
    src = """
    try:
        from pipeline.orchestrator.seats.data_collector import REGISTERED_GATES
    except:
        REGISTERED_GATES = {}
    """
    _write(_dc_path(tmp_path, "bare.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_CEDAR_NO_CATCH]
    )
    assert len(violations) == 1


def test_cedar_no_catch_passes_for_except_exception(tmp_path: Path):
    """``except Exception`` is allowed because CriticalPolicyError
    subclasses BaseException and so propagates through it."""
    src = """
    try:
        from pipeline.orchestrator.seats.data_collector import REGISTERED_GATES
    except Exception:
        REGISTERED_GATES = {}
    """
    _write(_dc_path(tmp_path, "ok.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_CEDAR_NO_CATCH]
    )
    assert violations == []


def test_cedar_no_catch_passes_for_unrelated_baseexception(tmp_path: Path):
    """``except BaseException`` is fine if the try-block does NOT import a
    DC module."""
    src = """
    try:
        x = 1 / 0
    except BaseException:
        pass
    """
    _write(_dc_path(tmp_path, "elsewhere.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_CEDAR_NO_CATCH]
    )
    assert violations == []


# ===========================================================================
# 11. R-DATACOLLECTOR-TOKEN-NONCE-UNIQUE
# ===========================================================================


def test_token_nonce_unique_fires_on_constant_nonce(tmp_path: Path):
    src = """
    def smuggler(aead, plaintext):
        return aead.encrypt(b'\\x00' * 12, plaintext, None)
    """
    _write(_dc_path(tmp_path, "bad_nonce.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_TOKEN_NONCE_UNIQUE]
    )
    assert len(violations) == 1
    assert violations[0].rule_name == "R-DATACOLLECTOR-TOKEN-NONCE-UNIQUE"


def test_token_nonce_unique_passes_for_urandom_nonce(tmp_path: Path):
    src = """
    import os

    def encryptor(aead, plaintext, aad):
        nonce = os.urandom(12)
        return aead.encrypt(nonce, plaintext, aad)
    """
    _write(_dc_path(tmp_path, "ok_nonce.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_TOKEN_NONCE_UNIQUE]
    )
    assert violations == []


# ===========================================================================
# 12. R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-ENUM
# ===========================================================================


def test_consent_tier_enum_fires_on_str_annotation(tmp_path: Path):
    src = """
    from dataclasses import dataclass

    @dataclass
    class BadRecord:
        consent_tier: str = "x"
    """
    _write(_dc_path(tmp_path, "bad_enum.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path),
        [R_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER_ENUM],
    )
    assert len(violations) == 1
    assert (
        violations[0].rule_name
        == "R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-ENUM"
    )


def test_consent_tier_enum_passes_for_canonical_literal(tmp_path: Path):
    src = """
    from typing import Literal
    from dataclasses import dataclass

    @dataclass
    class GoodRecord:
        consent_tier: Literal["my_eyes_only", "matchable_to_opportunities", "composable_with_others"] = "my_eyes_only"
    """
    _write(_dc_path(tmp_path, "good_enum.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path),
        [R_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER_ENUM],
    )
    assert violations == []


def test_consent_tier_enum_fires_on_wrong_literal_set(tmp_path: Path):
    """The annotation must match the v7.0.5 §6 enumerated set exactly."""
    src = """
    from typing import Literal
    from dataclasses import dataclass

    @dataclass
    class WrongEnum:
        consent_tier: Literal["public", "private"] = "public"
    """
    _write(_dc_path(tmp_path, "wrong_set.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path),
        [R_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER_ENUM],
    )
    assert len(violations) == 1


# ===========================================================================
# 13. R-DATACOLLECTOR-ENV-VAR-PROHIBIT-BYPASS
# ===========================================================================


@pytest.mark.parametrize("env_var_name", PROHIBITED_ENV_VAR_NAMES)
def test_env_var_prohibit_bypass_fires_on_prohibited_read(
    tmp_path: Path, env_var_name: str
):
    """Any reference to a prohibited env-var name outside the denylist
    literal fires."""
    src = f"""
    import os

    def smuggler():
        return os.environ.get({env_var_name!r})
    """
    _write(_dc_path(tmp_path, "env_smuggler.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_ENV_VAR_PROHIBIT_BYPASS]
    )
    assert len(violations) >= 1


def test_env_var_prohibit_bypass_passes_for_denylist_literal(tmp_path: Path):
    """The denylist literal itself (``("DC_AUTO", "DC_YES", ...)``) is the
    legitimate place where prohibited env-var names appear."""
    src = """
    PROHIBITED = (
        "DC_AUTO",
        "DC_YES",
        "DC_FORCE",
        "DATACOLLECTOR_AUTO_CONFIRM",
        "DATACOLLECTOR_YES",
        "DATACOLLECTOR_FORCE",
    )

    def reject_env_overrides(env):
        for name in PROHIBITED:
            if name in env:
                raise RuntimeError(f"prohibited env: {name}")
    """
    _write(_dc_path(tmp_path, "validator.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_ENV_VAR_PROHIBIT_BYPASS]
    )
    assert violations == []


def test_env_var_prohibit_bypass_passes_for_unrelated_string(tmp_path: Path):
    """Unrelated string literals don't trigger the rule."""
    src = """
    def f():
        return "channel_name"
    """
    _write(_dc_path(tmp_path, "unrelated.py"), src)
    violations = lint_tree(
        _dc_root(tmp_path), [R_DATACOLLECTOR_ENV_VAR_PROHIBIT_BYPASS]
    )
    assert violations == []


# ===========================================================================
# Live-tree cleanliness — every rule passes against the post-Slice-2 tree
# ===========================================================================


def test_all_slice_3_rules_clean_on_live_tree():
    """Slice 3 rules MUST pass against the live tree at commit time."""
    target = REPO_ROOT / "pipeline" / "orchestrator" / "seats" / "data_collector"
    violations = lint_tree(target, list(ALL_RULES))
    assert violations == [], (
        f"Slice 3 lint rules fired on the live Data Collector tree: "
        + "\n".join(f"{v.file}:{v.line}: {v.rule_name} [{v.reason_tag}]" for v in violations)
    )
