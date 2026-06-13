import json
import os
import pytest

def test_asset_register_valid_json():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    register_path = os.path.join(base_dir, 'asset_register.json')
    
    with open(register_path, 'r') as f:
        data = json.load(f)
    
    assert "assets" in data
    assert isinstance(data["assets"], list)

def test_asset_register_schema():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    schema_path = os.path.join(base_dir, 'asset_register.schema.json')
    register_path = os.path.join(base_dir, 'asset_register.json')
    
    with open(schema_path, 'r') as f:
        schema = json.load(f)
        
    with open(register_path, 'r') as f:
        register = json.load(f)
        
    try:
        import jsonschema
        jsonschema.validate(instance=register, schema=schema)
    except ImportError:
        pytest.skip("jsonschema not installed")
