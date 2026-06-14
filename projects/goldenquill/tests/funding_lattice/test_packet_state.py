import unittest
from pipeline.funding_lattice.models import OpportunityTarget, RouteLock, PacketState
from pipeline.funding_lattice.validators.validate_lattice import validate_target

class TestPacketState(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()
