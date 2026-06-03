"""
rpi5_car/manifest.py

Manifest helper functions.

The platform returns:

{
    "car_id": "...",
    "manifest": [...]
}

This file provides helper methods for working
with that manifest.
"""

from typing import Any, Dict, List, Optional


def get_manifest_entries(
    manifest_data: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Return manifest entries.
    """

    return manifest_data.get(
        "manifest",
        [],
    )


def find_delivery(
    manifest_data: Dict[str, Any],
    delivery_id: str,
) -> Optional[Dict[str, Any]]:
    """
    Find delivery by delivery_id.
    """

    for item in get_manifest_entries(
        manifest_data
    ):
        if (
            item.get("delivery_id")
            == delivery_id
        ):
            return item

    return None


def find_package(
    manifest_data: Dict[str, Any],
    package_id: str,
) -> Optional[Dict[str, Any]]:
    """
    Find package by package_id.
    """

    for item in get_manifest_entries(
        manifest_data
    ):
        if (
            item.get("package_id")
            == package_id
        ):
            return item

    return None


def list_pending_pickups(
    manifest_data: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Deliveries waiting for pickup.
    """

    return [
        item
        for item in get_manifest_entries(
            manifest_data
        )
        if item.get("status")
        == "PICKUP_PENDING"
    ]


def list_picked_up(
    manifest_data: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Packages already picked up.
    """

    return [
        item
        for item in get_manifest_entries(
            manifest_data
        )
        if item.get("status")
        == "PICKED_UP"
    ]


def list_delivered(
    manifest_data: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Packages already delivered.
    """

    return [
        item
        for item in get_manifest_entries(
            manifest_data
        )
        if item.get("status")
        == "DELIVERED"
    ]


if __name__ == "__main__":

    manifest = {
        "car_id": "CAR_RPI5_001",
        "manifest": [
            {
                "delivery_id": "DELIVERY_001",
                "package_id": "PKG_001",
                "status": "PICKUP_PENDING",
            },
            {
                "delivery_id": "DELIVERY_002",
                "package_id": "PKG_002",
                "status": "PICKED_UP",
            },
            {
                "delivery_id": "DELIVERY_003",
                "package_id": "PKG_003",
                "status": "DELIVERED",
            },
        ],
    }

    print(
        find_delivery(
            manifest,
            "DELIVERY_001",
        )
    )

    print(
        find_package(
            manifest,
            "PKG_002",
        )
    )

    print(
        list_pending_pickups(
            manifest
        )
    )

    print(
        list_picked_up(
            manifest
        )
    )

    print(
        list_delivered(
            manifest
        )
    )
