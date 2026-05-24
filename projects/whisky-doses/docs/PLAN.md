# Story And UI-Spec Iteration Plan

## Purpose

Turn the current DomainSpec feature packages into reviewable user stories and UI design contracts without implementing frontend pages, tests, backend code, or visual audits yet.

This pass produces:

- `docs/UI-ARCHITECTURE.md`
- `docs/features/<feature>/STORIES.md`
- `docs/features/<feature>/UI-SPEC.md`

## Feature Order

Run the iteration in dependency order:

1. `buyer-registry`
2. `bottle-listing-and-dose-allocation`
3. `dose-payment-tracking`
4. `payment-link-and-reminder-messaging`
5. `freight-and-shipment-batching`

## Execution Checklist

### 0. UI Architecture Prerequisite

- [x] Run `domainspec-ui-architecture`.
- [x] Confirm `docs/UI-ARCHITECTURE.md` exists.
- [x] Record any unresolved UI architecture decisions in this plan before generating per-feature UI specs.

### 1. Buyer Registry

- [x] Run `domainspec-sync-user-stories buyer-registry`.
- [x] Confirm `docs/features/buyer-registry/STORIES.md` exists.
- [x] Confirm `docs/features/buyer-registry/SPEC.md` links to `STORIES.md`.
- [x] Confirm story coverage includes public, admin/operations, cross-feature, and edge-case journeys.
- [x] Resolve or record unmapped concepts and drift warnings.
- [x] Run `domainspec-ui-phase-bridge buyer-registry`.
- [x] Confirm `docs/features/buyer-registry/UI-SPEC.md` exists.
- [x] Confirm UI-SPEC is constrained by `docs/UI-ARCHITECTURE.md`.
- [x] Confirm UI-SPEC maps user actions, queries, states, and key workflows.
- [x] Record any UI checker BLOCK or FLAG findings before moving on.

### 2. Bottle Listing And Dose Allocation

- [x] Run `domainspec-sync-user-stories bottle-listing-and-dose-allocation`.
- [x] Confirm `docs/features/bottle-listing-and-dose-allocation/STORIES.md` exists.
- [x] Confirm `docs/features/bottle-listing-and-dose-allocation/SPEC.md` links to `STORIES.md`.
- [x] Confirm story coverage includes public, admin/operations, cross-feature, and edge-case journeys.
- [x] Resolve or record unmapped concepts and drift warnings.
- [x] Run `domainspec-ui-phase-bridge bottle-listing-and-dose-allocation`.
- [x] Confirm `docs/features/bottle-listing-and-dose-allocation/UI-SPEC.md` exists.
- [x] Confirm UI-SPEC is constrained by `docs/UI-ARCHITECTURE.md`.
- [x] Confirm UI-SPEC maps user actions, queries, states, and key workflows.
- [x] Record any UI checker BLOCK or FLAG findings before moving on.

### 3. Dose Payment Tracking

- [x] Run `domainspec-sync-user-stories dose-payment-tracking`.
- [x] Confirm `docs/features/dose-payment-tracking/STORIES.md` exists.
- [x] Confirm `docs/features/dose-payment-tracking/SPEC.md` links to `STORIES.md`.
- [x] Confirm story coverage includes public, admin/operations, cross-feature, and edge-case journeys.
- [x] Resolve or record unmapped concepts and drift warnings.
- [x] Run `domainspec-ui-phase-bridge dose-payment-tracking`.
- [x] Confirm `docs/features/dose-payment-tracking/UI-SPEC.md` exists.
- [x] Confirm UI-SPEC is constrained by `docs/UI-ARCHITECTURE.md`.
- [x] Confirm UI-SPEC maps user actions, queries, states, and key workflows.
- [x] Record any UI checker BLOCK or FLAG findings before moving on.

### 4. Payment Link And Reminder Messaging

- [x] Run `domainspec-sync-user-stories payment-link-and-reminder-messaging`.
- [x] Confirm `docs/features/payment-link-and-reminder-messaging/STORIES.md` exists.
- [x] Confirm `docs/features/payment-link-and-reminder-messaging/SPEC.md` links to `STORIES.md`.
- [x] Confirm story coverage includes public, admin/operations, cross-feature, and edge-case journeys.
- [x] Resolve or record unmapped concepts and drift warnings.
- [x] Run `domainspec-ui-phase-bridge payment-link-and-reminder-messaging`.
- [x] Confirm `docs/features/payment-link-and-reminder-messaging/UI-SPEC.md` exists.
- [x] Confirm UI-SPEC is constrained by `docs/UI-ARCHITECTURE.md`.
- [x] Confirm UI-SPEC maps user actions, queries, states, and key workflows.
- [x] Record any UI checker BLOCK or FLAG findings before moving on.

### 5. Freight And Shipment Batching

- [x] Run `domainspec-sync-user-stories freight-and-shipment-batching`.
- [x] Confirm `docs/features/freight-and-shipment-batching/STORIES.md` exists.
- [x] Confirm `docs/features/freight-and-shipment-batching/SPEC.md` links to `STORIES.md`.
- [x] Confirm story coverage includes public, admin/operations, cross-feature, and edge-case journeys.
- [x] Resolve or record unmapped concepts and drift warnings.
- [x] Run `domainspec-ui-phase-bridge freight-and-shipment-batching`.
- [x] Confirm `docs/features/freight-and-shipment-batching/UI-SPEC.md` exists.
- [x] Confirm UI-SPEC is constrained by `docs/UI-ARCHITECTURE.md`.
- [x] Confirm UI-SPEC maps user actions, queries, states, and key workflows.
- [x] Record any UI checker BLOCK or FLAG findings before moving on.

## Final Validation

- [x] Confirm every target feature has `STORIES.md`.
- [x] Confirm every target feature has `UI-SPEC.md`.
- [x] Confirm every target feature `SPEC.md` links to `STORIES.md`.
- [x] Confirm no UI checker BLOCK findings remain unresolved.
- [x] Confirm unresolved questions are recorded in the section below.

## Unresolved Questions And Findings

Use this section while executing the checklist.

| Feature         | Type     | Question Or Finding                                                                                                                                                                                                                                              | Status   |
| --------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| UI Architecture | Decision | Created `docs/UI-ARCHITECTURE.md` using DomainSpec base TypeScript defaults: Astro, React, Tailwind, shadcn/ui, lucide-react, TanStack Query, React Hook Form, and Zod. No frontend scaffold was installed because this iteration stops at stories and UI specs. | recorded |

## Explicit Non-Scope

This iteration does not:

- implement frontend pages or components
- generate Playwright tests
- run visual audits
- implement backend code
- create migrations
- add WhatsApp posting automation

Those steps should happen after the stories and UI-SPECs are reviewed.
