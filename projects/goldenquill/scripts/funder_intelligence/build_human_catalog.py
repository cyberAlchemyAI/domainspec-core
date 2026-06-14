#!/usr/bin/env python3
import pandas as pd
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
import os

INPUT_PATH = "/Users/goldenquill/Downloads/tilth_golden_quill_master_funding_command_workbook_june2026_upgrade.xlsx"
OUTPUT_PATH = "/Users/goldenquill/Downloads/golden_quill_funding_source_catalog.xlsx"

# Expected New Columns
COLUMNS = [
    "Priority", "Funding Source", "Funder", "Program", "Funding Type",
    "Funding Category", "Amount / Range", "Deadline", "Deadline Status",
    "Geography", "Eligible Applicants", "Nonprofit Required?",
    "Idea Foundry Fit?", "Golden Quill Fit", "Best Use", "Verification Status",
    "Official Source", "Next Verification Step", "Notes"
]

def map_category(old_cat):
    # Mapping old three-axis to new categories loosely
    s = str(old_cat).lower()
    if 'tech' in s or 'ai' in s or 'cyber' in s: return "AI / Technology Infrastructure"
    if 'econ' in s or 'dev' in s: return "Economic Development"
    if 'business' in s or 'entrepreneur' in s: return "Entrepreneurship / Small Business Support"
    if 'workforce' in s or 'capacity' in s: return "Workforce / Capacity Building"
    if 'innovat' in s: return "Community Innovation"
    if 'research' in s or 'commercial' in s: return "Research Commercialization"
    if 'philanthropy' in s or 'civic' in s: return "Philanthropy / Civic Infrastructure"
    if 'regional' in s or 'pa' in s or 'pennsylvania' in s: return "Regional Development"
    if 'creative' in s or 'art' in s: return "Creative Technology"
    return "Community Innovation"  # Default

xls = pd.ExcelFile(INPUT_PATH)

# Load data and filter
raw_df = pd.DataFrame()
if '02 Opportunity Universe' in xls.sheet_names:
    raw_df = pd.read_excel(xls, sheet_name='02 Opportunity Universe')
elif '01 Priority Pipeline' in xls.sheet_names:
    raw_df = pd.read_excel(xls, sheet_name='01 Priority Pipeline')

# Remove Hackers Guild
if 'Proposed Project Angle' in raw_df.columns:
    raw_df = raw_df[~raw_df['Proposed Project Angle'].str.contains("Hackers Guild", na=False, case=False)]
if 'Best-Fit Components' in raw_df.columns:
    raw_df = raw_df[~raw_df['Best-Fit Components'].str.contains("Hackers Guild", na=False, case=False)]

# Create new dataframe
def get_col(df, cols):
    for c in cols:
        if c in df.columns:
            return df[c]
    return pd.Series([""] * len(df))

new_df = pd.DataFrame(columns=COLUMNS)
new_df["Funder"] = get_col(raw_df, ["Funder"])
new_df["Program"] = get_col(raw_df, ["Opportunity/Program", "Program"])
new_df["Funding Source"] = new_df["Funder"].astype(str) + " - " + new_df["Program"].astype(str)
new_df["Funding Type"] = get_col(raw_df, ["Opportunity Type"])
new_df["Funding Category"] = get_col(raw_df, ["Track", "Best-Fit Components"]).apply(map_category)
new_df["Amount / Range"] = get_col(raw_df, ["Amount/Support"])
new_df["Deadline"] = get_col(raw_df, ["Status/Deadline"])
new_df["Deadline Status"] = "Open"
new_df["Geography"] = get_col(raw_df, ["Geography"])
new_df["Eligible Applicants"] = get_col(raw_df, ["Eligibility/Fit Notes"])
new_df["Nonprofit Required?"] = get_col(raw_df, ["Eligibility/Fit Notes"]).str.contains("501c3|501\\(c\\)\\(3\\)", na=False, case=False).map({True: "Yes", False: "No"})
new_df["Idea Foundry Fit?"] = get_col(raw_df, ["Applicant Route"]).str.contains("Idea Foundry", na=False, case=False).map({True: "Yes", False: "Review Needed"})
new_df["Golden Quill Fit"] = get_col(raw_df, ["Fit Score"])
new_df["Best Use"] = get_col(raw_df, ["Proposed Project Angle"])
new_df["Verification Status"] = "UNVERIFIED_SOURCE_LEAD"
new_df["Official Source"] = get_col(raw_df, ["Source URL"])
new_df["Next Verification Step"] = "Verify Live Deadline and Eligibility"
new_df["Notes"] = get_col(raw_df, ["Constraints/Risks"])
new_df["Priority"] = get_col(raw_df, ["Tier"])

# Remove KDC references
new_df = new_df.replace({'KDC': '', 'Keystone Development Center': ''}, regex=True)

with pd.ExcelWriter(OUTPUT_PATH, engine='openpyxl') as writer:
    # 00 Start Here
    ws00 = writer.book.create_sheet("00 Start Here + Gemini Guide")
    ws00.append(["Golden Quill Funding Source Catalog"])
    ws00.append([""])
    ws00.append(["This is a funding-source catalog."])
    ws00.append(["Rows are research leads until live-verified."])
    ws00.append(["The workbook helps humans review funding possibilities."])
    ws00.append(["It does not authorize, submit, package, or approve grants."])
    ws00.append(["Idea Foundry is the fiscal sponsor route for Golden Quill."])
    ws00.append(["Gemini can be used to summarize, filter, and compare sources."])
    ws00.append([""])
    ws00.append(["Gemini Prompts:"])
    ws00.append(["- Summarize the top funding sources by deadline."])
    ws00.append(["- Which funding sources look most relevant to Golden Quill?"])
    ws00.append(["- Which sources require nonprofit sponsorship?"])
    ws00.append(["- Which sources could fit through Idea Foundry?"])
    ws00.append(["- Which sources are for AI, entrepreneurship, workforce, economic development, or research commercialization?"])
    ws00.append(["- Which sources need live deadline verification?"])
    ws00.append(["- Which sources are worth discussing with Idea Foundry?"])

    # 01 Best Funding Sources
    best_df = new_df[new_df["Priority"].str.contains("Tier A|High|1", na=False, case=False)]
    best_df.to_excel(writer, sheet_name="01 Best Funding Sources", index=False)

    # 02 Full Funding Source Catalog
    new_df.to_excel(writer, sheet_name="02 Full Funding Source Catalog", index=False)

    # 03 Idea Foundry / Sponsor-Fit Sources
    idea_df = new_df[new_df["Idea Foundry Fit?"] == "Yes"]
    idea_df.to_excel(writer, sheet_name="03 Idea Foundry Sponsor-Fit", index=False)

    # 04 to 10
    pd.DataFrame(columns=["Funder", "Program", "Fit Notes"]).to_excel(writer, sheet_name="04 Golden Quill Fit Notes", index=False)
    new_df[["Funding Source", "Verification Status", "Next Verification Step", "Official Source"]].to_excel(writer, sheet_name="05 Verification Queue", index=False)

    if '07 Integrated Funder Metadata' in xls.sheet_names:
        metadata_df = pd.read_excel(xls, sheet_name='07 Integrated Funder Metadata')
        metadata_df.to_excel(writer, sheet_name="06 Funder Metadata", index=False)
    else:
        pd.DataFrame().to_excel(writer, sheet_name="06 Funder Metadata", index=False)

    if '08 Search Seed Library' in xls.sheet_names:
        seeds_df = pd.read_excel(xls, sheet_name='08 Search Seed Library')
        # Remove hackers guild
        if 'Search Theme/Sector' in seeds_df.columns:
            seeds_df = seeds_df[~seeds_df['Search Theme/Sector'].str.contains("Hackers Guild", na=False, case=False)]
        seeds_df.to_excel(writer, sheet_name="07 Search Seeds", index=False)
    else:
        pd.DataFrame().to_excel(writer, sheet_name="07 Search Seeds", index=False)

    pd.DataFrame(columns=["Field", "Definition"]).to_excel(writer, sheet_name="08 Field Dictionary", index=False)
    pd.DataFrame(columns=["Date", "Change Description", "Changed By"]).to_excel(writer, sheet_name="09 Change Log", index=False)
    pd.DataFrame(columns=COLUMNS).to_excel(writer, sheet_name="10 Archived Sources", index=False)

    # Styling
    for sheetname in writer.book.sheetnames:
        ws = writer.book[sheetname]

        # Style sheet 00
        if sheetname == "00 Start Here + Gemini Guide":
            ws.column_dimensions['A'].width = 100
            for row in ws.iter_rows():
                for cell in row:
                    cell.alignment = Alignment(wrap_text=True)
                    if cell.row == 1:
                        cell.font = Font(bold=True, size=14)
            continue

        # Freeze panes & Add auto filter
        if ws.max_row > 0 and ws.max_column > 0:
            ws.freeze_panes = "A2"
            ws.auto_filter.ref = ws.dimensions

        # Style headers
        header_fill = PatternFill(start_color="D9EAD3", end_color="D9EAD3", fill_type="solid")
        header_font = Font(bold=True)
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")

        # Set column widths and text wrap
        for col in range(1, ws.max_column + 1):
            letter = get_column_letter(col)
            ws.column_dimensions[letter].width = 30
            for row in range(2, ws.max_row + 1):
                cell = ws.cell(row=row, column=col)
                cell.alignment = Alignment(wrap_text=True, vertical="top")

print(f"Generated {len(new_df)} total sources.")
