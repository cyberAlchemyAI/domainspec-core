# Machine Witness Report: SWU-OV1-013

## Result

Machine proof passed. A normal one-shot CLI process created and operated an
HTML presentation through the unchanged local HTTP APIs, the real workbench
displayed the final complete revision, iframe interaction entered the generic
V4 event projection, and server restart recovered the same immutable result.

This report does not decide whether the result is useful. That is the blocking
human review in [DECISION-GATE.md](DECISION-GATE.md).

## Proved Workflow

1. Created complete interactive presentation HTML in a temporary project.
2. Published the document through unchanged V0.
3. Derived an Operations V1 surface from the exact V0 revision.
4. Committed one whole-document replacement and one visible append using fresh
   operation ids and expected-revision CAS.
5. Redirected the durable workbench target and observed `status: loaded`.
6. Used the presentation controls and the appended control inside the iframe.
7. Sent `decision.selected` through `ide-extension.canvas.event` and observed
   V4 projection cursor `1` with `value: approve`.
8. Restarted the server on the same port, reloaded the browser, and recovered
   the exact final revision and content.

## Exact Retained Evidence

Both independent browser runs produced:

- V0 content SHA-256:
  `e7a06e1c93648f813f9bb92709e43193f61381cf396144de3f4255cedf5189f5`
- final content SHA-256:
  `5d9321586d5452d620da090ca3a3b518d48befd50caefebe7d67578e6fed5830`
- Operations V1 revision count: `3` (derive, replace, append)
- navigation acknowledgement: `loaded`
- projected interaction: `decision.selected`, cursor `1`, payload value
  `approve`
- restart result: recovered revision equals the final committed revision

Retained artifacts:

- [Desktop evidence](assets/desktop-operations-value.json)
- [Desktop screenshot](assets/desktop-operations-value.png)
- [Mobile evidence](assets/mobile-operations-value.json)
- [Mobile screenshot](assets/mobile-operations-value.png)

## Visual Inspection

- Desktop: nonblank workbench and iframe, Cyber Alchemy SVG visible, title and
  appended content readable, controls visible, no incoherent overlap.
- Mobile: single-column workbench remains readable, SVG/title/buttons fit, no
  horizontal overflow, Operations state remains legible.
- The desktop and mobile runs are separate journeys with distinct surface and
  revision ids; matching digests prove equivalent immutable content.

## Validation

| Check | Result |
| --- | --- |
| `npm run test:operations-value` | pass, 1/1 |
| `npm run test:e2e:operations-value` | pass, 2/2 desktop/mobile |
| `node --test --test-concurrency=1 tests/manual-session-bridge-cli.test.mjs` | pass, 3/3 |
| `node --test --test-concurrency=1 tests/session-content-workbench-cli.test.mjs` | pass, 1/1 |
| retained screenshot inspection | pass, desktop/mobile |

## Honest Boundary

The evidence supports a trusted local agent creating and operating complete
HTML revisions through the local workbench. It does not prove regions,
collaboration, automatic merge, hostile HTML safety, remote browser control,
provider execution, or protected effects.

