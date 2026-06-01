"""``tilth memory <verb>`` — operator-facing memory CLI.

Sibling of :mod:`pipeline.cli.tilth_memory_query` (separate; not landed in
this dispatch). The two CLIs share the ``tilth memory`` namespace defined
by the v0.1 Beta dispatch plan (`pipeline/planning/architecture_proficiency
_assessment_result_2026-05-11.md` Tier-0 items 2 + 3).

Verbs
-----
* ``tilth memory consolidate-index`` — promote bottom-half oldest MEMORY.md
  entries to a date-stamped archive index when the file exceeds the
  configurable soft threshold (default 20480 B; under the observed Cowork
  auto-memory loader hard cap of ~24.4 KB).

Usage
-----
::

    # Default: target the auto-memory dir derived from --memory-dir; threshold
    # 20 KB; consolidation_date = today UTC.
    python -m pipeline.cli.tilth_memory consolidate-index \\
        --memory-dir /path/to/memory

    # Custom threshold + dry-run.
    python -m pipeline.cli.tilth_memory consolidate-index \\
        --memory-dir /path/to/memory \\
        --threshold-bytes 18432 \\
        --dry-run \\
        --json-output

Exit codes
----------
* 0 — consolidation completed (fired) OR threshold not crossed (no-op).
* 1 — input error: MEMORY.md missing / fewer than 2 entries / malformed.
* 2 — CLI argument error (handled by argparse).

What this CLI is NOT
--------------------
* Not ``tilth memory query`` — unified retrieval CLI (Tier-0 item 2 of
  the assessment roadmap; separate dispatch).
* Not a LOCK-class amendment — pure operational utility. Each consolidation
  appends a ``lock_class=memory_consolidation`` row to lock_history for
  audit-trail discipline; no LOCK ceremony.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Sequence

from pipeline.memory.auto_consolidate_trigger import (
    DEFAULT_BYTE_THRESHOLD as TRIGGER_DEFAULT_BYTE_THRESHOLD,
    DEFAULT_LINE_THRESHOLD as TRIGGER_DEFAULT_LINE_THRESHOLD,
    EXIT_ERROR as TRIGGER_EXIT_ERROR,
    EXIT_TRIGGER_FIRED,
    EXIT_UNDER_THRESHOLD,
    MemoryTriggerError,
    run_auto_trigger,
)
from pipeline.memory.consolidate_index import (
    DEFAULT_THRESHOLD_BYTES,
    HARD_LOAD_LIMIT_BYTES,
    MemoryConsolidationError,
    run_consolidation,
)


# ---------------------------------------------------------------------------
# argparse
# ---------------------------------------------------------------------------


def _build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tilth_memory",
        description=(
            "Operator-facing memory CLI. Currently exposes "
            "consolidate-index; tilth memory query lands in a separate "
            "dispatch."
        ),
    )
    subparsers = parser.add_subparsers(
        dest="verb",
        required=True,
        title="verbs",
    )
    consolidate = subparsers.add_parser(
        "consolidate-index",
        help="Promote bottom-half oldest MEMORY.md entries to an archive.",
        description=(
            "Walks MEMORY.md; when its UTF-8 byte size exceeds the "
            "configurable soft threshold, promotes the bottom-half "
            "oldest entries to a date-stamped archive index in the same "
            "directory and prepends MEMORY.md with a pointer line. "
            "Hash-pins each consolidation to lock_history.v1.jsonl as a "
            "lock_class=memory_consolidation row when reachable."
        ),
    )
    consolidate.add_argument(
        "--memory-dir",
        dest="memory_dir",
        type=Path,
        required=True,
        help=(
            "Directory containing MEMORY.md. The archive file is written "
            "as a sibling inside this directory."
        ),
    )
    consolidate.add_argument(
        "--threshold-bytes",
        dest="threshold_bytes",
        type=int,
        default=DEFAULT_THRESHOLD_BYTES,
        help=(
            f"Soft threshold (UTF-8 bytes). Default {DEFAULT_THRESHOLD_BYTES}. "
            f"Must be <= {HARD_LOAD_LIMIT_BYTES} (Cowork auto-memory "
            "loader hard cap)."
        ),
    )
    consolidate.add_argument(
        "--consolidation-date",
        dest="consolidation_date",
        default=None,
        help=(
            "Override the YYYY-MM-DD stamp used in the archive filename "
            "and metadata. Defaults to today's UTC date."
        ),
    )
    consolidate.add_argument(
        "--repo-root",
        dest="repo_root",
        type=Path,
        default=Path.cwd(),
        help=(
            "Workspace root used to locate "
            "pipeline/engineering/lock_history.v1.jsonl when "
            "--lock-history-path is omitted. Defaults to CWD."
        ),
    )
    consolidate.add_argument(
        "--lock-history-path",
        dest="lock_history_path",
        type=Path,
        default=None,
        help=(
            "Explicit path to lock_history.v1.jsonl. When omitted, "
            "derived from --repo-root; skipped silently if not found."
        ),
    )
    consolidate.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help=(
            "Do not write any files. Report the consolidation that "
            "would happen."
        ),
    )
    consolidate.add_argument(
        "--json-output",
        dest="json_output",
        action="store_true",
        help="Emit a machine-readable JSON summary on stdout.",
    )

    # ------------------------------------------------------------------
    # Verb: auto-trigger
    # ------------------------------------------------------------------
    auto_trigger = subparsers.add_parser(
        "auto-trigger",
        help=(
            "Preflight check: signal a consolidation trigger when "
            "MEMORY.md exceeds the early-warning threshold."
        ),
        description=(
            "Reads MEMORY.md and compares against an early-warning "
            "threshold (default 200 lines / 12288 bytes). Sits BELOW "
            "the consolidate-index engine's own 20 KiB threshold so it "
            "nudges the operator before actual consolidation is "
            "needed. Defaults can be overridden via env vars "
            "MEMORY_TRIGGER_LINES / MEMORY_TRIGGER_BYTES / MEMORY_PATH "
            "/ MEMORY_TRIGGER_LOG, or via the CLI flags below. Logs "
            "every fired trigger to a JSONL audit trail. With --run, "
            "invokes consolidate-index directly when the trigger fires."
        ),
    )
    auto_trigger.add_argument(
        "--memory-path",
        dest="memory_path",
        type=Path,
        default=None,
        help=(
            "Explicit path to MEMORY.md. Defaults to $MEMORY_PATH or "
            "./MEMORY.md."
        ),
    )
    auto_trigger.add_argument(
        "--threshold-lines",
        dest="threshold_lines",
        type=int,
        default=None,
        help=(
            f"Early-warning line threshold. Default "
            f"{TRIGGER_DEFAULT_LINE_THRESHOLD} (or $MEMORY_TRIGGER_LINES)."
        ),
    )
    auto_trigger.add_argument(
        "--threshold-bytes",
        dest="threshold_bytes_trigger",
        type=int,
        default=None,
        help=(
            f"Early-warning byte threshold. Default "
            f"{TRIGGER_DEFAULT_BYTE_THRESHOLD} (or $MEMORY_TRIGGER_BYTES)."
        ),
    )
    auto_trigger.add_argument(
        "--run",
        dest="do_consolidate",
        action="store_true",
        help=(
            "Invoke consolidate-index directly when the trigger fires "
            "(unattended mode). Without this flag the CLI only signals."
        ),
    )
    auto_trigger.add_argument(
        "--log-clean",
        dest="log_clean",
        action="store_true",
        help=(
            "Also append an under_threshold record when MEMORY.md is "
            "below threshold. Default: log only fired events."
        ),
    )
    auto_trigger.add_argument(
        "--log-path",
        dest="log_path",
        type=Path,
        default=None,
        help=(
            "Explicit path to the JSONL trigger log. Defaults to "
            "$MEMORY_TRIGGER_LOG or "
            "./pipeline/institutional_memory/memory_consolidation_log.jsonl."
        ),
    )
    auto_trigger.add_argument(
        "--repo-root",
        dest="repo_root_auto",
        type=Path,
        default=None,
        help=(
            "Workspace root passed through to consolidate-index when "
            "--run is set. Defaults to CWD."
        ),
    )
    auto_trigger.add_argument(
        "--json-output",
        dest="json_output_auto",
        action="store_true",
        help="Emit a machine-readable JSON summary on stdout.",
    )
    auto_trigger.add_argument(
        "--quiet",
        dest="quiet",
        action="store_true",
        help="Suppress human-readable stderr output (only exit code).",
    )

    return parser


# ---------------------------------------------------------------------------
# Verb: consolidate-index
# ---------------------------------------------------------------------------


def _verb_consolidate_index(args: argparse.Namespace) -> int:
    try:
        outcome = run_consolidation(
            memory_dir=args.memory_dir.resolve(),
            threshold_bytes=args.threshold_bytes,
            consolidation_date=args.consolidation_date,
            lock_history_path=(
                args.lock_history_path.resolve()
                if args.lock_history_path is not None
                else None
            ),
            dry_run=args.dry_run,
            repo_root=(
                args.repo_root.resolve()
                if args.repo_root is not None
                else None
            ),
        )
    except MemoryConsolidationError as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 1

    result = outcome.result
    summary: dict = {
        "ok": True,
        "fired": result.fired,
        "dry_run": args.dry_run,
        "memory_path": str(outcome.memory_path),
        "archive_path": (
            str(outcome.archive_path)
            if outcome.archive_path is not None
            else None
        ),
        "threshold_bytes": result.threshold_bytes,
        "original_size_bytes": result.original_size_bytes,
        "new_size_bytes": result.new_size_bytes,
        "entries_kept": result.entries_kept,
        "entries_archived": result.entries_archived,
        "source_memory_sha3_512": result.source_memory_sha3_512,
        "new_memory_sha3_512": result.new_memory_sha3_512,
        "archive_sha3_512": result.archive_sha3_512,
        "lock_history_row_appended": outcome.lock_history_row_appended,
        "lock_history_path": (
            str(outcome.lock_history_path)
            if outcome.lock_history_path is not None
            else None
        ),
    }

    if args.json_output:
        sys.stdout.write(json.dumps(summary, ensure_ascii=False) + "\n")
    else:
        if result.fired:
            verb = "WOULD CONSOLIDATE (dry-run)" if args.dry_run else "CONSOLIDATED"
            sys.stderr.write(
                f"{verb}: {outcome.memory_path}\n"
                f"  original_size_bytes: {result.original_size_bytes}\n"
                f"  new_size_bytes:      {result.new_size_bytes}\n"
                f"  threshold_bytes:     {result.threshold_bytes}\n"
                f"  entries_kept:        {result.entries_kept}\n"
                f"  entries_archived:    {result.entries_archived}\n"
                f"  archive_path:        {outcome.archive_path}\n"
                f"  source_sha3_512:     {result.source_memory_sha3_512[:16]}…\n"
                f"  new_sha3_512:        {result.new_memory_sha3_512[:16]}…\n"
                f"  archive_sha3_512:    {result.archive_sha3_512[:16]}…\n"
                f"  lock_history_row:    {outcome.lock_history_row_appended}\n"
            )
        else:
            sys.stderr.write(
                f"NO-OP (under threshold): {outcome.memory_path}\n"
                f"  size_bytes:      {result.original_size_bytes}\n"
                f"  threshold_bytes: {result.threshold_bytes}\n"
            )
    return 0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Verb: auto-trigger
# ---------------------------------------------------------------------------


def _verb_auto_trigger(args: argparse.Namespace) -> int:
    try:
        result = run_auto_trigger(
            memory_path=(
                args.memory_path.resolve()
                if args.memory_path is not None
                else None
            ),
            line_threshold=args.threshold_lines,
            byte_threshold=args.threshold_bytes_trigger,
            do_consolidate=args.do_consolidate,
            log_clean=args.log_clean,
            log_path=(
                args.log_path.resolve()
                if args.log_path is not None
                else None
            ),
            repo_root=(
                args.repo_root_auto.resolve()
                if args.repo_root_auto is not None
                else None
            ),
        )
    except (MemoryTriggerError, MemoryConsolidationError) as exc:
        sys.stderr.write(f"error: {exc}\n")
        return TRIGGER_EXIT_ERROR

    outcome = result.outcome
    summary: dict = {
        "ok": True,
        "fired": outcome.fired,
        "action": result.action,
        "memory_path": str(outcome.memory_path),
        "size_bytes": outcome.size_bytes,
        "line_count": outcome.line_count,
        "byte_threshold": outcome.byte_threshold,
        "line_threshold": outcome.line_threshold,
        "reason": outcome.reason,
        "log_path": (
            str(result.log_path) if result.log_path is not None else None
        ),
        "consolidation": result.consolidation_summary,
    }

    if args.json_output_auto:
        sys.stdout.write(json.dumps(summary, ensure_ascii=False) + "\n")
    elif not args.quiet:
        if outcome.fired:
            ran = " AND RAN consolidate-index" if args.do_consolidate else ""
            sys.stderr.write(
                f"MEMORY.md auto-trigger FIRED{ran}: "
                f"{outcome.memory_path}\n"
                f"  size_bytes:     {outcome.size_bytes} "
                f"(threshold {outcome.byte_threshold})\n"
                f"  line_count:     {outcome.line_count} "
                f"(threshold {outcome.line_threshold})\n"
                f"  reason:         {outcome.reason}\n"
                f"  next action:    "
                + (
                    "consolidation executed; see log\n"
                    if args.do_consolidate
                    else "invoke the consolidate-memory skill, or run "
                    "`python -m pipeline.cli.tilth_memory consolidate-index "
                    f"--memory-dir {outcome.memory_path.parent}`\n"
                )
                + f"  log_path:       {result.log_path}\n"
            )
        else:
            sys.stderr.write(
                f"MEMORY.md auto-trigger: under threshold "
                f"({outcome.size_bytes} B / {outcome.line_count} lines "
                f"≤ {outcome.byte_threshold} B / "
                f"{outcome.line_threshold} lines)\n"
            )

    return EXIT_TRIGGER_FIRED if outcome.fired else EXIT_UNDER_THRESHOLD


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


VERB_DISPATCH = {
    "consolidate-index": _verb_consolidate_index,
    "auto-trigger": _verb_auto_trigger,
}


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _build_argparser()
    args = parser.parse_args(argv)
    handler = VERB_DISPATCH.get(args.verb)
    if handler is None:
        parser.error(f"unknown verb: {args.verb!r}")
        return 2
    return handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
