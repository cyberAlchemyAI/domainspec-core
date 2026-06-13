import argparse
import pandas as pd
import json
import os
import hashlib
from datetime import datetime

def generate_record_id(funder, program):
    s = f"{funder}_{program}".lower()
    return hashlib.md5(s.encode('utf-8')).hexdigest()[:12]

def clean_val(val):
    if pd.isna(val):
        return None
    if isinstance(val, str):
        val = val.strip()
        if not val:
            return None
    return val

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--manifest', required=True)
    args = parser.parse_args()

    if not os.path.exists(args.source):
        print(f"ERROR: Workbook not found at {args.source}")
        exit(1)

    xls = pd.ExcelFile(args.source)
    sheet_names = xls.sheet_names

    primary_sheet = None
    for s in sheet_names:
        if "Full Funding Source Catalog" in s:
            primary_sheet = s
            break

    if not primary_sheet:
        print(f"ERROR: Primary sheet not found. Available sheets: {sheet_names}")
        exit(1)

    # Dynamic header detection
    df_raw = pd.read_excel(xls, sheet_name=primary_sheet, header=None)
    header_idx = 0
    for i in range(10):
        if "Funding Source" in df_raw.iloc[i].values or "Funder" in df_raw.iloc[i].values:
            header_idx = i
            break

    df = pd.read_excel(xls, sheet_name=primary_sheet, header=header_idx)
    df = df.dropna(how='all')
    records = []

    for idx, row in df.iterrows():
        def get_val(possibilities):
            for p in possibilities:
                if p in row: return clean_val(row[p])
            return None

        funder = get_val(["Funder", "funder"]) or ""
        program = get_val(["Program", "program"]) or ""
        source_name = get_val(["Funding Source", "source_name"]) or f"{funder} {program}".strip()

        if not source_name:
            continue

        record_id = generate_record_id(funder, program)

        record = {
            "record_id": record_id,
            "source_name": source_name,
            "source_type": get_val(["Funding Type", "type"]),
            "funder_or_program": f"{funder} / {program}".strip(" /"),
            "url": get_val(["Official Source", "url", "Source URL"]),
            "category": get_val(["Funding Category", "category"]),
            "fit_summary": get_val(["Fit Notes", "fit_summary", "Language / Positioning Notes"]),
            "golden_quill_relevance": get_val(["Golden Quill Fit", "relevance"]),
            "idea_foundry_fit": get_val(["Idea Foundry Fit?", "Idea Foundry Fit"]),
            "priority": get_val(["Priority", "priority"]),
            "status": get_val(["Deadline Status", "status"]),
            "verification_status": get_val(["Verification Status"]) or "UNVERIFIED_SOURCE_LEAD",
            "deadline": get_val(["Deadline", "deadline"]),
            "amount_min": None,
            "amount_max": None,
            "geography": get_val(["Geography", "geography"]),
            "eligible_applicants": get_val(["Eligible Applicants", "eligibility", "Nonprofit Required?"]),
            "use_cases": get_val(["Best Use", "use_cases"]),
            "notes": get_val(["Notes", "notes"]),
            "tags": [],
            "source_sheet": primary_sheet,
            "source_row": idx + header_idx + 2,
            "source_workbook": os.path.basename(args.source),
            "cache_provenance": "operator_workbook",
            "verification_posture": get_val(["Verification Status"]) or "UNVERIFIED_SOURCE_LEAD"
        }
        records.append(record)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, 'w') as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    os.makedirs(os.path.dirname(args.manifest), exist_ok=True)

    import datetime as dt
    now_str = dt.datetime.now(dt.timezone.utc).isoformat()

    manifest = {
      "source_workbook_path": args.source,
      "source_workbook_filename": os.path.basename(args.source),
      "exported_at": now_str,
      "primary_sheet": primary_sheet,
      "included_sheets": [primary_sheet],
      "excluded_sheets": [s for s in sheet_names if s != primary_sheet],
      "row_count": len(df),
      "record_count": len(records),
      "column_map": {str(k): type(v).__name__ for k, v in dict(row).items() if pd.notna(k) and "Unnamed" not in str(k)},
      "notes": ["Funder Metadata and Search Seeds are not part of the cleaned workbook command surface and were not exported."],
      "cache_provenance": "operator_workbook"
    }
    with open(args.manifest, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"Used sheet: {primary_sheet}")
    print(f"Rows read: {len(df)}")
    print(f"Records exported: {len(records)}")
    print(f"Output path: {args.out}")
    print(f"Manifest path: {args.manifest}")

if __name__ == "__main__":
    main()
