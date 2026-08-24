# Plan template selection

Selected templates:

- Invoke `plan` mode for Work Pack gates, SWU reduction, and handoff;
- `implementation-layering` for L0-L3 sequencing and deferred-gate placement;
- split Work Pack because complexity is high and the five behaviors touch
  different owners and schema surfaces;
- execution pack for sequential wave choreography;
- task and wave pages so one Task Session can resolve one exact selector;
- machine manifests for SWU state, mutation admission, and closeout sync.

Not selected:

- single-file plan: it would hide atomicity and owner boundaries;
- live host experiment: this authoring route does not authorize spawning or
  claim a capacity API;
- consumer UX plan: route options expose a neutral contract only;
- host reservation/release implementation: both lack an admitted owner contract.
