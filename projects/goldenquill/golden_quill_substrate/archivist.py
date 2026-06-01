from uuid import UUID
from typing import List
from .contracts import RetrievalBundle
from .errors import SubstrateError
from .logician import raise_blocker_failure

class ArchivistPipeline:
    def __init__(self):
        self.execution_order = []

    def force_execution_order(self, order: List[str]):
        self.execution_order = order

    async def execute_search(self):
        # Enforce execution order T05
        expected = ["SQL_APPLIED_AS_PREFILTER", "STATE_FILTER", "SENSITIVITY_CUSTODY_FILTER", "VECTOR_SEARCH"]
        for idx, step in enumerate(self.execution_order):
            if step != expected[idx]:
                raise_blocker_failure(
                    status_code=500,
                    code="ARCHIVIST.RETRIEVAL_ORDER_VIOLATION",
                    message="Retrieval order violation"
                )

class MockArchivist:
    def __init__(self):
        self.rogue_entity_id = None

    def inject_rogue_result(self, applied_as_entity_id: UUID):
        self.rogue_entity_id = applied_as_entity_id

    # The actual retrieval bundle cross boundary logic is tested in handle_ingress
    # But Wait, T15 says: "Archivist result item.applied_as_entity_id != identity_context.applied_as_entity_id"
    # To pass T15 via handle_ingress, if the request is "archivist.retrieve", the mock might need to inject the rogue result into the pipeline.
    # Actually, in T15, the test calls `handle_ingress` and expects a 403 `ARCHIVIST.CROSS_BOUNDARY_RESULT`.
    # Let's add that to `ingress.py` or do it via the `RetrievalBundle` validation.
    pass
