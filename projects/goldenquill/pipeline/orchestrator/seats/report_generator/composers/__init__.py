"""§14 Report Generator per-sub-section composers (WS-J Slice 2).

Per §14 v1 LOCKED 2026-05-10 + Slice 2 handoff (2026-05-11). Five
per-sub-section composers, each:

* takes injected Vault read intent callables (one per substrate it reads),
* takes an injected Scribe Protocol (for per-field drafting),
* takes a ``clock`` callable (for ``authored_at_utc`` timestamps),
* takes a ``hash_bytes`` callable (for ``source_content_sha3_512``),
* returns a ``(markdown_fragment, tuple[ClaimEntry, ...])`` pair.

The substrate I/O is performed by the injected callables, NEVER by
``open()`` directly. AST-lint
``R-REPORT-VAULT-INTENT-REQUIRED`` (Slice 3) enforces structurally.

Composer-level invariants validated before return:

* Every claim has at least one source (also enforced by
  ``ClaimEntry.__post_init__``; composer-level double-check fires
  with a more contextual error message).
* ``claim_id`` is deterministic per
  ``(sub_section, paragraph_index, sentence_index, claim_keyword_hash)``
  — re-derivable at audit time.
* ``claim_kind`` matches the composer's sub-section kind.
"""

from __future__ import annotations

from .beneficiary_section import (
    BeneficiaryRecordRow,
    BeneficiarySectionDeps,
    BeneficiarySectionResult,
    compose_beneficiary_section,
)
from .financial_summary import (
    FinancialActualRow,
    FinancialSummaryDeps,
    FinancialSummaryResult,
    compose_financial_summary,
)
from .metrics_table import (
    MetricRow,
    MetricsTableDeps,
    MetricsTableResult,
    compose_metrics_table,
)
from .narrative import (
    NarrativeDeps,
    NarrativeEntryRow,
    NarrativeResult,
    compose_narrative,
)
from .photo_gallery import (
    PhotoGalleryDeps,
    PhotoGalleryResult,
    PhotoRow,
    compose_photo_gallery,
)
from ._base import (
    ClockCallable,
    ComposerError,
    HashBytesCallable,
    ScribeFieldSpec,
    ScribeProtocol,
    VaultReadIntentCallable,
    compute_claim_id,
)


__all__ = [
    "BeneficiaryRecordRow",
    "BeneficiarySectionDeps",
    "BeneficiarySectionResult",
    "ClockCallable",
    "ComposerError",
    "FinancialActualRow",
    "FinancialSummaryDeps",
    "FinancialSummaryResult",
    "HashBytesCallable",
    "MetricRow",
    "MetricsTableDeps",
    "MetricsTableResult",
    "NarrativeDeps",
    "NarrativeEntryRow",
    "NarrativeResult",
    "PhotoGalleryDeps",
    "PhotoGalleryResult",
    "PhotoRow",
    "ScribeFieldSpec",
    "ScribeProtocol",
    "VaultReadIntentCallable",
    "compose_beneficiary_section",
    "compose_financial_summary",
    "compose_metrics_table",
    "compose_narrative",
    "compose_photo_gallery",
    "compute_claim_id",
]
