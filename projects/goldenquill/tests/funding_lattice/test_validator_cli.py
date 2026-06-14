import unittest
import tempfile
import os
import subprocess
import sys
import yaml
from pipeline.funding_lattice.validators.validate_lattice import validate_file

class TestValidatorCLI(unittest.TestCase):
    def test_valid_entity_passes(self):
        errors = validate_file("pipeline/funding_lattice/examples/entities/fit_farms.example.yaml")
        self.assertEqual(errors, [])

    def test_valid_target_passes(self):
        errors = validate_file("pipeline/funding_lattice/examples/targets/pittsburgh_foundation_fictional.example.yaml")
        self.assertEqual(errors, [])

    def test_malformed_entity_fails(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("entity_id: bad_entity\nentity_type: applicant\n")
            f_path = f.name

        try:
            errors = validate_file(f_path)
            self.assertTrue(len(errors) > 0)
            self.assertTrue(any("missing required field" in e for e in errors))
        finally:
            os.remove(f_path)

    def test_malformed_target_fails(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("opportunity_id: bad_target\nlifecycle_stage: DRAFTING_ELIGIBLE\n")
            f_path = f.name

        try:
            errors = validate_file(f_path)
            self.assertTrue(len(errors) > 0)
        finally:
            os.remove(f_path)

    def test_cli_exits_nonzero_on_invalid(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("invalid_yaml: [ \n") # structural malformation
            f_path = f.name

        try:
            result = subprocess.run([sys.executable, "-m", "pipeline.funding_lattice.validators.validate_lattice", f_path], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
        finally:
            os.remove(f_path)

    def test_cli_exits_zero_on_valid_examples(self):
        files = []
        for root, _, fnames in os.walk("pipeline/funding_lattice/examples"):
            for fname in fnames:
                if fname.endswith(".yaml"):
                    files.append(os.path.join(root, fname))

        for f in files:
            result = subprocess.run([sys.executable, "-m", "pipeline.funding_lattice.validators.validate_lattice", f], capture_output=True)
            self.assertEqual(result.returncode, 0, f"Validation failed for {f}:\n{result.stderr.decode()}")

if __name__ == "__main__":
    unittest.main()
