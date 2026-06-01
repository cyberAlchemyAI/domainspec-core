import sys
import json
from pathlib import Path
from pipeline.nervous_system.funder_terrain.intake import intake_curated_funder_terrain_file

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Error: Missing required input file path.\n")
        sys.exit(1)

    if len(sys.argv) > 3:
        sys.stderr.write("Error: Too many arguments.\n")
        sys.exit(1)

    input_path_str = sys.argv[1]
    # Block remote-looking paths
    if input_path_str.startswith("http://") or input_path_str.startswith("https://") or "://" in input_path_str:
        sys.stderr.write("Error: Remote paths are not allowed.\n")
        sys.exit(1)

    input_path = Path(input_path_str)
    if not input_path.exists():
        sys.stderr.write(f"Error: Local file '{input_path}' not found.\n")
        sys.exit(1)

    output_dir = Path(sys.argv[2]) if len(sys.argv) == 3 else None

    try:
        record = intake_curated_funder_terrain_file(input_path, output_dir=output_dir)
        # Using json.dumps to guarantee deterministic sort_keys=True
        print(json.dumps(record.model_dump(exclude_none=True), sort_keys=True, indent=2))
    except Exception as e:
        sys.stderr.write(f"Error processing file: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
