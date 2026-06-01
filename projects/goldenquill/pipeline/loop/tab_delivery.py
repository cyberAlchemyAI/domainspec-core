"""pipeline.loop.tab_delivery — §4.11 three-tab envelope ordering + signing (Round 9).

Blueprint §5 v6 LOCKED 2026-04-19:
- §4.11 v3 ``assemble_and_deliver`` (lines 691-747) — inline-literal runtime
  tab-order check + module-load integrity assert + post-write envelope-hash
  verification.
- §3.2.6 ``TabEnvelope`` (v2 ``tab_ordering`` typed ``Final``) — Round 1
  dataclass consumed here via construction + :func:`dataclasses.replace`.
- §3.5 banned pattern (line 381, A-v1-06 closure) — NO ``TabEnvelope(`` call
  with inline tuple/list as ``tab_ordering`` arg; always reference
  ``TAB_ORDERING``.
- §4.1 step 11 — tab delivery follows ``report_signed`` + precedes
  ``tabs_delivered``. Round 9 does NOT mutate ``RunState.phase`` or
  ``RunState.three_tab_envelope_hash`` — those mutations belong to the
  capstone Round wiring (Round 10+) and the §5 `assemble_and_deliver` caller
  whose job is to sequence them.
- §4.15 export-bundle exclusion (line 916) — eval-mode reaching R9 raises
  :class:`F_PIPE_21` with trigger ``"eval_run_reached_tab_delivery"``. The
  entry gate compares ``run_state.mode`` against the INLINE LITERAL
  ``"submission"`` (V1 discipline; rebind-resistant).
- §6 F-PIPE-16 (``tab_envelope_ordering_violation``) + F-PIPE-01
  (``run_state_corrupt`` — post-write hash mismatch path, B-v1-09 closure) +
  F-PIPE-21 (``eval_run_reached_tab_delivery``, §4.15 shield).
- §8 ``TAB_ORDERING: Final[tuple[...]]`` constant with module-load integrity
  assert (mirrors Round 1 ``config.py``).

**Core design decisions (confirmed at Round 9 ORIENT — 2026-04-21)**

1. *Inline-literal rebind-resistance (V1 discipline).* The tab-ordering tuple
   ``("live_radar", "deep_brief", "council_draft")`` and the mode sentinel
   string ``"submission"`` appear as inline literals at every comparison
   site. A rebind of ``pipeline.loop.config.TAB_ORDERING`` OR of any
   module-level ``"submission"`` string literal cannot subvert runtime
   behaviour. Module-load asserts catch rebind-before-load.

2. *No wrapper exception classes.* The spec card proposed
   ``TabOrderViolation`` / ``TabDeliveryError`` wrappers around F_PIPE_16 /
   F_PIPE_01 but ORIENT resolution is to raise the F-PIPE codes directly
   (matches Round 7 precedent of raising :class:`F_PIPE_06` bare rather
   than wrapping).

3. *Canonical-bytes are module-level helpers, not dataclass methods.*
   Round 1's :class:`TabEnvelope` ships LOCKed without ``canonical_bytes``
   / ``canonical_bytes_without_self_hash`` methods. Round 9 adds them as
   free functions (``_canonical_bytes`` / ``_canonical_bytes_without_self_hash``)
   rather than mutating the frozen dataclass post-LOCK. Shape matches
   Round 2 + Round 6 + Round 7 canonicalizer template:
   ``json.dumps(asdict(envelope), sort_keys=True, separators=(",",":"))``.

4. *``write_mode="write-if-absent"``.* Blueprint §4.11 is silent on
   write_mode. Each ``run_id`` produces exactly one envelope, so write-if-
   absent provides CAS-style duplicate-write protection. A second
   :func:`deliver_tab` for the same ``run_id`` surfaces
   :class:`pipeline.vault.error_codes.VaultWriteExists` propagated
   unwrapped (E-023 trusted-operator residual — documented below).

5. *``intent="state-success"`` interim pattern.* Blueprint §4.11 line 736
   flags this as interim until a dedicated ``tab-envelope-write`` intent
   lands in a future §2 amendment (OQ-3). Round 9 matches; no-op swap
   once the intent is added.

6. *Payload-path derivation.* Blueprint §4.11 hardcodes three vault paths
   that reference ``run_state.run_id_date`` (date prefix) and ``final_N``
   (last iteration number). Round 1 ``RunState`` does not expose these
   directly, so Round 9 derives them locally:

   - ``run_id_date`` = ``run_state.started_at_iso[:10]`` (ISO-8601 date
     prefix; e.g. ``"2026-04-21"``). Empty on un-started RunState — the
     caller is expected to stamp ``started_at_iso`` at ``start_run``.
   - ``final_N`` = ``len(run_state.iterations)`` (the iteration count
     after the inner revision loop completes).

   The three paths are:

   - ``vault/fund_radar/{run_id_date}/live_radar.json``
   - ``vault/deep_brief/{run_state.run_id}/brief.md``
   - ``vault/pipeline/{run_state.run_id}/iter_{final_N}/scribe_draft.md``

7. *Signature-chain depth 1.* v0.1 ships a single envelope signature
   (the ``envelope_sha256`` SHA-256 over canonical-bytes-without-self-hash).
   No per-tab detached signatures; no multi-tab signing ceremony. Future
   Stage-2+ multi-tab signatures are out of scope.

**Threat model (§3.11 v5 trusted-operator envelope; E-023 residual surface)**

Round 9 is a §5 orchestrator primitive — no network, no subprocess, no
§4 Logician consumption (see the R9 Cedar / compound_commit carve-out in
``pipeline/engineering/spec_cards/section_05_round_9_tab_delivery.md``).
The following adversarial residuals are OUT-OF-SCOPE for v0.1 and
documented here so the threat-model surface is visible at the call-site:

- **Malformed envelope bytes at read-back.** If ``vault_read`` returns
  bytes that :func:`_parse_envelope` cannot decode, a ``json.JSONDecodeError``
  or ``KeyError`` propagates unwrapped (trusted-operator contract: the
  §2 vault CAS head guarantees byte-identical read-back of what we just
  wrote; any drift is a §2 invariant violation, not a Round 9 concern).

- **Missing signature file.** NOT applicable in v0.1 — Round 9 emits a
  single signed envelope; there are no detached signature files.

- **Half-signed tab.** NOT applicable in v0.1 — the envelope is one
  artefact covering all three payload hashes; partial signing cannot
  occur.

- **Zero-tab delivery.** NOT applicable — :class:`TabEnvelope`'s shape
  requires three non-optional payload-hash fields. Round 9 additionally
  asserts all three ``hash_file`` returns are non-empty strings before
  constructing the envelope (programmer contract — surface
  ``ValueError``).

- **Duplicate dispatch per ``run_id``.** ``write-if-absent`` is the
  CAS-style guardrail; a second :func:`deliver_tab` call for the same
  ``run_id`` surfaces :class:`VaultWriteExists` propagated unwrapped
  (E-023 trusted-operator residual).

- **Missing payload file.** ``hash_file`` raises
  :class:`FileNotFoundError` (or another OS error) — propagates
  unwrapped; no vault_write happens.

- **Non-monotonic clock.** ``assembled_at_iso`` is display-only metadata;
  it is included in the canonical-bytes hash (so a decreasing clock
  produces a stable-but-unusual timestamp). Downstream readers trust
  the envelope_sha256, not the wallclock.

Spec card:
``pipeline/engineering/spec_cards/section_05_round_9_tab_delivery.md``.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, is_dataclass, replace
from typing import Any, Final, Protocol, runtime_checkable

from pipeline.loop.config import TAB_ORDERING
from pipeline.loop.errors import F_PIPE_01, F_PIPE_16, F_PIPE_21
from pipeline.loop.run_lifecycle import VaultReadCallable
from pipeline.loop.state_checkpoint import ClockProtocol, VaultWriteCallable
from pipeline.loop.types import RunState, TabEnvelope

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_05_pipeline.md": {
        "version": "v6",
        "hash_sha3_512_prefix16": "feb5928491e4dc40",
        "sections_implemented": [
            "§4.11 v3 assemble_and_deliver (tab envelope + signing)",
            "§3.2.6 TabEnvelope consumption + replace() with computed sha256",
            "§4.15 export-bundle exclusion (eval-mode shield)",
            "§6 F-PIPE-16 tab_envelope_ordering_violation",
            "§6 F-PIPE-01 run_state_corrupt (post-write hash mismatch)",
            "§6 F-PIPE-21 eval_run_reached_tab_delivery",
        ],
    },
}


# ---------------------------------------------------------------------------
# Inline-literal module-load integrity asserts (V1 discipline)
# ---------------------------------------------------------------------------

assert TAB_ORDERING == ("live_radar", "deep_brief", "council_draft"), (
    "pipeline.loop.config.TAB_ORDERING has been rebound before "
    "pipeline.loop.tab_delivery import; refusing to load"
)


# ---------------------------------------------------------------------------
# Public Protocols (E-017 injected-callable pattern)
# ---------------------------------------------------------------------------


@runtime_checkable
class HashFileCallable(Protocol):
    """Injected payload-hash reader — SHA-256 hex over the file at ``path``.

    Round 9 does NOT read payload bytes itself; every payload-hash is
    computed by the injected :class:`HashFileCallable`. Production wires a
    concrete reader that streams the vault file and hashes it; tests pin
    per-path hashes deterministically without touching the filesystem.

    Return contract: non-empty SHA-256 hex string (64 lowercase chars).
    An empty or missing file surfaces as a ``FileNotFoundError`` or
    similar OS error from the callable, propagated unwrapped to the
    caller of :func:`deliver_tab`.
    """

    def __call__(self, path: str) -> str: ...


# ---------------------------------------------------------------------------
# Public result dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class TabSigningResult:
    """Returned on successful :func:`deliver_tab` completion.

    - ``envelope``: the signed :class:`TabEnvelope` (post-``replace`` with
      the computed ``envelope_sha256``).
    - ``stored_envelope_hash``: the ``envelope_sha256`` observed in the
      post-write vault_read. Must equal ``envelope.envelope_sha256`` — the
      B-v1-09 closure; a mismatch raises :class:`F_PIPE_01` before this
      dataclass is constructed.
    - ``vault_path``: the vault-relative path at which the envelope was
      committed (``pipeline/{run_id}/tab_envelope.json``).
    - ``written_at_iso``: the ``assembled_at_iso`` baked into the envelope
      (equals ``clock.now_iso()`` at the moment of envelope construction).
    """

    envelope: TabEnvelope
    stored_envelope_hash: str
    vault_path: str
    written_at_iso: str


# ---------------------------------------------------------------------------
# Internal canonicalization
# ---------------------------------------------------------------------------


def _canonical_default(obj: Any) -> Any:
    """``json.dumps`` default handler — mirrors Round 2 / Round 6 shape."""
    if is_dataclass(obj) and not isinstance(obj, type):
        return asdict(obj)
    if isinstance(obj, (frozenset, set)):
        return sorted(obj)
    if isinstance(obj, tuple):
        return list(obj)
    return {"__repr__": repr(obj)}


def _canonical_bytes(envelope: TabEnvelope) -> bytes:
    """Deterministic canonical-bytes for a :class:`TabEnvelope`.

    ``sort_keys=True`` + ``separators=(",", ":")`` + UTF-8 encoding.
    Includes ``envelope_sha256`` — this is the shape written to the vault.
    """
    payload = asdict(envelope)
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        default=_canonical_default,
    ).encode("utf-8")


def _canonical_bytes_without_self_hash(envelope: TabEnvelope) -> bytes:
    """Canonical-bytes with ``envelope_sha256`` removed.

    Used to compute the envelope's own ``envelope_sha256`` — a hash that
    includes itself would be unsatisfiable. The placeholder envelope
    passed here has ``envelope_sha256=""``; the field is popped before
    serialisation so the computed hash is independent of any placeholder
    value.
    """
    payload = asdict(envelope)
    payload.pop("envelope_sha256", None)
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        default=_canonical_default,
    ).encode("utf-8")


def _parse_envelope(raw: bytes) -> TabEnvelope:
    """Reverse of :func:`_canonical_bytes` — reconstruct a :class:`TabEnvelope`.

    JSON deserialization loses the ``tuple`` type; ``tab_ordering`` comes
    back as a list and is re-tupled before constructing the frozen
    dataclass. Any field mismatch (missing key, wrong type) raises
    ``KeyError`` / ``TypeError`` unwrapped — trusted-operator contract.

    :class:`TabEnvelope.__post_init__` re-runs the inline-literal
    tab-ordering check; a stored envelope whose ``tab_ordering`` was
    corrupted after write would raise :class:`F_PIPE_16` here.
    """
    payload = json.loads(raw.decode("utf-8"))
    tab_ordering_raw = payload["tab_ordering"]
    # JSON arrays deserialize as lists; re-tuple for TabEnvelope shape.
    tab_ordering = tuple(tab_ordering_raw)
    return TabEnvelope(
        run_id=payload["run_id"],
        tab_ordering=tab_ordering,  # type: ignore[arg-type]
        live_radar_payload_hash=payload["live_radar_payload_hash"],
        deep_brief_payload_hash=payload["deep_brief_payload_hash"],
        council_draft_payload_hash=payload["council_draft_payload_hash"],
        assembled_at_iso=payload["assembled_at_iso"],
        envelope_sha256=payload["envelope_sha256"],
    )


# ---------------------------------------------------------------------------
# Public API — deliver_tab
# ---------------------------------------------------------------------------


def deliver_tab(
    *,
    run_state: RunState,
    vault_read: VaultReadCallable,
    vault_write: VaultWriteCallable,
    clock: ClockProtocol,
    hash_file: HashFileCallable,
) -> TabSigningResult:
    """§4.11 v3 — assemble, sign, and deliver the three-tab envelope.

    **Sequence:**

    1. §4.15 eval-mode shield — ``run_state.mode != "submission"`` raises
       :class:`F_PIPE_21` with trigger ``"eval_run_reached_tab_delivery"``
       BEFORE any vault or hash_file interaction.
    2. Derive the three payload paths (live_radar / deep_brief /
       council_draft) from ``run_state`` (blueprint §4.11 lines 693-696).
    3. Invoke ``hash_file`` exactly three times — once per payload path,
       in declaration order.
    4. Stamp ``assembled_at_iso = clock.now_iso()``.
    5. Construct a placeholder :class:`TabEnvelope` with
       ``envelope_sha256=""`` (shape-valid; :class:`TabEnvelope.__post_init__`
       validates ``tab_ordering`` at construction time via an inline
       tuple literal).
    6. Compute ``envelope_sha256`` from
       :func:`_canonical_bytes_without_self_hash` of the placeholder, then
       :func:`dataclasses.replace` with the final hash.
    7. V1 inline-literal check: confirm ``envelope.tab_ordering ==
       ("live_radar", "deep_brief", "council_draft")``. A rebound
       ``TAB_ORDERING`` at construction time would pass Round 1's
       ``__post_init__`` (which uses its own inline literal) but Round 9
       re-asserts the invariant at the call site as defence-in-depth.
    8. ``vault_write`` the canonical bytes WITH self-hash at
       ``pipeline/{run_id}/tab_envelope.json`` via
       ``intent="state-success"`` (interim; OQ-3 tracked) +
       ``write_mode="write-if-absent"`` (one envelope per run_id).
    9. B-v1-09 post-write verification — ``vault_read`` the envelope back,
       :func:`_parse_envelope` it, assert
       ``stored.envelope_sha256 == envelope.envelope_sha256`` or raise
       :class:`F_PIPE_01` with trigger ``"tab_envelope_hash_mismatch"``.
    10. Return :class:`TabSigningResult`.

    Parameters
    ----------
    run_state
        Live :class:`RunState`. Must have ``mode == "submission"``; any
        other value (including ``"eval"``) raises :class:`F_PIPE_21`.
        Round 9 does NOT mutate ``run_state`` — phase transitions to
        ``"tabs_delivered"`` belong to the capstone caller.
    vault_read, vault_write, clock, hash_file
        Injected Protocols (see module-level docs).

    Raises
    ------
    F_PIPE_21
        ``run_state.mode != "submission"`` — eval-mode reached tab
        delivery.
    F_PIPE_16
        Tab-ordering invariant violated (defence-in-depth; Round 1's
        :class:`TabEnvelope.__post_init__` has the first-line check).
    F_PIPE_01
        Post-write envelope-hash mismatch — vault read-back returned
        different bytes than were written.
    ValueError
        ``hash_file`` returned an empty string for one or more payload
        paths (programmer-contract violation).
    VaultWriteExists
        Duplicate :func:`deliver_tab` for the same ``run_id`` (the
        ``write-if-absent`` CAS guardrail fired). E-023 residual.
    """
    # Step 1 — §4.15 eval-mode shield. Inline-literal "submission".
    if run_state.mode != "submission":
        raise F_PIPE_21(
            trigger="eval_run_reached_tab_delivery",
            details={
                "run_id": run_state.run_id,
                "observed_mode": run_state.mode,
            },
        )

    # Step 2 — derive the three payload paths.
    # run_id_date is the ISO date prefix of started_at_iso (YYYY-MM-DD).
    # final_N is the iteration count at report_signed.
    run_id_date = run_state.started_at_iso[:10]
    final_n = len(run_state.iterations)

    live_radar_path = f"vault/fund_radar/{run_id_date}/live_radar.json"
    deep_brief_path = f"vault/deep_brief/{run_state.run_id}/brief.md"
    council_draft_path = (
        f"vault/pipeline/{run_state.run_id}/iter_{final_n}/scribe_draft.md"
    )

    # Step 3 — hash each payload (order fixed; three calls exactly).
    live_radar_hash = hash_file(live_radar_path)
    deep_brief_hash = hash_file(deep_brief_path)
    council_draft_hash = hash_file(council_draft_path)

    # Programmer-contract defence (E-023 zero-tab impossibility): reject
    # empty hashes before constructing the envelope. Round 1's
    # :class:`TabEnvelope` dataclass does not enforce non-empty hashes.
    if not (live_radar_hash and deep_brief_hash and council_draft_hash):
        raise ValueError(
            "hash_file returned empty payload hash; refusing to assemble "
            f"tab envelope for run_id={run_state.run_id!r}"
        )

    # Step 4 — stamp timestamp.
    assembled_at_iso = clock.now_iso()

    # Step 5 — build placeholder envelope. MUST reference TAB_ORDERING
    # constant (A-v1-06 AST-grep ban); never an inline tuple literal here.
    placeholder = TabEnvelope(
        run_id=run_state.run_id,
        tab_ordering=TAB_ORDERING,
        live_radar_payload_hash=live_radar_hash,
        deep_brief_payload_hash=deep_brief_hash,
        council_draft_payload_hash=council_draft_hash,
        assembled_at_iso=assembled_at_iso,
        envelope_sha256="",
    )

    # Step 6 — compute envelope_sha256 from canonical-bytes-without-self.
    envelope_sha256 = hashlib.sha256(
        _canonical_bytes_without_self_hash(placeholder)
    ).hexdigest()
    envelope = replace(placeholder, envelope_sha256=envelope_sha256)

    # Step 7 — V1 rebind-resistant tab-order check (inline-literal RHS).
    # Defence-in-depth over Round 1's __post_init__ check; both raise
    # F_PIPE_16 on violation. Unreachable in practice because Round 1's
    # frozen-dataclass __post_init__ fires first on any bad tab_ordering
    # at construction time; retained for V1 discipline (inline-literal at
    # every comparison site).
    if envelope.tab_ordering != ("live_radar", "deep_brief", "council_draft"):  # pragma: no cover
        raise F_PIPE_16(
            trigger="tab_envelope_ordering_violation",
            details={
                "run_id": run_state.run_id,
                "observed": envelope.tab_ordering,
            },
        )

    # Step 8 — vault_write the canonical bytes.
    vault_path = f"pipeline/{run_state.run_id}/tab_envelope.json"
    payload = _canonical_bytes(envelope)
    vault_write(
        path=vault_path,
        payload=payload,
        intent="state-success",
        write_mode="write-if-absent",
        expected_current_file_hash=None,
    )

    # Step 9 — B-v1-09 post-write verification.
    stored_bytes = vault_read(path=vault_path)
    stored = _parse_envelope(stored_bytes)
    if stored.envelope_sha256 != envelope.envelope_sha256:
        raise F_PIPE_01(
            trigger="tab_envelope_hash_mismatch",
            details={
                "run_id": run_state.run_id,
                "expected": envelope.envelope_sha256,
                "observed": stored.envelope_sha256,
                "vault_path": vault_path,
            },
        )

    # Step 10 — return signed result.
    return TabSigningResult(
        envelope=envelope,
        stored_envelope_hash=stored.envelope_sha256,
        vault_path=vault_path,
        written_at_iso=assembled_at_iso,
    )


__all__ = [
    "BLUEPRINT_DEPS",
    "HashFileCallable",
    "TabSigningResult",
    "deliver_tab",
]
