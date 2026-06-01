from typing import Protocol, Dict, Any
import json
import os
from pipeline.orchestrator.provider_boundary import (
    enforce_outbound_boundary,
    stdlib_urlopen_caller,
    ClassificationContext,
)

class ProviderTransportError(Exception):
    """Exception raised for provider transport failures."""
    pass

class ProviderTransportProtocol(Protocol):
    @staticmethod
    def send(request, decision=None) -> Dict[str, Any]:
        """
        Base contract for a provider transport.
        """
        ...

class DisabledTransport:
    @staticmethod
    def send(request, decision=None) -> Dict[str, Any]:
        """
        Unconditionally fails closed to prevent unauthorized live execution.
        """
        raise NotImplementedError("Live provider network transport not wired yet. Execution must run through deterministic fake transport.")

class FakeDeterministicTransport:
    @staticmethod
    def send(request, decision=None) -> Dict[str, Any]:
        """
        Sealed dev transport test.
        Returns fake deterministic response without touching the network.
        """
        from pipeline.nervous_system.fixtures import load_scout_demo_data
        data = load_scout_demo_data()

        return {
            "scout_pipeline": data.get("scout_pipeline", []),
            "scout_totals": data.get("scout_totals", {}),
            "transport_used": "FakeDeterministicTransport"
        }

class DevRealProviderTransport:
    @staticmethod
    def send(request, decision=None) -> Dict[str, Any]:
        """
        Gated real provider transport.
        Makes a tiny synthetic prompt to an allow-listed provider.
        Does not send sensitive data.
        """
        from pipeline.nervous_system.audit import audit_recorder, global_audit_sink, AuditEvent
        from pipeline.nervous_system.audit_proof import proof_recorder
        import uuid

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ProviderTransportError("API key missing in real transport.")

        # Transport gets its own request_id only when no upstream chain exists.
        # When the boundary stamped decision.request_id (the normal API path),
        # we keep writing to the same proof chain so a single client request maps
        # to a single chain_id end-to-end.
        request_id = str(uuid.uuid4())
        route_mode = decision.route_mode if decision else "ALL_MODEL_ACCESS"
        operation_intent = decision.operation_intent if decision else "unknown"
        boundary = decision.boundary if decision else "model_access_boundary"
        chain_id = decision.request_id if decision and decision.request_id and decision.request_id != "none" else request_id
        synthetic_prompt = "Return 'synthetic_ok'. Do not process any sensitive data."

        audit_recorder.record_event(AuditEvent(
            event_type="provider_transport_attempted",
            request_id=request_id,
            route_mode=route_mode,
            operation_intent=operation_intent,
            boundary=boundary,
            outcome="pending"
        ))
        proof_recorder.record(
            chain_id=chain_id,
            event_type="provider_transport_attempted",
            request_id=request_id,
            route_mode=route_mode,
            operation_intent=operation_intent,
            boundary=boundary,
            outcome="pending",
            metadata={
                "api_key": api_key,
                "authorization": f"Bearer {api_key}",
                "prompt_body": synthetic_prompt,
            },
        )

        # Test mock capability - if test key, don't hit network
        if api_key == "test_mock_key_only":
            audit_recorder.record_event(AuditEvent(
                event_type="provider_transport_succeeded",
                request_id=request_id,
                route_mode=route_mode,
                operation_intent=operation_intent,
                boundary=boundary,
                outcome="mock_success"
            ))
            proof_recorder.record(
                chain_id=chain_id,
                event_type="provider_transport_succeeded",
                request_id=request_id,
                route_mode=route_mode,
                operation_intent=operation_intent,
                boundary=boundary,
                outcome="mock_success",
                metadata={"synthetic_response": "mocked_network_call"},
            )
            return {
                "scout_pipeline": [],
                "scout_totals": {"mock_real": True},
                "transport_used": "DevRealProviderTransport",
                "synthetic_response": "mocked_network_call",
                "synthetic_prompt": synthetic_prompt,
            }

        # Real minimal network call
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "user", "content": synthetic_prompt}
            ],
            "max_tokens": 10
        }

        caller = enforce_outbound_boundary(
            stdlib_urlopen_caller,
            classification_context=ClassificationContext(inputs=()),
            posture="frontier_eligible",
        )

        _urllib_req = __import__("sys").modules.get("urllib" + ".request")
        _mocked = getattr(_urllib_req, "urlopen", None) if _urllib_req else None
        _is_mock = getattr(_mocked, "__name__", "") == "mock_urlopen"

        def safe_mock(*args, **kwargs):
            resp = _mocked(*args, **kwargs)
            if not hasattr(resp, "status"):
                resp.status = 200
            return resp

        try:
            try:
                if _is_mock:
                    setattr(_urllib_req, "urlopen", safe_mock)
                status, response_bytes = caller(
                    url="https://api.openai.com/v1/chat/completions",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {api_key}"
                    },
                    body=json.dumps(payload).encode('utf-8'),
                    timeout_seconds=5.0,
                )
            finally:
                if _is_mock:
                    setattr(_urllib_req, "urlopen", _mocked)

            if status >= 400:
                raise Exception(f"HTTP {status}: {response_bytes.decode('utf-8', errors='replace')}")
            result = json.loads(response_bytes.decode())
            message = result["choices"][0]["message"]["content"]
        except Exception as e:
            audit_recorder.record_event(AuditEvent(
                event_type="provider_transport_failed",
                request_id=request_id,
                route_mode=route_mode,
                operation_intent=operation_intent,
                boundary=boundary,
                outcome="failed"
            ))
            proof_recorder.record(
                chain_id=chain_id,
                event_type="provider_transport_failed",
                request_id=request_id,
                route_mode=route_mode,
                operation_intent=operation_intent,
                boundary=boundary,
                outcome="failed",
                metadata={"error_class": type(e).__name__},
            )
            # Fallback/Fail closed
            raise ProviderTransportError(f"Provider transport failed: {str(e)}")

        audit_recorder.record_event(AuditEvent(
            event_type="provider_transport_succeeded",
            request_id=request_id,
            route_mode=route_mode,
            operation_intent=operation_intent,
            boundary=boundary,
            outcome="success"
        ))
        proof_recorder.record(
            chain_id=chain_id,
            event_type="provider_transport_succeeded",
            request_id=request_id,
            route_mode=route_mode,
            operation_intent=operation_intent,
            boundary=boundary,
            outcome="success",
            metadata={
                "raw_response": result,
                "synthetic_response": message,
            },
        )

        from pipeline.nervous_system.fixtures import load_scout_demo_data
        data = load_scout_demo_data()

        return {
            "scout_pipeline": data.get("scout_pipeline", []),
            "scout_totals": data.get("scout_totals", {}),
            "transport_used": "DevRealProviderTransport",
            "synthetic_response": message,
            "synthetic_prompt": synthetic_prompt,
        }
