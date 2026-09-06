# AlchLang documentation frontend

Repository-local React presentation for the AlchLang tutorial. It uses the
three-column structure common to technical documentation while keeping
AlchLang-specific content, styling, and assets.

The default route is an explanatory AlchLang overview. Its tutorial and
workspace links enter the section-addressable documentation view; the docs
header and brand return to the overview.

The overview constructs its example cumulatively across domain identity,
typed facts, an SFOL rule, authority contracts, and the final action and event.
The last step is byte-identical to the initial mini-workspace source.

The guide reflects the current `@cyberalchemy/domainspec-cli-candidate`
`0.4.0-candidate.0` implementation: canonical source loading, SFOL, all 13
DomainSpec backend type surfaces, deterministic compilation, guarded actions,
explicit Operation contracts, operation patterns, generated SQLite
transactional-Outbox code, durable dispatch, confirmed HTTP transport,
idempotent consumption, and the ORODI evidence boundary.

The language-realization boundary is explicit: this AlchLang compiler emits
TypeScript. The separate private DomainSpec 1.0.0 CLI retains its v2 package name.
The #domainspec-target guide documents the narrower AlchLang lowering profile,
explicit sidecar, fresh-output requirement and existing-application gaps. The
browser mini workspace does not execute that external compiler.

```bash
npm install
npm test
npm run build
npm run dev
```

The development server listens on `http://127.0.0.1:4193`. The build writes to
the ignored `dist/` directory.

## Frontend benchmark

Install the pinned Firefox runtime once, then run the benchmark against a fresh
production build:

```bash
npm run benchmark:install
npm run benchmark:frontend
npm run benchmark:pareto
```

The benchmark starts an isolated loopback preview on a free port and exercises
the overview, construction walkthrough, tutorial search, mini workspace, mobile
navigation, and reduced-motion behavior in Firefox. It scans both the overview
and complete tutorial/workspace DOM at desktop, tablet, and mobile sizes for
containment, every automated axe-core violation, duplicate IDs, target sizes,
and ARIA structure; indeterminate axe-core checks remain explicit review
findings. It also checks console, page, HTTP, request, and
external-network failures plus production bundle budgets. Performance timing
and undersized interactive targets are review signals rather than universal
pass/fail scores.

Each run writes a content-addressed evidence set under
`output/playwright/ux-validator/alchlang-docs-<timestamp>/`, including metadata,
findings, console/network evidence, axe results, ARIA snapshots, measurements,
screenshots, a Playwright trace, and explicit human-review residue. Passing the
benchmark is local browser evidence; it does not prove complete accessibility,
real-device behavior, reader comprehension, usability, deployment, or
production readiness.

### Pareto UI experiment

`npm run benchmark:pareto` builds one bundle and exercises four query-selected
treatments: `baseline`, `compact-spacing`, `progressive-reference`, and
`task-first`. Each variant runs through the same overview and tutorial surfaces
at desktop, tablet, and mobile sizes, producing 24 browser scans and 50
interaction checks, including progressive-disclosure defaults and deep links.

The run writes `pareto-tournament.json` and `pareto-summary.md` beside the
normal browser evidence. Automated viewport length produces a browser-proxy
frontier only. The product frontier remains `not_evaluable` until a completed
human-observation file supplies task time, comprehension, meaning coverage, and
pairwise preference for every eligible variant. Start from
`benchmark/human-observations.example.json`; never replace missing observations
with synthetic or zero values.

Individual treatments can be opened with `?variant=<id>`. Unknown IDs resolve
to `baseline`. A Pareto result is comparative test evidence, not product
approval or merge authority.

### Human pairwise review

Open `?view=compare` to review every unordered pair of the four treatments.
The six-match interface alternates display order, keeps both treatments visible,
and records A, B, or Tie for readability, navigation, information density, task
completion, and overall preference. Progress is stored only in the current
browser. A reset requires confirmation.

After all dimensions are complete, the page calculates non-dominated Pareto
layers and downloads a canonical JSON receipt with a SHA-256 evidence digest.
It deliberately applies no weighted total and declares no automatic winner.
The receipt is human comparison evidence only; it does not approve, merge,
publish, or deploy a treatment.

## Interactive workspace

The tutorial includes a browser-local workspace with an editable `.alch`
source file and three CLI-shaped actions:

- `domainspec check workspace.alch` validates the example and reports its
  source digest.
- `domainspec build workspace.alch --out generated` previews the generated
  artifact names under a virtual output path.
- `domainspec run workspace.alch ReleaseCredit ...` evaluates the example's
  approval rule and reports the simulated outcome.

The workspace is a deterministic learning sandbox. It does not invoke the
Node.js compiler, write files, call integration bindings, or perform external
effects. Its pattern listing is a documented browser snapshot, not a live
registry query. Use the repository CLI when native parsing, generated files,
registry closure, adapters, or provider execution are required.
