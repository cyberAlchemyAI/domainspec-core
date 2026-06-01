import pytest
from pipeline.nervous_system.scout_adapters.base import ScoutSourceAdapter
from pipeline.nervous_system.scout_adapters.registry import ScoutAdapterRegistry
from pipeline.nervous_system.scout_source_roster import SourceRecord, SourceStatus, SourceType

class DummyAdapter:
    @property
    def source_id(self) -> str:
        return "dummy_source_1"

    def get_metadata(self) -> SourceRecord:
        return SourceRecord(
            source_id=self.source_id,
            name="Dummy Source",
            source_type=SourceType.api,
            source_status=SourceStatus.verified,
            enabled=True
        )

    def ping_status(self) -> SourceStatus:
        return SourceStatus.verified

    def fetch_inventory(self) -> list[dict]:
        return [{"id": "item1", "title": "Raw Data"}]

def test_registry_registration_and_metadata():
    registry = ScoutAdapterRegistry()
    adapter = DummyAdapter()

    registry.register(adapter)

    with pytest.raises(ValueError, match="Duplicate source_id registered"):
        registry.register(adapter)

    metadata = registry.list_metadata()
    assert len(metadata) == 1
    assert metadata[0].source_id == "dummy_source_1"

def test_registry_ping_and_fetch():
    registry = ScoutAdapterRegistry()
    registry.register(DummyAdapter())

    statuses = registry.ping_all()
    assert statuses["dummy_source_1"] == SourceStatus.verified

    inventory = registry.fetch_inventory("dummy_source_1")
    assert len(inventory) == 1
    assert inventory[0]["id"] == "item1"

def test_registry_fetch_unknown():
    registry = ScoutAdapterRegistry()
    with pytest.raises(KeyError, match="No adapter registered for source_id"):
        registry.fetch_inventory("unknown_id")
