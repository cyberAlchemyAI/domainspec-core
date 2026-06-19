---
fixture_id: revise-baseline
class: medium
target: operating SKILL behavior contract
---

# Fixture — revise an approved baseline

## Starting state

A session exists with a committed baseline (variant B) and a registered revision head. The human wants
two changes to a card component.

## Human request (verbatim)

> "Make the primary button say 'Continue' instead of 'Go', and make the card title a bit bigger. Then
> I'll review it."

## Starting session facts

- `session open` done; baseline committed (B); head = rev-1.
- Components carry `data-od-id` (`cta.primary`, `card.title`, `card.root`).

## What the agent is expected to do (and not do)

Drive reversible steps; **stop at every durable gate**; let the human dispose. See `.expected.md`.
