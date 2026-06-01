"""pipeline.cards — Card System runtime modules.

Authoritative specs:
  pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md   # DRAFT
  pipeline/blueprint/v0.1/section_18_card_system.md                   # DRAFT
  pipeline/blueprint/v0.1/section_04_logician_v2_x_card_hardening.md            # DRAFT
  pipeline/cards/README.md                                                      # directory orientation

v0.1 Beta scope: schema + directory + Pydantic models + loader skeleton +
fixture stubs + F-CARDS-* dormant primitives. v0.2 first wave graduates
predicate bodies + runtime context injection.
"""

from pipeline.cards import models as _models   # noqa: F401  (re-export gate)

__all__ = ["models"]
