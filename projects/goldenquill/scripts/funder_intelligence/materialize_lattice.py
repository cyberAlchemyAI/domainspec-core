#!/usr/bin/env python3
import pandas as pd
import yaml
import os
import math

WORKBOOK_PATH = "/Users/goldenquill/Downloads/tilth_golden_quill_master_funding_command_workbook_june2026_upgrade.xlsx"
ORG_DIR = "/Users/goldenquill/Downloads/GoldenQuill/orgs/golden_quill"
PIPELINE_DIR = "/Users/goldenquill/Downloads/GoldenQuill/pipeline/funder_intelligence"
VAULT_DIR = "/Users/goldenquill/Downloads/GoldenQuill/vault_shared/cached_opportunities"

os.makedirs(ORG_DIR, exist_ok=True)
os.makedirs(PIPELINE_DIR, exist_ok=True)
os.makedirs(VAULT_DIR, exist_ok=True)

xls = pd.ExcelFile(WORKBOOK_PATH)

def clean_dict(d):
    """Remove NaN values for cleaner YAML"""
    return {k: v for k, v in d.items() if not (isinstance(v, float) and math.isnan(v))}

# 1. Master Pipeline YAML (Sheets 01 and 02)
pipeline_records = []
for sheet in ['01 Priority Pipeline', '02 Opportunity Universe']:
    if sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        for _, row in df.iterrows():
            record = clean_dict(row.to_dict())
            # Enforce Architectural Authorization Tokens
            record['verification_status'] = "UNVERIFIED_CACHE_REFERENCE"
            record['lifecycle_stage'] = "DRAFTING"
            record['authorization_status'] = "PENDING_AUTHORIZATION"
            if 'governance' not in record:
                record['governance'] = {
                    'law_4_scan': 'REQUIRED',
                    'private_benefit_guardrail': 'ENFORCED'
                }
            pipeline_records.append(record)

# Deduplicate by Funder/Program if needed, but for now just output Priority Pipeline logic
# We'll just write it as YAML
with open(os.path.join(VAULT_DIR, 'master_pipeline.yaml'), 'w') as f:
    yaml.dump(pipeline_records, f, sort_keys=False, allow_unicode=True)

print("Created master_pipeline.yaml")

# 2. Law 4 Term Register (Sheet 12)
if '12 Law 4 Term Register' in xls.sheet_names:
    df_terms = pd.read_excel(xls, sheet_name='12 Law 4 Term Register')
    with open(os.path.join(PIPELINE_DIR, 'LAW_4_TERM_REGISTER.md'), 'w') as f:
        f.write("# Law 4 Term Register\n\n")
        f.write("This register governs active admin-risk term scanning. Judge and Red Team agents use these substitutions to ensure apolitical, funder-preferred dialects are used in all federal and high-risk applications.\n\n")
        f.write(df_terms.to_markdown(index=False))
    print("Created LAW_4_TERM_REGISTER.md")

# 3. Project Context (Sheets 00, 05, 13, 14)
with open(os.path.join(ORG_DIR, 'PROJECT_CONTEXT.md'), 'w') as f:
    f.write("# Golden Quill / Tilth: Project Context & Routing\n\n")

    if '14 June 2026 Change Log' in xls.sheet_names:
        f.write("## June 2026 Change Log\n\n")
        f.write(pd.read_excel(xls, sheet_name='14 June 2026 Change Log').to_markdown(index=False) + "\n\n")

    if '13 Fiscal Sponsor Routes' in xls.sheet_names:
        f.write("## Fiscal Sponsor Routes\n\n")
        f.write(pd.read_excel(xls, sheet_name='13 Fiscal Sponsor Routes').to_markdown(index=False) + "\n\n")

    if '05 Route + Entity Strategy' in xls.sheet_names:
        f.write("## Route + Entity Strategy\n\n")
        f.write(pd.read_excel(xls, sheet_name='05 Route + Entity Strategy').to_markdown(index=False) + "\n\n")

print("Created PROJECT_CONTEXT.md")
print("Migration Complete.")
