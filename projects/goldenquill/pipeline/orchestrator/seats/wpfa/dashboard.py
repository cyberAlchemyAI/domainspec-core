"""WPFA operator dashboard — Cowork HTML artifact. [§17.8]

Per-org + per-quarter rollups. Pure read; reads from disk-state only,
never invokes external APIs, never writes back.

Three rollup tiers per §17.8.3:
  1. Per-org rollup (v0.1).
  2. Per-quarter rollup (v0.1) — workspace-aggregate discipline.
  3. Per-fleet rollup (Stage-2+) — data-free static text placeholder
     (RT-11 fold-in). NEVER renders SKU counts or aggregate facts.

The HTML artifact is consumed by Cowork's `mcp__visualize__show_widget`
or any equivalent widget surface. This module produces:
  - DashboardData: structured rollup data (used by tests + JSON output).
  - render_dashboard_html(): the Cowork-renderable HTML string.
"""

from __future__ import annotations

import html as _html
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final, Mapping

from pipeline.orchestrator.seats.wpfa._cedar_bootstrap import (
    CycleReceiptCedarDenied,
    CycleReceiptReadPrincipal,
    CycleReceiptResource,
    evaluate_cycle_receipt_read_isolation,
)
from pipeline.vault.sub_kinds.cycle_receipts import (
    CycleReceipt,
    from_canonical_bytes,
)


PER_FLEET_PLACEHOLDER_TEXT: Final[str] = (
    "Per-fleet rollup is a Stage-2+ deployment milestone. This view will "
    "populate when 12 Tilths are deployed and the Sovereign Node commons "
    "cooperative is online. v0.1 ships per-org and per-quarter rollups only."
)


# ---------------------------------------------------------------------------
# Rollup data shapes
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class PerOrgRollupRow:
    cycle_id: str
    emitted_at: str
    is_buyer_attested: bool
    actual_dollars_minor_units: int
    counterfactual_dollars_minor_units: int
    delta_dollars_minor_units: int
    actual_watt_hours_micro: int
    counterfactual_watt_hours_micro: int
    delta_watt_hours_micro: int


@dataclass(frozen=True, kw_only=True)
class PerOrgRollup:
    org_slug: str
    receipts: tuple[PerOrgRollupRow, ...]
    cumulative_dollars_saved_minor_units: int
    cumulative_watt_hours_saved_micro: int


@dataclass(frozen=True, kw_only=True)
class PerQuarterRollup:
    quarter: str
    per_org: Mapping[str, PerOrgRollup]
    total_dollars_saved_minor_units: int
    total_watt_hours_saved_micro: int


@dataclass(frozen=True, kw_only=True)
class DashboardData:
    per_org_rollups: Mapping[str, PerOrgRollup]
    per_quarter_rollups: Mapping[str, PerQuarterRollup]
    per_fleet_placeholder: str = field(default=PER_FLEET_PLACEHOLDER_TEXT)


# ---------------------------------------------------------------------------
# Disk-walk helpers
# ---------------------------------------------------------------------------


def _read_receipts_for_org(
    *,
    repo_root: Path,
    org_slug: str,
) -> tuple[CycleReceipt, ...]:
    subtree = (
        repo_root / "orgs" / org_slug / "vault" / "operational" / "cycle_receipts"
    )
    if not subtree.is_dir():
        return ()
    out: list[CycleReceipt] = []
    for entry in sorted(subtree.glob("*.json")):
        try:
            receipt = from_canonical_bytes(entry.read_bytes())
        except Exception:  # noqa: BLE001 — skip malformed; dashboard is read-only
            continue
        out.append(receipt)
    return tuple(out)


def _discover_org_slugs(repo_root: Path) -> tuple[str, ...]:
    orgs_dir = repo_root / "orgs"
    if not orgs_dir.is_dir():
        return ()
    return tuple(
        sorted(
            p.name
            for p in orgs_dir.iterdir()
            if p.is_dir() and not p.name.startswith("_") and not p.name.startswith(".")
        )
    )


def _per_org_rollup_for(
    receipts: tuple[CycleReceipt, ...],
    *,
    org_slug: str,
) -> PerOrgRollup:
    rows = tuple(
        PerOrgRollupRow(
            cycle_id=r.cycle_id,
            emitted_at=r.emitted_at,
            is_buyer_attested=r.is_buyer_attested,
            actual_dollars_minor_units=r.actual.dollars_total_minor_units,
            counterfactual_dollars_minor_units=(
                r.counterfactual.dollars_total_minor_units
            ),
            delta_dollars_minor_units=r.delta.dollars_saved_minor_units,
            actual_watt_hours_micro=r.actual.watt_hours_total_micro,
            counterfactual_watt_hours_micro=(
                r.counterfactual.watt_hours_total_micro
            ),
            delta_watt_hours_micro=r.delta.watt_hours_saved_micro,
        )
        for r in sorted(receipts, key=lambda r: r.emitted_at)
    )
    return PerOrgRollup(
        org_slug=org_slug,
        receipts=rows,
        cumulative_dollars_saved_minor_units=sum(
            row.delta_dollars_minor_units for row in rows
        ),
        cumulative_watt_hours_saved_micro=sum(
            row.delta_watt_hours_micro for row in rows
        ),
    )


# ---------------------------------------------------------------------------
# Build dashboard data
# ---------------------------------------------------------------------------


def build_dashboard_data(
    *,
    repo_root: Path,
    workspace_aggregate_principal_session_id: str = "operator",
) -> DashboardData:
    """Walk every org subtree and produce per-org + per-quarter rollups.

    Each org READ is gated by ``evaluate_cycle_receipt_read_isolation``
    with the workspace_aggregate principal — the Stage-1 operator-as-
    multi-org-actor carve-out per §15.2 + §17.9 #3. Per-org content does
    not leak across orgs; only aggregate statistics cross the boundary.
    """
    repo_root = Path(repo_root)
    principal = CycleReceiptReadPrincipal(
        session_id=workspace_aggregate_principal_session_id,
        principal_kind="workspace_aggregate",
    )
    per_org: dict[str, PerOrgRollup] = {}
    quarter_buckets: dict[str, dict[str, list[CycleReceipt]]] = {}
    for org_slug in _discover_org_slugs(repo_root):
        receipts = _read_receipts_for_org(
            repo_root=repo_root, org_slug=org_slug
        )
        if not receipts:
            continue
        # Cedar gate (defense-in-depth on disk walk).
        for r in receipts:
            try:
                evaluate_cycle_receipt_read_isolation(
                    principal,
                    CycleReceiptResource(
                        org_slug_hint=r.org_slug,
                        cycle_id=r.cycle_id,
                        is_buyer_attested=r.is_buyer_attested,
                    ),
                )
            except CycleReceiptCedarDenied:
                # Workspace-aggregate principal should never trip this; if
                # it does, skip the receipt and move on (fail-closed read).
                continue
        per_org[org_slug] = _per_org_rollup_for(receipts, org_slug=org_slug)
        for r in receipts:
            quarter_buckets.setdefault(r.baseline_quarter, {}).setdefault(
                org_slug, []
            ).append(r)

    per_quarter: dict[str, PerQuarterRollup] = {}
    for q, by_org in sorted(quarter_buckets.items()):
        per_org_q: dict[str, PerOrgRollup] = {}
        total_d = 0
        total_e = 0
        for org_slug, rs in sorted(by_org.items()):
            rollup = _per_org_rollup_for(tuple(rs), org_slug=org_slug)
            per_org_q[org_slug] = rollup
            total_d += rollup.cumulative_dollars_saved_minor_units
            total_e += rollup.cumulative_watt_hours_saved_micro
        per_quarter[q] = PerQuarterRollup(
            quarter=q,
            per_org=per_org_q,
            total_dollars_saved_minor_units=total_d,
            total_watt_hours_saved_micro=total_e,
        )
    return DashboardData(
        per_org_rollups=per_org,
        per_quarter_rollups=per_quarter,
    )


# ---------------------------------------------------------------------------
# HTML render
# ---------------------------------------------------------------------------


def _money(minor_units: int) -> str:
    return f"${minor_units / 100:.2f}"


def _kwh(micro_wh: int) -> str:
    return f"{micro_wh / 1_000_000_000:.3f} kWh"


def render_dashboard_html(data: DashboardData) -> str:
    """Render a self-contained HTML widget for Cowork.

    No external CSS / JS; transparent background; minimal styling so the
    widget inherits Cowork's CSS variables when injected.
    """
    e = _html.escape
    parts: list[str] = []
    parts.append("<div class='wpfa-dashboard'>")
    parts.append(
        "<style>"
        ".wpfa-dashboard{font-family:'Inter',system-ui,sans-serif;color:#1a1a1a}"
        ".wpfa-dashboard h2{color:#B8860B;margin-top:1em}"
        ".wpfa-dashboard h3{margin-top:1.2em;border-bottom:1px solid #ccc;padding-bottom:0.2em}"
        ".wpfa-dashboard table{border-collapse:collapse;width:100%;margin:0.5em 0}"
        ".wpfa-dashboard th,.wpfa-dashboard td{border:1px solid #ccc;padding:0.4em 0.6em;text-align:left;font-size:0.9em}"
        ".wpfa-dashboard th{background:#f5f1e8}"
        ".wpfa-dashboard .attested{color:#2a6b3a;font-weight:600}"
        ".wpfa-dashboard .placeholder{font-style:italic;color:#666;padding:1em;background:#f5f1e8;border-left:3px solid #B8860B;margin:1em 0}"
        ".wpfa-dashboard .total{font-weight:600;background:#fdf8e8}"
        "</style>"
    )
    parts.append("<h2>WPFA Dashboard — Watts Per Funding Action</h2>")

    # Per-org rollup
    parts.append("<h3>Per-org rollups</h3>")
    if not data.per_org_rollups:
        parts.append("<p>No CycleReceipts on disk yet.</p>")
    else:
        for org_slug, rollup in sorted(data.per_org_rollups.items()):
            parts.append(f"<h4>{e(org_slug)}</h4>")
            parts.append(
                "<table><thead><tr>"
                "<th>cycle_id</th><th>emitted_at</th><th>attested?</th>"
                "<th>actual $</th><th>counterfactual $</th><th>delta $</th>"
                "<th>actual kWh</th><th>counterfactual kWh</th><th>delta kWh</th>"
                "</tr></thead><tbody>"
            )
            for row in rollup.receipts:
                attested = (
                    "<span class='attested'>yes</span>"
                    if row.is_buyer_attested
                    else "no"
                )
                parts.append(
                    f"<tr>"
                    f"<td>{e(row.cycle_id)}</td>"
                    f"<td>{e(row.emitted_at)}</td>"
                    f"<td>{attested}</td>"
                    f"<td>{e(_money(row.actual_dollars_minor_units))}</td>"
                    f"<td>{e(_money(row.counterfactual_dollars_minor_units))}</td>"
                    f"<td>{e(_money(row.delta_dollars_minor_units))}</td>"
                    f"<td>{e(_kwh(row.actual_watt_hours_micro))}</td>"
                    f"<td>{e(_kwh(row.counterfactual_watt_hours_micro))}</td>"
                    f"<td>{e(_kwh(row.delta_watt_hours_micro))}</td>"
                    f"</tr>"
                )
            parts.append(
                "<tr class='total'>"
                f"<td colspan='5'>cumulative saved</td>"
                f"<td>{e(_money(rollup.cumulative_dollars_saved_minor_units))}</td>"
                f"<td colspan='2'></td>"
                f"<td>{e(_kwh(rollup.cumulative_watt_hours_saved_micro))}</td>"
                "</tr>"
            )
            parts.append("</tbody></table>")

    # Per-quarter rollup
    parts.append("<h3>Per-quarter rollups (workspace aggregate)</h3>")
    if not data.per_quarter_rollups:
        parts.append("<p>No quarter-bucketed receipts yet.</p>")
    else:
        for q, qr in sorted(data.per_quarter_rollups.items()):
            parts.append(
                f"<h4>{e(q)} — total saved: {e(_money(qr.total_dollars_saved_minor_units))} "
                f"/ {e(_kwh(qr.total_watt_hours_saved_micro))}</h4>"
            )
            parts.append(
                "<table><thead><tr>"
                "<th>org</th><th>n cycles</th><th>delta $</th><th>delta kWh</th>"
                "</tr></thead><tbody>"
            )
            for org_slug, rollup in sorted(qr.per_org.items()):
                parts.append(
                    f"<tr>"
                    f"<td>{e(org_slug)}</td>"
                    f"<td>{len(rollup.receipts)}</td>"
                    f"<td>{e(_money(rollup.cumulative_dollars_saved_minor_units))}</td>"
                    f"<td>{e(_kwh(rollup.cumulative_watt_hours_saved_micro))}</td>"
                    f"</tr>"
                )
            parts.append("</tbody></table>")

    # Stage-2+ placeholder (RT-11 fold-in — data-free static text only)
    parts.append("<h3>Per-fleet rollup</h3>")
    parts.append(
        f"<div class='placeholder'>{e(data.per_fleet_placeholder)}</div>"
    )
    parts.append("</div>")
    return "".join(parts)


__all__ = [
    "DashboardData",
    "PER_FLEET_PLACEHOLDER_TEXT",
    "PerOrgRollup",
    "PerOrgRollupRow",
    "PerQuarterRollup",
    "build_dashboard_data",
    "render_dashboard_html",
]
