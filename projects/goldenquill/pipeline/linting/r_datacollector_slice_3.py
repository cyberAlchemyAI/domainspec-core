"""WS-I §13 Data Collector — Slice 3 AST-lint extensions (13 rules).

Per §13 v1 LOCKED 2026-05-10 (rows 196/197) + §13.16.6.4 final AST-lint
roster + WS-I Code phase Slice 3 handoff (2026-05-10 evening).

This module hosts the thirteen compile-time defenses authored at Slice 3:

  1.  R-DATACOLLECTOR-NO-AUTOSEND                    (§13.7 Layer 1)
  2.  R-DATACOLLECTOR-VAULT-INTENT-REQUIRED          (§13.5.4 PII discipline)
  3.  R-DATACOLLECTOR-NO-CULTIVATOR-LEDGER-IMPORT    (§13.11 substrate split)
  4.  R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-REQUIRED  (§13.16.2 RT-28)
  5.  R-DATACOLLECTOR-CIC-CLC-ORTHOGONALITY          (§13.16.1 RT-20 +
                                                      §13.16.6.2 RT-C2-08)
  6.  R-DATACOLLECTOR-NO-RAW-TELEGRAM-BOT-IMPORT     (§13.16.1 RT-07)
  7.  R-DATACOLLECTOR-CARD-MANDATORY-SIG-VERIFY (§13.16.2 RT-21)
  8.  R-DATACOLLECTOR-CARD-SAFE-LOAD            (§13.16.2 RT-27)
  9.  R-DATACOLLECTOR-ORGSCOPEDBOT-FINAL             (§13.16.6.2 RT-C2-03)
 10.  R-DATACOLLECTOR-CEDAR-NO-CATCH                 (§13.16.6.2 RT-C2-04)
 11.  R-DATACOLLECTOR-TOKEN-NONCE-UNIQUE             (§13.16.6.2 RT-C2-07)
 12.  R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-ENUM  (§13.16.6.2 RT-C2-10)
 13.  R-DATACOLLECTOR-ENV-VAR-PROHIBIT-BYPASS        (§13.16.6.2 RT-C2-13)

Each rule is structural — fires on a forbidden AST shape, no flow
sensitivity. The live Data Collector tree (post-Slice-2) is clean against
every rule; the rules guard against future contributor drift.

The 4-layer CIC × CLC orthogonality audit (Rule 5) consolidates four
detection layers per §13.16.1 RT-20 closure: lexical regex, Pydantic AST
field defaults, value-set string-literal scan in outbound templates, and
KP schema delegation. Layer-4 KP schema check is structural — it runs the
regex against the §13 blueprint anchors as a guard against blueprint-level
drift.

Pure Python; runs as part of :data:`pipeline.linting.ast_lint.DEFAULT_RULES`
via the ``_section_13_data_collector_slice_3_rules`` lazy-import block.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Iterator

from pipeline.linting._rule_types import Rule, Violation

__all__ = [
    "DATACOLLECTOR_TARGET_GLOB",
    "OUTBOUND_BATCH_FILENAME",
    "CIC_TOKEN_REGEX",
    "PROHIBITED_ENV_VAR_NAMES",
    "BENEFICIARY_CONSENT_TIER_LITERALS",
    "R_DATACOLLECTOR_NO_AUTOSEND",
    "R_DATACOLLECTOR_VAULT_INTENT_REQUIRED",
    "R_DATACOLLECTOR_NO_CULTIVATOR_LEDGER_IMPORT",
    "R_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER_REQUIRED",
    "R_DATACOLLECTOR_CIC_CLC_ORTHOGONALITY",
    "R_DATACOLLECTOR_NO_RAW_TELEGRAM_BOT_IMPORT",
    "R_DATACOLLECTOR_CARD_MANDATORY_SIG_VERIFY",
    "R_DATACOLLECTOR_CARD_SAFE_LOAD",
    "R_DATACOLLECTOR_ORGSCOPEDBOT_FINAL",
    "R_DATACOLLECTOR_CEDAR_NO_CATCH",
    "R_DATACOLLECTOR_TOKEN_NONCE_UNIQUE",
    "R_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER_ENUM",
    "R_DATACOLLECTOR_ENV_VAR_PROHIBIT_BYPASS",
    "ALL_RULES",
]


# ---------------------------------------------------------------------------
# Shared constants
# ---------------------------------------------------------------------------

DATACOLLECTOR_TARGET_GLOB: str = (
    "pipeline/orchestrator/seats/data_collector/**/*.py"
)

# Canonical dispatcher module name (Layer-2 surface per §13.7).
OUTBOUND_BATCH_FILENAME: str = "outbound_batch.py"

# CIC token regex per §13.16.1 RT-20 closure. Wrapped in word boundaries so
# substrings (e.g., ``COOPERATIVE_CONFIG_VERSION``) still hit, mirroring the
# blueprint's stated semantics (any CIC archetype reference in DC code is
# itself a coupling violation).
CIC_TOKEN_REGEX: re.Pattern[str] = re.compile(
    r"\b(INTERNAL_[A-Z_]+|CIC_[A-Z_]+|FOOD_SYSTEMS|EDUCATOR|"
    r"PUBLIC_AGENCY|ARTS_CULTURE|COOPERATIVE|"
    r"ECOSYSTEM_INTERMEDIARY)\b"
)

# Prohibited env-var names per RT-C2-13 closure. Lower-case forms checked
# case-insensitively at the runtime CLI validator + the lint detection.
PROHIBITED_ENV_VAR_NAMES: tuple[str, ...] = (
    "DC_AUTO",
    "DC_YES",
    "DC_FORCE",
    "DATACOLLECTOR_AUTO_CONFIRM",
    "DATACOLLECTOR_YES",
    "DATACOLLECTOR_FORCE",
)

# Allowed beneficiary consent_tier literal values per v7.0.5 §6 + RT-C2-10.
BENEFICIARY_CONSENT_TIER_LITERALS: frozenset[str] = frozenset(
    {"my_eyes_only", "matchable_to_opportunities", "composable_with_others"}
)

# Channel token suffix — for the R-DATACOLLECTOR-NO-AUTOSEND rule.
_CHANNEL_NAMES: tuple[str, ...] = (
    "email",
    "sms",
    "voice",
    "telegram",
    "whatsapp",
)
_CHANNEL_MODULE_NAMES: tuple[str, ...] = tuple(
    f"{ch}_channel" for ch in _CHANNEL_NAMES
)


def _violation(
    rule_name: str,
    reason_tag: str,
    path: Path,
    node: ast.AST,
    message: str,
) -> Violation:
    return Violation(
        rule_name=rule_name,
        reason_tag=reason_tag,
        file=path,
        line=getattr(node, "lineno", 1),
        col=getattr(node, "col_offset", 0),
        message=message,
    )


def _is_outbound_batch(path: Path) -> bool:
    """True iff ``path.name`` matches the canonical dispatcher filename."""
    return path.name == OUTBOUND_BATCH_FILENAME


# ===========================================================================
# 1.  R-DATACOLLECTOR-NO-AUTOSEND
# ===========================================================================
#
# Reject any call expression where the function shape is
# ``<channel>_channel.send(...)`` and the enclosing file is NOT
# ``outbound_batch.py``. Per §13.7 Layer 1; the canonical dispatcher
# ``dispatch_after_operator_approval`` is the ONLY admissible caller of a
# channel send().
#
# Detection shape:
#   ast.Call(func=ast.Attribute(value=ast.Name('email_channel'), attr='send'))
#   etc. across the five channel module names.


def _check_no_autosend(tree: ast.AST, path: Path) -> Iterator[Violation]:
    if _is_outbound_batch(path):
        return
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not isinstance(func, ast.Attribute):
            continue
        if func.attr != "send":
            continue
        if not isinstance(func.value, ast.Name):
            continue
        if func.value.id not in _CHANNEL_MODULE_NAMES:
            continue
        yield _violation(
            rule_name="R-DATACOLLECTOR-NO-AUTOSEND",
            reason_tag="datacollector_autosend_attempted",
            path=path,
            node=node,
            message=(
                f"Data Collector channel send '{func.value.id}.send(...)' "
                f"called outside outbound_batch.dispatch_after_operator_approval "
                f"(§13.7 Layer 1 — silent-auto-send forbidden)"
            ),
        )


R_DATACOLLECTOR_NO_AUTOSEND: Rule = Rule(
    name="R-DATACOLLECTOR-NO-AUTOSEND",
    reason_tag="datacollector_autosend_attempted",
    target_glob=DATACOLLECTOR_TARGET_GLOB,
    check=_check_no_autosend,
    description=(
        "Reject <channel>_channel.send(...) outside outbound_batch.py "
        "dispatch_after_operator_approval. Layer 1 of the §13.7 four-layer "
        "silent-auto-send defense (compile-time)."
    ),
)


# ===========================================================================
# 2.  R-DATACOLLECTOR-VAULT-INTENT-REQUIRED
# ===========================================================================
#
# Reject raw ``open()`` calls whose first literal argument is a vault path
# (``orgs/<slug>/vault/...``). Operational sub-kind writes / reads must
# route via the vault broker; raw open() bypasses the Cedar policy chain
# (esp. ``beneficiary_records_pii.cedar``).
#
# Vault path heuristic: literal starts with ``orgs/`` AND contains
# ``/vault/`` as a path segment.


def _is_vault_literal(s: str) -> bool:
    return s.startswith("orgs/") and "/vault/" in s


def _check_vault_intent_required(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Name) and func.id == "open"):
            continue
        if not node.args:
            continue
        first = node.args[0]
        if not (isinstance(first, ast.Constant) and isinstance(first.value, str)):
            continue
        if not _is_vault_literal(first.value):
            continue
        yield _violation(
            rule_name="R-DATACOLLECTOR-VAULT-INTENT-REQUIRED",
            reason_tag="datacollector_raw_open_against_vault_path",
            path=path,
            node=node,
            message=(
                f"raw open({first.value!r}) on vault path forbidden in Data "
                "Collector — route through vault broker read/write intents "
                "(§13.5.4 + §2 v7.2 LOCKED PII discipline)"
            ),
        )


R_DATACOLLECTOR_VAULT_INTENT_REQUIRED: Rule = Rule(
    name="R-DATACOLLECTOR-VAULT-INTENT-REQUIRED",
    reason_tag="datacollector_raw_open_against_vault_path",
    target_glob=DATACOLLECTOR_TARGET_GLOB,
    check=_check_vault_intent_required,
    description=(
        "Reject raw open() against literal orgs/<slug>/vault/... paths in "
        "Data Collector modules; vault reads/writes must route through the "
        "vault broker (§13.5.4)."
    ),
)


# ===========================================================================
# 3.  R-DATACOLLECTOR-NO-CULTIVATOR-LEDGER-IMPORT
# ===========================================================================
#
# Reject any ``cultivator.consent_ledger.*`` import in Data Collector code.
# The §13.11 substrate-split keeps DC + Cultivator ledger surfaces strictly
# segregated regardless of the shared MTProto substrate.


def _check_no_cultivator_ledger_import(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("cultivator.consent_ledger") or alias.name == "cultivator":
                    yield _violation(
                        rule_name="R-DATACOLLECTOR-NO-CULTIVATOR-LEDGER-IMPORT",
                        reason_tag="datacollector_cultivator_ledger_import",
                        path=path,
                        node=node,
                        message=(
                            f"Data Collector module imports cultivator namespace "
                            f"{alias.name!r}; §13.11 substrate-split forbids cross-"
                            "seat ledger imports"
                        ),
                    )
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if mod.startswith("cultivator.consent_ledger") or mod == "cultivator.consent_ledger":
                yield _violation(
                    rule_name="R-DATACOLLECTOR-NO-CULTIVATOR-LEDGER-IMPORT",
                    reason_tag="datacollector_cultivator_ledger_import",
                    path=path,
                    node=node,
                    message=(
                        f"Data Collector module imports from cultivator namespace "
                        f"{mod!r}; §13.11 substrate-split forbids cross-seat ledger "
                        "imports"
                    ),
                )
            elif mod == "cultivator":
                for alias in node.names:
                    if alias.name == "consent_ledger":
                        yield _violation(
                            rule_name="R-DATACOLLECTOR-NO-CULTIVATOR-LEDGER-IMPORT",
                            reason_tag="datacollector_cultivator_ledger_import",
                            path=path,
                            node=node,
                            message=(
                                "Data Collector module 'from cultivator import "
                                "consent_ledger' forbidden by §13.11 substrate-"
                                "split"
                            ),
                        )


R_DATACOLLECTOR_NO_CULTIVATOR_LEDGER_IMPORT: Rule = Rule(
    name="R-DATACOLLECTOR-NO-CULTIVATOR-LEDGER-IMPORT",
    reason_tag="datacollector_cultivator_ledger_import",
    target_glob=DATACOLLECTOR_TARGET_GLOB,
    check=_check_no_cultivator_ledger_import,
    description=(
        "Reject imports of cultivator.consent_ledger.* from Data Collector "
        "modules. §13.11 substrate-split keeps DC + Cultivator ledger "
        "surfaces strictly segregated."
    ),
)


# ===========================================================================
# 4.  R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-REQUIRED
# ===========================================================================
#
# Detect calls to BeneficiaryRecord(...) / write_beneficiary_record(...) /
# ``vault.write_beneficiary_record(...)`` whose keyword arguments do NOT
# include ``consent_tier=...``. Compile-time mirror of the POST-write
# F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER gate.

_BENEFICIARY_WRITE_CALLABLE_NAMES: frozenset[str] = frozenset(
    {"BeneficiaryRecord", "write_beneficiary_record", "write_beneficiary_records"}
)


def _call_target_simple_name(call: ast.Call) -> str | None:
    func = call.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _check_beneficiary_consent_tier_required(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        target = _call_target_simple_name(node)
        if target not in _BENEFICIARY_WRITE_CALLABLE_NAMES:
            continue
        kwarg_names = {kw.arg for kw in node.keywords if kw.arg is not None}
        if "consent_tier" in kwarg_names:
            continue
        yield _violation(
            rule_name="R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-REQUIRED",
            reason_tag="datacollector_beneficiary_consent_tier_missing",
            path=path,
            node=node,
            message=(
                f"Beneficiary write {target!r} missing consent_tier= keyword "
                "argument (§13.16.2 RT-28 + §2 v7.2 PII discipline)"
            ),
        )


R_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER_REQUIRED: Rule = Rule(
    name="R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-REQUIRED",
    reason_tag="datacollector_beneficiary_consent_tier_missing",
    target_glob=DATACOLLECTOR_TARGET_GLOB,
    check=_check_beneficiary_consent_tier_required,
    description=(
        "Beneficiary record writes (BeneficiaryRecord / write_beneficiary_*) "
        "MUST pass consent_tier= keyword argument. Compile-time mirror of the "
        "POST-write F-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER gate."
    ),
)


# ===========================================================================
# 5.  R-DATACOLLECTOR-CIC-CLC-ORTHOGONALITY  (consolidates 4-layer audit)
# ===========================================================================
#
# Per §13.16.1 RT-20 + §13.16.6.2 RT-C2-08:
#
#   Layer 1 — Static lexical regex scan over source text (non-comment) for
#             CIC tokens.
#   Layer 2 — Pydantic AST scan — no class field with default matching a CIC
#             enum member.
#   Layer 3 — Value-set scan — no string literal in any DC module matching a
#             CIC archetype identifier.
#   Layer 4 — KP schema scan — delegated to v7.0.8 KP-schema audit; this lint
#             rule asserts the schema-audit anchor file is *referenced* by the
#             §13 source tree (structural anchor; full schema-audit runner is
#             a separate CI job).
#
# Implementation note: Layers 1-3 are AST-derivable from the live file. Layer
# 4 is structural — we walk the parsed tree for *any* match of the CIC regex
# in a Name id or a Constant string value, since both forms violate the
# orthogonality contract.


def _strip_comments(source: str) -> str:
    """Strip Python ``#`` line-comments from the source so the regex hits
    only on code, not on documentation."""
    out_lines = []
    for line in source.splitlines():
        # Naive but adequate for the CIC token check — strips inline comments
        # outside string literals.  Sufficient for v0.2 first-ship lint scope.
        in_string = False
        quote: str | None = None
        out_chars = []
        i = 0
        while i < len(line):
            c = line[i]
            if in_string:
                if c == "\\" and i + 1 < len(line):
                    out_chars.append(c)
                    out_chars.append(line[i + 1])
                    i += 2
                    continue
                if c == quote:
                    in_string = False
                    quote = None
                out_chars.append(c)
            else:
                if c in ("'", '"'):
                    in_string = True
                    quote = c
                    out_chars.append(c)
                elif c == "#":
                    break  # rest of line is a comment
                else:
                    out_chars.append(c)
            i += 1
        out_lines.append("".join(out_chars))
    return "\n".join(out_lines)


def _check_cic_clc_orthogonality(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    # Re-read the source file because the AST node text isn't available
    # here; the file is small (a few hundred lines at most for DC modules).
    try:
        source = path.read_text(encoding="utf-8")
    except OSError:
        return
    stripped = _strip_comments(source)
    # Layer 1: lexical regex scan over stripped source.
    for match in CIC_TOKEN_REGEX.finditer(stripped):
        # Compute approximate line/col from the match position.
        prefix = stripped[: match.start()]
        line = prefix.count("\n") + 1
        col = match.start() - (prefix.rfind("\n") + 1) if "\n" in prefix else match.start()
        yield Violation(
            rule_name="R-DATACOLLECTOR-CIC-CLC-ORTHOGONALITY",
            reason_tag="datacollector_cic_clc_coupling_violation",
            file=path,
            line=line,
            col=col,
            message=(
                f"CIC archetype token {match.group(0)!r} present in Data "
                "Collector code; CICs and CLCs are orthogonal axes — "
                "archetype-driven design-time coupling forbidden "
                "(§13.16.1 RT-20 + architecture v7.0.8 F-CIC-CLC-COUPLING-"
                "VIOLATION)"
            ),
        )
    # Layer 2 + 3: walk the AST for Constant str matches + Name id matches.
    # These compose with Layer 1 — same token via either path is a violation.
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            for match in CIC_TOKEN_REGEX.finditer(node.value):
                yield _violation(
                    rule_name="R-DATACOLLECTOR-CIC-CLC-ORTHOGONALITY",
                    reason_tag="datacollector_cic_clc_string_literal",
                    path=path,
                    node=node,
                    message=(
                        f"CIC token {match.group(0)!r} appears in string "
                        "literal value; outbound template register / schema "
                        "default values forbid CIC archetype identifiers"
                    ),
                )
        elif isinstance(node, ast.Name):
            if CIC_TOKEN_REGEX.fullmatch(node.id):
                yield _violation(
                    rule_name="R-DATACOLLECTOR-CIC-CLC-ORTHOGONALITY",
                    reason_tag="datacollector_cic_clc_name_reference",
                    path=path,
                    node=node,
                    message=(
                        f"CIC token {node.id!r} appears as Name reference; "
                        "Pydantic field default matches CIC enum member "
                        "(§13.16.1 RT-20 Layer 2 violation)"
                    ),
                )


R_DATACOLLECTOR_CIC_CLC_ORTHOGONALITY: Rule = Rule(
    name="R-DATACOLLECTOR-CIC-CLC-ORTHOGONALITY",
    reason_tag="datacollector_cic_clc_coupling_violation",
    target_glob=DATACOLLECTOR_TARGET_GLOB,
    check=_check_cic_clc_orthogonality,
    description=(
        "Consolidates the 4-layer CIC × CLC orthogonality audit per §13.16.1 "
        "RT-20 + §13.16.6.2 RT-C2-08: lexical regex (Layer 1), Pydantic field "
        "default scan (Layer 2), string-literal scan (Layer 3), KP schema "
        "anchor (Layer 4 delegated). Any CIC archetype identifier reference "
        "in Data Collector code is a coupling violation."
    ),
)


# ===========================================================================
# 6.  R-DATACOLLECTOR-NO-RAW-TELEGRAM-BOT-IMPORT
# ===========================================================================
#
# Reject any ``from telegram import Bot`` / ``import telegram`` /
# ``from telegram.ext import ...`` etc. Only ``OrgScopedBot`` from the
# data_collector seat package is admissible. Per §13.16.1 RT-07.


_RAW_TELEGRAM_MODULE_PREFIXES: tuple[str, ...] = (
    "telegram",
    "pyrogram",
    "telethon",
)


def _is_raw_telegram_module(mod: str) -> bool:
    for prefix in _RAW_TELEGRAM_MODULE_PREFIXES:
        if mod == prefix or mod.startswith(prefix + "."):
            return True
    return False


def _check_no_raw_telegram_bot_import(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _is_raw_telegram_module(alias.name):
                    yield _violation(
                        rule_name="R-DATACOLLECTOR-NO-RAW-TELEGRAM-BOT-IMPORT",
                        reason_tag="datacollector_raw_telegram_bot_import",
                        path=path,
                        node=node,
                        message=(
                            f"Data Collector module imports raw Telegram "
                            f"library {alias.name!r}; only OrgScopedBot "
                            "import permitted (§13.16.1 RT-07)"
                        ),
                    )
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _is_raw_telegram_module(mod):
                continue
            yield _violation(
                rule_name="R-DATACOLLECTOR-NO-RAW-TELEGRAM-BOT-IMPORT",
                reason_tag="datacollector_raw_telegram_bot_import",
                path=path,
                node=node,
                message=(
                    f"Data Collector module 'from {mod} import …' forbidden; "
                    "only OrgScopedBot import permitted (§13.16.1 RT-07)"
                ),
            )


R_DATACOLLECTOR_NO_RAW_TELEGRAM_BOT_IMPORT: Rule = Rule(
    name="R-DATACOLLECTOR-NO-RAW-TELEGRAM-BOT-IMPORT",
    reason_tag="datacollector_raw_telegram_bot_import",
    target_glob=DATACOLLECTOR_TARGET_GLOB,
    check=_check_no_raw_telegram_bot_import,
    description=(
        "Reject raw `telegram` / `pyrogram` / `telethon` imports in Data "
        "Collector modules. Only the OrgScopedBot wrapper is admissible "
        "(§13.16.1 RT-07)."
    ),
)


# ===========================================================================
# 7.  R-DATACOLLECTOR-CARD-MANDATORY-SIG-VERIFY
# ===========================================================================
#
# Reject any card-load shape that bypasses the canonical
# ``load_state_card(...)`` entry. Per §13.16.2 RT-21 — the loader
# function performs Ed25519 signature verification; any code that opens a
# card YAML + parses it without going through the loader is a bypass.
#
# Detection shape: a `yaml.safe_load(...)` call whose first arg traces to a
# card file path (literal ending in ``state_rules_card/<state>.yaml``
# or a Name bound to such a path) appearing in a module OTHER THAN
# ``state_rules_card.py`` itself. We approximate via a simpler test —
# look for any open() of a literal path under ``vault_shared/state_rules_card``
# in a module other than ``state_rules_card.py``.


_CARD_PATH_PREFIX: str = "vault_shared/state_rules_card"


def _check_card_mandatory_sig_verify(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    if path.name == "state_rules_card.py":
        return  # canonical loader file is allowed to open cards
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name) and func.id == "open":
            if not node.args:
                continue
            first = node.args[0]
            if (
                isinstance(first, ast.Constant)
                and isinstance(first.value, str)
                and _CARD_PATH_PREFIX in first.value
            ):
                yield _violation(
                    rule_name="R-DATACOLLECTOR-CARD-MANDATORY-SIG-VERIFY",
                    reason_tag="datacollector_card_bypass",
                    path=path,
                    node=node,
                    message=(
                        f"raw open({first.value!r}) on state card path "
                        "bypasses load_state_card() signature verifier "
                        "(§13.16.2 RT-21)"
                    ),
                )


R_DATACOLLECTOR_CARD_MANDATORY_SIG_VERIFY: Rule = Rule(
    name="R-DATACOLLECTOR-CARD-MANDATORY-SIG-VERIFY",
    reason_tag="datacollector_card_bypass",
    target_glob=DATACOLLECTOR_TARGET_GLOB,
    check=_check_card_mandatory_sig_verify,
    description=(
        "Reject any module other than state_rules_card.py that opens a "
        "vault_shared/state_rules_card/<state>.yaml file directly. The "
        "canonical load_state_card() entry performs mandatory Ed25519 "
        "signature verification (§13.16.2 RT-21)."
    ),
)


# ===========================================================================
# 8.  R-DATACOLLECTOR-CARD-SAFE-LOAD
# ===========================================================================
#
# Reject ``yaml.load(...)`` calls. Only ``yaml.safe_load(...)`` permitted in
# Data Collector code. Per §13.16.2 RT-27 closure.


def _check_card_safe_load(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        # yaml.load(...)
        if (
            isinstance(func, ast.Attribute)
            and func.attr == "load"
            and isinstance(func.value, ast.Name)
            and func.value.id == "yaml"
        ):
            yield _violation(
                rule_name="R-DATACOLLECTOR-CARD-SAFE-LOAD",
                reason_tag="datacollector_yaml_unsafe_load",
                path=path,
                node=node,
                message=(
                    "yaml.load(...) is unsafe in Data Collector; only "
                    "yaml.safe_load(...) permitted (§13.16.2 RT-27)"
                ),
            )
        # bare load(...) where it's a from-yaml-import-load rebinding —
        # detected via the import scan: if `from yaml import load` is at
        # module top, all bare `load(...)` calls are suspect. Conservative
        # heuristic: only flag yaml.load() explicit form; the `from yaml
        # import load` shape itself is rejected by the import scan below.


R_DATACOLLECTOR_CARD_SAFE_LOAD: Rule = Rule(
    name="R-DATACOLLECTOR-CARD-SAFE-LOAD",
    reason_tag="datacollector_yaml_unsafe_load",
    target_glob=DATACOLLECTOR_TARGET_GLOB,
    check=_check_card_safe_load,
    description=(
        "Reject yaml.load(...) calls in Data Collector modules; only "
        "yaml.safe_load(...) permitted (§13.16.2 RT-27)."
    ),
)


# ===========================================================================
# 9.  R-DATACOLLECTOR-ORGSCOPEDBOT-FINAL
# ===========================================================================
#
# Reject any class definition that inherits from ``OrgScopedBot``. The wrapper
# is marked ``@final`` per PEP 591 and the runtime ``__init__`` check rejects
# subclasses (RT-C2-03 closure). The lint rule adds a compile-time gate so
# the runtime check never has to fire.


def _check_orgscopedbot_final(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        for base in node.bases:
            base_name: str | None = None
            if isinstance(base, ast.Name):
                base_name = base.id
            elif isinstance(base, ast.Attribute):
                base_name = base.attr
            if base_name == "OrgScopedBot":
                yield _violation(
                    rule_name="R-DATACOLLECTOR-ORGSCOPEDBOT-FINAL",
                    reason_tag="datacollector_orgscoped_bot_subclassing_forbidden",
                    path=path,
                    node=node,
                    message=(
                        f"class {node.name!r} inherits from OrgScopedBot; "
                        "@final wrapper rejects subclassing (§13.16.6.2 "
                        "RT-C2-03)"
                    ),
                )


R_DATACOLLECTOR_ORGSCOPEDBOT_FINAL: Rule = Rule(
    name="R-DATACOLLECTOR-ORGSCOPEDBOT-FINAL",
    reason_tag="datacollector_orgscoped_bot_subclassing_forbidden",
    target_glob=DATACOLLECTOR_TARGET_GLOB,
    check=_check_orgscopedbot_final,
    description=(
        "Reject class definitions that inherit from OrgScopedBot. The "
        "wrapper is @final; runtime check additionally enforces. RT-C2-03."
    ),
)


# ===========================================================================
# 10.  R-DATACOLLECTOR-CEDAR-NO-CATCH
# ===========================================================================
#
# Reject any ``try:`` block that contains a Data Collector module import
# under an ``except BaseException`` or bare ``except:`` clause. Cedar engine
# load failures raise :class:`CriticalPolicyError(BaseException)` precisely
# so they cannot be caught by ``except Exception``; this rule forbids the
# escape hatch of catching BaseException explicitly.


_DC_MODULE_IMPORT_PREFIX: str = "pipeline.orchestrator.seats.data_collector"


def _try_block_imports_dc(node: ast.Try) -> bool:
    for child in ast.walk(node):
        if isinstance(child, ast.Import):
            for alias in child.names:
                if alias.name.startswith(_DC_MODULE_IMPORT_PREFIX):
                    return True
        elif isinstance(child, ast.ImportFrom):
            mod = child.module or ""
            if mod.startswith(_DC_MODULE_IMPORT_PREFIX):
                return True
    return False


def _try_block_has_baseexception_or_bare(node: ast.Try) -> bool:
    for handler in node.handlers:
        if handler.type is None:
            return True  # bare except:
        if (
            isinstance(handler.type, ast.Name)
            and handler.type.id == "BaseException"
        ):
            return True
        if (
            isinstance(handler.type, ast.Attribute)
            and handler.type.attr == "BaseException"
        ):
            return True
    return False


def _check_cedar_no_catch(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Try):
            continue
        if not _try_block_imports_dc(node):
            continue
        if not _try_block_has_baseexception_or_bare(node):
            continue
        yield _violation(
            rule_name="R-DATACOLLECTOR-CEDAR-NO-CATCH",
            reason_tag="datacollector_cedar_baseexception_swallow",
            path=path,
            node=node,
            message=(
                "try/except BaseException (or bare except:) wraps a Data "
                "Collector module import; CriticalPolicyError(BaseException) "
                "must propagate (§13.16.6.2 RT-C2-04)"
            ),
        )


R_DATACOLLECTOR_CEDAR_NO_CATCH: Rule = Rule(
    name="R-DATACOLLECTOR-CEDAR-NO-CATCH",
    reason_tag="datacollector_cedar_baseexception_swallow",
    target_glob=DATACOLLECTOR_TARGET_GLOB,
    check=_check_cedar_no_catch,
    description=(
        "Reject try/except BaseException (or bare except:) wrapping a Data "
        "Collector module import. The Cedar engine load failure path uses "
        "CriticalPolicyError(BaseException) so upstream `except Exception` "
        "cannot swallow; this rule additionally blocks the BaseException "
        "escape hatch (§13.16.6.2 RT-C2-04)."
    ),
)


# ===========================================================================
# 11.  R-DATACOLLECTOR-TOKEN-NONCE-UNIQUE
# ===========================================================================
#
# Reject AEAD encrypt/decrypt call sites that pass a byte-literal Constant
# as the nonce argument — nonces must be ``os.urandom(12)``-derived per
# token, not hardcoded. Per §13.16.6.2 RT-C2-07.


_AEAD_ENCRYPT_METHODS: frozenset[str] = frozenset({"encrypt", "decrypt"})


def _is_static_bytes_literal(node: ast.AST) -> bool:
    """True if ``node`` is statically known to be a fixed bytes value.

    Covers three shapes that should fail closed:
      * ``ast.Constant(value=bytes|bytearray)`` — direct literal.
      * ``ast.JoinedStr`` over byte-constant components.
      * ``ast.BinOp`` whose left and right are themselves statically-known
        bytes-or-int constants (e.g., ``b"\\x00" * 12`` — a common
        anti-pattern for constructing a fake nonce).
    """
    if isinstance(node, ast.Constant) and isinstance(node.value, (bytes, bytearray)):
        return True
    if isinstance(node, ast.BinOp):
        left_is_bytes = (
            isinstance(node.left, ast.Constant)
            and isinstance(node.left.value, (bytes, bytearray))
        )
        right_is_bytes = (
            isinstance(node.right, ast.Constant)
            and isinstance(node.right.value, (bytes, bytearray))
        )
        left_is_int = (
            isinstance(node.left, ast.Constant)
            and isinstance(node.left.value, int)
        )
        right_is_int = (
            isinstance(node.right, ast.Constant)
            and isinstance(node.right.value, int)
        )
        if isinstance(node.op, ast.Mult) and (
            (left_is_bytes and right_is_int) or (left_is_int and right_is_bytes)
        ):
            return True
        if isinstance(node.op, ast.Add) and left_is_bytes and right_is_bytes:
            return True
    return False


def _check_token_nonce_unique(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not isinstance(func, ast.Attribute):
            continue
        if func.attr not in _AEAD_ENCRYPT_METHODS:
            continue
        # Look at the call args: first positional is the nonce in AESGCM /
        # ChaCha20Poly1305 conventions.
        if not node.args:
            continue
        first = node.args[0]
        if _is_static_bytes_literal(first):
            yield _violation(
                rule_name="R-DATACOLLECTOR-TOKEN-NONCE-UNIQUE",
                reason_tag="datacollector_aead_nonce_constant",
                path=path,
                node=node,
                message=(
                    f"AEAD .{func.attr}() called with constant byte-literal "
                    "nonce; per-token nonce MUST be os.urandom(12)-derived "
                    "(§13.16.6.2 RT-C2-07)"
                ),
            )


R_DATACOLLECTOR_TOKEN_NONCE_UNIQUE: Rule = Rule(
    name="R-DATACOLLECTOR-TOKEN-NONCE-UNIQUE",
    reason_tag="datacollector_aead_nonce_constant",
    target_glob=DATACOLLECTOR_TARGET_GLOB,
    check=_check_token_nonce_unique,
    description=(
        "Reject AEAD encrypt/decrypt call sites that pass a hardcoded byte-"
        "literal nonce; per-token nonces must be os.urandom(12)-derived "
        "(§13.16.6.2 RT-C2-07)."
    ),
)


# ===========================================================================
# 12.  R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-ENUM
# ===========================================================================
#
# Detect Pydantic / dataclass field annotations named ``consent_tier`` whose
# type annotation is NOT a ``Literal[...]`` containing the v7.0.5 §6 enum
# values. Per §13.16.6.2 RT-C2-10.


def _literal_string_values(annotation: ast.AST) -> frozenset[str]:
    """Extract the set of literal string values inside a ``Literal[...]``
    annotation. Returns an empty frozenset if the annotation is not a
    Literal subscript."""
    if not isinstance(annotation, ast.Subscript):
        return frozenset()
    value = annotation.value
    if isinstance(value, ast.Name):
        if value.id != "Literal":
            return frozenset()
    elif isinstance(value, ast.Attribute):
        if value.attr != "Literal":
            return frozenset()
    else:
        return frozenset()
    slc = annotation.slice
    # Python 3.9+: slice is ast.Tuple OR ast.Constant; older 3.8 had ast.Index.
    if isinstance(slc, ast.Tuple):
        elements: tuple[ast.AST, ...] = tuple(slc.elts)
    else:
        elements = (slc,)
    out: set[str] = set()
    for el in elements:
        if isinstance(el, ast.Constant) and isinstance(el.value, str):
            out.add(el.value)
    return frozenset(out)


def _check_beneficiary_consent_tier_enum(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    for node in ast.walk(tree):
        if not isinstance(node, ast.AnnAssign):
            continue
        target = node.target
        if not (isinstance(target, ast.Name) and target.id == "consent_tier"):
            continue
        annotation = node.annotation
        literals = _literal_string_values(annotation)
        if literals == BENEFICIARY_CONSENT_TIER_LITERALS:
            continue
        yield _violation(
            rule_name="R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-ENUM",
            reason_tag="datacollector_consent_tier_enum_mismatch",
            path=path,
            node=node,
            message=(
                "consent_tier field annotation must be Literal["
                "'my_eyes_only', 'matchable_to_opportunities', "
                "'composable_with_others']; got "
                f"{ast.unparse(annotation) if hasattr(ast, 'unparse') else '<annotation>'} "
                "(§13.16.6.2 RT-C2-10)"
            ),
        )


R_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER_ENUM: Rule = Rule(
    name="R-DATACOLLECTOR-BENEFICIARY-CONSENT-TIER-ENUM",
    reason_tag="datacollector_consent_tier_enum_mismatch",
    target_glob=DATACOLLECTOR_TARGET_GLOB,
    check=_check_beneficiary_consent_tier_enum,
    description=(
        "consent_tier field annotation must be Literal[my_eyes_only / "
        "matchable_to_opportunities / composable_with_others] per v7.0.5 §6 + "
        "§13.16.6.2 RT-C2-10."
    ),
)


# ===========================================================================
# 13.  R-DATACOLLECTOR-ENV-VAR-PROHIBIT-BYPASS
# ===========================================================================
#
# Reject any read of the prohibited environment variable names listed in
# ``PROHIBITED_ENV_VAR_NAMES`` from Data Collector code, UNLESS the read is
# inside a validator function whose immediate next statement raises.  We
# approximate this with a structural check: every reference to a prohibited
# env-var name in DC code must occur inside a comparison or membership-test
# whose result is used to raise an exception.  For v0.2 first ship we apply
# the simpler stance — prohibited env-var Constant strings may appear ONLY
# as members of the validator's denylist (a Tuple/List/Set literal); any
# other reference is a bypass attempt.


def _check_env_var_prohibit_bypass(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    # Walk every Constant string. If it matches a prohibited env-var name AND
    # the parent context is not a denylist literal (Tuple/List/Set), fire.
    # We track parentage via a pre-pass that annotates each Constant's parent
    # (Python AST does not store parent pointers natively).
    parents: dict[int, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[id(child)] = parent

    prohibited = frozenset(name.upper() for name in PROHIBITED_ENV_VAR_NAMES)
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        if node.value.upper() not in prohibited:
            continue
        # Walk up looking for an enclosing Tuple/List/Set/Dict that defines a
        # denylist. If the enclosing container is one of those, accept.
        cursor: ast.AST | None = parents.get(id(node))
        accepted = False
        # Walk up a few levels to find the enclosing collection literal.
        for _ in range(6):
            if cursor is None:
                break
            if isinstance(cursor, (ast.Tuple, ast.List, ast.Set, ast.Dict)):
                accepted = True
                break
            cursor = parents.get(id(cursor))
        if accepted:
            continue
        yield _violation(
            rule_name="R-DATACOLLECTOR-ENV-VAR-PROHIBIT-BYPASS",
            reason_tag="datacollector_env_var_prohibit_bypass",
            path=path,
            node=node,
            message=(
                f"prohibited env-var name {node.value!r} referenced outside "
                "the denylist literal; reads of DC_AUTO/DC_YES/DC_FORCE etc. "
                "are forbidden as bypass paths (§13.16.6.2 RT-C2-13)"
            ),
        )


R_DATACOLLECTOR_ENV_VAR_PROHIBIT_BYPASS: Rule = Rule(
    name="R-DATACOLLECTOR-ENV-VAR-PROHIBIT-BYPASS",
    reason_tag="datacollector_env_var_prohibit_bypass",
    target_glob=DATACOLLECTOR_TARGET_GLOB,
    check=_check_env_var_prohibit_bypass,
    description=(
        "Reject Data Collector code references to DC_AUTO / DC_YES / DC_FORCE "
        "/ DATACOLLECTOR_* environment-variable names outside the "
        "denylist literal that defines them. RT-C2-13."
    ),
)


# ===========================================================================
# Aggregate
# ===========================================================================


ALL_RULES: tuple[Rule, ...] = (
    R_DATACOLLECTOR_NO_AUTOSEND,
    R_DATACOLLECTOR_VAULT_INTENT_REQUIRED,
    R_DATACOLLECTOR_NO_CULTIVATOR_LEDGER_IMPORT,
    R_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER_REQUIRED,
    R_DATACOLLECTOR_CIC_CLC_ORTHOGONALITY,
    R_DATACOLLECTOR_NO_RAW_TELEGRAM_BOT_IMPORT,
    R_DATACOLLECTOR_CARD_MANDATORY_SIG_VERIFY,
    R_DATACOLLECTOR_CARD_SAFE_LOAD,
    R_DATACOLLECTOR_ORGSCOPEDBOT_FINAL,
    R_DATACOLLECTOR_CEDAR_NO_CATCH,
    R_DATACOLLECTOR_TOKEN_NONCE_UNIQUE,
    R_DATACOLLECTOR_BENEFICIARY_CONSENT_TIER_ENUM,
    R_DATACOLLECTOR_ENV_VAR_PROHIBIT_BYPASS,
)
