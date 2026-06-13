#!/usr/bin/env python3
import json
import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    register_path = os.path.join(base_dir, 'asset_register.json')
    generated_dir = os.path.join(base_dir, 'generated')
    index_path = os.path.join(generated_dir, 'ASSET_INDEX.md')

    os.makedirs(generated_dir, exist_ok=True)

    with open(register_path, 'r') as f:
        data = json.load(f)

    with open(index_path, 'w') as f:
        f.write("# MyCel Asset Factory - Index\n\n")
        
        assets = data.get("assets", [])
        if not assets:
            f.write("No assets registered yet.\n")
            print(f"Index successfully rendered to {index_path} (Empty)")
            return

        f.write("| Asset ID | Title | Type | Status | QA Status | Created At |\n")
        f.write("|----------|-------|------|--------|-----------|------------|\n")
        
        for asset in assets:
            f.write(f"| {asset.get('asset_id', '')} | {asset.get('title', '')} | {asset.get('asset_type', '')} | {asset.get('status', '')} | {asset.get('qa_status', '')} | {asset.get('created_at', '')} |\n")

    print(f"Index successfully rendered to {index_path}")

if __name__ == "__main__":
    main()
