"""Statically compiled eTLD → ISO-3166-1 alpha-2 jurisdiction table.

Round 7 BT12 pre-flight consults this table to resolve the jurisdiction of a
registrable domain. Unknown eTLD → ``None`` → default-deny per F-BT12-03.

Blueprint anchors:
- §4.6 ``_jurisdiction_from_registrable_domain`` (lines 568-572).
- §5.1 BT12 M11 Channel F domain pre-flight (lines 1084-1095).
- A-14 closure — lookup keys are Punycode (``xn--`` form); callers must
  normalise via ``idna.encode(host, uts46=True)`` before lookup.

Table contents (≥ 250 entries per spec-card engineering-risks guidance):
- All ISO-3166-1 alpha-2 ccTLDs (250 codes) mapped to their own code.
- Common gTLDs (``.com``, ``.net``, ``.org``, ``.info``, ``.biz``, ``.io``,
  ``.co`` generic-use, ``.dev``, ``.app``, ``.ai``, ``.xyz``) mapped to
  ``"GTLD"`` — operator must explicitly allowlist ``GTLD`` in
  ``ChannelFJurisdictionPolicy.allowed_jurisdictions`` for any of these to
  pass pre-flight.
- US-administered reserved TLDs (``.gov``, ``.mil``, ``.edu``) mapped to
  ``"US"``.

The table is wrapped in :class:`types.MappingProxyType` at module scope so
no caller can mutate it. :func:`jurisdiction_for_etld` is the only public
surface — it accepts the last label of a registrable domain (lower-cased,
Punycode) and returns either the ISO code / ``"GTLD"`` / ``"US"`` /
``None``.

This file ships a **static** table. No network, no lazy load, no import
side effect. Coverage is intentionally the ISO-3166-1 set + a small
well-known gTLD list — not an authoritative Public Suffix List. BT12's
default-deny rule is the safety net for gaps.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Mapping, Optional


__all__ = [
    "JURISDICTION_TABLE",
    "jurisdiction_for_etld",
]


# -- ISO-3166-1 alpha-2 ccTLDs (self-mapping) -------------------------------

# Source: ISO-3166-1 alpha-2 list. Each code maps to itself (upper-case) —
# the ccTLD ``.us`` resolves to jurisdiction ``US``, ``.de`` resolves to
# ``DE``, etc. Operators opt in to specific ISO codes via the per-org
# policy file.

_ISO_3166_ALPHA2: tuple[str, ...] = (
    "AD", "AE", "AF", "AG", "AI", "AL", "AM", "AO", "AQ", "AR",
    "AS", "AT", "AU", "AW", "AX", "AZ",
    "BA", "BB", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BL",
    "BM", "BN", "BO", "BQ", "BR", "BS", "BT", "BV", "BW", "BY",
    "BZ",
    "CA", "CC", "CD", "CF", "CG", "CH", "CI", "CK", "CL", "CM",
    "CN", "CO", "CR", "CU", "CV", "CW", "CX", "CY", "CZ",
    "DE", "DJ", "DK", "DM", "DO", "DZ",
    "EC", "EE", "EG", "EH", "ER", "ES", "ET",
    "FI", "FJ", "FK", "FM", "FO", "FR",
    "GA", "GB", "GD", "GE", "GF", "GG", "GH", "GI", "GL", "GM",
    "GN", "GP", "GQ", "GR", "GS", "GT", "GU", "GW", "GY",
    "HK", "HM", "HN", "HR", "HT", "HU",
    "ID", "IE", "IL", "IM", "IN", "IO", "IQ", "IR", "IS", "IT",
    "JE", "JM", "JO", "JP",
    "KE", "KG", "KH", "KI", "KM", "KN", "KP", "KR", "KW", "KY",
    "KZ",
    "LA", "LB", "LC", "LI", "LK", "LR", "LS", "LT", "LU", "LV",
    "LY",
    "MA", "MC", "MD", "ME", "MF", "MG", "MH", "MK", "ML", "MM",
    "MN", "MO", "MP", "MQ", "MR", "MS", "MT", "MU", "MV", "MW",
    "MX", "MY", "MZ",
    "NA", "NC", "NE", "NF", "NG", "NI", "NL", "NO", "NP", "NR",
    "NU", "NZ",
    "OM",
    "PA", "PE", "PF", "PG", "PH", "PK", "PL", "PM", "PN", "PR",
    "PS", "PT", "PW", "PY",
    "QA",
    "RE", "RO", "RS", "RU", "RW",
    "SA", "SB", "SC", "SD", "SE", "SG", "SH", "SI", "SJ", "SK",
    "SL", "SM", "SN", "SO", "SR", "SS", "ST", "SV", "SX", "SY",
    "SZ",
    "TC", "TD", "TF", "TG", "TH", "TJ", "TK", "TL", "TM", "TN",
    "TO", "TR", "TT", "TV", "TW", "TZ",
    "UA", "UG", "UM", "US", "UY", "UZ",
    "VA", "VC", "VE", "VG", "VI", "VN", "VU",
    "WF", "WS",
    "YE", "YT",
    "ZA", "ZM", "ZW",
    # Traditional ccTLDs that differ from the ISO code:
    # - ``.uk`` (UK) but ISO code is GB; both are live in the wild.
    # - ``.eu`` (European Union) — treated as its own jurisdiction code.
)


# eTLD → jurisdiction mapping. Start from ccTLD self-mapping, then overlay
# well-known divergences + gTLD bucket.

_TABLE: dict[str, str] = {code.lower(): code for code in _ISO_3166_ALPHA2}

# ccTLD divergences / additions where the TLD label differs from the ISO
# alpha-2 code.
_TABLE["uk"] = "GB"       # traditional UK ccTLD; ISO code for UK is GB.
_TABLE["eu"] = "EU"       # European Union — its own jurisdiction tag.
_TABLE["su"] = "SU"       # Soviet-legacy TLD kept live.

# Common gTLDs — default-deny unless operator adds ``GTLD`` to
# ``allowed_jurisdictions``.
for _gtld in (
    "com", "net", "org", "info", "biz", "io", "co", "dev", "app",
    "ai", "xyz", "tech", "site", "online", "store", "club", "cloud",
    "me", "tv", "cc", "ws", "name",
):
    _TABLE[_gtld] = "GTLD"

# US-reserved TLDs historically administered by US agencies.
_TABLE["gov"] = "US"
_TABLE["mil"] = "US"
_TABLE["edu"] = "US"


JURISDICTION_TABLE: Mapping[str, str] = MappingProxyType(_TABLE)


def jurisdiction_for_etld(label: str) -> Optional[str]:
    """Return the ISO-3166-1 alpha-2 code (or ``"GTLD"`` / ``"US"``) for
    ``label``, or ``None`` when the label is not known.

    ``label`` must be the final label of a registrable domain in lower-cased
    ASCII Punycode form — callers normalise via
    ``idna.encode(host, uts46=True).decode("ascii").split(".")[-1]`` before
    calling.
    """
    if not isinstance(label, str):
        return None
    return JURISDICTION_TABLE.get(label.lower())
