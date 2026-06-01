"""pipeline.orchestrator.scribe_envelope_builder — production builder for
the Scribe seat IPC envelope, with sector-knowledge-pack injection.

Why this module exists
----------------------
Scribe seat consumes :class:`pipeline.seats.scribe.types.ScribeEnvelope`
v1 — frozen, kw-only, slots, schema-validated at construction time. Until
this module landed, the envelope was constructed implicitly via
``decode_envelope`` parsing JSON bytes from stdin; there was no
production Python builder. New v0.2 sector-knowledge-pack work
(``pipeline.seats.scribe.knowledge_packs``) needs a stable construction
site to inject pack content into ``project_context`` before the
envelope is sealed and shipped to the Scribe subprocess.

This module provides that construction site:

- :func:`build_scribe_envelope` — accepts already-prepared inputs
  (compiled_prompt + its shell hash, project_context, run metadata) and
  returns a sealed :class:`ScribeEnvelope`. Optionally takes a
  ``sector`` arg; when set, loads the sector pack and merges its
  rendered context block into ``project_context`` under the
  :data:`PROJECT_CONTEXT_PACK_KEY` key before constructing the envelope.
- :func:`emit_scribe_envelope_bytes` — serializes a built envelope to
  the JSON shape ``decode_envelope`` parses. Use this when handing the
  envelope to a subprocess via stdin.

Sector merge semantics
----------------------
- ``sector=None`` → no pack merge; project_context passes through.
  Backward-compatible with callers not yet sector-aware.
- ``sector="<sector>"`` (must be in :data:`SECTOR_VALID`) → loads pack
  via :func:`load_sector_pack`, merges via
  :func:`merge_pack_into_project_context`. If the sector dir is empty
  on disk, the merge surfaces ``loaded=False`` under the
  ``sector_knowledge`` key (no error — operator hasn't seeded yet).

Hash discipline
---------------
``compiled_prompt_shell_sha3_512`` is **caller-supplied** — this builder
does not compute the shell hash. The shell hash is the SHA3-512 of the
immutable prompt-shell portion (system frame + role frame + RFA header)
that the prompt-assembler emits alongside the compiled prompt; this
builder receives both and threads them into the envelope unchanged.
That separation keeps the builder agnostic of prompt-assembly internals.

What this builder does NOT do
-----------------------------
- It does NOT assemble the compiled prompt. That's a separate concern
  (prompt-assembler) — when that lands, it calls this builder with the
  compiled_prompt + shell hash already prepared.
- It does NOT validate ``operator_override_dialect`` against the
  closed enum — that validation lives on the
  :class:`ScribeEnvelope` constructor (``__post_init__``). The builder
  passes the value through and lets the dataclass enforce its invariant.
- It does NOT load PROJECT_CONTEXT.md from disk. The caller passes a
  parsed mapping; the builder treats it as opaque (apart from the
  sector merge).

Sovereignty / dependency posture
--------------------------------
Pure stdlib (``json``, ``datetime``, ``typing``) plus the existing Tilth
locked-substrate imports. Adheres to ``pyproject.toml`` § ``[project]``.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Callable, Final, Mapping, Optional

from pipeline.seats.scribe.knowledge_packs import (
    KnowledgePack,
    SECTOR_VALID,
    load_sector_pack,
    merge_pack_into_project_context,
)
from pipeline.seats.scribe.seat import ScribeEnvelope


# --------------------------------------------------------------------------
# Public protocols + types
# --------------------------------------------------------------------------

ClockFn = Callable[[], datetime]


def _default_utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


# Envelope schema version we emit. Mirrored against
# ``ScribeEnvelope.__post_init__`` literal check — must stay in sync.
ENVELOPE_VERSION: Final[str] = "scribe-envelope.v1"


# --------------------------------------------------------------------------
# Exceptions
# --------------------------------------------------------------------------

class EnvelopeBuilderError(Exception):
    """Base class for builder-time failures (pre-construction validation)."""


class InvalidSectorError(EnvelopeBuilderError):
    """Caller passed a sector name not in :data:`SECTOR_VALID`."""


# --------------------------------------------------------------------------
# Public entry points
# --------------------------------------------------------------------------

def build_scribe_envelope(
    *,
    # Run metadata
    run_id: str,
    org_slug: str,
    iteration_number: int,
    section_name: str,
    section_order: int,
    # Dialect + program
    funder_dialect: str,
    operator_override_dialect: Optional[str],
    program_code: str,
    # Risk register pin
    admin_risk_register_snapshot_path: str,
    admin_risk_snapshot_age_hours: float,
    conversation_log_anchor: Optional[str],
    # Prompt + caller-supplied shell hash
    compiled_prompt: str,
    compiled_prompt_shell_sha3_512: str,
    # Context (pre-pack merge)
    project_context: Mapping[str, Any],
    # v0.2 — sector pack merge (optional)
    sector: Optional[str] = None,
    # E-017 testability seam
    clock: Optional[ClockFn] = None,
) -> ScribeEnvelope:
    """Construct a sealed :class:`ScribeEnvelope` with optional sector merge.

    When *sector* is set (and is in :data:`SECTOR_VALID`), the builder
    loads the corresponding pack via :func:`load_sector_pack` and merges
    its rendered context block into *project_context* under the
    ``sector_knowledge`` key before sealing the envelope. When *sector*
    is None, *project_context* passes through unchanged.

    All envelope-shape invariants (envelope_version literal, sha3-512
    length, timezone-aware emitted-at, dialect enum) are enforced by
    :class:`ScribeEnvelope.__post_init__`. The builder constructs and
    lets the dataclass raise on contract violation — fail-fast at
    construction site, not deferred to subprocess decode.

    Args:
        run_id: Stable run identifier — propagates through Logician
            hashing and POST-gate result attribution.
        org_slug: Org-isolation key per Law 3. Must be non-empty.
        iteration_number: Which revision pass this envelope drives
            (0 for first draft).
        section_name: RFA-required section being drafted.
        section_order: 1-indexed canonical order from RFA section spec.
        funder_dialect: Closed-enum dialect (conservative / centrist /
            progressive / soul_fire). See ``pipeline.seats.scribe.dialect``.
        operator_override_dialect: Optional operator-set override; None
            when the auto-classified dialect stands.
        program_code: RFA program code (e.g. "VAPG", "REAP", "SCBGP").
        admin_risk_register_snapshot_path: Path to the version-pinned
            admin-risk register snapshot used for this draft.
        admin_risk_snapshot_age_hours: Hours since the snapshot was
            written (for F-SCRIBE-ADMIN-RISK-REGISTER-STALE 24h check).
        conversation_log_anchor: Optional anchor into the run-scoped
            conversation log for ConversationAnchor verification.
        compiled_prompt: Pre-assembled prompt body. Caller's prompt-
            assembler is responsible for content; builder does not edit.
        compiled_prompt_shell_sha3_512: SHA-3-512 hex of the immutable
            prompt-shell portion. Caller-supplied; 128 lowercase hex chars.
        project_context: Parsed PROJECT_CONTEXT mapping. Treated as
            opaque except for the sector pack merge.
        sector: Optional sector slug (must be in :data:`SECTOR_VALID`).
            When set, sector pack is loaded and merged into project_context.
        clock: E-017 testability seam — defaults to
            ``datetime.now(tz=timezone.utc)``. Tests inject fixed clocks.

    Returns:
        Sealed :class:`ScribeEnvelope` ready for serialization or
        in-process handoff.

    Raises:
        :class:`InvalidSectorError`: *sector* is not in :data:`SECTOR_VALID`.
        :class:`pipeline.seats.scribe.types.ScribeEnvelopeMalformed`: any
            envelope-shape invariant tripped.
    """
    # 1) Sector pack merge (if requested)
    augmented_project_context: Mapping[str, Any] = project_context
    if sector is not None:
        if sector not in SECTOR_VALID:
            raise InvalidSectorError(
                f"sector={sector!r} not in {sorted(SECTOR_VALID)}"
            )
        pack = load_sector_pack(sector)
        augmented_project_context = merge_pack_into_project_context(
            project_context, pack
        )

    # 2) Emitted-at (E-017 clock seam)
    emitted_at = (clock or _default_utc_now)()

    # 3) Construct envelope — ScribeEnvelope.__post_init__ enforces all
    # invariants (version literal, hex length/case, dialect enum, etc.)
    return ScribeEnvelope(
        envelope_version=ENVELOPE_VERSION,
        run_id=run_id,
        org_slug=org_slug,
        iteration_number=iteration_number,
        section_name=section_name,
        section_order=section_order,
        funder_dialect=funder_dialect,
        operator_override_dialect=operator_override_dialect,
        program_code=program_code,
        admin_risk_register_snapshot_path=admin_risk_register_snapshot_path,
        admin_risk_snapshot_age_hours=admin_risk_snapshot_age_hours,
        conversation_log_anchor=conversation_log_anchor,
        compiled_prompt_shell_sha3_512=compiled_prompt_shell_sha3_512,
        compiled_prompt=compiled_prompt,
        project_context=augmented_project_context,
        envelope_emitted_at_utc=emitted_at,
    )


def emit_scribe_envelope_bytes(envelope: ScribeEnvelope) -> bytes:
    """Serialize *envelope* to UTF-8 JSON bytes for subprocess stdin.

    The output shape matches what :func:`pipeline.seats.scribe.seat.decode_envelope`
    parses. Datetimes are emitted as ISO-8601 with timezone offset;
    MappingProxyType project_context is unwrapped to a plain dict for
    JSON encodability.
    """
    payload: dict[str, Any] = {
        "envelope_version": envelope.envelope_version,
        "run_id": envelope.run_id,
        "org_slug": envelope.org_slug,
        "iteration_number": envelope.iteration_number,
        "section_name": envelope.section_name,
        "section_order": envelope.section_order,
        "funder_dialect": envelope.funder_dialect,
        "operator_override_dialect": envelope.operator_override_dialect,
        "program_code": envelope.program_code,
        "admin_risk_register_snapshot_path": envelope.admin_risk_register_snapshot_path,
        "admin_risk_snapshot_age_hours": envelope.admin_risk_snapshot_age_hours,
        "conversation_log_anchor": envelope.conversation_log_anchor,
        "compiled_prompt_shell_sha3_512": envelope.compiled_prompt_shell_sha3_512,
        "compiled_prompt": envelope.compiled_prompt,
        "project_context": dict(envelope.project_context),
        "envelope_emitted_at_utc": envelope.envelope_emitted_at_utc.isoformat(),
    }
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


__all__ = [
    "ENVELOPE_VERSION",
    "EnvelopeBuilderError",
    "InvalidSectorError",
    "ClockFn",
    "build_scribe_envelope",
    "emit_scribe_envelope_bytes",
]
