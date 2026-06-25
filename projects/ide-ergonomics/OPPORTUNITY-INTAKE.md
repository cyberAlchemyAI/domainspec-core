---
tags: [ide, ergonomics, intake, capture, candidate, coordinate-admission]
node_type: intake
is_session: false
layer: workflow
nature: on-ramp
status: active
created: 2026-06-24
---

# Ergonomic Opportunity Intake

The **easy on-ramp**: a low-friction way to add a new ergonomic opportunity *right
now*, without running the whole lifecycle. Capturing is cheap and **candidate-only**
— nothing is promoted, built, or admitted by capturing it.

## How to add one (30 seconds)

1. Copy the template block below.
2. Fill the **five required fields** (everything else is optional).
3. Append it to [opportunity-backlog.md](opportunity-backlog.md) under `## Captured`.

That's it. A captured opportunity is a **default-deny candidate** on the coordinate
space (see [UNIFIED-PRODUCT-VIEW.md](UNIFIED-PRODUCT-VIEW.md) §"Coordinate Admission"):
it sits in the backlog until someone triages it, and it never becomes a coordinate,
a primitive, or canon until it passes the admission gate. Capture first, decide later
— the Necronomicon "side-note" discipline (`arcanum/spells/necronomicon/README.md`
§Interaction State Model) applied to product opportunities.

## Template

```md
### OPP-<NNN> <short title>
- friction: <the friction or lost-motion this removes — one sentence>
- coordinate: <restraint | routing-grammar | work-arc | session-state | evidence | input-side | social | NEW:?>
- first-owner: <the Arcanum capability or governance owner that would own the next step>
- priority-guess: <P0 | P1 | P2>
- status: captured
- captured: <YYYY-MM-DD>
- notes: <optional — source span, evidence, related primitive/opportunity>
```

### Field guide

- **friction** — what slow/lost/error-prone thing in the human-machine loop this fixes. If you can't name the friction, it's not an opportunity yet.
- **coordinate** — which axis of the model it touches (the seven current coordinates, or `NEW:?` if it doesn't fit any — a `NEW:?` is a *candidate coordinate* that must clear the irreducibility admission gate, so flag it).
- **first-owner** — who owns the next governed step (e.g. `definitions-governance`, `dispatch-spec`, `craft`, `experiment-harness`, `PRODUCT-VIEW.md owner`). Don't assign authority — just name the likely owner.
- **priority-guess** — a guess, not a commitment. Triage re-decides.
- **status** — always `captured` at intake. Triage moves it to `triaged → in-lifecycle → admitted | dropped`.

## Lifecycle (what happens after capture)

```text
captured  (intake — this file)
  -> triaged          (someone sets priority + confirms owner; or drops with reason)
  -> in-lifecycle     (the ide-assisted-arcanum-routing spell runs it: design -> plan -> implement -> test)
  -> admitted | dropped   (owner-gated: the coordinate-admission gate / decision-gate admits or rejects)
```

The backlog is the **front-door** of the `ide-assisted-arcanum-routing` spell. The
intake does not run the lifecycle; it just makes sure good opportunities don't
evaporate. A `NEW:?` coordinate triages through the admission gate before anything
is built on it.

## Boundaries

- Capture is candidate-only: no promotion, no build, no coordinate added.
- A `NEW:?` coordinate is a proposal, not a coordinate — it is default-deny until the
  irreducibility admission gate (owner = `PRODUCT-VIEW.md` / governance) admits it.
- The backlog is a read/work model; admitting an opportunity routes through its
  named owner with a receipt, never from the backlog alone.

## See also

- [opportunity-backlog.md](opportunity-backlog.md) — the captured queue (append here).
- [ERGONOMICS-OPPORTUNITIES.md](ERGONOMICS-OPPORTUNITIES.md) — the curated priority map (triaged/owned opportunities graduate here).
- [UNIFIED-PRODUCT-VIEW.md](UNIFIED-PRODUCT-VIEW.md) — the coordinate space + admission gate a captured opportunity is measured against.
