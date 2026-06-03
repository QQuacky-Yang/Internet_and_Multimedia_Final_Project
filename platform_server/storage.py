"""
platform_server/storage.py

SQLite persistent storage for platform server.
"""

import sqlite3
from pathlib import Path


DB_PATH = Path("data/platform/db/platform.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS senders (
        sender_id TEXT PRIMARY KEY,
        sender_pubkey TEXT NOT NULL,
        display_name TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS receivers (
        receiver_id TEXT PRIMARY KEY,
        receiver_pubkey TEXT NOT NULL,
        display_name TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        car_id TEXT PRIMARY KEY,
        car_pubkey TEXT NOT NULL,
        description TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS deliveries (
        delivery_id TEXT PRIMARY KEY,
        sender_id TEXT NOT NULL,
        receiver_id TEXT NOT NULL,
        package_id TEXT NOT NULL,
        car_id TEXT NOT NULL,
        status TEXT NOT NULL,
        sender_pickup_vc TEXT,
        receiver_delivery_vc TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS revoked_vcs (
        vc_id TEXT PRIMARY KEY,
        reason TEXT
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
