import sqlite3
import os
from typing import Optional

def get_db_connection(db_path: str = "mycel_audit.db") -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.execute("PRAGMA busy_timeout=5000;")
    return conn

def init_db(db_path: str = "mycel_audit.db"):
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_events (
            event_id            TEXT PRIMARY KEY,
            session_id          TEXT NOT NULL,
            seq                 INTEGER NOT NULL,
            event_type          TEXT NOT NULL,
            schema_version      TEXT NOT NULL,
            ts                  TEXT NOT NULL,
            actor_kind          TEXT NOT NULL,
            actor_id            TEXT NOT NULL,
            controller_state_id TEXT,
            parent_event_id     TEXT,
            correlation_id      TEXT,
            idempotency_key     TEXT,
            prev_hash           TEXT,
            event_hash          TEXT,
            payload             TEXT NOT NULL,
            UNIQUE(session_id, seq)
        );
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS ix_events_session_seq ON audit_events(session_id, seq);
    """)
    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS ux_events_idem
        ON audit_events(session_id, idempotency_key)
        WHERE idempotency_key IS NOT NULL;
    """)
    conn.close()
