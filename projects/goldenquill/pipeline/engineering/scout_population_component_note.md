# Scout Onboarding Population Component — Engineering Note

Context: When a new client org on-boards, Scout should not operate only on live API hits and ad-hoc searches. It needs a **Population** step that builds a durable funder/opportunity database for that org before regular radar runs.

## Requirement

For each new org (e.g., Mystic Mamas):

1. **Ingest legacy knowledge**
   - Accept one or more source spreadsheets/CSVs of known funders/programs ("legacy funder sheets").
   - Normalize them into the shared Tilth schema under `pipeline/db/`:
     - `funders.csv` (global funders)
     - `programs.csv` (programs under those funders)
     - `calls.csv` (known calls/NOFOs when available)
     - `orgs.csv` (org row for this client)
     - `org_program_fit.csv` (baseline fit rows for every program for this org)
     - `applications.csv` (empty skeleton for historical/forward tracking).

2. **Discover new funders/opportunities**
   - Run the API-based discovery (Grants.gov, SBIR, NSF as appropriate) and 990/website discovery passes for the org’s geography + sectors.
   - Append any newly discovered programs/funders to the same normalized tables.

3. **Org-specific fit tagging**
   - For this org, create `org_program_fit` rows for **every** program:
     - Default `priority = LOW`, `go_no_go = TBD`.
     - Elevate to TOP/HIGH/MEDIUM for programs that clearly match the org’s entity type, geography, sectors, and identity tags.

4. **Operator review / correction loop**
   - Present the initial TOP/HIGH/MEDIUM/IGNORE ratings to the org/operator as a review task early in onboarding.
   - The operator explicitly **agrees or disagrees** with each rating; any overrides (e.g., "this is actually a fit" / "this is not for us") are written back into `org_program_fit` and treated as ground truth.
   - This makes Scout learn the org’s preferences **from day one** instead of silently assuming its own heuristics are correct.

5. **Recall across future Scout runs**
   - All future Scout work for that org should **reuse** this normalized DB as the first stop:
     - When scanning APIs, match new hits back to existing `funders/programs/calls` before adding new rows.
     - When generating briefs, draw candidates from the org’s `org_program_fit` filtered by priority + current_status, not from scratch each time.

## Done Definition for Population Step

The Population component for an org is "done" when:

- Their legacy funder sheets are imported and normalized into `pipeline/db/*.csv`.
- All discovered programs have at least one `org_program_fit` row for the org.
- Medium/High/TOP candidates are clearly tagged for the org.
- Subsequent Scout runs can treat the normalized DB as the canonical source for that org’s funding universe.

This component should be wired into Scout's onboarding protocol so that **every new client** gets a fully populated funder/opportunity map before regular radar cycles begin.
