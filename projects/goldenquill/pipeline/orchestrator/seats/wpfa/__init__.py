"""WPFA — Watts Per Funding Action cycle-close accounting seat. [§17 v1]

Per-cycle telemetry artifact emission. Always-local; deterministic;
extends A12 Decimal mandate to energy quantities.

Public surface:
    - cycle_accountant.compose_receipt — deterministic composition callable
    - pdf_emitter.emit_buyer_facing_pdf — operator-attested PDF emission
"""

from __future__ import annotations

__all__ = ["cycle_accountant", "pdf_emitter"]
