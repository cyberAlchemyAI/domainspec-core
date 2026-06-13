import unittest
from pipeline.funding_lattice.projections.lattice_summary import summarize_lattice

class TestLatticeProjection(unittest.TestCase):
    def test_projection_summary(self):
        entities_dir = "pipeline/funding_lattice/examples/entities"
        targets_dir = "pipeline/funding_lattice/examples/targets"
        res = summarize_lattice(entities_dir, targets_dir)
        self.assertEqual(len(res), 1)
        target = res[0]
        self.assertEqual(target['opportunity_id'], "pittsburgh_foundation_fictional_2026")
        self.assertEqual(target['route_status'], "MISSING")
        self.assertEqual(target['next_valid_operator_action'], "Set or review route lock before drafting.")

if __name__ == "__main__":
    unittest.main()
