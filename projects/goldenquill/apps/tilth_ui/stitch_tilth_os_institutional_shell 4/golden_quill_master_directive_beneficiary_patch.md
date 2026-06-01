# STITCH MASTER DIRECTIVE — Golden Quill / Tilth Operator Console

## APPLIED-AS IDENTITY & BENEFICIARY ENFORCEMENT

The node is legally tethered to its licensed owner (e.g., FIT Farms LLC).

### Primary Beneficiary Rule (Non-Negotiable)
1. Every grant application must name the licensed node owner as Lead Applicant or Co-Applicant.
2. The node owner must receive >50% of the project's economic/operational benefit.
3. The system must auto-fill the Applicant section with the node owner's verified profile data.
4. The system must physically lock the drafting/authorization process if the node owner is not designated as the Lead or Co-Applicant.

### License Gate — Primary Beneficiary Verification
- **PASS**: If `Applicant` == `NodeOwner` OR (`Applicant` includes `NodeOwner` AND `BeneficiaryPct` > 50).
- **FAIL_CLOSED**: If `Applicant` != `NodeOwner` OR `BeneficiaryPct` < 50.

**Fail Explanation:**
"Primary Beneficiary Enforcement: This node is licensed exclusively for packets where [Node Owner] is the Lead or Co-Applicant and primary beneficiary. Third-party grant writing is not permitted."

## FINAL PACKET AUTHORIZATION
- **Screen Name**: Final Packet Authorization (Retired "Sign-Off").
- **Primary Action**: Authorize Packet.
- **Export-ready state**: Approve for Export.
- **Exit Action**: Log Out (Session only).

## SYSTEM SHELL
- **Top Bar**: AppliedAsIndicator (Global), PostureBadge, AuditPill, SigningKeyChip.
- **AppliedAsIndicator**: Shows Applied As, Licensed Node, and License State (e.g., `mismatch blocked`).
