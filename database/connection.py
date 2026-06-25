from __future__ import annotations

import sqlite3

from app.settings import settings


def get_connection() -> sqlite3.Connection:
    """
    Return a SQLite connection.

    Foreign keys are enabled by default.
    """

    conn = sqlite3.connect(settings.database_path)

    conn.execute("PRAGMA foreign_keys = ON;")

    conn.row_factory = sqlite3.Row

    return conn