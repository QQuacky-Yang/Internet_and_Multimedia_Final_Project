"""
platform_server/sender_registry.py
Stores and manages sender identities using SQLite.
"""

from typing import Dict, Optional

from platform_server.models import SenderRegistration
from platform_server.storage import get_connection, init_db


def _row_to_dict(row) -> Optional[dict]:
    if row is None:
        return None

    return {
        "sender_id": row["sender_id"],
        "sender_pubkey": row["sender_pubkey"],
        "display_name": row["display_name"],
    }


def register_sender(data: SenderRegistration) -> dict:
    """
    Register a sender with their public key.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO senders (
                sender_id,
                sender_pubkey,
                display_name
            )
            VALUES (?, ?, ?)
            """,
            (
                data.sender_id,
                data.sender_pubkey,
                data.display_name,
            ),
        )

        conn.commit()

    except Exception as e:
        conn.close()

        if "UNIQUE constraint failed" in str(e):
            raise ValueError(
                f"Sender already exists: {data.sender_id}"
            )

        raise

    conn.close()

    sender = get_sender(data.sender_id)

    if sender is None:
        raise RuntimeError("Sender registration failed unexpectedly")

    return sender


def get_sender(sender_id: str) -> Optional[dict]:
    """
    Return sender record if found.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT sender_id, sender_pubkey, display_name
        FROM senders
        WHERE sender_id = ?
        """,
        (sender_id,),
    )

    row = cur.fetchone()
    conn.close()

    return _row_to_dict(row)


def sender_exists(sender_id: str) -> bool:
    """
    Check whether sender exists.
    """

    return get_sender(sender_id) is not None


def list_senders() -> Dict[str, dict]:
    """
    Return all registered senders.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT sender_id, sender_pubkey, display_name
        FROM senders
        ORDER BY sender_id
        """
    )

    rows = cur.fetchall()
    conn.close()

    return {
        row["sender_id"]: _row_to_dict(row)
        for row in rows
    }


def clear_senders() -> None:
    """
    Clear sender registry.

    Only for testing.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM senders")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    clear_senders()

    test_sender = SenderRegistration(
        sender_id="sender_001",
        sender_pubkey="sender-public-key-placeholder",
        display_name="Alice Seller",
    )

    registered = register_sender(test_sender)
    print("Registered sender:")
    print(registered)

    print("Sender exists:", sender_exists("sender_001"))
    print("Get sender:", get_sender("sender_001"))
    print("All senders:", list_senders())