"""``tilth memory query`` — unified read-only retrieval CLI.

Sibling of :mod:`pipeline.cli.tilth_memory` (the namespace-parent CLI
that owns ``consolidate-index``). Both CLIs live under the ``tilth
memory`` namespace per the architecture proficiency assessment
2026-05-11 Tier-0 items 2 + 3.

Subcommands
-----------
* ``query <query> [--org <slug>] [--register <name>...] [--source <kind>]
  [--limit N | --top N] [--format text|json] [--posture local-only]``
  — natural-language BM25 query across the 15 memory registers. Returns
  ranked results with provenance.
* ``list-registers`` — table of the 15 registers with row counts +
  last-modified timestamps.
* ``inspect <register> [--org <slug>] [--limit N]`` — dump per-register
  surface (one entry per line; first line = provenance, second = text
  excerpt). Useful for "what's actually in the lessons.json file."

CLI ergonomics
--------------
The 2026-05-18 ``tilth memory query`` ship adds three operator
ergonomic flags plus a deployment-shape flag:

* ``--source lessons|lock_history|cards|docs|all`` — simplified
  source vocabulary that maps to the canonical register names
  (``lessons`` → ``lessons_json``; ``lock_history`` → ``lock_history``;
  ``cards`` → ``cards``; ``docs`` → ``docs``; ``all`` → no filter).
  Mutually exclusive with ``--register``.
* ``--top N`` — alias for ``--limit N``. Mutually exclusive.
* ``--format text|json`` — alias for the legacy ``--json-output``
  flag. ``text`` (default) = human; ``json`` = machine-readable.
* ``--posture local-only`` — explicit deployment-shape declaration.
  Default and only currently-accepted value is ``local-only``
  (deployment shape C, Local-Only-Sovereign). The flag is accepted
  for forward-compat with posture-aware routing; ``a`` /
  ``frontier-eligible`` / ``b`` / ``split-context-hybrid`` are
  rejected today with an instructional error pointing at the
  classification-review pipeline as the prerequisite. No external
  HTTP egress occurs in this CLI under any value of ``--posture``.

Law-3 isolation
---------------
Per-org registers (``kfr``, ``classification_register``,
``reflection_packets``, ``match_database``) require ``--org <slug>``.
Workspace registers are accessible without ``--org``. Cross-org reads
are blocked by the underlying :func:`Registry.query` / ``inspect``
methods raising :class:`Law3Violation`.

Exit codes
----------
* 0 — completed successfully (zero results is still success).
* 1 — input error: unknown register / Law-3 violation / empty query.
* 2 — CLI argument error (handled by argparse).

What this CLI is NOT
--------------------
* Not a writer. The only memory writer is
  ``tilth memory consolidate-index``.
* Not a LOCK-class amendment. Pure operational utility.
* Not a vector retrieval surface. v0.1 substrate is sparse BM25 only.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Sequence

from pipeline.memory.unified_query import (
    ALL_REGISTERS,
    DEFAULT_QUERY_LIMIT,
    Law3Violation,
    PER_ORG_REGISTERS,
    Registry,
    UnifiedQueryError,
    UnknownRegisterError,
    make_registry,
)


# ---------------------------------------------------------------------------
# Source-vocabulary alias map + posture vocabulary
# ---------------------------------------------------------------------------

# Simplified --source vocabulary → canonical register names. ``all``
# means "no register filter; let the registry decide based on --org".
SOURCE_ALIAS_MAP: dict[str, Optional[tuple[str, ...]]] = {
    "lessons": ("lessons_json",),
    "lock_history": ("lock_history",),
    "cards": ("cards",),
    "docs": ("docs",),
    "all": None,
}

# Accepted --posture values. Only Local-Only-Sovereign is wired today;
# the other two postures are rejected at CLI boundary with a
# pointer-to-classification-review error. The flag exists today as a
# forward-compat hook so callers (CI, downstream Tilth seats) can
# always pass the deployment shape explicitly.
POSTURE_LOCAL_ONLY = "local-only"
POSTURE_PUBLIC_FRONTIER = "frontier-eligible"
POSTURE_SPLIT_CONTEXT = "split-context-hybrid"
ACCEPTED_POSTURE_VALUES: tuple[str, ...] = (
    POSTURE_LOCAL_ONLY,
    POSTURE_PUBLIC_FRONTIER,
    POSTURE_SPLIT_CONTEXT,
)
SUPPORTED_POSTURE_VALUES: tuple[str, ...] = (POSTURE_LOCAL_ONLY,)


class PostureNotSupportedError(UnifiedQueryError):
    """Raised when ``--posture`` is set to a value the CLI does not
    currently support. The CLI accepts ``local-only`` today; the other
    two declared values are rejected at the boundary so downstream
    callers cannot accidentally believe they have been routed through
    posture-aware logic that is not wired.
    """


# ---------------------------------------------------------------------------
# argparse
# ---------------------------------------------------------------------------


def _build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tilth_memory_query",
        description=(
            "Unified read-only retrieval over the 13 memory registers. "
            "BM25-class ranking with provenance preserved. Law-3 "
            "isolated per-org via --org."
        ),
    )
    parser.add_argument(
        "--repo-root",
        dest="repo_root",
        type=Path,
        default=Path.cwd(),
        help="Workspace root. Defaults to CWD.",
    )
    parser.add_argument(
        "--json-output",
        dest="json_output",
        action="store_true",
        help=(
            "Emit machine-readable JSON on stdout instead of human "
            "text. Legacy spelling. Prefer ``--format json``."
        ),
    )
    parser.add_argument(
        "--format",
        dest="format",
        choices=("text", "json"),
        default=None,
        help=(
            "Output format. ``text`` (default) = human-readable; "
            "``json`` = machine-readable JSON. Alias for "
            "``--json-output`` (which remains supported)."
        ),
    )
    parser.add_argument(
        "--posture",
        dest="posture",
        choices=ACCEPTED_POSTURE_VALUES,
        default=POSTURE_LOCAL_ONLY,
        help=(
            "Deployment shape. ``local-only`` (default and currently "
            "the only supported value) is shape C — all retrieval on "
            "device, no frontier HTTP egress. The other declared "
            "values are accepted at the parser boundary for forward "
            "compatibility and rejected at runtime until posture-aware "
            "routing is wired."
        ),
    )
    subparsers = parser.add_subparsers(
        dest="verb", required=True, title="subcommands"
    )

    # query
    q = subparsers.add_parser(
        "query",
        help="Natural-language BM25 query across registers.",
        description=(
            "Tokenize the query string, score every document in every "
            "in-scope register via BM25 Okapi, return the top --limit "
            "results sorted by score descending."
        ),
    )
    q.add_argument(
        "query",
        type=str,
        help="Natural-language query string.",
    )
    q.add_argument(
        "--org",
        dest="org",
        type=str,
        default=None,
        help=(
            "Org slug — required to include per-org registers (KFR, "
            "classification register, reflection packets, match "
            "database). Omitting --org restricts the query to "
            "workspace-shared registers."
        ),
    )
    q.add_argument(
        "--register",
        dest="registers",
        action="append",
        default=None,
        help=(
            "Restrict to a specific register (repeatable). Default: "
            "all in-scope registers. Valid names: " + ", ".join(ALL_REGISTERS)
        ),
    )
    q.add_argument(
        "--limit",
        dest="limit",
        type=int,
        default=None,
        help=(
            f"Max results. Default {DEFAULT_QUERY_LIMIT}. "
            "Mutually exclusive with ``--top``."
        ),
    )
    q.add_argument(
        "--top",
        dest="top",
        type=int,
        default=None,
        help=(
            "Alias for ``--limit``. Mutually exclusive with "
            "``--limit``."
        ),
    )
    q.add_argument(
        "--source",
        dest="source",
        choices=tuple(SOURCE_ALIAS_MAP.keys()),
        default=None,
        help=(
            "Simplified source filter. ``lessons`` → ``lessons_json``; "
            "``lock_history`` → ``lock_history``; ``cards`` → "
            "``cards``; ``docs`` → ``docs``; ``all`` → no filter. "
            "Mutually exclusive with ``--register``."
        ),
    )

    # list-registers
    subparsers.add_parser(
        "list-registers",
        help="List the 13 memory registers with row counts and mtimes.",
        description=(
            "Probe each register, count documents, report last-modified. "
            "Per-org registers show count=0 / exists=False when --org "
            "is omitted; supply --org to populate them."
        ),
    ).add_argument(
        "--org",
        dest="org",
        type=str,
        default=None,
        help="Org slug for per-org register probing. Optional.",
    )

    # inspect
    insp = subparsers.add_parser(
        "inspect",
        help="Dump all documents from a single register.",
        description=(
            "Emit every document the named register exposes. Per-org "
            "registers require --org. --limit truncates the dump."
        ),
    )
    insp.add_argument(
        "register",
        type=str,
        choices=ALL_REGISTERS,
        help="Register name. One of: " + ", ".join(ALL_REGISTERS),
    )
    insp.add_argument(
        "--org",
        dest="org",
        type=str,
        default=None,
        help="Org slug — required for per-org registers.",
    )
    insp.add_argument(
        "--limit",
        dest="limit",
        type=int,
        default=None,
        help="Truncate the dump to N entries. Default: no limit.",
    )

    return parser


# ---------------------------------------------------------------------------
# Verb: query
# ---------------------------------------------------------------------------


def _verb_query(args: argparse.Namespace, registry: Registry) -> int:
    # --top / --limit reconciliation: at most one may be set; absent
    # both, fall back to the registry default.
    if args.limit is not None and args.top is not None:
        sys.stderr.write(
            "error: --limit and --top are mutually exclusive\n"
        )
        return 1
    resolved_limit = (
        args.limit
        if args.limit is not None
        else (args.top if args.top is not None else DEFAULT_QUERY_LIMIT)
    )

    # --source / --register reconciliation. The simplified --source
    # vocabulary maps to a closed set of canonical register names.
    # Mixing both at once would silently drop one; reject the mix.
    if args.source is not None and args.registers:
        sys.stderr.write(
            "error: --source and --register are mutually exclusive\n"
        )
        return 1
    if args.source is not None:
        resolved_registers = SOURCE_ALIAS_MAP[args.source]
        registers_arg = (
            list(resolved_registers) if resolved_registers is not None else None
        )
    else:
        registers_arg = args.registers

    try:
        results = registry.query(
            query=args.query,
            repo_root=args.repo_root.resolve(),
            org=args.org,
            registers=registers_arg,
            limit=resolved_limit,
        )
    except (UnifiedQueryError, Law3Violation) as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 1

    if _emit_json(args):
        payload = {
            "ok": True,
            "verb": "query",
            "query": args.query,
            "org": args.org,
            "registers": registers_arg,
            "source": args.source,
            "limit": resolved_limit,
            "posture": args.posture,
            "results": [
                {
                    "score": r.score,
                    "register": r.register,
                    "locator": r.provenance.locator,
                    "source_path": r.provenance.source_path,
                    "org": r.provenance.org,
                    "snippet": r.snippet,
                }
                for r in results
            ],
            "result_count": len(results),
        }
        sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
        return 0

    if not results:
        sys.stderr.write("no results\n")
        return 0
    for r in results:
        org_tag = f"[{r.provenance.org}] " if r.provenance.org else ""
        sys.stdout.write(
            f"{r.score:7.3f}  {r.register:25s}  "
            f"{org_tag}{r.provenance.source_path}:{r.provenance.locator}\n"
        )
        sys.stdout.write(f"          {r.snippet}\n\n")
    return 0


# ---------------------------------------------------------------------------
# Verb: list-registers
# ---------------------------------------------------------------------------


def _verb_list_registers(args: argparse.Namespace, registry: Registry) -> int:
    try:
        infos = registry.list_registers(
            repo_root=args.repo_root.resolve(), org=args.org
        )
    except (UnifiedQueryError, Law3Violation) as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 1

    if _emit_json(args):
        payload = {
            "ok": True,
            "verb": "list-registers",
            "org": args.org,
            "registers": [
                {
                    "name": i.name,
                    "scope": i.scope,
                    "source_path_pattern": i.source_path_pattern,
                    "document_count": i.document_count,
                    "last_modified_iso": i.last_modified_iso,
                    "exists": i.exists,
                }
                for i in infos
            ],
        }
        sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
        return 0

    sys.stdout.write(
        f"{'name':25s}  {'scope':10s}  {'exists':6s}  {'count':>6s}  "
        f"{'last_modified':25s}  source\n"
    )
    sys.stdout.write("-" * 110 + "\n")
    for i in infos:
        sys.stdout.write(
            f"{i.name:25s}  {i.scope:10s}  {str(i.exists):6s}  "
            f"{i.document_count:6d}  "
            f"{(i.last_modified_iso or '-'):25s}  {i.source_path_pattern}\n"
        )
    return 0


# ---------------------------------------------------------------------------
# Verb: inspect
# ---------------------------------------------------------------------------


def _verb_inspect(args: argparse.Namespace, registry: Registry) -> int:
    try:
        docs = registry.inspect(
            register=args.register,
            repo_root=args.repo_root.resolve(),
            org=args.org,
        )
    except (UnknownRegisterError, Law3Violation, UnifiedQueryError) as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 1

    if args.limit is not None and args.limit >= 0:
        docs = docs[: args.limit]

    if _emit_json(args):
        payload = {
            "ok": True,
            "verb": "inspect",
            "register": args.register,
            "org": args.org,
            "limit": args.limit,
            "documents": [
                {
                    "locator": d.provenance.locator,
                    "source_path": d.provenance.source_path,
                    "org": d.provenance.org,
                    "text": d.text,
                }
                for d in docs
            ],
            "document_count": len(docs),
        }
        sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
        return 0

    if not docs:
        sys.stderr.write(f"{args.register}: no documents\n")
        return 0
    for d in docs:
        org_tag = f"[{d.provenance.org}] " if d.provenance.org else ""
        sys.stdout.write(
            f"{org_tag}{d.provenance.source_path}:{d.provenance.locator}\n"
        )
        excerpt = d.text if len(d.text) <= 300 else d.text[:300] + "…"
        sys.stdout.write(f"  {excerpt}\n\n")
    return 0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


VERB_DISPATCH = {
    "query": _verb_query,
    "list-registers": _verb_list_registers,
    "inspect": _verb_inspect,
}


def _emit_json(args: argparse.Namespace) -> bool:
    """Return True if the operator asked for JSON output (either via
    the legacy ``--json-output`` flag or the newer ``--format json``).
    Format wins when both are present; never errors.
    """

    fmt = getattr(args, "format", None)
    if fmt == "json":
        return True
    if fmt == "text":
        return False
    return bool(getattr(args, "json_output", False))


def _enforce_posture(args: argparse.Namespace) -> None:
    """Raise :class:`PostureNotSupportedError` if the operator asked
    for a posture the CLI does not currently honor. Local-Only-Sovereign
    is the only wired posture in this build.
    """

    posture = getattr(args, "posture", POSTURE_LOCAL_ONLY)
    if posture in SUPPORTED_POSTURE_VALUES:
        return
    raise PostureNotSupportedError(
        f"--posture {posture!r} is not currently supported by this "
        f"CLI. Only {SUPPORTED_POSTURE_VALUES[0]!r} (deployment shape "
        "C, Local-Only-Sovereign) is wired today. Posture-aware "
        "routing (Frontier-Eligible and Split-Context-Hybrid) lands "
        "with the classification-review pipeline; until then this CLI "
        "refuses to silently fall through to an unintended shape."
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _build_argparser()
    args = parser.parse_args(argv)
    try:
        _enforce_posture(args)
    except PostureNotSupportedError as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 1
    handler = VERB_DISPATCH.get(args.verb)
    if handler is None:
        parser.error(f"unknown verb: {args.verb!r}")
        return 2
    registry = make_registry()
    return handler(args, registry)


if __name__ == "__main__":
    raise SystemExit(main())
