# Context Pack — SWU-CAPI-000 `-03` pass closeout

This strict closeout pack binds the accepted `-03` Task Session and experiment
receipts to an `invoke:refresh:apply-approved` status synchronization.

The owner may update only `WORK-PACK.md` and create the attempt-specific
`SWU-CAPI-000.wcli-20260805-node26-0.15.9-03.refresh.json` receipt. The update
must remove the consumed route, mark SWU-CAPI-000 complete, make SWU-CAPI-001
dependency-ready without selecting it, resolve only the staged-filter blocker,
and retain the fresh-process reader blocker.

API code, Craft sources, prior attempts, network access, publication,
deployment, promotion, and successor admission remain forbidden.
