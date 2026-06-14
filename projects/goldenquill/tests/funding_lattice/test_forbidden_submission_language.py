import unittest
import os

class TestForbiddenLanguage(unittest.TestCase):
    def test_forbidden_submission_language(self):
        # obfuscated to avoid triggering grep
        forbidden = ["ready for " + "submission", "ready to " + "submit", "autonomous " + "submission", "submit " + "automatically", "auto-" + "submit", "/builds/" + "authorized"]
        for root, dirs, files in os.walk("pipeline/funding_lattice"):
            for f in files:
                if f.endswith('.py') or f.endswith('.yaml') or f.endswith('.json'):
                    with open(os.path.join(root, f), 'r') as file:
                        content = file.read().lower()
                        for fb in forbidden:
                            self.assertNotIn(fb.lower(), content, f"Forbidden phrase '{fb}' found in {f}")

if __name__ == "__main__":
    unittest.main()
