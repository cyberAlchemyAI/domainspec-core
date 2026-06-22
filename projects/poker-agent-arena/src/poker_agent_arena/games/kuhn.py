from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any

from poker_agent_arena.constants import FIXTURE_ID, PROTOCOL_VERSION

CARDS = ("J", "Q", "K")
CARD_RANK = {"J": 0, "Q": 1, "K": 2}


@dataclass
class KuhnGame:
    match_id: str
    hand_id: str
    seed_handle: str
    raw_seed: str
    cards: dict[str, str] | None = None
    history: list[str] = field(default_factory=list)
    contributions: dict[str, int] = field(default_factory=lambda: {"seat_0": 1, "seat_1": 1})
    terminal: bool = False

    def __post_init__(self) -> None:
        if self.cards is None:
            deck = list(CARDS)
            random.Random(self.raw_seed).shuffle(deck)
            self.cards = {"seat_0": deck[0], "seat_1": deck[1]}

    @property
    def pot(self) -> int:
        return sum(self.contributions.values())

    def to_act(self) -> str | None:
        if self.terminal:
            return None
        if self.history == []:
            return "seat_0"
        if self.history == ["check"]:
            return "seat_1"
        if self.history == ["bet"]:
            return "seat_1"
        if self.history == ["check", "bet"]:
            return "seat_0"
        return None

    def legal_actions(self) -> list[dict[str, Any]]:
        if self.terminal:
            return []
        if self.history in ([], ["check"]):
            return [{"type": "check"}, {"type": "bet", "min_amount": 1, "max_amount": 1}]
        if self.history in (["bet"], ["check", "bet"]):
            return [{"type": "call"}, {"type": "fold"}]
        return []

    def decision_envelope(self, decision_index: int, deadline_ms: int) -> dict[str, Any]:
        seat = self.to_act()
        if seat is None:
            raise RuntimeError("cannot build decision envelope for terminal hand")
        decision_id = f"{self.hand_id}:d{decision_index}:s{seat[-1]}"
        return {
            "protocol_version": PROTOCOL_VERSION,
            "type": "decision",
            "match_id": self.match_id,
            "hand_id": self.hand_id,
            "decision_id": decision_id,
            "seat_id": seat,
            "deadline_ms": deadline_ms,
            "observation": {
                "fixture_id": FIXTURE_ID,
                "seat_id": seat,
                "own_card": self.cards[seat],
                "public_state": {
                    "pot": self.pot,
                    "betting_history": list(self.history),
                    "to_act": seat,
                    "contributions": dict(self.contributions),
                },
            },
            "legal_actions": self.legal_actions(),
        }

    def apply(self, action: dict[str, Any]) -> None:
        action_type = action["type"]
        actor = self.to_act()
        if actor is None:
            raise RuntimeError("terminal hand cannot accept actions")
        if action_type in {"bet", "call"}:
            self.contributions[actor] += 1
        self.history.append(action_type)
        if self.history in (
            ["check", "check"],
            ["bet", "call"],
            ["bet", "fold"],
            ["check", "bet", "call"],
            ["check", "bet", "fold"],
        ):
            self.terminal = True

    def result(self) -> dict[str, Any]:
        if not self.terminal:
            raise RuntimeError("cannot score non-terminal hand")
        folded = self.history[-1] == "fold"
        if folded:
            folder = "seat_1" if self.history == ["bet", "fold"] else "seat_0"
            winner = other_seat(folder)
            revealed_cards = {winner: self.cards[winner]}
        else:
            winner = max(("seat_0", "seat_1"), key=lambda seat: CARD_RANK[self.cards[seat]])
            revealed_cards = dict(self.cards)
        payouts = {}
        for seat in ("seat_0", "seat_1"):
            payouts[seat] = self.pot - self.contributions[seat] if seat == winner else -self.contributions[seat]
        return {
            "winner": winner,
            "payouts": payouts,
            "showdown": not folded,
            "revealed_cards": revealed_cards,
            "final_history": list(self.history),
            "pot": self.pot,
        }


def other_seat(seat: str) -> str:
    return "seat_1" if seat == "seat_0" else "seat_0"


def normalize_action(payload: Any) -> dict[str, Any]:
    if isinstance(payload, str):
        return {"type": payload}
    if isinstance(payload, dict):
        if "type" in payload:
            return dict(payload)
        if "action" in payload and isinstance(payload["action"], str):
            return {"type": payload["action"]}
    return {"type": "__invalid__"}
