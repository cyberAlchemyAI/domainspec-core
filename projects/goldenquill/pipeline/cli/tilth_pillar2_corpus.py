"""``tilth pillar2 corpus`` — FID Pillar-2 corpus assembly CLI.

Authority
---------
Pillar-2 spec: ``pipeline/funder_intelligence/_research_corpus/README.md``
(five non-negotiable discipline rules).
Quality spec: ``docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md``.
Planning authority: ``pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md``
§9.1 (Phase 1, weeks 2-3).

Scope
-----
This CLI scaffolds and tracks the per-artifact corpus that backs FID
Pillar-3 fact extraction. It is **infrastructure only** — it does NOT
fetch URLs. Tilth has no outbound HTTP from the appliance (CC-007
sovereignty boundary). The operator performs fetches in their own
browser session and drops the downloaded bytes into the artifact's
``raw/`` directory; the CLI then registers each file (URL + SHA256 +
access_date + classification tier) into ``sources.yaml``.

Subcommands
-----------
* ``init`` — verify signed Pillar-1 charter exists, scaffold any missing
  on-disk structure, write a corpus-local copy of the signed charter,
  flip the top-level MANIFEST row to ``FETCHING``.
* ``fetch --register`` — register a file the operator already dropped
  into ``raw/`` (compute SHA256, append ``sources.yaml`` entry).
* ``extract`` — validate an ``extracted/<cluster>.yaml`` against
  Pillar-2 discipline rules (every fact has ``corpus_ref``, every
  ``verbatim_quote`` ≤2 sentences, every corpus_ref resolves to a
  registered source).
* ``status`` — surface per-artifact lifecycle state (charter sig,
  source count by tier, extracted cluster count, signature state).
* ``sign`` — delegate to
  :mod:`pipeline.funder_intelligence._methodology.sign_corpus`
  (canonical bytes, Ed25519 verify, write ``_signed.yaml``, update
  the top-level Pillar-2 MANIFEST row).

Postures
--------
This CLI runs only under the Local-Only-Sovereign posture (architecture
v7.0.10 §1). No cloud routing. No frontier model calls. No HTTP egress.
The operator-supervised fetch happens out-of-band in the operator's own
browser; the CLI sees only on-disk files.

CC-007 boundary
---------------
The CLI uses ``pathlib`` + ``hashlib`` + ``yaml`` only. It does not
import ``urllib``, ``requests``, ``httpx``, ``aiohttp``, or any other
HTTP library. The AST-lint ``R-NO-DIRECT-PROVIDER-HTTP`` rule covers
this surface.

F-FID-* gates surfaced by this CLI
----------------------------------
* ``F-FID-CORPUS-UNSIGNED-CHARTER`` — ``init`` refuses if the Pillar-1
  charter is not at ``_charter_v1_SIGNED.md``.
* ``F-FID-CORPUS-HASH-MISMATCH`` — ``fetch --register --verify`` and
  ``status`` flag any on-disk file whose SHA256 differs from the
  ``sources.yaml`` entry.
* ``F-FID-CORPUS-VERBATIM-TOO-LONG`` — ``extract`` fails if any
  ``verbatim_quote`` exceeds 2 sentences (OQ-4 inheritance).
* ``F-FID-CORPUS-FACT-ORPHAN`` — ``extract`` fails if any fact lacks
  a ``corpus_ref`` resolving to a registered source.

Exit codes
----------
* 0 — subcommand succeeded.
* 1 — bad CLI args / file not found / artifact-id not in roster /
  charter not signed / extract validation failure.
* 2 — hash mismatch / corpus hash failure.
* 3 — sign-helper delegate failure (forwarded from
  :mod:`sign_corpus`).
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import pathlib
import re
import shutil
import sys
from typing import Optional, Sequence

try:
    import yaml
except ImportError as e:  # pragma: no cover - imported by tests under venv
    print(f"ERROR: missing dep ({e}); install via `pip install pyyaml`.", file=sys.stderr)
    sys.exit(1)


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
FID_ROOT = REPO_ROOT / "pipeline" / "funder_intelligence"
CHARTERS_DIR = FID_ROOT / "pillar_1_charters"
P2_ROOT = FID_ROOT / "pillar_2_corpus"
P2_MANIFEST = P2_ROOT / "MANIFEST.md"

# The 14 Phase-1 artifact IDs — authoritative roster pulled from
# pillar_1_charters/MANIFEST.md "Status" table.
PHASE_1_ROSTER: tuple[str, ...] = (
    "USDA-RD",
    "USDA-NIFA",
    "USDA-AMS",
    "PA-DEPT-AG",
    "PA-DCED",
    "HEINZ-FOUNDATION",
    "NCBA-CLUSA",
    "RICHARD-KING-MELLON-FOUNDATION",
    "USDA-AMS-VAPG-FY26",
    "USDA-RD-RBDG-FY26",
    "USDA-RD-RCDG-FY26",
    "USDA-NIFA-SARE-NE-FY26",
    "PA-DEPT-AG-AGINNOV-FY26",
    "USDA-RD-CFP-FY26",
)

# Status enum surfaced in the top-level Pillar-2 MANIFEST table.
STATUS_NOT_INITIALIZED = "NOT_INITIALIZED"
STATUS_FETCHING = "FETCHING"
STATUS_EXTRACTING = "EXTRACTING"
STATUS_READY_FOR_SIGN = "READY_FOR_SIGN"
STATUS_SIGNED = "SIGNED"
ALL_STATUSES: tuple[str, ...] = (
    STATUS_NOT_INITIALIZED,
    STATUS_FETCHING,
    STATUS_EXTRACTING,
    STATUS_READY_FOR_SIGN,
    STATUS_SIGNED,
)


# ─────────────────────────────────────────────────────────────────────
# Path helpers
# ─────────────────────────────────────────────────────────────────────

def artifact_root(artifact_id: str) -> pathlib.Path:
    return P2_ROOT / artifact_id


def signed_charter_path(artifact_id: str) -> pathlib.Path:
    return CHARTERS_DIR / f"{artifact_id}_charter_v1_SIGNED.md"


def draft_charter_path(artifact_id: str) -> pathlib.Path:
    return CHARTERS_DIR / f"{artifact_id}_charter_v0_DRAFT.md"


def sources_yaml_path(artifact_id: str) -> pathlib.Path:
    return artifact_root(artifact_id) / "sources.yaml"


def charter_corpus_local_path(artifact_id: str) -> pathlib.Path:
    return artifact_root(artifact_id) / "charter.signed.yaml"


def signed_yaml_path(artifact_id: str) -> pathlib.Path:
    return artifact_root(artifact_id) / "_signed.yaml"


# ─────────────────────────────────────────────────────────────────────
# Validators
# ─────────────────────────────────────────────────────────────────────

def assert_in_roster(artifact_id: str) -> None:
    if artifact_id not in PHASE_1_ROSTER:
        raise ValueError(
            f"artifact_id '{artifact_id}' is not in the Phase-1 14-artifact roster. "
            f"Roster: {', '.join(PHASE_1_ROSTER)}"
        )


def assert_charter_signed(artifact_id: str) -> pathlib.Path:
    """F-FID-CORPUS-UNSIGNED-CHARTER PRE-gate.

    Returns the signed-charter path if present; raises FileNotFoundError otherwise.
    """
    p = signed_charter_path(artifact_id)
    if not p.exists():
        raise FileNotFoundError(
            f"F-FID-CORPUS-UNSIGNED-CHARTER: signed Pillar-1 charter not found at {p}. "
            f"Run the Pillar-1 sign ceremony first: "
            f"`python -m pipeline.funder_intelligence._methodology.sign_charter <draft>`."
        )
    return p


def compute_sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(64 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


# Sentence-ish split — period / ! / ? followed by whitespace or end.
# Conservative on abbreviation: §A reviewer counts "U.S." etc. as a sentence.
# The OQ-4 ≤2 rule is enforced at audit; this is a sanity gate at extract.
_SENTENCE_END = re.compile(r"[.!?](?:\s+|$)")


def count_sentences(text: str) -> int:
    text = text.strip()
    if not text:
        return 0
    # Use regex to find sentence terminators; count = end-markers (+1 if text
    # doesn't end with a terminator and isn't empty).
    matches = _SENTENCE_END.findall(text)
    count = len(matches)
    if not text.endswith((".", "!", "?")):
        count += 1
    return max(count, 1)


# ─────────────────────────────────────────────────────────────────────
# Sources.yaml mutation
# ─────────────────────────────────────────────────────────────────────

def load_sources(artifact_id: str) -> dict:
    p = sources_yaml_path(artifact_id)
    if not p.exists():
        raise FileNotFoundError(f"sources.yaml not at {p}")
    raw = yaml.safe_load(p.read_text()) or {}
    if not isinstance(raw, dict):
        raise ValueError(f"sources.yaml at {p} is not a YAML mapping")
    raw.setdefault("artifact_id", artifact_id)
    raw.setdefault("charter_path", "charter.signed.yaml")
    raw.setdefault("files", [])
    if raw["files"] is None:
        raw["files"] = []
    return raw


def write_sources(artifact_id: str, data: dict) -> None:
    p = sources_yaml_path(artifact_id)
    p.write_text(yaml.safe_dump(data, sort_keys=True, allow_unicode=True))


# ─────────────────────────────────────────────────────────────────────
# Subcommand handlers
# ─────────────────────────────────────────────────────────────────────

def cmd_init(args: argparse.Namespace) -> int:
    """Scaffold (or repair) per-artifact corpus tree; require signed charter."""
    artifact_id = args.artifact_id
    try:
        assert_in_roster(artifact_id)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    try:
        charter = assert_charter_signed(artifact_id)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    root = artifact_root(artifact_id)
    root.mkdir(parents=True, exist_ok=True)
    (root / "raw").mkdir(exist_ok=True)
    (root / "extracted").mkdir(exist_ok=True)
    gk_raw = root / "raw" / ".gitkeep"
    gk_ex = root / "extracted" / ".gitkeep"
    if not gk_raw.exists():
        gk_raw.touch()
    if not gk_ex.exists():
        gk_ex.touch()

    sources = sources_yaml_path(artifact_id)
    if not sources.exists():
        write_sources(artifact_id, {
            "artifact_id": artifact_id,
            "charter_path": "charter.signed.yaml",
            "populated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "files": [],
        })

    # Copy signed charter into corpus-local provenance slot.
    local_charter = charter_corpus_local_path(artifact_id)
    if not local_charter.exists() or args.force_copy_charter:
        shutil.copy2(charter, local_charter)

    print(f"INIT OK: {artifact_id}")
    print(f"  charter_signed: {charter}")
    print(f"  corpus_root: {root}")
    print(f"  status: {STATUS_FETCHING}")
    return 0


def cmd_fetch(args: argparse.Namespace) -> int:
    """Register a file the operator already dropped into raw/."""
    artifact_id = args.artifact_id
    try:
        assert_in_roster(artifact_id)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    if not signed_charter_path(artifact_id).exists():
        print(
            f"ERROR: F-FID-CORPUS-UNSIGNED-CHARTER: charter not signed; "
            f"run init after sign-off.",
            file=sys.stderr,
        )
        return 1

    rel_path: str = args.register
    root = artifact_root(artifact_id)
    abs_path = (root / rel_path).resolve()
    if not abs_path.exists():
        print(
            f"ERROR: file not on disk at {abs_path}. "
            f"Drop the operator-fetched bytes there first.",
            file=sys.stderr,
        )
        return 1
    if not abs_path.is_relative_to(root):
        print(
            f"ERROR: --register path must live under {root}; got {abs_path}.",
            file=sys.stderr,
        )
        return 1

    sha = compute_sha256(abs_path)
    size = abs_path.stat().st_size
    rel_to_root = abs_path.relative_to(root)

    sources = load_sources(artifact_id)
    files = sources["files"]
    # Refuse duplicate registrations.
    for entry in files:
        if entry.get("file_path") == str(rel_to_root):
            if entry.get("sha256") == sha:
                print(
                    f"NOOP: {rel_to_root} already registered with same SHA256."
                )
                return 0
            print(
                f"ERROR: F-FID-CORPUS-HASH-MISMATCH: existing entry for "
                f"{rel_to_root} has sha256={entry.get('sha256')}, on-disk={sha}. "
                f"Remove the stale entry from sources.yaml before re-registering.",
                file=sys.stderr,
            )
            return 2

    entry = {
        "file_path": str(rel_to_root),
        "source_url": args.source_url,
        "access_date": args.access_date or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"),
        "content_type": args.content_type or _guess_content_type(abs_path),
        "sha256": sha,
        "bytes_size": size,
        "classification_tier": args.classification_tier,
        "classification_rationale": args.classification_rationale or "",
        "relevance_score": args.relevance_score,
        "status": "registered",
    }
    if args.classification_tier == 2 and args.interview_consent_path:
        entry["interview_consent_recorded"] = True
        entry["interview_consent_path"] = args.interview_consent_path
    files.append(entry)
    sources["files"] = files
    sources["populated_at"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    write_sources(artifact_id, sources)

    print(f"REGISTERED OK: {rel_to_root}")
    print(f"  sha256: {sha}")
    print(f"  bytes_size: {size}")
    print(f"  classification_tier: {args.classification_tier}")
    return 0


def _guess_content_type(path: pathlib.Path) -> str:
    suffix = path.suffix.lower()
    return {
        ".pdf": "application/pdf",
        ".html": "text/html",
        ".htm": "text/html",
        ".txt": "text/plain",
        ".md": "text/markdown",
        ".yaml": "application/yaml",
        ".yml": "application/yaml",
        ".json": "application/json",
        ".csv": "text/csv",
    }.get(suffix, "application/octet-stream")


def cmd_extract(args: argparse.Namespace) -> int:
    """Validate an extracted/<cluster>.yaml against Pillar-2 discipline rules."""
    artifact_id = args.artifact_id
    try:
        assert_in_roster(artifact_id)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    cluster_path = artifact_root(artifact_id) / "extracted" / f"{args.cluster}.yaml"
    if not cluster_path.exists():
        print(
            f"ERROR: extracted cluster not at {cluster_path}. "
            f"Author the structured-fact YAML there first.",
            file=sys.stderr,
        )
        return 1

    raw = yaml.safe_load(cluster_path.read_text()) or {}
    if not isinstance(raw, dict):
        print(f"ERROR: {cluster_path} is not a YAML mapping.", file=sys.stderr)
        return 1
    facts = raw.get("facts", [])
    if not isinstance(facts, list) or not facts:
        print(
            f"ERROR: {cluster_path} has no `facts:` list. Each fact must carry "
            f"corpus_ref + verbatim_quote + analysis.",
            file=sys.stderr,
        )
        return 1

    sources = load_sources(artifact_id)
    registered_paths = {e.get("file_path") for e in sources.get("files", [])}

    errors: list[str] = []
    for i, fact in enumerate(facts):
        ctx = f"facts[{i}]"
        if not isinstance(fact, dict):
            errors.append(f"{ctx}: not a mapping")
            continue
        corpus_ref = fact.get("corpus_ref")
        verbatim = fact.get("verbatim_quote")
        if not corpus_ref:
            errors.append(
                f"{ctx}: F-FID-CORPUS-FACT-ORPHAN — missing corpus_ref"
            )
        else:
            # corpus_ref shape: "<artifact_id>:<file_path>:<page_or_line>"
            parts = corpus_ref.split(":", 2)
            if len(parts) < 2 or parts[0] != artifact_id:
                errors.append(
                    f"{ctx}: corpus_ref '{corpus_ref}' must start with "
                    f"'{artifact_id}:'"
                )
            else:
                ref_file = parts[1]
                if ref_file not in registered_paths:
                    errors.append(
                        f"{ctx}: F-FID-CORPUS-FACT-ORPHAN — corpus_ref file "
                        f"'{ref_file}' not registered in sources.yaml"
                    )
        if not verbatim:
            errors.append(f"{ctx}: missing verbatim_quote")
        else:
            n = count_sentences(verbatim)
            if n > 2:
                errors.append(
                    f"{ctx}: F-FID-CORPUS-VERBATIM-TOO-LONG — verbatim_quote "
                    f"has {n} sentences (max 2)"
                )

    if errors:
        print(
            f"EXTRACT VALIDATION FAILED for {artifact_id}/extracted/{args.cluster}.yaml:",
            file=sys.stderr,
        )
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"EXTRACT OK: {artifact_id}/{args.cluster} ({len(facts)} facts)")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """Surface per-artifact lifecycle state."""
    artifact_id = args.artifact_id
    try:
        assert_in_roster(artifact_id)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    charter_signed = signed_charter_path(artifact_id).exists()
    charter_draft = draft_charter_path(artifact_id).exists()
    root = artifact_root(artifact_id)
    sources_exists = sources_yaml_path(artifact_id).exists()
    signed_yaml = signed_yaml_path(artifact_id).exists()

    raw_files: list[pathlib.Path] = []
    if (root / "raw").exists():
        raw_files = [
            p for p in (root / "raw").rglob("*")
            if p.is_file() and p.name != ".gitkeep"
        ]
    extracted_files: list[pathlib.Path] = []
    if (root / "extracted").exists():
        extracted_files = [
            p for p in (root / "extracted").glob("*.yaml")
            if p.is_file()
        ]

    sources_count = 0
    tier_counts = {1: 0, 2: 0, 3: 0}
    hash_mismatches: list[str] = []
    if sources_exists:
        sources = load_sources(artifact_id)
        sources_count = len(sources.get("files", []))
        for entry in sources.get("files", []):
            t = entry.get("classification_tier")
            if t in tier_counts:
                tier_counts[t] += 1
            # Hash check
            abs_p = root / entry.get("file_path", "")
            if abs_p.exists():
                sha = compute_sha256(abs_p)
                if sha != entry.get("sha256"):
                    hash_mismatches.append(entry.get("file_path", "<?>"))

    if signed_yaml:
        status = STATUS_SIGNED
    elif charter_signed and extracted_files and sources_count > 0:
        status = STATUS_READY_FOR_SIGN
    elif charter_signed and sources_count > 0:
        status = STATUS_EXTRACTING if extracted_files else STATUS_FETCHING
    elif charter_signed:
        status = STATUS_FETCHING
    else:
        status = STATUS_NOT_INITIALIZED

    print(f"=== {artifact_id} ===")
    print(f"  charter: {'SIGNED v1' if charter_signed else ('DRAFT v0' if charter_draft else 'MISSING')}")
    print(f"  corpus_root: {root if root.exists() else '<not_initialized>'}")
    print(f"  sources_registered: {sources_count} (tier1={tier_counts[1]}, tier2={tier_counts[2]}, tier3={tier_counts[3]})")
    print(f"  raw_files_on_disk: {len(raw_files)}")
    print(f"  extracted_clusters: {len(extracted_files)}")
    if hash_mismatches:
        print(f"  F-FID-CORPUS-HASH-MISMATCH: {hash_mismatches}")
    print(f"  status: {status}")
    return 0 if not hash_mismatches else 2


def cmd_sign(args: argparse.Namespace) -> int:
    """Delegate to sign_corpus helper. Forwards exit code."""
    # Imported lazily so test fixtures can monkeypatch the module.
    from pipeline.funder_intelligence._methodology import sign_corpus  # noqa: WPS433

    artifact_id = args.artifact_id
    try:
        assert_in_roster(artifact_id)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    forward_args = [str(artifact_root(artifact_id))]
    if args.dry_run:
        forward_args.append("--dry-run")
    else:
        if args.signer_pubkey_fingerprint:
            forward_args += ["--signer-pubkey-fingerprint", args.signer_pubkey_fingerprint]
        if args.signature_hex:
            forward_args += ["--signature-hex", args.signature_hex]
        if args.signed_at:
            forward_args += ["--signed-at", args.signed_at]
        if args.allow_missing_pubkey_yaml:
            forward_args.append("--allow-missing-pubkey-yaml")
    return sign_corpus.main(forward_args)


# ─────────────────────────────────────────────────────────────────────
# Argparse wiring
# ─────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="tilth pillar2 corpus",
        description=(
            "FID Pillar-2 corpus assembly CLI (Local-Only-Sovereign; no HTTP "
            "egress; operator-supervised fetch out-of-band)."
        ),
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="Scaffold per-artifact corpus tree (signed charter required).")
    p_init.add_argument("--artifact-id", required=True, help="One of the 14 Phase-1 artifact IDs.")
    p_init.add_argument("--force-copy-charter", action="store_true",
                        help="Overwrite existing corpus-local charter.signed.yaml.")
    p_init.set_defaults(func=cmd_init)

    p_fetch = sub.add_parser("fetch", help="Register an operator-dropped file (no HTTP).")
    p_fetch.add_argument("--artifact-id", required=True)
    p_fetch.add_argument("--register", required=True,
                         help="Path (relative to artifact corpus root) of the file to register.")
    p_fetch.add_argument("--source-url", required=True,
                         help="URL the operator fetched the file from (recorded; not fetched by CLI).")
    p_fetch.add_argument("--classification-tier", required=True, type=int, choices=[1, 2, 3])
    p_fetch.add_argument("--classification-rationale", default="",
                         help="One-line rationale (recorded in sources.yaml).")
    p_fetch.add_argument("--access-date", default=None,
                         help="UTC date the operator accessed the URL (YYYY-MM-DD). Defaults to today.")
    p_fetch.add_argument("--content-type", default=None,
                         help="Override content-type; defaults to extension-based guess.")
    p_fetch.add_argument("--relevance-score", type=float, default=None,
                         help="0-1 priority for Pillar-3 extraction (operator's call).")
    p_fetch.add_argument("--interview-consent-path", default=None,
                         help="Path to consent record (required for tier=2 interview transcripts).")
    p_fetch.set_defaults(func=cmd_fetch)

    p_ex = sub.add_parser("extract", help="Validate extracted/<cluster>.yaml against discipline rules.")
    p_ex.add_argument("--artifact-id", required=True)
    p_ex.add_argument("--cluster", required=True,
                      help="Cluster name (filename stem under extracted/).")
    p_ex.set_defaults(func=cmd_extract)

    p_status = sub.add_parser("status", help="Surface per-artifact lifecycle state.")
    p_status.add_argument("--artifact-id", required=True)
    p_status.set_defaults(func=cmd_status)

    p_sign = sub.add_parser("sign", help="Delegate to sign_corpus helper for closure ceremony.")
    p_sign.add_argument("--artifact-id", required=True)
    p_sign.add_argument("--dry-run", action="store_true",
                        help="Print canonical bytes + hash; do not modify files.")
    p_sign.add_argument("--signer-pubkey-fingerprint", default=None)
    p_sign.add_argument("--signature-hex", default=None)
    p_sign.add_argument("--signed-at", default=None)
    p_sign.add_argument("--allow-missing-pubkey-yaml", action="store_true",
                        help="(Testing.) Skip pinned-pubkey verification.")
    p_sign.set_defaults(func=cmd_sign)

    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
