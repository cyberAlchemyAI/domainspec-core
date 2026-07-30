# Task Session Context — SWU-BWVA-002

Strict coverage: `true`

## Selected unit

Render the admitted SWU-BWVA-001 projection as one complete static-first atlas
through an additive renderer and the existing generated-view pipeline.

## Live preflight

- selected cursor: `SWU-BWVA-002`
- dependency: SWU-BWVA-001 terminal and owner receipts pass
- coverage receipt: current and source-locked
- target atlas and renderer/test files: absent as expected
- current generator: matches the Design baseline
- existing output baselines:
  - `BUSINESS-VIEWS.html`: `8a6159b5def1982ab25de0bffaa3bc2124f7e8d085c3376f7c44bb6cf7dda2af`
  - `BUSINESS-JOURNEY-EXPERIMENT.html`: `2484193e538aa6ae1c8b1b2542e7b5052374aec2aed9410b87c20726e1d5833d`
- generator material writes only changed artifact bytes
- semantic source baselines: match `WORK-PACK.md`

## Boundary

Allowed material writes are the generator, renderer, and render test. Allowed
generated outputs are `BUSINESS-VIEW-ATLAS.html` and the additive link in
`BUSINESS-VIEWS.md`. Existing gallery, journey, and SVG bytes must remain
unchanged.

Authority ceiling: removable local generated projection only.

