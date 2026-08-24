# Decision Gate: WaveDB package provenance

- Status: unresolved blocker
- Source: `SWU-WCP-001` terminal provenance failure
- Consequential work blocked: package dependency resolution, native build,
  addon load, and SWU-WCP-002 through SWU-WCP-008
- Blocker fingerprint:
  `5b60290d587d390439f8d78ee74910b47ef5294481ab2fcba338793dc4132bfd`

## Admissible options

### OPT-STOP-CORRECTED-PROVENANCE — stop/defer (recommended)

Stop the current frontier and require a corrected registry release or an owner
provided exact provenance statement that binds one tarball to one reviewed
source tree. This creates no native risk and preserves the approved experiment
contract, but execution cannot continue until external evidence changes.

### OPT-REDESIGN-SOURCE-BUILD — action requiring a new route

Start a new Define/Design/Plan slice for a source build from the reviewed
commit, with its own dependency/toolchain pins, source archive integrity,
copy-sources behavior, package identity, and package/security owner gate. This
is reversible and candidate-local, but it is not the registry-package route the
current Work Pack admitted and cannot be executed by the blocked Task Session.

## Rejected automatic action

Treating CRLF-normalized similarity as exact provenance is rejected. It would
weaken an acceptance-critical gate and leave the packaged C source tree and
stale `gitHead` unexplained.

## Needed user decision

Select `OPT-STOP-CORRECTED-PROVENANCE` or authorize planning the separate
`OPT-REDESIGN-SOURCE-BUILD` route. “Explain / more context” remains available
and does not resolve the decision.
