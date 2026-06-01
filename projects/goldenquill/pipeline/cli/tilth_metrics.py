"""``tilth metrics`` — per-cycle cost telemetry CLI.

Sales-objection answer for the BYOK-bill question: "show me what this cycle
cost me." Joins three real on-disk sources to produce a per-cycle breakdown:

* ``tilth/logs/<org>/cache-ledger.jsonl`` — per-call BYOK telemetry written
  by ``tilth/bin/tilth-infer-cached.mjs``. After 2026-05-18 the writer
  stamps ``cycle_id``, ``seat``, ``card_id`` on each row; rows from before
  that change are treated as "unattributed" (see ``--include-unattributed``).
* ``pipeline/metrics/session_log.jsonl`` — Cowork-session metadata
  (per-session wall-time + turn count). Optional context; the join is
  "any session whose ``ts`` window overlaps the cycle's call timestamps."
* ``vault_shared/wpfa/coefficient_registry/active.yaml`` — SN-LLC-signed
  per-model coefficient table. When the registry is the unsigned scaffold
  (canonical v0.1 Beta-launch state — SN-LLC has not published the
  inaugural release yet), the CLI **degrades gracefully**: BYOK actual
  ``paid_usd`` from the ledger is the sales-grade number. Counterfactual
  and watt-hour columns are surfaced as "registry unsigned — N/A" rather
  than fabricated.

Subcommands
-----------
* ``cycle-cost <cycle_id>`` — per-cycle cost breakdown. ``--org`` is
  optional (scans all orgs when omitted). Output: text table (default),
  ``--json``, or ``--csv``.

Exit codes
----------
* 0 — success (zero matching rows is still success; an empty cycle is a
  valid result, but missing-cycle-id is a different error).
* 1 — no rows matched the requested cycle_id, or input file unreadable.
* 2 — argparse error (handled by argparse).

Why this is functional today
----------------------------
Per CLAUDE.md "Don't invent data plumbing" rule, this CLI only reports
what the on-disk artifacts actually contain. The Coefficient Registry's
canonical v0.1 Beta-launch state is "scaffold pending SN-LLC publish";
the CLI surfaces that state honestly rather than emitting fabricated
counterfactuals. When SN-LLC publishes the inaugural registry, the
"registry unsigned — N/A" columns automatically populate without code
changes (the schema is already wired through ``CoefficientRegistry``).
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable, Mapping, Optional, Sequence


# ---------------------------------------------------------------------------
# Paths — overridable via --repo-root so tests can synthesize fixtures.
# ---------------------------------------------------------------------------


DEFAULT_TILTH_LOGS_REL = Path("tilth/logs")
DEFAULT_SESSION_LOG_REL = Path("pipeline/metrics/session_log.jsonl")
DEFAULT_REGISTRY_REL = Path("vault_shared/wpfa/coefficient_registry/active.yaml")


_CYCLE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,128}$")


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LedgerRow:
    """One row of ``cache-ledger.jsonl``, normalized."""

    ts: str
    org: str
    workflow: str
    model: str
    elapsed_ms: int
    input_tokens: int
    output_tokens: int
    cache_read_input_tokens: int
    cache_creation_input_tokens: int
    paid_usd: float
    cached_savings_usd: float
    rates_fallback: bool
    cycle_id: Optional[str]
    seat: Optional[str]
    card_id: Optional[str]

    @classmethod
    def from_dict(cls, d: Mapping[str, object]) -> "LedgerRow":
        def _i(k: str, default: int = 0) -> int:
            v = d.get(k, default)
            return int(v) if v is not None else default

        def _f(k: str, default: float = 0.0) -> float:
            v = d.get(k, default)
            return float(v) if v is not None else default

        def _s(k: str, default: str = "") -> str:
            v = d.get(k, default)
            return str(v) if v is not None else default

        def _opt(k: str) -> Optional[str]:
            v = d.get(k)
            if v is None or v == "":
                return None
            return str(v)

        return cls(
            ts=_s("ts"),
            org=_s("org"),
            workflow=_s("workflow", "default"),
            model=_s("model"),
            elapsed_ms=_i("elapsed_ms"),
            input_tokens=_i("input_tokens"),
            output_tokens=_i("output_tokens"),
            cache_read_input_tokens=_i("cache_read_input_tokens"),
            cache_creation_input_tokens=_i("cache_creation_input_tokens"),
            paid_usd=_f("paid_usd"),
            cached_savings_usd=_f("cached_savings_usd"),
            rates_fallback=bool(d.get("rates_fallback", False)),
            cycle_id=_opt("cycle_id"),
            seat=_opt("seat"),
            card_id=_opt("card_id"),
        )


@dataclass
class Bucket:
    """Aggregate spend / tokens for a subset of ledger rows."""

    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_input_tokens: int = 0
    cache_creation_input_tokens: int = 0
    paid_usd: float = 0.0
    cached_savings_usd: float = 0.0

    def add(self, row: LedgerRow) -> None:
        self.calls += 1
        self.input_tokens += row.input_tokens
        self.output_tokens += row.output_tokens
        self.cache_read_input_tokens += row.cache_read_input_tokens
        self.cache_creation_input_tokens += row.cache_creation_input_tokens
        self.paid_usd = round(self.paid_usd + row.paid_usd, 6)
        self.cached_savings_usd = round(
            self.cached_savings_usd + row.cached_savings_usd, 6
        )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class CycleCost:
    """Top-level cycle-cost report."""

    cycle_id: str
    org_filter: Optional[str]
    orgs_seen: list[str]
    ts_start: Optional[str]
    ts_end: Optional[str]
    total: Bucket = field(default_factory=Bucket)
    per_seat: dict[str, Bucket] = field(default_factory=dict)
    per_card: dict[str, Bucket] = field(default_factory=dict)
    per_model: dict[str, Bucket] = field(default_factory=dict)
    posture: str = "unknown"
    registry_state: str = "unsigned-scaffold"
    registry_baseline_model: Optional[str] = None
    session_log_matches: int = 0

    @property
    def cache_hit_rate(self) -> float:
        """Cache-read tokens / (cache-read + uncached-input). 0.0 if no input."""
        denom = self.total.input_tokens + self.total.cache_read_input_tokens
        if denom == 0:
            return 0.0
        return round(self.total.cache_read_input_tokens / denom, 4)


# ---------------------------------------------------------------------------
# Readers
# ---------------------------------------------------------------------------


def _iter_jsonl(path: Path) -> Iterable[dict]:
    """Yield parsed JSON objects from a .jsonl file. Skips blank lines."""
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                # Skip malformed lines rather than aborting — partial ledger is
                # better than no ledger for a "show me the cost" sales answer.
                continue


def read_ledger_rows(
    *,
    repo_root: Path,
    org_filter: Optional[str] = None,
) -> Iterable[LedgerRow]:
    """Yield ledger rows from one org subdir or all org subdirs."""
    logs_root = repo_root / DEFAULT_TILTH_LOGS_REL
    if not logs_root.exists():
        return
    if org_filter is not None:
        target = logs_root / org_filter / "cache-ledger.jsonl"
        for d in _iter_jsonl(target):
            yield LedgerRow.from_dict(d)
        return
    for org_dir in sorted(p for p in logs_root.iterdir() if p.is_dir()):
        ledger = org_dir / "cache-ledger.jsonl"
        for d in _iter_jsonl(ledger):
            yield LedgerRow.from_dict(d)


def read_session_log(*, repo_root: Path) -> list[dict]:
    """Parse session_log.jsonl. Returns [] if missing."""
    path = repo_root / DEFAULT_SESSION_LOG_REL
    return list(_iter_jsonl(path))


def read_registry_state(*, repo_root: Path) -> tuple[str, Optional[str]]:
    """Return (state, baseline_model_id).

    State is one of:
      * ``"signed"`` — full SN-LLC signature present (signature is 128-char
        hex and ``schema_version`` is non-scaffold).
      * ``"unsigned-scaffold"`` — known scaffold / placeholder shape per the
        repo's seeded file. This is the canonical v0.1 Beta-launch state.
      * ``"missing"`` — registry file absent.

    Loading + verifying signatures lives in
    :func:`pipeline.vault.sub_kinds.coefficient_registry.load_active`. This
    CLI does a lightweight YAML-shape check only; the full crypto-verifying
    loader is invoked at WPFA emit time by ``tilth wpfa pdf emit``.
    """
    path = repo_root / DEFAULT_REGISTRY_REL
    if not path.exists():
        return "missing", None
    try:
        import yaml  # pyyaml is already a dep (see pyproject.toml)

        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    except Exception:  # noqa: BLE001 — degrade-gracefully on unreadable YAML
        return "missing", None

    schema_version = str(data.get("schema_version", ""))
    sig = str(data.get("sn_llc_signature_ed25519", ""))
    baseline = data.get("baseline_model_id")
    baseline_str = str(baseline) if baseline else None

    if not sig or "scaffold" in schema_version.lower():
        return "unsigned-scaffold", baseline_str
    if len(sig) == 128 and all(c in "0123456789abcdef" for c in sig.lower()):
        return "signed", baseline_str
    return "unsigned-scaffold", baseline_str


# ---------------------------------------------------------------------------
# Joiner
# ---------------------------------------------------------------------------


def build_cycle_cost(
    *,
    repo_root: Path,
    cycle_id: str,
    org_filter: Optional[str] = None,
    include_unattributed: bool = False,
    posture: str = "unknown",
) -> CycleCost:
    """Build a :class:`CycleCost` report by joining the three data sources."""

    if not _CYCLE_ID_RE.match(cycle_id):
        raise ValueError(
            f"cycle_id {cycle_id!r} must match ^[A-Za-z0-9_-]{{1,128}}$ "
            "(path-traversal defense; mirrors CycleReceipt grammar)"
        )

    rows = [
        r
        for r in read_ledger_rows(repo_root=repo_root, org_filter=org_filter)
        if r.cycle_id == cycle_id
        or (include_unattributed and r.cycle_id is None)
    ]

    registry_state, baseline_model = read_registry_state(repo_root=repo_root)

    report = CycleCost(
        cycle_id=cycle_id,
        org_filter=org_filter,
        orgs_seen=sorted({r.org for r in rows}),
        ts_start=min((r.ts for r in rows), default=None),
        ts_end=max((r.ts for r in rows), default=None),
        posture=posture,
        registry_state=registry_state,
        registry_baseline_model=baseline_model,
    )

    for r in rows:
        report.total.add(r)
        seat_key = r.seat or "unattributed"
        card_key = r.card_id or "unattributed"
        model_key = r.model or "unknown-model"
        report.per_seat.setdefault(seat_key, Bucket()).add(r)
        report.per_card.setdefault(card_key, Bucket()).add(r)
        report.per_model.setdefault(model_key, Bucket()).add(r)

    # Optional session-log join: count sessions whose date stamp matches the
    # cycle's ts window. Cheap context, not load-bearing for cost numbers.
    if report.ts_start and report.ts_end:
        start_date = report.ts_start[:10]
        end_date = report.ts_end[:10]
        for s in read_session_log(repo_root=repo_root):
            d = str(s.get("date", ""))[:10]
            if start_date <= d <= end_date:
                report.session_log_matches += 1

    return report


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------


def _fmt_usd(x: float) -> str:
    return f"${x:,.6f}"


def _fmt_int(x: int) -> str:
    return f"{x:,}"


def format_text(report: CycleCost) -> str:
    """Render a human-readable text table."""
    lines: list[str] = []
    lines.append(f"Cycle: {report.cycle_id}")
    lines.append(f"  org_filter        : {report.org_filter or '(all)'}")
    lines.append(f"  orgs_seen         : {', '.join(report.orgs_seen) or '(none)'}")
    lines.append(f"  ts_start          : {report.ts_start or '(none)'}")
    lines.append(f"  ts_end            : {report.ts_end or '(none)'}")
    lines.append(f"  posture           : {report.posture}")
    lines.append(f"  registry_state    : {report.registry_state}")
    lines.append(
        f"  baseline_model    : {report.registry_baseline_model or 'N/A'}"
    )
    lines.append(f"  session_log hits  : {report.session_log_matches}")
    lines.append("")

    t = report.total
    lines.append("TOTALS")
    lines.append(f"  calls              : {_fmt_int(t.calls)}")
    lines.append(f"  input_tokens       : {_fmt_int(t.input_tokens)}")
    lines.append(f"  output_tokens      : {_fmt_int(t.output_tokens)}")
    lines.append(f"  cache_read_tokens  : {_fmt_int(t.cache_read_input_tokens)}")
    lines.append(
        f"  cache_write_tokens : {_fmt_int(t.cache_creation_input_tokens)}"
    )
    lines.append(f"  cache_hit_rate     : {report.cache_hit_rate:.2%}")
    lines.append(f"  cached_savings_usd : {_fmt_usd(t.cached_savings_usd)}")
    lines.append(f"  paid_usd (BYOK)    : {_fmt_usd(t.paid_usd)}")
    lines.append("")

    if report.registry_state != "signed":
        lines.append(
            f"  counterfactual_usd : N/A "
            f"(coefficient registry state = {report.registry_state}; "
            "SN-LLC inaugural publish pending)"
        )
        lines.append(
            "  watt_hours         : N/A (same — counterfactual blocked)"
        )
        lines.append("")

    def _table(title: str, buckets: Mapping[str, Bucket]) -> None:
        if not buckets:
            return
        lines.append(title)
        width = max((len(k) for k in buckets), default=10)
        header = f"  {'key':<{width}}  {'calls':>6}  {'in_tok':>10}  {'out_tok':>10}  {'paid_usd':>14}"
        lines.append(header)
        lines.append("  " + "-" * (len(header) - 2))
        for key in sorted(buckets):
            b = buckets[key]
            lines.append(
                f"  {key:<{width}}  {b.calls:>6}  "
                f"{_fmt_int(b.input_tokens):>10}  "
                f"{_fmt_int(b.output_tokens):>10}  "
                f"{_fmt_usd(b.paid_usd):>14}"
            )
        lines.append("")

    _table("PER SEAT", report.per_seat)
    _table("PER CARD", report.per_card)
    _table("PER MODEL", report.per_model)

    coefficient_citations = (
        f"coefficient registry: vault_shared/wpfa/coefficient_registry/active.yaml "
        f"(state={report.registry_state})"
    )
    lines.append(coefficient_citations)

    return "\n".join(lines) + "\n"


def format_json(report: CycleCost) -> str:
    payload = {
        "cycle_id": report.cycle_id,
        "org_filter": report.org_filter,
        "orgs_seen": report.orgs_seen,
        "ts_start": report.ts_start,
        "ts_end": report.ts_end,
        "posture": report.posture,
        "registry_state": report.registry_state,
        "registry_baseline_model": report.registry_baseline_model,
        "session_log_matches": report.session_log_matches,
        "total": report.total.to_dict(),
        "cache_hit_rate": report.cache_hit_rate,
        "per_seat": {k: v.to_dict() for k, v in report.per_seat.items()},
        "per_card": {k: v.to_dict() for k, v in report.per_card.items()},
        "per_model": {k: v.to_dict() for k, v in report.per_model.items()},
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def format_csv(report: CycleCost) -> str:
    """Long-form CSV: one row per (scope, key) tuple."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(
        [
            "cycle_id",
            "scope",
            "key",
            "calls",
            "input_tokens",
            "output_tokens",
            "cache_read_input_tokens",
            "cache_creation_input_tokens",
            "paid_usd",
            "cached_savings_usd",
        ]
    )

    def _emit(scope: str, key: str, b: Bucket) -> None:
        writer.writerow(
            [
                report.cycle_id,
                scope,
                key,
                b.calls,
                b.input_tokens,
                b.output_tokens,
                b.cache_read_input_tokens,
                b.cache_creation_input_tokens,
                f"{b.paid_usd:.6f}",
                f"{b.cached_savings_usd:.6f}",
            ]
        )

    _emit("total", "ALL", report.total)
    for key in sorted(report.per_seat):
        _emit("seat", key, report.per_seat[key])
    for key in sorted(report.per_card):
        _emit("card", key, report.per_card[key])
    for key in sorted(report.per_model):
        _emit("model", key, report.per_model[key])

    return buf.getvalue()


# ---------------------------------------------------------------------------
# Argparse + entry point
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tilth metrics",
        description=(
            "Per-cycle cost telemetry. Joins cache-ledger + session_log + "
            "Coefficient Registry. Degrades gracefully when the registry "
            "is the unsigned scaffold (canonical v0.1 Beta-launch state)."
        ),
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)

    cc = sub.add_parser(
        "cycle-cost",
        help="Per-cycle cost breakdown.",
        description=(
            "Aggregate spend / tokens for a single cycle_id, broken out by "
            "seat, card, and model. Output: text (default), --json, or --csv."
        ),
    )
    cc.add_argument("cycle_id", help="Cycle id (^[A-Za-z0-9_-]{1,128}$).")
    cc.add_argument(
        "--org",
        default=None,
        help="Restrict to one org slug. Default: scan all orgs.",
    )
    cc.add_argument(
        "--include-unattributed",
        action="store_true",
        help=(
            "Also include ledger rows with no cycle_id stamp (legacy rows "
            "from before the writer learned --cycle-id). Off by default."
        ),
    )
    cc.add_argument(
        "--posture",
        default="unknown",
        choices=[
            "unknown",
            "frontier-eligible",
            "split-context-hybrid",
            "local-only-sovereign",
        ],
        help="Routing posture label to stamp on the report.",
    )
    fmt = cc.add_mutually_exclusive_group()
    fmt.add_argument("--json", action="store_true", help="JSON output.")
    fmt.add_argument("--csv", action="store_true", help="CSV output.")
    cc.add_argument(
        "--repo-root",
        default=None,
        help="Repo root (for tests). Default: walk up from CWD looking for "
        "pyproject.toml.",
    )
    return parser


def _resolve_repo_root(override: Optional[str]) -> Path:
    if override is not None:
        return Path(override).resolve()
    cwd = Path.cwd().resolve()
    for parent in (cwd, *cwd.parents):
        if (parent / "pyproject.toml").exists():
            return parent
    return cwd


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.subcommand != "cycle-cost":
        parser.error(f"unknown subcommand: {args.subcommand!r}")
        return 2  # unreachable

    try:
        repo_root = _resolve_repo_root(args.repo_root)
        report = build_cycle_cost(
            repo_root=repo_root,
            cycle_id=args.cycle_id,
            org_filter=args.org,
            include_unattributed=args.include_unattributed,
            posture=args.posture,
        )
    except ValueError as exc:
        print(f"tilth metrics cycle-cost: {exc}", file=sys.stderr)
        return 1

    if report.total.calls == 0:
        print(
            f"tilth metrics cycle-cost: no ledger rows matched "
            f"cycle_id={args.cycle_id!r}"
            + (f" org={args.org!r}" if args.org else "")
            + (
                " (try --include-unattributed for legacy rows without a "
                "cycle_id stamp)"
                if not args.include_unattributed
                else ""
            ),
            file=sys.stderr,
        )
        return 1

    if args.json:
        sys.stdout.write(format_json(report))
    elif args.csv:
        sys.stdout.write(format_csv(report))
    else:
        sys.stdout.write(format_text(report))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
