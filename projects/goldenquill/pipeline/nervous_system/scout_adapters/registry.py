from typing import List, Dict, Any
from pipeline.nervous_system.scout_source_roster import SourceRecord, SourceStatus
from .base import ScoutSourceAdapter

class ScoutAdapterRegistry:
    def __init__(self):
        self._adapters: Dict[str, ScoutSourceAdapter] = {}

    def register(self, adapter: ScoutSourceAdapter) -> None:
        if adapter.source_id in self._adapters:
            raise ValueError(f"Duplicate source_id registered: {adapter.source_id}")
        self._adapters[adapter.source_id] = adapter

    def list_metadata(self) -> List[SourceRecord]:
        return [adapter.get_metadata() for adapter in self._adapters.values()]

    def ping_all(self) -> Dict[str, SourceStatus]:
        return {
            source_id: adapter.ping_status()
            for source_id, adapter in self._adapters.items()
        }

    def fetch_inventory(self, source_id: str) -> List[Dict[str, Any]]:
        if source_id not in self._adapters:
            raise KeyError(f"No adapter registered for source_id: {source_id}")
        return self._adapters[source_id].fetch_inventory()

# Default deterministic empty registry
default_registry = ScoutAdapterRegistry()
