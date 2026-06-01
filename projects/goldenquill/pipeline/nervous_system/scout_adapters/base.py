from typing import Protocol, List, Any, Dict
from pipeline.nervous_system.scout_source_roster import SourceRecord, SourceStatus

class ScoutSourceAdapter(Protocol):
    """
    Deterministic external source adapter protocol.
    Enforces raw-inventory plumbing only. No LLM inference, scraping, or judgment allowed.
    """

    @property
    def source_id(self) -> str:
        """Globally unique identifier for the source this adapter manages."""
        ...

    def get_metadata(self) -> SourceRecord:
        """Returns the deterministic declaration of this source without side effects."""
        ...

    def ping_status(self) -> SourceStatus:
        """Checks source liveliness/availability without performing a full fetch."""
        ...

    def fetch_inventory(self) -> List[Dict[str, Any]]:
        """Returns deterministic, raw remote items, enforcing no inference/LLM extraction at this layer."""
        ...
