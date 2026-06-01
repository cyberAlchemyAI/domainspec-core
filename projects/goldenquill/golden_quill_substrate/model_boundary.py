from typing import List, Dict, Any
from .contracts import SubstrateResponse
from .ingress import _security_failure_response

class MockModelBoundary:
    def __init__(self):
        self.frontier_call_count = 0

    async def invoke(self, route_mode: str, outbound_payload: Dict[str, Any], known_non_public_canaries: List[str]) -> SubstrateResponse:
        if route_mode == "HYBRID_PUBLIC_FRONTIER_LOCAL_VAULT":
            # T06: Hybrid Attempts to Send Vault Data to Frontier
            # Check by type, hash, sensitivity label, and custody classification
            for key, value in outbound_payload.items():
                if isinstance(value, dict):
                    if value.get("custody_classification") == "NON_PUBLIC":
                        return _security_failure_response(403, "MODEL_BOUNDARY.HYBRID_VAULT_EGRESS_ATTEMPT", "Hybrid route cannot serialize non-public Vault content")
                    if value.get("sensitivity_label") == "RESTRICTED":
                        return _security_failure_response(403, "MODEL_BOUNDARY.HYBRID_VAULT_EGRESS_ATTEMPT", "Hybrid route cannot serialize non-public Vault content")
                    # Enforce type and hash blocking for non-public content
                    if value.get("evidence_type") in ["INTERNAL_MEMORY", "PRIVATE_GRANT_DRAFT"]:
                        return _security_failure_response(403, "MODEL_BOUNDARY.HYBRID_VAULT_EGRESS_ATTEMPT", "Hybrid route cannot serialize internal evidence types")
                    if value.get("evidence_hash") in known_non_public_canaries:
                        return _security_failure_response(403, "MODEL_BOUNDARY.HYBRID_VAULT_EGRESS_ATTEMPT", "Hybrid route cannot serialize known restricted hashes")

            payload_str = str(outbound_payload)
            for canary in known_non_public_canaries:
                if canary in payload_str:
                    return _security_failure_response(
                        403,
                        "MODEL_BOUNDARY.HYBRID_VAULT_EGRESS_ATTEMPT",
                        "Hybrid route cannot serialize non-public Vault content"
                    )

        self.frontier_call_count += 1
        return SubstrateResponse(status="ACCEPTED", status_code=200, result={})
