# IRO-REFRESH-001 source signal

The planning package had strong architecture and validation prose but no
single machine contract joining all ten units. Receipt names diverged between
the Work Pack, Dispatch, and closeout prose; later unit material scopes were
descriptive placeholders; successor semantics were implicit; and no strict
Context Builder, WPRA v2 epoch, or native Goal existed.

This Refresh is confined to the private internal planning package. It:

- makes `EXECUTION-CONTRACT.json` authoritative for ordered units, exact
  coordinator outputs, owner-material scope declarations, commands,
  successors, budgets, and pause gates;
- supplies strict terminal, closeout-owner, and IRO-001 decision-bundle schemas;
- keeps `DISPATCH.json` bounded to the first no-code runtime unit while the
  outer `IRO-FULL-STREAM` contract coordinates later owner-routed units;
- preserves zero current implementation, public mutation, promotion,
  publication, deployment, or production authority;
- makes a fresh WPRA v2 epoch mandatory after any semantic contract change.

The operator's direct request authorizes this exact planning-package repair and
the generation of Context, readiness, and Goal artifacts. Starting the Goal or
crossing a later owner pause remains a separate action.
