---
project: whisky-doses
status: draft
framework: astro
ui-framework: react
styling: tailwind
component-lib: shadcn
color-mode: light-dark
created: 2026-05-21
updated: 2026-05-21
---

# Frontend Architecture Constitution

Governing document for all frontend decisions in this project. Every UI-SPEC and frontend implementation must follow these conventions. Deviations require an explicit project decision update.

## Stack

| Layer          | Choice                | Version | Notes                                                                   |
| -------------- | --------------------- | ------- | ----------------------------------------------------------------------- |
| Meta-framework | Astro                 | planned | File-based pages with React islands for interactive screens             |
| UI framework   | React                 | planned | Client islands for operational tools, forms, tables, and stateful flows |
| Language       | TypeScript            | planned | DomainSpec base TypeScript stack                                        |
| Styling        | Tailwind CSS          | planned | Utility styling plus CSS variables for theme tokens                     |
| Component lib  | shadcn/ui             | planned | Copy-paste primitives built on Radix UI                                 |
| Icons          | lucide-react          | planned | Standard icon set for buttons, navigation, statuses, and actions        |
| Data fetching  | TanStack Query        | planned | Query caching, mutations, invalidation, and optimistic-safe refetches   |
| Forms          | React Hook Form + Zod | planned | Form state with schema validation close to API contracts                |
| Font           | Inter                 | planned | Local or package-loaded UI font; system fallback allowed                |

## Design Principles

1. **Operational first** — Screens prioritize repeated operator workflows over marketing presentation.
2. **Dense but calm** — Use tables, grouped panels, filters, and status chips for scan-friendly work without visual noise.
3. **Source truth visible** — Payment, allocation, buyer, and shipment status must show their authoritative source or freshness where useful.
4. **Copy/paste aware** — WhatsApp-ready outputs must be easy to review, select, and copy without implying direct delivery.
5. **Blockers are explicit** — Missing CPF, missing address, unpaid status, reconciliation exceptions, and shipment blockers must be visually obvious.

## Color System

Light/dark theme using shadcn-compatible HSL CSS variable tokens. Light mode is the default for operator work; dark mode must remain complete.

| Token                                    | Role                                          |
| ---------------------------------------- | --------------------------------------------- |
| `--background` / `--foreground`          | Page background / default text                |
| `--card` / `--card-foreground`           | Framed repeated items and modals              |
| `--popover` / `--popover-foreground`     | Menus, command palette, and floating overlays |
| `--primary` / `--primary-foreground`     | Primary operator actions                      |
| `--secondary` / `--secondary-foreground` | Lower-emphasis actions                        |
| `--muted` / `--muted-foreground`         | Subtle backgrounds and helper text            |
| `--accent` / `--accent-foreground`       | Hover, selected, and focus-support states     |
| `--destructive`                          | Error and destructive actions                 |
| `--border`                               | Borders and dividers                          |
| `--input`                                | Form control borders                          |
| `--ring`                                 | Focus rings                                   |
| `--sidebar-*`                            | Sidebar theming                               |
| `--chart-1..5`                           | Reporting and dashboard chart palette         |

Palette direction: neutral operational base with restrained amber for whisky/listing context, green for paid/ready/shipped, red for errors/destructive actions, and blue for informational states. Avoid beige/brown dominance, heavy purple gradients, decorative orbs, and marketing-style hero compositions.

## Typography

| Usage       | Font                                                   | Weight             |
| ----------- | ------------------------------------------------------ | ------------------ |
| Body / UI   | Inter                                                  | 400, 500, 600, 700 |
| Code / Mono | `ui-monospace`, `SFMono-Regular`, `Menlo`, `monospace` | 400, 500           |

Base size: 14px for dense operational screens. Use a compact scale: 12px metadata, 14px body, 16px section labels, 20px page titles, and 24px only for high-level dashboard titles. Do not scale font size with viewport width. Letter spacing must remain `0`.

## Layout

```text
┌──────────────────────────────────────────────────────────────┐
│ App Shell                                                     │
├───────────────┬──────────────────────────────────────────────┤
│ Sidebar       │ Top Bar: page title, filters, global actions │
│ Feature nav   ├──────────────────────────────────────────────┤
│ Status queues │ Page content: tables, forms, work queues     │
└───────────────┴──────────────────────────────────────────────┘
```

- **Sidebar** — Primary feature navigation and compact status queues.
- **Top bar** — Page title, selected context, filters, and one primary action.
- **Content region** — Work-focused layouts: tables, split list/detail views, editable forms, and copyable message previews.

Cards are allowed for repeated items, modals, and genuinely framed tools. Do not nest cards inside cards or make page sections look like floating cards.

## Routing & Page Structure

Astro file-based routing under `web/src/pages/`.

```text
web/src/pages/
├── buyers/index.astro
├── listings/index.astro
├── listings/[listingId].astro
├── payment-runs/index.astro
├── payment-runs/[paymentRunId].astro
├── messages/index.astro
├── shipments/index.astro
└── shipments/[shipmentBatchId].astro
```

Routes may be revised by feature UI-SPECs, but the information architecture must remain feature-oriented and operator-first.

## Component Organization

```text
web/src/
├── components/
│   ├── ui/           → shadcn/ui primitives
│   ├── layout/       → App shell, sidebar, page headers
│   └── <feature>/    → Feature-specific React components
├── hooks/            → Shared query and mutation hooks
├── lib/              → API client, query keys, formatting helpers
├── layouts/          → Astro layouts
├── pages/            → Astro routes
└── styles/
    └── global.css    → Tailwind imports and theme tokens
```

## Data Layer

### API Client

Use a typed fetch client under `web/src/lib/api-client.ts`.

- Base URL: `import.meta.env.PUBLIC_API_BASE_URL`, defaulting to `/api`.
- Auth: operator session credentials or token header, selected during backend implementation.
- Errors: normalize API failures into typed domain errors with `code`, `message`, and optional `fieldErrors`.
- Dates and money: parse at the boundary and format in UI helpers, not inline in components.

### TanStack Query

- Query keys live in `web/src/lib/query-keys.ts`.
- Use one custom hook per resource or read model.
- Mutations invalidate the narrowest affected query sets.
- UI-SPECs must name the read models and mutations each screen needs.

### Forms

- Use React Hook Form with Zod schemas.
- Prefer API-aligned schemas in feature modules.
- Show validation inline and preserve operator-entered values after failed submits.

## Component Standards

Use shadcn/ui primitives for:

- buttons, inputs, labels, selects, checkboxes, switches, sliders, textareas
- dialogs, sheets, popovers, dropdown menus, tooltips
- tables, tabs, badges, separators, skeletons, toasts
- command palette and searchable selectors when buyer/listing lookup grows

Use lucide icons inside icon buttons whenever an icon exists. Add tooltips to unfamiliar icon-only actions.

## Feature Navigation

Initial sidebar entries:

- Buyers
- Bottle Listings
- Payment Runs
- Payment Links & Reminders
- Shipments
- Exceptions

Exceptions should aggregate payment reconciliation issues, missing shipping addresses, blocked packages, and failed render/retry states when the underlying feature exposes them.

## Responsive Rules

- Desktop: optimized for table and split-pane workflows.
- Tablet: preserve tables where possible, with sticky key columns when needed.
- Mobile: stack filters above content, convert dense tables to grouped rows, and keep copyable text previews full-width.
- Fixed-format elements such as slot grids, status chips, icon buttons, and counters must have stable dimensions to avoid layout shift.

## Conventions

### Naming

| Item            | Convention          | Example                             |
| --------------- | ------------------- | ----------------------------------- |
| Component files | PascalCase `.tsx`   | `BuyerTable.tsx`                    |
| Hook files      | camelCase `use*.ts` | `useBuyer.ts`                       |
| Utility files   | kebab-case `.ts`    | `query-keys.ts`                     |
| Page files      | Astro route files   | `payment-runs/[paymentRunId].astro` |
| CSS variables   | kebab-case          | `--sidebar-background`              |

### Imports

- Use `@/` as the internal source alias.
- Keep feature-specific UI under `components/<feature>/`.
- Keep cross-feature primitives under `components/ui/` or `components/layout/`.

### Do NOT

- Do not imply WhatsApp messages were sent when they were only rendered for copy/paste.
- Do not display payment truth from messaging or rendering caches.
- Do not hide blockers such as missing address, unpaid dose, or reconciliation exception behind generic errors.
- Do not use landing-page heroes, decorative gradients, or ornamental imagery for operational screens.
- Do not add freight calculation or freight payment UI in v1 shipment screens.

## Dependencies To Install During Frontend Scaffold

```bash
pnpm create astro@latest web --template minimal --typescript strict
pnpm --dir web add @astrojs/react react react-dom
pnpm --dir web add @tanstack/react-query react-hook-form zod lucide-react
pnpm --dir web add -D tailwindcss postcss autoprefixer
pnpm --dir web dlx shadcn@latest init
```

## Initial Components

```bash
pnpm --dir web dlx shadcn@latest add button input label textarea select checkbox switch badge table tabs dialog sheet popover dropdown-menu tooltip separator skeleton toast command
```

## Verification Baseline

When the frontend scaffold exists, minimum verification before feature progression:

- `pnpm --dir web build`
- `pnpm --dir web astro check`
- feature UI-SPEC checker result: no BLOCK findings

## Current Scaffold Status

No frontend application files exist yet. This constitution intentionally records the planned UI architecture for story and UI-SPEC generation. Scaffolding, dependency installation, route creation, Playwright tests, and visual audit remain outside the current story/UI-spec iteration.

_Last updated: 2026-05-21_
