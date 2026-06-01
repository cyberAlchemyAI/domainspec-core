from typing import Any
from .contracts import SubstrateResponse
from .logician import raise_blocker_failure
from .errors import SubstrateError

class MockPacketEngine:
    async def prepare_packet(self, source_ref: str) -> SubstrateResponse:
        try:
            # T09: Packet Hash from Mutable Source
            if source_ref in ["drafts", "live", "current"] or "drafts" in source_ref or "live" in source_ref or "current" in source_ref:
                raise_blocker_failure(409, "PACKET.HASH_REQUIRES_IMMUTABLE_SNAPSHOT", "Packet hash requires immutable source")
        except SubstrateError as e:
            return SubstrateResponse(status="REJECTED", status_code=e.status_code, error=e.error)

        return SubstrateResponse(status="ACCEPTED", status_code=200, result={"hash": "immutable_hash_123"})
