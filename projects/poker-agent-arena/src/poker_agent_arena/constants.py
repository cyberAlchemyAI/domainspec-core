from pathlib import Path

PROTOCOL_VERSION = "paa.l0.v1"
FIXTURE_ID = "kuhn_hidden_info"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DECISION_TIMEOUT_MS = 5000
DEFAULT_PROCESS_KILL_AFTER_MS = 10000
FALLBACK_ORDER = ("check", "fold", "call", "bet")
FORBIDDEN_PUBLIC_FIELDS = {
    "raw_seed",
    "deck_order",
    "opponent_card",
    "future_state",
    "referee_trace",
    "hidden_state_hash",
}
