from uuid import uuid4, UUID
from typing import Dict, Any
from .contracts import SubstrateResponse, StateMachineContext
from .logician import raise_blocker_failure
from .errors import SubstrateError

class MockMemoryStore:
    def __init__(self):
        self.sections = {}
        self.records = {}

    def seed_section(self, state: str) -> UUID:
        section_id = uuid4()
        self.sections[section_id] = {"state": state}
        return section_id

    def seed_record(self, state: str) -> UUID:
        record_id = uuid4()
        self.records[record_id] = {"state": state}
        return record_id

    async def update_memory(self, sm_context: StateMachineContext, item_id: UUID, payload: Dict[str, Any]) -> SubstrateResponse:
        try:
            # T08: Sealed Section Mutation
            if item_id in self.sections:
                if self.sections[item_id]["state"] == "SEALED":
                    raise_blocker_failure(409, "STATE.SEALED_SECTION_MUTATION", "Cannot mutate a SEALED section")

            # T14: Superseded Memory Update
            if item_id in self.records:
                if self.records[item_id]["state"] == "SUPERSEDED":
                    raise_blocker_failure(409, "MEMORY.UPDATE_SUPERSEDED_RECORD", "Cannot update a SUPERSEDED memory record")
        except SubstrateError as e:
            return SubstrateResponse(status="REJECTED", status_code=e.status_code, error=e.error)

        return SubstrateResponse(status="ACCEPTED", status_code=200, result={})
