# MVP Two-Lane Synthesis

Status: resolved
Dispatch ID: `ide-ergonomics-mvp-two-lane-20260619T172822Z`
Registry dispatch ID: `2026-06-19-ide-ergonomics-mvp-two-lane`

## Decision

Replace the current three-card MVP with a bounded conversation-transition card
MVP.

The current MVP should not be implemented as three first-class widgets yet. It
is better understood as source material for one smaller proof: can an IDE
recognize a conversation transition and show the right owner-safe route without
silently promoting knowledge or executing work?

## Why

Lane Z validated the strongest version of the current MVP, then found the
counterexample: a user may need route disambiguation or side-node capture, not
definition, handoff, or delegated fanout. That means the three-card MVP proves
safe previews for three attractive actions, but not the wider recognition and
routing problem.

Lane A independently found the same pressure from the other side. The strongest
alternative is a bounded route-menu MVP because it validates upstream recognition
before downstream composers. Side-node capture is the strongest secondary route
option.

## Selected MVP

Name: bounded conversation-transition card.

Core behavior:

1. Detect or accept a selected conversation span.
2. Classify it as a possible workflow transition.
3. Show a compact route menu with owner, boundary, and next artifact preview.
4. Let the user choose one route, park it, or ignore it.
5. Produce only draft/local artifacts unless a downstream owner route approves.

Minimum route menu:

- definition candidate;
- side node;
- handoff draft;
- route ambiguity menu;
- delegated run preview;
- park or ignore.

## First-Proof Boundary

- Definition and handoff routes may create draft candidate packets.
- Side-node capture may create a local side-note candidate.
- Route ambiguity may only display the route menu and selected owner.
- Delegated run remains preview-only and permission-gated.
- No canonical definition, ontology, spell, sigil, or runtime behavior is
  promoted by the MVP.

## Scoring

| Candidate | Value Signal | Proof Cost | Boundary Safety | Owner Clarity | Implementation Surface | Recomposition |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Current three-card MVP | 4 | 2-3 | 4 | 4 | 2 | 4-5 |
| Bounded route-menu / transition-card MVP | 5 | 4 | 5 | 5 | 4 | 5 |
| Side-node capture only | 4 | 5 | 5 | 5 | 5 | 4 |

## Next Route

Use Invoke to define/design the bounded conversation-transition card, then run
one Task Session to build a tiny toy proof over static conversation fixtures.

Do not route to Spellcraft yet. Spellcraft becomes appropriate after the toy
proof shows repeated route composition worth turning into a reusable spell.
