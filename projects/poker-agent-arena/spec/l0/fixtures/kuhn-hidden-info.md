# Kuhn Hidden-Information Fixture

Status: frozen for MVP implementation

Kuhn is the first fixture gate. It uses a three-card deck: `J`, `Q`, `K`.
Each player antes one chip and receives one private card. Betting allows one
single-chip bet.

## Legal Sequences

- `check`, `check`: showdown, pot 2.
- `check`, `bet`, `fold`: bettor wins, pot 3.
- `check`, `bet`, `call`: showdown, pot 4.
- `bet`, `fold`: bettor wins, pot 3.
- `bet`, `call`: showdown, pot 4.

The fixture must prove that the acting agent sees only its own card and public
betting history.
