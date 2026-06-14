import unittest
import os
import json
from pipeline.funding_lattice.models import OpportunityTarget

class TestJsonlInspection(unittest.TestCase):
    def test_first_record_fields(self):
        jsonl_path = "vault_shared/cached_opportunities/master_workbook.jsonl"
        if not os.path.exists(jsonl_path):
            self.skipTest("master_workbook.jsonl not found")

        with open(jsonl_path, 'r') as f:
            line = f.readline()
            if not line:
                self.skipTest("master_workbook.jsonl is empty")

            record = json.loads(line)
            # Check for required fields to build a future OpportunityTarget
            required_keys = ['record_id', 'source_name', 'funder_or_program', 'verification_posture']
            for k in required_keys:
                self.assertIn(k, record, f"Missing {k} in JSONL record")

if __name__ == "__main__":
    unittest.main()
