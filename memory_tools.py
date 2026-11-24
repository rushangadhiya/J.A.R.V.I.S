import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "jarvis_memory.db"


def initialize_memory():
    """Create the memory database if it doesn't exist."""
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_memory(key: str, value: str):
    """Save or update a fact in long-term memory."""
    key = key.strip().lower()
    value = value.strip()

    if not key or not value:
        return {"success": False, "error": "Empty memory"}

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            INSERT INTO memories (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                updated_at = CURRENT_TIMESTAMP
        """, (key, value))

    return {
        "success": True,
        "saved": {key: value}
    }


def recall_memory(key: str):
    """Retrieve a saved fact by its key."""
    key = key.strip().lower()

    with sqlite3.connect(DB_PATH) as connection:
        result = connection.execute(
            "SELECT value FROM memories WHERE key = ?",
            (key,)
        ).fetchone()

    if result is None:
        return {"found": False, "key": key}

    return {
        "found": True,
        "key": key,
        "value": result[0]
    }


def list_memories():
    """List all saved facts."""
    with sqlite3.connect(DB_PATH) as connection:
        rows = connection.execute(
            "SELECT key, value FROM memories ORDER BY key"
        ).fetchall()

    return {
        "memories": [
            {"key": key, "value": value}
            for key, value in rows
        ]
    }


def delete_memory(key: str):
    """Delete a saved fact."""
    key = key.strip().lower()

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            "DELETE FROM memories WHERE key = ?",
            (key,)
        )

    return {
        "success": cursor.rowcount > 0,
        "key": key
    }
