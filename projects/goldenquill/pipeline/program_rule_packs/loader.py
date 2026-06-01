"""pipeline.program_rule_packs.loader — Program Rule Pack (PRP) loader.

v0.1 DRAFT scaffold. Mirrors the shape of pipeline.cards.loader so that the
two loader families share lifecycle/signing/manifest-binding discipline, but
NONE of the gate bodies are realized at v0.1 — every body raises
NotImplementedError("v0.2 first wave"), and the top-level entry point
load_active_prps() itself also raises NotImplementedError so that any seat
that wires PRP enforcement before v0.2 first wave fails-closed with a clear
refusal rather than silently dispatching.

Loader contract (ordered) — bodies graduate at v0.2 first wave:
  1. Read manifest from disk (pipeline/program_rule_packs/_manifest/active_prps.yaml).
  2. For each entry in active_prps:
     a. Verify entry is in active manifest (F-PRP-NOT-IN-ACTIVE-MANIFEST).
     b. Read PRP YAML body from disk.
     c. Validate schema_version match (F-PRP-SCHEMA-VERSION-MISMATCH).
     d. Validate lifecycle truth + env match (F-PRP-LIFECYCLE-ENV-MISMATCH).
     e. Recompute canonical-JSON SHA-256 and compare (F-PRP-CONTENT-HASH-INVALID).
     f. Verify Ed25519 signature against the pinned prp-publisher pubkey
        (F-PRP-SIGNATURE-INVALID).
     g. Verify today ∈ [effective_date, expiry_date] (F-PRP-EXPIRED).
     h. Verify no forbidden CIC↔CLC coupling fields appear in the body and no
        private-org-data fields appear (F-PRP-COUPLING-VIOLATION).
  3. Build the active-PRP runtime registry and return it.

PRPs are categorically distinct from cards: they encode LIVE LAW bounded by
effective_date/expiry_date. The seven F-PRP-* fail-closed primitives below
mirror the F-CARDS-* family shape so that the Logician (§4) can compose them
into the same kind of preflight invariants used for cards.

v0.1 DRAFT NOTE: this loader is on disk so reviewers can see the intended
shape. The top-level call raises NotImplementedError. None of the inner gates
is wired into a production code path. Graduation to LIVE preflight happens at
v0.2 first wave at the same ceremony as cards v0.2 loader graduation, per
section_19_program_rule_packs.md.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal, Mapping, Optional


Environment = Literal["development", "production"]


# ---------------------------------------------------------------------------
# Fail-closed primitive exceptions — the F-PRP-* family.
#
# Names mirror the F-CARDS-* family in pipeline/cards/loader.py so that the
# Logician (§4) can compose them into the same kind of preflight invariants.
# v0.1 DRAFT: classes are defined and importable, but no body raises them at
# v0.1 since every gate function below short-circuits to NotImplementedError.
# ---------------------------------------------------------------------------


class PRPLoaderError(RuntimeError):
    """Base class for fail-closed PRP-loader preflight errors."""


class PRPNotInActiveManifestError(PRPLoaderError):
    """F-PRP-NOT-IN-ACTIVE-MANIFEST: PRP file on disk is not bound to a
    manifest entry in pipeline/program_rule_packs/_manifest/active_prps.yaml.

    Mirrors the cards 'active manifest binding' invariant: only PRPs explicitly
    listed in the signed active manifest are loadable. Unbound PRP YAMLs may
    exist on disk for review purposes but MUST NOT be runtime-loaded.
    """


class PRPSchemaVersionMismatchError(PRPLoaderError):
    """F-PRP-SCHEMA-VERSION-MISMATCH: PRP body declares a schema_version that
    does not match the schema_version this loader is pinned against.

    v0.1 DRAFT loader is pinned to '1.0-prp'. Any other value fails-closed.
    """


class PRPLifecycleEnvMismatchError(PRPLoaderError):
    """F-PRP-LIFECYCLE-ENV-MISMATCH: PRP lifecycle state is inconsistent with
    the loader environment.

    Examples of mismatches:
      - draft_status='draft' loaded into production (refused — draft PRPs
        never runtime-load).
      - runtime_loadable=true but draft_status != 'signed' (malformed truth).
      - runtime_loadable=true but signed_at/signed_by/content_hash absent.
      - runtime_loadable=false paired with runtime_load_status='loaded'.
    """


class PRPContentHashInvalidError(PRPLoaderError):
    """F-PRP-CONTENT-HASH-INVALID: PRP lifecycle.content_hash does not match
    the canonical-JSON SHA-256 of the PRP body (with signature/hash fields
    excluded, mirroring cards canonical_bytes())."""


class PRPSignatureInvalidError(PRPLoaderError):
    """F-PRP-SIGNATURE-INVALID: PRP Ed25519 signature does not verify against
    the pinned prp-publisher pubkey from
    vault_shared/program_rule_packs/publisher_pubkey.signed.yaml.

    Note: this is a SEPARATE pubkey from the cards publisher pubkey at
    vault_shared/cards/publisher_pubkey.signed.yaml. PRPs and cards live in
    different trust domains because PRPs encode live law (the operator may
    delegate PRP authorship to a regulatory-research role without delegating
    card authorship)."""


class PRPExpiredError(PRPLoaderError):
    """F-PRP-EXPIRED: today's date falls outside [effective_date, expiry_date].

    Sub-tags emitted at v0.2 first wave:
      - PRP-NOT-YET-EFFECTIVE: today < effective_date.
      - PRP-PAST-EXPIRY: expiry_date != null AND today > expiry_date.

    Live-law truth: a PRP that has expired is not law anymore; loading it
    into a runtime that drives Scribe drafting or Logician enforcement would
    apply rules that are no longer authoritative."""


class PRPCouplingViolationError(PRPLoaderError):
    """F-PRP-COUPLING-VIOLATION: PRP body contains forbidden CIC↔CLC coupling
    fields, OR private-organization-data fields (per Law 3: PRPs encode
    published live law only).

    Mirrors F-CARDS-COUPLING-VIOLATION-EXTENSION on the cards side. Forbidden
    fields registry lives in pipeline/logician/gates/f_prp_coupling_violation.py
    when that gate body is realized at v0.2 first wave."""


# ---------------------------------------------------------------------------
# Pinned schema version + manifest path constants.
# ---------------------------------------------------------------------------


PRP_SCHEMA_VERSION_PINNED: str = "1.0-prp"

PRP_MANIFEST_PATH: str = (
    "pipeline/program_rule_packs/_manifest/active_prps.yaml"
)

PRP_PUBLISHER_PUBKEY_PATH: str = (
    "vault_shared/program_rule_packs/publisher_pubkey.signed.yaml"
)


# ---------------------------------------------------------------------------
# Top-level entry point.
#
# v0.1 DRAFT: raises NotImplementedError so any seat that wires PRP loading
# before v0.2 first wave gets a clear refusal. The internal gate functions
# below also raise NotImplementedError; they are stubs whose shape is on disk
# only for reviewer inspection.
# ---------------------------------------------------------------------------


def load_active_prps(
    *,
    environment: Environment,
    today: Optional[str] = None,
    manifest_path: str = PRP_MANIFEST_PATH,
    publisher_pubkey_path: str = PRP_PUBLISHER_PUBKEY_PATH,
) -> dict[str, Any]:
    """Load + validate + register all active Program Rule Packs.

    v0.1 DRAFT: this entry point raises NotImplementedError. The bodies of
    every gate function it would call also raise NotImplementedError. PRP
    loading does not run in any v0.1 code path.

    Raises:
        NotImplementedError: always, at v0.1 DRAFT.
    """

    raise NotImplementedError(
        "PRP v0.2 first wave — schema + manifest + loader skeleton drafted "
        "but not active. Top-level load_active_prps() is intentionally a "
        "fail-closed stub at v0.1 DRAFT so that any seat which wires PRP "
        "enforcement before the v0.2 first wave graduation ceremony gets a "
        "clear refusal rather than silent dispatch. See "
        "pipeline/blueprint/v0.1/section_19_program_rule_packs.md."
    )


# ---------------------------------------------------------------------------
# Internal gate functions — F-PRP-* primitives.
#
# v0.1 DRAFT: all bodies raise NotImplementedError. Shape kept on disk so the
# Logician (§4) reviewer can see the intended primitive registry.
# ---------------------------------------------------------------------------


def read_prp_body(*, path: str) -> dict[str, Any]:
    """Read a YAML PRP body from disk and require a mapping root.

    v0.2 first wave: mirrors pipeline.cards.loader.read_card_body shape.
    """

    raise NotImplementedError("v0.2 first wave")


def read_active_manifest(*, manifest_path: str) -> dict[str, Any]:
    """Read pipeline/program_rule_packs/_manifest/active_prps.yaml.

    v0.2 first wave: returns the parsed manifest mapping. v0.1 stub.
    """

    raise NotImplementedError("v0.2 first wave")


def enforce_in_active_manifest(
    *,
    prp_path: str,
    prp_body: Mapping[str, Any],
    manifest: Mapping[str, Any],
) -> None:
    """F-PRP-NOT-IN-ACTIVE-MANIFEST gate body.

    v0.2 first wave: raises PRPNotInActiveManifestError if prp_body.prp_id is
    not present in manifest.active_prps.
    """

    raise NotImplementedError("v0.2 first wave")


def enforce_schema_version(
    *,
    prp_path: str,
    prp_body: Mapping[str, Any],
    pinned: str = PRP_SCHEMA_VERSION_PINNED,
) -> None:
    """F-PRP-SCHEMA-VERSION-MISMATCH gate body.

    v0.2 first wave: raises PRPSchemaVersionMismatchError if
    prp_body.schema_version != pinned.
    """

    raise NotImplementedError("v0.2 first wave")


def enforce_lifecycle_env(
    *,
    prp_path: str,
    prp_body: Mapping[str, Any],
    environment: Environment,
) -> None:
    """F-PRP-LIFECYCLE-ENV-MISMATCH gate body.

    v0.2 first wave: mirrors pipeline.cards.loader.enforce_lifecycle_truth.
    Refuses draft PRPs, refuses runtime_loadable=true without draft_status
    'signed', refuses runtime_loadable=false paired with runtime_load_status
    'loaded'. Adds environment-aware refusal: in 'production' environment,
    any PRP not at draft_status='signed' fails-closed.
    """

    raise NotImplementedError("v0.2 first wave")


def enforce_content_hash(
    *,
    prp_path: str,
    prp_body: Mapping[str, Any],
) -> None:
    """F-PRP-CONTENT-HASH-INVALID gate body.

    v0.2 first wave: recompute canonical-JSON SHA-256 of prp_body with
    lifecycle.content_hash, lifecycle.signature_status, and
    _research_metadata.ed25519_signature stripped, compare to
    prp_body.lifecycle.content_hash. Mirror of cards canonical_bytes_sha256.
    """

    raise NotImplementedError("v0.2 first wave")


def enforce_signature(
    *,
    prp_path: str,
    prp_body: Mapping[str, Any],
    publisher_pubkey_bytes: bytes,
) -> None:
    """F-PRP-SIGNATURE-INVALID gate body.

    v0.2 first wave: verify Ed25519 signature from
    prp_body._research_metadata.ed25519_signature against
    publisher_pubkey_bytes (resolved from
    vault_shared/program_rule_packs/publisher_pubkey.signed.yaml).
    """

    raise NotImplementedError("v0.2 first wave")


def enforce_effective_window(
    *,
    prp_path: str,
    prp_body: Mapping[str, Any],
    today: str,
) -> None:
    """F-PRP-EXPIRED gate body.

    v0.2 first wave: parse prp_body.effective_date and prp_body.expiry_date
    (ISO 8601), verify today falls within the window. expiry_date=None means
    the rule has no operator-known expiry. Emits sub-tags PRP-NOT-YET-EFFECTIVE
    or PRP-PAST-EXPIRY.
    """

    raise NotImplementedError("v0.2 first wave")


def enforce_no_forbidden_coupling(
    *,
    prp_path: str,
    prp_body: Mapping[str, Any],
) -> None:
    """F-PRP-COUPLING-VIOLATION gate body.

    v0.2 first wave: walk the PRP body and reject any forbidden CIC↔CLC
    coupling field (common_clc_patterns_observed, eligible_clc_subset,
    preferred_cics, etc.) AND any private-organization-data field
    (private_member_roster, private_org_underwriting_override, etc. per Law 3).
    Mirrors pipeline.cards.loader._find_forbidden_keys shape.
    """

    raise NotImplementedError("v0.2 first wave")


# ---------------------------------------------------------------------------
# F-PRP-* primitive registry — name list exported for the Logician (§4) +
# section_19_program_rule_packs.md cross-reference. Order matters: this is
# the order in which gates run inside load_active_prps() at v0.2 first wave.
# ---------------------------------------------------------------------------


F_PRP_PRIMITIVE_NAMES: tuple[str, ...] = (
    "F-PRP-NOT-IN-ACTIVE-MANIFEST",
    "F-PRP-SCHEMA-VERSION-MISMATCH",
    "F-PRP-LIFECYCLE-ENV-MISMATCH",
    "F-PRP-CONTENT-HASH-INVALID",
    "F-PRP-SIGNATURE-INVALID",
    "F-PRP-EXPIRED",
    "F-PRP-COUPLING-VIOLATION",
)
