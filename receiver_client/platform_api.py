"""
receiver_client/platform_api.py

HTTP client for receiver to communicate with platform server.
"""

from typing import Any, Dict

import requests

from common.config import SERVER_URL


def register_receiver(
    receiver_id: str,
    receiver_pubkey: str,
    display_name: str | None = None,
) -> Dict[str, Any]:
    payload = {
        "receiver_id": receiver_id,
        "receiver_pubkey": receiver_pubkey,
        "display_name": display_name,
    }

    response = requests.post(
        f"{SERVER_URL}/register_receiver",
        json=payload,
        timeout=5,
    )
    response.raise_for_status()

    return response.json()


def get_receiver_delivery_vc(
    delivery_id: str,
) -> Dict[str, Any]:
    response = requests.get(
        f"{SERVER_URL}/vc/receiver/{delivery_id}",
        timeout=5,
    )
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    print(
        get_receiver_delivery_vc(
            "DELIVERY_001"
        )
    )