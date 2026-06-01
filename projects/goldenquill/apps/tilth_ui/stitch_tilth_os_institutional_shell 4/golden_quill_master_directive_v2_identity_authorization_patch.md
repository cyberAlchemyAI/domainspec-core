# STITCH MASTER DIRECTIVE — Golden Quill / Tilth Operator Console (V2)

Use this document together with the updated `DESIGN.md`. 

## 1. Core Identity: Final Packet Authorization

Golden Quill is an operator-owned grant intelligence workbench. All terminology and workflow must reflect "Packet Authorization" rather than "Sign-Off."

- **Final Packet Authorization** = The screen for final review, licensing, authorization, and export.
- **Authorize Packet** = The primary cryptographic action.
- **Approve for Export** = The export-ready state.
- **Log Out** = Ending the user session only.

## 2. Applied-As Identity Boundary

Every node and application cycle is bound to one authorized applicant identity.

### AppliedAsIndicator (Global Chrome)
Must be visible in the Top Bar or Nav Rail on every screen.
- Show: Applied As organization, Licensed node organization, License state.
- States: `internal use verified`, `authorization required`, `mismatch blocked`.

### License / Identity Gate
A deterministic gate that fail-closes if node.organization_slug does not match cycle.organization_slug without verified agent authorization.
- Pass: `LICENSE GATE — applicant authority verified`
- Fail: `LICENSE GATE FAIL_CLOSED — applicant does not match licensed node`

## 3. Workflow Lifecycle

1. Discover (Scout)
2. Ingest (Vault)
3. Gate (Logician)
4. Decompose (Module Mapper)
5. Draft (Scribe)
6. Validate Budget
7. Score (Judge)
8. Red Team (Adversarial)
9. Authorize (Final Packet Authorization)
10. Audit (Ledger)

## 4. Final Packet Authorization Screen Requirements

Operator question: 
> Is this packet current, cleared, authorized to this applicant identity, signed, and ready for human submission?

Required Elements:
- Final packet preview
- Readiness checklist (Gate rollup)
- Applied As identity (Persistent)
- Authorized Entity Inspector (Right side)
- License Compliance gate (Fail-closed if mismatched)
- Hard eligibility gate summary
- Budget validation state
- Judge current/stale state
- Red Team unresolved items
- Artifact checklist (Hashes)
- Posture attestation
- Audit / lock-history preview
- Ed25519 authorization panel
- Authorize Packet action (Terracotta)
- Approve for Export state (Success state)
- Export Packet button (Only when all gates pass)
- Manual submission reminder: "Golden Quill prepares the packet. The operator submits through the funder's required portal."

## 5. System Personality & Interaction

- Infrastructure-grade, sober, institutional.
- No chat UI, no "AI assistant" fluff.
- Serif for reading, Inter for controls, Mono for hashes/IDs.
- Autosave is mandatory and visible.
- Every claim must have provenance.
- Final authority rests with the operator.
