"""
platform_server/revocation.py
Persistent VC revocation list using SQLite.
"""

from typing import Dict, Optional

from platform_server.models import RevocationStatus
from platform_server.storage import get_connection, init_db


def revoke_vc(
    vc_id: str,
    reason: Optional[str] = None,
) -> RevocationStatus:
    """
    Revoke a VC by its credential ID.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO revoked_vcs (
            vc_id,
            reason
        )
        VALUES (?, ?)
        """,
        (
            vc_id,
            reason,
        ),
    )

    conn.commit()
    conn.close()

    return RevocationStatus(
        vc_id=vc_id,
        revoked=True,
        reason=reason,
    )


def is_revoked(vc_id: str) -> bool:
    """
    Check whether a VC is revoked.
    """

    return get_revocation_status(vc_id).revoked


def get_revocation_status(vc_id: str) -> RevocationStatus:
    """
    Return revocation status for a VC.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT vc_id, reason
        FROM revoked_vcs
        WHERE vc_id = ?
        """,
        (vc_id,),
    )

    row = cur.fetchone()
    conn.close()

    if row is None:
        return RevocationStatus(
            vc_id=vc_id,
            revoked=False,
            reason=None,
        )

    return RevocationStatus(
        vc_id=row["vc_id"],
        revoked=True,
        reason=row["reason"],
    )


def list_revoked_vcs() -> Dict[str, dict]:
    """
    Return all revoked VCs.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT vc_id, reason
        FROM revoked_vcs
        ORDER BY vc_id
        """
    )

    rows = cur.fetchall()
    conn.close()

    return {
        row["vc_id"]: {
            "vc_id": row["vc_id"],
            "reason": row["reason"],
        }
        for row in rows
    }


def clear_revocations() -> None:
    """
    Clear all revocations.

    Testing only.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM revoked_vcs")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    clear_revocations()

    test_vc_id = "urn:uuid:test-vc-001"

    print("Before revoke:")
    print(get_revocation_status(test_vc_id))

    revoke_vc(
        test_vc_id,
        reason="Package cancelled",
    )

    print("After revoke:")
    print(get_revocation_status(test_vc_id))

    print("Is revoked:")
    print(is_revoked(test_vc_id))

    print("All revoked:")
    print(list_revoked_vcs())