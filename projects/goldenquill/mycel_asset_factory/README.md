# MyCel Asset Factory

## Overview
The MyCel Asset Factory is an internal build workflow designed specifically for Josh and the FIT Farms team. It provides a lightweight, repo-contained asset generation system.

### What it is
- A tracking spine for registering generated MyCel assets.
- A system to record source inputs, generation prompts, and output paths.
- A mechanism to record asset and QA status.
- A deterministic metadata sidecar writer and index generator.

### What it is not
- It is NOT part of MyCel Core.
- It is NOT a user-facing UI component.
- It does NOT rely on heavy external frameworks or agents.

## Lane Boundaries
- **Asset Factory Lane**: Fully self-contained within this directory.
- **MyCel Core**: Modifying MyCel Core files from this lane is **FORBIDDEN**.
- **UI**: Modifying UI files from this lane is **FORBIDDEN**.
- **Governance Memory**: Modifying lessons or project history from this lane is **FORBIDDEN**.

## Posture
**FULL_ACCESS**
This is an internal build workflow for the founder’s own asset-generation process. The focus is exclusively on speed, asset generation, QA, traceability, reproducibility, and handoff quality.

## Asset Registration
To register a new asset:
1. Open `asset_register.json`.
2. Add a new JSON object adhering to the schema defined in `asset_register.schema.json`.

### Schema Fields
- `asset_id`: Unique identifier for the asset.
- `title`: Human-readable title.
- `asset_type`: Type of asset (e.g., diagram, wireframe, doc).
- `status`: Current status (`planned`, `generated`, `qa_pending`, `qa_passed`, `rejected`, `archived`).
- `created_at`: Creation timestamp (ISO 8601).
- `updated_at`: Last updated timestamp (ISO 8601).
- `source_inputs`: Array of input file paths.
- `generation_prompt_ref`: Path to the prompt used.
- `output_paths`: Array of generated output file paths.
- `qa_status`: Quality assurance status (`not_started`, `pending`, `passed`, `failed`, `needs_human_review`).
- `notes`: Any additional context.

## Scripts
- **Validate Register**: Run `python scripts/validate_asset_register.py` to ensure `asset_register.json` matches the schema.
- **Generate Index**: Run `python scripts/render_asset_index.py` to generate the human-readable index at `generated/ASSET_INDEX.md`.
