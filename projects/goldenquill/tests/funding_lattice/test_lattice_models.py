import unittest
from pipeline.funding_lattice.models import Entity

class TestLatticeModels(unittest.TestCase):
    def test_example_entities(self):
        e1 = Entity(entity_id="fit_farms", display_name="FIT Farms LLC", entity_type="applicant", legal_status="LLC")
        self.assertEqual(e1.entity_id, "fit_farms")

    def test_forbidden_submission_language(self):
        import os
        forbidden = ["ready for " + "submission", "ready to " + "submit", "autonomous " + "submission", "submit " + "automatically", "auto-" + "submit", "/builds/" + "authorized"]
        for root, dirs, files in os.walk("pipeline/funding_lattice"):
            for f in files:
                if f.endswith(('.py', '.yaml', '.json', '.md')):
                    with open(os.path.join(root, f), 'r', encoding='utf-8') as file:
                        content = file.read().lower()
                        for fb in forbidden:
                            self.assertNotIn(fb.lower(), content, f"Forbidden phrase '{fb}' found in {f}")

if __name__ == "__main__":
    unittest.main()
