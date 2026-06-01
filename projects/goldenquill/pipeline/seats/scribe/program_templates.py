"""pipeline.seats.scribe.program_templates — §7.9 program-specific templates.

Blueprint §7 Scribe v1.1.1 §7.9 LOCKED 2026-04-21. Pure data + pure
constructor. Zero I/O at R2 — Phase 0 template file read + hash-pin lands
at R3 when ``pipeline.vault`` surfaces are available.

v0.1 ships eight known programs (§7.9 enumeration): VAPG, REAP, SCBGP,
SARE, SBIR, AFRI, 2501 (Outreach), UAIP. New programs land as row-append
to ``KNOWN_PROGRAMS`` — no core refactor per §7.9 extensibility pin.

The ``template_content_sha3_512`` field is synthesized at R2 via
:func:`compute_template_sha3_512` over the canonical serialized content
cues; at R3 the field reflects the actual template markdown content-hash
for TOCTOU enforcement via PRE-gate ``F-SCRIBE-TEMPLATE-DRIFT``.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Callable, Final, Mapping

from pipeline.seats.scribe.dialect import Dialect
from pipeline.seats.scribe.types import SectionSpec


ClockFn = Callable[[], datetime]


def _default_utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


_SHA3_512_HEX_LEN: Final[int] = 128
_HEX_CHARS: Final[frozenset[str]] = frozenset("0123456789abcdef")


def _is_lowercase_hex(s: str) -> bool:
    return len(s) > 0 and all(ch in _HEX_CHARS for ch in s)


@dataclass(frozen=True, kw_only=True, slots=True)
class ProgramTemplate:
    """§7.9 template contract — program code + overrides + content cues +
    dialect default + content hash.
    """

    program_code: str
    section_overrides: Mapping[str, SectionSpec]
    required_content_cues: tuple[str, ...]
    dialect_default: Dialect
    template_content_sha3_512: str
    template_at_utc: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.program_code, str) or not self.program_code.strip():
            raise ValueError("ProgramTemplate.program_code must be non-empty.")
        if len(self.template_content_sha3_512) != _SHA3_512_HEX_LEN:
            raise ValueError(
                f"ProgramTemplate.template_content_sha3_512 must be "
                f"{_SHA3_512_HEX_LEN} hex chars; got "
                f"{len(self.template_content_sha3_512)!r}."
            )
        if not _is_lowercase_hex(self.template_content_sha3_512):
            raise ValueError(
                "ProgramTemplate.template_content_sha3_512 must be lowercase hex."
            )
        if self.template_at_utc.tzinfo is None:
            raise ValueError(
                "ProgramTemplate.template_at_utc must be timezone-aware."
            )
        if len(self.required_content_cues) == 0:
            raise ValueError(
                f"ProgramTemplate({self.program_code!r}).required_content_cues "
                f"must be non-empty."
            )
        # Freeze section_overrides if the caller passed a plain dict.
        if not isinstance(self.section_overrides, MappingProxyType):
            object.__setattr__(
                self,
                "section_overrides",
                MappingProxyType(dict(self.section_overrides)),
            )


# §7.9 — eight known programs at v0.1. Values are source-of-truth cue
# tuples + dialect defaults. Operator-extensible row-append discipline.
KNOWN_PROGRAMS: Final[Mapping[str, Mapping[str, object]]] = MappingProxyType(
    {
        "VAPG": MappingProxyType(
            {
                "required_content_cues": (
                    "feasibility study reference",
                    "marketing plan",
                    "producer ownership",
                    "value-added methodology",
                    "independent producer or cooperative status",
                ),
                "dialect_default": "conservative",
            }
        ),
        "REAP": MappingProxyType(
            {
                "required_content_cues": (
                    "energy audit",
                    "baseline vs projected energy use",
                    "payback period",
                    "technical report",
                ),
                "dialect_default": "conservative",
            }
        ),
        "SCBGP": MappingProxyType(
            {
                "required_content_cues": (
                    "industry-wide benefit",
                    "measurable dissemination plan",
                    "specialty crop focus",
                ),
                "dialect_default": "conservative",
            }
        ),
        "SARE": MappingProxyType(
            {
                "required_content_cues": (
                    "farmer involvement",
                    "sustainable ag practices",
                    "research / education integration",
                ),
                "dialect_default": "progressive",
            }
        ),
        "SBIR": MappingProxyType(
            {
                "required_content_cues": (
                    "technical innovation",
                    "commercialization potential",
                    "Phase I / II structure",
                ),
                "dialect_default": "centrist",
            }
        ),
        "AFRI": MappingProxyType(
            {
                "required_content_cues": (
                    "scientific merit",
                    "clear hypotheses",
                    "preliminary data",
                    "broader impacts",
                ),
                "dialect_default": "centrist",
            }
        ),
        "2501": MappingProxyType(
            {
                "required_content_cues": (
                    "outreach plan for SDA / veterans",
                    "capacity-building focus",
                ),
                "dialect_default": "progressive",
            }
        ),
        "UAIP": MappingProxyType(
            {
                "required_content_cues": (
                    "food access",
                    "equity",
                    "urban partnerships",
                ),
                "dialect_default": "progressive",
            }
        ),
    }
)


def compute_template_sha3_512(content_bytes: bytes) -> str:
    """Return the full 128-hex SHA-3-512 hash of ``content_bytes``.

    Canonical content-addressing per §2 Vault discipline. R3 Phase 0 /
    Phase 2 re-read both compute this and compare for
    ``F-SCRIBE-TEMPLATE-DRIFT`` enforcement.
    """
    if not isinstance(content_bytes, (bytes, bytearray)):
        raise TypeError(
            f"compute_template_sha3_512: content_bytes must be bytes; got "
            f"{type(content_bytes).__name__}."
        )
    return hashlib.sha3_512(bytes(content_bytes)).hexdigest()


def _synthesize_known_content_bytes(program_code: str) -> bytes:
    """Canonicalize the KNOWN_PROGRAMS cue tuple into a hashable byte string.

    Used at R2 to populate ``template_content_sha3_512`` without touching
    the filesystem. R3 replaces this with a real file read from
    ``skills/scribe-ghostwriter/templates/<program>.md``.
    """
    entry = KNOWN_PROGRAMS[program_code]
    cues = entry["required_content_cues"]
    dialect = entry["dialect_default"]
    parts: list[str] = [f"program_code={program_code}"]
    for cue in cues:  # type: ignore[attr-defined]
        parts.append(f"cue={cue}")
    parts.append(f"dialect_default={dialect}")
    return "\n".join(parts).encode("utf-8")


def build_known_template(
    program_code: str,
    *,
    clock: ClockFn = _default_utc_now,
) -> ProgramTemplate:
    """Construct a :class:`ProgramTemplate` from the KNOWN_PROGRAMS registry.

    Raises ``KeyError`` with a clear message for unknown codes — R3 maps
    this to PRE-gate ``F-SCRIBE-TEMPLATE-UNKNOWN``.
    """
    if program_code not in KNOWN_PROGRAMS:
        raise KeyError(
            f"Unknown program_code {program_code!r}. Known programs: "
            f"{sorted(KNOWN_PROGRAMS)}."
        )
    entry = KNOWN_PROGRAMS[program_code]
    content_bytes = _synthesize_known_content_bytes(program_code)
    sha = compute_template_sha3_512(content_bytes)
    return ProgramTemplate(
        program_code=program_code,
        section_overrides={},  # R2 synthesizes no overrides; operator custom
                               # templates at R3+ may carry overrides
        required_content_cues=tuple(entry["required_content_cues"]),  # type: ignore[arg-type]
        dialect_default=entry["dialect_default"],  # type: ignore[arg-type]
        template_content_sha3_512=sha,
        template_at_utc=clock(),
    )


__all__ = [
    "ProgramTemplate",
    "KNOWN_PROGRAMS",
    "ClockFn",
    "compute_template_sha3_512",
    "build_known_template",
]
