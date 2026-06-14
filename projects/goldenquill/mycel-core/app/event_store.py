import json
import sqlite3
import threading
from typing import List, Optional
from uuid import UUID

from app.schemas import EventEnvelope
from app.database import get_db_connection

class EventStore:
    def __init__(self, db_path: str = "mycel_audit.db"):
        self.db_path = db_path
        self._lock = threading.Lock()

    def append(self, event_envelope: EventEnvelope) -> EventEnvelope:
        with self._lock:
            conn = get_db_connection(self.db_path)
            # Use BEGIN IMMEDIATE to ensure exclusive write access
            conn.execute("BEGIN IMMEDIATE")
            try:
                cursor = conn.cursor()
                
                # 1. Check idempotency for session_id + idempotency_key
                if event_envelope.idempotency_key:
                    cursor.execute(
                        "SELECT event_id, session_id, seq, event_type, schema_version, ts, actor_kind, actor_id, controller_state_id, parent_event_id, correlation_id, idempotency_key, prev_hash, event_hash, payload FROM audit_events WHERE session_id = ? AND idempotency_key = ?",
                        (str(event_envelope.session_id), event_envelope.idempotency_key)
                    )
                    row = cursor.fetchone()
                    if row:
                        conn.execute("ROLLBACK")
                        return self._row_to_envelope(row)
                
                # 3. Read MAX(seq) for that session
                cursor.execute(
                    "SELECT MAX(seq) FROM audit_events WHERE session_id = ?",
                    (str(event_envelope.session_id),)
                )
                max_seq = cursor.fetchone()[0]
                
                # 4. Assign next seq
                next_seq = (max_seq or 0) + 1
                event_envelope.seq = next_seq
                
                # 6. Serialize with model_dump(mode="json")
                payload_json = json.dumps(event_envelope.payload)
                
                # 7. Insert
                cursor.execute(
                    """
                    INSERT INTO audit_events (
                        event_id, session_id, seq, event_type, schema_version, ts,
                        actor_kind, actor_id, controller_state_id, parent_event_id,
                        correlation_id, idempotency_key, prev_hash, event_hash, payload
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        str(event_envelope.event_id),
                        str(event_envelope.session_id),
                        event_envelope.seq,
                        event_envelope.event_type,
                        event_envelope.schema_version,
                        event_envelope.ts.isoformat(),
                        event_envelope.actor.kind,
                        event_envelope.actor.actor_id,
                        str(event_envelope.controller_state_id) if event_envelope.controller_state_id else None,
                        str(event_envelope.parent_event_id) if event_envelope.parent_event_id else None,
                        str(event_envelope.correlation_id) if event_envelope.correlation_id else None,
                        event_envelope.idempotency_key,
                        event_envelope.prev_hash,
                        event_envelope.event_hash,
                        payload_json
                    )
                )
                # 8. Commit
                conn.execute("COMMIT")
                return event_envelope
            except Exception as e:
                conn.execute("ROLLBACK")
                raise e
            finally:
                conn.close()

    def latest_seq(self, session_id: UUID) -> int:
        conn = get_db_connection(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT MAX(seq) FROM audit_events WHERE session_id = ?",
                (str(session_id),)
            )
            val = cursor.fetchone()[0]
            return val or 0
        finally:
            conn.close()

    def get_events(self, session_id: UUID, after_seq: int = 0) -> List[EventEnvelope]:
        conn = get_db_connection(self.db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT event_id, session_id, seq, event_type, schema_version, ts,
                       actor_kind, actor_id, controller_state_id, parent_event_id,
                       correlation_id, idempotency_key, prev_hash, event_hash, payload
                FROM audit_events
                WHERE session_id = ? AND seq > ?
                ORDER BY seq ASC
                """,
                (str(session_id), after_seq)
            )
            rows = cursor.fetchall()
            return [self._row_to_envelope(row) for row in rows]
        finally:
            conn.close()

    def _row_to_envelope(self, row) -> EventEnvelope:
        (
            event_id, session_id, seq, event_type, schema_version, ts,
            actor_kind, actor_id, controller_state_id, parent_event_id,
            correlation_id, idempotency_key, prev_hash, event_hash, payload
        ) = row

        return EventEnvelope(
            event_id=UUID(event_id),
            session_id=UUID(session_id),
            seq=seq,
            event_type=event_type,
            schema_version=schema_version,
            ts=ts,
            actor={"kind": actor_kind, "actor_id": actor_id},
            controller_state_id=UUID(controller_state_id) if controller_state_id else None,
            parent_event_id=UUID(parent_event_id) if parent_event_id else None,
            correlation_id=UUID(correlation_id) if correlation_id else None,
            idempotency_key=idempotency_key,
            prev_hash=prev_hash,
            event_hash=event_hash,
            payload=json.loads(payload)
        )
