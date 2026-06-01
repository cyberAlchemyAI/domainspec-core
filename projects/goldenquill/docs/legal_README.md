# `docs/legal/` — local-only legal working drafts

The `docs/legal/` directory in this repository is **gitignored** by design (see `.gitignore` "2026-05-17 — legal templates" block). This file is the public, repo-tracked breadcrumb describing what lives there locally on Josh's machine, so operators and agents working in this repo know the folder exists and what kind of artifacts to look for — without those artifacts entering the public engineering history.

## Why gitignored

Working drafts of NDA, non-compete, engagement-letter, and similar instruments are operator-facing legal documents. They contain placeholders for counterparty names, addresses, consideration amounts, and other specifics. They are intended for **attorney review before signature** — not for the public engineering repo. Anything that may be subject to attorney-client privilege or that names a specific counterparty before that counterparty has signed should never live in repo history.

Default-deny posture: `docs/legal/` and everything inside it is excluded from git. This file (`docs/legal_README.md`) lives one directory up — it is *not* covered by the ignore rule and is tracked normally.

## What is currently at `docs/legal/` locally (as of 2026-05-18)

The following files exist locally on Josh's working tree. They are not in git and should not be committed. Names only — no contents.

- `mutual_nda_template_2026-05-17.md` — generic mutual NDA template (any counterparty).
- `non_compete_template_2026-05-17.md` — generic non-compete + non-solicitation template (any signer).
- `NDA_PaulNorton_DRAFT_2026-05-18.md` — Paul Norton-specific mutual NDA draft, attorney-review-pending.
- `NonCompete_PaulNorton_DRAFT_2026-05-18.md` — Paul Norton-specific non-compete + non-solicitation draft, attorney-review-pending.
- `_summary_PaulNorton_2026-05-18.md` — one-page operator summary for the Paul packet.
- `FIT_Farms_Paul_Norton_NDA_NonSolicit_NonCircumvention_FILLED.pdf` — earlier-cycle filled artifact; reconcile with attorney before sending anything new.

## Adding new files

When a new legal working draft is added under `docs/legal/` locally:

1. The file lives at `docs/legal/<descriptive_name>_<YYYY-MM-DD>.md` (or appropriate extension).
2. Update the list above in this README with the file name and a one-line description (names only — never paste contents).
3. Commit the README change. Do not commit the underlying file.

## Posture rules (do not violate)

1. **No contents in git.** Never paste clause text, defined terms, or counterparty-specific language into any committed file (commit messages, PR descriptions, code comments, READMEs). If you need to reference a clause, reference it by section number and file name only.
2. **No counterparty PII in git.** Addresses, emails, phone numbers, signature blocks, EINs/SSNs/UEIs of counterparties stay out of the repo.
3. **Attorney review before execution.** No file under `docs/legal/` is executable until a licensed attorney has reviewed it for the relevant jurisdiction.
4. **Reconcile filled artifacts.** When a filled PDF lives alongside a markdown draft (as with the Paul Norton folder today), the attorney call is whether the new draft supersedes, supplements, or sets aside the filled artifact.

## Related

- `.gitignore` — the rule that excludes `docs/legal/` (block dated 2026-05-17).
- `CLAUDE.md` / `AGENTS.md` — workspace operator guidance for agents working in this repo.

*— Maintained as the index-only public note. Last updated 2026-05-18.*
