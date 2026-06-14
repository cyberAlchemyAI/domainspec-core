#!/usr/bin/env python3

import sys
import os
import shutil
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

# Column definitions
AWARD_LEDGER_COLS = [
    "Award ID", "Award Name", "Funder", "Applicant / Applied As", "Beneficiary",
    "Project / Geography", "Amount Awarded", "Cash Status", "Agreement Executed?",
    "Award Start Date", "Award End Date", "Restricted Uses", "Match Eligible?",
    "Federal Funds?", "Reporting Burden", "Evidence Created", "Award Verification Status",
    "Award Agreement Source / File Path", "Match Allowability Source", "Verified By",
    "Verified Date", "Leverage Status", "Notes"
]

LEVERAGE_ASSETS_COLS = [
    "Leverage Asset ID", "Source Award ID", "Leverage Class", "Leverage Type",
    "Asset Description", "Can Support", "Available As Of", "Asset Maturity Status",
    "Estimated Value", "Eligible Match Value", "Confidence", "Restriction / Condition",
    "Verification Source", "Verified By", "Verified Date", "Active?", "Notes"
]

MATCH_ALLOCATION_LEDGER_COLS = [
    "Allocation ID", "Leverage Asset ID", "Source Award ID", "Target Opportunity ID",
    "Target Opportunity Name", "Allocation Type", "Amount Allocated", "Allocation Status",
    "Allocation Date", "Released Date", "Remaining Eligible Value", "Notes"
]

STACK_PAIRINGS_COLS = [
    "Pairing ID", "Source Award ID", "Leverage Asset ID", "Target Opportunity ID",
    "Target Opportunity Name", "Proposed Use of Prior Award", "Why It Pairs",
    "Gate Result", "Gate Reason", "Required Match Amount", "Eligible Match Available",
    "Match Coverage %", "Stack Strength", "Final Stack Confidence", "Pairing Status",
    "Next Action", "Attached to Target?", "Operator Decision", "Decision Date", "Notes"
]

STACK_DASHBOARD_COLS = [
    "Award ID", "Award Name", "Amount Awarded", "Applicant / Applied As",
    "Leverage Summary", "Verified Leverage Count", "Available Match Total",
    "Encumbered Match Total", "Unencumbered Match Total", "Candidate Pairings Count",
    "Blocked Pairings Count", "Top Next Action", "Notes"
]

AWARD_SEED_CANDIDATES_COLS = [
    "Source Sheet", "Source Row", "Existing Opportunity / Award Name", "Existing Funder",
    "Existing Amount", "Existing Status", "Candidate Applicant / Applied As",
    "Candidate Beneficiary", "Candidate Verification Status", "Operator Review Notes",
    "Promote to Award Ledger?"
]

STACK_RULE_COLS = [
    "Stack Eligible?", "Accepts Prior Award Leverage?", "Accepts Federal Match?",
    "Match Required?", "Required Match Amount", "Match Type Accepted", "Target Deadline",
    "Asset Needed By", "Sponsor Authorization Required?", "Stack Notes", "Stack Gate Status",
    "Stack Next Action"
]

def add_dropdown(ws, col_letter, values, start_row=2, end_row=1000):
    dv = DataValidation(type="list", formula1=f'"{",".join(values)}"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"{col_letter}{start_row}:{col_letter}{end_row}")

def apply_formatting(ws, cols):
    header_font = Font(bold=True)
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    wrap_alignment = Alignment(wrap_text=True, vertical='top')

    for i, col in enumerate(cols, 1):
        col_letter = get_column_letter(i)
        ws.column_dimensions[col_letter].width = 25
        
        # Style header
        header_cell = ws.cell(row=1, column=i)
        header_cell.font = header_font
        header_cell.border = thin_border
        
        # Format columns based on names
        lower_col = col.lower()
        if "amount" in lower_col or "value" in lower_col:
            for r in range(2, 100):
                ws.cell(row=r, column=i).number_format = '"$"#,##0.00'
        elif "date" in lower_col or "as of" in lower_col or "needed by" in lower_col or "deadline" in lower_col:
            for r in range(2, 100):
                ws.cell(row=r, column=i).number_format = 'yyyy-mm-dd'
        elif "%" in col or "ratio" in lower_col:
            for r in range(2, 100):
                ws.cell(row=r, column=i).number_format = '0.00%'

        for r in range(2, 100):
            ws.cell(row=r, column=i).alignment = wrap_alignment

    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{ws.max_row}"

def setup_sheet(wb, title, cols):
    if title not in wb.sheetnames:
        ws = wb.create_sheet(title=title)
        ws.append(cols)
        apply_formatting(ws, cols)
        return ws
    return wb[title]

def apply_validations(ws, title):
    if title == "Award Ledger":
        add_dropdown(ws, get_column_letter(AWARD_LEDGER_COLS.index("Cash Status") + 1), ["Unknown", "Committed", "Reimbursable", "Cash Received", "Closed"])
        add_dropdown(ws, get_column_letter(AWARD_LEDGER_COLS.index("Agreement Executed?") + 1), ["Unknown", "Yes", "No"])
        add_dropdown(ws, get_column_letter(AWARD_LEDGER_COLS.index("Match Eligible?") + 1), ["Unknown", "Yes", "No", "Needs Review", "Restricted"])
        add_dropdown(ws, get_column_letter(AWARD_LEDGER_COLS.index("Federal Funds?") + 1), ["Unknown", "Yes", "No"])
        add_dropdown(ws, get_column_letter(AWARD_LEDGER_COLS.index("Award Verification Status") + 1), ["Unverified", "Award Notice Received", "Agreement Executed", "Funds Received", "Reimbursable", "Closed"])
        add_dropdown(ws, get_column_letter(AWARD_LEDGER_COLS.index("Leverage Status") + 1), ["Needs Review", "Candidate", "Verified", "Restricted", "Not Stackable", "Retired"])
    elif title == "Leverage Assets":
        add_dropdown(ws, get_column_letter(LEVERAGE_ASSETS_COLS.index("Leverage Class") + 1), ["Financial", "Evidence", "Readiness", "Credibility", "Capacity", "Compliance", "Partnership", "Infrastructure"])
        add_dropdown(ws, get_column_letter(LEVERAGE_ASSETS_COLS.index("Leverage Type") + 1), ["Cash Match", "Committed Match", "In-Kind Match", "Planning Complete", "Proof of Concept", "Prior Funder Validation", "Implementation Readiness", "Equipment Purchased", "Site Control", "Partner Commitment", "Evaluation Data", "Community Demand Evidence", "Federal Readiness", "Reporting Evidence", "Bridge Funding", "Reimbursement Capacity", "Narrative Credibility"])
        add_dropdown(ws, get_column_letter(LEVERAGE_ASSETS_COLS.index("Asset Maturity Status") + 1), ["Not Mature", "Available", "Pending Deliverable", "Restricted", "Expired", "Needs Review"])
        add_dropdown(ws, get_column_letter(LEVERAGE_ASSETS_COLS.index("Confidence") + 1), ["High", "Medium", "Low", "Needs Review"])
        add_dropdown(ws, get_column_letter(LEVERAGE_ASSETS_COLS.index("Active?") + 1), ["Yes", "No"])
    elif title == "Match Allocation Ledger":
        add_dropdown(ws, get_column_letter(MATCH_ALLOCATION_LEDGER_COLS.index("Allocation Type") + 1), ["Cash Match", "In-Kind Match", "Bridge Funding", "Reimbursement Capacity", "Evidence Only"])
        add_dropdown(ws, get_column_letter(MATCH_ALLOCATION_LEDGER_COLS.index("Allocation Status") + 1), ["Proposed", "Reserved", "Committed", "Released", "Rejected", "Expired"])
        # Scaffold formula for Remaining Eligible Value
        rem_val_idx = MATCH_ALLOCATION_LEDGER_COLS.index("Remaining Eligible Value") + 1
        ws.cell(row=2, column=rem_val_idx).value = "Formula Scaffold: =INDEX(LeverageAssets[Eligible Match Value], MATCH([@[Leverage Asset ID]], LeverageAssets[Leverage Asset ID], 0)) - SUMIFS([Amount Allocated], [Leverage Asset ID], [@[Leverage Asset ID]], [Allocation Status], \"Proposed\") - ..."
    elif title == "Stack Pairings":
        add_dropdown(ws, get_column_letter(STACK_PAIRINGS_COLS.index("Proposed Use of Prior Award") + 1), ["Cash Match", "In-Kind Match", "Proof of Concept", "Planning Evidence", "Implementation Readiness", "Prior Funder Validation", "Partner Commitment", "Site / Equipment Readiness", "Reporting Evidence", "Bridge Funding", "Narrative Credibility"])
        add_dropdown(ws, get_column_letter(STACK_PAIRINGS_COLS.index("Gate Result") + 1), ["Pass", "Blocked", "Needs Verification", "Needs Logician Review"])
        add_dropdown(ws, get_column_letter(STACK_PAIRINGS_COLS.index("Stack Strength") + 1), ["High", "Medium", "Low", "Risky", "Needs Judge Review"])
        add_dropdown(ws, get_column_letter(STACK_PAIRINGS_COLS.index("Final Stack Confidence") + 1), ["High", "Medium-High", "Medium", "Low", "Blocked", "Needs Review"])
        add_dropdown(ws, get_column_letter(STACK_PAIRINGS_COLS.index("Pairing Status") + 1), ["Candidate", "Needs Verification", "Verified", "Blocked", "Rejected", "Attached", "Retired"])
        add_dropdown(ws, get_column_letter(STACK_PAIRINGS_COLS.index("Attached to Target?") + 1), ["Yes", "No"])
        add_dropdown(ws, get_column_letter(STACK_PAIRINGS_COLS.index("Operator Decision") + 1), ["Use", "Do Not Use", "Hold", "Needs More Evidence", "Rejected"])
        # Scaffold formulas for Gate Result based on rule logic
        gate_res_idx = STACK_PAIRINGS_COLS.index("Gate Result") + 1
        ws.cell(row=2, column=gate_res_idx).value = "Formula Scaffold: Check Target vs Source Match Rules (Federal, Eligible, Deadlines, Encumbrance)"
    elif title == "Award Seed Candidates":
        add_dropdown(ws, get_column_letter(AWARD_SEED_CANDIDATES_COLS.index("Candidate Verification Status") + 1), ["Needs Review", "Verified by Operator", "Rejected", "Duplicate", "Insufficient Evidence"])
        add_dropdown(ws, get_column_letter(AWARD_SEED_CANDIDATES_COLS.index("Promote to Award Ledger?") + 1), ["No", "Ready for Manual Entry"])

def append_stack_rules(wb, sheet_name):
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        headers = [cell.value for cell in ws[1]]
        cols_added = 0
        
        start_col = ws.max_column + 1
        for rule_col in STACK_RULE_COLS:
            if rule_col not in headers:
                col_letter = get_column_letter(start_col + cols_added)
                ws.cell(row=1, column=start_col + cols_added, value=rule_col)
                # Style header
                ws.cell(row=1, column=start_col + cols_added).font = Font(bold=True)
                ws.cell(row=1, column=start_col + cols_added).border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

                # Add validations
                if rule_col in ["Stack Eligible?", "Accepts Prior Award Leverage?", "Sponsor Authorization Required?"]:
                    add_dropdown(ws, col_letter, ["Unknown", "Yes", "No", "Needs Review"])
                elif rule_col == "Accepts Federal Match?":
                    add_dropdown(ws, col_letter, ["Unknown", "Yes", "No", "Restricted", "Needs Review"])
                elif rule_col == "Match Required?":
                    add_dropdown(ws, col_letter, ["Unknown", "Yes", "No"])
                elif rule_col == "Match Type Accepted":
                    add_dropdown(ws, col_letter, ["Unknown", "Cash", "In-Kind", "Cash or In-Kind", "Federal Allowed", "Federal Not Allowed", "Needs Review"])
                elif rule_col == "Stack Gate Status":
                    add_dropdown(ws, col_letter, ["Not Reviewed", "Candidate", "Needs Verification", "Blocked", "Verified"])
                elif rule_col == "Stack Next Action":
                    add_dropdown(ws, col_letter, ["Review Match Rules", "Verify Award Agreement", "Verify Applicant Route", "Check Deadline", "Check Encumbrance", "Request Sponsor Authorization", "Ready for Pairing", "Do Not Stack"])
                
                # Apply column width
                ws.column_dimensions[col_letter].width = 25
                
                # Add formatting
                if "amount" in rule_col.lower():
                    for r in range(2, 100): ws.cell(row=r, column=start_col+cols_added).number_format = '"$"#,##0.00'
                elif "deadline" in rule_col.lower() or "by" in rule_col.lower() or "start" in rule_col.lower() or "end" in rule_col.lower():
                    for r in range(2, 100): ws.cell(row=r, column=start_col+cols_added).number_format = 'yyyy-mm-dd'
                elif "ratio" in rule_col.lower():
                    for r in range(2, 100): ws.cell(row=r, column=start_col+cols_added).number_format = '0.00%'

                for r in range(2, 100): ws.cell(row=r, column=start_col+cols_added).alignment = Alignment(wrap_text=True, vertical='top')

                cols_added += 1
        
        # Update auto filter
        if ws.auto_filter:
            ws.auto_filter.ref = f"A1:{get_column_letter(ws.max_column)}{ws.max_row}"
        return cols_added
    return 0

def find_won_rows(wb):
    seeds = []
    skip_sheets = ["Award Ledger", "Leverage Assets", "Match Allocation Ledger", "Stack Pairings", "Stack Dashboard", "Award Seed Candidates"]
    for sheet_name in wb.sheetnames:
        if sheet_name in skip_sheets:
            continue
        ws = wb[sheet_name]
        headers = [str(cell.value).strip().lower() if cell.value else "" for cell in ws[1]]
        
        status_col_idx = None
        for i, h in enumerate(headers):
            if "status" in h:
                status_col_idx = i
                break
        
        if status_col_idx is not None:
            opp_col_idx = next((i for i, h in enumerate(headers) if "opportunity" in h or "program" in h or "award" in h), None)
            funder_col_idx = next((i for i, h in enumerate(headers) if "funder" in h), None)
            amount_col_idx = next((i for i, h in enumerate(headers) if "amount" in h), None)
            
            for row_idx, row in enumerate(ws.iter_rows(min_row=2), 2):
                if row[status_col_idx].value is None: continue
                status_val = str(row[status_col_idx].value).strip().lower()
                if "won" in status_val or "awarded" in status_val:
                    opp_val = row[opp_col_idx].value if opp_col_idx is not None else ""
                    funder_val = row[funder_col_idx].value if funder_col_idx is not None else ""
                    amount_val = row[amount_col_idx].value if amount_col_idx is not None else ""
                    seeds.append({
                        "sheet": sheet_name,
                        "row": row_idx,
                        "opp": opp_val,
                        "funder": funder_val,
                        "amount": amount_val,
                        "status": row[status_col_idx].value
                    })
    return seeds

def main():
    if len(sys.argv) > 1:
        wb_path = sys.argv[1]
    else:
        wb_path = "research/funder_intelligence_seed/tilth_golden_quill_master_funding_command_workbook.xlsx"
        
    if not os.path.exists(wb_path):
        print(f"ERROR: Workbook not found at {wb_path}")
        sys.exit(1)
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dir_name = os.path.dirname(wb_path)
    base_name = os.path.basename(wb_path)
    name, ext = os.path.splitext(base_name)
    backup_path = os.path.join(dir_name, f"{name}_backup_{timestamp}{ext}")
    
    # In-place argument check
    in_place = False
    if "--in-place" in sys.argv:
        in_place = True
        output_path = wb_path
    else:
        output_name = name.replace("_upgrade", "").replace("_capital_stacking", "") + "_capital_stacking" + ext
        output_path = os.path.join(dir_name, output_name)

    shutil.copy2(wb_path, backup_path)
    
    wb = load_workbook(wb_path)
    
    sheets_added = []
    
    # 1. Award Ledger
    if "Award Ledger" not in wb.sheetnames:
        ws = setup_sheet(wb, "Award Ledger", AWARD_LEDGER_COLS)
        apply_validations(ws, "Award Ledger")
        sheets_added.append("Award Ledger")
        
    # 2. Leverage Assets
    if "Leverage Assets" not in wb.sheetnames:
        ws = setup_sheet(wb, "Leverage Assets", LEVERAGE_ASSETS_COLS)
        apply_validations(ws, "Leverage Assets")
        sheets_added.append("Leverage Assets")
        
    # 3. Match Allocation Ledger
    if "Match Allocation Ledger" not in wb.sheetnames:
        ws = setup_sheet(wb, "Match Allocation Ledger", MATCH_ALLOCATION_LEDGER_COLS)
        apply_validations(ws, "Match Allocation Ledger")
        sheets_added.append("Match Allocation Ledger")

    # 4. Stack Pairings
    if "Stack Pairings" not in wb.sheetnames:
        ws = setup_sheet(wb, "Stack Pairings", STACK_PAIRINGS_COLS)
        apply_validations(ws, "Stack Pairings")
        sheets_added.append("Stack Pairings")

    # 5. Stack Dashboard
    if "Stack Dashboard" not in wb.sheetnames:
        ws = setup_sheet(wb, "Stack Dashboard", STACK_DASHBOARD_COLS)
        sheets_added.append("Stack Dashboard")

    # Stack rule columns
    existing_sheets_modified = []
    c1 = append_stack_rules(wb, "02 Opportunity Universe")
    if c1 > 0: existing_sheets_modified.append("02 Opportunity Universe")
    c2 = append_stack_rules(wb, "Opportunity Universe")
    if c2 > 0: existing_sheets_modified.append("Opportunity Universe")
    c3 = append_stack_rules(wb, "01 Priority Pipeline")
    if c3 > 0: existing_sheets_modified.append("01 Priority Pipeline")
    c4 = append_stack_rules(wb, "Priority Pipeline")
    if c4 > 0: existing_sheets_modified.append("Priority Pipeline")

    # Award Seed Candidates
    seeds = find_won_rows(wb)
    if seeds and "Award Seed Candidates" not in wb.sheetnames:
        ws = setup_sheet(wb, "Award Seed Candidates", AWARD_SEED_CANDIDATES_COLS)
        apply_validations(ws, "Award Seed Candidates")
        sheets_added.append("Award Seed Candidates")
        for s in seeds:
            ws.append([
                s["sheet"], s["row"], s["opp"], s["funder"], s["amount"], s["status"],
                "", "", "Needs Review", "", ""
            ])
            # Default to needs review format
            ws.cell(row=ws.max_row, column=9).value = "Needs Review"
            
    wb.save(output_path)
    
    # Write report
    report_name = f"capital_stacking_upgrade_report_{timestamp}.txt"
    report_path = os.path.join(dir_name, report_name)
    with open(report_path, "w") as f:
        f.write("Capital Stacking Upgrade Report\n")
        f.write("===============================\n\n")
        f.write(f"1. Workbook path found: {wb_path}\n")
        f.write(f"2. Backup path created: {backup_path}\n")
        f.write(f"3. Upgraded workbook path: {output_path}\n")
        f.write(f"4. Sheets created: {', '.join(sheets_added) if sheets_added else 'None'}\n")
        f.write(f"5. Sheets already present: {', '.join([s for s in wb.sheetnames if s not in sheets_added])}\n")
        f.write(f"6. Columns added to existing sheets: Stack Rules appended to {', '.join(existing_sheets_modified) if existing_sheets_modified else 'None'}\n")
        f.write(f"7. Award Seed Candidates created: {'Yes' if 'Award Seed Candidates' in sheets_added else 'No'}\n")
        f.write(f"8. Number of legacy Won rows found: {len(seeds)}\n")
        f.write("9. Confirmation: No Won rows were promoted into Award Ledger.\n")
        f.write("10. Confirmation: No existing sheets were deleted.\n")
        f.write("11. Confirmation: No existing sheets were renamed.\n")
        f.write("12. Confirmation: No existing cell values were overwritten.\n")
        f.write("13. Formulas / Scaffolds added: Added scaffold descriptions in Match Allocation Ledger (Remaining Eligible Value) and Stack Pairings (Gate Result) to document intention without forcing fragile bindings.\n")
        f.write("14. Formula areas deferred: Exact formula mapping was deferred because exact Excel Table names/ranges are not guaranteed.\n")
        f.write("15. Final workbook save status: Success.\n")

    print(f"WORKBOOK_PATH|{wb_path}")
    print(f"BACKUP_PATH|{backup_path}")
    print(f"OUTPUT_PATH|{output_path}")
    print(f"REPORT_PATH|{report_path}")
    print(f"SHEETS_ADDED|{','.join(sheets_added)}")
    print(f"SHEETS_MODIFIED|{','.join(existing_sheets_modified)}")
    print(f"SEED_COUNT|{len(seeds)}")
    print(f"SEED_TAB_CREATED|{'Yes' if 'Award Seed Candidates' in sheets_added else 'No'}")

if __name__ == "__main__":
    main()
