"""
platform_server/receiver_registry.py

Stores and manages receiver identities using SQLite.
"""

from typing import Dict, Optional

from platform_server.models import ReceiverRegistration
from platform_server.storage import get_connection, init_db


def _row_to_dict(row) -> Optional[dict]:
    if row is None:
        return None

    return {
        "receiver_id": row["receiver_id"],
        "receiver_pubkey": row["receiver_pubkey"],
        "display_name": row["display_name"],
    }


def register_receiver(data: ReceiverRegistration) -> dict:
    """
    Register a receiver with their public key.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO receivers (
                receiver_id,
                receiver_pubkey,
                display_name
            )
            VALUES (?, ?, ?)
            """,
            (
                data.receiver_id,
                data.receiver_pubkey,
                data.display_name,
            ),
        )

        conn.commit()

    except Exception as e:
        conn.close()

        if "UNIQUE constraint failed" in str(e):
            raise ValueError(
                f"Receiver already exists: {data.receiver_id}"
            )

        raise

    conn.close()

    receiver = get_receiver(data.receiver_id)

    if receiver is None:
        raise RuntimeError("Receiver registration failed unexpectedly")

    return receiver


def get_receiver(receiver_id: str) -> Optional[dict]:
    """
    Return receiver record if found.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT receiver_id, receiver_pubkey, display_name
        FROM receivers
        WHERE receiver_id = ?
        """,
        (receiver_id,),
    )

    row = cur.fetchone()
    conn.close()

    return _row_to_dict(row)


def receiver_exists(receiver_id: str) -> bool:
    """
    Check whether receiver exists.
    """

    return get_receiver(receiver_id) is not None


def list_receivers() -> Dict[str, dict]:
    """
    Return all registered receivers.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT receiver_id, receiver_pubkey, display_name
        FROM receivers
        ORDER BY receiver_id
        """
    )

    rows = cur.fetchall()
    conn.close()

    return {
        row["receiver_id"]: _row_to_dict(row)
        for row in rows
    }


def clear_receivers() -> None:
    """
    Clear receiver registry.

    Only for testing.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM receivers")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    clear_receivers()

    test_receiver = ReceiverRegistration(
        receiver_id="receiver_001",
        receiver_pubkey="receiver-public-key-placeholder",
        display_name="Bob Receiver",
    )

    registered = register_receiver(test_receiver)
    print("Registered receiver:")
    print(registered)

    print("Receiver exists:", receiver_exists("receiver_001"))
    print("Get receiver:", get_receiver("receiver_001"))
    print("All receivers:", list_receivers())