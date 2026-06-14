import os
import pytest
from app.database import init_db, get_db_connection

@pytest.fixture(scope="session", autouse=True)
def init_database():
    init_db("mycel_audit.db")

@pytest.fixture(autouse=True)
def clear_db():
    conn = get_db_connection("mycel_audit.db")
    conn.execute("DELETE FROM audit_events;")
    conn.commit()
    conn.close()
