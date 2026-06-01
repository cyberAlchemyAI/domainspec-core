"""Plumbing for admin_risk_register migration audit decisions.

Per §4 v2.x apolitical_dialect §4.X.6 (LOCKED 2026-05-16T14:00:00Z). The
F-DIALECT-MIGRATION-INCOMPLETE gate requires three plumbing pieces beyond
its predicate body:

1. Parse ``pipeline/institutional_memory/admin_risk_register.yaml`` into
   :class:`pipeline.logician.gates.f_dialect_migration_incomplete.AdminRiskRegisterEntry`
   instances — :func:`read_admin_risk_register`.
2. Parse ``pipeline/institutional_memory/admin_risk_register_audit_decisions.md``
   into :class:`AuditDecisionRow` instances — :func:`read_audit_decisions`.
3. An Ed25519 signature verifier closure — :func:`make_signature_verifier`.

Canonical bytes for the per-term signature
------------------------------------------
Per Cycle 2 fold-in C2-H-4, the operator Ed25519 signature covers the
canonical-JSON bytes of::

    {"audit_status": "<status>", "term": "<term>", "term_hash": "<hex>"}

Produced via ``json.dumps(obj, sort_keys=True, separators=(",", ":"),
ensure_ascii=False).encode("utf-8")``. The verifier here recomputes the
same bytes and calls ``Ed25519PublicKey.verify(signature, canonical_bytes)``.

Decisions file format (Markdown table)
--------------------------------------
The decisions file is plain Markdown so the operator can read + edit it
directly. The expected shape is a single pipe-delimited table headed by::

    | term | term_hash | audit_status | operator_ed25519_signature_hex | operator_pubkey_ed25519_hex |

Plus optional `--` separator row. Each subsequent row carries one term's
decision. The reader is tolerant: leading/trailing whitespace stripped,
empty/`null`/`None` values normalized to ``None``, signature/pubkey hex
case-folded to lowercase.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Iterable, Iterator, Optional

import yaml

from pipeline.logician.gates.f_dialect_migration_incomplete import (
    AUDIT_STATUS_CONFIRMED_AVOID_ALL,
    AUDIT_STATUS_CONFIRMED_PER_CLC,
    AdminRiskRegisterEntry,
    AuditDecisionRow,
)


DEFAULT_ADMIN_RISK_REGISTER_PATH: Path = (
    Path(__file__).parent / "admin_risk_register.yaml"
)
DEFAULT_AUDIT_DECISIONS_PATH: Path = (
    Path(__file__).parent / "admin_risk_register_audit_decisions.md"
)


# ---------------------------------------------------------------------------
# Canonical bytes (mirrors gate's _term_hash + the per-row sig payload)
# ---------------------------------------------------------------------------


def compute_term_hash(term: str, severity: str) -> str:
    """Stable identifier for one admin_risk_register term.

    Mirrors :func:`pipeline.logician.gates.f_dialect_migration_incomplete._term_hash`
    byte-for-byte. Exposed here so the audit-decisions file authoring path
    + the gate path agree on identifiers.
    """
    return hashlib.sha3_256(
        f"{term}\x00{severity}".encode("utf-8")
    ).hexdigest()


def canonical_decision_bytes(
    *,
    term: str,
    term_hash: str,
    audit_status: str,
) -> bytes:
    """Canonical-JSON bytes the operator Ed25519 signature covers.

    Stable key order (json sort_keys=True), minimal separators, UTF-8 with
    ASCII-safe escape disabled (ensure_ascii=False) so operator-typed
    Unicode terms (e.g., accented characters in flagged terms) serialize
    losslessly.
    """
    return json.dumps(
        {
            "audit_status": audit_status,
            "term": term,
            "term_hash": term_hash,
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


# ---------------------------------------------------------------------------
# admin_risk_register.yaml reader
# ---------------------------------------------------------------------------


def read_admin_risk_register(
    path: Optional[Path] = None,
) -> Iterator[AdminRiskRegisterEntry]:
    """Yield one :class:`AdminRiskRegisterEntry` per ``entries[]`` row of
    the admin_risk_register YAML.

    Architecture v7.0.12 §1.2: ``per_clc_register`` is a map of CLC slug to
    {AVOID|OK|EXPECTED|PREFERRED}. Defaults to the empty map when absent,
    which the gate treats as "unmigrated — requires audit-decision row."

    Pre-v7.0.12 entries carry ``progressive_register`` (a single string);
    those entries surface here with ``per_clc_register = {}`` to force the
    gate's audit-decision lookup path.
    """
    p = path if path is not None else DEFAULT_ADMIN_RISK_REGISTER_PATH
    raw = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return
    entries = raw.get("entries", [])
    if not isinstance(entries, list):
        return
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        term = entry.get("term") or entry.get("flagged_term")
        severity = entry.get("severity")
        if not isinstance(term, str) or not isinstance(severity, str):
            continue
        raw_per_clc = entry.get("per_clc_register")
        if isinstance(raw_per_clc, dict):
            per_clc = {
                str(k): str(v)
                for k, v in raw_per_clc.items()
                if isinstance(k, str) and isinstance(v, str)
            }
        else:
            per_clc = {}
        yield AdminRiskRegisterEntry(
            term=term,
            severity=severity,
            per_clc_register=per_clc,
        )


# ---------------------------------------------------------------------------
# admin_risk_register_audit_decisions.md reader
# ---------------------------------------------------------------------------


_DECISIONS_TABLE_HEADER_RE = re.compile(
    r"\|\s*term\s*\|\s*term_hash\s*\|\s*audit_status\s*\|\s*"
    r"operator_ed25519_signature_hex\s*\|\s*"
    r"operator_pubkey_ed25519_hex\s*\|",
    re.IGNORECASE,
)
_SEPARATOR_ROW_RE = re.compile(r"\s*\|?\s*[-:]+\s*(\|\s*[-:]+\s*)+\|?\s*$")


def _normalize_optional_hex(value: str) -> Optional[str]:
    """Strip + lowercase a hex field; return None for empty / sentinel
    values (``""``, ``"null"``, ``"None"``, ``"<PENDING>"``)."""
    v = value.strip()
    if v == "" or v.lower() in {"null", "none", "-", "<pending>"}:
        return None
    return v.lower()


def _normalize_audit_status(value: str) -> str:
    v = value.strip()
    if v in {
        AUDIT_STATUS_CONFIRMED_AVOID_ALL,
        AUDIT_STATUS_CONFIRMED_PER_CLC,
    }:
        return v
    return v  # Unknown values pass through; the gate rejects them.


def read_audit_decisions(
    path: Optional[Path] = None,
) -> Iterator[AuditDecisionRow]:
    """Parse the audit-decisions Markdown table.

    Raises :class:`FileNotFoundError` if the file is absent — the
    F-DIALECT-MIGRATION-INCOMPLETE gate catches this and emits the
    ``.audit_decisions_missing`` sub-tag (per Cycle 2 fold-in C2-NEW-MED-4).

    Tolerant of:
      - leading/trailing whitespace
      - missing trailing pipe
      - separator rows with colons (``:-:``) for alignment
      - blank rows
      - sentinel values for unsigned/pending rows (``<PENDING>``, ``null``,
        ``-``, ``None`` → ``None``)
    """
    p = path if path is not None else DEFAULT_AUDIT_DECISIONS_PATH
    text = p.read_text(encoding="utf-8")
    in_table = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            in_table = False
            continue
        if _DECISIONS_TABLE_HEADER_RE.search(line):
            in_table = True
            continue
        if not in_table:
            continue
        if _SEPARATOR_ROW_RE.match(line):
            continue
        # Data row.
        parts = [
            cell.strip()
            for cell in line.strip("|").split("|")
        ]
        if len(parts) < 5:
            continue
        term, term_hash, audit_status, sig_hex, pubkey_hex = parts[:5]
        if not term or term.startswith("<"):
            # Header sentinel rows or operator-marker rows.
            continue
        yield AuditDecisionRow(
            term=term,
            term_hash=term_hash.strip().lower(),
            audit_status=_normalize_audit_status(audit_status),
            operator_ed25519_signature_hex=_normalize_optional_hex(sig_hex),
            operator_pubkey_ed25519_hex=_normalize_optional_hex(pubkey_hex),
        )


# ---------------------------------------------------------------------------
# Ed25519 signature verifier closure
# ---------------------------------------------------------------------------


def make_signature_verifier(
    *,
    expected_pubkey_hex: Optional[str] = None,
):
    """Construct a ``signature_verifier`` callable for the gate.

    If ``expected_pubkey_hex`` is supplied, every per-term signature must
    additionally be signed by that exact pubkey (defends against accepting
    a valid signature from an arbitrary key). If ``None``, any pubkey on
    the audit-decision row is accepted as long as the math verifies — useful
    during the cards-ceremony when the operator may rotate keys.

    The returned callable matches the
    :class:`pipeline.logician.gates.f_dialect_migration_incomplete.SignatureVerifierCallable`
    Protocol shape.
    """
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import (
            Ed25519PublicKey,
        )
    except ImportError as exc:
        raise RuntimeError(
            "cryptography>=42 required for Ed25519 verification; install "
            "per pyproject.toml dependencies"
        ) from exc

    expected_norm = (
        expected_pubkey_hex.lower() if expected_pubkey_hex else None
    )

    def _verify(
        *,
        term: str,
        term_hash: str,
        audit_status: str,
        signature_hex: str,
        pubkey_hex: str,
    ) -> bool:
        if expected_norm is not None and pubkey_hex.lower() != expected_norm:
            return False
        try:
            sig_bytes = bytes.fromhex(signature_hex)
            pub_bytes = bytes.fromhex(pubkey_hex)
        except ValueError:
            return False
        if len(pub_bytes) != 32:
            return False
        try:
            pubkey = Ed25519PublicKey.from_public_bytes(pub_bytes)
            pubkey.verify(
                sig_bytes,
                canonical_decision_bytes(
                    term=term,
                    term_hash=term_hash,
                    audit_status=audit_status,
                ),
            )
            return True
        except InvalidSignature:
            return False
        except Exception:
            return False

    return _verify


# ---------------------------------------------------------------------------
# Empty-template generation (operator scaffold)
# ---------------------------------------------------------------------------


def render_empty_decisions_template(
    *,
    entries: Iterable[AdminRiskRegisterEntry],
) -> str:
    """Render an empty audit-decisions Markdown table seeded with one row
    per admin_risk_register entry.

    The operator fills ``audit_status`` (``confirmed_avoid_all`` or
    ``confirmed_per_clc``), runs ``pipeline/scripts/audit_term_signer.py``
    to populate the signature columns, and commits. The
    F-DIALECT-MIGRATION-INCOMPLETE gate reads the resulting file.

    The template includes a header block describing the workflow + the
    canonical-bytes shape that signatures cover.
    """
    lines: list[str] = [
        "<!--",
        "  admin_risk_register_audit_decisions.md",
        "",
        "  One row per term in admin_risk_register.yaml.",
        "  Operator workflow:",
        "    1. Fill audit_status for each row:",
        "         - confirmed_avoid_all   → AVOID-everywhere is the right",
        "                                   default for this term across all 8 CLCs",
        "                                   (empty per_clc_register on the register entry)",
        "         - confirmed_per_clc     → operator populated per_clc_register on the",
        "                                   register entry with explicit per-CLC values",
        "    2. Run scripts/run_tests.sh (or equivalent) on a fixture to verify",
        "       the gate is happy with the current per_clc_register state.",
        "    3. Run `python pipeline/scripts/audit_term_signer.py --key <path>`",
        "       to fill the signature_hex + pubkey_hex columns.",
        "    4. Commit + run the LOCK ceremony.",
        "",
        "  Canonical bytes the per-term signature covers:",
        "    json.dumps({\"audit_status\": <s>, \"term\": <t>, \"term_hash\": <h>},",
        "               sort_keys=True, separators=(\",\", \":\"),",
        "               ensure_ascii=False).encode(\"utf-8\")",
        "",
        "  Authority: §4 v2.x apolitical_dialect §4.X.6 + Cycle 2 fold-ins",
        "  C2-H-4 (per-term Ed25519) + C2-NEW-MED-2 (audit_status closed set)",
        "  + C2-NEW-MED-4 (try/except on missing file).",
        "-->",
        "",
        "# admin_risk_register migration — per-term audit decisions",
        "",
        "| term | term_hash | audit_status | operator_ed25519_signature_hex | operator_pubkey_ed25519_hex |",
        "|------|-----------|--------------|--------------------------------|-----------------------------|",
    ]
    for entry in entries:
        term_hash = compute_term_hash(entry.term, entry.severity)
        lines.append(
            f"| {entry.term} | {term_hash} | <PENDING> | <PENDING> | <PENDING> |"
        )
    lines.append("")
    return "\n".join(lines)


__all__ = [
    "DEFAULT_ADMIN_RISK_REGISTER_PATH",
    "DEFAULT_AUDIT_DECISIONS_PATH",
    "canonical_decision_bytes",
    "compute_term_hash",
    "make_signature_verifier",
    "read_admin_risk_register",
    "read_audit_decisions",
    "render_empty_decisions_template",
]
