"""
rpi5_car/platform_api.py

HTTP client for the RPi5 car to communicate with the platform server.

Responsibilities:
- fetch car manifest
- fetch platform public key
- check VC revocation
- report pickup/delivery results
"""

from typing import Any, Dict

import requests

from common.config import SERVER_URL


def get_platform_public_key() -> str:
    response = requests.get(
        f"{SERVER_URL}/platform_public_key",
        timeout=5,
    )
    response.raise_for_status()

    return response.json()["platform_public_key"]


def get_manifest(car_id: str) -> Dict[str, Any]:
    response = requests.get(
        f"{SERVER_URL}/manifest/{car_id}",
        timeout=5,
    )
    response.raise_for_status()

    return response.json()


def get_delivery(delivery_id: str) -> Dict[str, Any]:
    response = requests.get(
        f"{SERVER_URL}/delivery/{delivery_id}",
        timeout=5,
    )
    response.raise_for_status()

    return response.json()


def check_revocation(vc_id: str) -> Dict[str, Any]:
    response = requests.get(
        f"{SERVER_URL}/revocation/{vc_id}",
        timeout=5,
    )
    response.raise_for_status()

    return response.json()


def report_delivery_result(
    delivery_id: str,
    car_id: str,
    status: str,
    detail: str | None = None,
) -> Dict[str, Any]:
    payload = {
        "delivery_id": delivery_id,
        "car_id": car_id,
        "status": status,
        "detail": detail,
    }

    response = requests.post(
        f"{SERVER_URL}/delivery_result",
        json=payload,
        timeout=5,
    )
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    test_car_id = "CAR_RPI5_001"

    print("Platform public key:")
    print(get_platform_public_key())

    print("Manifest:")
    print(get_manifest(test_car_id))
