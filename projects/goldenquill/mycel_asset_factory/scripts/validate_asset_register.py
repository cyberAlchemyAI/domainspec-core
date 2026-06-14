#!/usr/bin/env python3
import json
import os
import sys

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    schema_path = os.path.join(base_dir, 'asset_register.schema.json')
    register_path = os.path.join(base_dir, 'asset_register.json')

    try:
        import jsonschema
    except ImportError:
        print("jsonschema not installed. Doing basic JSON syntax check instead.")
        try:
            with open(register_path, 'r') as f:
                json.load(f)
            print("Basic JSON syntax valid.")
            sys.exit(0)
        except Exception as e:
            print(f"JSON syntax error: {e}")
            sys.exit(1)

    with open(schema_path, 'r') as f:
        schema = json.load(f)
        
    with open(register_path, 'r') as f:
        register = json.load(f)

    try:
        jsonschema.validate(instance=register, schema=schema)
        print("Validation successful. asset_register.json complies with schema.")
    except jsonschema.exceptions.ValidationError as e:
        print(f"Validation failed: {e.message}")
        sys.exit(1)

if __name__ == "__main__":
    main()
