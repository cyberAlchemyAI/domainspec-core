from pydantic import BaseModel
from typing import List, Optional, Dict
from pipeline.nervous_system.models import RouteMode

class ActionPolicy(BaseModel):
    name: str
    allowed_route_modes: List[str]
    requires_human: bool
    requires_applied_as: bool
    operation_intent: Optional[str] = None
    consequence_level: Optional[str] = None

class ActionRegistry:
    _actions: Dict[str, ActionPolicy] = {}

    @classmethod
    def register(cls, policy: ActionPolicy):
        cls._actions[policy.name] = policy

    @classmethod
    def get_policy(cls, action_name: str) -> Optional[ActionPolicy]:
        return cls._actions.get(action_name)

# Register default action policies
ActionRegistry.register(ActionPolicy(
    name="DISMISS_NOTICE",
    allowed_route_modes=[
        RouteMode.LOCAL_ONLY.value,
        RouteMode.HYBRID_PUBLIC_FRONTIER_LOCAL_VAULT.value,
        RouteMode.ALL_MODEL_ACCESS.value,
    ],
    requires_human=False,
    requires_applied_as=False,
    consequence_level="low"
))

ActionRegistry.register(ActionPolicy(
    name="STAGE_PACKET",
    allowed_route_modes=[
        RouteMode.LOCAL_ONLY.value,
        RouteMode.HYBRID_PUBLIC_FRONTIER_LOCAL_VAULT.value,
        RouteMode.ALL_MODEL_ACCESS.value,
    ],
    requires_human=True,
    requires_applied_as=True,
    consequence_level="high"
))
