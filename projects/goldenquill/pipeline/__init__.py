"""Tilth v0.1 — grant intelligence substrate running inside a Golden Quill.

Top-level package. Sections live at `pipeline.<section>`:
  - `pipeline.sovereignty`  Section 1 — Sovereignty Envelope
  - `pipeline.vault`        Section 2 — Vault Topology + Enforcement Envelope
  - `pipeline.scout`        Section 3 — Scout (two-stage discovery)
  - `pipeline.logician`     Section 4 — Logician (PRE/POST/COMMIT gates)
  - `pipeline.pipeline`     Section 5 — Pipeline orchestration

Public APIs live in each section's `__init__.py`. Downstream sections
import from `pipeline.<section>`, NOT from `pipeline.<section>.<module>`.
This boundary is enforced by the cross-section import AST-lint rule
(see `pipeline/engineering/engineering_process_v0.1.md` §4.1).
"""

__version__ = "0.1.0.dev0"

# D-RB-02 closure (2026-05-15) — process-wide Logfire bootstrap per
# v7.0.4-M1 §8.4.1 + runbook §9.1.  Called once at package import time;
# idempotent, honors `LOGFIRE_ENABLED=0` (Intake discipline), and degrades
# gracefully to a no-op + WARNING when logfire is not installed or the
# operator has not yet run `logfire auth`.  Must run AFTER `__version__`
# is bound — the shim reads it via `sys.modules.get('pipeline')` to tag
# spans with `service_version`.
from pipeline.observability.logfire_bootstrap import (  # noqa: E402
    bootstrap_logfire as _bootstrap_logfire,
)

_bootstrap_logfire()
