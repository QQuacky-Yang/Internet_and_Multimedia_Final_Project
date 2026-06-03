"""
platform_server/delivery_db.py
Persistent delivery database using SQLite.
"""

import json
from typing import Dict, Optional
from platform_server.models import DeliveryRecord
from platform_server.storage import get_connection, init_db


def _dict_to_json(data: Optional[dict]) -> Optional[str]:
    if data is None:
        return None

    return json.dumps(
        data,
        ensure_ascii=False,
        sort_keys=True,
    )


def _json_to_dict(data: Optional[str]) -> Optional[dict]:
    if data is None:
        return None

    return json.loads(data)


def _row_to_delivery(row) -> Optional[DeliveryRecord]:
    if row is None:
        return None

    return DeliveryRecord(
        delivery_id=row["delivery_id"],
        sender_id=row["sender_id"],
        receiver_id=row["receiver_id"],
        package_id=row["package_id"],
        car_id=row["car_id"],
        status=row["status"],
        sender_pickup_vc=_json_to_dict(row["sender_pickup_vc"]),
        receiver_delivery_vc=_json_to_dict(row["receiver_delivery_vc"]),
    )


def create_delivery(record: DeliveryRecord) -> DeliveryRecord:
    """
    Store a new delivery.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO deliveries (
                delivery_id,
                sender_id,
                receiver_id,
                package_id,
                car_id,
                status,
                sender_pickup_vc,
                receiver_delivery_vc
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.delivery_id,
                record.sender_id,
                record.receiver_id,
                record.package_id,
                record.car_id,
                record.status,
                _dict_to_json(record.sender_pickup_vc),
                _dict_to_json(record.receiver_delivery_vc),
            ),
        )

        conn.commit()

    except Exception as e:
        conn.close()

        if "UNIQUE constraint failed" in str(e):
            raise ValueError(
                f"Delivery already exists: {record.delivery_id}"
            )

        raise

    conn.close()

    delivery = get_delivery(record.delivery_id)

    if delivery is None:
        raise RuntimeError("Delivery creation failed unexpectedly")

    return delivery


def get_delivery(delivery_id: str) -> Optional[DeliveryRecord]:
    """
    Get delivery by ID.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            delivery_id,
            sender_id,
            receiver_id,
            package_id,
            car_id,
            status,
            sender_pickup_vc,
            receiver_delivery_vc
        FROM deliveries
        WHERE delivery_id = ?
        """,
        (delivery_id,),
    )

    row = cur.fetchone()
    conn.close()

    return _row_to_delivery(row)


def delivery_exists(delivery_id: str) -> bool:
    """
    Check whether delivery exists.
    """

    return get_delivery(delivery_id) is not None


def update_delivery_status(
    delivery_id: str,
    status: str,
) -> DeliveryRecord:
    """
    Update delivery status.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE deliveries
        SET status = ?
        WHERE delivery_id = ?
        """,
        (
            status,
            delivery_id,
        ),
    )

    conn.commit()
    changed = cur.rowcount
    conn.close()

    if changed == 0:
        raise ValueError(f"Delivery not found: {delivery_id}")

    delivery = get_delivery(delivery_id)

    if delivery is None:
        raise RuntimeError("Delivery status update failed unexpectedly")

    return delivery


def attach_sender_pickup_vc(
    delivery_id: str,
    vc: dict,
) -> DeliveryRecord:
    """
    Attach sender pickup VC to a delivery.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE deliveries
        SET sender_pickup_vc = ?
        WHERE delivery_id = ?
        """,
        (
            _dict_to_json(vc),
            delivery_id,
        ),
    )

    conn.commit()
    changed = cur.rowcount
    conn.close()

    if changed == 0:
        raise ValueError(f"Delivery not found: {delivery_id}")

    delivery = get_delivery(delivery_id)

    if delivery is None:
        raise RuntimeError("Sender VC attachment failed unexpectedly")

    return delivery


def attach_receiver_delivery_vc(
    delivery_id: str,
    vc: dict,
) -> DeliveryRecord:
    """
    Attach receiver delivery VC to a delivery.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE deliveries
        SET receiver_delivery_vc = ?
        WHERE delivery_id = ?
        """,
        (
            _dict_to_json(vc),
            delivery_id,
        ),
    )

    conn.commit()
    changed = cur.rowcount
    conn.close()

    if changed == 0:
        raise ValueError(f"Delivery not found: {delivery_id}")

    delivery = get_delivery(delivery_id)

    if delivery is None:
        raise RuntimeError("Receiver VC attachment failed unexpectedly")

    return delivery


def list_deliveries() -> Dict[str, DeliveryRecord]:
    """
    Return all deliveries.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            delivery_id,
            sender_id,
            receiver_id,
            package_id,
            car_id,
            status,
            sender_pickup_vc,
            receiver_delivery_vc
        FROM deliveries
        ORDER BY delivery_id
        """
    )

    rows = cur.fetchall()
    conn.close()

    return {
        row["delivery_id"]: _row_to_delivery(row)
        for row in rows
    }


def clear_deliveries() -> None:
    """
    Clear all deliveries.

    Testing only.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM deliveries")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    clear_deliveries()

    test_delivery = DeliveryRecord(
        delivery_id="DELIVERY_001",
        sender_id="sender_001",
        receiver_id="receiver_001",
        package_id="PKG_001",
        car_id="CAR_RPI5_001",
        status="CREATED",
    )

    created = create_delivery(test_delivery)

    print("Created:")
    print(created)

    updated = update_delivery_status(
        "DELIVERY_001",
        "PICKUP_PENDING",
    )

    print("Updated:")
    print(updated)

    attach_sender_pickup_vc(
        "DELIVERY_001",
        {"example": "sender pickup vc"},
    )

    attach_receiver_delivery_vc(
        "DELIVERY_001",
        {"example": "receiver delivery vc"},
    )

    print("Final:")
    print(get_delivery("DELIVERY_001"))