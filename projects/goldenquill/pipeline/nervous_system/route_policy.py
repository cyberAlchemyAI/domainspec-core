from pydantic import BaseModel
import os

class ModelAccessDecision(BaseModel):
    allowed: bool
    route_mode: str
    execution_mode: str
    provider_access: str
    reason: str
    boundary: str
    provider_adapter: str
    provider_name: str = "none"
    operation_intent: str = "none"
    request_id: str = "none"

class RoutePolicy:
    @staticmethod
    def evaluate(route_mode: str, operation_intent: str) -> ModelAccessDecision:
        """
        Evaluates the requested route_mode and operation_intent and returns a ModelAccessDecision.
        """
        # Dev Provider rules
        if route_mode == "ALL_MODEL_ACCESS" and operation_intent == "rescan_scout_opportunities":
            enable_dev = os.environ.get("GOLDEN_QUILL_ENABLE_DEV_PROVIDER") == "1"
            enable_real = os.environ.get("GOLDEN_QUILL_ENABLE_REAL_PROVIDER") == "1"
            provider_name = os.environ.get("GOLDEN_QUILL_PROVIDER_NAME")
            api_key = os.environ.get("OPENAI_API_KEY")

            if enable_dev and enable_real and provider_name == "openai-dev-stub" and api_key:
                return ModelAccessDecision(
                    allowed=True,
                    route_mode=route_mode,
                    execution_mode="dev_real_provider_transport",
                    provider_access="enabled_dev_only",
                    reason="Real provider access granted via explicit flags, API key, and allow-listed provider.",
                    boundary="model_access_boundary",
                    provider_adapter="dev",
                    provider_name=provider_name,
                    operation_intent=operation_intent
                )
            elif enable_dev:
                return ModelAccessDecision(
                    allowed=True,
                    route_mode=route_mode,
                    execution_mode="dev_provider_adapter",
                    provider_access="enabled",
                    reason="Explicit dev provider access granted via ALL_MODEL_ACCESS + environment flag.",
                    boundary="model_access_boundary_dev_stub",
                    provider_adapter="dev",
                    provider_name="none",
                    operation_intent=operation_intent
                )

        # Default fallback: deterministic fixture
        return ModelAccessDecision(
            allowed=True,
            route_mode=route_mode,
            execution_mode="deterministic_fixture",
            provider_access="disabled",
            reason="Route policy defaults to deterministic fixture until live execution is explicitly wired or authorized.",
            boundary="model_access_boundary_stub",
            provider_adapter="none",
            provider_name="none",
            operation_intent=operation_intent
        )
