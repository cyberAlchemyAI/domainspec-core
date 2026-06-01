from typing import Protocol, Dict, Any
from pipeline.nervous_system.transport import DisabledTransport, FakeDeterministicTransport, DevRealProviderTransport
from pipeline.nervous_system.route_policy import ModelAccessDecision

class ProviderAdapterProtocol(Protocol):
    @staticmethod
    def execute_live(request, decision: ModelAccessDecision = None) -> Dict[str, Any]:
        ...

class DisabledProviderAdapter:
    @staticmethod
    def execute_live(request, decision: ModelAccessDecision = None) -> Dict[str, Any]:
        """
        Stub for disabled live provider execution.
        """
        return DisabledTransport.send(request, decision=decision)

class DevProviderAdapter:
    @staticmethod
    def execute_live(request, use_real_transport: bool = False, decision: ModelAccessDecision = None) -> Dict[str, Any]:
        """
        Dev adapter for live provider execution.
        Delegates to real or fake transport based on the explicit flag.
        """
        if use_real_transport:
            return DevRealProviderTransport.send(request, decision=decision)
        return FakeDeterministicTransport.send(request, decision=decision)
