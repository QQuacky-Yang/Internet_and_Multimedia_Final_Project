"""
platform_server/car_registry.py
Stores and manages car identities using SQLite.
"""

from typing import Dict, Optional

from platform_server.models import CarRegistration
from platform_server.storage import get_connection, init_db


def _row_to_dict(row) -> Optional[dict]:
    if row is None:
        return None

    return {
        "car_id": row["car_id"],
        "car_pubkey": row["car_pubkey"],
        "description": row["description"],
    }


def register_car(data: CarRegistration) -> dict:
    """
    Register a car with its public key.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO cars (
                car_id,
                car_pubkey,
                description
            )
            VALUES (?, ?, ?)
            """,
            (
                data.car_id,
                data.car_pubkey,
                data.description,
            ),
        )

        conn.commit()

    except Exception as e:
        conn.close()

        if "UNIQUE constraint failed" in str(e):
            raise ValueError(
                f"Car already exists: {data.car_id}"
            )

        raise

    conn.close()

    car = get_car(data.car_id)

    if car is None:
        raise RuntimeError("Car registration failed unexpectedly")

    return car


def get_car(car_id: str) -> Optional[dict]:
    """
    Return car record if found.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT car_id, car_pubkey, description
        FROM cars
        WHERE car_id = ?
        """,
        (car_id,),
    )

    row = cur.fetchone()
    conn.close()

    return _row_to_dict(row)


def car_exists(car_id: str) -> bool:
    """
    Check whether car exists.
    """

    return get_car(car_id) is not None


def list_cars() -> Dict[str, dict]:
    """
    Return all registered cars.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT car_id, car_pubkey, description
        FROM cars
        ORDER BY car_id
        """
    )

    rows = cur.fetchall()
    conn.close()

    return {
        row["car_id"]: _row_to_dict(row)
        for row in rows
    }


def clear_cars() -> None:
    """
    Clear car registry.

    Only for testing.
    """

    init_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM cars")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    clear_cars()

    test_car = CarRegistration(
        car_id="CAR_RPI5_001",
        car_pubkey="car-public-key-placeholder",
        description="RPi5 autonomous delivery car",
    )

    registered = register_car(test_car)
    print("Registered car:")
    print(registered)

    print("Car exists:", car_exists("CAR_RPI5_001"))
    print("Get car:", get_car("CAR_RPI5_001"))
    print("All cars:", list_cars())