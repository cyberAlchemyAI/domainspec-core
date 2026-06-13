import unittest
from pipeline.funding_lattice.models import OpportunityTarget, RouteLock, PacketState, Entity
from pipeline.funding_lattice.validators.validate_lattice import validate_target

class TestRouteLockValidation(unittest.TestCase):
    def test_missing_route_lock_prevents_drafting(self):
        target = OpportunityTarget(
            opportunity_id="test_opt",
            title="Test",
            funder="Funder",
            source_url="",
            verification_status="UNVERIFIED",
            deadline="2026",
            lifecycle_stage="DRAFTING_ELIGIBLE",
            route_lock=RouteLock(route_status="MISSING"),
            packet_state=PacketState(),
            fatal_gates=[]
        )
        errors = validate_target(target, [])
        self.assertIn("MISSING route_status cannot have DRAFTING_ELIGIBLE lifecycle_stage", errors)
        self.assertIn("MISSING route_status must have route_lock_missing in fatal_gates", errors)

    def test_missing_final_authorization_keeps_export_blocked(self):
        target = OpportunityTarget(
            opportunity_id="test_opt",
            title="Test",
            funder="Funder",
            source_url="",
            verification_status="UNVERIFIED",
            deadline="2026",
            lifecycle_stage="PREPARE",
            route_lock=RouteLock(route_status="VALID"),
            packet_state=PacketState(operator_authorization_present=False, export_blocked=False),
            fatal_gates=[]
        )
        errors = validate_target(target, [])
        self.assertIn("If operator_authorization_present is false, export_blocked must be true", errors)

    def test_sponsor_authorization_missing(self):
        target = OpportunityTarget(
            opportunity_id="test_opt",
            title="Test",
            funder="Funder",
            source_url="",
            verification_status="UNVERIFIED",
            deadline="2026",
            lifecycle_stage="PREPARE",
            route_lock=RouteLock(route_status="VALID", authorization_record_required=True, authorization_record_present=False),
            packet_state=PacketState(),
            fatal_gates=[]
        )
        errors = validate_target(target, [])
        self.assertIn("Route status cannot be VALID if authorization is required but missing", errors)

if __name__ == "__main__":
    unittest.main()
