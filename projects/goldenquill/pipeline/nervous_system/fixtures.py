import json
import os

def load_scout_demo_data():
    """
    Loads deterministic fixture data for testing and mock seams.
    """
    fixture_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "tests", "fixtures", "nervous_system", "DEMO_DATA.json"
    )
    with open(fixture_path, "r") as f:
        return json.load(f)
