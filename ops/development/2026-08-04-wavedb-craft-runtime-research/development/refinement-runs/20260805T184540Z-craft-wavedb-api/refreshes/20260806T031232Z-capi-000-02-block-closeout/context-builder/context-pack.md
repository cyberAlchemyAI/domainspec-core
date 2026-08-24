# Context Pack: SWU-CAPI-000 `-02` Block Closeout

Strict coverage passes for the bounded Invoke Refresh closeout.

- Preserve the blocked Task Session and experiment receipts.
- Preserve the owner-selected 28-ledger/57-record scope.
- Update only the Work Pack and its SWU-CAPI-000 execution receipt.
- Remove the consumed automatic route.
- Do not repair the importer, create `-03`, select a successor, or touch product,
  Craft-source, publication, or deployment surfaces.

The controlling failure is `STAGED_LEDGER_FILTER_GAP`: the importer claims to
exclude staged evidence but its directory-component filter omitted the literal
`staged` name. No database was created.
